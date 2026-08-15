# Adapting Skills From Other Projects

How to build on someone else's work without creating a licensing problem for
everyone who adopts yours.

---

## Check the licence of the file, not the repository

A repository-level licence badge tells you nothing about the licence of a
specific file inside it.

We hit this directly. Evaluating an MIT-licensed skills repository for material
to adapt, we found that its `docx` and `pptx` skills were **not** the
repository owner's work and **not** MIT:

```yaml
license: Proprietary. LICENSE.txt has complete terms
metadata:
  skill-author: Anthropic, PBC
  source: https://github.com/anthropics/skills/tree/main/skills/pptx
```

Vendored proprietary skills sitting inside an otherwise-MIT repository. Nothing
improper on anyone's part — the frontmatter says exactly what it is — but a
repository-level assumption would have imported a licence violation into an
Apache-2.0 project, and from there into every organisation that adopted it.

**Read the frontmatter of every file you intend to derive from.**

---

## Compatibility, briefly

| From | Into Apache-2.0 | Requirement |
| --- | --- | --- |
| MIT | Yes | Preserve the copyright notice; attribute |
| BSD-2/3 | Yes | Preserve notices |
| Apache-2.0 | Yes | Preserve NOTICE; state changes |
| CC0 / public domain | Yes | Attribution courteous, not required |
| CC BY | Usually | Attribution required; check the version |
| CC BY-SA | **No** | Copyleft; incompatible with Apache-2.0 |
| GPL / AGPL | **No** | Copyleft |
| Proprietary | **No** | Regardless of where you found it |

Not legal advice. When a decision has consequences, ask a lawyer.

---

## Take architecture, not text

The valuable part of a good skill is rarely its prose. It is the structure — the
order of operations, the gates, the failure catalogue, the thing the author
learned the hard way and encoded.

Copying text imports someone else's domain assumptions along with their
sentences. Rewriting from the architecture forces you to decide whether each
element is right for *your* domain, and usually improves it.

We derived from six MIT-licensed skills and copied no files. One example: an
intake-gate → prohibited-output-language → mandatory-draft-marking →
source-ledger pattern, written for clinical report generation, became our house
safety architecture across every regulated skill — re-scoped for Medical
Affairs, with different gates and a different prohibited-language list.

The debt is real and worth recording either way.

---

## Record it, skill by skill

`THIRD-PARTY-NOTICES.md` names each derived skill, the pattern taken, and the
original. Not a blanket acknowledgement at the bottom of a README.

Also record what you deliberately **did not** use and why. Ours documents the
proprietary `docx`/`pptx` finding, which is more useful to a reader than any
attribution — it tells them to run the same check.

In a regulated industry a compliance reviewer will ask where something came
from. "Somewhere on GitHub" ends the conversation.

---

## Never redistribute licensed content

Distinct from code licensing and easy to get wrong.

Our terminology skill teaches correct use of **MedDRA**, **SNOMED CT**, **ICD**
and the **WHO Drug Dictionary**, and ships **none** of their content. Each
requires a licence we do not hold and adopters may not either.

The skill routes to a human with the licence instead of fabricating codes — an
approach that is both legally clean and, given what a wrong safety code costs,
the right behaviour anyway.

The same applies to copyrighted journal text beyond fair quotation, and to
proprietary guideline content.

---

## If someone adapts your work

Make it easy: a clear per-file licence header, a NOTICE with the attribution
text you want, and a statement of what you consider derivation versus copying.

And if you find your work attributed incorrectly here, open an issue titled
`[attribution]`. Getting it right matters more to us than being right.
