---
name: citation-integrity
description: >-
  Check that every factual claim traces to a real, retrievable source that
  actually says what it is cited for. Use whenever producing a Medical
  Affairs deliverable that cites literature. Covers the no-fabricated-
  reference protocol, verifying PMIDs and DOIs against PubMed, CrossRef and
  OpenAlex before use, quote fidelity, evidence-tier labelling, AMA
  formatting, and how to state a claim you cannot source. Load before
  drafting, not after — and always when citations came from memory rather
  than a search.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.1.0"
  tier: foundation
  maturity: stable
  requires:
    - medical-affairs-foundations
  produces: Verified reference list with evidence tiers
  network: [eutils.ncbi.nlm.nih.gov, api.crossref.org, api.openalex.org]
---

# Citation Integrity

Every claim must be supported by the source it cites, not merely a real identifier.

- **Real public sources:** retrieve and resolve identifiers, then read the source
  to check the claim. An access failure is unverified, not proof of fabrication.
- **Supplied documents:** cite the filename/version and page, table or record ID.
  Do not invent a DOI for internal evidence or claim to have checked unseen text.
- **Synthetic workshop sources:** cite `SYN:<TA>:<file>` plus section/record ID,
  labelled fictional. Do not resolve invented products or studies online.
- **Offline real sources:** retain accessible source text and provenance. Distinguish
  local inspection from a fresh external check; put unresolved items in a remediation
  log and qualify or omit claims that lack accessible support.

## The two failure modes

**Fabrication.** The reference does not exist. Caught by resolution.

**Misattribution.** The reference exists, and does not support the claim. This
is more common, harder to catch, and just as damaging. A real paper cited for a
number it does not contain, a subgroup result presented as the primary finding,
or a trial cited for a population it did not enrol.

Resolution catches the first. Only reading the source catches the second.

## The protocol

### 1. Never write a citation from memory

Use a retrieved source or an accessible supplied/cached document with provenance.
Memory alone is not a source. State the access date and any limits on freshness.

When you need a source for a claim, search for it (`pubmed-search`). Do not
recall it.

### 2. Resolve every identifier before use

Run the bundled verifier over your reference list:

```bash
python3 scripts/verify_citations.py --pmids 36001231,35660948
python3 scripts/verify_citations.py --dois 10.1056/NEJMoa2203478
python3 scripts/verify_citations.py --file references.txt --format ama
```

It queries PubMed (E-utilities), CrossRef, and OpenAlex, and reports for each
identifier whether it resolved, the retrieved title and author list, and any
mismatch against what you claimed. A failed request cannot establish whether the identifier exists. Keep unverified
items in a remediation log; do not present them as verified support.

Read `scripts/verify_citations.py --help` for the retraction check and the
offline fixture mode.

### 3. Check the source says what you are citing it for

For every claim carrying a citation, confirm from the abstract or full text:

- The **population** matches the claim's population
- The **number** matches, including its confidence interval
- The **endpoint** is the one named, and its type (primary, secondary, post hoc,
  exploratory) is stated
- The **direction** of the effect is right
- The claim is not stronger than the design supports (`evidence-appraisal`)

If you only have the abstract, say so, and label the evidence tier accordingly.

### 4. Check for retraction and correction

A retracted paper cited as evidence is a serious error. PubMed carries
retraction and expression-of-concern notices in its publication types and
comment/correction links; the verifier flags them. Retraction Watch's database
is more complete for recent actions.

This matters disproportionately in fast-moving fields, and retractions of
high-profile clinical papers are not rare.

### 5. Label the evidence tier

Every citation carries its tier, because the tier determines how much weight the
claim can bear. Readers cannot infer it from the format.

