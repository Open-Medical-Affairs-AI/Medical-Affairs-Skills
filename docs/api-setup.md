# Free public APIs, ready for the agent

The repository includes executable Python clients. No company connector is required.
The core routes work without API keys within public-service limits. Internet and
permission to make HTTPS requests are needed for live retrieval. The agent account
or hosted compute may still have costs.

| Service | Available work | Access |
|---|---|---|
| PubMed / NCBI E-utilities | Search, abstracts, MeSH, PMID checks | No key at basic limits; optional NCBI key |
| ClinicalTrials.gov v2 | Trial search, study records, status and design | Public API, no key |
| openFDA | US label retrieval and FAERS reaction counts | No key at basic limits; optional key for greater daily allowance |
| Europe PMC | Literature, open-access discovery, metadata and abstracts | Public REST search, no key |
| Crossref | Bibliographic search and DOI metadata | No registration for public REST access |
| OpenAlex | Existing optional DOI verification fallback | Availability/access requirements checked at use; optional OPENALEX_API_KEY |

OpenAlex is supplementary; the workshop and core searches do not depend on it.
Public services are subject to rate limits, changing terms and outages. A successful
connection check is not a promise of unlimited future access.

## One gateway

Run from the repository root. Python standard library is sufficient:

```bash
python3 scripts/public_evidence.py pubmed --query 'multiple myeloma' --limit 5
python3 scripts/public_evidence.py trials --query 'atopic dermatitis' --limit 5
python3 scripts/public_evidence.py labels --query metformin
python3 scripts/public_evidence.py faers --query metformin --limit 5
python3 scripts/public_evidence.py europepmc --query 'obesity AND OPEN_ACCESS:Y' --limit 5
python3 scripts/public_evidence.py crossref --query 'multiple myeloma randomized trial' --limit 5
```

Add `--out outputs/search-001.json` to save provenance. Existing files are not
silently replaced. Each response states source, query, time, access status and
whether claim support was checked. Retrieval alone never verifies a scientific claim.
A failed service returns unavailable, not zero results. Continue the synthetic mission.

The gateway runs bounded discovery queries. For precise query filters, pagination,
complete abstracts, label sections and citations, use the specialist client:

```bash
python3 skills/pubmed-search/scripts/pubmed.py search --query 'myeloma[tiab]' --from 2025 --limit 20 --format table
python3 skills/clinical-trials-search/scripts/ctgov.py search --condition 'multiple myeloma' --status RECRUITING --limit 10 --format table
python3 skills/regulatory-label-intelligence/scripts/openfda.py label --generic metformin --sections indications_and_usage,boxed_warning
python3 skills/citation-integrity/scripts/verify_citations.py --file outputs/references.md
```

An empty search is limited to its query, filters and source. PubMed misses some
literature, a registry search is not global trial coverage, and openFDA is US-specific.
The label client retrieves a matching submitted label; confirm product identity,
manufacturer, formulation and current authoritative status before real use.
FAERS counts are reports, not incidence, causal attribution or a product ranking.

## Workshop checks

```bash
python3 scripts/workshop.py check
python3 scripts/workshop.py check --live
python3 scripts/selftest_apis.py
python3 scripts/selftest_workshop.py
```

The first checks bundled mission inputs. The live check makes small real requests
through the gateway and reports each service separately. CI fixture tests verify
behavior without depending on internet. Do a live rehearsal near the workshop.

## Optional keys

NCBI permits basic use without a key and higher request rates with a free key.
openFDA also offers an optional key. Store keys in the host secret manager or local
environment variables `NCBI_API_KEY`, `OPENFDA_API_KEY`, and optionally
`OPENALEX_API_KEY`. `API_CONTACT_EMAIL` supplies contact metadata where supported.
Never paste keys in prompts or commit them. Public search queries must not contain
private case details, internal documents or credentials.

## Network destinations

Allow HTTPS to `eutils.ncbi.nlm.nih.gov`, `clinicaltrials.gov`, `api.fda.gov`,
`www.ebi.ac.uk`, and `api.crossref.org`. `api.openalex.org` is optional.
GitHub access is needed to retrieve this repository. Audio model downloads have
separate destinations and are not required for transcript-based workshop missions.
A host root URL returning HTTP 200 does not prove an API request succeeds; use the
actual live preflight above.

## Source rights and provenance

Real public snapshots live in `workshop/public-evidence/`; synthetic sources live
in `workshop/data/`. Never merge their truth status. Bibliographic metadata does not
license publisher full text. Retrieve permitted full text through supported APIs
and inspect each article license before redistribution. No paywall bypass is included.

Official documentation:

- [NCBI E-utilities and usage limits](https://www.ncbi.nlm.nih.gov/books/NBK25497/)
- [ClinicalTrials.gov API](https://clinicaltrials.gov/data-api/api)
- [openFDA authentication](https://open.fda.gov/apis/authentication/)
- [Europe PMC REST service](https://europepmc.org/RestfulWebService)
- [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)
- [OpenAlex help](https://help.openalex.org/)
- [PMC open-access reuse guidance](https://pmc.ncbi.nlm.nih.gov/tools/openftlist/)
