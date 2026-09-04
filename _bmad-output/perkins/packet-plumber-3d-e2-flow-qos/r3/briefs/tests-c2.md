You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Your cwd is the reviewed worktree — verify against files there; never modify anything.

--- PROJECT CONVENTIONS ---
none (no CLAUDE.md/AGENTS.md in the repo; README.md documents the game, controls, and the godot run command)

--- DIFF ---
diff --git a/README.md b/README.md
index ab0f9ed..ed97050 100644
--- a/README.md
+++ b/README.md
@@ -1,13 +1,16 @@
-# Packet Plumber 3D — Slice 1 (E1: Tiny Planet & Connect Verb)
+# Packet Plumber 3D — Slice 2 (E2: Flow Simulation, Packet Types & QoS)
 
 The internet is breaking. You are the only thing standing between civilization
 and **Error 404** — and now the whole internet lives on a **tiny planet** you
-hold in your hand: rotate the world, connect houses to routers, and (from E2)
-route packets to keep the network alive.
+hold in your hand: rotate the world, connect houses to routers, and route
+packets to keep the network alive.
 
-**This is slice 1** — the first playable vertical slice: a seeded tiny planet
-with three biome wedges, an orbit camera with a three-stop zoom ladder, and the
-connect verb with geodesic pipe arcs. **No simulation yet** (E2 brings packets).
+**This is slice 2** — the planet comes alive: the deterministic tick-driven
+flow simulation (E2.1), the two MVP packet classes (E2.2), link-level class
+queues with the assignment ladder (E2.3), visible node serialization (E2.4),
+and per-class SLA tracking (E2.5) — plus an editor-only **Regenerate
+Preview** button so the world shows in the editor without pressing play.
+World scale stays at slice 1 (33 nodes) by ruling; growth is E3's epic.
 
 ## Run it
 
@@ -17,38 +20,66 @@ godot --path <this repo>          # Godot 4.7.1 (/opt/homebrew/bin/godot)
 
 or open the project in the Godot 4.7.1 editor and press **F5**.
 
-## Controls (slice 1)
+## Controls (slice 2)
 
 | Input | Action |
 |---|---|
 | Drag on empty space | Orbit the planet (latitude clamped ±85° — the camera never rolls) |
 | Scroll | Zoom through the ladder: **globe → district → street** (damped stops) |
 | Drag from a node | Draw a pipe: the preview arc follows the surface; release **on a node** to connect, **anywhere else** to cancel |
-| — | Parallel pipes between the same pair merge into one fatter bundle |
+| — | Parallel pipes between the same pair merge into one fatter bundle with pooled capacity |
+| **Click a pipe** | Open the **QoS panel**: pick a ladder rung (100 · 70/30 · 50/30/20) and assign each class a lane; **Apply** commits it as a sim command. **Nothing auto-allocates** — every pipe starts with Standard at 100 % |
+
+Packets then stream along the arcs: blue dots are streaming, yellow are
+email; strand thickness = the lane's share, strand speed = lane priority
+(Express streaks, Best-effort crawls); buildings pulse as they serialize
+egress (Express → Standard → Best-effort, work-conserving). When a class's
+latency or loss SLA breaches (email 2000 ms / 30 %, streaming 1200 ms / 10 %
+— inherited canon), the HUD chip names it.
 
 ## Verify
 
 ```sh
-godot --headless -s res://tests/run_tests.gd    # epic test contracts (exit 0 = pass)
-godot --headless --import                       # import gate
+godot --headless -s res://tests/run_tests.gd          # all epic contracts (exit 0 = pass)
+godot --headless --import                             # import gate
+godot --headless -s res://tools/determinism_log.gd    # replay byte-identity log -> captures/05-*.txt
+godot --path . -- --capture                           # windowed: re-renders captures/01-04 + 06-07
 ```
 
 `captures/` holds committed in-game proof shots: globe with biome wedges,
-district altitude, a completed arc, and a merged parallel bundle.
+district altitude, a completed arc, a merged parallel bundle (thick lane +
+hairline lanes), **packets flowing on the spine**, the **QoS panel with the
+3-lane ladder applied**, the **replay-determinism log**, and the
+**editor preview** (the world in the Godot editor, no play pressed).
+
+## The editor preview (folded QoL)
+
+`scenes/main.tscn` → select the **Main** node → Inspector → **Regenerate
+Preview**: runs the same seeded generation the runtime boot uses, into the
+editor viewport. Runtime behavior is unchanged (the `@tool` root guards
+`_ready` on the editor hint). One-shot CLI for the committed capture:
+
+```sh
+godot --editor --path . res://scenes/main.tscn -- --editor-preview-shot
+```
 
 ## Design docs
 
 - **Game Design Document:**
   [`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-3d-2026-09-04/gdd.md`](_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-3d-2026-09-04/gdd.md)
   (+ `epics.md`, `decision-log.md` alongside it)
-- **Spec of record for this slice:** `epics.md` section **E1** — stories E1.1–E1.5
-  and the test contracts are the acceptance criteria.
+- **Spec of record for this slice:** `epics.md` section **E2** — stories
+  E2.1–E2.5 and the test contracts are the acceptance criteria.
 
 ## Engine & tooling
 
 - **Engine:** Godot 4.7.1 — text `.tscn`/`.tres` keep the world diff-able
 - **Build/verify surface:** the Godot MCP (scene tools, editor-run,
   debug-output, lsp-diagnostics)
+- **Sim doctrine:** owned seed-derived RNG streams, fixed 60 Hz tick,
+  integer milli-unit state, command bus (`add_pipe`, `set_lanes`), canonical
+  state dump + fnv1a hash — replay is byte-identical and view interactions
+  can never shift sim state
 - **Look:** little-planet look-parity — flat-shaded primitives + palette
   tokens only; no purchased or cloned assets (placeholder-art doctrine)
 
