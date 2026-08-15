# Label Sections — US PLR and EU SmPC

Knowing where information lives, and where the two jurisdictions diverge, is
what stops a deliverable from making a claim that is true in one market and
wrong in another.

---

## US Physician Labeling Rule (PLR) structure

Applies to products approved or relabelled since 2006 (21 CFR 201.56–57).

**Highlights of Prescribing Information** — the first page. A summary, and not
the authority. Never cite it in place of the full section.

**Full Prescribing Information:**

| § | Section | Medical Affairs relevance |
|---|---|---|
| — | Boxed Warning | Must appear in any balanced efficacy discussion |
| 1 | Indications and Usage | **Defines on-label.** Read every qualifier. |
| 2 | Dosage and Administration | Step-up dosing, premedication, monitoring, modification for toxicity |
| 3 | Dosage Forms and Strengths | |
| 4 | Contraindications | Absolute. Short section, high consequence. |
| 5 | Warnings and Precautions | Serious risks plus management guidance |
| 6 | Adverse Reactions | **Trial-derived rates with denominators.** Cite this for frequency, never FAERS. 6.1 clinical trials; 6.2 post-marketing (no denominator). |
| 7 | Drug Interactions | |
| 8 | Use in Specific Populations | Pregnancy, lactation, females and males of reproductive potential, paediatric, geriatric, renal, hepatic |
| 9 | Drug Abuse and Dependence | |
| 10 | Overdosage | |
| 11 | Description | Chemistry |
| 12 | Clinical Pharmacology | 12.1 mechanism, 12.2 pharmacodynamics, 12.3 pharmacokinetics, 12.6 immunogenicity |
| 13 | Nonclinical Toxicology | |
| 14 | Clinical Studies | Registration trial summaries — design, population, results |
| 15 | References | |
| 16 | How Supplied / Storage and Handling | |
| 17 | Patient Counseling Information | |

**Section 6.2 deserves a specific warning.** Post-marketing adverse reactions
are reported voluntarily from a population of uncertain size. The label itself
says so. Rates cannot be derived from it, and it is routinely misread as though
it carried the same denominator as 6.1.

---

## EU SmPC structure

| § | Section | Notes |
|---|---|---|
| 1 | Name of the medicinal product | |
| 2 | Qualitative and quantitative composition | |
| 3 | Pharmaceutical form | |
| 4.1 | Therapeutic indications | **The EU equivalent of "on-label"** |
| 4.2 | Posology and method of administration | |
| 4.3 | Contraindications | |
| 4.4 | Special warnings and precautions for use | Where EU puts most safety guidance |
| 4.5 | Interaction with other medicinal products | |
| 4.6 | Fertility, pregnancy and lactation | |
| 4.7 | Effects on ability to drive and use machines | No US equivalent |
| 4.8 | Undesirable effects | Uses **standard frequency categories** — see below |
| 4.9 | Overdose | |
| 5.1 | Pharmacodynamic properties | Includes clinical efficacy and safety data |
| 5.2 | Pharmacokinetic properties | |
| 5.3 | Preclinical safety data | |
| 6 | Pharmaceutical particulars | |

**EU frequency conventions** (SmPC section 4.8) are standardised and have no US
equivalent:

| Term | Frequency |
|---|---|
| Very common | ≥ 1/10 |
| Common | ≥ 1/100 to < 1/10 |
| Uncommon | ≥ 1/1,000 to < 1/100 |
| Rare | ≥ 1/10,000 to < 1/1,000 |
| Very rare | < 1/10,000 |
| Not known | Cannot be estimated from available data |

Translating a US percentage into an EU frequency term, or the reverse, without
saying you have done so introduces a precision that is not in the source.

---

## Where the jurisdictions commonly diverge

Worth checking explicitly rather than assuming alignment:

- **Indication scope.** Line of therapy, prior-therapy requirements, and
  biomarker restrictions frequently differ. A product approved for
  "at least four prior lines" in one market may be "at least three" in another.
- **Population.** Paediatric approvals, age cut-offs, and renal/hepatic
  restrictions.
- **Boxed warning vs. section 4.4.** The EU has no boxed warning concept; the
  equivalent content sits in special warnings, sometimes with different emphasis.
- **Timing.** Approvals and label updates land at different times, so the two
  labels are routinely out of step by months.
- **Conditional approvals.** EU conditional marketing authorisation and
  accelerated approval in the US carry different obligations and different
  associated wording.

---

## Where to get each

| Source | Covers | Access |
|---|---|---|
| **openFDA** `/drug/label.json` | US SPL | API — `scripts/openfda.py` |
| **DailyMed** | US SPL, authoritative | https://dailymed.nlm.nih.gov (has its own API) |
| **Drugs@FDA** | Approval history, review documents | https://www.accessdata.fda.gov/scripts/cder/daf/ |
| **EMA EPAR / SmPC** | EU | https://www.ema.europa.eu — no open API; retrieve documents |
| **eMC** | UK SmPC and PIL | https://www.medicines.org.uk |
| **PMDA** | Japan | https://www.pmda.go.jp |
| **Health Canada DPD** | Canada | https://health-products.canada.ca |

---

## Using label text in deliverables

**Quote indications verbatim.** Paraphrasing an indication is the most common
way an unintended broader claim enters a document.

**State the jurisdiction and the label date** whenever you cite one.

**Carry the safety information.** A deliverable that discusses efficacy without
comparable prominence for the boxed warning and principal risks fails fair
balance, regardless of accuracy (`medical-affairs-foundations`).

**Distinguish label from trial.** The label summarises the registration
evidence; it is not the publication. Where the detail matters — subgroups,
confidence intervals, censoring — go to the paper.
