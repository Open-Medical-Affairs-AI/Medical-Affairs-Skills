# Facilitator Guide

## The one thing to get right

Participants must never see YAML, skill architecture, MCP, or the word
"orchestrator" until Round 2. If you open with "today we're learning about
SKILL.md", you lose half the room in the first ten minutes.

Open with this instead:

> **Today you're going to give an AI agent a job, not a prompt.**

Everything else follows.

---

## Shape of the day

| | Round | Time | What happens |
|---|---|---|---|
| 1 | **Give the agent a job** | 30 min | Teams run their mission cold. No instruction on how. |
| — | **The reveal** | 15 min | *"How did it know how to do all that?"* |
| 2 | **Teach the agent** | 30 min | Each team adds 3–5 rules to one house-rules file, reruns, compares. |
| 3 | **Make it work** | 45–60 min | An objective, not a task. The agent has to plan. |
| — | **Show and tell** | 30 min | 5 min per team, then voting. |

Total: about three hours with breaks. It compresses to two by shortening
Round 3, and does not compress below that — Round 3 is where long-horizon
agency becomes tangible, and cutting it leaves people thinking this was a
prompting workshop.

---

## Before the day

- [ ] Each team has the repository available to their agent — cloned locally,
      or the URL if their agent can browse.
- [ ] Each team knows which mission and which therapeutic area they have.
- [ ] Someone has actually run one mission end to end. Do not skip this.
- [ ] Decide whether teams need literature retrieval. If yes,
      `eutils.ncbi.nlm.nih.gov`, `clinicaltrials.gov` and `api.fda.gov` must be
      reachable from their network — see [../docs/api-setup.md](../docs/api-setup.md).
      **Check this in advance.** Corporate networks block them more often than
      you would expect, and discovering it at 09:05 costs you Round 1.
- [ ] Print the mission cards. One per team, on paper. It keeps people out of
      the repository and in the problem.

**Six teams, one mission each.** Do not give two teams the same mission — the
breadth across the room is what makes the show-and-tell worth sitting through.

Teams pick their therapeutic area from `data/`: oncology (multiple myeloma),
immunology (atopic dermatitis), or cardiometabolic (obesity). The missions are
TA-agnostic; the data packs are not.

For workshops focused on a specific function, or for a second day beyond the
six introductory missions, use the expanded 32-file packs and the skill-by-skill
jobs in [`data/SKILL-COVERAGE.md`](data/SKILL-COVERAGE.md). The same file schema
is available in every therapeutic area, which makes cross-team comparisons
possible without giving teams identical clinical problems.

---

## Round 1 — Give the agent a job (30 min)

Hand out the mission cards. Say only:

> Your agent has everything it needs. Give it the mission. Don't tell it how.

Then **stop talking**. The instinct to help is strong and it ruins the exercise.

### What you will see, and what to do about it

**"It's asking us questions."** Good — that's Stage 1 working. It is telling
you what's missing before it answers. Let them answer or not; both are
informative.

**"It just started listing things."** Ask them what they asked for. Usually
they asked for a summary and got one. Have them ask for the decision instead.

**"It made something up."** Excellent. Note it down for the awards. Then have
them run the citation verifier on it:
`python3 skills/citation-integrity/scripts/verify_citations.py --file <their output>`

**Teams that finish in 12 minutes** have got a shallow answer. Give them the
follow-up on their mission card — every card has one.

### The moment to watch for

Around minute 20 someone will say a version of *"it found something we
missed"* — usually an adverse event buried in the field notes, or a
contradiction between two data sources. **Stop the room and have them read it
out.** That moment does more for adoption than any slide you could show.

---

## The reveal (15 min)

Now, and not before, ask:

> **How did it know how to do all of that?**

Let them guess. Then show them:

```
Your agent
   │
   ├── Medical Affairs principles ....... compliance, safety, the boundaries
   ├── Evidence appraisal ............... what a study design can support
   ├── Citation integrity ............... never cite what you haven't retrieved
   ├── Insight generation ............... observation → insight → action
   ├── Strategic analysis ............... so-what laddering, trade-offs
   └── Output quality ................... argue against yourself before delivering
```

Open **one** skill file — `skills/field-insight-synthesis/SKILL.md` works well —
and scroll it. Do not explain the frontmatter. The point to make is:

> This is just written-down expertise. Somebody's judgement, in a file. That's
> all a skill is.

