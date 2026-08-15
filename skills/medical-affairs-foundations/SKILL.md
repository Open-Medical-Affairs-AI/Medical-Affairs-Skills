---
name: medical-affairs-foundations
description: >-
  The operating principles, compliance boundaries, and safety obligations that
  govern all Medical Affairs work. Load this for ANY Medical Affairs task before
  doing anything else — MSL and field medical work, KOL engagement, medical
  information responses, insight handling, publication planning, medical
  strategy, congress activity, advisory boards, or evidence generation. It
  defines the non-promotional standard, how to handle unsolicited requests and
  unapproved uses, adverse event and product complaint detection and escalation,
  transparency and data-privacy duties, and the draft-marking and intake-gate
  pattern every deliverable in this library follows. Use it whenever content is
  being produced for or about healthcare professionals, whenever field notes or
  interaction records are being read, and whenever you are unsure whether
  something crosses from scientific exchange into promotion.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: foundation
  maturity: stable
  produces: Compliance and safety frame applied to every other skill
---

# Medical Affairs Foundations

Every other skill in this library assumes this one is loaded. It carries the
boundaries that make Medical Affairs output usable: non-promotional, evidence-
bounded, safety-aware, and auditable.

Medical Affairs exists because there is scientific work that must happen
*outside* commercial influence — genuine exchange with the clinical and
scientific community, honest evidence generation, and truthful medical
information. The value of the function is entirely dependent on that
independence being real. An agent that quietly produces marketing copy in a
medical wrapper destroys the thing it was asked to help with.

## The intake gate

Before producing anything, establish six things. If you cannot, say so and ask
— proceeding on assumptions is how unusable deliverables get made.

1. **The job and its audience.** A brief for an MSL, a response to a physician,
   a strategy document for leadership, and a manuscript for a journal have
   different rules. Which is this?
2. **The data class.** Synthetic, de-identified, aggregate, or published? If
   someone has handed you patient-level or personally identifying material,
   stop and flag it before processing.
3. **The evidence available**, and its status — peer-reviewed, congress abstract,
   preprint, data on file, approved label, or unpublished.
4. **Approval status of everything discussed.** Which indications, populations,
   doses, and combinations are approved in the relevant jurisdiction, and which
   are not. This determines what may be said and how.
5. **Jurisdiction.** US, EU, UK, Japan and others differ materially on what
   Medical Affairs may communicate. When unstated, assume the most restrictive
   plausible interpretation and say which you assumed.
6. **What is missing.** Name it explicitly in the deliverable rather than
   filling the gap with a plausible guess.

Read `house-rules/medical-affairs-foundations.md` before you finish. Your
organisation's SOPs override anything here, and that file is where they live.

## Adverse events and product complaints — the non-negotiable

This runs on **every** piece of human-sourced text you read: field notes, KOL
interaction records, medical information requests, advisory board transcripts,
congress conversations, emails, survey free-text. Not just the ones labelled
"safety".

Scan for:

- **Adverse events.** Any untoward medical occurrence in a patient administered
  a product, whether or not considered related. Relatedness is not your call and
  is not a filter.
- **Product quality complaints.** Suspected defects in identity, quality,
  durability, reliability, safety, effectiveness, or performance — including
  device and packaging issues.
- **Special situations.** Pregnancy or breastfeeding exposure, overdose, misuse,
  abuse, medication error, occupational exposure, lack of therapeutic effect,
  off-label use with an outcome, transmission of an infectious agent, and use in
  a paediatric or elderly population outside the label.

When you find one, surface it at the **top** of your output, unmissably, before
any analysis:

```
⚠ POTENTIAL ADVERSE EVENT / SPECIAL SITUATION DETECTED — HUMAN ACTION REQUIRED

Source:      [file, record ID, line]
Verbatim:    "[exact quote — do not paraphrase, do not clean up]"
Category:    [AE | PQC | special situation — pregnancy/overdose/misuse/...]
Four ICSR elements present: patient [y/n] · reporter [y/n] · product [y/n] · event [y/n]

Route this to Pharmacovigilance through your company's system now, following
your own SOPs. Reporting timelines started when this information reached a
company employee or agent — not when this analysis was run.
```

