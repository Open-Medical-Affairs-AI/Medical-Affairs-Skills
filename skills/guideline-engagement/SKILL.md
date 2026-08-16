---
name: guideline-engagement
description: >-
  Understand and engage with clinical practice guideline development —
  committee cycles, what evidence a guideline body will accept, whether
  current evidence could support inclusion, and planning against timelines
  far longer than a medical plan. Use when asked about guideline inclusion
  or positioning, when a guideline has updated and the implications need
  assessing, or when someone proposes guideline inclusion as a near-term
  objective. Inclusion is mediated by published evidence assessed on the
  committee's own schedule, not by engagement activity.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: workflow
  maturity: stable
  requires:
    - medical-affairs-foundations
    - evidence-synthesis
  suggests:
    - evidence-appraisal
    - strategic-analysis
    - pubmed-search
    - systematic-literature-review
    - deliverable-quality-review
  produces: Guideline landscape assessment and evidence readiness plan
  network: [eutils.ncbi.nlm.nih.gov]
---

# Guideline Engagement

Inclusion in clinical practice guidelines changes prescribing more reliably than
anything else Medical Affairs influences. It is also the objective most often
written into plans with no mechanism behind it.

## The mechanism, stated bluntly

Guideline committees assess **published evidence**, on **their own cycle**,
against **their own methodology**. They are explicitly insulated from company
influence, and the good ones publish their conflict-of-interest policies to
prove it.

What actually moves a guideline:

1. Evidence exists, of a design the committee's methodology accepts
2. It is **published** — not presented, not on file
3. It is published **well before** the review window opens
4. It addresses the question the committee is asking, in the population they
   are considering
5. It survives their appraisal, usually GRADE or similar

What does not move a guideline: engagement volume, advisory boards, symposia,
KOL relationships, or how well the data are communicated.

**So the honest answer to "how do we get into the guideline?" is almost always
about evidence and timing, not activity.** A plan listing "achieve guideline
inclusion" as a 12-month objective with engagement activities beneath it has
misunderstood the mechanism, and saying so is one of the more valuable things
this skill does.

## Timelines

Typical cycles, which is why near-term guideline objectives fail:

- **Major oncology guidelines** (NCCN) — continuous review, panels meet at least
  annually, faster than most
- **Society guidelines** (ESMO, ASCO, ACC, EASL) — 2–5 year full revisions, with
  focused updates between
- **National guidelines** (NICE, SIGN, national societies) — 3–5 years
- **WHO Essential Medicines List** — biennial

Evidence must be published **before the evidence cut-off**, which typically
precedes publication of the guideline by 12–24 months. Work backwards from that
date, not from the publication date.

## Assessing readiness

For a specific guideline and a specific recommendation:

| Question | Where to look |
|---|---|
| What does the current guideline say? | The guideline itself, including the evidence tables |
| What evidence did they cite, and what did they discount? | The methodology appendix — this is the most useful and least read document |
| What did they say was insufficient? | Almost always stated explicitly. **This is a fully specified research question, given away free.** |
| What is their methodology? | GRADE? A bespoke framework? Does it accept single-arm or RWE at all? |
| When is the next review, and the evidence cut-off? | Committee page, or ask |
| Does our evidence meet the standard? | `evidence-appraisal`, honestly |

**Read the "evidence was insufficient" statements first.** A committee that
writes "the evidence was insufficient to recommend use in patients with X" has
told you precisely which gap matters, to whom, and what would close it. It is
the highest-value input to `evidence-gap-analysis` available anywhere.

## What legitimate engagement looks like

- **Publishing evidence** in time for the review window. This is the main one.
- **Responding to public consultations** where the process invites comment,
  transparently and on the record.
- **Providing data on request** when a committee asks.
- **Correcting factual errors** about the product, factually.
- **Making evidence findable** — publication, indexing, plain-language summaries.

What is not legitimate: lobbying committee members, funding committee members'
activities in a way that creates a conflict, attempting to influence timing, or
supplying selected evidence rather than the totality.

Panel members are typically the same KOLs Medical Affairs engages with
scientifically. That is normal and unavoidable. The boundary is that the
engagement is scientific exchange, not advocacy for a guideline position — and
their COI declarations will record your interactions.

## When a guideline updates

Assess within days:

- **What changed**, specifically, and in which recommendation
- **What evidence drove it** — and whether it was ours
- **Does it change practice**, or codify what was happening already?
- **Does it position us differently**, favourably or otherwise?
- **What questions will the field now be asked** that they cannot answer?
- **If it went against us, why?** Read the rationale. It is usually an evidence
  statement, and it is usually specific.

Route the evidence implications to `evidence-gap-analysis` and the
communication implications to `scientific-communication-strategy`.

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus:

- Is any proposed activity actually capable of influencing a guideline?
- Does the timeline work backwards from the **evidence cut-off**?
- Have we read what the committee said was insufficient?
- If our evidence does not meet their standard, are we saying so plainly?

## Before you finish

Read `house-rules/guideline-engagement.md`. Rules on interacting with guideline
bodies and panel members are strict and local.
