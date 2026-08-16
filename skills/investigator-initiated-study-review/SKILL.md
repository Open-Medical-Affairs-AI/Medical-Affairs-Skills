---
name: investigator-initiated-study-review
description: >-
  Evaluate and govern investigator-initiated study proposals — IIS, ISR,
  IIT, investigator-sponsored research. Use when a proposal arrives for
  review, when designing or auditing the IIS programme itself, when deciding
  whether to support a study, or when an investigator asks what would make
  their proposal fundable. Covers scientific merit, feasibility, the
  compliance boundary that keeps an IIS genuinely investigator-owned, and
  the funding pattern that turns a legitimate programme into a compliance
  exposure. The study belongs to the investigator, not to the company.
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
    - real-world-evidence-design
    - deliverable-quality-review
  produces: IIS proposal assessment and recommendation
  network: [clinicaltrials.gov, eutils.ncbi.nlm.nih.gov]
---

# Investigator-Initiated Study Review

An investigator-initiated study belongs to the investigator. They conceived it,
they design it, they run it, they own the data, and they publish it regardless
of what it finds.

The company may support a study it considers scientifically valuable. It may not
direct the question, shape the design toward a preferred answer, or condition
support on the outcome. Every compliance failure in this area is a variation on
one of those three.

## The line, stated plainly

| Legitimate | Not |
|---|---|
| Investigator conceives and designs the study | Company suggests the question, then funds the proposal |
| Company assesses scientific merit and feasibility | Company negotiates the design toward a favourable endpoint |
| Support decided on merit | Support decided on the investigator's prescribing volume or influence |
| Investigator publishes whatever is found | Publication contingent on results, or subject to company approval beyond a factual review window |
| Investigator owns the data | Company controls analysis |
| Company may decline | Company shapes a decline into a redesign it wanted |

**The pattern is what gets examined, not the individual study.** Any single
funded proposal can look defensible. A programme where every funded study
happens to address a commercially useful question, in high-prescribing centres,
is a compliance exposure regardless of how each decision was documented.

Audit your own programme against that. If it is the case, say so.

## Assessing a proposal

### 1. Scientific merit

- **Is the question worth answering?** Would the answer change a decision
  someone makes? (`evidence-gap-analysis` — same test.)
- **Is it already answered?** Search the literature and the registry
  (`pubmed-search`, `clinical-trials-search`). Investigators often do not.
- **Is anyone else running it?** Including the company.
- **Can this design answer this question?** An underpowered study that will
  produce an uninterpretable result is not a kindness to fund. Say so, with the
  reason, and offer what would fix it — that is legitimate scientific feedback,
  not direction.
- **Will the result be believable** to the audience that needs convincing?

### 2. Feasibility

Recruitment realism (investigators systematically overestimate — ask what the
site's actual eligible population is), site capability, timeline, statistical
support, budget realism.

**Under-recruitment is the commonest failure mode.** A study that closes at 30%
of target has consumed the funding and answered nothing.

### 3. Safety and regulatory

Regulatory pathway (IND/CTA required?), safety reporting obligations and who
holds them, product supply, ethics approval, registration before enrolment.

**Safety reporting must be explicit in the agreement.** Ambiguity about who
reports what, to whom, in what timeframe is a serious risk that surfaces at
exactly the wrong moment.

### 4. Publication

Commitment to publish **regardless of outcome**, in the agreement. A company
review window for factual accuracy and confidential information is normal; a
right to delay or block publication is not, and non-publication of negative
results is a research-integrity failure the company would share in.

## The recommendation

State one of: **support**, **decline**, or **support conditional on** specific
changes — and be precise about which conditions are scientific feedback (fine)
versus direction (not).

Give the reason plainly. An investigator told "declined" learns nothing; one
told "the study is powered for a 15% difference and the observed effect in this
setting is around 6%, so it would be uninterpretable" gets something useful, and
may come back with a better proposal.

## Programme-level review

Run periodically, and be honest:

- **Distribution of questions.** Do funded studies cluster on commercially
  convenient topics?
- **Distribution of sites.** Correlated with prescribing volume?
- **Decline reasons.** Consistently applied, or applied more leniently to
  favourable proposals?
- **Publication rate.** What proportion of completed studies published? A low
  rate, particularly among negative studies, is the signal that matters.
- **Time to decision.** Slow decisions damage relationships and are a quiet
  form of decline.

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus:

- Would we fund this if the result were guaranteed to be unfavourable?
- Is any "condition" actually direction?
- Have we checked whether this is already being answered?
- Does the programme pattern look like science or like marketing?

## Before you finish

Read `house-rules/investigator-initiated-study-review.md`. IIS governance,
review committees, contracting and funding thresholds are entirely local and
this is an area where local process is the control.
