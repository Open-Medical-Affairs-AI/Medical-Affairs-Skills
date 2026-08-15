# Medical Slide Patterns

Layouts for the recurring medical slide types, and the specific way each one
goes wrong.

---

## The efficacy results slide

**Contains:** design and population in the subtitle · the endpoint · the effect
estimate with its confidence interval · N · the citation footnote.

**Goes wrong by:** a headline that states a conclusion rather than a finding.
"Substantial activity in heavily pretreated patients" is an interpretation.
"ORR 63.0% (95% CI 55.2–70.4) in triple-class-exposed patients (single-arm,
n=165)" is a finding. The interpretation belongs in the speaker's mouth where a
clinician can challenge it, not printed as a title where it looks settled.

**Also goes wrong by:** showing the response rate without the duration. A high
response rate with a three-month median duration is a different clinical story
from the same rate holding at eighteen months, and the second slide is often the
one omitted.

---

## The Kaplan-Meier slide

**Must contain a numbers-at-risk table.** Without it the tail is
uninterpretable — and the tail is exactly where the audience is looking. A curve
that appears to plateau on the strength of four remaining patients has told you
nothing, and the numbers-at-risk row is the only thing that reveals it.

**Also include:** median with CI for each arm, HR with CI, the number of events
(not just N), median follow-up, and censoring marks.

**Goes wrong by:** truncating the y-axis to exaggerate separation, omitting
censoring marks, and quoting a hazard ratio where the curves cross. If the
curves cross or separate late, a single HR is a weighted average that describes
no patient's experience — show RMST or a landmark analysis alongside it.

---

## The safety slide

**Contains:** the safety population and its denominator (different from the
efficacy population), any-grade and grade ≥3 rates, discontinuations due to
adverse events, deaths, and the events requiring specific management.

**Goes wrong by:** appearing twenty slides after the efficacy data, in smaller
type, with grade ≥3 rates only. Fair balance is about prominence, not presence.

**Also goes wrong by:** "well tolerated". It is a conclusion, it is not
supported by a rate table, and it is the phrase most likely to be flagged in
review.

---

## The comparative slide

**The default answer is: do not build one.** Cross-trial comparison is not
evidence, and a side-by-side layout asserts comparability whatever the footnote
says. Two columns of numbers from two trials communicate "these are comparable"
faster than any caveat can undo.

**If a comparison is genuinely needed:** use an adjusted method
(`evidence-appraisal/references/indirect-comparisons.md`), state the method and
its assumptions on the slide itself, and show the populations side by side so
the audience can see how different they are.

**Never** place two trials' results in adjacent columns without population
characteristics next to them.

---

## The "what we don't know" slide

The slide that builds the most credibility and is most often cut for time.

**Contains:** the questions the evidence does not answer, stated plainly, and —
where relevant — what is being done about them.

**Goes wrong by:** being omitted, or by being softened into "areas for future
research", which reads as a formality rather than an admission.

Put it before the questions section, not in the backup. An audience that has
heard you say what you do not know will believe what you say you do.

---

## The mechanism slide

**Contains:** the mechanism at the depth the audience needs, with the evidence
for it. Preclinical mechanism is preclinical — label it.

**Goes wrong by:** presenting a mechanistic rationale as though it were clinical
evidence. A plausible mechanism and an observed clinical effect are different
claims, and the slide should not blur them.

---

## The advisory board question slide

**Contains:** one question. Open. Genuinely uncertain. With enough context to
answer it and not so much that it leads.

**Goes wrong by:** asking a question the company has already answered. Advisors
detect this immediately and adjust — they stop giving advice and start giving
agreement, which is the failure mode the whole meeting exists to avoid.

**The test:** could the answer surprise you? If not, it is not a question.

---

## The backup slide

**Built from anticipated questions**, one per slide, with the appraised answer
and the citation. Not from content that did not fit.

Include slides for the questions you **cannot** answer, saying so. A presenter
who can turn to a slide that says "no data exist on this; here is what is
planned" is more credible than one who improvises.

---

## Typography and layout that affect comprehension

- **18pt minimum** for anything an audience must read from a data table.
- **One idea per slide.** A slide making three points makes none.
- **Do not use colour as the only encoding.** Around 8% of men have a colour
  vision deficiency. Add pattern, position, or direct labels.
- **Direct-label lines** rather than using a legend where possible — it removes
  a lookup step for the reader.
- **Highlight one row** in any table over six rows, or none will be read.
- **Left-align text; right-align numbers.** Decimal alignment for columns of
  estimates.
- **Consistent decimal places** within a column. Mixed precision reads as
  carelessness and undermines the data.
