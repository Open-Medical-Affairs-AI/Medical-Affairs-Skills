---
name: scientific-manuscript
description: >-
  Draft, structure and prepare a scientific manuscript for journal
  submission — primary trial reports, secondary analyses, real-world
  evidence papers, reviews and case reports. Use when asked to write or
  draft a paper, prepare a manuscript, pick a target journal, write a cover
  letter, or respond to peer reviewers. Applies ICMJE authorship criteria,
  GPP 2022, and the right EQUATOR reporting guideline for the design
  (CONSORT, PRISMA, STROBE, CARE, SPIRIT, RECORD, CHEERS). Produces a real
  .docx. Also use to check an existing draft against the reporting guideline
  before submission.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: content
  maturity: beta
  requires:
    - medical-affairs-foundations
    - citation-integrity
    - capability-detection
  suggests:
    - evidence-appraisal
    - evidence-synthesis
    - deliverable-quality-review
  produces: Manuscript draft (.docx) with reporting-guideline checklist
  python: [python-docx>=1.1]
---

# Scientific Manuscript

A manuscript is the most durable thing Medical Affairs produces. It outlives the
strategy, the team, and usually the product, and it is the form in which
evidence reaches guideline committees.

That permanence is why the integrity requirements below are not administrative
overhead. A paper with a guest author or an unstated conflict is a problem that
does not go away.

## Governance, settled before drafting

### Authorship — ICMJE, all four criteria

Every named author must meet **all four**:

1. Substantial contribution to conception or design, **or** to acquisition,
   analysis, or interpretation of data
2. Drafting the work **or** revising it critically for important intellectual
   content
3. Final approval of the version to be published
4. Agreement to be accountable for all aspects of the work

Someone who funded the study, supplied the drug, or ran the statistics without
contributing to interpretation does not automatically qualify. Contributors who
do not meet all four go in the acknowledgements with their contribution
described.

**Ghost authorship** — a substantive contributor unnamed — and **guest
authorship** — a named author who did not meet the criteria — are both serious
integrity breaches, not conventions.

### Medical writing support

Professional medical writing support is entirely legitimate **and must be
disclosed**, naming the writer, their affiliation, and who funded them. GPP 2022
is explicit. Concealing it is what turns acceptable support into ghostwriting.

### GPP 2022

- Authors have genuine access to the data and to the analyses
- Results are published **regardless of whether they are favourable**
- Trials are registered before enrolment; results are reported
- The publication steering committee's role is documented
- Funding and the sponsor's role in design, analysis, and the decision to
  publish are stated

## Pick the reporting guideline first

Structure follows the guideline. Choosing it after drafting means restructuring.

| Design | Guideline |
|---|---|
| Randomised trial | **CONSORT 2010** (+ extensions: cluster, non-inferiority, pilot, PRO, harms) |
| Trial protocol | **SPIRIT 2013** |
| Systematic review / meta-analysis | **PRISMA 2020** (+ NMA, ScR, IPD, DTA) |
| Observational (cohort, case-control, cross-sectional) | **STROBE** |
| Routinely-collected health data | **RECORD** (a STROBE extension) |
| Case report | **CARE** |
| Economic evaluation | **CHEERS 2022** |
| Diagnostic accuracy | **STARD 2015** |
| Prediction model | **TRIPOD** |
| Qualitative research | **COREQ** or **SRQR** |

The EQUATOR Network catalogues all of them. Complete the checklist **as you
write**, not afterwards — the items you cannot complete are usually telling you
something is missing from the study report.

## Structure — IMRaD

**Title.** Descriptive, includes the design. "A randomised, double-blind, phase
3 trial of X versus Y in Z" tells a reader more than a clever title, and it is
what makes the paper findable.

**Abstract.** Structured, to the journal's word limit. Every number that appears
here must appear in the results, with its confidence interval. The abstract is
the only part most people read and the part most likely to overclaim.

**Introduction.** Three paragraphs: what is known, what is not known, what this
study asked. Not a literature review. The last sentence states the objective and
the pre-specified hypothesis.

**Methods.** Reproducibility is the standard. Design, setting, participants with
eligibility criteria, interventions, outcomes with definitions and how they were
assessed, sample size calculation, randomisation and blinding, statistical
methods **including the testing hierarchy and how multiplicity was handled**,
and ethics approval with consent.

Register and protocol details go here. So do deviations from the protocol —
concealing them is the failure that peer review most reliably finds.

**Results.** Participant flow (with the diagram), baseline characteristics,
primary outcome, secondary outcomes, harms. Report **absolute and relative**
effects with confidence intervals. No interpretation.

Harms get proper reporting, not a sentence. Under-reporting harms is one of the
most consistent and consequential deficiencies in the trial literature.

**Discussion.** Principal findings, then how they sit against existing evidence,
then limitations, then implications. Limitations are specific and honest —
"limitations include the small sample size" is not a limitations section.

**Conclusion.** Proportionate to the evidence. A single-arm study does not
conclude that a treatment is effective; it concludes that a response rate was
observed. This is where overclaiming most often survives into print.

## The failure modes reviewers actually find

- **Spin.** A neutral primary result presented as positive by leading on a
  secondary endpoint. Reviewers and readers detect it, and it is the most common
  substantive criticism of industry-sponsored papers.
- **Outcome switching.** The reported primary outcome differs from the
  registered one. Trivially checkable on ClinicalTrials.gov, and increasingly
  checked.
- **Selective harms reporting.**
- **Conclusions unsupported by the design.**
- **Missing multiplicity handling.** Secondary endpoints treated as positive
  after the hierarchy had already failed.
- **Undisclosed writing support.**

## Building the document

```bash
S=skills/scientific-manuscript/scripts/build_manuscript.py

python3 $S --example > ms.json
python3 $S --spec ms.json --out manuscript.docx
python3 $S --spec ms.json --checklist consort   # gap-check before submission
```

The builder emits a properly structured .docx with numbered headings, a title
page carrying the authorship and disclosure blocks, and the draft marking. It
also refuses to build without a declared reporting guideline and a conflicts
statement.

**If a higher-fidelity Word renderer is available in your environment**, use it
for final formatting and keep this skill for the structure and the governance.

## Journal selection

Match the paper to the journal's scope and evidence standard, not to the highest
impact factor you can plausibly reach. A serial rejection cycle costs more
months than the impact factor is worth, and the evidence sits unpublished
meanwhile.

Check: scope and recent similar publications, word and reference limits,
structured abstract format, data-sharing requirements, open-access policy and
cost, and typical time to first decision.

**Predatory journals** are a real risk. Check membership of COPE, indexing in
MEDLINE and DOAJ, and whether the editorial board is real and contactable. If
the solicitation arrived by unsolicited email praising your "esteemed
contribution", it is predatory.

## Responding to reviewers

Point by point, in a table: the comment verbatim, the response, and where the
manuscript changed with line numbers.

Address every comment, including ones you disagree with — explain the
disagreement with evidence rather than declining to engage. Be courteous even
when a reviewer has misread the paper; if they misread it, other readers will
too, and the fix is usually to clarify the text.

## Before you finish

Read `house-rules/scientific-manuscript.md`, run `citation-integrity` over every
reference, run `deliverable-quality-review`, and complete the reporting
guideline checklist honestly.
