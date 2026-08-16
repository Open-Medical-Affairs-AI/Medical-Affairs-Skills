---
name: medical-strategy-plan
description: >-
  Build or challenge a medical plan — the scientific priorities, the choices
  behind them, and the activities that trace to them. Use for annual medical
  planning, therapeutic area strategy, landscape and situation assessment,
  and requests like "develop our medical plan", "what should our priorities
  be next year" or "review this medical plan". Enforces what separates a
  strategy from an activity list: every activity traces to a priority, every
  priority to a decision, every choice states what is given up, and every
  success measure could come back negative.
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
    - evidence-synthesis
    - insight-generation
    - clinical-trials-search
    - deliverable-quality-review
  produces: Medical plan with prioritised scientific objectives
  network: [eutils.ncbi.nlm.nih.gov, clinicaltrials.gov]
---

# Medical Strategy Plan

The failure mode is so consistent it is almost a genre: fifty activities, each
individually defensible, with no logic connecting them, no priority between
them, and no way to tell whether dropping any would matter.

An agent asked to build a medical plan will produce exactly this, competently
and quickly. Resisting it is the point of this skill.

## The three tests

Apply these to everything the plan contains. They are the difference between a
strategy and a list.

1. **Every activity traces to a priority.** If it does not trace, either the
   activity should go or a priority is unstated. Say which.
2. **Every priority traces to a decision or an outcome.** A priority that
   changes nothing is a theme.
3. **Every choice states what it costs.** A recommendation with no trade-off has
   not been thought through — it is a wish.

## Stage 1 — Inventory

- Current medical plan and what actually happened against it
- Evidence landscape — ours and competitors'
- Field insights (`field-insight-synthesis`)
- Competitive intelligence and upcoming readouts
- Lifecycle stage and upcoming milestones
- Disease-state context, treatment pathway, unmet need
- Resource envelope — headcount, budget, what is fixed
- Cross-functional context: what commercial, access and R&D are planning

**Name what you are missing.** A plan built without knowing the resource
envelope will allocate resources that do not exist, and everyone downstream
will know it.

## Stage 2 — Retrieve

- `clinical-trials-search`: what is running that will change the landscape
  inside the planning horizon, and when it reads out
- `pubmed-search`: recent evidence shifts, guideline activity, and what the
  field is publishing about
- Evidence gaps already identified (`evidence-gap-analysis`)

## Stage 3 — Analyse

### Situation — what is actually true now

Not a data dump. Four questions:

- **What is the standard of care, really?** Guidelines lag practice, and
  practice varies by setting and geography.
- **What changed since the last plan, and did it change anything for us?** Most
  changes do not. Saying so is a legitimate conclusion.
- **Where is the field's attention moving?** The dimension on which products are
  compared shifts — efficacy, then safety, then burden, then access — and a
  strategy built for the previous dimension stops working quietly.
- **What do we not know that matters?**

### Priorities — the choosing part

Three to five. More than five is not a set of priorities.

Each priority needs:

- **A statement of what we are trying to achieve** — an outcome, not an activity
- **Why it matters** — the decision or consequence it bears on
- **Why it outranks the things below it**
- **What we are giving up** to pursue it

Use forced ranking rather than a scoring matrix (`strategic-analysis`). Weighted
scores produce a spurious number and hide the judgement; defending each adjacent
pair exposes it.

### Activities — earned, not assumed

For each activity: which priority it serves, what it produces, who owns it, when,
what it costs, and **what happens if it does not occur**.

That last column is the useful one. Run it down the list. Activities where the
answer is "nothing much" are habit, and cutting them is where the capacity for
the real priorities comes from.

**Check the causal logic actually holds.** Plans routinely contain activities
whose stated effect does not follow from them. "Increase KOL engagement" does
not produce guideline inclusion — guideline inclusion is driven by published
evidence assessed by committees on their own cycles. When you find a missing
mechanism, say so; it is one of the most valuable things this analysis produces.

### Assumptions and pre-mortem

Surface the assumptions the plan depends on, with what breaks if each is wrong
and how you would know early (`strategic-analysis`).

Then run the pre-mortem: it is eighteen months later, the plan failed, write
why. Convert "what could go wrong" into "what did go wrong" and the answers get
honest.

### Success measures that can fail

For each priority, a measure that could genuinely come back negative. "Number of
KOL interactions" cannot fail; it only measures activity. "Proportion of field
scientific questions we could answer with published evidence" can, and tells you
something.

If nobody can say how they would know it worked, it will never be evaluated —
and it will be repeated next year regardless of outcome.

## Stage 4 — Challenge

This is where the skill earns its place, whether the plan is yours or someone
else's.

- **Trace every activity to a priority.** Report the orphans by name.
- **Trace every priority to a decision.** Report the themes.
- **Check the mechanism** for each claimed effect.
- **Is anything deliberately not being done?** A plan with no exclusions has not
  chosen anything.
- **Is the resourcing real?** Same person on nine activities, timelines assuming
  nothing slips.
- **Does the timing fit the cycle?** Analysis landing after the budget closes
  changes nothing until next year.
- **Would a competitor be pleased to see this plan?** If it is all defensive
  maintenance, they would.

Run `deliverable-quality-review`.

**Report the challenge honestly, including when the plan is sound.**
Manufacturing criticism to look rigorous is as useless as rubber-stamping. "Nine
of twelve activities trace cleanly; these three do not, and here is why" is the
useful form.

## Stage 5 — Deliver

Use `shared/templates/medical-plan.md`.

```
DRAFT — NOT FOR EXTERNAL USE. REQUIRES QUALIFIED MEDICAL REVIEW.

THE STRATEGY IN A PARAGRAPH   What we are choosing to do and not do
SITUATION                     What is true now, what changed, what it means
PRIORITIES                    3-5, each with rationale and trade-off
ACTIVITIES                    Traced to priorities, owned, timed, costed
NOT DOING                     Explicit, with reasons
ASSUMPTIONS                   What this rests on, what breaks it, early signals
PRE-MORTEM                    Why it failed, and whether we would see it coming
MEASURES                      Per priority, capable of coming back negative
EVIDENCE GAPS                 Routed to evidence generation
```

Lead with the strategy paragraph. Someone reading only that should be able to
say what the function is choosing to do.

## The compliance boundary

Medical Affairs plans are non-promotional. A medical plan built around
supporting a commercial objective — even when the activities look scientific —
is precisely what enforcement actions have targeted. Priorities should be
scientific: closing evidence gaps, answering clinical questions, supporting
appropriate use, advancing understanding of the disease.

Cross-functional alignment is legitimate and expected. Cross-functional
direction is not.

## Before you finish

Read `house-rules/medical-strategy-plan.md`. Planning frameworks, priority
vocabulary, template structure, and governance vary a great deal — and a plan
that uses the wrong local vocabulary will struggle in review regardless of its
quality.