Then the punchline that sets up Round 2:

> Which means **you** can write one.

---

## Round 2 — Teach the agent (30 min)

The mechanism is deliberately trivial:

```
house-rules/<the-skill-your-team-used>.md
```

Each file already contains seeded examples and a marker:

```
## YOUR RULES — ADD BELOW THIS LINE
```

The instruction:

> **What does an experienced person on your team know that this agent doesn't?**
> Write down three to five things. Then run the same mission again.

### Making the rules good

Teams will write vague rules first — "be more concise", "focus on what matters".
Push them toward specificity **and** a reason. Rules with reasons generalise;
rules without them produce brittle literal-mindedness.

Weak: *"Be careful with safety data."*

Strong: *"Never give an adverse event rate from a single-arm trial without the
denominator and median follow-up alongside it. Short follow-up understates
cumulative toxicity, and our reviewers send this back every time."*

The best source is the correction their medical reviewers make repeatedly. If
the same comment comes back on every document, that comment is a house rule
nobody has written down.

### The comparison

Have them run the mission again and diff the output. The progression to name
explicitly:

```
Generic agent  →  Medical Affairs agent  →  YOUR Medical Affairs agent
```

**If a team's output doesn't change**, their rules were too vague or too
consistent with what the skill already said. That is a useful failure — have
them say so, and try a rule that genuinely contradicts a default.

---

## Round 3 — Make it work (45–60 min)

Switch from task to objective. See
[round-3-longhorizon.md](round-3-longhorizon.md).

> We have an advisory board in three weeks. Determine the five most important
> scientific questions we need to explore, and prepare the team's briefing
> materials.

Nobody has told the agent which workflows to run. It has to decompose the
objective itself, and that decomposition — announced before it starts — is the
thing you want people to see.

**What to look for:** does it state a plan before working? Does it report at
stage boundaries so a human could redirect? Does it ever say "this stage found
nothing useful"? That last one is rare and worth pointing out — an agent willing
to report a null result is more trustworthy than one that always finds five
things.

**When a team's agent goes off the rails**, let it. Then ask where a human
should have intervened. That is the governance conversation, and it lands far
better as a debrief than as a policy slide.

---

## Show and tell (30 min)

Five minutes per team, five headings:

1. **The job** — what did you give it?
2. **The skills** — what expertise did you teach it?
3. **The work** — what did it do on its own?
4. **The result** — was it actually useful?
5. **The failure** — where did it still need a human?

**Insist on point 5.** A team with nothing to say there did not look hard
enough. Ask the room to help them find it.

Then vote — see [scorecard.md](scorecard.md).

🏆 Best Agent · 🧠 Best Medical Affairs Skill · ⚡ Biggest Time Saver ·
🤯 Most Surprising Result · 🚨 **Most Dangerous Agent Mistake**

That last award is not a joke category. It is the one that turns the day from
an AI demo into a governance conversation, and it should be presented last and
taken seriously.

---

## Closing

The progression to leave on the screen:

```
PROMPT     "Summarise these papers."
    ↓
TASK       "Analyse the evidence."
    ↓
WORKFLOW   "Determine what changed and what it means."
    ↓
AGENT      "Here is the objective. Work out what's needed.
            Execute it. Check yourself. Bring me the result."
```

And the one thing to say last:

> Everything you wrote in `house-rules/` today is yours. It is your expertise,
> in a form an agent can execute. That is the asset — not the model.

---

## Things that go wrong

| Problem | Fix |
|---|---|
| Network blocks PubMed | Check the day before. Missions work without it — the data packs are self-contained — but say so up front rather than letting teams hit errors. |
| A team's agent has no file access | Have them paste the mission and the data pack contents directly. Degrades the experience but does not break it. |
| Someone uploads real company data | Stop it immediately. Everything in `data/` is synthetic and must stay that way. Say this at the start, not when it happens. |
| A team finishes Round 1 in 10 minutes | They got a shallow answer. Use the follow-up question on their card. |
| Someone argues the agent's medical reasoning is wrong | They may well be right. This is the most valuable thing that can happen — capture it as a GitHub issue on the spot. |
| The room fixates on the model rather than the skills | Redirect to Round 2. The house-rules diff is the argument. |

---

## After the day

The output worth keeping is the `house-rules/` files. Collect them, merge the
generalisable ones, and open a pull request. A workshop that produces three
good house rules and one bug report has produced more than most.
