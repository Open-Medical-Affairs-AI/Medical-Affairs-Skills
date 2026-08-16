---
name: advisory-board-design
description: >-
  Design and run an advisory board that produces advice rather than
  agreement — charter, questions, advisor selection, fair market value,
  discussion design, and output that changes a decision. Use when planning
  an advisory board, expert panel, steering committee or scientific
  roundtable. Covers the compliance boundary between a legitimate advisory
  board and a promotional programme wearing a medical badge. This is one
  meeting: for the strategy it feeds use medical-strategy-plan, for briefing
  an individual advisor use kol-engagement-brief.
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
    - evidence-gap-analysis
    - kol-engagement-brief
    - medical-strategy-plan
    - deliverable-quality-review
  produces: Advisory board charter, questions and materials
---

# Advisory Board Design

An advisory board is the company asking for help with a question it cannot
answer. Everything that makes one legitimate — and everything that makes one
useful — follows from taking that sentence literally.

## The test

**Could the answer surprise you?**

If not, you are not seeking advice. You are seeking endorsement, and experienced
advisors detect this within the first hour, adjust their behaviour accordingly,
and give you agreement instead. You will then act on agreement you mistook for
advice.

An advisory board convened to deliver a message is a promotional programme with
a medical badge, and enforcement history treats it as one.

## Stage 1 — Establish the question

Before anything else: **what do we not know, that these people know, that would
change what we do?**

Write it down. Then check it against three failure modes:

- **We already know the answer.** Then this is a communication meeting. Call it
  that, or cancel it.
- **They cannot answer it either.** A question requiring data nobody has is a
  research question (`evidence-gap-analysis`), not an advisory question.
- **The answer would change nothing.** Interesting is not the same as
  actionable. Name the decision it feeds.

`evidence-gap-analysis` and `field-insight-synthesis` are the two best sources
of genuine questions — gaps you cannot close with data, and questions the field
is being asked that nobody can answer.

## Stage 2 — Charter

Written before invitations go out, because the invitation depends on it:

- **The question**, specifically
- **The decision it informs**, and who makes it
- **Why external advice is needed** — what the company cannot determine alone
- **What will be done with the output**, and how advisors will be told
- **Number of advisors**, with the reason. A defensible number is one where
  every person is there because of what they specifically bring. Thirty advisors
  is a broadcast.
- **Selection criteria**, applied before names
- **Compensation basis** — fair market value, by role and time
- **Who from the company attends, and why.** Commercial attendance at a medical
  advisory board needs a reason that survives scrutiny.

## Stage 3 — Select advisors

**Criteria first, names second.** Reversing this is how a list of the friendliest
KOLs becomes an advisory board.

Cover the perspectives the question needs — which almost always means including
people who will disagree, community as well as academic practice, and at least
one person who has publicly criticised your position. A panel of supporters
cannot tell you what is wrong with your plan.

Watch for: the same advisors on every board (they become house experts and stop
being external), advisors selected by prescribing volume (a commercial criterion
in a medical activity), and a panel with no one from the setting where most
patients are actually treated.

## Stage 4 — Design the discussion

**Weight the agenda toward questions.** If data presentation occupies more time
than discussion, you have built a symposium.

Rough shape for a half day: 20% context and data, 60% discussion, 20% synthesis
and prioritisation.

**Write discussion prompts that surface disagreement.** "What are your thoughts
on X?" produces polite consensus. "Where would you not use this, and why?" and
"What would have to be true for you to change practice?" produce advice.

Ask advisors to state where they disagree with each other, explicitly. A record
of unanimous agreement from ten independent experts usually means the questions
were too easy.

**Pre-read** (`medical-slide-deck`): enough to make the discussion informed, not
so much that it leads. Send it early enough to be read.

## Stage 5 — Capture and act

The failure at the end is as common as the failure at the start: good advice,
recorded, and nothing changes.

Capture **what was said, by how many, and where they disagreed** — not a
smoothed summary. Disagreement between experts is data about uncertainty in the
field, and averaging it destroys the most useful output of the meeting.

Then, within the meeting: **which three things should change as a result?**
Named, owned, with a decision attached.

Tell advisors what happened. An advisory board whose participants never learn
whether their advice mattered will not get their genuine attention next time.

## Compliance

- **Fair market value** compensation, by role and time, documented
- **Transparency reporting** — honoraria and travel are disclosable and will be
  published against the advisor's name
- **A genuine need**, documented in the charter
- **Written output** that shows the advice influenced something
- **No promotional content**, no product training, no message testing
- Contracts in place before the meeting

If the meeting would be embarrassing to describe accurately to a regulator, the
problem is the meeting.

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus:

- Could the answer to our question genuinely surprise us?
- Is anyone on this panel likely to disagree with us?
- Does the agenda spend more time asking than telling?
- Would we run this meeting if the product were not ours?
- What will we do differently depending on the answer?

## Before you finish

Read `house-rules/advisory-board-design.md`. Approval routes, FMV rates,
attendee restrictions and contracting are entirely local and usually stricter
than the general position here.
