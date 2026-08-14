---
name: deliverable-quality-review
description: >-
  Red-team your own Medical Affairs deliverable before anyone else sees it. Run
  this as the last step of every workflow — after the analysis is written and
  before it is handed over. It hunts the specific ways Medical Affairs output
  fails: promotional drift, overclaiming from single-arm or retrospective data,
  fabricated or misattributed citations, observations dressed up as insights,
  recommendations with no owner or decision attached, buried limitations,
  missing adverse event escalation, and conclusions that were fixed before the
  evidence was read. Use it whenever you have produced a brief, report, summary,
  strategy document, response, deck, or manuscript draft, and whenever someone
  asks you to check, review, critique, or sanity-check Medical Affairs content —
  including content a human wrote.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: foundation
  maturity: stable
  requires: [medical-affairs-foundations, evidence-appraisal, citation-integrity]
  produces: Review findings with severity, and a revised deliverable
---

# Deliverable Quality Review

This is Stage 4 of the execution contract — the challenge pass. It runs on your
own work, before delivery, every time.

The reason it exists: an agent that has just spent an hour building an argument
is the worst possible judge of that argument. The commitment is already made.
Reviewing requires deliberately adopting a different posture — reading as the
most sceptical qualified person who will see this, looking for reasons it is
wrong rather than confirmation it is right.

**Do this as a distinct pass.** Re-read the finished deliverable from the top
against the checks below. Do not review from memory of what you intended to
write; review what is actually on the page.

## Posture

Read as three people in sequence. They catch different things.

**The sceptical KOL.** An experienced clinician who knows this field better than
you do and has no stake in the conclusion. They will notice the trial you did
not mention, the population mismatch, the fact that the comparator is not what
anyone actually uses any more. What would they push back on in the first two
minutes?

**The compliance reviewer.** Reading for whether this is promotional, whether
approval status is stated, whether there is fair balance, whether the
comparative claim is substantiated. They are not looking for good science; they
are looking for exposure.

**The person who has to act on it.** They need to know what changed, what it
means, and what to do. Can they extract that in the first thirty seconds, or do
they have to read the whole thing to find out whether it matters?

## The failure catalogue

Work through these. Each is something that actually happens, repeatedly.

### 1. Promotional drift

- Comparative or superiority language without head-to-head evidence
- Selective presentation — favourable data foregrounded, unfavourable omitted or
  minimised
- Words doing work the evidence cannot support: *proven*, *demonstrated*,
  *safe*, *well-tolerated* (unqualified), *best-in-class*, *the only*
- A conclusion that would change if the product were a competitor's
- Limitations present but positioned where nobody will read them

**Test:** rewrite the key claim with the product names swapped. Does it still
read as a fair scientific statement? If it now reads as an attack on your own
product, the original was positioning.

### 2. Overclaiming from the design

- Causal language from single-arm, retrospective, or observational data
- Cross-trial comparison presented as evidence of difference
- Surrogate endpoints described as clinical benefit
- Subgroup findings presented as conclusions without an interaction test
- Secondary endpoints treated as positive when the testing hierarchy had already
  failed
- FAERS or spontaneous-report disproportionality described as risk or incidence
- "No signal observed" in an underpowered study read as evidence of safety

**Test:** for every claim, name the design that supports it. If the sentence and
the design do not match, the sentence is wrong.

### 3. Citation failures

- Any identifier not resolved in this session (`citation-integrity`)
- A real reference cited for a claim it does not make
- Numbers quoted without confidence intervals
- Congress abstracts cited alongside peer-reviewed papers without tier labels
- Author hedging removed — "may be associated with" tightened to "is associated
  with"
- The source's own stated limitation dropped

**Test:** pick the two most load-bearing citations and check them against the
actual abstract. Not the ones you are confident about — the ones the argument
depends on.

### 4. Observations masquerading as insights

The most common failure in field insight and congress work.

- A restatement of what was said or seen, with no interpretation
- A theme with no explanation of *why* it matters
- An implication with no action
- An action with no owner, no decision it informs, and no way to tell if it
  happened

**Test:** for each insight, ask "so what?" three times. If you run out of
answers before the third, it is an observation.

