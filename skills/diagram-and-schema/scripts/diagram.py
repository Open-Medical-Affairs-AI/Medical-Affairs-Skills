#!/usr/bin/env python3
"""Diagrams for Medical Affairs — Mermaid first, SVG next, ASCII as the floor.

Mermaid is text, so it diffs in a pull request and someone who cannot use a
drawing tool can still edit it. It renders natively on GitHub and in many agent
runtimes; when it does not render, the source is still readable.

    S=skills/diagram-and-schema/scripts/diagram.py

    python3 $S --example prisma > prisma.json
    python3 $S prisma  --spec prisma.json --out flow.mmd
    python3 $S prisma  --spec prisma.json --out flow.svg --format svg
    python3 $S pathway --spec pathway.json --format ascii

No dependencies.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from xml.sax.saxutils import escape

EXAMPLES = {
    "prisma": {
        "title": "PRISMA 2020 flow",
        "sources": {"PubMed/MEDLINE": 412, "Embase": 388, "CENTRAL": 94,
                    "Registries": 31, "Hand-searching": 12},
        "duplicates": 284,
        "screened_excluded": 561,
        "not_retrieved": 3,
        "excluded_full_text": {"Wrong population": 31, "Wrong comparator": 18,
                               "No outcome of interest": 14, "Duplicate report": 9,
                               "Abstract only, insufficient detail": 6},
        "included_studies": 11,
        "included_reports": 17,
    },
    "pathway": {
        "title": "Treatment pathway — relapsed/refractory myeloma",
        "nodes": [
            {"id": "dx", "label": "Relapsed disease confirmed"},
            {"id": "l1", "label": "Prior lines 1-3\n(triple-class exposure)"},
            {"id": "assess", "label": "Fit for T-cell redirection?", "shape": "decision"},
            {"id": "bispec", "label": "Bispecific antibody"},
            {"id": "alt", "label": "Alternative regimen"},
            {"id": "prog", "label": "Progression", "shape": "decision"},
            {"id": "next", "label": "Switch target class\n(ORR 58% vs 31% same class)"},
        ],
        "edges": [
            {"from": "dx", "to": "l1", "label": ""},
            {"from": "l1", "to": "assess", "label": ""},
            {"from": "assess", "to": "bispec", "label": "yes"},
            {"from": "assess", "to": "alt", "label": "no — frailty, access, no bed"},
            {"from": "bispec", "to": "prog", "label": ""},
            {"from": "prog", "to": "next", "label": "yes"},
        ],
        "divergence": [
            "Guideline says 4+ prior lines; practice increasingly uses 3 (field data)",
            "Inpatient step-up assumed; several centres now outpatient",
        ],
        "omits": "Supportive care, prophylaxis and transplant-eligible pathways.",
    },
    "schema": {
        "title": "Study schema — NVB-440",
        "nodes": [
            {"id": "scr", "label": "Screening\n(28 days)"},
            {"id": "rand", "label": "Randomisation 1:1\n(N=2280)", "shape": "decision"},
            {"id": "a", "label": "Arm A: investigational\nweekly SC"},
            {"id": "b", "label": "Arm B: standard of care"},
            {"id": "ep", "label": "Primary endpoint\nweight change at wk 72"},
        ],
        "edges": [
            {"from": "scr", "to": "rand", "label": ""},
            {"from": "rand", "to": "a", "label": "50%"},
            {"from": "rand", "to": "b", "label": "50%"},
            {"from": "a", "to": "ep", "label": "assessed q12w"},
            {"from": "b", "to": "ep", "label": "assessed q12w"},
        ],
        "omits": "Open-label extension and the off-treatment follow-up period.",
    },
}


def prisma_numbers(s: dict) -> dict:
    """Do the arithmetic, and refuse to emit a diagram that does not balance.

    Reviewers check this. A PRISMA diagram whose numbers do not add up is the
    fastest way to lose their confidence in the whole review.
    """
    identified = sum(s["sources"].values())
    screened = identified - s["duplicates"]
    sought = screened - s["screened_excluded"]
    assessed = sought - s.get("not_retrieved", 0)
    excluded = sum(s["excluded_full_text"].values())
    included = assessed - excluded
    if included != s["included_studies"]:
        raise SystemExit(
            f"PRISMA numbers do not reconcile.\n"
            f"  identified {identified} − duplicates {s['duplicates']} = screened {screened}\n"
            f"  − screened-out {s['screened_excluded']} = sought {sought}\n"
            f"  − not retrieved {s.get('not_retrieved', 0)} = assessed {assessed}\n"
            f"  − excluded {excluded} = {included}\n"
            f"  but included_studies says {s['included_studies']}.\n"
            f"Fix the numbers. Reviewers do this subtraction."
        )
    return {"identified": identified, "screened": screened, "sought": sought,
            "assessed": assessed, "excluded": excluded, "included": included}


def prisma_mermaid(s: dict) -> str:
    n = prisma_numbers(s)
    src = "<br>".join(f"{k} (n={v})" for k, v in s["sources"].items())
    exc = "<br>".join(f"{k} (n={v})" for k, v in s["excluded_full_text"].items())
    return f"""flowchart TD
    A["<b>Identification</b><br>{src}<br><b>Total n={n['identified']}</b>"]
    A -->|"Duplicates removed (n={s['duplicates']})"| B["Records screened<br>n={n['screened']}"]
    B -->|"Excluded (n={s['screened_excluded']})"| C["Reports sought for retrieval<br>n={n['sought']}"]
    C -->|"Not retrieved (n={s.get('not_retrieved', 0)})"| D["Reports assessed for eligibility<br>n={n['assessed']}"]
    D -->|"Excluded (n={n['excluded']})<br>{exc}"| E["<b>Studies included</b><br>n={s['included_studies']}<br>reported in n={s['included_reports']} publications"]
    style E fill:#e8f4ea,stroke:#009E73,stroke-width:2px
