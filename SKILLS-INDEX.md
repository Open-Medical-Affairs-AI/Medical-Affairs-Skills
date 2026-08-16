<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Regenerate with: python3 scripts/build_index.py
     CI fails if this file is out of sync with the skills' frontmatter. -->

# Skills Index

Every skill in this library, what it is for, and what it needs. If you are an
AI agent that has just been pointed at this repository, read [AGENTS.md](AGENTS.md)
first — it explains how to run these. This file is the catalogue.

**How to read the columns**

- **Requires** — other skills in this library that this one builds on. Load them too.
- **Produces** — the named deliverable. Skills without one are reasoning components.
- **Network** — external hosts the skill needs. Blank means it works fully offline.


**48 skills.**

## Orchestrator

Start here if you have been handed a job and do not know which skill does it. This one routes.

| Skill | What it does | Requires | Produces | Network |
| --- | --- | --- | --- | --- |
| [`medical-affairs-orchestrator`](skills/medical-affairs-orchestrator/SKILL.md) | Route any Medical Affairs request to the right workflow and run it end to end. | `medical-affairs-foundations` | A routed, executed Medical Affairs workflow | — |

## Foundation — always loaded

These four are loaded for every Medical Affairs task. They carry the compliance boundaries, the evidence-appraisal discipline, the citation rules, and the self-critique pass. Skipping them is how you get a beautifully formatted document that cannot survive review.

| Skill | What it does | Requires | Produces | Network |
| --- | --- | --- | --- | --- |
| [`capability-detection`](skills/capability-detection/SKILL.md) | Work out what this runtime can actually do before promising a deliverable, and degrade visibly rather than failing. | — | Capability report and a resolved output strategy | — |
| [`citation-integrity`](skills/citation-integrity/SKILL.md) | Guarantee every factual claim traces to a real, retrievable source that actually says what it is cited for. | `medical-affairs-foundations` | Verified reference list with evidence tiers | `eutils.ncbi.nlm.nih.gov`<br>`api.crossref.org`<br>`api.openalex.org` |
| [`deliverable-quality-review`](skills/deliverable-quality-review/SKILL.md) | Red-team your own Medical Affairs deliverable before anyone else sees it. | `medical-affairs-foundations` | Review findings with severity, and a revised deliverable | — |
| [`evidence-appraisal`](skills/evidence-appraisal/SKILL.md) | Critically appraise clinical evidence the way an experienced Medical Affairs scientist does — before summarising, citing or building strategy on it. | `medical-affairs-foundations` | Appraised evidence with stated certainty and limitations | — |
| [`medical-affairs-foundations`](skills/medical-affairs-foundations/SKILL.md) | The operating principles, compliance boundaries and safety obligations that govern all Medical Affairs work. | — | Compliance and safety frame applied to every other skill | — |

## Reasoning primitives — composed by the workflows

Not usually invoked directly. The workflow skills call these to do the actual thinking.

| Skill | What it does | Requires | Produces | Network |
| --- | --- | --- | --- | --- |
| [`evidence-synthesis`](skills/evidence-synthesis/SKILL.md) | Turn a body of clinical evidence into a defensible narrative that states what the totality supports, what it does not, and where it disagrees with itself. | `medical-affairs-foundations`<br>`evidence-appraisal` | Evidence narrative with stated certainty and open questions | — |
| [`insight-generation`](skills/insight-generation/SKILL.md) | Turn raw observations into insights that change a decision. | `medical-affairs-foundations` | Insight set with implications and actions | — |
| [`strategic-analysis`](skills/strategic-analysis/SKILL.md) | Reason about Medical Affairs strategy rather than generating activity lists. | `medical-affairs-foundations` | Prioritised strategic choices with stated assumptions and trade-offs | — |

## Data and search — live external evidence

These reach the public literature, trial registry, and label/safety databases. They need network access; see docs/api-setup.md.

