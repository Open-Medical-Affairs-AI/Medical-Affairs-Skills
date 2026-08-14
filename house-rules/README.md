# House Rules

This is where your organisation's practice overrides the library's defaults.

Every skill reads `house-rules/<skill-name>.md` before it produces anything.
Rules written here **beat** the defaults in the skill. You should not need to
fork this repository to make it behave like your company.

## Why this exists

The skills in this library encode general Medical Affairs practice. Your
organisation has SOPs, terminology, evidence thresholds, review pathways, and
hard-won lessons that differ — sometimes materially. Forking to encode them
means you never get upstream improvements again. Writing them here means you do.

## How to write a rule

Open the file for the skill, find the marker, and write below it:

```
## YOUR RULES — ADD BELOW THIS LINE
```

Rules work best when they are specific and explain themselves. The agent follows
reasoning better than it follows commands, and a rule with a reason generalises
to the cases you did not anticipate.

**Weak:** "Be careful with safety data."

**Strong:** "Never present an adverse event rate from a single-arm trial without
the denominator and the median follow-up alongside it. Rates from short
follow-up understate cumulative toxicity, and our reviewers send this back every
time."

## Where these come from

The best source is the feedback your medical reviewers give repeatedly. If the
same correction comes back on every document, that correction is a house rule
that has not been written down yet.

## A note for workshop participants

This is Round 2. Pick the skill your team used, add three to five rules
capturing what an experienced person on your team knows that the agent does not,
and run the same mission again. Compare the output.

That difference — generic agent, to Medical Affairs agent, to *your* Medical
Affairs agent — is the point of the exercise.
