---
name: medical-slide-deck
description: >-
  Build non-promotional medical slide decks — advisory board decks, MSL
  scientific presentations, congress readouts, medical-to-medical (M2M)
  presentations, internal data reviews and training material. Use whenever
  someone asks for slides, a deck, a presentation or a PowerPoint in a
  Medical Affairs context. Handles what makes a medical deck different from
  a commercial one: a reference on every data slide, the design named
  alongside every result, fair balance at comparable prominence, approval
  status stated, and a backup-slide set built from anticipated questions.
  Generates a real .pptx.
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
    - consulting-grade-design
    - deliverable-quality-review
  produces: Non-promotional medical slide deck (.pptx)
  deliverables: [pptx, pdf]
  python: [python-pptx>=1.0]
---

# Medical Slide Deck

A medical deck is not a commercial deck with the claims removed. It is built to
a different standard, and the differences are visible on every slide.

**Do not start here.** Build the deck once the analysis is done and reviewed.
Producing slides before the reasoning is finished is the most common failure in
this whole library — it yields a well-formatted document with nothing behind it,
and the format makes the emptiness harder to see.

## What makes a medical slide different

| | Commercial slide | Medical slide |
|---|---|---|
| Headline | The message | What the data show |
| Data | Selected to support | Presented with its design and limits |
| Comparison | Positioned favourably | Only where head-to-head evidence exists |
| Safety | Elsewhere in the deck | Alongside efficacy, comparable prominence |
| Citation | Sometimes | **Every data slide, every time** |
| Approval status | Assumed | Stated |
| Conclusion | Fixed in advance | Follows the evidence, including "unknown" |

**The headline test.** Write the slide title as what the data show, not as what
you want the audience to conclude. *"ORR 63% in triple-class-exposed patients
(single-arm, n=165)"* is a medical headline. *"Substantial activity in
heavily pretreated patients"* is an interpretation, and it belongs in the
speaker's mouth where it can be challenged, not printed as a title.

## Non-negotiables on every data slide

1. **Citation footnote.** Author, journal, year, and identifier. A data slide
   without a source cannot be reviewed and will come back from MLR.
2. **Design named.** In the title, subtitle, or footnote — never only in the
   backup. "Single-arm" and "randomised" have to be visible where the number is.
3. **N and the population.** A percentage without a denominator is not a result.
4. **Confidence intervals** wherever an estimate is shown.
5. **Evidence tier** where it is not a peer-reviewed publication —
   `[abstract]`, `[preprint]`, `[data on file]`.

## Structure

### Advisory board deck

The point of an advisory board is to get advice the company does not already
have. A deck that presents conclusions gets agreement, not advice — and an
advisory board convened to deliver a message is a promotional programme wearing
a medical badge.

```
Objectives            what we are asking them, and what we will do with it
Context               disease and treatment landscape — brief
The evidence          what is known, appraised, including what is weak
THE QUESTIONS         the substance. Open questions the company cannot answer.
Discussion prompts    per question, designed to surface disagreement
Backup                detail available if asked
```

Weight this toward questions. If the questions occupy fewer slides than the
data, reconsider what the meeting is for.

### MSL scientific presentation

```
Disease context       brief, calibrated to the audience
Unmet need            evidence-based, not assertion
The evidence          design, population, results with CIs, limitations
Safety                same prominence as efficacy
What remains unknown  the section that builds credibility
References
Backup                anticipated questions, with answers
```

### Congress readout deck

Follow `congress-intelligence`: what changed, why it matters, what to watch,
what we should do. Four sections. Resist the sixty-abstract summary.

### Backup slides

Build these from anticipated questions, not from leftover content. For each
question the audience is likely to ask, one slide with the appraised answer.
This is what separates a prepared presenter from a rehearsed one — and the
questions you cannot answer are worth a slide too, saying so.

## Building the file

Always through the bundled script — it installs python-pptx and matplotlib on
first use. Never hand-write a python-pptx script and never deliver the deck as
markdown: both produce the wall-of-text, default-styled slides this skill exists
to prevent.

```bash
python3 scripts/build_deck.py --example > deck.json        # worked spec
python3 scripts/build_deck.py --spec deck.json --out outputs/deck.pptx --preview outputs/preview
```

The spec is JSON (or a markdown draft where each `##` is a slide) so the content
is reviewable before it becomes a binary. Choose the slide type from the
content, not by habit — a deck of `bullets` slides is the failure:

