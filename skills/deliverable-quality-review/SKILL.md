---
name: deliverable-quality-review
description: >-
  Red-team your own Medical Affairs deliverable before anyone else sees it.
  Run as the last step of every workflow, after the analysis is written and
  before it is handed over. Hunts the specific ways Medical Affairs output
  fails: promotional drift, overclaiming from single-arm or retrospective
  data, fabricated citations, observations dressed up as insights,
  recommendations with no owner, buried limitations, missing adverse event
  escalation. Use whenever asked to check, review, critique or sanity-check
  Medical Affairs content — including content a human wrote.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: foundation
  maturity: stable
  requires:
    - medical-affairs-foundations
  suggests:
    - evidence-appraisal
    - citation-integrity
  produces: Review findings with severity, and a revised deliverable
---

# Deliverable Quality Review

This is Stage 4 of the execution contract — the challenge pass. It runs on your
own work, before delivery, every time. The reason it exists: an agent that has just spent an hour building an argument
is the worst possible judge of that argument — the commitment is already made.
Reviewing requires a different posture, reading as the most sceptical qualified
person who will see this and looking for reasons it is wrong.

**Do this as a distinct pass.** Re-read the finished deliverable from the top
against the checks below. Do not review from memory of what you intended to
write; review what is on the page.

## Posture

Read as three people in sequence. They catch different things.

**The sceptical KOL.** An experienced clinician who knows this field better than
you and has no stake in the conclusion. They notice the trial you did not
mention, the population mismatch, the comparator nobody uses any more. What
would they push back on in the first two minutes?

**The compliance reviewer.** Reading for whether this is promotional, approval
status is stated, fair balance exists, and the comparative claim is
substantiated. They are not looking for good science; they are looking for
exposure.

**The person who has to act on it.** They need to know what changed, what it
means and what to do. Can they extract that in thirty seconds, or must they read
the whole thing to find out whether it matters?

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

The most common failure in field insight and congress work: a restatement of
what was said or seen with no interpretation; a theme with no explanation of
*why* it matters; an implication with no action; an action with no owner, no
decision it informs, and no way to tell whether it happened.

**Test:** for each insight, ask "so what?" three times. If you run out of
answers before the third, it is an observation.

### 5. Recommendations that cannot be acted on

No named owner or function; no decision it feeds into; no timeframe, or one that
misses the planning cycle it needs to hit; not prioritised, so twelve
recommendations carry apparently equal weight; resource implications unstated;
no way to tell afterwards whether it worked.

**Test:** could the recipient forward this to one named person with "please
action"? If not, it is a suggestion.

### 6. Missing or buried limitations

Uncertainty acknowledged only in a closing paragraph nobody reads; contradicting
evidence omitted rather than addressed; gaps in the underlying material not
stated; assumptions made silently — particularly about jurisdiction, approval
status and population; confidence expressed uniformly across findings of very
different strength.

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

Buries the conclusion, so the reader reaches page 3 before learning whether
anything changed; wrong altitude for the audience — operational detail to
leadership, or strategic abstraction to someone who must act tomorrow; length
that will not be read, since a KOL brief that cannot be absorbed in ten minutes
has failed regardless of its quality; no provenance appendix.

### 9. The conclusion that arrived before the evidence

The hardest to catch in your own work, and the most damaging. Signs: every piece
of evidence points the same way; contradicting data appear only as objections to
be dismissed; the analysis reads as justification rather than investigation; you
cannot state what would have changed your mind.

**Test:** write down what evidence would have led to the opposite conclusion,
then check whether you looked for it. If you cannot name it, you were not
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

**Serious (1)** · **Improvement (2)** · **Note (1)** — see
`references/worked-example.md` for the full block.

**What would have changed my conclusion:** evidence of durable responses beyond
18 months in the comparator arm would have materially weakened the
differentiation argument. I searched for it (see provenance) and found none
published; this is an evidence gap, not a settled question.
```

That last line is the one that matters most. A reviewer who can see what you
looked for and did not find can trust the rest. A complete worked block, with
every severity level filled in, is in `references/worked-example.md`.

## Before you finish

Read `house-rules/deliverable-quality-review.md`. Organisations add their own
checks — banned terminology, mandatory sections, local regulatory requirements.

**Do not skip this pass because the deliverable looks finished.** Looking
finished is exactly the property that makes unreviewed output dangerous: it
signals to the reader that someone already checked.

## References

- `references/worked-example.md` — a complete self-review block at every
  severity level, to copy when writing one.
