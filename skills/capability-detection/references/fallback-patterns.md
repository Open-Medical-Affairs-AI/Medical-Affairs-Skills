# Fallback Patterns

Worked tier-3 renderers for each output type, and what each one actually loses.
Read this when writing a new content skill or extending an existing one.

---

## The shape every generator follows

```python
def _have(module: str) -> bool:
    try:
        __import__(module)
        return True
    except ImportError:
        return False

if _have("pptx"):
    build_pptx(spec, out)                    # tier 2
    return 0

write_markdown(out.with_suffix(".md"), spec) # tier 3
write_spec(out.with_suffix(".json"), spec)   # so tier 2 can be reached later
print(DEGRADATION_NOTICE)
return 0                                     # a degraded output is a SUCCESS
```

Three things to get right:

**Exit zero.** Otherwise the calling agent reports failure to someone who could
have had the content.

**Emit the spec alongside the fallback.** It lets whoever has the library
regenerate the real artefact without redoing any thinking — one `pip install`
and one command.

**Keep the check inline.** About twelve lines. `capability-detection` owns the
full diagnostic, but a copied skill directory must still work on its own.

---

## Deck → markdown + build spec

One `##` section per slide, carrying title, slide type, design statement, the
table or bullets, the citation footnote, and the speaker notes.

**Loses:** slide layout, theming.
**Keeps:** everything else — and for a review pass this is often easier to read
than the deck, because a reviewer can search it.

`skills/medical-slide-deck/scripts/build_deck.py::render_markdown`

---

## Poster → printable HTML

The case where tier 3 arguably beats tier 2. Physical dimensions go into
`@page { size: 48in 36in }` and type sizes stay in real points, so the two-metre
legibility rule is preserved exactly. Any browser prints it correctly, and
print-to-PDF is what most print shops want anyway.

**Loses:** nothing meaningful.
**Keeps:** size, columns, type hierarchy, takeaway box, disclosures.

`skills/congress-abstract-and-poster/scripts/build_poster.py::render_html`

---

## Manuscript → markdown

Title page, authors with their ICMJE criteria, structured abstract, IMRaD body,
the full statements block (ethics, funding, writing support, conflicts, data
sharing), and references.

**Loses:** Word styling and tracked changes.
**Keeps:** every element a journal requires. Most journals accept a plain
submission.

`skills/scientific-manuscript/scripts/build_manuscript.py::render_markdown`

---

## Figures → hand-written SVG + data table

A Kaplan-Meier curve is line segments. A forest plot is lines and circles. A
waterfall is rectangles. None of it needs a plotting library, and SVG scales
perfectly for print — which matters for posters.

**Loses:** essentially nothing for the figure types Medical Affairs uses.
Complex statistical plots would simplify.
**Keeps:** the full un-truncated axis, censoring marks, **numbers at risk**,
denominators, annotations.

The data table ships alongside deliberately. A figure can be misread; a table
cannot be read as more than it says.

`skills/data-visualization-for-medical/scripts/svg_fallback.py`

---

## Spreadsheet → CSV + markdown table

**Loses:** formulas, formatting, multiple sheets, charts.
**Keeps:** the data.

With several sheets, write one CSV per sheet plus a manifest listing them,
rather than flattening and losing the structure.

---

## PDF → HTML with a print stylesheet

**Loses:** nothing. Every browser prints to PDF.

Use `@media print` and `@page` for pagination. Say in the notice that the reader
should print-to-PDF, or they will assume the PDF failed.

---

## Reading a PDF → the honest exception

The one case where content genuinely cannot be recovered. If no PDF reader is
importable, the text is not obtainable and no fallback fixes that.

**Do not guess at the contents.** Say what happened and what would fix it:

> I cannot read this PDF — no PDF library is available in this environment
> (`pip install pypdf` would fix it). Options: paste the text directly, or give
> me the DOI/PMID and I will retrieve the metadata and abstract from PubMed
> instead.

Offering the specific alternative matters. "I can't read PDFs" ends the
conversation; naming two ways forward does not.

---

## What must survive every tier

If a fallback cannot carry one of these, the fallback is wrong — emit a
different format rather than dropping it.

- Every claim with its citation
- Study design named beside every result
- Confidence intervals
- Denominators
- Numbers at risk on a survival curve
- Safety data and fair balance
- Approval status statements
- The DRAFT marking
- The provenance appendix

A survival curve rendered without numbers at risk is not degraded, it is
**misleading**. Emit the data table instead and say why.

---

## Testing a new fallback

`scripts/selftest_fallbacks.py` runs each generator with its library hidden and
asserts four things: exit 0, a file was written, the notice is present and
complete, and the substantive content survived.

Add a `Case` when you add a generator. The `must_survive` tuple is the important
field — list the citation, the design statement, the denominator and the draft
marking. A fallback that produces a polite empty shell is worse than a crash,
because it looks like it worked.
