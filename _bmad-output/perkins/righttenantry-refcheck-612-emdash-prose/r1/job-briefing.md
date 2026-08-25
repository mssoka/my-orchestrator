# Briefing — righttenantry-refcheck-612-emdash-prose (issue #612 — em-dash exemptions ship em-dashes to landlords)

- **Job id:** `righttenantry-refcheck-612-emdash-prose`
- **Repo:** RightTenantry · **Base:** `develop` · **Slug:** `refcheck-612-emdash-prose`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow); your own adversarial pass
  uses `bmad-review-adversarial-general` + `bmad-review-edge-case-hunter`.
- **Perkins:** `pr_review: 1` (user-facing copy + lint-scope expansion).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `develop` @ 758f1d8. A sibling job (`refcheck-611-panel-persist`) may merge
  while you work — disjoint areas; rebase onto origin/develop if it lands first.
- **CI NOTE:** GitHub Actions billing is blocked at the account level — your PR's CI will
  be red/not-started until the user fixes it. NOT a code failure. Run the FULL local
  suite green (`make test-all`) before opening the PR; Perkins verifies locally.

## Mission — fix issue #612 (the issue IS the spec — read it in full first)

**The bug (bug-hunt finding, user-filed):** 16 spec-verbatim em-dash exemptions in the
refcheck copy still ship em-dashes to LANDLORDS — the global em-dash ban (from #607,
`scripts/lint_em_dash.py`) exempts spec-verbatim strings by owner name with provenance
notes, but those 16 exemptions are public, landlord-facing prose. The ban must extend
to ALL public prose — spec-verbatim or not.

**The fix:**
1. Re-work the 16 landlord-facing strings to be em-dash-free (dash-free composed
   labels, following the #607 pattern that moved compositions into `copy.gleam`).
   Spec-verbatim provenance does NOT justify an em-dash in prose a landlord reads.
2. Extend the lint so this class cannot recur: the exemption rule must not cover
   public-prose strings — if a spec-verbatim exemption remains, it must be for
   internal/spec-mirroring text ONLY, and the lint's exemption logic must encode that
   boundary (an em-dash in a user-facing string fails the lint regardless of owner).
3. Preserve the #607 guard properties: escaped quotes handled, log-call argument
   regions exempt, negative controls still pass.

**Acceptance:**

1. Zero em-dashes reach landlord-facing prose: grep + lint prove it; the 16 strings
   re-composed and pinned by copy tests.
2. `lint_em_dash.py` fails on any em-dash in a user-facing string literal — including
   the previously-exempt ones; negative controls re-verified (the lint still catches
   the old forms).
3. Full `make test-all` green; PR body lists the 16 re-composed strings + the
   exemption-boundary rule; PR closes issue #612 (`Fixes #612`).
4. Local suite green; Perkins verifies locally (CI billing blocked).

**Scope guard:** the 16 strings + the lint boundary only. No input-path work (that's
#611's job), no other copy sweep, no feature changes.

## Dispatch parameters

```
repo: RightTenantry
repo_root: /Users/moses/code/RightTenantry
slug: refcheck-612-emdash-prose
base: develop
model: deepseek/deepseek-v4-flash
github_issue: 612
pr_review: 1
```
