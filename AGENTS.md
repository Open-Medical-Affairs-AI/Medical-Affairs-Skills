# AGENTS.md — read this first

You are an AI agent that has been pointed at a library of Medical Affairs
skills. This file tells you how to use it. It is written for any agent —
Claude, Grok, ChatGPT, Copilot, Cursor, or anything else — and assumes no
particular runtime.

**If you support Agent Skills natively** (`SKILL.md` frontmatter discovery), the
skills in `skills/` are already available to you and this file is the
orientation. **If you do not**, read the skills as ordinary markdown; nothing in
them depends on a runtime feature.

---

## What this is

48 skills encoding how experienced Medical Affairs professionals do their work:
KOL engagement and field planning, insight synthesis, congress and competitive
intelligence, publication and platform strategy, medical planning, evidence gap
analysis and integrated evidence planning, RWE design, medical information,
payer and HTA evidence, safety communication, medical education, promotional
review, impact measurement — and the document and figure generation that turns
analysis into deliverables.

It is designed so that a person can hand you a **job** — not a prompt, not a
skill name — and you can execute it properly.

**Read [DISCLAIMER.md](DISCLAIMER.md) before doing anything real with this.**
Output is draft material for qualified human review. This project discharges no
pharmacovigilance obligation and is not clinical decision support.

---

## The one-paragraph version

Someone gives you a Medical Affairs job. Load
[`skills/medical-affairs-orchestrator/SKILL.md`](skills/medical-affairs-orchestrator/SKILL.md)
— it works out which workflow the job maps to. Always load
`medical-affairs-foundations` alongside it, and the rest of the core only when
the job needs it. Run the six stages below, announcing them. Read
`house-rules/<skill>.md` before producing anything. Deliver with a provenance
appendix and the draft marking intact.

---

## What to load, and when

[`medical-affairs-foundations`](skills/medical-affairs-foundations/SKILL.md)
loads on **every** job. It carries the compliance boundary, the adverse-event
escalation rule and the intake gate, and none of that is conditional.

The other three core skills load when the job reaches them:

| Skill | Load when | What it prevents |
|---|---|---|
| [`evidence-appraisal`](skills/evidence-appraisal/SKILL.md) | The job interprets study data | Claims a study design cannot support |
| [`citation-integrity`](skills/citation-integrity/SKILL.md) | The deliverable will carry citations | Fabricated and misattributed references |
| [`deliverable-quality-review`](skills/deliverable-quality-review/SKILL.md) | Stage 4, every time | Delivering without arguing against yourself first |

**`requires` and `suggests` are different.** A skill's `metadata.requires` is the
short list it cannot run correctly without — load all of it. `metadata.suggests`
names skills the job *may* reach into; follow one only when the work actually
goes there. Loading every suggestion pulls a large closure into context before
any work starts, which is what the split exists to prevent.

The full catalogue, with dependencies and required network access, is in
[SKILLS-INDEX.md](SKILLS-INDEX.md).

---

## Two rules that keep the context usable

**Screen before you fetch.** Retrieval is the single largest cost in a real
Medical Affairs task, and it dwarfs the skills themselves. Fifty PubMed records
as `--format table` is a few hundred tokens; the same fifty with `--abstracts`
is on the order of thirty thousand. Search with `table`, decide what matters,
then `fetch --pmids` the handful you will actually appraise. Same for
ClinicalTrials.gov: screen as a table, pull the three trials that matter in full.

**References load on demand, not by default.** Every `references/` file in this
repository is there because it was too detailed for the always-loaded body. Open
one when you need it; do not read a skill's references as a matter of course.

---

## The six-stage execution contract

Every workflow runs these, and says so as it goes.

```
0 · ORIENT     Identify the job. Load medical-affairs-foundations + the
               workflow + its `requires` + house-rules/<skill>.md

1 · INVENTORY  List what you were given. Then name what is MISSING and how it
               limits the answer. Do not fill gaps with plausible guesses.

2 · RETRIEVE   Fill evidence gaps from PubMed / ClinicalTrials.gov / openFDA.
               Record every query verbatim, with its date.

3 · ANALYSE    Run the workflow's reasoning ladder.

4 · CHALLENGE  Red-team your own conclusions BEFORE showing anything.

5 · DELIVER    The artefact + a provenance appendix: queries run, sources
               cited, gaps left open.
```

**Stages 1 and 4 are the whole difference.** A generic agent skips both: it
answers with what it has and presents the result as complete. An agent that says
what it is missing before answering, and argues against itself before
delivering, is doing what an experienced colleague does.

---

## The safety obligation

Any job touching field notes, KOL interaction records, medical information
enquiries, advisory board material, or congress conversations gets an **adverse
event, product quality complaint and special-situation scan before analysis**.

