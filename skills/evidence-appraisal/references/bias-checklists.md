# Risk of Bias — Working Checklists

Use the instrument that matches the design, and name it in your output. "Risk of
bias was assessed" without naming the tool is not an assessment.

**Contents**
1. [RoB 2 — randomised trials](#rob-2--randomised-trials)
2. [ROBINS-I — non-randomised studies of interventions](#robins-i--non-randomised-studies-of-interventions)
3. [Newcastle-Ottawa Scale](#newcastle-ottawa-scale)
4. [QUADAS-2 — diagnostic accuracy](#quadas-2--diagnostic-accuracy)
5. [Fast triage for congress abstracts](#fast-triage-for-congress-abstracts)

---

## RoB 2 — randomised trials

Five domains, each judged **low risk**, **some concerns**, or **high risk**, with
an overall judgement driven by the worst domain. Assessed **per outcome**, not
per trial — blinding may be adequate for mortality and inadequate for a
patient-reported outcome in the same study.

### D1. Bias arising from the randomisation process

- Was the allocation sequence random?
- Was allocation concealed until assignment? (Sealed opaque envelopes, central
  randomisation, IWRS. Alternate assignment and date-of-birth are not random.)
- Do baseline differences suggest a problem with randomisation? Note that
  baseline imbalance in a small trial is expected by chance; the concern is
  imbalance suggesting the sequence was subverted.

### D2. Bias due to deviations from intended interventions

Two variants depending on whether the question is about assignment (ITT-style)
or adherence (per-protocol style).

- Were participants and carers aware of assignment?
- Were there deviations beyond what would happen in routine care, and did they
  arise *because* of the trial context?
- Was an appropriate analysis used to estimate the effect of assignment?

Open-label trials with subjective outcomes and discretionary co-interventions
are where this domain bites hardest.

### D3. Bias due to missing outcome data

- Were data available for nearly all participants?
- Is there evidence the result was not biased by missing data — for example,
  sensitivity analyses under different missingness assumptions?
- **Could missingness depend on the true value?** Patients who progress or
  deteriorate are the ones who drop out. Differential dropout between arms is
  the warning sign.

### D4. Bias in measurement of the outcome

- Was the method appropriate and applied comparably across arms?
- Were outcome assessors blinded? For subjective outcomes this is decisive; for
  all-cause mortality it barely matters.
- Where investigator-assessed and blinded independent central review (BICR)
  results are both reported, do they agree? Divergence between investigator and
  BICR assessment is a meaningful signal in oncology trials.

### D5. Bias in selection of the reported result

- Was the analysis pre-specified in a protocol or SAP available *before*
  unblinding?
- Is the reported result selected from multiple eligible analyses, time points,
  or subgroups?
- Compare the publication against the registry entry. Changed primary endpoints
  after enrolment began are a serious concern and are visible on
  ClinicalTrials.gov's history tab.

---

## ROBINS-I — non-randomised studies of interventions

Judged **low / moderate / serious / critical risk**, or *no information*. The
framing move that makes ROBINS-I work: specify the **target trial** — the
hypothetical randomised trial this study is trying to emulate — and assess the
study against it.

**Note the scale difference:** "low risk" in ROBINS-I means comparable to a
well-conducted randomised trial. That bar is rarely met.

### Pre-intervention

**D1. Confounding.** The dominant issue in almost all observational
comparative research.
- Were all important confounding domains identified?
- Was a suitable method used (multivariable adjustment, propensity score,
  instrumental variable, new-user design)?
- **Confounding by indication** — sicker patients receive different treatment —
  is the default failure mode in treatment comparisons and is often not fully
  measurable.
- Time-varying confounding requires methods like marginal structural models.

**D2. Selection of participants into the study.** Were participants selected on
characteristics observed after intervention started? This is where **immortal
time bias** enters — see `real-world-evidence.md`.

### At intervention

**D3. Classification of interventions.** Were intervention groups clearly
defined, and was classification based on information recorded at the time
(rather than reconstructed with knowledge of outcome)?

### Post-intervention

**D4. Deviations from intended interventions.** Switching, discontinuation, and
co-interventions differing systematically between groups.

**D5. Missing data.** Missingness in exposure, outcome, or confounders. In
routinely collected data, missingness is frequently informative — a lab value is
missing because the clinician did not think it was needed.

**D6. Measurement of outcomes.** Could measurement differ between groups?
Outcome misclassification in claims data (an algorithm identifying an event with
70% positive predictive value) attenuates effects toward the null — or does not,
if misclassification is differential.

**D7. Selection of the reported result.** Multiple analyses, multiple outcome
definitions, multiple exposure windows. Database studies afford enormous
analytic flexibility; pre-registration is the mitigation.

---

## Newcastle-Ottawa Scale

Cohort and case-control studies. Nine stars across three domains. Crude, widely
used in meta-analyses, and better than no assessment.

**Cohort studies:**
- *Selection* (4 stars) — representativeness of exposed cohort; selection of
  non-exposed from the same population; ascertainment of exposure; demonstration
  that the outcome was not present at start
- *Comparability* (2 stars) — controls for the most important factor, and for
  additional factors. **Specify which factors** when you report this, or the
  stars mean nothing.
- *Outcome* (3 stars) — assessment method; adequate follow-up duration;
  adequacy of follow-up completeness

**Case-control studies:** adequate case definition, representativeness of cases,
control selection and definition, comparability, exposure ascertainment, same
method for both groups, non-response rate.

**Limitation worth stating:** NOS thresholds for "good quality" are arbitrary
and inconsistently applied across published meta-analyses. Where the assessment
matters, ROBINS-I is more informative.

---

## QUADAS-2 — diagnostic accuracy

Four domains — patient selection, index test, reference standard, and
flow/timing — each assessed for risk of bias, and the first three additionally
for applicability.

The recurring problems: a case-control design inflating accuracy (obviously
diseased vs obviously healthy), an imperfect reference standard, the index test
result being known when the reference standard was interpreted, and differential
verification where only positives get the gold standard.

---

## Fast triage for congress abstracts

Most Medical Affairs appraisal happens on abstracts, where the information for a
full assessment does not exist. That is itself the finding. A workable triage:

1. **Design named?** If the abstract does not say randomised, assume it is not.
2. **N and event count.** An HR from 30 events is not stable.
3. **Primary endpoint stated, and is the headline result it?** A press release
   or abstract leading with a secondary endpoint is a signal.
4. **Confidence intervals present?** Their absence is a limitation to state, not
   a gap to fill.
5. **Comparator relevant to current practice?**
6. **Follow-up duration** relative to the natural history of the disease.
7. **Registry entry** — check ClinicalTrials.gov for the pre-specified primary
   endpoint and whether it changed.
8. **Is there a full publication?** If yes, appraise that instead.

**Standing caveat for anything abstract-only:** not peer-reviewed, incomplete
methods, and results may change materially between abstract and full publication.
That is a routine occurrence, not a rare one. Label evidence tier explicitly —
`citation-integrity` requires it.

---

*Sources: Sterne et al., RoB 2 (BMJ 2019); Sterne et al., ROBINS-I (BMJ 2016);
Wells et al., Newcastle-Ottawa Scale; Whiting et al., QUADAS-2 (Ann Intern Med
2011). Cochrane Handbook chapters 8 and 25 are the practical reference.*
