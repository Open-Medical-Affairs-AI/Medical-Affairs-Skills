#!/usr/bin/env python3
"""Self-tests for the bundled API clients.

Two modes, and the distinction matters:

  (default)  Offline, against the recorded fixtures in shared/fixtures/. This is
             what CI runs. It genuinely tests parsing, pagination, empty-result
             handling, error paths, and — importantly — that the interpretation
             guardrails (FAERS caveats, unresolved-citation warnings, negation
             flagging) actually appear in the output. It does NOT prove the
             upstream APIs still return what the fixtures claim.

  --live     Against the real APIs. This is the only thing that catches an
             upstream schema change. Run it from a network with egress to
             eutils.ncbi.nlm.nih.gov, clinicaltrials.gov and api.fda.gov.

    python3 scripts/selftest_apis.py
    python3 scripts/selftest_apis.py --live
    python3 scripts/selftest_apis.py --verbose

Exit 0 = all passed.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FIXTURES = REPO / "shared" / "fixtures"

PUBMED = "skills/pubmed-search/scripts/pubmed.py"
CTGOV = "skills/clinical-trials-search/scripts/ctgov.py"
OPENFDA = "skills/regulatory-label-intelligence/scripts/openfda.py"
CITES = "skills/citation-integrity/scripts/verify_citations.py"
MESH = "skills/medical-terminology-mapping/scripts/mesh_resolve.py"


@dataclass
class Case:
    name: str
    argv: list[str]
    expect_exit: int = 0
    must_contain: tuple[str, ...] = ()
    must_not_contain: tuple[str, ...] = ()
    live_only: bool = False
    offline_only: bool = False


# Fixture-mode cases. `--fixtures` is spliced in for offline runs.
CASES: list[Case] = [
    # ---------------- PubMed -------------------------------------------
    Case(
        "pubmed: search returns parsed records with identifiers",
        [PUBMED, "search", "--query", "teclistamab AND myeloma", "--limit", "3"],
        must_contain=("36001231", "N Engl J Med", "PubMed search"),
    ),
    Case(
        "pubmed: abstracts parse, including structured section labels",
        [PUBMED, "search", "--query", "teclistamab AND myeloma", "--limit", "3",
         "--abstracts"],
        must_contain=("BACKGROUND:", "RESULTS:", "63.0%"),
    ),
    Case(
        "pubmed: NCT identifiers are extracted from the record",
        [PUBMED, "search", "--query", "teclistamab AND myeloma", "--limit", "3",
         "--abstracts"],
        must_contain=("NCT04557098",),
    ),
    Case(
        "pubmed: retracted publications are flagged, not silently listed",
        [PUBMED, "search", "--query", "teclistamab AND myeloma", "--limit", "3"],
        must_contain=("RETRACTED",),
    ),
    Case(
        "pubmed: partial result sets warn against treating them as representative",
        [PUBMED, "search", "--query", "teclistamab AND myeloma", "--limit", "3"],
        must_contain=("Showing 3 of 84",),
    ),
    Case(
        "pubmed: empty result is explained, not reported as a gap",
        [PUBMED, "search", "--query", "zzzznotarealdrugzzzz", "--limit", "3"],
        must_contain=("No results", "widen synonyms"),
    ),
    Case(
        "pubmed: unresolvable PMID exits non-zero and says why",
        [PUBMED, "fetch", "--pmids", "99999999"],
        expect_exit=1,
        must_contain=("DID NOT RESOLVE", "unverified"),
    ),
    Case(
        "pubmed: AMA formatting truncates author lists at the right threshold",
        [PUBMED, "search", "--query", "teclistamab AND myeloma", "--limit", "3",
         "--format", "ama"],
        must_contain=("Moreau P, Garfall AL, van de Donk NWCJ, et al",
                      "doi:10.1056/NEJMoa2203478"),
    ),
    Case(
        "pubmed: MeSH lookup surfaces entry terms and the indexing-lag warning",
        [PUBMED, "mesh", "--term", "multiple myeloma", "--limit", "2"],
        must_contain=("Multiple Myeloma", "Plasma Cell Myeloma", "indexing lags"),
    ),
    # ---------------- ClinicalTrials.gov --------------------------------
    Case(
        "ctgov: search parses design, enrolment and sponsor",
        [CTGOV, "search", "--term", "teclistamab", "--limit", "3"],
        must_contain=("NCT04557098", "MajesTEC-1", "Janssen"),
    ),
    Case(
        "ctgov: single-arm designs carry the no-comparative-inference caveat",
        [CTGOV, "search", "--term", "teclistamab", "--limit", "3"],
        must_contain=("no comparative inference",),
    ),
    Case(
        "ctgov: randomised designs are distinguished from single-arm",
        [CTGOV, "search", "--term", "teclistamab", "--limit", "3"],
        must_contain=("Randomised",),
    ),
    Case(
        "ctgov: output states that registry coverage is not global",
        [CTGOV, "search", "--term", "teclistamab", "--limit", "3"],
        must_contain=("not global", "EU CTIS"),
    ),
    Case(
        "ctgov: enrolment prints without an empty parenthesis when type is absent",
        [CTGOV, "get", "--nct", "NCT04557098"],
        must_not_contain=(" ()",),
    ),
    Case(
        "ctgov: invalid status is rejected with the valid list",
        [CTGOV, "search", "--term", "x", "--status", "NONSENSE"],
        expect_exit=1,
        must_contain=("Unknown status", "RECRUITING"),
    ),
    # ---------------- openFDA -------------------------------------------
    Case(
        "openfda: indication is returned verbatim with the on-label boundary noted",
        [OPENFDA, "indication", "--generic", "teclistamab"],
        must_contain=("at least four prior lines", "off-label"),
    ),
    Case(
        "openfda: label output states the US-only jurisdiction limit",
        [OPENFDA, "label", "--generic", "teclistamab",
         "--sections", "boxed_warning,indications_and_usage"],
        must_contain=("US label only", "CYTOKINE RELEASE SYNDROME"),
    ),
    Case(
        "openfda: FAERS output always carries the no-denominator caveat",
        [OPENFDA, "faers", "--generic", "teclistamab", "--limit", "5"],
        must_contain=("No denominator exists",
                      "CANNOT be compared between products",
                      "CYTOKINE RELEASE SYNDROME"),
    ),
    Case(
        "openfda: unknown product does not imply the product is unapproved",
        [OPENFDA, "label", "--generic", "notadrugatall"],
        expect_exit=1,
        must_contain=("No US label found",),
    ),
    # ---------------- citation integrity ---------------------------------
    Case(
        "citations: resolves a real PMID and rejects a fabricated one",
        [CITES, "--pmids", "36001231,99999999"],
        expect_exit=1,
        must_contain=("[OK]   36001231", "[FAIL] 99999999", "unresolved"),
    ),
    Case(
        "citations: extracts identifiers from free text",
        [CITES, "--pmids", "36001231", "--format", "ama"],
        must_contain=("Moreau P", "N Engl J Med"),
    ),
    # ---------------- terminology ----------------------------------------
    Case(
        "terminology: grades exact, synonym, fuzzy and unresolved separately",
        [MESH, "resolve", "--terms",
         "multiple myeloma, cytokine storm, zzz unmappable phrase"],
        must_contain=("exact", "synonym", "unresolved", "Cytokine Release Syndrome"),
    ),
    Case(
        "terminology: negation is flagged rather than collapsed",
        [MESH, "resolve", "--terms", "no infection"],
        must_contain=("NEGATED",),
    ),
    Case(
        "terminology: adverse-event language triggers escalation, not coding",
        [MESH, "resolve", "--terms", "grade 3 CRS requiring hospitalisation"],
        must_contain=("POTENTIAL ADVERSE EVENT", "NOT MedDRA"),
    ),
    Case(
        "terminology: output disclaims regulatory standing",
        [MESH, "resolve", "--terms", "multiple myeloma"],
        must_contain=("no\nregulatory standing",),
    ),
]

# Live mode uses a smaller set — enough to detect a schema change without
# hammering third-party infrastructure.
LIVE_CASES: list[Case] = [
    Case("live pubmed: search returns records",
         [PUBMED, "search", "--query", '"multiple myeloma"[MeSH]', "--limit", "3"],
         must_contain=("PMID",)),
    Case("live pubmed: abstracts still parse",
         [PUBMED, "search", "--query", '"teclistamab"[tiab]', "--limit", "2",
          "--abstracts"],
         must_contain=("PMID",)),
    Case("live pubmed: MeSH lookup still returns entry terms",
         [PUBMED, "mesh", "--term", "multiple myeloma", "--limit", "1"],
         must_contain=("MeSH heading",)),
    Case("live ctgov: search returns studies",
         [CTGOV, "search", "--condition", "multiple myeloma", "--limit", "3"],
         must_contain=("NCT",)),
    Case("live ctgov: a known NCT resolves",
         [CTGOV, "get", "--nct", "NCT04557098"], must_contain=("NCT04557098",)),
    Case("live openfda: a known label resolves",
         [OPENFDA, "indication", "--generic", "teclistamab"],
         must_contain=("indicated",)),
    Case("live citations: a known PMID resolves",
         [CITES, "--pmids", "36001231"], must_contain=("[OK]",)),
]


def run(case: Case, live: bool, verbose: bool) -> tuple[bool, str]:
    argv = [sys.executable] + case.argv
    if not live:
        # --fixtures is a top-level flag on every client, so it goes before the
        # subcommand. argv[0] is the script path.
        argv = argv[:2] + ["--fixtures", str(FIXTURES)] + argv[2:]

    try:
        proc = subprocess.run(
            argv, cwd=REPO, capture_output=True, text=True, timeout=120
        )
    except subprocess.TimeoutExpired:
        return False, "timed out after 120s"

    out = proc.stdout + proc.stderr
    if verbose:
        print("    $ " + " ".join(str(a) for a in argv[1:]))

    problems = []
    if proc.returncode != case.expect_exit:
        problems.append(f"exit {proc.returncode}, expected {case.expect_exit}")
    for needle in case.must_contain:
        if needle not in out:
            problems.append(f"missing expected text: {needle!r}")
    for needle in case.must_not_contain:
        if needle in out:
            problems.append(f"contained forbidden text: {needle!r}")

    if problems:
        detail = "; ".join(problems)
        if verbose:
            detail += "\n--- output ---\n" + out[:2000]
        return False, detail
    return True, ""


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--live", action="store_true",
                    help="test against the real APIs instead of fixtures")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    if not args.live and not (FIXTURES / "http_cache.json").exists():
        print("No fixtures found. Generate them with:")
        print("  python3 scripts/record_fixtures.py")
        return 1

    cases = LIVE_CASES if args.live else CASES
    mode = "LIVE (real APIs)" if args.live else "offline (fixtures)"
    print(f"API client self-test — {mode}\n")

    passed = failed = 0
    for case in cases:
        ok, detail = run(case, args.live, args.verbose)
        if ok:
            passed += 1
            print(f"  pass   {case.name}")
        else:
            failed += 1
            print(f"  FAIL   {case.name}")
            print(f"         {detail}")

    print(f"\n{passed} passed · {failed} failed")

    if failed:
        if args.live:
            print(
                "\nA live failure usually means an upstream API changed shape, not\n"
                "that this repository is broken. Re-record fixtures with\n"
                "  python3 scripts/record_fixtures.py --live\n"
                "and diff them to see exactly what moved."
            )
        return 1

    if not args.live:
        print(
            "\nThese passed against recorded fixtures. That proves the clients parse\n"
            "and guard correctly; it does not prove the upstream APIs still return\n"
            "this shape. Run --live from a network with egress to confirm that."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
