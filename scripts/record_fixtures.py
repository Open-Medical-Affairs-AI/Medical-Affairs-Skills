#!/usr/bin/env python3
"""Build (or re-record) the offline HTTP fixtures used by the API self-tests.

Two modes:

  --synthetic   (default) Write fixtures whose bodies match the documented
                response shapes of each API. This is what CI runs against, and
                it is what makes parsing, pagination and error handling testable
                on a machine with no egress.

  --live        Replay the same requests against the real APIs and record what
                actually comes back. Run this from a network that can reach
                NCBI, ClinicalTrials.gov and openFDA. It is the only way to
                catch an upstream schema change.

    python3 scripts/record_fixtures.py
    python3 scripts/record_fixtures.py --live

Fixtures are a single JSON file — shared/fixtures/http_cache.json — mapping a
request URL to {"status": int, "body": str}. One file keeps them reviewable in
a diff, which matters when a fixture change is really an upstream API change.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FIXTURES = REPO / "shared" / "fixtures" / "http_cache.json"

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
CTG = "https://clinicaltrials.gov/api/v2"
OPENFDA = "https://api.fda.gov"

# Every URL the self-test exercises. Keeping this list explicit (rather than
# capturing whatever a test run happens to emit) means adding a test forces you
# to think about which upstream contract it depends on.
REQUESTS: list[str] = [
    # --- PubMed -----------------------------------------------------------
    f"{EUTILS}/esearch.fcgi?db=pubmed&term=teclistamab+AND+myeloma&retmax=3&retstart=0&retmode=json&sort=relevance&tool=medical-affairs-skills",
    f"{EUTILS}/esearch.fcgi?db=pubmed&term=zzzznotarealdrugzzzz&retmax=3&retstart=0&retmode=json&sort=relevance&tool=medical-affairs-skills",
    f"{EUTILS}/esummary.fcgi?db=pubmed&id=36001231%2C35660948%2C37000001&retmode=json&tool=medical-affairs-skills",
    f"{EUTILS}/esummary.fcgi?db=pubmed&id=36001231&retmode=json&tool=medical-affairs-skills",
    f"{EUTILS}/esummary.fcgi?db=pubmed&id=99999999&retmode=json&tool=medical-affairs-skills",
    f"{EUTILS}/efetch.fcgi?db=pubmed&id=36001231%2C35660948%2C37000001&retmode=xml&tool=medical-affairs-skills",
    f"{EUTILS}/esearch.fcgi?db=mesh&term=multiple+myeloma&retmax=2&retmode=json&tool=medical-affairs-skills",
    f"{EUTILS}/esummary.fcgi?db=mesh&id=68009101&retmode=json&tool=medical-affairs-skills",
    f"{EUTILS}/esummary.fcgi?db=mesh&id=68000086&retmode=json&tool=medical-affairs-skills",
    # medical-terminology-mapping builds these slightly differently (retmax=1)
    f"{EUTILS}/esearch.fcgi?db=mesh&term=multiple+myeloma&retmax=1&retmode=json&tool=medical-affairs-skills",
    f"{EUTILS}/esearch.fcgi?db=mesh&term=cytokine+storm&retmax=1&retmode=json&tool=medical-affairs-skills",
    f"{EUTILS}/esearch.fcgi?db=mesh&term=zzz+unmappable+phrase&retmax=1&retmode=json&tool=medical-affairs-skills",
    f"{EUTILS}/esearch.fcgi?db=mesh&term=infection&retmax=1&retmode=json&tool=medical-affairs-skills",
    f"{EUTILS}/esearch.fcgi?db=mesh&term=grade+3+CRS+requiring+hospitalisation&retmax=1&retmode=json&tool=medical-affairs-skills",
    f"{EUTILS}/esummary.fcgi?db=mesh&id=68007239&retmode=json&tool=medical-affairs-skills",
    # --- ClinicalTrials.gov ----------------------------------------------
    f"{CTG}/studies?query.term=teclistamab&pageSize=3&countTotal=true",
    f"{CTG}/studies/NCT04557098",
    # --- openFDA ----------------------------------------------------------
    f'{OPENFDA}/drug/label.json?search=openfda.generic_name%3A%22teclistamab%22&limit=1',
    f'{OPENFDA}/drug/event.json?search=patient.drug.openfda.generic_name%3A%22teclistamab%22&count=patient.reaction.reactionmeddrapt.exact&limit=5',
    # openFDA answers "nothing matched" with a 404 and a JSON body, which is a
    # legitimate result rather than an error. Fixture it so that path is tested.
    f'{OPENFDA}/drug/label.json?search=openfda.generic_name%3A%22notadrugatall%22&limit=1',
]


def synthetic_body(url: str) -> tuple[int, str]:
    """Bodies shaped like the real APIs, for offline testing.

    These are hand-built to the published response schemas. They are NOT
    recordings of real responses — the machine this was authored on had no
    egress to these hosts. Re-record with --live to get ground truth.
    """
    # ---- PubMed esearch ---------------------------------------------------
    if "esearch.fcgi" in url and "db=pubmed" in url:
        if "zzzznotarealdrug" in url:
            return 200, json.dumps(
                {"esearchresult": {"count": "0", "retmax": "0", "retstart": "0", "idlist": []}}
            )
        return 200, json.dumps(
            {
                "esearchresult": {
                    "count": "84",
                    "retmax": "3",
                    "retstart": "0",
                    "idlist": ["36001231", "35660948", "37000001"],
                }
            }
        )

    # ---- PubMed esearch on MeSH ------------------------------------------
    if "esearch.fcgi" in url and "db=mesh" in url:
        if "zzz" in url:
            return 200, json.dumps(
                {"esearchresult": {"count": "0", "retmax": "0", "idlist": []}}
            )
        # "cytokine storm" is an entry term for the Cytokine Release Syndrome
        # descriptor — the case that exercises synonym-confidence mapping.
        if "cytokine" in url or "CRS" in url:
            return 200, json.dumps(
                {"esearchresult": {"count": "1", "retmax": "1", "idlist": ["68000086"]}}
            )
        if "term=infection" in url:
            return 200, json.dumps(
                {"esearchresult": {"count": "1", "retmax": "1", "idlist": ["68007239"]}}
            )
        return 200, json.dumps(
            {"esearchresult": {"count": "1", "retmax": "1", "idlist": ["68009101"]}}
        )

    # ---- MeSH esummary ----------------------------------------------------
    if "esummary.fcgi" in url and "db=mesh" in url:
        if "68007239" in url:
            return 200, json.dumps(
                {
                    "result": {
                        "uids": ["68007239"],
                        "68007239": {
                            "uid": "68007239",
                            "ds_meshterms": ["Infections", "Infection"],
                            "ds_scopenote": "Invasion of the host organism by "
                            "microorganisms or their toxins.",
                        },
                    }
                }
            )
        if "68000086" in url:
            return 200, json.dumps(
                {
                    "result": {
                        "uids": ["68000086"],
                        "68000086": {
                            "uid": "68000086",
                            "ds_meshterms": [
                                "Cytokine Release Syndrome",
                                "Cytokine Storm",
                                "Cytokine Storm Syndrome",
                            ],
                            "ds_scopenote": "A condition characterized by systemic "
                            "inflammation following immune cell activation.",
                        },
                    }
                }
            )
        return 200, json.dumps(
            {
                "result": {
                    "uids": ["68009101"],
                    "68009101": {
                        "uid": "68009101",
                        "ds_meshterms": [
                            "Multiple Myeloma",
                            "Myeloma, Multiple",
                            "Plasma Cell Myeloma",
                            "Kahler Disease",
                            "Myelomatosis",
                        ],
                        "ds_scopenote": "A malignancy of mature PLASMA CELLS engaging "
                        "in monoclonal immunoglobulin production.",
                    },
                }
            }
        )

    # ---- PubMed esummary --------------------------------------------------
    if "esummary.fcgi" in url and "db=pubmed" in url:
        if "99999999" in url:
            return 200, json.dumps(
                {
                    "result": {
                        "uids": [],
                        "99999999": {
                            "uid": "99999999",
                            "error": "cannot get document summary",
                        },
                    }
                }
            )
        records = {
            "36001231": {
                "uid": "36001231",
                "pubdate": "2022 Aug 11",
                "source": "N Engl J Med",
                "authors": [
                    {"name": "Moreau P", "authtype": "Author"},
                    {"name": "Garfall AL", "authtype": "Author"},
                    {"name": "van de Donk NWCJ", "authtype": "Author"},
                    {"name": "Nahi H", "authtype": "Author"},
                    {"name": "San-Miguel JF", "authtype": "Author"},
                    {"name": "Oriol A", "authtype": "Author"},
                    {"name": "Nooka AK", "authtype": "Author"},
                ],
                "title": "Teclistamab in Relapsed or Refractory Multiple Myeloma.",
                "volume": "387",
                "issue": "6",
                "pages": "495-505",
                "articleids": [
                    {"idtype": "pubmed", "value": "36001231"},
                    {"idtype": "doi", "value": "10.1056/NEJMoa2203478"},
                ],
                "pubtype": ["Journal Article", "Clinical Trial, Phase I"],
            },
            "35660948": {
                "uid": "35660948",
                "pubdate": "2022 Jun 4",
                "source": "Lancet",
                "authors": [
                    {"name": "Example A", "authtype": "Author"},
                    {"name": "Example B", "authtype": "Author"},
                ],
                "title": "A randomised controlled trial in relapsed myeloma.",
                "volume": "399",
                "issue": "10343",
                "pages": "2210-2220",
                "articleids": [
                    {"idtype": "pubmed", "value": "35660948"},
                    {"idtype": "doi", "value": "10.1016/S0140-6736(22)00000-0"},
                ],
                "pubtype": ["Journal Article", "Randomized Controlled Trial"],
            },
            # A retracted record, so the retraction path is genuinely exercised.
            "37000001": {
                "uid": "37000001",
                "pubdate": "2023 Jan 15",
                "source": "J Example Med",
                "authors": [{"name": "Retracted C", "authtype": "Author"}],
                "title": "A study later retracted.",
                "volume": "10",
                "issue": "1",
                "pages": "1-9",
                "articleids": [
                    {"idtype": "pubmed", "value": "37000001"},
                    {"idtype": "doi", "value": "10.9999/example.2023.1"},
                ],
                "pubtype": ["Journal Article", "Retracted Publication"],
            },
        }
        wanted = [k for k in records if k in url]
        return 200, json.dumps(
            {"result": {"uids": wanted, **{k: records[k] for k in wanted}}}
        )

    # ---- PubMed efetch ----------------------------------------------------
    if "efetch.fcgi" in url:
        return 200, """<?xml version="1.0" ?>
