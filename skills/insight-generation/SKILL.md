---
name: insight-generation
description: >-
  Turn raw observations into insights that change a decision. Use whenever
  working with field medical notes, MSL interaction records, KOL feedback,
  advisory board output, congress conversations, enquiry patterns, or any
  qualitative human-sourced material where someone needs to know what it
  means rather than what it says. Enforces the distinction between an
  observation and an insight, and drives every finding from observation to
  pattern to insight to strategic implication to action with a named owner.
  Handles frequency versus significance, and the weak signal only one or two
  people have mentioned.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: primitive
  maturity: stable
  requires:
    - medical-affairs-foundations
  produces: Insight set with implications and actions
---

# Insight Generation

Most Medical Affairs insight programmes fail in the same place. Field teams
record observations diligently, a system aggregates them into themes, a
dashboard displays the themes, and nothing ever happens. Field staff notice that
nothing happens and stop putting effort in. The data gets worse, which confirms
that the programme was not worth much.

The break is almost always at one specific joint: the step from *what was
observed* to *what it means for a decision we are about to make*. That step is
what this skill does.

## The distinction that everything else depends on

**An observation is what happened. An insight explains why it matters and what
follows.**

| Observation | Insight |
|---|---|
| "Dr. Chen said she is concerned about the infection risk." | "Prophylaxis practice is diverging from the label across academic centres, driven by early real-world infection reports. Clinicians are improvising because we have not published a prophylaxis analysis — which means practice is being set without us, and will be hard to shift later." |
| "Three KOLs asked about sequencing after BCMA therapy." | "The sequencing question is now the primary barrier to earlier-line adoption. It is being asked by prescribers who have already decided to use the class — this is a how question, not a whether question, and we have no data to answer it." |
| "Congress had a lot of bispecific data." | "The competitive frame shifted from efficacy to tolerability and administration burden. Every major presentation led with step-up dosing and monitoring requirements rather than response rates. Our differentiation narrative is still built on efficacy." |

The right-hand column has three things the left does not: a **mechanism**
(why this is happening), a **consequence** (what it changes), and an implicit
**decision** it bears on.

**The test:** an insight tells someone something they would act on differently
if they believed it. If a reader can say "yes, and?", it is not an insight yet.

## The ladder

Every finding goes through five levels. Stopping early is the failure mode.

```
OBSERVATION      What was said, seen, or recorded. Verbatim where possible.
      ↓
PATTERN          What recurs across sources, and what varies with it.
      ↓
INSIGHT          Why it is happening, and what it means.
      ↓
IMPLICATION      What it changes for our strategy, evidence, or communication.
      ↓
ACTION           What to do, who owns it, and what decision it feeds.
```

Work up the ladder explicitly. When you cannot get from one rung to the next,
say so — a pattern you cannot explain is worth reporting *as an unexplained
pattern*, because someone with more context may explain it immediately.

## Method

### 1. Read everything first

Before any coding or clustering, read the whole corpus. Themes imposed early
determine what you can see later. The most valuable material is frequently a
single remark that does not fit any category.

While reading, run the **AE/PQC scan** required by `medical-affairs-foundations`.
Field notes are one of the highest-yield sources of unreported safety
information, and finding one is more important than any insight in the set.

### 2. Separate signal from noise, without deleting the anomalies

- **Deduplicate carefully.** Two MSLs reporting the same KOL saying the same
  thing is one observation. Two different KOLs saying the same thing
  independently is a pattern. Getting this wrong either inflates frequency or
  destroys it. Check the source, the date, and the individual.
- **Do not average away contradictions.** If academic centres say one thing and
  community practice says the opposite, that difference *is* the insight.
  Reporting the mean of the two describes nobody.
- **Preserve the outliers.** Set aside a bucket for observations that do not fit
  and revisit it deliberately. This is where emerging signals live.

### 3. Weigh frequency and significance separately

