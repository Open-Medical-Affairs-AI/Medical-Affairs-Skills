# Medical Affairs Agent Skills

![Medical Affairs colleagues working alongside AI agents that use a shelf of ready-made skills](assets/readme/skills-hero.jpg)

**A free library of 65 ready-made "skills" that teach any AI agent how to do real Medical Affairs work: field insights, KOL preparation, medical information, congress readouts, launch plans and more.**

## New to GitHub? Start here

You don't need to install anything, write code or even have a GitHub account. This page is just a link you hand to your AI agent.

![Three steps: 1 copy the repository link, 2 give it to your AI agent, 3 the agent does the job and you review it](assets/readme/how-it-works.jpg)

1. **Copy this page's link.** It's the address in your browser's address bar:
   `https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills`.
   (You can also click the green **Code** button near the top right of this page and copy the link shown under **HTTPS**.)
2. **Give it to your AI agent.** Open Grok Bot, ChatGPT, Claude, Microsoft Copilot or the agent you use, start a new conversation and paste a sentence like this:

   ```
   Read https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills and use its skills to tell me the three field insights leadership should act on this quarter, using the synthetic oncology data.
   ```

   Swap the last part for your own job, for example *"…to prepare me for a difficult KOL meeting"* or *"…to build a medical launch plan for our upcoming asset"*.
3. **Let it work, then review.** The agent picks the right skills and the practice data, does the work and hands back a draft (Word, PowerPoint or PDF where it can). **You are the final judge.** Check it the way you'd check a new colleague's work.

**Agent can't open links?** Click the green **Code** button → **Download ZIP**, then upload the ZIP (or one of the small [starter files](workshop/bundles/)) to your agent.

## What's inside

