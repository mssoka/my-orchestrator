# Perkins briefing — round 3 (FINAL): righttenantry-refcheck-rc2-2

- **PR:** https://github.com/solarity-services/RightTenantry/pull/590 (targets `develop`)
- **Reviewed sha:** `645ae7f4f858f7d9426e219d6b9e172367871820` (head `refcheck-rc2-2`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 3 of 3 (FINAL — after this, the human takes over for merge)
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc2-2-r3` — pinned at exactly the reviewed sha.
- **Spec:** the job briefing + the story spec at `_bmad-output/implementation-artifacts/spec-rc2-2-viewed-application-status-end-to-end.md`. No GitHub issue.
- **prior_findings:** `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc2-2/r2/consolidated.json` (r2 CHANGES_REQUESTED, 1 blocker B1 = CI format gate, on sha `a55481e`).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What changed since r2 (round 3 scope)

r2 (sha `a55481e`) returned CHANGES_REQUESTED with 1 blocker:
- **B1** — CI format gate fails: the new `list_endpoint_renders_viewed_status_test` in `application_integration_test.gleam:342-343` was unformatted (`let assert Ok(entry) =` split across lines); `gleam format --check` fails; CI format step fails; PR can't merge.
Plus W1 (no client-unit test for the reducer's `"viewed"` arm) + notes.

The implementing minion's r2 rework (sha `645ae7f`) reports:
- **B1 (format gate):** FIXED — ran `gleam format`; verified `gleam format --check` clean across all 3 packages (the exact CI gate).
- **W1 (reducer viewed-arm test):** FIXED — added `api_returned_status_update_maps_viewed_test` (dispatches `ApiReturnedStatusUpdate(Ok("viewed"))`, asserts the model status flips to Viewed); lifts the advisory gate to PASS.
- **N1:** FIXED — renamed the stale comparison-CTA test name (Contact now renders for Shortlisted AND Viewed).
- **N3:** correctly rejected as false-positive (balanced parens, verified programmatically); N2/N4 acknowledged as not-defects.
- Verification: `gleam format --check` clean; unit (shared 101 / client 471 / server) + integration 395 green.

### r3 review focus (fix-audit r2, then the delta)

1. **Fix-audit r2 B1:** `gleam format --check` is now genuinely clean across all 3 packages — confirm the formatter move (the `let assert Ok(entry) =` joined) is in place and the CI format gate would pass. (This was the merge-blocker.)
2. **Fix-audit r2 W1:** the reducer viewed-arm client test actually exercises the arm + bites (asserts the status flips to Viewed; a silent revert would fail it).
3. **No-regression / scope:** the rework should be minimal (format + the reducer test + the rename). Re-confirm the lens-guard items still intact (sweep-nudge/bulk-reject exclusion; Contact-CTA merge; pill recolour). No new em-dashes (RT CI ban).
4. **Existing statuses:** still render correctly (no rank/pill/filter regression).

## ⚠️ CRITICAL lens-guard (still in force — 3rd round, don't re-litigate)

- **Do NOT flag** viewed's exclusion from sweep-nudge/bulk-reject (deliberate), the Contact-CTA merge (deliberate), or the pill recolour (the recolour IS the fix). These were confirmed in r1 + r2.
- **Do NOT flag** the additive migration, N3's balanced parens (false-positive), N2 (pre-existing unreachable) or N4 (test-only raw SQL) — all adjudicated in r2.

Legitimate r3 findings: B1/W1 NOT actually fixed (format still fails / the reducer test doesn't bite / in the wrong place), a NEW regression in the 645ae7f delta, em-dashes in copy, or a parse/test regression.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. This is the FINAL round (3 of 3) — after your verdict, the human takes over for merge.
- Save the canonical diff first: `gh pr diff 590 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc2-2/r3/diff.patch`.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = this briefing + the job briefing + the story spec, `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc2-2/r3`, `prior_findings` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc2-2/r2/consolidated.json`. Headless mode owns pane mechanics (dedicated tab, `mm-<lens>-r3`), `<lens>.json` + existence check, one retry per failed lens, big-diff chunking, verification pass, consolidation, `consolidated.json`. Close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes` (note: this is the FINAL round — a CHANGES_REQUESTED here means the human takes over, cap reached); 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`): `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)`; on failure fall back to `gh pr comment 590 --repo solarity-services/RightTenantry --body-file <body.md>` + note `fallback-comment`; else `GH_TOKEN=$TOKEN gh pr review 590 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Body format:
  ```
  ## 🤖 Perkins automated review — round 3 of 3 (FINAL)
  **Job:** righttenantry-refcheck-rc2-2 · **Reviewed sha:** 645ae7f · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed — <rejected> false-positive[, <u> unverified]
  **Prior-round fix audit:** r2 B1 (format gate) <addressed/open> · r2 W1 (reducer viewed-arm test) <addressed/open>

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Final round — fix-audit of r2 B1 (format gate) + W1 (reducer viewed-arm test). After this verdict, the human takes over for merge._
  ```
- Before posting, re-fetch `headRefOid`. If it moved, post anyway + note "reviewed `645ae7f`, head now `<new>` — cap reached; human review".
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc2-2-perkins-r3 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5.
