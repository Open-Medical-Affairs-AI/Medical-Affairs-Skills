---
name: launch-medical-readiness
description: >-
  Assess whether Medical Affairs is actually ready for a launch, label expansion
  or major data readout — and say plainly where it is not. Use when preparing for
  a launch, running a readiness review or gate, planning the medical activities
  ahead of an approval, or when someone asks whether the team is ready. This is
  a gate with a verdict, not a plan: it tests evidence readiness, field
  capability, medical information coverage, publication timing, and the questions
  the field will be asked in the first six months that nobody can currently
  answer. For the plan itself, use medical-strategy-plan.
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
    - medical-strategy-plan
    - deliverable-quality-review
  produces: Launch readiness assessment with a verdict
---

# Launch Medical Readiness

A readiness review is a gate, not a plan. It has a verdict, and the verdict is
sometimes "no".

The failure mode is a review that produces a status deck where everything is
amber and nothing is decided. If nothing could come back red, it was not an
assessment.

## The window that determines everything

**What clinicians misunderstand in the first six months tends to persist.**
Early impressions are formed on incomplete information, spread through informal
networks, and are much harder to shift later than to set correctly at the start.

That makes launch readiness disproportionately about one thing: **can the field
answer the questions they will actually be asked, in the first six months?**

## The six-month question list

The single most valuable output of this skill. Build it before anything else.

Sources: field insight from similar products (`field-insight-synthesis`),
medical information enquiry patterns from the class, the questions the pivotal
trial's design invites, the questions the label's wording invites, and the
evidence gaps you already know about (`evidence-gap-analysis`).

For each question, classify honestly:

| Status | Meaning |
|---|---|
| **Answered** | Published evidence exists, the field has it, and they can find it |
| **Answerable** | Evidence exists but is unpublished, or published and not in field hands |
| **Unanswerable** | No evidence. The honest answer is "we don't know." |

**The "answerable" list is the actionable one** — it is a communication and
training problem with weeks of lead time, not years.

**The "unanswerable" list must be trained explicitly.** A field team that has
not rehearsed saying "we don't have that data, and here is what we do have" will
improvise, and improvisation near a label boundary is where compliance problems
begin.

## The readiness dimensions

Assess each with a verdict, not a percentage.

**Evidence.** Is the pivotal evidence published, or only presented? Are the
analyses the field will need available? Is anything embargoed past launch?

**Scientific platform.** Does it exist, is it substantiated, and is it current
(`scientific-platform`)?

**Field capability.** Trained on the data *and* on its limitations. The
limitation training is what gets cut for time and what matters at the boundary.
Can they handle an unsolicited off-label question correctly? Have they
practised, not just been told?

**Medical information.** Standard response documents for the anticipated
questions, including the uncomfortable ones. Enquiry routing live. Capacity for
the launch spike, which is real and consistently underestimated.

**Publications.** Is the primary publication out, or will the field be
discussing data that has no citable source? Presenting at congress and
publishing months later leaves a gap where the field cannot cite the evidence
they are discussing.

**Safety.** PV processes live, AE reporting routes known to everyone, field
trained on detection and escalation.

**Evidence generation.** Are the studies that address the six-month unanswerable
questions started? If they start at launch, they read out too late to matter.

## The verdict

For each dimension: **ready** · **ready with named gaps** · **not ready**.

Then one overall verdict, and — the part that is usually missing — **what would
have to happen to change it, by when, owned by whom.**

State the consequence of launching not ready in the specific dimension. "Field
cannot answer the sequencing question" is a status; "field will be asked the
sequencing question in most interactions, cannot answer it, and will either
improvise near the label boundary or lose credibility" is an assessment.

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus:

- Is anything red? If everything is amber, this is not an assessment.
- Would we say "not ready" if that were true — and does the process allow it?
- Is the six-month question list built from evidence, or from what we would
  like to be asked?
- Has the field practised the "we don't know" answer, or only been told about it?
- What is the cost of launching not ready in each dimension, specifically?

## Before you finish

Read `house-rules/launch-medical-readiness.md`. Gate criteria, governance and
escalation routes are local, and the escalation route matters most — a readiness
assessment nobody can act on is theatre.
