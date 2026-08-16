#!/usr/bin/env python3
"""Tier-3 SVG renderers for clinical figures — no matplotlib, no dependencies.

A Kaplan-Meier curve is a set of line segments. A forest plot is lines and
circles. A waterfall is rectangles. None of that needs a plotting library, and
SVG scales perfectly and opens in every browser.

This is not a consolation prize. For the figure types Medical Affairs actually
uses, hand-written SVG loses essentially nothing.

The integrity rules are enforced here exactly as they are in the matplotlib
path: axes are not truncated, numbers at risk are mandatory on a survival curve,
denominators are shown. A fallback that dropped those would not be a degraded
figure, it would be a misleading one.
"""

from __future__ import annotations

from xml.sax.saxutils import escape

PALETTE = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#56B4E9", "#E69F00"]
DASH = ["", "8,4", "12,3,3,3", "2,3", "14,4,2,4", "6,2"]
INK, MUTED, WARN = "#1a1a1a", "#555555", "#993300"


def _t(x, y, s, size=12, *, anchor="start", weight="normal", fill=INK):
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Helvetica,Arial,sans-serif" '
        f'font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" '
        f'fill="{fill}">{escape(str(s))}</text>'
    )


def _wrap(body: str, w: int, h: int, title: str, caption: str) -> str:
    foot = []
    if caption:
        foot.append(_t(10, h - 16, caption, 10, fill=MUTED))
    foot.append(_t(w - 10, h - 16, "DRAFT — REQUIRES QUALIFIED MEDICAL REVIEW",
                   10, anchor="end", fill=WARN))
    foot.append(_t(w - 10, h - 4,
                   "Rendered without matplotlib (tier 3). Content complete.",
                   9, anchor="end", fill=MUTED))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">'
        f'<rect width="{w}" height="{h}" fill="white"/>'
        + body + "".join(foot) + "</svg>"
    )


def km(spec: dict) -> str:
    """Kaplan-Meier curve with a mandatory numbers-at-risk row."""
    arms = spec["arms"]
    risk_times = spec["risk_times"]
    for arm in arms:
        if len(arm.get("at_risk", [])) != len(risk_times):
            raise ValueError(
                f"Arm '{arm.get('label')}' has an incomplete numbers-at-risk row. "
                f"A survival curve without one cannot be interpreted, so it is "
                f"not rendered in any tier."
            )

    W, H = 860, 640
    L, R, T = 90, 40, 80
    plot_h = 380
    B = T + plot_h
    pw = W - L - R
    t0, t1 = min(risk_times), max(risk_times)

    def px(t):
        return L + (t - t0) / (t1 - t0) * pw

    def py(s):
        return B - (s / 100.0) * plot_h  # y always 0-100, never truncated

    out = [
        _t(L, 32, spec.get("title", ""), 17, weight="bold"),
        _t(L, 52, spec.get("subtitle", ""), 11, fill=MUTED),
    ]

    # axes + gridlines
    out.append(f'<line x1="{L}" y1="{T}" x2="{L}" y2="{B}" stroke="#333" stroke-width="1"/>')
    out.append(f'<line x1="{L}" y1="{B}" x2="{W-R}" y2="{B}" stroke="#333" stroke-width="1"/>')
    for v in (0, 20, 40, 60, 80, 100):
        y = py(v)
        out.append(f'<line x1="{L}" y1="{y:.1f}" x2="{W-R}" y2="{y:.1f}" '
                   f'stroke="#e8e8e8" stroke-width="1"/>')
        out.append(_t(L - 8, y + 4, v, 11, anchor="end"))
    for t in risk_times:
        out.append(_t(px(t), B + 18, t, 11, anchor="middle"))

    out.append(
        f'<text x="26" y="{T + plot_h/2:.0f}" font-family="Helvetica,Arial,sans-serif" '
        f'font-size="12" text-anchor="middle" fill="{INK}" '
        f'transform="rotate(-90 26 {T + plot_h/2:.0f})">'
        f'{escape(spec.get("ylabel", "Survival (%)"))}</text>'
    )

    # step curves
    for i, arm in enumerate(arms):
        colour = PALETTE[i % len(PALETTE)]
        dash = DASH[i % len(DASH)]
        pts = []
        prev_y = None
        for t, s in zip(arm["times"], arm["survival"]):
            x, y = px(t), py(s)
            if prev_y is not None:
                pts.append(f"L{x:.1f},{prev_y:.1f}")
            pts.append(f"{'M' if prev_y is None else 'L'}{x:.1f},{y:.1f}")
            prev_y = y
        da = f' stroke-dasharray="{dash}"' if dash else ""
        out.append(f'<path d="{" ".join(pts)}" fill="none" stroke="{colour}" '
                   f'stroke-width="2.2"{da}/>')

        # censoring marks — omitting them changes how a curve should be read
        for ct in arm.get("censor_times", []):
            s = None
            for t, v in zip(arm["times"], arm["survival"]):
                if t <= ct:
                    s = v
            if s is not None:
                x, y = px(ct), py(s)
                out.append(f'<line x1="{x:.1f}" y1="{y-5:.1f}" x2="{x:.1f}" '
                           f'y2="{y+5:.1f}" stroke="{colour}" stroke-width="1.8"/>')

        out.append(f'<line x1="{W-R-190}" y1="{T+14+i*18}" x2="{W-R-160}" '
                   f'y2="{T+14+i*18}" stroke="{colour}" stroke-width="2.2"'
                   + (f' stroke-dasharray="{dash}"' if dash else "") + "/>")
        out.append(_t(W - R - 154, T + 18 + i * 18, arm["label"], 11))

    if spec.get("annotation"):
        for j, line in enumerate(str(spec["annotation"]).split("\n")):
            out.append(_t(L + 12, B - 58 + j * 14, line, 10.5))

    # numbers at risk — mandatory
    ny = B + 52
    out.append(_t(L, ny, "Number at risk", 12, weight="bold"))
    for i, arm in enumerate(arms):
        colour = PALETTE[i % len(PALETTE)]
        y = ny + 22 + i * 20
        for t, n in zip(risk_times, arm["at_risk"]):
            out.append(_t(px(t), y, n, 11, anchor="middle", fill=colour))
    out.append(_t(L + pw / 2, ny + 32 + len(arms) * 20,
                  spec.get("xlabel", "Time"), 12, anchor="middle"))

    return _wrap("".join(out), W, H, spec.get("title", ""), spec.get("caption", ""))