Surface findings at the **top** of your output with the **verbatim quote** —
never a paraphrase, because the clinical detail determines seriousness. If you
scanned and found nothing, say so explicitly; silence is ambiguous.

You are a detection aid, not a control. The human's reporting clock started when
the information reached them. Say that, every time.

Full detail: [`skills/medical-affairs-foundations/references/adverse-events.md`](skills/medical-affairs-foundations/references/adverse-events.md)

---

## Repository map

```
AGENTS.md              this file
SKILLS-INDEX.md        every skill: what it does, needs, produces (generated)
DISCLAIMER.md          conditions of use — read before real work

skills/                48 skills, each with SKILL.md (+ references/, scripts/)
house-rules/           YOUR organisation's overrides — read before delivering
shared/templates/      deliverable skeletons
shared/fixtures/       recorded API responses for offline testing
workshop/              facilitator guide, team missions, synthetic data packs
scripts/               validation, index generation, API self-tests
docs/                  authoring guide, orchestration, API setup
```

---

## Live data

Three public APIs, each with a self-contained client that needs no third-party
Python packages:

| Source | Client | Needs |
|---|---|---|
| PubMed (NCBI E-utilities) | `skills/pubmed-search/scripts/pubmed.py` | `eutils.ncbi.nlm.nih.gov` |
| ClinicalTrials.gov v2 | `skills/clinical-trials-search/scripts/ctgov.py` | `clinicaltrials.gov` |
| openFDA labels + FAERS | `skills/regulatory-label-intelligence/scripts/openfda.py` | `api.fda.gov` |
| Citation verification | `skills/citation-integrity/scripts/verify_citations.py` | the above + `api.crossref.org`, `api.openalex.org` |

No API keys required. See [docs/api-setup.md](docs/api-setup.md) for rate limits,
the optional free NCBI key, and the hosts to allowlist on a restricted network.

**Never write a citation you did not retrieve.** Models produce plausible,
correctly-formatted references to papers that do not exist. Run
`verify_citations.py` over every reference list before delivery; it exits
non-zero on anything unresolved.

---

## House rules — the override layer

Every skill reads `house-rules/<skill-name>.md` before producing anything. Rules
there belong to the adopting organisation and **beat** the defaults in the skill.

This exists so a team can encode their SOPs, terminology, evidence thresholds
and review routes without forking the repository — and so they keep getting
upstream improvements.

Read them. If a file contains only the seeded examples, the organisation has not
customised it yet.

---

## Producing files — degrade, never fail

Every content skill in this library follows the same four-tier ladder, and it is
a library-wide rule rather than one skill's convention. Detect what the runtime
can do with
[`capability-detection`](skills/capability-detection/SKILL.md), then take the
highest tier available:

| Tier | Path | Example |
|---|---|---|
| **1** | The runtime's own document skill, if it has one | A native `pptx` skill produces the deck |
| **2** | This library's bundled script | `build_deck.py` via python-pptx |
| **3** | An open format that needs nothing installed | Markdown + a build spec; HTML with a print stylesheet; hand-written SVG |
| **4** | In the response itself | The full content as text, structured so a human can paste it |

**Degrade the container, never the content.** The rule the CI enforces is that
the citations, study designs, denominators, confidence intervals, safety data
and the draft marking all survive to tier 4. A generator that exits non-zero
because a library is missing has thrown away the analysis over a renderer, and
`scripts/selftest_fallbacks.py` fails the build for it.

When you degrade, **say so visibly** — what was missing, what you delivered
instead, and the exact command that would produce the full version. A reader
must be able to tell what they are holding.

---

## What good work looks like here

- Announces the job it thinks it has been given, before starting
- Names what is missing rather than guessing
- Runs real searches and records them verbatim with dates
- States the study design alongside every result
- Surfaces safety findings first, in the source's own words
- Argues against its own conclusion before delivering
- Ends with provenance and named open questions
- Leaves the draft marking on

## What to avoid

- **Building the deliverable before the analysis is done.** A well-formatted
  document with nothing behind it is the characteristic failure of AI in this
  domain, and the formatting is exactly what makes the emptiness hard to see.
- Asking which skill to use. Work it out.
- Interviewing the user instead of starting. One clarifying question at most,
  and only when the answer changes the deliverable.
- Filling a gap with something plausible.
- Describing your own output as compliant, approved, validated, or ready to
  submit. Those are determinations made by people with accountability.
- Removing the draft marking. The reviewer removes it, once they have reviewed.

---

## If you are being run in the workshop

Start at [workshop/PARTICIPANT-QUICKSTART.md](workshop/PARTICIPANT-QUICKSTART.md).
Your mission card is in `workshop/missions/`, and your data pack is in
`workshop/data/<therapeutic-area>/`. All of it is synthetic.
