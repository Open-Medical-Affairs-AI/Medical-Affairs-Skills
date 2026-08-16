---
name: pubmed-search
description: >-
  Search PubMed properly and retrieve real, verifiable literature via the
  NCBI E-utilities API. Use whenever a Medical Affairs task needs published
  evidence — what exists on a topic, a KOL's publication record, the
  evidence base for a brief or synthesis, the trial behind a congress
  abstract, or whether a claim has published support. Covers MeSH-aware
  query construction, field tags, filters, the history server,
  deduplication, rate limits and the free API key. Use this instead of
  recalling references from memory: models fabricate citations that look
  correct, and every reference has to resolve.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: data
  maturity: stable
  requires:
    - citation-integrity
  suggests:
    - evidence-appraisal
    - medical-terminology-mapping
  produces: Verified literature result set with search strategy recorded
  network: [eutils.ncbi.nlm.nih.gov]
---

# PubMed Search

PubMed is the primary evidence source for Medical Affairs, and searching it
badly is the most common reason an evidence review misses the paper that matters.

Two rules frame everything below. **Never write a citation you did not
retrieve** — see `citation-integrity`. And **always record the exact query
string and the date**, because a search that cannot be reproduced is not
evidence, it is an anecdote about what you happened to find.

## The client

**Screen first, then fetch.** This is the pattern to use by default:

```bash
S=skills/pubmed-search/scripts/pubmed.py

# 1. Screen — one line per record: PMID, year, journal, evidence tier, title
python3 $S search --query '"teclistamab"[tiab] AND "multiple myeloma"[MeSH]' \
        --limit 50 --format table

# 2. Fetch abstracts only for the records that survived screening
python3 $S fetch --pmids 36001231,35660948,34891112 --abstracts
```

The reason is cost, and it is not marginal. Fifty records as a table is a few
hundred tokens; fifty structured abstracts is on the order of thirty thousand —
more than every skill in this library put together. Pulling abstracts for a
whole result set to find the four papers that matter wastes most of the context
the actual analysis needs.

So: `--abstracts` is opt-in, and it should stay that way. Reach for it on a
first search only when the set is genuinely small and you know you will appraise
all of it.

```bash
# Look up how PubMed indexes a concept before you search for it
python3 $S mesh --term "multiple myeloma"

# What has this author published recently?
python3 $S search --query 'Moreau P[au] AND myeloma' --from 2022 --limit 40 --format table

# What cites this, and what is related
python3 $S links --pmid 36001231 --kind citedby

# A reference list for a deliverable
python3 $S fetch --pmids 36001231,35660948 --format ama
```

`--format table` to screen, `--format json` for downstream processing,
`--format markdown` for prose, `--format ama` for a reference list. `--help`
documents the rest.

**Get a free API key.** Register at https://account.ncbi.nlm.nih.gov/settings/
and export `NCBI_API_KEY`. It raises the rate limit from 3 to 10 requests per
second. The client throttles itself either way, so without a key large searches
are simply slower.

## Building a query that actually works

The default failure is a bare keyword search that returns 4,000 records, of
which you read 20 and assume they are representative. They are not — PubMed's
default relevance ordering is not evidence-weighted.

### MeSH plus free text, together

MeSH terms are human-assigned and precise but lag publication by weeks to
months, so a MeSH-only search **misses the newest papers** — which are usually
the ones you care about. Free-text catches new material but misses synonyms and
picks up irrelevant hits.

Use both:

```
("multiple myeloma"[MeSH] OR "multiple myeloma"[tiab] OR "plasma cell myeloma"[tiab])
AND
("teclistamab"[tiab] OR "TECVAYLI"[tiab] OR "JNJ-64007957"[tiab])
```

Note the drug synonyms. Generic name, brand name, and development code all
appear in the literature depending on when the paper was written. Missing the
development code loses the early trials. Run `mesh --term` first to see how
PubMed actually indexes the concept, including its entry terms.

### Field tags worth knowing

| Tag | Searches | Note |
|---|---|---|
| `[MeSH]` | Assigned subject headings | Add `[majr]` for major-topic only |
| `[tiab]` | Title and abstract | The workhorse for anything recent |
| `[tw]` | Text words — broader still | Use when recall matters most |
| `[au]` | Author | `Moreau P[au]`. Common names need an affiliation filter |
| `[ad]` | Affiliation | Institution-based searching |
| `[ta]` | Journal title abbreviation | |
| `[pt]` | Publication type | See below |
| `[dp]` | Date of publication | `2023:2026[dp]` |
| `[sb]` | Subset | `systematic[sb]` is a curated filter |

MeSH terms explode to include narrower terms automatically. Suppress with
`[MeSH:noexp]` when the narrower terms are noise.

