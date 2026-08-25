## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantry-refcheck-rc3-5
**Reviewed sha:** cc1b041
**Reviewers:** 7/7 completed (blind · edge · acceptance · security · architecture · codebase · tests) — no failed lenses
**Verification:** 15/31 raw reviewer findings survived dedup + re-verification against the source (1 rejected as not-a-defect; the rest merged into the 15 below)

The load-bearing invariants are **defended**: the **no-duplicate-T0-across-retry** test is real and passes; the guarded atomic updates (`WHERE id AND status AND attempt_count=$n`) are correctly atomic; **terminal-state respect** holds (the due-SELECT excludes every terminal + taken-over + `awaiting_correction` by construction); the **co-nudge gate** (form-opened OR draft → skip) is correct; the **cadence math** (24/24/48/48h) is correct (manually re-derived — agrees with the spec's `created_at + offset` under normal operation); the **failure path sends no landlord notification**; and the **Terraform** follows the retention/digest house pattern (production-gated, narrow-secret posture, scheduler token-creator binding present, manual-fire route shared-secret-gated). One blocker on the guarded-update *failure* path.

### Blockers (1)

**1. Persistent guarded-update error silently re-sends every 15 min — AC7 + AD-15 unmet for this path** `[blind, edge, tests]` — `server/src/reference_checks/sweep.gleam:317-321` (also `:365-367`, `:406`, `:448`, `:508-511`)
The `Error(_)` branch of every guarded UPDATE returns `StoodDown` with **no Sentry capture and no `failed` transition**, leaving the row due. Because each step sends *before* the claim (send-then-claim), a row whose UPDATE persistently errors (a CHECK/trigger violation, poison data) **re-sends its invite/reminder every 15 min forever, silently**. That breaks AC7 ("a DB/decode failure mid-tick → failed + Sentry"), AD-15 ("fail loudly"), and exactly-once under failure. The comment's orphaned-invite rationale justifies the *transient* case, not the unbounded silent loop.
*Fix:* Sentry-capture every guarded-update `Error`, and either `mark_failed` on Error or cap consecutive stand-downs (N retries) before terminalising.

### Warnings (5)

**W1. Attempt-log `at` timestamps are `""` in production** `[blind, edge, acceptance, architecture, codebase]` — `sweep.gleam:164` + `sweep_handler.gleam:39`
Both production entry points pass `now_iso: ""`; nothing substitutes a real clock for the `at` field, so every `attempts[]` entry (and the result-JSON re-emit + warm-handoff render) is blank. Cadence *timing* is unaffected (`next_attempt_at` uses SQL `now()`), but the audit/display log loses timestamps. *Fix:* pass a real ISO now in production, or stamp `at` from `now()` when the value is empty.

**W2. Warm-handoff email renders a fabricated single `email`/`reminder_2` entry** `[blind, acceptance, architecture, codebase]` — `sweep.gleam:530-536`
`dispatch_warm_handoff` reads the **stale** pre-advance `row.attempts` and appends one hardcoded `email/reminder_2` entry. Reminder 2 actually sends on **email + SMS** (2 real entries), so the landlord's attempt-log render misrepresents the actual sends. *Fix:* re-read the row's attempts after the guarded advance (or pass this tick's real `entries`/`outcomes` and merge).

**W3. Warm-handoff notification can be permanently lost** `[blind, edge, architecture]` — `sweep.gleam:555-556`
`dispatch_warm_handoff` runs after the guarded advance (row now T+144-due, won't be re-selected) and discards the dispatch Result with `let _ =`. If the in-app insert fails, the §8.3 notification — the *only* unreachable notification (T+144 is silent) — is lost with no log and no Sentry. *Fix:* log + Sentry-capture an `Error`; consider a retry.

**W4. Manual-fire handler threads live `config.sentry`** `[blind, acceptance]` — `sweep_handler.gleam:33,40`
Spec OWNS #7 pins `sentry_client.Disabled` ("manual runs don't escalate"); the handler uses live `config.sentry`, so a manual drain of broken rows captures to Sentry. *Fix:* thread `Disabled` (match spec) or update the spec wording.

**W5. Cadence offsets (24/24/48/48h) never asserted** `[tests]` — integration test `:37,:141-149,:248-260`; `sweep.gleam:56-65`
The `now_iso` fake-clock pin exists but the tests pass `""` and re-arm `next_attempt_at` with raw SQL, so a wrong offset constant would ship undetected (a reminder at the wrong time). The math is correct (manually verified); it's just untested. *Fix:* a fake-clock test per step asserting `next_attempt_at = prior + expected offset`.

### Notes (9)

- **N1.** Due-SELECT failure exits 0 ("sweep complete: due=0") — Sentry captures but Cloud Run sees success `[blind, acceptance]` `sweep.gleam:188-193`. Consider exiting non-zero so a failed SELECT is a failed tick.
- **N2.** `mark_failed` writes only the generic `sweep_processing_error` slug to `terminal_reason`; the specific reason is Sentry-only `[blind]` `sweep.gleam:587`.
- **N3.** Draft detection for `'{}'` deviates from Dev Note 5's literal wording (code: empty decoded map → unreachable; note: non-empty string → partial) `[blind]`. Code behavior is arguably better; reconcile the wording.
- **N4.** `awaiting_correction` exclusion untested (only objected + taken-over pinned) `[tests]`.
- **N5.** Guarded-update concurrent race + 0-row `StoodDown` path untested (only sequential retry) `[tests]`. The SQL `WHERE attempt_count=$n` guard makes a concurrent double-advance impossible, but the Gleam branch has zero coverage.
- **N6.** `sweep.gleam` duplicates `result.gleam`'s `{at,channel,outcome,detail}` attempt decoder `[codebase]` `:725-745` vs `result.gleam:489-522`. Hoist one into `messages.gleam`.
- **N7.** `standard_sender` const duplicated verbatim `[codebase]` `send.gleam:34` / `notification_dispatch.gleam:18`.
- **N8.** `sweep.gleam` re-implements `messages.first_name` (no `string.trim`) `[codebase]` `:686-691` vs `messages.gleam:139-144`.
- **N9.** Integration-test helpers build SQL by raw string concatenation of row ids (controlled UUIDs, no real injection; test-hygiene) `[security]`.

### Reviewer agreement
Six findings were independently confirmed by ≥2 lenses — highest confidence, prioritise first: the **`at: ""`** blank-timestamp bug (5 lenses), the **fabricated warm-handoff entry** (4 lenses), the **warm-handoff dispatch-loss** (3 lenses), and the **blocker** (3 lenses).

**Verdict: NEEDS CHANGES** — 1 blocker. The exactly-once / terminal-respect / guarded-update / co-nudge / terraform invariants all hold and the required no-duplicate-T0 test is real; the blocker is the silent failure-path on persistent guarded-update errors. The warm-handoff area (`at: ""` + fabricated entry + dispatch-loss) is the other cluster worth a pass.

---
Address the findings and push; round 2 will re-verify against the new sha. (Perkins reviews only — the implementing minion owns the fixes.)