<PubmedArticleSet>
 <PubmedArticle>
  <MedlineCitation>
   <PMID Version="1">36001231</PMID>
   <Article>
    <ArticleTitle>Teclistamab in Relapsed or Refractory Multiple Myeloma.</ArticleTitle>
    <Abstract>
     <AbstractText Label="BACKGROUND">Teclistamab is a T-cell-redirecting bispecific antibody.</AbstractText>
     <AbstractText Label="METHODS">In this phase 1-2 study, we administered teclistamab to patients with relapsed or refractory myeloma.</AbstractText>
     <AbstractText Label="RESULTS">The overall response rate was 63.0% (95% CI, 55.2 to 70.4).</AbstractText>
     <AbstractText Label="CONCLUSIONS">Teclistamab showed substantial activity in this single-arm study.</AbstractText>
    </Abstract>
   </Article>
   <DataBankList>
    <DataBank>
     <DataBankName>ClinicalTrials.gov</DataBankName>
     <AccessionNumberList><AccessionNumber>NCT04557098</AccessionNumber></AccessionNumberList>
    </DataBank>
   </DataBankList>
  </MedlineCitation>
 </PubmedArticle>
 <PubmedArticle>
  <MedlineCitation>
   <PMID Version="1">35660948</PMID>
   <Article>
    <ArticleTitle>A randomised controlled trial in relapsed myeloma.</ArticleTitle>
    <Abstract><AbstractText>A randomised trial with no section labels.</AbstractText></Abstract>
   </Article>
  </MedlineCitation>
 </PubmedArticle>
 <PubmedArticle>
  <MedlineCitation>
   <PMID Version="1">37000001</PMID>
   <Article><ArticleTitle>A study later retracted.</ArticleTitle></Article>
  </MedlineCitation>
 </PubmedArticle>
