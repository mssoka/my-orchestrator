# Perkins briefing — round 2: righttenantry-refcheck-rc2-3

- **PR:** https://github.com/solarity-services/RightTenantry/pull/591 (targets `develop`)
- **Reviewed sha:** `5d405b6cd1cdac8feb20edaca90c81070ff8985c` (head `refcheck-rc2-3`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 2 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc2-3-r2` — pinned at exactly the reviewed sha.
- **Spec:** the job briefing + the story spec. No GitHub issue.
- **prior_findings:** `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc2-3/r1/consolidated.json` (r1 CHANGES_REQUESTED, 1 blocker B1 = advisory test gate FAIL, on sha `109ec5d`).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What changed since r1 (round 2 scope)

r1 (sha `109ec5d`) returned CHANGES_REQUESTED with 1 blocker:
- **B1** — Advisory test gate FAIL: the headline AC (viewed-PATCH creates reference_call rows) had NO automated pin through the real hook; the 3 HTTP handlers (handle_start/skip/re_enable) + the trigger dispatcher (maybe_trigger_reference_checks) had ZERO direct test coverage. Fix requested: HTTP-level integration tests (happy 200 + cross-tenant 404 + archived 422 + unknown-slot 400 + mid-flight-skip 409) + one e2e viewed-PATCH-creates-rows test.
Plus 5 warnings (incl. W1 skip-racing-concurrent-viewed-trigger).

The implementing minion pushed the fix (sha `5d405b6`). Round 2 verifies it.

### r2 review focus (fix-audit-first, then the delta)

1. **Fix-audit r1 B1:** the HTTP handlers + trigger dispatcher now have direct test coverage — confirm the integration tests genuinely exercise the real hook (not just the DB layer), the 3 handlers are tested (happy + error paths), and the e2e viewed-PATCH-creates-rows test pins the headline AC. The advisory test gate should now PASS.
2. **Fix-audit r1 warnings:** W1 (skip-racing-concurrent-viewed-trigger) addressed? Other warnings?
3. **No-regression / scope:** the rework should be additive (tests + any warning fixes). Re-confirm the lens-guard items (no-migration, post-commit fail-open trigger, idempotency INSERT ON CONFLICT, nothing-sent). No new em-dashes (RT CI ban).

## ⚠️ CRITICAL lens-guard (still in force — 2nd round, don't re-litigate)

- **Do NOT flag** the no-migration (skipped enum already in RC2.1), the post-commit fail-open trigger, the idempotency, or nothing-sent — all confirmed in r1 as deliberate.
- **Do NOT flag** missing production features (leaderboards, save system, etc.) — this is a scoped sprint story.

Legitimate r2 findings: B1 NOT actually fixed (the tests don't cover the real hook / don't bite), a NEW regression in the 5d405b6 delta, em-dashes in copy, or a parse/test regression.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge.
- Save the canonical diff first: `gh pr diff 591 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc2-3/r2/diff.patch`.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = this briefing + the job briefing + the story spec, `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc2-3/r2`, `prior_findings` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc2-3/r1/consolidated.json`. Headless mode owns pane mechanics (dedicated tab, `mm-<lens>-r2`), `<lens>.json` + existence check, one retry per failed lens, big-diff chunking, verification pass, consolidation, `consolidated.json`. Close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`): `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)`; on failure fall back to `gh pr comment 591 --repo solarity-services/RightTenantry --body-file <body.md>` + note `fallback-comment`; else `GH_TOKEN=$TOKEN gh pr review 591 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Body format:
  ```
  ## 🤖 Perkins automated review — round 2 of 3
  **Job:** righttenantry-refcheck-rc2-3 · **Reviewed sha:** 5d405b6 · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed — <rejected> false-positive[, <u> unverified]
  **Prior-round fix audit:** r1 B1 (test gate / HTTP handler coverage) <addressed/open>

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Fix-audit of B1 (HTTP handler + trigger dispatcher test coverage); the deliberate decisions confirmed intact._
  ```
- Before posting, re-fetch `headRefOid`. If it moved, post anyway + note "reviewed `5d405b6`, head now `<new>` — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc2-3-perkins-r2 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5.