"""


def flow_mermaid(s: dict) -> str:
    lines = ["flowchart TD"]
    for node in s["nodes"]:
        label = node["label"].replace("\n", "<br>")
        if node.get("shape") == "decision":
            lines.append(f'    {node["id"]}{{"{label}"}}')
        else:
            lines.append(f'    {node["id"]}["{label}"]')
    for e in s["edges"]:
        arrow = f'-->|"{e["label"]}"|' if e.get("label") else "-->"
        lines.append(f'    {e["from"]} {arrow} {e["to"]}')
    return "\n".join(lines) + "\n"


def flow_svg(s: dict) -> str:
    """Simple vertical layout. Deliberately plain — legibility over elegance."""
    nodes = s["nodes"]
    W, box_w, box_h, gap = 760, 300, 74, 46
    H = 90 + len(nodes) * (box_h + gap)
    out = [f'<text x="30" y="42" font-family="Helvetica,Arial" font-size="17" '
           f'font-weight="bold">{escape(s.get("title", ""))}</text>']
    pos = {}
    for i, node in enumerate(nodes):
        x, y = (W - box_w) / 2, 74 + i * (box_h + gap)
        pos[node["id"]] = (x + box_w / 2, y, y + box_h)
        if node.get("shape") == "decision":
            cx, cy = x + box_w / 2, y + box_h / 2
            out.append(f'<polygon points="{cx},{y} {x+box_w},{cy} {cx},{y+box_h} {x},{cy}" '
                       f'fill="#fff7e6" stroke="#E69F00" stroke-width="1.8"/>')
        else:
            out.append(f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="6" '
                       f'fill="#eef4fa" stroke="#0072B2" stroke-width="1.6"/>')
        for j, line in enumerate(node["label"].split("\n")):
            out.append(f'<text x="{x+box_w/2}" y="{y+box_h/2 - 6 + j*15}" '
                       f'font-family="Helvetica,Arial" font-size="12.5" '
                       f'text-anchor="middle">{escape(line)}</text>')
    for e in s["edges"]:
        if e["from"] not in pos or e["to"] not in pos:
            continue
        x1, _, y1 = pos[e["from"]]
        x2, y2, _ = pos[e["to"]]
        out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#555" '
                   f'stroke-width="1.6" marker-end="url(#a)"/>')
        if e.get("label"):
            out.append(f'<text x="{x1+8}" y="{(y1+y2)/2+4}" font-family="Helvetica,Arial" '
                       f'font-size="11" fill="#555">{escape(e["label"])}</text>')
    if s.get("omits"):
        out.append(f'<text x="30" y="{H-16}" font-family="Helvetica,Arial" font-size="10" '
                   f'fill="#993300">Omits: {escape(s["omits"])}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}"><defs><marker id="a" markerWidth="9" markerHeight="9" '
            f'refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#555"/>'
            f'</marker></defs><rect width="{W}" height="{H}" fill="white"/>'
            + "".join(out) + "</svg>")


def flow_ascii(s: dict) -> str:
    lines = [s.get("title", ""), "=" * len(s.get("title", "")), ""]
    byid = {n["id"]: n for n in s["nodes"]}
    for node in s["nodes"]:
        mark = "<>" if node.get("shape") == "decision" else "[]"
        label = node["label"].replace("\n", " / ")
        lines.append(f"  {mark[0]} {label} {mark[1]}")
        outs = [e for e in s["edges"] if e["from"] == node["id"]]
        for e in outs:
            tgt = byid.get(e["to"], {}).get("label", e["to"]).replace("\n", " / ")
            lbl = f" ({e['label']})" if e.get("label") else ""
            lines.append(f"      |{lbl}")
            lines.append(f"      v  {tgt}")
        lines.append("")
    if s.get("omits"):
        lines += [f"Omits: {s['omits']}"]
    return "\n".join(lines) + "\n"


def prisma_ascii(s: dict) -> str:
    n = prisma_numbers(s)
    L = [s.get("title", "PRISMA flow"), "=" * 40, ""]
    L.append("IDENTIFICATION")
    for k, v in s["sources"].items():
        L.append(f"  {k}: n={v}")
    L += [f"  Total identified: n={n['identified']}",
          f"  Duplicates removed: n={s['duplicates']}", "",
          "SCREENING",
          f"  Records screened: n={n['screened']}",
          f"  Excluded: n={s['screened_excluded']}",
          f"  Reports sought: n={n['sought']}",
          f"  Not retrieved: n={s.get('not_retrieved', 0)}",
          f"  Assessed for eligibility: n={n['assessed']}",
          "  Excluded, with reasons:"]
    for k, v in s["excluded_full_text"].items():
        L.append(f"    {k}: n={v}")
    L += ["", "INCLUDED",
          f"  Studies: n={s['included_studies']}",
          f"  Reported in: n={s['included_reports']} publications",
          "", "Numbers reconcile."]
    return "\n".join(L) + "\n"


KINDS = {
    "prisma": {"mermaid": prisma_mermaid, "ascii": prisma_ascii,
               "svg": lambda s: flow_svg({"title": s.get("title", "PRISMA"),
                                          "nodes": [], "edges": []})},
    "pathway": {"mermaid": flow_mermaid, "svg": flow_svg, "ascii": flow_ascii},
    "schema": {"mermaid": flow_mermaid, "svg": flow_svg, "ascii": flow_ascii},
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kind", nargs="?", choices=sorted(KINDS))
    ap.add_argument("--spec")
    ap.add_argument("--out")
    ap.add_argument("--format", default="mermaid", choices=["mermaid", "svg", "ascii"])
    ap.add_argument("--example", choices=sorted(EXAMPLES))
    args = ap.parse_args()

    if args.example:
        print(json.dumps(EXAMPLES[args.example], indent=2))
        return 0
    if not args.kind:
        ap.print_help(); return 2
    spec = (json.loads(Path(args.spec).read_text(encoding="utf-8"))
            if args.spec else EXAMPLES[args.kind])

    fmt = args.format
    if args.out:
        suffix = Path(args.out).suffix.lower()
        fmt = {".mmd": "mermaid", ".md": "mermaid", ".svg": "svg",
               ".txt": "ascii"}.get(suffix, fmt)
    if fmt == "svg" and args.kind == "prisma":
        print("PRISMA renders as Mermaid or ASCII only — the box-and-arrow SVG "
              "layout does it no favours. Falling back to Mermaid.", file=sys.stderr)
        fmt = "mermaid"

    body = KINDS[args.kind][fmt](spec)
    if fmt == "mermaid" and (not args.out or Path(args.out).suffix == ".md"):
        body = "```mermaid\n" + body + "```\n"

    if args.out:
        p = Path(args.out); p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
        print(f"Wrote {p} ({fmt})")
        if fmt == "mermaid":
            print("Mermaid renders natively on GitHub and in many agent runtimes. "
                  "Where it does not, the source is still readable.")
    else:
        print(body)

    if spec.get("divergence"):
        print("\nWhere practice diverges from the diagram — state this alongside it:",
              file=sys.stderr)
        for d in spec["divergence"]:
            print(f"  - {d}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
