#!/usr/bin/env python3
"""ClinicalTrials.gov API v2 client for trial landscape assessment.

The registry shows what is being answered right now, which the published
literature cannot. For Medical Affairs that is usually the more actionable half
of the picture.

    S=skills/clinical-trials-search/scripts/ctgov.py

    python3 $S search --intervention teclistamab --limit 25
    python3 $S search --condition "multiple myeloma" --phase 3 --status RECRUITING
    python3 $S search --sponsor Janssen --condition "multiple myeloma" --format table
    python3 $S get     --nct NCT04557098
    python3 $S history --nct NCT04557098

No API key required. Self-contained by design — see CONTRIBUTING.md on why each
skill owns its client rather than importing a shared library.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field, asdict
from pathlib import Path

API = "https://clinicaltrials.gov/api/v2"
UA = "medical-affairs-skills/1.0"

STATUSES = {
    "NOT_YET_RECRUITING", "RECRUITING", "ENROLLING_BY_INVITATION",
    "ACTIVE_NOT_RECRUITING", "SUSPENDED", "TERMINATED", "COMPLETED",
    "WITHDRAWN", "UNKNOWN",
}


@dataclass
class Trial:
    nct_id: str = ""
    title: str = ""
    acronym: str = ""
    status: str = ""
    why_stopped: str = ""
    phases: list[str] = field(default_factory=list)
    study_type: str = ""
    allocation: str = ""
    masking: str = ""
    primary_purpose: str = ""
    enrollment: str = ""
    enrollment_type: str = ""
    conditions: list[str] = field(default_factory=list)
    interventions: list[str] = field(default_factory=list)
    sponsor: str = ""
    collaborators: list[str] = field(default_factory=list)
    primary_outcomes: list[str] = field(default_factory=list)
    start_date: str = ""
    primary_completion: str = ""
    completion: str = ""
    last_update: str = ""
    eligibility: str = ""
    has_results: bool = False

    @property
    def design_caveat(self) -> str:
        """The sentence an appraiser needs and the phase label does not give."""
        if self.study_type == "OBSERVATIONAL":
            return "Observational — associational only"
        if self.allocation == "NON_RANDOMIZED" or (
            self.study_type == "INTERVENTIONAL" and self.allocation == ""
        ):
            return "Non-randomised/single-arm — no comparative inference"
        if self.allocation == "RANDOMIZED":
            m = self.masking or "masking not stated"
            return f"Randomised ({m})"
        return ""


def http_get(url: str, fixtures: dict | None, retries: int = 3) -> tuple[int, str]:
    if fixtures is not None:
        entry = fixtures.get(url)
        if entry is None:
            raise SystemExit(f"No fixture recorded for:\n  {url}")
        return entry.get("status", 200), entry.get("body", "")

    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45) as resp:
                return resp.status, resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(2**attempt)
                continue
            return exc.code, ""
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt < retries - 1:
                time.sleep(2**attempt)
                continue
            raise SystemExit(
                f"Could not reach clinicaltrials.gov: {exc}\n"
                f"See docs/api-setup.md for hosts that must be allowlisted."
            )
    return 0, ""


def parse_study(study: dict) -> Trial:
    p = study.get("protocolSection", {})
    ident = p.get("identificationModule", {})
    status = p.get("statusModule", {})
    design = p.get("designModule", {})
    design_info = design.get("designInfo", {})
    arms = p.get("armsInterventionsModule", {})
    cond = p.get("conditionsModule", {})
    spons = p.get("sponsorCollaboratorsModule", {})
    outcomes = p.get("outcomesModule", {})
    elig = p.get("eligibilityModule", {})

    t = Trial(
        nct_id=ident.get("nctId", ""),
        title=ident.get("briefTitle", ""),
        acronym=ident.get("acronym", ""),
        status=status.get("overallStatus", ""),
        why_stopped=status.get("whyStopped", ""),
        phases=design.get("phases", []) or [],
        study_type=design.get("studyType", ""),
        allocation=design_info.get("allocation", ""),
        masking=(design_info.get("maskingInfo") or {}).get("masking", ""),
        primary_purpose=design_info.get("primaryPurpose", ""),
        enrollment=str((design.get("enrollmentInfo") or {}).get("count", "")),
        enrollment_type=(design.get("enrollmentInfo") or {}).get("type", ""),
        conditions=cond.get("conditions", []) or [],
        interventions=[
            f"{i.get('type', '')}: {i.get('name', '')}".strip(": ")
            for i in arms.get("interventions", []) or []
        ],
        sponsor=(spons.get("leadSponsor") or {}).get("name", ""),
        collaborators=[c.get("name", "") for c in spons.get("collaborators", []) or []],
        primary_outcomes=[
            f"{o.get('measure', '')} [{o.get('timeFrame', 'timeframe not stated')}]"
            for o in outcomes.get("primaryOutcomes", []) or []
        ],
        start_date=(status.get("startDateStruct") or {}).get("date", ""),
        primary_completion=(status.get("primaryCompletionDateStruct") or {}).get("date", ""),
        completion=(status.get("completionDateStruct") or {}).get("date", ""),
        last_update=(status.get("lastUpdatePostDateStruct") or {}).get("date", ""),
        eligibility=(elig.get("eligibilityCriteria") or "")[:1500],
        has_results=bool(study.get("resultsSection")),
    )
    return t


def search(args, fixtures) -> tuple[int, list[Trial]]:
    params: dict[str, str] = {}
    if args.term:
        params["query.term"] = args.term
    if args.condition:
        params["query.cond"] = args.condition
    if args.intervention:
        params["query.intr"] = args.intervention
    if args.sponsor:
        params["query.spons"] = args.sponsor
    if args.status:
        bad = [s for s in args.status.upper().split(",") if s.strip() not in STATUSES]
        if bad:
            raise SystemExit(
                f"Unknown status: {', '.join(bad)}\nValid: {', '.join(sorted(STATUSES))}"
            )
        params["filter.overallStatus"] = args.status.upper()
    if args.phase:
        phases = ["PHASE" + p.strip() for p in args.phase.split(",") if p.strip()]
        params["query.term"] = (
            params.get("query.term", "") + " AREA[Phase](" + " OR ".join(phases) + ")"
        ).strip()

    if not params:
        raise SystemExit(
            "Give at least one of --term, --condition, --intervention, --sponsor."
        )

    params["pageSize"] = str(min(args.limit, 100))
    params["countTotal"] = "true"

    trials: list[Trial] = []
    total = 0
    token = ""
    while len(trials) < args.limit:
        q = dict(params)
        if token:
            q["pageToken"] = token
        url = f"{API}/studies?" + urllib.parse.urlencode(q)
        status, body = http_get(url, fixtures)
        if status != 200 or not body:
            raise SystemExit(f"ClinicalTrials.gov returned HTTP {status}")
        data = json.loads(body)
        total = data.get("totalCount", total)
        page = data.get("studies", [])
        if not page:
            break
        trials.extend(parse_study(s) for s in page)
        token = data.get("nextPageToken", "")
        if not token or fixtures is not None:
            break
    return total, trials[: args.limit]


def render(trials: list[Trial], total: int, fmt: str, query_desc: str) -> str:
    if fmt == "json":
        return json.dumps(
            {"query": query_desc, "total": total, "returned": len(trials),
             "trials": [asdict(t) for t in trials]},
            indent=2,
        )

    if fmt == "table":
        rows = [
            f"{'NCT':<12} {'Phase':<12} {'Status':<24} {'N':>6}  {'Compl.':<9} Sponsor / Title"
        ]
        rows.append("-" * 118)
        for t in trials:
            ph = ",".join(x.replace("PHASE", "P") for x in t.phases) or "n/a"
            rows.append(
                f"{t.nct_id:<12} {ph:<12} {t.status[:24]:<24} {t.enrollment:>6}  "
                f"{t.primary_completion:<9} {t.sponsor[:22]} — {(t.acronym or t.title)[:40]}"
            )
        return "\n".join(rows)

    out = [
        f"**ClinicalTrials.gov** — {query_desc}",
        f"{total} record(s) matched · {len(trials)} retrieved · "
        f"searched {time.strftime('%Y-%m-%d')}",
        "",
        "_Registry coverage is not global (EU CTIS, ISRCTN, jRCT, ChiCTR not "
        "included) and status fields are sponsor-maintained._",
        "",
    ]
    for t in trials:
        head = f"### {t.acronym + ' — ' if t.acronym else ''}{t.title}"
        out.append(head)
        ph = ", ".join(x.replace("PHASE", "Phase ") for x in t.phases) or "not stated"
        out.append(f"`{t.nct_id}` · {ph} · **{t.status}**")
        if t.why_stopped:
            out.append(f"> ⚠ **Stopped:** {t.why_stopped}")
        if t.design_caveat:
            out.append(f"*Design: {t.design_caveat}*")
        # "estimated" vs "actual" is the difference between a target and a
        # result, so never print the number without it when it is available.
        n = "not stated"
        if t.enrollment:
            n = t.enrollment + (
                f" ({t.enrollment_type.lower()})" if t.enrollment_type else ""
            )
        out.append(f"- Enrolment: {n}")
        out.append(f"- Sponsor: {t.sponsor}" + (f" (+{len(t.collaborators)} collaborators)" if t.collaborators else ""))
        if t.conditions:
            out.append(f"- Conditions: {', '.join(t.conditions[:4])}")
        if t.interventions:
            out.append(f"- Interventions: {'; '.join(t.interventions[:4])}")
        for po in t.primary_outcomes[:3]:
            out.append(f"- Primary outcome: {po}")
        out.append(
            f"- Dates: start {t.start_date or '?'} · primary completion "
            f"{t.primary_completion or '?'} · last updated {t.last_update or '?'}"
        )
        if t.has_results:
            out.append("- Results posted: yes")
        out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--fixtures", help="offline fixture directory or file")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="search the registry")
    s.add_argument("--term", default="", help="free-text across all fields")
    s.add_argument("--condition", default="")
    s.add_argument("--intervention", default="")
    s.add_argument("--sponsor", default="")
    s.add_argument("--status", default="", help="comma-separated, e.g. RECRUITING,COMPLETED")
    s.add_argument("--phase", default="", help="comma-separated, e.g. 2,3")
    s.add_argument("--limit", type=int, default=25)
    s.add_argument("--format", default="markdown", choices=["json", "markdown", "table"])

    g = sub.add_parser("get", help="one trial in full")
    g.add_argument("--nct", required=True)
    g.add_argument("--format", default="markdown", choices=["json", "markdown", "table"])

    h = sub.add_parser("history", help="check whether the protocol changed after registration")
    h.add_argument("--nct", required=True)

    args = ap.parse_args()

    fixtures = None
    if args.fixtures:
        p = Path(args.fixtures)
        p = p / "http_cache.json" if p.is_dir() else p
        fixtures = json.loads(p.read_text(encoding="utf-8"))

    if args.cmd == "search":
        desc = ", ".join(
            f"{k}={v}"
            for k, v in [
                ("term", args.term), ("condition", args.condition),
                ("intervention", args.intervention), ("sponsor", args.sponsor),
                ("status", args.status), ("phase", args.phase),
            ]
            if v
        )
        total, trials = search(args, fixtures)
        if not trials:
            if args.format == 'json':
                print(render([], total, 'json', desc))
                return 0
            print(f"No trials matched: {desc}")
            print(
                "\nBefore concluding nothing is running: sponsor names vary across\n"
                "subsidiaries, and this registry is not global. Try variants, and\n"
                "check EU CTIS / ISRCTN / jRCT before reporting a gap."
            )
            return 0
        print(render(trials, total, args.format, desc))
        if total > len(trials) and args.format != 'json':
            print(f"\n_Showing {len(trials)} of {total}. Raise --limit._")
        return 0

    if args.cmd == "get":
        nct = args.nct.upper()
        status, body = http_get(f"{API}/studies/{nct}", fixtures)
        if status != 200 or not body:
            print(f"{nct} did not resolve (HTTP {status}).")
            print("This NCT number is unverified. Check the identifier and access; failure alone does not prove fabrication.")
            return 1
        trial = parse_study(json.loads(body))
        print(render([trial], 1, args.format, nct))
        return 0

    if args.cmd == "history":
        nct = args.nct.upper()
        url = f"{API}/studies/{nct}?fields=protocolSection.statusModule"
        status, body = http_get(url, fixtures)
        if status != 200:
            print(f"{nct} did not resolve (HTTP {status}).")
            return 1
        print(
            f"Change history for {nct} is not exposed as structured data by the v2\n"
            f"API. Read it here:\n\n"
            f"  https://clinicaltrials.gov/study/{nct}?tab=history\n\n"
            f"What to look for, and why it matters:\n"
            f"  - Primary outcome measure changed AFTER the study start date.\n"
            f"    This is a RoB 2 domain 5 concern (selective reporting) and is\n"
            f"    invisible in the eventual publication.\n"
            f"  - Sample size revised downward — may indicate recruitment failure\n"
            f"    or an underpowered final analysis.\n"
            f"  - Eligibility criteria narrowed mid-trial — changes who the result\n"
            f"    generalises to.\n"
            f"  - Completion dates repeatedly pushed — a programme in difficulty."
        )
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
