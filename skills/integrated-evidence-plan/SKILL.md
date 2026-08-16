---
name: integrated-evidence-plan
description: >-
  Build the cross-functional evidence plan for an asset — every study, analysis
  and publication across clinical development, Medical Affairs, HEOR and market
  access, sequenced against the decisions and milestones each has to serve. Use
  when asked for an integrated evidence plan or IEP, when planning evidence
  across functions or across a product lifecycle, or when reconciling competing
  evidence requests under one budget. This is the whole plan across functions;
  `evidence-gap-analysis` identifies and ranks the gaps that feed it.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: workflow
  maturity: stable
  requires:
    - medical-affairs-foundations
    - strategic-analysis
    - evidence-appraisal
  suggests:
    - evidence-gap-analysis
    - real-world-evidence-design
    - payer-value-dossier
    - deliverable-quality-review
  produces: Integrated evidence plan with sequencing, owners and decision links
---

# Integrated Evidence Plan

An integrated evidence plan exists because the same asset is asked different
questions by regulators, payers, guideline committees, clinicians and patients —
and because generating evidence for one audience at a time produces a portfolio
that answers the regulatory question thoroughly and everything else late.

`evidence-gap-analysis` finds and ranks the gaps. This skill turns a ranked gap
list into a sequenced, owned, funded plan across functions.

## The four audiences and what each requires

They are not variations on one standard. They diverge on comparator, endpoint
and time horizon, and a plan that ignores the divergence produces evidence that
satisfies one and none of the others.

| Audience | Comparator | Endpoint they act on | Timing |
|---|---|---|---|
| **Regulator** | Placebo or established standard, as agreed | The pre-specified primary endpoint, with the licence at stake | Fixed to submission |
| **HTA / payer** | The comparator actually used in that country's pathway — often not the trial comparator | Comparative effectiveness, absolute benefit, cost consequence, quality of life | Assessment window, frequently within months of approval |
| **Guideline committee** | Whatever their methodology accepts | Published evidence surviving their appraisal | Their own cycle — see `guideline-engagement` |
| **Clinician** | The alternative they are choosing between today | Practical: sequencing, subpopulations, management, real-world tolerability | Continuous, and unforgiving of gaps |

**The recurring structural failure** is a development programme comparing
against a comparator no payer accepts, discovered at HTA submission when it is
years too late to fix. Surfacing that at plan time is one of the highest-value
things this skill does.

## Building the plan

**1. Assemble the evidence requirements** from every function — clinical
development, Medical Affairs, HEOR, market access, regulatory, and where they
have a view, patient advocacy. Collect them as *questions with decisions
attached*, not as study proposals. A proposal already encodes a design choice
that may not be the best way to answer the question.

**2. Map each question to the decision it serves** and to who makes it. A
question no one is waiting on is not an evidence requirement; it may still be
worth doing, but it competes on different grounds.

**3. Deduplicate.** Different functions routinely ask overlapping questions in
their own vocabulary. One well-designed study frequently serves three of them —
and finding those is where the "integrated" in the name earns its place.

**4. Choose the vehicle for each question.** The design follows the question and
the evidence standard of the audience that needs it:

| Question type | Usual vehicle |
|---|---|
| Efficacy and safety for licensure | Registrational trial |
| Comparative effectiveness vs. real-world comparator | Head-to-head trial, or RWE via `real-world-evidence-design` |
| Long-term safety and durability | Registry, extension study, RWE |
| Sequencing, subpopulations, practical use | RWE, IIS, secondary analysis, sometimes a pragmatic trial |
| Quality of life, patient experience | PRO instruments embedded prospectively — retrofitting is not possible |
| Economic and budget impact | Economic model with parameters the trials must supply |
| Indirect comparison | Prospective design of the ITC, planned before the data exist |

**5. Sequence backwards from when the answer is needed**, not forwards from
when the data arrive. Work back through publication lead time, analysis, data
maturity, enrolment, start-up and approval. Guideline evidence cut-offs and HTA
submission windows are hard dates, and most plans discover the impossibility of
their sequencing only after committing to it.

**6. Allocate under the real constraint.** Fixed budget, fixed headcount, fixed
data access. Rank, fund down the list, and state explicitly what falls below the
line and what the organisation gives up. The below-the-line list is what
leadership actually debates.

**7. Assign owners.** Every item: an accountable function, a named decision it
feeds, a date, and a publication route. Evidence that is generated and not
published does not exist to a guideline committee.

## The plan on a page

For each evidence item: the **question**; the **decision and audience** it
serves; the **vehicle**; the **owner**; **start and readout dates**; the
**publication plan**; **dependencies**; and the **cost**. Anything that cannot
fill all eight is not ready to be in the plan.

Alongside it, three lists that get skipped and should not be: what we are
**deliberately not doing** and why; the **assumptions** the sequence depends on,
with early indicators; and the **evidence a competitor is generating** that
would change this plan if it reads out positively.

## Lifecycle shape

- **Pre-approval** — registrational evidence dominates, but this is the only
  moment when HTA comparators, PRO instruments and economic model parameters can
  still be built into a trial. Most integrated-evidence value is created or lost
  here.
- **Launch** — the questions clinicians ask arrive immediately and the plan must
  already have routes to answer them. See `launch-medical-readiness`.
- **Established** — RWE, sequencing, long-term outcomes, subpopulations,
  guideline-directed evidence, and the HTA re-assessments that follow.
- **Late lifecycle** — decide what to stop. Generating evidence for a question
  nobody is asking any more is a real and common failure.

## Governance

An IEP is a live document with a review cadence, not an annual artefact. Changes
worth a formal review: a competitor readout, a guideline update, an HTA
rejection, a safety signal, a regulatory interaction that changes expectations.

Keep the boundary visible throughout. Company-sponsored research is company-run;
investigator-initiated studies belong to the investigator and cannot be planned
as company deliverables — see `investigator-initiated-study-review`. An IEP that
counts a hoped-for IIS as a planned evidence item has crossed that line on paper
before anyone crossed it in practice.

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus:

- Does every item name a decision, an audience and an owner?
- Is the HTA comparator addressed, and does it match the trial comparator? If
  not, is that stated as a risk with a mitigation?
- Does the sequencing work backwards from evidence cut-offs and submission
  windows, and is it actually achievable?
- Are PROs and economic parameters built in while it is still possible?
- What is below the line, and does the plan say what is lost by it?
- Are any IIS or external studies counted as though we control them?
- Which single assumption, if wrong, breaks the most of this plan?

## Before you finish

Read `house-rules/integrated-evidence-plan.md`. Governance, who owns the IEP,
and the approval route for evidence commitments differ substantially between
organisations, and in many the plan itself is a controlled document.
