---
name: evidence-appraisal
description: >-
  Critically appraise clinical evidence the way an experienced Medical
  Affairs scientist does — before summarising, citing or building strategy
  on it. Use whenever you read, cite, compare or draw a conclusion from a
  trial, publication, congress abstract, real-world study, meta-analysis or
  safety database. Covers what each design can support, effect measures and
  confidence intervals, multiplicity, subgroup interpretation, non-
  inferiority margins, surrogate endpoints, time-to-event pitfalls, risk-of-
  bias tools and GRADE. Use especially when someone asks which product is
  better, or a claim sounds stronger than the design allows.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: foundation
  maturity: stable
  requires:
    - medical-affairs-foundations
  produces: Appraised evidence with stated certainty and limitations
---

# Evidence Appraisal

The job here is to know what a result actually supports before anyone builds on
it. Most bad Medical Affairs output is not fabricated — it is a real number,
correctly quoted, carrying a conclusion its design cannot bear.

Apply this to every piece of evidence you touch. It is not a separate step you
do when asked to appraise something; it is what reading means.

## The four questions, in order

Ask these of any study before you quote a single number.

**1. What question was this designed to answer?** Not the question you want
answered. A trial powered for PFS in a biomarker-positive second-line population
does not answer what happens in first line, in biomarker-negative patients, or
for overall survival.

**2. Could the design answer it?** Randomised and adequately powered, or
single-arm? Prospective or retrospective? Was the primary endpoint pre-specified,
and is the result you are quoting the primary endpoint or something further down
the list?

**3. What is the effect, with what precision?** The point estimate alone is
almost meaningless. The confidence interval tells you what the data are
compatible with.

**4. Who does this apply to?** The trial population is rarely the clinic
population. Eligibility criteria, performance status, prior lines, organ
function, age, and comorbidity all constrain generalisability.

If you cannot answer all four from what you have, say so. "The abstract does not
report the confidence interval" is a legitimate and useful statement. Inventing
one is not.

## Design hierarchy — what each can support

| Design | Supports | Does not support |
|---|---|---|
| Well-conducted RCT, pre-specified primary endpoint | Causal inference for that endpoint, in that population, vs. that comparator | Effects in unstudied populations; endpoints not powered for |
| RCT secondary endpoint | Supportive evidence, hypothesis-strengthening | Standalone causal claims, unless alpha was formally allocated |
| Non-inferiority RCT | That the product is not worse by more than the margin | Superiority, unless pre-specified and hierarchically tested |
| Single-arm trial | Response rates and safety observations in that cohort | Any comparative or causal claim. There is no counterfactual. |
| Prospective observational cohort | Association, natural history, real-world patterns | Causality, without serious confounding control |
| Retrospective database study | Hypothesis generation, association, feasibility | Causality. Confounding by indication is usually fatal. |
| Registry | Long-term safety signals, practice patterns, rare events | Comparative effectiveness without careful design |
| Case series / case report | Existence, feasibility, rare event description | Frequency, causality, or effect size |
| Spontaneous reports (FAERS, EudraVigilance) | Signal detection, hypothesis generation | Incidence, risk, or causality. No denominator exists. |
| Meta-analysis of RCTs | Pooled effect, when studies are combinable | More certainty than the underlying trials, if they were biased |
| Network meta-analysis | Indirect comparison under stated assumptions | Anything, if transitivity fails |

**The single-arm rule.** A single-arm trial result is what happened to those
patients. It is not what the drug does relative to anything. Every time you cite
one, name the design in the same sentence: *"in the single-arm X trial, ORR was
63% (95% CI 54–71)"*, never *"X produces responses in 63% of patients"*.

## Reading the numbers

Four rules apply without being looked up. The rest — effect-measure definitions,
analysis populations, multiplicity, non-inferiority margins, time-to-event
pitfalls and meta-analysis — is in `references/statistical-interpretation.md`.
Open it whenever you are appraising a specific result rather than recalling a
rule.

**State relative and absolute together.** A 50% relative risk reduction is 25
percentage points if the control rate is 50% and 0.05 percentage points if it is
0.1%. Reporting only the relative measure is the commonest way a modest effect
is made to sound transformative, and it is recognised as misleading reporting
rather than a stylistic choice.

