# Contributing

This library exists because Medical Affairs expertise is trapped in people's
heads and in SOPs that no agent can read. Every good contribution moves a piece
of that expertise into something an agent can execute.

You do not need to be a developer to contribute. If you know what an experienced
MSL checks before a KOL meeting, or why a particular publication plan failed, or
what a reviewer always sends back — that knowledge is the scarce input here. The
markdown is the easy part.

---

## Ways to contribute, easiest first

1. **Report what went wrong.** Open an issue with the prompt, the output, and
   what an experienced person would have done differently. This is genuinely the
   most valuable contribution and takes ten minutes.
2. **Add a house rule.** If your organisation's practice differs from a default,
   the fix is often a rule in `house-rules/`, not a code change. Contributing the
   *generalisable* ones back helps everyone.
3. **Improve a skill.** Sharpen the reasoning, add a failure mode to a checklist,
   fix an outdated standard reference.
4. **Add a skill.** A new recurring MA job that nothing here covers.

## Before you open a PR

Run this. It is the same thing CI runs.

```bash
pip install pyyaml
python3 scripts/build_index.py      # regenerate the index if you touched frontmatter
python3 scripts/validate_skills.py  # structural checks
python3 scripts/selftest_apis.py    # offline API client tests
```

---

## Adding a skill

### 1. Is it actually a skill?

A skill is **one job with a named deliverable**. Good: "prepare a KOL engagement
brief". Bad: "medical affairs helper" — an agent will never work out when to load
that, so it will never load it.

If your idea is a *rule* ("always state approval status when discussing an
unapproved use"), it belongs in an existing skill or in `house-rules/`, not in a
new skill.

Check `SKILLS-INDEX.md` first. If something close exists, extending it is usually
better than adding a near-duplicate: two skills with overlapping descriptions
compete for selection and both trigger less reliably.

### 2. Structure

```
skills/your-skill-name/
├── SKILL.md            required
├── references/         depth that is only sometimes needed
├── scripts/            deterministic work better done in code than in tokens
└── assets/             templates and files that end up in the output
```

Keep each skill directory **self-contained**. Someone will copy one skill into
their own repo, and it should work when they do. That is worth a little
duplication between skills.

### 3. Frontmatter

```yaml
---
name: your-skill-name          # must equal the directory name
description: >-
  What it does, and — crucially — the concrete situations that should trigger
  it. This is the only thing an agent sees when deciding whether to load the
  skill. 120–1400 characters.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"             # semver; bump it when behaviour changes
  tier: workflow               # foundation|primitive|data|workflow|content|orchestrator
  maturity: beta               # stable|beta|experimental
  requires: [medical-affairs-foundations, citation-integrity]
  produces: KOL engagement brief    # required for workflow and content tiers
  network: [eutils.ncbi.nlm.nih.gov]  # omit if the skill works offline
  python: [python-docx>=1.1]          # omit if no third-party packages needed
---
```

### 4. Writing the body

**The description is the product surface.** It is the only text an agent reads
before deciding whether to load you. Write what the skill does *and* when to use
it. Agents systematically under-trigger skills, so be concrete and slightly
pushy about the trigger conditions. Name the phrases a real user would type.

**Respect progressive disclosure.** Body under ~500 lines. Anything deeper goes
in `references/` with a clear pointer telling the agent when to go read it. A
bloated body does not make the agent smarter; it crowds out the actual task.

**Explain why, do not stack MUSTs.** Modern models follow reasoning better than
they follow shouted absolutes, and reasoning generalises to the cases you did not
anticipate. Write "state the approval status because a reader who assumes an
indication is approved may act on it" rather than "ALWAYS STATE APPROVAL STATUS".
Reserve hard prohibitions for the genuinely bright lines — safety reporting,
fabricated citations, promotional claims.

**Assume an experienced reader.** These skills are for people who have run
advisory boards and been through MLR review a hundred times. Do not explain what
an MSL is. Do explain the thing that is easy to get wrong.

**Write the compliance boundary in.** Any skill touching field notes, KOL
interactions, or medical information must handle adverse event and product
complaint detection, and must state the non-promotional boundary. See
`skills/medical-affairs-foundations/SKILL.md` for the house pattern.

### 5. Register it

```bash
python3 scripts/build_index.py                 # regenerates SKILLS-INDEX.md
touch house-rules/your-skill-name.md           # then add the edit marker
python3 scripts/validate_skills.py
```

Every skill needs a `house-rules/<name>.md` file containing the
`## YOUR RULES — ADD BELOW THIS LINE` marker. The validator enforces this,
because the override layer is what lets an organisation adopt this library
without forking it.

---

## Sample data rules

All data in `workshop/data/` must be **fictional**: fictional company, fictional
products, fictional KOLs, fictional institutions. Every file carries a
`SYNTHETIC DATA` banner in its first eight lines and the validator fails without
it.

Real published trials, real approved drugs, and real disease science may be
referenced — that is public literature. What must never appear is a real named
individual's opinions or interaction history, or anything resembling
company-confidential material.

If you are contributing sample data, ask yourself: *if this leaked, would anyone
care?* If the answer is anything but a flat no, do not contribute it.

---

## Versioning

Each skill carries its own `metadata.version`. Downstream teams pin behaviour, so
a silent edit that changes output is a broken contract.

- **Patch** (1.0.0 → 1.0.1) — typos, clarifications, no behaviour change.
- **Minor** (1.0.0 → 1.1.0) — new capability, additional checks, same contract.
- **Major** (1.0.0 → 2.0.0) — changed deliverable structure, removed behaviour,
  or a different set of required inputs.

Record anything a user would notice in `CHANGELOG.md`.

---

## Licensing and provenance

Contributions are accepted under **Apache-2.0**. By opening a PR you confirm you
have the right to contribute the content and are licensing it under those terms.

If your contribution is derived from other work, say so in the PR and add it to
`THIRD-PARTY-NOTICES.md`. Check the licence of the **specific file** you are
deriving from, not the repository badge — we found proprietary files sitting
inside an MIT-labelled repository while building this one. It happens more than
you would think.

Do not contribute:

- Licensed terminology content (MedDRA, SNOMED CT, WHO Drug Dictionary). Skills
  may *teach* their use; they may not carry their content.
- Copyrighted journal text beyond fair quotation.
- Anything from your employer that you do not have clear permission to release.

---

## Code of conduct and safety

See `CODE_OF_CONDUCT.md`. Safety reports — fabricated citations presented as
real, promotional drift, a missed adverse event pathway — take priority over
features. Tag them `[safety]` or follow `SECURITY.md` if the report itself should
not be public.
