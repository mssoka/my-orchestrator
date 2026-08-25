You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. You are a REVIEW LENS: you never fix, never push, never merge — findings only.

--- INPUTS (absolute paths) ---
- DIFF: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r4/diff.patch
  (the canonical diff under review — 22 files, 2682 lines; the two docs/captures/*.png entries are binary one-liners; read it whole)
- WORKTREE (the checkout at exactly the reviewed sha af26d8a — every verification read happens here): /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-camera-zoom-r4
- PROJECT CONVENTIONS: /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-camera-zoom-r4/project-context.md
- SPEC / CONTEXT (review_mode = full):
  1. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r4/spec/job-briefing.md
  2. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r4/spec/perkins-briefing-r4.md

--- ROUND CONTEXT (round 4 — FIX AUDIT) ---
Round 4 of PR #89. Round 3 (CHANGES_REQUESTED) found 2 blockers + 8 warnings + 14 notes; the advisory coverage gate was CONCERNS (P1 ~87%). Head af26d8a claims: B1 both mid-ease mirror pins, B2 when-branched build pins + gate-9 PP_DEBUG test leg, W4 pin de-vacuified (router AFTER the seed), advisory closed (wheel band / pan values / ease-rate band pins), N1/N6/N7 completed. Prior findings: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/consolidated.json (still-present prior items are carry-forwards, not new discoveries).

--- YOUR LENS (source tag: tests) ---

Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- New/modified API endpoints without matching coverage
- Happy-path-only coverage where error handling is implied
- New state transitions without boundary tests
- Test level mix (unit/integration/E2E): flag mismatches as findings.

Round-specific audit (verify the NEW r4 pins' SUBSTANCE — each must FAIL under the exact regression it claims to pin; do the arithmetic yourself from the fixture):

- Fixture facts (app/pullback_test.odin pullback_test_app): world 64×36 tiles × 26px = 1664×936 px; win 1280×720; fit = min(1280/1664, 720/936) = 0.76923 (both ratios 1.3 — world center (832, 468)); the fixture spawns 3 nodes BEFORE any test spawn (2 terminals + 1 router), so a test's first spawn_with_event gets id 3 and its place_router id 4 — the comments claiming "id 6"/"id 7" are the r3 N14 disease: verify actual ids (does run_init spawn anything? read it).
- `pan_clamps_at_the_target_zoom_not_the_live_zoom` (B1): mirror 1 — live 2.0 / target 1.0, cam_wy_to=585, dy=-200: compute camera_pan_center(585, -200, fit, 2.0) (read the proc — sign convention!), then camera_clamp_center at zoom 1.0 (the FLOOR: viewport == world → center pinned to 468?) — does the asserted 468 match the code's math, and would the OLD live-zoom clamp (y-band at 2.0 = 468 ± (720/2)/(fit·2) = [234, 702]) have produced a DIFFERENT value (i.e. the pin BITES)? Mirror 2 — live 1.0 / target 2.0, anchor cam_wx_to=700, pan (0,0): under the OLD code the 1.0 clamp pins to 832 → the ==700 assertion fails → bites; but ALSO check the test's own second assertion band [416, 1248] (the real 2.0 x-band = 832 ± (1280/2)/(fit·2) = [416, 1248]) vs the COMMENT's "[278, 762]" — a wrong-band comment.
- `wheel_clamp_band_and_pan_values_are_pinned` (advisory): +20 notches from 4.0-fixture — camera_zoom_step multiplies 1.25^20 ≈ 86.7 → clamps at 4.0 ✓? -20 from wherever the fixture target sits → clamps at 1.0 ✓? The pan-value leg: after manually setting cam_zoom=cam_zoom_to=2.0, cam_wx_to=520, effect_pan(100, 0) → expected 520 − 100/(fit·2) ≈ 455 — verify camera_pan_center's actual formula + sign produce EXACTLY that, and that the 1e-3 tolerance is meaningful; also verify the clamp doesn't fire at 455 (2.0 x-band [416,1248] — 455 is inside, barely: 39px of headroom — would a slightly different fit break the leg?).
- `pullback_ease_rate_sits_in_the_ruled_band` (advisory): the fixture arm (seed at (23,10) from camera 4.0@260,260) → target zoom ≈ ?; the ease converges when residual < 0.005 (read camera_update's pullback ease + snap threshold + CAMERA_PULLBACK_EASE rate); compute the convergence frame count at the pinned rate — does it land in [90, 150]? Would a 0.14-rate regression (r3 W7's example, ~0.66 s) fall OUTSIDE the band (i.e. does the pin discriminate)?
- The de-vacuified W4 pin: seed spawned FIRST (event), router placed AFTER (no event, NEWER id) — the newest-first walk must traverse + skip the router. Verify: the OLD r2 count-based walk-back (next_node_id−1 → the router) would have mapped the event to the router → pullback NOT armed → the expect(app.pullback) FAILS under the regression → the pin bites; and simulate mentally: does the CURRENT walk (camera_newest_terminals — read it) actually probe the router before the seed (ids 4 then 3)?
- The when-branched build pins (B2): `effect_zoom_and_pan_respect_the_wheel_policy_and_modal` now sets app.overlay_on = true and branches on `when #config(PP_DEBUG, false)` — in a plain `odin test app` run (gate 2) the else/release leg asserts zoom-over-panel; in gate 9's `odin test app -define:PP_DEBUG=true` the debug leg asserts scroll-not-zoom — verify BOTH legs are actually run in CI (read tools/ci-local.sh gate 9 + .github/workflows/ci.yml).
- Remaining r3 P1/P2 gaps NOT folded (verify absent in the worktree, then emit as carry-forward gaps): N4 (start_run's pan-latch reset untested — r2 W10 explicitly asked), N11 (camera_newest_terminals direct unit pins: 0-found bail, >8 spawns, dead-id skip, newest-first order), N12 (the claimed "a second SEED mid-ease retargets" has no test), W2 (the app7 settings-adjust leg writing the real HOME dotfile — still present?).
- Count the actual @(test) procs per test file vs the PR body's "4 + 4 + 4 + 2" claim (third round of the N3 drift if still stale).

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with coverage percentages (P0/P1/overall over the diff's behaviour changes)
- recommended_fix: what would raise the gate

Gate thresholds:
- PASS: P0 100%, P1 ≥90%, overall ≥80%
- CONCERNS: P0 100%, P1 80–89%, overall ≥80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this path (create parent dirs if needed; write the file, do not print the JSON into chat):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r4/tests.json

Each element must match this schema exactly:
{
  "source": "tests",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<≤40 words>"
}

Output contract:
- The file contains ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, STOP. Do not fix anything. Do not push. You are a reviewer.

ACCURACY MANDATE: every finding will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY. Open the file, read the lines, paste them verbatim in `evidence`. Hedging ("might", "could") means you have not verified — drop it. Accuracy > volume.
