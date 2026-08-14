#!/usr/bin/env python3
"""Pre-check Medical Affairs content against what MLR reviewers actually reject.

Most first-round rejections are mechanical — an unreferenced number, a
comparative adjective with no head-to-head trial behind it, an absolute safety
claim. Every one is findable before submission, and each costs a one-to-three
week cycle when it is not.

    S=skills/mlr-review-readiness/scripts/claim_audit.py

    python3 $S --file deck-content.md
    python3 $S --file doc.md --format matrix   # claim-evidence matrix skeleton
    python3 $S --file doc.md --format json

This finds the mechanical problems. It CANNOT tell you whether a cited source
actually supports the claim attached to it — that requires reading the source,
and it is the most common substantive finding in review. Do it yourself.

Nothing this script outputs makes content compliant, MLR-ready, or approved.
Those are determinations made by people with accountability.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

# (pattern, severity, why it is flagged, what to do instead)
RULES: list[tuple[str, str, str, str]] = [
    (r"\b(proven|proves|demonstrated conclusively|conclusively)\b", "high",
     "implies certainty beyond what most designs support",
     "say what was observed, and name the design"),
    (r"\b(safe|is safe|proven safe)\b", "high",
     "absolute safety claim",
     "give the actual adverse event rates with denominators"),
    (r"\bwell[- ]tolerated\b", "high",
     "absolute safety claim unless qualified with rates",
     "report the rates, or qualify explicitly"),
    (r"\b(superior|superiority|more effective|better than|outperform\w*)\b", "high",
     "comparative claim — requires head-to-head evidence",
     "report each trial separately with its population, or use an adjusted "
     "indirect comparison with assumptions stated"),
    (r"\b(best[- ]in[- ]class|first[- ]in[- ]class|gold standard)\b", "high",
     "comparative and promotional", "remove"),
    (r"\bthe only\b", "high",
     "comparative claim, and usually factually fragile", "remove"),
    (r"\b(unlike other|compared with other|versus other)\b", "high",
     "implicit comparative claim", "remove or substantiate with head-to-head data"),
    (r"\b(should be used|recommended for|treatment of choice|first[- ]line choice)\b",
     "high", "prescribing direction — not Medical Affairs' role", "remove"),
    (r"\b(dramatic\w*|remarkable\w*|breakthrough|revolutionary|game[- ]chang\w+)\b",
     "medium", "promotional register", "remove"),
    (r"\b(significant\w*)\b", "medium",
     "ambiguous between statistical and clinical significance",
     "say which, and give the effect size with its confidence interval"),
    (r"\b(well[- ]established|widely accepted|it is known that)\b", "medium",
     "vague appeal to consensus", "cite the guideline or the evidence"),
    (r"\b(no (significant )?side effects|no safety concerns|no safety signal)\b",
     "high", "absence of evidence stated as evidence of absence",
     "state what was observed, in what N, over what follow-up"),
    (r"\b(cure[sd]?|curative)\b", "high",
     "very strong claim, rarely supportable", "state the actual endpoint"),
    (r"\b(rapid|fast|immediate) (onset|response|relief)\b", "medium",
     "comparative implication without a comparator", "give the actual time-to-event"),
]

# A numeric assertion with no nearby citation marker.
NUMERIC = re.compile(
    r"(?<![\w.])(\d{1,3}(?:\.\d+)?\s*%|\d+\.\d+\s*(?:months?|years?)|"
    r"HR\s*[=:]?\s*\d?\.\d+|OR\s*[=:]?\s*\d?\.\d+|RR\s*[=:]?\s*\d?\.\d+)"
)
CITATION_MARKER = re.compile(
    r"(PMID|doi|DOI|NCT\d{8}|\[\d+\]|\(\d{4}\)|et al|USPI|SmPC|data on file|"
    r"prescribing information)", re.I
)
CI_MARKER = re.compile(r"(95%\s*CI|confidence interval|\bCI\b)", re.I)
APPROVAL_MARKER = re.compile(
    r"(approved (for|in)|not approved|indicated for|investigational|"
    r"off[- ]label|unapproved)", re.I
)
FAIR_BALANCE = re.compile(
    r"(adverse (event|reaction)|safety|toxicit|warning|contraindicat|"
    r"grade\s*[≥>]?\s*3|discontinu)", re.I
)
EFFICACY = re.compile(
    r"(efficac|response rate|\bORR\b|\bPFS\b|\bOS\b|survival|remission|"
    r"reduction in|improvement in)", re.I
)


@dataclass
class Finding:
    line: int
    severity: str
    kind: str
    text: str
    why: str
    fix: str


def _blocks(text: str) -> list[tuple[int, str]]:
    """Split into paragraphs, keeping the starting line number of each.

    Claims are evaluated in the context of their paragraph, not their physical
    line — prose wraps, and a citation at the end of a sentence still supports
    a number near its start. Checking line-by-line produces false positives on
    any wrapped document, which trains people to ignore the output.
    """
    blocks: list[tuple[int, str]] = []
    current: list[str] = []
    start = 1
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip():
            if not current:
                start = i
            current.append(line)
        elif current:
            blocks.append((start, "\n".join(current)))
            current = []
    if current:
        blocks.append((start, "\n".join(current)))
    return blocks


def audit(text: str) -> tuple[list[Finding], dict]:
    findings: list[Finding] = []
    lines = text.splitlines()

    for start, block in _blocks(text):
        if block.lstrip().startswith(("<!--", "|---", "```")):
            continue

        def line_of(offset: int) -> int:
            return start + block[:offset].count("\n")

        for pattern, severity, why, fix in RULES:
            for m in re.finditer(pattern, block, re.I):
                findings.append(Finding(
                    line=line_of(m.start()), severity=severity, kind="language",
                    text=m.group(0), why=why, fix=fix,
                ))

        # A number stated as fact with nothing in its paragraph to trace it to.
        block_cited = bool(CITATION_MARKER.search(block))
        block_has_ci = bool(CI_MARKER.search(block))
        for m in NUMERIC.finditer(block):
            if not block_cited:
                findings.append(Finding(
                    line=line_of(m.start()), severity="high", kind="unreferenced",
                    text=m.group(0),
                    why="numeric claim with no citation anywhere in its paragraph",
                    fix="attach the source; reviewers stop at every number",
                ))
            if re.search(r"(HR|OR|RR)\s*[=:]?\s*\d?\.\d+", m.group(0), re.I) \
                    and not block_has_ci:
                findings.append(Finding(
                    line=line_of(m.start()), severity="medium", kind="precision",
                    text=m.group(0),
                    why="effect estimate without a confidence interval",
                    fix="a point estimate alone asserts precision the data do "
                        "not have",
                ))

    doc = {
        "approval_status_stated": bool(APPROVAL_MARKER.search(text)),
        "efficacy_content": bool(EFFICACY.search(text)),
        "safety_content": bool(FAIR_BALANCE.search(text)),
        "lines": len(lines),
    }
    return findings, doc


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", required=True, help="text or markdown content to audit")
    ap.add_argument("--format", default="report",
                    choices=["report", "matrix", "json"])
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"No such file: {path}", file=sys.stderr)
        return 2
    text = path.read_text(encoding="utf-8")
    findings, doc = audit(text)

    if args.format == "json":
        print(json.dumps(
            {"findings": [asdict(f) for f in findings], "document": doc}, indent=2
        ))
        return 1 if findings else 0

    if args.format == "matrix":
        print("# Claim-evidence matrix\n")
        print("Fill one row per assertion. The column that does the work is "
              "'supports as written?' — a real reference attached to a claim it "
              "does not support is the most common substantive review finding, "
              "and no script can detect it.\n")
        print("| # | Claim (verbatim) | Location | Type | Source | Tier | "
              "Supports as written? | Note |")
        print("| --- | --- | --- | --- | --- | --- | --- | --- |")
        seen = set()
        n = 0
        for f in findings:
            if f.kind not in ("unreferenced", "language") or f.severity != "high":
                continue
            key = (f.line, f.text.lower())
            if key in seen:
                continue
            seen.add(key)
            n += 1
            print(f"| {n} | {f.text} | line {f.line} | | | | | {f.why} |")
        if not n:
            print("| 1 | | | | | | | |")
        return 0

    # report
    high = [f for f in findings if f.severity == "high"]
    med = [f for f in findings if f.severity == "medium"]

    print(f"MLR pre-check — {path.name}\n")
    for f in sorted(findings, key=lambda x: (x.line, x.severity)):
        tag = "HIGH" if f.severity == "high" else "med "
        print(f"  {tag}  line {f.line}: \"{f.text}\"")
        print(f"        {f.why}")
        print(f"        → {f.fix}")

    print("\n--- document-level checks ---")
    if not doc["approval_status_stated"]:
        print("  HIGH  no approval-status statement found. State what is approved, "
              "in which jurisdiction, and that anything else is investigational.")
    else:
        print("  ok    approval-status language present (verify it is prominent, "
              "not small print)")

    if doc["efficacy_content"] and not doc["safety_content"]:
        print("  HIGH  efficacy content present with no safety content. Fair "
              "balance requires safety at comparable prominence in the same "
              "section, not an appendix.")
    elif doc["efficacy_content"]:
        print("  ok    both efficacy and safety content present (verify the "
              "prominence is comparable)")

    print(f"\n{len(high)} high · {len(med)} medium · {doc['lines']} lines checked")
    print(
        "\nThis found the mechanical problems only. It cannot tell you whether a\n"
        "cited source supports the claim attached to it — read the sources against\n"
        "the sentences. Do not describe this content as compliant, MLR-ready or\n"
        "approved; those are determinations made by people with accountability."
    )
    return 1 if high else 0


if __name__ == "__main__":
    raise SystemExit(main())