def forest(spec: dict) -> str:
    import math

    rows = spec["rows"]
    W = 980
    row_h = 30
    T = 88
    H = T + row_h * len(rows) + 110
    L, R = 300, 300
    pw = W - L - R
    lo = min(r["lower"] for r in rows) * 0.85
    hi = max(r["upper"] for r in rows) * 1.15
    log = spec.get("log_scale", True)

    def px(v):
        v = max(v, 1e-6)
        if log:
            return L + (math.log(v) - math.log(lo)) / (math.log(hi) - math.log(lo)) * pw
        return L + (v - lo) / (hi - lo) * pw

    out = [
        _t(20, 32, spec.get("title", ""), 17, weight="bold"),
        _t(20, 52, spec.get("subtitle", ""), 11, fill=MUTED),
        _t(L, 72, "← " + spec.get("favours_left", ""), 10, fill=MUTED),
        _t(L + pw, 72, spec.get("favours_right", "") + " →", 10, anchor="end", fill=MUTED),
    ]

    null_x = px(spec.get("null_value", 1.0))
    out.append(f'<line x1="{null_x:.1f}" y1="{T-6}" x2="{null_x:.1f}" '
               f'y2="{T + row_h*len(rows)}" stroke="#888" stroke-width="1" '
               f'stroke-dasharray="5,4"/>')

    for i, r in enumerate(rows):
        y = T + i * row_h + row_h / 2
        weight = "bold" if r.get("bold") else "normal"
        label = r["label"] + (f"  (n={r['n']})" if r.get("n") else "")
        out.append(_t(L - 16, y + 4, label, 11.5, anchor="end", weight=weight))
        out.append(f'<line x1="{px(r["lower"]):.1f}" y1="{y:.1f}" '
                   f'x2="{px(r["upper"]):.1f}" y2="{y:.1f}" stroke="#333" stroke-width="1.4"/>')
        for end in ("lower", "upper"):
            x = px(r[end])
            out.append(f'<line x1="{x:.1f}" y1="{y-4:.1f}" x2="{x:.1f}" y2="{y+4:.1f}" '
                       f'stroke="#333" stroke-width="1.4"/>')
        cx = px(r["estimate"])
        if r.get("bold"):
            out.append(f'<rect x="{cx-6:.1f}" y="{y-6:.1f}" width="12" height="12" '
                       f'fill="{PALETTE[0]}"/>')
        else:
            out.append(f'<circle cx="{cx:.1f}" cy="{y:.1f}" r="4.5" fill="#333"/>')
        txt = f'{r["estimate"]:.2f} ({r["lower"]:.2f}–{r["upper"]:.2f})'
        if r.get("interaction_p") is not None:
            txt += f'   p(int)={r["interaction_p"]:.2f}'
        out.append(_t(L + pw + 18, y + 4, txt, 10.5))

    ay = T + row_h * len(rows) + 6
    out.append(f'<line x1="{L}" y1="{ay}" x2="{L+pw}" y2="{ay}" stroke="#333"/>')
    ticks = spec.get("ticks") or [0.25, 0.5, 1.0, 2.0, 4.0]
    for t in ticks:
        if lo <= t <= hi:
            out.append(_t(px(t), ay + 18, t, 11, anchor="middle"))
    out.append(_t(L + pw / 2, ay + 40, spec.get("xlabel", "Effect (95% CI)"),
                  12, anchor="middle"))
    if spec.get("note"):
        for j, line in enumerate(str(spec["note"]).split("\n")):
            out.append(_t(20, ay + 62 + j * 13, line, 10, fill=MUTED))

    return _wrap("".join(out), W, H, spec.get("title", ""), spec.get("caption", ""))


