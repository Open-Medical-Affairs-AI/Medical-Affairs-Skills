---
name: strategic-analysis
description: >-
  Reason about Medical Affairs strategy rather than generating activity
  lists. Use when building or challenging a medical plan, prioritising
  evidence generation, allocating limited budget or headcount, assessing a
  competitive or landscape shift, deciding what to stop doing, or answering
  "so what should we do about it". Provides so-what laddering, the
  distinction between a strategy and a list, assumption surfacing and
  testing, pre-mortem analysis, and prioritisation under real constraints.
  Load whenever someone asks for recommendations or priorities — especially
  to critique one that already exists.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: primitive
  maturity: stable
  requires:
    - medical-affairs-foundations
  produces: Prioritised strategic choices with stated assumptions and trade-offs
---

# Strategic Analysis

The question this skill exists to force: **should we be doing this at all?**

An agent asked to build a medical plan will produce a competent list of
activities. Every one will be defensible in isolation. Collectively they will
have no logic, no priority, and no way to tell whether dropping any of them
would matter. That is the default failure of medical planning with or without
AI, and it is worth resisting hard.

## Strategy is choosing what not to do

A strategy is a set of choices under constraint. If a plan contains no
trade-offs, nothing was chosen.

**The diagnostic questions:**

- What are we deliberately **not** doing, and why?
- If our budget were cut 30%, what would go — and what does that reveal about
  what we actually believe?
- What would a competitor most want us to keep spending on?
- Which of these activities, if it did not happen, would nobody notice?

That last question is the sharpest. Ask it of every line in a plan. Activities
that survive it are the plan; the rest are habit.

## The so-what ladder

Take every finding up until it reaches a decision.

```
FACT              What is true.
   ↓ so what?
INTERPRETATION    What it means.
   ↓ so what?
IMPLICATION       What it changes for us.
   ↓ so what?
CHOICE            What we should do differently — and what we give up to do it.
```

**Worked example:**

> **Fact.** Three competitors presented subcutaneous formulations at the last
> two congresses.
> **So what?** Administration burden is becoming a competitive dimension, not
> just a convenience feature.
> **So what?** Our evidence and narrative are built almost entirely on efficacy.
> If the field's decision criterion shifts to burden, our differentiation
> argument stops addressing the question clinicians are asking.
> **So what?** We need real-world evidence on treatment burden and its effect on
> adherence within 12 months — which means displacing something from the current
> evidence plan. The candidate is the fourth-line expansion analysis, which
> answers a question nobody is asking.

That final trade-off is where most analysis stops short: a recommendation with
no stated cost is a wish.

## Surfacing assumptions

Every strategy rests on beliefs about the future that may be wrong; naming them
turns an argument into something testable. For each significant recommendation,
write down:

| Assumption | If wrong, what breaks | How would we know early? |
|---|---|---|

Assumptions that recur in Medical Affairs plans, worth checking explicitly:

- The competitor's readout will be positive / negative
- Guidelines will update within the planning horizon *(they usually will not —
  guideline cycles are slower than medical plans and require published evidence
  well in advance)*
- The label will expand on schedule
- Clinicians care about the dimension we are strongest on
- Our KOLs' views represent the broader prescribing community *(they very often
  do not — academic and community practice diverge systematically)*
- Field insight reflects the market, not who our MSLs preferentially visit
- The evidence gap we identified is one clinicians actually feel

**The highest-value analytical move** is identifying the single assumption the
whole plan depends on and proposing the cheapest way to test it early.

## Pre-mortem

Before finalising, assume it is eighteen months later and the plan failed
completely. Write the explanation.

This surfaces risks a forward-looking assessment reliably misses, because it
converts "what could go wrong" — which invites reassuring answers — into "what
did go wrong", which invites honest ones. Then, for each failure mode: is it
detectable early, preventable, and survivable? Failure modes that are none of
the three should change the plan.

## Prioritisation

