---
name: capability-detection
description: >-
  Work out what this runtime can actually do before promising a deliverable,
  and degrade visibly rather than failing. Use when about to produce any file —
  deck, document, spreadsheet, PDF, figure, report — and whenever a
  generation script has failed, a library is missing, there is no network,
  or the filesystem is not writable. Defines the four-tier output ladder
  every content skill in this library follows, and the rule that the
  analysis is never lost to a missing container format.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: foundation
  maturity: stable
  produces: Capability report and a resolved output strategy
  deliverables: [docx, pdf]
---

# Capability Detection and Graceful Degradation

An agent that cannot produce a `.pptx` should not produce nothing. It should
produce the deck — as markdown, as a build spec, as HTML — and say plainly that
the container changed and the content did not.

This matters more here than in most domains. The analysis behind a Medical
Affairs deliverable is hours of reasoning about evidence. The `.pptx` is a
container. Losing the first because the second is unavailable is an absurd
trade, and it is what happens by default.

## The rule

> **Never lose the analysis. Degrade the container, never the content.**

And its corollary, which matters just as much in a regulated context:

> **Degrade visibly.** A reader must be able to tell what they are holding.
> Silent fallback produces a document someone forwards believing it is
> something it is not.

## The four-tier ladder

Resolve every file output through this ladder, stopping at the first available
tier.

| Tier | Path | When |
|---|---|---|
| **1 — Bundled engine** | `scripts/ma_render.py` in every skill: installs `python-pptx`, `python-docx`, `matplotlib`, `reportlab` on first use, then builds .pptx/.docx/.pdf with charts and layout QA | The default. Consistent design, compliance furniture, previews you can inspect |
| **2 — Host document tools** | A runtime-provided `pptx`/`docx`/`pdf` skill, fed the same spec | Only when tier 1 cannot run (no Python) — keep this library's content rules |
| **3 — Standard-library files** | The engine's own no-package writers: a real `.docx`, print-ready 16:9 HTML slides, HTML-to-PDF, SVG figures, CSV | Python without pip. Still a file a stakeholder can open, print or forward |
| **4 — In-response** | The structured content in your reply | No filesystem. Always possible — say which file you could not create |

**Markdown is never a deliverable.** It is a drafting and review format:
`python3 scripts/ma_render.py report draft.md --out brief.docx` turns a markdown
draft into the designed Word and PDF files. Handing over the `.md` itself, or a
hand-rolled python-pptx script with default styling, is the failure this
ladder exists to prevent.

## Checking

```bash
S=skills/capability-detection/scripts/capabilities.py

python3 $S                          # full report
python3 $S --json                   # machine-readable
python3 $S --best-path deck         # which tier will be used, and why
python3 $S --best-path figure --require-tier 2   # exit non-zero if unavailable
python3 $S --check-network          # which API hosts are reachable
```

Check **before** promising an output format, and run `python3 scripts/ma_render.py
bootstrap` first — most "unavailable" packages are one install away. Telling
someone at the start that you will deliver print-ready HTML because Python has no
pip is a different conversation from handing it over when they expected slides.

## The degradation notice

Every degraded output carries this, at the top of the file **and** in your reply:

```
⚠ DEGRADED OUTPUT — python-pptx is not available and could not be installed.

   Delivered:  deck.html (one 16:9 slide per printed page) plus deck.json
   Not delivered: the .pptx itself
   To get it:  pip install python-pptx
               python3 scripts/ma_render.py deck deck.json --out deck.pptx

   The content is complete. Only the container changed.
```

Four things it must contain: **what was missing**, **what you delivered
instead**, **the exact command to get the full version**, and **an explicit
statement about whether content was lost**. That last line is what stops a
reader assuming the worst — or assuming nothing happened.

## Writing a script that degrades

The pattern the bundled generators follow. Keep the check inline and small —
about twelve lines — so a copied skill directory still works.

