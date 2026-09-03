---
name: consulting-grade-design
description: >-
  The shared visual language every generated deliverable follows — palette,
  typography, chart furniture, layout and image use — so a deck, PDF, HTML
  report or figure leaves looking like it came from a top-tier advisory
  firm. Use whenever producing any visual deliverable: slides, documents,
  dashboards, infographics or charts. Also use when someone says the output
  looks unpolished, asks for "executive-ready" or "board-ready" material,
  or wants a consistent look across artefacts.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: content
  maturity: beta
  requires:
    - medical-affairs-foundations
    - capability-detection
  suggests:
    - data-visualization-for-medical
    - medical-slide-deck
    - interactive-html-report
    - pdf-generation
  produces: Design system applied across every generated deliverable
  python: [matplotlib>=3.7]
---

# Consulting-Grade Design

The analysis earns the trust; the design decides whether anyone reads far
enough to find it. A Medical Affairs deliverable competes for the same ten
minutes of a leadership team's attention as work from expensive advisory
firms, and it should not lose that comparison on looks.

Design here is in service of the content, never a substitute for it. A
beautiful deck built on thin analysis is the characteristic AI failure in this
domain — run the analysis first, then apply this skill to how it is shown.

## The palette

One ink, one accent, one reserved warning colour. Restraint is the look.

| Role | Hex | Use |
|---|---|---|
| Ink | `#12283A` | Titles, primary data series, body headings |
| Slate | `#5B6B79` | Secondary text, axes, captions, muted series |
| Teal (accent) | `#0E7C7B` | The one thing the reader should look at |
| Gold | `#C89B3C` | Callouts and highlights, sparingly |
| Oxblood | `#8C2F39` | Safety findings and warnings — reserved, never decorative |
| Cloud | `#E8ECEF` | Gridlines, panel fills, table banding |

Two rules carry most of the value. **One accent per artefact**: teal points at
the finding; if everything is highlighted, nothing is. **Oxblood means
safety**: once a reader learns that red-brown marks safety content, it must
never mean anything else.

## Typography and layout

- Titles are findings, not topics: "Grade ≥3 CRS remained under 1%", never
  "Safety results". A reader skimming only the titles gets the argument.
- A small uppercase **kicker line** above the title carries the study design
  and N — the content the figure must not travel without.
- Generous margins. If a slide feels full, it holds two slides' content.
- Left-align nearly everything. Centring is for title slides.
- One idea per slide or panel; the appendix exists for the rest.

## Charts

`scripts/ma_theme.py` applies all of this to matplotlib and is the single
source of the chart look — import it rather than restyling by hand:

```bash
python3 scripts/ma_theme.py --gallery out/   # synthetic-data samples
```

```python
import sys; sys.path.insert(0, "skills/consulting-grade-design/scripts")
import ma_theme
fig, ax = ma_theme.new_figure()
# ... plot with ma_theme.ARMS colours ...
ma_theme.finish(ax, title="ORR attenuates by line of therapy",
                kicker="SINGLE-ARM PHASE 2 · N=165",
                source="Author A, et al. J Med 2026. PMID 12345678")
ma_theme.save(fig, "figure.png")
```

The furniture it stamps — horizontal gridlines only, no chart borders, direct
series labels instead of legends where the data allow, a source line under
every chart — is the consulting look. What it deliberately does not override:
the graphical-integrity rules in `data-visualization-for-medical`. Zero-based
efficacy axes, numbers at risk, visible denominators and censoring marks are
clinical honesty requirements and outrank any aesthetic choice.

Prefer the chart forms consultants reach for because they carry an argument:
slope charts for before/after, ordered horizontal bars for rankings, small
multiples over one crowded panel, a single highlighted series against muted
comparators. Avoid pies, 3-D anything, and dual y-axes.

## Images

Generated or stock imagery is welcome on **title slides, section dividers and
report covers** — and almost nowhere else. An image next to data competes
with the data.

- Abstract, scientific, restrained: molecular surfaces, tissue microscopy
  tones, muted laboratory scenes. Desaturate toward the palette; a full-colour
  stock photo breaks the room's quiet.
- Never place text on a busy image without a solid ink-colour panel behind it.
- Never use imagery that implies a clinical claim — a smiling patient next to
  efficacy data is a promotional device, not decoration.
- If the runtime can generate images, prompt for "muted navy and teal
  scientific abstract, minimal, editorial" rather than literal renderings of
  the disease or product.

## Tables

Banded rows in Cloud, no vertical rules, headers in Ink bold, numbers
right-aligned, units in the header not the cells. A table with more than
seven rows on a slide is an appendix table being shown too early.

## What this skill never touches

The compliance furniture is not styling and survives every design choice:
the draft marking, citations on data slides, design-and-N statements,
approval status, and the provenance appendix. A deliverable may be beautiful
and must still be traceable.

## Before you finish

Read `house-rules/consulting-grade-design.md` — adopting organisations
replace this palette with their brand system, and their rules win.

Then look at the artefact the way a sceptical partner would: is there one
message per page, does the accent point at it, would the titles alone carry
the argument, and does anything decorative sit next to a number?
