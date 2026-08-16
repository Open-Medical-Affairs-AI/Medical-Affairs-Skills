---
name: medical-terminology-mapping
description: >-
  Resolve free-text clinical language to controlled vocabulary so insights,
  adverse events, conditions and interventions can be counted and compared
  consistently. Use when coding field insights into a taxonomy, normalising
  adverse event verbatims toward MedDRA, building a PubMed search that needs
  the right MeSH descriptor, or deduplicating a dataset where one concept
  appears in a dozen phrasings. Covers MeSH, queried live, and how to work
  correctly with MedDRA, SNOMED CT, ICD and ATC — which are licensed, so
  none of their content ships here.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0.0"
  tier: data
  maturity: beta
  requires:
    - medical-affairs-foundations
  produces: Concept-to-code mappings with confidence and unresolved list
  network: [eutils.ncbi.nlm.nih.gov]
---

# Medical Terminology Mapping

Field insights, medical information enquiries, and advisory board notes all
arrive as free text. Free text cannot be counted. Twelve MSLs describing the
same concern in twelve ways produces a frequency of one for each, and the signal
disappears.

Mapping to controlled vocabulary is what makes aggregation honest — and it is
also where a subtle error can manufacture a signal that is not there, by
collapsing distinct concepts into one code.

## The rule

**Resolve, then validate. Never invent a code.**

A code you have not looked up is as dangerous as a citation you have not
resolved — arguably worse, because a wrong code propagates silently into counts
that other people then act on. If a concept does not resolve, report it as
unresolved. An unresolved list is useful; a fabricated code is not.

## What you can resolve here, and what you cannot

| Vocabulary | Use | Availability |
|---|---|---|
| **MeSH** | Literature indexing, PubMed search construction, broad disease and intervention concepts | **Public domain.** Queried live via NCBI — this skill resolves it. |
| **MedDRA** | Adverse event and medical history coding; the regulatory standard for safety | **Licensed** (MSSO subscription). Not shipped, not resolvable here. |
| **SNOMED CT** | Clinical documentation, EHR-derived data | **Licensed** (Affiliate; free in Member countries via the national release centre). Not shipped. |
| **ICD-10 / ICD-11** | Diagnosis, claims, epidemiology | WHO/CMS terms apply. Not shipped. |
| **ATC** | Drug classification | WHO Collaborating Centre terms apply. Not shipped. |
| **RxNorm / UNII** | US drug normalisation | Public. Reachable via openFDA `openfda.rxcui` / `openfda.unii`. |
| **LOINC** | Laboratory observations | Free with registration. Not shipped. |

This is a real constraint, deliberately observed. Redistributing licensed
terminology would expose adopters to a licensing problem they did not choose.
Where a licensed vocabulary is required, this skill tells you what to do and
hands off to a human with the licence.

## The client

```bash
S=skills/medical-terminology-mapping/scripts/mesh_resolve.py

# Free text -> MeSH descriptor
python3 $S resolve --terms "myeloma, skin rash, tocilizumab"

# A whole column of verbatims
python3 $S resolve --file insights.csv --column observation

# Is this descriptor real and current?
python3 $S validate --terms "Multiple Myeloma,Plasmacytoma,Not A Real Heading"
```

Output carries a confidence per mapping and an explicit unresolved list.

## Method

### 1. Decide what you are mapping for

The purpose determines the vocabulary and the granularity, and getting this
wrong wastes the whole exercise.

- **Counting insights by theme** → a local taxonomy, mapped loosely. Precision
  matters less than consistency.
- **Adverse event terminology** → MedDRA. Nothing else is acceptable to
  pharmacovigilance, and this skill cannot do it — route to PV.
- **Building a literature search** → MeSH. This is what MeSH is for.
- **Aggregating EHR or claims data** → SNOMED CT or ICD.
- **Comparing across data sources** → you will need a crosswalk, and crosswalks
  are lossy. Say so.

### 2. Normalise before mapping

Free text needs light cleaning first, and heavy cleaning destroys meaning:

- Expand abbreviations **in context** — "MM" is multiple myeloma in one corpus
  and mucous membrane in another. Do not expand from a global dictionary.
- Preserve negation. "No evidence of progression" and "progression" are
  opposites and both contain the word.
