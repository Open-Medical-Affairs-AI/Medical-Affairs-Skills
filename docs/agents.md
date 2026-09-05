# Give the skills to your agent

The workshop uses **GrokBot with internet**. These instructions are portable text;
what the agent can execute depends on the host that is running it.

## GrokBot: the participant path

1. Open the workshop-provided GrokBot.
2. Paste the starter prompt from the README.
3. Let it retrieve this repository, read AGENTS.md, and select a mission and inputs.
4. It should produce a short plan and start the task, using synthetic materials.
5. Ask for a different therapeutic area or your own Medical Affairs objective.

If it cannot fetch GitHub, upload the repository ZIP using **Code → Download ZIP**
on GitHub, or one of the self-contained starter files in `workshop/bundles/`.
The bot needs to be able to read uploaded files for that path. If it has neither
URL retrieval nor file upload, paste a starter bundle within its context limits.

If it has a shell, the agent can clone the repository itself:

```bash
git clone https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills.git
cd Medical-Affairs-Skills
python3 scripts/workshop.py check --live
```

Reading a link does not install software or grant permissions. The agent should
use its actual tools, state gaps briefly and deliver useful supported content.
The workshop host must be tested by the facilitator before the session.

## Other agents

| Environment | Starting route | Capability to verify |
|---|---|---|
| Claude Code | Clone/read AGENTS.md; optional marketplace install below | Shell, allowed network and file creation |
| Claude with file upload | Upload starter bundle or permitted repository files | File reading, tools and output limits for that product |
| Codex coding environment | Open/clone repository and read AGENTS.md | Network permissions, Python and output access |
| GrokBot or another autonomous host | Repository URL or local checkout | Fetch, shell, files, long-run persistence and scheduling |
| Chat-only environment | Upload/paste a starter bundle | May deliver text but not execute scripts or unattended work |

Optional Claude Code marketplace route, subject to the current host/plugin support:

```text
/plugin marketplace add Open-Medical-Affairs/Medical-Affairs-Skills
/plugin install medical-affairs-skills@open-medical-affairs-ai
```

For portable Markdown use, no plugin installation is required. Keep the directory
structure because skills reference shared materials. Installing one isolated
SKILL.md without its dependencies is not equivalent to installing the repository.

## Honest compatibility status

Repository scripts and fixtures can be tested in the build environment. That is
separate from a live GrokBot, Claude or Codex product test. Record the exact host,
version/date, account tier if relevant, first-run time, successful mission, file
outputs and limits in the facilitator rehearsal. No host is labelled certified.
