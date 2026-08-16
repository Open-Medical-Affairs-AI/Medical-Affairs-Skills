---
name: field-medical-planning
description: >-
  Plan the field medical function over a cycle — territory and account
  prioritisation, MSL objectives, engagement planning across a stakeholder map,
  capacity modelling, and the metrics that describe scientific impact rather
  than activity volume. Use for annual or quarterly field planning, sizing or
  redesigning territories, setting MSL objectives, planning coverage of a
  congress or a launch, or reviewing whether a field plan is realistic. This is
  the plan across many interactions; `kol-engagement-brief` prepares one meeting.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: workflow
  maturity: stable
  requires:
    - medical-affairs-foundations
    - strategic-analysis
  suggests:
    - kol-engagement-brief
    - field-insight-synthesis
    - medical-affairs-metrics
    - deliverable-quality-review
  produces: Field medical plan with prioritised accounts, objectives and capacity
---

# Field Medical Planning

A field plan answers three questions: who we need scientific relationships with
and why, what those relationships are meant to achieve, and whether the team we
have can actually do it. Most field plans answer the first, gesture at the
second, and skip the third.

## Start from the objective, not the list

The failure mode is a plan that begins with a list of names and works forwards.
Begin instead with what the medical strategy needs from the field this cycle —
from `medical-strategy-plan` if one exists. Typically some combination of:

- Understanding something the organisation does not currently understand
  (feeding `evidence-gap-analysis` and `field-insight-synthesis`)
- Supporting evidence generation — site identification, feasibility, IIS pipeline
- Ensuring the scientific narrative is understood accurately where it matters
- Being available to answer questions the field is being asked
- Building the relationships that make the above possible over years, not months

Each objective then determines who, which is the reverse of the usual order and
produces a much shorter list.

## The stakeholder map

"KOL" is too coarse to plan with. Segment by the role someone plays relative to
your objectives:

| Type | What they influence | What they need from you |
|---|---|---|
| **Clinical trial investigators** | Evidence generation, feasibility, recruitment | Protocol clarity, operational responsiveness, data back |
| **Guideline and society panellists** | Practice standards, on their own cycle | Published evidence, and nothing that looks like lobbying |
| **Formulary and P&T decision-makers** | Access | Comparative and economic evidence — see `payer-value-dossier` |
| **High-volume treaters** | Practice, and what the questions actually are | Practical clinical detail, sequencing, management of specific situations |
| **Emerging experts** | The next cycle | Genuine scientific engagement before they are obvious |
| **Regional and community leaders** | Practice outside academic centres, where most patients are treated | Applicability of academic evidence to their setting |
| **Patient organisations** | Patient-facing understanding | Plain-language material — see `plain-language-summary` |

**Academic influence and prescribing influence are different things.** A plan
built entirely from publication counts systematically over-weights academic
centres and under-weights the community setting where most patients are treated.
Say which kind of influence each prioritisation reflects.

## Prioritisation that survives contact

Force distinction — a plan where everyone is tier 1 is not a plan. Prioritise
against explicit criteria, and record them:

- **Relevance to this cycle's objectives** — the dominant criterion
- **Influence**, stated as influence *over what* and on whom
- **Scientific engagement** — willingness to engage substantively, not
  receptiveness to a message
- **Current relationship state** and what would move it
- **Reachability** — an influential person who will not meet you is not a plan
- **Coverage gaps** — geographies, settings or specialties currently unserved

**Interaction frequency is not a target.** A quarterly cadence applied uniformly
produces meetings with no purpose, which damages the relationship it was meant
to build. Plan the *reason* for the next interaction; if there is not one, the
correct plan is no interaction.

## Capacity — the part that makes the plan real

Model it explicitly, because this is where plans quietly become fiction.

Per MSL, per quarter: working days, minus congresses, internal meetings,
training and administration, gives available field days. Multiply by realistic
interactions per field day — including travel in the territory — to get
capacity. Then compare with the plan.

Account for the work that is not an interaction: preparation (a substantive
scientific meeting needs real preparation, and `kol-engagement-brief` assumes
it), insight capture and write-up, follow-up on questions, medical information
requests generated by meetings, congress attendance, and internal reporting.
Teams routinely plan interaction volume as though it were the whole job, and
insight quality is the first thing that degrades when it is not.

If the plan exceeds capacity, cut the plan. Recording the cut — what falls below
the line and what the organisation loses by it — is more useful than a plan that
silently will not happen.

## Territory design

Balance on the work, not the map. Consider account count and complexity, travel
burden and geography, therapeutic area breadth, trial site load, and language
where relevant. Revisit when the portfolio changes rather than annually by
default; territory churn destroys relationships that took years to build, and
that cost is rarely counted against the redesign that caused it.

## MSL objectives that are not activity counts

Objectives should describe what changes, be within the MSL's influence, and be
assessable without counting. Some that work:

- *"Establish, across the top 12 accounts in the territory, what would need to
  be true for them to use the sequencing approach the guideline now recommends;
  report the barriers by Q3"* — an understanding objective
- *"Identify and qualify three sites capable of enrolling the planned Phase 3
  in the community setting"* — an evidence-generation objective
- *"Ensure the five investigators in territory can accurately state the trial's
  primary endpoint and its limitations"* — a comprehension objective, assessable
  by asking

Contrast: *"conduct 120 KOL interactions"*, which is satisfied by 120 meetings
that changed nothing.

## The compliance boundary in field planning

Field medical is non-promotional. Several planning practices erode that,
sometimes without anyone deciding to:

- **Targeting by prescribing data.** Where MSL planning uses commercial
  targeting data, the function's independence is compromised in fact whatever
  the SOP says. Check what the prioritisation is actually built from.
- **Shared objectives with sales.** Aligning on an account is normal; sharing a
  volume objective is not.
- **Message deployment.** A "key message" cascade to the field converts
  scientific exchange into promotion. The field carries scientific content and
  answers questions; it does not deliver messages.
- **Sales-directed activity.** Requests routed from commercial to an MSL for a
  specific customer need a medical rationale and a medical decision.

Field notes are among the highest-yield sources of unreported adverse events.
Every interaction record is scanned — `medical-affairs-foundations` — and the
plan must include the time to do it.

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus:

- Does every prioritised account trace to an objective, and every objective to
  something the medical strategy needs?
- Is the plan inside capacity, with the below-the-line list stated?
- Are the objectives assessable without counting interactions?
- Is prioritisation built on scientific relevance, or on prescribing volume
  wearing scientific language?
- Does the plan include time for insight capture, preparation and follow-up?
- Would an MSL reading this know what to do on Monday?

## Before you finish

Read `house-rules/field-medical-planning.md`. Territory models, what data the
field may use for planning, and the medical/commercial boundary are heavily
company-specific, and several organisations operate under commitments that
restrict field planning inputs more tightly than the general standard.
