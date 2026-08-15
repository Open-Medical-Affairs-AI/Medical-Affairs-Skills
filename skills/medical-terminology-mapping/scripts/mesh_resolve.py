#!/usr/bin/env python3
"""Resolve free-text clinical concepts to MeSH descriptors, with graded confidence.

Free text cannot be counted. Twelve people describing the same concern twelve
ways produces a frequency of one for each, and the signal disappears. Mapping
fixes that — and can also manufacture a signal that is not there, by collapsing
distinct concepts. So this tool grades every mapping and never hides the ones it
could not resolve.

    S=skills/medical-terminology-mapping/scripts/mesh_resolve.py

    python3 $S resolve  --terms "myeloma, skin rash, cytokine storm"
    python3 $S resolve  --file insights.csv --column observation
    python3 $S validate --terms "Multiple Myeloma,Not A Real Heading"

MeSH only. MedDRA, SNOMED CT, ICD and ATC are licensed and are deliberately not
resolved here — see the SKILL.md for what to do instead.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from pathlib import Path

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
TOOL = "medical-affairs-skills"

# Phrases that invert meaning. Collapsing "no infection" into "infection" is a
# small parsing error with clinical consequences, so we refuse to map these
# without flagging them.
NEGATION = re.compile(
    r"\b(no|not|without|absence of|denies|negative for|ruled out|free of)\b", re.I
)

# Language that suggests a possible adverse event. This tool does not code AEs —
# it routes them — but it should never let one pass unremarked.
AE_HINT = re.compile(
    r"\b(adverse|toxicit|side effect|grade [1-5]|hospitali[sz]|discontinu|"
    r"death|died|fatal|serious|reaction|overdose|pregnan)\w*",
    re.I,
)


@dataclass
class Mapping:
    verbatim: str
    concept: str = ""
    confidence: str = "unresolved"  # exact|synonym|fuzzy|unresolved
    entry_terms: list[str] | None = None
    scope_note: str = ""
    negated: bool = False
    ae_flag: bool = False
    note: str = ""


def get(url: str, fixtures: dict | None, retries: int = 3) -> str:
    if fixtures is not None:
        entry = fixtures.get(url)
        if entry is None:
            raise SystemExit(f"No fixture recorded for:\n  {url}")
        return entry.get("body", "")
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": f"{TOOL}/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                time.sleep(0.34)  # stay under NCBI's unauthenticated limit
                return resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(2**attempt)
                continue
            return ""
        except (urllib.error.URLError, TimeoutError):
            if attempt < retries - 1:
                time.sleep(2**attempt)
                continue
            raise SystemExit(
                "Could not reach eutils.ncbi.nlm.nih.gov. "
                "See docs/api-setup.md for hosts that must be allowlisted."
            )
    return ""


def lookup(term: str, fixtures: dict | None) -> Mapping:
    m = Mapping(verbatim=term)
    m.negated = bool(NEGATION.search(term))
    m.ae_flag = bool(AE_HINT.search(term))

    cleaned = NEGATION.sub("", term).strip(" ,.;:")
    if not cleaned:
        m.note = "nothing left after removing negation"
        return m

    url = (
        f"{EUTILS}/esearch.fcgi?"
        + urllib.parse.urlencode(
            {"db": "mesh", "term": cleaned, "retmax": 1, "retmode": "json", "tool": TOOL}
        )
    )
    raw = get(url, fixtures)
    if not raw:
        m.note = "MeSH lookup failed"
        return m
    try:
        uids = json.loads(raw).get("esearchresult", {}).get("idlist", [])
    except json.JSONDecodeError:
        m.note = "MeSH returned invalid JSON"
        return m
    if not uids:
        m.note = "no MeSH descriptor matched"
        return m

    url = (
        f"{EUTILS}/esummary.fcgi?"
        + urllib.parse.urlencode(
            {"db": "mesh", "id": uids[0], "retmode": "json", "tool": TOOL}
        )
    )
    raw = get(url, fixtures)
    try:
        rec = (json.loads(raw).get("result") or {}).get(uids[0]) or {}
    except json.JSONDecodeError:
        m.note = "MeSH summary returned invalid JSON"
        return m

    terms = rec.get("ds_meshterms") or []
    if not terms:
        m.note = "descriptor had no terms"
        return m

    m.concept = terms[0]
    m.entry_terms = terms[1:]
    m.scope_note = (rec.get("ds_scopenote") or "").strip()

    norm = cleaned.lower().strip()
    if norm == m.concept.lower():
        m.confidence = "exact"
    elif any(norm == t.lower() for t in terms[1:]):
        m.confidence = "synonym"
    else:
        m.confidence = "fuzzy"
        m.note = "approximate match — confirm before counting"
    return m


def read_terms(args) -> list[str]:
    if args.terms:
        return [t.strip() for t in args.terms.split(",") if t.strip()]
    path = Path(args.file)
    if not path.exists():
        raise SystemExit(f"No such file: {path}")
    if path.suffix.lower() in {".csv", ".tsv"}:
        delim = "\t" if path.suffix.lower() == ".tsv" else ","
        with path.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh, delimiter=delim)
            if args.column not in (reader.fieldnames or []):
                raise SystemExit(
                    f"Column '{args.column}' not found. Available: "
                    f"{', '.join(reader.fieldnames or [])}"
                )
            return [r[args.column].strip() for r in reader if (r.get(args.column) or "").strip()]
    return [l.strip() for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--fixtures")
    ap.add_argument("--format", default="markdown", choices=["markdown", "json"])
    sub = ap.add_subparsers(dest="cmd", required=True)

    for name, helptext in [
        ("resolve", "map free text to MeSH descriptors"),
        ("validate", "check that descriptors exist and are current"),
    ]:
        p = sub.add_parser(name, help=helptext)
        p.add_argument("--terms", help="comma-separated")
        p.add_argument("--file", help="text file (one per line) or CSV/TSV")
        p.add_argument("--column", default="", help="column name when --file is CSV/TSV")

    args = ap.parse_args()
    if not args.terms and not args.file:
        print("Give --terms or --file.", file=sys.stderr)
        return 2

    fixtures = None
    if args.fixtures:
        p = Path(args.fixtures)
        p = p / "http_cache.json" if p.is_dir() else p
        fixtures = json.loads(p.read_text(encoding="utf-8"))

    terms = read_terms(args)
    # Preserve the count per distinct verbatim — frequency is the whole point.
    counts: dict[str, int] = {}
    for t in terms:
        counts[t] = counts.get(t, 0) + 1

    results = [lookup(t, fixtures) for t in counts]

    if args.format == "json":
        print(json.dumps(
            [{**asdict(m), "n": counts[m.verbatim]} for m in results], indent=2
        ))
        return 0

    resolved = [m for m in results if m.confidence in ("exact", "synonym")]
    fuzzy = [m for m in results if m.confidence == "fuzzy"]
    unresolved = [m for m in results if m.confidence == "unresolved"]
    negated = [m for m in results if m.negated]
    ae = [m for m in results if m.ae_flag]

    if ae:
        print("⚠ POTENTIAL ADVERSE EVENT LANGUAGE DETECTED — HUMAN ACTION REQUIRED\n")
        for m in ae:
            print(f'   "{m.verbatim}"  (n={counts[m.verbatim]})')
        print(
            "\n   These verbatims contain adverse-event, toxicity or special-situation\n"
            "   language. Route them to pharmacovigilance with the verbatim intact,\n"
            "   following your own SOPs. Analytical grouping below is NOT MedDRA\n"
            "   coding and has no regulatory standing.\n"
        )

    print("## Terminology mapping — MeSH\n")
    print(f"Resolved via NCBI E-utilities on {time.strftime('%Y-%m-%d')}\n")
    print("| Verbatim (n) | MeSH concept | Confidence | Note |")
    print("| --- | --- | --- | --- |")
    for m in sorted(results, key=lambda x: -counts[x.verbatim]):
        note = m.note
        if m.negated:
            note = ("NEGATED — do not aggregate with the affirmative concept. " + note).strip()
        print(
            f"| {m.verbatim} ({counts[m.verbatim]}) | {m.concept or '—'} "
            f"| {m.confidence} | {note} |"
        )

    print(
        f"\n**{len(resolved)} resolved · {len(fuzzy)} fuzzy · "
        f"{len(unresolved)} unresolved** of {len(results)} distinct verbatims."
    )
    if fuzzy or unresolved:
        print(
            "\nFuzzy and unresolved mappings must be reviewed by a person before any\n"
            "count derived from them is published. Report the unresolved list in the\n"
            "deliverable — an unresolved concept is information, a wrong code is not."
        )
    if negated:
        print(
            f"\n{len(negated)} verbatim(s) contain negation and were flagged rather\n"
            "than mapped. Collapsing these into the affirmative concept would invert\n"
            "their meaning."
        )
    print(
        "\n_MeSH is a literature-indexing vocabulary. It is not MedDRA and carries no\n"
        "regulatory standing for adverse event coding._"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
