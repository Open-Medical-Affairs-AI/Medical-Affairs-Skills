## Long-horizon objectives

Some jobs need several workflows chained. Example:

> "We have an advisory board in three weeks. Work out the five most important
> scientific questions to explore and prepare the briefing materials."

Do not attempt this in one pass. Decompose, state the plan, and let each stage
feed the next:

```
1. evidence-gap-analysis      → what we genuinely do not know
2. field-insight-synthesis    → what the field is asking that we cannot answer
3. congress-intelligence      → what changed recently that bears on it
   ─────────────────────────────────────────────────────────────────
4. strategic-analysis         → rank to the five questions worth an advisory board
5. medical-slide-deck         → the pre-read, weighted toward questions
6. kol-engagement-brief       → one per advisor
7. mlr-review-readiness       → before anything leaves the building
```

State the decomposition before starting and report at each boundary, so the
person can redirect early rather than after everything is built.

**Where a stage produces nothing useful, say so and continue.** "The gap
analysis found no unanswered question that would justify an advisory board on
this topic" is a legitimate finding, and exactly the kind an agent optimising
for apparent productivity avoids.


**A whole launch plan** is the largest chain in the library and has its own
coordinator: load `medical-launch-plan`. It runs the workflows as an org chart
of digital workers, each with its own context packet, in waves separated by
human decision gates, and ends with an independent readiness verdict.

For checkpoint format and change propagation, read [execution.md](../../../docs/execution.md).
