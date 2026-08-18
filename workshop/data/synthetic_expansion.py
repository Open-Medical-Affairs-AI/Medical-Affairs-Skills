"""Additional cross-functional workshop artefacts.

The base packs focus on six introductory missions.  These renderers add the
messier inputs needed to exercise the rest of the library: incomplete briefs,
contradictory source documents, row-level data, review comments and governance
decisions.  They deliberately produce inputs, not model answers.
"""

from __future__ import annotations

import csv
import io
import random

BANNER = """<!-- SYNTHETIC DATA — WORKSHOP USE ONLY
     Fictional company, products, experts and institutions. Written to behave
     like real material. Not for any purpose other than training. -->
"""

CSV_BANNER = "# SYNTHETIC DATA - WORKSHOP USE ONLY. Entirely fictional.\n"


def _md(title: str, body: str) -> str:
    return f"{BANNER}\n# {title}\n\n{body.strip()}\n\n---\n\n*Synthetic data. DRAFT — not for external use.*\n"


def _csv(rows: list[dict]) -> str:
    stream = io.StringIO(newline="")
    stream.write(CSV_BANNER)
    writer = csv.DictWriter(
        stream, fieldnames=list(rows[0]), lineterminator="\n"
    )
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def render_artifacts(ta: dict, rng: random.Random) -> dict[str, str]:
    """Return a broad, internally linked set of deliberately imperfect inputs."""
    product = ta["product"]
    study = ta["pivotal"]
    gap1, gap2, gap3 = ta["gaps"][:3]
    lead = ta["kols"][0]["name"]
    result1 = ta["key_results"][0]
    result2 = ta["key_results"][1]
    safety1 = ta["safety"][0]

    evidence_rows = []
    for i, (endpoint, result, role) in enumerate(ta["key_results"], 1):
        evidence_rows.append({
            "source_id": f"EV-{i:02d}", "study": study,
            "design": ta["pivotal_design"], "population_n": ta["pivotal_n"],
            "endpoint": endpoint, "result": result, "role": role,
            "evidence_tier": "synthetic pivotal report", "limitation": "See protocol and SAP; not independently verified",
        })
    for i, (title, sponsor, design, result) in enumerate(ta["congress"][:5], 10):
        evidence_rows.append({
            "source_id": f"EV-{i:02d}", "study": title, "design": design,
            "population_n": "extract from abstract", "endpoint": "reported finding",
            "result": result, "role": "context", "evidence_tier": "congress abstract",
            "limitation": f"Methods incomplete; sponsor: {sponsor}",
        })

    enquiries = [
        {"id":"MI-001","date":"2026-06-03","requester":"Hospital pharmacist","country":"UK","channel":"email","verbatim":f"Is {product} approved for the population in the product profile? Please send dosing and monitoring information.","response_status":"open"},
        {"id":"MI-002","date":"2026-06-05","requester":"Specialist physician","country":"US","channel":"phone","verbatim":f"Unsolicited question: what evidence exists outside the approved population? I treated one patient that way; they were admitted with severe infection two weeks later.","response_status":"escalation not recorded"},
        {"id":"MI-003","date":"2026-06-07","requester":"Nurse","country":"DE","channel":"portal","verbatim":f"The carton seal on {product} was broken when pharmacy opened the shipment. No dose was administered. What should we do with the pack?","response_status":"awaiting response"},
        {"id":"MI-004","date":"2026-06-10","requester":"Specialist physician","country":"FR","channel":"email","verbatim":f"A patient became pregnant during exposure to {product}. Please provide any pregnancy information.","response_status":"forwarded to medical information only"},
        {"id":"MI-005","date":"2026-06-12","requester":"Payer adviser","country":"US","channel":"email","verbatim":"Can you provide an indirect comparison and budget impact estimate for our formulary review?","response_status":"triaged"},
        {"id":"MI-006","date":"2026-06-18","requester":"Patient organisation","country":"ES","channel":"web","verbatim":f"Could you explain the main {study} results without medical jargon?","response_status":"open"},
    ]

    accounts = []
    for i in range(1, 16):
        accounts.append({
            "account_id": f"ACC-{i:03d}", "region": ["North","South","East","West"][i % 4],
            "setting": ["Academic","Community","Integrated network"][i % 3],
            "eligible_patients_estimate": 18 + i * 3, "scientific_need_score": 1 + (i * 3) % 5,
            "access_minutes": 25 + (i * 17) % 180, "last_meaningful_exchange": f"2026-{1 + i % 6:02d}-{5 + i:02d}",
            "open_request": "yes" if i in (2, 7, 11) else "no", "priority_in_current_plan": "High" if i < 9 else "Low",
        })

    metrics = []
    for month in range(1, 7):
        metrics.append({
            "month": f"2026-{month:02d}", "scientific_exchanges": 75 + month * 9,
            "unique_hcps": 44 + month * 2, "repeat_hcp_share": f"{31 + month}%",
            "insights_submitted": 18 + month, "insights_actioned": 2 + (month % 3),
            "requests_closed_on_time": f"{88 + month}%", "publication_milestones_on_time": f"{82 - month * 2}%",
            "note": "Volume target increased in April" if month == 4 else "",
        })

    terminology = [
        {"record":"T-01","verbatim":"bad infection needed a bed","proposed_concept":"serious infection","proposed_code":"DO NOT GUESS","confidence":"low","review_needed":"yes"},
        {"record":"T-02","verbatim":"medicine stopped working","proposed_concept":"lack of therapeutic effect","proposed_code":"DO NOT GUESS","confidence":"medium","review_needed":"yes"},
        {"record":"T-03","verbatim":"pen jammed; dose leaked","proposed_concept":"device malfunction / product quality complaint","proposed_code":"DO NOT GUESS","confidence":"high","review_needed":"yes"},
        {"record":"T-04","verbatim":"used before the labelled line","proposed_concept":"off-label use","proposed_code":"not a MedDRA coding decision","confidence":"high","review_needed":"yes"},
        {"record":"T-05","verbatim":"felt wiped out","proposed_concept":"fatigue OR malaise","proposed_code":"UNRESOLVED","confidence":"low","review_needed":"yes"},
    ]

    patient_rows = []
    for i in range(1, 61):
        arm = "Product" if i % 3 else "Comparator"
        baseline = round(rng.uniform(18, 44), 1)
        change = round(rng.gauss(-8.5 if arm == "Product" else -4.0, 5.5), 1)
        patient_rows.append({
            "patient_id": f"SYN-{i:03d}", "arm": arm, "age_band": ["12-17","18-64","65+"][i % 3],
            "region": ["NA","EU","APAC"][i % 3], "baseline_score": baseline,
            "week16_change": change, "responder": "yes" if change <= -7 else "no",
            "time_to_event_days": 28 + (i * 19) % 340, "event": "1" if i % 5 == 0 else "0",
            "ae_grade3_plus": "yes" if i in (9, 27, 48) else "no",
        })

    artifacts = {
        "structured-evidence-table.csv": _csv(evidence_rows),
        "medical-information-enquiries.csv": _csv(enquiries),
        "field-account-plan.csv": _csv(accounts),
        "medical-impact-metrics.csv": _csv(metrics),
        "terminology-coding-queue.csv": _csv(terminology),
        "patient-level-analysis.csv": _csv(patient_rows),
        "advisory-board-transcript.md": _md(f"Advisory board transcript — {ta['label']}", f"""
**Meeting status:** unapproved working transcript; speaker names are fictional pseudonyms.

**Chair:** Our decision is whether the next evidence investment should address sequencing, implementation, or durability.

**{lead}:** "The {result1[0].lower()} is not the decision problem. {gap1}. Until that changes, another subgroup poster adds nothing."

**Advisor B:** Community adoption is blocked by logistics, not efficacy. A pragmatic study would change our protocol next quarter.

**Advisor C:** I disagree. The proposed pragmatic study is underpowered and duplicates a registry that will report next year.

**Advisor D:** "One patient was hospitalised after {product} with a severe infection; I do not know whether it was related." The case was discussed for six minutes, but the minutes contain no PV routing entry.

**Chair:** The group ranked durability first (6 votes), implementation second (5), and sequencing third (5). Two advisors abstained. The vendor summary says there was "strong consensus for durability."

**Unresolved:** ownership, budget, whether the quoted case was reported, and how abstentions should affect the conclusion.
"""),
        "iis-proposal.md": _md(f"Investigator-initiated study proposal — IIS-26-014", f"""
**Applicant:** {lead}, Fictional Research Hospital  
**Title:** A prospective single-centre evaluation addressing: {gap2}  
**Request:** £780,000 over 30 months; 42 participants  
**Primary endpoint:** "clinical benefit and feasibility" at 12 months  
**Comparator:** none  
**Statistical rationale:** sample described as feasible; no effect size or precision target  
**Recruitment:** 24 eligible patients treated at the centre last year; applicant projects 2/month  
**Data ownership/publication:** investigator owns analysis; sponsor receives a 90-day review period  
**Safety:** protocol says adverse events will be handled "per routine care"  
**Strategic link claimed:** Medical plan imperative 2  
**Known overlap:** a multicentre registry in `integrated-evidence-plan.csv` asks a similar question.

The committee has £1.2m remaining and two other proposals under review. No recommendation is supplied; participants must make and defend it.
"""),
        "rwe-study-concept.md": _md(f"RWE protocol concept — RW-{ta['code']}", f"""
**Decision to inform:** whether practice outside pivotal-trial eligibility needs additional risk-minimisation or implementation support.  
**Target trial question:** outcomes with {product} versus locally selected alternative in routine care.  
**Candidate source:** fictional claims linked to an oncology/dermatology/metabolic EHR network (2019–2026).  
**Eligibility:** broad treated population; index date not yet operationalised.  
**Exposure:** first recorded administration; switching and discontinuation rules absent.  
**Outcomes:** effectiveness, discontinuation and hospitalisation. Outcome validation unknown.  
**Confounding:** disease severity, access, prior therapy and centre experience; several are incompletely recorded.  
**Planned analysis:** propensity-score weighting. Positivity and missing-data diagnostics not specified.  
**Feasibility count:** 620 exposed records before applying eligibility; comparator n=1,840.  
**Known trap:** the draft calls hospitalisation rates "incidence of treatment-related complications," which the data cannot establish.
"""),
        "payer-hta-brief.md": _md(f"Payer and HTA evidence brief — {product}", f"""
**Decision:** fictional national payer reassessment in Q1 2027.  
**Population/comparator:** approved population versus current reimbursed standard.  
**Clinical evidence:** {study}, {ta['pivotal_design']}, n={ta['pivotal_n']}; {result1[0]}: {result1[1]}.  
**Economic model:** partitioned survival, lifetime horizon, 3.5% discounting; utility source is an unpublished mapping analysis.  
**Base-case ICER:** £54,800/QALY.  
**Scenario range:** £31,200–£112,400/QALY; results most sensitive to duration of effect and treatment discontinuation.  
**Budget impact:** assumes 38% uptake in year one despite 12% current class uptake.  
**Evidence problem:** no randomised comparative estimate; proportional-hazards assumption not assessed.  
**Equity consideration:** travel and administration burden may fall disproportionately on rural patients.  
**Draft claim to challenge:** "{product} is cost-effective and reduces hospital use." Neither statement follows without thresholds, uncertainty and comparative data.
"""),
        "guideline-landscape.md": _md(f"Guideline landscape — {ta['label']}", f"""
| Body | Current edition | Next evidence cut-off | Current treatment position | Evidence accepted |
| --- | --- | --- | --- | --- |
| Fictional International Society | 2024 | 2027-03 | Class mentioned; product not named | Published peer-reviewed comparative evidence preferred |
| North Region Network | 2025 | Rolling | Restricted to approved population | Label plus local implementation data |
| Fictional Payer Consortium | 2023 | Unknown | Not assessed | SLR and economic model |

The current medical plan promises "guideline inclusion by Q4 2026," before the international body's evidence cut-off. Committee membership and conflict-of-interest rules have not been checked. The relevant evidence-readiness issue is `{gap1}`.
"""),
        "launch-readiness-register.md": _md(f"Launch readiness register — proposed label expansion for {product}", """
**Target decision date:** 15 February 2027 (planning assumption, not confirmed by regulator)

| Workstream | RAG | Evidence offered | Owner | Dependency |
| --- | --- | --- | --- | --- |
| Scientific narrative | Green | Draft platform v0.7 | Scientific Comms | Final label |
| Medical information | Amber | 8 of 20 response documents drafted | MI lead | Final label and safety tables |
| Field training | Green | 92% module completion | Field Excellence | Assessment only tests recall |
| Safety readiness | Red | Escalation reconciliation not rehearsed | PV liaison | SOP simulation |
| Evidence dissemination | Amber | Manuscript submitted, not accepted | Publications | Journal timeline |
| Stakeholder mapping | Green | 45 priority experts | Field lead | Consent and access checks |

The steering committee currently reports overall status as **Green** by averaging workstream scores. No documented gate criterion defines which red item is launch-blocking.
"""),
        "medical-education-needs.md": _md(f"Independent medical education needs assessment — {ta['label']}", f"""
**Observed practice gap:** variable confidence applying evidence to populations under-represented in {study}.  
**Evidence of need:** 14/54 field observations ask about selection or implementation; three are duplicate reports from the same contact. No formal learner survey has been completed.  
**Target learners:** specialists and multidisciplinary teams in community settings.  
**Proposed learning objective:** "Understand {product} and increase its use." This is not an acceptable independent educational objective and should be rewritten around competence or practice.  
**Proposed format:** two 60-minute case-based virtual sessions with pre/post assessment and 90-day commitment-to-change follow-up.  
**Faculty:** three experts, two of whom participated in the product programme.  
**Independence issue:** the draft agenda was copied from a branded internal symposium.  
**Outcome limitation:** attendance alone cannot demonstrate practice change.
"""),
        "promotional-claims-review.md": _md(f"Medical review exercise — draft claims for {product}", f"""
Review each proposed claim against the supplied evidence, indication, prominence of qualification and audience.

| ID | Proposed copy | Cited support | Deliberate issue |
| --- | --- | --- | --- |
| C-01 | "{product}: the new standard for every eligible patient" | {study} | Universal superiority claim from {ta['pivotal_design']} |
| C-02 | "{result1[0]}: {result1[1]}" | {study} | Check design, denominator, endpoint hierarchy and context |
| C-03 | "Proven safer" | Overall discontinuation table | Undefined comparator and selective safety framing |
| C-04 | "Works fast" | Exploratory analysis | Vague endpoint; exploratory status omitted |
| C-05 | "Ask about use before the approved population" | None | Proactive off-label suggestion |
| C-06 | "{safety1[0]} occurred in {safety1[1]}" | Product profile | Accurate number, but severity/context and fair balance absent |

The footer says "For scientific exchange only," but the audience list includes sales representatives and the call to action is commercial.
"""),
        "safety-case-series.md": _md(f"Safety communication source cases — {product}", """
These are unvalidated intake fragments for detection and communication practice, not a case assessment.

1. **CASE-01:** "Patient was admitted overnight with a severe infection 12 days after the second dose; recovered after IV treatment." Age, indication, reporter contact and causality are missing.
2. **CASE-02:** "The injector would not deploy and liquid ran down the patient's arm. We cannot tell how much dose entered." Lot number and device return status are missing.
3. **CASE-03:** "Pregnancy test became positive during treatment; outcome not yet known." Last dose and estimated gestation are missing.
4. **CASE-04:** "Patient accidentally received the scheduled dose twice. No symptoms so far." Timing, dose and follow-up are missing.

The source spreadsheet marks CASE-02 and CASE-04 as "not an AE" and therefore closed. Participants should challenge that routing logic and preserve each verbatim report.
"""),
        "scientific-platform-draft.md": _md(f"Scientific platform draft v0.7 — {product}", f"""
**Scientific narrative:** Patients need an option that combines meaningful outcomes with practical delivery. {product} was designed around `{ta['moa']}`.

| Statement | Support | Status noted by author |
| --- | --- | --- |
| The disease imposes substantial burden | No source supplied | Approved |
| {product} delivers {result1[0].lower()} of {result1[1]} | {study} | Approved |
| Benefits are durable across all subgroups | Secondary analyses | Approved |
| {product} has a manageable safety profile | Product profile | Approved |
| The evidence supports earlier use | Mechanistic rationale | Proposed |

**Lexicon:** prefer "meaningful," "transformative," and "best-in-class"; avoid "single-arm" in headings.

This is intentionally flawed: substantiation, design limitations, audience decisions and non-promotional language all need review.
"""),
        "manuscript-draft.md": _md(f"Manuscript source draft — 24-month follow-up of {study}", f"""
## Abstract
At 24 months, {product} demonstrated durable and clinically meaningful benefit with no new safety signals.

## Methods
This follow-up of a {ta['pivotal_design']} enrolled {ta['pivotal_n']} participants. The analysis cut-off and estimand are not stated here. Missing patient-reported outcomes were treated as missing at random.

## Results
{result1[0]} was {result1[1]}; {result2[0]} was {result2[1]}. The draft results table uses n={ta['pivotal_n'] - 3}, while the methods use n={ta['pivotal_n']}. Three deaths after discontinuation are absent from the safety summary pending reconciliation.

## Discussion
The results prove superiority to available treatment and support earlier use. This overreaches the design and approved indication. Limitations currently contain one sentence.

**Authorship status:** six proposed authors; contribution statements and protocol access not collected.  
**References:** placeholders `[REF1]`–`[REF8]`; no citations should be invented to fill them.
"""),
        "abstract-poster-brief.md": _md(f"Congress abstract and poster brief — {study}", f"""
**Congress:** Fictional Annual Scientific Meeting 2027  
**Abstract limit:** 300 words excluding title; one table; no trade names in title  
**Poster:** 16:9 landscape PowerPoint; QR codes allowed only to congress-hosted content  
**Data cut:** 30 June 2026  
**Required result:** {result1[0]} — {result1[1]}  
**Required limitation:** {ta['pivotal_design']}; no causal comparative claim  
**Draft title from team:** "{product} transforms outcomes and sets a new standard"  
**Problem:** promotional wording, trade name and claim unsupported by design.  
**Missing:** author approvals, exact denominator for one subgroup, statistical-analysis version and encore status.
"""),
        "plain-language-source.md": _md(f"Plain-language summary source — {study}", f"""
**Audience:** adults and adolescents reading at approximately an 8th-grade level; translations planned.  
**What was studied:** {ta['indication']}.  
**Design:** {ta['pivotal_design']}; {ta['pivotal_n']} people.  
**Main result:** {result1[0]} was {result1[1]}.  
**Important harms:** {safety1[0]} was reported in {safety1[1]} ({safety1[2]}).  
**Uncertainty:** `{gap3}`.  
**Team's problematic draft sentence:** "The medicine worked and was safe for most people." It removes the comparator/design context and compresses safety into a value judgement.  
**Missing from source:** participant flow, absolute numbers for all outcomes and contact route for questions.
"""),
        "mlr-review-comments.md": _md(f"MLR review history — scientific deck SD-{ta['code']}-07", """
| Cycle | Reviewer | Comment | Team response | Status |
| --- | --- | --- | --- | --- |
| 1 | Medical | Add study design and denominator to every result | Added on appendix only | Open |
| 1 | Legal | "Best" is unsupported and implies superiority | Changed to "leading" | Open |
| 1 | Regulatory | Off-label population appears before approved indication | "Scientific exchange" footer added | Open |
| 2 | Medical | Safety slide lacks exposure duration and severity | Font reduced; no content added | Open |
| 2 | Legal | Reference 7 cannot be retrieved | Replaced with "data on file" | Open |
| 2 | Regulatory | Audience and intended use conflict | No response | Open |

The content owner marked the asset "ready for approval" because all comments have a response. Participants must distinguish response completion from issue resolution and build a claim–evidence matrix.
"""),
        "integrated-evidence-plan.csv": _csv([
            {"work_id":"IEP-01","question":gap1,"decision":"guideline evidence readiness","design":"comparative study","owner":"Clinical Development","cost_gbp":"4200000","start":"2027-Q1","readout":"2029-Q4","status":"concept","dependency":"regulatory alignment"},
            {"work_id":"IEP-02","question":gap2,"decision":"implementation protocol","design":"prospective pragmatic cohort","owner":"Medical Affairs","cost_gbp":"900000","start":"2026-Q4","readout":"2028-Q1","status":"proposed","dependency":"site feasibility"},
            {"work_id":"IEP-03","question":gap2,"decision":"publication narrative","design":"investigator-initiated single-centre cohort","owner":"IIS Committee","cost_gbp":"780000","start":"2027-Q1","readout":"2029-Q2","status":"under review","dependency":"IIS-26-014"},
            {"work_id":"IEP-04","question":gap3,"decision":"payer reassessment","design":"claims-EHR comparative RWE","owner":"HEOR","cost_gbp":"650000","start":"2026-Q3","readout":"2027-Q3","status":"feasibility","dependency":"outcome validation"},
            {"work_id":"IEP-05","question":"24-month safety and durability","decision":"scientific communication","design":"existing trial follow-up analysis","owner":"Publications","cost_gbp":"120000","start":"2026-Q2","readout":"2026-Q4","status":"drafting","dependency":"data reconciliation"},
        ]),
        "document-ingestion-challenge.md": _md(f"Scanned-source transcription challenge — {product}", f"""
> This file simulates imperfect OCR extracted from a supplied PDF. Preserve uncertainty rather than silently correcting it.

**Page 3:** "Primary endp0int: {result1[0]}; ana1ysis population N={ta['pivotal_n']}."  
**Page 7 table:** "{result1[1]}" but the footnote says "95% Cl" (letter l, not I).  
**Page 9:** Safety denominator appears as `N={ta['pivotal_n'] - 2}`; reason for difference is cut off.  
**Page 11 image:** chart labels are not captured in extracted text.  
**Handwritten margin:** "3 deaths after cutoff? reconcile" (low-confidence transcription).  

Task material should identify what can be extracted, what requires page-image inspection, and which claims cannot be used until reconciled.
"""),
    }
    return artifacts
