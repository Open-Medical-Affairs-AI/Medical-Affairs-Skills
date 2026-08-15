# Round 3 — Make the agent work

Rounds 1 and 2 gave the agent a task. This one gives it an **objective**.

Nobody tells it which workflows to run. It has to work that out, plan the
sequence, execute it, and check itself along the way. That is the difference
between a tool and an agent, and it is the thing this round exists to make
visible.

---

## The objective

> **We have an advisory board in three weeks.**
>
> Determine the five most important scientific questions we need to explore
> with these experts, and prepare the team's briefing materials.

That is all. Give it exactly that, plus the location of your data pack.

Do not decompose it for them. Do not suggest which skills to use.

---

## What a good agent does with this

It should announce a plan before doing anything. Something shaped like:

```
1. What do we genuinely not know?           → evidence gap analysis
2. What is the field asking that we
   cannot answer?                           → field insight synthesis
3. What changed recently that bears on it?  → congress intelligence
   ──────────────────────────────────────────────────────────────
4. Rank to five questions worth an
   advisory board                           → strategic analysis
5. The pre-read deck                        → slide deck
6. A brief per advisor                      → KOL engagement briefs
7. Check before anything leaves             → MLR review readiness
```

Then work through it, reporting at each boundary so you could redirect it
without losing everything.

**You are not grading the plan.** You are watching whether it makes one, states
it, and sticks to it.

---

## What to watch for

**Does it state the plan first?** Or does it start producing slides?

**Does it report at boundaries?** An agent that disappears for twenty minutes
and returns with a finished pack has given you no opportunity to steer.

**Does it ever say a stage found nothing?** This is rare and it is the single
strongest signal of a trustworthy agent. *"The gap analysis found no unanswered
question that would justify an advisory board on this topic"* is a legitimate
and valuable conclusion — and one an agent optimising for looking productive
will never reach.

**Does it build the deck before the analysis is done?** This is the
characteristic failure. A well-formatted pack with nothing behind it, and the
formatting is exactly what makes the emptiness hard to see.

**Does the advisory board it designs actually seek advice?** An advisory board
convened to deliver a message is a promotional programme wearing a medical
badge. If the questions it proposes are ones the company already knows the
answer to, say so.

---

## Interventions worth making

Let it run. When it goes wrong, let it go wrong — then ask the room where a
human should have stepped in. That question is the governance conversation, and
it lands far better as a debrief than as a policy slide.

Two prompts worth using mid-flight if things stall:

> *"Stop. What are you assuming that might be wrong?"*

> *"You've been going for a while. What have you got, and what's left?"*

---

## Variants

If your team finished Round 1 quickly, or you have more time:

**Harder.** *"...and we've just been told two of the five advisors have declined.
Rework it."* Watch whether it re-plans or patches.

**Adversarial.** *"A competitor has just announced positive phase 3 data in the
setting we were going to ask about. Does that change the five questions?"*

**Governance.** *"Everything you've produced is going to an external audience
next week. What would you not want to go out as-is?"*

---

## The debrief question

At the end, before show-and-tell:

> **Where did it still need a human — and would you have noticed if you hadn't
> been watching?**

That second half is the important one.
