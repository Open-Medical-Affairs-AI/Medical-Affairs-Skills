#!/usr/bin/env python3
"""Generate SKILLS-INDEX.md from the skills' frontmatter.

Why this exists: SKILL.md frontmatter is how Claude and other Agent-Skills
runtimes discover skills, but an agent that is simply pointed at this
repository URL — Grok, ChatGPT, a coding agent — has no such mechanism. It
reads AGENTS.md, and AGENTS.md points here. Generating the index rather than
hand-maintaining it means the two views of the library cannot drift apart.

validate_skills.py fails CI if the committed index does not match this output.

Usage:
    python3 scripts/build_index.py            # write SKILLS-INDEX.md
    python3 scripts/build_index.py --check    # exit 1 if it would change
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required. Install it with:  pip install pyyaml")

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO / "skills"
INDEX = REPO / "SKILLS-INDEX.md"

TIER_ORDER = ["orchestrator", "foundation", "primitive", "data", "workflow", "content"]

TIER_HEADINGS = {
    "orchestrator": (
        "Orchestrator",
        "Start here if you have been handed a job and do not know which skill "
        "does it. This one routes.",
    ),
    "foundation": (
        "Foundation — the core",
        "`medical-affairs-foundations` loads on every Medical Affairs task, "
        "without exception: it carries the compliance boundary and the "
        "adverse-event escalation rule. The others load when the job reaches "
        "them — evidence appraisal when interpreting study data, citation "
        "integrity when the deliverable will carry references, quality review "
        "at stage 4, capability detection when producing a file.",
    ),
    "primitive": (
        "Reasoning primitives — composed by the workflows",
        "Usually reached as a dependency rather than chosen: the workflow "
        "skills call these to do the actual thinking. `strategic-analysis` is "
        "the exception and is routable directly, for a request that is purely "
        "\"so what should we do about it\" with no workflow behind it.",
    ),
    "data": (
        "Data and search — live external evidence",
        "These retrieve or prepare public, supplied and local evidence. Public literature, trial registry, and label/safety "
        "databases need network access; local data and supplied transcripts do not. See docs/api-setup.md.",
    ),
    "workflow": (
        "Workflows — the jobs",
        "One per recurring Medical Affairs job. Each produces a named "
        "deliverable and runs the six-stage execution contract in AGENTS.md.",
    ),
    "content": (
        "Content generation — the deliverables",
        "Turn analysis into the artefact somebody actually receives: a deck, "
        "a manuscript, an abstract, a poster, a lay summary, a review pack.",
    ),
}

HEADER = """<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Regenerate with: python3 scripts/build_index.py
     CI fails if this file is out of sync with the skills' frontmatter. -->

# Skills Index

Every skill in this library, what it is for, and what it needs. If you are an
AI agent that has just been pointed at this repository, read [AGENTS.md](AGENTS.md)
first — it explains how to run these. This file is the catalogue.

**How to read the columns**

- **Requires** — what this skill cannot run correctly without. Load all of it.
- **Suggests** — where the job may go next. Follow one only when the work
  actually goes there; loading every suggestion pulls a large closure into
  context before any work starts.
- **Produces** — the named deliverable. Skills without one are reasoning components.
- **Network** — external hosts the skill needs. Blank means no direct host is declared; dependencies or the host may still need access.

"""

FOOTER = """
---

## Loading order

For any real task the order that works is:

1. **`medical-affairs-foundations`** — always, on every job.
2. **Orchestrator** — if you do not already know which workflow you need.
3. **One workflow** — the job itself.
4. **Whatever that workflow *requires*** — the short list it cannot run without.
5. **The rest of the core, when the job reaches it** — `evidence-appraisal` when
   interpreting study data, `citation-integrity` when the deliverable will carry
   references, `deliverable-quality-review` at stage 4.
6. **One content skill** — only once the analysis is done and reviewed.

**`suggests` is not a load list.** It names skills the job may reach into;
follow one when the work actually goes there, not in advance. Dependencies load
transitively, so speculative loading pulls a large closure into context before
any work has started.

Loading a content skill before the analysis is finished is the most common
failure mode. It produces a well-formatted document with nothing behind it.

## Overrides

