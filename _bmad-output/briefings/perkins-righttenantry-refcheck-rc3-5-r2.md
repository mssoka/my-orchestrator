# Perkins briefing — round 2 (FIX-AUDIT): righttenantry-refcheck-rc3-5

- **PR:** https://github.com/solarity-services/RightTenantry/pull/600 (targets `develop`)
- **Reviewed sha:** `33d237e1aba0171d2abefde7d61126e06f83f756` (short `33d237e`; commit "RC3.5 r2: address Perkins r1 (B1 blocker + W1-W5)")
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 2 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-5-r2` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc3-5.md` + the epics (`_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md`, story RC3.5) + the architecture (`_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md`: AD-4/AD-6/AD-14/AD-15, A2, A7, §4.6, §8.3, §9) + the GitHub issue #548 (dumped at `_bmad-output/perkins/righttenantry-refcheck-rc3-5/r2/issue-548.json`).
- **prior_findings:** **`/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r1/consolidated.json`** — this is a FIX-AUDIT round. The implementing minion pushed fixes for the r1 blocker (B1) + warnings W1-W5; you verify those are addressed + carry the carry-forward markers + re-confirm the load-bearing invariants still hold (no regression). Read `prior_findings` FIRST; the r1 verdict was CHANGES_REQUESTED (1 blocker).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What changed since r1 (the fix-audit scope)

The head moved `cc1b041` (r1) → `33d237e` (this round). The commit message says "address Perkins r1 (B1 blocker + W1-W5)". Your job: **fix-audit-first** — verify each r1 finding is actually fixed at this sha, THEN a normal pass over the delta for any new issue the fix introduced. The r1 findings to verify:

- **B1 (BLOCKER, `sweep.gleam` Error branch):** persistent guarded-update error silently re-sent every 15 min forever (no Sentry capture, no `failed` transition). **Verify FIXED:** the `Error(_)` branch of every guarded UPDATE now Sentry-captures AND either `mark_failed`s OR caps consecutive stand-downs before terminalising. Confirm the unbounded silent loop is gone.
- **W1 (`at:""` blank timestamps):** production entry points passed `now_iso: ""`. **Verify FIXED:** a real ISO now is passed in production (or `at` is stamped from SQL `now()` when empty).
- **W2 (fabricated warm-handoff entry):** `dispatch_warm_handoff` read the stale pre-advance `row.attempts` + hardcoded one `email/reminder_2` entry. **Verify FIXED:** it re-reads the row's attempts after the guarded advance (or merges this tick's real entries).
- **W3 (warm-handoff dispatch-loss):** `dispatch_warm_handoff` ran after the guarded advance + discarded the Result with `let _ =`. **Verify FIXED:** the dispatch Result is logged + Sentry-captured on Error (the T+144 notification is otherwise unreachable).
- **W4 (live sentry in manual fire):** the manual handler threaded live `config.sentry` (spec OWNS #7 pins `Disabled`). **Verify FIXED:** `sentry_client.Disabled` is threaded in the manual-fire path.
- **W5 (cadence offsets untested):** offsets 24/24/48/48h were never asserted (the fake-clock pin existed but tests passed `""`). **Verify FIXED:** a fake-clock test per cadence step asserting `next_attempt_at = prior + expected offset`.

**r1 Notes (N1-N9) are ADVISORY — NOT must-fix.** Do NOT escalate a Note to a blocker/warning just because it's still open; the minion was asked to fix B1+W1-W5 only. Carry each still-open Note forward in your Notes section (mark it "carried from r1, open") so it stays visible; flag as a NEW finding only if the fix delta broke something there.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

Production server code + infra on the referee path. The diagnosis/design is PINNED. This is a FIX-AUDIT.

- **Do NOT re-litigate the r1 findings as NEW findings.** B1/W1-W5 are in fix-audit scope — you VERIFY each is fixed (mark "FIXED" with the new code location, or "STILL OPEN" with evidence). A correctly-fixed r1 finding is NOT a round-2 blocker. Only re-flag one if the fix is WRONG/INCOMPLETE or introduced a new defect.
- **Do NOT re-open the rc3-4 findings** (verified fixed in their own rounds) — carry-forward markers only.
- **EXACTLY-ONCE + IDEMPOTENT remains the load-bearing invariant** (carry from r1): the no-duplicate-T0-across-retry test + every cadence step's re-run idempotency MUST still hold after the fixes. A fix that broke exactly-once is a NEW blocker.
- **The guarded atomic update (AD-4/AD-14)** still must be one guarded `UPDATE ... WHERE` — the B1 fix touches the Error branch, NOT the happy path; verify the race test + no-duplicate-T0 still pass and the guard logic is intact.
- **Terminal-state respect (rc3-4 carry-forward):** `objected` (sticky AD-6), `refused`/`awaiting_correction`/`form_completed`, taken-over rows — still skipped. Verify the fixes didn't alter the due-SELECT's exclusions.
- **The co-nudge gate + cadence math + failure path (no landlord notification) + infra (Terraform house pattern, manual-fire shared-secret) + no-op-without-Twilio-keys + no em-dashes** — all still apply (carry from r1); only flag if the fix delta touched them.
- **Regression guard:** the existing fake-clock cadence tests + the race test + no-duplicate-T0 + terminal-respect tests must still pass at `33d237e`. If a fix regressed one, that's a NEW finding.

### Legitimate round-2 findings would be
- An r1 finding (B1/W1-W5) **still open or wrongly fixed** at `33d237e` (re-flag it, mark "not fixed in r2").
- A **new defect the fix introduced** (e.g. the B1 Error-branch fix broke exactly-once, or the W1 now_iso change mis-stamps, or the W5 test is a false-pass).
- A regression in the r1-confirmed invariants (exactly-once / guarded-update / terminal-respect / co-nudge / cadence math).
- A Gleam compile/test failure at `33d237e`.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 600 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r2/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree at `33d237e`), `spec_files` = this briefing + the job briefing + the epics + the architecture + the issue #548 dump, `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r2`, `prior_findings` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r1/consolidated.json` (fix-audit-first: verify r1 B1+W1-W5 addressed, then delta pass). Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r2` labels), `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (the script writes cache warnings to stderr which would corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 600 --repo solarity-services/RightTenantry --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 600 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `33d237e`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 2 of 3` / **Job:** righttenantry-refcheck-rc3-5 / **Reviewed sha:** 33d237e / **Fix-audit:** r1 B1+W1-W5 (FIXED|STILL OPEN per item) / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc3-5-perkins-r2 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: `zai-coding-cn/glm-5.2`** — kimi quota is DOWN this billing cycle (confirmed 403 on k3 at launch: "usage limit reached"). glm-5.2 is the sanctioned fallback (r1 ran the full round on it). Silas redirected mid-session via `/model`. If glm-5.2 429s mid-turn, one `continue` may revive it; if it hard-fails, self-report `blocked`.
