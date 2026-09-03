#!/usr/bin/env python3
"""Render the library menu card — every skill, grouped by job, one page.

Reads each skill's frontmatter (name + tier) from skills/*/SKILL.md and lays
the library out as a menu in the consulting-grade-design palette. SVG is
written natively by matplotlib; a PNG sibling is written for READMEs.

    python3 menu_card.py --out assets/menu-card.svg

Degrades, never fails: without matplotlib it writes a markdown menu next to
the requested path and exits 0, stating what was delivered and how to get
the graphic.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SKILLS = REPO / "skills"

# Palette (mirrors ma_theme.py; duplicated so the directory is portable).
INK = "#12283A"
SLATE = "#5B6B79"
TEAL = "#0E7C7B"
GOLD = "#C89B3C"
OXBLOOD = "#8C2F39"
CLOUD = "#E8ECEF"
PAPER = "#FBFBF9"

# The menu groups. A skill listed nowhere lands in "Foundations & retrieval"
# so a new skill can never silently vanish from the card.
GROUPS: list[tuple[str, str, list[str]]] = [
    ("Understand what you have", TEAL, [
        "document-ingestion", "field-insight-synthesis", "insight-generation",
        "spreadsheet-analysis", "evidence-synthesis", "evidence-appraisal",
        "medical-terminology-mapping",
    ]),
    ("Prepare for the moment", INK, [
        "kol-engagement-brief", "congress-intelligence",
        "competitive-intelligence", "launch-medical-readiness",
        "congress-abstract-and-poster",
    ]),
    ("Build the plan", INK, [
        "medical-strategy-plan", "integrated-evidence-plan",
        "evidence-gap-analysis", "scientific-communication-strategy",
        "scientific-platform", "field-medical-planning",
        "medical-education-program", "medical-affairs-metrics",
        "strategic-analysis",
    ]),
    ("Design the study or event", TEAL, [
        "real-world-evidence-design", "advisory-board-design",
        "investigator-initiated-study-review", "guideline-engagement",
        "systematic-literature-review",
    ]),
    ("Answer the question", INK, [
        "medical-information-response", "payer-value-dossier",
        "safety-communication", "regulatory-label-intelligence",
        "medical-correspondence", "promotional-material-medical-review",
        "mlr-review-readiness",
    ]),
    ("Produce the artefact", GOLD, [
        "medical-slide-deck", "scientific-manuscript", "executive-briefing",
        "plain-language-summary", "visual-abstract",
        "data-visualization-for-medical", "interactive-html-report",
        "pdf-generation", "diagram-and-schema", "consulting-grade-design",
    ]),
    ("Keep watch", OXBLOOD, [
        "literature-surveillance",
    ]),
    ("Foundations & retrieval", SLATE, [
        "medical-affairs-orchestrator", "medical-affairs-foundations",
        "citation-integrity", "deliverable-quality-review",
        "capability-detection", "pubmed-search", "clinical-trials-search",
        "library-menu",
    ]),
]


def discover() -> list[str]:
    names = []
    for d in sorted(SKILLS.iterdir()):
        if (d / "SKILL.md").exists():
            names.append(d.name)
    return names


def grouped(names: list[str]):
    placed: set[str] = set()
    out = []
    for title, colour, members in GROUPS:
        present = [m for m in members if m in names]
        placed.update(present)
        out.append((title, colour, present))
    leftovers = [n for n in names if n not in placed]
    if leftovers:
        title, colour, members = out[-1]
        out[-1] = (title, colour, members + leftovers)
    return out


def render_markdown(names: list[str], out: Path) -> Path:
    md = out.with_suffix(".md")
    lines = [f"# Medical Affairs Skills — menu ({len(names)} skills, {date.today()})", ""]
    for title, _c, members in grouped(names):
        if not members:
            continue
        lines.append(f"## {title}")
        lines += [f"- `{m}`" for m in members] + [""]
    md.write_text("\n".join(lines), encoding="utf-8")
    return md


def render_card(names: list[str], out: Path) -> list[Path]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch

    groups = [g for g in grouped(names) if g[2]]

    # Two-column layout, groups flowing down each column.
    fig_w, fig_h = 14, 15
    fig = plt.figure(figsize=(fig_w, fig_h), facecolor=PAPER)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    # Header
    ax.text(0.05, 0.965, "MEDICAL AFFAIRS SKILLS", fontsize=13, color=TEAL,
            fontweight="bold", family="sans-serif")
    ax.text(0.05, 0.935, "The library, as a menu", fontsize=30, color=INK,
            fontweight="bold", family="serif")
    ax.text(0.05, 0.912,
            f"{len(names)} skills · open source · Apache-2.0 · works with any agent · "
            f"generated {date.today():%d %b %Y}",
            fontsize=10.5, color=SLATE)
    ax.plot([0.05, 0.95], [0.9, 0.9], color=INK, lw=1.4)

    # Flow groups into two columns
    col_x = [0.05, 0.525]
    col_w = 0.425
    y_top = 0.875
    line_h = 0.0148       # per skill row
    head_h = 0.030        # group header
    pad = 0.016

    heights = [head_h + line_h * len(m) + pad for _t, _c, m in groups]
    # balance columns greedily in order
    col_y = [y_top, y_top]
    assign = []
    total = sum(heights)
    running = 0.0
    for g, h in zip(groups, heights):
        col = 0 if running < total / 2 else 1
        assign.append((g, col))
        running += h

    for (title, colour, members), col in assign:
        x = col_x[col]
        y = col_y[col]
        # group header
        ax.add_patch(FancyBboxPatch((x, y - 0.006), col_w, 0.024,
                                    boxstyle="round,pad=0.002,rounding_size=0.004",
                                    linewidth=0, facecolor=colour, alpha=0.10))
        ax.plot([x, x], [y - 0.006, y + 0.018], color=colour, lw=3,
                solid_capstyle="butt")
        ax.text(x + 0.012, y, title.upper(), fontsize=11.5, color=colour,
                fontweight="bold", va="bottom")
        y -= head_h
        for m in members:
            ax.plot([x + 0.014], [y + 0.004], marker="o", markersize=2.6,
                    color=colour)
            ax.text(x + 0.028, y, m, fontsize=10.3, color=INK,
                    family="monospace")
            y -= line_h
        y -= pad
        col_y[col] = y

    # Footer
    foot_y = min(col_y) - 0.01
    ax.plot([0.05, 0.95], [foot_y, foot_y], color=CLOUD, lw=1.2)
    ax.text(0.05, foot_y - 0.018,
            "Hand the agent a job, not a skill name — the orchestrator routes it. "
            "Every deliverable ships with provenance, verified citations and its draft marking.",
            fontsize=10, color=SLATE, style="italic")
    ax.text(0.05, foot_y - 0.036,
            "DRAFT OUTPUTS — ALL ARTEFACTS REQUIRE QUALIFIED MEDICAL REVIEW",
            fontsize=9, color=OXBLOOD, fontweight="bold")

    out.parent.mkdir(parents=True, exist_ok=True)
    written = []
    for target in (out, out.with_suffix(".png")):
        fig.savefig(target, facecolor=PAPER, bbox_inches="tight", dpi=180)
        written.append(target)
    plt.close(fig)
    return written


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="assets/menu-card.svg")
    args = ap.parse_args()
    out = Path(args.out)

    names = discover()
    if not names:
        print("No skills found — is this script inside the repository?", file=sys.stderr)
        return 2

    try:
        import matplotlib  # noqa: F401
    except ImportError:
        md = render_markdown(names, out)
        print(f"""⚠ DEGRADED OUTPUT — matplotlib is not available in this environment.

   Delivered:      {md}   (the menu as markdown, all {len(names)} skills)
   Not delivered:  {out}
   To get it:      pip install matplotlib
                   python3 {Path(__file__).name} --out {out}

   The grouping and every skill name survived; only the graphic was lost.
""")
        return 0

    for p in render_card(names, out):
        print(f"Wrote {p}")
    print(f"{len(names)} skills on the card. Regenerate whenever a skill is added or removed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
