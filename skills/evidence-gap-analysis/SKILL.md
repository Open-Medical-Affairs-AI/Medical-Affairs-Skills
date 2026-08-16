---
name: evidence-gap-analysis
description: >-
  Identify what we still do not know, decide which gaps are worth closing,
  and propose how. Use for evidence generation planning, research
  prioritisation, budget allocation across studies, and requests like "what
  evidence are we missing" or "what should we study next". Enforces the rule
  that a gap is only worth closing if closing it changes a decision —
  missing data is not by itself a reason to generate more. Ranks candidate
  gaps by decision impact, feasibility, differentiation and timing, and
  allocates under a real constraint with an explicit below-the-line list.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: workflow
  maturity: stable
  requires:
    - medical-affairs-foundations
    - evidence-appraisal
    - strategic-analysis
  suggests:
    - evidence-synthesis
    - pubmed-search
    - clinical-trials-search
    - deliverable-quality-review
  produces: Prioritised evidence gap analysis with research proposals
  network: [eutils.ncbi.nlm.nih.gov, clinicaltrials.gov]
---

# Evidence Gap Analysis

Anyone can list what is unknown. The list is always long and always true, and it
is why this exercise so often produces a wish list that nothing gets funded from
and that gets repeated the following year.

**The discipline: do not propose a study because data are missing. Propose it
because closing the gap changes a decision someone will make.**

That single filter removes most of the list, and what survives is fundable.

## What makes a gap worth closing

Four conditions. A gap failing any of them is a genuine gap and still not a
priority.

1. **A decision depends on it.** Someone — a clinician choosing therapy, a
   guideline committee, a payer, a regulator — would act differently depending
   on the answer. Name the decision and the decision-maker.
2. **The question is answerable.** With a study that could actually be run, in
   this population, within a useful timeframe.
3. **Nobody is already answering it.** Check the registry. Proposing a trial a
   competitor completes first is an expensive way to learn to check.
4. **The answer would be believed.** A study design that will not convince the
   people who need convincing is not worth running. Ask what evidence a
   guideline committee would accept, not what evidence you can generate.

## Stage 1 — Inventory

- The evidence landscape — ours and the field's
- Current evidence generation plan and what is in flight
- Field insights: the questions clinicians actually ask
  (`field-insight-synthesis`)
- Medical information enquiry patterns — a direct signal of what the label and
  literature do not answer
- Guideline positions and where they say evidence is insufficient
- Payer and HTA feedback, and any rejections and their stated reasons
- Competitive evidence position
- The resource envelope

**Guideline and HTA documents are the highest-value input and are routinely
overlooked.** When NICE or a guideline committee writes "the evidence was
insufficient to recommend", they have told you precisely which gap matters, to
whom, and what would close it. That is a fully specified research question given
away for free.

## Stage 2 — Retrieve

**Confirm each gap is real** (`pubmed-search`). A gap claimed on a narrow search
is not a finding, it is a search failure. Use a deliberately over-broad strategy
— all synonyms, `[tw]` not `[tiab]`, no publication-type filter, no date limit.
Record the exact query: it is the evidence for the claim.

**Check who is already answering it** (`clinical-trials-search`). Search the
question, not just your product. Include terminated trials — a competitor's
failed attempt at the same question tells you something about feasibility.

## Stage 3 — Analyse

### Categorise the gaps

Different types need different responses:

| Type | Example | Typical answer |
|---|---|---|
| **Population** | No data in renal impairment, older patients, a comorbid group | Dedicated cohort, RWE, subgroup pooling |
| **Comparator** | No head-to-head against current standard of care | RCT, or adjusted indirect comparison |
| **Endpoint** | Surrogate only; no data on the outcome that matters | Long-term follow-up, registry |
| **Duration** | No data beyond 12 months | Extension study, RWE |
| **Sequencing** | What to use after this, or before it | RWE, pragmatic trial |
| **Practice** | How it performs outside trial conditions | RWE, registry, pragmatic trial |
| **Mechanism** | Why some patients do not respond | Translational, biomarker |
| **Economic** | No cost-effectiveness evidence | Economic modelling, RWE |
| **Contradiction** | Two studies disagree and nobody knows why | Targeted study, or re-analysis |

