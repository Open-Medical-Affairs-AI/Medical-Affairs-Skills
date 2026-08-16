---
name: real-world-evidence-design
description: >-
  Design a real-world evidence study that will survive scrutiny — target trial
  emulation, data source selection, the estimand, confounding control, and a
  protocol written and registered before the data are touched. Use when
  proposing or designing an RWE study, choosing between claims, EHR and registry
  data, planning an external control arm, or when someone asks what evidence to
  generate outside a trial. This designs a study; `evidence-appraisal` judges one
  somebody else ran, and `evidence-gap-analysis` decides whether the question is
  worth answering at all.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: workflow
  maturity: stable
  requires:
    - medical-affairs-foundations
    - evidence-appraisal
  suggests:
    - evidence-gap-analysis
    - clinical-trials-search
    - integrated-evidence-plan
    - deliverable-quality-review
  produces: RWE study concept or protocol with the estimand and design stated
  network: [clinicaltrials.gov]
---

# Real-World Evidence Design

Most RWE fails not because the data were poor but because the question was never
specified precisely enough to be answered. Target trial emulation fixes that by
forcing you to describe the randomised trial you would have run, then say how
each element is approximated in the data you have.

## Start with the target trial

Write the protocol of the trial you cannot run. Seven elements, all of them
before you look at any data:

| Element | Specify |
|---|---|
| **Eligibility** | Who would be enrolled — using only information available at baseline |
| **Treatment strategies** | The interventions being compared, including duration and what counts as adherence |
| **Assignment** | Randomised in the target trial; in the emulation, how does treatment get assigned and what determines it? |
| **Follow-up start** | When time zero begins — for every arm, at the same point in the disease course |
| **Outcome** | Defined operationally in the data, with the algorithm and its validation |
| **Causal contrast** | Intention-to-treat or per-protocol. Say which. |
| **Analysis plan** | The estimator, the confounders, and the sensitivity analyses — written first |

Then, element by element, state how the observational data emulates it and where
the emulation breaks. **The places it breaks are the limitations section**, and
writing them at design time is the difference between a limitation and a
reviewer's finding.

## The estimand, stated plainly

Before methods, state: in **which population**, comparing **what strategy** to
**what alternative**, on **what outcome**, over **what horizon**, handling
**which intercurrent events** in which way (treatment discontinuation, switching,
death as a competing risk).

An RWE study without a stated estimand produces a number that different readers
interpret differently, which is how the same analysis gets cited for
contradictory claims.

## The named biases, and the design choices that address them

These recur in almost every database study. Each has a design fix; none has an
analysis fix that works reliably after the fact.

- **Confounding by indication.** Sicker patients get different treatment. The
  central threat. Address with active comparator + new user design, rich
  baseline covariates, propensity methods, and negative control outcomes.
- **Immortal time bias.** Time between time zero and treatment initiation during
  which the outcome cannot occur, misassigned to the treated arm. Produces
  spectacular spurious benefit. Fix by aligning time zero with eligibility and
  treatment assignment, or by using a cloning/censoring/weighting design.
- **Prevalent user bias.** Enrolling patients already on treatment conditions on
  survival and tolerance. Use a new-user design.
- **Depletion of susceptibles.** Related: those who would react badly have
  already stopped, making the drug look safer than it is.
- **Outcome misclassification.** Claims and EHR outcomes are algorithms, not
  observations. Use a validated algorithm, report its PPV and sensitivity, and
  run a quantitative bias analysis if the outcome is the point of the study.
- **Informative censoring.** Loss to follow-up related to prognosis. Address
  with IPCW, and report censoring rates by arm.
- **Unmeasured confounding.** Always present. Report an E-value or equivalent
  quantifying how strong an unmeasured confounder would need to be to explain
  the result away.

**Active comparator, new user (ACNU) is the default design.** Non-user
comparisons are only rarely defensible, because "not treated" is a heterogeneous
state driven by the same factors that drive the outcome.

## Choosing a data source

| Source | Strong for | Weak for |
|---|---|---|
| **Administrative claims** | Complete capture of billed events, large N, longitudinal continuity while enrolled | No clinical detail — no labs, stage, performance status, biomarkers. Enrolment gaps break follow-up. |
| **EHR** | Clinical richness, labs, notes | Care outside the network is invisible; missingness is informative; structured fields are inconsistently populated |
| **Disease registry** | Curated, clinically specific, often includes staging and biomarkers | Selection into the registry; smaller N; site-dependent completeness |
| **Linked claims-EHR** | Combines completeness with detail | Linkage error, restricted subpopulation, higher governance burden |
| **Patient-generated / wearable** | Outcomes patients experience, between visits | Adherence to collection, device drift, non-representative adopters |
| **Chart review** | Anything the coded data cannot give you | Cost, abstractor variability, small N |

Check **fitness for purpose** explicitly: is the exposure identifiable? Is the
outcome validated in *this* database? Are the confounders measured, at baseline?
Is follow-up long enough? Is the population the one you care about? A source can
be excellent and still unfit for one specific question.

## External control arms

When a single-arm trial needs a comparator, an external control can support a
regulatory or HTA argument — but only under conditions that are usually stated
too loosely.

Required: the same eligibility criteria applied to the external cohort; the same
outcome definition and assessment schedule (or an explicit adjustment for the
difference); contemporaneous data where possible, because standard of care
moves; baseline covariate balance achieved and demonstrated; and a
pre-specified analysis. Regulators have accepted external controls in rare
disease and in settings with a stable natural history, and have rejected them
where standard of care changed or outcome assessment differed.

Say plainly which of these conditions your design does not meet.

## Registration, transparency, and the protocol

Register the protocol before analysis — ClinicalTrials.gov, EU PAS Register, or
HMA-EMA Catalogues of RWD studies — and record the registration number in every
output. Follow the reporting guideline for the design at publication: **RECORD**
(and RECORD-PE for pharmacoepidemiology) extends STROBE for routinely collected
data; **STaRT-RWE** structures the design specification; **SPIRIT** applies to
prospective protocols.

The single most damaging RWE practice is analysing first and specifying after.
It is also usually invisible in the published paper, which is exactly why
registration matters. If a design change is genuinely needed after seeing the
data, record it as a protocol amendment with the date and the reason.

## Governance

Data use agreements, IRB or ethics determination, and privacy law (HIPAA, GDPR
including the legal basis for secondary use) all attach before analysis. Patient
privacy in RWE is not satisfied by de-identification alone at small cell counts —
apply the cell-suppression rules the data holder requires, and never report a
cell small enough to identify anyone.

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus:

- Is the target trial written out, and is every element mapped to the data?
- Is the estimand stated, including intercurrent events?
- Is this new-user, active-comparator? If not, why is the alternative defensible?
- Is time zero identical across arms, and is immortal time impossible by design?
- Is the outcome algorithm validated *in this data source*, with its PPV stated?
- What is the E-value, and is it plausible that unmeasured confounding is that
  strong?
- Would we accept this design from a competitor claiming the opposite result?

## Before you finish

Read `house-rules/real-world-evidence-design.md`. Data source access, approval
pathways for RWE studies and registration practice vary considerably, and some
organisations require internal epidemiology sign-off before a concept is shared
externally.

`evidence-appraisal` carries the appraisal side of the same material: its
real-world-evidence reference covers target trial emulation from the reader's
perspective rather than the designer's.
