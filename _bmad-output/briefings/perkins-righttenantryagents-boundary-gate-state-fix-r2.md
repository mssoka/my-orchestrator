# Perkins briefing — round 2 (fix-audit): righttenantryagents-boundary-gate-state-fix

- **PR:** https://github.com/solarity-services/RightTenantryAgents/pull/173 (targets `develop`)
- **Reviewed sha:** `b1ebd960691ec880739de171a512e1cd1b68fdb8` (short `b1ebd96`; commit "fix(compliance): address Perkins r1 on #173 (B1+W1+W2)"; r1 was `39443b2`)
- **repo_root:** `/Users/moses/code/RightTenantryAgents`
- **Round:** 2 of 3 — **fix-audit** of r1's CHANGES_REQUESTED
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantryAgents/perkins-boundary-gate-state-fix-r2` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantryagents-boundary-gate-state-fix.md` + issue #172.
- **prior_findings:** `/Users/moses/code/_bmad-output/perkins/righttenantryagents-boundary-gate-state-fix/r1/consolidated.json` (r1 = CHANGES_REQUESTED: 1 blocker / 2 warnings / 6 notes; 9/10 confirmed). This is a **re-review / fix-audit** — run the fix audit FIRST against prior findings, then scan the delta for new issues.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **Model:** zai-coding-cn/glm-5.2 (kimi quota down — sanctioned fallback).

## What changed since r1 (the rework under review)

The impl minion addressed ALL of r1's findings in `b1ebd96`:
- **B1 (r1 blocker):** restored the stable telemetry event name `compliance.review_unparseable` (a drive-by codespell sed had renamed it to `review_unparsable`, breaking the BQ/Sentry event-name contract + `test_unparseable_review_emits_failed_rollup`). Added `unparseable` to `[tool.codespell] ignore-words-list` (the token's spelling is intentional frozen vocabulary — a stable telemetry contract; prose keeps standard spelling).
- **W1 (r1):** added producer-path tests — `test_verification_compliance_judge` + `test_final_compliance_reviewer` drive `log_boundary/final_compliance_review` and assert the verdict stamp lands off the judge's OWN ctx (the independent witness).
- **W2 (r1):** hardened the defensive cross-check in both `finalize_*_gate` guards to require BOTH `passed` AND `violation_count == 0` (was `passed` alone) so an inconsistent stamp (passed=True but violations>0) can never mask a real violation on the safety path. Added W2 tests for both gates.
- Suite: 2049 passed (2041-after-B1-break + restored test + 7 new W1/W2); codespell + ruff + pre-commit clean. Core fix untouched (the state-view reads).

## ⚠️ CRITICAL lens-guards (carried from r1 — verify, don't re-litigate)

- **THE LOAD-BEARING INVARIANT (both directions):** genuinely-missing judge → still fails closed; clean stamp + None review → does NOT abort; and NOW: an INCONSISTENT stamp (passed=True but violation_count>0) → still fails closed (the W2 hardening). Verify all three directions with the r2 code.
- **B1's fix must be complete + the contract intact:** `compliance.review_unparseable` restored everywhere the contract expects (the telemetry writer + the rollup/evidence queries + the test), the codespell ignore-word is in place, and no OTHER stable token was renamed by the same sed (grep for `unparsable` vs `unparseable` in the event-name context).
- **The W1 producer tests must be REAL:** they drive the actual `log_boundary/final_compliance_review` callbacks (not hand-seeded stamps) and assert the stamp's fields (passed, parseable, violation_count, judge_kind, run_id) off the judge's own ctx.
- **The W2 hardening must not break the clean path:** the `violation_count == 0` requirement must NOT make a legitimately-clean verdict (0 violations) fail-close, and must catch an inconsistent stamp. Verify the W2 tests cover both.
- **The core fix (state-view reads) unchanged + still correct** — the r1 verification (adk-cheatsheet + empirical repro) stands; confirm the r2 diff didn't touch the gate reads or `finalize_*_gate` signatures beyond the W2 guard.
- **No new regressions** in the delta (grep the r2 diff for anything beyond the B1/W1/W2 scope).
- **Suite claim:** 2049 passed — verify real (not skipped/tautological), codespell/ruff clean.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 173 --repo solarity-services/RightTenantryAgents` → `/Users/moses/code/_bmad-output/perkins/righttenantryagents-boundary-gate-state-fix/r2/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the job briefing + issue #172, `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantryagents-boundary-gate-state-fix/r2`, `prior_findings` = r1's consolidated.json (fix-audit FIRST, carry-forward markers). Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r2` labels), `<lens>.json` output contract + existence check, one retry per failed lens, verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`**.
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 173 --repo solarity-services/RightTenantryAgents --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 173 --repo solarity-services/RightTenantryAgents --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 2 of 3 (fix-audit)` / **Job:** righttenantryagents-boundary-gate-state-fix / **Reviewed sha:** b1ebd96 (r1 was 39443b2) / **r1 audit:** <b>/<b> blockers FIXED, <w>/<w> warnings fixed / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers / ### Warnings / ### Notes / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set righttenantryagents-boundary-gate-state-fix-perkins-r2 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
