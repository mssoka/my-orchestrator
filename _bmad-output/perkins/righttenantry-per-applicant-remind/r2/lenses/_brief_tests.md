Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80-89% OR P2 gap
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
- PASS: P0 100%, P1 >= 90%, overall >= 80%
- CONCERNS: P0 100%, P1 80-89%, overall >= 80%
- FAIL: P0 < 100%, or P1 < 80%, or overall < 80%

Round-2 specific: round 1's gate was CONCERNS (P0 100%, P1 ~87.5% — the BAD_BODY validation branches were the only untested P1 scenarios). The fold-in added 3 validation tests (malformed body, empty email, invalid email). Re-evaluate the gate with them included — does it clear 90% now? Also check the 3 new tests are real (would fail if the branch broke) rather than tautologies, and note any validation branch still untested (e.g. wisp.require_json's no-body path).