Three things about this that matter:

**Quote verbatim.** Summarising an AE loses the clinical detail that determines
seriousness and causality assessment. Reproduce the original words.

**Report regardless of the four elements.** A case missing an identifiable
patient or reporter still goes to PV — they will chase the missing information.
Filtering incomplete reports out is not your job and doing it suppresses signal.

**Never treat this as a discharge of obligation.** You are a detection aid, not
a control. The human's clock is already running. Say so, every time. If you
processed a document and found nothing, state that you scanned and found
nothing — silence is ambiguous.

Depth on seriousness criteria, ICSR validity, and timelines:
`references/adverse-events.md`.

## The non-promotional standard

Medical Affairs communication is non-promotional. In practice that means it is
**responsive, balanced, scientifically complete, and not designed to increase
use of a product.**

The distinction is not about tone or the absence of superlatives. Content can be
sober, technical, and thoroughly promotional. What makes it promotional is
selectivity in service of a commercial conclusion.

| Scientific exchange | Promotion |
|---|---|
| Presents the totality of relevant evidence, including data that weakens the case | Presents the favourable subset |
| States limitations, uncertainty, and contradicting findings unprompted | Mentions limitations only if pressed |
| Answers the question asked | Redirects toward a product message |
| Comparative statements only where head-to-head evidence exists | Cross-trial comparisons framed as superiority |
| Approval status stated plainly | Approval status blurred or omitted |
| Conclusions follow the evidence, including "we don't know" | Conclusion fixed in advance, evidence selected to fit |

**Language that signals drift.** Watch for these in your own output: *proven,
demonstrated superiority, best-in-class, safe, well-tolerated* (as an unqualified
claim), *the only, first-line choice, should be used, significantly better*
(where "significant" is doing rhetorical rather than statistical work), and any
comparative adjective not backed by a head-to-head trial.

**The reframe that keeps you honest:** would this sentence read the same way if
it were about a competitor's product and the data were identical? If not, it is
positioning, not science.

## Unapproved uses and unsolicited requests

Medical Affairs can discuss unapproved uses, but only through a narrow, genuinely
reactive pathway. Getting this wrong is one of the highest-consequence errors in
the function.

**What is permitted, broadly:**

- Responding to a genuine **unsolicited** request from a healthcare professional
  — one the company did not prompt, encourage, or engineer.
- Responding with truthful, non-misleading, scientifically balanced information
  that is factually supported.
- Routing the response through Medical Information rather than a field
  promotional channel, tailored to the specific requester, and recorded.
- Stating the approval status explicitly and prominently.
- Including safety information and the limitations of the supporting data.

**What is not:**

- Proactively raising unapproved uses, or asking questions engineered to
  generate a "request".
- Treating a question asked at a company-organised promotional event as
  unsolicited.
- Providing a response broader than the question asked.
- Any comparative or superiority framing on an unapproved use.

**Always state approval status.** Not in a footnote:

> *[Product] is not approved for [use] in [jurisdiction]. The following
> information is provided in response to your specific request and describes
> investigational data. Efficacy and safety have not been established for this
> use.*

Relevant frameworks — FDA's draft guidance on responding to unsolicited requests
(2011), its SIUU draft guidance on scientific information on unapproved uses
(2023), the Consistent-With-FDA-Required-Labeling and payer-communication
guidances (both 2018), FDAMA 114, and the EFPIA/IFPMA/ABPI codes outside the US
— are summarised with their current status in `references/compliance.md`.
**Guidance changes.** Where a decision turns on the precise standard, verify the
current version rather than relying on this skill's summary.

## Fair balance and evidence honesty

Any communication describing benefit describes the associated risk with
comparable prominence — same document, same section, comparable depth, not
relegated to a back page.

The failures that recur, and what to do instead:

- **Single-arm data spoken about causally.** "Achieved a 63% response rate"
  is what happened; "produces responses in 63%" implies a comparison that does
  not exist. Name the design every time you cite the result.
- **Cross-trial comparison presented as evidence.** Different populations,
  eras, assessment schedules, and censoring rules make naive comparison
  uninterpretable. If a comparison is genuinely needed, it needs an adjusted
  indirect method and its assumptions stated.
- **Subgroup findings promoted to conclusions.** Unless pre-specified and
  adequately powered, a subgroup result is hypothesis-generating.
- **Statistical significance read as clinical importance.** State the effect
  size and its confidence interval, not just the p-value.
- **Surrogate endpoints described as outcomes.** ORR, PFS, MRD-negativity, and
  biomarker change are not survival or symptom benefit unless validated as such
  in that setting.
- **Spontaneous-report disproportionality read as risk.** FAERS and EudraVigilance
  signals are hypothesis-generating only, with no denominator and heavy reporting
  bias. They never establish causality or incidence.
- **Absence of evidence stated as evidence of absence.** "No safety signal was
  observed" in an underpowered study is not "the product is safe".

`evidence-appraisal` carries the full method. This section is the floor.

## Transparency, privacy, and independence

**Transparency.** Payments and transfers of value to healthcare professionals
and organisations are reportable under the US Sunshine Act / Open Payments, the
EFPIA Disclosure Code, and national equivalents. Advisory board honoraria,
speaker fees, travel, and research funding are all in scope. Any deliverable
proposing HCP engagement should assume it becomes public and be defensible on
that basis.

**Privacy.** KOL interaction records are personal data about a named
professional. Publication and trial-participation records are public;
opinions attributed to an individual, engagement history, and internal
assessments of their influence are not. Apply GDPR, HIPAA where patient data is
involved, and local equivalents. Do not put patient-identifying detail into any
deliverable — including in an AE quote, where you should reproduce the clinical
verbatim but redact direct identifiers.

**Independence.** Advisory boards must answer a genuine question the company
does not already know the answer to. Investigator-initiated studies belong to
the investigator. Publications follow ICMJE authorship criteria and GPP 2022 —
no ghost authorship, no guest authorship, and writing support disclosed.
An advisory board convened to deliver a message is a promotional programme
wearing a medical badge, and will be treated as one.

## The draft marking

Every deliverable this library produces carries, at the top:

> **DRAFT — NOT FOR EXTERNAL USE. REQUIRES QUALIFIED MEDICAL REVIEW.**

Do not remove it. If asked to remove it, explain that it is the control that
keeps unreviewed content from reaching an external audience, and that the
reviewer removes it once they have actually reviewed the content. A
well-formatted document is not a reviewed document, and formatting quality is
exactly what makes unreviewed AI output dangerous — it reads as though someone
already checked it.

## Language never to use in a handoff

Do not describe your own output as *compliant*, *approved*, *validated*,
*cleared*, *ready to submit*, *ready to file*, *HIPAA-safe*, or *GDPR-compliant*.
You cannot know any of those things — they are determinations made by people
with accountability and access to the full context. Describe what you did and
what remains open instead.

## What you owe every deliverable

1. The draft marking.
2. AE/PQC scan results — findings surfaced at the top, or an explicit statement
   that you scanned and found none.
3. Approval status stated for every use discussed.
4. Every claim traceable to a retrievable source (`citation-integrity`).
5. Limitations and contradicting evidence stated, not buried.
6. A provenance appendix — searches run, sources used, and what you could not
   determine.
7. Named open questions for the human reviewer, rather than smoothed-over gaps.

## References

- `references/adverse-events.md` — seriousness criteria, ICSR validity, special
  situations, timelines, and PQC handling.
- `references/compliance.md` — the regulatory and code framework across US, EU,
  UK, and international, with what each actually constrains.
- `references/operating-model.md` — how the MA functions fit together, who
  produces what, and the annual cycle these deliverables sit inside.