### Publication-type filters that map to evidence tiers

```
AND "randomized controlled trial"[pt]        # RCTs only
AND ("meta-analysis"[pt] OR "systematic review"[pt])
AND "practice guideline"[pt]
NOT ("review"[pt] OR "editorial"[pt] OR "comment"[pt])
NOT ("case reports"[pt])
```

`"randomized controlled trial"[pt]` is more reliable than `randomized[tiab]`,
which catches every paper that mentions randomisation in passing.

For safety questions, do the opposite: **include** case reports. They are where
rare events first appear.

### Recall versus precision — decide deliberately

- **High recall** (systematic review, safety signal, "does anything exist on
  this?"): broad synonyms, `[tw]`, no publication-type restriction, accept the
  noise, screen systematically.
- **High precision** (a brief due in an hour, a specific number): `[MeSH:majr]`,
  publication-type filters, tight date range.

State which you chose. A brief built on a high-precision search should not claim
to have surveyed the literature.

## Search strategy for common Medical Affairs jobs

**Everything on our product.** Generic + brand + development code, no date
limit, no publication-type filter. Then stratify by type. This is also how you
find the case reports you would otherwise miss.

**Profiling a KOL** (`kol-engagement-brief`). Author search with an affiliation
qualifier, last 3–5 years. Read what they published *and* what changed: a
researcher who moved from single-agent to combination work has changed their
question. Watch for author-name ambiguity — check affiliations, and use ORCID
where present.

**Competitive landscape.** Each competitor product by all its names, restricted
to trials and to the relevant disease MeSH term. Then run the disease term with
`"randomized controlled trial"[pt]` and a recent date range to catch entrants
you did not know to look for.

**Finding the paper behind an abstract.** Congress abstracts are mostly not in
PubMed. Search the trial acronym and the NCT number in `[tw]`, plus first and
last author. If nothing, the full publication does not exist yet — which is
itself the finding, and it determines the evidence tier you must label.

**Safety questions.** Drug + adverse event term, including case reports, no date
limit. Cross-check with `regulatory-label-intelligence` for label language and
FAERS.

**Evidence gaps** (`evidence-gap-analysis`). Search the question you wish were
answered. Zero relevant results, confirmed with a genuinely broad strategy, is a
real and reportable finding.

## What PubMed will not tell you

Knowing the boundaries prevents overclaiming from a search.

- **Congress abstracts are largely absent.** ASCO, ASH, ESMO, EHA, AAD
  abstracts are generally not indexed. In fast-moving areas the most current
  evidence is invisible here.
- **Indexing lags.** MeSH assignment takes weeks to months. Recent papers are
  findable by `[tiab]` only.
- **Absence of evidence is not evidence of absence** — but a well-documented
  broad search returning nothing is genuine evidence of a gap. The documentation
  is what makes the difference.
- **Relevance ranking is not quality ranking.** Sort by date, or screen
  systematically. Never take the top 20 as representative.
- **Retracted papers remain in PubMed**, flagged by publication type. Always
  run `citation-integrity`'s verifier over a final reference list.
- **Grey literature, registries, regulatory documents, and theses** are out of
  scope. Use `clinical-trials-search` and `regulatory-label-intelligence`.

## Recording the strategy

Every search goes into the provenance appendix, verbatim:

```markdown
**PubMed** (searched 2026-08-14, NCBI E-utilities)
Query: ("multiple myeloma"[MeSH] OR "multiple myeloma"[tiab])
       AND ("teclistamab"[tiab] OR "TECVAYLI"[tiab] OR "JNJ-64007957"[tiab])
Filters: none · Date range: none
Results: 84 · Screened on title/abstract: 84 · Included: 11
Excluded: 51 not on this product, 14 non-clinical, 8 duplicate reports of the
same trial
```

Reproducibility is not bureaucracy. It is what lets the next person extend your
work instead of redoing it, and what lets a reviewer see whether you looked in
the right place.

## Deduplication

The same trial appears as a primary publication, one or more congress abstracts,
secondary analyses, and pooled analyses. Counting these as independent evidence
inflates apparent support — a real and common error in evidence synthesis.

Group by **trial**, not by publication. The NCT number is the reliable key; the
trial acronym is a good secondary. Report "11 publications reporting 4 trials",
never "11 studies".

## Before you finish

Read `house-rules/pubmed-search.md` — organisations often mandate specific
search filters, date limits, or evidence thresholds.

Then run `citation-integrity`'s verifier over everything you are about to cite.

## References

- `references/query-cookbook.md` — worked, copy-ready query patterns for the
  recurring Medical Affairs search jobs.
- `references/eutilities-api.md` — the API surface, parameters, the history
  server, rate limits, and error handling, for when you need to go beyond the
  bundled client.
