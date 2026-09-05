# Workshop readiness record

Checked on 5 September 2026. This records engineering checks, not clinical
validation or a completed rehearsal on the workshop's GrokBot deployment.

| Check | Result |
|---|---|
| Skill structure and bundled input coverage | 62 skills; no validation errors |
| Workshop behavior | 17 tests passed, including preparation of all 16 missions in all 3 therapeutic areas |
| Existing API client fixtures | 25 tests passed |
| Output format fallbacks | 12 tests passed |
| Live public retrieval | PubMed, ClinicalTrials.gov, openFDA labels, openFDA FAERS, Europe PMC and Crossref returned results |
| Curated public examples | 9 deliberately selected DOI/title matches; metadata only |
| Practice database | Foreign keys and numerical constraints checked; writes and attachments rejected by the query helper |
| MSL helper | Traceable pre-call context and stable task keys; no invented meeting facts or external writes |
| README visual | Generated infographic inspected; capability menu regenerated for 62 skills |

Live checks are point-in-time observations. A successful retrieval does not verify
that a source supports a particular scientific claim. The 48 mission preparations
check routing and inputs; they are not 48 completed scientific outputs.

## Before the October session

Rehearse the first mission on the exact GrokBot deployment using the
[runbook](../workshop/OCTOBER-RUNBOOK.md). Confirm repository or uploaded-file
reading, public web access, output download and any terminal capability. The
self-contained starter files support hosts that cannot clone the repository.

Native audio transcription and optional local Whisper require an actual audio
rehearsal; supplied transcript import has been tested. Enterprise connections are
documented integration paths, not installed tenant credentials or working CRM
sessions. No real outreach, CRM updates or safety reports were submitted.

The owner must activate and verify the [GitHub governance settings](repository-governance.md).
CODEOWNERS alone does not enforce review. Organization membership and all access
paths could not be audited through the available integration.

## Reproduce

```bash
python3 scripts/build_index.py --check
python3 scripts/validate_skills.py
python3 scripts/selftest_workshop.py
python3 scripts/selftest_apis.py
python3 scripts/selftest_fallbacks.py
python3 scripts/workshop.py check --live
```

The first five commands are suitable for CI. The live check depends on upstream
availability. Review scientific deliverables separately with the workshop rubric.
