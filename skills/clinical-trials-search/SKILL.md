---
name: clinical-trials-search
description: >-
  Search ClinicalTrials.gov via the v2 API to map the trial landscape — what
  is running, by whom, in which populations, with what endpoints, and what
  is about to read out. Use for competitive pipeline assessment, finding the
  trial behind an abstract, checking whether a question is already being
  answered before proposing a study, verifying NCT numbers, or reviewing a
  trial's amendment history. Pair with pubmed-search when assessing evidence
  gaps: the registry shows what is coming, which the literature cannot.
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
    - pubmed-search
  produces: Trial landscape with sponsors, phases, endpoints and timelines
  network: [clinicaltrials.gov]
---

# Clinical Trials Search

The literature tells you what has been answered. The registry tells you what is
being answered right now — and that is usually the more strategically useful
question.

No API key, no registration, no rate limit published beyond a request to be
reasonable.

## The client

```bash
S=skills/clinical-trials-search/scripts/ctgov.py

# What is running on this intervention?
python3 $S search --intervention teclistamab --limit 25

# Landscape by condition and phase, currently enrolling
python3 $S search --condition "multiple myeloma" --phase 3 --status RECRUITING

# Competitor pipeline
python3 $S search --sponsor "Janssen" --condition "multiple myeloma" --status RECRUITING

# One trial in full
python3 $S get --nct NCT04557098

# Has the primary endpoint changed since registration?
python3 $S history --nct NCT04557098

# Landscape table for a deliverable
python3 $S search --condition "atopic dermatitis" --phase 2,3 --format table
```

`--format json | markdown | table`. `--help` for the rest.

**Screen with `--format table`, then pull the few trials that matter in full.**
A registry record is long — eligibility criteria alone run to hundreds of words
— so a 25-record landscape in `markdown` costs an order of magnitude more than
the same landscape as a table, and you rarely need the detail on more than three
or four of them. Same discipline as `pubmed-search`: narrow first, then read.

## What the registry is good for

**Competitive pipeline.** Every interventional trial a competitor is running,
with phase, enrolment, and expected completion. This is public and it is the
single richest source of competitive intelligence available to Medical Affairs.

**Whether your evidence gap is actually a gap.** Before proposing a study,
check whether someone is already running it. `evidence-gap-analysis` depends on
this — proposing a trial that a competitor completes first is an expensive way
to learn to check the registry.

**What is about to read out.** Sort by primary completion date. A phase 3 with a
primary completion date six months out is the thing that will change your
landscape, and it is knowable today.

**The trial behind a paper or abstract.** NCT numbers appear in publications and
abstracts. The registry gives you the full protocol context the abstract omitted.

**Endpoint archaeology.** The change history shows whether the primary endpoint,
sample size, or eligibility was altered — and when relative to enrolment. A
primary endpoint changed after enrolment began is a serious risk-of-bias signal
(`evidence-appraisal`, RoB 2 domain 5) and it is invisible in the publication.

**Enrolling trials for a KOL conversation.** Knowing which trials a KOL's
institution is a site for is directly useful preparation.

## What it is not good for

- **Data quality is sponsor-controlled.** Status fields go stale constantly.
  "Recruiting" may mean recruitment finished two years ago and nobody updated
  it. Cross-check the last-update date against the status before relying on it.
- **Results posting is incomplete.** Required for applicable trials under FDAAA
  801, and compliance is imperfect and late.
- **Not every trial is registered here.** EU CTIS, ISRCTN, jRCT, ChiCTR, and
  CTRI carry trials that never appear on ClinicalTrials.gov. A registry search
  is not a global census — say so when reporting.
- **Free-text fields are inconsistent.** Sponsor names vary across subsidiaries
  and over time; search several variants.
- **Observational studies are under-registered** relative to interventional
  ones.

## Reading a trial record critically

When you pull a record, these are what matter:

**Design.** `studyType`, `phases`, `allocation` (RANDOMIZED vs NON_RANDOMIZED),
`interventionModel`, `maskingInfo`, `primaryPurpose`. A "phase 2" that is
single-arm and open-label supports very different claims from a randomised one —
and the phase label alone does not tell you which it is.

**Enrolment.** `enrollmentInfo.count` with `type`: `ESTIMATED` is a target,
`ACTUAL` is what happened. A trial that closed well below its estimate had a
problem worth understanding.

**Primary outcome and its timeframe.** The timeframe tells you when data can
possibly exist. A primary outcome measured "up to 5 years" will not read out
next year regardless of what the completion date says.

**Eligibility.** This is the population the eventual result will apply to, and
it is where generalisability is decided. Read it before assuming a result
transfers to your patients of interest.

**Dates.** `startDate`, `primaryCompletionDate`, `completionDate`, and
`lastUpdatePostDate`. The gap between the last update and today is your
staleness signal.

**Sponsor and collaborators.** Reveals partnerships and, sometimes, that an
"investigator-initiated" study is company-supported.

## Search construction

The v2 API supports both simple terms and Essie expression syntax.

```bash
# Broad
--term "bispecific antibody myeloma"

# Structured — more precise
--condition "multiple myeloma" --intervention teclistamab --sponsor Janssen

# Status filters combine
--status RECRUITING,NOT_YET_RECRUITING,ACTIVE_NOT_RECRUITING
```

Valid statuses: `NOT_YET_RECRUITING`, `RECRUITING`,
`ENROLLING_BY_INVITATION`, `ACTIVE_NOT_RECRUITING`, `SUSPENDED`, `TERMINATED`,
`COMPLETED`, `WITHDRAWN`, `UNKNOWN`.

**`TERMINATED` and `WITHDRAWN` trials are worth reading, not filtering out.**
The termination reason is recorded, and "terminated for futility" or "terminated
for toxicity" in a competitor programme is high-value intelligence that appears
nowhere else. Analysts routinely filter these out and miss the most informative
records in the set.

## Deduplication and grouping

One trial, many identifiers: an NCT number, an EudraCT or CTIS number, a sponsor
protocol ID, and an acronym. The same programme may also run as several
separate NCT records for different regions or cohorts.

Group by **programme**, not by record, and say which you are counting. "14 NCT
records covering 9 distinct trials across 4 sponsors" is informative; "14 trials"
is misleading.

## Recording the search

```markdown
**ClinicalTrials.gov** (searched 2026-08-14, API v2)
Query: condition="multiple myeloma", intervention="teclistamab", status=all
Results: 14 records · 9 distinct trials · 4 sponsors
Note: registry coverage is not global — EU CTIS and jRCT not searched.
```

## Before you finish

Read `house-rules/clinical-trials-search.md`, and verify every NCT number you
cite (`citation-integrity` — registry identifiers are as fabricable as PMIDs).

## References

- `references/ctgov-api.md` — endpoints, the field-selection syntax, pagination
  by page token, and the response structure module by module.
