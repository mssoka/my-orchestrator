# LENS: tests (source tag: `tests`) — Perkins r4 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r4/lens-briefs/_shared.md` FIRST (shared context, inputs, lens-guards, output contract), then `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r4/lens-briefs/prior-findings.md` (the r4 FIX AUDIT list — you own the tests-class items: the r3 TOCTOU race pin (the vacuous-pin question), r3 N4 per-slot re-arm pin, r3 N8-client ?slot= test, r3 N11 resend pins, r3 N12 client wiring pins, r3 N15 timestamp fixture, r3 N18 no_em_dash duplicate disjunct, r3 N22 advisory gate).

Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics: new/modified API endpoints without matching coverage; auth/authz paths missing negative tests; happy-path-only coverage where error handling is implied; new DB operations without integration coverage; new state transitions without boundary tests. Test level mix (unit/integration/E2E): flag mismatches.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds: PASS: P0 100%, P1 ≥90%, overall ≥80%; CONCERNS: P0 100%, P1 80–89%, overall ≥80%; FAIL: P0 <100%, or P1 <80%, or overall <80%.

**Round 4 — VERIFY-DON'T-REOPEN: FIRST check whether each r3 gap now has a REAL pin (fixed = silent; still missing/vacuous = finding with original severity, title prefixed `STILL PRESENT (r3): `). Then trace the NEW behaviours of this rework.**

**Round-specific traceability — THE RACE-PIN VACUITY QUESTION (the round's #1 mandate):**

1. **THE r3 TOCTOU blocker's race pin.** The r3-rework adds `wrong_person_awaiting_sql_has_taken_over_backstop_test`. Read it in the worktree. Two questions: (a) Does it drive the ACTUAL wrong-person POST route (via `handle_wrong_person_post` / `apply_wrong_person`), or does it call `rc_sql.mark_awaiting_correction_wrong_person(db, call)` DIRECTLY? (b) If the handler were still wired to the UNGUARDED `update_reference_call_status`, would this test fail? A test that calls the guarded SQL function directly CANNOT catch an unwired backstop — it is a VACUOUS pin. Per the round-4 standing orders, a missing/weak backstop or a vacuous race pin = a blocker. If the pin is vacuous (and/or the handler is unwired), emit `STILL PRESENT (r3): ` blocker with the exact test lines as evidence.
2. **Fallback-leg stale bounce (r3 W2 pin).** `fallback_leg_stale_bounce_stands_down_test` — does it exercise the delivery-failure webhook path with an unmatched send_ref post-correction, asserting stand-down (status unchanged, no referee_contact_invalid)? Is there a control that a genuine post-correction failure still exhausts?
3. **Co-nudge exclusion (r3 W3 pin).** `co_nudge_bounce_stands_down_test` — asserts a bounce of the applicant's address stands down. Does a genuine referee-channel failure still exhaust (control)?
4. **Sweep terminal guards (r3 W4 pin).** `sweep_terminal_writers_respect_taken_over_test` — asserts both sweep_terminal and sweep_mark_failed stand down on taken-over rows.
5. **Per-slot re-arm (r3 N4 pin).** `per_slot_rearm_and_declined_no_rearm_test` — asserts only the requested slot re-arms AND the declined path does not re-arm.
6. **Resend effective (r3 N11 pins).** `resend_effective_contact_pre/post_correction_test` in form_handler_test.gleam — assert the corrected-only rule (cleared channel stays absent post-correction).
7. **r3 N8-client.** client/test/api/reference_checks_api_test.gleam (NEW file in this PR) — does it pin the `?slot=` URL building for per-row start?
8. **r3 N12 client wiring.** Client update-handler tests for UserConfirmedRefcheckAction(TakeOver) / UserSavedRefcheckEdit(Correct/Substitute) asserting the API effect fires with the right URL/payload — added in this rework?
9. **r3 N15 timestamp fixture.** `stale_pre_correction_failure_stands_down_test` — now()-relative or still a fixed absolute timestamp?
10. **r3 N18.** no_em_dash_test duplicate disjunct cleaned?
11. **Settled pins — verify no regression.** The r1/r2 pins (same_day_stale_bounce_stands_down_test, taken-over stand-down on the webhook paths, B1 cadence re-arm, B2 disabled adjacency, B3 hooks, W3 route guard, W5 400, W7 409, authz negatives, exhaustion on both routes with audit + notification, sweep exclusion, late-completion §8.6) — still present in the diff and still asserting what they claim?
12. **NEW behaviour of this rework.** Any new code paths in the diff without tests: the wrong-person exhaustion 0-row/Error split (r3 N13), the `correction_cycles = 0` SQL backstop (r3 N21), the rewritten find_reference_call_by_send_ref SQL (r3 N14sql — malformed 'at' handling tested?), the new sql.gleam generated functions.

Counts claimed by the implementer: 533 integration / 554 client / 110 shared / 1482 server unit green at `df0ea22`. Spot-check the integration test file (`server/test/integration/reference_checks_actions_integration_test.gleam` in the diff, chunk c5) for the guard pins above — read the ACTUAL test bodies in the worktree, not just the names.
