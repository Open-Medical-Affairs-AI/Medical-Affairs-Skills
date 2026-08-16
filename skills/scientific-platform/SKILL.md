---
name: scientific-platform
description: >-
  Build or challenge the scientific platform — the core evidence-based
  narrative, the scientific statements it supports, the lexicon, and the
  communication objectives everything else derives from. Use when developing
  or revising a scientific platform, medical narrative, communication
  objectives or disease-state narrative, and when asked what the scientific
  story is or whether the narrative still holds. Every statement traces to
  evidence with its certainty stated; unsubstantiated statements are marked
  as gaps rather than aspirations. This is the WHAT of the narrative; for
  what to publish and when, use scientific-communication-strategy.
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
    - citation-integrity
    - scientific-communication-strategy
    - deliverable-quality-review
  produces: Scientific platform with substantiated statements
---

# Scientific Platform

The platform is the foundational artefact. Every deck, brief, response and
publication derives from it, which means an unsubstantiated statement in the
platform propagates into everything.

It is also the artefact most likely to have been written backwards — starting
from the desired position and finding evidence to fit.

## What a platform is

Four layers, each traceable to the one below:

```
COMMUNICATION OBJECTIVES   what we want the scientific community to understand
        ↑
SCIENTIFIC STATEMENTS      what we can say, each with its evidence and certainty
        ↑
EVIDENCE                   what exists, appraised
        ↑
DISEASE AND UNMET NEED     what is true about the disease
```

**Build upwards.** A platform built downwards from the objectives is a marketing
narrative that will not survive contact with a sceptical clinician.

## The statement table

The core of the platform. Every scientific statement, with what supports it.

| # | Statement | Evidence | Design | Certainty | Substantiated? | Where it may be used |
|---|---|---|---|---|---|---|

**"Substantiated?" is the column that does the work.** Three honest values:

- **Yes** — the evidence supports the statement as written
- **Partially** — supported in a narrower population, or at lower certainty than
  the wording implies. Rewrite the statement to match the evidence.
- **No** — this is a **gap**, not a statement. Move it out.

The discipline that keeps a platform useful: **a statement we want to make and
cannot substantiate is an evidence gap.** Route it to `evidence-gap-analysis`.
Leaving it in the platform as an aspiration guarantees somebody eventually says
it out loud.

## Writing statements that survive

- **Match the wording to the design.** "In a single-arm study, an overall
  response rate of 62.5% (95% CI 54.8–69.8) was observed in patients with ≥4
  prior lines" is a statement. "Delivers deep responses in heavily pretreated
  patients" is a claim.
- **State the population.** A statement without one will be applied to
  populations it does not cover.
- **Name the endpoint and its type.** Surrogates labelled as surrogates.
- **No comparatives without head-to-head evidence.** This is where platforms
  most often cross the line, because the competitive framing feels natural in a
  strategy document.
- **Include what we cannot say.** A platform section headed "statements we
  cannot make and why" is unusual, and it is what stops the field improvising.

## The lexicon

The words the platform uses, and the words it does not.

Precision matters more than it seems: "response" and "remission" are not
synonyms; "tolerability" and "safety" describe different things; "real-world
evidence" and "real-world data" are routinely confused. Fix the vocabulary
centrally or every downstream document invents its own.

Include a banned-terms list with reasons — the promotional adjectives, the
absolute safety language, the comparatives.

## Challenging an existing platform

This is the more common request, and the more valuable one:

1. **Take each statement to its evidence.** Does the source say this, in this
   population, at this certainty? Read the sources, do not trust the citation.
2. **Find the comparatives.** Every one needs head-to-head data.
3. **Check the design match.** Causal wording on single-arm evidence is the
   commonest defect.
4. **Look for what is missing.** Which question would a sceptical clinician ask
   that the platform does not address? That silence is usually deliberate and
   usually the most interesting finding.
5. **Check it is current.** Platforms age badly — new evidence, competitor data,
   guideline changes. A statement true in 2024 may be indefensible now.
6. **Test the top statement against a hostile reading.** If a competitor's
   medical team read this, what would they attack first?

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus:

- Was this built upwards from evidence, or backwards from objectives?
- Is every statement substantiated, or are some aspirations?
- Would each statement survive being read aloud to a sceptical KOL?
- Does the platform say what we cannot say?

## Before you finish

Read `house-rules/scientific-platform.md`. Platform structure, approval routes
and the relationship to the commercial brand narrative are all local — and the
boundary between them is one your compliance function will have a firm view on.