</PubmedArticleSet>"""

    # ---- ClinicalTrials.gov ----------------------------------------------
    if "/studies/NCT" in url:
        return 200, json.dumps(
            {
                "protocolSection": {
                    "identificationModule": {
                        "nctId": "NCT04557098",
                        "briefTitle": "A Study of Teclistamab in Participants With "
                        "Relapsed or Refractory Multiple Myeloma",
                        "acronym": "MajesTEC-1",
                    },
                    "statusModule": {"overallStatus": "ACTIVE_NOT_RECRUITING"},
                    "designModule": {"phases": ["PHASE1", "PHASE2"]},
                }
            }
        )

    if "/studies?" in url:
        return 200, json.dumps(
            {
                "totalCount": 14,
                "studies": [
                    {
                        "protocolSection": {
                            "identificationModule": {
                                "nctId": "NCT04557098",
                                "briefTitle": "A Study of Teclistamab in RRMM",
                                "acronym": "MajesTEC-1",
                                "organization": {"fullName": "Janssen R&D"},
                            },
                            "statusModule": {
                                "overallStatus": "ACTIVE_NOT_RECRUITING",
                                "startDateStruct": {"date": "2020-10"},
                                "primaryCompletionDateStruct": {"date": "2024-06"},
                            },
                            "designModule": {
                                "phases": ["PHASE1", "PHASE2"],
                                "studyType": "INTERVENTIONAL",
                                "enrollmentInfo": {"count": 165},
                                "designInfo": {
                                    "allocation": "NON_RANDOMIZED",
                                    "primaryPurpose": "TREATMENT",
                                },
                            },
                            "conditionsModule": {"conditions": ["Multiple Myeloma"]},
                            "armsInterventionsModule": {
                                "interventions": [
                                    {"type": "BIOLOGICAL", "name": "Teclistamab"}
                                ]
                            },
                            "sponsorCollaboratorsModule": {
                                "leadSponsor": {"name": "Janssen Research & Development"}
                            },
                            "outcomesModule": {
                                "primaryOutcomes": [
                                    {"measure": "Overall Response Rate", "timeFrame": "Up to 2 years"}
                                ]
                            },
                        }
                    },
                    {
                        "protocolSection": {
                            "identificationModule": {
                                "nctId": "NCT05083169",
                                "briefTitle": "Teclistamab in Earlier Lines",
                                "acronym": "MajesTEC-3",
                            },
                            "statusModule": {"overallStatus": "RECRUITING"},
                            "designModule": {
                                "phases": ["PHASE3"],
                                "studyType": "INTERVENTIONAL",
                                "enrollmentInfo": {"count": 560},
                                "designInfo": {"allocation": "RANDOMIZED"},
                            },
                            "conditionsModule": {"conditions": ["Multiple Myeloma"]},
                            "sponsorCollaboratorsModule": {
                                "leadSponsor": {"name": "Janssen Research & Development"}
                            },
                        }
                    },
                ],
            }
        )

    # ---- openFDA ----------------------------------------------------------
    if "drug/label.json" in url and "notadrugatall" in url:
        return 404, json.dumps(
            {"error": {"code": "NOT_FOUND", "message": "No matches found!"}}
        )

    if "drug/label.json" in url:
        return 200, json.dumps(
            {
                "meta": {"results": {"skip": 0, "limit": 1, "total": 1}},
                "results": [
                    {
                        "openfda": {
                            "generic_name": ["TECLISTAMAB-CQYV"],
                            "brand_name": ["TECVAYLI"],
                            "manufacturer_name": ["Janssen Biotech, Inc."],
                        },
                        "indications_and_usage": [
                            "TECVAYLI is indicated for the treatment of adult patients "
                            "with relapsed or refractory multiple myeloma who have "
                            "received at least four prior lines of therapy."
                        ],
                        "boxed_warning": [
                            "WARNING: CYTOKINE RELEASE SYNDROME and NEUROLOGIC TOXICITY"
                        ],
                        "warnings_and_cautions": [
                            "Cytokine Release Syndrome: occurred in 72% of patients."
                        ],
                        "adverse_reactions": [
                            "Most common adverse reactions were CRS, pyrexia, and "
                            "musculoskeletal pain."
                        ],
                    }
                ],
            }
        )

    if "drug/event.json" in url:
        return 200, json.dumps(
            {
                "meta": {"results": {"skip": 0, "limit": 5, "total": 5}},
                "results": [
                    {"term": "CYTOKINE RELEASE SYNDROME", "count": 412},
                    {"term": "PYREXIA", "count": 260},
                    {"term": "NEUTROPENIA", "count": 188},
                    {"term": "PNEUMONIA", "count": 143},
                    {"term": "COVID-19", "count": 97},
                ],
            }
        )

    return 404, ""


def fetch_live(url: str) -> tuple[int, str]:
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "medical-affairs-skills/1.0"}
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")
    except Exception as exc:  # noqa: BLE001 — surfacing the reason is the point
        print(f"  ! {exc}")
        return 0, ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--live", action="store_true",
                    help="record real responses instead of synthetic ones")
    args = ap.parse_args()

    import time

    cache: dict[str, dict] = {}
    for url in REQUESTS:
        if args.live:
            print(f"GET {url[:100]}...")
            status, body = fetch_live(url)
            time.sleep(0.4)  # be a good API citizen
            if status != 200:
                print(f"  -> HTTP {status}; keeping any existing fixture")
                if FIXTURES.exists():
                    old = json.loads(FIXTURES.read_text(encoding="utf-8"))
                    if url in old:
                        cache[url] = old[url]
                continue
        else:
            status, body = synthetic_body(url)
            # A non-200 WITH a body is a real API behaviour worth fixturing
            # (openFDA's 404-means-no-matches). A non-200 with no body means
            # nothing was defined for this URL.
            if not body:
                print(f"  ! no synthetic body defined for {url}")
                continue
        cache[url] = {"status": status, "body": body}

    FIXTURES.parent.mkdir(parents=True, exist_ok=True)
    FIXTURES.write_text(json.dumps(cache, indent=1, sort_keys=True), encoding="utf-8")
    kind = "live" if args.live else "synthetic"
    print(f"\nWrote {len(cache)} {kind} fixture(s) to {FIXTURES.relative_to(REPO)}")
    if not args.live:
        print(
            "\nNote: these are hand-built to the published response schemas, not\n"
            "recordings. Run with --live from a network with egress to verify the\n"
            "real APIs still match."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
