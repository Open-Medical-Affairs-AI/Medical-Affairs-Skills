---
name: interactive-html-report
description: >-
  Build a self-contained HTML report that opens in any browser with no
  dependencies — evidence dashboards, insight reports with filterable
  tables, congress readouts, competitive landscapes, evidence gap trackers.
  Use when a deliverable carries more content than a document should, when
  the reader needs to filter or sort rather than read linearly, or when
  nothing else can be generated in the environment. Everything inlines into
  one file — no CDN, no external assets — so it can be emailed, opened
  offline and archived. This is the output type that always works.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.1.0"
  tier: content
  maturity: beta
  requires:
    - capability-detection
    - medical-affairs-foundations
  suggests:
    - citation-integrity
    - consulting-grade-design
  produces: Self-contained interactive HTML report
---

# Interactive HTML Report

The output type with no dependencies at all. If the filesystem is writable, this
works — which makes it the universal fallback as well as a good format in its
own right.

It earns its place when the reader needs to **do** something with the content:
filter fifty insights by setting, sort an evidence table by certainty, expand
the detail behind a claim without reading it all.

## Self-contained means self-contained

One file. No CDN, no external stylesheet, no web font, no remote image.

This is not fussiness. These documents are emailed, opened on aircraft, opened
inside networks that block outbound requests, and archived for years. A report
that renders as unstyled text because a CDN moved is a report nobody trusts
again.

Inline the CSS. Inline the JavaScript. Embed images as data URIs. Prefer SVG
generated inline (`data-visualization-for-medical`, `diagram-and-schema`) over
raster images.

## What works well here

**A filterable insight table.** Fifty insights with setting, country, confidence
and theme. The reader filters to what they own. Far better than a static table.

**Progressive disclosure of evidence.** The claim visible; the appraisal, design
and citation behind a disclosure triangle. Keeps the document readable without
losing the detail that makes it defensible.

**An evidence map.** Questions against certainty, colour and label, clickable
through to the studies.

**A congress readout.** The four sections visible, every abstract's detail
expandable underneath.

## Regulated-document requirements

Everything from `medical-affairs-foundations` applies, plus two specific to this
format:

**The draft marking must survive printing.** Fix it in the header with
`position: sticky`, and repeat it in an `@media print` block. An HTML report
printed without the marking has lost its only control.

**Nothing important behind interaction alone.** If safety data is only visible
after clicking a tab, a reader who prints the page never sees it — and that is
a fair balance failure. Collapsible detail is fine; collapsible *safety* is not.
The builder expands everything under `@media print` for this reason.

## Using it

```bash
S=skills/interactive-html-report/scripts/build_report.py

python3 $S --example > report.json
python3 $S --spec report.json --out insights.html
```

Section types: `summary`, `table` (sortable and filterable), `cards`,
`evidence` (with expandable appraisal), `figure` (inline SVG), `provenance`.

## Accessibility

- Real semantic HTML — `<table>`, `<th scope>`, headings in order
- Keyboard operable; anything clickable is focusable
- 4.5:1 contrast minimum
- Colour never the only encoding
- Works with JavaScript disabled: content present in the HTML, with JS adding
  filtering rather than supplying content

## The look

Style the report with `consulting-grade-design`: its palette as CSS custom
properties, Cloud (`#E8ECEF`) banding for tables, Teal (`#0E7C7B`) for the
single accent and interactive states, Oxblood (`#8C2F39`) reserved for
safety content. One accent per view — a dashboard where everything is
highlighted reads as a warning screen, not an analysis.

## Before you finish

Read `house-rules/interactive-html-report.md`. Some organisations do not permit
HTML attachments by email — in which case print to PDF and send that.
