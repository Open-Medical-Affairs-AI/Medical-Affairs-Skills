---
name: mlr-review-readiness
description: >-
  Prepare Medical Affairs content for Medical/Legal/Regulatory review and
  pre-check it against what reviewers actually reject. Use before submitting
  a deck, document, response or material to MLR/MRC review, when a piece has
  come back and you need to work out why, or when asked whether content is
  promotional, substantiated or fair-balanced. Builds a claim-evidence
  matrix, detects promotional language and unsubstantiated comparative
  claims, and assembles the annotated reference pack. This prepares your own
  content; to sit as medical signatory on someone else's promotional
  material, use promotional-material-medical-review.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: content
  maturity: beta
  requires:
    - medical-affairs-foundations
    - citation-integrity
  suggests:
    - evidence-appraisal
    - promotional-material-medical-review
    - deliverable-quality-review
  produces: Claim-evidence matrix and MLR submission pack
---

# MLR Review Readiness

Every MLR cycle costs one to three weeks. Most first-round rejections are
mechanical — an unreferenced claim, a missing approval statement, a comparative
adjective with no head-to-head trial behind it — and every one of them is
findable before submission.

This skill is the pre-check. It is not a substitute for review: the reviewers
hold the accountability, and nothing here makes content compliant. It removes
the avoidable round.

**Never describe the output of this skill as "MLR-ready", "compliant", or
"approved".** Those are determinations made by people with accountability. Say
what was checked and what remains open.

## The claim-evidence matrix

The core artefact. Every assertion in the piece, mapped to what supports it.

| # | Claim (verbatim) | Location | Type | Source | Evidence tier | Supports the claim as written? | Note |
|---|---|---|---|---|---|---|---|

**Claim types**, because each has a different evidence requirement:

| Type | Requirement |
|---|---|
| **Efficacy** | Result with CI, from a design that supports the claim as phrased |
| **Safety** | Rate with denominator, from the label or the trial — not FAERS |
| **Comparative** | **Head-to-head evidence.** Nothing else substantiates a comparison. |
| **Mechanism** | Evidence, labelled preclinical if preclinical |
| **Epidemiology** | Cited source, with population and geography matching the claim |
| **Economic** | Analysis with stated assumptions and perspective |
| **Regulatory status** | The label, jurisdiction stated |

The column that does the work is **"supports the claim as written?"**. A real
reference attached to a claim it does not support is the most common substantive
finding in review, and it is invisible unless someone reads the source against
the sentence.

```bash
python3 skills/mlr-review-readiness/scripts/claim_audit.py --file deck-content.md
python3 skills/mlr-review-readiness/scripts/claim_audit.py --file doc.md --format matrix
```

The script flags promotional language, comparative constructions, absolute
safety claims, unreferenced numeric assertions, and missing approval-status
statements. It cannot judge whether a source supports a claim — that requires
reading the source, and it is your job.

## What reviewers reject, in rough order of frequency

**1. Unreferenced claims.** Any statement of fact needs a source. Numbers
especially. The fastest self-check: read the piece and stop at every number.

**2. Comparative claims without head-to-head data.** Including implicit ones —
"the only", "first-line choice", "unlike other agents", and any side-by-side
layout of two trials' results. A side-by-side table asserts comparability
whatever the footnote says.

**3. Absolute safety language.** "Safe", "well tolerated" without
qualification, "no significant side effects". Safety claims carry rates and
denominators.

**4. Missing or inadequate fair balance.** Efficacy without proportionate
safety, in the same section rather than in an appendix.

**5. Approval status not stated**, or stated only in small print, for any use
discussed.

**6. Overclaiming from the design.** Causal language from single-arm or
retrospective data. Surrogate endpoints described as clinical benefit.
Secondary endpoints treated as positive after the testing hierarchy failed.

**7. Data on file not labelled**, or labelled without a retrievable document
reference.

**8. Old references.** A superseded guideline, a label version that has changed,
a paper that has been retracted.

**9. Off-label content** outside the reactive pathway.

**10. Reference pack incomplete.** Reviewers cannot verify what they cannot
open.

## Promotional language

Words that reliably trigger a query, and what to write instead:

| Flagged | Why | Instead |
|---|---|---|
| proven, demonstrated | Implies certainty beyond most designs | "was observed", "showed" with the design named |
| safe, well tolerated | Absolute safety claim | the actual rates with denominators |
| superior, better, more effective | Comparative | only with head-to-head data; otherwise report each trial separately |
| best-in-class, first-in-class | Comparative and promotional | remove |
| the only | Comparative and often factually fragile | remove |
| significant | Ambiguous between statistical and clinical | say which, and give the effect size |
| dramatic, remarkable, breakthrough | Promotional register | remove |
| should be used, recommended | Prescribing direction | not Medical Affairs' role |
| well established | Vague appeal to consensus | cite the guideline |

**The swap test:** rewrite the claim with a competitor's product name. If it now
reads as an unfair attack, the original was positioning rather than science.

## The submission pack

What to hand the reviewers:

1. **The piece**, with claims numbered and annotated
2. **The claim-evidence matrix**
3. **The reference pack** — every cited source as a retrievable file, annotated
   to show the exact passage supporting each claim. Highlight it. Reviewers
   should not have to hunt through a 12-page paper.
4. **Approval status statement** with jurisdiction
5. **The safety information** included, and the source it came from
6. **Prior version and its approval reference**, if this is a revision, with
   changes marked
7. **Intended audience, channel, and use** — the same content can be acceptable
   for one and not another
8. **Known open items** — the questions you already know the reviewers will ask,
   answered in advance

That last item shortens cycles more than anything else. Reviewers respond well
to being told where the author is uncertain.

## Before you finish

Run `deliverable-quality-review` first — it catches the reasoning failures; this
skill catches the mechanical ones, and reasoning failures reappear as compliance
findings if left.

Read `house-rules/mlr-review-readiness.md`. MLR processes, required forms,
banned terminology lists, and reference pack conventions are entirely
organisation-specific, and this is one of the skills where local rules matter
most.
