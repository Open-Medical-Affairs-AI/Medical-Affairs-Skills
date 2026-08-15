# GRADE — Rating Certainty in a Body of Evidence

GRADE (Grading of Recommendations, Assessment, Development and Evaluations) rates
how confident we can be that an estimated effect is close to the true effect. It
is used by WHO, Cochrane, NICE, and most guideline bodies, which is why Medical
Affairs should be able to speak it fluently: it is the language in which your
evidence will be judged by the people who write guidelines.

**The critical framing:** GRADE rates certainty **for a specific question and a
specific outcome**, across the whole body of evidence. It is not a quality score
you attach to a paper. "This is a GRADE high-quality study" is a category error.

---

## The four levels

| Level | Meaning | Conventional phrasing |
|---|---|---|
| **High** | Very confident the true effect lies close to the estimate | "X reduces Y" |
| **Moderate** | Moderately confident; true effect likely close, possibly substantially different | "X probably reduces Y" |
| **Low** | Limited confidence; true effect may be substantially different | "X may reduce Y" |
| **Very low** | Very little confidence; true effect likely substantially different | "The evidence is very uncertain about the effect of X on Y" |

Those phrasings are conventional in GRADE-based summaries and are worth adopting
verbatim. They communicate certainty without a numeric badge, and they stop the
reader from over-reading a low-certainty finding.

---

## Starting point

- Randomised trials start at **high**.
- Observational studies start at **low**.

Then rate down for five things, and (for observational evidence) potentially up
for three.

---

## Rating down

### 1. Risk of bias

Assessed with RoB 2 for RCTs, ROBINS-I for non-randomised studies. Rate down one
level for serious concerns, two for very serious. What matters is bias in the
studies contributing most weight, not the worst study in the set.

Common triggers: lack of blinding where the outcome is subjective, substantial
loss to follow-up with imbalance between arms, selective outcome reporting, and
early stopping for benefit.

### 2. Inconsistency

Unexplained heterogeneity of results across studies. Look at:

- Point estimates varying widely
- Confidence intervals with little overlap
- I² high (>50% warrants a look; >75% is substantial)
- A statistically significant heterogeneity test

**Only rate down for *unexplained* inconsistency.** If heterogeneity is explained
by a credible subgroup effect — different doses, different populations — the
right response is to present the subgroups separately rather than to rate down.

### 3. Indirectness

The evidence does not directly answer the question. Four flavours, and in
Medical Affairs this is the one that bites most often:

- **Population** — trials in fit, younger, single-comorbidity patients; question
  concerns the clinic population.
- **Intervention** — different dose, schedule, formulation, or administration
  setting.
- **Comparator** — the trial comparator is not the current standard of care.
  This is extremely common and frequently glossed over.
- **Outcome** — a surrogate endpoint stands in for the outcome that matters.
  PFS for OS, MRD-negativity for long-term control, bone density for fracture.

Indirect comparison (no head-to-head evidence) is also indirectness, and usually
warrants rating down at least one level.

### 4. Imprecision

Wide confidence intervals, few events, or a small sample. The practical test:
does the confidence interval span values that would lead to different clinical
decisions? An interval running from "clinically important benefit" to "no
benefit" is imprecise regardless of the point estimate.

Optimal information size — roughly, whether the evidence base has as many events
as an adequately powered single trial would need — is the formal criterion.

### 5. Publication bias

Suspected when the evidence consists of small positive studies, when most trials
are industry-funded with none reporting negative results, or when funnel plot
asymmetry is present. Rate down one level when strongly suspected.

Note honestly that detection methods are weak with fewer than about ten studies.

---

## Rating up (observational evidence only)

Applied only when risk of bias is not serious.

1. **Large effect.** RR >2 or <0.5 with no plausible confounders → up one.
   RR >5 or <0.2 → up two.
2. **Dose-response gradient.** A monotonic relationship supports causality.
3. **Plausible residual confounding working against the observed effect.** If
   the likely biases would have attenuated the effect and one was still seen,
   the true effect is probably at least as large.

---

## Worked example

*Question: In triple-class-exposed relapsed/refractory multiple myeloma, does
bispecific antibody therapy improve overall survival compared with standard of
care?*

- Evidence: two single-arm trials, one retrospective comparative cohort.
- Start: observational/single-arm → **low**
- Rate down for **indirectness** — no randomised comparison against the relevant
  comparator; single-arm data with an external reference → **very low**
- Consider rating up for large effect — response rates substantially exceed
  historical expectations, but survival comparison remains unadjusted for
  prognostic imbalance → **no rating up**

**Certainty: very low.** Phrasing: *"The evidence is very uncertain about the
effect of bispecific antibody therapy on overall survival in this population;
observed response rates substantially exceed historical benchmarks, but no
randomised comparison exists."*

That statement is defensible, informative, and will survive a guideline
committee reading it. The alternative — *"bispecifics improve survival in
triple-class-exposed myeloma"* — will not, and it is what a summarising agent
produces if nobody applies this framework.

---

## Using GRADE in Medical Affairs deliverables

**Where it earns its place:** evidence gap analyses, scientific platform
documents, medical strategy evidence reviews, payer and guideline submissions,
and any internal document that will inform a funding decision.

**Where it is overkill:** a KOL pre-read brief, a congress readout. There, the
underlying discipline still applies — name the design, state the limitation —
but formal GRADE tables are the wrong register.

**The strategic use.** If your product's evidence for an important clinical
question rates low or very low, that is not a communications problem to be
managed. It is an evidence gap, and it is precisely what `evidence-gap-analysis`
should be surfacing to evidence generation. Guideline committees will apply
GRADE whether or not you do; knowing your own rating first is the entire point.

---

*Primary source: GRADE Handbook (Schünemann et al.) and the GRADE series in the
Journal of Clinical Epidemiology. GRADEpro GDT is the standard tooling.*
