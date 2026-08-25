--- YOUR LENS (source tag: tests) ---

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

Test level mix (unit/integration/E2E): flag mismatches as findings.

The claimed new tests (verify each EXISTS, RUNS, and actually BITES — a test that can't fail is not a test):
- app/render/camera_test.odin — the camera-math pins: seed/attach classification (incl. the exactly-10 boundary + dead id), pullback target (in-view no-op / out-of-view target / fit floor / margin edge), zoom step compounding, anchor-center pinning, pan-center mapping, clamp-center (fit pin / world edges / interior passthrough).
- app/input/camera_input_test.odin — the input-wiring pins: wheel → Zoom → on_zoom with exact anchor; empty-ground drag → Pan with exact deltas, never draws, release never selects; plain click still selects/deselects THROUGH the pan surface; node-anchored draw never pans.
- app/pullback_test.odin — the pullback pins: SEED arms + target within fit floor + district+margin included in the CONVERGED viewport; ATTACH never arms; toggle OFF + already-visible no-op; no-snap frame-1 partway + still-in-flight at 0.5s + convergence clears pullback.
- app/settings_test.odin — the settings pins: v2 round-trip + out-of-range pullback byte; v1 file loads a11y unchanged with pullback ON; corrupt v1 checksum falls back.

Round-briefing flags to verify (not assume): the conflict gates actually bite (pan never starts a draw; a pan release never click-selects; a node press still draws; a plain click still selects) — trace each assertion to the code path that makes it fail-able. Is the two-finger touch Pan path (exec Pan via touch_map) covered anywhere, or only the mouse pan? Is the PP_CAM_E2E drive wired into any gate (harness verb / CI), or is it manual-only evidence? Is the NOC wheel-ownership policy (scroll only over panel; zoom elsewhere; modal blocks) traced to ANY test, or only to the e2e captures? Is effect_zoom's NOC-panel branch PP_DEBUG-only — and is there a test pinning the release-build behavior (wheel always zooms)?

Count the actual @(test) functions added per file and compare with the PR body's claimed counts (4 camera-math + 4 input + 4 pullback + 2 settings; briefing says 18 pins total = 8 original + 10 new) — a miscount is a documentation finding (note), not a coverage gap per se.

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

Output path: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r2/tests.json