| What | In plain words | Where |
|---|---|---|
| 🧠 **65 skills** | Step-by-step know-how for one Medical Affairs job each (an MSL brief, an MI response, a publication plan…) | [`skills/`](skills/) · [list of all skills](SKILLS-INDEX.md) |
| 🎯 **17 missions** | Ready-made assignments with a clear goal, the right files and the deliverables to expect | [`workshop/catalog.json`](workshop/catalog.json) · [team missions](workshop/missions/) |
| 📝 **House rules** | One page per skill where your team writes "how we do it here"; the agent follows your rules over its defaults | [`house-rules/`](house-rules/) |
| 🧪 **Practice data** | A fictional company with three fictional products, plus a catalog of 52 real public data sources, kept in a separate repository | [Open-Medical-Affairs/Data-Sources](https://github.com/Open-Medical-Affairs/Data-Sources) |
| 🌐 **Event website** | Copy-ready prompts, missions, datasets and a prompt optimizer for the AI in Action event | [Open-Medical-Affairs/AI-in-Action-Website](https://github.com/Open-Medical-Affairs/AI-in-Action-Website) |
| 🤖 **For agents** | The agent's own instructions | [`AGENTS.md`](AGENTS.md) |

![A shelf of skill cards that an AI agent can load](assets/readme/skills-shelf.jpg)

## Meet the launch swarm

![An org chart of AI digital workers coordinated by a human lead](assets/readme/swarm-orgchart.jpg)

The newest skill, [`medical-launch-plan`](skills/medical-launch-plan/SKILL.md), builds an entire medical launch plan for any upcoming asset. Instead of one chatbot, it runs an **org chart of digital workers** (strategy, evidence, publications and congress, field, training, medical information, safety, content review, metrics and more). Each worker gets its own context, they work in waves, and **a human decides at every gate**. Ask your agent:

```
Read https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills and use the medical-launch-plan skill to build a launch plan for the fictional product NORVANTIB, using the synthetic oncology data. Stop at each decision gate for my review.
```

The practice data it uses lives in **[Open-Medical-Affairs/Data-Sources](https://github.com/Open-Medical-Affairs/Data-Sources)**.

![A Medical Affairs leader reviewing the agents' work: the human is always the final judge](assets/readme/human-judge.jpg)

<sub>Illustrations generated for Open Medical Affairs.</sub>

---

# For builders

**Give your agent a Medical Affairs objective. Get a traceable draft you can review.**

65 skills · 17 workshop missions · 3 therapeutic areas · public scientific APIs · synthetic data included

![How Medical Affairs Agent Skills works: give an objective, use synthetic data or public evidence, let the agent analyze and check, then review the deliverables.](assets/how-it-works.png)

## Start here. No coding required.

Open the workshop **GrokBot**, copy the prompt below, and let it work:

```text
Use https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills
Read AGENTS.md and start a workshop mission using the bundled synthetic data.
Begin with oncology field insights unless I choose another area.
Find the three things leadership should know, explain why they matter,
and create a concise leadership brief with source records and next actions.
Use available public APIs only when useful, keeping real evidence separate
from fictional workshop facts. Do not ask me to connect company systems.
If you cannot retrieve the repository, tell me which starter file to upload.
```

**That is the first exercise.** You do not need a GitHub account, company data,
Veeva, Salesforce, SharePoint, or an API key to use the synthetic materials.
You do need a working agent that can read the repository or an uploaded starter.
Internet enables live evidence retrieval. Your agent service may have its own costs.

**Cannot open GitHub from your agent?** Download and upload a self-contained starter:
[Oncology](workshop/bundles/first-mission-oncology-mm.md) ·
[Immunology](workshop/bundles/first-mission-immunology-ad.md) ·
[Cardiometabolic](workshop/bundles/first-mission-cardiometabolic-obesity.md).
On the file page use **Download raw file**. For everything, use **Code → Download ZIP**.

> **Agent reading this?** Start with [AGENTS.md](AGENTS.md). Select the relevant
> skills and inputs; do not load the entire repository into context.

## Choose what you want to accomplish

| Say this to your agent | What it can prepare |
|---|---|
| “Tell leadership what the field is telling us.” | Insight report, source records, priority actions |
| “Prepare me for this difficult KOL meeting.” | Expert brief, scientific questions, unresolved evidence |
| “What changed after congress?” | Readout, evidence limitations, implications for the plan |
| “Work through this medical enquiry queue.” | Triage, draft responses, gaps and simulated safety routing |
| “Which evidence projects should we fund?” | Prioritized portfolio, budget trade-offs, dependencies |
| “Turn this study into consistent scientific materials.” | Manuscript draft, abstract, figure and plain-language summary |
| “Prepare an advisory board around unanswered questions.” | Charter, questions, advisor briefs and pre-read |
| “Are we ready for launch?” | Gate assessment, unresolved dependencies and remediation plan |
| “Use the practice CRM to plan field coverage.” | Account priorities and a feasible field plan |
| “Update content across our medical channels.” | Asset review queue, channel plan, evidence-change impact |
| “Build patient input into our evidence priorities.” | Accessible engagement plan and feedback-to-decision table |
| “Run the next 30 days of Medical Affairs.” | Coordinated plan, brief, tracker and scientific materials |

Use your own task too. The agent routes and combines skills. If a task needs missing
data, a tool or a human decision, it should name that gap and finish the supported work.
This is broad workflow coverage, not a guarantee that every task can be automated.

## How it works

1. **You give the objective.** No skill names or technical prompt required.
2. **The agent selects the inputs.** Synthetic packs for workshop work; your supplied
   data or authorized connections for actual work.
3. **It retrieves and analyzes.** Public evidence where useful, exact sources,
   appropriate study interpretation and explicit gaps.
4. **It checks the draft.** Challenges claims, reconciles numbers and preserves
   material limitations and safety findings.
5. **You review the result.** Designed files — Word + PDF for briefs and research,
   PowerPoint + PDF for decks — with sources, next actions and remaining
   decisions. Professional approval stays with accountable people.

Every skill carries the same standalone deliverable engine (`scripts/ma_render.py`):
native charts, stat cards, banded tables, cover pages, draft marking on every
page, and a preview contact sheet the agent inspects before handing over.
Markdown is only a drafting format. For GrokBot agents, build complete uploads
with `python3 scripts/package_skills.py` — see [agent setup](docs/agents.md).

## No company connectors? Start anyway.

| What is available | What happens |
|---|---|
| Synthetic pack only | The agent completes the supported mission with local sources |
| Internet and public APIs | It can add separately labelled real-disease evidence |
| Your authorized company connections | It can use the permitted records and document versions |
| Python but no pip | The engine still writes a real .docx or print-ready HTML and says what degraded |
| No code execution or file creation | It reads available files and provides structured content in the response |

A public API outage is not an empty search. A missing renderer is not permission
to lose the analysis. The agent states what it could and could not do.

## More HCP engagement. Less MSL administration.

The MSL workflow gathers prior interactions, open commitments, scientific evidence
and access context, then prepares a focused pre-call brief. After the conversation,
it turns supplied notes into draft CRM records, follow-up tasks and scientific gaps.
It can also identify relevant professional profiles and appropriate institutional
access routes, guided by scientific need rather than prescribing value.

**New MSL missions:** pre-call preparation, HCP discovery/access, post-call follow-up
and clearing the administrative queue. The practice organization includes **90 access
records and 180 task records**. Actual outreach and CRM updates need authorized tools.

[MSL workflow and starter prompt](docs/msl-workflow.md)

## Public scientific tools are included

**PubMed, ClinicalTrials.gov, openFDA, Europe PMC and Crossref** have executable
search/retrieval routes. Citation checking resolves identifiers and supports a
separate source-to-claim review. Core public routes need no key at basic limits.
OpenAlex is an optional verification fallback, with access requirements checked at use.

**Transcription:** supplied transcripts work immediately. Native audio tools or
optional local Whisper can process recordings where the environment supports them.
Local Whisper is free software; a hosted transcription service is not assumed free.

The agent can run these from a Python-capable environment:

```bash
python3 scripts/workshop.py check --live
python3 scripts/public_evidence.py pubmed --query 'multiple myeloma' --limit 5
```

[API setup and limitations](docs/api-setup.md) · [Audio/transcription](docs/transcription.md)

## A fictional organization you can actually work with

The practice data lives in its own repository,
**[Open-Medical-Affairs/Data-Sources](https://github.com/Open-Medical-Affairs/Data-Sources)**, which keeps two clearly separated halves:
**synthetic** workshop datasets (fictional, marked `SYNTHETIC`) and a catalog of
**52 real public data sources** grouped by Medical Affairs job. Clone it into this
repository's root so paths such as `Data-Sources/synthetic/oncology-mm/product-profile.md`
resolve (the folder is git-ignored here):

```bash
git clone https://github.com/Open-Medical-Affairs/Data-Sources.git Data-Sources   # or: python3 scripts/data_sources.py --fetch
```

A sibling checkout (`../Data-Sources`) or `MA_DATA_SOURCES=/path` also works. Agents
without a shell can read every file through the raw links in
[`synthetic/index.json`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/index.json).

The oncology, immunology and cardiometabolic packs contain **31 source files each,
plus a README**: profiles, field notes, enquiries, trial summaries, congress abstracts,
manuscripts, budgets, study concepts, readiness trackers, review comments and more.

The connected practice organization adds **24 accounts, 90 clinicians, 163 field
interactions, 18 enquiries, 36 content assets, 90 engagement records, 12 patient
partnership records and 18 projects**, plus a data dictionary and source registry.
Use its CSV files or the included SQLite database. No server or login is needed.

All products, people and clinical results in these packs are fictional. Their
inconsistencies are deliberate exercises in judgment. Real bibliographic examples
are stored [separately](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/public/evidence-snapshots/README.md), never as evidence for
fictional product claims.

[Synthetic datasets](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/README.md) ·
[Public data sources](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/public/catalog.md) ·
[Practice organization](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/README.md) ·
[Original skill coverage](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/SKILL-COVERAGE.md) ·
[Complete mission and input catalog](workshop/catalog.json)

## The October workshop

Start with a small win, improve it with a local rule, then tackle a larger objective.
The capstone asks the agent to plan the next 30 days. Halfway through, the facilitator
introduces changed evidence, a budget cut or a new constraint. The agent must identify
and update the affected work, with a visible change log.

[Participant quickstart](workshop/PARTICIPANT-QUICKSTART.md) ·
[Two-hour facilitator runbook](workshop/OCTOBER-RUNBOOK.md) ·
[Change cards](workshop/change-cards/README.md) · [Scorecard](workshop/scorecard.md)

[Readiness checks and remaining rehearsal steps](docs/validation.md)

## Bring it to work later

Use the [connection guide](docs/connections.md) for Veeva Vault CRM, Veeva CRM on
Salesforce, other Vault applications, Salesforce, SharePoint and local databases.
The agent first checks what is actually connected, then asks for the specific
missing access or an approved export. Tenant permissions are never bundled here.

Customize `house-rules/<skill-name>.md` in your own workspace. Private SOPs and
company records stay private. Seeded examples are not active company policy.
See [agent setup](docs/agents.md) and [execution behavior](docs/execution.md).

## What the files can look like

The [synthetic advisory-board example](examples/advisory-board-deck/) demonstrates
the shared visual style, clinical figures and deck generator. Available formats
include presentations, documents, spreadsheets, PDFs and interactive HTML.
Actual formats depend on the agent environment; supported content remains available
when a preferred renderer is missing.

[All 65 skills](SKILLS-INDEX.md) · [Capability menu](assets/menu-card.svg)

## Open to use. Official changes controlled by the maintainers.

**Apache-2.0.** The industry can use and adapt these skills. Forks do not grant
write access to this official repository. Contributions come through pull requests;
`@vivmuk` is the default code owner. Enforced review also requires the owner to
activate GitHub branch rules. [Governance setup and current verification limits](docs/repository-governance.md).

[Contributing](CONTRIBUTING.md) · [License](LICENSE) · [Attribution](THIRD-PARTY-NOTICES.md)

## Review before real use

Outputs are drafts requiring qualified review. This is not a clinical decision
system, validated GxP platform or pharmacovigilance reporting system. Workshop
safety cases are simulated; real cases follow your actual reporting procedures.
See [DISCLAIMER.md](DISCLAIMER.md). Do not upload real company or patient data into
the workshop environment.
