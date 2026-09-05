---
name: workshop-launcher
description: >-
  Start a Medical Affairs workshop from a repository link or a simple request. Use when a participant wants a first mission, has no company connectors, needs synthetic data selected, or wants to resume workshop work. Select a small useful task, orient the agent and produce actual draft deliverables.
license: Apache-2.0
metadata:
  version: "0.2.0"
  tier: orchestrator
  maturity: beta
  requires:
    - medical-affairs-foundations
  produces: A prepared and executed synthetic workshop mission
---

# Workshop Launcher

Participants have GrokBot and internet. Check what this particular host can read,
execute and save; do not assume a browser chat has a terminal or background jobs.

1. Read [the participant quickstart](../../workshop/PARTICIPANT-QUICKSTART.md).
2. Use the task the participant gave. If none, start `field-insights` in oncology;
   invite a therapeutic-area change while continuing. Do not ask for a skill name.
3. Read [catalog.json](../../workshop/catalog.json), selecting only the relevant
   mission and inputs. For a named skill use its `skill_inputs` entry.
4. With Python, run `python3 scripts/workshop.py start --mission field-insights
   --ta oncology-mm` as one command from the repository root. Without Python,
   read the same input files directly using available file tools.
5. Follow [execution.md](../../docs/execution.md) and the selected workflow.
   The launcher prepares inputs; you must do the analysis and create the outputs.
6. Use public APIs only when they add useful real-disease context. The synthetic
   mission works without them. No enterprise account is needed.
7. Deliver one useful result before offering a larger capstone.

If the URL cannot be fetched, ask for the repository ZIP or the selected mission
bundle. Do not invent its contents. If outputs cannot be saved, deliver labelled
structured content in the conversation. See [compatibility](../../docs/agents.md).
Read `house-rules/workshop-launcher.md` if customized by the participant.
