# Disclaimer and Conditions of Use

**Read this before using these skills on anything real.**

This project helps Medical Affairs professionals direct an AI agent through
professional workflows. It produces **drafts for expert review**. It does not
replace the judgement, accountability, or regulatory obligations of a qualified
person.

---

## 1. What this is not

This project is **not**:

- **A medical device.** It does not diagnose, treat, prevent, or mitigate disease,
  and it is not intended to inform individual patient care. It is not, and must
  not be deployed as, Clinical Decision Support under 21 CFR 880.6310 / FDA CDS
  guidance, EU MDR Annex VIII Rule 11, or equivalent frameworks.
- **Medical advice.** Nothing it produces is advice to a patient, clinician, or
  caregiver.
- **A regulatory system of record.** It is not validated under 21 CFR Part 11,
  EU Annex 11, or GxP computerised-system requirements. Do not use its output as
  a controlled record, and do not use it to make or document a regulatory
  submission decision without independent qualified review.
- **A pharmacovigilance system.** It does not perform, replace, or discharge any
  adverse event reporting obligation. See section 4.
- **Promotional material generation.** Medical Affairs output is non-promotional
  by definition. These skills are built to keep it that way, but the
  responsibility remains yours.

## 2. Human review is required, not optional

Every deliverable this project produces carries the marking:

> **DRAFT — NOT FOR EXTERNAL USE. REQUIRES QUALIFIED MEDICAL REVIEW.**

Do not remove that marking until a qualified reviewer has actually reviewed the
content. The skills are written to refuse to remove it themselves.

An AI agent will confidently produce a well-formatted document containing a
misattributed hazard ratio, an inverted confidence interval, or a citation to a
paper that does not exist. Formatting quality is not evidence of accuracy. The
review step is where the value is protected, not where it is slowed down.

## 3. Data handling — your responsibility

- **Use synthetic, de-identified, or aggregate data.** All sample data shipped in
  `workshop/data/` is entirely fictional and marked `SYNTHETIC DATA`.
- **Do not submit PHI or personal data** to any AI system without a lawful basis,
  a completed DPIA where required, and an executed data processing agreement
  covering that specific system. HIPAA, GDPR, and equivalent regimes apply to
  your use of an AI vendor exactly as they apply to any other processor.
- **Do not submit company-confidential material** to a consumer AI service. Use
  an enterprise deployment with contractual assurances on training and retention.
- **KOL and HCP information is personal data.** Publication records are public;
  interaction notes, opinions attributed to a named individual, and engagement
  history are not. Handle accordingly, and observe your transparency-reporting
  obligations (US Sunshine Act / Open Payments, EFPIA Disclosure Code, and local
  equivalents).

## 4. Adverse events and product quality complaints

**This project does not report adverse events. You do.**

Every skill that touches field notes, KOL interactions, medical information
requests, or any other human-sourced content is required to scan for potential
adverse events, product quality complaints, special-situation reports (pregnancy,
overdose, off-label use with an outcome, medication error), and to surface them
prominently and unmissably to the human operator.

That surfacing is a prompt to *you*. Your reporting clock started when the
information reached a company employee or agent — typically **24 hours** for
serious cases under most PV SOPs — and it is running regardless of whether the
agent flagged it, missed it, or was never shown the file. Route through your
company's pharmacovigilance system, following your own SOPs, every time.

Never rely on an AI system as your AE detection control.

## 5. Off-label information

Skills in this project handle scientific exchange about unapproved uses only in
the narrow way Medical Affairs legitimately does: in response to a genuine
**unsolicited** request, with truthful non-misleading scientific data, routed
through the appropriate Medical Information channel, with the approval status
stated explicitly.

The skills will not help you proactively disseminate off-label information, and
they will not help you make a promotional claim. If you find a way to make them
do so, that is a bug — please report it.

## 6. Accuracy of retrieved data

Skills query PubMed, ClinicalTrials.gov, and openFDA live. Those sources are
authoritative for what they contain and are still incomplete, lagged, and
occasionally wrong. In particular:

- **openFDA FAERS** is a spontaneous reporting database. Disproportionality
  signals are **hypothesis-generating only**. They do not establish causality,
  incidence, or risk. Presenting them as if they do is a serious error.
- **ClinicalTrials.gov** registration data is sponsor-submitted and may be stale.
- **PubMed** indexing lags publication; absence of a record is not absence of
  evidence.

## 7. No warranty

This project is provided under the Apache License 2.0, **"AS IS", WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND**, express or implied. See sections 7 and 8
of `LICENSE` for the full warranty disclaimer and limitation of liability.

The contributors are not your compliance function, not your legal counsel, and
not your medical reviewer. Your organisation's SOPs govern. Where anything in
this project conflicts with your SOPs, **your SOPs win** — and you should record
that conflict in `house-rules/` so your agent follows them too.

## 8. Reporting a safety problem

If a skill produces output that could cause harm — a fabricated citation
presented as real, a promotional claim, a missed adverse event, an off-label
claim — please open an issue titled `[safety]`, or follow `SECURITY.md` if the
report itself should not be public. These reports take priority over features.
