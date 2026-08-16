---
name: document-ingestion
description: >-
  Read documents someone has given you — PDF, Word, PowerPoint, Excel, CSV.
  Use whenever a user references, uploads, attaches or points at a file you
  need to understand: a competitor's publication, a congress abstract book,
  a protocol, a field insight export, an advisory board transcript, a label
  PDF. Extracts text, tables and structure, reports what it could NOT read
  rather than guessing, and runs the mandatory adverse event scan over
  anything human-sourced. Load this before any skill that needs to analyse a
  file.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: content
  maturity: beta
  requires:
    - medical-affairs-foundations
    - capability-detection
  produces: Extracted document text, tables and structure
  python: [pypdf, pdfplumber, python-docx, python-pptx, openpyxl]
---

# Document Ingestion

Almost every real Medical Affairs task starts with a file somebody sends you.
A competitor's paper as a PDF. The abstract book. A protocol. Last year's
advisory board deck. A field insight export from the CRM.

Nothing else in this library can read those. This skill is the front door.

## The rule that matters most

**Never guess at content you could not read.**

If a PDF is a scanned image and no OCR is available, you do not know what it
says. Producing a plausible summary of a document you could not open is the
single most damaging failure available here, because it is invisible — the
output looks exactly like a real one.

Say what you could not read, and offer a route forward.

## Reading a file

```bash
S=skills/document-ingestion/scripts/ingest.py

python3 $S --file paper.pdf                    # text + structure
python3 $S --file paper.pdf --tables           # try table extraction too
python3 $S --file deck.pptx --format json      # per-slide, machine-readable
python3 $S --file insights.xlsx --sheet 2
python3 $S --dir ./uploads                     # everything in a folder
python3 $S --file paper.pdf --scan-safety      # AE/PQC scan over the text
```

The script reports, for every file: what it extracted, **what it could not**,
and which extraction path it used. That last part matters — text pulled from a
PDF's embedded layer is reliable; text from a layout heuristic is not, and you
should treat numbers from it with suspicion.

## What each format gives you, and what it hides

| Format | Reliable | Treat with caution |
|---|---|---|
| **PDF (digital)** | Body text via the embedded text layer | Tables — column structure is inferred, not stored. Multi-column layouts interleave. Figures are images; their content is invisible. |
| **PDF (scanned)** | Nothing without OCR | Everything. Say so. |
| **DOCX** | Text, headings, tables, comments | Tracked changes may or may not be resolved — check which version you have |
| **PPTX** | Slide text, speaker notes, tables | Text inside images is invisible. Grouped shapes can read out of order. |
| **XLSX** | Cell values, sheet names | Formulas evaluate to their cached value; merged cells and multi-row headers confuse naive parsing |
| **CSV** | The data | Encoding and delimiter guessing; a leading comment block breaks header detection |

**The recurring trap is PDF tables.** A results table extracted from a PDF can
silently misalign a column, which turns a hazard ratio into a confidence
interval bound. Whenever a number matters, check it against the rendered
document rather than trusting extraction. Say in your provenance which numbers
you verified by eye.

## The safety scan is mandatory

Any human-sourced document — advisory board transcripts, field note exports,
medical information logs, investigator correspondence, meeting minutes — gets
the adverse event, product complaint and special situation scan from
`medical-affairs-foundations` **as it is read**, before analysis.

```bash
python3 $S --file advisory-transcript.docx --scan-safety
```

The scan is a keyword-and-pattern aid, not a control. It will miss things. Say
so, and say that the human's reporting clock started when the document reached
them.

Published literature and regulatory documents do not need the scan — a safety
table in a paper is literature, not a case report. Individual case reports in
the literature about your own product **do** have literature-monitoring
implications; route those to PV.

## When you cannot read it

Be specific about the failure and offer routes:

> I could not read `appraisal.pdf` — it is a scanned image with no text layer,
> and no OCR is available here (`pip install pytesseract` plus the tesseract
> binary would fix it).
>
> Alternatives: paste the relevant section as text; or if it is a published
> paper, give me the DOI or PMID and I will pull the abstract and metadata from
> PubMed; or tell me which pages matter and I will say what I would look for.

Never fill the gap with something plausible. "I could not read this" is a
completely acceptable outcome and a much better one than a confident
fabrication.

## After extraction

Extraction is not analysis. Hand the text on:

- A publication → `evidence-appraisal`, then `citation-integrity` to verify it
  is what it claims to be
- A congress abstract book → `congress-intelligence`
- A field insight export → `field-insight-synthesis`
- A competitor deck or press release → `competitive-intelligence`
- A label PDF → cross-check against `regulatory-label-intelligence`
- An HTA appraisal → `payer-value-dossier`

**Verify what you extracted actually is what it claims to be.** A PDF titled
`NEJM_teclistamab.pdf` may be a preprint, a poster, or a different paper
entirely. Check the identifiers in the text against PubMed
(`citation-integrity`) before citing anything from it.

## Provenance

Record for every file: filename, format, extraction path used, pages or sheets
read, what failed, and which numbers you verified against the rendered
document.

```markdown
**Documents read**
- `competitor-paper.pdf` — 12 pages, digital text layer (pypdf). Tables 2 and 3
  extracted with pdfplumber; **HR values in Table 3 verified by eye against the
  rendered PDF**. Figure 2 is an image — contents not read.
- `abstracts.pdf` — pages 1–4 only; pages 5+ are scanned images, not read.
- `insights.xlsx` — sheet "Q2 2026", 312 rows, 8 columns. Merged header row
  handled manually.
```

## Data handling

A file someone uploads may contain more than they intended — patient
identifiers in a case discussion, another company's confidential material,
personal data in interaction notes.

If you encounter apparent patient-identifying information, **stop, say so, and
do not reproduce it** in any output. Quote clinical detail for a safety finding
if needed, with direct identifiers redacted.

## Before you finish

Read `house-rules/document-ingestion.md`. Some organisations restrict which
document types may be processed by an AI system at all.

## References

- `references/extraction-notes.md` — per-format behaviour, the failure modes
  that produce plausible-but-wrong output, and how to sanity-check a table.