| Tier | Marker | What it means for the claim |
|---|---|---|
| **Peer-reviewed publication** | (none needed) | Full methods available; appraise normally |
| **Congress abstract** | `[abstract]` | Abstract-level review varies; limited methods; findings may change before full publication |
| **Congress presentation / poster** | `[presented]` | As above, and often not retrievable later |
| **Preprint** | `[preprint]` | Not peer-reviewed; may change substantially |
| **Data on file** | `[data on file]` | Unpublished company data; external readers cannot verify it. Say who holds it. |
| **Approved label** | `[USPI]` / `[SmPC]` | Regulator-reviewed; jurisdiction-specific; state which |
| **Regulatory document** | `[FDA review]` etc. | Public but not peer-reviewed |
| **Clinical trial registry** | `[NCT########]` | Sponsor-submitted, may be stale |
| **Guideline** | `[guideline]` | Name the body, version, and year |

An unlabelled abstract cited alongside peer-reviewed papers implies a parity that
does not exist. This is one of the quieter ways deliverables mislead.

### 6. When you cannot source a claim

Do not delete the claim silently, and do not soften it into vagueness so it no
longer needs a citation. Both hide information the reviewer needs.

Flag it:

> **[UNSOURCED]** Claim: "Approximately 40% of patients discontinue within 6
> months." No supporting reference located in PubMed (searches run: see
> provenance appendix). This may be internal data, may derive from a congress
> presentation not indexed, or may be incorrect. Requires source or removal
> before use.

That is useful to a reviewer. A quietly removed claim is not.

## Quote fidelity

When quoting a source directly:

- Reproduce exactly, including punctuation. Use ellipses for omissions and
  square brackets for insertions.
- Never alter a quotation to fit your sentence.
- Preserve hedging. Authors write "may be associated with" for a reason;
  tightening it to "is associated with" changes the claim.
- Quote enough context that the meaning is not inverted by the surrounding text.
- For a numeric result, carry the confidence interval with the point estimate.

**The most common quote failure in Medical Affairs** is dropping the authors'
own limitation statement. If a paper's discussion says the finding requires
confirmation in a randomised trial, citing the finding without that caveat
misrepresents the source.

## Reference format

AMA is the default for medical publications: numbered in order of first
appearance, superscript in text, journal abbreviations per the NLM catalogue,
DOIs included wherever available because they are the most durable identifier
and the easiest for a reviewer to check.

Worked examples for journal articles, congress abstracts, package inserts and
registry records are in `references/ama-format.md`. Where your organisation or
target journal specifies a different style, that wins; record it in
`house-rules/citation-integrity.md`.

## The provenance appendix

Every deliverable ends with one. It is what makes the work auditable, and it is
what a reviewer reads first when something looks surprising.

```markdown
## Provenance

**Searches run**
- PubMed, 2026-08-14: ("teclistamab"[tiab]) AND ("myeloma"[MeSH]) — 84 results,
  23 screened, 11 included
- ClinicalTrials.gov, 2026-08-14: teclistamab, phase 2-3, recruiting — 14 records

**References verified:** 11 of 11 resolved (PubMed + CrossRef). 0 retracted.

**Evidence tiers:** 7 peer-reviewed · 3 congress abstracts · 1 USPI

**Could not determine**
- Discontinuation rate beyond 12 months — no published data located
- Head-to-head comparison vs [comparator] — no such trial exists
```

The "could not determine" section is the most valuable part and the one most
often omitted. A gap named is a gap someone can close; a gap smoothed over
becomes an assumption nobody knows they are making.

## Before you finish

Read `house-rules/citation-integrity.md`. Organisations differ on acceptable
evidence tiers, on whether abstracts may be cited externally, and on reference
style.

Then run the verifier one final time over the finished reference list. Citations
get edited during drafting, and a number that was correct when you wrote it can
be attached to the wrong reference by the time you finish.

## References

- `references/ama-format.md` — AMA worked examples for every source type
  Medical Affairs cites.
- `references/verification-sources.md` — what PubMed, CrossRef, OpenAlex, and
  Retraction Watch each cover, where they disagree, and which to trust for what.
