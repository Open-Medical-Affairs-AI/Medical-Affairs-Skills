#!/usr/bin/env python3
"""Package skills for agents that load uploaded files (GrokBot, Claude projects).

A GrokBot agent only knows what it has been given. Pointing it at one SKILL.md
loses the scripts, the dependencies the skill's reasoning relies on and the
deliverable engine — which is how an agent ends up improvising its own slides.
This builds uploads that are complete on their own:

  dist/grokbot/skills/<skill>.zip      one skill + its metadata.requires closure
  dist/grokbot/agents/<mission>.zip    one agent per workshop mission: its skills,
                                       their closure, and the mission's inputs
  workshop/grokbot-agents.json         the agent roster: skills in load order,
                                       files to upload, and the agent instructions

Every zip keeps repository-relative paths (skills/<name>/..., AGENTS.md,
docs/execution.md, house-rules/<name>.md), so cross-references still resolve,
and every skill inside carries scripts/ma_render.py and scripts/requirements.txt.

    python3 scripts/package_skills.py                # build dist/ and the roster
    python3 scripts/package_skills.py --check        # CI: roster is current
    python3 scripts/package_skills.py --skill medical-slide-deck
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS = REPO / "skills"
DIST = REPO / "dist" / "grokbot"
ROSTER = REPO / "workshop" / "grokbot-agents.json"
ALWAYS = ["medical-affairs-foundations", "deliverable-quality-review", "capability-detection"]
SHARED_FILES = ["AGENTS.md", "docs/execution.md", "DISCLAIMER.md"]
SKIP_PARTS = {"__pycache__", ".pytest_cache"}


def frontmatter(skill: str) -> dict:
    text = (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8")
    end = text.index("\n---", 3)
    fm = text[3:end]
    try:
        import yaml
        return yaml.safe_load(fm) or {}
    except ImportError:  # minimal parse: enough for requires/deliverables
        meta: dict = {"metadata": {}}
        for key in ("requires", "deliverables"):
            m = re.search(rf"^  {key}:\s*\n((?:    - .+\n)+)", fm + "\n", re.M)
            if m:
                meta["metadata"][key] = [x.strip()[2:].strip() for x in m.group(1).splitlines()]
            m = re.search(rf"^  {key}:\s*\[(.*)\]", fm, re.M)
            if m:
                meta["metadata"][key] = [x.strip() for x in m.group(1).split(",") if x.strip()]
        d = re.search(r"^description:\s*>-?\s*\n((?:  .+\n)+)", fm + "\n", re.M)
        meta["description"] = " ".join(x.strip() for x in d.group(1).splitlines()) if d else ""
        return meta


def closure(skills: list[str]) -> list[str]:
    """Skills plus everything they require, dependencies first."""
    order: list[str] = []

    def visit(name: str, trail: tuple = ()):
        if name in order or name in trail or not (SKILLS / name / "SKILL.md").exists():
            return
        for dep in (frontmatter(name).get("metadata") or {}).get("requires") or []:
            visit(dep, trail + (name,))
        order.append(name)

    for s in ALWAYS + skills:
        visit(s)
    return order


def skill_files(skill: str) -> list[Path]:
    base = SKILLS / skill
    files = [p for p in sorted(base.rglob("*")) if p.is_file()
             and not (set(p.relative_to(base).parts) & SKIP_PARTS) and p.suffix != ".pyc"]
    hr = REPO / "house-rules" / f"{skill}.md"
    return files + ([hr] if hr.exists() else [])


def write_zip(out: Path, skills: list[str], extra: list[Path], readme: str) -> int:
    out.parent.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("START-HERE.md", readme)
        for rel in SHARED_FILES:
            if (REPO / rel).exists():
                z.write(REPO / rel, rel); seen.add(rel)
        for s in skills:
            for f in skill_files(s):
                rel = str(f.relative_to(REPO))
                if rel not in seen:
                    z.write(f, rel); seen.add(rel)
        for f in extra:
            rel = str(f.relative_to(REPO))
            if f.exists() and rel not in seen:
                z.write(f, rel); seen.add(rel)
    return len(seen) + 1


def deliverable_line(skills: list[str]) -> str:
    kinds: list[str] = []
    for s in skills:
        for d in (frontmatter(s).get("metadata") or {}).get("deliverables") or []:
            if d not in kinds:
                kinds.append(d)
    return ", ".join(kinds) or "docx, pdf"


def instructions(title: str, objective: str, skills: list[str], load: list[str], engine_skill: str) -> str:
    return (
        f"You are the '{title}' Medical Affairs agent. Objective: {objective}\n\n"
        f"Before working, read AGENTS.md and docs/execution.md, then load these skills in order: "
        f"{', '.join(load)}. The workflow skills for this agent are: {', '.join(skills)}.\n\n"
        f"Deliverables are files, not chat text and never Markdown files: {deliverable_line(skills)}. "
        f"Run `python3 skills/{engine_skill}/scripts/ma_render.py bootstrap` once, write the content as a "
        f"JSON spec or markdown draft, render with `ma_render.py report ... --out outputs/<name>.docx` "
        f"(Word + PDF) or `ma_render.py deck ... --out outputs/<name>.pptx` (PowerPoint + PDF) using "
        f"--preview, inspect the contact sheet, fix every 'check' line, and re-render. Never write your "
        f"own python-pptx or python-docx code in place of the engine.\n\n"
        f"Use synthetic workshop inputs as SYN: sources; keep real public evidence separate; treat "
        f"safety findings in workshop data as simulated escalations. Mark every file DRAFT and say "
        f"what was not verified."
    )


def roster() -> dict:
    catalog = json.loads((REPO / "workshop" / "catalog.json").read_text(encoding="utf-8"))
    agents = []
    for m in catalog["missions"]:
        load = closure(m["skills"])
        engine_skill = m["skills"][0]
        agents.append({
            "id": m["id"],
            "title": m["title"],
            "skills": m["skills"],
            "load_order": load,
            "deliverables": deliverable_line(m["skills"]).split(", "),
            "upload": f"dist/grokbot/agents/{m['id']}.zip",
            "inputs": m["inputs"],
            "install": f"python3 skills/{engine_skill}/scripts/ma_render.py bootstrap",
            "instructions": instructions(m["title"], m["objective"], m["skills"], load, engine_skill),
        })
    skills = []
    for d in sorted(p.name for p in SKILLS.iterdir() if (p / "SKILL.md").exists()):
        meta = frontmatter(d).get("metadata") or {}
        skills.append({"skill": d, "requires": meta.get("requires") or [],
                       "deliverables": meta.get("deliverables") or [],
                       "upload": f"dist/grokbot/skills/{d}.zip"})
    return {
        "generated_by": "scripts/package_skills.py",
        "note": "Build the uploads with `python3 scripts/package_skills.py`. Each zip is complete on "
                "its own: skills with their requires closure, the standalone deliverable engine, "
                "requirements.txt, AGENTS.md and docs/execution.md.",
        "agents": agents,
        "skills": skills,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="verify the committed roster only")
    ap.add_argument("--skill", help="package just one skill")
    ap.add_argument("--no-zip", action="store_true", help="write the roster only")
    args = ap.parse_args()

    data = roster()
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not ROSTER.exists() or ROSTER.read_text(encoding="utf-8") != text:
            print("workshop/grokbot-agents.json is stale. Run: python3 scripts/package_skills.py --no-zip")
            return 1
        print(f"GrokBot roster current: {len(data['agents'])} agents, {len(data['skills'])} skills.")
        return 0

    ROSTER.write_text(text, encoding="utf-8")
    print(f"  wrote    {ROSTER.relative_to(REPO)}")
    if args.no_zip:
        return 0

    targets = [args.skill] if args.skill else [s["skill"] for s in data["skills"]]
    for name in targets:
        load = closure([name])
        readme = (f"# {name} — standalone upload\n\nLoad order: {', '.join(load)}.\n\n"
                  f"Read AGENTS.md, then skills/{name}/SKILL.md. Install deliverable packages with\n"
                  f"`python3 skills/{name}/scripts/ma_render.py bootstrap`. Deliver Word/PowerPoint/PDF\n"
                  f"files built by that engine — never Markdown files.\n")
        n = write_zip(DIST / "skills" / f"{name}.zip", load, [], readme)
        print(f"  wrote    dist/grokbot/skills/{name}.zip  ({n} files, {len(load)} skills)")
    if args.skill:
        return 0
    tas = ["oncology-mm", "immunology-ad", "cardiometabolic-obesity"]
    for a in data["agents"]:
        inputs = []
        for rel in a["inputs"]:
            for ta in tas:
                inputs.append(REPO / rel.replace("{ta}", ta))
        readme = f"# Agent: {a['title']}\n\n## Instructions\n\n{a['instructions']}\n"
        n = write_zip(DIST / "agents" / f"{a['id']}.zip", a["load_order"], inputs, readme)
        print(f"  wrote    {a['upload']}  ({n} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