Frequency is not importance. The two dimensions are independent, and treating
frequency as a proxy for importance is why insight programmes surface the
obvious and miss the consequential.

|  | **Low significance** | **High significance** |
|---|---|---|
| **High frequency** | Known and noisy — report briefly, do not lead with it | **Established issue** — probably already known; the value is in quantification and trend |
| **Low frequency** | Noise — record, do not report | **Weak signal** — the highest-value category, and the one that gets filtered out |

A weak signal is an observation from one or two credible sources that, if true,
would change something important. A single respected investigator saying she has
stopped using a therapy in a subpopulation is worth more than thirty people
saying the disease is difficult to treat.

**Report weak signals explicitly labelled as such.** "Mentioned by 2 of 47
sources; if generalisable, this would affect [X]. Recommend targeted follow-up
to confirm or dismiss." That framing is honest about the evidence and still gets
it in front of someone.

### 4. Look for what is absent

The questions nobody asks are informative. If no one is asking about long-term
safety, either they are not worried or they have concluded they will not get an
answer. If a competitor's major data readout generates no comment, that is a
finding.

Compare against what you would have expected to hear. The gap between expected
and actual is often where the real insight is.

### 5. Attribute honestly

- Say how many sources, and of what kind. "6 of 47 field interactions, all
  academic centres" carries very different weight from "6 of 47, spread across
  settings".
- Distinguish what a KOL said from what the MSL inferred. Field notes blend
  these constantly, and the distinction matters.
- Keep verbatim quotes for the load-bearing points. A paraphrase loses the thing
  that made it worth recording.
- Note whose voice is missing. A set of insights drawn entirely from academic
  prescribers describes academic practice.

## Output format

Use this table. It forces the ladder to be walked.

| # | Insight | Evidence | Sources | Confidence | Strategic implication | Recommended action | Owner |
|---|---|---|---|---|---|---|---|
| 1 | *Why it matters, in one or two sentences* | Verbatim or close paraphrase | n/N, and their composition | High/Med/Low + why | What it changes | Specific and actionable | Named function |

**Confidence** rests on the number of independent sources, their credibility and
diversity, consistency across them, and whether corroborating evidence exists
outside the field data. State the reason, not just the rating.

Below the table, three sections that are usually more valuable than the table:

**Contradictions.** Where sources genuinely disagree, and what would resolve it.

**Weak signals.** Low frequency, high potential significance, with the follow-up
that would confirm or dismiss each.

**What we did not hear.** Expected topics that did not come up, and what that
might mean.

## The three-question close

Before delivering, answer these. They are what leadership will ask.

1. **Which three of these should leadership care about most, and why those
   three?** Forcing a ranking exposes whether you have judgement or just
   categories. Say what makes these three more consequential than the rest.
2. **What would change our mind?** For the highest-confidence insight, name the
   evidence that would overturn it.
3. **What is the cost of doing nothing?** For each recommended action, what
   happens if it does not occur. If the answer is "not much", say so — and
   consider whether it belonged in the set.

## Common failures

- **The theme list.** Five categories with counts and no interpretation. This is
  a data summary wearing an insight report's clothes.
- **Frequency ranking.** Ordering by mention count buries every weak signal.
- **Consensus manufacture.** Smoothing genuine disagreement into a single
  statement nobody would endorse.
- **Confirmation.** Finding insights that support the strategy already chosen.
  If every insight validates the current plan, you have not been analysing.
- **Actions without owners.** "Consider developing further data" is not an
  action.
- **Losing the verbatim.** Once the original words are gone, the finding cannot
  be re-examined by anyone who reads it later.
- **Sanitising.** Field notes contain criticism, frustration, and unflattering
  comparisons. Removing them removes the signal. The uncomfortable observations
  are the valuable ones.

## Before you finish

Read `house-rules/insight-generation.md`. Insight taxonomies, confidence
definitions, and required routing differ by organisation, and this is one of the
skills teams most often want to customise.
