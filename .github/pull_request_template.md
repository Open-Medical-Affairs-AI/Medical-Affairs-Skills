## What this changes

<!-- One or two sentences. What is different after this merges? -->

## Type of change

- [ ] New skill
- [ ] Change to an existing skill
- [ ] Sample data / workshop material
- [ ] Scripts, validation, or CI
- [ ] Documentation
- [ ] Safety or compliance fix

## Triggering

<!-- Skip if this PR does not touch a SKILL.md description. -->

**What should load this skill:**

**What should NOT load it** (the near-misses that would otherwise steal the trigger):

## Medical Affairs review

- [ ] The reasoning would hold up to a senior MA colleague reading it cold
- [ ] Compliance boundaries are intact (non-promotional, off-label handled only via unsolicited-request pathway, approval status stated)
- [ ] AE / product-complaint detection is present if this touches field notes, KOL interactions, or medical information
- [ ] Evidence claims are appraised, not just repeated — no causal language from single-arm, retrospective, or FAERS data
- [ ] Any standard or guideline referenced is current, and named with its version/year

## Checks

```bash
python3 scripts/build_index.py
python3 scripts/validate_skills.py
python3 scripts/selftest_apis.py
```

- [ ] All three pass locally
- [ ] `metadata.version` bumped if behaviour changed
- [ ] `CHANGELOG.md` updated if a user would notice the change
- [ ] `house-rules/<skill>.md` exists for any new skill

## Data and licensing

- [ ] No PHI, no personal data, no employer-confidential material
- [ ] Any new sample data is fictional and carries a `SYNTHETIC DATA` banner
- [ ] No licensed terminology content (MedDRA, SNOMED CT, WHO Drug Dictionary)
- [ ] Derived work is recorded in `THIRD-PARTY-NOTICES.md`, with the licence of the **specific file** checked — not the repository badge
- [ ] I have the right to contribute this under Apache-2.0

## Anything you want a reviewer to look at hardest

<!-- Where are you least confident? -->
