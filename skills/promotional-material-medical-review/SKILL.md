---
name: promotional-material-medical-review
description: >-
  Support a qualified medical signatory reviewing commercial promotional material
  by assessing that every claim is scientifically accurate, substantiated by
  the referenced data, and fairly balanced. Use when asked to review, approve,
  sign off or medically certify an advertisement, sales aid, leave-piece,
  website, congress booth panel, email campaign or social post, and when
  adjudicating a claim a commercial team wants to make. This is the reviewer's
  seat, judging someone else's material; `mlr-review-readiness` prepares your own
  Medical Affairs content for review.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.1.0"
  tier: workflow
  maturity: stable
  requires:
    - medical-affairs-foundations
    - evidence-appraisal
  suggests:
    - regulatory-label-intelligence
    - citation-integrity
    - mlr-review-readiness
    - deliverable-quality-review
  produces: Draft medical review findings and recommendation for the signatory
---

# Promotional Material Medical Review

You support the qualified medical signatory. Your output is a draft assessment,
not certification, a signature or authorization to distribute material. Record
findings and a recommendation for the accountable reviewer.

The commercial team's job is to make the strongest legitimate case. Yours is to
establish where legitimate ends. That tension is the design of the system, not a
dysfunction in it — and a signatory who approves everything provides no control
at all.

## Before reading a single claim

Establish: the **jurisdiction** and therefore the applicable code; the **audience**
(HCP or public — direct-to-consumer promotion of prescription medicines is
prohibited outside the US and New Zealand); the **product's current licence** in
that jurisdiction, pulled fresh via `regulatory-label-intelligence` rather than
from memory; the **material type**; and whether it is new or a revision, because
a revision still needs the whole thing checked.

## The claim-by-claim method

Work through the piece systematically. For each claim, in this order:

1. **What exactly is being asserted?** Including by implication, by image, by
   juxtaposition, and by what a reasonable reader would take away. The claim is
   what is communicated, not what is written.
2. **Is it consistent with the licence?** Indication, population, line of
   therapy, dose, combination, duration. Anything outside it is off-label
   promotion regardless of how well referenced.
3. **What reference supports it?** Named specifically — not "data on file"
   without a retrievable document.
4. **Does that reference actually say it?** Open it. Check the population, the
   endpoint, the analysis, the numbers. This is where most findings come from.
5. **Does the design support the strength of the claim?** Apply
   `evidence-appraisal`. A single-arm ORR does not support a comparative claim; a
   secondary endpoint below a failed hierarchy step cannot establish confirmatory
   statistical significance; any descriptive reporting needs explicit qualification.
6. **Is it fairly balanced?** Prominence, position, and comparable depth.

## What reviewers reject, in descending frequency

- **Claims the reference does not support.** The reference is real, the number
  is real, and the population or endpoint is different from the one claimed.
- **Comparative claims without head-to-head evidence.** Including implied
  comparison — "the only", "unlike other agents", or a competitor's trial data
  placed alongside your own on one page.
- **Cross-trial comparison presented as difference.** Two bar charts side by side
  from separate trials is a comparative claim, whatever the footnote says.
- **Superlatives without substantiation.** *Superior, best-in-class, most
  effective, proven, unique*, and *safe* used unqualified. "Well tolerated" is a
  claim requiring support.
- **Safety information subordinated.** Correct text in smaller type, later
  position, or a page the reader will not reach.
- **Efficacy graphs with truncated or unlabelled axes**, missing denominators,
  missing error bars, or a visual scale that exaggerates the difference. Apply
  `data-visualization-for-medical`.
- **Subgroup or post-hoc data presented as the finding.**
- **Surrogate endpoints described as clinical benefit.**
- **Anecdote as evidence** — a case vignette implying typical results.
- **Imagery outrunning the data** — a patient depicted more active than the
  studied population, or imagery implying an unstudied outcome.
- **Missing mandatory elements** — prescribing information, adverse event
  reporting statement, prescribing information access route, job code and date
  of preparation, non-promotional status statements where required.

## Reading the framework you are signing under

The specifics differ by jurisdiction and you must apply the local one, but the
architecture is consistent: promotion must be consistent with the licence,
capable of substantiation, and not misleading by omission, exaggeration or
implication.

- **US** — FDA regulations on prescription drug advertising: fair balance, no
  false or misleading claims, adequate provision, submission on first use via
  Form 2253; the OPDP untitled and warning letters are the practical guide to
  what gets enforced.
- **UK** — the ABPI Code, administered by the PMCPA, with a **named signatory**
  who must be a registered medical practitioner or pharmacist and who certifies
  personally. Clause breaches are published with the company named.
- **EU** — Directive 2001/83/EC as implemented nationally, plus the EFPIA Code.
- **International** — the IFPMA Code.

The published case reports of the UK and other self-regulatory bodies are the
most useful training material available for this work: they describe exactly
which claim, on which page, breached which clause.

## The decision, and how to record it

Every finding gets: the location, the claim as understood, why it fails, the
clause or principle, and what would fix it. "Not approved" without a route
forward is a poor review — the commercial team usually has a legitimate version
of the same message.

| Decision | Meaning |
|---|---|
| **Recommend acceptance for signatory review** | No unresolved issues found within the stated review scope; not certified |
| **Revise and re-review** | Specify changes and evidence required before a human decision |
| **Recommend rejection/defer** | State unresolved issues and what would change the recommendation |

**You cannot certify material; do not recommend acceptance of unverified claims.** If a reference is
unavailable, if the data are on file and you cannot see the file, or if you
cannot establish the licence position, that is not approvable yet — say so
rather than approving conditionally on someone else's assurance.

## Where it gets uncomfortable

The pressure to approve is real, arrives close to a deadline, and is often
framed as a commercial consequence of your decision. Some responses that hold:

- Separate the **claim** from the **wording**. Often the claim is legitimate and
  only the phrasing overreaches; offer the version you can sign.
- Where a claim is not supportable, say what evidence would support it. That
  routes a genuine gap to `evidence-gap-analysis` rather than to an argument.
- Where you are being asked to accept a reading the reference does not bear,
  quote the reference. The document settles it, not seniority.
- Record dissent. If a material proceeds against your advice through an
  escalation route, the record of your position is the point.

Never write that something is "compliant" — describe the checks you performed on
specific claims. Compliance is a broader determination.

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus:

- Did I open every reference, or accept any on its citation alone?
- Did I assess the take-away a reader gets, or only the literal text?
- Would I reach the same decision if a competitor had produced this material?
- Is the safety information genuinely comparably prominent, on the page as laid
  out rather than in the source document?
- Have I said what would make each rejected claim approvable?

## Before you finish

Read `house-rules/promotional-material-medical-review.md`. Signatory
qualification, escalation routes, certification wording and local code
requirements are organisation- and country-specific, and this is one of the few
skills here where the local rule is the operative one rather than a refinement.
