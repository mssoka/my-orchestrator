# LENS: Test Coverage (source: `tests`)

You are reviewing a code diff. Read-only repository access for verification.

--- REPOSITORY / WORKTREE ---
Worktree: `/Users/moses/.herdr/worktrees/RightTenantryAgents/perkins-boundary-gate-slot-clear-r1`
Canonical diff: `/Users/moses/code/_bmad-output/briefings/...` — actual diff at: `/Users/moses/code/_bmad-output/perkins/righttenantryagents-boundary-gate-slot-clear/r1/diff.patch`

--- PROJECT CONVENTIONS ---
Python + pytest + uv. Tests in `tests/unit/` + `tests/integration/`. The regression test for this fix is in `tests/unit/test_gate_state_marshalling.py`.

--- SPEC / CONTEXT ---
- `/Users/moses/code/_bmad-output/briefings/perkins-righttenantryagents-boundary-gate-slot-clear-r1.md` (CRITICAL: the "regression test must drive the real path + negative control bites" lens-guard)
- `/Users/moses/code/_bmad-output/briefings/righttenantryagents-boundary-gate-slot-clear.md` (REQUIRED regression test; do NOT mask via simulate.form_body shortcut — the #599 r2 lesson)

The regression test requirement: drive the REAL `_run_*_compliance_gate` loops through the production state-view divergence (`_DivergentCtx`); real scrub + real finalize + real cross-check; only the judge's state-writes + repair pass stubbed. Neutralized pops → the new tests FAIL (the stale dirty review `passed: False` survives alongside the clean stamp, finalize bypasses the cross-check, fail-closes); restored → pass. The inverse (genuinely-missing judge still fail-closes) must be asserted.

--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check FOR THIS DIFF:
- Does the new test ACTUALLY exercise the slot-clear, or does it stub/bypass the gate loop? (Read `_multi_attempt_judge_run_node` + the test bodies — does `agent_mod._run_boundary_compliance_gate` / `_run_final_compliance_gate` actually run, or is it mocked away?)
- Does the negative control bite? (If you mentally neutralize the `pop(...)` lines, does the test fail? Trace the data flow: attempt 0 writes dirty review + dirty stamp; attempt 1 — does the pop matter?)
- Is the inverse (genuinely-missing judge fail-closes) still covered by an EXISTING test? Name it.
- Is the single-attempt clean case (#173) still covered?
- Are both gates (boundary + final) covered symmetrically?
- Does the test mask the fix via a `simulate.form_body`-style shortcut or by hand-seeding the finalize input instead of driving the real loop?

Test level mix (unit/integration/E2E): flag mismatches as findings.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds: PASS: P0 100%, P1 ≥90%, overall ≥80% | CONCERNS: P0 100%, P1 80–89%, overall ≥80% | FAIL: P0 <100%, or P1 <80%, or overall <80%

--- OUTPUT ---
ONE valid JSON array (include the advisory-gate finding as one element). Schema:
{
  "source": "tests",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<exact lines you READ, verbatim; 'N/A' only for no-code-reference findings>",
  "detail": "<≤40 words>",
  "recommended_fix": "<≤40 words>"
}
Output contract: ONLY the JSON array. `[]` is NOT expected here — always emit the advisory-gate finding.
ACCURACY MANDATE: every finding re-verified against the actual code; unverified DISCARDED silently. Quote exact lines. No hedging.

--- FILE-OUTPUT CONTRACT ---
Write your final JSON array to: `/Users/moses/code/_bmad-output/perkins/righttenantryagents-boundary-gate-slot-clear/r1/tests.json`
Then stop.
