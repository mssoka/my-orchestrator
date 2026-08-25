# Lens: TEST COVERAGE (source: `tests`)

**First:** Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r2/prompts/_preamble.md` in full and internalize the lens-guards + the fix-audit scope.

Test coverage analysis via traceability. For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per NEW gap with severity: blocker (P0 gap or P1 <80%), warning (P1 80–89% or P2 gap), note (P3 gap).

## Fix-audit priority — W2, W3, W4, N5, N6 (the r1 test-coverage findings)

Verify each r1 coverage finding is closed at `5576ccb` (read the actual test files; grep, do not assume):
- **W2 (carry_line_type).** `server/test/reference_checks/fraud_test.gleam` — are there real tests for the 3 branches: empty→Unknown, valid→mapped, missing-key/unparseable→Unknown? (r1 said 0 tests.)
- **W3 (Phase-1 trigger wiring).** `server/test/integration/reference_checks_trigger_integration_test.gleam` — is there an integration test that calls `trigger.run_create_checks` AND asserts the `fraud_signals` column landed (not just `Created(count:)`)? (r1 said the column write was unasserted.)
- **N5 (submit form_session block).** `server/test/integration/reference_exit_routes_integration_test.gleam` — does the submit test now assert the FULL form_session block (completion_seconds, ip_matches_applicant, device_fingerprint_match, referee_ip/ua), not just focus_seconds_reported? (r1 said richer fields were unit-only.)
- **N6 (line_type round-trip + unknown fallback).** `server/test/reference_checks/lookup_test.gleam` — are there tests for `line_type_to_string` (all variants), `line_type_from_string` (round-trip), and the unmapped-string → Unknown fallback? (r1 said 0 tests.)
- **W4 (advisory gate).** Re-evaluate the gate against the CURRENT coverage. If W2+W3+N5+N6 are all closed (P1 ≥90%, overall ≥80%), the gate should now be PASS. Emit the gate finding accordingly.

Each of W2/W3/W4/N5/N6 correctly closed → FIXED (do NOT re-file). A gap that is still open, or a test that asserts the wrong thing (false confidence), is a NEW finding.

## Delta pass — new behaviour, new coverage

Trace any NEW behaviour the B1 fix or W1 extraction introduced and whether it is covered:
- **B1 regression coverage.** Is there a test that a re-trigger (idempotent, inserted==0) does NOT wipe a submitted sibling's fraud_signals? (This is the B1 blocker — its regression test is load-bearing.) Is there a sibling test (a re-trigger creating a NEW row leaves the submitted sibling untouched)? Read `reference_checks_trigger_integration_test.gleam` for `re_trigger_*` tests and verify they assert the RIGHT invariant (the submitted form_session survives).
- The `fraud_inputs.gleam` helpers (`effective_contact`, `other_refs_from_rows`, `cross_application_reuse`) — are they covered directly or via the wiring tests?
- The `stamp_creation_fraud_signals` / `stamp_referee_contact_invalid` SQL contracts — covered by `reference_checks_fraud_integration_test.gleam`? (r1 confirmed this; re-verify the stamp-preserves-keys + null-column cases still hold.)

Finally, emit ONE advisory-gate finding (the W4 re-evaluation): title "Advisory test gate: PASS|CONCERNS|FAIL", category "coverage-gate", severity PASS→note / CONCERNS→warning / FAIL→blocker, detail with the P0/P1/P2 percentages, recommended_fix what would raise it. Gate thresholds: PASS = P0 100%, P1 ≥90%, overall ≥80%; CONCERNS = P0 100%, P1 80–89%, overall ≥80%; FAIL = P0 <100% OR P1 <80% OR overall <80%.

**Output:** Write ONLY a JSON array to `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r2/tests.json`, using `source: "tests"`. Include the advisory-gate finding as the last element. Follow the schema, accuracy mandate, and lens-guards from the preamble. Empty array (minus the gate finding) is valid. Stop when written.
