---
name: medical-launch-plan
description: >-
  Build the entire Medical Affairs launch plan for an upcoming asset, new
  indication or label expansion by running a coordinated team of digital
  workers — one per launch workstream, each given its own context — under a
  Launch Lead, with humans deciding at every gate. Use when asked to "build the
  launch plan", "plan the medical launch for X", "what does medical need to do
  before approval", or to stand up an agent swarm for a launch. This builds the
  plan; `launch-medical-readiness` judges whether the plan has made us ready.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: workflow
  maturity: beta
  requires:
    - medical-affairs-foundations
    - strategic-analysis
  suggests:
    - launch-timeline-and-governance
    - launch-field-training
    - launch-medical-readiness
    - medical-strategy-plan
    - scientific-platform
    - integrated-evidence-plan
    - scientific-communication-strategy
    - field-medical-planning
    - medical-information-response
    - deliverable-quality-review
  produces: Integrated medical launch plan with workstream plans, critical path, owners and human decision gates
  deliverables: [docx, pdf, pptx]
---

# Medical Launch Plan

A launch plan is the medical strategy, the evidence, the narrative, the field,
medical information, safety, education, payers and patients — all landing on
the same date, all depending on the same label wording. Most launch plans are
fourteen workstream decks stapled together. Nobody owns the joins, and the joins
are where launches fail: the SRDs written before the platform settled, the
training built on a draft label, the pivotal paper still in review when the
field starts presenting the data.

This skill exists to own the joins. It runs the plan as an **organisation of
digital workers**: a Launch Lead that holds the whole picture, specialists that
each do one workstream properly with the existing skills, and an independent
auditor that tries to break the result. People decide. Workers draft.

## The org chart

Read [references/digital-workers.md](references/digital-workers.md) before
dispatching anyone. It holds each worker's brief: the skills it runs, the exact
context it receives, what it must hand back, and what it may not do.

```
                      LAUNCH MEDICAL DIRECTOR (human — final judge)
                                       │
                         LAUNCH LEAD (coordinator — this skill)
                                       │
  ┌──────────────┬────────────────┬────┴─────────────┬───────────────┬────────────────┐
STRATEGY &      NARRATIVE &       EXTERNAL           ANSWER &        MEASURE &
EVIDENCE        COMMUNICATION     ENGAGEMENT         PROTECT         GOVERN
Strategy        Narrative         Field Medical      Medical Info    Launch PMO
Evidence        Pubs & Congress   Field Training     Safety Liaison  Metrics Analyst
Value & Access  Guideline Scout   Expert Input       Content & MLR
                                  Education
                                  Patient Partnership
                                       │
                    READINESS AUDITOR (independent — reports to the human, not the Lead)
```

Not every launch needs every worker. A label expansion in an established
population may need no new territory design; a first-in-class launch needs all
of them. **Staff the chart from the inventory, and say which workers you did not
start and why.** An idle worker producing a plausible plan is worse than none.

## Context engineering — the part that makes the swarm work

A sub-agent knows only what it is handed. Two failures dominate: giving every
worker everything (each drowns, and all of them drift toward the same generic
plan), and giving each worker a different version of the facts (the platform
says one thing, the SRDs another).

So the Launch Lead builds two things before anyone starts:

1. **The launch facts sheet** — one page, the single source of truth every
   worker receives: asset, mechanism, proposed indication wording, target
   decision date *labelled as an assumption*, pivotal evidence with design,
   approved lexicon, markets in scope, resource envelope, and what is unknown.
   When a fact changes, it changes here and the dependent outputs are marked stale.
2. **A context packet per worker** — objective, the facts sheet, only its slice
   of the inputs, the upstream outputs it depends on, its house rules, its
   output contract, and its boundaries.

**The six-month question list is the spine.** Build it first (method in
`launch-medical-readiness`). Every worker receives it, because almost every
workstream exists to answer, publish, train, or rehearse one of those questions.

## Stage 0 — Orient

Load `medical-affairs-foundations` and `strategic-analysis`; read this skill's
house rules. State the job: asset, launch event, markets, horizon. Announce the
plan: which workers, which waves, which human gates.

## Stage 1 — Inventory

- Product profile, current or proposed label wording, pivotal publications
- Current medical plan, IEP, publication plan, scientific platform draft
- Field insights, MI enquiry history, advisory board output for the class
- Competitive landscape and readouts inside the launch window
- Payer/HTA timelines, guideline cycles, congress calendar
- Readiness register or status reports, if one exists
- Resource envelope — headcount, budget, agency capacity, what is fixed
- Governance — who signs off what, and the escalation route

Run the foundations safety scan on any human-sourced records **before**
dispatching workers, and surface findings first.

**Name what is missing.** The commonest gap is the indication wording itself.
A plan built on assumed wording must say so on every page that depends on it.

## Stage 2 — Dispatch in waves

Parallel where independent; sequenced where one output is another's input.

