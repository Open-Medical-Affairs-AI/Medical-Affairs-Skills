#!/usr/bin/env python3
"""Self-contained interactive HTML report — the one output that always works.

One file. No CDN, no external stylesheet, no web font, no remote image. These
documents get emailed, opened on aircraft, opened inside networks that block
outbound requests, and archived for years. A report that renders as unstyled
text because a CDN moved is a report nobody trusts again.

    S=skills/interactive-html-report/scripts/build_report.py
    python3 $S --example > report.json
    python3 $S --spec report.json --out insights.html

No dependencies.
"""
from __future__ import annotations
import argparse, json, sys
from html import escape
from pathlib import Path

DRAFT = "DRAFT — NOT FOR EXTERNAL USE. REQUIRES QUALIFIED MEDICAL REVIEW."

EXAMPLE = {
    "title": "Field insight report — Q2 2026",
    "subtitle": "Relapsed/refractory multiple myeloma · NORVANTIB",
    "meta": "Prepared 2026-08-15 · Medical Affairs · US",
    "sections": [
        {"type": "summary", "title": "What leadership should know",
         "items": [
             "Adoption is gated on delivery, not efficacy — 11 records across all settings.",
             "The field has stopped comparing on response rate; durability is the question.",
             "Infection prophylaxis practice is standardising without us.",
         ]},
        {"type": "table", "title": "Insights", "filterable": True,
         "columns": ["#", "Insight", "Sources", "Confidence", "Action", "Owner"],
         "rows": [
             ["1", "Delivery capability gates adoption", "11/55", "High",
              "Fund outpatient step-up study", "Evidence Generation"],
             ["2", "Durability, not ORR, is the question", "8/55", "High",
              "Push 24-month data to field", "Sci Comms"],
             ["3", "Prophylaxis practice diverging", "3/55", "Medium",
              "Bring prophylaxis analysis forward", "Publications"],
         ]},
        {"type": "evidence", "title": "Evidence behind insight 1",
         "items": [{
             "claim": "Outpatient step-up dosing appears feasible without CRS escalation.",
             "certainty": "Low",
             "detail": "One centre, 11 patients, no escalations (OBS-003). Competitor "
                       "prospective data n=94 shows no grade 3+ CRS with outpatient "
                       "step-up. Single-arm; no comparative inference available.",
             "source": "Field record OBS-003; congress abstract 1003 [abstract]",
         }]},
        {"type": "provenance", "title": "Provenance",
         "items": ["55 records, 30 contacts, 7 MSLs, 2026-04-01 to 2026-06-28",
                   "No network access — references NOT verified",
                   "Could not determine: payer perspective (absent from corpus)"]},
    ],
}

CSS = """
:root{--ink:#1a1a1a;--muted:#5a5a5a;--line:#dcdcdc;--accent:#00518c;--warn:#993300;--bg:#fff;--panel:#f7f9fb}
*{box-sizing:border-box}
body{margin:0;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg)}
.draft{position:sticky;top:0;z-index:10;background:var(--warn);color:#fff;font-weight:700;font-size:13px;padding:8px 20px;letter-spacing:.02em}
header{padding:28px 20px 12px;max-width:1100px;margin:0 auto}
h1{font-size:26px;margin:0 0 6px}
.sub{color:var(--muted);margin:0 0 4px}
.meta{color:var(--muted);font-size:13px}
main{max-width:1100px;margin:0 auto;padding:0 20px 60px}
section{margin:32px 0;border-top:1px solid var(--line);padding-top:20px}
h2{font-size:19px;color:var(--accent);margin:0 0 14px}
ul{margin:0;padding-left:20px}li{margin-bottom:8px}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:var(--panel);font-weight:600;cursor:pointer;user-select:none}
th:hover{background:#eef2f6}
th[aria-sort]::after{content:" ▾";color:var(--accent)}
th[aria-sort="ascending"]::after{content:" ▴"}
tbody tr:hover{background:#fafcfe}
.filter{margin-bottom:10px;padding:8px 10px;border:1px solid var(--line);border-radius:5px;width:100%;max-width:380px;font:inherit;font-size:14px}
details{border:1px solid var(--line);border-radius:6px;padding:12px 14px;margin-bottom:10px;background:var(--panel)}
summary{cursor:pointer;font-weight:600}
.cert{display:inline-block;font-size:11px;font-weight:700;padding:2px 7px;border-radius:3px;border:1px solid;margin-left:8px}
.cert-High{color:#1b5e20;border-color:#1b5e20;background:#e8f5e9}
.cert-Moderate{color:#7a5200;border-color:#7a5200;background:#fff8e1}
.cert-Low,.cert-Very-low{color:#8a1c1c;border-color:#8a1c1c;background:#fdecea}
.src{font-size:12.5px;color:var(--muted);margin-top:8px}
footer{max-width:1100px;margin:0 auto;padding:20px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}
@media print{
  /* Nothing important may hide behind interaction — a printed page that omits
     safety data is a fair balance failure. */
  details{border:none;background:none}
  details>*{display:block!important}
  details[open],details:not([open]){}
  details>summary{list-style:none}
  .filter,th{cursor:auto}
  .draft{position:static;background:none;color:var(--warn);border-bottom:2px solid var(--warn)}
  section{page-break-inside:avoid}
}
"""

