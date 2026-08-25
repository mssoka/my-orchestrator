# LENS: tests (source tag: `tests`) — Perkins r5 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/lens-briefs/_shared.md`
FIRST (shared context, inputs, lens-guards, output contract), then
`/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/lens-briefs/prior-findings.md`
(the r5 FIX AUDIT list — you own the tests-class items: B1 race pin vacuity, W2 pin bite,
N6 no_em_dash dedupe, N15 client pins, N16 sweep_mark_failed pin, N19 hygiene).

Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing).
Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics: new/modified API endpoints without matching coverage; auth/authz
paths missing negative tests; happy-path-only coverage where error handling is implied; new
DB operations without integration coverage; new state transitions without boundary tests.
Test level mix (unit/integration/E2E): flag mismatches.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds: PASS: P0 100%, P1 ≥90%, overall ≥80%; CONCERNS: P0 100%, P1 80–89%,
overall ≥80%; FAIL: P0 <100%, or P1 <80%, or overall <80%.

**Round 5 — VERIFY-DON'T-REOPEN: FIRST check whether each r4 gap now has a REAL pin (fixed
= silent; still missing/vacuous = finding with original severity, title prefixed
`STILL PRESENT (r4): `). Then trace the NEW behaviours of this rework.**

**Round-specific traceability — the RACE-PIN VACUITY QUESTION (the round's #1 mandate):**

1. **B1 race pin.** Read `wrong_person_taken_over_race_stands_down_test` in the worktree
   (~1734 in reference_checks_actions_integration_test.gleam). Questions: (a) Does it drive
   the ACTUAL wrong-person POST route (router.handle_request on
   /reference/wp-race-token/wrong-person) AND call the guarded SQL directly? (b) Does it
   assert 303 + status contact_initiated + taken_over_at set + ZERO
   reference_call_wrong_person audit rows on the taken-over row? (c) Would removing the
   `taken_over_at IS NULL` guard from the SQL turn it red (the direct call returns 0 rows
   on the taken-over row; the control without takeover returns 1 + awaiting_correction)?
   (d) Is the control arm real? A vacuous, route-bypassing, or guard-insensitive pin =
   blocker per the standing orders.
2. **W2 pin bite.** `co_nudge_bounce_stands_down_test` — fixture LEGACY-shaped (untagged
   single-email co-nudge entry) with a POST-correction timestamp, so deleting the
   batch-shape exclusion turns it red (matched → send_is_post_correction → exhaust).
   Control: a genuine dual-channel referee send bounce still exhausts. Producer side:
   sweep_integration_test asserts the `"kind": "co_nudge"` tag lands in the attempts log.
3. **W1 pin.** `genuine_post_correction_failure_exhausts_test` — the fixture now adds an
   sms sibling at the same `at` (the batch shape of a real dual-channel send) — does the
   test fail if the exclusion is deleted? (It shouldn't — genuine sends must still
   exhaust.) Does anything pin that a genuine single-channel (email-only) referee send is
   NOT excluded? (The sweep always appends a skipped sms sibling — check whether that
   invariant is tested anywhere, e.g. send_test/sweep_test.)
4. **N8 malformed-at.** Is the new `send_is_malformed` gate covered by ANY test (a
   malformed-at fixture standing down)? The r4 note said "the malformed branch has no
   test" — check whether one was added.
5. **N15 client pins.** New tests: refcheck_start_confirm_dispatches_test,
   refcheck_substitute_save_dispatches_test, refcheck_export_handler_marks_clipboard_test.
   Still missing per the r4 note? prefill-level pins (UserChoseRefcheckAction →
   substitute-empty / corrected-override prefill) and the validation tests' "fires
   nothing" assertions (the `eff` is never asserted as none()).
6. **N16.** sweep_mark_failed_respects_taken_over_test — drives the SQL with a taken-over
   row, asserts 0 rows + status untouched. Real?
7. **Settled pins — verify no regression.** The r1/r2/r3 pins (same_day_stale_bounce,
   taken-over stand-down on the webhook paths, B1 cadence re-arm, B2 disabled adjacency,
   B3 hooks, W3 route guard, W5 400, W7 409, authz negatives, exhaustion on both routes
   with audit + notification, sweep exclusion, late-completion §8.6, per-slot re-arm,
   resend effective contact, fallback-leg stand-down) — still present and still asserting.
8. **NEW behaviour of this rework.** The wrong-person exhaustion 0-row/Error split, the
   `correction_cycles = 0` SQL backstop, the rewritten find_reference_call_by_send_ref SQL
   (batch-shape exclusion + malformed gate), the vacancy-check Error arm (N10), the
   webhooks exhaust Error arm (N11), the effective-basis trio_matches_row (N7) — trace
   each to a test.

Counts claimed by the implementer: CI green at ccc0ff6 (suites shared / client / server
unit / integration). Spot-check the test files in the worktree — read the ACTUAL test
bodies, not just the names. Quote exact lines in `evidence`.