| Skill | What it does | Requires | Produces | Network |
| --- | --- | --- | --- | --- |
| [`clinical-trials-search`](skills/clinical-trials-search/SKILL.md) | Search ClinicalTrials.gov via the v2 API to map the trial landscape — what is running, by whom, in which populations, with what endpoints, and what is about to read out. | `citation-integrity` | Trial landscape with sponsors, phases, endpoints and timelines | `clinicaltrials.gov` |
| [`medical-terminology-mapping`](skills/medical-terminology-mapping/SKILL.md) | Resolve free-text clinical language to controlled vocabulary so insights, adverse events, conditions and interventions can be counted and compared consistently. | `medical-affairs-foundations` | Concept-to-code mappings with confidence and unresolved list | `eutils.ncbi.nlm.nih.gov` |
| [`pubmed-search`](skills/pubmed-search/SKILL.md) | Search PubMed properly and retrieve real, verifiable literature via the NCBI E-utilities API. | `citation-integrity` | Verified literature result set with search strategy recorded | `eutils.ncbi.nlm.nih.gov` |
| [`regulatory-label-intelligence`](skills/regulatory-label-intelligence/SKILL.md) | Retrieve approved US label content and post-marketing safety data via openFDA, and interpret both correctly. | `medical-affairs-foundations` | Label-grounded product facts and correctly-caveated safety context | `api.fda.gov` |
| [`systematic-literature-review`](skills/systematic-literature-review/SKILL.md) | Run a reproducible, PRISMA-aligned systematic literature review — protocol first, documented search strategy, screening funnel with recorded exclusion reasons, structured extraction, and risk-of-bias assessment. | `pubmed-search`<br>`evidence-appraisal` | PRISMA-aligned systematic review with flow diagram and evidence tables | `eutils.ncbi.nlm.nih.gov`<br>`clinicaltrials.gov` |

## Workflows — the jobs

One per recurring Medical Affairs job. Each produces a named deliverable and runs the six-stage execution contract in AGENTS.md.

