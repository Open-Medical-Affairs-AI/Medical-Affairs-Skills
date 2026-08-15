#!/usr/bin/env python3
"""Clinical trial figures that follow the graphical integrity rules by default.

A figure is an argument, and most of the ways clinical figures mislead are
conventions people follow without noticing. This script bakes the rules in: it
refuses to truncate an efficacy y-axis, it will not render a survival curve
without numbers at risk, and it puts the denominator on every panel.

    S=skills/data-visualization-for-medical/scripts/clinical_figures.py

    python3 $S km        --example > km.json
    python3 $S km        --spec km.json      --out km.png
    python3 $S forest    --spec forest.json  --out forest.png
    python3 $S waterfall --spec wf.json      --out waterfall.png
    python3 $S ae        --spec ae.json      --out ae.png

Requires matplotlib:  pip install matplotlib
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Colour-blind-safe, and every series also gets a distinct line style or marker
# because colour must never be the only encoding.
PALETTE = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#56B4E9", "#E69F00"]
DASHES = ["-", "--", "-.", ":", (0, (3, 1, 1, 1)), (0, (5, 2))]
MARKERS = ["o", "s", "^", "D", "v", "P"]

EXAMPLES = {
    "km": {
        "title": "Progression-free survival",
        "subtitle": "Randomised, open-label, phase 3 (ITT)",
        "xlabel": "Months from randomisation",
        "ylabel": "Progression-free survival (%)",
        "risk_times": [0, 6, 12, 18, 24, 30],
        "arms": [
            {
                "label": "Investigational (n=280)",
                "times": [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30],
                "survival": [100, 92, 81, 70, 61, 54, 49, 45, 43, 42, 41],
                "at_risk": [280, 241, 198, 155, 112, 61],
                "censor_times": [14, 19, 23, 26, 29],
            },
            {
                "label": "Standard of care (n=278)",
                "times": [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30],
                "survival": [100, 85, 68, 53, 41, 33, 27, 23, 21, 20, 19],
                "at_risk": [278, 219, 160, 106, 63, 28],
                "censor_times": [16, 22, 28],
            },
        ],
        "annotation": (
            "Median PFS 20.4 mo (95% CI 17.1–24.8) vs 10.2 mo (8.9–12.4)\n"
            "HR 0.58 (95% CI 0.47–0.72); 341 events; median follow-up 26.3 mo\n"
            "Proportional hazards assumption not violated (Schoenfeld p=0.42)"
        ),
        "caption": "SYNTHETIC EXAMPLE DATA — not a real trial.",
    },
    "forest": {
        "title": "Progression-free survival by subgroup",
        "subtitle": "Pre-specified subgroups; interaction p-values shown",
        "xlabel": "Hazard ratio (95% CI)",
        "null_value": 1.0,
        "log_scale": True,
        "favours_left": "Favours investigational",
        "favours_right": "Favours control",
        "rows": [
            {"label": "Overall", "estimate": 0.58, "lower": 0.47, "upper": 0.72,
             "n": 558, "bold": True},
            {"label": "Age < 65", "estimate": 0.55, "lower": 0.41, "upper": 0.74, "n": 302},
            {"label": "Age ≥ 65", "estimate": 0.63, "lower": 0.45, "upper": 0.88,
             "n": 256, "interaction_p": 0.51},
            {"label": "ECOG 0", "estimate": 0.52, "lower": 0.38, "upper": 0.71, "n": 291},
            {"label": "ECOG 1", "estimate": 0.67, "lower": 0.49, "upper": 0.92,
             "n": 267, "interaction_p": 0.28},
            {"label": "High-risk cytogenetics", "estimate": 0.71, "lower": 0.48, "upper": 1.05,
             "n": 148},
            {"label": "Standard risk", "estimate": 0.53, "lower": 0.41, "upper": 0.69,
             "n": 410, "interaction_p": 0.14},
        ],
        "note": (
            "Subgroup analyses are hypothesis-generating unless pre-specified and\n"
            "adequately powered. No interaction test was significant."
        ),
        "caption": "SYNTHETIC EXAMPLE DATA — not a real trial.",
    },
    "waterfall": {
        "title": "Best percentage change in target lesion size",
        "subtitle": "Response-evaluable population",
        "ylabel": "Best change from baseline (%)",
        "thresholds": [{"value": -30, "label": "PR threshold (−30%)"},
                       {"value": 20, "label": "PD threshold (+20%)"}],
        "values": [-92, -88, -81, -76, -72, -68, -64, -61, -55, -51, -47, -44,
                   -39, -35, -32, -29, -24, -19, -14, -8, -3, 4, 11, 18, 27, 38],
        "n_enrolled": 34,
        "n_evaluable": 26,
        "exclusion_note": (
            "8 of 34 enrolled patients are not shown: 5 progressed or died before "
            "first assessment, 3 withdrew. Excluding them makes this figure more "
            "favourable than the enrolled population."
        ),
        "caption": "SYNTHETIC EXAMPLE DATA — not a real trial.",
    },
    "ae": {
        "title": "Adverse events occurring in ≥ 10% of patients",
        "subtitle": "Safety population (n=165)",
        "n": 165,
        "events": [
            {"term": "Cytokine release syndrome", "any_grade": 72.1, "grade3plus": 0.6},
            {"term": "Neutropenia", "any_grade": 70.9, "grade3plus": 64.2},
            {"term": "Anaemia", "any_grade": 52.1, "grade3plus": 37.0},
            {"term": "Pyrexia", "any_grade": 37.6, "grade3plus": 1.2},
            {"term": "Thrombocytopenia", "any_grade": 40.0, "grade3plus": 21.2},
            {"term": "Injection site reaction", "any_grade": 26.1, "grade3plus": 0.0},
            {"term": "Pneumonia", "any_grade": 18.2, "grade3plus": 12.7},
            {"term": "Diarrhoea", "any_grade": 15.8, "grade3plus": 1.8},
        ],
        "caption": "SYNTHETIC EXAMPLE DATA — not a real trial.",
    },
}


def _finish(fig, ax_or_none, spec, out: Path):
    import matplotlib.pyplot as plt

    caption = spec.get("caption", "")
    if caption:
        fig.text(0.01, 0.005, caption, fontsize=7, color="#555555", ha="left")
    fig.text(
        0.99, 0.005,
        "DRAFT — REQUIRES QUALIFIED MEDICAL REVIEW",
        fontsize=7, color="#993300", ha="right",
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def draw_km(spec: dict, out: Path) -> None:
    import matplotlib.pyplot as plt

    arms = spec["arms"]
    risk_times = spec["risk_times"]

    # Numbers at risk are not optional. The tail is where readers look and
    # where the data are thinnest; without this row the curve is uninterpretable.
    for arm in arms:
        if len(arm.get("at_risk", [])) != len(risk_times):
            raise SystemExit(
                f"Arm '{arm['label']}' has {len(arm.get('at_risk', []))} at-risk "
                f"values for {len(risk_times)} risk_times.\n"
                f"Every survival curve requires a complete numbers-at-risk row. "
                f"A KM plot without one cannot be interpreted."
            )

    n_arms = len(arms)
    fig, (ax, tbl) = plt.subplots(
        2, 1, figsize=(8, 6.4),
        gridspec_kw={"height_ratios": [4, 0.5 + 0.28 * n_arms], "hspace": 0.05},
    )

    for i, arm in enumerate(arms):
        colour = PALETTE[i % len(PALETTE)]
        ax.step(arm["times"], arm["survival"], where="post",
                color=colour, linestyle=DASHES[i % len(DASHES)],
                linewidth=2, label=arm["label"])
        # Censoring marks change how a curve should be read; hiding them hides that.
        for ct in arm.get("censor_times", []):
            surv = None
            for t, s in zip(arm["times"], arm["survival"]):
                if t <= ct:
                    surv = s
            if surv is not None:
                ax.plot(ct, surv, marker="|", color=colour, markersize=9,
                        markeredgewidth=1.6)

    ax.set_ylim(0, 100)  # never truncated
    ax.set_xlim(min(risk_times), max(risk_times))
    ax.set_ylabel(spec.get("ylabel", "Survival (%)"))
    ax.set_title(spec.get("title", ""), fontsize=13, fontweight="bold", loc="left", pad=24)
    if spec.get("subtitle"):
        ax.text(0, 1.02, spec["subtitle"], transform=ax.transAxes,
                fontsize=9, color="#555555")
    ax.grid(alpha=0.25, linewidth=0.6)
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.set_xticks(risk_times)
    ax.tick_params(labelbottom=False)

    if spec.get("annotation"):
        ax.text(0.02, 0.06, spec["annotation"], transform=ax.transAxes,
                fontsize=8.5, va="bottom",
                bbox={"facecolor": "white", "edgecolor": "#cccccc", "pad": 5})

    tbl.set_xlim(min(risk_times), max(risk_times))
    tbl.set_ylim(-1.6, n_arms + 0.6)
    tbl.axis("off")
    tbl.text(min(risk_times), n_arms + 0.15, "Number at risk",
             fontsize=9, fontweight="bold")
    for i, arm in enumerate(arms):
        y = n_arms - 1 - i
        colour = PALETTE[i % len(PALETTE)]
        for t, n in zip(risk_times, arm["at_risk"]):
            tbl.text(t, y, str(n), fontsize=8.5, ha="center", color=colour)
    for t in risk_times:
        tbl.text(t, -0.55, str(t), fontsize=9, ha="center")
    tbl.text((min(risk_times) + max(risk_times)) / 2, -1.25,
             spec.get("xlabel", "Time"), fontsize=10, ha="center")

    _finish(fig, ax, spec, out)


def draw_forest(spec: dict, out: Path) -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    rows = spec["rows"]
    n = len(rows)
    fig, ax = plt.subplots(figsize=(9, 0.45 * n + 2.2))

    ys = list(range(n - 1, -1, -1))
    for y, row in zip(ys, rows):
        est, lo, hi = row["estimate"], row["lower"], row["upper"]
        ax.plot([lo, hi], [y, y], color="#333333", linewidth=1.4)
        ax.plot([est], [y], marker="s" if row.get("bold") else "o",
                markersize=9 if row.get("bold") else 6,
                color=PALETTE[0] if row.get("bold") else "#333333")

    ax.axvline(spec.get("null_value", 1.0), color="#888888",
               linestyle="--", linewidth=1)
    if spec.get("log_scale"):
        from matplotlib.ticker import NullLocator, NullFormatter

        ax.set_xscale("log")
        ticks = spec.get("ticks") or [0.25, 0.5, 1.0, 2.0, 4.0]
        ax.set_xticks(ticks)
        ax.set_xticklabels([str(t) for t in ticks])
        # Log minor ticks collide with the labelled majors and make the axis
        # unreadable, which defeats the point of showing the scale at all.
        ax.xaxis.set_minor_locator(NullLocator())
        ax.xaxis.set_minor_formatter(NullFormatter())
        ax.set_xlim(min(ticks) * 0.9, max(ticks) * 1.1)

    ax.set_yticks(ys)
    ax.set_yticklabels(
        [f"{r['label']}  (n={r['n']})" if r.get("n") else r["label"] for r in rows],
        fontsize=9,
    )
    for tick, row in zip(ax.get_yticklabels(), rows):
        if row.get("bold"):
            tick.set_fontweight("bold")

    ax.set_xlabel(spec.get("xlabel", "Effect (95% CI)"))
    ax.set_title(spec.get("title", ""), fontsize=13, fontweight="bold", loc="left", pad=42)
    if spec.get("subtitle"):
        ax.text(0, 1.055, spec["subtitle"], transform=ax.transAxes,
                fontsize=9, color="#555555")

    xmax = ax.get_xlim()[1]
    for y, row in zip(ys, rows):
        txt = f"{row['estimate']:.2f} ({row['lower']:.2f}–{row['upper']:.2f})"
        if row.get("interaction_p") is not None:
            txt += f"   p(int)={row['interaction_p']:.2f}"
        ax.text(xmax * 1.05, y, txt, fontsize=8.5, va="center")

    # Place the directional labels relative to the null line so they always
    # sit on the correct side, whatever the scale.
    if spec.get("favours_left"):
        ax.text(0.02, 1.005, "← " + spec["favours_left"], transform=ax.transAxes,
                fontsize=8.5, color="#555555", va="bottom")
    if spec.get("favours_right"):
        ax.text(0.98, 1.005, spec["favours_right"] + " →", transform=ax.transAxes,
                fontsize=8.5, color="#555555", va="bottom", ha="right")
    if spec.get("note"):
        fig.text(0.02, -0.02, spec["note"], fontsize=8, color="#555555", va="top")

    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="x", alpha=0.2)
    _finish(fig, ax, spec, out)


def draw_waterfall(spec: dict, out: Path) -> None:
    import matplotlib.pyplot as plt

    values = sorted(spec["values"], reverse=True)
    fig, ax = plt.subplots(figsize=(9, 4.6))

    colours = []
    for v in values:
        if v <= -30:
            colours.append(PALETTE[2])
        elif v >= 20:
            colours.append(PALETTE[1])
        else:
            colours.append("#999999")

    ax.bar(range(len(values)), values, color=colours, edgecolor="white", linewidth=0.4)
    for th in spec.get("thresholds", []):
        ax.axhline(th["value"], color="#555555", linestyle="--", linewidth=1)
        ax.text(len(values) * 0.995, th["value"], "  " + th["label"],
                fontsize=8, va="bottom", ha="right", color="#555555")
    ax.axhline(0, color="#333333", linewidth=0.9)

    ax.set_ylabel(spec.get("ylabel", "Best change from baseline (%)"))
    ax.set_xlabel(f"Individual patients (n={spec.get('n_evaluable', len(values))})")
    ax.set_xticks([])
    ax.set_title(spec.get("title", ""), fontsize=13, fontweight="bold", loc="left", pad=24)
    if spec.get("subtitle"):
        ax.text(0, 1.02, spec["subtitle"], transform=ax.transAxes,
                fontsize=9, color="#555555")
    ax.spines[["top", "right"]].set_visible(False)

    # Waterfall plots routinely show only evaluable patients, which quietly
    # excludes those who progressed or died before assessment. Say so.
    note = spec.get("exclusion_note")
    if spec.get("n_enrolled") and spec.get("n_evaluable"):
        if spec["n_enrolled"] != spec["n_evaluable"] and not note:
            raise SystemExit(
                "n_enrolled differs from n_evaluable but no exclusion_note was "
                "given.\nA waterfall showing only evaluable patients is more "
                "favourable than the enrolled population. State who is excluded "
                "and why."
            )
    if note:
        ax.text(0, -0.22, note, transform=ax.transAxes, fontsize=8,
                color="#993300", va="top", wrap=True)

    _finish(fig, ax, spec, out)


def draw_ae(spec: dict, out: Path) -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    events = sorted(spec["events"], key=lambda e: e["any_grade"])
    terms = [e["term"] for e in events]
    any_g = [e["any_grade"] for e in events]
    g3 = [e["grade3plus"] for e in events]

    y = np.arange(len(terms))
    h = 0.38
    fig, ax = plt.subplots(figsize=(9, 0.5 * len(terms) + 2))

    # Paired bars rather than stacked: stacking makes the grade >=3 segment
    # hard to compare across rows, which is exactly the comparison that matters.
    ax.barh(y + h / 2, any_g, height=h, color=PALETTE[4], label="Any grade")
    ax.barh(y - h / 2, g3, height=h, color=PALETTE[1], hatch="//",
            edgecolor="white", label="Grade ≥ 3")

    for yi, v in zip(y + h / 2, any_g):
        ax.text(v + 0.8, yi, f"{v:.1f}%", va="center", fontsize=8)
    for yi, v in zip(y - h / 2, g3):
        ax.text(v + 0.8, yi, f"{v:.1f}%", va="center", fontsize=8)

    ax.set_yticks(y)
    ax.set_yticklabels(terms, fontsize=9)
    ax.set_xlabel(f"Patients (%), safety population n={spec['n']}")
    ax.set_xlim(0, max(any_g) * 1.18)
    ax.set_title(spec.get("title", ""), fontsize=13, fontweight="bold", loc="left", pad=24)
    if spec.get("subtitle"):
        ax.text(0, 1.02, spec["subtitle"], transform=ax.transAxes,
                fontsize=9, color="#555555")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", alpha=0.2)
    _finish(fig, ax, spec, out)


DRAWERS = {"km": draw_km, "forest": draw_forest,
           "waterfall": draw_waterfall, "ae": draw_ae}

CAPTION_NOTE = (
    "Caption requirement: state design, population, N, endpoint and its type,\n"
    "the effect measure, and the principal limitation. A figure that travels\n"
    "without its caption must still be interpretable."
)


def _have(module: str) -> bool:
    """Inline capability check, kept small so a copied directory still works.

    The full diagnostic lives in skills/capability-detection/.
    """
    try:
        __import__(module)
        return True
    except ImportError:
        return False


def render_svg_fallback(kind: str, spec: dict, out: Path) -> tuple[Path, Path]:
    """Tier 3: hand-written SVG plus the underlying data table.

    Imported lazily and by path so this script stays self-contained — the
    fallback module sits in the same directory.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import svg_fallback  # noqa: E402 — deliberate late import

    svg_path = out.with_suffix(".svg")
    tbl_path = out.with_suffix(".md")
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text(svg_fallback.RENDERERS[kind](spec), encoding="utf-8")
    tbl_path.write_text(svg_fallback.data_table(kind, spec), encoding="utf-8")
    return svg_path, tbl_path


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("kind", choices=sorted(DRAWERS))
    ap.add_argument("--spec")
    ap.add_argument("--out", default="figure.png")
    ap.add_argument("--example", action="store_true",
                    help="print a worked spec for this figure type")
    ap.add_argument("--force-svg", action="store_true",
                    help="use the dependency-free SVG renderer even if matplotlib "
                         "is available (SVG scales better for print and posters)")
    args = ap.parse_args()

    if args.example:
        print(json.dumps(EXAMPLES[args.kind], indent=2))
        return 0

    if not args.spec:
        ap.print_help()
        return 2
    path = Path(args.spec)
    if not path.exists():
        print(f"No such file: {path}", file=sys.stderr)
        return 2

    spec = json.loads(path.read_text(encoding="utf-8"))
    out = Path(args.out)

    if _have("matplotlib") and not args.force_svg:
        DRAWERS[args.kind](spec, out)
        print(f"Wrote {out}")
        print(CAPTION_NOTE)
        return 0

    # Tier 3. This is a success, not a failure — exit 0.
    try:
        svg_path, tbl_path = render_svg_fallback(args.kind, spec, out)
    except ValueError as exc:
        # An integrity rule failed. These hold in EVERY tier — a survival curve
        # without numbers at risk is misleading, not merely degraded.
        print(f"BLOCKED  {exc}", file=sys.stderr)
        return 1

    reason = ("--force-svg requested" if args.force_svg
              else "matplotlib is not available in this environment")
    print(f"""⚠ DEGRADED OUTPUT — {reason}.

   Delivered:      {svg_path}  (scalable vector, opens in any browser)
                   {tbl_path}  (the underlying numbers)
   Not delivered:  {out} (raster via matplotlib)
   To get it:      pip install matplotlib
                   python3 {Path(__file__).name} {args.kind} --spec {args.spec} --out {args.out}

   The content is complete. Every integrity rule still applies — the axis is
   not truncated, numbers at risk are present, denominators are shown. Only
   the rendering path changed.
""")
    print(CAPTION_NOTE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
