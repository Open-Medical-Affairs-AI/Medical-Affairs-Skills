# Digital worker briefs — the launch org chart

Each worker is a sub-agent (or a separate GrokBot agent built from the skill's
zip). Give it **exactly** the context packet below — the launch facts sheet, the
six-month question list, its slice of the inputs and the upstream outputs it
consumes — and nothing else. Inputs are named by their workshop file; in real
work substitute the organisation's equivalent source.

Every worker:

- loads `medical-affairs-foundations` and its own skills' `requires`, and reads
  `house-rules/<skill>.md` for each;
- returns its **output contract** (below) as a designed file plus a short
  structured hand-back: claims with source IDs, assumptions, open questions,
  dependencies on other workers, and gaps each with a proposed human owner and date;
- never approves, certifies, sends, registers, contacts or edits external
  systems; it drafts for a named human.

## The coordinator

### Launch Lead — `medical-launch-plan`
- **Context:** everything in the inventory, at summary level; the house rules;
  the governance map.
- **Does:** builds the facts sheet and six-month question list, staffs the
  chart, writes packets, sequences waves, integrates the joins, logs conflicts.
- **Hands back:** the integrated plan and the decision log.
- **May not:** rewrite a worker's conclusion, resolve a conflict silently, or
  edit the auditor's verdict.

## Pod 1 — Strategy & Evidence

### Strategy worker — `medical-strategy-plan` (+ `strategic-analysis`)
- **Context:** facts sheet, question list, `medical-plan.md`,
  `evidence-landscape.md`, `competitor-announcements.md`, `field-observations.csv`.
- **Output:** 3–5 launch medical objectives with trade-offs, a "not doing"
  list, and a success measure per objective that could come back negative.

### Evidence worker — `evidence-gap-analysis` → `integrated-evidence-plan` (+ `real-world-evidence-design` if a study is proposed)
- **Context:** facts sheet, question list, `integrated-evidence-plan.csv`,
  `evidence-landscape.md`, `rwe-study-concept.md`, `iis-proposal.md`.
- **Output:** the launch-window IEP: which unanswerable six-month questions have
  a study started, which will read out too late, and what that costs.

### Value & Access worker — `payer-value-dossier`
- **Context:** facts sheet, `payer-hta-brief.md`, the Evidence worker's IEP.
- **Output:** payer/HTA evidence readiness, the comparator payers will use, and
  the claims that do not survive their scrutiny.

## Pod 2 — Narrative & Communication

### Narrative worker — `scientific-platform`
- **Context:** facts sheet, question list, `scientific-platform-draft.md`,
  `product-profile.md`, `structured-evidence-table.csv`.
- **Output:** substantiated statement table, lexicon (including words to
  avoid), communication objectives. **Becomes part of every Wave 2 packet once
  a human approves it at Gate 1.**

### Pubs & Congress worker — `scientific-communication-strategy` (+ `congress-abstract-and-poster`, pre-congress `congress-intelligence`)
- **Context:** approved platform, question list, `publication-plan.md`,
  `congress-abstracts.md`, `abstract-poster-brief.md`, congress calendar.
- **Output:** launch publication and congress plan sequenced so every data
  point the field will discuss has a citable source first; encore and embargo risks.

### Guideline Scout — `guideline-engagement`
- **Context:** facts sheet, `guideline-landscape.md`, IEP.
- **Output:** guideline cycles inside the horizon, what evidence each body
  accepts, and whether any "guideline inclusion" objective is achievable at all.

## Pod 3 — External Engagement

### Field Medical worker — `field-medical-planning` (+ `hcp-discovery-and-access`)
- **Context:** facts sheet, objectives, `field-account-plan.csv`,
  `kol-dossiers.md`, capacity and headcount.
- **Output:** launch deployment: stakeholder map, account priorities, capacity
  model, MSL objectives that are not activity counts.

### Field Training worker — `launch-field-training`
- **Context:** approved platform, question list, label wording (or the
  assumption), `medical-information-enquiries.csv`, `safety-case-series.md`.
- **Output:** curriculum, scenario bank including "we don't know" and
  unsolicited off-label rehearsals, and a certification design that tests
  application rather than recall.

### Expert Input worker — `advisory-board-design` (+ `kol-engagement-brief` per advisor)
- **Context:** question list, evidence gaps, `advisory-board-transcript.md`,
  `kol-dossiers.md`.
- **Output:** advisory boards only where a question is genuinely open, with
  charters; "no advisory board is justified" is a valid result.

### Education worker — `medical-education-program`
- **Context:** `medical-education-needs.md`, question list, platform.
- **Output:** education plan that keeps independent education independent;
  rewritten learning objectives around competence, not product uptake.

### Patient Partnership worker — `patient-engagement-planning` (+ `plain-language-summary`)
- **Context:** facts sheet, `plain-language-source.md`, evidence gaps.
- **Output:** patient organisation engagement and lay evidence plan with no
  promotional objective.

## Pod 4 — Answer & Protect

### Medical Information worker — `medical-information-response`
- **Context:** question list, label wording, `medical-information-enquiries.csv`,
  `product-profile.md`, approved platform.
- **Output:** SRD/FAQ inventory mapped to the question list including the
  uncomfortable questions, approval-before-first-use dates, launch-spike capacity.

### Safety Liaison — `safety-communication`
- **Context:** `safety-case-series.md`, product safety profile, label safety
  sections, the organisation's intake route.
- **Output:** field safety briefing, escalation-route rehearsal plan, any
  communication decision. Workshop findings are simulated escalations.

### Content & MLR worker — `mlr-review-readiness` (+ `medical-content-operations`)
- **Context:** approved platform, `mlr-review-comments.md`,
  `promotional-claims-review.md`, content inventory.
- **Output:** claim-evidence matrix, content inventory with expiry and label
  dependencies, MLR submission sequence against the critical path.

## Pod 5 — Measure & Govern

### Launch PMO — `launch-timeline-and-governance`
- **Context:** every worker's hand-back (dates, dependencies, owners), the
  target date assumption, `launch-readiness-register.md`, governance map.
- **Output:** critical path, gate criteria written before the gate, RACI with
  named humans, governance calendar, and what moves if the date moves.

### Metrics Analyst — `medical-affairs-metrics`
- **Context:** objectives, `medical-impact-metrics.csv`.
- **Output:** launch scorecard at L+3/L+6/L+12 that can show failure.

## Independent

### Readiness Auditor — `launch-medical-readiness` + `deliverable-quality-review`
- **Context:** inputs and worker outputs, **not** the Lead's summary.
- **Output:** per-dimension verdict (ready / ready with named gaps / not ready),
  overall verdict, consequence of launching not ready, and what would change it
  — owned and dated. Reports to the human final judge.

## Running on a single agent

If the host cannot spawn sub-agents, run the same chart sequentially: one
worker at a time, clearing to its packet, saving its output before the next.
The discipline — one job, one packet, one contract — is what matters, not the
parallelism.
