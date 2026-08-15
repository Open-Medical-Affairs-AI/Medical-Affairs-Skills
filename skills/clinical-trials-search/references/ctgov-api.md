# ClinicalTrials.gov API v2 — Reference

Base: `https://clinicaltrials.gov/api/v2`
Docs: https://clinicaltrials.gov/data-api/api

No key, no registration. The legacy v1 API was retired — anything written
against `/api/query/` no longer works.

---

## Endpoints

| Endpoint | Returns |
|---|---|
| `GET /studies` | Search. Paginated by `nextPageToken`. |
| `GET /studies/{nctId}` | One study in full |
| `GET /studies/metadata` | Field definitions — use this to discover valid field paths |
| `GET /stats/size` | Corpus statistics |

### `/studies` parameters

| Parameter | Notes |
|---|---|
| `query.term` | Free text across all fields; accepts Essie expressions |
| `query.cond` | Condition / disease |
| `query.intr` | Intervention / treatment |
| `query.titles` | Title fields only |
| `query.spons` | Sponsor |
| `query.locn` | Location |
| `query.id` | NCT number or other identifier |
| `filter.overallStatus` | Comma-separated status values |
| `filter.geo` | `distance(lat,long,radius)` |
| `filter.advanced` | Essie expression, e.g. `AREA[Phase](PHASE3)` |
| `fields` | Comma-separated field paths — returns only these. Use it; full records are large. |
| `pageSize` | Max 1000; default 10 |
| `pageToken` | From the previous response's `nextPageToken` |
| `countTotal` | `true` to get `totalCount` |
| `sort` | e.g. `@relevance`, `LastUpdatePostDate:desc`, `EnrollmentCount:desc` |

**Pagination is token-based, not offset-based.** There is no `skip`. Follow
`nextPageToken` until it is absent.

### Essie expressions

Used in `query.term` and `filter.advanced`:

```
AREA[Phase](PHASE2 OR PHASE3)
AREA[OverallStatus]RECRUITING
AREA[LeadSponsorName]"Janssen"
AREA[PrimaryCompletionDate]RANGE[2026-01-01,2027-12-31]
AREA[InterventionType]BIOLOGICAL
```

Combine with `AND`, `OR`, `NOT`. `RANGE[MIN,MAX]` works on date and numeric
fields. This is where the real query power is; the simple `query.*` parameters
are a convenience layer over it.

---

## Response structure

```json
{
  "totalCount": 14,
  "nextPageToken": "NF0g5J...",
  "studies": [ { "protocolSection": {...},
                 "resultsSection": {...},
                 "derivedSection": {...},
                 "hasResults": true } ]
}
```

### `protocolSection` modules

| Module | Key fields |
|---|---|
| `identificationModule` | `nctId`, `briefTitle`, `officialTitle`, `acronym`, `orgStudyIdInfo`, `secondaryIdInfos` (EudraCT, CTIS) |
| `statusModule` | `overallStatus`, `whyStopped`, `startDateStruct`, `primaryCompletionDateStruct`, `completionDateStruct`, `lastUpdatePostDateStruct` |
| `sponsorCollaboratorsModule` | `leadSponsor`, `collaborators`, `responsibleParty` |
| `descriptionModule` | `briefSummary`, `detailedDescription` |
| `conditionsModule` | `conditions`, `keywords` |
| `designModule` | `studyType`, `phases`, `enrollmentInfo{count,type}`, `designInfo{allocation, interventionModel, primaryPurpose, maskingInfo}` |
| `armsInterventionsModule` | `armGroups`, `interventions` |
| `outcomesModule` | `primaryOutcomes`, `secondaryOutcomes` (each with `measure`, `description`, `timeFrame`) |
| `eligibilityModule` | `eligibilityCriteria` (free text), `sex`, `minimumAge`, `maximumAge`, `healthyVolunteers` |
| `contactsLocationsModule` | `locations` with facility, city, country, and investigator contacts |

### `resultsSection`

Present only when results have been posted: `participantFlowModule`,
`baselineCharacteristicsModule`, `outcomeMeasuresModule`, `adverseEventsModule`.

`adverseEventsModule` is genuinely valuable — it carries serious and other
adverse events **with denominators by arm**, which is exactly what FAERS cannot
give you. When a trial has posted results, this beats a publication's abstract
for safety detail.

### `derivedSection`

ClinicalTrials.gov's own derivations, including `conditionBrowseModule` and
`interventionBrowseModule` with MeSH mappings. Useful for linking a registry
record to a PubMed search strategy.

---

## Field selection

Full records are large. Request what you need:

```
/studies?query.cond=multiple+myeloma
  &fields=protocolSection.identificationModule.nctId,
          protocolSection.identificationModule.briefTitle,
          protocolSection.statusModule.overallStatus,
          protocolSection.designModule.phases
  &pageSize=100
```

`GET /studies/metadata` lists every valid path.

---

## Things that will catch you out

- **`whyStopped` is free text and frequently the most informative field in the
  record.** "Terminated — futility" in a competitor's phase 3 is high-value
  intelligence. Analysts who filter out TERMINATED trials never see it.
- **Status is sponsor-maintained and often stale.** Always compare
  `lastUpdatePostDate` against today before treating "Recruiting" as current.
- **`enrollmentInfo.type`** distinguishes `ESTIMATED` (a target) from `ACTUAL`
  (what happened). Reporting an estimate as a result is a real error.
- **Phase does not tell you the design.** A "PHASE2" study may be single-arm and
  open-label. Read `designInfo.allocation` before making any comparative claim.
- **One programme, many NCT records.** Regional and cohort-specific
  registrations are common. Group by programme and say what you are counting.
- **Change history is not in the API.** Only on the web UI at
  `/study/{nctId}?tab=history`. This is where you see a primary endpoint changed
  after enrolment began — a RoB 2 selective-reporting concern that never appears
  in the publication.
- **Coverage is not global.** EU CTIS, ISRCTN, jRCT, ChiCTR, CTRI, and ANZCTR
  carry trials absent here. The WHO ICTRP aggregates across registries and is
  the right cross-check before declaring that nothing is running.
- **No published rate limit**, but be reasonable — throttle bulk jobs.
