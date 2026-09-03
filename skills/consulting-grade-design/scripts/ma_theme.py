#!/usr/bin/env python3
"""The library's shared visual language for charts, applied to matplotlib.

Every figure a Medical Affairs deliverable carries should look like it came
from the same expensive advisory firm: one palette, one type scale, generous
white space, horizontal gridlines only, direct labels instead of legends where
the data allow, and a source line under every chart.

This module is self-contained (matplotlib only) so a copied skill directory
still works. It never blocks content: if matplotlib is missing, importing
fails loudly and the calling skill degrades to its next tier as usual.

Usage from any figure-producing script or agent-written code:

    import sys; sys.path.insert(0, "skills/consulting-grade-design/scripts")
    import ma_theme
    ma_theme.apply()                       # global rcParams
    fig, ax = ma_theme.new_figure()        # 16:9, themed
    ...
    ma_theme.finish(ax, title="ORR by line of therapy",
                    kicker="SINGLE-ARM PHASE 2 · N=165",
                    source="Example A, et al. J Example Med 2024. PMID 00000000")
    ma_theme.save(fig, "orr.png")

Demo gallery (renders sample charts with synthetic data):

    python3 ma_theme.py --gallery out_dir/
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

# ---------------------------------------------------------------------------
# Palette — restrained, print-safe, colour-blind aware.
# INK anchors everything; one accent at a time; safety data always in OXBLOOD.
# ---------------------------------------------------------------------------
INK = "#12283A"        # deep navy — titles, primary series
SLATE = "#5B6B79"      # secondary text, axes, muted series
TEAL = "#0E7C7B"       # the accent — one per figure, used to point
GOLD = "#C89B3C"       # highlights, callouts (sparingly)
OXBLOOD = "#8C2F39"    # safety findings, warnings — reserved
CLOUD = "#E8ECEF"      # gridlines, fills
PAPER = "#FFFFFF"      # figure background (white; decks supply their own)

# Categorical sequence for study arms / groups. Position + direct labels carry
# the encoding; colour is never the only channel (8% of men are CVD).
ARMS = [INK, TEAL, GOLD, SLATE, "#7A9CB8", OXBLOOD]

SERIF = "Georgia, 'Times New Roman', serif"
SANS_STACK = ["DejaVu Sans", "Arial", "Helvetica"]


def apply() -> None:
    """Set global rcParams. Call once before plotting."""
    plt.rcParams.update({
        "figure.facecolor": PAPER,
        "axes.facecolor": PAPER,
        "savefig.facecolor": PAPER,
        "font.family": "sans-serif",
        "font.sans-serif": SANS_STACK,
        "text.color": INK,
        "axes.edgecolor": SLATE,
        "axes.labelcolor": SLATE,
        "axes.titlecolor": INK,
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,          # y carried by gridlines
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": CLOUD,
        "grid.linewidth": 0.8,
        "xtick.color": SLATE,
        "ytick.color": SLATE,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "axes.labelsize": 11,
        "legend.frameon": False,
        "legend.fontsize": 10,
        "lines.linewidth": 2.2,
        "figure.dpi": 200,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.25,
    })


def new_figure(width: float = 11.5, height: float = 6.0):
    """A 16:9-ish canvas sized for a deck's chart area."""
    apply()
    fig, ax = plt.subplots(figsize=(width, height))
    return fig, ax


def finish(ax, *, title: str = "", kicker: str = "", source: str = "",
           note: str = "") -> None:
    """Stamp the editorial furniture: kicker, message title, source line.

    The title is a finding, not a topic — "Grade ≥3 CRS remained under 1%",
    not "Safety results". The kicker carries design and N, because a chart
    that travels without its caption must still name its design.
    """
    fig = ax.get_figure()
    y = 1.02
    if title:
        ax.set_title(title, fontsize=15, fontweight="bold", loc="left",
                     color=INK, pad=18)
    if kicker:
        ax.text(0, 1.06, kicker.upper(), transform=ax.transAxes,
                fontsize=9, color=TEAL, fontweight="bold")
    footer = " · ".join(x for x in [source, note] if x)
    if footer:
        fig.text(0.01, -0.02, footer, fontsize=8, color=SLATE, ha="left")


