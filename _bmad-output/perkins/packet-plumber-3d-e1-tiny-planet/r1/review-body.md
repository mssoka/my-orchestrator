## 🤖 Perkins automated review — round 1

**Job:** packet-plumber-3d-e1-tiny-planet · **Reviewed sha:** 9fad932 · **Reviewers:** 7/7 completed
**Verification:** 46/47 findings confirmed against the code — 1 discarded as false-positive

**Independently re-verified this round:** headless suite `godot --headless -s res://tests/run_tests.gd` → `SUITE RESULT: PASS (0 failure(s))`, exit 0 (Godot 4.7.1) · LSP diagnostics on all 17 GDScript files — no genuine errors/warnings · the 4 committed captures are real 1600×900 in-game PNGs and on-brief (globe+wedges / district / completed arc / merged bundle), look-parity with the little-planet frames holds (vision-checked), nothing copied · README + PR body carry the run command (A2 holds). The math spine, camera no-roll sweep, disambiguation rule, and no-sim contract all verified clean.

### Blockers (3)

1. **Node-separation formula never applies the documented 0.25 rad minimum — 13 node pairs ship with overlapping pick hitboxes** `[blind, edge, acceptance, architecture, codebase]` — `scripts/world_seed.gd:148`
   `sep := MAXF_SEPARATION_FLOOR * (1.0 - attempt/80.0) * MIN_NODE_SEPARATION_RAD` = 0.25×0.25 = 0.0625 at attempt 0 — exactly the floor, so separation is a **constant 0.0625 rad (~0.5 units at R=8)** and the decay is dead code. Runtime-verified at the shipped seed: min pairwise separation **0.678 units** (n25/n30) vs the **1.9-unit** hitbox diameter. This falsifies the PR body's "node separation 0.25 rad keeps the 0.95-radius hitboxes non-overlapping" and the spec's "separation floor keeps hitboxes disjoint". Presses on visually empty surface inside an inflated overlapping sphere begin DRAW instead of ORBIT — the epic's *"input disambiguation never misfires"* contract is undermined in practice.
   **Fix:** drop the `MAXF_SEPARATION_FLOOR` factor (`sep := MIN_NODE_SEPARATION_RAD * (1.0 - attempt/80.0)`, floored at 25%), re-run the suite, regenerate captures.

2. **Connect-verb gesture lifecycle has zero test coverage** `[tests]` — `scripts/connect_controller.gd:76`
   grep-verified: no test touches `draw_begin/draw_move/draw_end/draw_cancel`; only the `connect_programmatic` shortcut is exercised. E1.3's release-to-connect / cancel-elsewhere — the slice's primary verb — is unverified, and two confirmed latent bugs (stale `_last_preview_end`; stale snap-target commit, see Notes) live inside exactly this untested region.
   **Fix:** drive the real gesture path headless on the instantiated main scene: press-on-node → move → release-on-node commits; release-elsewhere cancels; focus-loss cancels.

3. **Advisory test gate: FAIL** `[tests]` — gate roll-up of blocker 2 per the review-skill thresholds (P0 critical path < 100%). Rises to PASS once the gesture lifecycle is covered.

### Warnings (6)

