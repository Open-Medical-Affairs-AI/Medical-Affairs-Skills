#!/usr/bin/env python3
"""Check a congress abstract against the submission rules before you submit.

Abstracts fail on rules, not on science: a character limit exceeded, a required
heading missing, "data will be presented" standing in for results. All of it is
checkable in advance, and discovering it late is where the science gets damaged
by hurried cutting.

    S=skills/congress-abstract-and-poster/scripts/abstract_check.py

    python3 $S --file abstract.md --limit 2500 --unit chars --structured
    python3 $S --file abstract.md --limit 300  --unit words
    python3 $S --file abstract.md --limit 2000 --unit chars --include-title

Character limits usually include spaces and often include the title. Confirm
against the congress's own rules — this tool checks what you tell it to check.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DEFAULT_HEADINGS = ["Background", "Methods", "Results", "Conclusion"]

# Things congress reviewers reject or score down.
RED_FLAGS = [
    (r"data will be (presented|shown|available)",
     "reviewers score this down and several congresses reject on it outright — "
     "an abstract without results is not an abstract"),
    (r"\b(results are|analysis is) (pending|ongoing|forthcoming)\b",
     "same problem: submit when you have results"),
    (r"\b(proven|superior|best[- ]in[- ]class|the only)\b",
     "comparative or promotional claim — congresses and MLR both reject these"),
    (r"\bwell[- ]tolerated\b",
     "absolute safety claim; give the rates instead"),
    (r"\bsafe\b",
     "absolute safety claim; give the rates instead"),
]

DESIGN_WORDS = re.compile(
    r"(randomi[sz]ed|single[- ]arm|double[- ]blind|open[- ]label|phase\s*[1-4I]{1,3}|"
    r"retrospective|prospective|observational|cohort|case[- ]control|"
    r"cross[- ]sectional|meta[- ]analysis|systematic review)", re.I
)
CI_RE = re.compile(r"(95%\s*CI|confidence interval)", re.I)
N_RE = re.compile(r"\b[Nn]\s*=\s*\d+")
SAFETY_RE = re.compile(
    r"(adverse|safety|toxicit|grade\s*[≥>]?\s*3|discontinu|serious)", re.I
)
PERCENT_RE = re.compile(r"\d+(\.\d+)?\s*%")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", required=True)
    ap.add_argument("--limit", type=int, required=True)
    ap.add_argument("--unit", default="words", choices=["words", "chars"])
    ap.add_argument("--include-title", action="store_true",
                    help="count the title line toward the limit (many congresses do)")
    ap.add_argument("--structured", action="store_true",
                    help="require the standard structured headings")
    ap.add_argument("--headings", default=",".join(DEFAULT_HEADINGS))
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"No such file: {path}", file=sys.stderr)
        return 2
    raw = path.read_text(encoding="utf-8")

    lines = [l for l in raw.splitlines()]
    title = ""
    body_lines = []
    for l in lines:
        if not title and l.strip().startswith("#"):
            title = l.lstrip("#").strip()
            continue
        body_lines.append(l)
    body = "\n".join(body_lines).strip()

    counted = (title + "\n" + body) if args.include_title else body
    if args.unit == "chars":
        count = len(counted)
        unit = "characters (including spaces)"
    else:
        count = len(re.findall(r"\S+", counted))
        unit = "words"

    over = count - args.limit
    print(f"Abstract check — {path.name}\n")
    print(f"  Title: {title or '(none found — add one as a level-1 heading)'}")
    print(f"  Count: {count} {unit} against a limit of {args.limit}"
          f"{' (title included)' if args.include_title else ' (title excluded)'}")
    if over > 0:
        print(f"  OVER BY {over}. Cut background first, then non-load-bearing "
              f"secondary endpoints, then every adjective. Do not cut the design, "
              f"N, the primary endpoint with its CI, or safety.")
    else:
        print(f"  {abs(over)} {unit} of headroom.")

    problems = 0

    if args.structured:
        print("\n  Structured headings:")
        for h in [x.strip() for x in args.headings.split(",") if x.strip()]:
            present = re.search(rf"^\s*\**{re.escape(h)}", body,
                                re.I | re.M) is not None
            print(f"    [{'x' if present else ' '}] {h}")
            if not present:
                problems += 1

    print("\n  Content checks:")
    checks = [
        ("study design named", bool(DESIGN_WORDS.search(body)),
         "'single-arm' or 'randomised' costs two words and determines what the "
         "abstract can claim"),
        ("N stated", bool(N_RE.search(body)),
         "a percentage without a denominator is not a result"),
        ("confidence interval present", bool(CI_RE.search(body)),
         "a point estimate alone asserts precision the data do not have"),
        ("safety data included", bool(SAFETY_RE.search(body)),
         "fair balance applies to abstracts"),
        ("numeric results present", bool(PERCENT_RE.search(body) or N_RE.search(body)),
         "an abstract without numbers will be scored down"),
    ]
    for label, ok, why in checks:
        print(f"    [{'x' if ok else ' '}] {label}")
        if not ok:
            print(f"         {why}")
            problems += 1

    flags = []
    for pattern, why in RED_FLAGS:
        for m in re.finditer(pattern, raw, re.I):
            flags.append((m.group(0), why))
    if flags:
        print("\n  Flagged language:")
        for text, why in flags:
            print(f"    \"{text}\" — {why}")
        problems += len(flags)

    print(f"\n{problems} issue(s). Limit exceeded: {'yes' if over > 0 else 'no'}.")
    print(
        "\nConfirm the limit, the counted elements, the structured headings, and\n"
        "the encore/prior-publication policy against the congress's own rules —\n"
        "this tool checks what you told it to check, and every congress differs."
    )
    return 1 if (problems or over > 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
