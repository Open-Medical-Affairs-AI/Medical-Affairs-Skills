# Authoring Open-Source Agent Skills

What we learned building this library, written for anyone open-sourcing skills
for a regulated industry. Most of it applies to any domain; the last section is
specific to healthcare and life sciences.

---

## Part 1 — What makes a skill get used

### 1. The description is the entire product surface

It is the only text an agent sees before deciding whether to load your skill.
Everything else — the careful reasoning, the reference files, the scripts — is
inert if the description does not trigger.

Write **what it does** *and* **the concrete situations that should trigger it**.
Name the phrases a real person would type, including the casual ones.

**Weak:** "Helps with medical writing."

**Strong:** "Draft, structure and prepare a scientific manuscript for journal
submission… Use when asked to write or draft a paper, prepare a manuscript, pick
a target journal, write a cover letter, or respond to peer reviewers."

Agents systematically **under**-trigger skills — they handle things themselves
when they could have consulted something better. Be slightly pushy. Name the
adjacent cases. State when it should *not* trigger if there is a near-miss skill
that would compete.

### 2. One skill = one job with a named deliverable

"Medical affairs helper" will never trigger, because no agent can work out when
it applies. "Prepare a KOL engagement brief" triggers reliably.

If you cannot name what comes out at the end, you have a topic rather than a
job — and it probably belongs inside an existing skill.

Our validator enforces this: skills in the workflow and content tiers must
declare `metadata.produces`.

### 3. Progressive disclosure, seriously applied

Three levels:

1. **Frontmatter** — always in context. Roughly 100 words.
2. **Body** — in context whenever the skill triggers. Under ~500 lines.
3. **`references/`** — loaded only when needed. Unbounded.

A bloated body does not make the agent smarter. It crowds out the actual task
and degrades reasoning on everything else in context. When a body approaches the
limit, that is a signal to add a layer of hierarchy, not to compress the prose.

Point at reference files explicitly and say *when* to read them: "Depth on
seriousness criteria and reporting timelines: `references/adverse-events.md`."

### 4. Explain why; do not stack MUSTs

Capitalised absolutes make models brittle and literal-minded. Reasoning
generalises to the cases you did not anticipate; commands do not.

**Brittle:** "ALWAYS STATE THE APPROVAL STATUS."

**Better:** "State the approval status because a reader who assumes an
indication is approved may act on it."

Reserve hard prohibitions for genuine bright lines — safety reporting,
fabricated citations, promotional claims. If everything is a MUST, nothing is.

### 5. Assume an expert reader

Skills for professionals should not explain the profession. Do not define what
an MSL is. Do explain the thing that is easy to get wrong: that serious and
severe mean different things, that a per-protocol analysis is the *less*
conservative choice in a non-inferiority trial, that PFS depends on how often
you scan.

The value is in the failure modes, not the overview.

### 6. Bundle scripts for anything deterministic

If the agent would otherwise write the same helper every time, ship it. We
noticed this pattern and moved API access, citation verification, document
generation and figure rendering into scripts.

Two further benefits worth designing for:

**Scripts can enforce what prose only requests.** Our deck builder refuses to
render a data slide without a citation. Our Kaplan-Meier renderer will not
produce a curve without a numbers-at-risk row. A rule in a script is a rule; a
rule in prose is a suggestion.

**Scripts make failures legible.** When a script exits non-zero with an
explanation, the agent and the human both learn something. When prose is
ignored, nobody finds out.

### 7. Self-contained directories

Someone will copy one skill into their own repository. Make that work.

We deliberately duplicate a small HTTP helper across four API clients rather
than sharing a library. DRY is the wrong optimisation here: the strongest
predictor of adoption is that a directory works when you move it.

---

## Part 2 — What makes a library maintainable

### 8. Ship a validator and CI from the first commit

We wrote `validate_skills.py` before the first skill, so it constrained
everything written afterwards. Retrofitting a validator to 48 skills would have
been a week of cleanup.

Ours checks: frontmatter parses; `name` matches the directory; description
length and trigger-phrase presence; declared dependencies resolve and the graph
is acyclic; relative links and bundled-script paths exist; body length against
progressive-disclosure limits; every skill has an override file; every sample
data file carries its synthetic-data banner; and the generated index matches the
frontmatter.

This is what turns a prompt collection into infrastructure, and what lets you
accept outside contributions without reading every line.

### 9. Generate anything that can drift

`SKILLS-INDEX.md` is generated from frontmatter and CI fails if the committed
copy is stale. Two hand-maintained descriptions of the same thing will diverge,
and a stale index is worse than no index because agents route off it.

### 10. Version each skill, not just the library

Downstream teams pin behaviour. A silent edit that changes output is a broken
contract. Semver per skill in `metadata.version`, plus a changelog for anything
a user would notice.

### 11. Test the guardrails in both directions

