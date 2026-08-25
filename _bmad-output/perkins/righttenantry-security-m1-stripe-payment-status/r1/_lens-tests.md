# Lens: Test Coverage (source: `tests`)

Read your shared context first: `/Users/moses/code/_bmad-output/perkins/righttenantry-security-m1-stripe-payment-status/r1/_shared.md` — it defines your inputs, the round-specific guards, the output schema, and the accuracy mandate. Your assigned `source` value is `tests`. Your output path is: `/Users/moses/code/_bmad-output/perkins/righttenantry-security-m1-stripe-payment-status/r1/tests.json`

--- YOUR LENS ---

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

The behaviour changes in this diff include:
1. M-1 gate: `checkout.session.completed` with payment_status != "paid" (processing / unpaid / structurally missing) refuses unlock, claims event, acks 200, no audit/burst/notification
2. Fail-closed decode: absent `payment_status` → None → "" → pending
3. New arm: `checkout.session.async_payment_succeeded` routed through the same completion machinery; full pending → settle → replay-idempotent cycle (unlock, row completed, audit, notification, burst scoring)
4. Card-only: `payment_method_types[0]=card` in `checkout_session_form_body` (unit-test tripwire)
5. Idempotency tag bump `consent_v3_card_only` consumed in the session-create path
6. `arm` threading through claim + error/consent log messages
7. Existing completed-event fixtures now default `payment_status="paid"` (no silent flip of pre-existing tests)

Non-vacuity checks (the round guards demand these): for the processing/unpaid/missing fixtures, would the test actually FAIL if the gate were removed (i.e. do they assert the locked/pending state rather than merely asserting a 200)? For the settle test: does it drive the whole cycle end-to-end (unlock + completed row + audit + notification + burst) and the replay short-circuit, or is any part stubbed? Is there any coverage for a card-only happy-path regression (existing completed tests through the gate with "paid")?

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
