# API Setup

Four public data sources, no API key required for any of them. This page covers
rate limits, the optional free NCBI key, and what to do on a restricted
corporate network.

---

## Hosts to allowlist

If your agent runs behind a proxy or on a locked-down network, these must be
reachable over HTTPS:

| Host | Used by | Required for |
| --- | --- | --- |
| `eutils.ncbi.nlm.nih.gov` | `pubmed-search`, `medical-terminology-mapping`, `citation-integrity` | Literature search, MeSH lookup, PMID verification |
| `clinicaltrials.gov` | `clinical-trials-search`, `citation-integrity` | Trial landscape, NCT verification |
| `api.fda.gov` | `regulatory-label-intelligence` | Approved labels, FAERS |
| `api.crossref.org` | `citation-integrity` | DOI verification |
| `api.openalex.org` | `citation-integrity` | DOI fallback, retraction flags |

**Check this before a workshop, not during one.** Corporate networks block these
more often than people expect, and finding out at 09:05 costs you the first
session.

Quick test:

```bash
for h in eutils.ncbi.nlm.nih.gov clinicaltrials.gov api.fda.gov \
         api.crossref.org api.openalex.org; do
  printf "%-32s " "$h"
  curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 "https://$h" || echo "BLOCKED"
done
```

### If they are blocked

Everything except literature retrieval still works. The workshop data packs are
self-contained, so all six missions run without network access — the agent
simply cannot verify citations or search for new evidence.

Say so up front rather than letting teams hit connection errors and assume the
tooling is broken.

---

## NCBI API key (optional, free, recommended)

Raises the E-utilities rate limit from **3 to 10 requests per second**.

1. Sign in at https://account.ncbi.nlm.nih.gov/
2. Settings → API Key Management → create a key
3. Export it:

```bash
export NCBI_API_KEY="your-key-here"
```

The clients throttle themselves either way, so without a key large searches are
simply slower. Nothing fails.

NCBI also asks that tools identify themselves. The clients send a `tool`
parameter automatically; you can add a contact address:

```bash
export API_CONTACT_EMAIL="you@example.org"
```

This matters in practice — NCBI contacts you before blocking, and without
contact details they just block.

---

## openFDA API key (optional, free)

Without a key: 240 requests/minute, 1,000/day per IP.
With a key: 240 requests/minute, 240,000/day.

Register at https://open.fda.gov/apis/authentication/ then:

```bash
export OPENFDA_API_KEY="your-key-here"
```

---

## ClinicalTrials.gov

No key, no registration, no published rate limit. Be reasonable — throttle bulk
jobs.

---

## Verifying it all works

```bash
# Offline: parsing, pagination, error paths, and the interpretation guardrails
python3 scripts/selftest_apis.py

# Live: confirms the upstream APIs still return the shapes we parse
python3 scripts/selftest_apis.py --live
```

**Run the live test after any long gap.** It is the only thing that catches an
upstream schema change. If it fails, re-record the fixtures and read the diff:

```bash
python3 scripts/record_fixtures.py --live
git diff shared/fixtures/
```

The diff tells you exactly what moved.

---

## Rate limiting and courtesy

All four clients implement exponential backoff on 429 and 5xx, and self-throttle
below the documented limits. Please do not remove that.

These are free public services funded by taxpayers and used by researchers
worldwide. Hammering them gets IP ranges blocked, and on shared corporate
infrastructure that affects colleagues who had nothing to do with it.

---

## Terms of use

| Source | Terms |
| --- | --- |
| NCBI E-utilities | https://www.ncbi.nlm.nih.gov/home/about/policies/ |
| ClinicalTrials.gov | https://clinicaltrials.gov/about-site/terms-conditions |
| openFDA | https://open.fda.gov/terms/ — public domain, explicitly **not** for clinical decision-making |
| CrossRef | https://www.crossref.org/documentation/retrieve-metadata/rest-api/ |
| OpenAlex | CC0 |

No data from these sources is redistributed in this repository.
