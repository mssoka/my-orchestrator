Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- New command kind Cmd_Place_Router: validation paths (terminal reject, unknown type, off-map, min-sep, boundary AT the radius), apply path (gen bump, id monotonic, live junction), serialization round-trip, version-2 log rejection, replay byte-identical — which are covered by core/placement_test.odin and which are not?
- Port limits: 5th pipe on basic (4 ports), demolish frees port, terminals never limited, mid (8) / high (16) capacities — covered? What about a draw where BOTH endpoints are junctions (both port-checked)? What about the app-layer paths: tray arm/cancel/ESC/right-click, press-move guard, chip swallow — are any of these tested (or is that acceptable for a game app layer)?
- Negative controls: does a neutralized validation actually make tests go red (the min-sep radius test pins boundary semantics)?
- The demo place.dem + goldens/place.t1 + place T2 PNGs: does the T2 golden actually pin the placed router + new pipe?

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
