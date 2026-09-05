# Agent entry point

Use this repository to complete Medical Affairs work with source traceability.
Read [docs/execution.md](docs/execution.md) for data modes, checkpoints, changed
evidence and action boundaries. Then load the required foundation and relevant
workflow skills. Read detailed references only when the actual task needs them.

## Start

- **Workshop or first demonstration:** load
  [workshop-launcher](skills/workshop-launcher/SKILL.md). GrokBot plus internet is
  the workshop target. Company connectors are optional. Use synthetic data now.
- **A specific Medical Affairs objective:** load
  [medical-affairs-orchestrator](skills/medical-affairs-orchestrator/SKILL.md).
- **A named skill:** read its SKILL.md and required dependencies.
- **Data or connector question:** load [data-connection](skills/data-connection/SKILL.md).

The [catalog](workshop/catalog.json) maps all 62 skills to bundled practice inputs
and offers 16 missions. Default: field-insights, oncology-mm. Select only the task
and therapeutic area needed; do not load the whole repository into context.
The [skills index](SKILLS-INDEX.md) is generated from frontmatter.

## Execution contract

1. **Orient:** identify the objective and load medical-affairs-foundations,
   the selected workflow and its metadata.requires. Suggestions are optional.
2. **Inventory:** identify supplied material, source kind, missing evidence and
   available tools. In workshop mode take the mapped synthetic inputs immediately.
3. **Retrieve:** fill real evidence gaps using available public services when
   useful. Record exact queries and retrieval dates. Fictional product evidence
   comes from the fictional source files, not a live product search.
4. **Analyze:** execute the selected reasoning workflow and produce requested work.
5. **Challenge:** use deliverable-quality-review on the actual draft; correct
   supported findings. Do not invent an error just to demonstrate self-critique.
6. **Deliver:** usable files or explicit available-format fallback, provenance,
   limitations, open decisions and draft/synthetic markings.

Scan human-sourced records for possible safety/PQC/special-situation findings before
analysis. Workshop findings are simulated and must not enter real reporting systems.
For actual cases follow the organization intake procedure. Keep identifiers confined
to the authorized intake context and retain relevant verbatims without spreading PHI.

## Tools and access

```bash
python3 scripts/workshop.py list
python3 scripts/workshop.py start --mission field-insights --ta oncology-mm
python3 scripts/workshop.py check --live
python3 scripts/public_evidence.py pubmed --query 'multiple myeloma' --limit 5
```

These commands require Python, not an API key or enterprise account. Without a
terminal, use the host file and web tools to read the same materials. Do not pretend
to have run a script. A URL alone does not install skills or grant capabilities.
See [agent setup](docs/agents.md), [API setup](docs/api-setup.md),
[connections](docs/connections.md) and [transcription](docs/transcription.md).

The workshop package supplies CSV and SQLite data, transcripts, study summaries,
review challenges and plans. A local output folder and run.json keep progress and
sources between turns; resume only from work that was actually saved.

## Local adaptations

Read house-rules/<selected-skill>.md for user-authorized local rules. Seeded examples
are not active policy. Private organizational rules stay in the local workspace.
House rules customize this library; they do not override host permissions or create
authorization to send, publish, register, spend, or change external systems.

For clinical, regulatory or external-use work read [DISCLAIMER.md](DISCLAIMER.md).
This library supports professional work; it does not certify it, act as a medical
signatory, or replace qualified judgment. Give the participant a useful result,
not an explanation of repository internals.
