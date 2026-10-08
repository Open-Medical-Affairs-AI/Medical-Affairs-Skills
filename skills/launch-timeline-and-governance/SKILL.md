---
name: launch-timeline-and-governance
description: >-
  Build the Medical Affairs launch critical path and the governance that runs
  it — workback from the decision date, dependencies on label wording and
  publication, gate criteria written before the gate, named owners, and what
  moves when the date moves. Use for a launch timeline, workback plan, launch
  RACI, gate criteria, or "what has to happen by when". This is the schedule
  and the decision rights; `medical-launch-plan` builds the content and
  `launch-medical-readiness` runs the gate.
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
    - medical-launch-plan
    - launch-medical-readiness
    - spreadsheet-analysis
    - diagram-and-schema
    - deliverable-quality-review
  produces: Launch critical path, gate criteria and governance plan with named owners
  deliverables: [docx, pdf, pptx]
---

# Launch Timeline and Governance

Launch timelines fail in two predictable ways. The first is the Gantt chart in
which every workstream ends the week before launch, so nothing depends on
anything and the critical path is invisible. The second is governance that
reports status without deciding anything — the steering committee that averages
six workstreams into "Green" while one of them is red and launch-blocking.

This skill produces the schedule a launch actually runs on and the decision
rights that let it say "stop".

## Stage 1 — Inventory

- The target decision or launch date — and whether it is confirmed or a
  **planning assumption**. Label it on every page either way.
- Each workstream's deliverables, durations and dependencies (from the
  `medical-launch-plan` workers or the existing plan)
- Fixed external dates: regulatory milestones, congress abstract deadlines,
  journal timelines, guideline evidence cut-offs, HTA submission windows
- Internal fixed dates: budget cycle, MLR turnaround, training windows,
  hiring lead time
- Existing governance: who sits on which committee, who can sign what

**Name what is missing.** A timeline without MLR turnaround or journal
acceptance time is a wish list with dates on it.

## Stage 2 — Build the workback

Work backwards from the date, not forwards from today. Typical anchor points —
**illustrative; replace with the organisation's actual lead times**:

| Window | What normally has to be true |
|---|---|
| L−24 to L−18 months | Launch medical objectives set; IEP studies that answer the six-month unanswerable questions started |
| L−18 to L−12 | Scientific platform and lexicon approved; publication and congress plan locked; field deployment and hiring plan approved |
| L−12 to L−6 | Primary manuscript submitted; SRD/FAQ drafting against expected wording; training curriculum built; advisory input complete |
| L−6 to L−0 | Final label wording received → dependent content updated and approved; field certified; MI capacity for the launch spike in place; safety escalation rehearsed |
| L+0 to L+12 | First-six-months monitoring of questions, insights and enquiries; post-launch reviews at L+3, L+6, L+12 |

Then for each deliverable: **duration, predecessor, owner, slack**. The
critical path is the chain with no slack. Report it explicitly; most teams have
never seen theirs.

### The dependencies that are usually missing

- **Label wording → nearly everything.** SRDs, training, platform statements,
  content. Plan the "label lands" sprint: what is pre-built against expected
  wording, what must be redone, and how many days that takes.
- **Manuscript acceptance → field discussion.** If the paper is not accepted
  by the time the field presents, the field discusses data with no citable source.
- **Platform approval → all Wave 2 work.** Content built on an unapproved
  platform gets rebuilt.
- **MLR turnaround × volume.** Twenty SRDs at a realistic review cycle do not
  fit in the last six weeks. Count them.
- **Hiring and onboarding → field capacity.** New MSLs are not launch-ready on
  their start date.

## Stage 3 — Governance

### Gate criteria, written before the gate

For each gate: what must be true, how it is evidenced, and **which single
failures are launch-blocking regardless of everything else**. Write this before
the gate meets. Criteria written at the gate are negotiated to fit the status.

Never aggregate a gate by averaging workstream colours. One red, launch-blocking
item makes the gate red; that is what launch-blocking means.

### Decision rights

A RACI with **named people**, not functions. For each gate and each
cross-workstream conflict: who decides, who is consulted, the escalation route,
and the date the decision is needed by. An escalation route that ends at a
committee with no meeting before the deadline is not a route.

### Cadence

Match the cadence to the phase: monthly while the plan is forming, fortnightly
inside L−6, weekly inside L−8 weeks and through the first month. Each meeting
reviews the critical path and open decisions, not workstream status slides.

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus:

- Does anything on the critical path end the week before launch with no slack?
- Is any date stated as fact that is actually an assumption?
- Could the governance say "not ready"? Who would say it, and is it written down?
- If the date moved three months later, or one month earlier, what changes? If
  the answer is "we would replan", the plan has no dependency logic.
- Does any single person own more critical-path items than they can deliver?

## Stage 5 — Deliver

```
DRAFT — NOT FOR EXTERNAL USE. REQUIRES QUALIFIED MEDICAL REVIEW.

THE DATE            Confirmed or assumption; what moves if it moves
CRITICAL PATH       The chain with no slack, drawn
WORKBACK            By window, each deliverable with owner and predecessor
GATES               Criteria, evidence, launch-blocking items, decision owner
RACI                Named people; escalation routes with dates
CADENCE             What meets when, and what it decides
RISKS               Top schedule risks with early signals
```

Use `diagram-and-schema` for the critical-path visual and `spreadsheet-analysis`
when the plan needs to live as a tracker.

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

Read `house-rules/launch-timeline-and-governance.md`. Gate names, lead times,
committee structures and sign-off authority are local, and a timeline that uses
the wrong gate names will not be read by the people who run the gates.
