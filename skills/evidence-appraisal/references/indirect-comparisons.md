# Indirect and Adjusted Comparisons

Read this when there is no head-to-head trial and someone still needs to know
how two treatments compare — which in Medical Affairs is most of the time.

The central discipline: **every method here rests on assumptions that can fail,
and the honest presentation states them.** An indirect comparison presented
without its assumptions is a naive comparison with extra arithmetic.

---

## The baseline: naive comparison is not a method

Putting two trials' numbers side by side and observing that one is larger is not
an indirect comparison. It ignores every difference between the trials, and
those differences are usually larger than the treatment effect being claimed.

What differs between two apparently similar trials:

- **Population** — eligibility criteria, prior lines of therapy, performance
  status, biomarker status, organ function, age distribution, comorbidity
- **Era** — supportive care, imaging, and standard of care all improve over
  time. A 2015 trial's control arm is not a 2024 control arm.
- **Geography** — treatment patterns, access, and population genetics
- **Endpoint definition and assessment schedule** — PFS assessed every 6 weeks
  is not PFS assessed every 12 weeks
- **Censoring rules** and handling of missing data
- **Analysis population** — ITT vs mITT definitions differ

In Medical Affairs, presenting a naive cross-trial comparison as evidence of
superiority is both scientifically indefensible and a promotional claim without
substantiation. Say this plainly when asked to make one.

---

## Bucher indirect comparison

**What it is.** The simplest adjusted method. With trials A-vs-C and B-vs-C, the
A-vs-B effect is estimated by preserving randomisation within each trial and
comparing the *relative* effects, not the absolute arm results.

```
ln(HR_AB) = ln(HR_AC) − ln(HR_BC)
```

**Assumption: transitivity** (also called similarity). The trials must be
sufficiently similar in every effect-modifying respect that the common
comparator C behaves the same way in both. If C's performance differs between
the trials, transitivity has failed.

**How it fails.** The most detectable failure is comparing the control arms: if
the standard-of-care arm achieved median PFS of 5 months in one trial and 9 in
the other, the populations are not exchangeable and the indirect comparison is
not interpretable. Always look at the common comparator arms first.

**What it preserves.** Randomisation within each trial. This is why Bucher beats
naive comparison — it never compares one trial's arm directly to another's.

---

## Network meta-analysis (NMA)

**What it is.** Bucher generalised to a network of many treatments and trials,
combining direct and indirect evidence, usually in a Bayesian framework.

**Assumptions:**

1. **Transitivity** — as above, across the whole network.
2. **Consistency** — direct and indirect estimates for the same comparison
   agree. Testable where a loop exists (node-splitting, design-by-treatment
   interaction models). Inconsistency is a finding, not a nuisance.
3. **Homogeneity** within each pairwise comparison.

**What to check in someone else's NMA:**

- Is the network geometry shown, and are the connections thin? A comparison
  resting on a single small trial is fragile regardless of the credible interval.
- Were effect modifiers assessed for balance across the network?
- Was inconsistency formally tested, and what happened?
- **Rankings and SUCRA are routinely over-read.** A treatment can rank first
  with overlapping credible intervals against everything below it. Ranking
  probabilities describe the probability of being best, not the magnitude of
  being better. Report the effect estimates, not the league table.

---

## Population-adjusted comparisons: MAIC and STC

Used when you have **individual patient data (IPD)** for your trial and only
**aggregate data** for the comparator — the standard situation for a company
comparing its own trial to a competitor's publication.

### MAIC — Matching-Adjusted Indirect Comparison

Reweights your IPD so that its baseline characteristics match the published
aggregate characteristics of the comparator trial, then compares outcomes.

**Assumptions:**
- All effect modifiers (and, for an unanchored comparison, all prognostic
  factors) are measured and adjusted for. This is a strong and unverifiable
  assumption.
- The reported aggregate characteristics are sufficient to characterise the
  comparator population.

**Key diagnostic: effective sample size (ESS).** Reweighting discards
information. If your N=300 trial reweights to an ESS of 42, the comparison rests
on far less data than it appears to, and the intervals should reflect that. An
ESS collapse is the clearest sign that the populations were too dissimilar to
match. **Always report ESS** — a MAIC without it is not interpretable.

### STC — Simulated Treatment Comparison

Fits an outcome regression model on your IPD, then predicts outcomes in the
comparator trial's population. Similar assumptions; different mechanics. More
efficient than MAIC when the outcome model is correctly specified, and more
sensitive to misspecification.

### Anchored vs unanchored — the distinction that matters most

- **Anchored** — a common comparator exists in both trials. Randomisation is
  partially preserved. Requires adjustment for *effect modifiers* only.
- **Unanchored** — no common comparator, typically comparing two single-arm
  trials. Requires adjustment for **all prognostic factors and all effect
  modifiers**, which is essentially never achievable.

NICE DSU Technical Support Document 18 is explicit that unanchored comparisons
carry a very high risk of bias and should be avoided where an anchored
comparison is possible. Unanchored MAIC of two single-arm trials is common in
oncology and should be presented with heavy caveats — it is the weakest
respectable method, not a substitute for evidence.

---

## Choosing, and describing honestly

| Situation | Method | Realistic certainty |
|---|---|---|
| Head-to-head RCT exists | Use it | High |
| Common comparator, aggregate data both sides | Bucher / NMA | Moderate at best |
| Common comparator, IPD one side | Anchored MAIC / STC | Low to moderate |
| No common comparator, single-arm trials | Unanchored MAIC | Very low |
| Nothing comparable | Do not compare | — |

**How to write it up.** Every indirect comparison result should carry, in the
same breath: the method, the assumption it rests on, whether that assumption was
assessed, and the resulting certainty.

> In an anchored MAIC adjusting for prior lines, ISS stage, and cytogenetic
> risk, the estimated HR for PFS was 0.78 (95% CI 0.61–0.99) favouring
> [product]. Effective sample size fell from 312 to 184. This is an adjusted
> indirect comparison, not a head-to-head trial; residual confounding from
> unmeasured effect modifiers cannot be excluded, and no direct comparative
> evidence exists.

Compare that with *"[product] reduces the risk of progression by 22% versus
[competitor]"* — same analysis, and the second version will not survive review.

---

## The Medical Affairs judgement call

Sometimes the right answer to "how do we compare?" is that **the comparison
cannot responsibly be made**, and the useful output is naming the head-to-head
trial or the pragmatic study that would answer it. That is an evidence gap, and
routing it to `evidence-gap-analysis` is more valuable than producing a fragile
number that will be challenged the first time a KOL sees it.

---

*Key sources: Bucher et al. (1997); NICE DSU Technical Support Documents 18
(population-adjusted indirect comparisons) and 3 (network meta-analysis);
Phillippo et al. on MAIC/STC methodology; ISPOR good practices task force
reports on indirect treatment comparisons.*
