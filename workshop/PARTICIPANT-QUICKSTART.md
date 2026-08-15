# Start here

You are going to give an AI agent a **job**, not a prompt.

You do not need to know how any of this is built. That is the point.

---

## 1. Point your agent at this folder

However your agent takes files — a local folder, an upload, a repository URL.

If it asks what to do with it, tell it:

> Read AGENTS.md first.

---

## 2. Give it your mission

Your mission card is in `missions/`. Your team has one.

Your materials are in `data/<your therapeutic area>/`:

- `oncology-mm/` — multiple myeloma
- `immunology-ad/` — atopic dermatitis
- `cardiometabolic-obesity/` — obesity

Tell the agent the mission and where the materials are. Something like:

> Read AGENTS.md, then run the mission in workshop/missions/mission-2.md using
> the materials in workshop/data/oncology-mm/.

**Then let it work.** Do not tell it how. Working out how is its job, and
watching it do that is the exercise.

---

## 3. Watch for these four things

They are what separate an agent from a chatbot.

**It says what it is about to do.** A plan, before it starts.

**It tells you what is missing.** Before it answers, not after. If it says
*"there are no prior interaction notes, so I cannot tell you what changed"* —
that is the behaviour you want.

**It argues with itself.** Somewhere near the end it should challenge its own
conclusions and change something.

**It shows its working.** Which searches it ran, which sources it used, what it
could not determine.

---

## 4. Push on it

When it finishes, do not stop. Ask:

- *"Which three of these matter most, and why those three?"*
- *"What would change your mind?"*
- *"What did you miss?"*
- *"What's the cost of doing nothing?"*

The follow-up question on your mission card is designed for this.

---

## A few things to know

**Everything in `data/` is invented.** Fictional company, fictional products,
fictional people, fictional institutions. It is written to behave like the real
thing.

**Do not upload real company data.** Not today, not into this.

**The output is a draft.** It will say so. That marking stays on until a
qualified person has actually reviewed the content — which is not today.

**If it makes something up, that is a finding.** Write it down. There is an
award for it.

---

That is everything. Go.
