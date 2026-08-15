# Verification Sources — Coverage, Gaps, and Who to Trust for What

`scripts/verify_citations.py` queries several sources because none of them is
complete. Knowing what each covers tells you what a failure to resolve actually
means.

---

## PubMed / NCBI E-utilities

**Covers:** ~37 million citations from MEDLINE, PubMed Central, and publisher-
deposited records. Biomedical and life sciences.

**Authoritative for:** PMIDs, MeSH indexing, publication types (including
retraction status), and the linkage between PMID / DOI / PMC ID.

**Does not cover:**
- Most congress abstracts. ASCO, ASH, ESMO, EHA, AAD abstracts are generally
  **not** in PubMed. A failure to resolve an abstract citation is expected, not
  evidence of fabrication — but it does mean the citation cannot be verified
  this way, and the `[abstract]` tier label becomes essential.
- Preprints, except those deposited by participating servers (a growing subset
  via the NIH Preprint Pilot).
- Non-biomedical literature.
- Very recent publications — indexing lags by days to weeks.

**Retraction detection:** publication type `Retracted Publication` marks the
retracted article; `Retraction of Publication` marks the notice. Also carries
`Expression of Concern`. Reliable once indexed, with a lag after the publisher
acts.

**Rate limits:** 3 requests/second unlicensed, 10/second with a free
`NCBI_API_KEY`. Register at https://account.ncbi.nlm.nih.gov/settings/. The
scripts here throttle themselves either way.

---

## CrossRef

**Covers:** ~150 million DOI-registered works across all disciplines — journal
articles, books, conference proceedings, preprints, datasets, and components.

**Authoritative for:** DOI resolution and publisher-deposited metadata.

**Strengths over PubMed:** all disciplines; faster for very recent content
(a DOI is registered at publication); carries `update-to` relationships that
surface retractions and corrections.

**Weaknesses:** metadata quality varies enormously by publisher. Author lists
may be incomplete, and abstracts are often absent. Some older content has no
DOI at all.

---

## OpenAlex

**Covers:** ~250 million works. CC0 licensed, successor to Microsoft Academic
Graph.

**Use it as:** a second opinion when CrossRef misses a DOI, and for the
`is_retracted` flag, which aggregates several sources.

**Also useful for:** citation counts, open-access status, and institutional
affiliations — relevant to `kol-engagement-brief` when profiling a researcher's
output.

**Weakness:** aggregation means occasional duplicate or merged records.

---

## ClinicalTrials.gov API v2

**Authoritative for:** NCT numbers, registered protocol details, sponsor,
status, and — importantly — the **history of changes**, which reveals whether a
primary endpoint was altered after enrolment began.

**Weakness:** sponsor-submitted and updated at the sponsor's discretion. Status
fields are frequently stale. Results posting is required for applicable trials
but compliance is imperfect.

---

## Retraction Watch Database

**Covers:** retractions, corrections, and expressions of concern across all
fields, with reasons coded.

**Why it matters:** it is generally faster and more complete than PubMed's
publication-type indexing, particularly in the weeks immediately after a
retraction. It is now integrated into CrossRef's infrastructure.

The bundled verifier does not query it directly. For a high-stakes deliverable
— a manuscript, a payer dossier, a guideline submission — check the key
references there manually.

---

## What a failure to resolve actually means

| Situation | Interpretation |
|---|---|
| PMID does not resolve in PubMed | Almost certainly fabricated or mistyped. PMIDs are sequential and dense; there are very few valid gaps. **Remove it.** |
| DOI resolves nowhere | Very likely fabricated. DOI registration is a precondition of publication for essentially all journals. **Remove it.** |
| Congress abstract not in PubMed | Expected. Verify against the congress's own abstract portal, and label `[abstract]`. |
| Preprint not in PubMed but resolves in CrossRef | Normal. Label `[preprint]`. |
| Very recent paper not in PubMed but has a working DOI | Indexing lag. Fine to cite; note the DOI. |
| NCT number does not resolve | Fabricated or mistyped. Registry numbers are never retired. **Remove it.** |

**The asymmetry worth internalising:** a resolution failure is much more likely
to indicate fabrication than to indicate a gap in coverage. Treat it that way.
The cost of removing a real-but-unverifiable citation is small; the cost of
publishing a fabricated one is the credibility of the whole function.

---

## Sources this project deliberately does not use

**Google Scholar.** No official API, terms prohibit automated access, and
results are not reproducible between sessions. Fine for a human to check
something; unsuitable as a verification step in an auditable workflow.

**Publisher websites, scraped.** Fragile, frequently blocked, and legally
ambiguous. Where a DOI resolves, use the metadata.

**The model's own memory.** The reason this skill exists.
