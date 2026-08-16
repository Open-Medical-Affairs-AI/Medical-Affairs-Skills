#!/usr/bin/env python3
"""Report what this runtime can actually do, and resolve the best output path.

Check before promising a deliverable. Telling someone up front that you will
deliver markdown because python-pptx is unavailable is a different conversation
from handing them markdown when they expected slides.

    S=skills/capability-detection/scripts/capabilities.py

    python3 $S                                    # full report
    python3 $S --json                             # machine-readable
    python3 $S --best-path deck                   # which tier, and why
    python3 $S --best-path figure --require-tier 2  # non-zero if unavailable
    python3 $S --check-network                    # per-host reachability

No dependencies beyond the standard library — this has to work in exactly the
environments where nothing else does.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import socket
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

# Optional packages. Everything in this library works without all of them; each
# one moves an output type from tier 3 to tier 2.
PACKAGES = {
    "pptx": ("python-pptx", "slide decks and posters"),
    "docx": ("python-docx", "manuscripts and letters"),
    "openpyxl": ("openpyxl", "spreadsheets"),
    "matplotlib": ("matplotlib", "clinical figures"),
    "reportlab": ("reportlab", "PDF generation"),
    "pypdf": ("pypdf", "reading PDFs"),
    "pdfplumber": ("pdfplumber", "reading PDFs with layout and tables"),
    "yaml": ("pyyaml", "skill validation tooling"),
}

# Hosts fail independently — corporate networks block NCBI far more often than
# openFDA — so probe each one rather than reporting "network: yes".
HOSTS = {
    "eutils.ncbi.nlm.nih.gov": "PubMed literature search and MeSH",
    "clinicaltrials.gov": "trial registry",
    "api.fda.gov": "approved labels and FAERS",
    "api.crossref.org": "DOI verification",
    "api.openalex.org": "DOI fallback and retraction flags",
}

# output type -> (tier 2 requirement, tier 3 format, what tier 3 loses)
OUTPUTS = {
    "deck": ("pptx", "markdown + deck.json build spec",
             "slide layout and theming; no content is lost"),
    "poster": ("pptx", "printable HTML at the correct aspect ratio",
               "exact print positioning; no content is lost"),
    "document": ("docx", "markdown with the full structure and statements block",
                 "Word styling; no content is lost"),
    "manuscript": ("docx", "markdown with the full IMRaD structure",
                   "Word styling; no content is lost"),
    "spreadsheet": ("openpyxl", "CSV plus a markdown table",
                    "formulas, formatting and multiple sheets"),
    "figure": ("matplotlib", "hand-written SVG plus the underlying data table",
               "nothing for line and bar figures; complex plots simplify"),
    "pdf": ("reportlab", "HTML with print stylesheet",
            "nothing — print to PDF from any browser"),
    "read-pdf": ("pypdf", "ask the user to paste the text",
                 "everything — a PDF cannot be read without a reader"),
}


def have(module: str) -> bool:
    """True if importable. find_spec avoids the cost and side effects of import."""
    try:
        return importlib.util.find_spec(module) is not None
    except (ImportError, ValueError, ModuleNotFoundError):
        return False


def native_skills() -> list[str]:
    """Best-effort detection of runtime-provided document skills (tier 1).

    Cannot be detected reliably from inside a script — the runtime exposes these
    to the agent, not to the filesystem in any standard place. Treated as a hint
    only; the agent knows better than this function does.
    """
    found = []
    candidates = [
        Path.home() / ".claude" / "skills",
        Path("/opt/skills"),
        Path.cwd() / ".claude" / "skills",
    ]
    for root in candidates:
        if not root.exists():
            continue
        for name in ("pptx", "docx", "xlsx", "pdf"):
            if (root / name / "SKILL.md").exists() or (
                root / "synced" / name / "SKILL.md"
            ).exists():
                found.append(name)
    return sorted(set(found))


def writable(path: str | None = None) -> tuple[bool, str]:
    target = Path(path) if path else Path.cwd()
    try:
        with tempfile.NamedTemporaryFile(dir=target, delete=True):
            pass
        return True, str(target)
    except (OSError, PermissionError) as exc:
        try:
            t = tempfile.gettempdir()
            with tempfile.NamedTemporaryFile(dir=t, delete=True):
                pass
            return True, t
        except (OSError, PermissionError):
            return False, f"{target}: {exc}"


def reachable(host: str, timeout: float = 6.0) -> tuple[bool, str]:
    try:
        socket.getaddrinfo(host, 443)
    except socket.gaierror as exc:
        return False, f"DNS failed ({exc.strerror or exc})"
    try:
        req = urllib.request.Request(
            f"https://{host}/", headers={"User-Agent": "medical-affairs-skills/1.0"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return True, f"HTTP {resp.status}"
    except urllib.error.HTTPError as exc:
        # A 4xx from the host itself still proves we reached it.
        return True, f"HTTP {exc.code} (reachable)"
    except urllib.error.URLError as exc:
        return False, str(exc.reason)
    except Exception as exc:  # noqa: BLE001 — the reason is the useful part
        return False, str(exc)


def resolve(output: str, check_net: bool = False) -> dict:
    if output not in OUTPUTS:
        raise SystemExit(
            f"Unknown output type '{output}'.\nKnown: {', '.join(sorted(OUTPUTS))}"
        )
    module, tier3, loses = OUTPUTS[output]
    pkg = PACKAGES.get(module, (module, ""))[0]
    natives = native_skills()
    can_write, where = writable()

    native_map = {"deck": "pptx", "poster": "pptx", "document": "docx",
                  "manuscript": "docx", "spreadsheet": "xlsx", "pdf": "pdf"}
    if native_map.get(output) in natives:
        tier, path, why = 1, f"native '{native_map[output]}' skill", \
            "runtime provides a document skill; hand the content to it"
    elif have(module):
        tier, path, why = 2, f"bundled script via {pkg}", f"{pkg} is importable"
    elif can_write:
        tier, path, why = 3, tier3, f"{pkg} unavailable; writing an open format instead"
    else:
        tier, path, why = 4, "structured content in the response", \
            f"{pkg} unavailable and no writable filesystem ({where})"

    return {
        "output": output,
        "tier": tier,
        "path": path,
        "why": why,
        "degraded": tier >= 3,
        "missing_package": None if tier <= 2 else pkg,
        "what_tier3_loses": loses if tier >= 3 else None,
        "writable_dir": where if can_write else None,
    }


def report(check_net: bool) -> dict:
    pkgs = {}
    for mod, (pkg, purpose) in PACKAGES.items():
        pkgs[mod] = {"package": pkg, "available": have(mod), "enables": purpose}

    can_write, where = writable()
    data = {
        "python": sys.version.split()[0],
        "packages": pkgs,
        "native_document_skills": native_skills(),
        "filesystem_writable": can_write,
        "writable_dir": where if can_write else None,
        "network": {},
        "outputs": {k: resolve(k) for k in OUTPUTS},
    }
    if check_net:
        for host, purpose in HOSTS.items():
            ok, detail = reachable(host)
            data["network"][host] = {"reachable": ok, "detail": detail,
                                     "enables": purpose}
    return data


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--best-path", metavar="OUTPUT",
                    help=f"one of: {', '.join(sorted(OUTPUTS))}")
    ap.add_argument("--require-tier", type=int, choices=[1, 2, 3],
                    help="exit non-zero if the resolved tier is worse than this")
    ap.add_argument("--check-network", action="store_true",
                    help="probe API hosts (adds a few seconds)")
    args = ap.parse_args()

    if args.best_path:
        r = resolve(args.best_path)
        if args.json:
            print(json.dumps(r, indent=2))
        else:
            print(f"{args.best_path}: tier {r['tier']} — {r['path']}")
            print(f"  why: {r['why']}")
            if r["degraded"]:
                print(f"  tier 3 loses: {r['what_tier3_loses']}")
                print(f"  to reach tier 2:  pip install {r['missing_package']}")
                print("  Degrade VISIBLY — say what is missing, what you delivered,")
                print("  the command to get the full version, and whether content was lost.")
        if args.require_tier and r["tier"] > args.require_tier:
            return 1
        return 0

    data = report(args.check_network)
    if args.json:
        print(json.dumps(data, indent=2))
        return 0

    print(f"Runtime capabilities — Python {data['python']}\n")

    print("Optional packages")
    for mod, info in data["packages"].items():
        mark = "yes" if info["available"] else "NO "
        print(f"  {mark}  {info['package']:<14} {info['enables']}")

    if data["native_document_skills"]:
        print(f"\nNative document skills detected: "
              f"{', '.join(data['native_document_skills'])}")
        print("  Prefer these (tier 1) — better fidelity, and they handle themes")
        print("  and templates this library does not attempt.")
    else:
        print("\nNative document skills: none detected")
        print("  (Detection is best-effort — the runtime exposes these to you,")
        print("   not to the filesystem. If you have them, use them.)")

    print(f"\nFilesystem writable: {'yes — ' + data['writable_dir'] if data['filesystem_writable'] else 'NO'}")
    if not data["filesystem_writable"]:
        print("  Tier 4 only: deliver structured content in your response.")

    if args.check_network:
        print("\nNetwork")
        for host, info in data["network"].items():
            mark = "yes" if info["reachable"] else "NO "
            print(f"  {mark}  {host:<32} {info['detail']}")
        if not any(i["reachable"] for i in data["network"].values()):
            print("\n  No API host is reachable. Citations CANNOT be verified.")
            print("  Label every reference as unverified in the deliverable —")
            print("  do not emit them as though they had been checked.")

    print("\nResolved output paths")
    for name, r in data["outputs"].items():
        flag = "  DEGRADED" if r["degraded"] else ""
        print(f"  {name:<12} tier {r['tier']}  {r['path']}{flag}")

    degraded = [n for n, r in data["outputs"].items() if r["degraded"]]
    if degraded:
        print(
            f"\n{len(degraded)} output type(s) will degrade. That is fine — every "
            f"one still\nproduces the full content in an open format. Say so in the "
            f"deliverable\nrather than letting a reader assume they have the "
            f"finished article."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
