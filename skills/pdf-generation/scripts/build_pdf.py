#!/usr/bin/env python3
"""PDF deliverables, with an HTML print fallback that loses nothing.

Every browser prints to PDF, so this is the output type where degrading costs
almost nothing — the fallback notice says what to do rather than apologising.

    S=skills/pdf-generation/scripts/build_pdf.py
    python3 $S --example > doc.json
    python3 $S --spec doc.json --out brief.pdf
    python3 $S --spec doc.json --out brief.pdf --html-only

reportlab is optional.
"""
from __future__ import annotations
import argparse, json, sys
from html import escape
from pathlib import Path

DRAFT = "DRAFT — NOT FOR EXTERNAL USE. REQUIRES QUALIFIED MEDICAL REVIEW."

EXAMPLE = {
    "title": "Scientific response: NORVANTIB in renal impairment",
    "document_id": "SRD-0142", "version": "3", "date": "2026-08-15",
    "review_date": "2027-08-15", "author": "Medical Information",
    "approval_status": ("NORVANTIB is approved in the US for adults with "
                        "relapsed/refractory multiple myeloma after ≥4 prior lines. "
                        "Use in severe renal impairment is not established."),
    "sections": [
        {"heading": "Question as asked",
         "body": "Is dose adjustment required for patients with CrCl below 30 mL/min?"},
        {"heading": "Summary answer",
         "body": "No dedicated renal impairment study has been conducted. The "
                 "pivotal trial excluded CrCl <40 mL/min, so no data are available "
                 "in this population and no dosing recommendation can be made."},
        {"heading": "Supporting evidence",
         "body": "NVB-201 (single-arm, phase 1/2, n=168) excluded patients with "
                 "CrCl <40 mL/min. Population PK analysis found no clinically "
                 "meaningful effect across the studied range (CrCl 40-150), which "
                 "does not extrapolate below the studied range."},
        {"heading": "What the evidence does not establish",
         "body": "Safety, efficacy or appropriate dosing at CrCl <40 mL/min."},
    ],
    "references": [
        "Example A, et al. J Example Med. 2024;12(3):100-110. PMID 00000000",
    ],
}


def _have(m: str) -> bool:
    try:
        __import__(m); return True
    except ImportError:
        return False


def check(spec: dict) -> list[str]:
    out = []
    if not spec.get("title"):
        out.append("no title")
    if not spec.get("sections"):
        out.append("no sections")
    if not spec.get("approval_status"):
        out.append("no approval_status — required wherever a product use is discussed")
    for f in ("document_id", "version", "date"):
        if not spec.get(f):
            out.append(f"no {f} — document control is noticed only after distribution")
    return out


def render_html(spec: dict) -> str:
    secs = "".join(
        f'<section><h2>{escape(s["heading"])}</h2><p>{escape(s["body"])}</p></section>'
        for s in spec.get("sections", []))
    refs = "".join(f"<li>{escape(r)}</li>" for r in spec.get("references", []))
    ctrl = (f'{escape(spec.get("document_id",""))} · v{escape(str(spec.get("version","")))}'
            f' · {escape(spec.get("date",""))}'
            + (f' · review by {escape(spec["review_date"])}' if spec.get("review_date") else ""))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{escape(spec['title'])}</title><style>
