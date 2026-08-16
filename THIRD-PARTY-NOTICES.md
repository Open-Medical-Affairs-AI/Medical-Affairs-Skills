# Third-Party Notices

This project is licensed under Apache-2.0 (see `LICENSE`). This file records
third-party work that influenced or is incorporated into it, and the license
terms that apply.

We take provenance seriously. In a regulated industry, "where did this come
from?" is a question a compliance reviewer will actually ask, and an
unanswerable one is a blocker to adoption.

---

## 1. K-Dense-AI/scientific-agent-skills — MIT License

**Source:** https://github.com/K-Dense-AI/scientific-agent-skills
**License:** MIT
**Copyright:** Copyright (c) K-Dense Inc.

### What we used

We did **not** copy files from this project. We studied the architecture of six
MIT-licensed skills authored by K-Dense Inc. and rewrote that architecture from
scratch, re-scoped for Medical Affairs. MIT permits this outright; we record it
here because attribution is the right thing to do and because the design debt is
real and worth acknowledging.

| Our skill | Architectural pattern derived | Original K-Dense skill |
|---|---|---|
| All regulated skills (house pattern) | Intake gate → prohibited output language → mandatory `DRAFT — NOT FOR CLINICAL USE` marking → source ledger | `clinical-reports` |
| `skills/systematic-literature-review/` | PRISMA-aligned phase structure; search documentation for reproducibility; screening funnel with recorded exclusion reasons | `literature-review` |
| `skills/mlr-review-readiness/` | Claim–evidence matrix; separation of confidential vs. author-facing channels | `peer-review` |
| `skills/scientific-manuscript/` | Reporting-guideline selector (EQUATOR-aligned) driven off study design | `peer-review` |
| `skills/citation-integrity/` | Multi-source metadata reconciliation (CrossRef / PubMed / OpenAlex) and verification-before-formatting ordering | `citation-management` |
| `skills/congress-abstract-and-poster/` | Manifest-driven poster generation with pre-generation asset/palette audit and post-generation technical audit | `pptx-posters` |
| `skills/medical-terminology-mapping/` | Two-direction resolve/validate model; obsolete-term handling; an explicit "API behaviour that will mislead you" section | `ontology-term-resolution` |

Note that `medical-terminology-mapping` targets a completely different set of
vocabularies (MeSH, MedDRA, SNOMED CT, ICD, ATC) than the original, which covers
bio-ontologies via OLS4 and explicitly does not cover the clinical vocabularies
Medical Affairs needs.

### What we deliberately did NOT use

The `docx` and `pptx` skills in that repository are **not** K-Dense work and are
**not** MIT licensed. Their frontmatter reads:

```yaml
license: Proprietary. LICENSE.txt has complete terms
metadata:
  skill-author: Anthropic, PBC
  source: https://github.com/anthropics/skills/tree/main/skills/pptx
```

They are vendored copies of Anthropic, PBC's proprietary skills. We did not copy,
adapt, or derive from them. Our document and presentation generation is written
from scratch against `python-pptx` and `python-docx`.

This is a useful cautionary example for anyone assembling an open-source skill
library: **a repository-level license badge does not tell you the license of every
file inside it.** Check per-file frontmatter before you vendor anything.

### MIT License (full text, as applying to the K-Dense-authored skills)

```
MIT License

Copyright (c) K-Dense Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 2. Runtime dependencies

These are **not** bundled. They are installed by the user via `pip` when a skill's
scripts are run. Listed for license transparency.

| Package | License | Used by |
|---|---|---|
| `python-pptx` | MIT | `medical-slide-deck`, `congress-abstract-and-poster` |
| `python-docx` | MIT | `scientific-manuscript`, `medical-information-response`, `medical-correspondence` |
| `matplotlib` | PSF-based (BSD-compatible) | `data-visualization-for-medical`, `visual-abstract` |
| `openpyxl` | MIT | `spreadsheet-analysis` |
| `reportlab` | BSD-3-Clause | `pdf-generation` |
| `pypdf` | BSD-3-Clause | `document-ingestion` |
| `pdfplumber` | MIT | `document-ingestion` (table extraction) |
| `requests` | Apache-2.0 | all API skills (optional; stdlib fallback provided) |

All API scripts fall back to the Python standard library (`urllib`) when
`requests` is unavailable, so the core retrieval skills have **zero** third-party
runtime dependencies.

**Every one of these is optional.** Each content skill detects what is available
and degrades through the four-tier ladder in `capability-detection` rather than
failing — markdown plus a build spec instead of `.pptx`, HTML with a print
stylesheet instead of PDF, hand-written SVG instead of matplotlib, CSV plus a
markdown table instead of `.xlsx`. `scripts/selftest_fallbacks.py` runs the
generators in an environment where these packages are deliberately unimportable
and fails the build if any of them exits non-zero or loses content.

---

## 3. Public data sources accessed at runtime

No data from these sources is redistributed in this repository. Skills query them
live, and each skill documents the source's terms and rate limits.

| Source | Terms |
|---|---|
| NCBI E-utilities (PubMed / PMC) | https://www.ncbi.nlm.nih.gov/home/about/policies/ — public domain records; usage policy and rate limits apply |
| ClinicalTrials.gov API v2 | https://clinicaltrials.gov/about-site/terms-conditions — U.S. Government work, public domain |
| openFDA | https://open.fda.gov/terms/ — public domain; **not** for clinical decision-making |
| CrossRef REST API | https://www.crossref.org/documentation/retrieve-metadata/rest-api/ — metadata openly available |
| OpenAlex | CC0 |

### Licensed terminologies we do NOT ship

`medical-terminology-mapping` teaches correct use of these but **contains none of
their content**, because redistribution requires a license we do not hold and you
may not either:

- **MedDRA** — subscription required from MSSO (https://www.meddra.org/subscription).
- **SNOMED CT** — Affiliate License required; free in Member countries via the
  national release centre (https://www.snomed.org/get-snomed).
- **ICD-10-CM / ICD-11** — WHO/CMS terms apply.
- **WHO Drug Dictionary** — subscription required from Uppsala Monitoring Centre.

MeSH is public domain and is queried live via NCBI, so it is the default
vocabulary for anything this project does automatically.

---

## Reporting an attribution problem

If you believe something here is attributed incorrectly or incompletely, open an
issue titled `[attribution]` or email the maintainers. We will correct it
promptly — getting this right matters more to us than being right.
