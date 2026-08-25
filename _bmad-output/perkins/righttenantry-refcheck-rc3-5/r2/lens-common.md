# Perkins round 2 — shared lens context (read FIRST)

You are a review lens in a **Perkins round 2 FIX-AUDIT** of PR #600
(RightTenantry — the reference-check sweep cadence engine + Cloud Run Job).

- **PR:** https://github.com/solarity-services/RightTenantry/pull/600 (targets `develop`)
- **Reviewed sha:** `33d237e1aba0171d2abefde7d61126e06f83f756` (short `33d237e`)
- **Commit:** "RC3.5 r2: address Perkins r1 (B1 blocker + W1-W5)"
- **Your worktree (read-only verify target):** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-5-r2` (detached at exactly `33d237e`). Trust this state, not `origin/develop`.
- **Canonical diff (review THESE bytes):** `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r2/diff.patch` (full PR vs develop, 3018 lines).
- **Focused r1→r2 delta (what the fix changed):** `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r2/delta-r1-r2.patch` (245 insertions / 45 deletions across `sweep.gleam`, `sweep_handler.gleam`, the sweep integration test).
- **Prior round findings (FIX-AUDIT scope):** `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r1/consolidated.json` — r1 verdict was CHANGES_REQUESTED (1 blocker B1, 5 warnings W1-W5, 9 notes N1-N9).
- **Job briefing (your spec):** `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc3-5.md`
- **Issue dump:** `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r2/issue-548.json`

## The fix-audit scope — verify these r1 findings are FIXED

The implementing minion pushed fixes for exactly these. **Fix-audit-first:** for each, re-read the cited code at `33d237e` and classify `FIXED` (with the new code location) or `STILL OPEN` (with evidence). A correctly-fixed r1 finding is NOT a round-2 finding. Only re-flag one if the fix is WRONG/INCOMPLETE or introduced a NEW defect.

- **B1 (BLOCKER) — guarded-update Error silently re-sent every 15 min forever.** r1: every guarded `UPDATE` `Error(_)` branch returned `StoodDown` with no Sentry, no `mark_failed`, row untouched → a poison row re-sends its invite/reminder every tick forever. r1 locations: `sweep.gleam` step_t0 / step_co_nudge / step_reminder / step_warm_handoff / step_terminal Error branches. **Verify FIXED:** each guarded Error branch now Sentry-captures AND `mark_failed`s.
- **W1 — production `at:""` blank timestamps.** r1: `bootstrap()` + `sweep_handler` passed `now_iso: ""`. **Verify FIXED:** a real ISO now is passed in production (`sweep.now_iso()`).
- **W2 — fabricated warm-handoff entry.** r1: `dispatch_warm_handoff` read the stale pre-advance `row.attempts` + appended ONE hardcoded `email/reminder_2` entry. **Verify FIXED:** it merges this tick's REAL reminder-2 `outcomes`.
- **W3 — warm-handoff dispatch-loss.** r1: `dispatch_warm_handoff` ran after the guarded advance + discarded the Result with `let _ =`. **Verify FIXED:** the dispatch Result is logged + Sentry-captured on Error.
- **W4 — live sentry in manual fire.** r1: `sweep_handler` threaded live `config.sentry` (spec OWNS #7 pins `Disabled`). **Verify FIXED:** `sentry_client.Disabled` is threaded in the manual-fire path.
- **W5 — cadence offsets untested.** r1: offsets 24/24/48/48h never asserted. **Verify FIXED:** a fake-clock test per cadence step asserting `next_attempt_at = anchor + expected offset`.

## r1 Notes N1-N9 are ADVISORY — NOT must-fix

Do NOT escalate a Note to a blocker/warning just because it's still open; the minion was asked to fix B1+W1-W5 only. Carry each still-open Note forward as `still present since round 1, open` (a Note, not escalated). Flag a Note as a NEW finding ONLY if the fix delta broke something there. (Note: N2 — `mark_failed` writing only the generic slug — may be incidentally fixed by the B1 fix; verify and mark accordingly.)

## ⚠️ Lens-guards (prevents false positives) — the diagnosis/design is PINNED

- **Do NOT re-litigate the r1 findings as NEW findings.** B1/W1-W5 are in fix-audit scope — you VERIFY each is fixed. A correctly-fixed r1 finding is NOT a round-2 blocker.
- **Do NOT re-open the rc3-4 findings** (verified fixed in their own rounds).
- **EXACTLY-ONCE + IDEMPOTENT remains the load-bearing invariant:** the no-duplicate-T0-across-retry test + every cadence step's re-run idempotency + the guarded atomic `UPDATE ... WHERE attempt_count=$n` MUST still hold after the fixes. A fix that broke exactly-once is a NEW blocker.
- **The guarded atomic update (AD-4/AD-14)** is unchanged on the happy path — the B1 fix touches only the Error branch; verify the guard logic + the 0-row StoodDown path are intact.
- **Terminal-state respect** (objected / refused / awaiting_correction / form_completed / taken-over rows skipped) — verify the fixes didn't alter the due-SELECT's exclusions.
- **Co-nudge gate + cadence math + failure path (no landlord notification on `failed`) + infra (Terraform house pattern, manual-fire shared-secret) + no-op-without-Twilio-keys + no em-dashes** — all still apply; only flag if the fix delta touched them.
- **Regression guard:** the existing fake-clock cadence tests + the race test + no-duplicate-T0 + terminal-respect tests must still pass at `33d237e`.

## Legitimate round-2 findings (the only things you should file)

- An r1 finding (B1/W1-W5) **still open or wrongly fixed** at `33d237e` (re-flag, mark "not fixed in r2").
- A **new defect the fix introduced** (e.g. the B1 Error-branch fix broke exactly-once, or the W1 now_iso change mis-stamps, or the W5 test is a false-pass, or `mark_failed`'s free-form reason violates a column constraint).
- A regression in an r1-confirmed invariant (exactly-once / guarded-update / terminal-respect / co-nudge / cadence math).
- A Gleam compile/test failure at `33d237e`.

**If you find nothing wrong, return `[]` — that is the honest, expected answer for a clean fix-audit.** Accuracy > volume. Do not invent findings.

## Project conventions (RightTenantry — load-bearing for this review)

- Gleam/Lustre monorepo; server target = erlang (Wisp/Mist API). Server-side Erlang FFI allowed; **JS FFI banned**.
- **No `let assert` in production code** (test files OK) — crashes the BEAM; use `case` with explicit error handling.
- **Explicit HTTP timeouts** on every outbound call (not relevant to this sweep delta, but the lint enforces it).
- **Squirrel is mandatory** for SQL — never hand-write query code. Timestamps: output cast `::text` (lowercase); input `$1::timestamptz` or `CASE WHEN $1='' THEN NULL ELSE $1::timestamptz END`.
- **All fallible ops return `Result`**; public fns have explicit type signatures; `gleam/dynamic/decode` for JSON.
- **Exactly-once + guarded atomic updates** are the spine of this feature (AD-4/AD-14): state transitions are guarded `UPDATE ... WHERE attempt_count=$n` (concurrent writers: only one's UPDATE returns a row). Messages are send-then-claim (worst case under crash-mid-tick = a duplicate message, never a missing one, never a duplicate state transition).
- `terminal_reason` column is plain `TEXT` (no CHECK/enum) — confirmed at `supabase/migrations/20260731222000_create_reference_call.sql:83`.
