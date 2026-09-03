---
name: data-visualization-for-medical
description: >-
  Produce clinical trial figures that are honest and interpretable — Kaplan-
  Meier curves with numbers at risk, forest plots, waterfall and spider
  plots, adverse event figures, PRISMA flow diagrams. Use whenever a Medical
  Affairs deliverable needs a chart of clinical data, or when reviewing
  whether an existing figure misleads. Enforces the graphical integrity
  rules that matter clinically: no axis truncation on efficacy figures,
  numbers at risk on every survival curve, censoring shown, denominators
  visible, and colour never the only encoding.
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
  produces: Publication-quality clinical figures
  python: [matplotlib>=3.7]
---

# Data Visualization for Medical

A figure is an argument. In clinical data the same numbers can be drawn to
support opposite readings, and most of the ways this happens are conventions
people follow without noticing.

The rules below are not aesthetic preferences. Each one exists because breaking
it changes what a clinician concludes.

## The integrity rules

**1. Do not truncate the y-axis on an efficacy figure.**
Starting a bar chart of response rates at 40% makes a 5-point difference look
like a doubling. On safety figures a truncated axis may be defensible to show
low-frequency events — say so on the figure when you do it.

**2. Every survival curve carries a numbers-at-risk table.**
The tail is where the audience is looking and where the data are thinnest. A
curve that appears to plateau on four remaining patients has said nothing, and
only the numbers-at-risk row reveals it. A KM plot without one is not
interpretable.

**3. Show censoring marks.**
Heavy early censoring changes how a curve should be read. Hiding the marks hides
that.

**4. Denominators are always visible.**
A percentage without an N is not a result. This applies to every bar, every
table cell, every waterfall.

**5. Colour is never the only encoding.**
Around 8% of men have a colour vision deficiency. Use pattern, position, direct
labels, or line style as well. Direct-labelling lines also removes a lookup step
for every reader.

**6. Show the confidence, not just the estimate.**
Error bars, shaded confidence bands, or intervals in the labels. A point
estimate drawn alone asserts a precision the data do not have.

**7. Consistent scales when figures will be compared.**
Two panels with different y-axes side by side will be read as though they
shared one.

## The figure types

```bash
S=skills/data-visualization-for-medical/scripts/clinical_figures.py

python3 $S km      --spec km.json      --out km.png
python3 $S forest  --spec forest.json  --out forest.png
python3 $S waterfall --spec wf.json    --out waterfall.png
python3 $S ae      --spec ae.json      --out ae.png

python3 $S km --example > km.json   # worked spec for any type
```

### Kaplan-Meier

For time-to-event outcomes. Requires: curves per arm, numbers at risk at each
tick, censoring marks. Include median with CI, HR with CI, event counts, and
median follow-up in the annotation.

**Check proportional hazards before quoting a single HR.** If the curves cross
or separate late — common with immunotherapy — one HR is a weighted average
describing no patient. Say so on the figure, and show RMST or a landmark
analysis.

### Forest plot

For subgroup analyses and meta-analyses. Requires: point estimate, confidence
interval, a reference line at the null, and — for subgroups — the **interaction
p-value**, not per-subgroup p-values.

**The most misread figure in oncology.** Twenty subgroups will produce one or
two apparently striking results by chance. Annotate the figure with the
interaction test and label subgroup findings as hypothesis-generating unless
pre-specified and powered.

### Waterfall

Best change from baseline per patient, ordered. Requires: reference lines at the
response thresholds, N, and a statement of who is included — waterfall plots
routinely show only evaluable patients, which quietly excludes those who
progressed or died before assessment. **State the exclusion**; it is the
difference between an honest figure and a flattering one.

### Spider / swimmer

Individual trajectories over time. Useful for durability and for showing
heterogeneity that a median conceals. Mark treatment discontinuation and
ongoing response.

### Adverse event table or figure

Any-grade and grade ≥3, with denominators, ordered by frequency. If a figure,
paired horizontal bars work better than stacked ones — stacking makes the
grade ≥3 segment hard to compare across rows.

### PRISMA flow diagram

For systematic reviews. The numbers must reconcile
(`systematic-literature-review`).

## Reviewing someone else's figure

Fast checks, in order of how often they find something:

1. **Does the y-axis start at zero?** If not, why not, and is it stated?
2. **Are there numbers at risk** on the survival curve?
3. **Is N shown**, for every group?
4. **Are confidence intervals shown**, or only point estimates?
5. **Are the axes on comparable panels identical?**
6. **Who is excluded** from a waterfall or responder analysis?
7. **Is a subgroup forest plot annotated with the interaction test?**
8. **Does the caption state the design?**

## Captions

Every figure caption states: design, population, N, endpoint and its type,
the effect measure, and the principal limitation. A figure that travels without
its caption — into a slide, a poster, a memo — must still be interpretable, so
put the design in the figure title as well.

## The look

Integrity rules decide what a figure says; `consulting-grade-design` decides
how it dresses. Its bundled theme module (ma_theme.py, in that skill's
scripts directory) applies the library palette and chart furniture to
matplotlib — import it before plotting rather than restyling by hand, and
let its `finish()` stamp the kicker (design + N), message-first title and
source line. Where the two ever appear to conflict, the integrity rules in
this skill win; honesty outranks elegance.

## Before you finish

Read `house-rules/data-visualization-for-medical.md`. Brand colours,
journal-specific figure requirements, and mandatory annotations vary.

Run `deliverable-quality-review` on the figures alongside the text — a figure
can overclaim just as a sentence can, and it is more persuasive when it does.
