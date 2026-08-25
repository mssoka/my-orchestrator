# Lens: TEST COVERAGE (source: `tests`)

**First:** Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r1/prompts/_preamble.md` in full and internalize the lens-guards.

Test coverage analysis via traceability. For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics: new/modified API endpoints without coverage; auth/authz missing negative tests; happy-path-only where error handling is implied; new DB operations without integration coverage; new state transitions without boundary tests.

Trace these behaviours to tests (read `server/test/reference_checks/fraud_test.gleam`, `server/test/integration/reference_checks_fraud_integration_test.gleam`, and existing form/result suites):
- `fraud.creation_fraud_signals` — full AD-10 table (unit-tested? AC1)
- `fraud.submission_fraud_signals` + `form_session_block` — completion_seconds, ip_matches, ua_matches, focus_seconds, raw IP/UA inside form_session (unit-tested? AC3)
- `fraud.carry_line_type` — empty/unparseable/missing-key paths (is it tested at all? grep)
- `fraud.with_referee_contact_invalid` — the spec lists it as an OWNED entry point + AC5. Is the STAMPING fn unit-tested? Is the Gleam-level `with_referee_contact_invalid` helper actually present + tested? (The diff shows `stamp_referee_contact_invalid` SQL tested in integration, but verify the spec's named `with_referee_contact_invalid` Gleam function exists and is tested.)
- `lookup.line_type_to_string` / `line_type_from_string` — round-trip + unknown fallback tested? (grep)
- **Phase 1 wiring (`trigger.gleam::stamp_creation_fraud`)** — is the actual trigger integration path tested, or only the SQL contract directly? The integration test calls `stamp_creation_fraud_signals` directly, not via the trigger. Is there a test that the trigger fires it? (AC2's "at row creation".)
- **Phase 2 wiring (`form_handler.gleam::build_submission_fraud_signals` + `save_submit`)** — is the actual submission path (handle_submit → save_submit → result with fraud_signals) integration-tested end-to-end, or only the SQL + pure unit? The spec's AC says "Integration coverage for the Phase 1 + Phase 2 writes." Verify whether Phase 2 (the form submit writing `result.fraud_signals` + column) has integration coverage, or only unit coverage of the pure builder.
- W1 (`claim_webhook_event` removal) — is `resend_redelivery_is_idempotent_test` still present and does it still assert audit_count==1 / notification_count==1? (AC7 pins this.)
- Innocent-reuse fixtures (AC4) — are they real (same-name letting agent across apps → count 0)?

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate", severity: PASS→note, CONCERNS→warning, FAIL→blocker
- detail: rationale with coverage percentages for the P0/P1/P2 paths above
- recommended_fix: what would raise the gate

Gate thresholds: PASS = P0 100%, P1 ≥90%, overall ≥80%; CONCERNS = P0 100%, P1 80–89%, overall ≥80%; FAIL = P0 <100% OR P1 <80% OR overall <80%.

**Output:** Write ONLY a JSON array to `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r1/tests.json`, using `source: "tests"`. Follow the schema, accuracy mandate, and lens-guards from the preamble. Include the advisory-gate finding as the last element. Stop when written.