@page{{size:A4;margin:22mm 18mm 24mm;
  @bottom-left{{content:"{ctrl}";font-size:8pt;color:#555}}
  @bottom-center{{content:"{DRAFT}";font-size:8pt;color:#993300}}
  @bottom-right{{content:"page " counter(page) " of " counter(pages);font-size:8pt;color:#555}}}}
body{{font:11.5pt/1.5 Georgia,"Times New Roman",serif;color:#1a1a1a;max-width:170mm;margin:0 auto;padding:16px}}
h1{{font-size:17pt;margin:0 0 4px}}
.ctrl{{font-size:9pt;color:#555;border-bottom:1px solid #ccc;padding-bottom:8px;margin-bottom:16px}}
.approval{{border-left:3px solid #00518c;padding:8px 12px;background:#f4f8fb;font-size:10.5pt;margin-bottom:18px}}
h2{{font-size:12.5pt;color:#00518c;margin:18px 0 6px;page-break-after:avoid}}
section{{page-break-inside:avoid}}
ol{{font-size:10pt}} li{{margin-bottom:5px;page-break-inside:avoid}}
.draft{{color:#993300;font-weight:bold;font-size:10pt;border:1px solid #993300;padding:6px 10px;margin-bottom:14px}}
@media screen{{.print-hint{{background:#fff8e1;border:1px solid #e0c060;padding:10px 14px;margin-bottom:18px;font-family:sans-serif;font-size:10pt}}}}
@media print{{.print-hint{{display:none}}}}
</style></head><body>
<div class="print-hint"><b>To produce the PDF:</b> print this page (Ctrl/Cmd-P) and
choose "Save as PDF". Pagination, running footers and page numbers are set in the
stylesheet, so the result matches what a PDF library would have produced.</div>
<div class="draft">{DRAFT}</div>
<h1>{escape(spec['title'])}</h1>
<div class="ctrl">{ctrl}{(' · ' + escape(spec['author'])) if spec.get('author') else ''}</div>
<div class="approval"><b>Approval status.</b> {escape(spec.get('approval_status',''))}</div>
{secs}
{f'<h2>References</h2><ol>{refs}</ol>' if refs else ''}
</body></html>
"""


def build_pdf(spec: dict, out: Path) -> None:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    ListFlowable, ListItem)

    styles = getSampleStyleSheet()
    warn = ParagraphStyle("warn", parent=styles["Normal"], textColor=colors.HexColor("#993300"),
                          fontSize=9, spaceAfter=10)
    h2 = ParagraphStyle("h2x", parent=styles["Heading2"],
                        textColor=colors.HexColor("#00518c"), fontSize=12)

    def footer(canvas, doc):
        canvas.saveState(); canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.HexColor("#555555"))
        ctrl = f"{spec.get('document_id','')} · v{spec.get('version','')} · {spec.get('date','')}"
        canvas.drawString(18 * mm, 12 * mm, ctrl)
        canvas.drawRightString(A4[0] - 18 * mm, 12 * mm, f"page {doc.page}")
        canvas.setFillColor(colors.HexColor("#993300"))
        canvas.drawCentredString(A4[0] / 2, 12 * mm, DRAFT)
        canvas.restoreState()

    story = [Paragraph(DRAFT, warn), Paragraph(spec["title"], styles["Title"]),
             Paragraph(f"{spec.get('document_id','')} · v{spec.get('version','')} · "
                       f"{spec.get('date','')}", styles["Normal"]), Spacer(1, 8)]
    if spec.get("approval_status"):
        story += [Paragraph(f"<b>Approval status.</b> {spec['approval_status']}",
                            styles["Normal"]), Spacer(1, 10)]
    for s in spec.get("sections", []):
        story += [Paragraph(s["heading"], h2), Paragraph(s["body"], styles["BodyText"])]
    if spec.get("references"):
        story += [Paragraph("References", h2),
                  ListFlowable([ListItem(Paragraph(r, styles["Normal"]))
                                for r in spec["references"]], bulletType="1")]
    out.parent.mkdir(parents=True, exist_ok=True)
    SimpleDocTemplate(str(out), pagesize=A4, topMargin=22*mm, bottomMargin=24*mm,
                      leftMargin=18*mm, rightMargin=18*mm,
                      title=spec["title"]).build(story, onFirstPage=footer,
                                                 onLaterPages=footer)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec"); ap.add_argument("--out", default="document.pdf")
    ap.add_argument("--example", action="store_true")
    ap.add_argument("--html-only", action="store_true")
    args = ap.parse_args()
    if args.example:
        print(json.dumps(EXAMPLE, indent=2)); return 0
    spec = (json.loads(Path(args.spec).read_text(encoding="utf-8"))
            if args.spec else EXAMPLE)
    problems = check(spec)
    for p in problems:
        print(f"  BLOCKED  {p}")
    if problems:
        return 1
    out = Path(args.out)
    if _have("reportlab") and not args.html_only:
        build_pdf(spec, out); print(f"Wrote {out}"); return 0
    html = out.with_suffix(".html")
    html.parent.mkdir(parents=True, exist_ok=True)
    html.write_text(render_html(spec), encoding="utf-8")
    why = "--html-only requested" if args.html_only else "reportlab is not available"
    print(f"""⚠ DEGRADED OUTPUT — {why}.

   Delivered:      {html}  (print-ready, A4, running footers and page numbers)
   Not delivered:  {out}
   To get the PDF: open {html.name} and print to PDF (Ctrl/Cmd-P → Save as PDF)
                   or  pip install reportlab  and rerun

   Nothing was lost. Pagination, the draft marking on every page, document
   control and page numbering are all set in the stylesheet.
""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
