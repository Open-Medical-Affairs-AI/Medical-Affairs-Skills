---
name: medical-information-response
description: >-
  Draft responses to unsolicited medical enquiries from healthcare
  professionals, patients and payers, and build the standard response
  documents and FAQ library behind them. Use when answering a specific
  clinical question about a product, developing or updating a standard
  response document, building an FAQ set for a launch, or handling a
  question that touches an unapproved use. Enforces the reactive-only
  pathway: answer the question asked and no more, state approval status,
  ground every statement in the label or in appraised evidence, and scan the
  enquiry itself for adverse events.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.1.0"
  tier: workflow
  maturity: stable
  requires:
    - medical-affairs-foundations
    - citation-integrity
    - regulatory-label-intelligence
  suggests:
    - evidence-appraisal
    - pubmed-search
    - deliverable-quality-review
  produces: Standard response document or scientific response letter
  network: [eutils.ncbi.nlm.nih.gov, api.fda.gov]
---

# Medical Information Response

Medical Information is where the company answers questions it did not choose.
That is what makes it legitimate, and it is also the constraint that governs
everything here.

Two rules shape every response:

**Answer the question that was asked.** Not the adjacent question you would
rather answer, and not a broader one. Scope creep in a medical information
response is how a reactive communication becomes a proactive one — which is a
regulatory problem, regardless of how accurate the additional content is.

**The enquiry may contain a case.** *"My patient developed X after starting Y —
what do you know about this?"* is an adverse event report wearing a question. Scan
first, always.

## Stage 0 — Safety scan

Before drafting anything, read the enquiry for adverse events, product quality
complaints, and special situations (`medical-affairs-foundations`).

Enquiries are a high-yield source because the question is frequently prompted by
something that just happened to a patient. Surface any finding at the top, with
the verbatim, and route to pharmacovigilance. The response can proceed in
parallel — but the safety routing is not contingent on it.

## Stage 1 — Establish the request

Before drafting, establish and record:

- **What exactly was asked.** Quote it. Ambiguity is resolved by asking, not by
  guessing broadly.
- **Was it genuinely unsolicited?** A question the company prompted, engineered,
  or asked at a company-organised promotional event is not unsolicited, and the
  reactive pathway does not apply.
- **Who is asking.** HCP, patient or carer, payer. This changes the register,
  the depth, and in some jurisdictions what may be provided at all.
- **Jurisdiction.** Approval status differs. When unstated, ask; if you must
  proceed, state the jurisdiction you assumed.
- **Is this on- or off-label?** (`regulatory-label-intelligence`) — this
  determines the whole shape of the response.

## Stage 2 — Retrieve

**The label first** (`regulatory-label-intelligence`). It is the primary source
for anything within the approved indication, and its wording settles what
on-label means.

```bash
python3 skills/regulatory-label-intelligence/scripts/openfda.py \
  indication --generic [product]
```

**Then published evidence** (`pubmed-search`) where the question goes beyond the
label. Appraise it (`evidence-appraisal`) — a medical information response that
repeats a single-arm result causally is as wrong as any other document making
that error, and it is more consequential because a clinician may act on it.

**Verify every citation** (`citation-integrity`). Responses go to clinicians who
may look them up.

## Stage 3 — Draft

### If the question is on-label

Ground the answer in the label, supplemented by published evidence where it adds
genuine clarity. Include the relevant safety information. Keep to the question.

### If the question touches an unapproved use

This is the pathway that requires care. The response must:

- **State the approval status prominently** — not in a footnote:

  > *[Product] is not approved for [use] in [jurisdiction]. The following
  > information is provided in response to your specific enquiry and describes
  > investigational data. The safety and efficacy of [product] for this use have
  > not been established.*

- Be **truthful, non-misleading, and scientifically balanced** — including data
  that do not support the use, and the limitations of what does
- Be **tailored to this enquiry**, not a general document
- Include **safety information**
- Contain **no comparative or superiority framing**
- Be delivered through Medical Information, recorded, and not through a
  promotional channel

If your organisation does not permit off-label responses in your channel, route
rather than answer. Several do not, and the house rules will say so.

### If the answer is "we don't know"

Say so. This is a legitimate and common outcome, and it is more useful than a
constructed answer.

> No published data address [X] in this population. [Trial] excluded patients
> with [Y], and we are not aware of ongoing studies in this setting (registry
> searched [date]). We have recorded this question.

Recording the question matters: recurring enquiries the label and literature
cannot answer are direct evidence of an evidence gap. Route them to
`evidence-gap-analysis`. Medical Information enquiry patterns are one of the
best gap signals a company has and are chronically under-used.

## Standard response documents

An SRD answers a recurring question once, properly, for reuse.

**Structure:**

```
Question (as it is actually asked, in the enquirer's words)
Approval status statement
Summary answer — 2-4 sentences, the answer itself
Supporting evidence — appraised, with design named, tiers labelled
Limitations — what the evidence does not establish
Safety information — relevant to the question
References — verified, AMA format
Document control — version, approval date, review date, approver
```

**What makes an SRD go wrong:**

- **Scope creep on reuse.** An SRD written for one question gets sent for an
  adjacent one. Write the question narrowly and maintain more documents.
- **Ageing.** Evidence moves; SRDs do not update themselves. Every SRD carries a
  review date, and an out-of-date SRD is worse than none because it carries the
  authority of an approved document.
- **Overclaiming through summarisation.** The summary answer is where design
  caveats get dropped. Keep them.
- **Missing approval status** on anything touching an unapproved use.

## FAQ development

For a launch or new indication, build the FAQ set from what people will
**actually** ask, not from what you want to explain.

Sources, in order of value: prior enquiry data for similar products; field
insights (`field-insight-synthesis`); questions raised at advisory boards and
congresses; the questions the label leaves open; and the questions your own
evidence gaps imply.

**Include the uncomfortable questions.** An FAQ that answers only the easy
questions is transparently a marketing document, and clinicians read it that
way. The questions about what you do not know, about the comparator you lack,
and about the safety signal are the ones that build credibility when answered
honestly.

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus:

- **Did I answer more than was asked?** Cut it.
- **Is approval status stated and prominent?**
- **Is there any comparative claim?** Remove it unless head-to-head data support
  it.
- **Is safety information present and proportionate?**
- **Would this read as promotional to a regulator?** Reread as a compliance
  reviewer.
- **Is every citation verified, tiered, and appraised?**
- **Did I scan the enquiry for an adverse event?**

## Stage 5 — Deliver

Use `shared/templates/medical-information-response.md`.

Prepare a response-register entry and a separate evidence-gap entry where useful.
Write to a live system or send only with existing user authorization and available
permitted tools. In workshop mode keep these as simulated local records.

## Before you finish

Read `house-rules/medical-information-response.md`. This is one of the most
tightly governed activities in Medical Affairs. Approval routes, permitted
channels, whether off-label enquiries may be answered at all, required document
control, and retention periods are all local, and local policy is almost always
stricter than the general position described here.
