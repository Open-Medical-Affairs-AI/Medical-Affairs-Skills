---
name: systematic-literature-review
description: >-
  Run a reproducible, PRISMA-aligned systematic literature review — protocol
  first, documented search strategy, screening funnel with recorded
  exclusion reasons, structured extraction, and risk-of-bias assessment. Use
  when the question demands defensible completeness rather than a quick
  scan: payer and HTA submissions, guideline engagement, evidence dossiers,
  indirect comparison feasibility, and "what is ALL the evidence on X". Also
  use to appraise someone else's published review. Say which you are doing —
  a narrative summary presented as a systematic review is a serious
  misrepresentation.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: data
  maturity: stable
  requires:
    - pubmed-search
    - evidence-appraisal
  suggests:
    - citation-integrity
    - evidence-synthesis
  produces: PRISMA-aligned systematic review with flow diagram and evidence tables
  network: [eutils.ncbi.nlm.nih.gov, clinicaltrials.gov]
---

# Systematic Literature Review

The defining property of a systematic review is not thoroughness. It is
**reproducibility** — another competent person, given your protocol, would
arrive at the same included set.

That is what an HTA body, a guideline committee, or a journal is checking. It is
also why the protocol comes first: a search strategy written after you know what
you found is not a search strategy, it is a justification.

**Be honest about which you are doing.** A rapid evidence scan is a legitimate
and often correct choice under time pressure. Calling one a systematic review
when it is not is a misrepresentation that experienced reviewers spot at once,
usually from the absence of an exclusion log.

## The seven phases

### 1. Protocol — before any searching

Write and freeze:

- **The question, in PICO form.** Population, Intervention, Comparator,
  Outcomes. Add Study design and Timeframe where relevant (PICOS/PICOT).
- **Inclusion and exclusion criteria**, decided in advance. Every criterion
  should be applicable by someone who has not read the papers.
- **Databases and the date range.**
- **The full search strategy** for at least one database, translatable to the
  others.
- **Screening process** — who screens, at what level, how disagreements resolve.
- **Data to extract.**
- **Risk-of-bias tool**, chosen by design.
- **Synthesis approach** — narrative, or meta-analysis with a stated model.

Register it where the review will be published or submitted — PROSPERO for
health-related reviews. Registration is what makes "we pre-specified this"
checkable.

**The most common protocol failure** is criteria so vague that they can absorb
any decision: "relevant studies", "high quality", "recent". Each of those hides
a judgement that should be explicit.

### 2. Search — recall first

Systematic review search is deliberately over-inclusive. You accept a large
volume of irrelevant results to be confident you have not missed anything.

- **Minimum three sources.** PubMed/MEDLINE plus Embase and Cochrane CENTRAL is
  the conventional floor for a health-technology submission. This library
  reaches PubMed and ClinicalTrials.gov; Embase and CENTRAL are subscription
  resources and must be searched separately. **Say so in your limitations** —
  a PubMed-only search is not a systematic review search, and claiming otherwise
  is the failure HTA reviewers find most often.
- **Combine controlled vocabulary and free text** for every concept
  (`pubmed-search`).
- **Do not restrict by language** unless justified; language restriction
  introduces bias and must be declared.
- **Do not restrict by publication type** unless the question demands it.
- **Search trial registries** (`clinical-trials-search`) for unpublished and
  ongoing studies. Their absence from the literature is itself a finding, and
  registry searching is what lets you say something about publication bias.
- **Hand-search:** reference lists of included studies and relevant reviews,
  plus forward citation searching (`pubmed.py links --kind citedby`).
- **Grey literature** where relevant: HTA agency reports, regulatory review
  documents, conference proceedings.

Record every search verbatim — database, platform, exact string, date run,
number of hits. This is not documentation for its own sake; it is the evidence
that the review is reproducible.

### 3. Screening

Two levels: title/abstract, then full text.

- **Dual independent screening** is the standard. Where a second reviewer is not
  available, say so — it is a stated limitation, not something to conceal.
- **Record an exclusion reason for every full-text exclusion.** Title/abstract
  exclusions are counted, not itemised; full-text exclusions are itemised with
  reasons. This list is the single most scrutinised part of a submitted review.
- **Pilot the criteria** on 20–30 records first and refine before the main pass.
  Refinement after piloting is legitimate; refinement mid-screening is not, and
  must be declared if it happens.
- **When in doubt, include at the title/abstract stage.** Errors at the first
  level are unrecoverable; errors at full text are visible.

