---
name: msl-post-call-follow-up
description: >-
  Convert actual MSL engagement notes or a transcript into factual CRM-ready drafts, scientific follow-up tasks and evidence-gap records. Use after a call to reduce duplicate typing, preserve HCP questions and commitments, identify potential safety intake, and prepare follow-up correspondence without inventing what occurred.
license: Apache-2.0
metadata:
  version: "0.2.0"
  tier: workflow
  maturity: beta
  requires:
    - medical-affairs-foundations
  produces: Draft CRM note, follow-up task list and scientific-question register
---

# MSL Post-call Follow-up

Use actual supplied notes or a transcript. A pre-call plan is not evidence of what
happened. If no encounter record exists, prepare a blank capture template and ask
for the notes; never fabricate attendance, duration, sentiment or commitments.

1. Scan actual notes for possible safety/PQC/special-situation content before
   synthesis. Retain source location and original language in the appropriate
   restricted intake; workshop routing remains simulated.
2. Separate HCP statements, MSL observations, interpretation and unanswered questions.
   Quote only attributable text and preserve uncertainty in speaker attribution.
3. Create a concise CRM draft: date/time if supplied, participants, scientific purpose,
   topics, substantive questions, evidence discussed, materials actually used,
   commitments actually made and requested follow-up. Unavailable fields stay blank.
4. Convert explicit commitments into tasks with source IDs. An owner/date not stated
   is proposed or unresolved, not an agreed assignment. Check existing tasks first
   so repeating the job does not create duplicate CRM actions.
5. Route an unresolved scientific question to `medical-information-response` or
   `evidence-gap-analysis`. An individual anecdote does not establish a general signal.
6. Draft a tailored follow-up with source-supported content and permitted materials.
   Preserve unsolicited scope and relevant limitations. Do not send a draft automatically.
7. Present one concise review packet rather than repeatedly interviewing the MSL.
   Include fields requiring confirmation and a diff for any proposed CRM update.

For approved writes, use the actual CRM schema and required fields, an idempotency
key where supported, a preview, then verify the returned record ID/status. An HTTP
request sent without a confirmed result is not a completed write. Local CSV exports
are proposed records, not vendor-certified import files or evidence of a live update.

In workshop mode use interaction records as historical source notes, explicitly
labelled as such. See [MSL workflow](../../docs/msl-workflow.md).
Read `house-rules/msl-post-call-follow-up.md`.
