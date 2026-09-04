## 🤖 Perkins automated review — round 1
**Job:** packet-plumber-3d-e2-flow-qos · **Reviewed sha:** dfd1f1e · **Reviewers:** 14/14 lens runs completed (7 lenses × 2 chunks — the 3636-line diff was chunked per the big-diff policy: implementation core / tests+artifacts)
**Verification:** 52/53 findings confirmed against the code — 1 discarded as false-positive

**Independent verification:** headless suite `godot --headless -s res://tests/run_tests.gd` → **PASS, 0 failures, 142/142 checks** (needs `--import` first on a fresh clone — class-cache, not a code defect). Replay determinism pins assert exact per-tick hash equality + byte-identical dumps with mutation legs; view-purity shakes orbit/zoom/QoS-panel noise against a lockstep reference sim — hash never shifts; nothing-auto-allocates holds (fresh pipes Standard 100%, set_lanes only via the command bus, panel Apply-only); ECMP is a stateless hash over (src,dst,class,pkt_id) — replay-stable; canon `_ready()` is untouched by the editor preview. All 8 captures verified **mechanically** (real PNGs, right resolutions, mandated subjects, non-blank) — aesthetic parity deferred (k3 re-check): this round's reviewer is text-only.

### Blockers (1)
- **Pipe-select input grammar (SELECT mode, pick_pipe, pipe_selected signal) has zero test coverage** [tests] — `scripts/input_router.gd:92-101`
  E2.3's AC 'QoS panel on pipe select' is reachable only through the SELECT branch (pick_pipe -> pipe_selected -> panel). Zero automated coverage: gesture, signal emission, click-slop and drag-to-orbit paths unpinned. Flagged by the tests lens in BOTH chunk waves.

### Warnings (11)
- **Pooled packet dots keep the first occupant's class material on slot reuse — dot colors misreport packet class** [edge+acceptance] — `scripts/flow_view.gd:142-153`
  Reuse branch sets visible/position but never rebinds material_override; a slot that once held streaming (blue) renders later email (yellow) packets blue. README sells color=class — A2's visible-evidence contract undermined.
- **QosPanel ladder/fallback/apply logic exercised only as view noise, never asserted** [tests] — `scripts/qos_panel.gd:143-171`
  Panel's only real logic — rung fallback when a class's lane goes inactive (incl. the Standard-inactive edge) and the apply-guard — feeds set_lanes commands with zero assertions; test_view_purity drives it as noise only.
- **Command-bus invalid-command no-ops under-tested — add_pipe validation entirely unpinned** [tests] — `scripts/sim/sim_core.gd:112-159`
  apply_command promises deterministic no-ops; only 2 set_lanes branches tested (sum>100, inactive lane). add_pipe range/self-loop guards and set_lanes size/unknown-pipe branches have no negative tests.
- **FlowView.pick_pipe geometric picking and occlusion guard untested** [tests] — `scripts/flow_view.gd:56-88`
  Sole entry to the QoS panel; occlusion guard + clampf(0.25,1.5) threshold are load-bearing geometry with no regression pin.
- **no_route drop path and unreachable-demand SLA isolation never pinned** [tests] — `scripts/sim/sim_core.gd:211-272`
  Documented invariant — isolated houses must not poison loss SLAs — plus the no_route drop reason have zero tests; a _reachable regression silently flips gentle networks into breaches.
- **Advisory test gate: CONCERNS (P0 100%, P1 ~85%, overall ~65% automation-only)** [tests] — `tests/run_tests.gd:20-31`
  P0 = 100% (5/5 epic test contracts). P1 ~85% (select path 0). Overall ~65% automation-only, ~80% counting A2 captures as visual evidence.
- **Latency SLA breach events are not attributable to any pipe/node (pipe:-1, node:-1)** [acceptance] — `scripts/sim/sim_core.gd:412-415`
  Test contract says breach is detectable AND attributable; loss events carry pipe/node, latency events carry -1/-1 — only tick+class. Delivery-time attribution should record the delivering packet's last pipe/node.
- **Parallel-bundle merge no longer pops — E1 'grow bigger' feedback silently dropped in the FlowView rewrite** [blind] — `scripts/flow_view.gd:_rebuild_view`
  _create_view pops; the merge path (_rebuild_view on parallel change) rebuilds without the pop. E1 feedback lost with no test noticing (visual surfaces untested).
- **Runtime composition root references editor-only EditorInterface under @tool — exported builds cannot parse main.gd** [blind] — `scripts/main.gd:_editor_preview_shot`
  @tool main.gd always loads in exports; EditorInterface is absent from export ClassDB -> script parse fails -> composition root dead in any exported build. A shipped landmine even for a slice prototype.
- **Runtime script error inside an awaited test coroutine silently yields PASS with exit 0 (false-green gate)** [edge] — `tests/run_tests.gd:42`
  Independently reproduced on Godot 4.7.1 during this review: an aborted coroutine makes `await inst.run_all()` evaluate to 0 and `failures += 0` absorbs it — a mid-test regression error bypasses the A1 gate while the suite prints PASS/exit 0. Current suite verified non-aborted (142/142 source checks printed ok).
- **Autoload guard is vacuous: has_setting("autoload") is always false in Godot — the no-Sim-autoload pin can never fail** [blind] — `tests/test_world.gd:91-95`
  Autoloads register as autoload/<Name> leaves, never a bare "autoload" key, so the guard always takes the check(true) branch; registering a Sim autoload would still pass. Same vacuity class as the E1 round.

