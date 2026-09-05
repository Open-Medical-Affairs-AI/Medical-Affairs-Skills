#!/usr/bin/env python3
"""openFDA client — approved US label content and FAERS post-marketing reports.

The label settles what is on- and off-label, and is the correct source for
adverse reaction frequency. FAERS detects rare signals and cannot tell you a
rate. This client prints the caveats alongside FAERS output because omitting
them is the single most common error made with this data.

    S=skills/regulatory-label-intelligence/scripts/openfda.py

    python3 $S label      --generic teclistamab
    python3 $S label      --brand TECVAYLI --sections boxed_warning,indications_and_usage
    python3 $S indication --generic teclistamab
    python3 $S compare    --generics teclistamab,talquetamab --section boxed_warning
    python3 $S faers      --generic teclistamab --limit 20

No API key required (240 requests/minute). Set OPENFDA_API_KEY for a higher
limit. Self-contained by design.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import textwrap
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.fda.gov"
UA = "medical-affairs-skills/1.0"

# Ordered as they appear in a PLR label, so output reads like the document.
LABEL_SECTIONS = [
    "boxed_warning",
    "indications_and_usage",
    "dosage_and_administration",
    "dosage_forms_and_strengths",
    "contraindications",
    "warnings_and_cautions",
    "adverse_reactions",
    "drug_interactions",
    "use_in_specific_populations",
    "description",
    "clinical_pharmacology",
    "clinical_studies",
]

FAERS_CAVEAT = """\
─────────────────────────────────────────────────────────────────────────────
HOW THIS DATA MAY AND MAY NOT BE USED

FAERS is a spontaneous reporting system. These are counts of REPORTS, not
rates of events.

  · No denominator exists. You cannot derive incidence from this.
  · A report is not evidence of causation.
  · Counts CANNOT be compared between products. Reporting volume tracks launch
    recency, media attention, litigation, indication severity and surveillance
    intensity — not safety.
  · Under-reporting is severe and non-uniform.

