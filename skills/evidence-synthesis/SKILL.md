---
name: evidence-synthesis
description: >-
  Turn a body of clinical evidence into a defensible narrative that states
  what the totality supports, what it does not, and where it disagrees with
  itself. Use when you have multiple studies, trials or analyses and need a
  coherent scientific position rather than a study-by-study list —
  scientific platforms, medical narratives, congress readouts, evidence
  sections of strategy documents, and answering "what does the evidence
  actually say about X". Handles weight of evidence, reconciling conflicting
  trials, and stating certainty honestly.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: primitive
  maturity: stable
  requires:
    - medical-affairs-foundations
    - evidence-appraisal
  suggests:
    - citation-integrity
  produces: Evidence narrative with stated certainty and open questions
---

# Evidence Synthesis

Synthesis is not summarisation. A summary tells you what each paper said. A
synthesis tells you what is true, how confident we can be, and where the
evidence disagrees with itself.

The structural giveaway: if your output is organised by study — *Trial A showed…
Trial B showed… Trial C showed…* — you have summarised. A synthesis is organised
by **question**, with studies appearing as evidence bearing on each question.

## The three-bucket discipline

Every claim in a synthesis falls into one of three buckets, and the reader must
be able to tell which.

**Established.** Multiple consistent lines of evidence, adequate design, no
serious unexplained contradiction. State it plainly.

**Plausible but unconfirmed.** Directionally supported, but limited by design,
sample, consistency, or indirectness. Use conditional language, and say what
would confirm it.

**Unknown.** No adequate evidence. Say so explicitly rather than omitting the
question — an unanswered question that is not named reads as a question nobody
thought to ask.

The most common synthesis failure is collapsing all three into a single
confident register. Everything reads as equally settled, and the reader has no
way to tell which claims will survive a challenge.

## Method

### 1. Frame the questions first

Before reading, write the questions the synthesis must answer. They come from
the decision it feeds — a scientific platform needs different questions than a
congress readout.

Typical frames: what is the efficacy in the relevant population; how does it
compare with current standard of care; what is the safety and tolerability
profile in practice; who benefits most and least; what happens over the long
term; what remains unknown.

Organising by question is what makes the difference between synthesis and
summary, and it has to happen before you read or you will inherit the papers'
own structure.

### 2. Build the evidence map

For each question, tabulate what bears on it:

| Question | Study | Design | N | Population | Endpoint | Result (95% CI) | Certainty | Bears on the question how? |
|---|---|---|---|---|---|---|---|---|

Two things this exposes immediately: questions with no evidence at all, and
questions where all the evidence comes from one trial. Both are findings.

Appraise as you go (`evidence-appraisal`). A synthesis built on unappraised
inputs propagates every weakness in them, with added confidence from the
aggregation.

### 3. Weigh, do not count

Three studies agreeing does not outweigh one well-designed study disagreeing,
if the three share a common flaw. Weight by:

- **Design** — randomised beats observational for causal questions
- **Directness** — does it address *this* population, comparator, and outcome?
- **Precision** — event counts and interval width
- **Risk of bias** — assessed with a named tool
- **Independence** — three analyses of the same dataset are one piece of
  evidence, not three. This is easy to miss and common in real-world evidence,
  where several publications frequently share a database and a cohort.
- **Consistency** — do effects agree in direction and magnitude?

### 4. Confront contradictions

When studies disagree, resolving the disagreement is usually the most valuable
part of the whole synthesis. Work through the candidate explanations in order:

1. **Different populations.** Line of therapy, biomarker status, disease
   severity, prior treatment, age and comorbidity.
2. **Different comparators.** A trial against an outdated standard produces a
   larger effect than one against current practice.
3. **Different endpoints or definitions.** PFS assessed on different schedules;
   response criteria revised between trial eras.
4. **Different follow-up.** Immature data moves.
5. **Chance.** With enough studies, some will disagree. Check whether the
   confidence intervals overlap before reaching for a mechanism — apparently
   contradictory results frequently are not.
6. **Bias.** Only after the above have been considered.

Then state the resolution honestly, including "we do not know why these
disagree" when that is the answer. An unexplained contradiction that is named is
a research question. One that is averaged away is a trap for whoever relies on
the synthesis.

### 5. State certainty per claim

Apply GRADE-style language (see `evidence-appraisal/references/grade.md`) claim
by claim, not document by document. A single synthesis routinely contains
high-certainty and very-low-certainty claims, and the reader needs to know which
is which.

> **Efficacy in triple-class-exposed disease.** Response rates in the 60–65%
> range are consistently reported across three single-arm trials in similar
> populations (n=165, 117, 143). *Moderate certainty for the response rate
> itself; very low certainty for any comparative claim,* as no randomised
> comparison against current standard of care exists in this setting.

### 6. Name the gaps as gaps

Close with what the evidence does not establish. This section is what makes a
synthesis useful to evidence generation and to strategy — and it is the section
most often cut for length, which is exactly backwards.

Distinguish:
- **Not yet studied** — nobody has looked
- **Studied inadequately** — underpowered, indirect, or high risk of bias
- **Studied with conflicting results** — looked at and unresolved
- **Unknowable from current designs** — would require a trial nobody will run

Feed these to `evidence-gap-analysis` rather than leaving them in a document
nobody revisits.

## Structure

```markdown
# Evidence synthesis: [question or topic]
DRAFT — NOT FOR EXTERNAL USE. REQUIRES QUALIFIED MEDICAL REVIEW.

## What the evidence supports
The two or three things a reader should take away. Certainty stated for each.

## Evidence by question
### [Question 1]
What the totality shows, why, and the certainty. Studies cited as evidence,
not narrated in sequence.
### [Question 2]
...

## Where the evidence conflicts
Each conflict, the candidate explanations, and the resolution — or an explicit
statement that it is unresolved.

## What the evidence does not establish
Categorised gaps.

## Evidence table
Full appraisal detail for reference.

## Provenance
Searches run, sources included and excluded with reasons, references verified.
```

**Lead with the conclusion.** Readers of a synthesis are deciding something. The
detail supports the conclusion; it does not build up to it.

## Common failures

- **The annotated bibliography.** Study-by-study, no integration. The most
  common output when a synthesis was requested.
- **Vote counting.** "Four studies positive, one negative" — ignores design,
  size, and quality entirely.
- **Uniform confidence.** Every claim stated in the same register regardless of
  the evidence behind it.
- **Contradictions omitted.** The paper that disagrees left out of the reference
  list. A reader who knows the field will spot the omission, and will then
  distrust everything else.
- **Double-counting.** The same trial appearing as its primary publication, its
  congress abstract, and a pooled analysis, counted as three.
- **The gap section that got cut.** Where most of the strategic value was.
- **Selective inclusion.** An inclusion criterion that happens to exclude the
  inconvenient studies. State inclusion and exclusion criteria up front, and
  list what was excluded and why.

## Before you finish

Read `house-rules/evidence-synthesis.md`, then run
`deliverable-quality-review` — synthesis is where overclaiming most often enters
a document, because aggregation feels like it adds certainty when it usually
does not.