1. **Placement last-resort loop never retries** `[blind, edge]` — `world_seed.gd:163`: `fallback` is computed once outside the loop; the 10 iterations re-check the identical point and the unconditional `return fallback` ignores the result. Move the draw inside the loop or delete it.
2. **Pinch zoom specified but unhandled** `[edge, blind]` — `input_router.gd:31`: only mouse-wheel buttons map to zoom; `InputEventMagnifyGesture` (trackpad pinch) does nothing, though epic E1.2 and the spec matrix both say "scroll/pinch". Handle it or document the deferral to E7.
3. **Spec artifact declares `status: 'done'` with its A3 Godot-MCP verification task unchecked** `[blind, acceptance, codebase]` — `spec-e1-tiny-planet.md`: the tracker contradicts itself about briefing item A3 ("verified, not claimed"). My own re-verification came out clean, so this is paperwork — but the shipped artifact should not declare done over an unchecked verification task.
4. **Headless suite hangs forever (no FAIL) on a staged-world regression** `[edge]` — `test_no_sim.gd:57`: `sites[0..3]` indexing continues after the soft `check(sites.size() == 33)`; the out-of-bounds error aborts `run_all` → `failures += null` aborts the runner → `quit()` never runs → CI hang. Early-return on the size check.
5. **InputRouter integration path untested** `[tests]` — `input_router.gd:77`: only pure `classify()` is pinned; the `_pick` mask (0b11), mode transitions, and focus-loss cancel have no tests.
6. **E1.5 node orientation/collision untested** `[tests]` — `node_site.gd:38`: suite asserts count and wedge spread only; nothing checks basis-vs-surface-normal or collision layer 2, the property the input grammar stands on.

### Notes (22)

State hygiene: `draw_end` never resets `_last_preview_end` (draw_cancel does) — rare transient invisible preview · `draw_end` commits the last motion event's snap target; the release point is never re-snapped · dead `orbit_started` signal (emitted, never connected) `[blind, codebase]` · `_arc_mid` double-scales a radius-length vector (masked by callers normalizing) · capture-02 comment promises nearest-neighbor framing, code uses the 0.65-rad pair · capture-01 frames with the normalized-sum trick on the *most antipodal* pair — the same file's docstring flags it as degenerate (latent, seed-dependent).
Tests: "no Sim autoload" check is vacuous — `has_setting("autoload") == false`, runtime-verified (the other two no-sim checks are substantive, contract still holds) `[blind, edge, codebase]` · "same geodesic path" test checks only endpoints · seed literal `20260904` duplicated across test_no_sim · `test_input.gd` leaks a Camera3D (matches the suite's leaked-RID warnings byte-for-byte).
Gameplay/hygiene: merged-bundle radius+elevation grow uncapped (only strands are capped) `[blind, edge]` · cloud puff salt omits the cloud index (all 4 clouds share one puff layout) · `geodesic_axis` comment claims "least aligned", code avoids only the dominant axis `[blind, codebase]` · spec task references nonexistent `tools/capture.gd` `[blind, codebase]` · capture_runner ignores save/dir error codes (green run on failed capture).
GDD drift: slice stages **33 nodes vs GDD "MVP node count 4–6"** (gdd.md:327) — the epic pins no count and the PR body cites user direction; recorded so the deviation is traceable, not silent.
Architecture (all note-grade, fine for slice 1): `snap_candidate` returns Node3D from the "pure" math module · sibling-path `get_node("../…")` coupling · CaptureRunner inside the shipped scene · `ray_sphere` production-unused · basis idiom + `elevated_path` duplication · name-keyed bundle registry.

### Reviewer agreement

- **Separation formula dead / hitboxes overlap** — reported independently by **5 of 7 lenses** (blind, edge, acceptance, architecture, codebase); runtime-verified by me. Highest-confidence finding of the round.
- Fallback loop ornamental `[blind, edge]` · pinch missing `[edge, blind]` · spec-done/A3-unchecked `[blind, acceptance, codebase]` · vacuous autoload check `[blind, edge, codebase]` · uncapped merge growth `[blind, edge]` · dead `orbit_started` `[blind, codebase]` · perp-axis comment `[blind, codebase]` · `tools/capture.gd` stale ref `[blind, codebase]`.

**Verdict:** NEEDS CHANGES

The core is strong — the math spine, camera construction, disambiguation rule, and no-sim contract all verified clean, and the captures genuinely look the part. But blocker 1 is a shipped-world defect that falsifies a load-bearing PR claim and erodes the disambiguation contract, and blocker 2 leaves the primary verb's actual gesture path (where two real bugs already hide) untested. Both are small, well-scoped fixes.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