| Skill | What it does | Requires | Produces | Network |
| --- | --- | --- | --- | --- |
| [`advisory-board-design`](skills/advisory-board-design/SKILL.md) | Design and run an advisory board that produces advice rather than agreement — charter, questions, advisor selection, fair market value, discussion design, and output that changes a decision. | `medical-affairs-foundations`<br>`strategic-analysis` | Advisory board charter, questions and materials | — |
| [`competitive-intelligence`](skills/competitive-intelligence/SKILL.md) | Track and interpret competitor scientific activity continuously — pipeline movement, publication patterns, evidence strategy, regulatory milestones and positioning shifts, and what they signal. | `medical-affairs-foundations`<br>`evidence-appraisal`<br>`strategic-analysis` | Competitive intelligence assessment | `clinicaltrials.gov`<br>`eutils.ncbi.nlm.nih.gov`<br>`api.fda.gov` |
| [`congress-intelligence`](skills/congress-intelligence/SKILL.md) | Analyse what changed at a medical congress and what the organisation should do about it — not summarise what was presented. | `medical-affairs-foundations`<br>`evidence-appraisal`<br>`strategic-analysis` | Congress intelligence readout | `eutils.ncbi.nlm.nih.gov`<br>`clinicaltrials.gov` |
| [`evidence-gap-analysis`](skills/evidence-gap-analysis/SKILL.md) | Identify what we still do not know, decide which gaps are worth closing, and propose how. | `medical-affairs-foundations`<br>`evidence-appraisal`<br>`strategic-analysis` | Prioritised evidence gap analysis with research proposals | `eutils.ncbi.nlm.nih.gov`<br>`clinicaltrials.gov` |
| [`field-insight-synthesis`](skills/field-insight-synthesis/SKILL.md) | Turn a body of field medical observations into insights leadership can act on. | `medical-affairs-foundations`<br>`insight-generation` | Field insight report with ranked insights and actions | — |
| [`field-medical-planning`](skills/field-medical-planning/SKILL.md) | Plan the field medical function over a cycle — territory and account prioritisation, MSL objectives, engagement planning across a stakeholder map, capacity modelling, and the metrics that describe scientific impact rather than activity volume. | `medical-affairs-foundations`<br>`strategic-analysis` | Field medical plan with prioritised accounts, objectives and capacity | — |
| [`guideline-engagement`](skills/guideline-engagement/SKILL.md) | Understand and engage with clinical practice guideline development — committee cycles, what evidence a guideline body will accept, whether current evidence could support inclusion, and planning against timelines far longer than a medical plan. | `medical-affairs-foundations`<br>`evidence-synthesis` | Guideline landscape assessment and evidence readiness plan | `eutils.ncbi.nlm.nih.gov` |
| [`integrated-evidence-plan`](skills/integrated-evidence-plan/SKILL.md) | Build the cross-functional evidence plan for an asset — every study, analysis and publication across clinical development, Medical Affairs, HEOR and market access, sequenced against the decisions and milestones each has to serve. | `medical-affairs-foundations`<br>`strategic-analysis` | Integrated evidence plan with sequencing, owners and decision links | — |
| [`investigator-initiated-study-review`](skills/investigator-initiated-study-review/SKILL.md) | Evaluate and govern investigator-initiated study proposals — IIS, ISR, IIT, investigator-sponsored research. | `medical-affairs-foundations`<br>`evidence-appraisal` | IIS proposal assessment and recommendation | `clinicaltrials.gov`<br>`eutils.ncbi.nlm.nih.gov` |
| [`kol-engagement-brief`](skills/kol-engagement-brief/SKILL.md) | Prepare an MSL or medical lead for a specific scientific exchange with a named external expert. | `medical-affairs-foundations`<br>`citation-integrity` | KOL engagement brief | `eutils.ncbi.nlm.nih.gov`<br>`clinicaltrials.gov` |
| [`launch-medical-readiness`](skills/launch-medical-readiness/SKILL.md) | Assess whether Medical Affairs is actually ready for a launch, label expansion or major data readout — and say plainly where it is not. | `medical-affairs-foundations`<br>`strategic-analysis` | Launch readiness assessment with a verdict | — |
| [`medical-affairs-metrics`](skills/medical-affairs-metrics/SKILL.md) | Measure whether Medical Affairs work changed anything, rather than counting how much of it happened. | `medical-affairs-foundations`<br>`strategic-analysis` | Metric set with definitions, sources and interpretation limits | — |
| [`medical-education-program`](skills/medical-education-program/SKILL.md) | Design independent medical education and company-organised scientific education — IME grant strategy, curricula, needs assessments, speaker programmes and their governance, symposia and preceptorships. | `medical-affairs-foundations`<br>`strategic-analysis` | Education programme design, needs assessment and governance plan | — |
| [`medical-information-response`](skills/medical-information-response/SKILL.md) | Draft responses to unsolicited medical enquiries from healthcare professionals, patients and payers, and build the standard response documents and FAQ library behind them. | `medical-affairs-foundations`<br>`citation-integrity`<br>`regulatory-label-intelligence` | Standard response document or scientific response letter | `eutils.ncbi.nlm.nih.gov`<br>`api.fda.gov` |
| [`medical-strategy-plan`](skills/medical-strategy-plan/SKILL.md) | Build or challenge a medical plan — the scientific priorities, the choices behind them, and the activities that trace to them. | `medical-affairs-foundations`<br>`strategic-analysis` | Medical plan with prioritised scientific objectives | `eutils.ncbi.nlm.nih.gov`<br>`clinicaltrials.gov` |
| [`payer-value-dossier`](skills/payer-value-dossier/SKILL.md) | Build evidence for payers and health technology assessment bodies — AMCP format dossiers, NICE, G-BA and HAS submissions, value propositions, budget impact narratives, and responses to HTA critique. | `medical-affairs-foundations`<br>`evidence-synthesis` | Payer value dossier or HTA evidence submission | — |
| [`promotional-material-medical-review`](skills/promotional-material-medical-review/SKILL.md) | Review commercial promotional material as the medical signatory — the person who certifies that every claim is scientifically accurate, substantiated by the referenced data, and fairly balanced. | `medical-affairs-foundations`<br>`evidence-appraisal` | Medical review findings with a signatory decision and rationale | — |
| [`real-world-evidence-design`](skills/real-world-evidence-design/SKILL.md) | Design a real-world evidence study that will survive scrutiny — target trial emulation, data source selection, the estimand, confounding control, and a protocol written and registered before the data are touched. | `medical-affairs-foundations`<br>`evidence-appraisal` | RWE study concept or protocol with the estimand and design stated | `clinicaltrials.gov` |
| [`safety-communication`](skills/safety-communication/SKILL.md) | Communicate safety information to healthcare professionals and internal audiences — new safety findings, label safety changes, emerging signals, responses to safety questions, and the decision about whether and how to communicate at all. | `medical-affairs-foundations`<br>`regulatory-label-intelligence` | Safety communication plan and content | `api.fda.gov`<br>`eutils.ncbi.nlm.nih.gov` |
| [`scientific-communication-strategy`](skills/scientific-communication-strategy/SKILL.md) | Decide what the publication and scientific communication strategy should be — which questions to answer, for which audiences, in what sequence — rather than listing papers by data availability. | `medical-affairs-foundations`<br>`strategic-analysis` | Scientific communication strategy and prioritised publication plan | `eutils.ncbi.nlm.nih.gov` |
| [`scientific-platform`](skills/scientific-platform/SKILL.md) | Build or challenge the scientific platform — the core evidence-based narrative, the scientific statements it supports, the lexicon, and the communication objectives everything else derives from. | `medical-affairs-foundations`<br>`evidence-synthesis` | Scientific platform with substantiated statements | — |

## Content generation — the deliverables

Turn analysis into the artefact somebody actually receives: a deck, a manuscript, an abstract, a poster, a lay summary, a review pack.

