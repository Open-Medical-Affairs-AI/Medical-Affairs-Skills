---
name: scientific-communication-strategy
description: >-
  Decide what the publication and scientific communication strategy should
  be — which questions to answer, for which audiences, in what sequence —
  rather than listing papers by data availability. Use for building or
  challenging a publication plan, congress submission strategy, and
  questions like "what should we publish next year" or "what are we over-
  communicating". Works backwards from audience information needs and
  evidence gaps to communication priorities, distinguishes an evidence gap
  from a communication gap, and applies GPP 2022 and ICMJE authorship
  requirements throughout.
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
    - pubmed-search
    - citation-integrity
    - scientific-platform
    - deliverable-quality-review
  produces: Scientific communication strategy and prioritised publication plan
  network: [eutils.ncbi.nlm.nih.gov]
---

# Scientific Communication Strategy

Most publication plans are lists of papers sequenced by when data become
available. That is a production schedule, not a strategy.

A strategy starts from a different question: **what does the scientific
community need to know that it currently does not, and which of those gaps can
we credibly close?** Data availability then determines timing, not priority.

## The distinction the whole skill turns on

**An evidence gap** is a question nobody has answered. The fix is research.

**A communication gap** is a question that *has* been answered, in data we hold
or have published, and the answer has not reached the people who need it.

Conflating them is the most consequential error in this domain, and it runs in
both directions. Proposing a study to solve a communication problem wastes
years and millions. Proposing a publication to solve an evidence problem
produces a paper that cannot answer its own question, and reviewers say so.

For every priority you identify, state which it is. If it is an evidence gap,
route it to `evidence-gap-analysis` — it does not belong in a publication plan.

## Stage 1 — Inventory

- Existing publication plan, and what has actually published against it
- Our published evidence, and our unpublished data
- Competitor publication activity and volume
- The scientific narrative or platform
- Evidence gaps already identified
- Upcoming data readouts and their timing
- Audiences and what decisions each is making
- Congress calendar and abstract deadlines

## Stage 2 — Retrieve

**What have we published, and what have they?** (`pubmed-search`)

Run the same search structure on your product and each competitor. Volume is not
the interesting comparator; **coverage** is. Map both sets against the questions
clinicians actually ask. Where the competitor has published on a question you
have not, that is a communication gap regardless of who has better data.

**What is already answered in the literature, by anyone?** A question answered
by independent investigators may not need a company publication at all — and
saying so is a legitimate strategic conclusion that saves resource.

## Stage 3 — Analyse

### Work backwards from audience decisions

For each audience, what decision are they making, and what would they need to
know to make it well?

| Audience | Decision | What they need |
|---|---|---|
| Treating clinicians | Whether and when to use this, in whom | Efficacy in patients like theirs, practical toxicity management, sequencing |
| Guideline committees | Whether to recommend, and at what strength | Randomised evidence, GRADE-assessable, published well before the review window |
| Payers / HTA | Whether to fund | Comparative effectiveness, economic evidence, real-world outcomes |
| Investigators | Whether to research | Mechanism, unanswered questions, feasibility |
| Patients | Whether to accept | Plain language, benefit and risk, what treatment is like |

**Guideline timing deserves specific attention.** Committees work on multi-year
cycles and assess published evidence. A publication plan that treats guideline
inclusion as a near-term outcome has misunderstood the mechanism — the evidence
must exist, be published, and be assessable well before the review window opens.

### Map coverage against need

| Question audiences need answered | Evidence exists? | Published? | Communicated? | Gap type |
|---|---|---|---|---|

This grid is the analysis. Four patterns come out of it:

- **Evidence exists, published, communicated** — stop investing here. This is
  where over-communication lives.
- **Evidence exists, published, not reaching people** — a dissemination problem.
  Medical education, congress presence, plain-language summaries.
- **Evidence exists, not published** — the highest-value and most common
  finding. Data on file that answers a real question. Publish it.
- **No evidence** — an evidence gap. Not a publication.

### Ask what we are over-communicating

Rarely asked and usually revealing. Signs: the fifth paper on the same endpoint
in the same population; congress abstracts that are subgroup slices of a trial
already fully published; a narrative that keeps restating what is settled while
leaving contested questions unaddressed.

Over-communication is not merely wasteful. It reads as promotional, it crowds
out the questions that matter, and reviewers and KOLs notice.

### Ask what we are failing to answer

The uncomfortable question. Which question, if a clinician asked it, would we be
unable to answer well? Field insight (`field-insight-synthesis`) and medical
information enquiry patterns are the best evidence here — the questions people
actually ask reveal where the narrative is thin.

Being unable to answer is not a communications failure to be managed. It is
information about where the evidence needs to go.

### Sequence deliberately

Sequencing carries meaning. Primary results before subgroup analyses. Safety
alongside efficacy, not eighteen months later. Real-world evidence after the
trial evidence it contextualises. A plan that publishes favourable analyses
first and inconvenient ones last is visible as such, and is a
research-integrity problem, not a tactical choice.

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus:

- **Does every planned publication answer a question someone actually asked?**
  Or does it exist because the data exist?
- **Is any of this a study dressed as a paper** — an evidence gap misfiled?
- **Are we publishing negative or neutral results?** Non-publication of
  unfavourable findings is a research-integrity failure. If none are planned,
  ask whether there are any.
- **Does authorship meet ICMJE criteria** for every planned publication, and is
  writing support disclosed?
- **Is the sequencing defensible if someone reconstructs it later?**
- **What are we deliberately not publishing, and why?**

## Stage 5 — Deliver

Use `shared/templates/publication-plan.md`.

```
DRAFT — NOT FOR EXTERNAL USE. REQUIRES QUALIFIED MEDICAL REVIEW.

THE STRATEGIC POSITION   What the communication strategy is, in a paragraph.
                         The choice, not the list.
AUDIENCE NEEDS           By audience: the decision, and what would inform it
COVERAGE ANALYSIS        The grid. Where we are over- and under-communicating.
PRIORITIES               Ranked, with the reason each outranks the next
THE PLAN                 Publication/congress/education, sequenced, with owners
NOT DOING                What we are deliberately not communicating, and why
EVIDENCE GAPS FOUND      Routed to evidence generation — NOT publications
GOVERNANCE               Authorship approach, GPP 2022 compliance, disclosures
```

## Governance — not optional

**GPP 2022** and **ICMJE** apply to everything in the plan:

- All four ICMJE authorship criteria must be met by every named author
- No ghost authorship, no guest authorship
- Professional medical writing support is legitimate **and must be disclosed**,
  with the funder named
- Authors need genuine access to the data
- Results are published regardless of whether they are favourable
- Trials are registered before enrolment, and results reported

`scientific-manuscript` carries the detail for individual publications.

## Before you finish

Read `house-rules/scientific-communication-strategy.md`. Publication steering
committee structure, approval routes, and target journal tiers are all
organisation-specific.
