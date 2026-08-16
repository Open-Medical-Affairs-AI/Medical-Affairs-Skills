---
name: safety-communication
description: >-
  Communicate safety information to healthcare professionals and internal
  audiences — new safety findings, label safety changes, emerging signals,
  responses to safety questions, and the decision about whether and how to
  communicate at all. Use when a safety signal needs communicating, a label
  safety section has changed, a Dear Healthcare Professional letter is being
  considered, or a KOL has raised a safety concern. Handles the boundaries
  that make safety communication defensible: no minimisation, no reassurance
  beyond the evidence, and absolute clarity that this discharges no
  pharmacovigilance obligation.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: workflow
  maturity: stable
  requires:
    - medical-affairs-foundations
    - regulatory-label-intelligence
  suggests:
    - evidence-appraisal
    - citation-integrity
    - medical-correspondence
    - deliverable-quality-review
  produces: Safety communication plan and content
  network: [api.fda.gov, eutils.ncbi.nlm.nih.gov]
---

# Safety Communication

Safety communication is where the temptation to soften is strongest and the
consequence of softening is highest.

Three lines govern everything here.

**This is not pharmacovigilance.** PV owns signal detection, evaluation,
causality assessment and regulatory reporting. This skill covers communicating
what PV has established. It discharges no reporting obligation of any kind.

**No minimisation.** Not in the framing, the ordering, the adjectives or the
omissions. A safety communication that reads as reassuring when the evidence is
not reassuring is worse than no communication, because it is believed.

**No reassurance beyond the evidence.** "No causal relationship has been
established" is often true and is routinely read as "it doesn't cause it". If
that is not what you mean, say what you do mean.

## Deciding whether to communicate

Not every finding warrants proactive communication, and over-communication
desensitises the audience to the ones that matter.

Communicate proactively when: the label has changed; a new risk requires a
change in monitoring or management; a risk is being under-recognised in
practice; a regulator requires it; or the field is being asked and cannot
answer.

Do not communicate proactively on: a disproportionality signal in spontaneous
reports with no causal assessment; a single case report; or a competitor's
safety issue — that last one is not scientific exchange whatever the framing,
and it will be seen for what it is.

**When a decision is genuinely borderline, the tiebreaker is the clinician's
information need, not the commercial consequence.** Record that reasoning.

## Getting the evidence right

`evidence-appraisal` applies with unusual force here, because safety evidence is
the most commonly misused kind.

- **Spontaneous reports have no denominator.** FAERS counts are counts of
  reports. They cannot produce incidence, cannot establish causality, and cannot
  be compared between products (`regulatory-label-intelligence`).
- **Trial rates have denominators** — cite these for frequency.
- **State follow-up duration.** A rate from short follow-up understates
  cumulative toxicity, and this is the most common way safety data misleads
  without anyone intending it.
- **Distinguish serious from severe.** Different concepts, routinely conflated,
  and the difference changes the regulatory meaning.
- **Absence of a signal in an underpowered study is not safety.**

## Content that must appear

- **What the finding is**, plainly, in the first two sentences
- **The evidence**, with its design and denominator
- **What is not known** — usually more than what is
- **What the recipient should do**: monitoring, management, patient selection.
  Specific, not "exercise clinical judgement"
- **Adverse event reporting instructions**, with the actual local route
- **Where to get more information**, with a named contact

## Register

Direct and unhedged. Short sentences.

Do not open with thanks, partnership language or background. A safety letter
that spends its first paragraph on pleasantries reads as evasive, and recipients
notice.

Do not lead with what is reassuring. If both a concern and a reassurance are
true, the concern goes first — leading with the reassurance is minimisation by
ordering, and it is the most common form.

## Briefing the field

The field will be asked about a safety topic long before any formal
communication. They need:

- The evidence, with its limitations
- What they may and may not say
- The routing for questions beyond it
- **Explicit permission to say "we don't know"** — without it they improvise
- A reminder that any AE mentioned in an interaction is reportable, with the
  route

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus:

- **Read it as a clinician whose patient has had this event.** Does it feel
  honest?
- Is anything minimised by ordering, adjective or omission?
- Does any reassurance exceed the evidence?
- Are the actions specific enough to follow?
- Is the AE reporting route the actual local one?
- Would we be comfortable with a regulator reading this alongside the full
  safety data?

## Before you finish

Read `house-rules/safety-communication.md`.

Safety communications have a review pathway that includes pharmacovigilance,
regulatory and usually the regulator itself. **Nothing here substitutes for it.**
Never issue a safety communication on the strength of this skill alone.
