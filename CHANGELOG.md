# Changelog

All notable changes to this project are recorded here. Skills are versioned
individually in their `metadata.version` field; this file records what changed
across the library as a whole.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial public release of the Medical Affairs Agent Skills library.
- Apache-2.0 licensing, third-party attribution, and conditions of use.
- `scripts/validate_skills.py` and `scripts/build_index.py`, with CI enforcement
  from the first commit.
- 26 skills across six tiers: orchestrator, foundation, reasoning primitives,
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
