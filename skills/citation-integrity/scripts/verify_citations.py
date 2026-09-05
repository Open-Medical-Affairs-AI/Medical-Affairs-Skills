#!/usr/bin/env python3
"""Resolve and verify citations against PubMed, CrossRef, and OpenAlex.

A citation that has not been resolved against an external source is an
assertion. Language models produce plausible, correctly-formatted references to
papers that do not exist, and attach real identifiers to the wrong papers. Both
failures are invisible on inspection and obvious on resolution.

Run this over a reference list BEFORE the deliverable goes anywhere.

    # Verify identifiers directly
    python3 verify_citations.py --pmids 36001231,35660948
    python3 verify_citations.py --dois 10.1056/NEJMoa2203478

    # Pull every PMID/DOI/NCT out of a draft and check them all
    python3 verify_citations.py --file draft.md

    # Emit AMA-formatted references for the ones that resolved
    python3 verify_citations.py --file draft.md --format ama

    # Offline, against recorded fixtures (used by the test suite)
    python3 verify_citations.py --pmids 36001231 --fixtures ../../../shared/fixtures

Exit codes: 0 = everything resolved and nothing retracted, 1 = at least one
identifier failed to resolve or is retracted, 2 = usage error.

No API key is required. Set NCBI_API_KEY to raise the NCBI rate limit from 3 to
10 requests/second; this script stays well under either.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
CROSSREF = "https://api.crossref.org/works"
OPENALEX = "https://api.openalex.org/works"

# NCBI asks that tools identify themselves. Being a good API citizen is also
# what keeps this working for everyone else using the library.
TOOL = "medical-affairs-skills"
CONTACT = os.environ.get("API_CONTACT_EMAIL", "")

PMID_RE = re.compile(r"\bPMID:?\s*(\d{1,8})\b|pubmed\.ncbi\.nlm\.nih\.gov/(\d{1,8})", re.I)
BARE_PMID_RE = re.compile(r"\b(\d{8})\b")
DOI_RE = re.compile(r"\b(10\.\d{4,9}/[-._;()/:A-Z0-9]+)", re.I)
NCT_RE = re.compile(r"\b(NCT\d{8})\b", re.I)

# PubMed publication types that mean "do not cite this as evidence".
RETRACTION_TYPES = {
    "Retracted Publication",
    "Retraction of Publication",
    "Expression of Concern",
}


@dataclass
class Record:
    identifier: str
    kind: str  # pmid | doi | nct
    resolved: bool = False
    source: str = ""
    title: str = ""
    authors: list[str] = field(default_factory=list)
    journal: str = ""
    year: str = ""
    volume: str = ""
    issue: str = ""
    pages: str = ""
    doi: str = ""
    pmid: str = ""
    pubtypes: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def retracted(self) -> bool:
        return bool(RETRACTION_TYPES & set(self.pubtypes))


class Http:
    """Tiny HTTP client with backoff, and a fixture mode for offline testing.

    Fixtures live in a single JSON file mapping URL -> {"status": int,
    "body": str}. Keeping them in one file makes them easy to record, review in
    a diff, and reason about.
    """

    def __init__(self, fixtures: Path | None = None, delay: float = 0.34):
        self.fixtures: dict | None = None
        self.delay = delay
        self._last = 0.0
        if fixtures:
            path = fixtures / "http_cache.json" if fixtures.is_dir() else fixtures
            self.fixtures = json.loads(path.read_text(encoding="utf-8"))

    def get(self, url: str, retries: int = 3) -> tuple[int, str]:
        if self.fixtures is not None:
            entry = self.fixtures.get(url)
            if entry is None:
                return 404, ""
            return entry.get("status", 200), entry.get("body", "")

        # Stay under NCBI's unauthenticated limit of 3 requests/second.
        gap = time.time() - self._last
        if gap < self.delay:
            time.sleep(self.delay - gap)

        headers = {"User-Agent": f"{TOOL}/1.0" + (f" ({CONTACT})" if CONTACT else "")}
        for attempt in range(retries):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=30) as resp:
                    self._last = time.time()
                    return resp.status, resp.read().decode("utf-8", "replace")
            except urllib.error.HTTPError as exc:
                self._last = time.time()
                # 429 and 5xx are worth retrying; 404 means it does not exist.
                if exc.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                    time.sleep(2**attempt)
                    continue
                return exc.code, ""
            except (urllib.error.URLError, TimeoutError) as exc:
                if attempt < retries - 1:
                    time.sleep(2**attempt)
                    continue
                # Unavailable is not nonexistent; keep checking other identifiers.
                return 0, ""
        return 0, ""


def _ncbi_key_param() -> str:
    key = os.environ.get("NCBI_API_KEY", "").strip()
    return f"&api_key={urllib.parse.quote(key)}" if key else ""


def resolve_pmid(pmid: str, http: Http) -> Record:
    rec = Record(identifier=pmid, kind="pmid", pmid=pmid)
    url = (
        f"{EUTILS}/esummary.fcgi?db=pubmed&id={urllib.parse.quote(pmid)}"
        f"&retmode=json&tool={TOOL}{_ncbi_key_param()}"
    )
    status, body = http.get(url)
    if status != 200 or not body:
        rec.notes.append(f"PubMed returned HTTP {status}")
        return rec

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        rec.notes.append("PubMed returned a response that was not valid JSON")
        return rec

    entry = (data.get("result") or {}).get(pmid)
    if not entry or "error" in entry:
        rec.notes.append("no PubMed record for this PMID")
        return rec

    rec.resolved = True
    rec.source = "PubMed"
    rec.title = (entry.get("title") or "").rstrip(".")
    rec.authors = [
        a.get("name", "")
        for a in entry.get("authors", [])
        if a.get("authtype") == "Author"
    ]
    rec.journal = entry.get("source", "")
    rec.year = (entry.get("pubdate") or "")[:4]
    rec.volume = entry.get("volume", "")
    rec.issue = entry.get("issue", "")
    rec.pages = entry.get("pages", "")
    rec.pubtypes = list(entry.get("pubtype") or [])
    for aid in entry.get("articleids", []):
        if aid.get("idtype") == "doi":
            rec.doi = aid.get("value", "")
    return rec


def resolve_doi(doi: str, http: Http) -> Record:
    doi = doi.rstrip(".,;)")
    rec = Record(identifier=doi, kind="doi", doi=doi)

    status, body = http.get(f"{CROSSREF}/{urllib.parse.quote(doi, safe='')}")
    if status == 200 and body:
        try:
            msg = json.loads(body).get("message", {})
        except json.JSONDecodeError:
            msg = {}
        if msg:
            rec.resolved = True
            rec.source = "CrossRef"
            rec.title = (msg.get("title") or [""])[0]
            rec.authors = [
                f"{a.get('family', '')} {(a.get('given') or '')[:1]}".strip()
                for a in msg.get("author", [])
            ]
            rec.journal = (msg.get("container-title") or [""])[0]
            parts = (msg.get("published") or msg.get("issued") or {}).get(
                "date-parts", [[""]]
            )
            rec.year = str(parts[0][0]) if parts and parts[0] else ""
            rec.volume = msg.get("volume", "")
            rec.issue = msg.get("issue", "")
            rec.pages = msg.get("page", "")
            if msg.get("update-to"):
                for upd in msg["update-to"]:
                    if "retract" in str(upd.get("type", "")).lower():
                        rec.pubtypes.append("Retracted Publication")
            return rec

    # OpenAlex access requirements can change. Use an optional local key;
    # Crossref remains the keyless primary path. Fixtures never use real keys.
    key = '' if http.fixtures is not None else os.environ.get('OPENALEX_API_KEY', '')
    suffix = ('?api_key=' + urllib.parse.quote(key)) if key else ''
    status, body = http.get(f"{OPENALEX}/doi:{urllib.parse.quote(doi, safe='')}{suffix}")
    if status == 200 and body:
        try:
            msg = json.loads(body)
        except json.JSONDecodeError:
            msg = {}
        if msg.get("id"):
            rec.resolved = True
            rec.source = "OpenAlex"
            rec.title = msg.get("title") or ""
            rec.authors = [
                (a.get("author") or {}).get("display_name", "")
                for a in msg.get("authorships", [])
            ]
            loc = (msg.get("primary_location") or {}).get("source") or {}
            rec.journal = loc.get("display_name", "")
            rec.year = str(msg.get("publication_year") or "")
            if msg.get("is_retracted"):
                rec.pubtypes.append("Retracted Publication")
            ids = msg.get("ids") or {}
            if ids.get("pmid"):
                rec.pmid = str(ids["pmid"]).rsplit("/", 1)[-1]
            return rec

    rec.notes.append("not verified by available Crossref/OpenAlex responses; an outage or access limit is not proof of fabrication")
    return rec


def resolve_nct(nct: str, http: Http) -> Record:
    """Trial registry records are cited too, and are just as fabricable."""
    nct = nct.upper()
    rec = Record(identifier=nct, kind="nct")
    url = (
        f"https://clinicaltrials.gov/api/v2/studies/{nct}"
        f"?fields=protocolSection.identificationModule"
    )
    status, body = http.get(url)
    if status != 200 or not body:
        rec.notes.append(f"ClinicalTrials.gov returned HTTP {status}")
        return rec
    try:
        ident = (
            json.loads(body).get("protocolSection", {}).get("identificationModule", {})
        )
    except json.JSONDecodeError:
        rec.notes.append("ClinicalTrials.gov returned invalid JSON")
        return rec
    if ident.get('nctId', '').upper() != nct or not ident.get('briefTitle'):
        rec.notes.append('trial identifier/title missing or mismatched in registry response')
        return rec
    rec.resolved = True
    rec.source = "ClinicalTrials.gov"
    rec.title = ident.get("briefTitle", "")
    return rec


def extract_identifiers(text: str) -> dict[str, list[str]]:
    """Pull explicitly labelled identifiers; dates/account IDs are not PMIDs."""
    pmids = [a or b for a, b in PMID_RE.findall(text)]
    dois = [d.rstrip(".,;)") for d in DOI_RE.findall(text)]
    ncts = [n.upper() for n in NCT_RE.findall(text)]

    def dedupe(seq):
        seen, out = set(), []
        for s in seq:
            if s not in seen:
                seen.add(s)
                out.append(s)
        return out

    return {"pmids": dedupe(pmids), "dois": dedupe(dois), "ncts": dedupe(ncts)}


def format_ama(rec: Record, n: int) -> str:
    """AMA 11th-edition style: all authors up to 6, else first 3 + et al."""
    if len(rec.authors) > 6:
        authors = ", ".join(rec.authors[:3]) + ", et al"
    else:
        authors = ", ".join(rec.authors)
    bits = [f"{n}. "]
    if authors:
        bits.append(f"{authors}. ")
    if rec.title:
        bits.append(f"{rec.title}. ")
    if rec.journal:
        bits.append(f"*{rec.journal}.* ")
    if rec.year:
        vol = rec.volume
        iss = f"({rec.issue})" if rec.issue else ""
        pg = f":{rec.pages}" if rec.pages else ""
        bits.append(f"{rec.year};{vol}{iss}{pg}. ")
    if rec.doi:
        bits.append(f"doi:{rec.doi}")
    return "".join(bits).strip()


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--pmids", help="comma-separated PubMed IDs")
    ap.add_argument("--dois", help="comma-separated DOIs")
    ap.add_argument("--ncts", help="comma-separated ClinicalTrials.gov IDs")
    ap.add_argument("--file", help="extract and verify every identifier in this file")
    ap.add_argument(
        "--format",
        choices=["report", "ama", "json"],
        default="report",
        help="report (default) | ama reference list | json for downstream tooling",
    )
    ap.add_argument("--fixtures", help="offline fixture directory or file")
    args = ap.parse_args()

    pmids = [p.strip() for p in (args.pmids or "").split(",") if p.strip()]
    dois = [d.strip() for d in (args.dois or "").split(",") if d.strip()]
    ncts = [n.strip() for n in (args.ncts or "").split(",") if n.strip()]

    if args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"No such file: {path}", file=sys.stderr)
            return 2
        found = extract_identifiers(path.read_text(encoding="utf-8"))
        pmids += found["pmids"]
        dois += found["dois"]
        ncts += found["ncts"]

    if not (pmids or dois or ncts):
        ap.print_help()
        return 2

    http = Http(Path(args.fixtures) if args.fixtures else None)
    records: list[Record] = []
    for p in dict.fromkeys(pmids):
        records.append(resolve_pmid(p, http))
    for d in dict.fromkeys(dois):
        records.append(resolve_doi(d, http))
    for n in dict.fromkeys(ncts):
        records.append(resolve_nct(n, http))

    failed = [r for r in records if not r.resolved]
    retracted = [r for r in records if r.retracted]

    if args.format == "json":
        print(json.dumps([r.__dict__ for r in records], indent=2))
    elif args.format == "ama":
        for i, rec in enumerate([r for r in records if r.resolved], 1):
            print(format_ama(rec, i))
        for rec in failed:
            print(f"!! UNVERIFIED — resolve before citing as verified: {rec.identifier}")
    else:
        for rec in records:
            if rec.resolved:
                flag = "  ⚠ RETRACTED/CONCERN" if rec.retracted else ""
                first = rec.authors[0] if rec.authors else "—"
                print(f"[OK]   {rec.identifier}  ({rec.source}){flag}")
                print(f"       {rec.title[:100]}")
                print(f"       {first} et al · {rec.journal} · {rec.year}")
                if rec.retracted:
                    print(f"       pubtypes: {', '.join(rec.pubtypes)}")
            else:
                print(f"[FAIL] {rec.identifier}  — {'; '.join(rec.notes) or 'unresolved'}")
            print()

        print(
            f"{len(records)} identifier(s) · {len(records) - len(failed)} resolved · "
            f"{len(failed)} unresolved · {len(retracted)} retracted/concern"
        )
        if failed:
            print(
                "\nDo not treat unresolved references as verified support. Preserve them\n"
                "in the remediation log. Access failures are not proof of fabrication.\n"
                "Check the source and the claim before scientific use."
            )
        if retracted:
            print(
                "\nRetracted or flagged papers must not be cited as evidence. If the\n"
                "retraction itself is the point being made, cite it as such explicitly."
            )

    return 1 if (failed or retracted) else 0


if __name__ == "__main__":
    raise SystemExit(main())
