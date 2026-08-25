## 🤖 Perkins automated review — round 2 of 3 (FIX-AUDIT)

**Job:** righttenantry-refcheck-rc3-5 · **Reviewed sha:** `33d237e` · **Reviewers:** 6/7 completed (architecture stuck — see note)
**Fix-audit scope:** r1 blocker **B1** + warnings **W1–W5**
**Verification:** 7/7 fix-audit items confirmed FIXED against the code at `33d237e` (N2 incidentally fixed); 6/6 new findings confirmed against the code, 0 rejected as false-positive.

> **Head sha stable:** `33d237e` throughout the round.

---

### Fix audit (r1) — ✅ all addressed

| r1 | Status | Evidence (at `33d237e`) |
|----|--------|-------------------------|
| **B1** blocker — guarded-UPDATE `Error` silently re-sent every 15 min forever | ✅ **FIXED** | All 5 guarded Error branches (`step_t0` :343, `step_co_nudge` :396, `step_reminder` :445, `step_warm_handoff` :491, `step_terminal` :553) now call `mark_failed(db, sentry, row.id, <reason>)` + the `capture()` helper Sentry-captures. `mark_failed` sets `status='failed'` → **excluded by the due-SELECT** → the poison row leaves the queue. The infinite re-send loop is genuinely broken (not cosmetic). `terminal_reason` is plain `TEXT`, so the free-form reason string is safe. |
| **W1** — production `at:""` blank timestamps | ✅ **FIXED** | `bootstrap()` (:169) + `sweep_handler` (:37) now pass `sweep.now_iso()` (`timestamp.system_time |> to_rfc3339 utc_offset`). Server compiles clean → API resolves. |
| **W2** — fabricated warm-handoff entry | ✅ **FIXED** | `step_warm_handoff` (:480) passes the real this-tick `outcomes`; `dispatch_warm_handoff` appends `outcomes_to_entries(outcomes)` (:571) — no fabricated entry. |
| **W3** — warm-handoff dispatch-loss (`let _ =`) | ✅ **FIXED** | `dispatch_warm_handoff` now case-matches the Result (:595): `Ok→Nil`, `Error→log_error + sentry_client.capture(ReferenceWarmHandoffLost)`. |
| **W4** — live sentry in manual fire | ✅ **FIXED** | `sweep_handler` threads `sentry_client.Disabled` in both `SendDeps` (:37) and `sweep.run` (:44) — matches spec OWNS #7. |
| **W5** — cadence offsets untested | ✅ **FIXED** | `cadence_offsets_pinned_with_fake_clock_test` (:619) seeds 4 rows at a shared anchor, runs at anchor+1s, asserts `24/24/48/48h`. Sound; pins the AD-4 increments a step-advance-only test cannot catch. |
| **N2** (bonus) — `mark_failed` wrote only a generic slug | ✅ **FIXED (incidental)** | `mark_failed` (:649) now passes the per-call `reason`; the generic `reason_processing_error` const was removed. |

**Load-bearing invariants intact:** the fix touched only Gleam Error branches + helpers — **the SQL is unchanged**. Exactly-once guarded update (`WHERE attempt_count=$n`), terminal-respect due-SELECT, and no-duplicate-T0 all still hold. Code compiles clean at `33d237e` (3 pre-existing warnings in unrelated files).

---

### Blockers (0)

None. 🎉

---

### Warnings (2) — both about the B1 fix's trade-off, neither blocking

**W1. Transient per-row UPDATE error now terminalises a healthy row (orphaning an already-sent T0 invite)** · `sweep.gleam:338-343` (identical pattern in all 5 Error branches) · *blind + edge agree*

The chosen fix (`mark_failed` on Error) is one of the two options r1's recommended-fix endorsed, and B1's silent infinite loop IS broken (row → `failed` → excluded from the due-SELECT, Sentry-captured). **But** a transient per-row error (deadlock / timeout / connection-drop on a healthy row) now permanently fails the row + orphans the invite sent just before the claim. It is **loud and recoverable** (Sentry event, ops can re-trigger), but a one-off DB hiccup can kill a legitimate reference-check.
*Fix if desired:* accept with the documented recovery path, or add a consecutive-error cap (re-arm for N ticks, terminalise on the Nth) to distinguish poison data from a transient — r1's alternative option.

