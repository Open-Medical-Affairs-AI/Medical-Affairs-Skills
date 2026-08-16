---
name: competitive-intelligence
description: >-
  Track and interpret competitor scientific activity continuously — pipeline
  movement, publication patterns, evidence strategy, regulatory milestones
  and positioning shifts, and what they signal. Use for ongoing competitive
  monitoring, assessing what a competitor announcement means, or preparing
  for a competitor readout. Applies the same evidence appraisal standard to
  competitor data as to your own, because asymmetric scepticism is detected
  immediately and destroys credibility. For a single congress use congress-
  intelligence; this is the continuous view between them.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: workflow
  maturity: stable
  requires:
    - medical-affairs-foundations
    - evidence-appraisal
    - strategic-analysis
  suggests:
    - clinical-trials-search
    - pubmed-search
    - regulatory-label-intelligence
    - congress-intelligence
    - deliverable-quality-review
  produces: Competitive intelligence assessment
  network: [clinicaltrials.gov, eutils.ncbi.nlm.nih.gov, api.fda.gov]
---

# Competitive Intelligence

Competitor scientific strategy is almost entirely public. Trial registrations,
publications, label changes, congress presentations and investor statements
together describe what a competitor believes and where they are going — usually
12 to 24 months before it becomes obvious.

Most companies read this reactively, one announcement at a time, and miss the
trajectory.

## Sources, in order of value

**The trial registry** (`clinical-trials-search`). The richest source available.
Every interventional trial, with phase, population, endpoints, enrolment and
expected completion. Read it as intent: what a competitor is *studying* tells
you what they intend to claim.

Specifically:
- **Endpoints reveal the intended claim.** A trial powered for treatment burden
  rather than response rate signals the axis they intend to compete on.
- **Population reveals the intended positioning.** Earlier line, broader
  eligibility, a specific subgroup.
- **Comparator reveals confidence.** A head-to-head against the market leader is
  a strong signal.
- **`whyStopped` on terminated trials** is high-value intelligence available
  nowhere else. Analysts routinely filter terminated trials out and miss the
  most informative records in the set.

**Publications** (`pubmed-search`). Volume matters less than **coverage** — map
their publications against the questions clinicians ask, and yours against the
same list. Where they have published and you have not is a communication gap
regardless of who has better data.

**Label changes** (`regulatory-label-intelligence`). Indication expansions,
new warnings, population changes.

**Congress activity** (`congress-intelligence`). What they lead with, and what
they have stopped leading with.

**Public corporate statements.** Investor calls and press releases state
strategy more explicitly than any scientific channel. Read them for framing:
the words a company uses about its own product tell you the dimension it intends
to compete on.

## Reading the trajectory

Individual announcements are noise. The signal is in the pattern:

- **Where is their evidence investment going?** Trials started in the last 18
  months describe the next 3 years.
- **What have they stopped?** Terminated programmes and quietly dropped
  indications say as much as new starts.
- **Has their framing shifted?** When a company moves from talking about
  efficacy to talking about administration burden, the axis of competition has
  moved — and a narrative built for the old axis quietly stops answering the
  question being asked.
- **What are they not studying?** A gap in a competitor's programme is either an
  opportunity or a reason they know something you do not.

## The discipline that makes this credible

**Apply the same appraisal standard to their data as to yours.**

The near-universal failure is asymmetry: rigorous scepticism about a
competitor's single-arm study, generosity about your own. External audiences —
and your own field team — detect it immediately, and it destroys the credibility
of everything else in the assessment.

Practical test: write your assessment of their key study, then substitute your
product's name and read it again. If it now reads as unfairly harsh, it was
unfairly harsh.

If a competitor's data is genuinely strong, **say so plainly**. An intelligence
function that never reports bad news is not providing intelligence.

## The compliance boundary

Competitive analysis is legitimate internal intelligence from public sources.

Two lines not to cross:

**Do not gather information improperly.** No misrepresenting your identity, no
soliciting confidential information from employees or investigators, no
accessing material non-public information.

**Do not let internal analysis become external claims.** A side-by-side
comparison of two trials is useful internally and a promotional claim without
substantiation the moment it goes outside (`medical-affairs-foundations`). Mark
internal-only material clearly, because it circulates.

## Output

```
WHAT CHANGED        since the last assessment — with the source and date
WHAT IT SIGNALS     interpretation, and confidence in it
TRAJECTORY          where their evidence investment points, 18-36 months out
IMPLICATIONS        for our evidence, narrative, field and plans
WHAT TO WATCH       specific, with expected timing
WHAT WE GOT WRONG   previous assessments now known to be incorrect
```

That last section is what makes an intelligence function improve. Most drop it.

## Stage 4 — Challenge

Run `deliverable-quality-review`, plus:

- Did I appraise their data as sceptically as my own — or more so?
- Is every claim sourced to something public and dated?
- Am I reporting a trajectory, or a list of announcements?
- Have I said anything that would be a promotional claim if it escaped?

## Before you finish

Read `house-rules/competitive-intelligence.md`. Rules on competitive information
gathering and its distribution are strict and local.
