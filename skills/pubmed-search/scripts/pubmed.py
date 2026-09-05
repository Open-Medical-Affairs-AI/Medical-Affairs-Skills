#!/usr/bin/env python3
"""PubMed client for Medical Affairs literature retrieval (NCBI E-utilities).

Retrieval, not recall. Every reference in a Medical Affairs deliverable has to
resolve to a real record, and the only way to guarantee that is to fetch it.

    S=skills/pubmed-search/scripts/pubmed.py

    python3 $S search --query '"teclistamab"[tiab] AND "myeloma"[MeSH]' --limit 50
    python3 $S search --query 'teclistamab' --abstracts --format markdown
    python3 $S search --query 'Moreau P[au] AND myeloma' --from 2022
    python3 $S fetch  --pmids 36001231,35660948 --abstracts
    python3 $S mesh   --term "multiple myeloma"
    python3 $S links  --pmid 36001231 --kind citedby

Formats: json (default) | markdown | ama | table

Rate limits: 3 req/s without a key, 10 with one. Set NCBI_API_KEY (free, from
https://account.ncbi.nlm.nih.gov/settings/) to go faster. This client throttles
itself to stay compliant either way.

This module is intentionally self-contained — no imports from sibling skills —
so that a team can copy this one directory into their own repository and have it
work. See CONTRIBUTING.md on why that duplication is deliberate.
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
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, asdict
from pathlib import Path

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
TOOL = "medical-affairs-skills"
MAX_IDS_PER_REQUEST = 200  # NCBI accepts more via POST; 200 keeps URLs sane.


@dataclass
class Article:
    pmid: str = ""
    title: str = ""
    authors: list[str] = field(default_factory=list)
    journal: str = ""
    year: str = ""
    pubdate: str = ""
    volume: str = ""
    issue: str = ""
    pages: str = ""
    doi: str = ""
    pmcid: str = ""
    pubtypes: list[str] = field(default_factory=list)
    abstract: str = ""
    nct_ids: list[str] = field(default_factory=list)

    @property
    def retracted(self) -> bool:
        joined = " ".join(self.pubtypes).lower()
        return "retract" in joined or "expression of concern" in joined

    @property
    def evidence_tier(self) -> str:
        """Rough tier, to be confirmed by a human. Drives citation labelling."""
        pts = {p.lower() for p in self.pubtypes}
        if any("meta-analysis" in p or "systematic review" in p for p in pts):
            return "systematic review / meta-analysis"
        if any("practice guideline" in p or "guideline" == p for p in pts):
            return "guideline"
        if "randomized controlled trial" in pts:
            return "randomised controlled trial"
        if any("clinical trial" in p for p in pts):
            return "clinical trial (non-randomised or phase-specified)"
        if "case reports" in pts:
            return "case report"
        if any("review" in p for p in pts):
            return "review"
        return "journal article"


class Eutils:
    """E-utilities transport: throttling, backoff, and an offline fixture mode."""

    def __init__(self, fixtures: Path | None = None):
        self.key = os.environ.get("NCBI_API_KEY", "").strip()
        self.delay = 0.11 if self.key else 0.34
        self._last = 0.0
        self.fixtures: dict | None = None
        if fixtures:
            path = fixtures / "http_cache.json" if fixtures.is_dir() else fixtures
            self.fixtures = json.loads(path.read_text(encoding="utf-8"))

    def _url(self, endpoint: str, params: dict) -> str:
        params = {k: v for k, v in params.items() if v not in (None, "")}
        params["tool"] = TOOL
        if self.key:
            params["api_key"] = self.key
        return f"{EUTILS}/{endpoint}?" + urllib.parse.urlencode(params)

    def get(self, endpoint: str, params: dict, retries: int = 4) -> str:
        url = self._url(endpoint, params)

        if self.fixtures is not None:
            # Fixtures are keyed without the api_key, which varies by user.
            key = re.sub(r"&api_key=[^&]*", "", url)
            entry = self.fixtures.get(key) or self.fixtures.get(url)
            if entry is None:
                raise SystemExit(
                    f"No fixture recorded for this request.\n  {key}\n"
                    f"Record one, or drop --fixtures to go live."
                )
            return entry.get("body", "")

        gap = time.time() - self._last
        if gap < self.delay:
            time.sleep(self.delay - gap)

        for attempt in range(retries):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": f"{TOOL}/1.0"})
                with urllib.request.urlopen(req, timeout=45) as resp:
                    self._last = time.time()
                    return resp.read().decode("utf-8", "replace")
            except urllib.error.HTTPError as exc:
                self._last = time.time()
                if exc.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                    # NCBI throttles aggressively without a key. Back off hard.
                    time.sleep(2**attempt)
                    continue
                raise SystemExit(f"PubMed returned HTTP {exc.code} for:\n  {url}")
            except (urllib.error.URLError, TimeoutError) as exc:
                if attempt < retries - 1:
                    time.sleep(2**attempt)
                    continue
                raise SystemExit(
                    f"Could not reach eutils.ncbi.nlm.nih.gov: {exc}\n"
                    f"On a restricted network, see docs/api-setup.md for the "
                    f"hosts that must be allowlisted."
                )
        return ""


# --------------------------------------------------------------------------
# Core operations
# --------------------------------------------------------------------------


def esearch(api: Eutils, query: str, limit: int, date_from: str, date_to: str,
            sort: str) -> tuple[int, list[str]]:
    """Return (total_available, pmids). Pages transparently up to `limit`."""
    ids: list[str] = []
    total = 0
    retstart = 0
    while len(ids) < limit:
        batch = min(MAX_IDS_PER_REQUEST, limit - len(ids))
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": batch,
            "retstart": retstart,
            "retmode": "json",
            "sort": sort,
        }
        if date_from or date_to:
            params["datetype"] = "pdat"
            params["mindate"] = date_from or "1800"
            params["maxdate"] = date_to or "3000"
        data = json.loads(api.get("esearch.fcgi", params))
        result = data.get("esearchresult", {})
        if "ERROR" in result:
            raise SystemExit(f"PubMed rejected the query: {result['ERROR']}")
        total = int(result.get("count", 0))
        page = result.get("idlist", [])
        if not page:
            break
        ids.extend(page)
        retstart += len(page)
        if retstart >= total:
            break
    return total, ids[:limit]


def esummary(api: Eutils, pmids: list[str]) -> list[Article]:
    out: list[Article] = []
    for i in range(0, len(pmids), MAX_IDS_PER_REQUEST):
        chunk = pmids[i : i + MAX_IDS_PER_REQUEST]
        raw = api.get(
            "esummary.fcgi",
            {"db": "pubmed", "id": ",".join(chunk), "retmode": "json"},
        )
        result = json.loads(raw).get("result", {})
        for pmid in result.get("uids", []):
            e = result.get(pmid) or {}
            if "error" in e:
                continue
            art = Article(
                pmid=pmid,
                title=(e.get("title") or "").rstrip("."),
                authors=[
                    a.get("name", "")
                    for a in e.get("authors", [])
                    if a.get("authtype") == "Author"
                ],
                journal=e.get("source", ""),
                pubdate=e.get("pubdate", ""),
                year=(e.get("pubdate") or "")[:4],
                volume=e.get("volume", ""),
                issue=e.get("issue", ""),
                pages=e.get("pages", ""),
                pubtypes=list(e.get("pubtype") or []),
            )
            for aid in e.get("articleids", []):
                if aid.get("idtype") == "doi":
                    art.doi = aid.get("value", "")
                elif aid.get("idtype") == "pmc":
                    art.pmcid = aid.get("value", "")
            out.append(art)
    return out


def efetch_abstracts(api: Eutils, articles: list[Article]) -> None:
    """Fill in abstracts and any NCT identifiers, in place."""
    by_pmid = {a.pmid: a for a in articles}
    pmids = list(by_pmid)
    for i in range(0, len(pmids), MAX_IDS_PER_REQUEST):
        chunk = pmids[i : i + MAX_IDS_PER_REQUEST]
        xml = api.get(
            "efetch.fcgi",
            {"db": "pubmed", "id": ",".join(chunk), "retmode": "xml"},
        )
        try:
            root = ET.fromstring(xml)
        except ET.ParseError:
            continue
        for node in root.findall(".//PubmedArticle"):
            pid_el = node.find(".//MedlineCitation/PMID")
            if pid_el is None or pid_el.text not in by_pmid:
                continue
            art = by_pmid[pid_el.text]

            # Structured abstracts carry section labels worth preserving —
            # "METHODS" vs "RESULTS" matters when appraising.
            parts = []
            for ab in node.findall(".//Abstract/AbstractText"):
                label = ab.get("Label") or ab.get("NlmCategory")
                text = "".join(ab.itertext()).strip()
                if not text:
                    continue
                parts.append(f"{label}: {text}" if label else text)
            art.abstract = "\n".join(parts)

            for db in node.findall(".//DataBankList/DataBank"):
                name = db.find("DataBankName")
                if name is not None and (name.text or "").lower() == "clinicaltrials.gov":
                    for acc in db.findall(".//AccessionNumber"):
                        if acc.text:
                            art.nct_ids.append(acc.text.strip())


def elink(api: Eutils, pmid: str, kind: str, limit: int) -> list[str]:
    linkname = {
        "citedby": "pubmed_pubmed_citedin",
        "related": "pubmed_pubmed",
        "refs": "pubmed_pubmed_refs",
    }[kind]
    raw = api.get(
        "elink.fcgi",
        {
            "dbfrom": "pubmed",
            "db": "pubmed",
            "id": pmid,
            "linkname": linkname,
            "retmode": "json",
        },
    )
    out: list[str] = []
    for ls in json.loads(raw).get("linksets", []):
        for db in ls.get("linksetdbs", []):
            if db.get("linkname") == linkname:
                out.extend(db.get("links", []))
    return out[:limit]


def mesh_lookup(api: Eutils, term: str, limit: int) -> list[dict]:
    """How does PubMed actually index this concept? Run before searching."""
    raw = api.get(
        "esearch.fcgi",
        {"db": "mesh", "term": term, "retmax": limit, "retmode": "json"},
    )
    uids = json.loads(raw).get("esearchresult", {}).get("idlist", [])
    if not uids:
        return []
    raw = api.get(
        "esummary.fcgi", {"db": "mesh", "id": ",".join(uids), "retmode": "json"}
    )
    result = json.loads(raw).get("result", {})
    out = []
    for uid in result.get("uids", []):
        e = result.get(uid) or {}
        out.append(
            {
                "mesh_term": e.get("ds_meshterms", [""])[0]
                if e.get("ds_meshterms")
                else e.get("title", ""),
                "entry_terms": e.get("ds_meshterms", [])[1:],
                "scope_note": (e.get("ds_scopenote") or "").strip(),
                "tree_numbers": e.get("ds_idxlinks", []),
                "uid": uid,
            }
        )
    return out


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------


def fmt_ama(a: Article, n: int) -> str:
    au = ", ".join(a.authors[:3]) + ", et al" if len(a.authors) > 6 else ", ".join(a.authors)
    s = f"{n}. "
    if au:
        s += f"{au}. "
    s += f"{a.title}. "
    if a.journal:
        s += f"*{a.journal}.* "
    if a.year:
        s += f"{a.year};{a.volume}{f'({a.issue})' if a.issue else ''}{f':{a.pages}' if a.pages else ''}. "
    if a.doi:
        s += f"doi:{a.doi}"
    return s.strip() + (f"  **[RETRACTED/CONCERN]**" if a.retracted else "")


def render(articles: list[Article], fmt: str, total: int, query: str) -> str:
    if fmt == "json":
        return json.dumps(
            {
                "query": query,
                "total_available": total,
                "returned": len(articles),
                "articles": [asdict(a) for a in articles],
            },
            indent=2,
        )

    if fmt == "ama":
        return "\n".join(fmt_ama(a, i) for i, a in enumerate(articles, 1))

    if fmt == "table":
        rows = ["PMID     | Year | Journal              | Tier                | Title"]
        rows.append("-" * 110)
        for a in articles:
            rows.append(
                f"{a.pmid:<8} | {a.year:<4} | {a.journal[:20]:<20} | "
                f"{a.evidence_tier[:19]:<19} | {a.title[:45]}"
            )
        return "\n".join(rows)

    # markdown
    out = [
        f"**PubMed search** — `{query}`",
        f"{total} record(s) available · {len(articles)} retrieved · "
        f"searched {time.strftime('%Y-%m-%d')}",
        "",
    ]
    for a in articles:
        flag = "  ⚠ **RETRACTED / EXPRESSION OF CONCERN**" if a.retracted else ""
        out.append(f"### {a.title}{flag}")
        au = ", ".join(a.authors[:3]) + (" et al" if len(a.authors) > 3 else "")
        out.append(f"{au} · *{a.journal}* {a.pubdate}")
        ids = [f"PMID {a.pmid}"]
        if a.doi:
            ids.append(f"doi:{a.doi}")
        if a.pmcid:
            ids.append(a.pmcid)
        if a.nct_ids:
            ids.append(" ".join(a.nct_ids))
        out.append(f"`{' · '.join(ids)}`")
        out.append(f"*Tier: {a.evidence_tier}*")
        if a.abstract:
            out.append("")
            out.append(a.abstract)
        out.append("")
    return "\n".join(out)


# --------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--fixtures", help="offline fixture directory or file")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="search PubMed")
    s.add_argument("--query", required=True, help="PubMed query with field tags")
    s.add_argument("--limit", type=int, default=25)
    s.add_argument("--from", dest="date_from", default="", help="YYYY or YYYY/MM/DD")
    s.add_argument("--to", dest="date_to", default="")
    s.add_argument(
        "--sort",
        default="relevance",
        choices=["relevance", "date", "pub_date", "author", "journal"],
        help="relevance ranking is NOT quality ranking; use date for currency",
    )
    s.add_argument("--abstracts", action="store_true", help="also fetch abstracts")
    s.add_argument("--format", default="markdown", choices=["json", "markdown", "ama", "table"])

    f = sub.add_parser("fetch", help="fetch specific PMIDs")
    f.add_argument("--pmids", required=True)
    f.add_argument("--abstracts", action="store_true")
    f.add_argument("--format", default="markdown", choices=["json", "markdown", "ama", "table"])

    m = sub.add_parser("mesh", help="look up how PubMed indexes a concept")
    m.add_argument("--term", required=True)
    m.add_argument("--limit", type=int, default=5)

    l = sub.add_parser("links", help="citing or related articles")
    l.add_argument("--pmid", required=True)
    l.add_argument("--kind", default="citedby", choices=["citedby", "related", "refs"])
    l.add_argument("--limit", type=int, default=25)
    l.add_argument("--format", default="markdown", choices=["json", "markdown", "ama", "table"])

    args = ap.parse_args()
    api = Eutils(Path(args.fixtures) if args.fixtures else None)

    if args.cmd == "mesh":
        terms = mesh_lookup(api, args.term, args.limit)
        if not terms:
            print(f"No MeSH heading found for '{args.term}'.")
            print("Search free-text with [tiab] instead, and note the limitation.")
            return 1
        for t in terms:
            print(f"MeSH heading : {t['mesh_term']}")
            if t["entry_terms"]:
                print(f"Entry terms  : {', '.join(t['entry_terms'][:12])}")
            if t["scope_note"]:
                print(f"Scope        : {t['scope_note'][:300]}")
            print(
                f"Use as       : \"{t['mesh_term']}\"[MeSH]  "
                f"(add [majr] for major topic only)\n"
            )
        print(
            "Reminder: MeSH indexing lags publication by weeks to months. Combine\n"
            "with [tiab] free text or you will miss the newest papers."
        )
        return 0

    if args.cmd == "search":
        total, pmids = esearch(
            api, args.query, args.limit, args.date_from, args.date_to, args.sort
        )
        if not pmids:
            if args.format == 'json':
                print(render([], 'json', total, args.query))
                return 0
            print(f"No results for: {args.query}\n")
            print(
                "A well-documented empty result is a real finding — record the exact\n"
                "query and date. Before concluding a gap exists, widen synonyms\n"
                "(generic, brand, development code), drop publication-type filters,\n"
                "and try [tw] instead of [tiab]."
            )
            return 0
        articles = esummary(api, pmids)
        if args.abstracts:
            efetch_abstracts(api, articles)
        print(render(articles, args.format, total, args.query))
        if total > len(articles) and args.format != 'json':
            print(
                f"\n_Showing {len(articles)} of {total}. Raise --limit, or narrow the "
                f"query — do not treat this subset as representative._"
            )
        return 0

    if args.cmd == "fetch":
        pmids = [p.strip() for p in args.pmids.split(",") if p.strip()]
        articles = esummary(api, pmids)
        if args.abstracts:
            efetch_abstracts(api, articles)
        missing = set(pmids) - {a.pmid for a in articles}
        print(render(articles, args.format, len(pmids), "fetch"))
        if missing:
            print(f"\n!! DID NOT RESOLVE: {', '.join(sorted(missing))}")
            print("These PMIDs are unverified. Check identifiers and access before use; a failed lookup alone does not prove fabrication.")
            return 1
        return 0

    if args.cmd == "links":
        linked = elink(api, args.pmid, args.kind, args.limit)
        if not linked:
            print(f"No {args.kind} links for PMID {args.pmid}.")
            return 0
        articles = esummary(api, linked)
        print(render(articles, args.format, len(linked), f"{args.kind} of {args.pmid}"))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
