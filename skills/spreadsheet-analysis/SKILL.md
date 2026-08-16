---
name: spreadsheet-analysis
description: >-
  Analyse and produce spreadsheets — field insight exports, enquiry logs,
  publication trackers, evidence tables, budget allocations, congress
  abstract lists. Use when data arrives as .xlsx or .csv and needs
  summarising, cross-tabulating, de-duplicating or checking, and when the
  deliverable is itself a tracker someone will filter and sort. Handles what
  quietly corrupts clinical data analysis: multi-row headers, merged cells,
  inconsistent category spellings that split a count, dates stored as text,
  and percentages without denominators.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: content
  maturity: beta
  requires:
    - capability-detection
    - medical-affairs-foundations
  produces: Spreadsheet analysis or a generated workbook
  python: [openpyxl]
---

# Spreadsheet Analysis

Medical Affairs data arrives in spreadsheets: field insight exports, medical
information enquiry logs, publication trackers, evidence extraction tables. It
usually arrives messy, and the mess is not cosmetic — it changes the answer.

## The failures that change the answer

**Inconsistent categories split a count.** "CRS", "cytokine release syndrome"
and "Cytokine Release Sy." are one concept and three rows. The frequency that
mattered disappears into three small ones. Use
`medical-terminology-mapping`, and **publish the collapsing decisions** — a
count of 26 that silently merges three concepts is worse than no count.

**Multi-row headers.** Two header rows are normal in clinical tables and
default parsing reads the second as data. Check the first five rows before
trusting a header.

**Merged cells.** They read as one value plus blanks. A merged "Cohort A"
spanning six rows leaves five rows with no cohort.

**Dates as text.** Sorting `01/02/2026` and `1 Feb 2026` in the same column
produces nonsense. Normalise before any temporal analysis, and check whether the
source is day-first or month-first — getting this wrong is silent.

**Percentages without denominators.** A column of percentages with no N is not
analysable. Find the denominator or say you could not.

**Trailing junk.** Exports carry comment blocks, totals rows and blank
separators. A totals row included as data double-counts everything.

## Using it

```bash
S=skills/spreadsheet-analysis/scripts/sheets.py

python3 $S inspect  --file insights.xlsx          # structure and data-quality check
python3 $S summarise --file insights.csv --by setting,country
python3 $S dedupe   --file insights.csv --key contact_id --show-conflicts
python3 $S write    --spec table.json --out tracker.xlsx
```

**Run `inspect` first, always.** It reports header rows, merged cells, mixed
types per column, blank rows, candidate duplicate categories, and columns whose
values look like dates stored as text. Most of the value is here.

## Producing a spreadsheet

Trackers and evidence tables are legitimate deliverables. What makes them usable:

- **One header row.** Freeze it.
- **One concept per column.** Not "Result (95% CI)" — split estimate, lower,
  upper, so it can be sorted and plotted.
- **A denominator column** wherever a percentage appears.
- **A source column** on every row carrying a claim (`citation-integrity`).
- **An evidence-tier column** where rows mix peer-reviewed and abstract sources.
- **No colour-only encoding.** A red cell means nothing to a colour-blind reader
  or in a printout; add a status column.
- **The draft marking** in row 1 or a clearly-named first sheet.

## Fallback

Without `openpyxl`, `write` emits CSV plus a markdown table and says so. The
data survives; formulas, formatting and multiple sheets do not. With several
sheets it writes one CSV each plus a manifest, rather than flattening and losing
the structure.

## Before you finish

Read `house-rules/spreadsheet-analysis.md`. Tracker formats and required columns
are usually prescribed locally.
