#!/usr/bin/env python3
"""Validate every skill in this repository.

This runs in CI on every push and is the thing that keeps a growing,
multi-contributor skill library from quietly rotting. It checks the boring
structural properties that are easy to get wrong and expensive to discover
later: frontmatter that a skill loader can actually parse, dependencies that
resolve, links that are not broken, and sample data that is unmistakably
synthetic.

Usage:
    python3 scripts/validate_skills.py            # validate everything
    python3 scripts/validate_skills.py --strict   # treat warnings as errors
    python3 scripts/validate_skills.py --skill pubmed-search

Exit code 0 = clean, 1 = errors found.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit(
        "PyYAML is required to validate skills.\n"
        "Install it with:  pip install pyyaml"
    )

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO / "skills"
HOUSE_RULES_DIR = REPO / "house-rules"
WORKSHOP_DATA = REPO / "workshop" / "data"

VALID_TIERS = {
    "foundation",
    "primitive",
    "data",
    "workflow",
    "content",
    "orchestrator",
}
VALID_MATURITY = {"stable", "beta", "experimental"}

# Description bounds. Too short and the agent cannot tell when to load the
# skill; too long and it crowds out every other skill in the selection context.
DESC_MIN = 120
DESC_MAX = 1400

# Body length. Progressive disclosure means depth belongs in references/,
# not in the always-loaded body.
BODY_WARN = 520
BODY_MAX = 900

SYNTHETIC_BANNER = "SYNTHETIC DATA"
SYNTHETIC_SCAN_LINES = 8

# Phrases that signal a description written for a human reader rather than for
# an agent deciding whether to load the skill.
WEAK_DESC_OPENERS = ("this skill", "a skill", "skill for", "helps you")


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")

    @property
    def ok(self) -> bool:
        return not self.errors


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    """Split a SKILL.md into (frontmatter dict, body).

    Raises ValueError with a message aimed at whoever has to fix it.
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("file does not begin with a '---' frontmatter fence")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("frontmatter opening fence is never closed with '---'")
    raw = text[4:end]
    body = text[end + 5 :]
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise ValueError(f"frontmatter is not valid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return data, body


def check_frontmatter(name: str, fm: dict, rep: Report) -> None:
    where = f"skills/{name}/SKILL.md"

    # --- required top-level fields -------------------------------------
    for key in ("name", "description", "license"):
        if key not in fm:
            rep.error(where, f"missing required frontmatter field '{key}'")

    if fm.get("name") != name:
        rep.error(
            where,
            f"frontmatter name '{fm.get('name')}' does not match directory "
            f"name '{name}' — skill loaders resolve by directory, so these "
            f"must agree",
        )

    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        rep.error(where, f"'{name}' must be lowercase-hyphenated")

    if fm.get("license") != "Apache-2.0":
        rep.error(
            where,
            f"license is '{fm.get('license')}' but this repository ships "
            f"Apache-2.0; if this skill is derived from other work, record "
            f"that in THIRD-PARTY-NOTICES.md rather than changing the license",
        )

    # --- description ----------------------------------------------------
    desc = fm.get("description", "")
    if isinstance(desc, str) and desc:
        n = len(desc)
        if n < DESC_MIN:
            rep.error(
                where,
                f"description is {n} chars; under {DESC_MIN} it rarely carries "
                f"enough trigger context for an agent to select the skill",
            )
        elif n > DESC_MAX:
            rep.error(
                where,
                f"description is {n} chars, over the {DESC_MAX} limit; move "
                f"detail into the body",
            )
        low = desc.lower().lstrip()
        if low.startswith(WEAK_DESC_OPENERS):
            rep.warn(
                where,
                "description opens with a weak self-referential phrase; lead "
                "with what it does and when to use it",
            )
        if " use " not in low and " when " not in low:
            rep.warn(
                where,
                "description does not appear to state WHEN to trigger; agents "
                "under-trigger skills, so name the situations explicitly",
            )

    # --- metadata block --------------------------------------------------
    meta = fm.get("metadata")
    if not isinstance(meta, dict):
        rep.error(where, "missing 'metadata' mapping in frontmatter")
        return

    if "version" not in meta:
        rep.error(where, "metadata.version is required (downstream teams pin it)")
    elif not re.fullmatch(r"\d+\.\d+\.\d+", str(meta["version"])):
        rep.error(
            where, f"metadata.version '{meta['version']}' must be semver x.y.z"
        )

    tier = meta.get("tier")
    if tier not in VALID_TIERS:
        rep.error(
            where,
            f"metadata.tier '{tier}' must be one of {sorted(VALID_TIERS)}",
        )

    maturity = meta.get("maturity", "stable")
    if maturity not in VALID_MATURITY:
        rep.error(
            where,
            f"metadata.maturity '{maturity}' must be one of "
            f"{sorted(VALID_MATURITY)}",
        )

    if tier in {"workflow", "content"} and not meta.get("produces"):
        rep.error(
            where,
            "metadata.produces is required for workflow and content skills — "
            "a skill without a named deliverable is a topic, not a job",
        )

    for key in ("requires", "network", "python"):
        if key in meta and not isinstance(meta[key], list):
            rep.error(where, f"metadata.{key} must be a list")


def check_dependencies(skills: dict[str, dict], rep: Report) -> None:
    """Every declared dependency must resolve, and the graph must be acyclic."""
    for name, fm in skills.items():
        where = f"skills/{name}/SKILL.md"
        requires = (fm.get("metadata") or {}).get("requires") or []
        for dep in requires:
            if dep == name:
                rep.error(where, f"skill requires itself ('{dep}')")
            elif dep not in skills:
                rep.error(
                    where,
                    f"metadata.requires names '{dep}', which is not a skill in "
                    f"this repository",
                )

    # Cycle detection over the requires graph.
    graph = {
        n: [d for d in ((fm.get("metadata") or {}).get("requires") or []) if d in skills]
        for n, fm in skills.items()
    }
    WHITE, GREY, BLACK = 0, 1, 2
    colour = dict.fromkeys(graph, WHITE)

    def visit(node: str, trail: list[str]) -> None:
        colour[node] = GREY
        for nxt in graph.get(node, []):
            if colour[nxt] == GREY:
                cycle = " -> ".join(trail + [node, nxt])
                rep.error("dependency graph", f"circular requires: {cycle}")
            elif colour[nxt] == WHITE:
                visit(nxt, trail + [node])
        colour[node] = BLACK

    for node in graph:
        if colour[node] == WHITE:
            visit(node, [])


LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
BACKTICK_PATH_RE = re.compile(r"`((?:scripts|references|assets)/[\w./-]+)`")


def check_body(name: str, body: str, skill_dir: Path, rep: Report) -> None:
    where = f"skills/{name}/SKILL.md"
    lines = body.splitlines()

    if len(lines) > BODY_MAX:
        rep.error(
            where,
            f"body is {len(lines)} lines, over the hard limit of {BODY_MAX}; "
            f"move depth into references/",
        )
    elif len(lines) > BODY_WARN:
        rep.warn(
            where,
            f"body is {len(lines)} lines; past ~{BODY_WARN} the always-loaded "
            f"context starts crowding out the actual task",
        )

    # Relative links must resolve.
    for target in LINK_RE.findall(body):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        clean = target.split("#", 1)[0]
        if not clean:
            continue
        resolved = (skill_dir / clean).resolve() if not clean.startswith("/") else (REPO / clean.lstrip("/"))
        if not resolved.exists():
            rep.error(where, f"broken relative link: {target}")

    # Backticked script/reference paths must exist too — these are how skills
    # tell the agent what to run, and a stale one sends it down a dead end.
    for target in set(BACKTICK_PATH_RE.findall(body)):
        if not (skill_dir / target).exists():
            rep.error(where, f"references a bundled file that does not exist: {target}")

    if "house-rules/" not in body:
        rep.warn(
            where,
            "body never points at house-rules/; adopters need the override "
            "hook or they will fork the skill instead",
        )


def check_house_rules(skills: dict[str, dict], rep: Report) -> None:
    if not HOUSE_RULES_DIR.exists():
        rep.error("house-rules/", "directory is missing")
        return
    marker = "YOUR RULES"
    for name in skills:
        f = HOUSE_RULES_DIR / f"{name}.md"
        if not f.exists():
            rep.error("house-rules/", f"no house-rules file for skill '{name}'")
        elif marker not in f.read_text(encoding="utf-8"):
            rep.error(
                f"house-rules/{name}.md",
                f"missing the '{marker}' edit marker that tells participants "
                f"where to write",
            )


def check_synthetic_data(rep: Report) -> None:
    """Sample data must be unmistakably synthetic, on every single file.

    This is the check that stops someone dropping a real field-insight export
    into the workshop pack.
    """
    if not WORKSHOP_DATA.exists():
        return
    exts = {".md", ".csv", ".json", ".jsonl", ".txt", ".yaml", ".yml"}
    for f in sorted(WORKSHOP_DATA.rglob("*")):
        if not f.is_file() or f.suffix.lower() not in exts:
            continue
        rel = f.relative_to(REPO)
        try:
            head = "".join(
                f.read_text(encoding="utf-8").splitlines(keepends=True)[
                    :SYNTHETIC_SCAN_LINES
                ]
            )
        except UnicodeDecodeError:
            rep.error(str(rel), "is not valid UTF-8")
            continue
        if SYNTHETIC_BANNER not in head.upper():
            rep.error(
                str(rel),
                f"missing a '{SYNTHETIC_BANNER}' banner in the first "
                f"{SYNTHETIC_SCAN_LINES} lines",
            )
        if f.suffix.lower() in {".json", ".jsonl"}:
            try:
                text = f.read_text(encoding="utf-8")
                if f.suffix.lower() == ".json":
                    json.loads(text)
                else:
                    for i, line in enumerate(text.splitlines(), 1):
                        if line.strip():
                            json.loads(line)
            except json.JSONDecodeError as exc:
                rep.error(str(rel), f"invalid JSON: {exc}")


def check_index_is_current(skills: dict[str, dict], rep: Report) -> None:
    """A stale index is worse than no index — agents route off it."""
    index = REPO / "SKILLS-INDEX.md"
    if not index.exists():
        rep.error("SKILLS-INDEX.md", "is missing; run scripts/build_index.py")
        return
    try:
        sys.path.insert(0, str(REPO / "scripts"))
        from build_index import render_index  # type: ignore
    except Exception as exc:  # pragma: no cover
        rep.warn("SKILLS-INDEX.md", f"could not import build_index.py ({exc})")
        return
    if index.read_text(encoding="utf-8").strip() != render_index(skills).strip():
        rep.error(
            "SKILLS-INDEX.md",
            "is out of date — regenerate it with 'python3 scripts/build_index.py'",
        )


def load_skills(only: str | None, rep: Report) -> dict[str, dict]:
    skills: dict[str, dict] = {}
    if not SKILLS_DIR.exists():
        rep.error("skills/", "directory is missing")
        return skills
    for d in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        if only and d.name != only:
            continue
        skill_md = d / "SKILL.md"
        if not skill_md.exists():
            rep.error(f"skills/{d.name}/", "has no SKILL.md")
            continue
        try:
            fm, body = parse_frontmatter(skill_md)
        except ValueError as exc:
            rep.error(f"skills/{d.name}/SKILL.md", str(exc))
            continue
        skills[d.name] = fm
        check_frontmatter(d.name, fm, rep)
        check_body(d.name, body, d, rep)
    return skills


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    ap.add_argument("--skill", help="validate a single skill by directory name")
    args = ap.parse_args()

    rep = Report()
    skills = load_skills(args.skill, rep)

    if not args.skill:
        check_dependencies(skills, rep)
        check_house_rules(skills, rep)
        check_synthetic_data(rep)
        check_index_is_current(skills, rep)

    for w in rep.warnings:
        print(f"  warn   {w}")
    for e in rep.errors:
        print(f"  ERROR  {e}")

    n = len(skills)
    print(
        f"\n{n} skill{'s' if n != 1 else ''} checked · "
        f"{len(rep.errors)} error(s) · {len(rep.warnings)} warning(s)"
    )

    if rep.errors or (args.strict and rep.warnings):
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
