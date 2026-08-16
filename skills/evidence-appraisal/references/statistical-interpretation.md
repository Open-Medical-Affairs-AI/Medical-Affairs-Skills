# Statistical interpretation — the working detail

Everything here was once in the always-loaded body of `evidence-appraisal`. It
moved because it is reference material: you reach for it when appraising a
specific result, not on every task. The body keeps the rules you must apply
without being asked; this file keeps the detail you look up.

---

## Effect measures

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
is. A point estimate without its interval is an assertion, not a result.

**P-values.** A p-value is not the probability the treatment works, not the
probability the null is true, and not a measure of effect size. p = 0.049 and
p = 0.051 are the same evidence. Statistical significance in a large trial can
accompany a clinically trivial effect.

---

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

---

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

---

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

---

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

---

## Time-to-event pitfalls

Check these before you quote a hazard ratio:

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

---

## Surrogate endpoints

ORR, PFS, DFS, MRD-negativity, biomarker change and ctDNA clearance are not
clinical benefit unless validated as predicting it *in that disease and that
setting*. Validation is setting-specific: a surrogate that tracks survival in one
line of therapy may not in another.

State the endpoint type whenever you cite it. "Improved PFS" is a real finding.
"Improved outcomes" is an interpretation that requires justification.

---

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

---

## Risk-of-bias instruments — which to use

- **RoB 2** — randomised trials. Five domains: randomisation process, deviations
  from intended interventions, missing outcome data, measurement of the outcome,
  selection of the reported result.
- **ROBINS-I** — non-randomised studies of interventions. Seven domains,
  including confounding and selection into the study. The key move is comparing
  against a hypothetical target trial.
- **Newcastle-Ottawa Scale** — cohort and case-control studies. Widely used,
  crude, and better than nothing.
- **QUADAS-2** — diagnostic accuracy studies.

Domain-by-domain working detail is in `bias-checklists.md`.