### 4. Extraction

Extract into a structured table, pre-specified in the protocol:

Study ID · design · setting and country · enrolment period · N · population
characteristics · intervention and comparator with dosing · follow-up duration ·
outcomes with definitions · results with effect estimates and confidence
intervals · funding source and conflicts of interest.

**Link publications to trials, not to each other.** One trial commonly generates
a primary paper, congress abstracts, secondary analyses, and pooled analyses.
Extract at trial level with the publications listed beneath, or you will
double-count. Use the NCT number as the key.

**Extract what is reported, not what you infer.** Where a value is missing, mark
it missing. Calculating a confidence interval from a p-value and an N is
sometimes legitimate — and must be labelled as derived, with the method stated.

### 5. Risk of bias

Apply the instrument that matches the design — RoB 2, ROBINS-I,
Newcastle-Ottawa, QUADAS-2 — as set out in
`evidence-appraisal/references/bias-checklists.md`. Assess **per outcome**, not
per study, and report domain-level judgements rather than only an overall score.

### 6. Synthesis

Follow `evidence-synthesis`: organise by question, weigh rather than count,
confront contradictions.

**Meta-analyse only when the studies are combinable.** Clinical and
methodological heterogeneity matters more than statistical heterogeneity. A
precise pooled estimate across incomparable populations describes nothing real.
When you do not pool, say why — "not pooled owing to differences in comparator
and line of therapy" is a finding, not a failure.

Where you do pool: state fixed vs random effects and why, report I² with a
confidence interval, pre-specify subgroup analyses, and assess publication bias
only when there are enough studies for the test to mean anything (conventionally
≥10).

### 7. Reporting

Follow **PRISMA 2020** — the 27-item checklist plus the flow diagram. Use the
extension that matches your review type: PRISMA-NMA for network meta-analyses,
PRISMA-ScR for scoping reviews, PRISMA-S for the search component,
PRISMA-IPD for individual patient data.

## The PRISMA flow diagram

Numbers must reconcile. Reviewers check the arithmetic, and it frequently does
not add up.

```
Identification
  Records identified from:
    PubMed/MEDLINE (n = 412)
    Embase         (n = 388)
    CENTRAL        (n =  94)
    Registries     (n =  31)
    Hand-searching (n =  12)                    Total (n = 937)
  Records removed before screening:
    Duplicates (n = 284)                        → screened (n = 653)

Screening
  Records screened (n = 653)      → excluded (n = 561)
  Reports sought for retrieval (n = 92)  → not retrieved (n = 3)
  Reports assessed for eligibility (n = 89)
    Excluded, with reasons:
      Wrong population        (n = 31)
      Wrong comparator        (n = 18)
      No outcome of interest  (n = 14)
      Duplicate report        (n =  9)
      Conference abstract only, insufficient detail (n = 6)   → excluded (n = 78)

Included
  Studies included (n = 11)  reported in (n = 17) publications
```

Note the last line. Reporting "17 studies" when 17 publications describe 11
trials inflates the apparent evidence base — the error this diagram exists to
prevent.

## Appraising someone else's review

The questions that separate a sound review from a decorated narrative:

1. Was a protocol registered **before** the search? Check PROSPERO, and check
   whether the registered outcomes match the reported ones.
2. Is the full search strategy reproduced, for every database, with dates?
3. Were at least three sources searched, including a registry?
4. Was screening dual and independent?
5. Are full-text exclusions listed **with reasons**?
6. Was risk of bias assessed with a named tool, per outcome?
7. Does the flow diagram reconcile?
8. Is heterogeneity addressed, or just reported?
9. Are conclusions proportionate to the certainty of the evidence?
10. Are funding and conflicts declared?

AMSTAR-2 and ROBIS are the formal instruments for this.

## Limitations you must state

- Databases **not** searched — name them. PubMed-only is the most common gap.
- Single-reviewer screening or extraction, if that is what happened.
- Language restrictions.
- Date cut-off, and how quickly the field is moving.
- Grey literature and unpublished data not sought.
- Conference abstracts included or excluded, and why.

## Before you finish

Read `house-rules/systematic-literature-review.md` — organisations and HTA
bodies specify required databases and reporting standards, and the requirements
differ by submission target.

Then run `deliverable-quality-review`.

## References

- `references/prisma-checklist.md` — the PRISMA 2020 items with what each
  actually requires, and the common ways each is fudged.
