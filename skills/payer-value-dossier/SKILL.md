---
name: payer-value-dossier
description: >-
  Build evidence for payers and health technology assessment bodies — AMCP
  format dossiers, NICE, G-BA and HAS submissions, value propositions,
  budget impact narratives, and responses to HTA critique. Use when
  preparing payer or HTA material, when an assessment has rejected or
  restricted a product, or when someone asks what payers need that
  clinicians do not. Payer audiences apply different evidence standards —
  comparative effectiveness against the real comparator, absolute benefit,
  cost consequence — and material written for clinicians consistently fails
  with them.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: workflow
  maturity: beta
  requires:
    - medical-affairs-foundations
    - evidence-synthesis
  suggests:
    - evidence-appraisal
    - systematic-literature-review
    - citation-integrity
    - deliverable-quality-review
  produces: Payer value dossier or HTA evidence submission
---

# Payer and HTA Value Dossier

Payers ask a different question from clinicians. A clinician asks *does this
work for my patient?* A payer asks *is this worth funding for this population,
relative to what we fund now?*

Material that answers the first question consistently fails the second, and the
gap is not presentational — it is evidentiary.

## What payers need that clinicians do not

| Clinician evidence | Payer evidence |
|---|---|
| Efficacy vs the trial comparator | Effectiveness vs **what is actually funded now** |
| Relative effect | **Absolute** benefit, and how many patients gain it |
| Response rate | Outcomes that carry cost — hospitalisation, progression, mortality |
| Trial population | The population they will actually fund, including those the trial excluded |
| "Works" | Works **enough**, at this price, versus the alternative |
| Safety profile | Cost consequences of managing toxicity |

**The comparator is where submissions fail most often.** Registration trials
compare against what was standard when they were designed. HTA bodies assess
against what is standard now. If those differ, the pivotal evidence does not
answer the question being asked, and no amount of writing fixes it — it needs an
indirect comparison (`evidence-appraisal/references/indirect-comparisons.md`)
with its assumptions stated, or new evidence.

## The framework by body

**AMCP Format** (US managed care) — product information, place in therapy,
supporting clinical and economic evidence, modelling report. Unsolicited
provision is constrained; understand the request pathway before responding
(`medical-affairs-foundations`).

**NICE** (England) — cost-effectiveness against a threshold, with the ICER
central. Committee documents are public, and the *reasons for a negative or
restricted recommendation are the most specific evidence-gap statement you will
ever be given.* Read them before designing anything.

**G-BA / IQWiG** (Germany) — added benefit against a defined comparator, graded.
Extremely strict on comparator choice and on which endpoints count; patient-
relevant endpoints only, and the definition is narrower than most sponsors
expect.

**HAS** (France) — SMR and ASMR, with clinical benefit and improvement graded
separately.

Each has published methods. Read the actual guide, not a summary.

## Building the dossier

**1. Define the decision problem.** Population, intervention, comparator,
outcomes, and the perspective (payer, societal). Get this wrong and everything
downstream is wrong.

**2. Systematic evidence base.** HTA bodies expect systematic identification,
not selective citation — see `systematic-literature-review`. A submission with
a non-systematic evidence base is discounted.

**3. Comparative effectiveness.** Direct where it exists; adjusted indirect
comparison where it does not, with assumptions stated. Naive comparison will be
identified and dismissed.

**4. Absolute benefit.** NNT with its time horizon, absolute risk difference,
events avoided per 1,000 patients treated. Relative measures alone are the
commonest reason a strong clinical story reads as weak to a payer.

**5. Economic evidence.** Model structure, inputs, assumptions, sensitivity
analysis. State the assumptions the result is most sensitive to — reviewers find
them anyway, and finding them yourself is what credibility looks like.

**6. Budget impact.** Eligible population, uptake assumptions, offsets. Uptake
assumptions are scrutinised hard; justify them.

**7. Uncertainty.** State it. HTA reviewers are professional identifiers of
overstated certainty, and a submission that acknowledges its weaknesses is
treated more seriously than one that does not.

## Responding to a negative or restricted assessment

The reasons are published and specific. Work through them literally:

- Which were **evidence** gaps? → `evidence-gap-analysis`
- Which were **comparator** disagreements? → indirect comparison, or accept it
- Which were **modelling** assumptions? → sensitivity analysis, better inputs
- Which were **price**? → not a Medical Affairs problem; say so plainly rather
  than trying to solve it with evidence

Do not respond to a price objection with more clinical data. It is a common and
transparent move.

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus:

- Is the comparator what is **actually funded now**, or what the trial used?
- Is absolute benefit stated, not only relative?
- Was the evidence base identified systematically?
- Are the model's most sensitive assumptions stated up front?
- Would a hostile reviewer find an uncertainty we did not declare?

## Before you finish

Read `house-rules/payer-value-dossier.md`. Submission templates, the boundary
between Medical Affairs and Market Access, and rules on unsolicited provision
of health-economic information are all local and vary substantially.