| Skill | What it does | Requires | Produces | Network |
| --- | --- | --- | --- | --- |
| [`congress-abstract-and-poster`](skills/congress-abstract-and-poster/SKILL.md) | Write congress abstracts that fit the submission rules and build the posters that follow them. | `medical-affairs-foundations`<br>`citation-integrity`<br>`capability-detection` | Congress abstract and poster (.pptx) | — |
| [`data-visualization-for-medical`](skills/data-visualization-for-medical/SKILL.md) | Produce clinical trial figures that are honest and interpretable — Kaplan- Meier curves with numbers at risk, forest plots, waterfall and spider plots, adverse event figures, PRISMA flow diagrams. | `medical-affairs-foundations`<br>`evidence-appraisal`<br>`capability-detection` | Publication-quality clinical figures | — |
| [`diagram-and-schema`](skills/diagram-and-schema/SKILL.md) | Draw the diagrams Medical Affairs actually needs — treatment pathways, study schemas, PRISMA flow diagrams, patient journeys, evidence maps, decision trees, mechanism-of-action schematics, and governance flows. | `capability-detection` | Diagram (Mermaid, SVG or ASCII) | — |
| [`document-ingestion`](skills/document-ingestion/SKILL.md) | Read documents someone has given you — PDF, Word, PowerPoint, Excel, CSV. | `medical-affairs-foundations`<br>`capability-detection` | Extracted document text, tables and structure | — |
| [`interactive-html-report`](skills/interactive-html-report/SKILL.md) | Build a self-contained HTML report that opens in any browser with no dependencies — evidence dashboards, insight reports with filterable tables, congress readouts, competitive landscapes, evidence gap trackers. | `capability-detection`<br>`medical-affairs-foundations` | Self-contained interactive HTML report | — |
| [`medical-correspondence`](skills/medical-correspondence/SKILL.md) | Write the formal correspondence Medical Affairs sends — Dear Healthcare Professional letters, responses to investigators and institutions, agency and vendor briefs, advisory board invitations, author correspondence, and letters accompanying scientific responses. | `medical-affairs-foundations`<br>`capability-detection` | Formal medical correspondence | — |
| [`medical-slide-deck`](skills/medical-slide-deck/SKILL.md) | Build non-promotional medical slide decks — advisory board decks, MSL scientific presentations, congress readouts, medical-to-medical (M2M) presentations, internal data reviews and training material. | `medical-affairs-foundations`<br>`citation-integrity`<br>`capability-detection` | Non-promotional medical slide deck (.pptx) | — |
| [`mlr-review-readiness`](skills/mlr-review-readiness/SKILL.md) | Prepare Medical Affairs content for Medical/Legal/Regulatory review and pre-check it against what reviewers actually reject. | `medical-affairs-foundations`<br>`citation-integrity` | Claim-evidence matrix and MLR submission pack | — |
| [`pdf-generation`](skills/pdf-generation/SKILL.md) | Produce PDF deliverables — briefs, reports, standard response documents, one-pagers, evidence summaries, anything that must look the same for every reader and print predictably. | `capability-detection`<br>`medical-affairs-foundations` | PDF deliverable (or print-ready HTML) | — |
| [`plain-language-summary`](skills/plain-language-summary/SKILL.md) | Write plain language summaries of clinical research for patients and the public — trial results lay summaries, plain language summaries of publications, and patient-facing scientific material. | `medical-affairs-foundations`<br>`evidence-appraisal` | Plain language summary | — |
| [`scientific-manuscript`](skills/scientific-manuscript/SKILL.md) | Draft, structure and prepare a scientific manuscript for journal submission — primary trial reports, secondary analyses, real-world evidence papers, reviews and case reports. | `medical-affairs-foundations`<br>`citation-integrity`<br>`capability-detection` | Manuscript draft (.docx) with reporting-guideline checklist | — |
| [`spreadsheet-analysis`](skills/spreadsheet-analysis/SKILL.md) | Analyse and produce spreadsheets — field insight exports, enquiry logs, publication trackers, evidence tables, budget allocations, congress abstract lists. | `capability-detection`<br>`medical-affairs-foundations` | Spreadsheet analysis or a generated workbook | — |
| [`visual-abstract`](skills/visual-abstract/SKILL.md) | Create visual abstracts and infographics that summarise a study or a body of evidence honestly. | `medical-affairs-foundations`<br>`evidence-appraisal`<br>`capability-detection` | Visual abstract or infographic (SVG) | — |


---

## Loading order

For any real task the order that works is:

1. **Foundation** — all four, always.
2. **Orchestrator** — if you do not already know which workflow you need.
3. **One workflow** — the job itself.
4. **Whatever that workflow requires** — it declares its own dependencies.
5. **One content skill** — only once the analysis is done and reviewed.

Loading a content skill before the analysis is finished is the most common
failure mode. It produces a well-formatted document with nothing behind it.

## Overrides

Every skill reads `house-rules/<skill-name>.md` before it produces anything.
That is where your organisation's SOPs, terminology, and standards go. Rules
there beat the defaults in the skill. You should not need to fork this
repository to make it behave like your company.
