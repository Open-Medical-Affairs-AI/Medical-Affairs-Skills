---
name: launch-field-training
description: >-
  Design the training and certification that make field medical teams able to
  handle launch conversations — the data, its limitations, the questions
  nobody can answer yet, unsolicited off-label requests and adverse event
  escalation — tested by scenario rather than recall. Use when planning launch
  or new-indication training for MSLs or medical teams, building a scenario
  bank, or checking whether field training is real. This is the field's
  capability; `field-medical-planning` decides deployment and capacity.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: workflow
  maturity: beta
  requires:
    - medical-affairs-foundations
    - evidence-appraisal
  suggests:
    - launch-medical-readiness
    - scientific-platform
    - medical-information-response
    - safety-communication
    - field-medical-planning
    - deliverable-quality-review
  produces: Field launch curriculum, scenario bank and certification plan
  deliverables: [docx, pdf, pptx]
---

# Launch Field Training

Launch training is usually measured by completion: 92% of modules done, green.
Completion measures attendance. What matters at launch is whether an MSL,
asked a hard question by a sceptical specialist in the first month, gives an
accurate, balanced, non-promotional answer — and says "we don't have that data"
when that is the truth, instead of improvising near the label boundary.

This skill designs training around that moment.

## Stage 1 — Inventory

- The six-month question list (`launch-medical-readiness`), classified answered
  / answerable / unanswerable. **If it does not exist, build it first** — the
  curriculum is built from it.
- Label wording, or the expected wording labelled as an assumption
- Approved scientific platform and lexicon (`scientific-platform`)
- Pivotal and supporting evidence with design and limitations
- MI enquiry history for the product or class; field insights
- Safety profile, intake routes, the unsolicited-request SOP
- Existing curriculum, assessment and completion data

**Name what is missing.** Training built before the platform is approved will
be rebuilt; say which modules depend on it.

## Stage 2 — The curriculum

Five strands. The last three are the ones that get cut for time, and the ones
that matter at the boundary.

| Strand | Content | Typical failure |
|---|---|---|
| **Disease and landscape** | Unmet need, pathway, competitors' evidence fairly stated | Competitor evidence presented weaker than it is |
| **The data** | Pivotal design, endpoints, results with uncertainty | Point estimates without intervals; subgroups quoted as findings |
| **The limitations** | What the design cannot show; populations not studied; open safety questions | Skipped, or one slide at the end |
| **"We don't know"** | Each unanswerable question with the honest answer and what *is* known | Never rehearsed, so improvised in the field |
| **Boundaries** | Unsolicited off-label pathway, AE/PQC detection and escalation, non-promotional exchange | Taught as policy reading, not practised |

Every module traces to a question on the list or to a boundary. A module that
traces to neither is a candidate to cut.

## Stage 3 — Scenarios and certification

Build a **scenario bank**: realistic exchanges, each with the question as a
clinician would actually ask it, the evidence-based answer, the limitation that
must be stated, the boundary in play, and what a failing answer sounds like.
Include, at minimum:

- the comparator question the trial does not answer;
- a question about a population that was excluded or under-represented;
- an unsolicited off-label request — correct routing, not refusal or answer;
- an adverse event mentioned in passing — detection and reporting route;
- a question where the right answer is "we don't have that data" plus what is known.

**Certify on application, not recall.** Role-play or recorded scenario
assessment scored against the bank, by a qualified reviewer. A multiple-choice
quiz on endpoint values is a recall test; it tells you nothing about the
moment that matters. Report certification by strand, so "trained" can be broken
down into "can explain the data" and "can handle the boundary".

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus:

- Does every unanswerable question have a rehearsed answer?
- Does any training claim say more than the platform? Stronger in training than
  in the approved platform is promotional drift.
- Is the competitor evidence stated fairly?
- Does the certification measure application? If 100% pass on first attempt,
  it is probably testing recall.
- What happens when the label wording lands different from the assumption —
  which modules and scenarios change, and how long does recertification take?

## Stage 5 — Deliver

```
DRAFT — NOT FOR EXTERNAL USE. REQUIRES QUALIFIED MEDICAL REVIEW.

QUESTION MAP        Six-month questions → module → scenario
CURRICULUM          Five strands, each module traced
SCENARIO BANK       Question, answer, limitation, boundary, failing answer
CERTIFICATION       Method, reviewer, pass criteria by strand
TIMELINE            Build, label-lands update, certify, refresh at L+3
READINESS EVIDENCE  What the readiness gate should accept as proof
```

Training material is internal but may be reused externally; anything leaving
the field team goes through `mlr-review-readiness`.

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

Read `house-rules/launch-field-training.md`. Certification standards, who may
assess, the unsolicited-request SOP and AE reporting routes are local, and
training that teaches the wrong reporting route is worse than none.
