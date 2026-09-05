---
name: medical-content-operations
description: >-
  Plan and maintain non-promotional Medical Affairs content across channels using audience needs, evidence, content inventories and engagement measures. Use for omnichannel medical planning, content reuse, localization, expiry remediation or an evidence change that affects several assets.
license: Apache-2.0
metadata:
  version: "0.2.0"
  tier: workflow
  maturity: beta
  requires:
    - medical-affairs-foundations
  produces: Audience-channel plan, content register and evidence-change impact list
---

# Medical Content Operations

Start with the scientific question and audience need, not a campaign volume target.
Use [connected practice assets](../../workshop/data/connected/README.md) in workshop
mode; real work needs the permitted inventory, channel rules and approved sources.

1. Inventory each asset: ID, owner, version, audience, jurisdiction, language,
   evidence/claim IDs, review status, expiry and permitted channels. A draft or
   expired item is not eligible for distribution.
2. Map needs to content and access preferences. Do not turn a medical interaction
   into promotional targeting. Permission to receive email does not itself
   authorize this agent to send it or establish permitted content.
3. Build a sequence that answers scientific needs: question, channel, asset,
   accountable owner, review dependency and an observable learning outcome.
4. Reuse evidence consistently across a brief, deck, FAQ and lay summary. Every
   transformed claim retains its design limitation, population and source.
5. For localization, preserve scientific meaning and route country-specific label
   and code questions for qualified review. Do not invent approval in a new market.
6. Assess outcomes with valid denominators. Separate invited, attended, completed
   and paired pre/post respondents. Engagement is not evidence of behavior change
   or causal patient benefit.
7. When evidence changes, list affected claims and assets, mark them stale, revise
   draft content, and provide the change log and review queue.

Deliver the content register, prioritized plan, draft examples and metrics table.
Use `medical-affairs-metrics`, relevant content-generation skills and
`mlr-review-readiness` when reached. Read `house-rules/medical-content-operations.md`.
