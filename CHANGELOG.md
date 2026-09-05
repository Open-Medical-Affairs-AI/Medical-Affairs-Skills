# Changelog

## 0.2.0 candidate — October workshop upgrade

- Reconciled the expanded synthetic packs with the current 52-skill library.
- Added ten skills, including four MSL workflows for pre-call planning, HCP
  discovery and access, post-call follow-up and administrative operations.
- Added 16 workshop missions, three self-contained starter bundles, a connected
  fictional organization, change cards and a two-hour facilitator runbook.
- Added a public evidence gateway, transcript import, a read-only database helper
  and a traceable MSL preparation helper; repaired API JSON and error handling.
- Strengthened source verification, action boundaries and synthetic-data handling
  in the foundations, orchestrator and selected scientific workflows.
- Added nine curated public bibliographic examples, enterprise connection guidance,
  owner governance instructions, CODEOWNERS and workshop CI checks.
- Rebuilt the beginner README with a generated infographic and updated skill menu.
- Recorded engineering checks and remaining rehearsal steps in docs/validation.md.

## Unreleased

- Expanded each workshop therapeutic-area pack from 10 to 32 synthetic files,
  adding cross-functional inputs for all 48 skills, including safety and
  Medical Information intake, account planning, metrics, advisory boards, IIS,
  RWE, payer/HTA, guideline and launch readiness, MLR, publications, structured
  evidence and patient-level analysis data.
- Added a skill-to-data coverage catalogue with suggested jobs, testable
  tensions and three cross-functional capstones.

All notable changes to this project are recorded here. Skills are versioned
individually in their `metadata.version` field; this file records what changed
across the library as a whole.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

- **Four new skills (48 → 52):** `consulting-grade-design` (the shared visual
  language), `library-menu` (capability overview + menu-card generator),
  `executive-briefing` (leadership-ready distillation), and
  `literature-surveillance` (ongoing delta-based watch).
- **Consulting-grade design applied across every output skill** — palette,
  accent bars, kicker lines, banded tables in the deck builder; "The look"
  sections in pdf-generation, interactive-html-report, visual-abstract,
  congress-abstract-and-poster, diagram-and-schema, data-visualization-for-medical.
- **Deck builder:** banded data tables with ink headers, teal accent bars,
  design-statement kickers, optional full-bleed title image with scrim.
- **Exemplar:** `examples/advisory-board-deck/` — a complete synthetic 13-slide
  deck with four themed matplotlib figures and a rebuild script.
- **README:** rewritten with the generated menu-card graphic and exemplar
  walkthrough; orchestrator routing covers the four new skills.


## [Unreleased]

### Added

- Six workflow skills closing the remaining Medical Affairs coverage gaps:
  `medical-education-program`, `real-world-evidence-design`,
  `promotional-material-medical-review`, `field-medical-planning`,
  `integrated-evidence-plan`, `medical-affairs-metrics`.
- Eight further workflow skills: `advisory-board-design`, `scientific-platform`,
  `payer-value-dossier`, `investigator-initiated-study-review`,
  `guideline-engagement`, `competitive-intelligence`,
  `launch-medical-readiness`, `safety-communication`.
- Seven content skills: `document-ingestion`, `spreadsheet-analysis`,
  `pdf-generation`, `visual-abstract`, `diagram-and-schema`,
  `interactive-html-report`, `medical-correspondence`.
- `capability-detection` and a four-tier degradation ladder every content skill
  follows, with `scripts/selftest_fallbacks.py` proving in CI — in an
  environment with no document libraries installed — that generators degrade
  visibly instead of failing, and that citations, study designs, denominators,
  confidence intervals, safety data and the draft marking all survive.
- `metadata.suggests`: dependencies a job may reach into, named but not loaded,
  distinct from `metadata.requires` which is what a skill cannot run without.

### Changed

- The always-loaded core is now staged. `medical-affairs-foundations` loads on
  every job; `evidence-appraisal`, `citation-integrity` and
  `deliverable-quality-review` load when the job reaches them. Previously all
  four loaded on every task regardless of relevance.
- `metadata.requires` capped at three entries, with the rest moved to
  `suggests`. Typical dependency closures fell from 8–10 skills to 4–5.
- `medical-affairs-foundations` 257 → 189 lines and `evidence-appraisal`
  276 → 169, with the detail moved into `references/` rather than deleted.
- Descriptions rewritten against a 700-character ceiling (was 1400); average
  fell from 810 to 584 characters. The enumerated trigger phrasings moved into
  the orchestrator's routing table, which is read once per routed job rather
  than sitting in context on every request.
- `scripts/validate_skills.py` enforces per-tier body-length budgets in place of
  a single flat limit that no skill came near.
- `pubmed-search` and `clinical-trials-search` now document a screen-then-fetch
  retrieval pattern. Fifty PubMed records as a table cost a few hundred tokens;
  the same fifty with abstracts cost roughly thirty thousand.


- Initial public release of the Medical Affairs Agent Skills library.
- Apache-2.0 licensing, third-party attribution, and conditions of use.
- `scripts/validate_skills.py` and `scripts/build_index.py`, with CI enforcement
  from the first commit.
- 52 skills across six tiers: orchestrator, foundation, reasoning primitives,
  data and search, workflows, and content generation.
- Working clients for PubMed E-utilities, ClinicalTrials.gov v2, openFDA, and
  citation verification against CrossRef and OpenAlex. No third-party Python
  packages required; offline fixtures and a `--live` mode for both.
- Document and figure generation: `.pptx` decks and posters, `.docx`
  manuscripts, and clinical figures (Kaplan-Meier, forest, waterfall, adverse
  event) that enforce graphical integrity rules.
- `house-rules/` override layer, one file per skill.
- Workshop materials: facilitator guide, participant quickstart, six mission
  cards, a long-horizon Round 3 exercise, and a scorecard.
- Synthetic data packs in three therapeutic areas, generated from
  `workshop/data/generate.py`.
- `AGENTS.md` as the agent-neutral entry point, and `SKILLS-INDEX.md` generated
  from frontmatter.
- Documentation: skill authoring guide, orchestration, API setup, and guidance
  on adapting third-party skills.

### Known limitations

- The API fixtures are hand-built to published response schemas rather than
  recorded from live responses; the authoring environment had no egress to
  NCBI, ClinicalTrials.gov or openFDA. Run
  `python3 scripts/selftest_apis.py --live` from a connected network to confirm
  the upstream contracts.
- No Europe PMC fallback, so PubMed has no alternative source if NCBI is
  unreachable.
