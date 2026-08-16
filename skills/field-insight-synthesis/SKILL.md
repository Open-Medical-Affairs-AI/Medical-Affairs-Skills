---
name: field-insight-synthesis
description: >-
  Turn a body of field medical observations into insights leadership can act
  on. Use when given MSL interaction records, field notes, KOL feedback,
  advisory board output or medical information enquiry patterns and asked
  what they mean — "what is the field telling us", "synthesise these field
  notes". Produces a ranked insight set with evidence, frequency,
  confidence, strategic implication and a named owner, plus the
  contradictions, the weak signals and what the field did NOT say. Runs a
  mandatory adverse event scan across every record first.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: workflow
  maturity: stable
  requires:
    - medical-affairs-foundations
    - insight-generation
  suggests:
    - strategic-analysis
    - medical-terminology-mapping
    - spreadsheet-analysis
    - deliverable-quality-review
  produces: Field insight report with ranked insights and actions
---

# Field Insight Synthesis

Field medical generates the richest primary intelligence any pharmaceutical
company has about how its science is landing in practice. Most of it is wasted.

The waste happens at a predictable point: observations get aggregated into
themes, themes get displayed on a dashboard, and no decision ever changes. Field
staff notice and stop investing effort in recording, so the input degrades, which
appears to confirm that the programme was never worth much.

This skill is built to break that loop by refusing to stop at themes.

## Stage 0 — Safety scan, before anything else

**Read every record for adverse events, product quality complaints, and special
situations before you begin analysis.** Field notes are one of the highest-yield
sources of unreported safety information in a company, and the reports are almost
never labelled as such.

What this looks like in real field notes:

- *"He's had a couple of patients stop because of the rash"* — AEs with an outcome
- *"They had to admit someone for the cytokine release"* — serious AE
- *"She's using it in second line now"* — off-label use
- *"One of his patients got pregnant on study"* — pregnancy exposure
- *"The pens have been jamming"* — product quality complaint
- *"It just stopped working for two of hers"* — possible lack of effect

Surface every finding at the **top** of the output, with the record ID and the
**verbatim quote**, following the escalation format in
`medical-affairs-foundations`. Do not summarise the quote — the clinical detail
determines seriousness.

If you scanned and found nothing, say that explicitly. Silence is ambiguous, and
a reader needs to know the scan happened.

Then continue with the analysis. Both matter; the safety finding is more urgent.

## Stage 1 — Inventory

Before analysing, characterise the corpus honestly. This determines what the
findings can support:

- **How many records, over what period?**
- **How many distinct MSLs, and how many distinct external contacts?** Forty
  observations from six MSLs about twelve KOLs is a much narrower base than
  forty independent observations.
- **What is the composition?** Academic vs community, geography, specialty. A
  set drawn entirely from academic centres describes academic practice.
- **What is missing?** Which regions, settings, or stakeholder types are absent.
- **Are these verbatims or MSL summaries?** Summaries have already been
  interpreted once.

State this at the top of the report. Every frequency claim that follows depends
on it, and a reader who does not know the denominator will over-read the counts.

## Stage 2 — Read everything before coding

Read the whole corpus first, without categorising. Themes imposed early
determine what you can subsequently see, and the most valuable material is
usually the remark that does not fit.

## Stage 3 — Analyse

Follow `insight-generation`. The specifics for field data:

### Deduplicate carefully

Two MSLs reporting the same KOL saying the same thing is **one** observation.
Two different KOLs saying the same thing independently is a **pattern**. Getting
this wrong either invents a signal or destroys one. Check contact, date, and
source before merging anything.

### Normalise the language, and show your working

Twelve people describe the same concern twelve ways, and the frequency
disappears. Use `medical-terminology-mapping`, and publish the collapsing
decisions — a frequency of 26 that silently merges three distinct concepts is
worse than no number at all.

### Separate what the KOL said from what the MSL concluded

Field notes blend these constantly. *"Dr Chen is concerned about infection risk"*
may be what she said, or what the MSL inferred from her asking about prophylaxis.
The distinction changes the confidence. Where the note does not make it clear,
say so.

### Weigh frequency and significance independently

The matrix in `insight-generation` applies. In field data specifically, the
**weak signal** category is where the value concentrates and where standard
reporting destroys it: one respected investigator saying she has stopped using a
therapy in a subgroup is worth more than thirty people saying the disease is
hard to treat.

Report weak signals explicitly labelled, with the follow-up that would confirm
or dismiss them.

### Preserve contradictions

Where academic and community practice diverge, or where regions disagree, that
difference *is* the insight. Averaging it produces a statement describing nobody.

### Note what was not said

Compare against what you would have expected to hear. If a competitor's major
readout generated no comment, that is a finding. If nobody is asking about
long-term safety, either they are not worried or they have given up expecting an
answer — both are worth knowing.

## Stage 4 — Challenge

Run `deliverable-quality-review`, and specifically:

- **Is every "insight" actually an insight?** Apply the "so what?" test three
  times. Anything that stops early gets relabelled as an observation and moved
  to an appendix. Do not quietly upgrade it.
- **Does every insight have an owner and a decision it feeds?**
- **Is the sample composition stated wherever a frequency is claimed?**
- **Did I sanitise anything?** Field notes contain criticism, frustration, and
  unflattering comparisons with competitors. Removing them removes the signal.
  The uncomfortable observations are the valuable ones, and softening them is the
  most common way this deliverable fails.
- **Does every insight support the current strategy?** If so, you have been
  confirming rather than analysing. Go back and look for what contradicts it.

## Stage 5 — Deliver

Use `shared/templates/insight-report.md`.

```
DRAFT — NOT FOR EXTERNAL USE. REQUIRES QUALIFIED MEDICAL REVIEW.

⚠ SAFETY FINDINGS        AEs/PQCs with verbatims — or "scanned, none found"
WHAT LEADERSHIP SHOULD KNOW   the three that matter, and why those three
BASIS                    records, MSLs, contacts, period, composition, gaps
INSIGHTS                 the table
CONTRADICTIONS           genuine disagreement, and what would resolve it
WEAK SIGNALS             low frequency, high consequence, with follow-up
WHAT WE DIDN'T HEAR      expected and absent
OBSERVATIONS             did not reach insight — retained, labelled
PROVENANCE               mapping decisions, unresolved terms, method
```

The insight table:

| # | Insight | Evidence | Sources | Confidence | Strategic implication | Action | Owner |
|---|---|---|---|---|---|---|---|

### The three-question close

Answer these explicitly — they are what leadership will ask:

1. **Which three insights should leadership care about most, and why those
   three?** The ranking is the analysis. Say what makes these more consequential
   than the rest.
2. **What would change our mind about the highest-confidence insight?**
3. **What is the cost of doing nothing** on each recommended action? If the
   answer is "not much", say so — and reconsider whether it belonged in the set.

## What makes this deliverable fail

- **The theme list.** Categories with counts and no interpretation.
- **Frequency ranking.** Buries every weak signal by construction.
- **Insights with no owner.** "Consider generating further data" is not an action.
- **Losing the verbatim.** Once the original words are gone, nobody can
  re-examine the finding.
- **Manufactured consensus.** Smoothing real disagreement into a statement
  nobody would endorse.
- **The safety scan skipped** because the task was framed as strategic analysis.

## Before you finish

Read `house-rules/field-insight-synthesis.md`. Insight taxonomies, confidence
definitions, escalation routes, and reporting cadence are all organisation-
specific, and this is the skill teams most often need to customise.
