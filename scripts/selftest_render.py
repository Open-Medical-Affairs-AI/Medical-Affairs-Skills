#!/usr/bin/env python3
"""Prove the deliverable engine produces finished Word, PowerPoint and PDF files.

Runs with the document packages installed (CI installs them). For each case it
renders a real file and checks that it opens, carries the compliance furniture,
and passes the engine's own layout QA — a deck that overflows or is all text
fails here before a participant ever sees it.

    pip install python-pptx python-docx matplotlib reportlab
    python3 scripts/selftest_render.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ENGINE = REPO / "shared" / "ma_render" / "ma_render.py"
DECK = REPO / "skills" / "medical-slide-deck" / "scripts" / "build_deck.py"
OBESITY = REPO / "examples" / "obesity-advisory-preread" / "deck.json"

MD_DRAFT = """# Congress readout: what changed

*Oncology · synthetic workshop example*

## Bottom line

> **Key finding:** The new phase 3 data change sequencing questions, not the label.

- ORR 63% (95% CI 55.2–70.4) in the single-arm cohort (n=165)
- Grade ≥3 CRS 0.6%

## Evidence table

| Study | Design | n | Result |
|---|---|---|---|
| Example-1 | Single-arm phase 2 | 165 | ORR 63% |
| Example-2 | Randomised phase 3 | 480 | HR 0.58 (0.47–0.72) |
Source: Example A, et al. J Example Med 2024. PMID 00000000

## References

1. Example A, et al. J Example Med. 2024;12(3):100-110. PMID 00000000
"""


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable] + args, cwd=cwd, capture_output=True, text=True, timeout=600)


def docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        return z.read("word/document.xml").decode("utf-8", errors="replace")


def main() -> int:
    sys.path.insert(0, str(ENGINE.parent))
    import ma_render  # noqa: E402

    missing = [m for m in ("pptx", "docx", "matplotlib") if not ma_render.have(m)]
    if missing:
        print(f"Install the document packages first: {', '.join(missing)} missing.")
        return 1

    failures: list[str] = []
    passed = 0
    with tempfile.TemporaryDirectory() as td:
        work = Path(td)

        # 1. Worked deck example through the engine.
        spec = work / "deck.json"
        spec.write_text(json.dumps(ma_render.EXAMPLE_DECK), encoding="utf-8")
        proc = run([str(ENGINE), "deck", str(spec), "--out", str(work / "deck.pptx"), "--no-pdf",
                    "--no-install"], REPO)
        issues = ma_render.qa_pptx(work / "deck.pptx") if (work / "deck.pptx").exists() else ["not written"]
        if proc.returncode or issues:
            failures.append(f"engine example deck: rc={proc.returncode} {issues} {proc.stderr[-300:]}")
        else:
            passed += 1

        # 2. The rebuilt advisory pre-read must render clean — no overflow, not text-only.
        proc = run([str(ENGINE), "deck", str(OBESITY), "--out", str(work / "obesity.pptx"),
                    "--no-pdf", "--no-install"], REPO)
        issues = ma_render.qa_pptx(work / "obesity.pptx") if (work / "obesity.pptx").exists() else ["not written"]
        if proc.returncode or issues:
            failures.append(f"obesity pre-read: rc={proc.returncode} {issues}")
        else:
            passed += 1

        # 3. The medical deck builder wraps the engine and keeps its compliance gate.
        ex = run([str(DECK), "--example"], REPO)
        (work / "med.json").write_text(ex.stdout, encoding="utf-8")
        proc = run([str(DECK), "--spec", str(work / "med.json"), "--out", str(work / "med.pptx"),
                    "--no-pdf", "--no-install"], REPO)
        if proc.returncode or not (work / "med.pptx").exists():
            failures.append(f"build_deck.py: rc={proc.returncode} {proc.stdout[-300:]}")
        else:
            passed += 1
        bad = json.loads(ex.stdout)
        bad["slides"] = [s for s in bad["slides"]]
        for s in bad["slides"]:
            if s.get("type") == "data":
                s.pop("citation", None)
        (work / "bad.json").write_text(json.dumps(bad), encoding="utf-8")
        proc = run([str(DECK), "--spec", str(work / "bad.json"), "--out", str(work / "bad.pptx"),
                    "--no-install"], REPO)
        if proc.returncode == 0 or "citation" not in proc.stdout:
            failures.append("build_deck.py rendered a data slide without a citation")
        else:
            passed += 1

        # 4. Report spec -> designed Word document (+ PDF via reportlab when available).
        spec = work / "report.json"
        spec.write_text(json.dumps(ma_render.EXAMPLE_REPORT), encoding="utf-8")
        proc = run([str(ENGINE), "report", str(spec), "--out", str(work / "report.docx"), "--no-install"], REPO)
        docx = work / "report.docx"
        if proc.returncode or not docx.exists() or "DRAFT" not in docx_text(docx):
            failures.append(f"report: rc={proc.returncode} {proc.stdout[-300:]}")
        else:
            passed += 1
        if ma_render.have("reportlab") and not (work / "report.pdf").exists():
            failures.append("report: reportlab installed but no PDF written")

        # 5. A markdown draft becomes Word, never a delivered .md.
        md = work / "readout.md"
        md.write_text(MD_DRAFT, encoding="utf-8")
        proc = run([str(ENGINE), "report", str(md), "--out", str(work / "readout.docx"), "--no-install"], REPO)
        out = work / "readout.docx"
        text = docx_text(out) if out.exists() else ""
        needles = ["Congress readout", "HR 0.58", "PMID 00000000", "KEY FINDING", "DRAFT"]
        lost = [n for n in needles if n not in text]
        if proc.returncode or lost:
            failures.append(f"markdown draft -> docx lost {lost}")
        else:
            passed += 1

        # 6. Standard-library .docx is a valid Word package.
        path = work / "stdlib.docx"
        ma_render.report_docx_stdlib(ma_render.EXAMPLE_REPORT, path)
        with zipfile.ZipFile(path) as z:
            names = set(z.namelist())
        if not {"[Content_Types].xml", "word/document.xml", "word/styles.xml"} <= names:
            failures.append("stdlib docx is missing required parts")
        else:
            passed += 1

    for f in failures:
        print(f"  FAIL   {f}")
    print(f"\n{passed} passed · {len(failures)} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
