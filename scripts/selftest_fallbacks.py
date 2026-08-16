#!/usr/bin/env python3
"""Prove every content generator degrades instead of failing.

The rule this suite enforces: **never lose the analysis; degrade the container,
never the content.** A generator that exits non-zero when an optional library is
missing fails here, because the calling agent would report failure to a user who
could have had the content.

Each case runs a generator twice — once normally, once with the library hidden
via a sitecustomize shim — and asserts that the degraded run:

  1. exits 0 (a degraded output is a success)
  2. still wrote a file
  3. printed a visible degradation notice naming what was missing, what was
     delivered, and how to get the full version
  4. **kept the substantive content** — the citations, designs, denominators
     and compliance elements that must survive every tier

Check 4 is the one that matters. A fallback that produces an empty shell with a
polite note is worse than a crash, because it looks like it worked.

    python3 scripts/selftest_fallbacks.py
    python3 scripts/selftest_fallbacks.py --verbose
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

DECK = "skills/medical-slide-deck/scripts/build_deck.py"
MANUSCRIPT = "skills/scientific-manuscript/scripts/build_manuscript.py"
POSTER = "skills/congress-abstract-and-poster/scripts/build_poster.py"
FIGURES = "skills/data-visualization-for-medical/scripts/clinical_figures.py"
SHEET = "skills/spreadsheet-analysis/scripts/sheets.py"
PDF = "skills/pdf-generation/scripts/build_pdf.py"
LETTER = "skills/medical-correspondence/scripts/letter.py"
CAPS = "skills/capability-detection/scripts/capabilities.py"

# Phrases every degradation notice must carry. These are not stylistic — a
# reader has to be able to tell what they are holding and how to get the full
# version.
#
# "To get" rather than the exact "To get it:" because a generator that can name
# the artefact says something more useful — build_pdf.py writes "To get the
# PDF:", and pinning the literal string would have forced it to be vaguer. The
# guarantee being enforced is that a route forward is stated, not its wording.
NOTICE_MARKERS = ("DEGRADED OUTPUT", "Delivered:", "To get", "pip install")


@dataclass
class Case:
    name: str
    script: str
    hide: str                      # module to make unimportable
    example_args: list[str] = field(default_factory=list)
    build_args: list[str] = field(default_factory=lambda: ["--spec", "SPEC", "--out", "OUT"])
    out_name: str = "out.bin"
    expect_files: tuple[str, ...] = ()      # suffixes that must exist afterwards
    must_survive: tuple[str, ...] = ()      # content that must appear in the output


CASES = [
    Case(
        name="deck degrades to markdown + build spec",
        script=DECK, hide="pptx",
        example_args=["--example"],
        out_name="deck.pptx",
        expect_files=(".md", ".json"),
        must_survive=(
            "Example A, et al. J Example Med",   # the citation
            "Single-arm",                         # the design statement
            "n=165",                              # the denominator
            "DRAFT",                              # the draft marking
            "NORVANTIB is approved",              # approval status
            "What remains unknown",               # the limitations slide
        ),
    ),
    Case(
        name="manuscript degrades to markdown",
        script=MANUSCRIPT, hide="docx",
        example_args=["--example"],
        out_name="ms.docx",
        expect_files=(".md",),
        must_survive=(
            "ICMJE",                              # authorship criteria retained
            "Conflicts of interest",
            "Funding",
            "Medical writing support",            # GPP 2022 disclosure
            "NCT00000000",                        # registration
            "95% CI 17.1-24.8",                   # the confidence interval
            "DRAFT",
        ),
    ),
    Case(
        name="poster degrades to printable HTML",
        script=POSTER, hide="pptx",
        example_args=["--example"],
        out_name="poster.pptx",
        expect_files=(".html",),
        must_survive=(
            "48in 36in",                          # physical size preserved
            "Cytokine release syndrome 72.1%",    # safety data
            "95% CI 55.2",                        # confidence interval
            "investigational",                    # approval status
            "DRAFT",
        ),
    ),
    Case(
        name="KM figure degrades to SVG + data table",
        script=FIGURES, hide="matplotlib",
        example_args=["km", "--example"],
        build_args=["km", "--spec", "SPEC", "--out", "OUT"],
        out_name="km.png",
        expect_files=(".svg", ".md"),
        must_survive=(
            "Number at risk",                     # mandatory in every tier
            "280", "241", "61",                   # the at-risk numbers themselves
            "HR 0.58",
            "DRAFT",
        ),
    ),
    Case(
        name="forest plot degrades to SVG + data table",
        script=FIGURES, hide="matplotlib",
        example_args=["forest", "--example"],
        build_args=["forest", "--spec", "SPEC", "--out", "OUT"],
        out_name="forest.png",
        expect_files=(".svg", ".md"),
        must_survive=("0.58", "0.47", "0.72", "p(int)", "hypothesis-generating"),
    ),
    Case(
        name="waterfall degrades to SVG + data table",
        script=FIGURES, hide="matplotlib",
        example_args=["waterfall", "--example"],
        build_args=["waterfall", "--spec", "SPEC", "--out", "OUT"],
        out_name="wf.png",
        expect_files=(".svg", ".md"),
        must_survive=("not shown", "Enrolled", "34"),   # the exclusion must survive
    ),
    Case(
        name="spreadsheet degrades to CSV + markdown table",
        script=SHEET, hide="openpyxl",
        example_args=["write", "--example"],
        build_args=["write", "--spec", "SPEC", "--out", "OUT"],
        out_name="tracker.xlsx",
        expect_files=(".csv", ".md"),
        must_survive=(
            "DRAFT",                              # the draft marking
            "INS-003",                            # every row, not just the top ones
            "n screened",                         # the denominator column
            "40",                                 # the denominator itself
            "Low — weak signal",                  # the confidence qualifier
            "Evidence Generation Lead",           # the owner
        ),
    ),
    Case(
        name="PDF degrades to printable HTML",
        script=PDF, hide="reportlab",
        example_args=["--example"],
        out_name="brief.pdf",
        expect_files=(".html",),
        must_survive=(
            "SRD-0142",                           # document control identifier
            "NORVANTIB is approved",              # approval status statement
            "CrCl &lt;40 mL/min",                 # the exclusion that is the answer,
                                                  # HTML-escaped as it should be
            "no dosing recommendation can be made",
            "DRAFT",
        ),
    ),
    Case(
        name="letter degrades to markdown",
        script=LETTER, hide="docx",
        example_args=["--example", "dhcp"],
        out_name="letter.docx",
        expect_files=(".md",),
        must_survive=(
            "antimicrobial prophylaxis",          # the actual safety instruction
            "post-marketing reports of serious infections",
            "DRAFT",
        ),
    ),
    Case(
        name="AE figure degrades to SVG + data table",
        script=FIGURES, hide="matplotlib",
        example_args=["ae", "--example"],
        build_args=["ae", "--spec", "SPEC", "--out", "OUT"],
        out_name="ae.png",
        expect_files=(".svg", ".md"),
        must_survive=("n=165", "Cytokine release syndrome", "72.1", "64.2"),
    ),
]


def run(argv: list[str], cwd: Path, hide: str | None = None) -> subprocess.CompletedProcess:
    """Run a script, optionally making `hide` unimportable.

    A sitecustomize shim is used rather than sys.modules patching because the
    script runs in a fresh interpreter — this is how it would genuinely behave
    on a machine where the package is not installed.
    """
    env = None
    if hide:
        shim = cwd / "_shim"
        shim.mkdir(exist_ok=True)
        (shim / "sitecustomize.py").write_text(
            "import sys\n"
            "class _Block:\n"
            "    def find_module(self, name, path=None):\n"
            f"        return self if name == {hide!r} or name.startswith({hide!r} + '.') else None\n"
            "    def load_module(self, name):\n"
            "        raise ImportError(name)\n"
            "    def find_spec(self, name, path=None, target=None):\n"
            f"        if name == {hide!r} or name.startswith({hide!r} + '.'):\n"
            "            raise ImportError(name)\n"
            "        return None\n"
            "sys.meta_path.insert(0, _Block())\n",
            encoding="utf-8",
        )
        import os
        env = dict(os.environ)
        env["PYTHONPATH"] = str(shim) + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(
        [sys.executable] + argv, cwd=cwd, capture_output=True, text=True,
        timeout=120, env=env,
    )


def check_case(case: Case, verbose: bool) -> tuple[bool, list[str]]:
    problems: list[str] = []
    with tempfile.TemporaryDirectory() as td:
        work = Path(td)

        # 1. Generate the example spec (uses the real interpreter, no hiding).
        spec_path = work / "spec.json"
        proc = run([str(REPO / case.script)] + case.example_args, REPO)
        if proc.returncode != 0:
            return False, [f"could not generate example spec: {proc.stderr[:300]}"]
        spec_path.write_text(proc.stdout, encoding="utf-8")

        # 2. Run the builder with the library hidden.
        out = work / case.out_name
        argv = [str(REPO / case.script)] + [
            str(out) if a == "OUT" else (str(spec_path) if a == "SPEC" else a)
            for a in case.build_args
        ]
        proc = run(argv, work, hide=case.hide)
        combined = proc.stdout + proc.stderr

        if verbose:
            print(f"    $ (with {case.hide} hidden) {' '.join(argv[1:])}")

        # -- assertion 1: exit 0 -------------------------------------------
        if proc.returncode != 0:
            problems.append(
                f"exited {proc.returncode} with {case.hide} hidden — a degraded "
                f"output is a success, not a failure. Output: {combined[:300]}"
            )

        # -- assertion 2: a file was still produced -------------------------
        produced = []
        for suffix in case.expect_files:
            f = out.with_suffix(suffix)
            if f.exists() and f.stat().st_size > 0:
                produced.append(f)
            else:
                problems.append(f"expected fallback file {f.name} was not written")

        # -- assertion 3: visible degradation notice ------------------------
        for marker in NOTICE_MARKERS:
            if marker not in combined:
                problems.append(
                    f"degradation notice missing {marker!r} — a reader must be able "
                    f"to tell what they are holding and how to get the full version"
                )

        # -- assertion 4: the substantive content survived -------------------
        blob = "\n".join(p.read_text(encoding="utf-8", errors="replace")
                         for p in produced)
        for needle in case.must_survive:
            if needle not in blob:
                problems.append(
                    f"content lost in fallback: {needle!r} does not appear in the "
                    f"degraded output. Degrade the container, never the content."
                )

    return not problems, problems


def check_no_hard_exits() -> list[str]:
    """No content generator may SystemExit on a missing optional package."""
    problems = []
    for script in (DECK, MANUSCRIPT, POSTER, FIGURES, SHEET, PDF, LETTER):
        text = (REPO / script).read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines(), 1):
            if "SystemExit" in line and "is required" in line:
                problems.append(
                    f"{script}:{i} raises SystemExit for a missing package — "
                    f"degrade instead"
                )
        if "def _have(" not in text:
            problems.append(f"{script} has no inline capability check (_have)")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    print("Fallback self-test — every generator must degrade, not fail\n")

    passed = failed = 0

    static = check_no_hard_exits()
    if static:
        failed += 1
        print("  FAIL   static check: hard exits on missing packages")
        for p in static:
            print(f"         {p}")
    else:
        passed += 1
        print("  pass   static check: no generator hard-exits on a missing package")

    for case in CASES:
        ok, problems = check_case(case, args.verbose)
        if ok:
            passed += 1
            print(f"  pass   {case.name}")
        else:
            failed += 1
            print(f"  FAIL   {case.name}")
            for p in problems:
                print(f"         {p}")

    # capability-detection must itself work with nothing installed
    proc = run([str(REPO / CAPS), "--json"], REPO, hide="pptx")
    if proc.returncode == 0 and '"packages"' in proc.stdout:
        passed += 1
        print("  pass   capability-detection runs with packages missing")
    else:
        failed += 1
        print("  FAIL   capability-detection broke when a package was missing")

    print(f"\n{passed} passed · {failed} failed")
    if failed:
        print(
            "\nThe rule: never lose the analysis. Degrade the container, never the\n"
            "content. A generator that exits non-zero on a missing optional package\n"
            "loses hours of reasoning to a missing renderer."
        )
        return 1
    print(
        "\nEvery generator degrades visibly and keeps its substantive content —\n"
        "citations, study designs, denominators, confidence intervals, safety data\n"
        "and the draft marking all survive the fallback path."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