diff --git a/_bmad-output/implementation-artifacts/deferred-work.md b/_bmad-output/implementation-artifacts/deferred-work.md
new file mode 100644
index 0000000..c46c8bf
--- /dev/null
+++ b/_bmad-output/implementation-artifacts/deferred-work.md
@@ -0,0 +1,9 @@
+
+## From packet-plumber-3d-e2-flow-qos step-04 review (2026-09-04)
+
+- [defer] Demand-stream salt bands drift into each other over very long runs
+  (destination salt 7_000_000 + counter*31337 grows unboundedly; after ~1M
+  spawns/house it can cross other draw bands → statistical (NOT determinism)
+  coupling between seeded streams). Guard when E3 re-tunes demand: bound the
+  per-stream counter space (e.g. counter % 8192) and re-pin demand-driven
+  test thresholds. (edge-hunter finding 5)
diff --git a/_bmad-output/implementation-artifacts/spec-e2-flow-qos.md b/_bmad-output/implementation-artifacts/spec-e2-flow-qos.md
new file mode 100644
index 0000000..a2d3529
--- /dev/null
+++ b/_bmad-output/implementation-artifacts/spec-e2-flow-qos.md
@@ -0,0 +1,187 @@
+---
+title: 'E2 — Flow Simulation, Packet Types & QoS (+ editor preview QoL)'
+type: 'feature'
+created: '2026-09-05'
+status: 'done'
+baseline_commit: 'c4edcef'
+context:
+  - '{project-root}/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-3d-2026-09-04/epics.md'
+  - '{project-root}/_bmad-output/implementation-artifacts/spec-e1-tiny-planet.md'
+---
+
+<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">
+
+## Intent
+
+**Problem:** The slice-1 world is inert — no packets flow, no routing trade-offs, no QoS craft (epic E2 undelivered); the editor also cannot show the generated world without pressing play.
+
+**Approach:** Add a deterministic, tick-driven sim core (owned RNG, command bus, replay hash) beneath the untouched view layer: junction forwarding (fattest route, ECMP split by hash), bundled parallel pipes, two MVP packet classes, per-link class lanes with the assignment ladder, visible node serialization, and per-class SLA tracking — plus an `@tool` inspector "Regenerate Preview" on the composition root. World stays at slice-1 scale (33 nodes).
+
+## Boundaries & Constraints
+
+**Always:**
+- Epic test contracts hold: replay byte-identity on a fixed seed; contention drops by drop precedence (lowest first); a dedicated lane reservation holds its class's capacity; SLA breach detectable + attributable; view-layer changes never shift sim state.
+- Sim state mutates ONLY via the command bus (`add_pipe`, `set_lanes`) + its own fixed tick; camera/orbit/zoom/panel interactions issue no commands.
+- Owned sim RNG (seed-derived), integer milli-unit paths, no wall-clock anywhere in the sim; fixed tick stepped from the physics loop.
+- Inherited canon values (PP-Odin packet_types.json): email 2000 ms / 30 % loss, streaming 1200 ms / 10 %, default lane Standard; 3D capacity ladder per this GDD (10/25/50/120 u/s; only standard drawable in E2).
+- Nothing auto-allocates: fresh pipes carry Standard at 100 %; lanes change only by player command through the QoS panel.
+- E1 contracts keep passing (snap-intent, geodesic validity, no-roll, disambiguation) — E1 tests update only where the no-sim structural assertion is superseded.
+
+**Ask First:**
+- Any new packet class, tier, auto-allocation, density/scale change, or deviating from the ladder (100 · 70/30 · 50/30/20).
+
+**Never:**
+- No scale/density changes (big world is E3); no demand director/forecast/surge (E4); no win/lose, health meter, node health states (E6/E3); no eras (E5); no new packet types (E10).
+- No wall-clock, global RNG, or view-layer writes into sim state; no auto QoS.
+
+## I/O & Edge-Case Matrix
+
+| Scenario | Input / State | Expected Output / Behavior | Error Handling |
+|----------|--------------|---------------------------|----------------|
+| Replay identity | Same seed + same command stream, two fresh sims | Identical per-tick hashes + identical final state serialization | Divergence = test failure |
+| View noise | Orbit/zoom/select-panel calls between ticks | Sim hash byte-identical to an isolated run | N/A |
+| Saturation | Lane demand > reserved share | Drops fire lowest drop-precedence class first; drop records carry tick/pipe/node/class | N/A |
+| Reservation | 3-lane pipe saturated on one lane | Each fed lane still delivers ≈ its reserved share over a window | N/A |
+| Gap-filling | Express lane empty | Standard/Best-effort use the freed budget (work-conserving), serialization order Express→Standard→Best-effort | N/A |
+| Equal-cost split | Two equal-cost next hops | splitmix64(src,dst,class,pkt_id) mod N picks deterministically per packet | N/A |
+| Editor preview | "Regenerate Preview" pressed twice in editor | Identical staging each time; runtime `_ready` flow unchanged | N/A |
+
+</frozen-after-approval>
+
+## Code Map
+
+- `scripts/sim/sim_balance.gd` -- NEW: all tunables as const data (tiers, classes, lanes, ladder, speeds, queue depths, SLA thresholds, colors)
+- `scripts/sim/sim_core.gd` -- NEW: RefCounted deterministic sim: state, owned RNG, Dijkstra+ECMP routing, per-tick step (spawn → serialize/admit → traverse → arrive → SLA), command bus, fnv1a-32 state hash + canonical dump
+- `scripts/flow_view.gd` -- NEW: binds sim state to view nodes (pipe registry, packet dots); reads snapshots only
+- `scripts/pipe_arc.gd` -- EDIT: strands become the 3 class lanes (thickness = share, packet dots ride their strand, speed by lane)
+- `scripts/qos_panel.gd` -- NEW: pipe-select panel (ladder buttons + per-class lane assignment) emitting commands
+- `scripts/input_router.gd` -- EDIT: press-on-pipe = select (click) → QoS panel; node→draw, else→orbit unchanged
+- `scripts/node_site.gd` -- EDIT: egress pulse (visible serialization)
+- `scripts/connect_controller.gd` -- EDIT: commits emit `add_pipe` (pipe id from sim)
+- `scripts/main.gd` -- EDIT: owns+steps SimCore (physics tick), wires commands; `@tool` + "Regenerate Preview" (editor-only path, runtime `_ready` untouched)
+- `scripts/world_seed.gd` -- UNCHANGED (world gen stays sim-free)
+- `tests/` -- EDIT/NEW: sim contract tests (replay, qos, sla, flow, view-purity, editor-preview) + runner list
+- `scripts/capture_runner.gd` + `captures/` -- EDIT: packets-flowing, QoS-panel, determinism log, editor-preview shots
+
+## Tasks & Acceptance
+
+**Execution:**
+- [x] `scripts/sim/sim_balance.gd` + `scripts/sim/sim_core.gd` -- deterministic core (state, RNG, routing, tick, commands, hash) -- E2.1/E2.2 foundation
+- [x] `tests/test_sim_replay.gd`, `tests/test_sim_flow.gd`, `tests/test_sim_qos.gd`, `tests/test_sim_sla.gd` -- every E2 test contract as a headless pin with a mutation leg -- A1
+- [x] `scripts/pipe_arc.gd` + `scripts/flow_view.gd` + `scripts/node_site.gd` -- lanes-as-strands, packet dots, egress pulse -- E2.4 visible
+- [x] `scripts/input_router.gd` + `scripts/qos_panel.gd` + `scripts/connect_controller.gd` + `scripts/main.gd` -- select grammar, QoS panel, command bus, sim stepping -- E2.3
+- [x] `tests/test_view_purity.gd` + `tests/test_editor_preview.gd` -- view-noise hash invariance; preview determinism -- A1 + QoL
+- [x] `tests/test_no_sim.gd` → `tests/test_world.gd` -- keep world contracts, drop the superseded no-sim assertion, add sim-wiring checks
+- [x] `scripts/capture_runner.gd` + `captures/` + `README.md` -- E2 captures (flow, QoS panel, determinism log, editor preview) + controls/run docs -- A2
+- [x] `tests/run_tests.gd` -- wire the new suite -- A1
+
+**Acceptance Criteria:**
+- Given the headless suite runs, when it completes, then every E2 test contract passes with exit 0, each new pin proven by a mutation leg (flipping the mechanism turns it red).
+- Given play mode, when pipes are drawn, then packets visibly stream along strands at lane-dependent speed and node egress serialization is readable in 3D.
+- Given a pipe is clicked, when the QoS panel changes the lane ladder, then only that pipe's allocation changes (command into sim), strands re-thicken, and the sim hash matches an isolated sim fed the same commands.
+- Given the editor (no play), when "Regenerate Preview" runs, then the seeded world appears in the viewport identically to runtime staging; runtime behavior is unchanged.
+- Given Godot MCP verification, when `editor-run` + `debug-output` + LSP diagnostics run over all scripts, then zero errors.
+
+## Spec Change Log
+
+- 2026-09-04 (step-04 review, patch class): hash wording fixed — the code's
+  state hash is FNV-1a 32-bit and ECMP uses the WorldSeed-owned 32-bit
+  splitmix-family mix, not "fnv1a64/splitmix64" as first written (the GDD's
+  splitmix64 row names the canon CONTRACT: deterministic per-packet pick).
+  Determinism unaffected. KEEP: the integer milli-unit state + canonical
+  dump approach (byte-identity is exact).
+
+## Design Notes
+
+- Sim/view seam: SimCore is scene-free and RefCounted; the view renders snapshots. Packet dots interpolate arc samples; sim numbers are integer milli-units (capacity u/s → milli-units/tick) so byte-identity is machine-local exact.
+- Breach latches are sticky-Enter (inherited PP-Odin lesson: ratios dilute, counters do not).
+- ECMP: per-junction next-hop sets from integer-cost Dijkstra (fat = cheap: narrow 4 / standard 3 / wide 2 / backbone 1); the repo's owned 32-bit splitmix-family hash picks per packet (the GDD's splitmix64 contract is the deterministic per-packet pick; WorldSeed.hash_i32 is this repo's owned implementation of it).
+- Editor preview: `@export_tool_button` (Godot 4.4+) on the `@tool` composition root; editor path clears + re-runs the same seeded generation; `Engine.is_editor_hint()` guard keeps the runtime `_ready()` byte-path identical.
+
+## Verification
+
+**Commands:**
+- `godot --headless --import` -- expected: clean import, no script errors
+- `godot --headless -s res://tests/run_tests.gd` -- expected: all contracts PASS, exit 0
+- Godot MCP `editor-run` + `debug-output` + LSP diagnostics -- expected: clean boot, zero errors
+- `captures/` -- expected: new E2 captures present + referenced from the PR body
+
+## Suggested Review Order
+
+**The deterministic core (start here)**
+
+- The balance table: every tunable in one data source, inherited canon flagged
+  [`sim_balance.gd:34`](../../scripts/sim/sim_balance.gd#L34)
+
+- The tick: fixed order spawn → admit → traverse (the determinism spine)
+  [`sim_core.gd:200`](../../scripts/sim/sim_core.gd#L200)
+
+- The command bus — the ONLY mutation door for game code
+  [`sim_core.gd:100`](../../scripts/sim/sim_core.gd#L100)
+
+- set_lanes + the re-enqueue guard (stranded-lane fix from review)
+  [`sim_core.gd:140`](../../scripts/sim/sim_core.gd#L140)
+
+- ECMP: flow-pinned hash over equal-cost next hops
+  [`sim_core.gd:294`](../../scripts/sim/sim_core.gd#L294)
+
+- The deficit-credit serializer: reserves hold, gaps cascade down
+  [`sim_core.gd:315`](../../scripts/sim/sim_core.gd#L315)
+
+- Canonical dump + fnv1a hash (the replay byte-identity contract)
+  [`sim_core.gd:546`](../../scripts/sim/sim_core.gd#L546)
+
+**Contracts as tests (each has a non-vacuity leg)**
+
+- Replay byte-identity + seed divergence + command-timing state
+  [`test_sim_replay.gd:22`](../../tests/test_sim_replay.gd#L22)
+
+- Reservation / gap-fill / drop precedence / allocation-drives-throughput
+  [`test_sim_qos.gd:88`](../../tests/test_sim_qos.gd#L88)
+
+- DIRECT admission-order observation (Express → Standard → Best-effort)
+  [`test_sim_qos.gd:168`](../../tests/test_sim_qos.gd#L168)
+
+- Deactivation never strands queued packets (review fix pin)
+  [`test_sim_qos.gd:202`](../../tests/test_sim_qos.gd#L202)
+
+- SLA breach: long-pipe trigger, sticky latch, attributable drops
+  [`test_sim_sla.gd:11`](../../tests/test_sim_sla.gd#L11)
+
+- View purity: orbit/zoom/panel noise never shifts the sim hash
+  [`test_view_purity.gd:16`](../../tests/test_view_purity.gd#L16)
+
+**View binding (reads snapshots, never writes)**
+
+- Pipe views: lanes-as-strands, packet dots on their lane's strand
+  [`pipe_arc.gd:37`](../../scripts/pipe_arc.gd#L37)
+
+- The sim→view sync: bundles, dots, ghost-dot guard
+  [`flow_view.gd:39`](../../scripts/flow_view.gd#L39)
+
+- Pipe pick with the occlusion guard (far-side can't win a click)
+  [`flow_view.gd:56`](../../scripts/flow_view.gd#L56)
+
+**Player surface**
+
+- The QoS panel: ladder rungs + per-class lanes, Apply = one command
+  [`qos_panel.gd:1`](../../scripts/qos_panel.gd#L1)
+
+- Pipe-select grammar (click slop → panel, drag → orbit)
+  [`input_router.gd:63`](../../scripts/input_router.gd#L63)
+
+- Composition root: sim stepping, command wiring, connect commit
+  [`main.gd:59`](../../scripts/main.gd#L59)
+
+**Editor preview (folded QoL)**
+
+- @tool guard + one-shot evidence capture (same generation body)
+  [`main.gd:98`](../../scripts/main.gd#L98)
+
+**Evidence + peripherals**
+
+- Determinism log generator (aligned CMDS with the replay test)
+  [`determinism_log.gd:12`](../../tools/determinism_log.gd#L12)
+
+- World contracts re-based on sim wiring (no-sim assertion superseded)
+  [`test_world.gd:16`](../../tests/test_world.gd#L16)
diff --git a/captures/01-globe-biomes.png b/captures/01-globe-biomes.png
index a820d81..802f9fb 100644
Binary files a/captures/01-globe-biomes.png and b/captures/01-globe-biomes.png differ
diff --git a/captures/01-globe-biomes.png.import b/captures/01-globe-biomes.png.import
new file mode 100644
index 0000000..0aa16c7
--- /dev/null
+++ b/captures/01-globe-biomes.png.import
@@ -0,0 +1,40 @@
+[remap]
+
+importer="texture"
+type="CompressedTexture2D"
+uid="uid://cxths4eixkbjt"
+path="res://.godot/imported/01-globe-biomes.png-be2e61c1409157130c27b1202f158118.ctex"
+metadata={
+"vram_texture": false
+}
+
+[deps]
+
+source_file="res://captures/01-globe-biomes.png"
+dest_files=["res://.godot/imported/01-globe-biomes.png-be2e61c1409157130c27b1202f158118.ctex"]
+
+[params]
+
+compress/mode=0
+compress/high_quality=false
+compress/lossy_quality=0.7
+compress/uastc_level=0
+compress/rdo_quality_loss=0.0
+compress/hdr_compression=1
+compress/normal_map=0
+compress/channel_pack=0
+mipmaps/generate=false
+mipmaps/limit=-1
+roughness/mode=0
+roughness/src_normal=""
+process/channel_remap/red=0
+process/channel_remap/green=1
+process/channel_remap/blue=2
+process/channel_remap/alpha=3
+process/fix_alpha_border=true
+process/premult_alpha=false
+process/normal_map_invert_y=false
+process/hdr_as_srgb=false
+process/hdr_clamp_exposure=false
+process/size_limit=0
+detect_3d/compress_to=1
diff --git a/captures/02-district.png b/captures/02-district.png
index 55cb3c2..441ecde 100644
Binary files a/captures/02-district.png and b/captures/02-district.png differ
diff --git a/captures/02-district.png.import b/captures/02-district.png.import
new file mode 100644
index 0000000..5af7228
--- /dev/null
+++ b/captures/02-district.png.import
@@ -0,0 +1,40 @@
+[remap]
+
+importer="texture"
+type="CompressedTexture2D"
+uid="uid://c02tbsn4vttuh"
+path="res://.godot/imported/02-district.png-0243bc4fcfff911f89926f2ab933872f.ctex"
+metadata={
+"vram_texture": false
+}
+
+[deps]
+
+source_file="res://captures/02-district.png"
+dest_files=["res://.godot/imported/02-district.png-0243bc4fcfff911f89926f2ab933872f.ctex"]
+
+[params]
+
+compress/mode=0
+compress/high_quality=false
+compress/lossy_quality=0.7
+compress/uastc_level=0
+compress/rdo_quality_loss=0.0
+compress/hdr_compression=1
+compress/normal_map=0
+compress/channel_pack=0
+mipmaps/generate=false
+mipmaps/limit=-1
+roughness/mode=0
+roughness/src_normal=""
+process/channel_remap/red=0
+process/channel_remap/green=1
+process/channel_remap/blue=2
+process/channel_remap/alpha=3
+process/fix_alpha_border=true
+process/premult_alpha=false
+process/normal_map_invert_y=false
+process/hdr_as_srgb=false
+process/hdr_clamp_exposure=false
+process/size_limit=0
+detect_3d/compress_to=1
diff --git a/captures/03-arc-connected.png b/captures/03-arc-connected.png
index 78d022e..26003ea 100644
Binary files a/captures/03-arc-connected.png and b/captures/03-arc-connected.png differ
diff --git a/captures/03-arc-connected.png.import b/captures/03-arc-connected.png.import
new file mode 100644
index 0000000..5c33fce
--- /dev/null
+++ b/captures/03-arc-connected.png.import
@@ -0,0 +1,40 @@
+[remap]
+
+importer="texture"
+type="CompressedTexture2D"
+uid="uid://ctbyktr6nxmwl"
+path="res://.godot/imported/03-arc-connected.png-7c1de8385d9442bcdd42bef91f3f1e91.ctex"
+metadata={
+"vram_texture": false
+}
+
+[deps]
+
+source_file="res://captures/03-arc-connected.png"
+dest_files=["res://.godot/imported/03-arc-connected.png-7c1de8385d9442bcdd42bef91f3f1e91.ctex"]
+
+[params]
+
+compress/mode=0
+compress/high_quality=false
+compress/lossy_quality=0.7
+compress/uastc_level=0
+compress/rdo_quality_loss=0.0
+compress/hdr_compression=1
+compress/normal_map=0
+compress/channel_pack=0
+mipmaps/generate=false
+mipmaps/limit=-1
+roughness/mode=0
+roughness/src_normal=""
+process/channel_remap/red=0
+process/channel_remap/green=1
+process/channel_remap/blue=2
+process/channel_remap/alpha=3
+process/fix_alpha_border=true
+process/premult_alpha=false
+process/normal_map_invert_y=false
+process/hdr_as_srgb=false
+process/hdr_clamp_exposure=false
+process/size_limit=0
+detect_3d/compress_to=1
diff --git a/captures/04-parallel-bundle.png b/captures/04-parallel-bundle.png
index 736ed70..04c04a9 100644
Binary files a/captures/04-parallel-bundle.png and b/captures/04-parallel-bundle.png differ
diff --git a/captures/04-parallel-bundle.png.import b/captures/04-parallel-bundle.png.import
new file mode 100644
index 0000000..4046769
--- /dev/null
+++ b/captures/04-parallel-bundle.png.import
@@ -0,0 +1,40 @@
+[remap]
+
+importer="texture"
+type="CompressedTexture2D"
+uid="uid://cnf2va26v1o2d"
+path="res://.godot/imported/04-parallel-bundle.png-c8bb2c473de0fc5c3e836fb629338e11.ctex"
+metadata={
+"vram_texture": false
+}
+
+[deps]
+
+source_file="res://captures/04-parallel-bundle.png"
+dest_files=["res://.godot/imported/04-parallel-bundle.png-c8bb2c473de0fc5c3e836fb629338e11.ctex"]
+
+[params]
+
+compress/mode=0
+compress/high_quality=false
+compress/lossy_quality=0.7
+compress/uastc_level=0
+compress/rdo_quality_loss=0.0
+compress/hdr_compression=1
+compress/normal_map=0
+compress/channel_pack=0
+mipmaps/generate=false
+mipmaps/limit=-1
+roughness/mode=0
+roughness/src_normal=""
+process/channel_remap/red=0
+process/channel_remap/green=1
+process/channel_remap/blue=2
+process/channel_remap/alpha=3
+process/fix_alpha_border=true
+process/premult_alpha=false
+process/normal_map_invert_y=false
+process/hdr_as_srgb=false
+process/hdr_clamp_exposure=false
+process/size_limit=0
+detect_3d/compress_to=1
diff --git a/captures/05-replay-determinism.txt b/captures/05-replay-determinism.txt
new file mode 100644
index 0000000..12d4e7d
--- /dev/null
+++ b/captures/05-replay-determinism.txt
@@ -0,0 +1,24 @@
+Packet Plumber 3D — E2 replay determinism (the A1 contract)
+seed=20260904 ticks=900 commands=17 (three-wedge network + a 50/30/20 set_lanes)
+run A / run B: two fresh SimCore instances, identical command streams,
+stepped in lockstep; hash = fnv1a over the canonical integer state dump.
+
+tick   0   hashA 3268ebfb   hashB 3268ebfb   MATCH
+tick  60   hashA 0e435331   hashB 0e435331   MATCH
+tick 120   hashA 20ffef81   hashB 20ffef81   MATCH
+tick 180   hashA 7cfe7e55   hashB 7cfe7e55   MATCH
+tick 240   hashA af28d251   hashB af28d251   MATCH
+tick 300   hashA ebfc5f7e   hashB ebfc5f7e   MATCH
+tick 360   hashA 1ea31096   hashB 1ea31096   MATCH
+tick 420   hashA e2e8d807   hashB e2e8d807   MATCH
+tick 480   hashA b9d90990   hashB b9d90990   MATCH
+tick 540   hashA bb69f762   hashB bb69f762   MATCH
+tick 600   hashA f0502a8f   hashB f0502a8f   MATCH
+tick 660   hashA 422fcd7a   hashB 422fcd7a   MATCH
+tick 720   hashA abdcec13   hashB abdcec13   MATCH
+tick 780   hashA 4c47e510   hashB 4c47e510   MATCH
+tick 840   hashA 8c27e48a   hashB 8c27e48a   MATCH
+
+final state dumps byte-identical: YES
+traffic carried: 10 packets delivered across the run
+VERDICT: PASS — replay byte-identity holds on the fixed seed
diff --git a/captures/06-packets-flowing.png b/captures/06-packets-flowing.png
new file mode 100644
index 0000000..d4b390e
Binary files /dev/null and b/captures/06-packets-flowing.png differ
diff --git a/captures/06-packets-flowing.png.import b/captures/06-packets-flowing.png.import
new file mode 100644
index 0000000..1eb7f1f
--- /dev/null
+++ b/captures/06-packets-flowing.png.import
@@ -0,0 +1,40 @@
+[remap]
+
+importer="texture"
+type="CompressedTexture2D"
+uid="uid://cvjhlx3mpaeya"
+path="res://.godot/imported/06-packets-flowing.png-d62b04d2bec51bdeac4cd8d46f7c9bab.ctex"
+metadata={
+"vram_texture": false
+}
+
+[deps]
+
+source_file="res://captures/06-packets-flowing.png"
+dest_files=["res://.godot/imported/06-packets-flowing.png-d62b04d2bec51bdeac4cd8d46f7c9bab.ctex"]
+
+[params]
+
+compress/mode=0
+compress/high_quality=false
+compress/lossy_quality=0.7
+compress/uastc_level=0
+compress/rdo_quality_loss=0.0
+compress/hdr_compression=1
+compress/normal_map=0
+compress/channel_pack=0
+mipmaps/generate=false
+mipmaps/limit=-1
+roughness/mode=0
+roughness/src_normal=""
+process/channel_remap/red=0
+process/channel_remap/green=1
+process/channel_remap/blue=2
+process/channel_remap/alpha=3
+process/fix_alpha_border=true
+process/premult_alpha=false
+process/normal_map_invert_y=false
+process/hdr_as_srgb=false
+process/hdr_clamp_exposure=false
+process/size_limit=0
+detect_3d/compress_to=1
diff --git a/captures/07-qos-panel.png b/captures/07-qos-panel.png
new file mode 100644
index 0000000..aca62e2
Binary files /dev/null and b/captures/07-qos-panel.png differ
diff --git a/captures/07-qos-panel.png.import b/captures/07-qos-panel.png.import
new file mode 100644
index 0000000..79f1714
--- /dev/null
+++ b/captures/07-qos-panel.png.import
@@ -0,0 +1,40 @@
+[remap]
+
+importer="texture"
+type="CompressedTexture2D"
+uid="uid://bc25n1uflqdic"
+path="res://.godot/imported/07-qos-panel.png-e0e4fc9befafb9de79f90241a96d370d.ctex"
+metadata={
+"vram_texture": false
+}
+
+[deps]
+
+source_file="res://captures/07-qos-panel.png"
+dest_files=["res://.godot/imported/07-qos-panel.png-e0e4fc9befafb9de79f90241a96d370d.ctex"]
+
+[params]
+
+compress/mode=0
+compress/high_quality=false
+compress/lossy_quality=0.7
+compress/uastc_level=0
+compress/rdo_quality_loss=0.0
+compress/hdr_compression=1
+compress/normal_map=0
+compress/channel_pack=0
+mipmaps/generate=false
+mipmaps/limit=-1
+roughness/mode=0
+roughness/src_normal=""
+process/channel_remap/red=0
+process/channel_remap/green=1
+process/channel_remap/blue=2
+process/channel_remap/alpha=3
+process/fix_alpha_border=true
+process/premult_alpha=false
+process/normal_map_invert_y=false
+process/hdr_as_srgb=false
+process/hdr_clamp_exposure=false
+process/size_limit=0
+detect_3d/compress_to=1
diff --git a/captures/08-editor-preview.png b/captures/08-editor-preview.png
new file mode 100644
index 0000000..8a9c0ce
Binary files /dev/null and b/captures/08-editor-preview.png differ
diff --git a/captures/08-editor-preview.png.import b/captures/08-editor-preview.png.import
new file mode 100644
index 0000000..6036a74
--- /dev/null
+++ b/captures/08-editor-preview.png.import
@@ -0,0 +1,40 @@
+[remap]
+
+importer="texture"
+type="CompressedTexture2D"
+uid="uid://dle7govdbssrf"
+path="res://.godot/imported/08-editor-preview.png-47a7fdd97be0c759d41b530198357dd7.ctex"
+metadata={
+"vram_texture": false
+}
+
+[deps]
+
+source_file="res://captures/08-editor-preview.png"
+dest_files=["res://.godot/imported/08-editor-preview.png-47a7fdd97be0c759d41b530198357dd7.ctex"]
+
+[params]
+
+compress/mode=0
+compress/high_quality=false
+compress/lossy_quality=0.7
+compress/uastc_level=0
+compress/rdo_quality_loss=0.0
+compress/hdr_compression=1
+compress/normal_map=0
+compress/channel_pack=0
+mipmaps/generate=false
+mipmaps/limit=-1
+roughness/mode=0
+roughness/src_normal=""
+process/channel_remap/red=0
+process/channel_remap/green=1
+process/channel_remap/blue=2
+process/channel_remap/alpha=3
+process/fix_alpha_border=true
+process/premult_alpha=false
+process/normal_map_invert_y=false
+process/hdr_as_srgb=false
+process/hdr_clamp_exposure=false
+process/size_limit=0
+detect_3d/compress_to=1
diff --git a/tests/run_tests.gd b/tests/run_tests.gd
index 6b0a854..d3f9589 100644
--- a/tests/run_tests.gd
+++ b/tests/run_tests.gd
@@ -22,8 +22,15 @@ func _run_once() -> void:
 		"res://tests/test_geodesic.gd",
 		"res://tests/test_camera.gd",
 		"res://tests/test_input.gd",
-		"res://tests/test_no_sim.gd",
+		"res://tests/test_world.gd",
 		"res://tests/test_gesture.gd",
+		"res://tests/test_sim_replay.gd",
+		"res://tests/test_sim_flow.gd",
+		"res://tests/test_sim_qos.gd",
+		"res://tests/test_sim_sla.gd",
+		"res://tests/test_view_purity.gd",
+		"res://tests/test_view_interaction.gd",
+		"res://tests/test_editor_preview.gd",
 	]
 	for path in scripts:
 		var packed: GDScript = load(path)
@@ -33,7 +40,26 @@ func _run_once() -> void:
 			continue
 		var inst: RefCounted = packed.new()
 		inst.tree = self
-		failures += await inst.run_all()
+		var result: Variant = await inst.run_all()
+		# Semantic gate (r2 B2): an aborted coroutine can still yield an int,
+		# so the return value alone cannot be trusted. Two independent trips:
+		# (1) the completion flag run_all sets as its LAST statement, and
+		# (2) the pinned per-file check count (a mid-script abort eats checks).
+		if not bool(inst.completed):
+			printerr("  FAIL %s — run_all ABORTED before its completion flag" % path)
+			failures += 1
+		var ran_checks: int = int(inst.checks)
+		var pinned: Variant = inst.get("EXPECTED_CHECKS")
+		var expected: int = int(pinned) if pinned != null else -1
+		if expected >= 0 and ran_checks != expected:
+			printerr("  FAIL %s — check-count gate: ran %d, expected %d (checks are being eaten)" % [path, ran_checks, expected])
+			failures += 1
+		if result is int:
+			failures += result
+		else:
+			printerr("  FAIL %s — run_all yielded no int result; counting as failure" % path)
+			failures += 1
+		print("  -- %s: %d checks (expected %d)" % [path, ran_checks, expected])
 		inst = null # RefCounted — never .free()
 	print("SUITE RESULT: %s (%d failure(s))" % ["PASS" if failures == 0 else "FAIL", failures])
 	quit(1 if failures > 0 else 0)
diff --git a/tests/test_base.gd b/tests/test_base.gd
index b76f197..123dd82 100644
--- a/tests/test_base.gd
+++ b/tests/test_base.gd
@@ -6,6 +6,11 @@ extends RefCounted
 var tree: SceneTree
 var failures := 0
 var checks := 0
+var completed := false # set by run_all's LAST statement — the abort detector
+
+## Each test file pins its own `const EXPECTED_CHECKS := N` — the runner
+## fails any shortfall. Friction on purpose: a mid-script abort silently
+## eating checks is exactly how the r2 phantom-check bug stayed green.
 
 
 func check(cond: bool, label: String) -> void:
diff --git a/tests/test_camera.gd b/tests/test_camera.gd
index 2bf1220..04cf1b9 100644
--- a/tests/test_camera.gd
+++ b/tests/test_camera.gd
@@ -3,6 +3,7 @@ extends "res://tests/test_base.gd"
 ## E1.2 camera contracts: the up-vector never rolls at any azimuth within the
 ## latitude clamp, the clamp holds, and ladder zoom stops are exact.
 
+const EXPECTED_CHECKS := 10 # pinned — the runner fails check-count shortfalls (r2 B2)
 const R := 5.0
 
 var _rig: OrbitCamera
@@ -21,6 +22,7 @@ func run_all() -> int:
 	_frame_point_centers_target()
 	tree.root.remove_child(_rig)
 	_rig.free()
+	completed = true
 	return failures
 
 
diff --git a/tests/test_editor_preview.gd b/tests/test_editor_preview.gd
new file mode 100644
index 0000000..4845c43
--- /dev/null
+++ b/tests/test_editor_preview.gd
@@ -0,0 +1,76 @@
+extends "res://tests/test_base.gd"
+
+## Folded QoL: the @tool editor preview. Structural pins: main.gd is @tool,
+## carries the "Regenerate Preview" inspector button, and guards _ready
+## under the editor hint (runtime boot path untouched). Behavioral pin: the
+## shared generation body is deterministic + idempotent — regenerating
+## produces byte-identical staging, and it matches the runtime boot's world.
+
+const EXPECTED_CHECKS := 5 # pinned — the runner fails check-count shortfalls (r2 B2)
+const SEED := 20260904
+const MAIN_SCRIPT := "res://scripts/main.gd"
+
+
+func run_all() -> int:
+	print("[test_editor_preview]")
+	_structural()
+	var result: int = await _behavioral()
+	completed = true
+	return result
+
+
+func _structural() -> void:
+	var script: GDScript = load(MAIN_SCRIPT)
+	var src := script.source_code
+	check(src.begins_with("@tool"), "main.gd is @tool (annotation on line 1 — a doc mention can't satisfy this)")
+	check(src.contains("@export_tool_button(\"Regenerate Preview\""), "inspector button 'Regenerate Preview' exists")
+	check(src.contains("Engine.is_editor_hint()"), "editor-hint guard present (runtime _ready path unchanged)")
+
+
+func _behavioral() -> int:
+	var packed: PackedScene = load("res://scenes/main.tscn")
+	if packed == null:
+		check(false, "main.tscn loads")
+		return failures
+	var scene: Node = packed.instantiate()
+	tree.root.add_child(scene)
+	await tree.process_frame # let the runtime boot stage the world
+	var boot_positions := _staging(scene)
+
+	# The editor path: clear + regenerate (the button's exact body, via the
+	# shared helpers) — must reproduce the boot world IDENTICALLY.
+	scene._clear_generated()
+	scene._generate_world(WorldSeed.wedge_layout(SEED))
+	var regen_positions := _staging(scene)
+	check(_same(boot_positions, regen_positions), "regenerate reproduces the boot world byte-identically")
+
+	# Idempotence: a SECOND regenerate changes nothing.
+	scene._clear_generated()
+	scene._generate_world(WorldSeed.wedge_layout(SEED))
+	check(_same(regen_positions, _staging(scene)), "a second regenerate is idempotent")
+
+	tree.root.remove_child(scene)
+	scene.free()
+	return failures
+
+
+func _staging(scene: Node) -> Dictionary:
+	var planet: Planet = scene.get_node("Planet")
+	var sites: Array = scene.get_node("Nodes").get_children().filter(func(c): return c is NodeSite)
+	var pos := PackedVector3Array()
+	for s in sites:
+		pos.append((s as NodeSite).surface_pos)
+	return {"planet_children": planet.get_child_count(), "site_count": sites.size(), "positions": pos}
+
+
+func _same(a: Dictionary, b: Dictionary) -> bool:
+	if a.planet_children != b.planet_children or a.site_count != b.site_count:
+		return false
+	var pa: PackedVector3Array = a.positions
+	var pb: PackedVector3Array = b.positions
+	if pa.size() != pb.size():
+		return false
+	for i in pa.size():
+		if not pa[i].is_equal_approx(pb[i]):
+			return false
+	return true
diff --git a/tests/test_editor_preview.gd.uid b/tests/test_editor_preview.gd.uid
new file mode 100644
index 0000000..57456b3
--- /dev/null
+++ b/tests/test_editor_preview.gd.uid
@@ -0,0 +1 @@
+uid://o0403wgj2k01
diff --git a/tests/test_geodesic.gd b/tests/test_geodesic.gd
index 679aa48..c8f5df7 100644
--- a/tests/test_geodesic.gd
+++ b/tests/test_geodesic.gd
@@ -4,6 +4,7 @@ extends "res://tests/test_base.gd"
 ## containment (no tunneling), elevation profile, antipodal determinism,
 ## ray/sphere projection.
 
+const EXPECTED_CHECKS := 28 # pinned — the runner fails check-count shortfalls (r2 B2)
 const R := 5.0
 
 
@@ -15,6 +16,7 @@ func run_all() -> int:
 	_antipodal_deterministic()
 	_ray_sphere()
 	_snap_selection()
+	completed = true
 	return failures
 
 
diff --git a/tests/test_gesture.gd b/tests/test_gesture.gd
index cada219..47ac8ea 100644
--- a/tests/test_gesture.gd
+++ b/tests/test_gesture.gd
@@ -3,15 +3,18 @@ extends "res://tests/test_base.gd"
 ## E1.3 gesture lifecycle — drives the REAL input path headless: parsed
 ## InputEvents → InputRouter._unhandled_input → physics _pick →
 ## ConnectController state machine → commit/cancel. Never the programmatic
-## connect_programmatic shortcut (that path is covered in test_no_sim).
+## connect_programmatic shortcut (that path is covered in test_world).
 
+const EXPECTED_CHECKS := 12 # pinned — the runner fails check-count shortfalls (r2 B2)
 const SCENE := "res://scenes/main.tscn"
 const FRAMES_FOR_PHYSICS := 4
 
 
 func run_all() -> int:
 	print("[test_gesture]")
-	return await _run_gestures()
+	var result: int = await _run_gestures()
+	completed = true
+	return result
 
 
 func _run_gestures() -> int:
@@ -56,13 +59,13 @@ func _run_gestures() -> int:
 	rig.frame_point(c_site.global_position, 1)
 	rig.snap()
 	await tree.process_frame
-	var size_before: int = controller._registry.size()
+	var size_before: int = scene.sim.pipes.size()
 	await _press(_unproject(c_site.global_position))
 	check(controller._source == c_site, "second gesture also enters DRAW")
 	var empty := _empty_surface_point(sites, c_site)
 	await _move(_unproject(c_site.global_position), _unproject(empty))
 	await _release(_unproject(empty))
-	check(controller._registry.size() == size_before, "release on empty surface CANCELS (no pipe)")
+	check(scene.sim.pipes.size() == size_before, "release on empty surface CANCELS (no pipe)")
 	check(controller._source == null, "cancel clears gesture state")
 
 	# --- sky release cancels (pointer leaves the planet mid-drag) ---
@@ -72,7 +75,7 @@ func _run_gestures() -> int:
 	await _press(_unproject(c_site.global_position))
 	var sky := _sky_screen_point()
 	await _release(sky)
-	check(controller._registry.size() == size_before, "release over open SKY cancels (no stale-snap commit)")
+	check(scene.sim.pipes.size() == size_before, "release over open SKY cancels (no stale-snap commit)")
 
 	# --- focus loss cancels a live gesture ---
 	await _press(_unproject(c_site.global_position))
@@ -81,7 +84,7 @@ func _run_gestures() -> int:
 	check(router._mode == InputRouter.Mode.NONE, "focus-loss resets the router mode")
 	check(controller._source == null and not controller._preview.visible, "focus-loss cancels preview + state")
 	await _release(sky)
-	check(controller._registry.size() == size_before, "post-cancel release commits nothing")
+	check(scene.sim.pipes.size() == size_before, "post-cancel release commits nothing")
 
 	tree.root.remove_child(scene)
 	scene.free()
diff --git a/tests/test_gesture.gd.uid b/tests/test_gesture.gd.uid
new file mode 100644
index 0000000..8f4688e
--- /dev/null
+++ b/tests/test_gesture.gd.uid
@@ -0,0 +1 @@
+uid://jqk1tdawwie1
diff --git a/tests/test_input.gd b/tests/test_input.gd
index 4d81f13..30c4e36 100644
--- a/tests/test_input.gd
+++ b/tests/test_input.gd
@@ -3,9 +3,11 @@ extends "res://tests/test_base.gd"
 ## E1.3 input contracts: the positional disambiguation rule and the
 ## snap-honors-intent commit path.
 
+const EXPECTED_CHECKS := 4 # pinned — the runner fails check-count shortfalls (r2 B2)
 func run_all() -> int:
 	print("[test_input]")
 	_classify()
+	completed = true
 	return failures
 
 
diff --git a/tests/test_no_sim.gd.uid b/tests/test_no_sim.gd.uid
deleted file mode 100644
index 2ae46dc..0000000
--- a/tests/test_no_sim.gd.uid
+++ /dev/null
@@ -1 +0,0 @@
-uid://blgkgikxo7bsg
diff --git a/tests/test_sim_base.gd b/tests/test_sim_base.gd
new file mode 100644
index 0000000..db2034f
--- /dev/null
+++ b/tests/test_sim_base.gd
@@ -0,0 +1,64 @@
+extends "res://tests/test_base.gd"
+
+## Shared SimCore harness: seeded placements + step/flood helpers.
+## Node index map (WorldSeed.node_placements): each wedge w owns indices
+## w*11 .. w*11+10 as [router, h, h, h, h, h, h, h, h, router, h].
+
+const SEED := 20260904
+const REPLAY_TICKS := 900
+const REPLAY_INJECT_TICK := 300 # the tick both consumers apply REPLAY_CMDS at
+## The replay-evidence command stream — ONE definition shared by
+## tests/test_sim_replay.gd and tools/determinism_log.gd so the committed
+## capture and its sibling test can never drift apart.
+## Three-wedge network (16 pipes, 12 reachable houses) + a 50/30/20 set_lanes.
+const REPLAY_CMDS := [
+	{"cmd": "add_pipe", "a": 1, "b": 0},
+	{"cmd": "add_pipe", "a": 2, "b": 0},
+	{"cmd": "add_pipe", "a": 3, "b": 0},
+	{"cmd": "add_pipe", "a": 4, "b": 0},
+	{"cmd": "add_pipe", "a": 0, "b": 9},
+	{"cmd": "add_pipe", "a": 10, "b": 9},
+	{"cmd": "add_pipe", "a": 12, "b": 9},
+	{"cmd": "add_pipe", "a": 13, "b": 9},
+	{"cmd": "add_pipe", "a": 9, "b": 11},
+	{"cmd": "add_pipe", "a": 13, "b": 11},
+	{"cmd": "add_pipe", "a": 15, "b": 11},
+	{"cmd": "add_pipe", "a": 17, "b": 11},
+	{"cmd": "add_pipe", "a": 11, "b": 22},
+	{"cmd": "add_pipe", "a": 23, "b": 22},
+	{"cmd": "add_pipe", "a": 25, "b": 22},
+	{"cmd": "add_pipe", "a": 27, "b": 22},
+	{"cmd": "set_lanes", "pipe": 5, "alloc": [50, 30, 20], "cls_lane": {"email": 2, "streaming": 0}},
+]
+
+
+func make_sim(seed_value := SEED) -> SimCore:
+	var sim := SimCore.new()
+	sim.setup(seed_value, WorldSeed.node_placements(seed_value, WorldSeed.wedge_layout(seed_value)))
+	return sim
+
+
+func drive(sim: SimCore, ticks: int) -> void:
+	for i in ticks:
+		sim.step_tick()
+
+
+## Longest / shortest house-to-house arcs (for latency breach staging).
+func house_pair_extremes(sim: SimCore) -> Dictionary:
+	var houses: Array[int] = []
+	for i in sim.node_is_house.size():
+		if sim.node_is_house[i]:
+			houses.append(i)
+	var longest := [houses[0], houses[1]]
+	var shortest := [houses[0], houses[1]]
+	for i in houses.size():
+		for j in range(i + 1, houses.size()):
+			var arc := Geodesic.arc_angle(sim.node_pos[houses[i]], sim.node_pos[houses[j]])
+			if arc > Geodesic.arc_angle(sim.node_pos[longest[0]], sim.node_pos[longest[1]]):
+				longest = [houses[i], houses[j]]
+			if arc < Geodesic.arc_angle(sim.node_pos[shortest[0]], sim.node_pos[shortest[1]]):
+				shortest = [houses[i], houses[j]]
+	return {
+		"longest": longest, "longest_milli": int(round(Geodesic.arc_length(sim.node_pos[longest[0]], sim.node_pos[longest[1]], WorldSeed.PLANET_RADIUS) * SimBalance.MILLI)),
+		"shortest": shortest, "shortest_milli": int(round(Geodesic.arc_length(sim.node_pos[shortest[0]], sim.node_pos[shortest[1]], WorldSeed.PLANET_RADIUS) * SimBalance.MILLI)),
+	}
diff --git a/tests/test_sim_base.gd.uid b/tests/test_sim_base.gd.uid
new file mode 100644
index 0000000..a0aaf9c
--- /dev/null
+++ b/tests/test_sim_base.gd.uid
@@ -0,0 +1 @@
+uid://duuj7nq1riblb
diff --git a/tests/test_sim_flow.gd b/tests/test_sim_flow.gd
new file mode 100644
index 0000000..7134a14
--- /dev/null
+++ b/tests/test_sim_flow.gd
@@ -0,0 +1,183 @@
+extends "res://tests/test_sim_base.gd"
+
+## E2.1 flow contracts: ECMP equal-cost split, min-cost route choice,
+## parallel-bundle pooled capacity. In-flight observations filter by
+## origin-destination pair so natural demand cannot pollute the pins.
+
+const EXPECTED_CHECKS := 14 # pinned — the runner fails check-count shortfalls (r2 B2)
+func run_all() -> int:
+	print("[test_sim_flow]")
+	_ecmp_split()
+	_min_cost_route()
+	_pooled_bundle_capacity()
+	_duplex_capacity()
+	_command_validation_noops()
+	_lane_speed_differential()
+	completed = true
+	return failures
+
+
+## The command bus promises deterministic no-ops for invalid commands —
+## pin every validation branch so a removed guard is visible.
+func _command_validation_noops() -> void:
+	var sim := make_sim()
+	# add_pipe rejections: self-loop, out-of-range indices.
+	sim.apply_command({"cmd": "add_pipe", "a": 5, "b": 5})
+	check(sim.pipes.is_empty(), "add_pipe self-loop rejected")
+	sim.apply_command({"cmd": "add_pipe", "a": -1, "b": 2})
+	sim.apply_command({"cmd": "add_pipe", "a": 1, "b": 99})
+	sim.apply_command({"cmd": "add_pipe", "a": 1})
+	check(sim.pipes.is_empty(), "add_pipe range/missing-field rejects leave no pipes")
+	# set_lanes rejections: unknown pipe, wrong array size.
+	sim.apply_command({"cmd": "add_pipe", "a": 1, "b": 2})
+	var before: Array = (sim.bundle_for_pair(1, 2).alloc as Array).duplicate()
+	sim.apply_command({"cmd": "set_lanes", "pipe": 99, "alloc": [50, 30, 20],
+		"cls_lane": {"email": 1, "streaming": 0}})
+	sim.apply_command({"cmd": "set_lanes", "pipe": 1, "alloc": [50, 30],
+		"cls_lane": {"email": 1, "streaming": 0}})
+	sim.apply_command({"cmd": "set_lanes", "pipe": 1, "alloc": [50, 30, 20],
+		"cls_lane": {"email": 1}})
+	sim.apply_command({"cmd": "set_lanes", "alloc": [50, 30, 20],
+		"cls_lane": {"email": 1, "streaming": 0}})
+	var p = sim.bundle_for_pair(1, 2)
+	check(p.alloc[0] == before[0] and p.alloc[1] == before[1] and p.alloc[2] == before[2],
+		"set_lanes unknown-pipe/size/missing-class/missing-field rejects are no-ops")
+	check(int(sim.command_log.size()) == int(sim.commands_total) and int(sim.commands_total) == 9,
+		"rejected commands are still RECORDED (deterministic audit trail): %d/%d" % [sim.command_log.size(), sim.commands_total])
+
+
+func _od_inflight(sim: SimCore, src: int, dst: int) -> Array:
+	var out: Array = []
+	for pid in sim.pipes.keys():
+		var p: Dictionary = sim.pipes[pid]
+		for id in p.inflight_a:
+			if sim.packets[id].src == src and sim.packets[id].dst == dst:
+				out.append(int(pid))
+		for id in p.inflight_b:
+			if sim.packets[id].src == src and sim.packets[id].dst == dst:
+				out.append(int(pid))
+	return out
+
+
+## Diamond with two equal-cost paths h1 -> r0 -> {r9 | r22} -> h3: the ECMP
+## hash must use BOTH deterministically (per-packet, flow-pinned).
+func _ecmp_split() -> void:
+	var run := func() -> Dictionary:
+		var sim := make_sim()
+		for c in [
+			{"cmd": "add_pipe", "a": 1, "b": 0},
+			{"cmd": "add_pipe", "a": 0, "b": 9},
+			{"cmd": "add_pipe", "a": 0, "b": 22},
+			{"cmd": "add_pipe", "a": 9, "b": 3},
+			{"cmd": "add_pipe", "a": 22, "b": 3},
+		]:
+			sim.apply_command(c)
+		var carried := {}
+		for i in 400:
+			sim._spawn_packet(1, 3, "email")
+			sim.step_tick()
+			for pid in _od_inflight(sim, 1, 3):
+				carried[pid] = true
+		return {"sim": sim, "carried": carried}
+	var r1: Dictionary = run.call()
+	var r2: Dictionary = run.call()
+	check(r1.carried.has(2) and r1.carried.has(3),
+		"ECMP: both equal-cost branches carry traffic (%s)" % str(r1.carried.keys()))
+	check(int(r1.sim.sla["email"].delivered) > 30, "ECMP diamond delivers (%d; the flood saturates by design)" % r1.sim.sla["email"].delivered)
+	check(int(r1.sim.sla["email"].delivered) == int(r2.sim.sla["email"].delivered)
+		and r1.carried.keys() == r2.carried.keys(),
+		"ECMP split is deterministic across reruns")
+
+
+## Path cost = static tier cost: with one drawable tier the cheapest path is
+## the fewest hops — the direct pipe must beat the 2-hop detour.
+func _min_cost_route() -> void:
+	var sim := make_sim()
+	for c in [
+		{"cmd": "add_pipe", "a": 1, "b": 0},
+		{"cmd": "add_pipe", "a": 1, "b": 2},
+		{"cmd": "add_pipe", "a": 2, "b": 0},
+	]:
+		sim.apply_command(c)
+	var via_detour := false
+	for i in 200:
+		sim._spawn_packet(1, 0, "email")
+		sim.step_tick()
+		for pid in _od_inflight(sim, 1, 0):
+			if pid != 1:
+				via_detour = true
+	check(not via_detour, "min-cost: packets take the direct pipe, never the 2-hop detour")
+	check(int(sim.sla["email"].delivered) > 25, "min-cost scenario delivers (%d; flood saturates by design)" % sim.sla["email"].delivered)
+
+
+## Parallel pipes pool capacity: 2x standard between a pair delivers ~2x
+## under the same offered load (mutation leg: 1x vs 2x on identical floods).
+func _pooled_bundle_capacity() -> void:
+	var single := _saturated_delivery(1)
+	var doubled := _saturated_delivery(2)
+	check(single >= 180 and single <= 320,
+		"pooled: single standard pipe delivers ~250 streaming/1200 ticks (got %d)" % single)
+	check(doubled >= single * 18 / 10, "pooled: 2 parallel pipes deliver >= 1.8x (got %d vs %d)" % [doubled, single])
+
+
+## E2.4 "class-dependent speed": same pipe, same direction, different lanes —
+## progress deltas over an identical tick window are EXACTLY the
+## LANE_SPEED_MILLI ratios (200 / 100 / 60 milli per tick).
+func _lane_speed_differential() -> void:
+	var sim := make_sim()
+	sim.apply_command({"cmd": "add_pipe", "a": 0, "b": 9})
+	for i in 7: # 8 parallel — both classes admit within the first ticks
+		sim.apply_command({"cmd": "add_pipe", "a": 0, "b": 9})
+	var pid := int(sim.bundle_for_pair(0, 9).id)
+	sim.apply_command({"cmd": "set_lanes", "pipe": pid, "alloc": [50, 30, 20],
+		"cls_lane": {"email": SimBalance.LANE_STANDARD, "streaming": SimBalance.LANE_EXPRESS}})
+	sim._spawn_packet(0, 9, "streaming")
+	var stream_id := sim.next_packet_id - 1
+	sim._spawn_packet(0, 9, "email")
+	var email_id := sim.next_packet_id - 1
+	drive(sim, 5) # both admitted well before this point
+	var s1 := int(sim.packets[stream_id].progress_milli)
+	var e1 := int(sim.packets[email_id].progress_milli)
+	drive(sim, 10)
+	var s2 := int(sim.packets[stream_id].progress_milli)
+	var e2 := int(sim.packets[email_id].progress_milli)
+	check(s2 - s1 == 2000 and e2 - e1 == 1000,
+		"lane speed: express %d vs standard %d milli per 10 ticks (exact LANE_SPEED_MILLI)" % [s2 - s1, e2 - e1])
+	# Best-effort wave: reassign email to BE, drain, re-stage.
+	sim.apply_command({"cmd": "set_lanes", "pipe": pid, "alloc": [50, 30, 20],
+		"cls_lane": {"email": SimBalance.LANE_BEST_EFFORT, "streaming": SimBalance.LANE_EXPRESS}})
+	drive(sim, 200) # drain everything in flight
+	sim._spawn_packet(0, 9, "email")
+	var be_id := sim.next_packet_id - 1
+	drive(sim, 5)
+	var b1 := int(sim.packets[be_id].progress_milli)
+	drive(sim, 10)
+	check(int(sim.packets[be_id].progress_milli) - b1 == 600,
+		"lane speed: best-effort crawls at 600 milli per 10 ticks (got %d)" % (int(sim.packets[be_id].progress_milli) - b1))
+
+
+func _saturated_delivery(parallel: int) -> int:
+	var sim := make_sim()
+	for i in parallel:
+		sim.apply_command({"cmd": "add_pipe", "a": 1, "b": 2})
+	for i in 1200:
+		sim._spawn_packet(1, 2, "streaming")
+		sim.step_tick()
+	return int(sim.sla["streaming"].delivered)
+
+
+## Link capacity is FULL-DUPLEX (documented in sim_core's doctrine header):
+## each endpoint admits against the full pooled budget, so a
+## bidirectionally saturated link carries ~2x a one-direction flood. This
+## pin PINS that semantic — a half-duplex change becomes a deliberate,
+## test-visible re-decision.
+func _duplex_capacity() -> void:
+	var sim := make_sim()
+	sim.apply_command({"cmd": "add_pipe", "a": 1, "b": 2})
+	for i in 1200:
+		sim._spawn_packet(1, 2, "streaming")
+		sim._spawn_packet(2, 1, "streaming")
+		sim.step_tick()
+	var both := int(sim.sla["streaming"].delivered)
+	var one := _saturated_delivery(1)
+	check(both >= one * 17 / 10, "duplex: bidirectionally saturated link carries >= 1.7x one direction (%d vs %d)" % [both, one])
diff --git a/tests/test_sim_flow.gd.uid b/tests/test_sim_flow.gd.uid
new file mode 100644
index 0000000..e1c3325
--- /dev/null
+++ b/tests/test_sim_flow.gd.uid
@@ -0,0 +1 @@
+uid://eymcgftvkt5
diff --git a/tests/test_sim_qos.gd b/tests/test_sim_qos.gd
new file mode 100644
index 0000000..c222cb0
--- /dev/null
+++ b/tests/test_sim_qos.gd
@@ -0,0 +1,231 @@
+extends "res://tests/test_sim_base.gd"
+
+## E2.3/E2.4 contracts: nothing auto-allocates (Standard 100% default, ladder
+## data-driven, per-pipe override via command only), a dedicated lane
+## reservation holds its class's capacity under saturation, work-conserving
+## gap-filling cascades spare capacity DOWN the ladder, contention drops by
+## drop precedence (lowest first), and egress serialization follows the
+## Express -> Standard -> Best-effort ladder.
+
+const EXPECTED_CHECKS := 25 # pinned — the runner fails check-count shortfalls (r2 B2)
+func run_all() -> int:
+	print("[test_sim_qos]")
+	_defaults_and_no_auto_alloc()
+	_set_lanes_command()
+	_reservation_holds()
+	_gap_filling()
+	_drop_precedence()
+	_allocation_drives_throughput()
+	_serialization_order_direct()
+	_lane_deactivation_never_strands()
+	completed = true
+	return failures
+
+
+func _fresh_pipe(sim: SimCore, alloc := [], cls_lane := {}) -> int:
+	sim.apply_command({"cmd": "add_pipe", "a": 1, "b": 2})
+	var p = sim.bundle_for_pair(1, 2)
+	if not alloc.is_empty():
+		sim.apply_command({"cmd": "set_lanes", "pipe": int(p.id), "alloc": alloc, "cls_lane": cls_lane})
+	return int(p.id)
+
+
+## Nothing auto-allocates: fresh pipes carry Standard at 100%, every class
+## rides Standard, and a fresh sim has zero pipes.
+func _defaults_and_no_auto_alloc() -> void:
+	var sim := make_sim()
+	check(sim.pipes.is_empty(), "fresh sim creates no pipes (nothing auto-allocates)")
+	var pid := _fresh_pipe(sim)
+	var p = sim.bundle_for_pair(1, 2)
+	check(p.alloc[SimBalance.LANE_STANDARD] == 100 and p.alloc[0] == 0 and p.alloc[2] == 0,
+		"fresh pipe: Standard lane at 100%%")
+	check(int(p.cls_lane.email) == SimBalance.LANE_STANDARD and int(p.cls_lane.streaming) == SimBalance.LANE_STANDARD,
+		"fresh pipe: both classes ride Standard")
+	check(sim.pipes[pid].parallel == 1, "fresh pipe is a single pipe (parallel 1)")
+
+
+## The QoS command is the ONLY lane mutation path; invalid ones are no-ops.
+func _set_lanes_command() -> void:
+	var sim := make_sim()
+	var pid := _fresh_pipe(sim)
+	sim.apply_command({"cmd": "set_lanes", "pipe": pid, "alloc": [50, 30, 20],
+		"cls_lane": {"email": 2, "streaming": 0}})
+	var p = sim.pipes[pid]
+	check(p.alloc[0] == 50 and p.alloc[1] == 30 and p.alloc[2] == 20, "set_lanes applies the 50/30/20 ladder rung")
+	check(int(p.cls_lane.email) == 2 and int(p.cls_lane.streaming) == 0, "set_lanes applies per-class lane assignment")
+	var before: Array = p.alloc.duplicate()
+	sim.apply_command({"cmd": "set_lanes", "pipe": pid, "alloc": [60, 60, 0],
+		"cls_lane": {"email": 1, "streaming": 0}})
+	check(p.alloc[0] == before[0] and p.alloc[1] == before[1], "invalid ladder (sum > 100) is rejected as a no-op")
+	sim.apply_command({"cmd": "set_lanes", "pipe": pid, "alloc": [0, 100, 0],
+		"cls_lane": {"email": 0, "streaming": 0}})
+	check(int(p.cls_lane.email) == 2, "class cannot be assigned to an inactive lane (rejected)")
+
+
+## Dedicated lane reservation: 3-lane pipe, Express fed with streaming and
+## Best-effort flooded with email — Express KEEPS its 50% share; Best-effort
+## also receives the idle Standard lane's cascaded 30% (spare flows down).
+func _reservation_holds() -> void:
+	var sim := make_sim()
+	_fresh_pipe(sim, [50, 30, 20], {"email": SimBalance.LANE_BEST_EFFORT, "streaming": SimBalance.LANE_EXPRESS})
+	for i in 1200:
+		sim._spawn_packet(1, 2, "streaming")
+		sim._spawn_packet(1, 2, "email")
+		sim.step_tick()
+	var stream := int(sim.sla["streaming"].delivered)
+	var mail := int(sim.sla["email"].delivered)
+	check(stream >= 95 and stream <= 160,
+		"reservation: Express holds ~50%% for streaming under BE flood (got %d, expect ~125)" % stream)
+	check(mail >= 200 and mail <= 320,
+		"reservation+cascade: Best-effort email gets 20%% + idle Standard 30%% (got %d, expect ~250)" % mail)
+	check(mail > stream, "reservation: express-milli(2x) still trails cascade-fed email count")
+
+
+## Work-conserving gap-filling: only Best-effort is fed — the idle Express +
+## Standard reserves cascade down and Best-effort approaches the FULL pipe.
+func _gap_filling() -> void:
+	var sim := make_sim()
+	_fresh_pipe(sim, [50, 30, 20], {"email": SimBalance.LANE_BEST_EFFORT, "streaming": SimBalance.LANE_EXPRESS})
+	for i in 1200:
+		sim._spawn_packet(1, 2, "email")
+		sim.step_tick()
+	var mail := int(sim.sla["email"].delivered)
+	check(mail >= 420, "gap-filling: idle reserves cascade down (email %d, reserve-only would be ~100, full ~500)" % mail)
+
+
+## Contention drops by drop precedence — lowest first. DIRECTED pin: fill a
+## pipe's queue, force one overflow, and the lowest-precedence packet is the
+## victim no matter who arrives. (The shared FIFO lane makes raw streaming
+## drop COUNTS dominate — emails always losing the victim contest IS the
+## precedence; the directed cases + ratios pin it honestly.)
+func _drop_precedence() -> void:
+	# Directed case 1: queue full of streaming, an email arrives -> the
+	# newcomer email is the victim, every streaming packet survives.
+	var sim := make_sim()
+	sim.apply_command({"cmd": "add_pipe", "a": 1, "b": 2})
+	for i in SimBalance.QUEUE_DEPTH:
+		sim._spawn_packet(1, 2, "streaming")
+	sim._spawn_packet(1, 2, "email")
+	check(int(sim.dropped_total) == 1, "precedence: exactly one packet dropped on the forced overflow")
+	check(str(sim.drops[0].cls) == "email", "precedence: the email is the victim of an all-streaming queue")
+	check(sim.packets.size() == SimBalance.QUEUE_DEPTH, "precedence: the streaming queue survives intact")
+	# Directed case 2: queue full of email, a streaming packet arrives -> an
+	# EMAIL is evicted to make room; the higher-precedence newcomer survives.
+	var sim2 := make_sim()
+	sim2.apply_command({"cmd": "add_pipe", "a": 1, "b": 2})
+	for i in SimBalance.QUEUE_DEPTH:
+		sim2._spawn_packet(1, 2, "email")
+	sim2._spawn_packet(1, 2, "streaming")
+	check(int(sim2.dropped_total) == 1 and str(sim2.drops[0].cls) == "email",
+		"precedence: a queued email is evicted, never the streaming newcomer")
+	var has_stream := false
+	for id in sim2.packets:
+		if sim2.packets[id].cls == "streaming":
+			has_stream = true
+	check(has_stream, "precedence: the streaming newcomer joined the queue")
+	# Statistical sanity on a real saturated run: email must lose proportionally more.
+	var sim3 := make_sim()
+	sim3.apply_command({"cmd": "add_pipe", "a": 1, "b": 2})
+	for i in 1200:
+		sim3._spawn_packet(1, 2, "streaming")
+		sim3._spawn_packet(1, 2, "email")
+		sim3.step_tick()
+	var mail_offered := int(sim3.sla["email"].dropped) + int(sim3.sla["email"].delivered)
+	var stream_offered := int(sim3.sla["streaming"].dropped) + int(sim3.sla["streaming"].delivered)
+	var mail_ratio := float(int(sim3.sla["email"].dropped)) / maxf(1.0, float(mail_offered))
+	var stream_ratio := float(int(sim3.sla["streaming"].dropped)) / maxf(1.0, float(stream_offered))
+	check(sim3.dropped_total > 50 and mail_ratio > stream_ratio,
+		"precedence: email loses proportionally more under real contention (%.2f vs %.2f)" % [mail_ratio, stream_ratio])
+
+
+## Egress serialization: with both lanes backlogged equally, the HIGHER lane
+## carries more milli-units — and the winner follows the ASSIGNMENT, not the
+## class (nothing auto-allocates by priority).
+func _allocation_drives_throughput() -> void:
+	var sim_a := make_sim()
+	_fresh_pipe(sim_a, [70, 30, 0], {"email": SimBalance.LANE_STANDARD, "streaming": SimBalance.LANE_EXPRESS})
+	for i in 1200:
+		sim_a._spawn_packet(1, 2, "streaming")
+		sim_a._spawn_packet(1, 2, "email")
+		sim_a.step_tick()
+	var stream_milli := int(sim_a.sla["streaming"].delivered) * 2000
+	var mail_milli := int(sim_a.sla["email"].delivered) * 1000
+	check(stream_milli > mail_milli,
+		"serialization: Express-assigned lane out-carries Standard under equal load (%d vs %d milli)" % [stream_milli, mail_milli])
+	var sim_b := make_sim()
+	_fresh_pipe(sim_b, [70, 30, 0], {"email": SimBalance.LANE_EXPRESS, "streaming": SimBalance.LANE_STANDARD})
+	for i in 1200:
+		sim_b._spawn_packet(1, 2, "streaming")
+		sim_b._spawn_packet(1, 2, "email")
+		sim_b.step_tick()
+	var stream_milli_b := int(sim_b.sla["streaming"].delivered) * 2000
+	var mail_milli_b := int(sim_b.sla["email"].delivered) * 1000
+	check(mail_milli_b > stream_milli_b,
+		"serialization: swapping the assignment swaps the winner (%d vs %d milli) — allocation, not class, drives throughput" % [mail_milli_b, stream_milli_b])
+
+
+## DIRECT observation of the egress ladder: with budget headroom and one
+## packet queued per lane, one tick admits Express, then Standard, then
+## Best-effort — visible in the bundle's in-flight order.
+func _serialization_order_direct() -> void:
+	var sim := make_sim()
+	# Router endpoints (0, 9) — routers never spawn natural demand, so the
+	# observed in-flight order is purely the staged packets.
+	sim.apply_command({"cmd": "add_pipe", "a": 0, "b": 9})
+	for i in 7: # 8 parallel — budget headroom for all three admissions in one tick
+		sim.apply_command({"cmd": "add_pipe", "a": 0, "b": 9})
+	var p = sim.bundle_for_pair(0, 9)
+	var pid := int(p.id)
+	sim.apply_command({"cmd": "set_lanes", "pipe": pid, "alloc": [50, 30, 20],
+		"cls_lane": {"email": SimBalance.LANE_STANDARD, "streaming": SimBalance.LANE_EXPRESS}})
+	# Wave 1: streaming (Express) + email (Standard) queued in spawn order.
+	sim._spawn_packet(0, 9, "streaming")
+	var stream_id := sim.next_packet_id - 1
+	sim._spawn_packet(0, 9, "email")
+	var email_id := sim.next_packet_id - 1
+	drive(sim, 3) # credit banking may need 2+ ticks before a 2000-milli packet admits
+	var inflight: Array = p.inflight_a
+	check(inflight.size() == 2 and int(inflight[0]) == stream_id and int(inflight[1]) == email_id,
+		"serialization: Express admitted before Standard (in-flight %s)" % str(inflight))
+	# Wave 2: reassign email to Best-effort; the next email must admit AFTER
+	# the existing traffic (the ladder never skips a higher lane).
+	sim.apply_command({"cmd": "set_lanes", "pipe": pid, "alloc": [50, 30, 20],
+		"cls_lane": {"email": SimBalance.LANE_BEST_EFFORT, "streaming": SimBalance.LANE_EXPRESS}})
+	sim._spawn_packet(0, 9, "email")
+	var be_id := sim.next_packet_id - 1
+	drive(sim, 3)
+	var inflight2: Array = p.inflight_a
+	if inflight2.is_empty():
+		check(false, "serialization: Best-effort wave admitted (in-flight empty — guard)")
+		return
+	check(int(inflight2[inflight2.size() - 1]) == be_id and inflight2.find(be_id) > inflight2.find(email_id),
+		"serialization: Best-effort admits after the higher lanes (tail = %d)" % int(inflight2[inflight2.size() - 1]))
+
+
+## The re-enqueue guard: reallocating so a class's lane goes INACTIVE must
+## never strand its queued packets (they re-route onto the active lane).
+func _lane_deactivation_never_strands() -> void:
+	var sim := make_sim()
+	var pid := _fresh_pipe(sim)
+	sim.apply_command({"cmd": "set_lanes", "pipe": pid, "alloc": [50, 30, 20],
+		"cls_lane": {"email": SimBalance.LANE_BEST_EFFORT, "streaming": SimBalance.LANE_EXPRESS}})
+	# Fill the Best-effort queue with emails (no stepping — nothing admitted).
+	for i in SimBalance.QUEUE_DEPTH:
+		sim._spawn_packet(1, 2, "email")
+	# Player collapses the ladder to Standard-only: BE goes inactive.
+	sim.apply_command({"cmd": "set_lanes", "pipe": pid, "alloc": [0, 100, 0],
+		"cls_lane": {"email": SimBalance.LANE_STANDARD, "streaming": SimBalance.LANE_STANDARD}})
+	var stranded := 0
+	for endpoint in 2:
+		for lane in 3:
+			stranded += (sim.queues[pid][endpoint][lane] as Array).size()
+	check(stranded == SimBalance.QUEUE_DEPTH, "deactivation: queued emails re-enqueued, none stranded (%d queued)" % stranded)
+	var all_standard := true
+	for id in sim.packets:
+		if int(sim.packets[id].lane) != SimBalance.LANE_STANDARD:
+			all_standard = false
+	check(all_standard, "deactivation: every queued packet now rides an ACTIVE (Standard) lane")
+	# And they still FLOW: after enough ticks everything delivers (no silent loss).
+	drive(sim, 1800)
+	var accounted := int(sim.sla["email"].delivered) + int(sim.sla["email"].dropped)
+	check(accounted >= SimBalance.QUEUE_DEPTH, "deactivation: every packet accounted (delivered+dropped = %d >= %d)" % [accounted, SimBalance.QUEUE_DEPTH])
diff --git a/tests/test_sim_qos.gd.uid b/tests/test_sim_qos.gd.uid
new file mode 100644
index 0000000..855f7e6
--- /dev/null
+++ b/tests/test_sim_qos.gd.uid
@@ -0,0 +1 @@
+uid://snomxw3tu4hl
diff --git a/tests/test_sim_replay.gd b/tests/test_sim_replay.gd
new file mode 100644
index 0000000..07be758
--- /dev/null
+++ b/tests/test_sim_replay.gd
@@ -0,0 +1,63 @@
+extends "res://tests/test_sim_base.gd"
+
+## E2.1 determinism contract: replay byte-identity on a fixed seed.
+## (Command stream + tick count: REPLAY_CMDS / REPLAY_TICKS in test_sim_base
+## — ONE definition shared with tools/determinism_log.gd.)
+
+const EXPECTED_CHECKS := 5 # pinned — the runner fails check-count shortfalls (r2 B2)
+func run_all() -> int:
+	print("[test_sim_replay]")
+	_replay_identity()
+	_seed_divergence()
+	_command_timing_matters()
+	completed = true
+	return failures
+
+
+## Two fresh sims, same seed, same commands at the same ticks: identical
+## hash at EVERY tick and byte-identical final dumps.
+func _replay_identity() -> void:
+	var a := make_sim()
+	var b := make_sim()
+	var diverged_at := -1
+	for t in REPLAY_TICKS:
+		if t == REPLAY_INJECT_TICK:
+			for c in REPLAY_CMDS:
+				a.apply_command(c)
+				b.apply_command(c)
+		a.step_tick()
+		b.step_tick()
+		if a.state_hash() != b.state_hash():
+			diverged_at = t
+			break
+	check(diverged_at < 0, "replay: identical state hash at every tick (diverged at %d)" % diverged_at)
+	check(a.dump_state() == b.dump_state(), "replay: final state dumps byte-identical")
+	var carried := int(a.sla["email"].delivered) + int(a.sla["streaming"].delivered)
+	check(carried >= 8, "replay scenario carries real traffic (%d delivered — pin is not vacuous)" % carried)
+
+
+## The hash is SENSITIVE: a different seed must diverge (mutation leg —
+## proves the identity pin above can actually fail).
+func _seed_divergence() -> void:
+	var a := make_sim(111)
+	var b := make_sim(222)
+	for c in REPLAY_CMDS:
+		a.apply_command(c)
+		b.apply_command(c)
+	drive(a, 300)
+	drive(b, 300)
+	check(a.state_hash() != b.state_hash(), "different seeds diverge (hash sensitivity)")
+
+
+## The command log is part of state: the same command at a DIFFERENT tick
+## produces a different world (command-bus determinism).
+func _command_timing_matters() -> void:
+	var a := make_sim()
+	var b := make_sim()
+	a.apply_command({"cmd": "add_pipe", "a": 1, "b": 0})
+	drive(a, 100)
+	drive(b, 100)
+	b.apply_command({"cmd": "add_pipe", "a": 1, "b": 0})
+	drive(a, 50)
+	drive(b, 50)
+	check(a.dump_state() != b.dump_state(), "same command at a different tick diverges (timing is state)")
diff --git a/tests/test_sim_replay.gd.uid b/tests/test_sim_replay.gd.uid
new file mode 100644
index 0000000..eaec030
--- /dev/null
+++ b/tests/test_sim_replay.gd.uid
@@ -0,0 +1 @@
+uid://dnhl7q8kgv44j
diff --git a/tests/test_sim_sla.gd b/tests/test_sim_sla.gd
new file mode 100644
index 0000000..587ce03
--- /dev/null
+++ b/tests/test_sim_sla.gd
@@ -0,0 +1,137 @@
+extends "res://tests/test_sim_base.gd"
+
+## E2.5 contracts: per-class SLA tracking — latency/loss accumulate per
+## class, breach is detectable (thresholds bite), attributable (records name
+## pipe/node/class/tick), and latches are sticky-Enter (inherited canon:
+## ratios dilute, latches must not chatter).
+
+const EXPECTED_CHECKS := 26 # pinned — the runner fails check-count shortfalls (r2 B2)
+const EMAIL_TOL_TICKS := 120 # 2000 ms canon at 60 Hz
+
+
+func run_all() -> int:
+	print("[test_sim_sla]")
+	_latency_breach_long_pipe()
+	_latency_threshold_bites_on_short_pipe()
+	_loss_breach_attributable()
+	_gentle_network_stays_clean()
+	_no_route_and_unreachable_isolation()
+	_streaming_latency_breach()
+	completed = true
+	return failures
+
+
+## A long pipe breaches the email latency SLA; the latch sticks.
+func _latency_breach_long_pipe() -> void:
+	var sim := make_sim()
+	var ext := house_pair_extremes(sim)
+	var a: int = ext.longest[0]
+	var b: int = ext.longest[1]
+	check(int(ext.longest_milli) >= EMAIL_TOL_TICKS * 100,
+		"staging: longest house arc %d milli gives > %d-tick transit (precondition)" % [ext.longest_milli, EMAIL_TOL_TICKS])
+	sim.apply_command({"cmd": "add_pipe", "a": a, "b": b})
+	for i in 5:
+		sim._spawn_packet(a, b, "email")
+		drive(sim, 360)
+	drive(sim, 200)
+	var s: Dictionary = sim.sla["email"]
+	check(int(s.delivered) >= 4, "long-pipe scenario delivers (%d)" % s.delivered)
+	check(bool(s.lat_breach), "SLA: latency breach detected on the long pipe")
+	check(int(s.lat_tick) >= 0 and not (s.events as Array).is_empty(), "SLA: breach carries tick + event record")
+	var mean_latency := float(int(s.latency_sum)) / maxf(1.0, float(int(s.delivered)))
+	check(mean_latency > float(EMAIL_TOL_TICKS), "SLA: mean latency %.0f exceeds the %d-tick tolerance" % [mean_latency, EMAIL_TOL_TICKS])
+	var latched_at := int(s.lat_tick)
+	drive(sim, 600)
+	check(int(sim.sla["email"].lat_tick) == latched_at and bool(sim.sla["email"].lat_breach),
+		"SLA: breach latch is sticky-Enter (no chatter)")
+
+
+## Mutation leg: the SAME gentle traffic on a SHORT pipe never breaches —
+## the threshold is what bites, not the scenario.
+func _latency_threshold_bites_on_short_pipe() -> void:
+	var sim := make_sim()
+	var ext := house_pair_extremes(sim)
+	var a: int = ext.shortest[0]
+	var b: int = ext.shortest[1]
+	check(int(ext.shortest_milli) < EMAIL_TOL_TICKS * 60,
+		"staging: shortest house arc %d milli keeps transit well under tolerance (precondition)" % ext.shortest_milli)
+	sim.apply_command({"cmd": "add_pipe", "a": a, "b": b})
+	for i in 5:
+		sim._spawn_packet(a, b, "email")
+		drive(sim, 360)
+	check(int(sim.sla["email"].delivered) >= 4, "short-pipe scenario delivers")
+	check(not bool(sim.sla["email"].lat_breach), "mutation leg: short pipe does NOT breach the latency SLA")
+
+
+## Sustained overload breaches the LOSS SLA for both classes; every drop is
+## attributable (pipe, node, class, tick, reason).
+func _loss_breach_attributable() -> void:
+	var sim := make_sim()
+	sim.apply_command({"cmd": "add_pipe", "a": 1, "b": 2})
+	for i in 1200:
+		sim._spawn_packet(1, 2, "streaming")
+		sim._spawn_packet(1, 2, "email")
+		sim.step_tick()
+	check(bool(sim.sla["email"].loss_breach), "SLA: email loss breach detected (>30%)")
+	check(bool(sim.sla["streaming"].loss_breach), "SLA: streaming loss breach detected (>10%)")
+	check(int(sim.sla["streaming"].loss_tick) >= 0 and int(sim.sla["email"].loss_tick) >= 0, "SLA: loss latches carry ticks")
+	check(sim.dropped_total > 50, "overload drops massively (%d — pin is not vacuous)" % sim.dropped_total)
+	var attributable := true
+	for d in sim.drops:
+		if int(d.pipe) < 0 or int(d.node) < 0 or int(d.tick) < 1 \
+				or not (d.cls in SimBalance.CLASS_IDS) or str(d.reason) != "queue_overflow":
+			attributable = false
+	check(attributable, "SLA: every drop record names pipe, node, class, tick and reason")
+	# N26 twin: the loss latch is sticky-Enter too (no chatter once latched).
+	var latched_at := int(sim.sla["email"].loss_tick)
+	drive(sim, 600)
+	check(int(sim.sla["email"].loss_tick) == latched_at and bool(sim.sla["email"].loss_breach),
+		"SLA: loss latch is sticky-Enter (no chatter)")
+
+
+## A gentle short-hop network stays clean on BOTH classes (the latches are
+## not always-on).
+func _gentle_network_stays_clean() -> void:
+	var sim := make_sim()
+	var ext := house_pair_extremes(sim)
+	sim.apply_command({"cmd": "add_pipe", "a": ext.shortest[0], "b": ext.shortest[1]})
+	for i in 6:
+		sim._spawn_packet(ext.shortest[0], ext.shortest[1], "email")
+		sim._spawn_packet(ext.shortest[0], ext.shortest[1], "streaming")
+		drive(sim, 240)
+	drive(sim, 400)
+	check(int(sim.sla["email"].delivered) >= 5 and int(sim.sla["streaming"].delivered) >= 5, "gentle scenario delivers both classes")
+	check(not bool(sim.sla["email"].lat_breach) and not bool(sim.sla["email"].loss_breach), "gentle: email clean on both SLAs")
+	check(not bool(sim.sla["streaming"].lat_breach) and not bool(sim.sla["streaming"].loss_breach), "gentle: streaming clean on both SLAs")
+
+
+## The TIGHTER bound: streaming (1200 ms = 72 ticks) latches its own
+## latency breach on the same long pipe that breaches email at 120.
+func _streaming_latency_breach() -> void:
+	var sim := make_sim()
+	var ext := house_pair_extremes(sim)
+	sim.apply_command({"cmd": "add_pipe", "a": ext.longest[0], "b": ext.longest[1]})
+	check(int(ext.longest_milli) >= 72 * 100, "staging: long arc exceeds streaming's 72-tick tolerance (precondition)")
+	for i in 4:
+		sim._spawn_packet(ext.longest[0], ext.longest[1], "streaming")
+		drive(sim, 240)
+	check(int(sim.sla["streaming"].delivered) >= 3, "streaming latency scenario delivers (%d)" % sim.sla["streaming"].delivered)
+	check(bool(sim.sla["streaming"].lat_breach), "SLA: streaming latches its own latency breach (1200 ms)")
+
+
+## Documented invariant: unreachable demand never spawns (must not poison
+## loss SLAs), and a packet with no route drops WITH a no_route record.
+func _no_route_and_unreachable_isolation() -> void:
+	var sim := make_sim() # zero pipes — nothing reachable
+	drive(sim, 900)
+	check(int(sim.dropped_total) == 0, "isolation: an empty network drops NOTHING (unreachable demand is skipped, not dropped)")
+	check(int(sim.sla["email"].loss_breach) == 0 and int(sim.sla["streaming"].loss_breach) == 0,
+		"isolation: unreachable demand never breaches a loss SLA")
+	# Manual spawn to an unreachable destination: recorded, attributable.
+	sim._spawn_packet(1, 20, "email") # 20 lives in another wedge, unconnected
+	check(str(sim.drops[0].reason) == "no_route" and int(sim.drops[0].pipe) == -1,
+		"no_route: unroutable packet drops with an attributable no_route record")
+	check(int(sim.sla["email"].dropped) == 1, "no_route drop counts against the class")
+	# Real lost traffic counts: the injected unroutable packet is 1 drop of
+	# 1 total (100% > 30%) — the latch firing here is the sim being honest.
+	check(bool(sim.sla["email"].loss_breach), "no_route: injected lost traffic latches the loss SLA (honest accounting)")
diff --git a/tests/test_sim_sla.gd.uid b/tests/test_sim_sla.gd.uid
new file mode 100644
index 0000000..e7d0993
--- /dev/null
+++ b/tests/test_sim_sla.gd.uid
@@ -0,0 +1 @@
+uid://c65uguybmg00d
diff --git a/tests/test_view_interaction.gd b/tests/test_view_interaction.gd
new file mode 100644
index 0000000..aff76d7
--- /dev/null
+++ b/tests/test_view_interaction.gd
@@ -0,0 +1,306 @@
+extends "res://tests/test_sim_base.gd"
+
+## B1 (Perkins r1): the pipe-select input grammar — the ONLY door to E2.3's
+## "QoS panel on pipe select" — pinned through the REAL input path:
+## parsed InputEvents → InputRouter → FlowView.pick_pipe → pipe_selected →
+## QosPanel. Also pins the geometry the grammar leans on: the pick occlusion
+## guard, click-slop vs drag disambiguation, pooled-dot material rebinding,
+## and the strand geometry the dots ride.
+
+const EXPECTED_CHECKS := 27 # pinned — the runner fails check-count shortfalls (r2 B2)
+const SCENE := "res://scenes/main.tscn"
+
+var _picked: Array = []
+
+
+func run_all() -> int:
+	print("[test_view_interaction]")
+	var result: int = await _run()
+	completed = true
+	return result
+
+
+func _run() -> int:
+	var packed: PackedScene = load(SCENE)
+	if packed == null:
+		check(false, "main.tscn loads")
+		return failures
+	var scene: Node = packed.instantiate()
+	tree.root.add_child(scene)
+	for i in 4:
+		await tree.physics_frame # colliders register
+
+	var main := scene
+	var router: InputRouter = main.get_node("InputRouter")
+	var rig: OrbitCamera = main.get_node("OrbitRig")
+	var panel: QosPanel = main.get_node("QosPanel")
+	var flow: FlowView = main.get_node("FlowView")
+	var cam: Camera3D = main.get_node("OrbitRig/Camera3D")
+	var sites: Array = main.get_node("Nodes").get_children().filter(func(c): return c is NodeSite)
+	router.pipe_selected.connect(func(id): _picked.append(id))
+
+	var pair := _pair_with_arc(sites, 0.65)
+	if pair.is_empty():
+		check(false, "readable site pair found")
+		tree.root.remove_child(scene)
+		scene.free()
+		return failures
+	var a: NodeSite = pair[0]
+	var b: NodeSite = pair[1]
+	var arc: PipeArc = main.request_connect(a, b)
+	var sim: SimCore = main.get("sim")
+	var pipe_id := int(sim.bundle_for_pair(a.node_index, b.node_index).id)
+
+	rig.frame_point(Geodesic.geodesic_points(a.global_position, b.global_position, 2)[1] * WorldSeed.PLANET_RADIUS, 1)
+	rig.snap()
+	await tree.process_frame
+	await tree.process_frame
+
+	# --- B1 leg 1: click (press + release within slop) selects the pipe ---
+	var mid: Vector3 = arc.sample_at(0.5)
+	var click := cam.unproject_position(mid)
+	await _press(click)
+	await _release(click)
+	check(_picked.size() == 1 and int(_picked[0]) == pipe_id,
+		"select: click on a pipe emits pipe_selected with its id (%s)" % str(_picked))
+	check(panel.visible, "select: the QoS panel opens on pipe select")
+
+	# --- B1 leg 2: dragging from a pipe past the slop becomes an ORBIT ---
+	panel.close_panel()
+	_picked.clear()
+	var az0: float = rig._target_azimuth
+	var side := click + Vector2(40, 12)
+	await _press(click)
+	await _move(click, side) # first motion crosses the slop: SELECT -> ORBIT
+	await _move(side, side + Vector2(24, -8)) # this one actually orbits
+	await _release(side + Vector2(24, -8))
+	check(_picked.is_empty(), "select: a dragged pipe press never emits pipe_selected")
+	check(not panel.visible, "select: a dragged pipe press opens no panel")
+	check(absf(az0 - rig._target_azimuth) > 0.001, "select: the drag orbited (camera target moved)")
+
+	# --- B1 leg 3: a sky click is never a select ---
+	_picked.clear()
+	var sky := _sky_screen_point(cam)
+	await _press(sky)
+	await _release(sky)
+	check(_picked.is_empty(), "select: sky press/release never selects")
+
+	# --- W4: pick occlusion — far-side pipes lose to the planet ---
+	_pick_occlusion(flow, cam)
+
+	# --- W2: the panel's own logic — rungs, fallback, apply payload ---
+	_panel_logic(panel, sim, pipe_id)
+
+	# --- W1: pooled dot slots REBIND their class material on reuse ---
+	await _dot_material_rebind(main, sim, flow)
+
+	# --- N28: the strand geometry the dots ride ---
+	_strand_geometry(arc)
+
+	# --- r2 W4: the HUD breach chip (both latches, show/hide) ---
+	_hud_chip(main)
+
+	# --- r2 W5: the node egress pulse + cooldown ---
+	_egress_pulse(main)
+
+	tree.root.remove_child(scene)
+	scene.free()
+	return failures
+
+
+## Synthetic geometry: camera on +Z at 20, planet R=8. The near pipe rides
+## the +Z surface; far pipes sit where each probe ray EXITS the sphere.
+func _pick_occlusion(flow: FlowView, cam: Camera3D) -> void:
+	var saved: Dictionary = flow._pipe_views
+	var arc_near := PipeArc.new()
+	arc_near.build(Vector3(2.6, 0, 7.55), Vector3(-2.6, 0, 7.55)) # mid ≈ (0,0,8.5)
+	var arc_far_axis := PipeArc.new()
+	arc_far_axis.build(Vector3(2.6, 0, -7.55), Vector3(-2.6, 0, -7.55)) # mid ≈ (0,0,-8.5)
+	var arc_far_bare := PipeArc.new()
+	arc_far_bare.build(Vector3(2.6, 7.55, 0), Vector3(-2.6, 7.55, 0)) # mid ≈ (0,8,0)
+	flow._pipe_views = {901: arc_near, 902: arc_far_axis, 903: arc_far_bare}
+	var keep_cam := cam.global_transform
+	cam.global_transform = Transform3D(Basis.IDENTITY, Vector3(0, 0, 20))
+	# a) a click aimed at the near pipe picks IT, never the on-axis far pipe
+	var got := flow.pick_pipe(cam.unproject_position(Vector3(0, 0, 8.5)), cam)
+	check(got == 901, "occlusion: the near-side pipe wins its own click (got %s)" % str(got))
+	# b) a bare-surface click whose ray EXITS near the far pipe returns -1 —
+	# the guard rejects samples beyond the planet's near hit. Mutation leg:
+	# without the max_t guard this ray scores the far pipe at distance ~0.
+	var got2 := flow.pick_pipe(cam.unproject_position(Vector3(0, 5.66, 5.66)), cam)
+	check(got2 == -1, "occlusion: a far-side pipe behind the planet is rejected (got %s)" % str(got2))
+	cam.global_transform = keep_cam
+	flow._pipe_views = saved
+
+
+## The panel's real logic: ladder rungs, the inactive-lane class fallback,
+## and a payload that always satisfies the command-bus validation.
+func _panel_logic(panel: QosPanel, sim: SimCore, pipe_id: int) -> void:
+	panel.open(pipe_id, sim)
+	check(panel.visible and panel._pipe_id == pipe_id, "panel: opens on a real pipe")
+	var payload: Array = []
+	panel.apply_requested.connect(func(pid, alloc, cls): payload.append([pid, alloc, cls]))
+	panel._on_rung(3)
+	check(panel._alloc[0] == 50 and panel._alloc[1] == 30 and panel._alloc[2] == 20, "panel: rung 3 = 50/30/20")
+	panel._on_class_cycle("email")
+	panel._on_class_cycle("streaming")
+	panel._on_apply()
+	check(payload.size() == 1, "panel: Apply emits exactly one payload")
+	var pl: Array = payload[0]
+	check(int(pl[0]) == pipe_id, "panel: payload names the selected pipe")
+	var alloc: Array = pl[1]
+	var cls: Dictionary = pl[2]
+	var payload_ok := alloc.size() == 3
+	var total := 0
+	for lane in 3:
+		var share := int(alloc[lane])
+		if share < 0 or share > 100:
+			payload_ok = false
+		total += share
+	if total > 100:
+		payload_ok = false
+	for cls_name in cls:
+		if int(alloc[int(cls[cls_name])]) <= 0:
+			payload_ok = false # every class rides an ACTIVE lane
+	check(payload_ok, "panel: the payload passes the sim's set_lanes validation")
+	# The fallback: 3-lane with email on Best-effort, collapse to rung 2 —
+	# email (BE now inactive) must fall back to the still-active Standard.
+	panel._on_rung(3)
+	panel._cls_lane["email"] = SimBalance.LANE_BEST_EFFORT
+	panel._on_rung(2)
+	check(int(panel._alloc[2]) == 0 and int(panel._cls_lane["email"]) == SimBalance.LANE_STANDARD,
+		"panel: collapsing to 2 lanes falls a Best-effort class back to Standard")
+	panel.close_panel()
+	check(not panel.visible, "panel: close hides it")
+
+
+## Slot reuse must rebind the class material: wave 1 puts streaming in slot
+## 0; after everything delivers, a lone email must render EMAIL-colored in
+## that same slot.
+func _dot_material_rebind(main: Node, sim: SimCore, flow: FlowView) -> void:
+	sim.apply_command({"cmd": "add_pipe", "a": 0, "b": 9})
+	for i in 7: # parallel headroom — both classes admit within a few ticks
+		sim.apply_command({"cmd": "add_pipe", "a": 0, "b": 9})
+	flow.sync() # view picks up the new bundle
+	var pipe_id := int(sim.bundle_for_pair(0, 9).id)
+	var email_mat: Material = flow._dot_mats["email"]
+	var stream_mat: Material = flow._dot_mats["streaming"]
+	# Wave 1: streaming then email — admitted in that order, slots 0 and 1.
+	sim._spawn_packet(0, 9, "streaming")
+	sim._spawn_packet(0, 9, "email")
+	drive(sim, 3)
+	flow.sync()
+	var pool: Array = flow._dots[pipe_id]
+	check(pool.size() >= 2 and pool[0].material_override == stream_mat and pool[1].material_override == email_mat,
+		"dots: wave 1 renders streaming then email (slot materials correct)")
+	# Drain, then a lone email reuses slot 0.
+	drive(sim, 220)
+	flow.sync()
+	sim._spawn_packet(0, 9, "email")
+	drive(sim, 3)
+	flow.sync()
+	check(pool[0].visible and pool[0].material_override == email_mat,
+		"dots: slot reuse REBINDS the class material (slot 0 now renders email)")
+
+
+func _strand_geometry(arc: PipeArc) -> void:
+	check(vapprox(arc.sample_at(0.0), arc._a, 1e-4) and vapprox(arc.sample_at(1.0), arc._b, 1e-4),
+		"strands: sample_at spans endpoint to endpoint")
+	check(arc.sample_at(0.25).distance_to(arc.sample_at(0.75)) > 0.1, "strands: sampling moves along the path")
+	var s0 := arc.strand_point(0, 0.5)
+	var s1 := arc.strand_point(1, 0.5)
+	var s2 := arc.strand_point(2, 0.5)
+	check(s0.distance_to(s1) > 0.05 and s1.distance_to(s2) > 0.05 and s0.distance_to(s2) > 0.05,
+		"strands: the three lane points occupy distinct ring positions")
+
+
+## r2 W4 — the HUD breach chip: empty keeps it hidden, either latch names
+## its class, BOTH latch lines show together (the elif regression), and a
+## cleared state hides the chip again.
+func _hud_chip(main: Node) -> void:
+	var hud: Hud = main.get_node("HUD")
+	var sim: SimCore = main.get("sim")
+	hud.set_breaches("")
+	check(not hud._breach_panel.visible, "hud: no breaches keeps the chip hidden")
+	sim.sla["email"].lat_breach = true # white-box latch injection (view-only read path under test)
+	var line: String = main._breach_lines()
+	check("email latency SLA breached" in line, "hud: latency latch names the class")
+	sim.sla["email"].loss_breach = true
+	line = main._breach_lines()
+	check("email latency SLA breached" in line and "email loss SLA breached" in line,
+		"hud: BOTH latch lines show together (elif regression pin)")
+	hud.set_breaches(line)
+	check(hud._breach_panel.visible and "email" in hud._breach.text, "hud: chip visible with the breach text")
+	hud.set_breaches("")
+	check(not hud._breach_panel.visible, "hud: cleared state hides the chip")
+	sim.sla["email"].lat_breach = false
+	sim.sla["email"].loss_breach = false
+
+
+## r2 W5 — the visible serialization beat: admissions trip the pulse and
+## the cooldown gates re-pulses.
+func _egress_pulse(main: Node) -> void:
+	var flow: FlowView = main.get_node("FlowView")
+	var sim: SimCore = main.get("sim")
+	var sites: Array = main.get_node("Nodes").get_children().filter(func(c): return c is NodeSite)
+	var site: NodeSite = sites[0]
+	site._pulse_cd = 0.0
+	sim.node_admissions[0] = 2
+	flow.pulse_egress()
+	check(site._pulse_cd > 0.0 and site._pulse_cd <= NodeSite.PULSE_COOLDOWN,
+		"egress: admissions trip the pulse cooldown (%.2fs)" % site._pulse_cd)
+	var cd_after := site._pulse_cd
+	flow.pulse_egress()
+	check(is_equal_approx(site._pulse_cd, cd_after), "egress: the cooldown gates re-pulses")
+	sim.node_admissions[0] = 0
+
+
+func _pair_with_arc(sites: Array, target: float) -> Array:
+	var best: Array = []
+	var best_diff := 1e9
+	for i in sites.size():
+		for j in range(i + 1, sites.size()):
+			var diff: float = absf(Geodesic.arc_angle(sites[i].global_position, sites[j].global_position) - target)
+			if diff < best_diff:
+				best_diff = diff
+				best = [sites[i], sites[j]]
+	return best
+
+
+func _sky_screen_point(cam: Camera3D) -> Vector2:
+	var screen_up := cam.global_transform.basis.y
+	var cam_dir: Vector3 = cam.global_position.normalized()
+	var sky_dir := cam_dir.rotated(screen_up, 0.62).normalized()
+	return cam.unproject_position(cam.global_position + sky_dir * 20.0)
+
+
+func _press(pos: Vector2) -> void:
+	var e := InputEventMouseButton.new()
+	e.button_index = MOUSE_BUTTON_LEFT
+	e.pressed = true
+	e.position = pos
+	e.global_position = pos
+	Input.parse_input_event(e)
+	await tree.process_frame
+	await tree.process_frame
+
+
+func _move(from: Vector2, to: Vector2) -> void:
+	var e := InputEventMouseMotion.new()
+	e.position = to
+	e.global_position = to
+	e.relative = to - from
+	Input.parse_input_event(e)
+	await tree.process_frame
+	await tree.process_frame
+
+
+func _release(pos: Vector2) -> void:
+	var e := InputEventMouseButton.new()
+	e.button_index = MOUSE_BUTTON_LEFT
+	e.pressed = false
+	e.position = pos
+	e.global_position = pos
+	Input.parse_input_event(e)
+	await tree.process_frame
+	await tree.process_frame
diff --git a/tests/test_view_interaction.gd.uid b/tests/test_view_interaction.gd.uid
new file mode 100644
index 0000000..2375952
--- /dev/null
+++ b/tests/test_view_interaction.gd.uid
@@ -0,0 +1 @@
+uid://clo0qa3n8knn0
diff --git a/tests/test_view_purity.gd b/tests/test_view_purity.gd
new file mode 100644
index 0000000..80746af
--- /dev/null
+++ b/tests/test_view_purity.gd
@@ -0,0 +1,85 @@
+extends "res://tests/test_base.gd"
+
+## A1 view contract: orbit / zoom / QoS-panel interactions NEVER shift sim
+## state. The live scene sim must stay byte-identical to an isolated
+## reference sim fed the same commands at the same ticks while the view is
+## being shaken aggressively.
+
+const EXPECTED_CHECKS := 5 # pinned — the runner fails check-count shortfalls (r2 B2)
+const SEED := 20260904
+const SCENE := "res://scenes/main.tscn"
+
+
+func run_all() -> int:
+	print("[test_view_purity]")
+	var result: int = await _run()
+	completed = true
+	return result
+
+
+func _run() -> int:
+	var packed: PackedScene = load(SCENE)
+	if packed == null:
+		check(false, "main.tscn loads")
+		return failures
+	var scene: Node = packed.instantiate()
+	tree.root.add_child(scene)
+	var main := scene
+	var sites: Array = main.get_node("Nodes").get_children().filter(func(c): return c is NodeSite)
+
+	# Same commands, same ticks: the scene path (request_connect / qos apply)
+	# and the reference sim get identical inputs at tick 0.
+	var ref := SimCore.new()
+	ref.setup(SEED, WorldSeed.node_placements(SEED, WorldSeed.wedge_layout(SEED)))
+	var pipe_pairs := [[1, 0], [0, 9], [9, 10], [3, 0], [5, 0], [7, 9], [11, 10], [14, 9]]
+	for pair in pipe_pairs:
+		main.request_connect(sites[pair[0]], sites[pair[1]])
+		ref.apply_command({"cmd": "add_pipe", "a": sites[pair[0]].node_index, "b": sites[pair[1]].node_index})
+	main._on_qos_apply(2, [50, 30, 20], {"email": 2, "streaming": 0})
+	ref.apply_command({"cmd": "set_lanes", "pipe": 2, "alloc": [50, 30, 20], "cls_lane": {"email": 2, "streaming": 0}})
+
+	var rig: OrbitCamera = main.get_node("OrbitRig")
+	var qos: QosPanel = main.get_node("QosPanel")
+	var diverged := -1
+	for i in 420:
+		await tree.physics_frame
+		# --- VIEW NOISE: everything that must never touch the sim ---
+		rig.orbit(Vector2(1.7, -0.9))
+		if i % 7 == 0:
+			rig.zoom(1 if (i / 7) % 2 == 0 else -1)
+		rig.frame_point(sites[3].global_position, i % 3)
+		if i % 5 == 0:
+			qos.open(2, main.sim)
+			qos._on_class_cycle("email")
+			qos._on_class_cycle("email")
+			qos._on_class_cycle("streaming")
+			qos.close_panel()
+		# ------------------------------------------------------------
+		while ref.tick < main.sim.tick:
+			ref.step_tick()
+		if ref.tick == main.sim.tick and ref.state_hash() != main.sim.state_hash():
+			diverged = i
+			break
+
+	check(diverged < 0, "view noise never shifts sim state (hash identical; diverged at %d)" % diverged)
+	check(main.sim.tick >= 400, "scene sim actually stepped (%d ticks — pin is not vacuous)" % main.sim.tick)
+	var carried := int(main.sim.sla["email"].delivered) + int(main.sim.sla["streaming"].delivered)
+	check(carried > 0, "purity scenario carries real traffic (%d delivered)" % carried)
+	check(ref.dump_state() == main.sim.dump_state(), "final dumps byte-identical under view noise")
+
+	# Negative control — the comparison must be ABLE to fail: one deliberate
+	# sim-side command the reference never sees diverges the hashes at once.
+	var caught := false
+	main.sim.apply_command({"cmd": "add_pipe", "a": 21, "b": 20})
+	for i in 5:
+		await tree.physics_frame
+		while ref.tick < main.sim.tick:
+			ref.step_tick()
+		if ref.tick == main.sim.tick and ref.state_hash() != main.sim.state_hash():
+			caught = true
+			break
+	check(caught, "purity negative control: a real sim mutation IS detected (this pin can fail)")
+
+	tree.root.remove_child(scene)
+	scene.free()
+	return failures
diff --git a/tests/test_view_purity.gd.uid b/tests/test_view_purity.gd.uid
new file mode 100644
index 0000000..2e4c4bf
--- /dev/null
+++ b/tests/test_view_purity.gd.uid
@@ -0,0 +1 @@
+uid://luyw8yb55qs3
diff --git a/tests/test_no_sim.gd b/tests/test_world.gd
similarity index 55%
rename from tests/test_no_sim.gd
rename to tests/test_world.gd
index f575e7d..1166d1f 100644
--- a/tests/test_no_sim.gd
+++ b/tests/test_world.gd
@@ -1,15 +1,16 @@
 extends "res://tests/test_base.gd"
 
-## Structural contracts: the slice boots headless, wires all its nodes, and
-## carries NO simulation state (E1 is presentation + input only). Also pins
-## the snap-intent commit endpoints and the parallel-bundle merge.
+## Structural contracts (E2): the slice boots headless, wires all its nodes,
+## and owns a deterministic SimCore whose pipe state flows ONLY through the
+## command bus. E2 supersedes E1's "no sim anywhere" structural assertion —
+## the sim now exists, is seed-fixed, and the world contracts keep holding.
 
-const SIM_METHOD_FRAGMENTS := ["tick", "step_", "advance", "simulate", "_sim_"]
+const EXPECTED_CHECKS := 24 # pinned — the runner fails check-count shortfalls (r2 B2)
 const SEED := 20260904
 
 
 func run_all() -> int:
-	print("[test_no_sim]")
+	print("[test_world]")
 	var packed: PackedScene = load("res://scenes/main.tscn")
 	if packed == null:
 		check(false, "main.tscn loads")
@@ -19,12 +20,13 @@ func run_all() -> int:
 	check(true, "main scene instantiates headless (boots)")
 
 	if _world_built(scene):
+		_sim_wiring(scene)
 		_commit_endpoints(scene)
 		_parallel_merge(scene)
-	_no_sim_state(scene)
 
 	tree.root.remove_child(scene)
 	scene.free()
+	completed = true
 	return failures
 
 
@@ -49,14 +51,19 @@ func _world_built(scene: Node) -> bool:
 	# E1.5 input-grammar properties: surface-normal orientation + layer 2.
 	var orient_ok := true
 	var layer_ok := true
-	for s2 in sites:
+	var indexed := true
+	for i in sites.size():
+		var s2: NodeSite = sites[i]
 		var n2: Vector3 = s2.surface_pos.normalized()
 		if s2.global_transform.basis.y.dot(n2) < 0.999:
 			orient_ok = false
 		if s2.collision_layer != 2:
 			layer_ok = false
+		if s2.node_index != i:
+			indexed = false
 	check(orient_ok, "node bases align to their surface normals")
 	check(layer_ok, "nodes sit on physics layer 2 (the press-to-draw grammar)")
+	check(indexed, "node_index matches staging order (sim id = view id)")
 	# Determinism: same seed -> identical placements.
 	var a := WorldSeed.node_placements(SEED, WorldSeed.wedge_layout(SEED))
 	var b := WorldSeed.node_placements(SEED, WorldSeed.wedge_layout(SEED))
@@ -69,15 +76,40 @@ func _world_built(scene: Node) -> bool:
 	return true
 
 
+func _sim_wiring(scene: Node) -> void:
+	var sim = scene.get("sim")
+	check(sim is SimCore, "main owns a SimCore (RefCounted — no sim Node in the tree)")
+	check(sim.seed_value == SEED, "sim seed = the slice seed")
+	check(sim.pipes.is_empty(), "boot state has no pipes (nothing auto-creates)")
+	check(sim.tick == 0, "sim boots at tick 0")
+	var in_sim_group := false
+	var stack: Array = [scene]
+	while not stack.is_empty():
+		var n: Node = stack.pop_back()
+		if n.is_in_group("sim"):
+			in_sim_group = true
+		stack.append_array(n.get_children())
+	check(not in_sim_group, "no NODE carries the 'sim' group (sim state lives outside the tree)")
+	# Autoloads register as autoload/<Name> settings — a bare "autoload" key
+	# never exists, so the old has_setting("autoload") guard was vacuous.
+	check(not ProjectSettings.has_setting("autoload/Sim"), "no Sim autoload registered")
+
+
 func _commit_endpoints(scene: Node) -> void:
-	var controller: ConnectController = scene.get_node("ConnectController")
+	var sim: SimCore = scene.get("sim")
+	if sim == null:
+		check(false, "sim wiring present (cannot commit without it)")
+		return
 	var sites: Array = scene.get_node("Nodes").get_children().filter(func(c): return c is NodeSite)
+	if sites.size() < 2:
+		return # world_built already flagged the staging failure
 	var a: NodeSite = sites[0]
 	var b: NodeSite = sites[1]
-	var arc := controller.connect_programmatic(a, b)
+	var arc: PipeArc = scene.request_connect(a, b)
 	check(arc != null, "commit returns the pipe arc")
-	check(vapprox(arc._a, a.global_position, 1e-5), "arc endpoint = snapped NODE a (intent, not release point)")
-	check(vapprox(arc._b, b.global_position, 1e-5), "arc endpoint = snapped NODE b (intent, not release point)")
+	check(vapprox(arc._a, a.surface_pos, 1e-5), "arc endpoint = node a surface position (sim geometry)")
+	check(vapprox(arc._b, b.surface_pos, 1e-5), "arc endpoint = node b surface position (sim geometry)")
+	check(sim.pipe_count(a.node_index, b.node_index) == 1, "sim registers the bundle")
 	var pts := Geodesic.elevated_path(arc._a, arc._b, WorldSeed.PLANET_RADIUS, PipeArc.BASE_ELEVATION_FRAC * WorldSeed.PLANET_RADIUS, 16)
 	var ok := true
 	for p in pts:
@@ -87,43 +119,19 @@ func _commit_endpoints(scene: Node) -> void:
 
 
 func _parallel_merge(scene: Node) -> void:
-	var controller: ConnectController = scene.get_node("ConnectController")
+	var sim: SimCore = scene.get("sim")
+	if sim == null:
+		return # _commit_endpoints already flagged it
 	var sites: Array = scene.get_node("Nodes").get_children().filter(func(c): return c is NodeSite)
+	if sites.size() < 4:
+		return
 	var a: NodeSite = sites[2]
 	var b: NodeSite = sites[3]
-	controller.connect_programmatic(a, b)
-	var arc := controller.connect_programmatic(a, b)
-	check(controller.pipe_count(a, b) == 2, "parallel pipes register under one bundle")
-	check(arc._radius_scale > 1.0, "merged bundle renders fatter")
-	check(vapprox(arc._a, a.global_position, 1e-5) and vapprox(arc._b, b.global_position, 1e-5), "merged bundle keeps the same geodesic path")
-	# Reverse-direction draw merges into the SAME bundle.
-	controller.connect_programmatic(b, a)
-	check(controller.pipe_count(a, b) == 3, "A->B and B->A share the bundle key")
-
-
-func _no_sim_state(scene: Node) -> void:
-	var in_sim_group := false
-	var stack: Array = [scene]
-	while not stack.is_empty():
-		var n: Node = stack.pop_back()
-		if n.is_in_group("sim"):
-			in_sim_group = true
-		stack.append_array(n.get_children())
-	check(not in_sim_group, "no node carries the 'sim' group")
-	var scripts_dirty := false
-	var script_stack: Array = [scene]
-	while not script_stack.is_empty():
-		var sn: Node = script_stack.pop_back()
-		if sn.get_script() != null:
-			for m in sn.get_script().get_script_method_list():
-				var lower: String = str(m.name).to_lower()
-				for frag in SIM_METHOD_FRAGMENTS:
-					if lower.contains(frag):
-						scripts_dirty = true
-		script_stack.append_array(sn.get_children())
-	check(not scripts_dirty, "no tick/step/advance/simulate methods anywhere in the slice")
-	if not ProjectSettings.has_setting("autoload"):
-		check(true, "no autoloads registered at all (no Sim possible)")
-	else:
-		var autoloads: Dictionary = ProjectSettings.get_setting("autoload")
-		check(not autoloads.has("Sim"), "no Sim autoload registered")
+	var arc1: PipeArc = scene.request_connect(a, b)
+	var arc2: PipeArc = scene.request_connect(a, b)
+	check(sim.pipe_count(a.node_index, b.node_index) == 2, "parallel pipes register under ONE sim bundle")
+	check(arc1 == arc2, "the view reuses one arc for the merged bundle")
+	check(arc1._radius_scale > 1.0, "merged bundle renders fatter")
+	var arc3: PipeArc = scene.request_connect(b, a)
+	check(sim.pipe_count(a.node_index, b.node_index) == 3, "A->B and B->A share the bundle")
+	check(arc3 == arc1, "reverse draw merges into the same view arc")
diff --git a/tests/test_world.gd.uid b/tests/test_world.gd.uid
new file mode 100644
index 0000000..e228bc9
--- /dev/null
+++ b/tests/test_world.gd.uid
@@ -0,0 +1 @@
+uid://bm510mrht41c


--- SPEC / CONTEXT ---
=== ORIGINAL JOB BRIEFING (task spec) ===
# Briefing: packet-plumber-3d-e2-flow-qos

Read the standing orders first: `/Users/moses/code/docs/orchestration-playbook.md`
section 'Minion standing orders'. This briefing is your task spec.

## Task

Build **E2 — Flow Simulation, Packet Types & QoS** (the living network), plus
one folded QoL story (editor preview). Spec of record:
`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-3d-2026-09-04/epics.md`
section **E2** (+ GDD's sim/QoS sections). The epic's stories E2.1–E2.5 and
test contracts ARE your acceptance criteria.

## Scope (from the epic)

1. **E2.1 Flow simulation** — deterministic tick-driven sim core (owned RNG,
   fixed tick); junctions forward per-packet (ECMP hash across equal-cost
   paths); parallel pipes bundle into pooled capacity; path cost = static
   pipe-tier cost. *(PP-Odin rulings inherited.)*
2. **E2.2 Packet classes** — MVP: email (low/low/low) + streaming (med/med/high).
3. **E2.3 Link-level class queues** — 3 lanes per pipe (Express/Standard/
   Best-effort); all traffic starts Standard 100%; assignment ladder
   (100 · 70/30 · 50/30/20) data-driven; per-pipe overrides; QoS panel on
   pipe select. **Nothing auto-allocates.**
4. **E2.4 Serialization at nodes** — Express → Standard → Best-effort
   egress, work-conserving gap-filling; VISIBLE in 3D (strand speed + node
   egress rate).
5. **E2.5 Per-class SLA tracking** — latency/loss per class; thresholds
   from the GDD's Numerical Design section.

**Folded QoL (user ruling, gate feedback):** `@tool` **editor preview** — an
inspector "Regenerate Preview" on the composition root that runs the SAME
seeded generation inside the editor viewport (canon `_ready()` flow
untouched; no behavior change at runtime). The user should SEE the world in
the editor without pressing play.

**Scale ruling (user):** world stays at slice-1 scale for E2 — NO scale/density
changes. Big world is E3's epic. Do not freelance density.

## Acceptance

- **A1 (canon):** every E2 test contract demonstrable — replay **byte-identity
  on a fixed seed** · contention drops by drop precedence (lowest first) ·
  dedicated lane reservation holds its class's capacity · SLA breach
  detectable + attributable · **view-layer changes never shift sim state**
  (orbit/zoom/QoS panel interactions leave the replay hash unchanged).
- **A2 (visible):** packets visibly stream along arcs at class-dependent
  speed; egress serialization readable at nodes. Captures in `captures/`
  referenced from the PR body (replay determinism capture + a QoS-panel
  interaction capture + editor-preview viewport capture).
- **A3 (verified):** Godot MCP is your build/verify surface — `editor-run`,
  `debug-output`, `lsp_get_diagnostics` clean on all GDScript.
- **A4 (gate):** PR opens, Perkins loops to APPROVED, the user plays and
  rules. PR body carries the run command.

## Model policy

Minion: **`zai-coding-cn/glm-5.3-flash`**. Mega-minions: same, skills named.

## Skills policy

Workflow: **`gds-quick-dev`**. No lavish (code deliverable).

## Perkins

`pr_review=1` — canon-surface sim code. Loop-until-APPROVED; fold fixes
locally, hold the push until each verdict posts.

## Dispatch parameters

```
job_id:    packet-plumber-3d-e2-flow-qos
repo:      packet-plumber-3d
repo_root: /Users/moses/code/packet-plumber-3d
slug:      e2-flow-qos
base:      main
model:     zai-coding-cn/glm-5.3-flash
pr_review: 1
notes:     Worktree from origin/main (c4edcef). _bmad symlink bootstrap.
           PARALLEL LANE: packet-plumber-3d-asset-scout also dispatches —
           create worktrees strictly sequentially (index.lock race).
```


=== EPIC SPEC: E2 — Flow Simulation, Packet Types & QoS (the acceptance criteria: stories E2.1–E2.5 + test contracts) ===
## E2 — Flow Simulation, Packet Types & QoS

**Delivers** the living network: PP-E1's flow simulation (deterministic, tick-driven) + PP-E2's packet types and QoS in full. *Playable value: packets stream across the little world; routing has trade-offs.*

- **E2.1** Flow simulation *(from PP-E1)* — deterministic tick-driven sim core (owned RNG, fixed tick); junctions forward per-packet (ECMP hash across equal-cost paths); parallel pipes bundle into pooled capacity; path cost = static pipe-tier cost ("fattest route; equal cost splits by hash"). *(PP-Odin 2026-08-10/13 rulings, inherited.)*
- **E2.2** Packet-class definition — MVP: email (low/low/low) + streaming (med/med/high). `[FORGE #4]`
- **E2.3** Link-level class queues — 3 lanes per pipe (Express/Standard/Best-effort); all traffic starts Standard at 100%; assignment ladder (100 · 70/30 · 50/30/20) data-driven; per-pipe overrides; QoS panel on pipe select. **Nothing auto-allocates.** *(Inherited.)*
- **E2.4** Serialization at nodes — Express → Standard → Best-effort egress, work-conserving gap-filling; visible in 3D (strand-speed + node egress). *(Inherited.)*
- **E2.5** Per-class SLA tracking — latency/loss accumulate per class; thresholds from Numerical Design.
- **Test contracts:** replay byte-identity on a fixed seed (determinism contract); contention drops by drop precedence (lowest first); a dedicated lane reservation holds its class's capacity; SLA breach is detectable and attributable; view-layer changes never shift sim state.


--- YOUR LENS ---
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

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

--- CHUNKING DISCLOSURE ---
This PR's diff (4240 lines) was split into 2 file-group chunks per the big-diff policy; you are reviewing chunk 2 of 2 — the TESTS + EVIDENCE: tests/, captures/, _bmad-output/, README (44 files, 2302 lines). The other chunk is reviewed by a sibling wave. Do NOT report the other chunk's content as missing — its absence from your DIFF section is an artifact of chunking, not a PR defect.


--- FILE-OUTPUT CONTRACT (headless round) ---
Write ONLY your JSON array to this exact absolute path (do not derive it, do not write anywhere else):
/Users/moses/code/_bmad-output/perkins/packet-plumber-3d-e2-flow-qos/r3/tests-c2.json
The file must contain the JSON array and nothing else. Then stop.
