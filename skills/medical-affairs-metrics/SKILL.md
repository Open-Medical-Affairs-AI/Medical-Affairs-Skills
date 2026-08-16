---
name: medical-affairs-metrics
description: >-
  Measure whether Medical Affairs work changed anything, rather than counting
  how much of it happened. Use when building or reviewing an MA scorecard,
  setting KPIs and objectives, defending the function's value, choosing success
  measures for a plan or programme, or when a metric is driving behaviour nobody
  intended. The organising rule is that a measure which cannot come back
  negative is not a measure — and most Medical Affairs dashboards are built
  almost entirely from measures that cannot.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: workflow
  maturity: stable
  requires:
    - medical-affairs-foundations
    - strategic-analysis
  suggests:
    - field-medical-planning
    - medical-strategy-plan
    - field-insight-synthesis
    - deliverable-quality-review
  produces: Metric set with definitions, sources and interpretation limits
---

# Medical Affairs Metrics

Medical Affairs is measured badly almost everywhere, for a structural reason:
the things easiest to count — interactions, publications, enquiries, attendees —
are outputs of activity, and the things that matter are changes in understanding
and decisions, which are hard to attribute and slow to appear.

The result is dashboards full of numbers that go up, cannot go down, and tell
nobody anything.

## The test that does most of the work

**Could this measure come back negative, and would that tell us something we
would act on?**

- *Number of MSL interactions* — cannot meaningfully come back negative;
  measures effort, and rises whenever the team is told it is being watched.
- *Proportion of priority investigators who can accurately state the trial's
  primary endpoint and its principal limitation* — can absolutely come back
  negative, and if it does you know what to do.

Apply it to every metric. The ones that fail should be retained only as
**operational** measures (is the function functioning?) and clearly separated
from **impact** measures. Mixing them in one scorecard is what lets a function
report a green dashboard while achieving nothing.

## Three tiers, kept apart

| Tier | Question | Examples |
|---|---|---|
| **Activity** | Did the work happen? | Interactions, publications submitted, responses issued, programmes delivered, grants reviewed |
| **Quality** | Was it any good? | Insight actionability rate, response accuracy and turnaround, first-pass MLR approval rate, publication reporting-guideline compliance, time from question to answer |
| **Impact** | Did anything change? | Understanding shifts in a defined audience, evidence gaps closed that changed a decision, guideline evidence adopted, protocol amendments avoided by field input, questions the field can now answer that it could not |

Activity metrics belong in operational management. Only quality and impact
belong in a value conversation, and a scorecard presented to leadership that is
90% activity is telling them the function is busy.

## Impact measures that hold up

The credible ones share a shape: a defined audience, a defined thing that
changed, and a before-and-after that could have gone the other way.

- **Understanding.** Measured by asking. A short structured assessment across a
  defined group — can they state the endpoint, the population, the principal
  limitation? Repeat it after the intervention. This is uncomfortable precisely
  because it can fail, which is what makes it a measure.
- **Insight-to-decision.** Of the insights escalated this cycle, how many
  reached a decision forum, and how many changed something? Track the decision,
  not the escalation. A high escalation rate with no decisions is a reporting
  process, not an insight process.
- **Evidence gaps closed.** Of the gaps prioritised as decision-changing, how
  many now have an answer — and did the decision change?
- **Questions the field cannot answer.** Track the recurring unanswerable
  question. Its disappearance is real evidence that something worked; its
  persistence across cycles is real evidence that nothing did.
- **Guideline and HTA evidence adoption.** Did the committee cite the evidence,
  and did their "insufficient evidence" statement change? Slow, unambiguous,
  and directly attributable to published work.
- **Avoided rework.** Protocol amendments prevented by field feasibility input;
  MLR cycles saved by pre-review. Both countable and both genuinely attributable.
- **Time-to-answer** for medical information questions, measured from when the
  clinician asked.

## What to stop measuring

- **Interaction counts as a performance target.** They drive meetings with no
  purpose, and they degrade the relationship the meetings were meant to build.
- **Share of voice, message recall, message penetration.** These are promotional
  constructs. Their presence on a Medical Affairs scorecard is evidence the
  function is being run as a communication channel, and in several jurisdictions
  their presence is itself a compliance finding.
- **Anything correlated with prescribing at the individual HCP level.** Medical
  Affairs must not be measured on sales outcomes attributed to named clinicians.
  This is a boundary, not a preference.
- **Publication counts without regard to what was published.** Rewards volume,
  and quietly rewards salami-slicing.
- **Insight volume.** Rewards submission. Measure whether insights were
  actionable and acted on — see `field-insight-synthesis`.
- **Satisfaction scores as the primary quality measure.** People are satisfied
  with pleasant meetings.

## Attribution, honestly

Medical Affairs influences outcomes it does not control, over years, alongside
everything else. Overclaiming attribution is the fastest way to lose the
credibility of the whole scorecard.

Three honest positions, in descending strength: **direct** (the evidence we
published is cited in the guideline recommendation that changed); **contributory**
(understanding in this audience shifted over the period during which we ran this
programme, and no other obvious cause is identified); and **associated** (these
moved together, and we cannot separate them).

State which one you are claiming. A contributory claim clearly labelled is more
persuasive than a direct claim that does not survive a question.

## Designing a metric so it survives use

For each metric, define: what it measures; the **exact operational definition**;
the data source and its known biases; the cadence; the owner; the **target and
the reason for that number**; what would count as a bad result; and what
decision a bad result would trigger. A metric with no decision attached will be
reported and ignored.

**Anticipate the gaming.** Every metric creates an incentive; write down how this
one would be satisfied without doing the work, and decide whether you can live
with it. Interaction counts are met by short meetings. Insight counts are met by
low-value submissions. Turnaround time is met by answering easy questions first.
Publication counts are met by splitting papers. If a metric's cheapest path to
green is not the work you want, change the metric.

## Presenting it

Lead with what changed and what it means, not with the dashboard. Show the
measures that moved the wrong way and what is being done — a scorecard with no
red is not reassuring to an experienced reader, it is evidence the measures are
not measuring. Separate activity from impact visibly. State attribution level.
Say what you could not measure and why.

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus:

- For each metric: could it come back negative, and what would we do if it did?
- Are activity and impact measures visibly separated?
- Is any measure a promotional construct or correlated with individual-level
  prescribing?
- Is the attribution level stated for every impact claim?
- For each metric, what is the cheapest way to satisfy it without doing the
  work — and can we live with that?
- Does anything here have a target with no rationale behind the number?

## Before you finish

Read `house-rules/medical-affairs-metrics.md`. Scorecard structures, reporting
cycles and — importantly — which metrics are prohibited for the medical function
are set locally, and the prohibitions are frequently stricter than the general
standard.
