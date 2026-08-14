#!/usr/bin/env python3
"""Readability and jargon check for patient-facing material.

Treat the score as a smoke alarm, not a target. Readability formulas count
syllables and sentence length; they cannot tell whether the meaning survived
simplification. Text can score at grade 6 and still be incomprehensible, and
chopping sentences to hit a number often destroys the logical connections that
made a passage understandable.

Use it to find the passages worth rereading, then read them.

    S=skills/plain-language-summary/scripts/readability.py

    python3 $S --file summary.md
    python3 $S --file summary.md --target 8
    python3 $S --file summary.md --format json

No dependencies beyond the standard library.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VOWELS = "aeiouy"

# Terms that recur in trial summaries and are not everyday language. Flagged
# when used without a nearby explanation.
JARGON = {
    "progression-free survival": "how long people lived without the cancer growing",
    "overall survival": "how long people lived",
    "hazard ratio": "give the absolute numbers instead",
    "confidence interval": "the range the true value is likely to lie in",
    "statistically significant": "unlikely to be due to chance alone",
    "adverse event": "a health problem that happened during the study",
    "randomised": "put into groups by chance, like a coin toss",
    "randomized": "put into groups by chance, like a coin toss",
    "double-blind": "neither participants nor their doctors knew which treatment",
    "placebo": "a dummy treatment with no active medicine",
    "median": "the middle value — half were above it, half below",
    "efficacy": "how well it worked",
    "administered": "given",
    "titration": "gradually adjusting the dose",
    "refractory": "not responding to treatment",
    "relapsed": "the disease came back",
    "cohort": "group",
    "endpoint": "what the study measured",
    "prognosis": "the likely course of the illness",
    "contraindicated": "should not be used",
    "comorbidity": "another illness at the same time",
    "eligibility criteria": "who could take part",
    "subcutaneous": "under the skin",
    "intravenous": "into a vein",
    "monotherapy": "used on its own",
    "utilise": "use",
    "utilize": "use",
    "demonstrate": "show",
    "prior to": "before",
    "in order to": "to",
}

# Language that reads as advice. A lay summary describes findings; it does not
# tell anyone what to take.
ADVICE = re.compile(
    r"\b(you should|patients should|we recommend|is recommended|"
    r"talk to your doctor about (starting|switching|taking)|"
    r"ask your doctor for|consider (taking|switching))\b", re.I
)

# Relative-risk framing, which is uninterpretable to a lay reader and sounds
# far larger than the absolute change.
RELATIVE = re.compile(
    r"\b(reduc\w*\s+(the\s+)?risk\s+by|increas\w*\s+(the\s+)?risk\s+by|"
    r"\d+\s*%\s*(reduction|increase)\s*in\s*(the\s+)?risk|"
    r"\d+\s*%\s*(less|more)\s+likely|halved|doubled|tripled|"
    r"relative risk reduction)\b", re.I
)


def syllables(word: str) -> int:
    word = re.sub(r"[^a-z]", "", word.lower())
    if not word:
        return 0
    count, prev_vowel = 0, False
    for ch in word:
        is_vowel = ch in VOWELS
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if word.endswith("e") and count > 1 and not word.endswith(("le", "ee")):
        count -= 1
    return max(1, count)


def analyse(text: str) -> dict:
    body = re.sub(r"^#.*$", "", text, flags=re.M)          # headings
    # Note: hyphens are NOT stripped. "progression-free survival" and
    # "double-blind" are single terms, and splitting them hides the jargon.
    body = re.sub(r"[*_`>|#]", " ", body)                   # markdown noise
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", body) if s.strip()]
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", body)

    if not sentences or not words:
        return {"error": "no readable prose found"}

    syl = sum(syllables(w) for w in words)
    W, S = len(words), len(sentences)

    flesch = 206.835 - 1.015 * (W / S) - 84.6 * (syl / W)
    fk_grade = 0.39 * (W / S) + 11.8 * (syl / W) - 15.59
    polysyllabic = [w for w in words if syllables(w) >= 3]

    long_sentences = sorted(
        [(len(re.findall(r"[A-Za-z][A-Za-z'-]*", s)), s) for s in sentences],
        reverse=True,
    )[:5]

    lowered = body.lower()
    jargon_found = []
    for term, plain in JARGON.items():
        for m in re.finditer(re.escape(term), lowered):
            window = lowered[max(0, m.start() - 160): m.end() + 160]
            # Consider it explained if a plain gloss appears nearby.
            explained = any(
                tok in window for tok in plain.lower().split()[:3] if len(tok) > 4
            )
            jargon_found.append({"term": term, "suggestion": plain,
                                 "explained_nearby": explained})
            break

    return {
        "words": W,
        "sentences": S,
        "mean_sentence_length": round(W / S, 1),
        "polysyllabic_pct": round(100 * len(polysyllabic) / W, 1),
        "flesch_reading_ease": round(flesch, 1),
        "flesch_kincaid_grade": round(fk_grade, 1),
        "longest_sentences": [{"words": n, "text": s[:160]} for n, s in long_sentences],
        "jargon": jargon_found,
        "advice_phrases": [m.group(0) for m in ADVICE.finditer(body)],
        "relative_risk_phrases": [m.group(0) for m in RELATIVE.finditer(body)],
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", required=True)
    ap.add_argument("--target", type=float, default=8.0,
                    help="target Flesch-Kincaid grade level (default 8)")
    ap.add_argument("--format", default="report", choices=["report", "json"])
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"No such file: {path}", file=sys.stderr)
        return 2
    r = analyse(path.read_text(encoding="utf-8"))

    if "error" in r:
        print(r["error"], file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(r, indent=2))
        return 0

    print(f"Readability — {path.name}\n")
    print(f"  Flesch-Kincaid grade   {r['flesch_kincaid_grade']}  (target ≤ {args.target})")
    print(f"  Flesch Reading Ease    {r['flesch_reading_ease']}  (higher is easier; 60-70 is plain English)")
    print(f"  Mean sentence length   {r['mean_sentence_length']} words  (aim ≤ 20)")
    print(f"  Long words (3+ syll.)  {r['polysyllabic_pct']}%")
    print(f"  {r['words']} words in {r['sentences']} sentences")

    issues = 0
    if r["flesch_kincaid_grade"] > args.target:
        issues += 1
        print(f"\n  Above the target grade level. The longest sentences are usually "
              f"where the problem is:")
        for s in r["longest_sentences"][:3]:
            print(f"    {s['words']} words: \"{s['text']}...\"")

    unexplained = [j for j in r["jargon"] if not j["explained_nearby"]]
    if unexplained:
        issues += len(unexplained)
        print(f"\n  Unexplained technical terms ({len(unexplained)}):")
        for j in unexplained:
            print(f"    \"{j['term']}\" → {j['suggestion']}")

    if r["relative_risk_phrases"]:
        issues += len(r["relative_risk_phrases"])
        print("\n  Relative-risk framing found:")
        for p in r["relative_risk_phrases"]:
            print(f"    \"{p}\"")
        print("    Relative figures are uninterpretable to a lay reader and sound")
        print("    far larger than the change. Use absolute natural frequencies:")
        print("    \"out of 100 people, 4 had this instead of 8\", giving both arms.")

    if r["advice_phrases"]:
        issues += len(r["advice_phrases"])
        print("\n  Language that reads as treatment advice:")
        for p in r["advice_phrases"]:
            print(f"    \"{p}\"")
        print("    A lay summary describes what a study found. It does not tell")
        print("    anyone what to take. Direct the reader to their own clinician.")

    print(f"\n{issues} issue(s).")
    print(
        "\nThis is a smoke alarm, not a target. A formula counts syllables and\n"
        "sentence length; it cannot tell whether the meaning survived. Shortening\n"
        "sentences to hit a number often destroys the connections that made a\n"
        "passage understandable.\n"
        "\nThe check that matters most is not here: have a patient or patient\n"
        "advocate read it."
    )
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
