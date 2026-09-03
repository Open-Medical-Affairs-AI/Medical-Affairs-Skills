---
name: congress-abstract-and-poster
description: >-
  Write congress abstracts that fit the submission rules and build the
  posters that follow them. Use when preparing a submission to ASCO, ASH,
  ESMO, EHA, AAD, ACR, ADA, ACC or any medical congress, when an abstract is
  over the word limit, or when preparing a poster or encore presentation.
  Handles structured formats, the character limits that cause late
  rejections, late-breaker criteria, embargo and prior-publication rules,
  and poster layout built to be read from two metres away. Generates a real
  .pptx at the congress's physical dimensions.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.1.0"
  tier: content
  maturity: beta
  requires:
    - medical-affairs-foundations
    - citation-integrity
    - capability-detection
  suggests:
    - evidence-appraisal
    - data-visualization-for-medical
    - deliverable-quality-review
    - consulting-grade-design
  produces: Congress abstract and poster (.pptx)
  python: [python-pptx>=1.0]
---

# Congress Abstract and Poster

Two artefacts, one submission, and two different failure modes. Abstracts fail
on rules — a limit exceeded, a deadline missed, a prior-publication violation.
Posters fail on legibility — nobody reads them.

## The abstract

### Rules first, writing second

Get the submission rules **before** drafting. Every congress differs, and
rewriting to a limit you discovered late is where the science gets damaged.

Check and record: word or character limit and whether it includes the title,
authors, and table; structured vs unstructured, and the required headings;
whether tables and figures are permitted and how they count; author limits;
the encore and prior-publication policy; late-breaker criteria and deadline;
embargo terms.

**Character limits usually include spaces, and often include the title.** This
catches people out routinely.

```bash
S=skills/congress-abstract-and-poster/scripts/abstract_check.py

python3 $S --file abstract.md --limit 2500 --unit chars --structured
python3 $S --file abstract.md --limit 300 --unit words
```

The checker counts against the limit, verifies the required headings are
present, and flags the things reviewers reject: absent numbers, missing
denominators, conclusions the design does not support, and "data will be
presented" as a substitute for results.

### Writing to a hard limit

A congress abstract has room for roughly: one sentence of background, two of
methods, the results, and one conclusion. Everything else is cut.

**What must survive the cut:**

- **The design.** "Single-arm" or "randomised" costs two words and determines
  what the abstract can claim.
- **N**, and the population definition.
- **The primary endpoint and its result, with a confidence interval.**
- **Safety**, at least the serious events and discontinuations.
- **A conclusion proportionate to the design.**

**What to cut first:** background beyond one sentence, methodological detail
that does not change interpretation, secondary endpoints that are not
load-bearing, and any adjective.

**Never write "data will be presented at the meeting"** in place of results.
Reviewers score it down, and several congresses reject on it outright.

### The conclusion sentence

Where abstracts most often overclaim, because it is written last and to a word
budget. A single-arm study concludes that a response rate was observed, not that
a treatment is effective. `evidence-appraisal` applies here exactly as it does
in a manuscript.

### Encore and prior publication

Most congresses restrict material already presented or published. Encore rules
vary — some permit it with disclosure, some prohibit it. Getting this wrong can
mean withdrawal after acceptance, which is worse than not submitting.

Check the specific congress's policy and disclose prior presentation where
required.

## The poster

### The two-metre rule

A poster is read standing up, from about two metres, in a crowded hall, by
someone deciding in three seconds whether to stop. Design for that reader, not
for the person who will download the PDF.

- **Title legible from five metres.** 72–100pt.
- **Body text 24pt minimum.** Not 18pt because the content did not fit — cut
  the content.
- **Figures large.** A poster with one clear figure beats one with four small
  ones.
- **The conclusion visible without reading the poster.** Many posters put a
  single takeaway box at the top; it is the most effective layout decision
  available.
- **Whitespace.** A full poster is an unread poster. Aim for 30–40% empty.

### Layout

Three or four columns, reading left to right. Standard flow: background →
methods → results → conclusions, with results occupying the most space by a
wide margin.

Include a QR code to the full data or the publication. It is the single most
useful addition of the last decade and costs nothing.

### Building it

```bash
S=skills/congress-abstract-and-poster/scripts/build_poster.py

python3 $S --example > poster.json
python3 $S --spec poster.json --out poster.pptx
```

**Confirm the physical dimensions with the congress and the printer before
building.** There is no universal poster size, and the specification differs
between congresses and sometimes between sessions. The builder takes width and
height in inches and warns when the requested text sizes will not be legible at
that size.

The builder enforces the minimum font sizes and refuses to render body text
below the legibility threshold — the most common poster defect, and one that
cannot be fixed at the venue.

## Compliance

Everything in `medical-affairs-foundations` applies. Specifically:

- Disclosure of funding and author conflicts, on the poster
- Approval status stated where an unapproved use is discussed
- Fair balance — safety data on the poster, not only in the abstract
- Every data element traceable to the source
- Embargo respected; do not circulate before the congress releases it

## Stage 4 — Challenge

- Does the conclusion match the design?
- Is the primary endpoint the headline, or has a secondary been promoted?
- Are confidence intervals present?
- Is safety on the poster?
- Would this be legible from two metres? Print a page at 25% and look at it.
- Is every number traceable to the source data?

Run `deliverable-quality-review` and `mlr-review-readiness`.

## The look

Posters take the `consulting-grade-design` language: ink headings, one teal
accent guiding the read path, generous white space over dense panels, and
charts themed through its `ma_theme.py`. A poster is read at two metres for
ten seconds before anyone steps closer — the design decides whether they do.

## Before you finish

Read `house-rules/congress-abstract-and-poster.md`. Templates, branding, review
routes, and internal submission deadlines — usually well before the congress
deadline — are organisation-specific.
