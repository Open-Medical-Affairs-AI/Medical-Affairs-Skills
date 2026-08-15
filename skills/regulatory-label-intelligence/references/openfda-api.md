# openFDA API — Reference

Base: `https://api.fda.gov`
Docs: https://open.fda.gov/apis/

No key required (240 requests/minute, 1,000/day per IP). A free key raises this
to 240 requests/minute and 240,000/day: https://open.fda.gov/apis/authentication/

---

## Endpoints Medical Affairs uses

| Endpoint | Contains |
|---|---|
| `/drug/label.json` | Structured Product Labeling — the approved US label |
| `/drug/event.json` | FAERS adverse event reports |
| `/drug/ndc.json` | National Drug Code directory — packaging, marketing status |
| `/drug/enforcement.json` | Recalls and field actions |
| `/drug/drugsfda.json` | Approval history, application numbers, submissions |
| `/device/event.json` | MAUDE device adverse events |

---

## Query syntax

```
?search=<field>:"<value>"&limit=<n>
?search=<field>:"<value>"&count=<field>.exact&limit=<n>
```

- **`search`** filters. Quote values containing spaces. Combine with
  `+AND+` and `+OR+`; group with parentheses. URL-encode the whole expression.
- **`count`** aggregates and returns `{"term": ..., "count": ...}` pairs instead
  of records. Append `.exact` to count whole field values rather than tokens —
  without it, "CYTOKINE RELEASE SYNDROME" is counted as three separate words.
- **`limit`** max 1000. **`skip`** max 25000 — deep pagination is not possible,
  so use `count` for aggregate questions.
- **Date ranges:** `field:[20200101+TO+20261231]`

**A 404 with a JSON body means "no matches", not "error".** Handle it as a
legitimate empty result.

---

## Useful field paths

### `/drug/label.json`

Identity lives under `openfda`:
`openfda.generic_name`, `openfda.brand_name`, `openfda.substance_name`,
`openfda.manufacturer_name`, `openfda.product_type`, `openfda.route`,
`openfda.application_number`, `openfda.rxcui`, `openfda.unii`.

Content sections are top-level arrays of strings: `boxed_warning`,
`indications_and_usage`, `dosage_and_administration`,
`dosage_forms_and_strengths`, `contraindications`, `warnings_and_cautions`,
`adverse_reactions`, `drug_interactions`, `use_in_specific_populations`,
`description`, `clinical_pharmacology`, `clinical_studies`,
`how_supplied`, `patient_counseling_information`, `spl_unclassified_section`.

`effective_time` (YYYYMMDD) is the label version date. **Check it** — openFDA
lags label revisions.

```
# All products carrying a boxed warning in a class
?search=_exists_:boxed_warning+AND+openfda.pharm_class_epc:"..."&limit=50
```

### `/drug/event.json` (FAERS)

| Path | Contains |
|---|---|
| `patient.drug.openfda.generic_name` | Drug, normalised |
| `patient.drug.drugcharacterization` | 1 = suspect, 2 = concomitant, 3 = interacting |
| `patient.reaction.reactionmeddrapt` | MedDRA preferred term |
| `patient.reaction.reactionoutcome` | 1 recovered … 5 fatal, 6 unknown |
| `serious` | 1 = serious |
| `seriousnessdeath`, `seriousnesshospitalization`, `seriousnesslifethreatening`, `seriousnessdisabling`, `seriousnesscongenitalanomali`, `seriousnessother` | Seriousness criteria |
| `patient.patientonsetage`, `patient.patientsex` | Demographics (often missing) |
| `receivedate`, `receiptdate` | Report dates |
| `primarysource.qualification` | 1 physician, 2 pharmacist, 3 other HCP, 4 lawyer, 5 consumer |
| `occurcountry` | |

**Restrict to suspect drugs.** Without
`patient.drug.drugcharacterization:1`, you are counting reports where the drug
was merely concomitant — a systematic overcount.

```
# Serious reactions where the drug was the suspect
?search=patient.drug.openfda.generic_name:"X"
       +AND+patient.drug.drugcharacterization:1
       +AND+serious:1
       &count=patient.reaction.reactionmeddrapt.exact&limit=25
```

### `/drug/drugsfda.json`

`application_number`, `sponsor_name`, `products.brand_name`,
`products.marketing_status`, `submissions.submission_type` (ORIG / SUPPL),
`submissions.submission_status_date`.

Useful for reconstructing an approval timeline — original approval, then each
supplemental indication with its date. That timeline is often exactly what a
landscape assessment needs and is tedious to assemble by hand.

---

## Interpretation rules that are not optional

**FAERS counts are counts of reports.** No denominator exists. They cannot
produce incidence, cannot establish causality, and **cannot be compared between
products** — reporting volume tracks launch recency, notoriety, litigation, and
surveillance intensity rather than safety. `scripts/openfda.py` prints this
caveat with every FAERS result deliberately; do not strip it when copying output
into a deliverable.

**Disproportionality measures** (PRR, ROR, EBGM) are not provided by openFDA and
should not be hand-calculated from these counts for external use. They are
signal-detection tools for pharmacovigilance professionals working with the full
dataset and appropriate statistical controls.

**The label is US-only.** For the EU, use the EMA EPAR and SmPC (no equivalent
open API — retrieve from the EMA website). Indication wording, population
restrictions, and safety sections diverge between jurisdictions more often than
people expect.

**openFDA is not the legal record.** It is a convenience layer over DailyMed and
FAERS. For anything consequential, verify against the source document.

---

## Data quality notes

- Duplicate FAERS reports are common — the same case reported by manufacturer
  and consumer appears twice.
- Drug name normalisation via `openfda.*` fails when a report used a name the
  normaliser did not recognise; those reports lack `openfda` fields entirely and
  are invisible to a generic-name search.
- Age and sex are frequently missing.
- Label records may exist for multiple manufacturers of the same generic, with
  differing section content.
