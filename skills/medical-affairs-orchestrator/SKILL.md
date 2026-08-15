---
name: medical-affairs-orchestrator
description: >-
  Route any Medical Affairs request to the right workflow and run it end to end.
  Load this FIRST whenever someone gives you a Medical Affairs job rather than a
  named skill — "prepare me for this KOL meeting", "what do these field notes
  mean", "tell leadership what changed at the congress", "what should we publish
  next year", "build our medical plan", "what evidence are we missing", "answer
  this clinical enquiry", or any multi-part objective such as preparing for an
  advisory board. It works out which workflow the job maps to, loads the
  foundation skills and the workflow's dependencies, and enforces the six-stage
  execution contract so the agent inventories what is missing and challenges its
  own conclusions before delivering anything. Also handles long-horizon
  objectives that need several workflows chained together. Use it when the
  request names a Medical Affairs outcome rather than a skill, when you are
  unsure which skill applies, or when the objective clearly needs more than one.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: orchestrator
  maturity: stable
  requires: [medical-affairs-foundations]
  produces: A routed, executed Medical Affairs workflow
---

# Medical Affairs Orchestrator

You have been given a job, not a skill name. Your task is to work out what job
it is, load what you need, and execute it properly.

Do not ask the user which skill to use. They should never have to know.

## Stage 0 — Orient

**Always load these four first.** They carry the boundaries that make Medical
Affairs output usable, and every workflow assumes them:

- `medical-affairs-foundations` — compliance, safety escalation, the intake gate
- `evidence-appraisal` — what each design can support
- `citation-integrity` — never emit an unresolved citation
- `deliverable-quality-review` — the challenge pass, run before delivery

Then route.

## Routing

Match on what the person wants to *end up with*, not on the words they used.

| The job sounds like | Load |
|---|---|
| Prepare for a meeting with a named expert; KOL profile; "brief me before this call" | `kol-engagement-brief` |
| Make sense of field notes, MSL records, interaction logs; "what is the field telling us" | `field-insight-synthesis` |
| What happened at a congress; post-meeting readout; competitor data assessment | `congress-intelligence` |
| What should we publish; publication plan; scientific platform; "what are we over-communicating" | `scientific-communication-strategy` |
| Annual plan; scientific priorities; landscape assessment; "review this medical plan" | `medical-strategy-plan` |
| What don't we know; what should we study; research prioritisation; budget allocation | `evidence-gap-analysis` |
| Answer this clinical question; standard response document; FAQ development | `medical-information-response` |
| Find the literature on X; what has been published | `pubmed-search` |
| What trials are running; competitor pipeline | `clinical-trials-search` |
| What is it approved for; label wording; safety profile | `regulatory-label-intelligence` |
| Everything on X, defensibly complete; HTA or guideline submission | `systematic-literature-review` |
| Code these observations; normalise this terminology | `medical-terminology-mapping` |
| Make slides, a deck, a presentation | `medical-slide-deck` |
| Write a paper, manuscript, or reviewer response | `scientific-manuscript` |
| Congress abstract or poster | `congress-abstract-and-poster` |
| Lay summary, patient-facing material | `plain-language-summary` |
| Check this before review; is this promotional | `mlr-review-readiness` |
| A chart, KM curve, forest plot, AE figure | `data-visualization-for-medical` |

Load the workflow skill, then whatever it declares in `metadata.requires`.
`SKILLS-INDEX.md` lists every skill with its dependencies.

**When the job maps to more than one workflow**, that is normal — see the
long-horizon section below. **When it maps to none**, say so plainly, and do
the work using the foundation skills rather than forcing a poor fit.

**When the request is ambiguous in a way that changes the deliverable** — "help
with the congress" could be preparation or readout — ask one question. One.
Do not interview the user.

## The six-stage execution contract

Every workflow runs these, and **announces them** as it goes. This is what makes
it read as an agent doing a job rather than a model answering a prompt.

```
0 · ORIENT     Identify the job. Load foundations, the workflow, its
               dependencies, and house-rules/<skill>.md.

1 · INVENTORY  List what you were given. Then name what is MISSING and how it
               limits the answer. Do not fill gaps with plausible guesses.

2 · RETRIEVE   Fill evidence gaps from PubMed, ClinicalTrials.gov, openFDA.
               Record every query verbatim with its date.

3 · ANALYSE    Run the workflow's reasoning ladder.

4 · CHALLENGE  Red-team your own conclusions with deliverable-quality-review,
               BEFORE showing anything.

5 · DELIVER    The artefact, plus a provenance appendix: queries run, sources
               cited, gaps left open.
```

**Stages 1 and 4 are the ones a generic agent skips**, and they are what
separate this from summarisation. An agent that reports what is missing before
it answers, and that argues against itself before delivering, is doing the job
an experienced colleague does.

Announce the plan at the start, briefly:

> I'll treat this as a field insight synthesis. Five stages: inventory the
> records and say what's missing, scan everything for safety findings, build the
> insights, challenge them, then deliver with provenance. Starting with the
> inventory.

Then do it. Do not narrate every step; report at the stage boundaries.

## The safety scan is not optional

Any job touching field notes, KOL interactions, medical information enquiries,
advisory board records, or congress conversations gets an adverse event,
product-complaint and special-situation scan **before analysis**, per
`medical-affairs-foundations`. Surface findings at the top of the output with
verbatim quotes. If you scanned and found nothing, say so.

This runs even when the request is framed as strategic. Especially then — that
is when it gets skipped.

## House rules

Before producing anything, read `house-rules/<skill-name>.md` for every skill
you loaded. Rules there are the adopting organisation's, and they **override**
the defaults. This is how a team adapts the library without forking it.

If a house-rules file contains only the seeded examples, the organisation has
not customised it yet — use the defaults, and it is worth mentioning once that
the file exists.

## Long-horizon objectives

Some jobs need several workflows chained. Example:

> "We have an advisory board in three weeks. Work out the five most important
> scientific questions to explore and prepare the briefing materials."

Do not attempt this in one pass. Decompose, state the plan, execute in
sequence, and let each stage feed the next:

```
1. evidence-gap-analysis      → what we genuinely do not know
2. field-insight-synthesis    → what the field is asking that we cannot answer
3. congress-intelligence      → what changed recently that bears on it
   ─────────────────────────────────────────────────────────────────
4. strategic-analysis         → rank to the five questions worth an advisory board
5. medical-slide-deck         → the pre-read, weighted toward questions
6. kol-engagement-brief       → one per advisor
7. mlr-review-readiness       → before anything leaves the building
```

State the decomposition before starting, and report at each boundary so the
person can redirect early rather than after everything is built.

**Where a stage produces nothing useful, say so and continue.** "The gap
analysis found no unanswered question that would justify an advisory board on
this topic" is a legitimate and valuable finding — and is exactly the kind of
conclusion an agent optimising for apparent productivity will avoid.

## What good execution looks like

- Announces the job it thinks it has been given, before starting
- Names what is missing rather than guessing
- Runs real searches and records them
- States design alongside every result
- Surfaces safety findings first
- Argues against its own conclusion before delivering
- Ends with a provenance appendix and named open questions
- Keeps the draft marking on

## What to avoid

- Producing a deliverable before the analysis is finished. A well-formatted
  document with nothing behind it is the most common failure here, and the
  formatting is what makes the emptiness hard to see.
- Asking the user which skill to use.
- Interviewing the user instead of starting work.
- Filling a gap with a plausible-sounding fact.
- Skipping stage 4 because the output looks finished. Looking finished is the
  property that makes unreviewed output dangerous.