Every skill reads `house-rules/<skill-name>.md` before it produces anything.
That is where your organisation's SOPs, terminology, and standards go. Rules
there beat the defaults in the skill. You should not need to fork this
repository to make it behave like your company.
"""


def load_all() -> dict[str, dict]:
    skills: dict[str, dict] = {}
    if not SKILLS_DIR.exists():
        return skills
    for d in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        f = d / "SKILL.md"
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        end = text.find("\n---\n", 4)
        if end == -1:
            continue
        try:
            fm = yaml.safe_load(text[4:end])
        except yaml.YAMLError:
            continue
        if isinstance(fm, dict):
            skills[d.name] = fm
    return skills


def _cell(value) -> str:
    """Render a frontmatter value into a table cell without breaking the table."""
    if not value:
        return "—"
    if isinstance(value, list):
        return "<br>".join(f"`{v}`" for v in value)
    return str(value).replace("|", "\\|")


def _summary(fm: dict) -> str:
    """Enough of the description to route on: what it does, and when.

    One sentence is not enough. `competitive-intelligence` opens with
    "continuously", which reads as excluding the single-announcement case it in
    fact handles; `evidence-synthesis` opens without any trigger at all. A
    cold-start routing test misrouted both from the index alone. So take the
    opening sentence plus the first one that says when to use it, which by the
    library's own description convention starts "Use ".
    """
    desc = " ".join(str(fm.get("description", "")).split())
    parts, buf = [], desc
    for _ in range(6):
        cut = min((buf.find(s) for s in (". ", "? ") if s in buf), default=-1)
        if cut == -1:
            parts.append(buf)
            break
        parts.append(buf[: cut + 1])
        buf = buf[cut + 2 :]

    out = parts[:1]
    for sentence in parts[1:]:
        out.append(sentence)
        if sentence.startswith(("Use ", "Load ")):
            break
    else:
        out = parts[:1]          # no trigger sentence found; keep it short

    return " ".join(out).replace("|", "\\|")


def render_index(skills: dict[str, dict]) -> str:
    out = [HEADER]
    by_tier: dict[str, list[tuple[str, dict]]] = {}
    for name, fm in skills.items():
        tier = (fm.get("metadata") or {}).get("tier", "workflow")
        by_tier.setdefault(tier, []).append((name, fm))

    total = len(skills)
    out.append(f"**{total} skills.**\n")

    for tier in TIER_ORDER:
        entries = sorted(by_tier.get(tier, []))
        if not entries:
            continue
        heading, blurb = TIER_HEADINGS.get(tier, (tier.title(), ""))
        out.append(f"## {heading}\n")
        if blurb:
            out.append(f"{blurb}\n")
        out.append("| Skill | What it does | Requires (load) | Suggests (follow if needed) | Produces | Network |")
        out.append("| --- | --- | --- | --- | --- | --- |")
        for name, fm in entries:
            meta = fm.get("metadata") or {}
            out.append(
                f"| [`{name}`](skills/{name}/SKILL.md) "
                f"| {_summary(fm)} "
                f"| {_cell(meta.get('requires'))} "
                f"| {_cell(meta.get('suggests'))} "
                f"| {_cell(meta.get('produces'))} "
                f"| {_cell(meta.get('network'))} |"
            )
        out.append("")

    # Any tier not in TIER_ORDER would silently vanish; surface it instead.
    for tier in sorted(set(by_tier) - set(TIER_ORDER)):
        out.append(f"## {tier} (unrecognised tier)\n")
        for name, _ in sorted(by_tier[tier]):
            out.append(f"- `{name}`")
        out.append("")

    out.append(FOOTER)
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--check",
        action="store_true",
        help="do not write; exit 1 if the committed index is stale",
    )
    args = ap.parse_args()

    skills = load_all()
    rendered = render_index(skills)

    if args.check:
        current = INDEX.read_text(encoding="utf-8") if INDEX.exists() else ""
        if current.strip() != rendered.strip():
            print("SKILLS-INDEX.md is out of date. Run: python3 scripts/build_index.py")
            return 1
        print("SKILLS-INDEX.md is current.")
        return 0

    INDEX.write_text(rendered, encoding="utf-8")
    print(f"Wrote {INDEX.relative_to(REPO)} ({len(skills)} skills).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
