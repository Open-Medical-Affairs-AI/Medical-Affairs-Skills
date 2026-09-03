---
name: visual-abstract
description: >-
  Create visual abstracts and infographics that summarise a study or a body
  of evidence honestly. Use when a publication needs a visual abstract for a
  journal or social media, when a congress presentation needs a graphical
  summary, when patient-facing material needs a visual, or when someone asks
  for an infographic. Enforces the rules that stop a visual abstract
  overstating its study: the design is stated on the graphic, absolute
  numbers appear alongside relative ones, the sample size is visible, and a
  single-arm study never gets a comparative layout. Renders dependency-free
  SVG.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.1.0"
  tier: content
  maturity: beta
  requires:
    - medical-affairs-foundations
    - evidence-appraisal
    - capability-detection
  suggests:
    - consulting-grade-design
  produces: Visual abstract or infographic (SVG)
---

# Visual Abstract

A visual abstract is the most-shared and least-scrutinised output a publication
produces. It travels without its paper, gets screenshotted, and is read in three
seconds by people who will never open the full text.

That makes graphical honesty a bigger obligation here than anywhere else in the
library, not a smaller one.

## The rules

**1. State the design on the graphic.** "Single-arm, n=165" or "Randomised,
n=558". Not in a caption that will be cropped — on the image.

**2. A single-arm study never gets a comparative layout.** Two panels side by
side reads as a comparison whatever the labels say. One arm, one panel.

**3. Absolute numbers alongside relative ones.** "50% reduction" beside
"8 of 100 → 4 of 100". The relative figure alone is the standard way visual
abstracts mislead.

**4. Show the denominator.** Every percentage, every icon array.

**5. Endpoint type stated.** "Progression-free survival" not "outcomes". If it
is a surrogate, the word appears.

**6. Confidence intervals or a range.** A bare point estimate in a graphic
asserts precision the study does not have.

**7. Safety visible.** A visual abstract showing only efficacy fails fair
balance exactly as a slide would.

**8. Colour is not the only encoding.** Around 8% of men have a colour vision
deficiency, and these images get printed in greyscale.

## Formats

**Journal visual abstract** — usually a fixed aspect ratio, three panels:
population / intervention / findings. Check the journal's specification; many
prescribe dimensions and font sizes.

**Icon array** — the best way to show frequency to a non-specialist. 100 figures,
affected ones highlighted, two arrays side by side for a comparison. Pairs with
`plain-language-summary`.

**Evidence summary graphic** — for a body of evidence rather than one study.
Certainty must be shown per claim (`evidence-synthesis`), or the graphic
flattens strong and weak findings into the same visual weight. This is the
commonest failure in evidence infographics.

## Using it

```bash
S=skills/visual-abstract/scripts/visual_abstract.py

python3 $S --example > va.json
python3 $S --spec va.json --out abstract.svg
python3 $S icon-array --n 100 --affected 8 --comparator 4 --out icons.svg
```

SVG throughout — no dependencies, scales perfectly for print, and opens in
every browser. The builder refuses a comparative layout when the spec declares a
single-arm design.

## The look

The library's visual language (`consulting-grade-design`) applies with full
force here — palette, direct labels, message-first title — because a visual
abstract is judged in the first second. The integrity rules above still
outrank any aesthetic choice.

## Before you finish

Read `house-rules/visual-abstract.md`, then `mlr-review-readiness` — visual
abstracts go through review like any other external material, and they are
reviewed less carefully than they should be.
