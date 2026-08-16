---
name: medical-correspondence
description: >-
  Write the formal correspondence Medical Affairs sends — Dear Healthcare
  Professional letters, responses to investigators and institutions, agency
  and vendor briefs, advisory board invitations, author correspondence, and
  letters accompanying scientific responses. Use when a letter, formal email
  or written communication to an external professional audience is needed.
  Handles the register, the structure each type requires, and the compliance
  content that must appear: approval status, adverse event reporting
  instructions, and transfer-of-value disclosure.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: content
  maturity: beta
  requires:
    - medical-affairs-foundations
    - capability-detection
  suggests:
    - citation-integrity
    - safety-communication
    - deliverable-quality-review
  produces: Formal medical correspondence
  python: [python-docx]
---

# Medical Correspondence

Letters are where the promotional boundary is easiest to cross without noticing.
A warm, helpful, personal register is exactly the register in which an
unsubstantiated claim slips through — and a letter is a durable, forwardable,
quotable record.

## The types, and what each requires

### Dear Healthcare Professional (DHCP) letter

The most consequential. Used for safety communications, label changes and
product actions, and usually reviewed by a regulator.

- **State the purpose in the first sentence.** Not background. What has changed
  and what the reader must do.
- The new safety information, plainly, with the evidence behind it
- **Specific actions** for the recipient, not general advice
- Adverse event reporting instructions with the actual contact route
- Contact details for questions
- No promotional content whatsoever — not one favourable comparison

DHCP letters are typically agreed with the regulator before distribution.
`safety-communication` covers the decision to send one; this skill covers
writing it.

### Response to an investigator or institution

Accompanies a scientific response. Answer what was asked
(`medical-information-response`), state approval status, and do not extend
beyond the question.

### Agency or vendor brief

Scope, audience, deliverable, evidence available, compliance constraints,
review pathway, timeline. **State explicitly what the agency may not do** —
briefs that omit the boundary produce material that has to be rewritten.

### Advisory board invitation

The question you are asking them, why their expertise specifically, the
commitment, fair market value compensation, and the transparency-reporting
consequence. An invitation that reads as an honour rather than a request for
advice sets the wrong tone for the meeting (`advisory-board-design`).

### Author correspondence

Cover letters, reviewer responses, authorship agreements. `scientific-manuscript`
covers the manuscript; this covers the letters around it.

## Register

Formal without being stiff. Direct. Short sentences. No marketing language and
no false warmth — a letter that opens by thanking someone for their "continued
partnership" before delivering a safety message reads as evasive.

Address a clinical audience as peers: precise, unhedged where the evidence is
clear, explicitly uncertain where it is not.

## What every letter carries

- Date, recipient, sender with their role and qualifications
- The purpose, in the first two sentences
- Approval status wherever a product use is discussed
- Adverse event reporting instructions where the letter concerns a product
- A named contact
- The draft marking until reviewed

## Using it

```bash
S=skills/medical-correspondence/scripts/letter.py

python3 $S --example dhcp > letter.json
python3 $S --spec letter.json --out letter.docx
```

Types: `dhcp`, `investigator-response`, `agency-brief`, `advisory-invitation`,
`author-cover`. Falls back to markdown without `python-docx`. The builder blocks
a DHCP letter with no adverse event reporting instructions and any letter
discussing a product use without an approval-status statement.

## Before you finish

Read `house-rules/medical-correspondence.md` — letterhead, signatory rules and
approval routes are entirely local. Then `mlr-review-readiness`.

DHCP letters in particular have a review pathway that usually includes
regulatory and, often, the regulator. Never send one on the strength of this
skill alone.
