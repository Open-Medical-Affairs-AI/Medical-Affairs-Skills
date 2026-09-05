---
name: literature-surveillance
description: >-
  Run ongoing literature and evidence surveillance — a repeatable watch on
  a topic, product, class or competitor that reports what is NEW since the
  last cycle and what it changes, rather than a one-off search. Use for
  weekly or monthly literature updates, "keep me posted on X", building or
  refreshing a surveillance strategy, congress-season monitoring, or when
  someone asks what has been published since a date. For a single
  point-in-time search, use pubmed-search directly instead.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.1.0"
  tier: workflow
  maturity: beta
  requires:
    - medical-affairs-foundations
    - evidence-appraisal
    - citation-integrity
  suggests:
    - pubmed-search
    - clinical-trials-search
    - regulatory-label-intelligence
    - competitive-intelligence
    - deliverable-quality-review
  produces: Surveillance cycle report with delta, appraisal and implications
  network: [eutils.ncbi.nlm.nih.gov, clinicaltrials.gov, api.fda.gov]
---

# Literature Surveillance

A surveillance cycle answers one question: **what is new since last time,
and what does it change?** A report that re-describes the known landscape
each cycle trains its readers to stop reading — the delta is the product.

A recurring request needs a supported host scheduler. Verify a created schedule
and next run before saying surveillance is active; otherwise deliver the current
cycle and reusable strategy. Track publication date separately from indexing date;
use an overlap window with ID deduplication to catch delayed indexing and corrections.

## The strategy, written once

A watch is only as good as its written strategy. Before the first cycle,
fix and record:

- **Scope.** Product, class, competitors, indication, and the adjacent
  topics that matter (mechanism, biomarker, guideline movement). Name what
  is deliberately out of scope — scope creep is how a watch becomes noise.
- **Queries, verbatim.** The exact PubMed strategy (MeSH + free text, via
  `medical-terminology-mapping` if the vocabulary is unsettled), the
  ClinicalTrials.gov filters, and the openFDA scope if labels and FAERS are
  watched. The same queries run every cycle; a changed query is a versioned
  change, noted in the report, or the delta stops meaning anything.
- **Cadence and date anchoring.** Use `--from`/publication-date filters off
  the **last cycle's run date**, not "last 30 days" — drifting windows drop
  papers at the boundary. Record every run date.
- **Triage thresholds.** What earns full appraisal versus a listing line —
  by design (randomised and large RWE always appraised), by topic (anything
  safety always appraised), by source tier.

## The cycle

1. **Run the recorded queries** with the date anchor. Screen as tables
   first — `--format table`, never `--abstracts` on the full result set —
   then fetch only what passes triage.
2. **Safety scan before anything else.** New signals, case reports, FAERS
   movement, label changes in the watched class surface at the top of the
   report, verbatim finding first. A surveillance report that buries a
   safety finding under efficacy news has failed at its one structural job.
3. **Appraise what passed triage** (`evidence-appraisal`): design, N,
   endpoint, the finding, the limitation that most constrains it.
4. **State the delta.** Three bins, explicitly: **changes what we believe**
   (rare — say what belief, and what should happen next), **strengthens or
   weakens a known position** (the usual case — name the position), **noted,
   no action** (the honest majority). An empty first bin is a normal,
   reportable result: "nothing this cycle changes our position" is
   information, not filler.
5. **Route what leaves the report.** A competitive finding feeds
   `competitive-intelligence`; a gap confirmed feeds `evidence-gap-analysis`;
   a KOL's new paper feeds the next `kol-engagement-brief`. Surveillance
   that terminates in its own PDF changes nothing.

## The report

Lead with a five-line executive read: cycle dates, volume screened, items
appraised, safety scan result stated explicitly even when negative, and the
single most consequential item. Then safety, then the delta bins, then the
listing. Recurring reports benefit from `interactive-html-report` — a
filterable table outlives a static list — and take the
`consulting-grade-design` language either way.

Every cycle ends with provenance: queries verbatim, run dates, counts at
each triage stage, and items deliberately excluded with the reason. The next
cycle — possibly run by someone else, or by a different agent — must be able
to reproduce this one from the report alone. That reproducibility is the
difference between surveillance and a sequence of unrelated searches.

## Failure modes

- **Volume as value.** Forty listed abstracts with no triage is cost
  disguised as diligence. The reader pays attention only for the delta.
- **Silent query drift.** Rewording a query mid-stream invalidates every
  cross-cycle comparison. Version it, note it, restate the baseline.
- **Missing-cycle gaps.** A skipped month leaves an unwatched window unless
  the next run anchors to the last **run date**, not the calendar.

## Before you finish

Read `house-rules/literature-surveillance.md` — cadence, distribution lists
and mandatory-appraisal topics are house decisions, and theirs win.
