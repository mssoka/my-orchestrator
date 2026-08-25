# LENS: tests (source tag: `tests`) — Perkins r3 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r3/lens-briefs/_shared.md` FIRST (shared context, inputs, lens-guards, output contract), then `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r3/lens-briefs/prior-findings.md` (the FIX AUDIT list — you own the tests-class items: r2 W8 (coverage-gate), r2 N8 (client `?slot=`), r2 N9 (fraud stamp test), r2 N10 (authz negatives), r2 N11 (wrong-person notification pin), r2 N12 (sweep effective-contact + route-reset pins)).

Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- New/modified API endpoints without matching coverage
- Auth/authz paths missing negative tests
- Happy-path-only coverage where error handling is implied
- New DB operations without integration coverage
- New state transitions without boundary tests

Test level mix (unit/integration/E2E): flag mismatches as findings.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds:
- PASS: P0 100%, P1 ≥90%, overall ≥80%
- CONCERNS: P0 100%, P1 80–89%, overall ≥80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%

**This is round 3 of a re-review — the r2 gaps are the FIX AUDIT targets. FIRST check whether each r2 gap now has a pinning test in the current worktree (fixed = silent; still missing = finding with original severity, title prefixed `STILL PRESENT (r2): `). Then trace the NEW behaviours of this rework.**

**Round-specific traceability (the load-bearing guards — each needs a pinned test):**

1. **THE r2 BLOCKER — failure paths vs take-over.** The delivery-failure and wrong-person paths must stand down taken-over rows. Pinned? The briefing says the minion's map is "delivery-failure/wrong-person paths now taken_over_at-aware". Find the tests: a bounce on a taken-over row must NOT re-enter the correction loop; a wrong-person on a taken-over row must NOT exhaust; the late completion after take-over must still transition to `form_completed` (§8.6 — was pinned before; must still hold).
2. **Stale-bounce gate (r2 W1).** **`same_day_stale_bounce_stands_down_test` MUST EXIST and pin the SAME-DAY case** (the exact case r1/r2 got wrong — the r2 pins only exercised cross-day fixtures). Verify the fixture: same-day send timestamp vs correction timestamp; the test must fail if the comparison were still lexical. Also: does the test exercise the typed SQL comparison path (integration) not a mocked unit?
3. **Correction session-state clear (r2 W2).** Test asserting `form_opened_at` + `draft_answers` are cleared by the correction SQL (or that a corrected row's fresh form does NOT rehydrate the previous draft)?
4. **Resend effective rule (r2 W4).** Sweep-level test that a cleared channel stays absent after correction? The r2 N12: the effective-contact rule must have sweep-level tests (claimed: `sweep_test.gleam` is a NEW unit test file — verify it pins the corrected-only rule).
5. **Substitute guard rails (r2 W5/W7).** Identical-trio → 400 pinned? History-row re-submit with different details → 409 pinned? Empty prefill pinned (client test)? The r2 N9: creation-fraud stamping asserted on the successor row's `fraud_signals`? Double-submit idempotency (one successor row + one audit) still pinned?
6. **Per-slot re-arm (r2 N4).** Per-slot start re-arms ONLY the requested slot — pinned? No re-arm on declined — pinned? The r2 N8: the client's `?slot=` wire format now tested (not just the server 400)?
7. **Exhaustion LIVE.** Both routes (webhooks + wrong-person) at handler level with audit + **in-app notification** (r2 N11 — the wrong-person leg previously pinned status+audit but not the notification)? First failure does NOT exhaust (boundary test)? Objected row does NOT flip on a late failure?
8. **Authz negatives (r2 N10).** Non-owning-landlord 404 and archived-vacancy 422 for take-over/correct/substitute — pinned?
9. **Client tests.** Menu dispatch (actions actually fire), inline confirm (never modal), Escape closes the menu (r2 N14), toasts, detail refetch after action, route-guarded late-response drop (r2 W3 — toast AND refetch), the W9 route-change reset pin (r2 N12), the B2 serialized adjacency test, the W5 saving-flag reset.
10. **Migration/back-compat.** The additive `corrected_name`/`corrected_at` decode with back-compat; RC4.1 strip assertions untouched; `schema_migration_test` extended with the RC4.3 additive columns (r1 N15 — verify still holds); detail payload integration test asserts the RC4.3 wire fields (r1 N14 — verify still holds).

Counts claimed by the implementer: 528 integration / 547 client / 110 shared / 1480 server unit green at `111e221`. Spot-check the integration test file (`server/test/integration/reference_checks_actions_integration_test.gleam` in the diff) and the NEW `server/test/reference_checks/sweep_test.gleam` for the guard pins above.