**Never quote a point estimate without its interval.** The confidence interval
is what tells you what the data are compatible with; the estimate alone is an
assertion. A wide interval means few events, however attractive the midpoint.

**A secondary endpoint below a failed step in the testing hierarchy is
descriptive only** — nominal, no matter how small the p-value. Check the
hierarchy and alpha allocation before treating any secondary endpoint as
positive. Interim analyses spend alpha too, and a trial stopped early for
benefit overestimates the effect.

**A subgroup result is hypothesis-generating** unless it was pre-specified,
powered, and supported by a significant *interaction* test. Comparing p-values
across subgroups is not an interaction test, and twenty subgroups will produce
one or two striking results by chance.

## Endpoints

Surrogate endpoints — ORR, PFS, DFS, MRD-negativity, biomarker change, ctDNA
clearance — are not clinical benefit unless validated as predicting it *in that
disease and that setting*. State the endpoint type whenever you cite it:
"improved PFS" is a finding, "improved outcomes" is an interpretation that
needs justifying.

Before quoting a hazard ratio, check proportional hazards, censoring, assessment
schedule, crossover and data maturity — the five ways an HR misleads are set out
in `references/statistical-interpretation.md`.

## Cross-trial comparison

**Naive cross-trial comparison is not evidence.** Different populations,
eligibility criteria, prior therapy, geography, standard of care, era,
assessment schedules, and censoring rules make raw numbers non-comparable. This
holds even when the trials look similar.

Where a comparison is genuinely needed, adjusted methods exist — Bucher indirect
comparison, network meta-analysis, MAIC, STC — each with assumptions that must
be stated and can fail. See `references/indirect-comparisons.md`.

In Medical Affairs this is also a compliance boundary, not only a scientific
one: presenting a cross-trial numerical comparison as evidence of superiority is
a promotional claim without substantiation.

## Risk of bias and certainty

Name the instrument you used. **RoB 2** for randomised trials, **ROBINS-I** for
non-randomised studies of interventions, **Newcastle-Ottawa** for cohort and
case-control, **QUADAS-2** for diagnostic accuracy. Domains and worked detail
are in `references/bias-checklists.md`.

**GRADE** rates certainty in a body of evidence — high, moderate, low, very low
— starting from design and rating down for risk of bias, inconsistency,
indirectness, imprecision and publication bias, or up for large effect,
dose-response, and plausible confounding working against the observed effect.
See `references/grade.md`.

Certainty is a property of the body of evidence for a specific question, not a
badge on a paper. A meta-analysis of biased trials is a precise biased estimate;
pooling and heterogeneity are covered in
`references/statistical-interpretation.md`.

## Real-world evidence

RWE answers questions RCTs cannot — long-term outcomes, unselected populations,
comparative effectiveness in practice — and is uniquely vulnerable to specific
biases: confounding by indication, immortal time bias, prevalent user bias,
and outcome misclassification. Target trial emulation is the framework that
makes RWE credible. See `references/real-world-evidence.md`.

## How to report an appraisal

Whatever the deliverable, an appraised citation carries: design, N, population,
comparator, endpoint and its type, effect estimate with confidence interval,
whether it was primary or where it sat in the hierarchy, and the principal
limitation.

> MajesTEC-1 (single-arm, phase 1/2, N=165, triple-class-exposed RRMM): ORR
> 63.0% (95% CI 55.2–70.4), median follow-up 14.1 months. Single-arm design —
> no comparative inference. CRS in 72.1% (grade ≥3, 0.6%).

That is one sentence longer than the unappraised version and it is the
difference between a claim that survives review and one that does not.

Before finishing, read `house-rules/evidence-appraisal.md` — organisations
differ on evidence thresholds and on what they will allow to be cited.

## References

- `references/grade.md` — applying GRADE, with the rating-down and rating-up
  criteria and how to phrase a certainty statement.
- `references/indirect-comparisons.md` — Bucher, NMA, MAIC, STC: assumptions,
  failure modes, and how to describe results honestly.
- `references/bias-checklists.md` — RoB 2, ROBINS-I, Newcastle-Ottawa domains in
  working detail.
- `references/real-world-evidence.md` — target trial emulation and the named
  biases that recur in database studies.
- `references/statistical-interpretation.md` — effect measures, analysis
  populations, multiplicity, subgroups, non-inferiority, time-to-event
  pitfalls and meta-analysis, in working detail.
