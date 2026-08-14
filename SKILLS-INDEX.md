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


**0 skills.**


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
