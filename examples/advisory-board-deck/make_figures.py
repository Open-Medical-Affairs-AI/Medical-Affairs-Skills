#!/usr/bin/env python3
"""Render the synthetic charts for the exemplar advisory-board deck.

All data is SYNTHETIC — invented for design demonstration. Every figure says
so in its source line, because a chart this polished would otherwise be
believed.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "skills/consulting-grade-design/scripts"))
import ma_theme
from ma_theme import INK, SLATE, TEAL, GOLD, OXBLOOD, CLOUD

import numpy as np

OUT = Path(__file__).resolve().parent / "figures"
SRC = "SYNTHETIC DATA — invented for design demonstration. Not a clinical result."

# 1 — KM-style curve with numbers at risk
fig, (ax, axn) = None, (None, None)
import matplotlib.pyplot as plt
ma_theme.apply()
fig = plt.figure(figsize=(11.5, 6.8))
gs = fig.add_gridspec(2, 1, height_ratios=[5, 1], hspace=0.05)
ax = fig.add_subplot(gs[0])
axn = fig.add_subplot(gs[1]); axn.set_axis_off()

t = np.linspace(0, 24, 200)
s1 = np.exp(-0.028 * t) * 100
s2 = np.exp(-0.052 * t) * 100
ax.step(t, s1, color=TEAL, lw=2.4)
ax.step(t, s2, color=SLATE, lw=2.4)
# censoring ticks
rng = np.random.default_rng(3)
for tt in rng.uniform(2, 23, 14):
    ax.plot(tt, np.exp(-0.028 * tt) * 100, marker="|", color=TEAL, ms=8)
for tt in rng.uniform(2, 20, 11):
    ax.plot(tt, np.exp(-0.052 * tt) * 100, marker="|", color=SLATE, ms=8)
ma_theme.direct_label(ax, 24, s1[-1], "NOVA-201 arm  51%", color=TEAL)
ma_theme.direct_label(ax, 24, s2[-1], "Historical control  29%", color=SLATE)
ax.set_xlim(0, 27.5); ax.set_ylim(0, 100)
ax.set_xlabel("Months from first dose"); ax.set_ylabel("Progression-free (%)")
ax.text(0.55, 12, "Median PFS 17.8 mo (95% CI 13.1–NE) vs 11.2 mo\nHR 0.58 (95% CI 0.41–0.82) — cross-study, hypothesis-generating only",
        fontsize=9.5, color=INK)
ma_theme.finish(ax, title="PFS separation emerges after month 3 and is sustained",
                kicker="SYNTHETIC EXAMPLE · SINGLE-ARM PHASE 2 (N=165) VS HISTORICAL CONTROL — NOT A RANDOMISED COMPARISON",
                source=SRC)
# numbers at risk
axn.text(-0.02, 0.75, "No. at risk", fontsize=9, fontweight="bold", color=INK, transform=axn.transAxes)
ticks = [0, 6, 12, 18, 24]
n1 = [165, 141, 118, 84, 41]; n2 = [165, 120, 88, 51, 20]
for x, a, b in zip(ticks, n1, n2):
    fx = x / 27.5
    axn.text(fx, 0.45, str(a), fontsize=9, color=TEAL, ha="center", transform=axn.transAxes)
    axn.text(fx, 0.10, str(b), fontsize=9, color=SLATE, ha="center", transform=axn.transAxes)
ma_theme.save(fig, OUT / "fig1_km.png"); print("fig1")

# 2 — Forest plot, subgroups
fig, ax = ma_theme.new_figure(10.5, 6.2)
groups = ["All patients", "Age <65", "Age ≥65", "ECOG 0–1", "ECOG 2",
          "Prior anti-CD38", "Penta-refractory", "High-risk cytogenetics"]
est = [0.58, 0.55, 0.62, 0.54, 0.81, 0.60, 0.72, 0.66]
lo  = [0.41, 0.36, 0.40, 0.38, 0.44, 0.41, 0.45, 0.39]
hi  = [0.82, 0.84, 0.96, 0.77, 1.49, 0.88, 1.15, 1.12]
y = np.arange(len(groups))[::-1]
for yi, e, l, h, g in zip(y, est, lo, hi, groups):
    c = INK if g == "All patients" else SLATE
    ax.plot([l, h], [yi, yi], color=c, lw=1.8)
    ax.plot(e, yi, "s", color=c, ms=9 if g == "All patients" else 6)
    ax.text(3.05, yi, f"{e:.2f} ({l:.2f}–{h:.2f})", fontsize=9.5, color=c, va="center")
ax.axvline(1.0, color=OXBLOOD, lw=1.2, ls="--")
ax.set_xscale("log"); ax.set_xlim(0.3, 3.0)
ax.set_xticks([0.5, 1.0, 2.0], ["0.5", "1.0", "2.0"])
ax.set_yticks(y, groups)
ax.grid(axis="x")
ax.text(0.31, -1.35, "◀ Favours NOVA-201", fontsize=9, color=TEAL)
ax.text(1.05, -1.35, "Favours control ▶", fontsize=9, color=SLATE)
ma_theme.finish(ax, title="Effect is consistent across subgroups; ECOG 2 is uninformative, not discordant",
                kicker="SYNTHETIC EXAMPLE · INTERACTION P=0.41 — SUBGROUPS HYPOTHESIS-GENERATING ONLY",
                source=SRC)
ma_theme.save(fig, OUT / "fig2_forest.png"); print("fig2")

# 3 — AE profile paired bars
fig, ax = ma_theme.new_figure(10.5, 6.0)
aes = ["CRS", "Neutropenia", "Anaemia", "Infections", "ICANS", "Fatigue", "Diarrhoea"]
anyg = [76, 64, 52, 47, 9, 41, 33]
g3   = [2, 46, 31, 21, 1, 4, 2]
ypos = np.arange(len(aes))[::-1]
ax.barh(ypos + 0.19, anyg, height=0.36, color=CLOUD, edgecolor=SLATE, lw=0.7, label="Any grade")
ax.barh(ypos - 0.19, g3, height=0.36, color=OXBLOOD, label="Grade ≥3")
for yi, a, g in zip(ypos, anyg, g3):
    ax.text(a + 1, yi + 0.19, f"{a}%", fontsize=9, color=SLATE, va="center")
    ax.text(g + 1, yi - 0.19, f"{g}%", fontsize=9, color=OXBLOOD, va="center", fontweight="bold")
ax.set_yticks(ypos, aes); ax.set_xlim(0, 90)
ax.set_xlabel("Patients (%) · N=165 · treatment-emergent")
ax.grid(axis="x"); ax.legend(loc="lower right")
ma_theme.finish(ax, title="Cytopenias carry the grade ≥3 burden; CRS is frequent but low-grade",
                kicker="SYNTHETIC EXAMPLE · SINGLE-ARM PHASE 2 · SAFETY-EVALUABLE POPULATION (N=165)",
                source=SRC)
ma_theme.save(fig, OUT / "fig3_ae.png"); print("fig3")

# 4 — Evidence gap / investment slope
fig, ax = ma_theme.new_figure(10.5, 5.8)
cats = ["Randomised\ncomparison", "Sequencing after\nBCMA exposure", "Real-world\neffectiveness", "Long-term\nsafety", "PRO / QoL"]
now  = [0, 1, 2, 1, 1]
target = [3, 3, 3, 2, 2]
x = np.arange(len(cats))
ax.bar(x - 0.17, now, width=0.34, color=SLATE, label="Evidence today")
ax.bar(x + 0.17, target, width=0.34, color=TEAL, label="Needed for guideline inclusion")
ax.set_xticks(x, cats, fontsize=9.5)
ax.set_yticks([0, 1, 2, 3], ["None", "Emerging", "Moderate", "Robust"])
ax.legend(loc="upper right")
ma_theme.finish(ax, title="The randomised comparison is the binding constraint on every downstream ambition",
                kicker="SYNTHETIC EXAMPLE · INTERNAL EVIDENCE-MATURITY ASSESSMENT, 4-LEVEL ORDINAL SCALE",
                source=SRC)
ma_theme.save(fig, OUT / "fig4_gaps.png"); print("fig4")
