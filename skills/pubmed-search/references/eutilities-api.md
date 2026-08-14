# NCBI E-utilities — API Reference

Read this when `scripts/pubmed.py` does not cover what you need and you have to
call the API directly.

Base: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`
Official docs: https://www.ncbi.nlm.nih.gov/books/NBK25501/

---

## Usage policy — read before you script anything

- **3 requests/second** without an API key; **10/second** with one.
- API keys are free: https://account.ncbi.nlm.nih.gov/settings/. Pass as
  `&api_key=...`.
- Identify your tool with `&tool=` and `&email=`. NCBI contacts you before
  blocking; without contact details they just block.
- Large jobs should run outside 09:00–17:00 US Eastern on weekdays.
- Exceeding limits returns **HTTP 429**. Back off exponentially — hammering
  gets the IP blocked, and on shared infrastructure that affects other people.

---

## The endpoints

### `esearch.fcgi` — find records

| Parameter | Notes |
|---|---|
| `db` | `pubmed`, `pmc`, `mesh`, `books`, … |
| `term` | The query. URL-encode it. |
| `retmax` | Max IDs returned. Cap is 10,000 per request. |
| `retstart` | Offset for pagination. |
| `retmode` | `json` or `xml` |
| `sort` | `relevance` (default), `pub_date`, `Author`, `JournalName` |
| `datetype` | `pdat` (publication), `edat` (Entrez), `mdat` (modification) |
| `mindate` / `maxdate` | `YYYY`, `YYYY/MM`, or `YYYY/MM/DD`. Require `datetype`. |
| `usehistory` | `y` returns `WebEnv` + `QueryKey` instead of shipping IDs around |

```json
{"esearchresult": {"count": "84", "retmax": "20", "retstart": "0",
                   "idlist": ["36001231", "..."],
                   "translationstack": [...]}}
```

`translationstack` shows what Automatic Term Mapping actually ran. Worth
inspecting when a result set surprises you.

Errors appear as `{"esearchresult": {"ERROR": "..."}}` with HTTP 200 — check for
the key rather than trusting the status code.

### `esummary.fcgi` — document summaries

Metadata without the abstract: title, authors, journal, dates, pagination,
`articleids` (PMID / DOI / PMC), and `pubtype`.

`pubtype` is how you detect retractions (`Retracted Publication`,
`Expression of Concern`) and infer evidence tier.

### `efetch.fcgi` — full records

`retmode=xml` for PubMed (JSON is not supported for full records). Key paths:

```
//PubmedArticle/MedlineCitation/PMID
//Article/ArticleTitle
//Abstract/AbstractText          @Label / @NlmCategory for structured sections
//AuthorList/Author/{LastName,ForeName,Initials}
//MeshHeadingList/MeshHeading/DescriptorName        @MajorTopicYN
//PublicationTypeList/PublicationType
//DataBankList/DataBank[DataBankName='ClinicalTrials.gov']//AccessionNumber
//CommentsCorrectionsList/CommentsCorrections       @RefType='RetractionIn'
```

`AbstractText` may contain inline markup (`<i>`, `<sup>`); use `itertext()`
rather than `.text` or you will silently truncate.

For PMC full text: `db=pmc`, `id=<PMCID without the "PMC" prefix>`. Only
open-access subset content is retrievable.

### `elink.fcgi` — relationships

| `linkname` | Returns |
|---|---|
| `pubmed_pubmed` | Related articles (NCBI's similarity model) |
| `pubmed_pubmed_citedin` | Articles citing this one *within PubMed Central* |
| `pubmed_pubmed_refs` | This article's references |
| `pubmed_pmc` | Linked PMC full text |

**Citation counts here are incomplete** — they cover PMC only, not all of the
literature. Do not present them as citation metrics. Use OpenAlex or Scopus if
bibliometrics actually matter.

### `einfo.fcgi` — database metadata

Lists valid field tags and record counts for a database. Useful when you are
unsure whether a tag exists.

---

## The history server

For result sets over a few hundred, or multi-step workflows, keep the IDs on
NCBI's side.

```
esearch.fcgi?db=pubmed&term=...&usehistory=y
  → {"esearchresult": {"count": "5231", "webenv": "MCID_...", "querykey": "1"}}

esummary.fcgi?db=pubmed&WebEnv=MCID_...&query_key=1&retstart=0&retmax=500
```

Also lets you combine queries server-side: `&term=%231+AND+%232` where `#1` and
`#2` are prior query keys in the same WebEnv.

`WebEnv` expires after roughly an hour of inactivity.

---

## Error handling that matters in practice

| Symptom | Cause | Response |
|---|---|---|
| HTTP 429 | Rate limit | Exponential backoff. Get an API key. |
| HTTP 414 | URL too long | POST instead of GET, or use the history server |
| `{"ERROR": "..."}` with HTTP 200 | Malformed query | Read the message; usually an unbalanced quote or bracket |
| Empty `idlist`, `count > 0` | `retstart` past the end | Check pagination |
| `esummary` omits a UID | Record does not exist | **Treat as a fabricated identifier** |
| Truncated XML | Too many IDs in one efetch | Chunk to ≤200 |
| HTTP 400 on efetch | Invalid `retmode`/`rettype` pair | PubMed full records are XML only |

---

## Things that will catch you out

- **`count` is the total matching, not the number returned.** Reporting `count`
  as "results found" while having read 20 of them is a real and common error in
  evidence reviews.
- **Relevance sort is opaque and non-reproducible over time.** For anything that
  must be reproducible, sort by date.
- **PMIDs are strings.** Leading zeros do not occur, but treating them as
  integers breaks joins with data from other systems.
- **A PMID can be retired or merged** when duplicate records are discovered.
  Rare, but it happens.
- **`[au]` matching is imperfect.** Name changes, transliteration variants, and
  common surnames all cause misses and false hits. Verify against affiliation.
- **MeSH indexing lags weeks to months.** A MeSH-only search cannot find last
  month's papers. Always pair with `[tiab]`.
- **Ahead-of-print records** may lack volume, issue, and pages, and get updated
  later. Cite the DOI.

---

## Related NCBI resources

| Database | `db=` | Use |
|---|---|---|
| PubMed Central | `pmc` | Open-access full text |
| MeSH | `mesh` | Vocabulary lookup — see `medical-terminology-mapping` |
| ClinVar | `clinvar` | Variant interpretation |
| Gene | `gene` | Target background |
| Books | `books` | StatPearls, GeneReviews, NCBI Bookshelf |
