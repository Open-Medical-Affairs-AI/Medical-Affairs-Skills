---
name: kol-engagement-brief
description: >-
  Prepare an MSL or medical lead for a specific scientific exchange with a
  named external expert. Use when someone is about to meet a KOL,
  investigator, guideline author or society leader and needs to walk in
  ready — "prep me for my meeting with Dr X", "build me a KOL profile".
  Produces a brief covering who they are, what they actually care about,
  what has changed since last contact, the questions worth asking, the
  questions they will ask, and the boundaries of what may be discussed.
  Written to be absorbed in ten minutes, not to be comprehensive.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: workflow
  maturity: stable
  requires:
    - medical-affairs-foundations
    - citation-integrity
  suggests:
    - evidence-appraisal
    - pubmed-search
    - clinical-trials-search
    - deliverable-quality-review
  produces: KOL engagement brief
  network: [eutils.ncbi.nlm.nih.gov, clinicaltrials.gov]
---

# KOL Engagement Brief

The brief exists to make one conversation go better. Everything follows from
that.

An MSL reads this in the ten minutes before the meeting, often in a car park or
a corridor. A comprehensive document is a failed brief regardless of its
quality, because it will not be read. **Two pages. Three at the outside.**

The unit of value is a question the MSL can ask that they would not otherwise
have asked, or an answer they can give that they would otherwise have fumbled.

## The stance this skill takes

A KOL is a scientific peer, not a target. The purpose of the meeting is genuine
exchange — you learn what they think, they get access to data and to the
company's scientific thinking. A brief written to move someone toward a
prescribing position is a call plan wearing a lab coat, and experienced MSLs
find them insulting to use.

The practical consequence: this brief tells the MSL **what to ask**, not what to
say.

## Stage 1 — Inventory

State what you have and what you are missing:

- Expert identity and institution
- Prior interaction notes
- Their publications
- Their trial involvement
- The medical strategy and current scientific priorities
- The evidence base for anything likely to come up
- Product approval status in their jurisdiction
- The meeting's purpose and duration

If you have no prior interaction notes, say so — the brief cannot tell the MSL
what changed, and that is the most useful section.

## Stage 2 — Retrieve

**Publications** (`pubmed-search`):

```bash
python3 skills/pubmed-search/scripts/pubmed.py search \
  --query '"Lastname I"[au] AND "[disease]"[MeSH]' --from 2021 --sort date --limit 40
```

Read the trajectory, not just the list. What someone published three years ago
tells you their reputation; what they published last year tells you what they
are thinking about now. A researcher who moved from single-agent efficacy work
to sequencing or toxicity management has changed the question they care about,
and that shift is the most useful thing in the brief.

Watch for author-name ambiguity. Confirm against affiliation before attributing
a paper.

**Trial involvement** (`clinical-trials-search`): search their institution as a
site and their name as an investigator. Someone running a competitor's trial has
a relationship and a set of commitments that shape the conversation.

**What changed since last contact.** New publications, new trial roles,
guideline committee appointments, moves between institutions, and any data
readout in their area. This is the section MSLs actually use.

## Stage 3 — Analyse

### Who they are, in three lines

Role, institution, and the specific thing they are known for. Not a biography.
"Runs the myeloma programme at [institution]; known for MRD-directed therapy
de-escalation; principal investigator on two ongoing bispecific trials."

### What they actually care about

Inferred from what they publish, what they present, and what they said last
time — not from a market-research segment. Be specific: "durability of response
after BCMA-directed therapy" is useful; "efficacy and safety" is not.

Where you are inferring, say so. "Their last four papers concern treatment
discontinuation, suggesting an interest in de-escalation" is an honest inference.
Asserting it as fact is not.

### What has changed since last contact

The delta. New data in their field, new publications of theirs, positions they
have taken publicly, and anything from the last interaction left unresolved.

### Their likely position, held loosely

If prior notes or publications indicate scepticism, say what about and on what
grounds. **Take their objection seriously.** A KOL who is unconvinced usually has
a reason, and the reason is often good. Briefs that frame scepticism as an
obstacle to overcome produce conversations that go badly.

For a genuinely difficult expert, the useful framing is: what would change their
mind, and do we have it? If we do not, that is an evidence gap
(`evidence-gap-analysis`), and the honest conversation is about the gap.

### Questions worth asking

Four to six, specific to this person. The test: could this question only be
asked of this expert? If it could be asked of anyone, it is not prepared.

Good questions are open, genuinely uncertain, and about something the company
does not already know:

> "You've moved toward MRD-guided discontinuation in your recent work — what
> would you need to see before applying that outside a trial setting?"

Not:

> "What are your thoughts on our product?"

### Questions they are likely to ask, and the evidence

Anticipate three to five, with the appraised answer and the citation. For each,
be explicit about the answer's limits — including where the honest answer is
"we don't have that data".

**"I don't know, and here is what we do have"** is a better answer than a
confident one built on a cross-trial comparison. Prepare the MSL to say it.

### Boundaries

State plainly:

- Which uses are approved in this jurisdiction and which are not
- That unapproved-use discussion happens only in response to an unsolicited
  question, and how to route it
- Anything under embargo or subject to material non-public information rules
- That AEs mentioned in conversation must be reported

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus these:

- **Would this person be comfortable reading this brief?** If any characterisation
  would embarrass you if they saw it, rewrite it. This is a real risk, not a
  hypothetical one, and it is also the right ethical test.
- Is anything asserted about their views that is actually inferred?
- Are the questions genuinely specific to them?
- Is it short enough to be read in the car park?
- Have I prepared the MSL to listen, or only to talk?

## Stage 5 — Deliver

Use `shared/templates/kol-brief.md`. The structure:

```
DRAFT — NOT FOR EXTERNAL USE. REQUIRES QUALIFIED MEDICAL REVIEW.

WHO THEY ARE           3 lines
WHAT THEY CARE ABOUT   3-4 bullets, specific, sourced
WHAT'S CHANGED         since last contact — the delta
ASK THEM               4-6 questions only they could be asked
THEY MAY ASK           3-5 anticipated questions + appraised answers + limits
KNOW COLD              the 3 numbers or facts to have ready, with design named
BOUNDARIES             approval status, off-label routing, AE reporting
PROVENANCE             searches run, sources, what could not be determined
```

**"Know cold"** is three items, not ten. Pick the ones the conversation turns on,
and give each with its design: *"ORR 63.0% (95% CI 55.2–70.4), single-arm,
n=165 — no comparative claim available."*

## Data protection

KOL information is personal data about a named professional. Publications and
registered trial roles are public. Interaction history, inferred motivations,
and internal influence assessments are not, and they carry real reputational and
legal risk if mishandled.

Do not include influence tiers, prescribing data, or commercial segmentation in
a medical brief. Beyond being poor practice, their presence converts a medical
document into evidence that the medical function was operating commercially.

## Before you finish

Read `house-rules/kol-engagement-brief.md`. Length limits, required sections,
and what may be recorded about an individual vary considerably between
organisations, and this is an area where local policy is usually stricter than
the general position here.
