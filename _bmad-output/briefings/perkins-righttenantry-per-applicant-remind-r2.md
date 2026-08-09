# Perkins briefing — round 2: righttenantry-per-applicant-remind

- **PR:** https://github.com/solarity-services/RightTenantry/pull/586 (targets `develop`)
- **Reviewed sha:** `b48b581cd5ba6b535ae4ebf35081c83e19b188d6` (head `per-applicant-remind`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 2 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-per-applicant-remind-r2` — pinned at exactly the reviewed sha.
- **Spec:** the original job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-per-applicant-remind.md`. No GitHub issue.
- **prior_findings:** `/Users/moses/code/_bmad-output/perkins/righttenantry-per-applicant-remind/r1/consolidated.json` (r1 APPROVED, 0B/4W/1N on sha `c6868b8`).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What changed since r1 (round 2 scope)

r1 (sha `c6868b8`) APPROVED with 0 blockers + 4 warnings + 1 note. The user then folded in **W1 + W3** pre-merge (NOT W2, NOT N1 — those are deliberate follow-ups):

- **W1 (policy-gate, ADDRESSED):** added `ApiReturnedApplicantReminder(Error(e)) -> check(e)` to the `msg_triggered_policy_reaccept` allowlist in `client/src/client.gleam` (beside the bulk sibling `ApiReturnedReminder(Error(e)) -> check(e)`), so a per-applicant policy-reaccept 428 surfaces the reaccept modal, not an error toast.
- **W3 (coverage, ADDRESSED):** added tests for the 400-validation branches in `handle_remind_applicant` (`server/src/inbound_email/inbound_handler.gleam`) — empty/invalid email, malformed body.

### r2 review focus (fix-audit-first, then the new diff)

1. **Fix-audit r1's warnings:** W1 (allowlist) → now ADDRESSED (confirm the allowlist arm is correct + actually fires the reaccept modal path); W3 (validation tests) → now ADDRESSED (confirm the tests genuinely exercise the 400 branches + bite). W2 (110-line copy-paste) → **deliberately NOT folded** (tracked follow-up) — re-confirm it's unchanged, don't escalate. W4 (test-gate concerns) → check if W3's new tests moved the needle.
2. **Review the new diff** (the W1 allowlist addition + W3 tests): is the allowlist arm correct + complete? Do the validation tests actually test the right branches (not tautologies)? Did the fold-in accidentally touch anything else (the gate-respecting logic, the bulk path, the atomicity)?
3. **No-regression:** the backend mirror is still exact; the re-enquiry edge still safe; no em-dashes; `make test-server` + `test-integration` green at this sha.

## ⚠️ CRITICAL lens-guard (still in force)

- **Do NOT flag W2 (the copy-paste/dedup) as a must-fix blocker.** The user **deliberately deferred** it (tracked follow-up, not this PR). A lens re-raising W2 as a blocker is re-litigating a closed decision = false positive. (Note-only is fine if you have new evidence; not a blocker.)
- **Do NOT flag N1 (duplicated awaiting-refetch block) as a must-fix.** Also deliberately not folded.
- **Do NOT flag "no force-remind" or "reuses bulk plumbing"** (the r1 lens-guard still applies — both are user-confirmed design).

Legitimate r2 findings: W1/W3 fold-in is INCORRECT or incomplete (allowlist arm wrong/missing, tests don't bite), the fold-in introduced a regression (gate breach, atomicity gap, broken bulk path), a NEW issue in the b48b581 diff, or a parse/test regression.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge.
- Save the canonical diff first: `gh pr diff 586 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-per-applicant-remind/r2/diff.patch`.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = this briefing + the original job briefing (no GitHub issue), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-per-applicant-remind/r2`, `prior_findings` = `/Users/moses/code/_bmad-output/perkins/righttenantry-per-applicant-remind/r1/consolidated.json`. Headless mode owns pane mechanics (dedicated tab, `mm-<lens>-r2`), `<lens>.json` + existence check, one retry per failed lens, big-diff chunking, verification pass, consolidation, `consolidated.json`. Close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`): `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)`; on failure fall back to `gh pr comment 586 --repo solarity-services/RightTenantry --body-file <body.md>` + note `fallback-comment`; else `GH_TOKEN=$TOKEN gh pr review 586 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Body format:
  ```
  ## 🤖 Perkins automated review — round 2 of 3
  **Job:** righttenantry-per-applicant-remind · **Reviewed sha:** b48b581 · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed — <rejected> false-positive[, <u> unverified]
  **Prior-round fix audit:** r1 W1 (allowlist) <addressed/open> · r1 W3 (validation tests) <addressed/open> · r1 W2 (copy-paste) <deferred-follow-up, not-folded> · r1 W4 (test-gate) <pass/improved?>

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _W1+W3 folded in pre-merge; W2 + N1 deliberately deferred (follow-up). Gate-respecting, no force-remind — user-confirmed._
  ```
- Before posting, re-fetch `headRefOid`. If it moved, post anyway + note "reviewed `b48b581`, head now `<new>` — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-per-applicant-remind-perkins-r2 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5.
