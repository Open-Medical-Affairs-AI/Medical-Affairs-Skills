---
name: medical-affairs-orchestrator
description: >-
  Route any Medical Affairs request to the right workflow and run it end to
  end. Load this FIRST when someone gives you a Medical Affairs job
  rather than a named skill — "prepare me for this KOL meeting", "what do
  these field notes mean", "build our medical plan", "what evidence are we
  missing" — or any multi-part objective. Works out which workflow the job
  maps to, loads only what that job actually needs, and enforces the six-
  stage execution contract so the agent inventories what is missing and
  challenges its own conclusions before delivering anything.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.2.0"
  tier: orchestrator
  maturity: stable
  requires:
    - medical-affairs-foundations
  produces: A routed, executed Medical Affairs workflow
---

# Medical Affairs Orchestrator

You have been given a job, not a skill name. Your task is to work out what job
it is, load what you need, and execute it properly.

Do not ask the user which skill to use. They should never have to know.

Read [execution.md](../../docs/execution.md) for workshop mode, resumable tasks,
source dependencies and authorized actions. For workshop inputs, consult the
selected entry in [catalog.json](../../workshop/catalog.json).

## Stage 0 — Orient

**Load `medical-affairs-foundations` first, always.** It carries the compliance
boundary, the safety escalation rule and the intake gate, and nothing here is
safe to run without it.

Then load the rest of the core **when the job needs it**, not by reflex. Loading
all of it on every task costs more context than most jobs contain:

| Load | When |
|---|---|
| `evidence-appraisal` | The job interprets study data — any trial, publication, abstract, real-world analysis or safety database. Skip it only when nothing you are handling carries a study behind it: transcribing narrative or process content into a new format is exempt, but the moment a result appears you have to name its design, and naming a design is interpretation. |
| `citation-integrity` | The deliverable will carry citations, or the agent is about to write a reference from memory. |
| `deliverable-quality-review` | **At stage 4**, not now. It is the challenge pass; loading it at orient time buys nothing. |
| `capability-detection` | The job produces a file. |

Then route.

## Routing

Match on what the person wants to *end up with*, not on the words they used.
This table carries the trigger phrasings, so that the skills themselves do not
have to hold them in permanently resident context.

**Someone hands you material and asks what it means**

| The job sounds like | Load |
|---|---|
| First workshop task, synthetic inputs, getting started | `workshop-launcher` |
| Connect CRM, Veeva, Salesforce, SharePoint or SQL data | `data-connection` |
| Audio or a meeting transcript to review before synthesis | `meeting-transcription` |
| A file to read first — PDF, Word, PowerPoint, Excel, CSV; "here's the paper", "look at this deck" | `document-ingestion`, then route on what it turns out to be |
| Field notes, MSL records, interaction logs; "what is the field telling us", "synthesise these" | `field-insight-synthesis` |
| A spreadsheet, enquiry log, tracker; cross-tabulate, de-duplicate, check this data | `spreadsheet-analysis` |
| What happened at a congress; post-meeting readout; "what did we learn at ASH" | `congress-intelligence` |
| What a competitor announcement means; ongoing competitor monitoring | `competitive-intelligence` |
| Code these observations; normalise this terminology; map to MeSH or MedDRA | `medical-terminology-mapping` |

**Someone wants a decision, a plan or a position**

| The job sounds like | Load |
|---|---|
| Medical content across channels, asset expiry or localization | `medical-content-operations` |
| Patient organizations, accessible listening or co-creation | `patient-engagement-planning` |
| Annual plan; scientific priorities; landscape assessment; "review this medical plan" | `medical-strategy-plan` |
| What don't we know; what should we study; research prioritisation; budget allocation | `evidence-gap-analysis` |
| Evidence across functions and lifecycle; "build the integrated evidence plan"; reconciling competing evidence requests | `integrated-evidence-plan` |
| What should we publish; publication plan; "what are we over-communicating" | `scientific-communication-strategy` |
| The core narrative, scientific statements, lexicon; "what is our scientific story" | `scientific-platform` |
| Territory and MSL planning; field objectives; "is this field plan realistic" | `field-medical-planning` |
| Are we ready for launch; readiness gate; label expansion preparation | `launch-medical-readiness` |
| Guideline inclusion or positioning; a guideline just updated | `guideline-engagement` |
| Scorecard, KPIs, "how do we show medical's value", choosing success measures | `medical-affairs-metrics` |
| What does the totality of evidence say; reconciling conflicting trials into one position | `evidence-synthesis` |
| Any of the above, but the question is really "so what should we do" | `strategic-analysis` |

**Someone wants an event, a programme or a study designed**