| Content | Slide type |
|---|---|
| 2–4 headline numbers | `stats` (value, label, note; `style: safety` for AE numbers) |
| A comparison, trend or subgroup result | `chart` — native, editable column/bar/line; forest and KM via image; optional `bullets` panel |
| Values the reader must take away exactly | `table` (`highlight_row` for the row that matters) |
| Known vs unknown, efficacy vs safety, option A vs B | `two_column` |
| Advisory questions | `questions` |
| Milestones, a pathway, a process | `timeline`, `process` |
| One sentence the room must remember | `callout` |
| Agenda, section break, next steps | `agenda`, `section`, `closing` |

Every slide takes `design` (kicker: study design and N), `citation`, `takeaway`
(the so-what bar) and `notes`. The builder blocks a data, chart, table or stats
slide without a citation and a deck without approval status. It then checks
layout: text overflow, dense slides, tiny fonts, text-only decks, off-slide
shapes. **Open `outputs/preview/contact-sheet.png` and look at every slide**;
fix each `check` line and re-render until none remain. It cannot detect
promotional framing — that is `deliverable-quality-review`'s job and yours.

## Design that helps comprehension

Not decoration — these affect whether the science lands.

- **One idea per slide.** A slide making three points makes none.
- **Data legible from the back of the room.** 18pt minimum for data labels.
- **Do not truncate axes** on efficacy figures. See
  `data-visualization-for-medical`.
- **Colour is not the only encoding.** Roughly 8% of men have a colour vision
  deficiency; use pattern, position or direct labels as well.
- **Kaplan-Meier curves need numbers at risk.** A KM plot without them cannot be
  interpreted where it matters most — in the tail.
- **Tables over 6 rows** need a highlighted row or they will not be read.

The builder already carries the library's visual language — palette, accent
rule, kicker line, banded tables, stat cards. For the reasoning behind it, load
`consulting-grade-design`.

## Charts and imagery on slides

**A number that can be a chart should be a chart.** Use a `chart` slide for a
comparison, trend or distribution; for KM curves with numbers at risk use
`data-visualization-for-medical` and place the PNG with an `image` slide —
reserving `table` slides for the values a reader will want to take away exactly.
The citation and design statement still travel on the slide, because a chart
inherits every rule a table has.

**Images are welcome where data is not.** Title slides and section dividers
take generated or licensed imagery well — abstract, desaturated toward the
palette, never implying a clinical claim. If the runtime can generate images,
prompt in the register of "muted navy and teal scientific abstract, minimal,
editorial". Keep imagery off data slides entirely; next to a number, a
picture is either noise or an argument, and neither belongs there.

## Stage 4 — Challenge

Run `deliverable-quality-review`, then walk the deck slide by slide:

- Does every data slide carry a citation, an N, and the design?
- Is safety information present at comparable prominence to efficacy?
- Read every title aloud. Is any of them a conclusion rather than a finding?
- Is there a comparative claim anywhere without head-to-head data?
- Is approval status stated for every use discussed?
- Would this deck read the same if the product were a competitor's?
- Is the DRAFT marking still on the title slide?

<!-- ma-render:begin — generated by scripts/sync_renderer.py; edit the template there -->
## Deliverable format

Deliver a designed **PowerPoint deck (.pptx) plus a PDF copy**.
Build it with this skill's bundled engine. Markdown is for drafting only —
never hand over a .md file, and never hand-write a python-pptx or
python-docx script instead of the engine.

```bash
python3 scripts/ma_render.py bootstrap      # installs python-pptx, python-docx, matplotlib, reportlab
python3 scripts/ma_render.py example deck > spec.json   # spec format; or write a markdown draft
python3 scripts/ma_render.py deck spec.json --out outputs/<name>.pptx --preview outputs/preview
```

Turn numbers into `stats`/`chart` blocks and comparisons into tables or
`two_column` slides; put a source on every data element. Then open
`outputs/preview/contact-sheet.png`, fix every overflow, empty or text-only
page, and re-render. If a package cannot be installed the engine still
writes a real .docx or print-ready HTML and says what degraded.

`scripts/build_deck.py` wraps the engine and blocks a deck without approval status or a data slide without its citation — use it for medical decks.
<!-- ma-render:end -->

## Before you finish

Read `house-rules/medical-slide-deck.md`. Template, branding, mandatory slides,
and MLR routing are all organisation-specific — most companies have a required
deck template and a required safety slide, and this skill does not know yours.

Then run `mlr-review-readiness` before the deck goes to review.

## References

- `references/slide-patterns.md` — worked layouts for the recurring medical
  slide types, and the specific ways each one goes wrong.
