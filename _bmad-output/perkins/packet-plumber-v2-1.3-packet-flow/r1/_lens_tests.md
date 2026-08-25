# Lens: tests (Test Coverage) — Perkins r1

**OUTPUT FILE:** `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.3-packet-flow/r1/tests.json`

First read the common context:
`/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.3-packet-flow/r1/_lens_common.md`

## Your lens
Test coverage analysis via traceability. For each behaviour change in the diff,
trace to a test (new in `core/flow_test.odin`, or existing in
`core/*_test.odin`, or the harness golden `demos/flow.dem`). Classify as
FULL / PARTIAL / NONE coverage. Emit one finding per gap.

Behaviour changes to trace (the 1.3 contracts):
1. Per-hop forwarding source→router→sink (the packet traverses the router).
2. Forwarding table rebuild on topology change (rule 1 — the story's Golden).
3. E29 no-stale-route (a packet spawned unroutable re-forwards once a path
   appears — NO cached route).
4. Replay byte-identical over the flow (E10).
5. Unroutable packet waits then flows (E28 shape).
6. The render shows the packet moving (T2 mid-traversal frame — the harness
   golden).
7. The `on_edge`/id-0 handling (a packet on pipe id 0 / at node id 0).
8. Delivery emits `Packet_Arrived`; delivered packets are culled.

Also emit ONE advisory gate finding:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate", source: "tests"
- severity: PASS→note, CONCERNS→warning, FAIL→blocker
- Gate thresholds: PASS = P0(critical path) 100% & P1 ≥90% & overall ≥80%;
  CONCERNS = P0 100% & P1 80–89%; FAIL = P0 <100% or P1 <80% or overall <80%.

Note: this PR adds 5 new `@(test)` tests + a flow demo golden. Calibrate the
gate to a trivial single-path story (1.3) — later slices (ECMP, QoS, SLA,
demolish) are explicitly out of scope and NOT gaps here.

## Output
Write ONE valid JSON array to your OUTPUT FILE (source = `"tests"`). `[]` plus
the one gate finding is valid. Accuracy > volume. Then print `LENS DONE: tests`
and stop.