The **contradiction** category is under-used and often the cheapest to close —
sometimes with a pooled re-analysis of data already held rather than a new study.

### Ask what decision each gap blocks

For each gap, complete this sentence: *"If we knew X, then [named person or
body] would be able to decide Y."*

If you cannot complete it, the gap is real and it is not a priority. Say that
explicitly rather than dropping it — the list of real-but-not-prioritised gaps
is useful, and it prevents the same gaps being rediscovered next year.

### Rank

Forced ranking on:

- **Decision impact** — dominates everything else
- **Feasibility** — can this actually be run, here, in time?
- **Differentiation** — does it advance something only we can do, or is it table
  stakes anyone will generate?
- **Timing** — will the answer arrive while the decision is still open?
- **Credibility of the achievable design** — will the answer convince?
- **Cost of not knowing** — what happens if this stays open

### Match design to question

Do not default to a trial.

| Question | Design |
|---|---|
| Comparative efficacy vs current standard | Randomised trial. Nothing else convinces a guideline committee. |
| Effectiveness in practice, unselected patients | RWE with target trial emulation |
| Long-term safety, rare events | Registry, extension, database study |
| Sequencing | RWE first; pragmatic trial if the question is decision-critical |
| Subpopulation efficacy | Dedicated cohort, or pooled analysis if data exist |
| Practice patterns, unmet need | Chart review, survey, RWE |
| Economic | Modelling on existing data, plus RWE inputs |
| Why heterogeneity exists | Translational or biomarker sub-study |

**Check first whether existing data already answer it.** Pooled analyses,
secondary analyses of completed trials, and long-term follow-up of existing
cohorts are dramatically cheaper than new studies and are systematically
under-considered. A meaningful proportion of "evidence gaps" are unpublished
analyses of data the company already holds.

### Investigator-initiated studies

IIS are a legitimate route, and they belong to the investigator. The company may
support a study it considers scientifically valuable; it may not direct the
question, the design, or the publication. An IIS programme used to generate
company-specified evidence is a compliance exposure, not a strategy — and it is
identifiable as such from the pattern of what gets funded.

## Constrained allocation

When there is a fixed budget — and there always is — allocate explicitly:

```
| Rank | Gap | Design | Cost | Time to answer | Decision it unblocks |
|------|-----|--------|------|----------------|----------------------|
                                    ─── LINE ───
| Below the line, with what we lose by not funding it                |
```

**The below-the-line list is as informative as the funded one.** It is what
leadership actually debates, and it is what makes the trade-offs visible instead
of implicit. Never present only the funded set.

Also state the **portfolio shape**: a plan of six long expensive randomised
trials answers nothing for four years. A mix of horizons — something that
answers this year, something that answers in three — is usually the better
allocation, and saying why is part of the analysis.

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus:

- **Is every proposed study justified by a decision, or by the absence of data?**
  Re-read each rationale. "No data exist" is not a rationale.
- **Did I confirm each gap with a genuinely broad search**, and record it?
- **Did I check the registry** for each?
- **Could existing data answer any of these** without a new study?
- **Would the proposed design convince the audience that needs convincing?**
- **Is anything here proposed because it would produce a favourable result**
  rather than because the question is open? That is not evidence generation.

## Stage 5 — Deliver

Use `shared/templates/evidence-gap-analysis.md`.

```
DRAFT — NOT FOR EXTERNAL USE. REQUIRES QUALIFIED MEDICAL REVIEW.

THE THREE THAT MATTER      Top gaps, the decisions they block, what closes them
GAP INVENTORY              All identified, categorised, with the decision each
                           blocks — or an explicit "blocks no decision"
CONFIRMED HOW              Search strategies proving each gap is real
ALREADY BEING ANSWERED     Registry findings — gaps someone else is closing
PROPOSALS                  Ranked, with design, cost, timing, and credibility
ALLOCATION                 Funded, the line, and below it with what is lost
EXISTING DATA FIRST        Questions answerable from data already held
NOT PRIORITISED            Real gaps that block no decision — recorded, not lost
```

## Before you finish

Read `house-rules/evidence-gap-analysis.md`. Governance for evidence generation,
IIS processes, and the threshold for proposing a study differ substantially
between organisations.
