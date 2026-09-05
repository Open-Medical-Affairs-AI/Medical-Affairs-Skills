# Public use, owner-controlled official releases

The repository stays public under Apache-2.0. People may use, modify and distribute
their own copies subject to that license. Only authorized repository roles can
change this official project. Forking does not grant write access upstream.

## Recorded findings on 5 September 2026

- Connected GitHub identity: `vivmuk`; repository metadata reports admin permission.
- Default branch: `claude/medical-affairs-agent-workshop-ttpxhf`.
- `main` and the default branch diverged. The workshop branch merges both histories.
- The rulesets endpoint returned an empty list. Legacy branch-protection read returned
  HTTP 403 because the GitHub integration lacks administration access.
- Therefore existing legacy protection, organization owners, inherited team access,
  app access and collaborator membership are **not fully verified**.
- This change adds CODEOWNERS and governance instructions; it does not activate
  GitHub settings. A committed document cannot enforce repository permissions.

## Owner setup in GitHub

Do this after reviewing and merging the workshop changes. These steps require an
organization/repository administrator using the actual GitHub settings interface.

1. **Organization access:** in organization Settings → People/Teams, retain owner
   roles only for you and explicitly designated co-owners. Give ordinary members
   read access unless more is needed. Review outside collaborators, installed apps,
   deploy keys and automation identities. Do not remove an account without checking
   its purpose. Repository write access and organization ownership are different.
2. **Canonical branch:** bring the reconciled content to `main`, then set `main`
   as the default. Verify README, raw links, Actions and open PR bases. Preserve
   the development branches until their work is confirmed merged.
3. **Branch rules:** create an active ruleset for the default/release branch.
   Require pull requests, code-owner review, resolved discussions and passing
   required CI checks. Block force pushes and deletion. Restrict changes to
   authorized maintainers and inspect all bypass actors.
4. **Required checks:** use the actual check names shown on the tested PR:
   Skill structure and sample data; API clients (offline fixtures); Graceful
   degradation; Workshop behavior. Do not require the optional live API check,
   which can fail because a public service is unavailable.
5. **Solo owner workflow:** GitHub does not let you approve your own PR. If you
   are the only reviewer, either use a trusted designated reviewer or a narrowly
   scoped owner bypass with a documented self-review. Do not grant every admin,
   contributor or application a broad bypass for convenience.
6. **Delegates:** add only approved usernames/teams to CODEOWNERS and grant the
   necessary repository role. Protect `.github/` itself. Multiple owners on a line
   mean any one can satisfy code-owner review, not unanimous approval.
7. **Releases:** protect version tags against unauthorized creation/update/deletion.
   Publish an October release after rehearsal, and distribute that version for
   consistent workshop behavior. Update it deliberately if public APIs change.

## Acceptance check

Confirm a non-maintainer can read/download/fork but cannot push upstream. Confirm
an authorized collaborator change follows the intended review path and cannot
silently edit governance. Confirm the owner still has an intentional recovery route.
Review the rendered ruleset, bypass list and effective access, not just this file.

Official guidance: [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners),
[rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets),
[Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