def waterfall(spec: dict) -> str:
    values = sorted(spec["values"], reverse=True)
    W, H = 900, 470
    L, R, T = 80, 30, 80
    ph = 250
    zero_frac = max(values + [0]) / (max(values + [0]) - min(values + [0]) or 1)
    zero_y = T + ph * zero_frac
    pw = W - L - R
    bw = pw / max(len(values), 1)
    span = (max(values + [0]) - min(values + [0])) or 1

    out = [
        _t(L, 32, spec.get("title", ""), 17, weight="bold"),
        _t(L, 52, spec.get("subtitle", ""), 11, fill=MUTED),
    ]
    for i, v in enumerate(values):
        h = abs(v) / span * ph
        y = zero_y - h if v > 0 else zero_y
        colour = PALETTE[2] if v <= -30 else (PALETTE[1] if v >= 20 else "#999999")
        out.append(f'<rect x="{L + i*bw:.1f}" y="{y:.1f}" width="{max(bw-1.2,1):.1f}" '
                   f'height="{h:.1f}" fill="{colour}"/>')
    for th in spec.get("thresholds", []):
        y = zero_y - (th["value"] / span * ph)
        out.append(f'<line x1="{L}" y1="{y:.1f}" x2="{L+pw}" y2="{y:.1f}" '
                   f'stroke="#555" stroke-width="1" stroke-dasharray="5,4"/>')
        out.append(_t(L + pw, y - 4, th["label"], 10, anchor="end", fill=MUTED))
    out.append(f'<line x1="{L}" y1="{zero_y:.1f}" x2="{L+pw}" y2="{zero_y:.1f}" stroke="#333"/>')

    n_eval = spec.get("n_evaluable", len(values))
    out.append(_t(L + pw / 2, T + ph + 46, f"Individual patients (n={n_eval})",
                  12, anchor="middle"))
    out.append(
        f'<text x="24" y="{T + ph/2:.0f}" font-family="Helvetica,Arial,sans-serif" '
        f'font-size="12" text-anchor="middle" fill="{INK}" '
        f'transform="rotate(-90 24 {T + ph/2:.0f})">'
        f'{escape(spec.get("ylabel", "Best change from baseline (%)"))}</text>'
    )
    note = spec.get("exclusion_note")
    if spec.get("n_enrolled") and n_eval != spec.get("n_enrolled") and not note:
        raise ValueError(
            "n_enrolled differs from n_evaluable but no exclusion_note was given. "
            "A waterfall showing only evaluable patients is more favourable than "
            "the enrolled population; the exclusion must be stated in every tier."
        )
    if note:
        import textwrap
        for j, line in enumerate(textwrap.wrap(note, 110)):
            out.append(_t(L, T + ph + 74 + j * 13, line, 10, fill=WARN))

    return _wrap("".join(out), W, H, spec.get("title", ""), spec.get("caption", ""))


