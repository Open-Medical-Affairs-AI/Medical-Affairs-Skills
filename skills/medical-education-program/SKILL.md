---
name: medical-education-program
description: >-
  Design independent medical education and company-organised scientific
  education — IME grant strategy, curricula, needs assessments, speaker
  programmes and their governance, symposia and preceptorships. Use when
  planning or reviewing an education programme, assessing an IME grant
  request, building a curriculum, or designing speaker training. The whole
  discipline turns on which side of the independence line a programme sits:
  independent education the company funds but does not control, versus
  company-organised education it does. Getting that wrong is the single
  largest source of enforcement exposure in Medical Affairs.
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
    - evidence-gap-analysis
    - scientific-communication-strategy
    - medical-affairs-metrics
    - deliverable-quality-review
  produces: Education programme design, needs assessment and governance plan
---

# Medical Education Program

Two entirely different activities share this name, and conflating them is how
companies end up under a Corporate Integrity Agreement.

## The independence line

Establish which of these you are designing **before anything else**. Every rule
below depends on the answer.

| | Independent medical education (IME/CME) | Company-organised education |
|---|---|---|
| **Who controls content** | The accredited provider, independently | The company |
| **Who selects faculty** | The provider | The company |
| **Company role** | Funds via a grant, then steps back | Designs, delivers, is accountable |
| **Company input on content** | **None.** Not suggestions, not review, not "scientific accuracy checks" beyond what the provider requests through their own process | Full — and full responsibility |
| **Promotional?** | No — must be free of company influence | Depends: MSL-delivered scientific exchange is non-promotional; commercially organised education generally is |
| **Governed by** | ACCME Standards for Integrity and Independence, EACCME, national accreditors | Company SOPs, promotional review, OIG guidance |

**The failure mode is drift, not fraud.** A grant is made cleanly, then someone
suggests a topic, then a faculty name, then asks to see slides. Each step feels
reasonable and the aggregate is a controlled programme dressed as independent
education. If you are documenting a grant, document what was *not* provided.

## Independent education — what the company may legitimately do

- Define **therapeutic areas of interest** for grant funding, published openly
- Operate a **grant review process** separated from commercial functions, with
  documented criteria and decisions
- Fund a programme and receive **aggregate outcome data** afterwards
- Decline to fund

What it may not do: suggest content, faculty, format or title; review slides;
attend as an organiser; link funding to prescribing, formulary status or any
commercial metric; or route the grant decision through commercial staff.

**Grant review criteria that hold up:** a genuine educational need with evidence
behind it; a provider with the capability and accreditation to deliver it; a
design matched to the learning objective; an evaluation plan; no duplication of
what is already available; and a budget proportionate to the activity. Decisions
and rationale get recorded, including the declines.

## Needs assessment — the part usually skipped

An education programme with no demonstrated need is a communication programme.
Build the need from evidence, not from what the company wants discussed:

- **Practice-gap data** — published audits, registry data, guideline adherence
  studies showing what clinicians actually do versus what is recommended
- **Knowledge and competence data** — surveys, prior programme evaluations, board
  examination and MOC data where published
- **Field-sourced signals** — recurring questions from `field-insight-synthesis`
  and enquiry volumes from medical information, which show where understanding
  is thin. Treat these as hypothesis-generating: MSL-visible questions reflect
  who MSLs visit.
- **New evidence** that has not yet reached practice

State the gap as *current practice → desired practice → the barrier between
them*. Education only fixes the barriers that are knowledge or competence. If
the barrier is access, cost, workflow, or reimbursement, say so — a programme
aimed at a non-educational barrier will not move the outcome, and will be
measured as though it should have.

## Speaker programmes — the highest-risk format

The OIG's Special Fraud Alert on speaker programmes (November 2020) is
unusually direct, and it named the patterns rather than the principles. Treat
these as red flags in any design put in front of you:

- Little or no substantive educational content, or the same content repeated to
  the same audience
- Alcohol served, or meals beyond modest value
- Venues not conducive to education — restaurants, entertainment venues, sports
  events
- Attendees who are friends, colleagues from the speaker's own practice, or
  people with no legitimate educational need
- Repeat attendance at the same programme
- Speakers selected by sales, or on the basis of prescribing volume
- High-volume speakers earning substantial cumulative honoraria
- Programmes run after the product has been on the market long enough that the
  content is no longer new

**Medical Affairs' role in speaker programmes varies by company** — sometimes
content owner, sometimes reviewer, sometimes not involved. Establish which it is
before advising, and if the answer is "Medical Affairs approves the content but
commercial selects the speakers and the audience", name that as a governance
weakness rather than working around it.

Speaker payments are transfers of value and are individually reportable. Assume
every honorarium appears in a public database next to the speaker's name, and
that a journalist can sort by total.

## Formats and what each is actually good for

| Format | Works for | Fails when |
|---|---|---|
| **Symposium at a congress** | Reaching a large engaged audience with new data | Used to launch a message rather than teach; satellite symposia must be labelled as industry-supported |
| **Preceptorship** | Deep procedural or diagnostic skill transfer at a centre of expertise | The hosting centre becomes a de facto promotional site, or attendee selection tracks prescribing |
| **Advisory board** | Getting advice — **not** education | Used to deliver a message. That is a promotional programme; see `advisory-board-design` |
| **Standalone meeting / roundtable** | Focused peer discussion of a clinical problem | The agenda is a product story with discussion slots |
| **eLearning / enduring material** | Scale, reach, measurable completion | Built once and left to decay past the evidence it describes |
| **MSL scientific exchange** | Individual, responsive, deep | Turned into a slide-driven briefing round with call targets |

## Designing the curriculum

Write learning objectives that are observable. "Understand the mechanism" is not
assessable; "explain how the mechanism accounts for the observed time-to-onset"
is. Each objective maps to content, to a method appropriate to it, and to an
assessment.

Sequence from what the learner already knows. The commonest design error in
company-organised education is starting from the data set the company wants
covered rather than from the clinical decision the learner has to make.

Balance: an education programme covering a therapeutic area covers the area,
including competitor agents and including where your own product is not the
answer. A curriculum that never mentions an alternative is not education,
whoever paid for it.

## Governance and documentation

For each programme, record: the need and its evidence; the objectives; who
controlled content and faculty; funding and how it was decided; the firewall
between medical and commercial in that decision; the evaluation plan; transfers
of value; and — for independent education — an explicit statement of what the
company did not do.

## Measurement

Attendance is not an outcome. Use the Moore levels: participation, satisfaction,
learning (declarative and procedural), competence, performance, patient health
outcomes. Most programmes can honestly claim levels 1–3 and should not claim
higher without data. See `medical-affairs-metrics`.

Independent education returns **aggregate** outcome data only. A grantee
providing you with attendee-level prescribing data is a compliance problem, not
a good report.

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus:

- Which side of the independence line is this, and does every element agree?
- Is the need evidenced, or asserted?
- Is the barrier actually educational?
- Would this programme survive being described accurately in a news article?
- If speakers are involved: how were they selected, who selects the audience,
  and is the content genuinely new?
- Does the content cover the area, or the product?

## Before you finish

Read `house-rules/medical-education-program.md`. Grant governance, speaker
programme rules and the medical/commercial split differ sharply between
companies, and several operate under commitments that are stricter than the
external standard.
