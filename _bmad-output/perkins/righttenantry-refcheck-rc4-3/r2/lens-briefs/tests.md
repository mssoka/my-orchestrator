# LENS: tests (source tag: `tests`) — Perkins r2 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r2/lens-briefs/_shared.md` FIRST (shared context, inputs, lens-guards, output contract), then `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r2/lens-briefs/prior-findings.md` (the FIX AUDIT list — you own the tests-class items: W12, N3, N4, N12, N13, N14, N15).

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

**This is round 2 of a re-review — the r1 gaps (W12, N3, N4, N13, N14, N15, N12) are the FIX AUDIT targets. FIRST check whether each r1 gap now has a pinning test in the current worktree (fixed = silent; still missing = finding with original severity, title prefixed `STILL PRESENT (r1): `). Then trace the NEW behaviours of this rework.**

**Round-specific traceability (the load-bearing guards — each needs a pinned test):**

1. **Take-over (A7):** guarded pre-states (queued/contact_initiated/unreachable OK; wrong-state rejection), `taken_over_at` write + cadence clock cleared, **sweep exclusion pinned by test** (the briefing says "Sweep exclusion pinned by test" — find that test), late completion after take-over still transitions to form_completed + notifies (the §8.6 transition). HTTP-level wiring test (r1 N3 — take-over HTTP arm with a REAL owning landlord, not a mismatched uuid).
2. **Correct (AD-7/A1):** awaiting_correction → queued with corrected trio, snapshot immutable (original contact_* unchanged — test asserts), `correction_cycles = 1`, re-arm (`next_attempt_at = now()`), audit row written. **The r1 B1 double-pin: (a) positive — corrected row re-claims T0 to the corrected contact (attempt_count reset + form_token rotation); (b) negative control — `corrected_row_without_attempt_reset_dead_ends_test` (a corrected row WITHOUT the reset dead-ends). Both exist?** Second correction blocked (cycle > 1) — test pinned? terminal_reason-clearing assertion now meaningful (r1 N4)?
3. **Substitute (AD-16):** new row created, prior retained, audit carries old+new ids. **Double-submit idempotency — test asserts exactly one successor row + one audit on double-submit?** Creation-fraud stamping on substituted rows (r1 N1) tested? Substitute HTTP arm with a REAL owning landlord (r1 N3)?
4. **Exhaustion LIVE:** second failure → `unreachable` + `referee_contact_invalid` at the webhook routes AND the wrong-person route, with audit + in-app notification — **both routes tested at the handler level (r1 W12 — the r1 version only drove the SQL directly)**? First failure does NOT exhaust (boundary test)? Stale-bounce stand-down tested (r1 W3 — a redelivered PRE-correction failure does not stamp)?
5. **Ownership/authz:** action endpoints reject a landlord who doesn't own the row (negative test)? Pre-state guard rejection (0-row-result stand-down) tested? The app↔vacancy mismatch rejection (r1 W10 fix — `verify_application_in_vacancy.sql` 409/422 tested)?
6. **Client tests:** menu dispatch (actions actually fire — the RC4.2 guard flip), inline confirm render (never modal), toasts, detail refetch after action, `?slot=` per-row start (r1 N13 — invalid slot → 400 and the wire format), skipped-row re-enable, the B2 serialized adjacency test (enabled buttons have NO disabled attribute), the W5 saving-flag reset, the W8 late-response route guard, the W9 route-change reset.
7. **Migration/back-compat:** the additive `corrected_name`/`corrected_at` decode with back-compat (old payload shape still decodes); RC4.1 strip assertions untouched (in `shared/test/reference_call_test.gleam`); `schema_migration_test` extended with the RC4.3 additive columns (r1 N15); detail payload integration test asserts the RC4.3 wire fields (r1 N14).

Counts claimed by the implementer: 521 integration / 544 client / 110 shared / 1477 server unit green at `0fdbf93`. Spot-check the integration test file (`server/test/integration/reference_checks_actions_integration_test.gleam` in the diff) for the guard pins above.
