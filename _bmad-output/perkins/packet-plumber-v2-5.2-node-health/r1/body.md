## 🤖 Perkins automated review — round 1 of 3
**Job:** packet-plumber-v2-5.2-node-health · **Reviewed sha:** 088fdcd · **Reviewers:** 7/7 completed
**Verification:** 21/22 findings confirmed against the code — 1 discarded as false-positive

### Blockers (0)
None.

### Warnings (5)
1. **Hover inspect card is never clamped to the viewport or tray band** — traceability numbers render off-screen for map-edge nodes `app/render/node_health.odin:50-56`. Verified geometry: at the 1280×720 design grid (`view_compute`: scale 0.923, off_y 0) a bottom-row node anchors the 52px card at y 708..760 — **both text lines land below 720, fully invisible**; right-column nodes clip ~65px. Growth-born drowning nodes live exactly at this periphery — the one place hard req 2 ("a 🔴 node is ALWAYS traceable") breaks. The repo's anchored-panel convention (`popover_rect`, `app/render/popover.odin:39-63`) flips/clamps/stays clear of `TRAY_CLEAR`; the card should do the same.
2. **Stuck-pile measurement implemented twice** — `core/warnings.odin:189-201` (inline `nload` loop) vs `core/node_health.odin:66-77` (`node_health_measure`); identical filter + identical math in two independently-maintained sites. `view.odin:344`'s "equal by construction" rests on one static fixture for 120 ticks. Extract one shared per-slot stuck-load helper — one implementation, two consumers; the never-serialized `node_health` separation is unchanged.
3. **The "@t400 host resolution" claim is false** — `_pr_body.md:98` + story card say the golden pins "host resolution @t400"; the demo's own comment says the host is still red at t400 (recovery begins in the T1 tail), and **I inspected `goldens/node_health/20000ms.png`: the host shows a RED ring in the capture**. No test or golden pins the downward (resolution) transition at all. Correct the copy, or add a capture past the pile drain + a core test that asserts the host clears to 🟢 after the pipe draw.
4. **Dead/demolished slot → `.None` branch untested** — `core/node_health.odin:106-109`; 4.1's twin branch has `test_warning_dead_node_silent` (`warnings_test.odin:452`), 5.2 has no demolish case. Mirror it: demolish a red node, assert the slot reads `None`.
5. **Advisory test gate: CONCERNS** — P0 100% (up-transitions + 70/90 boundary pins, determinism, the derive-don't-record negative control all green: 183 tests, 29/29 demos, 204 drift mutations); P1 ≈86% (the two gaps above). Closing W3/W4 lifts it to PASS.

### Notes (7)
- **Replay pin overstated** — the body says "live == replay levels at every tick"; the test compares the final-tick levels snapshot + per-tick hashes (per-tick level equality is hash-implied, not directly compared). `_pr_body.md:67-68` vs `node_health_test.odin:125-142`.
- **`node_health_evaluate` is O(nodes × packets)** — measure rescans all packets per slot; matches the existing 4.1 complexity class but doubles the per-tick scan. Falls out of the W2 shared helper.
- **Mouse sampling + world picking inside `draw_hud`** rather than `handle_input` — deviation from the input → App-state → draw convention (all other mouse reads live in `handle_input`); harmless today, unreachable to 5.4's input-parity layer. `app/main.odin:1215-1226`.
- **Tri-state glyph/color vocabulary duplicated** between `draw_health_ring` (`view.odin:360-371`) and `node_health_card_state` — share one mapping proc.
- **Card occludes the demolish popover's button** while hovering the selected node (popover drawn at `main.odin:350`, card later inside `draw_hud` at :387; no `sel_node` guard in the hover block). Visual only — hit-testing is geometric.
- **Card geometry comment says "2-line" but draws three rows**, and the trace line's 12px text ends 2px past the 52px frame.
- **Hover card render has no automated pin** — sanctioned by the app-layer-only convention (harness never calls `draw_hud`; core numbers are pinned); informational.

### Reviewer agreement
- W1 (card clamp) — **5 independent lenses** (blind, edge, acceptance, architecture, codebase): the highest-confidence signal in this round.
- W2 (measure duplication) — 4 lenses (blind, acceptance, architecture, codebase).
- W3 (@t400 mislabel) — 2 lenses (blind, tests), confirmed against the golden PNG.
- Replay-pin overstatement — 2 lenses (blind, tests).

**Verdict:** READY TO MERGE

The load-bearing contracts hold: derive-don't-record is structurally sound (serializer untouched, negative control pins it), the stuck-pile measure + shared 70/90 thresholds are game-correct and coherent by construction, T1/replay identity is unbroken, catalog_hash untouched, the font fold is presentation-only, and all 29 goldens share one catalog hash. The 5 warnings are real but none break the sim, the goldens, or the core contracts — address them in a follow-up push and I'll re-review the new sha.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