def direct_label(ax, x, y, text, color=INK, dx=6, dy=0) -> None:
    """Label a series at its end point instead of using a legend."""
    ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points",
                fontsize=10, fontweight="bold", color=color, va="center")


def save(fig, path) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    plt.close(fig)
    return out


# ---------------------------------------------------------------------------
# Gallery — synthetic-data samples proving the look. Never real data.
# ---------------------------------------------------------------------------

def _gallery(outdir: Path) -> list[Path]:
    import numpy as np
    rng = np.random.default_rng(7)
    written = []

    # 1 — bar chart with direct value labels, zero-based axis
    fig, ax = new_figure(9, 5)
    cats = ["1L", "2L", "3L", "4L+"]
    vals = [71, 58, 44, 29]
    bars = ax.bar(cats, vals, color=[SLATE, SLATE, TEAL, SLATE], width=0.62)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v}%",
                ha="center", fontsize=11, fontweight="bold", color=INK)
    ax.set_ylim(0, 80)
    ax.set_ylabel("ORR (%)")
    finish(ax, title="Response attenuates by line — the 3L window is where the question lives",
           kicker="Synthetic data · illustrative only",
           source="SYNTHETIC DATA — design demonstration, not a clinical result")
    written.append(save(fig, outdir / "gallery_bar.png"))

    # 2 — slope chart (before/after), direct labels, no legend
    fig, ax = new_figure(8, 5.5)
    groups = [("Anti-CD38 exposed", 62, 48, SLATE),
              ("Triple-class exposed", 55, 34, TEAL),
              ("Penta-exposed", 41, 22, OXBLOOD)]
    for name, a, b, c in groups:
        ax.plot([0, 1], [a, b], color=c, marker="o", markersize=5)
        direct_label(ax, 1, b, f"{name}  {b}%", color=c)
    ax.set_xlim(-0.1, 1.9)
    ax.set_xticks([0, 1], ["2023", "2026"])
    ax.set_ylabel("Median PFS proxy (%)")
    finish(ax, title="The exposed populations are where outcomes moved",
           kicker="Synthetic data · illustrative only",
           source="SYNTHETIC DATA — design demonstration, not a clinical result")
    written.append(save(fig, outdir / "gallery_slope.png"))

    # 3 — horizontal AE bars, paired any-grade vs grade ≥3
    fig, ax = new_figure(9, 5.5)
    aes = ["CRS", "Neutropenia", "Infections", "ICANS", "Fatigue"]
    anyg = [72, 51, 45, 10, 38]
    g3 = [1, 33, 19, 2, 3]
    ypos = range(len(aes))[::-1]
    ax.barh([y + 0.18 for y in ypos], anyg, height=0.34, color=CLOUD,
            edgecolor=SLATE, linewidth=0.6, label="Any grade")
    ax.barh([y - 0.18 for y in ypos], g3, height=0.34, color=OXBLOOD,
            label="Grade ≥3")
    ax.set_yticks(list(ypos), aes)
    ax.set_xlabel("Patients (%)  ·  N=165")
    ax.grid(axis="x")
    ax.legend(loc="lower right")
    finish(ax, title="Cytopenias, not CRS, carry the grade ≥3 burden",
           kicker="Synthetic data · illustrative only",
           source="SYNTHETIC DATA — design demonstration, not a clinical result")
    written.append(save(fig, outdir / "gallery_ae.png"))

    return written


def main() -> int:
    if len(sys.argv) >= 2 and sys.argv[1] == "--gallery":
        outdir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("gallery")
        for p in _gallery(outdir):
            print(f"Wrote {p}")
        return 0
    print(__doc__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