**W2. The B1 `Error→mark_failed` transition (5 branches) has zero test coverage — the round's headline fix rests on inspection only** · `sweep.gleam` (5 Error branches) + `reference_checks_sweep_integration_test.gleam` (no `mark_failed`/`failed` assertion) · *tests* · **Advisory gate: CONCERNS** (P0 100%, P1 <90%)

Hard to test (needs a forced UPDATE error — a CHECK/trigger violation or a mock), but the fix is the round's primary change and its new terminalise-on-Error behaviour is unverified beyond reading.
*Fix if desired:* a targeted test that forces a guarded-UPDATE error and asserts `status='failed'` + `terminal_reason` set, or a `mark_failed` unit test pinning at least one branch.

---

### Notes — new (4)

- **mark_failed fire-and-forgets its own DB write — now load-bearing on every error path** · `sweep.gleam:646-657` · *blind* — `let _ = sql.sweep_mark_failed(...)`; if the write itself fails the row stays due. `capture()` always runs (loud), and a global write failure also fails the due-SELECT, so the residual loop only opens in the rare read-ok/write-fail window. Accept, or log a 0-row result so ops can tell "concurrent-writer no-op" from "write failed".
- **`sweep_mark_failed` WHERE omits `attempt_count` — a committed-but-errored advance can be clobbered** · `sweep_mark_failed.sql:18` (contrast `sweep_advance.sql:22`) · *edge* — if an advance commits but the client errors (connection drop between commit + result read), `mark_failed` sees `status='contact_initiated'` and wrongly terminalises a successfully-advanced row (+ a reminder already sent). Rare ambiguous-outcome window. *Fix:* add `attempt_count = $n` to the WHERE.
- **`sweep_handler` module docstring contradicts the W4 fix** · `sweep_handler.gleam:8-10` · *acceptance* — still says "failures escalate to Sentry… same as a scheduled tick"; the fix threads `sentry_client.Disabled`. Update the docstring.
- **`run/5` docstring still claims "production passes `""`"** · `sweep.gleam:187-189` · *codebase* — W1 made `bootstrap()` pass `now_iso()`. Update the docstring.

### Notes — carried from r1 (8, advisory, untouched by this fix — not escalated)

- **N1** Due-SELECT failure exits 0 (`sweep.gleam:191-196`).
- **N3** Draft `'{}'` detection decodes to empty map vs Dev Note 5 literal (`sweep.gleam:681`).
- **N4** `awaiting_correction` due-SELECT exclusion untested.
- **N5** Guarded-update 0-row `StoodDown` branch + concurrent race untested.
- **N6** `AttemptEntry` JSONB decoder duplicated in `sweep.gleam` + `result.gleam`.
- **N7** `standard_sender` const duplicated (`send.gleam` + `notification_dispatch.gleam`).
- **N8** `sweep.gleam` re-implements `messages.first_name` (no `string.trim`).
- **N9** Integration-test helpers build SQL by raw string concat of row ids.

---

### Reviewer agreement
- **Transient→terminal trade-off (W1):** blind + edge — highest-confidence signal, surfaced first.

### Note on reviewer completion
**Architecture lens did not complete** (6/7). It stalled >22 min over-verifying the `gleam_time` calendar/timestamp API (which compiles clean). Its architectural concerns are covered by the other lenses: the transient trade-off (blind+edge), the `now_iso` boundary + orphan checks (codebase), and the docstring drift (acceptance). The degraded guard (a failed lens with zero findings) does **not** apply — 6 lenses produced actionable findings.

---

### Verdict: **READY TO MERGE**

All 6 r1 findings (B1 + W1–W5) are fixed and verified; the load-bearing invariants (exactly-once, terminal-respect, no-duplicate-T0) are intact; 0 blockers. The 2 warnings are the chosen B1 fix's defensible trade-off (transient→terminal, r1-endorsed, loud+recoverable) and a coverage gap on that same fix (hard to test, inspection-thorough) — neither blocks. The 8 carried notes are advisory and untouched by this fix.

The human remains the only merger. If you'd like the minion to refine the transient→terminal trade-off (consecutive-error cap) and/or pin the B1 path with a test before merge, that's a reasonable round-3 spend; otherwise this is merge-ready as-is.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._

---
*Perkins r2 · model glm-5.2 (kimi quota down this cycle) · 6/7 lenses · fix-audit-first*
