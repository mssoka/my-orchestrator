# Lens: Test Coverage (source: `tests`) — Perkins RC3.5 r1

Read and follow `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r1/lens-prompts/_shared_context.md` first (inputs, invariants, output contract). Then apply this lens.

## YOUR LENS — test coverage analysis via traceability
For each behaviour change in the diff, trace to a test (new in the diff, or existing — mainly `server/test/integration/reference_checks_sweep_integration_test.gleam`). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Behaviours to trace (the briefing's "required tests"):
1. **No-duplicate-T0 across a retry** (the hard exactly-once requirement) — is there a REAL test? Does it actually re-run the sweep and assert 0 re-invites + 0 due?
2. Per-step cadence (T0/T+24/T+48/T+96/T+144) — a fake-clock test per step?
3. The guarded-update RACE (two concurrent ticks) — is there a real concurrency test, or only a sequential retry test? If only sequential, is that a gap?
4. Terminal-state respect: objected (sticky), taken-over (skipped), awaiting_correction (excluded by NULL next_attempt_at). Is each covered?
5. Co-nudge gate: fires when unopened+no-draft; suppressed when form opened; suppressed when draft exists.
6. partial vs unreachable from drafts (confidence capped medium).
7. Failure path (mark_failed → status failed, outcome NULL, Sentry, NO notification).
8. Warm-handoff fires exactly once at T+96 (notification_count==1 across the full walk; 0 at T+144).

Blind-spot heuristics: new DB operations without integration coverage; new state transitions without boundary tests; happy-path-only where error handling is implied; the no-op-without-Twilio-keys path.

Also emit ONE advisory-gate finding:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate", severity PASS→note, CONCERNS→warning, FAIL→blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate
Gate thresholds: PASS = P0 100%, P1 ≥90%, overall ≥80%; CONCERNS = P0 100%, P1 80–89%, overall ≥80%; FAIL = P0 <100% or P1 <80% or overall <80%.

## OUTPUT
Write ONLY your JSON array to: `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r1/tests.json`
Use `"source": "tests"`. Then stop.
