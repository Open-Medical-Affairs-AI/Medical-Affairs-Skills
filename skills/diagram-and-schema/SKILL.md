---
name: diagram-and-schema
description: >-
  Draw the diagrams Medical Affairs actually needs — treatment pathways,
  study schemas, PRISMA flow diagrams, patient journeys, evidence maps,
  decision trees, mechanism-of-action schematics, and governance flows. Use
  when a relationship, sequence or flow would be clearer as a picture than
  as prose, when a protocol needs a study schema, or when someone asks for a
  flowchart or pathway. Emits Mermaid, which renders natively in GitHub and
  several agent runtimes, and falls back to SVG then structured ASCII so a
  diagram is always produced.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.1.0"
  tier: content
  maturity: beta
  requires:
    - medical-affairs-foundations
    - capability-detection
  suggests:
    - consulting-grade-design
  produces: Diagram (Mermaid, SVG or ASCII)
---

# Diagram and Schema

Some things are relationships, and prose describes them badly. A treatment
pathway with four decision points takes a paragraph nobody finishes and a
diagram everybody understands.

## Format choice

**Mermaid first.** It is text, so it diffs in a pull request and can be edited
by someone who cannot use a drawing tool. It renders natively on GitHub, in many
agent runtimes and in most markdown viewers. When it does not render, the source
is still readable.

**SVG** when precise layout matters — a study schema with specific arm widths,
or a poster figure that must scale.

**ASCII** as the floor. Ugly and always available; a reader in a plain terminal
still gets the structure.

## The diagrams worth having

### PRISMA flow diagram

Required for systematic reviews (`systematic-literature-review`). **The numbers
must reconcile** and reviewers check the arithmetic. The builder does the
subtraction and refuses to emit a diagram that does not balance — a PRISMA
diagram whose numbers do not add up is the fastest way to lose a reviewer's
confidence.

### Treatment pathway

Lines of therapy, decision points, and what happens at progression. The one to
get right: **show where practice diverges from the guideline**, because that gap
is usually the interesting part and pathway diagrams normally hide it.

### Study schema

Screening, randomisation, arms, dosing, assessment schedule, endpoints. State
the randomisation ratio and the assessment interval — PFS depends on how often
you look, and a schema that omits the interval hides that.

### Patient journey

Symptom onset → presentation → diagnosis → treatment, with the delays marked.
The delays are the finding; a journey diagram without them is decoration.

### Evidence map

Questions on one axis, evidence strength on the other. Makes gaps visible in a
way a table does not. Feeds `evidence-gap-analysis`.

## Using it

```bash
S=skills/diagram-and-schema/scripts/diagram.py

python3 $S prisma  --spec prisma.json --out flow.mmd
python3 $S prisma  --spec prisma.json --out flow.svg --format svg
python3 $S pathway --spec pathway.json --format ascii
python3 $S --example prisma > prisma.json
```

## Rules

- **Label every arrow.** An unlabelled arrow between two boxes tells you almost
  nothing.
- **Numbers on the flow** where the diagram describes a population.
- **Show exclusions and their reasons**, not just the survivors. The excluded
  branch is where the bias lives.
- **One direction.** Top-to-bottom or left-to-right, not both.
- **Do not encode meaning in colour alone.**
- **Say what the diagram omits.** A simplified pathway is fine; a simplified
  pathway presented as complete is not.

## The look

Diagrams follow `consulting-grade-design`: ink strokes, cloud fills, one teal
accent on the path that matters, oxblood only for safety-relevant nodes.
A diagram with six colours has six competing claims to attention and makes
none.

## Before you finish

Read `house-rules/diagram-and-schema.md`.
