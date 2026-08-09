# Perkins briefing — round 2: righttenantry-refcheck-rc2-2

- **PR:** https://github.com/solarity-services/RightTenantry/pull/590 (targets `develop`)
- **Reviewed sha:** `a55481ef3dae6ee07ecbade0133b1e71964b8d4b` (head `refcheck-rc2-2`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 2 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc2-2-r2` — pinned at exactly the reviewed sha.
- **Spec:** the job briefing + the story spec at `_bmad-output/implementation-artifacts/spec-rc2-2-viewed-application-status-end-to-end.md`. No GitHub issue.
- **prior_findings:** `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc2-2/r1/consolidated.json` (r1 CHANGES_REQUESTED, 1 blocker B1, 15/16 confirmed, on sha `dc1e08f`).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What changed since r1 (round 2 scope)

r1 (sha `dc1e08f`) returned CHANGES_REQUESTED with 1 blocker:
- **B1** — the leaderboard list endpoint (`server/src/vacancy/application_list_handler.gleam:86-95`, GET `/api/v1/vacancies/:id/applications`) had NO `"viewed"` arm in its status-string→enum case → viewed rows hit the `unknown ->` fallback → coerced to `application.Submitted` (slate pill rank 0, not navy Viewed rank 3) + logged "Unknown application status: viewed" on every leaderboard load. Violated AC4. **Fix expected:** add `"viewed" -> application.Viewed` between shortlisted and approved.

The implementing minion pushed the fix (new sha `a55481e`). Round 2 verifies it.

### r2 review focus (fix-audit-first, then the delta)

1. **Fix-audit r1 B1:** the leaderboard handler now has the `"viewed"` arm — confirm it maps to `application.Viewed` correctly, viewed rows render the navy pill at rank 3 (not Submitted/rank 0), the spurious "Unknown application status: viewed" log is gone, and AC4 is satisfied. Verify the fix is in the RIGHT place (the leaderboard/list handler, not just the detail handler — r1 B1 was specifically the list endpoint).
2. **No-regression / scope:** the fix should be MINIMAL (just the viewed arm). Did the rework touch anything else? Re-confirm the lens-guard items (the deliberate decisions from r1) are still intact: viewed EXCLUDED from sweep-nudge/bulk-reject; viewed MERGED into Shortlisted Contact CTA; shared `status_pill` recolour. No new em-dashes in copy (RT CI ban).
3. **Existing statuses:** Submitted/Reviewing/Shortlisted/Approved/Reject/AutoClosed still render correctly (no rank/pill/filter regression from the viewed addition).

## ⚠️ CRITICAL lens-guard (still in force)

- **Do NOT flag "viewed should be in sweep-nudge/bulk-reject"** — its EXCLUSION is deliberate (a viewed applicant is engaged, not auto-rejectable).
- **Do NOT flag "viewed merged into the Shortlisted Contact CTA"** — deliberate.
- **Do NOT flag the shared `status_pill` recolour** — it realigns a drift to the brand doc (the recolour IS the fix).
- **Do NOT flag the migration** — additive/idempotent; existing values unchanged.

Legitimate r2 findings: B1 NOT actually fixed (the viewed arm missing/wrong, or in the wrong handler), the fix introduced a regression (broke an existing status / the leaderboard / a filter), a NEW issue in the a55481e delta, em-dashes in copy, or a parse/test regression.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge.
- Save the canonical diff first: `gh pr diff 590 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc2-2/r2/diff.patch`.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = this briefing + the job briefing + the story spec (no GitHub issue), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc2-2/r2`, `prior_findings` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc2-2/r1/consolidated.json`. Headless mode owns pane mechanics (dedicated tab, `mm-<lens>-r2`), `<lens>.json` + existence check, one retry per failed lens, big-diff chunking, verification pass, consolidation, `consolidated.json`. Close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`): `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)`; on failure fall back to `gh pr comment 590 --repo solarity-services/RightTenantry --body-file <body.md>` + note `fallback-comment`; else `GH_TOKEN=$TOKEN gh pr review 590 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Body format:
  ```
  ## 🤖 Perkins automated review — round 2 of 3
  **Job:** righttenantry-refcheck-rc2-2 · **Reviewed sha:** a55481e · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed — <rejected> false-positive[, <u> unverified]
  **Prior-round fix audit:** r1 B1 (leaderboard viewed arm) <addressed/open>

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Fix-audit of B1 (viewed leaderboard arm); the deliberate decisions (sweep-nudge exclusion, Contact-CTA merge, pill recolour) are confirmed intact._
  ```
- Before posting, re-fetch `headRefOid`. If it moved, post anyway + note "reviewed `a55481e`, head now `<new>` — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc2-2-perkins-r2 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5.