### 5. Recommendations that cannot be acted on

- No named owner or function
- No decision it feeds into
- No timeframe, or a timeframe that misses the planning cycle it needs to hit
- Not prioritised — twelve recommendations of apparently equal weight
- Resource implications unstated
- No way to tell afterwards whether it worked

**Test:** could the recipient forward this to one named person with "please
action"? If not, it is a suggestion.

### 6. Missing or buried limitations

- Uncertainty acknowledged in a closing paragraph nobody reads
- Contradicting evidence omitted rather than addressed
- Gaps in the underlying material not stated
- Assumptions made silently — particularly about jurisdiction, approval status,
  and population
- Confidence expressed uniformly across findings of very different strength

**Test:** could a reader who acts on this be blindsided by something you knew?

### 7. Safety and compliance omissions

- No AE/PQC scan result stated — neither findings nor an explicit "scanned,
  none found"
- Potential AE content present in source material and not surfaced
- Approval status not stated for a use discussed
- Off-label content that is not clearly responsive to an unsolicited request
- Patient-identifying detail present
- The DRAFT marking missing or removed

**These are stop-and-fix, not note-and-continue.**

### 8. Structural and altitude problems

- Buries the conclusion — the reader has to reach page 3 to learn whether
  anything changed
- Wrong altitude for the audience: operational detail to leadership, or strategic
  abstraction to someone who needs to act tomorrow
- Length that will not be read. A KOL brief that cannot be absorbed in the ten
  minutes before a meeting has failed regardless of its quality.
- No provenance appendix

### 9. The conclusion that arrived before the evidence

The hardest to catch in your own work, and the most damaging.

Signs: every piece of evidence points the same way; contradicting data appear
only as objections to be dismissed; the analysis section reads as justification
rather than investigation; you cannot state what would have changed your mind.

**Test:** write down what evidence would have led to the opposite conclusion.
Then check whether you looked for it. If you cannot name it, you were not
analysing — you were assembling support.

## Severity

Not everything found is equally urgent. Classify, so the human knows what to
look at first.

| Severity | Meaning | Examples |
|---|---|---|
| **Blocking** | Do not deliver until fixed | Unresolved citation, missed AE, promotional claim, off-label content outside the reactive pathway, patient identifiers |
| **Serious** | Fix before delivery; changes what the reader concludes | Overclaim from design, missing limitation that would change a decision, unsupported comparative statement |
| **Improvement** | Would make it materially more useful | Observation not developed into insight, recommendation without an owner, poor altitude |
| **Note** | Flag for the human, no change needed | A judgement call worth confirming, an assumption worth checking |

## Output

Report what you found, then fix what you can and hand over what you cannot.

```markdown
## Self-review

**Blocking (2)**
- PMID 38112xxx did not resolve — removed; the claim it supported is now marked
  [UNSOURCED] pending a real reference.
- Field note MSL-034 describes a hospitalisation for cytokine release syndrome.
  Surfaced at the top of this document as a potential serious AE.

**Serious (1)**
- "Superior depth of response" rested on a cross-trial comparison. Rewritten to
  report each trial separately, with populations stated and the absence of
  head-to-head evidence noted.

**Improvement (2)**
- Insights 4 and 7 were observations. Developed to implication and action;
  insight 9 could not be developed and is retained as an observation, labelled.
- Recommendations now carry owners and the decisions they inform.

**Note (1)**
- Assumed US approval status throughout, as jurisdiction was unstated. Flagged
  in the assumptions section — confirm before use outside the US.

**What would have changed my conclusion:** evidence of durable responses beyond
18 months in the comparator arm would have materially weakened the
differentiation argument. I searched for it (see provenance) and found none
published; this is an evidence gap, not a settled question.
```

That last line is the one that matters most. A reviewer who can see what you
looked for and did not find can trust the rest.

## Before you finish

Read `house-rules/deliverable-quality-review.md`. Organisations add their own
checks — banned terminology, mandatory sections, local regulatory requirements.

**Do not skip this pass because the deliverable looks finished.** Looking
finished is exactly the property that makes unreviewed output dangerous: it
signals to the reader that someone already checked.
