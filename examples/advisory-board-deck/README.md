# Exemplar — advisory board deck

**Everything in this directory is SYNTHETIC.** The product, the molecule, the
numbers, the citations: all invented, and every figure and slide says so.
This is a design exemplar showing what the library's output looks like when
`medical-slide-deck`, `data-visualization-for-medical` and
`consulting-grade-design` run together — not a clinical document.

## What it demonstrates

- **The consulting-grade look.** Ink/teal palette, accent bars, kicker lines
  carrying design and N, banded tables, message-first titles, a generated
  title-slide backdrop sitting under an ink scrim.
- **Charts as first-class slides.** Four matplotlib figures themed by
  `ma_theme.py`: a KM-style curve **with numbers at risk and censoring
  marks**, a subgroup forest plot **annotated with the interaction p-value**,
  paired AE bars with the reserved safety colour, and an evidence-maturity
  chart.
- **The compliance furniture surviving the design.** Draft marking on every
  slide, citation line on every data slide, approval status on the title
  slide, and a "what remains unknown" slide at full prominence.

## Rebuild it

```bash
pip install matplotlib python-pptx
python3 examples/advisory-board-deck/make_figures.py
python3 skills/medical-slide-deck/scripts/build_deck.py \
    --spec examples/advisory-board-deck/deck.json \
    --out  examples/advisory-board-deck/advisory-board-exemplar.pptx
```

The title background is a generated image (muted navy/teal scientific
abstract). Regenerate with any image model using a prompt in that register,
or delete the `title_image` key — the builder falls back to the ink panel.

## SYNTHETIC DATA

This directory carries the repository's synthetic-data rule: nothing here
may be presented, adapted or excerpted as if it described a real product or
real patients.
