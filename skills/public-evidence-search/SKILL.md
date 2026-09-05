---
name: public-evidence-search
description: >-
  Search free public scientific sources through the bundled gateway when a task needs literature, trial records, labels, adverse-event reports or citation metadata. Use for supplementary open-access discovery with Europe PMC and Crossref, or to choose an available public source without enterprise connectors.
license: Apache-2.0
metadata:
  version: "0.2.0"
  tier: data
  maturity: beta
  requires:
    - medical-affairs-foundations
  produces: Retrieved public evidence with query and access status
---

# Public Evidence Search

Use the existing specialist skills for detailed PubMed queries, trial filters,
label interpretation and citation checks. This gateway adds Europe PMC and Crossref
search and provides a common availability/provenance wrapper for all six sources.

From the repository root:

```bash
python3 scripts/public_evidence.py pubmed --query 'multiple myeloma' --limit 5
python3 scripts/public_evidence.py europepmc --query 'atopic dermatitis AND OPEN_ACCESS:Y' --limit 5
python3 scripts/public_evidence.py crossref --query 'obesity randomized trial' --limit 5
python3 scripts/public_evidence.py trials --query 'multiple myeloma' --limit 5
python3 scripts/public_evidence.py labels --query metformin
python3 scripts/public_evidence.py faers --query metformin --limit 5
```

Use `--out outputs/search-001.json` for a new evidence snapshot. Results contain
source, exact query, retrieval time and status. `unavailable` is not zero results.
These are bounded discovery searches, not systematic reviews or complete databases.
Use specialist clients for pagination and protocol-defined retrieval.

- Search real disease, class and endpoint terms, never fictional product names.
- Screen records before fetching full text. A DOI resolving does not establish
  that its paper supports a claim. Check population, design, endpoint and numbers.
- Europe PMC `isOpenAccess` and full-text links support discovery; inspect the
  article license before redistributing text. PubMed inclusion is not a reuse license.
- Crossref metadata may describe corrections or retraction notices; interpret their
  relationships rather than assuming any record with update metadata is retracted.
- openFDA is US-specific. Spontaneous reports have no exposed-population denominator.
- If blocked, use available native tools or named bundled sources with explicit
  limitations. Never switch real evidence to fictional data silently.

See [API setup](../../docs/api-setup.md) for official docs and access requirements.
Read `house-rules/public-evidence-search.md` for authorized source preferences.