JS = """
// Progressive enhancement only: every row is already in the HTML. With
// JavaScript disabled the report is complete, just not filterable.
document.querySelectorAll('table[data-sortable]').forEach(function(t){
  t.querySelectorAll('th').forEach(function(th,i){
    th.setAttribute('tabindex','0');
    function sort(){
      var body=t.tBodies[0], rows=[].slice.call(body.rows);
      var asc=th.getAttribute('aria-sort')!=='ascending';
      t.querySelectorAll('th').forEach(function(o){o.removeAttribute('aria-sort')});
      th.setAttribute('aria-sort',asc?'ascending':'descending');
      rows.sort(function(a,b){
        var x=a.cells[i].innerText.trim(), y=b.cells[i].innerText.trim();
        var nx=parseFloat(x), ny=parseFloat(y);
        if(!isNaN(nx)&&!isNaN(ny)) return asc?nx-ny:ny-nx;
        return asc?x.localeCompare(y):y.localeCompare(x);
      });
      rows.forEach(function(r){body.appendChild(r)});
    }
    th.addEventListener('click',sort);
    th.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();sort();}});
  });
});
document.querySelectorAll('input[data-filters]').forEach(function(inp){
  inp.addEventListener('input',function(){
    var t=document.getElementById(inp.getAttribute('data-filters'));
    var q=inp.value.toLowerCase();
    [].slice.call(t.tBodies[0].rows).forEach(function(r){
      r.style.display=r.innerText.toLowerCase().indexOf(q)>-1?'':'none';
    });
  });
});
"""


def render(spec: dict) -> str:
    parts = []
    for i, s in enumerate(spec.get("sections", [])):
        kind = s.get("type")
        parts.append(f'<section><h2>{escape(s.get("title",""))}</h2>')
        if kind in ("summary", "provenance"):
            parts.append("<ul>" + "".join(
                f"<li>{escape(x)}</li>" for x in s.get("items", [])) + "</ul>")
        elif kind == "table":
            tid = f"t{i}"
            if s.get("filterable"):
                parts.append(f'<input class="filter" data-filters="{tid}" '
                             f'placeholder="Filter rows…" aria-label="Filter table">')
            head = "".join(f"<th>{escape(str(c))}</th>" for c in s.get("columns", []))
            body = "".join(
                "<tr>" + "".join(f"<td>{escape(str(c))}</td>" for c in row) + "</tr>"
                for row in s.get("rows", []))
            parts.append(f'<table id="{tid}" data-sortable><thead><tr>{head}</tr>'
                         f'</thead><tbody>{body}</tbody></table>')
        elif kind == "cards":
            for it in s.get("items", []):
                parts.append(f'<details open><summary>{escape(it.get("title",""))}'
                             f'</summary><p>{escape(it.get("body",""))}</p></details>')
        elif kind == "evidence":
            for it in s.get("items", []):
                cert = str(it.get("certainty", "")).replace(" ", "-")
                parts.append(
                    f'<details><summary>{escape(it.get("claim",""))}'
                    f'<span class="cert cert-{escape(cert)}">'
                    f'{escape(it.get("certainty",""))}</span></summary>'
                    f'<p>{escape(it.get("detail",""))}</p>'
                    f'<p class="src">Source: {escape(it.get("source","not stated"))}</p>'
                    f'</details>')
        elif kind == "figure":
            parts.append(s.get("svg", "<p><em>No figure supplied.</em></p>"))
            if s.get("caption"):
                parts.append(f'<p class="src">{escape(s["caption"])}</p>')
        parts.append("</section>")

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(spec.get('title','Report'))}</title>
<style>{CSS}</style></head><body>
<div class="draft">{DRAFT}</div>
<header>
  <h1>{escape(spec.get('title',''))}</h1>
  <p class="sub">{escape(spec.get('subtitle',''))}</p>
  <p class="meta">{escape(spec.get('meta',''))}</p>
</header>
<main>{''.join(parts)}</main>
<footer>{DRAFT}<br>Self-contained: no external assets. Safe to email, archive
and open offline.</footer>
<script>{JS}</script>
</body></html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec"); ap.add_argument("--out", default="report.html")
    ap.add_argument("--example", action="store_true")
    args = ap.parse_args()
    if args.example:
        print(json.dumps(EXAMPLE, indent=2)); return 0
    spec = (json.loads(Path(args.spec).read_text(encoding="utf-8"))
            if args.spec else EXAMPLE)
    p = Path(args.out); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(render(spec), encoding="utf-8")
    print(f"Wrote {p} ({p.stat().st_size:,} bytes, fully self-contained)")
    print("No external assets. Content is present in the HTML — JavaScript only "
          "adds sorting and filtering, so it works with JS disabled.")
    print("Everything expands under @media print, so a printed copy cannot hide "
          "safety data behind a collapsed section.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
