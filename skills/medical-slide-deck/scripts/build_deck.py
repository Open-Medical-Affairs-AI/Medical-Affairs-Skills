#!/usr/bin/env python3
"""Render a non-promotional medical slide deck from a JSON spec.

The spec is JSON so the content is reviewable and diffable before it becomes a
binary that nobody can inspect in a pull request. The builder enforces the
mechanical compliance rules — a data slide cannot render without a citation, the
draft marking is stamped on the title slide — and leaves the judgement calls to
deliverable-quality-review and to you.

    S=skills/medical-slide-deck/scripts/build_deck.py

    python3 $S --example > deck.json      # a worked spec to start from
    python3 $S --spec deck.json --out advisory-board.pptx
    python3 $S --spec deck.json --check   # validate without rendering

Rendering is done by the bundled engine (scripts/ma_render.py), which installs
python-pptx and matplotlib on first use, builds native editable charts, stat
cards, two-column and question layouts, writes a PDF copy when LibreOffice is
present, and runs layout QA. Without python-pptx it writes print-ready HTML —
never a markdown "deck".
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ma_render  # noqa: E402  (bundled, standalone copy)

DRAFT = "DRAFT — NOT FOR EXTERNAL USE. REQUIRES QUALIFIED MEDICAL REVIEW."

EXAMPLE = {
    "title": "Bispecific antibodies in relapsed/refractory myeloma",
    "subtitle": "Advisory board — scientific questions for discussion",
    "presenter": "Medical Affairs",
    "date": "2026-09-12",
    "jurisdiction": "US",
    "approval_status": (
        "NORVANTIB is approved in the US for adult patients with "
        "relapsed/refractory multiple myeloma after ≥ 4 prior lines. "
        "Uses discussed beyond this are investigational."
    ),
    "slides": [
        {
            "type": "section",
            "title": "Why we asked you here",
        },
        {
            "type": "bullets",
            "title": "Objectives for today",
            "bullets": [
                "Understand how you are sequencing BCMA-directed therapy in practice",
                "Test whether our proposed evidence plan answers questions you have",
                "Identify what we are missing",
            ],
            "notes": "Say explicitly what will be done with the advice.",
        },
        {
            "type": "data",
            "title": "ORR 63.0% in triple-class-exposed patients",
            "design": "Single-arm, phase 1/2 (n=165). No comparative inference.",
            "rows": [
                ["Endpoint", "Result (95% CI)", "Note"],
                ["Overall response rate", "63.0% (55.2–70.4)", "Primary endpoint"],
                ["Median DOR", "18.4 months (14.9–NE)", "Immature"],
                ["CRS, any grade", "72.1%", "Grade ≥3: 0.6%"],
            ],
            "citation": "Example A, et al. J Example Med. 2024;12(3):100-110. PMID 00000000",
            "tier": "peer-reviewed",
        },
        {
            "type": "bullets",
            "title": "What remains unknown",
            "bullets": [
                "No randomised comparison against current standard of care",
                "No data beyond 24 months of follow-up",
                "Sequencing after BCMA-directed therapy: no prospective data",
            ],
            "notes": "This slide builds credibility. Do not cut it for time.",
        },
        {
            "type": "questions",
            "title": "Questions for the group",
            "questions": [
                "What would you need to see before using this earlier in the pathway?",
                "Where does your practice diverge from the label, and why?",
                "What question would you want answered that we have not asked?",
            ],
        },
        {"type": "references", "title": "References", "references": []},
    ],
}


def validate(spec: dict) -> list[str]:
    """Mechanical checks only. Promotional framing is a human judgement."""
    problems: list[str] = []
    if not spec.get("title"):
        problems.append("spec has no title")
    slides = spec.get("slides") or []
    if not slides:
        problems.append("spec has no slides")

    for i, s in enumerate(slides, 1):
        kind = s.get("type", "")
        where = f"slide {i} ({kind or 'no type'})"
        if kind not in ma_render.DECK_TYPES:
            problems.append(f"{where}: unknown slide type — use one of "
                            f"{sorted(ma_render.DECK_TYPES)}")
        if not s.get("title") and kind not in {"callout", "quote"}:
            problems.append(f"{where}: no title")

        if kind in {"data", "table", "chart", "stats"}:
            # The rule this script exists to enforce.
            if not s.get("citation"):
                problems.append(
                    f"{where}: data slide has no citation. Every data slide carries "
                    f"its source — a slide that cannot be traced cannot be reviewed."
                )
            if not s.get("design"):
                problems.append(
                    f"{where}: data slide does not name the study design. 'Single-arm' "
                    f"and 'randomised' must be visible where the number is, not only "
                    f"in the backup."
                )
            if kind in {"data", "table"} and not s.get("rows"):
                problems.append(f"{where}: data slide has no rows")

    if not spec.get("approval_status"):
        problems.append(
            "spec has no approval_status. State what is approved, in which "
            "jurisdiction, and that anything else is investigational."
        )
    return problems


def _have(module: str) -> bool:
    """Inline capability check, kept small so a copied directory still works."""
    try:
        __import__(module)
        return True
    except ImportError:
        return False


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--spec", help="JSON deck specification")
    ap.add_argument("--out", default="deck.pptx")
    ap.add_argument("--check", action="store_true", help="validate only, do not render")
    ap.add_argument("--example", action="store_true", help="print a worked spec")
    ap.add_argument("--no-pdf", action="store_true", help="skip the PDF copy")
    ap.add_argument("--no-install", action="store_true", help="do not pip-install missing packages")
    ap.add_argument("--preview", help="folder for PNG page renders and a contact sheet")
    args = ap.parse_args()

    if args.example:
        print(json.dumps(EXAMPLE, indent=2))
        return 0

    if not args.spec:
        ap.print_help()
        return 2

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"No such file: {spec_path}", file=sys.stderr)
        return 2

    try:
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Spec is not valid JSON: {exc}", file=sys.stderr)
        return 2

    problems = validate(spec)
    for p in problems:
        print(f"  BLOCKED  {p}")
    if problems:
        print(
            f"\n{len(problems)} problem(s). These are mechanical compliance rules, "
            f"not style preferences — fix them before rendering.\n"
            f"Note that passing these checks does NOT mean the deck is "
            f"non-promotional. Run deliverable-quality-review for that."
        )
        return 1

    if args.check:
        print("Spec passes the mechanical checks.")
        print(
            "Still required: deliverable-quality-review for promotional framing, "
            "and mlr-review-readiness before the deck goes to review."
        )
        return 0

    out = Path(args.out)
    res = ma_render.render_deck(
        spec, out, pdf=not args.no_pdf, strict_approval=True,
        install=False if args.no_install else None,
        preview_dir=Path(args.preview) if args.preview else None,
    )
    code = ma_render._print_result(res, "Deck")
    if code == 0 and not res.get("degraded"):
        print("Next: open the preview contact sheet, then run deliverable-quality-review "
              "and mlr-review-readiness.")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