- Preserve severity, temporality, and grade. "Grade 3 CRS" and "mild CRS" should
  not collapse to one code without the qualifier being carried.
- Keep the verbatim alongside the code, always. Someone will need to re-examine
  it.

### 3. Resolve, with graded confidence

| Confidence | Basis |
|---|---|
| **Exact** | String matches the preferred term |
| **Synonym** | Matches a recorded entry term |
| **Narrower/broader** | Resolves to a parent or child concept — state which, because it changes the count |
| **Fuzzy** | Approximate match. Requires human confirmation before use. |
| **Unresolved** | No credible match. Report as unresolved. |

Never silently promote a fuzzy match to a confident one. Where the count matters
— and it usually does — a human reviews the fuzzy and unresolved lists before
any aggregate is published.

### 4. Watch for the errors that manufacture signal

- **Over-collapsing.** Mapping "fatigue", "asthenia", and "lethargy" to one code
  triples an apparent frequency. Sometimes correct, sometimes not. Decide
  deliberately and record the decision.
- **Under-collapsing.** Leaving "CRS", "cytokine release syndrome", and
  "cytokine storm" as three concepts destroys a real signal.
- **Losing the qualifier.** Grade, severity, and body site frequently carry the
  clinical meaning.
- **Mapping the wrong axis.** A drug name mapped to a disease concept because
  the string matched an indication.
- **Ignoring negation.** Mapping "no infection" to "infection" is a
  straightforward error with clinical consequences.

### 5. Report the mapping, not just the result

Any aggregate built on mapped data ships with the mapping visible:

```markdown
## Terminology mapping

Vocabulary: MeSH (2026), resolved via NCBI E-utilities on 2026-08-14

| Verbatim (n) | Mapped concept | Confidence | Note |
|---|---|---|---|
| "cytokine release syndrome" (14) | Cytokine Release Syndrome | exact | |
| "CRS" (9) | Cytokine Release Syndrome | synonym | |
| "cytokine storm" (3) | Cytokine Release Syndrome | synonym | Collapsed deliberately |
| "infusion reaction" (4) | — | unresolved | Distinct concept; NOT collapsed into CRS |

**Unresolved (6 of 52 verbatims).** Listed in full in the appendix and reviewed
by [name]. Counts below exclude them.

**Collapsing decisions.** "Fatigue" and "asthenia" were kept separate because
the source notes distinguish them consistently.
```

The collapsing decisions section is what makes the counts defensible. Without
it, a reader cannot tell whether a frequency of 26 is one concept or three.

## Adverse event terminology — the boundary

If you are mapping adverse event verbatims, stop and read this.

MedDRA coding is a **regulated activity** performed by trained coders in a
validated system, following version-controlled conventions. Getting it wrong
changes seriousness assessment, signal detection, and regulatory reporting.

This skill can help you **recognise and group** AE-related language so that
nothing is missed and so that field insights can be triaged. It cannot and must
not produce MedDRA codes for regulatory use.

The workflow: detect and surface the AE verbatim
(`medical-affairs-foundations`), route it to pharmacovigilance with the verbatim
intact, and let qualified coders code it. Any grouping you do for insight
analysis is explicitly labelled as **analytical grouping, not MedDRA coding**.

## Building a local insight taxonomy

Most Medical Affairs insight programmes need a house taxonomy rather than a
standard vocabulary — and most house taxonomies fail the same way, by growing
categories until nothing is comparable year on year.

What works:

- **Two axes, not one.** Typically *topic* (efficacy, safety, access, unmet
  need, competitor, practice pattern) crossed with *object* (product, class,
  disease, pathway). One flat list collapses under its own weight.
- **A small, fixed top level.** 6–10 categories. Detail lives in a second level
  that can grow.
- **A defined "other".** Reviewed every cycle. A growing "other" is the signal
  that the taxonomy needs revision.
- **Version it.** Changing the taxonomy breaks trend comparison unless you
  record when it changed and re-map history or declare the break.

Put your taxonomy in `house-rules/medical-terminology-mapping.md` and this skill
will use it.

## Before you finish

Read `house-rules/medical-terminology-mapping.md`. This is the skill most likely
to need local configuration — every organisation has its own taxonomy, and using
the wrong one makes the output useless.