For every rule a script enforces, we tested that clean input passes **and** that
deliberately non-compliant input is blocked with a useful message. A guardrail
you have only tested in the passing direction is not known to work.

### 12. Make offline testing possible

Our API clients ship recorded fixtures and a `--fixtures` mode, so CI tests
parsing, pagination, empty results and error paths with no network. A separate
`--live` mode catches upstream schema changes and runs only on manual dispatch.

This matters more than it sounds: if a third-party outage turns your CI red,
people stop trusting CI.

### 13. Build an override layer

This is the difference between a repository people use and one they fork once
and abandon.

Every skill reads `house-rules/<skill-name>.md` before producing anything. Rules
there beat the defaults. An adopting organisation encodes its SOPs, terminology
and thresholds without forking — and keeps receiving upstream improvements.

Seed each file with worked examples and an explicit edit marker, so the first
contribution is a two-minute edit rather than a blank page.

### 14. Contribution ergonomics

A skill template, issue forms, and a PR checklist that asks the question people
forget: **"What should this trigger on, and what should it deliberately *not*
trigger on?"** Overlapping descriptions are the most common cause of a skill
that mysteriously stops firing.

---

## Part 3 — Licensing and provenance

### 15. Licence for the adopter's lawyer, not for you

We chose **Apache-2.0** over MIT specifically because of the explicit patent
grant. In pharmaceutical companies the binding constraint on adoption is legal
approval, not technical merit, and Apache-2.0 is the licence conservative legal
teams approve fastest.

Optimise for the person who has to say yes.

### 16. Audit licences per file, not per repository

This one cost us a design decision and is worth passing on.

We evaluated an MIT-licensed skills repository for material to adapt. Its
`docx` and `pptx` skills turned out to be **Anthropic proprietary**, vendored in
with frontmatter reading `license: Proprietary`. A repository-level licence
badge tells you nothing about the licence of a specific file.

Check per-file frontmatter before vendoring anything.

### 17. Attribute derived work explicitly

`THIRD-PARTY-NOTICES.md`, naming each derived skill and what was derived. We
took architecture rather than text and said so, skill by skill.

In a regulated industry, sloppy provenance is not a style problem — it is a
blocker. A compliance reviewer will ask where something came from, and
"somewhere on GitHub" ends the conversation.

### 18. Do not redistribute licensed content

Our terminology skill teaches correct use of MedDRA, SNOMED CT and the WHO Drug
Dictionary and ships **none** of their content, because redistribution requires
a licence we do not hold and adopters may not either.

Handing someone a licensing liability they did not ask for is a good way to get
your repository banned internally.

---

## Part 4 — Regulated domains

### 19. Write the compliance boundary into the skill

Not into a separate document nobody reads. Every skill that touches field notes,
KOL interactions or medical information carries adverse-event and product-
complaint detection, and states the non-promotional boundary inline.

Omitting safety escalation is the fastest way to get a healthcare skill library
banned by a compliance function — and rightly so.

### 20. Be explicit about what the tool is not

`DISCLAIMER.md` states plainly that this is not a medical device, not clinical
decision support, not a validated GxP system, and discharges no
pharmacovigilance obligation. It says the reporting clock starts when
information reaches a human, regardless of what the agent flagged.

State the negative space. It is what lets a risk assessor approve the positive.

### 21. Make the tool disclaim its own authority

Our scripts refuse to describe their output as *compliant*, *approved*,
*validated*, or *ready to submit*, and say why: those are determinations made by
people with accountability.

An agent that overstates its own standing is more dangerous than one that
underperforms, because the overstatement is what causes a human to skip the
check.

### 22. Mandatory draft marking

Every deliverable carries **DRAFT — REQUIRES QUALIFIED MEDICAL REVIEW**, and the
skills refuse to remove it. The reviewer removes it once they have reviewed.

The reason is specific: a well-formatted document signals to a reader that
somebody already checked it. Formatting quality is exactly what makes unreviewed
AI output dangerous, so the marking has to survive the formatting.

### 23. Show provenance in the output

Every deliverable ends with the searches run, the sources used, and what could
not be determined. In a regulated industry an unauditable deliverable is an
unusable one — and the "could not determine" section is the most valuable part,
because a named gap is one somebody can close.

### 24. Synthetic data only, enforced mechanically

All our sample data is fictional and every file carries a banner the validator
checks for. Do not rely on a convention; make the check fail.

---

## The short version

If you remember five things:

1. **The description is the product.** Everything else is inert without it.
2. **Progressive disclosure.** Body under 500 lines, depth in `references/`.
3. **Explain why.** Reasoning generalises; MUSTs make models brittle.
4. **Validator and CI from commit one.** It is what makes contribution safe.
5. **An override layer.** Or people fork you once and never come back.

And for regulated domains, a sixth: **write the safety boundary into the skill
itself**, not into a document beside it.
