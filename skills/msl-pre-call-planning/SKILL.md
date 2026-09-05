---
name: msl-pre-call-planning
description: >-
  Prepare an MSL for an upcoming scientific HCP engagement using verified professional context, prior interactions, unresolved enquiries, current evidence and permitted materials. Use for pre-call briefs, meeting objectives, anticipated scientific questions, account context and a focused discussion plan.
license: Apache-2.0
metadata:
  version: "0.2.0"
  tier: workflow
  maturity: beta
  requires:
    - medical-affairs-foundations
  produces: One-page pre-call brief, evidence pack and unresolved-question list
---

# MSL Pre-call Planning

The purpose is a useful scientific exchange. Do the administrative collection so
the MSL can spend time listening, exploring uncertainty and building trust.

## Collect once

Use `data-connection` for authorized records and `kol-engagement-brief` for the
scientific profile. Confirm the HCP identity with professional identifiers or
institution/specialty, the meeting purpose, date, time zone and audience. Never
mix similarly named clinicians. For fictional HCPs, use only the supplied records.

Read prior interactions, open enquiries and commitments, account access rules,
current relevant evidence, material review status and the MSL objectives. Retrieve
publications by verified identity; author-name coincidence is not a match. Do not
infer beliefs, personal characteristics or prescribing behavior from online traces.

## Prepare the brief

- **Why this meeting:** one scientific objective connected to the known need.
- **What changed:** new evidence or a resolved/open question since last interaction.
- **Continuity:** what was asked, what was promised, and what has actually been done.
- **Three questions:** neutral prompts to understand clinical practice, uncertainty
  and unmet evidence needs. Avoid steering to a predetermined product message.
- **Likely questions:** source-supported answers, limitations and an honest route
  for what is unknown. Check jurisdiction and the permitted scientific pathway.
- **Materials:** only correctly scoped, current items eligible under local review
  rules. Draft/expired practice assets are examples for review, not sendable content.
- **Logistics:** verified channel, institution rules, time zone and access route;
  leave missing details explicit rather than inventing appointments or contact data.
- **What to listen for:** contradictions, unanswered scientific questions and
  potential safety information. Do not pre-write a conversation that has not happened.

Deliver a one-page brief with source IDs, a small evidence appendix and an optional
calendar-description draft. Mark facts, inferences and proposed questions separately.
A useful pre-call brief can be produced with incomplete input if its limits are clear.

## Workshop execution

Run `python3 scripts/msl_admin.py --ta oncology-mm --hcp HCP-138 --out outputs`
to collate the linked fictional records. This creates source/context files, not
an analyzed brief. Read them and complete the brief using this skill. Use
[MSL workflow](../../docs/msl-workflow.md) for the full before/during/after cycle.
Read `house-rules/msl-pre-call-planning.md`.
