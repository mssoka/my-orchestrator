# LENS: tests (source tag: `tests`) — Perkins r1 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r1/lens-briefs/_shared.md` FIRST (shared context, inputs, lens-guards, output contract).

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

**Round-specific traceability (the load-bearing guards — each needs a pinned test):**

1. **Take-over (A7):** guarded pre-states (queued/contact_initiated/unreachable OK; wrong-state rejection), `taken_over_at` write + cadence clock cleared, **sweep exclusion pinned by test** (the briefing says "Sweep exclusion pinned by test" — find that test), late completion after take-over still transitions to form_completed + notifies (the §8.6 transition).
2. **Correct (AD-7/A1):** awaiting_correction → queued with corrected trio, snapshot immutable (original contact_* unchanged — test asserts), `correction_cycles = 1`, re-arm (`next_attempt_at = now()`), audit row written. **Second correction blocked (cycle > 1) — test pinned?**
3. **Substitute (AD-16):** new row created, prior retained, audit carries old+new ids. **Double-submit idempotency — test asserts exactly one successor row + one audit on double-submit?**
4. **Exhaustion LIVE:** second failure → `unreachable` + `referee_contact_invalid` at the webhook routes AND the wrong-person route, with audit + in-app notification — both routes tested? First failure does NOT exhaust (boundary test)?
5. **Ownership/authz:** action endpoints reject a landlord who doesn't own the row (negative test)? Pre-state guard rejection (0-row-result stand-down) tested?
6. **Client tests:** menu dispatch (actions actually fire — the RC4.2 guard flip), inline confirm render (never modal), toasts, detail refetch after action, `?slot=` per-row start, skipped-row re-enable.
7. **Migration/back-compat:** the additive `corrected_name` decodes with back-compat (old payload shape still decodes); RC4.1 strip assertions untouched (in `shared/test/reference_call_test.gleam`).

Counts claimed by the implementer: 512 integration / 540 client / 110 shared / 1476 server unit green. Spot-check the integration test file (`server/test/integration/reference_checks_actions_integration_test.gleam` in the diff) for the guard pins above.
