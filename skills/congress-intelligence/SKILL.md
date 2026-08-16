---
name: congress-intelligence
description: >-
  Analyse what changed at a medical congress and what the organisation
  should do about it — not summarise what was presented. Use for post-
  congress readouts, pre-congress preparation, and requests like "what
  happened at ASCO" or "brief leadership on the meeting". Produces a four-
  part readout — what changed, why it matters, what to watch, what we should
  do — by comparing what was expected against what happened and separating
  genuinely new evidence from incremental updates. Deliberately resists the
  abstract summary, which is the default failure.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: workflow
  maturity: stable
  requires:
    - medical-affairs-foundations
    - evidence-appraisal
    - strategic-analysis
  suggests:
    - evidence-synthesis
    - citation-integrity
    - clinical-trials-search
    - deliverable-quality-review
  produces: Congress intelligence readout
  network: [eutils.ncbi.nlm.nih.gov, clinicaltrials.gov]
---

# Congress Intelligence

Leadership does not need to know what was presented. They need to know **what
changed**, and whether anything they are doing should now be different.

That distinction is the whole skill. A forty-slide deck summarising sixty
abstracts is the default output, it takes a week to produce, and by the time it
lands everyone has formed their impressions from corridor conversations. A
four-paragraph note delivered within seventy-two hours, saying what moved and
what it means, is worth more than all of it.

**Timing is a design constraint, not a nice-to-have.** Post-congress readouts
have a half-life measured in days.

## The reasoning chain

This is the analysis. Work through it in order; each step depends on the one
before.

```
What did we EXPECT?              Establish the prior. Without it, nothing is
      ↓                          surprising and everything looks important.
What actually HAPPENED?
      ↓
What was genuinely NEW?          Separate new evidence from longer follow-up
      ↓                          of things already known.
What CONTRADICTS prior evidence? The highest-value category, and the one
      ↓                          most often smoothed over.
What changed COMPETITIVELY?
      ↓
What matters CLINICALLY?         Would a thoughtful clinician change anything?
      ↓
What matters to MEDICAL AFFAIRS? Our evidence, narrative, field, plans.
      ↓
What should we DO?               With owners and timing.
```

**Step one is the one people skip.** Without a stated prior, every abstract
looks equally novel, and the readout becomes a list. Write down what you
expected before you read anything: which readouts were scheduled, what the
consensus expectation was, what would count as a surprise.

## Stage 1 — Inventory

- Congress, dates, and therapeutic scope
- Abstracts, presentations, press releases, competitor announcements available
- The medical strategy and current scientific narrative
- What was expected — from `clinical-trials-search`, prior guidance, and
  scheduled readouts
- Field notes from on-site conversations, if any

**On-site conversation is the most valuable and least captured input.** What
investigators said in the hallway about a presentation is frequently more
informative than the presentation. If you have it, weight it — and run the
safety scan over it (`medical-affairs-foundations`).

## Stage 2 — Retrieve

Congress abstracts are largely **not** in PubMed. Do not conclude that a study
does not exist because a search returns nothing.

- `clinical-trials-search` for the trials behind the abstracts — design,
  population, and endpoints that the abstract omitted
- `pubmed-search` to check whether a full publication now exists, and to place
  the new data against what was already published
- Check whether a registered primary endpoint was changed
  (`ctgov.py history`) — that context does not appear in the abstract

## Stage 3 — Analyse

### Appraise before you interpret

Congress abstracts are the weakest routinely-cited evidence tier: not
peer-reviewed, methods incomplete, and results that change materially before
full publication more often than people assume. `evidence-appraisal` has a fast
triage for abstracts.

Label every citation `[abstract]` (`citation-integrity`). An abstract cited
alongside peer-reviewed papers without a tier label implies a parity that does
not exist.

### Separate genuinely new from incremental

Most congress data is longer follow-up of something already known. That is
useful and it is not news. Reserve "new" for: a first readout, a new population,
a result that contradicts expectation, or an unexpected safety finding.

**Longer follow-up is only news when it changes the conclusion** — a plateau
emerging, a durability signal holding or failing, a late toxicity appearing.

### Hunt for contradiction

What was presented that disagrees with prior evidence, with the label, with
guidelines, or with your own narrative? This is the highest-value category and
the one most often quietly dropped, because it is uncomfortable.

Work through the reconciliation candidates in `evidence-synthesis` before
concluding — different populations, comparators, endpoints, or follow-up will
explain most apparent contradictions. Those that survive are important.

### Competitive change, honestly

The failure mode here is asymmetry: rigorous scepticism applied to competitor
data, generosity applied to your own. External audiences detect it instantly,
and it destroys the credibility of the whole readout.

Apply the same appraisal standard to both. If a competitor's single-arm data
looks strong, say so. If your own does not, say that too.

Also watch the **dimension shift**. The axis on which a field compares products
moves over time — efficacy, then safety, then administration burden, then
access. A congress where every major presentation led with step-up dosing and
monitoring rather than response rates has told you the axis moved, and a
narrative built for the previous axis has quietly stopped answering the question
being asked.

### What it means for us

Be concrete about consequences:

- Does anything invalidate a claim in our scientific narrative?
- Does it open or close an evidence gap? (Route to `evidence-gap-analysis`.)
- Will the field hear questions they cannot answer? (Route to field training.)
- Does it change what we should publish, or when?
- Does it change a planned study's rationale or comparator?

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus:

- **Did I state a prior?** Without it, this is a list.
- **Would a competitor's Medical Affairs team recognise this as fair?**
- **Did I bury anything unfavourable?** Re-read the sections about your own
  product with the scepticism you applied to theirs.
- **Is anything here actually news**, or is it all longer follow-up?
- **Could someone act on this today?**

## Stage 5 — Deliver

Use `shared/templates/congress-readout.md`. Four sections, in this order,
one page:

```
DRAFT — NOT FOR EXTERNAL USE. REQUIRES QUALIFIED MEDICAL REVIEW.

WHAT CHANGED       3-5 items. Each: what happened, evidence tier, why it is
                   a change. Nothing that was expected and happened.
WHY IT MATTERS     Clinical and competitive consequence. The "so what".
WHAT TO WATCH      Not yet actionable, but developing. Readouts due,
                   contradictions unresolved, signals to confirm.
WHAT WE SHOULD DO  Specific, owned, with timing. Ordered by consequence.
```

Then, below the fold for those who want it: the appraised evidence detail, the
full abstract list, and provenance.

**If nothing changed, say so.** "Three days of data, no change to our position;
here is why" is a legitimate and valuable readout. Manufacturing significance to
justify the effort of attending is a real and common failure.

## Pre-congress use

The same skill runs forwards. Before the congress:

- What is scheduled to read out, and what do we expect?
- What would be a genuine surprise, in either direction?
- What questions will the field be asked that they cannot currently answer?
- Which competitor presentations should we make sure someone attends?
- What is our prior, written down, so that the post-congress readout has
  something to compare against?

Writing the prior down beforehand is what makes the post-congress analysis
possible. Reconstructing it afterwards produces hindsight, not intelligence.

## Before you finish

Read `house-rules/congress-intelligence.md`. Format, distribution, timing
expectations, and rules on citing abstracts differ by organisation — several
prohibit external use of abstract-tier evidence entirely.
