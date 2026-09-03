---
name: library-menu
description: >-
  Explain what this entire library can do and render the visual menu card
  that shows it — every skill grouped by the job it serves, as prose, a
  table or an SVG/PNG infographic for a README, a slide or a stakeholder
  walkthrough. Use when someone asks "what can you do", "what's in this
  library", "show me the skills", wants a capability overview for
  leadership, or needs the menu-card graphic regenerated after skills are
  added or removed.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: content
  maturity: beta
  requires:
    - medical-affairs-foundations
  suggests:
    - medical-affairs-orchestrator
    - consulting-grade-design
  produces: Library capability overview and menu-card infographic (SVG/PNG)
  python: [matplotlib>=3.7]
---

# Library Menu

Someone wants to know what this library can do — a new user, a leadership
audience deciding whether to adopt it, or an agent orienting itself. The
answer is organised by **job**, never by file listing, because nobody hires a
library for its directory structure.

## The menu, by job

**"I have material — tell me what it means."**
Field notes and MSL records (`field-insight-synthesis`), any document
(`document-ingestion`), spreadsheets and trackers (`spreadsheet-analysis`),
a body of evidence (`evidence-synthesis`), one study (`evidence-appraisal`).

**"Prepare me."**
A KOL meeting (`kol-engagement-brief`), a congress before or after
(`congress-intelligence`), a competitor readout (`competitive-intelligence`),
a launch or readiness gate (`launch-medical-readiness`).

**"Build the plan."**
Medical plan (`medical-strategy-plan`), integrated evidence plan
(`integrated-evidence-plan`), evidence gaps and what to fund
(`evidence-gap-analysis`), publications (`scientific-communication-strategy`),
field deployment (`field-medical-planning`), education programmes
(`medical-education-program`), metrics (`medical-affairs-metrics`).

**"Design the study / event."**
RWE study (`real-world-evidence-design`), advisory board
(`advisory-board-design`), IIS review (`investigator-initiated-study-review`),
guideline engagement (`guideline-engagement`).

**"Answer the question."**
Medical information response (`medical-information-response`), payer and HTA
evidence (`payer-value-dossier`), safety communication
(`safety-communication`), label questions (`regulatory-label-intelligence`).

**"Produce the artefact."**
Deck (`medical-slide-deck`), manuscript (`scientific-manuscript`), abstract
and poster (`congress-abstract-and-poster`), executive briefing
(`executive-briefing`), lay summary (`plain-language-summary`), visual
abstract (`visual-abstract`), figures (`data-visualization-for-medical`),
HTML dashboard (`interactive-html-report`), PDF (`pdf-generation`),
correspondence (`medical-correspondence`), the look of all of it
(`consulting-grade-design`).

**"Keep watch."**
Literature surveillance (`literature-surveillance`), competitor monitoring
(`competitive-intelligence`), FAERS and label movement
(`regulatory-label-intelligence`).

**Live retrieval underneath all of it:** `pubmed-search`,
`clinical-trials-search`, `regulatory-label-intelligence`,
`citation-integrity` — real APIs, no keys, every citation verified.

When asked in conversation, answer from this map at whatever depth the
audience needs; the generated `SKILLS-INDEX.md` carries the authoritative
one-line-per-skill detail if more is wanted.

## The menu card

`scripts/menu_card.py` reads every skill's frontmatter and renders the
one-page infographic — the library as a menu, grouped as above, in the
`consulting-grade-design` palette:

```bash
python3 scripts/menu_card.py --out assets/menu-card.svg   # also writes .png
```

Regenerate it whenever a skill is added, renamed or removed — a stale menu
card misroutes people exactly the way a stale index misroutes agents. The
README embeds the PNG from the repository-level assets directory; CI does
not check freshness, so regeneration is part of the skill-authoring
checklist.

The card states the library version date and the skill count it was built
from. If the count in the card and the count in `SKILLS-INDEX.md` disagree,
the card is stale — say so and regenerate rather than presenting it.

## Presenting the library to leadership

Three points carry the adoption argument, in this order:

1. **It encodes judgement, not formatting.** Stage 1 names what is missing
   before answering; stage 4 argues against its own conclusion. That is what
   distinguishes it from a general-purpose agent with a template.
2. **The compliance floor is mechanical.** Citations are verified against
   live sources, data slides cannot render without them, safety findings
   surface first, and the draft marking survives until a qualified reviewer
   removes it.
3. **Adoption does not mean forking.** House rules override defaults per
   organisation; upstream improvements keep flowing.

## Before you finish

Read `house-rules/library-menu.md`. An adopting organisation may have
disabled skills, added private ones, or have a preferred grouping — their
menu beats this one.
