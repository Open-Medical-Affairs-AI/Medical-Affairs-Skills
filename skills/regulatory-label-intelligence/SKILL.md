---
name: regulatory-label-intelligence
description: >-
  Retrieve approved US label content and post-marketing safety data via
  openFDA, and interpret both correctly. Use when you need the exact
  approved indication wording, boxed warnings, contraindications, adverse
  reaction tables or use in specific populations — for medical information
  responses, deciding whether a use is on- or off-label, checking fair
  balance, or looking at FAERS reports. Enforces the correct reading of
  spontaneous reporting data: FAERS has no denominator, disproportionality
  is hypothesis-generating only, and presenting it as incidence is a serious
  error.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: data
  maturity: stable
  requires:
    - medical-affairs-foundations
  suggests:
    - evidence-appraisal
  produces: Label-grounded product facts and correctly-caveated safety context
  network: [api.fda.gov]
---

# Regulatory Label Intelligence

The approved label is the reference standard for what a product is indicated
for, what its known risks are, and — therefore — what is on-label and what is
not. In Medical Affairs, most compliance questions reduce to a label question,
and answering from memory is how people get them wrong.

openFDA also exposes FAERS, the US spontaneous adverse event reporting system.
That data is genuinely useful and is misinterpreted more often than any other
data source in this function. Half of this skill is about interpreting it
correctly.

## The client

```bash
S=skills/regulatory-label-intelligence/scripts/openfda.py

# The approved label, section by section
python3 $S label --generic teclistamab
python3 $S label --brand TECVAYLI --sections boxed_warning,indications_and_usage

# Just the indication wording — what "on-label" actually means
python3 $S indication --generic teclistamab

# Compare label language across a class
python3 $S compare --generics teclistamab,talquetamab,elranatamab --section boxed_warning

# FAERS reaction counts (read the caveats below before using these)
python3 $S faers --generic teclistamab --limit 20
```

`--format json | markdown`. No API key needed; set `OPENFDA_API_KEY` to raise
the limit from 240 requests/minute to 240,000/day.

## Reading a label

The sections that matter for Medical Affairs work, and what each is for:

| Section | What it settles |
|---|---|
| `indications_and_usage` | The **exact** approved population and line of therapy. Read the whole sentence — qualifiers like "who have received at least four prior lines" define the boundary. |
| `boxed_warning` | The most serious risks. Must appear in any balanced discussion. |
| `contraindications` | Absolute — situations where the product must not be used |
| `warnings_and_cautions` | Serious risks with management guidance |
| `adverse_reactions` | Trial-derived rates **with denominators**. This is what you cite for frequency, not FAERS. |
| `use_in_specific_populations` | Pregnancy, lactation, paediatric, geriatric, renal/hepatic impairment |
| `dosage_and_administration` | Including step-up dosing, premedication, monitoring |
| `drug_interactions` | |
| `clinical_studies` | Summary of the registration evidence |

**Quote the label verbatim when the exact wording matters** — and for indication
scope it always matters. Paraphrasing an indication is how a broader claim gets
made by accident.

**The label is jurisdiction-specific.** openFDA is US only. The EU SmPC, the
UK SmPC, and other national labels differ, sometimes materially in indication
wording and population. State which jurisdiction you are describing. For EU,
consult the EMA EPAR and SmPC directly — there is no equivalent open API here.

**Labels change.** openFDA reflects the most recent submitted version, but check
the effective date before relying on it for a high-stakes determination.

## FAERS — the section to read before you use it

FAERS is a **spontaneous reporting system**. Anyone may submit a report;
manufacturers are legally required to. This makes it valuable for detecting rare
events that trials cannot, and unsuitable for almost everything else people try
to use it for.

**What FAERS cannot tell you:**

- **Incidence or rate.** There is no denominator. You do not know how many
  people took the drug, so a count of 412 reports is a count of reports, not a
  rate of anything.
- **Causality.** A report means someone thought it was worth reporting. It does
  not mean the drug caused it.
- **Comparative safety.** Reporting rates differ between products for reasons
  unrelated to safety — time since launch, media attention, litigation,
  indication severity, prescriber population, and whether the product is under
  active surveillance. **Comparing FAERS counts between products is not a
  comparison of their safety profiles**, and presenting it as one is both
  scientifically wrong and, if the other product is a competitor, a compliance
  problem.
- **Whether an event is new.** Reports accumulate for known label events too.

**What FAERS can tell you:**

- That a rare event has been reported at all — signal detection
- What clinicians and patients are reporting, which informs what questions field
  teams will hear
- A hypothesis worth investigating with a designed study

**Known biases:** the Weber effect (reporting peaks in the first two years after
launch and declines), notoriety bias (a media story or a label change causes a
reporting spike), duplicate reports, and heavy under-reporting overall — most
adverse events are never reported.

**How to state a FAERS finding honestly:**

> FAERS contains 412 reports of cytokine release syndrome associated with
> [product] (retrieved 2026-08-14). Spontaneous reports have no denominator and
> cannot establish incidence or causality; reporting is influenced by launch
> recency and by known-risk awareness. The label reports CRS in 72.1% of
> patients in the registration trial (n=165), which is the appropriate source
> for frequency.

That last sentence is the move that matters. **When a labelled rate exists, cite
the label, not FAERS.** FAERS is for what the label does not yet cover.

## Using this in practice

**Determining on- vs off-label.** Retrieve `indications_and_usage`, compare the
proposed use against the exact wording, and state the conclusion with the
jurisdiction. If the use falls outside it, `medical-affairs-foundations` governs
what may be said and through which channel.

**Fair balance in a deliverable.** Any document discussing efficacy must carry
the boxed warning and principal safety information with comparable prominence.
Pull them from the label rather than from a summary.

**Medical information responses.** The label is the primary source. Where the
question goes beyond it, `pubmed-search` and the reactive-request pathway apply.

**Class comparison.** `compare --section` puts the same section from several
products side by side. Useful and legitimate for internal understanding of a
class. It becomes a compliance issue the moment it turns into an external
comparative claim without head-to-head evidence.

**Recalls.** `enforcement` covers product recalls and field actions — relevant
to product quality complaint context.

## Before you finish

Read `house-rules/regulatory-label-intelligence.md`. Many organisations require
the local label rather than the US one, and specify which safety information
must appear in which deliverables.

Verify anything you quote against the current label — this API is a convenience
layer over documents that are themselves the authority.

## References

- `references/openfda-api.md` — endpoints, the search syntax, field paths,
  `count` aggregation, pagination, and rate limits.
- `references/label-sections.md` — what each PLR label section contains, how EU
  SmPC sections map onto it, and where the two commonly diverge.