def ae(spec: dict) -> str:
    events = sorted(spec["events"], key=lambda e: e["any_grade"])
    W = 900
    row_h = 34
    T = 84
    H = T + row_h * len(events) + 90
    L, R = 250, 110
    pw = W - L - R
    mx = max(e["any_grade"] for e in events) * 1.1

    out = [
        _t(20, 32, spec.get("title", ""), 17, weight="bold"),
        _t(20, 52, spec.get("subtitle", ""), 11, fill=MUTED),
    ]
    for i, e in enumerate(events):
        y = T + i * row_h
        out.append(_t(L - 14, y + 20, e["term"], 11.5, anchor="end"))
        w1 = e["any_grade"] / mx * pw
        w2 = e["grade3plus"] / mx * pw
        out.append(f'<rect x="{L}" y="{y+3:.1f}" width="{w1:.1f}" height="12" fill="{PALETTE[4]}"/>')
        out.append(f'<rect x="{L}" y="{y+18:.1f}" width="{w2:.1f}" height="12" '
                   f'fill="{PALETTE[1]}" fill-opacity="0.85"/>')
        out.append(_t(L + w1 + 6, y + 13, f'{e["any_grade"]:.1f}%', 9.5))
        out.append(_t(L + w2 + 6, y + 28, f'{e["grade3plus"]:.1f}%', 9.5))

    by = T + row_h * len(events) + 10
    out.append(f'<rect x="{L}" y="{by}" width="14" height="10" fill="{PALETTE[4]}"/>')
    out.append(_t(L + 20, by + 9, "Any grade", 11))
    out.append(f'<rect x="{L+110}" y="{by}" width="14" height="10" '
               f'fill="{PALETTE[1]}" fill-opacity="0.85"/>')
    out.append(_t(L + 130, by + 9, "Grade ≥ 3", 11))
    out.append(_t(L, by + 34, f"Patients (%), safety population n={spec['n']}", 12))

    return _wrap("".join(out), W, H, spec.get("title", ""), spec.get("caption", ""))


def data_table(kind: str, spec: dict) -> str:
    """The underlying numbers as markdown — always emitted alongside the SVG.

    A figure can be misread; a table cannot be read as more than it says.
    """
    lines = [f"# {spec.get('title', kind)}", ""]
    if spec.get("subtitle"):
        lines += [f"*{spec['subtitle']}*", ""]

    if kind == "km":
        lines += ["| Time | " + " | ".join(a["label"] for a in spec["arms"]) + " |",
                  "| --- | " + " | ".join("---" for _ in spec["arms"]) + " |"]
        for idx, t in enumerate(spec["risk_times"]):
            cells = []
            for a in spec["arms"]:
                surv = next((s for tt, s in zip(a["times"], a["survival"]) if tt >= t), "—")
                cells.append(f"{surv}% (n at risk {a['at_risk'][idx]})")
            lines.append(f"| {t} | " + " | ".join(str(c) for c in cells) + " |")
        if spec.get("annotation"):
            lines += ["", "```", spec["annotation"], "```"]
    elif kind == "forest":
        lines += ["| Subgroup | n | Estimate (95% CI) | Interaction p |",
                  "| --- | ---: | --- | --- |"]
        for r in spec["rows"]:
            p = f"{r['interaction_p']:.2f}" if r.get("interaction_p") is not None else "—"
            lines.append(f"| {r['label']} | {r.get('n', '—')} | "
                         f"{r['estimate']:.2f} ({r['lower']:.2f}–{r['upper']:.2f}) | {p} |")
        if spec.get("note"):
            lines += ["", f"> {spec['note']}"]
    elif kind == "waterfall":
        vals = sorted(spec["values"], reverse=True)
        resp = sum(1 for v in vals if v <= -30)
        lines += [f"- Patients shown: {spec.get('n_evaluable', len(vals))}",
                  f"- Enrolled: {spec.get('n_enrolled', 'not stated')}",
                  f"- Best change ≤ −30%: {resp}/{len(vals)}",
                  f"- Range: {min(vals)}% to {max(vals)}%"]
        if spec.get("exclusion_note"):
            lines += ["", f"> **{spec['exclusion_note']}**"]
    elif kind == "ae":
        lines += [f"Safety population n={spec['n']}", "",
                  "| Event | Any grade | Grade ≥3 |", "| --- | ---: | ---: |"]
        for e in sorted(spec["events"], key=lambda x: -x["any_grade"]):
            lines.append(f"| {e['term']} | {e['any_grade']:.1f}% | {e['grade3plus']:.1f}% |")

    if spec.get("caption"):
        lines += ["", f"*{spec['caption']}*"]
    lines += ["", "**DRAFT — REQUIRES QUALIFIED MEDICAL REVIEW**"]
    return "\n".join(lines) + "\n"


RENDERERS = {"km": km, "forest": forest, "waterfall": waterfall, "ae": ae}