Ranking everything "high priority" is not prioritisation. Force distinction.

**Dimensions that matter for Medical Affairs choices:**

- **Decision impact** — does this change a decision someone will actually make?
  It dominates everything else.
- **Scientific value** — a real question, or confirmation of what is believed?
- **Feasibility** — in the time available, with the data and access we have?
- **Timing fit** — does it land inside the window where it can influence
  anything? A perfect analysis delivered after the planning cycle closes changes
  nothing until next year.
- **Differentiation** — only we can do it, or table stakes?
- **Cost of not doing it** — the question that separates genuine priorities from
  comfortable ones.

**Forced ranking beats scoring matrices.** Weighted scoring produces a spurious
number and hides the judgement; ordering items 1 to N and defending each
adjacent pair exposes it. If two genuinely cannot be separated, say so rather
than resolving it with an arbitrary weight.

**Under a hard constraint** — a fixed budget, a fixed headcount — allocate
explicitly, state what falls below the line, and say what the organisation loses
by not funding it. The below-the-line list is as informative as the funded one,
and it is what a leadership team actually debates.

## Challenging an existing plan

When handed a medical plan, an evidence strategy, or a set of proposed
activities, this is the review:

1. **Trace every activity to a priority.** Any that trace to nothing are either
   orphans or reveal an unstated priority. Both are worth surfacing.
2. **Trace every priority to a decision or outcome.** A priority that changes
   nothing is a theme.
3. **Check the logic actually holds.** Does the proposed activity plausibly
   produce the claimed effect? "Increase KOL engagement" does not by itself
   produce guideline inclusion — guideline inclusion is driven by published
   evidence assessed by committees on their own cycles. Plans routinely contain
   this kind of missing mechanism.
4. **Look for what is missing.** Which important questions has the plan not
   addressed? Absence is harder to see than error.
5. **Check the resourcing is real.** Is the same person named on nine
   activities? Does the timeline assume nothing goes wrong?
6. **Ask what success looks like.** If nobody can say how they would know it
   worked, it will not be evaluated and will be repeated next year regardless.

**Report the challenge honestly, including when the plan is sound.** An analysis
that manufactures criticism to look rigorous is as useless as one that rubber-
stamps. If three of twelve activities do not trace to a priority, say that — and
say the other nine do.

## Landscape and competitive analysis

Analyse what changed and what it means, not what exists. Five questions:

- **What is the current standard of care, really?** Guidelines lag practice, and
  practice varies by setting and geography.
- **What changed recently, and does it alter a decision?** Most changes do not,
  and saying so is a legitimate conclusion.
- **Where is the field's attention moving?** The dimension on which products are
  compared shifts over time — efficacy, then safety, then burden, then access —
  and a narrative built for the previous dimension quietly stops working.
- **What are competitors investing in that we are not**, and is that a gap or a
  deliberate choice?
- **What would have to be true for our current position to be wrong?**

Competitive analysis is legitimate internal intelligence; it becomes a problem
the moment it turns into external comparative claims without head-to-head
evidence (`medical-affairs-foundations`).

## Output

```markdown
## Strategic recommendation

**The choice:** [what to do, in one sentence]
**What we give up:** [the trade-off — required, not optional]
**Why now:** [the timing logic]

### Reasoning
The so-what chain, ending in the decision.

### Assumptions this rests on
| Assumption | If wrong | Early indicator |

### What we are deliberately not doing
And why.

### Pre-mortem
It failed. Here is the most likely reason, and whether we would see it coming.

### How we would know it worked
A measure that could actually come back negative.
```

That last requirement is not a formality. A success measure that cannot fail is
not a measure, and its presence in a plan is a reliable sign that nobody intends
to evaluate the activity.

## Before you finish

Read `house-rules/strategic-analysis.md`. Planning frameworks, priority
definitions and governance vary considerably, and the local vocabulary matters
for a document that must survive a leadership review.
