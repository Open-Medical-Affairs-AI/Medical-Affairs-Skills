# PubMed Query Cookbook

Copy-ready patterns for the searches Medical Affairs actually runs. Replace the
bracketed placeholders. Always run `pubmed.py mesh --term "<concept>"` first to
confirm how PubMed indexes the concept — entry terms frequently surprise.

---

## Product surveillance — everything on our compound

Catch every naming convention. Development codes matter: they are how the early
trials were published.

```
("[GENERIC]"[tiab] OR "[BRAND]"[tiab] OR "[DEV-CODE]"[tiab] OR "[ALT-DEV-CODE]"[tiab])
```

Add nothing else on the first pass. Filter afterwards — you want to see the case
reports, letters, and correspondence, because that is where early safety
observations surface.

**Recent additions only** (for periodic monitoring):

```
(...as above...) AND "last 90 days"[dp]
```

---

## Disease landscape — high recall

```
("[DISEASE]"[MeSH] OR "[DISEASE]"[tiab] OR "[SYNONYM 1]"[tiab] OR "[SYNONYM 2]"[tiab])
AND ("[INTERVENTION CLASS]"[tiab] OR "[MECHANISM]"[tiab])
AND ("2021"[dp] : "3000"[dp])
```

**Restrict to the strongest designs:**

```
AND ("randomized controlled trial"[pt] OR "meta-analysis"[pt] OR "systematic review"[pt])
```

**Guidelines only:**

```
"[DISEASE]"[MeSH] AND ("practice guideline"[pt] OR "guideline"[pt] OR "consensus development conference"[pt])
```

---

## KOL publication profile

```
"[LASTNAME] [INITIALS]"[au] AND "[DISEASE]"[MeSH] AND ("2021"[dp] : "3000"[dp])
```

**Disambiguate a common name** with an affiliation:

```
"Smith J"[au] AND ("[INSTITUTION]"[ad] OR "[CITY]"[ad])
```

Then look at trajectory, not just volume — `--sort date` and read the titles in
order. A researcher who moved from single-agent trials to combination or
sequencing work has changed the question they care about, and that is what
makes a briefing useful.

**What are they cited for?**

```bash
python3 pubmed.py links --pmid [THEIR_KEY_PAPER] --kind citedby --limit 50
```

**Senior-author position** signals where they lead rather than collaborate.
PubMed cannot filter on this; retrieve and inspect the author lists.

---

## Competitive intelligence

Each competitor, all names, restricted to clinical work:

```
("[COMPETITOR GENERIC]"[tiab] OR "[COMPETITOR BRAND]"[tiab] OR "[COMPETITOR CODE]"[tiab])
AND "[DISEASE]"[MeSH]
AND ("clinical trial"[pt] OR "randomized controlled trial"[pt])
```

**Find entrants you did not know about** — search the mechanism rather than the
product:

```
("[TARGET]"[tiab] OR "[MECHANISM]"[tiab]) AND "[DISEASE]"[MeSH]
AND ("2024"[dp] : "3000"[dp])
```

---

## Safety questions

Deliberately inclusive of case reports — they are the point.

```
("[DRUG]"[tiab] OR "[DRUG CLASS]"[tiab])
AND ("[ADVERSE EVENT]"[MeSH] OR "[ADVERSE EVENT]"[tiab] OR "[SYNONYM]"[tiab])
```

**Class-level safety:**

```
"[DRUG CLASS]"[Pharmacological Action] AND "[ADVERSE EVENT]"[MeSH]
```

**Pharmacovigilance literature:**

```
"[DRUG]"[tiab] AND ("adverse effects"[sh] OR "pharmacovigilance"[tiab] OR "safety"[ti])
```

Note `[sh]` — MeSH subheadings such as `adverse effects`, `therapeutic use`,
`drug therapy`, `mortality`, `diagnosis` attach to a heading:

```
"Multiple Myeloma/drug therapy"[MeSH]
```

---

## Finding the paper behind a congress abstract

Congress abstracts are mostly not in PubMed. To check whether a full publication
exists yet:

```
("[TRIAL ACRONYM]"[tw] OR "[NCT NUMBER]"[tw] OR "[NCT NUMBER]"[si])
```

`[si]` searches secondary source identifiers, which is where registry numbers
are indexed. If nothing returns, the full publication does not exist — label the
evidence `[abstract]` and say so.

---

## Real-world evidence

```
"[DRUG]"[tiab]
AND ("real world"[tiab] OR "routine practice"[tiab] OR "registry"[tiab]
     OR "observational"[tiab] OR "retrospective"[tiab] OR "claims"[tiab]
     OR "electronic health record*"[tiab])
NOT ("randomized controlled trial"[pt])
```

---

## Health economics

```
"[DISEASE]"[MeSH]
AND ("cost"[tiab] OR "cost-effectiveness"[tiab] OR "economic"[tiab]
     OR "budget impact"[tiab] OR "quality-adjusted"[tiab] OR "QALY"[tiab])
```

---

## Patient-reported outcomes

```
"[DISEASE]"[MeSH]
AND ("quality of life"[MeSH] OR "patient reported outcome*"[tiab]
     OR "PROM"[tiab] OR "EORTC"[tiab] OR "EQ-5D"[tiab] OR "PRO-CTCAE"[tiab])
```

---

## Testing whether an evidence gap is real

Before reporting a gap, run a deliberately over-broad search. A gap claimed on a
narrow search is not a finding, it is a search failure.

```
("[DISEASE]"[MeSH] OR "[DISEASE]"[tw])
AND ("[QUESTION CONCEPT]"[tw] OR "[SYNONYM 1]"[tw] OR "[SYNONYM 2]"[tw])
```

No publication-type filter, no date limit, `[tw]` throughout. If that returns
nothing relevant, you have a genuine, documentable gap. Record the exact query —
it is the evidence for the claim.

---

## Syntax notes worth remembering

| Pattern | Effect |
|---|---|
| `"exact phrase"` | Phrase search; without quotes, terms are ANDed and may be auto-mapped |
| `term*` | Truncation. Disables automatic term mapping, so add MeSH explicitly |
| `[MeSH:noexp]` | Do not explode to narrower terms |
| `[majr]` | Major topic only — far more precise, lower recall |
| `2020:2026[dp]` | Publication date range |
| `"last 5 years"[dp]` | Relative date range |
| `hasabstract` | Records with an abstract |
| `english[la]` | Language filter — use with care, it excludes real evidence |
| `humans[mh]` | Excludes preclinical |

**Automatic Term Mapping** silently rewrites unquoted queries, expanding them
via MeSH and synonyms. It is usually helpful and occasionally does something you
did not intend. When a result set looks wrong, check what PubMed actually ran —
the web interface shows the translation under "Search Details".
