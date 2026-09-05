# Give MSLs more time for scientific engagement

The agent handles gathering, organizing and preparing records so the MSL can
concentrate on HCP conversations, scientific questions and unmet needs.

| When | Agent work | Skill |
|---|---|---|
| Build coverage | Find relevant professional profiles, verify identity and identify missing perspectives | hcp-discovery-and-access |
| Plan access | Check institution procedures, existing relationships and permitted introduction routes | hcp-discovery-and-access; field-medical-planning |
| Before the meeting | Gather prior notes, open questions, evidence, access context and current materials | msl-pre-call-planning; kol-engagement-brief |
| During/after | Process actual supplied notes or a permitted recording | meeting-transcription; msl-post-call-follow-up |
| Close the loop | Prepare CRM notes, follow-up drafts and a deduplicated task queue | msl-post-call-follow-up; msl-administrative-operations |
| Weekly | Summarize commitments, unresolved scientific needs, coverage gaps and time constraints | msl-administrative-operations; medical-affairs-metrics |

## One request to start

```text
Use the Medical Affairs Skills repository to prepare my next HCP engagement.
In workshop mode use oncology HCP-138. Gather the prior interactions, open
tasks and access context, create a one-page pre-call brief, and propose three
neutral scientific questions. Prepare the administrative records as drafts.
Do not invent a meeting date, HCP statement or completed follow-up.
```

With Python, the helper collects the records first:

```bash
python3 scripts/msl_admin.py --ta oncology-mm --hcp HCP-138 --out outputs
```

The packet contains context.json, proposed-tasks.csv and PRE-CALL.md. The helper
does not synthesize the scientific brief; the agent does that using the skill.
Repeated preparation produces the same proposed task keys, allowing reconciliation
instead of duplicate task creation. No company account is needed for this exercise.

## Real HCP discovery and access

Use public institutional profiles, scientific publications, trial listings and
published conference programs. Verify identity before joining information. Propose
access through legitimate institutional procedures and relevant scientific networks.
Do not infer sales potential, prescribing behavior, private contact details or
personal vulnerabilities. A coauthor is not automatically a personal introduction.

An access plan helps identify relevant HCPs and appropriate next steps; it cannot
guarantee access. Respect declines and local contact rules. The MSL owns the purpose
and relationship. Scientific needs, not product uptake, guide prioritization.

## Automating administration in a real tenant

Use [connections.md](connections.md) to connect authorized CRM, calendar and file
sources. Start with a readable preview and map fields to the actual tenant schema.
When the user has authorized a specific write/send action, the host tools can execute
it and verify the returned status. Otherwise prepare the complete draft packet.
The repo does not ship credentials, an email sender, a scheduler or a live CRM session.

Track the difference between a task proposed, assigned, attempted and confirmed done.
Do not pre-write post-call facts from a pre-call plan. Expense and time records need
actual supplied evidence; no invented receipts, visits or hours.
