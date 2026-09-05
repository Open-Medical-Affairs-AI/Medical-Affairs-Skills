# October workshop: from one request to coordinated work

**Default duration: 120 minutes. Target environment: GrokBot with internet.**
Participants use fictional data on personal/workshop devices. Company connectors
and API keys are not prerequisites. Do not use real company or patient material.

## Before the session

1. Rehearse on the actual GrokBot instance and participant account type. Paste the
   README prompt in a fresh session. Verify it can fetch GitHub, read files and
   either produce files or give clear structured content. Record the host/version.
2. If the host can execute Python, run `python3 scripts/workshop.py check --live`.
   Test a small real query, not just network connectivity. Shared-IP rate limits
   matter when a room starts together; stagger live searches and keep limits small.
3. Prepare the three starter bundles and a repository ZIP for upload fallback.
   Put a stable release URL on the event slide once a release has been approved.
4. Test the preferred output formats. Transcripts are supplied; audio installation
   is optional and should not consume workshop time.
5. Open the change cards and scorecard. Keep facilitator evaluation prompts out of
   the participant task context. They are public files, not access-controlled secrets.
6. Confirm the bot context/run limits and how participants retrieve saved outputs.
   A Python preflight does not prove a live agent can complete a mission.

## Run of show

| Minutes | Activity | Participant outcome |
|---|---|---|
| 0–10 | Explain the objective, paste the starter, establish synthetic mode | A task underway |
| 10–30 | First mission in oncology, immunology or cardiometabolic | A source-grounded brief |
| 30–45 | Add one local rule and request a revision | A visibly improved result |
| 45–55 | Demonstrate a live literature query and citation/source checking | Understand retrieved vs verified |
| 55–85 | Run the 30-day capstone in teams | Coordinated draft outputs |
| 85–105 | Introduce a change card; request impact analysis and revisions | Updated work with change traceability |
| 105–120 | Show-and-tell and judging | Explain where human judgment mattered |

## Team allocation

Use the 16 missions in `catalog.json`. For six tables, start with field insights,
KOL meeting, congress, medical information, evidence investment and publication.
Use different therapeutic areas to compare reasoning, not just output wording.
Fast teams can try connected planning, patient partnership or launch readiness.

## Teach one local rule

Ask each team to state a real preference such as “MSL briefs are two pages,”
“Separate observations from insights,” or “Every action has an accountable role.”
The agent can apply the rule from the conversation. File-capable hosts may store
it in a local house-rules file. No one edits the official public repository.
Do not add fabricated policy or confidential SOPs to the workshop.

## Capstone prompt

```text
Using this repository and the synthetic data for our therapeutic area, prepare
the next 30 days of Medical Affairs work. Choose the important priorities,
create a leadership brief, action tracker and scientific briefing, and keep
track of which sources each output depends on. Use the thirty-day-capstone
mission. Complete the supported work and identify the decisions still needed.
```

Then give one [change card](change-cards/README.md):

```text
This new information has arrived. Identify which conclusions and files it
affects. Update the relevant work, preserve the old version, and show me the
changes with their reasons. Tell me what still cannot be determined.
```

## Judge outcomes

Use the existing scorecard plus the [behavioral rubric](evaluation/rubric.md).
Do not reward invented certainty, extra files, fabricated safety findings or merely
announcing that a review occurred. The participant must inspect the actual draft.
No external message, CRM update, publication or real safety report is part of the exercise.

## Recovery prompts

- “Use the supplied synthetic sources. Continue without live APIs.”
- “Give the complete brief here if you cannot create the file.”
- “Show what is already saved and the next unfinished step.”
- “Which source supports that number? Keep it unresolved if none does.”

End by asking: **What decision did the agent help you make, and what still required
your expertise?**
