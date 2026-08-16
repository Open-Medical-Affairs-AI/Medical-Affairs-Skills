# Extraction Notes — Per-Format Behaviour and Failure Modes

The failures that matter here are the ones that produce plausible-but-wrong
output, because they are invisible. A crashed extraction is obvious; a table
with one column shifted is not.

---

## PDF

**Two completely different problems wear the same file extension.**

*Digital PDFs* carry an embedded text layer. Extraction is reliable for body
text and unreliable for anything positional.

*Scanned PDFs* are images. There is no text. Without OCR you do not know what
the document says, and no amount of effort changes that — say so and stop.

Tell them apart by extracting page 1: empty output from a page that visibly has
text means it is scanned.

### Tables are the danger

**PDF does not store tables.** It stores glyphs at coordinates. Every extractor
reconstructs the grid from spacing, and every reconstruction can be wrong.

The specific failure: a column shifts by one, so a value from the CI column
lands in the estimate column. The output looks entirely normal. In a clinical
results table that turns `HR 0.58 (0.47–0.72)` into `HR 0.47`.

**Verify by eye any number that will appear in a deliverable**, and record in
your provenance which ones you checked. This is not optional diligence; it is
the difference between an extraction and a guess.

### Other PDF traps

- **Multi-column layouts interleave.** Two-column journal articles extract as
  alternating fragments unless the extractor is layout-aware. Read the first
  paragraph — if it is nonsense, this is why.
- **Figures are images.** Their content, including any data labels, is invisible.
- **Headers, footers and line numbers** interleave with body text.
- **Ligatures and hyphenation.** "ﬁ" may extract as one glyph; words broken
  across lines may keep the hyphen. Both break naive search.
- **Superscript reference markers** attach to the preceding word: "myeloma12".

`pdfplumber` handles layout and tables better than `pypdf`. `pypdf` is lighter
and adequate for flowing text.

---

## DOCX

Generally reliable. Two things to watch:

**Tracked changes.** A `.docx` can contain both the original and the revision.
Extraction returns the stored state, which may not be what the sender sees on
screen. Confirm which version you have before quoting from a document under
revision.

**Comments.** Often the most interesting content in a review document, and
easily missed — they live outside the main body.

Tables extract reliably because DOCX genuinely stores table structure.

---

## PPTX

**Shape order is not reading order.** Shapes are stored in z-order, which
usually approximates reading order and sometimes does not, particularly with
grouped shapes and text boxes added during editing. If sequence matters, check.

**Text inside images is invisible.** Decks frequently contain a screenshot of a
results table. That data is not extractable.

**Speaker notes are frequently the substance.** The slide says "ORR 63%"; the
notes say "single-arm, do not compare to competitor data". Always extract them.

---

## XLSX

**Formulas extract as cached values.** If the workbook was never recalculated
after its inputs changed, those values are stale — and there is no way to tell
from the file.

**Merged cells** return the value once and blanks for the rest of the span. A
merged "Cohort A" across six rows leaves five rows with no cohort.

**Multi-row headers** are normal in clinical tables and break naive parsing.

**Dates** may be real dates, text, or Excel serial numbers, sometimes in the
same column. Day-first versus month-first is silent and unrecoverable without
context.

**Hidden rows, columns and sheets** extract like any other. That is usually what
you want and occasionally a surprise.

---

## CSV

**Encoding.** UTF-8 is not universal; Windows exports are often cp1252. Mojibake
in names is the symptom.

**Delimiter.** Comma, semicolon (common in European locales where comma is the
decimal separator), tab, pipe. Sniff it.

**Leading comment blocks** are common in system exports and break header
detection. Skip lines starting with `#` before parsing.

**Embedded newlines** inside quoted fields — free-text observation columns are
full of them. Use a real CSV parser, never `split(",")`.

**Totals rows** at the bottom get read as data and double-count everything.

---

## A checklist before you trust an extraction

1. Does the first paragraph read as sense, or as interleaved fragments?
2. Does the row count match what the document appears to contain?
3. Do the column headers match the first data row's shape?
4. Pick three numbers that matter — do they match the rendered document?
5. Are there pages, sheets or slides you did not read? Say which.
6. Is anything obviously missing — a results table, a figure, an appendix?

Record the answers in the provenance. A reader who knows what you verified can
trust the rest; a reader who does not has to re-check everything.
