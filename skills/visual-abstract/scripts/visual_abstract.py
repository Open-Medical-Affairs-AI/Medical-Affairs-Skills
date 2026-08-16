#!/usr/bin/env python3
"""Visual abstracts and icon arrays as dependency-free SVG.

A visual abstract travels without its paper, gets screenshotted, and is read in
three seconds by people who will never open the full text. That makes graphical
honesty a bigger obligation here than anywhere else, not a smaller one.

    S=skills/visual-abstract/scripts/visual_abstract.py
    python3 $S --example > va.json
    python3 $S --spec va.json --out abstract.svg
    python3 $S icon-array --n 100 --affected 8 --comparator 4 --out icons.svg

No dependencies.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from xml.sax.saxutils import escape

ACCENT, INK, MUTED, WARN = "#00518c", "#1a1a1a", "#5a5a5a", "#993300"
AFFECTED, WELL, COMP = "#D55E00", "#d8dde2", "#0072B2"

EXAMPLE = {
    "title": "NORVANTIB in triple-class-exposed relapsed/refractory myeloma",
    "design": "Single-arm, phase 1/2",
    "n": 168,
    "population": "Adults with RRMM and ≥4 prior lines, including a PI, an IMiD "
                  "and an anti-CD38 antibody",
    "intervention": "NORVANTIB weekly subcutaneously after step-up dosing",
    "findings": [
        {"label": "Overall response rate", "value": "62.5%", "ci": "95% CI 54.8–69.8",
         "absolute": "105 of 168 patients"},
        {"label": "Median duration of response", "value": "18.1 mo", "ci": "95% CI 14.2–NE",
         "absolute": "immature — 41% still in response at 24 months"},
    ],
    "safety": "Cytokine release syndrome 71.4% (grade ≥3: 0.6%); "
              "grade ≥3 infections 43.5%",
    "endpoint_note": "Response rate is a surrogate endpoint; it is not survival.",
    "limitation": "Single-arm — no comparative inference is available.",
    "caption": "SYNTHETIC EXAMPLE — not a real study or product.",
}


def _t(x, y, s, size=13, *, anchor="start", weight="normal", fill=INK):
    return (f'<text x="{x:.0f}" y="{y:.0f}" font-family="Helvetica,Arial,sans-serif" '
            f'font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" '
            f'fill="{fill}">{escape(str(s))}</text>')


def _wrap_text(x, y, text, size, width_chars, fill=INK, lh=None):
    import textwrap
    lh = lh or size * 1.35
    return "".join(_t(x, y + i * lh, line, size, fill=fill)
                   for i, line in enumerate(textwrap.wrap(str(text), width_chars)))


def abstract(spec: dict) -> str:
    comparative = spec.get("comparator") is not None
    single_arm = "single-arm" in str(spec.get("design", "")).lower()
    if comparative and single_arm:
        raise SystemExit(
            "This spec declares a single-arm design AND a comparator panel.\n"
            "Two panels side by side read as a comparison whatever the labels say, "
            "and a single-arm study has no counterfactual. Remove the comparator."
        )

    W, H = 1000, 620
    P = 44
    col = (W - 2 * P) / 3
    out = [f'<rect width="{W}" height="{H}" fill="white"/>',
           f'<rect x="0" y="0" width="{W}" height="6" fill="{ACCENT}"/>']
    out.append(_wrap_text(P, 52, spec["title"], 21, 62, ACCENT))
    # Design and N on the graphic itself — not in a caption that gets cropped.
    out.append(_t(P, 108, f'{spec["design"]} · n={spec["n"]}', 15, weight="bold"))

    y0 = 148
    for i, (head, body) in enumerate([
        ("POPULATION", spec.get("population", "")),
        ("INTERVENTION", spec.get("intervention", "")),
        ("KEY FINDING", ""),
    ]):
        x = P + i * col
        out.append(f'<line x1="{x}" y1="{y0}" x2="{x + col - 20}" y2="{y0}" '
                   f'stroke="{ACCENT}" stroke-width="2"/>')
        out.append(_t(x, y0 + 22, head, 12, weight="bold", fill=ACCENT))
        if body:
            out.append(_wrap_text(x, y0 + 46, body, 13, 34))

    f0 = spec["findings"][0]
    x = P + 2 * col
    out.append(_t(x, y0 + 62, f0["value"], 40, weight="bold", fill=ACCENT))
    out.append(_t(x, y0 + 86, f0.get("ci", ""), 12, fill=MUTED))
    out.append(_wrap_text(x, y0 + 108, f0["label"], 12.5, 30))
    if f0.get("absolute"):
        out.append(_wrap_text(x, y0 + 146, f0["absolute"], 12, 30, MUTED))

    y1 = 380
    out.append(f'<line x1="{P}" y1="{y1}" x2="{W-P}" y2="{y1}" stroke="#dcdcdc"/>')
    ry = y1 + 26
    for f in spec["findings"][1:]:
        out.append(_t(P, ry, f["label"] + ": ", 13, weight="bold"))
        out.append(_t(P + 250, ry, f'{f["value"]}  ({f.get("ci","")})', 13))
        if f.get("absolute"):
            out.append(_t(P + 250, ry + 17, f["absolute"], 11.5, fill=MUTED))
        ry += 46

    if spec.get("safety"):
        out.append(_t(P, ry + 6, "SAFETY", 12, weight="bold", fill=ACCENT))
        out.append(_wrap_text(P, ry + 26, spec["safety"], 12.5, 108))
        ry += 56

    for note in (spec.get("endpoint_note"), spec.get("limitation")):
        if note:
            out.append(_t(P, ry, note, 12, weight="bold", fill=WARN))
            ry += 20

    out.append(_t(P, H - 26, spec.get("caption", ""), 10, fill=MUTED))
    out.append(_t(W - P, H - 26, "DRAFT — REQUIRES QUALIFIED MEDICAL REVIEW", 10,
                  anchor="end", fill=WARN))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}">' + "".join(out) + "</svg>")


def icon_array(n: int, affected: int, comparator: int | None,
               labels: tuple[str, str] = ("Treatment", "Control")) -> str:
    per_row, r, gap = 10, 11, 30
    rows = (n + per_row - 1) // per_row
    panel_w = per_row * gap + 40
    W = panel_w * (2 if comparator is not None else 1) + 60
    H = rows * gap + 150

    def panel(x0, label, k):
        out = [_t(x0, 46, label, 15, weight="bold", fill=ACCENT),
               _t(x0, 70, f"{k} of {n}", 26, weight="bold", fill=AFFECTED)]
        for i in range(n):
            cx = x0 + (i % per_row) * gap + r
            cy = 100 + (i // per_row) * gap + r
            fill = AFFECTED if i < k else WELL
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r-2}" fill="{fill}"/>')
            if i < k:  # never colour alone
                out.append(f'<circle cx="{cx}" cy="{cy}" r="{r-2}" fill="none" '
                           f'stroke="{INK}" stroke-width="1.6"/>')
        return "".join(out)

    body = panel(30, labels[0], affected)
    if comparator is not None:
        body += panel(30 + panel_w, labels[1], comparator)
    body += _t(30, H - 20,
               "Each circle is one patient. Affected patients are filled and outlined "
               "— colour is never the only encoding.", 11, fill=MUTED)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="white"/>'
            + body + "</svg>")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    ia = sub.add_parser("icon-array")
    ia.add_argument("--n", type=int, default=100)
    ia.add_argument("--affected", type=int, required=True)
    ia.add_argument("--comparator", type=int)
    ia.add_argument("--labels", default="Treatment,Control")
    ia.add_argument("--out", default="icons.svg")
    ap.add_argument("--spec"); ap.add_argument("--out", default="abstract.svg")
    ap.add_argument("--example", action="store_true")
    args = ap.parse_args()

    if args.example:
        print(json.dumps(EXAMPLE, indent=2)); return 0
    if args.cmd == "icon-array":
        labels = tuple((args.labels.split(",") + ["Control"])[:2])
        svg = icon_array(args.n, args.affected, args.comparator, labels)
        p = Path(args.out); p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(svg, encoding="utf-8")
        print(f"Wrote {p}")
        print("Icon arrays communicate frequency to a non-specialist better than any "
              "sentence. Always give both arms with the same denominator.")
        return 0

    spec = (json.loads(Path(args.spec).read_text(encoding="utf-8"))
            if args.spec else EXAMPLE)
    for f in ("title", "design", "n", "findings"):
        if not spec.get(f):
            print(f"BLOCKED  missing '{f}' — the design and N must appear ON the "
                  f"graphic, not in a caption that gets cropped", file=sys.stderr)
            return 1
    p = Path(args.out); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(abstract(spec), encoding="utf-8")
    print(f"Wrote {p}")
    print("Check before release: design and N on the image · absolute alongside "
          "relative · denominator shown · endpoint type stated · safety visible · "
          "colour not the only encoding. Then run mlr-review-readiness.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
