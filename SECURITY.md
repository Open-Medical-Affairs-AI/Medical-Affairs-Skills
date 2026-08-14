# Security and Safety Policy

This project has two categories of report. Both matter; the second is the one
people forget exists.

---

## 1. Software security issues

Report privately via **GitHub Security Advisories** on this repository
(Security → Report a vulnerability). Do not open a public issue.

In scope:

- Command injection or path traversal in any bundled script.
- Unsafe deserialisation, XML entity expansion, or archive extraction.
- Anything that would cause a skill's script to exfiltrate data, write outside
  its working directory, or execute unreviewed remote content.
- Leaked credentials in the repository history.

Out of scope: vulnerabilities in third-party packages (report upstream), and the
fact that skills instruct an AI agent to run scripts — that is the design.

**Response:** acknowledgement within 5 working days, assessment within 10.

---

## 2. Safety issues — the ones specific to this project

A skill that produces plausible, well-formatted, wrong medical content is a
safety problem even though no code is broken. Report these as a public issue
tagged `[safety]` unless the report itself contains sensitive content, in which
case use a private advisory.

Please report:

| What you saw | Why it matters |
|---|---|
| A **fabricated citation** presented as real — a PMID, DOI, or author list that does not resolve | The single most damaging failure mode. `citation-integrity` exists to prevent it; if it got through, that skill has a hole. |
| **Promotional drift** — a skill producing comparative claims, superiority language, or off-label promotion | Medical Affairs output is non-promotional by definition. This is a regulatory exposure, not a style issue. |
| A **missed adverse event pathway** — content describing a possible AE, product complaint, or special situation that the skill did not surface | Reporting clocks start when information reaches a company employee. A skill that fails to flag is actively harmful. |
| **Overclaiming from weak evidence** — causal language from single-arm, retrospective, or FAERS disproportionality data | Presenting a hypothesis-generating signal as an established finding misleads readers who trust the format. |
| **Removal of the DRAFT marking** by the agent itself | The marking is the control that keeps unreviewed content from being used externally. |
| **PHI or real personal data** anywhere in the repository | Report privately. We will purge history. |

Include the prompt, the skill(s) loaded, the model and runtime, and the output.
Redact anything confidential — a paraphrase is fine.

Safety reports take priority over feature work.

---

## Handling data when using this project

The skills are written to work with synthetic, de-identified, or aggregate data.
If you point one at real material:

- Confirm your AI runtime has contractual assurances on training and retention.
- Complete whatever privacy assessment your jurisdiction requires *before* the
  first upload, not after.
- Remember that KOL interaction notes are personal data about a named
  professional even when they contain no patient information.

See `DISCLAIMER.md` for the full conditions of use.

---

## What this project does not do

It does not phone home, collect telemetry, or transmit your content anywhere
except the public APIs a skill explicitly tells you it is querying
(`eutils.ncbi.nlm.nih.gov`, `clinicaltrials.gov`, `api.fda.gov`,
`api.crossref.org`, `api.openalex.org`). Every network call originates from a
script you can read in `skills/*/scripts/`.

If you find a network call that is not documented in the skill's
`metadata.network` field, that is a security bug. Report it.