| The job sounds like | Load |
|---|---|
| Advisory board, expert panel, steering committee, scientific roundtable | `advisory-board-design` |
| MSL pre-call preparation, prior commitments and logistics | `msl-pre-call-planning` |
| Find scientifically relevant HCPs and appropriate access routes | `hcp-discovery-and-access` |
| Post-call CRM notes and scientific follow-up drafts | `msl-post-call-follow-up` |
| MSL open tasks, duplicate records and weekly administration | `msl-administrative-operations` |
| Prepare for a meeting with a named expert; KOL profile; "brief me before this call" | `kol-engagement-brief` |
| Medical education, IME grant, curriculum, speaker programme, symposium, preceptorship | `medical-education-program` |
| An IIS, ISR or IIT proposal to review; governing the IIS programme | `investigator-initiated-study-review` |
| Design an RWE study, external control arm, choosing a data source | `real-world-evidence-design` |

**Someone wants evidence retrieved**

| The job sounds like | Load |
|---|---|
| Supplementary open-access discovery or public API access | `public-evidence-search` |
| Find the literature on X; what has been published; a KOL's publication record | `pubmed-search` |
| What trials are running; competitor pipeline; verify an NCT number | `clinical-trials-search` |
| What is it approved for; label wording; boxed warning; FAERS reports | `regulatory-label-intelligence` |
| Everything on X, defensibly complete; HTA or guideline submission | `systematic-literature-review` |
| Keep me posted on X; weekly or monthly literature update; what's new since last month | `literature-surveillance` |

**Someone wants something produced**

| The job sounds like | Load |
|---|---|
| Slides, a deck, a presentation, an M2M deck | `medical-slide-deck` |
| A paper, manuscript, cover letter, or reviewer response | `scientific-manuscript` |
| Congress abstract or poster | `congress-abstract-and-poster` |
| A letter, DHCP letter, formal email to an external professional | `medical-correspondence` |
| Answer this clinical question; standard response document; FAQ development | `medical-information-response` |
| Payer or HTA material; AMCP dossier; NICE or G-BA submission; value proposition | `payer-value-dossier` |
| Communicate a safety finding, signal or label safety change | `safety-communication` |
| Lay summary, patient-facing material | `plain-language-summary` |
| A PDF; something that must print identically for every reader | `pdf-generation` |
| An interactive report, dashboard, filterable table | `interactive-html-report` |
| A chart, KM curve, forest plot, waterfall, AE figure | `data-visualization-for-medical` |
| A visual abstract or infographic | `visual-abstract` |
| A treatment pathway, study schema, PRISMA diagram, flowchart | `diagram-and-schema` |
| The exec summary, one-pager, "brief leadership", C-suite or board audience | `executive-briefing` |
| What can you do; what's in this library; capability overview for stakeholders | `library-menu` |
| It looks unpolished; "executive-ready" or "board-ready"; consistent look across outputs | `consulting-grade-design` |

**Someone wants content checked**

| The job sounds like | Load |
|---|---|
| Check our own content before MLR; "is this promotional"; why did this come back | `mlr-review-readiness` |
| Review or sign off someone else's promotional material as medical signatory | `promotional-material-medical-review` |
| Does this reference say what we claim; verify these citations | `citation-integrity` |
| Red-team this; critique this deliverable | `deliverable-quality-review` |

Load the workflow skill, then whatever it declares in `metadata.requires` — that
is the short list it cannot run without. `metadata.suggests` names skills the
job **may** reach into; follow one only when the work actually goes there, and
tell the user rather than loading it speculatively. `SKILLS-INDEX.md` lists
every skill with both.

**Two skills that look alike, and are not.** `mlr-review-readiness` prepares our
own material for review; `promotional-material-medical-review` is the reviewer
of someone else's. `kol-engagement-brief` is one meeting;
`field-medical-planning` is the cycle. `evidence-gap-analysis` finds the gaps;
`integrated-evidence-plan` sequences the studies that close them.
`real-world-evidence-design` designs a study; `evidence-appraisal` judges one.

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
separate this from summarisation. Announce the plan briefly at the start —
*"I'll treat this as a field insight synthesis: inventory the records and say
what's missing, scan for safety findings, build the insights, challenge them,
then deliver with provenance"* — then do it. Do not narrate every step; report
at the stage boundaries.

## The safety scan is not optional

Any job touching field notes, KOL interactions, medical information enquiries,
advisory board records or congress conversations gets an adverse event,
product-complaint and special-situation scan **before analysis**, per
`medical-affairs-foundations`. Surface findings at the top with verbatim quotes;
if you scanned and found nothing, say so. This runs even when the request is
framed as strategic — especially then, because that is when it gets skipped.

## House rules

Before producing anything, read `house-rules/<skill-name>.md` for every skill
you loaded. Rules there are the adopting organisation's and they **override**
the defaults — this is how a team adapts the library without forking it. If a
file contains only the seeded examples the organisation has not customised it
yet; use the defaults, and mention once that the file exists.

## Long-horizon objectives

Read [the worked example](references/long-horizon.md) when several workflows must
feed one another. Maintain run.json with completed steps and output dependencies.
When new evidence arrives, reassess affected conclusions and revise dependent
outputs. A host scheduler is required for future unattended work.

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