### Notes (29)
- SimBalance.BASE_TRAVEL_U_S is unreferenced and documents a 'lane multiplier' mechanism that does not exist [blind+codebase] — `scripts/sim/sim_balance.gd:69`
- classify() comments claim pipe-select is pinnable there, but classify() never returns SELECT [acceptance+codebase] — `scripts/input_router.gd:8`
- Spec front-matter says status done; every task checkbox is unchecked [blind+codebase] — `_bmad-output/implementation-artifacts/spec-e2-flow-qos.md:hunk`
- Stale cross-reference: test_gesture.gd header still cites test_no_sim, which this diff renames to test_world [acceptance+codebase] — `tests/test_gesture.gd:6`
- 17-command replay topology duplicated byte-for-byte between tools/determinism_log.gd and tests/test_sim_replay.gd, kept in sync by comment only [architecture] — `tools/determinism_log.gd:11-13`
- [demoted from warning] Editor-preview pin claims 'byte-identical' but compares approximately [blind] — `tests/test_editor_preview.gd:hunk`
- HUD breach chip (set_breaches/_breach_lines) untested [tests] — `scripts/hud.gd:56-64`
- Capture 06 cannot show 'class-dependent speed' — shot taken before any lane allocation [acceptance] — `scripts/capture_runner.gd:98-109`
- determinism_log.gd uses FileAccess.open result unchecked — null crash on missing captures/ dir [blind] — `tools/determinism_log.gd:_go`
- Seeded world layout computed twice in _ready — staged nodes and sim placements can silently drift apart [blind] — `scripts/main.gd:_ready`
- sim_core header claims work-conserving lane cascade, but unspendable allowance is banked, not lent downward [blind] — `scripts/sim/sim_core.gd:_admit_all`
- Zoom/magnify during a held pipe press keeps SELECT alive; release opens the pre-zoom pick [edge] — `scripts/input_router.gd:44-53,92-101`
- Editor shot dereferences get_camera_3d() without a null check [edge] — `scripts/main.gd:109-111`
- @tool script auto-executes disk write and force-quits the editor process off a lingering --editor-preview-shot user arg [security] — `scripts/main.gd:34-37,124-125`
- InputRouter now calls directly into FlowView; the SELECT branch of the positional grammar lives outside the pinned static classify() [architecture] — `scripts/input_router.gd:92-93`
- Capture harness reaches into main's private signal handlers and untyped sim instead of the public path [architecture] — `scripts/capture_runner.gd:104-109`
- FlowView.pulse_egress maps sim node index to Nodes-container child position — a cross-module invariant held only by staging order [architecture] — `scripts/flow_view.gd:167-170`
- PipeArc.build_legacy compat shim has one caller and is behaviorally identical to build(a, b, 1.0) [architecture] — `scripts/pipe_arc.gd:49-50`
- Editor-only capture routine (viewport camera mutation, force_draw, PNG save, quit) embedded in the runtime composition root [architecture] — `scripts/main.gd:98`
- QosPanel._sim member is assigned in open() and never read [architecture] — `scripts/qos_panel.gd:14,116`
- View-purity and editor-preview pins lack the mutation leg the spec requires [blind] — `tests/test_view_purity.gd:hunk`
- Drop-attributability check claims class/tick validation but never checks them [blind] — `tests/test_sim_sla.gd:hunk (_loss_breach_attributable)`
- Replay comment claims 13 reachable houses; CMDS connect 12 [blind] — `tests/test_sim_replay.gd:hunk`
- Sync tests dereference after non-branching checks and index unguarded array tails — regressions abort checks as script errors [edge] — `tests/test_world.gd:80,105,125 | tests/test_sim_qos.gd:196`
- test_view_purity re-implements the seeded-sim construction instead of using test_sim_base.make_sim [codebase] — `tests/test_view_purity.gd:29`
- Loss-latch stickiness (no-chatter) unpinned while the latency twin is pinned [tests] — `tests/test_sim_sla.gd:39-72`
- Visual flow surfaces (packet dots, egress pulses) have no automated coverage [tests] — `scripts/flow_view.gd:121-171`
- PipeArc share-driven strand geometry API (strand_point/sample_at/hairline) untested [tests] — `scripts/pipe_arc.gd:59-94`
- Structural '@tool' pin is satisfied by a doc comment, so it cannot fail [architecture] — `tests/test_editor_preview.gd:22`

### Reviewer agreement
- **Pooled packet dots keep the first occupant's class material on slot reuse — dot colors misreport packet class** — [edge + acceptance]
- **SimBalance.BASE_TRAVEL_U_S is unreferenced and documents a 'lane multiplier' mechanism that does not exist** — [blind + codebase]
- **classify() comments claim pipe-select is pinnable there, but classify() never returns SELECT** — [acceptance + codebase]
- **Spec front-matter says status done; every task checkbox is unchecked** — [blind + codebase]
- **Stale cross-reference: test_gesture.gd header still cites test_no_sim, which this diff renames to test_world** — [acceptance + codebase]

**Full detail (evidence, fixes, verification status):** `_bmad-output/perkins/packet-plumber-3d-e2-flow-qos/r1/consolidated.json` in the orchestrator's output dir.

**Verdict:** NEEDS CHANGES

_The blocker: the pipe-select gesture — the only door to the QoS panel, an E2.3 acceptance criterion — has zero automated coverage (flagged in both chunk waves). The strongest warnings: pooled dot reuse misreports packet class (README claims color=class), and the async test harness can false-green on a mid-test runtime error (reproduced on Godot 4.7.1 during this review). Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
