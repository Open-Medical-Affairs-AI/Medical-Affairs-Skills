---
name: pdf-generation
description: >-
  Produce PDF deliverables — briefs, reports, standard response documents,
  one-pagers, evidence summaries, anything that must look the same for every
  reader and print predictably. Use when someone asks for a PDF, when a
  document is going to an external audience, when it must be printed, or
  when layout fidelity matters more than editability. Falls back to HTML
  with a print stylesheet when no PDF library is available, which loses
  nothing because every browser prints to PDF. Handles the draft marking on
  every page, document control, and references that survive pagination.
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
  produces: PDF deliverable (or print-ready HTML)
  python: [reportlab]
---

# PDF Generation

PDF is the format Medical Affairs uses when a document leaves the department:
standard response documents, briefs, evidence summaries, one-pagers. It looks
the same for everyone and it prints predictably.

## The honest position on the fallback

This is the output type where degrading costs almost nothing. **Every browser
prints to PDF.** HTML with a proper print stylesheet gives correct pagination,
running headers, and page numbers via CSS paged media.

So the notice should say what to do, not apologise:

> Delivered `brief.html`. Open it and print to PDF (Ctrl/Cmd-P → Save as PDF)
> for the distributable version. Pagination, headers and page numbers are set in
> the stylesheet, so the result matches what a PDF library would have produced.

## What a regulated PDF needs

- **The draft marking on every page**, not just the first. Pages get separated.
- **Page numbers as "page N of M"** — a reader must be able to tell whether they
  have the whole document.
- **Document control in the footer**: document ID, version, date, and the review
  date where one applies.
- **References that survive pagination.** A reference list broken mid-entry
  across a page break is a common and avoidable defect.
- **Approval status** on the first page where any product use is discussed.
- **No orphaned tables.** A table header on one page and its rows on the next is
  unreadable; keep them together.

## Using it

```bash
S=skills/pdf-generation/scripts/build_pdf.py

python3 $S --example > doc.json
python3 $S --spec doc.json --out brief.pdf
python3 $S --spec doc.json --out brief.pdf --html-only   # skip the PDF path
```

The spec is JSON so the content is reviewable before it becomes a binary. The
builder refuses to render without a draft marking and without document control
fields — both are the kind of thing that is noticed only after distribution.

## The look

Report covers, section pages and typography follow `consulting-grade-design`
— its palette, one-accent rule and message-first headings apply to print as
much as to slides. A PDF is the artefact most often forwarded upward, so it
is the one most often judged against expensive-firm output.

## Before you finish

Read `house-rules/pdf-generation.md`. Templates, letterhead, footer content and
document-control conventions are organisation-specific.
