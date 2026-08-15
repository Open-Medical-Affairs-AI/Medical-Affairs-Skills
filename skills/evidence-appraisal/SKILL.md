---
name: evidence-appraisal
description: >-
  Critically appraise clinical evidence the way an experienced Medical Affairs
  scientist does — before summarising, citing, or building strategy on it. Use
  whenever you read, cite, compare, or draw a conclusion from a clinical trial,
  publication, congress abstract, real-world study, meta-analysis, or safety
  database. Covers study design and what each design can support, effect
  measures and confidence intervals, ITT versus per-protocol, multiplicity and
  hierarchical testing, subgroup interpretation, non-inferiority margins,
  surrogate versus clinical endpoints, time-to-event pitfalls including the
  proportional hazards assumption and informative censoring, risk-of-bias tools
  (RoB 2, ROBINS-I, Newcastle-Ottawa), GRADE certainty, single-arm and external
  control studies, meta-analysis heterogeneity, and why naive cross-trial
  comparison is not evidence. Use it especially when someone asks which of two
  products is better, or when a claim sounds stronger than the design allows.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: foundation
  maturity: stable
  requires: [medical-affairs-foundations]
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

## Effect measures and what they hide

**Relative vs absolute.** A relative risk reduction of 50% is a 25 percentage-
point absolute reduction if the control rate is 50%, and a 0.05 percentage-point
reduction if the control rate is 0.1%. Relative measures are stable across
baseline risk and are what trials report; absolute measures are what determine
clinical value. **State both.** Reporting only the relative measure is the single
most common way of making a modest effect sound transformative — and it is a
recognised form of misleading reporting, not a stylistic choice.

- **Hazard ratio (HR)** — the ratio of instantaneous event rates over time. HR
  0.70 means a 30% reduction in the hazard *at any given moment*, not that 30%
  more patients survive, and not that patients live 30% longer.
- **Odds ratio (OR)** — approximates RR when events are rare (<10%), and
  materially overstates it when they are common. Watch for ORs from logistic
  regression being spoken about as risk ratios.
- **Risk ratio / relative risk (RR)** — ratio of cumulative incidence. More
  intuitive; less used in time-to-event settings.
- **Absolute risk reduction (ARR)** and **number needed to treat (NNT = 1/ARR)**
  — NNT is time-dependent and only meaningful with the time horizon attached.
  An NNT of 25 "at 2 years" is a different claim from an NNT of 25.
- **Median difference** — a median PFS improvement of 3.2 months describes the
  midpoint, not the average benefit, and says nothing about the tail. With
  crossing or non-proportional hazards, the median can move while the curves
  tell a different story.
- **Restricted mean survival time (RMST)** — increasingly reported, and more
  robust when proportional hazards fails. Difference in RMST is interpretable as
  average time gained over a defined horizon.

**Confidence intervals do the work.** A CI that crosses 1.0 (for a ratio) or 0
(for a difference) is compatible with no effect. A very wide CI means the study
was small or events were few, regardless of how attractive the point estimate
is. Report the interval whenever you report the estimate; a point estimate
without its interval is an assertion, not a result.

**P-values.** A p-value is not the probability the treatment works, not the
probability the null is true, and not a measure of effect size. p = 0.049 and
p = 0.051 are the same evidence. Statistical significance in a large trial can
accompany a clinically trivial effect.

## Analysis populations

- **ITT (intention-to-treat)** — everyone randomised, analysed as randomised.
  Preserves randomisation and is conservative for superiority. The default for
  efficacy.
- **mITT (modified ITT)** — ITT with exclusions. The exclusions are where the
  bias enters. Always ask what was excluded and whether the definition was
  pre-specified; a post-hoc mITT is a red flag.
- **Per-protocol** — only compliant patients. Breaks randomisation and generally
  favours the active arm because compliance correlates with doing well. It is,
  however, the *less* conservative choice in a non-inferiority trial — which is
  why non-inferiority trials should report both and agree.
- **Safety population** — everyone who received any dose, analysed as treated.
  Correct for safety, and note it is a different denominator from the efficacy
  population.

Discordance between ITT and per-protocol results is informative, not a
technicality. Say so when you see it.

## Multiplicity and the testing hierarchy

Modern trials pre-specify a hierarchical testing sequence with formal alpha
allocation. Once a step in the hierarchy fails, everything below it is
**nominal** — descriptive only, no matter how small the p-value.