Use FAERS to detect that a rare event has been reported, and to generate a
hypothesis worth investigating. For adverse reaction FREQUENCY, cite the
approved label's adverse_reactions section, which has a denominator.
─────────────────────────────────────────────────────────────────────────────"""


def http_get(url: str, fixtures: dict | None, retries: int = 3) -> tuple[int, str]:
    if fixtures is not None:
        entry = fixtures.get(url)
        if entry is None:
            raise SystemExit(f"No fixture recorded for:\n  {url}")
        return entry.get("status", 200), entry.get("body", "")

    key = os.environ.get("OPENFDA_API_KEY", "").strip()
    if key:
        url += ("&" if "?" in url else "?") + "api_key=" + urllib.parse.quote(key)

    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45) as resp:
                return resp.status, resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            # openFDA returns 404 with a JSON body when nothing matches, which
            # is a legitimate answer rather than an error.
            if exc.code == 404:
                return 404, exc.read().decode("utf-8", "replace")
            if exc.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(2**attempt)
                continue
            return exc.code, ""
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt < retries - 1:
                time.sleep(2**attempt)
                continue
            raise SystemExit(
                f"Could not reach api.fda.gov: {exc}\n"
                f"See docs/api-setup.md for hosts that must be allowlisted."
            )
    return 0, ""


def fetch_label(name: str, by: str, fixtures) -> dict | None:
    field = {
        "generic": "openfda.generic_name",
        "brand": "openfda.brand_name",
        "substance": "openfda.substance_name",
    }[by]
    search = urllib.parse.quote(f'{field}:"{name}"', safe="")
    url = f"{API}/drug/label.json?search={search}&limit=1"
    status, body = http_get(url, fixtures)
    if status == 404:
        return None
    if status != 200 or not body:
        raise SystemExit(f'Label service unavailable (HTTP {status}); approval status is not determined')
    try:
        results = json.loads(body).get("results", [])
    except json.JSONDecodeError:
        raise SystemExit('Label service returned invalid JSON; approval status is not determined')
    return results[0] if results else None


def show_label(rec: dict, sections: list[str], fmt: str) -> str:
    of = rec.get("openfda", {})
    if fmt == "json":
        return json.dumps(
            {k: rec.get(k) for k in ["openfda"] + sections if k in rec}, indent=2
        )

    out = []
    generic = ", ".join(of.get("generic_name", []) or ["?"])
    brand = ", ".join(of.get("brand_name", []) or ["?"])
    mfr = ", ".join(of.get("manufacturer_name", []) or ["?"])
    out.append(f"# {brand} ({generic})")
    out.append(f"*{mfr}* · US prescribing information via openFDA · "
               f"retrieved {time.strftime('%Y-%m-%d')}")
    out.append("")
    out.append("> **US label only.** EU SmPC and other national labels differ, "
               "sometimes in indication scope. State the jurisdiction in any "
               "deliverable using this.")
    out.append("")

    for sec in sections:
        content = rec.get(sec)
        if not content:
            continue
        heading = sec.replace("_", " ").title()
        marker = "⚠ " if sec == "boxed_warning" else ""
        out.append(f"## {marker}{heading}")
        text = "\n\n".join(content) if isinstance(content, list) else str(content)
        out.append(textwrap.fill(text, width=88, replace_whitespace=False))
        out.append("")
    return "\n".join(out)


def faers_reactions(name: str, limit: int, fixtures) -> list[dict]:
    search = urllib.parse.quote(
        f'patient.drug.openfda.generic_name:"{name}"', safe=""
    )
    url = (
        f"{API}/drug/event.json?search={search}"
        f"&count=patient.reaction.reactionmeddrapt.exact&limit={limit}"
    )
    status, body = http_get(url, fixtures)
    if status == 404:
        return []
    if status != 200 or not body:
        raise SystemExit(f'FAERS service unavailable (HTTP {status}); report counts are not determined')
    try:
        return json.loads(body).get("results", [])
    except json.JSONDecodeError:
        raise SystemExit('FAERS service returned invalid JSON; report counts are not determined')


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--fixtures", help="offline fixture directory or file")
    ap.add_argument("--format", default="markdown", choices=["markdown", "json"])
    sub = ap.add_subparsers(dest="cmd", required=True)

    l = sub.add_parser("label", help="retrieve approved label sections")
    l.add_argument("--generic")
    l.add_argument("--brand")
    l.add_argument("--substance")
    l.add_argument(
        "--sections",
        default="",
        help=f"comma-separated; default is all. Options: {', '.join(LABEL_SECTIONS)}",
    )

    i = sub.add_parser("indication", help="just the approved indication wording")
    i.add_argument("--generic")
    i.add_argument("--brand")

    c = sub.add_parser("compare", help="one section across several products")
    c.add_argument("--generics", required=True, help="comma-separated")
    c.add_argument("--section", default="boxed_warning")

    f = sub.add_parser("faers", help="FAERS reaction counts (read the caveats)")
    f.add_argument("--generic", required=True)
    f.add_argument("--limit", type=int, default=20)

    args = ap.parse_args()

    fixtures = None
    if args.fixtures:
        p = Path(args.fixtures)
        p = p / "http_cache.json" if p.is_dir() else p
        fixtures = json.loads(p.read_text(encoding="utf-8"))

    if args.cmd in ("label", "indication"):
        by, name = None, None
        for candidate in ("generic", "brand", "substance"):
            val = getattr(args, candidate, None)
            if val:
                by, name = candidate, val
                break
        if not name:
            print("Give one of --generic, --brand, or --substance.", file=sys.stderr)
            return 2

        rec = fetch_label(name, by, fixtures)
        if rec is None:
            print(f"No US label found for {by} name '{name}'.")
            print(
                "\nThis could mean: the product is not FDA-approved; the name is\n"
                "spelled differently in the label (try --brand or --substance); or\n"
                "it is approved outside the US only. Do not conclude it is\n"
                "unapproved without checking the EMA and other national registers."
            )
            return 1

        if args.cmd == "indication":
            ind = rec.get("indications_and_usage") or []
            print("## Approved US indication (verbatim)\n")
            for para in ind:
                print(textwrap.fill(para, width=88))
                print()
            print(
                "Read the qualifiers, not just the disease name. Line-of-therapy and\n"
                "population restrictions in this text are what define the on-label\n"
                "boundary — any use outside it is off-label and is governed by the\n"
                "unsolicited-request pathway in medical-affairs-foundations."
            )
            return 0

        sections = (
            [s.strip() for s in args.sections.split(",") if s.strip()]
            if args.sections
            else LABEL_SECTIONS
        )
        print(show_label(rec, sections, args.format))
        return 0

    if args.cmd == "compare":
        names = [n.strip() for n in args.generics.split(",") if n.strip()]
        print(f"# Label comparison — {args.section.replace('_', ' ').title()}\n")
        print(
            "> Internal reference only. Side-by-side label text is not evidence of\n"
            "> comparative safety or efficacy, and must not become an external\n"
            "> comparative claim without head-to-head data.\n"
        )
        for name in names:
            rec = fetch_label(name, "generic", fixtures)
            print(f"## {name}")
            if rec is None:
                print("_No US label found._\n")
                continue
            content = rec.get(args.section)
            if not content:
                print(f"_No {args.section} section in this label._\n")
                continue
            text = "\n\n".join(content) if isinstance(content, list) else str(content)
            print(textwrap.fill(text, width=88))
            print()
        return 0

    if args.cmd == "faers":
        rows = faers_reactions(args.generic, args.limit, fixtures)
        if args.format == 'json':
            print(json.dumps({'generic': args.generic, 'retrieved': time.strftime('%Y-%m-%d'),
                              'reactions': rows, 'caveat': FAERS_CAVEAT}, indent=2))
            return 0
        print(f"# FAERS reported reactions — {args.generic}")
        print(f"Retrieved {time.strftime('%Y-%m-%d')} via openFDA\n")
        if not rows:
            print("No FAERS reports matched that generic name.\n")
            print(FAERS_CAVEAT)
            return 0
        if args.format == "json":
            print(json.dumps(rows, indent=2))
        else:
            print("| MedDRA preferred term | Reports |")
            print("| --- | ---: |")
            for r in rows:
                print(f"| {r.get('term', '')} | {r.get('count', 0)} |")
        print()
        print(FAERS_CAVEAT)
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
