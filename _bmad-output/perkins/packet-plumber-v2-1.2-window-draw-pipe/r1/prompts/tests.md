# LENS: Test Coverage (source = `tests`)

First load the shared context: read `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.2-window-draw-pipe/r1/prompts/_shared.md` (lens-guards, output schema + contract, empirical gate status, canonical input paths). Follow it exactly.

## YOUR LENS — test coverage via traceability
For each BEHAVIOUR CHANGE in the diff, trace to a test (new in the diff, or existing). Classify FULL / PARTIAL / NONE coverage. Emit one finding per gap. Severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Behaviours to trace (the 1.2 deltas):
- **Replay-equality over a DRAW sequence (lens-guard #1, P0):** is there a test that records a draw sequence AND replays it byte-identically AND is non-vacuous (asserts the draw actually changed state)? → `core/determinism_test.odin::test_replay_byte_identical`. Is the APP's fast-path↔log convergence (E10) tested anywhere, or only the pure-log path?
- **Topology validation rejections (E3/E26/span/missing-node/unknown-tier, P0/P1):** → `core/topology_test.odin`. Are all five rejection paths covered? Is "a rejected draw mutates nothing" asserted?
- **Monotonic ids (E11, P1):** → `test_node_ids_monotonic_never_recycled`. Is the never-recycled-on-demolish half covered (no demolish yet — is that a gap or out-of-scope)?
- **Snap inclusive radius (E4, P1):** → `test_distance_metric_pinned`. Is the snap logic in `app/main.odin::snap_node` (the f64 metric + tie-break) tested, or only the core `span_between`? (App-side snap is UI; core metric is pinned — is that enough?)
- **The binary log round-trip + rejections (P0):** → `test_action_log_binary_roundtrip`. v1-log rejection, unknown-tag rejection covered?
- **The harness replay gate / T1 manifests / T2 pixel golden (P0):** → exercised by `tools/harness.sh run` (boot + draw). Is the T2 compare actually byte-exact (lens-guard #4)? Is there a test that the harness's `lower_intents` ↔ `intent_apply_tick` convention matches the app's `apply_tick = tick+1`?
- **W1 drift-rejection (lens-guard #5, P0):** → `tools/harness.sh drift-check`. Is it in CI (`.github/workflows/ci.yml`)? Does it actually assert REJECTION (not just mutation)?

Blind-spot heuristics: happy-path-only coverage where error handling is implied; new state transitions without boundary tests; the `isqrt` edge cases (x=0, x=1, large values, the round-half-up branch).

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate", severity: PASS→note / CONCERNS→warning / FAIL→blocker
- detail: rationale with coverage percentages; recommended_fix: what would raise the gate.
Gate thresholds — PASS: P0 100%, P1 ≥90%, overall ≥80%; CONCERNS: P0 100%, P1 80–89%, overall ≥80%; FAIL: P0 <100%, or P1 <80%, or overall <80%.

## OUTPUT
Write ONE valid JSON array (schema + contract in `_shared.md`) to:
`/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.2-window-draw-pipe/r1/tests.json`

`source` = `"tests"`. Only the JSON array in the file (include the advisory-gate finding as one element). `[]` is NOT expected from you — at minimum emit the advisory-gate finding. Verify every claim by reading the actual code/tests; quote exact lines in `evidence`. When done, stop.
