LENS: tests (source tag: "tests") — Test coverage. EXACT OUTPUT PATH: `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r1/lenses/tests.json`

**FIRST: read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r1/lenses/_shared_header.md` for the output contract, schema, and accuracy mandate.** Then apply your lens below.

## YOUR LENS — Test coverage via traceability

For each behaviour change in the diff, trace to a test (new in the diff, or existing). The test files:
- `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-4-r1/server/test/integration/reference_exit_routes_integration_test.gleam` (per-path + registry-coverage)
- `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-4-r1/server/test/reference_checks/result_test.gleam` (AD-9 unit)
- `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-4-r1/server/test/reference_checks/form_copy_test.gleam` (em-dash/copy)
- Any `form_handler_test.gleam` for objection-stickiness/abuse/classify.

Classify each behaviour as FULL / PARTIAL / NONE. Emit one finding per gap:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

**Behavioural changes to trace (the ACs):**
- AC1 submit: deterministic result structuring + guarded transition + result/fraud written + purge_after + submitted_at + audit + notify + thank-you
- AC2 one-submission: second POST → branded page, no dup
- AC3 decline → refused + null verification + null next_attempt_at + notify
- AC4 objection → objected + evidence written ONCE + re-tap no-op + channel 'web'
- AC5 **objection stickiness vs late submit** (the load-bearing one) — is the test REAL (asserts status/outcome/result/evidence unchanged) or tautological?
- AC6 wrong-person → awaiting_correction + next_attempt_at NULL + no notify
- AC7 abuse posture on every POST (honeypot + timing → fake success, stop must NOT object)
- AC8 route-registry coverage (full router+middleware stack, not pure-prefix only)
- AC9 no em-dashes in copy; SSR no-JS reachable

**Critical check:** open `reference_exit_routes_integration_test.gleam` and confirm AC5 (`objected_row_survives_a_late_submit_test` or similar) actually asserts the result JSONB outcome/verification are unchanged (not just the status column). A tautological test (asserts only status, not result) is a finding.

Finally, emit ONE additional finding for the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"; severity: PASS→note, CONCERNS→warning, FAIL→blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds: PASS = P0 100%, P1 ≥90%, overall ≥80%; CONCERNS = P0 100%, P1 80–89%, overall ≥80%; FAIL = P0 <100%, or P1 <80%, or overall <80%.
