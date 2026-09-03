# Changelog

All notable changes to this project are recorded here. Skills are versioned
individually in their `metadata.version` field; this file records what changed
across the library as a whole.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
