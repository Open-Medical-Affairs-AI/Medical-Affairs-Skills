# How Orchestration Works

Why an agent pointed at this repository can be handed a job rather than a skill
name, and what happens next.

---

## The two entry points, and why there are two

**`SKILL.md` frontmatter** is the Agent Skills discovery mechanism. Claude Code
and Claude.ai read the `name` and `description` of every skill and decide what
to load. Nothing needs to be said to make this work.

**`AGENTS.md`** is for everything else. Grok, ChatGPT, Copilot and Cursor do not
read SKILL.md frontmatter. They read plain markdown at the repository root, and
`AGENTS.md` is the emerging convention for that.

Both describe the same library. `scripts/build_index.py` generates
`SKILLS-INDEX.md` from the frontmatter, and `validate_skills.py` fails CI if the
committed index is stale — so the two views cannot drift apart. That is the only
mechanism preventing the classic failure where the human-readable catalogue
slowly stops matching reality.

---

## Routing

`skills/medical-affairs-orchestrator/SKILL.md` holds a routing table mapping
job-shaped requests to workflow skills. It routes on **what the person wants to
end up with**, not on the words they used — "brief me before this call", "what
should I know about Dr Okafor" and "prepare for Thursday" all land on
`kol-engagement-brief`.

Three rules make routing behave:

1. **Never ask the user which skill to use.** They should not need to know the
   library has skills at all.
2. **One clarifying question, at most**, and only when the answer changes the
   deliverable. "Help with the congress" could be preparation or readout; that
   is worth one question. Anything else is an interview, and interviews are how
   agents avoid starting.
3. **When nothing fits, say so** and work with the foundation skills, rather
   than forcing a poor match.

---

## Dependency resolution

Each skill declares what it builds on:

```yaml
metadata:
  requires: [medical-affairs-foundations, evidence-appraisal, citation-integrity]
```

The orchestrator loads the workflow plus everything it declares. The validator
checks every declared dependency resolves to a real skill and that the graph is
acyclic — a cycle would send an agent into a loading loop it cannot escape.

Four skills are loaded for **every** job regardless of routing:
`medical-affairs-foundations`, `evidence-appraisal`, `citation-integrity`,
`deliverable-quality-review`. They carry the boundaries that make the output
usable at all.

---

## The six-stage contract

```
0 · ORIENT     Identify the job. Load foundations + workflow + dependencies
               + house-rules/<skill>.md
1 · INVENTORY  What you have; what is MISSING and how that limits the answer
2 · RETRIEVE   Fill gaps from PubMed / ClinicalTrials.gov / openFDA, recording
               every query verbatim with its date
3 · ANALYSE    Run the workflow's reasoning ladder
4 · CHALLENGE  Red-team your own conclusions BEFORE showing anything
5 · DELIVER    Artefact + provenance appendix
```

**Stages 1 and 4 are the entire difference**, and they are precisely the two a
generic agent skips. An agent that answers immediately with what it has, and
presents the result as complete, is behaving like a chatbot. One that says what
it is missing before answering and argues against itself before delivering is
behaving like a colleague.

The agent is instructed to **announce** the stages. This is not ceremony: a
human who can see which stages ran can tell whether to trust the output, and can
redirect at a boundary rather than after everything is built.

---

## The override layer

Before producing anything, the agent reads `house-rules/<skill-name>.md` for
every skill it loaded. Rules there belong to the adopting organisation and
**beat** the defaults.

Why this design rather than configuration:

- **No forking.** An organisation encodes its SOPs and still receives upstream
  improvements.
- **Plain markdown.** The people with the expertise are not developers, and a
  YAML schema would exclude exactly the contributors who matter most.
- **Reviewable.** A house rule is a sentence a medical director can read and
  approve.
- **Enforced.** The validator requires a file per skill with an edit marker, so
  the hook cannot silently disappear.

---

## Long-horizon objectives

Some jobs need several workflows chained — an advisory board, a launch readiness
review, a full evidence strategy. The orchestrator decomposes these, states the
chain before starting, and reports at each boundary.

The instruction that matters most here: **where a stage produces nothing useful,
say so and continue.** "The gap analysis found no unanswered question that would
justify an advisory board on this topic" is a legitimate and valuable finding,
and it is exactly the conclusion an agent optimising for apparent productivity
will never reach on its own.

---

## Extending the routing

Adding a skill means adding a row to the orchestrator's routing table and
regenerating the index:

```bash
python3 scripts/build_index.py
python3 scripts/validate_skills.py
```

If two skills have overlapping descriptions they compete for selection and
**both** trigger less reliably. This is the most common cause of a skill that
mysteriously stops firing after someone adds a neighbour. The PR template asks
what a skill should *not* trigger on for exactly this reason.