```python
def _have(module: str) -> bool:
    try:
        __import__(module)
        return True
    except ImportError:
        return False

if _have("pptx"):
    build_pptx(spec, out)                       # tier 1
else:
    html = ma_render.deck_html(spec)            # tier 3 — never markdown
    out.with_suffix(".html").write_text(html)
    spec_path.write_text(json.dumps(spec, indent=2))
    print(DEGRADED_NOTICE.format(...))
    # exit 0 — this succeeded, it just succeeded differently
```

**Exit zero.** A degraded output is a success. Exiting non-zero tells the calling
agent the job failed, and it will either retry pointlessly or report failure to
a user who could have had the content.

Reserve non-zero for genuine failures: a malformed spec, a compliance gate not
met, an unwritable path.

## What to degrade, and what never to

Some things are containers. Some are the substance, and must survive every tier.

| Never lose | Why |
|---|---|
| Every claim and its citation | The content is the deliverable |
| Study design named alongside every result | Without it the number is misleading (`evidence-appraisal`) |
| Confidence intervals | A point estimate alone asserts false precision |
| Safety data and fair balance | A compliance requirement, not a formatting one |
| Approval status statements | Same |
| Numbers at risk on a survival curve | The curve is uninterpretable without them |
| Denominators | A percentage without one is not a result |
| The DRAFT marking | The control that keeps unreviewed content from going out |
| The provenance appendix | What makes the work auditable |

If a fallback format cannot carry one of these, that fallback is wrong. A
survival curve rendered without numbers at risk is not a degraded figure, it is
a misleading one — emit a data table instead.

## Capabilities worth checking

**Python packages.** `pptx`, `docx`, `openpyxl`, `matplotlib`, `reportlab`,
`pypdf`. All optional; everything in this library works without all of them.

**Network.** Per host, because they fail independently — corporate networks
block `eutils.ncbi.nlm.nih.gov` far more often than `api.fda.gov`. Without
network you cannot verify citations, so say so and label every reference as
unverified rather than implying it was checked.

**Filesystem.** Some runtimes give no writable path. Tier 4 exists for this.

**Office converter.** LibreOffice (`soffice`) turns the .pptx/.docx into an
identical PDF and powers the page previews; without it the engine renders PDFs
with reportlab and skips previews. `bootstrap` reports both.

## When the network is missing specifically

This one deserves care, because the failure is silent and consequential.

Without network you cannot run `citation-integrity`'s verifier. Every reference
is then **unverified**, and the deliverable must say so:

> **References unverified.** No network access in this session, so no identifier
> was resolved against PubMed, CrossRef or ClinicalTrials.gov. Every reference
> below must be checked before use. Models fabricate plausible, correctly
> formatted citations to papers that do not exist.

Do not quietly emit citations as though they had been checked. That is the
single most damaging thing this library could do.

<!-- ma-render:begin — generated by scripts/sync_renderer.py; edit the template there -->
## Deliverable format

Deliver a designed **Word document (.docx) plus a PDF copy**.
Build it with this skill's bundled engine. Markdown is for drafting only —
never hand over a .md file, and never hand-write a python-pptx or
python-docx script instead of the engine.

```bash
python3 scripts/ma_render.py bootstrap      # installs python-pptx, python-docx, matplotlib, reportlab
python3 scripts/ma_render.py example report > spec.json   # spec format; or write a markdown draft
python3 scripts/ma_render.py report spec.json --out outputs/<name>.docx --preview outputs/preview
```

Turn numbers into `stats`/`chart` blocks and comparisons into tables or
`two_column` slides; put a source on every data element. Then open
`outputs/preview/contact-sheet.png`, fix every overflow, empty or text-only
page, and re-render. If a package cannot be installed the engine still
writes a real .docx or print-ready HTML and says what degraded.
<!-- ma-render:end -->

## Before you finish

Read `house-rules/capability-detection.md` — some organisations mandate specific
output formats, or prohibit certain fallbacks entirely.

## References

- `references/fallback-patterns.md` — worked tier-3 renderers for each output
  type, including SVG survival curves and printable HTML posters.
