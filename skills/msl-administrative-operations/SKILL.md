---
name: msl-administrative-operations
description: >-
  Reduce repetitive MSL administration by assembling source-backed meeting packs, open-task queues, draft CRM imports, weekly summaries and coverage reports. Use for record consolidation, duplicate follow-up detection, overdue commitments or planning administrative work around HCP engagements without fabricating completed activity.
license: Apache-2.0
metadata:
  version: "0.2.0"
  tier: workflow
  maturity: beta
  requires:
    - medical-affairs-foundations
  produces: Prioritized administrative queue, draft record packet and weekly status brief
---

# MSL Administrative Operations

Automate data gathering and preparation; preserve the distinction between proposed
work, documented activity and confirmed external updates. Use the companion pre-call,
post-call and HCP access skills for the scientific engagement cycle.

## Tasks to take off the MSL plate

| Administrative task | What to prepare automatically | What needs confirmation |
|---|---|---|
| Pre-call record gathering | Prior notes, open questions, relevant materials, access context | Identity and any missing meeting facts |
| Duplicate typing | A factual structured note and mapped CRM draft fields | Actual encounter details and live write scope |
| Follow-up management | Deduplicated commitments and overdue-action queue | Unstated owner/date and completion status |
| Scheduling preparation | Availability comparison and calendar-description draft | Time zone, participants and invitation authorization |
| Material requests | Evidence/source links and current review-status check | Eligibility for external use and delivery action |
| Weekly reporting | Activities, unresolved needs and source-linked status | Unsupported outcome or causal impact claims |
| Expense/document administration | Extract supplied receipt fields and missing-document list | Policy decisions and submission authorization |

Do not invent hours, visits, receipts, expenses or engagement outcomes. Count unique
records with a defined date range; use explicit statuses rather than guessing from
narrative. A source update should amend a draft, not generate duplicate tasks.

The bundled helper assembles a fictional MSL packet with only Python:

```bash
python3 scripts/msl_admin.py --ta oncology-mm --hcp HCP-138 --out outputs
```

It exports matching historical interactions, open task rows and access context,
with provenance and deterministic proposed-record keys. The agent then synthesizes
the requested brief. It does not send email, schedule meetings or write to a CRM.
For real data use an authorized connector/export via `data-connection`; inspect
actual schema and permission scope. This helper is for the supplied practice DB.

For recurring work, use the host scheduler only when available and requested.
Confirm the actual schedule and next run; a skill alone is not a background service.
Read `house-rules/msl-administrative-operations.md`.