This is routinely mishandled. If OS was tested after PFS in a fixed sequence and
PFS did not meet its boundary, an OS p-value of 0.01 is not a positive OS
result. Check the statistical analysis plan or the paper's methods for the
hierarchy and alpha spending before treating any secondary endpoint as positive.

Interim analyses spend alpha too. A trial stopped early for benefit at an
interim tends to **overestimate** the effect size, particularly with few events.

## Subgroups

Treat a subgroup result as hypothesis-generating unless all of these hold:
pre-specified, with a pre-specified hypothesis and direction; adequately
powered; and supported by a statistically significant **interaction test**, not
merely a significant result within the subgroup.

The recurring error is comparing p-values across subgroups. A significant effect
in men and a non-significant effect in women does not demonstrate that the
treatment works differently by sex — that requires the interaction test, and
non-significance in a smaller subgroup is usually just less power.

Forest plots of twenty subgroups will contain one or two apparently striking
results by chance alone. That is what the multiplicity is.

## Non-inferiority

Three things determine whether a non-inferiority result means anything:

1. **The margin, and its justification.** Was it derived from the historical
   effect of the active comparator against placebo, and does it preserve a
   clinically meaningful fraction of that effect? A margin chosen for
   feasibility rather than clinical logic makes the whole trial uninterpretable.
2. **Assay sensitivity.** Could this trial have detected a difference if one
   existed? If the comparator underperformed its historical effect, non-
   inferiority may reflect a failed trial rather than an equivalent product.
3. **Both analysis populations agreeing.** ITT and per-protocol should both
   support non-inferiority.

Non-inferiority never establishes superiority. Superiority claims from a
non-inferiority trial require pre-specified hierarchical testing.

## Endpoints

**Surrogate endpoints** — ORR, PFS, DFS, MRD-negativity, biomarker change,
ctDNA clearance — are not clinical benefit unless validated as predicting it
*in that disease and that setting*. Validation is setting-specific: a surrogate
that tracks survival in one line of therapy may not in another.

State the endpoint type whenever you cite it. "Improved PFS" is a real finding.
"Improved outcomes" is an interpretation that requires justification.

**Time-to-event pitfalls** worth checking before you quote an HR:

- **Proportional hazards.** The HR assumes a constant ratio over time. With
  crossing curves, delayed separation (common in immunotherapy), or plateaus, a
  single HR is a weighted average that may describe no patient's experience.
  Look for a Schoenfeld residual test, or landmark/RMST analyses reported
  alongside.
- **Censoring.** Informative censoring — patients censored for reasons related
  to prognosis — biases the estimate. Check the censoring rules and rates by arm.
- **Assessment schedule.** PFS depends on how often you look. Different
  imaging intervals between arms or between trials make PFS non-comparable.
- **Crossover.** Extensive crossover to the experimental arm dilutes an OS
  difference. Adjusted analyses (RPSFT, IPCW) exist and their assumptions should
  be stated.
- **Immature data.** An HR from few events moves a lot with additional
  follow-up. Check the event count, not just the N.

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

Use the right instrument and name it:

- **RoB 2** — randomised trials. Five domains: randomisation process, deviations
  from intended interventions, missing outcome data, measurement of the outcome,
  selection of the reported result.
- **ROBINS-I** — non-randomised studies of interventions. Seven domains,
  including confounding and selection into the study. The key move is comparing
  against a hypothetical target trial.
- **Newcastle-Ottawa Scale** — cohort and case-control studies. Widely used,
  crude, and better than nothing.
- **QUADAS-2** — diagnostic accuracy studies.

**GRADE** rates certainty in a body of evidence — high, moderate, low, very low
— starting from design and rating down for risk of bias, inconsistency,
indirectness, imprecision, and publication bias, or up for large effect,
dose-response, and plausible confounding working against the observed effect.
See `references/grade.md`.

Certainty is a property of the body of evidence for a specific question, not a
badge on a paper.

## Meta-analysis

- **Heterogeneity.** I² describes the proportion of variability due to
  heterogeneity rather than chance. High I² does not invalidate a pooled
  estimate but demands explanation. Pooling clinically dissimilar studies
  produces a precise number describing nothing.
- **Fixed vs random effects.** Fixed assumes one true effect; random assumes a
  distribution. Random effects give wider intervals and weight small studies
  more heavily — which matters when small studies are the biased ones.
- **Publication bias.** Funnel plot asymmetry and Egger's test are weak with few
  studies. Absence of evidence of publication bias is not evidence of its
  absence.
- **Garbage in.** A meta-analysis of biased trials is a precise biased estimate.

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
