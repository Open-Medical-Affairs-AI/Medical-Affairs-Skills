---
name: plain-language-summary
description: >-
  Write plain language summaries of clinical research for patients and the
  public — trial results lay summaries, plain language summaries of
  publications, and patient-facing scientific material. Use when asked for a
  lay summary, patient summary or plain language version, and when meeting
  the EU Clinical Trials Regulation requirement for a results summary
  understandable to laypersons. Covers reading-level targets, translating
  clinical concepts without distorting them, absolute risk in natural
  frequencies, and the traps — false reassurance, false alarm, implied
  treatment advice — that make patient material harmful rather than merely
  unclear.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: content
  maturity: beta
  requires:
    - medical-affairs-foundations
    - evidence-appraisal
  suggests:
    - deliverable-quality-review
  produces: Plain language summary
---

# Plain Language Summary

Writing for patients is harder than writing for clinicians, and it is usually
given to whoever is free. The result is either a technical summary with the
jargon lightly sanded off, or a simplification that has quietly changed what the
evidence says.

Both are failures, and the second is the dangerous one.

## The obligation

**EU Clinical Trials Regulation 536/2014** requires a summary of results in
language understandable to laypersons, submitted to the EU database within
defined timelines. This is a legal obligation, not a communications nicety, and
it applies to trials regardless of outcome.

Beyond compliance: participants gave their time and accepted risk. Telling them
what was found is owed to them.

## The reading level target

Aim for **grade 6–8** reading level (UK: age 11–14). This is not condescension —
it is what health-literacy research supports for general-population materials,
and specialists read plain writing faster too.

```bash
python3 skills/plain-language-summary/scripts/readability.py --file summary.md
```

The script reports Flesch Reading Ease, Flesch-Kincaid grade level, sentence and
word length, and flags unexplained medical jargon against a list of terms that
recur in trial summaries.

**Treat the score as a smoke alarm, not a target.** Readability formulas count
syllables and sentence length; they cannot tell whether the meaning survived.
Text can score at grade 6 and still be incomprehensible, and shortening
sentences to hit a number often destroys the logical connections that made the
passage understandable. Use it to find the passages worth rereading.

## Translating without distorting

The discipline: **simplify the language, never the uncertainty.**

| Clinical | Plain — and still accurate |
|---|---|
| Progression-free survival | how long people lived without the cancer growing |
| Overall response rate | the proportion of people whose tumour shrank by a set amount |
| Hazard ratio 0.58 | in this study, people taking X were less likely to have their cancer grow at any given time — but see the absolute numbers below |
| Statistically significant | the difference was unlikely to be due to chance alone |
| Adverse event | a health problem that happened during the study, whether or not caused by the treatment |
| Randomised | people were put into groups by chance, like a coin toss, so the groups could be compared fairly |
| Double-blind | neither the participants nor their doctors knew which treatment they were getting |
| Placebo | a dummy treatment with no active medicine |
| Median | the middle value — half the people were above it and half below |

**"Median" is the one people get wrong most often.** A median PFS of 20 months
does not mean everyone had 20 months. Say that explicitly.

## Presenting risk and benefit

This is where lay summaries most often mislead, and the fixes are well
established.

**Use absolute numbers, not relative.** "Reduced the risk by 50%" is
uninterpretable and sounds enormous. "Out of 100 people, 4 had this problem
instead of 8" is interpretable.

**Use natural frequencies with a consistent denominator.** "3 out of 100 people"
throughout, not "3%" in one place and "1 in 33" in another.

**Give both arms.** A benefit or harm quoted for one group alone means nothing
without the comparison.

**Do not round away meaningful differences**, and do not imply precision the
data lack.

**Consider a visual.** An icon array — 100 figures with the affected ones
highlighted — communicates frequency better than any sentence. Use two arrays
side by side for the comparison.

## The three traps

**False reassurance.** Softening a serious risk to avoid alarming people.
"Some people had a reaction" where the label says 72% had cytokine release
syndrome is not kindness; it is withholding information someone needs.

**False alarm.** Listing every adverse event with equal weight, so a common mild
event and a rare serious one look the same. Give frequencies, and say which
matter.

**Implied treatment advice.** A lay summary describes what a study found. It
does not tell anyone what to take. Every summary ends by directing the reader to
their own healthcare professional, and no sentence in it should read as a
recommendation.

## Structure

For a trial results lay summary, the EU template expects roughly:

```
What was this study about?          the question, in one or two sentences
Why was it done?                    the problem it addressed
Who took part?                      how many, and who they were
What happened during the study?     design, in plain terms
What were the results?              main findings, absolute numbers, both arms
What side effects happened?         frequencies, with the serious ones flagged
What does this mean?                proportionate. Include what is still unknown.
Where can I find more?              registration number, publication, contacts
```

Check the current EU template and timelines before submitting — they are
prescriptive and have been revised.

For a plain language summary of a publication, journals increasingly request one
and specify a word limit. The same rules apply in less space.

## What good looks like

- Short sentences, one idea each
- Active voice — "we gave", not "was administered"
- Everyday words: "used" not "utilised", "showed" not "demonstrated"
- Every technical term explained on first use, or removed
- No abbreviations unless unavoidable, and then defined
- Direct address: "you", "we", "people in the study"
- Numbers as numerals — "4 people", not "four people"
- Nothing that reads as advice

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus:

- **Read it aloud.** Anything you stumble over needs rewriting.
- Has any uncertainty been lost in simplification?
- Are risks in absolute numbers, with both arms?
- Would a patient come away with a *correct* impression, not merely a
  favourable one?
- Does any sentence read as treatment advice?
- Is what remains unknown stated?
- **Has a patient or patient advocate actually read it?** This is the check that
  matters most, and no tool substitutes for it.

## Before you finish

Read `house-rules/plain-language-summary.md`. Templates, required sections,
reading-level targets, and patient-review processes are organisation-specific,
and EU submission templates are prescriptive.
