# Real-World Evidence

RWE answers questions randomised trials cannot: long-term outcomes, unselected
populations, treatment sequencing in practice, rare events, and comparative
effectiveness under real prescribing. It is also the easiest place in Medical
Affairs to produce a confident, precise, wrong answer.

The difference between credible and non-credible RWE is almost never the data
source. It is the design.

---

## Target trial emulation — the framework that makes RWE credible

Before any analysis, specify the randomised trial you would run if you could,
then state how the observational data emulates each component. Most RWE failures
are visible as a mismatch in one of these:

| Component | Specify |
|---|---|
| **Eligibility criteria** | Applied using only information available *at baseline* |
| **Treatment strategies** | Precisely defined, including dose, duration, and what counts as switching |
| **Assignment procedure** | How exchangeability is achieved — which confounders, adjusted how |
| **Follow-up start (time zero)** | The single most important decision. See below. |
| **Outcome** | Definition and how it is ascertained in the data source |
| **Causal contrast** | Intention-to-treat analogue, or per-protocol analogue with appropriate adjustment |
| **Analysis plan** | Pre-specified, ideally registered |

**Time zero must be the same moment for eligibility assessment, treatment
assignment, and start of follow-up.** When these come apart, bias follows
mechanically. This one alignment rule prevents most of the named biases below.

---

## The named biases, and how to spot them

### Immortal time bias

The most common serious error in database pharmacoepidemiology.

**What happens.** A period of follow-up during which the outcome could not have
occurred is misassigned to the treated group. Classic form: patients are
classified as "treated" if they ever received the drug during follow-up, but
follow-up starts at diagnosis. To receive the drug, they had to survive until
they received it. That survival time is guaranteed — immortal — and it is
credited to the treatment.

**Signature.** A treatment appearing to produce an implausibly large mortality
benefit, particularly in a retrospective cohort where exposure is defined over a
window rather than at a point.

**Fix.** Align time zero with treatment initiation (new-user design), or use a
landmark analysis, or treat exposure as time-varying.

### Confounding by indication

Patients receive a treatment *because* of prognostic characteristics. Sicker
patients get the more aggressive therapy; fitter patients get the newer one.
Adjustment can address measured confounders; the ones driving the clinical
decision — performance status, frailty, clinician gestalt — are frequently
unmeasured in claims data.

**Fix, partially.** Active comparator new-user design: compare against another
treatment used for the same indication at the same decision point, rather than
against non-users. This removes much of the "treated vs untreated" confounding
in one design move and is the single highest-value choice in comparative RWE.

### Prevalent user bias

Including patients already on treatment at study start excludes everyone who
already discontinued due to toxicity or lack of effect, and everyone who died.
The surviving prevalent users are a selected, tolerant, responsive group.

**Fix.** New-user (incident user) design.

### Depletion of susceptibles

Related: the risk of an adverse effect is often highest early. A prevalent-user
cohort has already depleted the susceptible population, so the treatment appears
safer than it is.

### Healthy adherer effect

Adherent patients have better outcomes on placebo too. Adherence is a marker of
health behaviour, not just of drug exposure. Any per-protocol style RWE analysis
inherits this.

### Detection / surveillance bias

Patients on treatment are monitored more closely, so more events are found. A
"higher rate" of an asymptomatic finding may be a higher rate of looking.

### Outcome misclassification

Claims-based algorithms have imperfect sensitivity and positive predictive value.
Non-differential misclassification biases toward the null; differential
misclassification can bias either way. Validated algorithms should be cited with
their operating characteristics.

### Informative censoring

Patients lost to follow-up because they got sicker, changed insurer, or died
outside the capture window. Standard survival methods assume censoring is
uninformative; when it is not, estimates are biased.

### Left truncation and data capture windows

A claims database only sees a patient while they are enrolled. Prior therapy
before enrolment is invisible, so "first-line" may not be first line.

---

## Data sources and what each can and cannot do

| Source | Strengths | Blind spots |
|---|---|---|
| **Claims** (Medicare, commercial) | Complete capture of billed events, large N, longitudinal within enrolment | No labs, no stage, no performance status, no mortality unless linked; enrolment gaps |
| **EHR** | Labs, vitals, notes, more clinical granularity | Care outside the system is invisible; enormous missingness; documentation varies by site |
| **Registry** | Disease-specific detail, curated, often includes staging and biomarkers | Selected sites, incomplete population coverage, voluntary participation |
| **Chart review** | Highest fidelity | Small, expensive, abstractor variability, retrospective selection |
| **Patient-generated / wearable** | Symptoms, function, real-time | Selection by digital access, adherence to the device |
| **Spontaneous reports** (FAERS) | Rare event signal detection, post-market | **No denominator.** Reporting bias, duplicates, no causality. Hypothesis-generating only. |

**On FAERS specifically:** disproportionality measures (PRR, ROR, EBGM) compare
reporting rates within the database. They do not estimate risk, incidence, or
causality, and they are heavily influenced by notoriety, litigation, launch
recency, and media coverage. A "signal" in FAERS means "worth investigating",
full stop. Presenting one as a rate or as evidence of harm is a serious error —
and presenting a *competitor's* FAERS signal that way is both a scientific and a
compliance failure.

---

## Regulatory context

- **FDA RWE Program framework** (21st Century Cures Act mandate) and the
  subsequent guidance series on RWD from EHRs and claims, registries, data
  standards, and regulatory considerations for external control arms.
- **EMA** — DARWIN EU, and the ENCePP Guide on Methodological Standards.
- **External control arms** are accepted in narrow circumstances — rare disease,
  high unmet need, large expected effect, well-characterised natural history —
  and require rigorous contemporaneity and comparability. They are not a
  general substitute for randomisation.
- **Transparency expectations** have risen sharply: pre-registration of the
  protocol and analysis plan (EU PAS Register, ClinicalTrials.gov, HMA-EMA
  catalogues) is now the expected standard for credible comparative RWE.

---

## Appraising an RWE study quickly

1. **New-user design?** If prevalent users are included, note it.
2. **Active comparator?** Treated-vs-untreated comparisons are much weaker.
3. **Time zero aligned** across eligibility, exposure, and follow-up?
4. **Which confounders were adjusted, and which important ones were unavailable?**
   The unmeasured ones are what matter — a paper that names them is more
   trustworthy than one that does not.
5. **Was the protocol pre-registered?**
6. **Outcome definition validated?**
7. **Negative control outcome or falsification endpoint?** A well-designed study
   often includes an outcome the treatment could not plausibly affect; if an
   effect appears there, residual confounding is present. Its presence is a
   strong marker of methodological seriousness.
8. **Sensitivity analyses** — E-value or similar quantitative bias analysis for
   how strong unmeasured confounding would need to be to explain the result.

---

## For Medical Affairs specifically

RWE is often the only evidence available for the questions clinicians actually
ask — sequencing, older and frailer patients, comorbid populations, adherence in
practice, duration of benefit. That makes it strategically central and makes
disciplined appraisal more important, not less.

Two practical positions worth holding:

**Do not let a weak RWE study stand in for a needed trial.** If the question
matters and the observational answer is fragile, that is an evidence gap. Route
it to `evidence-gap-analysis`.

**Appraise your own RWE as hard as a competitor's.** The asymmetry — rigorous
about their real-world data, relaxed about yours — is the most common form of
scientific bad faith in this function, and external audiences detect it
immediately.
