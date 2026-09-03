---
name: executive-briefing
description: >-
  Distil any body of Medical Affairs work into the two-page brief or
  ten-slide read a leadership team actually absorbs — situation, what
  changed, what it means, what to decide, by when. Use when the audience
  is C-suite, a franchise head or a board; when someone asks for "the
  exec summary", "a briefing for leadership", "one-pager for the CMO";
  or when a long analysis needs a decision-forcing front end. Not for
  scientific audiences — they get the full analysis, not this.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: workflow
  maturity: beta
  requires:
    - medical-affairs-foundations
    - strategic-analysis
  suggests:
    - consulting-grade-design
    - medical-slide-deck
    - pdf-generation
    - deliverable-quality-review
  produces: Executive briefing (two-page memo or short deck)
---

# Executive Briefing

Leadership does not read Medical Affairs work; it reads the first page and
decides whether to trust the rest. This skill builds that first page — and
the discipline is subtraction, not summary.

**This is a front end, not a shortcut.** The full analysis must exist before
the briefing does. Distilling work that was never done produces confident
emptiness, which is worse than nothing because it forecloses the questions.

## The shape

Whether memo or deck, the same five moves in the same order:

1. **The situation, in two sentences.** What the reader already half-knows,
   sharpened. No background section — an executive briefing that opens with
   disease epidemiology has already lost its reader.
2. **What changed.** The new fact: the readout, the competitor move, the
   signal, the gap. Dated, sourced, design named. This is why the briefing
   exists now rather than last quarter.
3. **What it means for us.** The interpretation, with its confidence stated
   plainly — "we believe X, on single-arm evidence, and randomised data in
   2027 could reverse it". Executives handle uncertainty well; what they
   punish is discovering it later.
4. **The decision.** What is being asked of the reader: approve, fund,
   stop, choose between named options. If nothing is being asked, say "no
   decision required — awareness ahead of [event]" and mean it.
5. **What we would do next.** Owner, cost, date, and the first thing that
   would tell us we were wrong.

## The discipline

- **The answer goes first.** Not the method, not the journey. Pyramid
  principle: conclusion, then the two or three supports, then the evidence
  behind each — the reader stops when satisfied, at any depth.
- **Titles carry the argument.** Reading only the headings must deliver the
  whole case. "CagriSema's failure moves our comparator question forward a
  year", not "Competitive update".
- **One page of prose per topic; two pages total.** Length is the tax the
  writer pays for not deciding what matters. Everything else is appendix,
  and the appendix travels separately.
- **Numbers keep their clothes on.** An effect size travels with its design
  and N even here — "ORR 63% (single-arm, n=165)" costs eleven characters
  and prevents the misreading that a stripped number invites. The compliance
  furniture survives compression; that is non-negotiable.
- **No hedging chains.** "May potentially suggest" is three escapes in a
  row. State the claim at the confidence the evidence buys and name what
  would change it.

## Format

Memo (two pages, `pdf-generation`) when the reader is alone; deck (ten
slides, `medical-slide-deck`, one idea each) when the reading is a meeting.
Both take the `consulting-grade-design` language — the briefing is the
artefact most often judged against expensive-firm output, and it is judged
on looks first.

A deck built here keeps every rule of `medical-slide-deck`: citations on
data slides, approval status stated, the draft marking on. Executive
audience does not mean exempt audience.

## The challenge pass

Before delivery, run `deliverable-quality-review` and ask the two questions
this format is uniquely bad at surviving:

- **Would a sceptical CFO find the weakest link in five minutes?** If yes,
  name it in the briefing first — pre-empted weakness is credibility,
  discovered weakness is a lost audience.
- **Has compression created a claim the evidence does not make?** Shortening
  is the most common way an honest analysis becomes an overclaim. Check the
  briefing against the source analysis line by line.

## Before you finish

Read `house-rules/executive-briefing.md` — organisations have strong local
conventions on memo formats, and theirs win. End with the provenance line:
what analysis this distils, what was left out, and where the full version
lives.