| Wave | Workers | Why this order |
|---|---|---|
| 0 | Launch Lead | Facts sheet, six-month question list, worker roster |
| 1 | Strategy · Evidence · Narrative · Value & Access · Guideline Scout | These set the objectives, the evidence position and the words everyone else uses |
| **Gate 1** | **Human: strategy, platform and evidence position** | Nothing downstream should be built on an unapproved narrative |
| 2 | Pubs & Congress · Field Medical · Field Training · Expert Input · Education · Patient Partnership · Medical Info · Safety Liaison · Content & MLR | Each consumes the approved platform and the question list |
| 3 | Launch PMO · Metrics Analyst | Integrate dates, dependencies, owners and measures across everything above |
| 4 | Readiness Auditor | Independent challenge and a verdict |
| **Gate 2** | **Human: integrated plan and readiness verdict** | Accept, send back, or accept with named gaps |

Report at each wave boundary in two or three lines: what came back, what
conflicts, what needs a person.

## Stage 3 — Integrate (the Launch Lead's real job)

Workers return their output contract; the Lead does not rewrite their work. It
checks the joins:

- **Label dependency.** Which outputs depend on indication wording, and what
  each does if the wording changes. This is usually most of them.
- **Narrative consistency.** Platform statements, SRDs, training, education
  objectives and publication messages use the same claims at the same strength.
  A claim stronger in the training than in the platform is a finding.
- **Citable before discussed.** For every data point the field will present,
  is there a citable source by the date they present it?
- **Question coverage.** Every six-month question has a named workstream that
  answers it, publishes it, trains it — or trains "we don't know".
- **Capacity.** The same human owner across nine critical-path tasks is not a
  plan. Count it.
- **Conflicts.** When two workers disagree, do not average or pick the
  convenient one. Record both positions and make it a decision for a named person.

## Stage 4 — Challenge

The Readiness Auditor runs `launch-medical-readiness` and
`deliverable-quality-review` against the integrated plan. It receives the
worker outputs and the inputs, **not** the Lead's summary — independence is the
point. It reports to the human, not to the Lead.

Plus the Lead's own checks:

- Is any workstream green only because its dependency was averaged away?
- Does any activity exist because it existed last launch? Ask what happens if
  it does not occur.
- Could the verdict come back "not ready"? If the plan cannot fail the gate, the
  gate is decoration.
- Is anything promotional in medical clothing — objectives that are really
  uptake targets? Those leave the medical plan.

## Stage 5 — Deliver

```
DRAFT — NOT FOR EXTERNAL USE. REQUIRES QUALIFIED MEDICAL REVIEW.

LAUNCH ON A PAGE        Objectives, the verdict, the three decisions needed now
LAUNCH FACTS SHEET      Including every assumption, labelled
THE ORG CHART           Workers started, not started (and why), human owners
SIX-MONTH QUESTIONS     Answered / answerable / unanswerable, each with a route
WORKSTREAM PLANS        One section per worker, traced to an objective
CRITICAL PATH           From launch-timeline-and-governance
DECISION GATES          Who decides, criteria written in advance, what blocks
CONFLICTS & DECISIONS   Both positions, decision owner, date needed
READINESS VERDICT       From the auditor, unedited by the Lead
GAP REGISTER            Every gap with an owner and a date
PROVENANCE              Sources, assumptions, what each output depends on
```

Keep `run.json` current with each worker's output path and source IDs so a
change to the label or the date propagates to exactly the affected sections.

## Human decision gates — not negotiable

The swarm drafts; people decide. Agents do not approve platforms, certify
material, submit to MLR, register studies, contact experts, change CRM records
or send anything. Every gap carries a **named human owner and a date** — a gap
assigned to "Medical" or to a worker has no owner. The final verdict can be
"not ready", and the plan must make that answer possible to give.

<!-- ma-render:begin — generated by scripts/sync_renderer.py; edit the template there -->
## Deliverable format

Deliver a designed **Word document (.docx) plus a PDF copy**, and a **PowerPoint deck (.pptx)** when the audience will be presented to.
Build it with this skill's bundled engine. Markdown is for drafting only —
never hand over a .md file, and never hand-write a python-pptx or
python-docx script instead of the engine.

```bash
python3 scripts/ma_render.py bootstrap      # installs python-pptx, python-docx, matplotlib, reportlab
python3 scripts/ma_render.py example report > spec.json   # spec format; or write a markdown draft
python3 scripts/ma_render.py report spec.json --out outputs/<name>.docx --preview outputs/preview
python3 scripts/ma_render.py deck deck.json --out outputs/<name>.pptx --preview outputs/preview
```

Turn numbers into `stats`/`chart` blocks and comparisons into tables or
`two_column` slides; put a source on every data element. Then open
`outputs/preview/contact-sheet.png`, fix every overflow, empty or text-only
page, and re-render. If a package cannot be installed the engine still
writes a real .docx or print-ready HTML and says what degraded.
<!-- ma-render:end -->

## Before you finish

Read `house-rules/medical-launch-plan.md`. Launch governance, gate names,
sign-off authority and which workstreams Medical Affairs owns versus supports
are local. A plan that assigns medical ownership to a workstream your
organisation runs from Market Access will be rejected on sight.
