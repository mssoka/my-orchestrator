# Perkins lens prompt — edge (round 1, single wave)

**You are the `edge` lens. Your assigned `source` tag is `edge`. Your output file is `/Users/moses/code/_bmad-output/perkins/packet-plumber-routing-readability-assist/r1/edge.json`.**

You are ONE lens in a Perkins automated PR-review swarm (round 1 of 3). Perkins reviews; lenses find; nobody fixes. You run as a pi agent. Review, then write your JSON and STOP — do not fix anything, do not modify any file other than your output file.

## Your inputs (READ THESE)
- CANONICAL DIFF (review exactly these bytes): /Users/moses/code/_bmad-output/perkins/packet-plumber-routing-readability-assist/r1/diff.patch (embedded below for convenience)
- WORKTREE (read-only verification at the reviewed sha b0a6def): /Users/moses/.herdr/worktrees/packet-plumber/perkins-routing-readability-assist-r1
- SPEC / CONTEXT:  - Perkins briefing (your charter + the CRITICAL lens-guards): /Users/moses/code/_bmad-output/perkins/packet-plumber-routing-readability-assist/r1/spec/perkins-briefing-r1.md
  - Job briefing (the original Job-A brief — context for what B builds on): /Users/moses/code/_bmad-output/perkins/packet-plumber-routing-readability-assist/r1/spec/job-briefing.md
  - The canon (user ruling 2026-08-13 — PROBLEM DEFINITION, SUCCESS CRITERIA, RECOMMENDED SOLUTION with the R2a/R3/T2 package; this drives Job B): /Users/moses/code/_bmad-output/perkins/packet-plumber-routing-readability-assist/r1/spec/canon.md
  - PR body (the minion's own launchable description): /Users/moses/code/_bmad-output/perkins/packet-plumber-routing-readability-assist/r1/spec/pr-body.md
  - The minion's frozen spec is IN the diff itself (_bmad-output/implementation-artifacts/spec-routing-readability-assist.md) — the acceptance matrix + code map + the documented balance.json deviation.

--- DIFF ---
diff --git a/.github/workflows/ci.yml b/.github/workflows/ci.yml
index 3a0e1b5..c76dbab 100644
--- a/.github/workflows/ci.yml
+++ b/.github/workflows/ci.yml
@@ -88,6 +88,14 @@ jobs:
       - name: W1 drift-rejection negative test
         run: tools/harness.sh drift-check
 
+      # Job B (readability package): the R2a what-if preview must equal the
+      # sim's own routing once the candidate draw commits (preview DAG edge
+      # set + cost + tie splits vs the rebuilt table + the packet's actual
+      # hash-picked path). The negative control is a local run; CI pins the
+      # green path.
+      - name: Assist preview cross-check (R2a preview == sim routing)
+        run: tools/harness.sh preview-check
+
       - name: Upload diff bundles on failure
         if: failure()
         uses: actions/upload-artifact@v4
diff --git a/_bmad-output/field-notes/packet-plumber-routing-readability-assist.md b/_bmad-output/field-notes/packet-plumber-routing-readability-assist.md
new file mode 100644
index 0000000..43bcb73
--- /dev/null
+++ b/_bmad-output/field-notes/packet-plumber-routing-readability-assist.md
@@ -0,0 +1,17 @@
+# Field notes — packet-plumber-routing-readability-assist (Job B)
+
+- 2026-08-14: packets spawn AND forward in the same tick — a packet at a
+  source with a complete route is never observable at the node; the preview's
+  "packet at a node" states need either unroutable-waiting packets or the
+  between-ticks ARRIVAL WINDOW (an edge completing at tick T leaves the packet
+  at the node until T+1's forward) — the tie scenario's junction packet is
+  only observable that way.
+- 2026-08-14: with a spawn-then-forward flow, "fat path vs reachable narrow
+  rival" preview states are unconstructible with the packet at the source —
+  the honest pin is: rival legs drawn at PREVIEW time (excluded by reachability)
+  + the narrow second leg drawn at the CROSS-CHECK step, then assert the sim
+  table excludes the now-REACHABLE rival (the competition is proven post-commit).
+- 2026-08-14: a cancelled drag must never corrupt the R3 glow — the live drag
+  DAG and the committed glow DAG need SEPARATE buffers (deep-copied at commit);
+  the shared-buffer first cut rendered a never-committed path (raw halo over a
+  nonexistent pipe) for the rest of the old glow window (2-hunter review HIGH).
diff --git a/_bmad-output/implementation-artifacts/spec-routing-readability-assist.md b/_bmad-output/implementation-artifacts/spec-routing-readability-assist.md
new file mode 100644
index 0000000..210e863
--- /dev/null
+++ b/_bmad-output/implementation-artifacts/spec-routing-readability-assist.md
@@ -0,0 +1,183 @@
+---
+status: done
+job: packet-plumber-routing-readability-assist
+slug: routing-readability-assist
+base: v2
+baseline_commit: 69fc2e5
+canon: _bmad-output/problem-solution-2026-08-13.md (R2a/R3/T2, fun-factor, M6-M9)
+---
+
+# Spec — Job B: the readability package (app layer)
+
+## Intent
+
+**Problem:** Job A's cost routing is invisible — players cannot predict "flows
+prefer fat pipes" by looking, upgrades show no visible payoff, and ECMP splits
+look random. The fun gate (user ruling 2026-08-13) demands PERCEPTION, not
+mental arithmetic.
+
+**Approach:** a view-only readability package: R2a live cost-sum preview while
+drawing (what-if routing over the candidate pipe: winning-path glow + ONE
+number), tiered assist (full → glow-only → off, T toggles, data-driven
+graduation nudge, opt-in never forced), R3 post-draw route glow (the stored
+preview DAG, expiring), T2 tie cue ("equal cost - split by hash" marks both
+paths at ECMP splits). STRICT ODN-12: never feeds sim state; goldens must not
+shift.
+
+## Boundaries & Constraints
+
+**Always:**
+- View-only (ODN-12): reads the routing table + tier costs; NEVER mutates
+  `Run_State` (the what-if table lives on an app-owned scratch clone).
+- Goldens byte-identical: no change to any `data/*.json` folded into
+  `catalog_hash` (balance/pipe_tiers/node_types/packet_types/demand/crises),
+  no change to `core/` (scope guard), no pixels added to the harness capture
+  path (`draw_world` untouched; the harness passes a zero drag and never calls
+  the new draw procs).
+- Deterministic render math: no transcendentals; ASCII-only string literals in
+  render/app (lint gate 6 — "equal cost - split by hash" with a hyphen, never
+  an em-dash).
+- Assist config is data-driven (ODN-5) but in a NEW cosmetic-class file
+  (`data/assist.json`, palette pattern — never handed to `catalogs_load`).
+  **Deviation from the briefing's "N in balance.json": balance.json folds
+  every byte into cat.hash → any field addition re-blesses ALL goldens
+  (violates acceptance 5, STRICT). Precedent: PLACEMENT_MIN_SEP_TILES in
+  core/topology.odin carries the same comment. Flagged for the human; a
+  future legitimate re-bless can move it.**
+
+**Ask First:** nothing expected — the acceptance hierarchy resolves the
+balance.json conflict (STRICT golden clause wins).
+
+**Never:** no core/sim changes (not even new core procs — `routing_rebuild` is
+already public + pure and is CALLED, not modified); no forecast-panel changes
+(Job C owns `app/render/forecast.odin` — parallel worktree; if needed, flag to
+Silas); no re-bless of any golden; no `balance.json` edits.
+
+## I/O & Edge-Case Matrix
+
+| Scenario | Input / State | Expected Output / Behavior | Error Handling |
+|----------|--------------|---------------------------|----------------|
+| Draw completes a route (fixture: drag router→host while a packet waits at res) | valid candidate; packet at res, dst host | glow = full DAG res→router→host; "route 20"; commit → R3 glow 120 ticks | candidate invalid → ghost red, no preview |
+| Upgrade shifts the flow (wide m1→host beats narrow m2→host) | candidate fat edge | glow = fat path only (narrow legs NOT in DAG); "route 10" | no packet affected → no glow, no number |
+| True different-tier tie (15 == 15) | candidate completes an equal-cost 2nd path | BOTH paths glow; split node marked "equal cost - split by hash"; "route 15" | — |
+| Draw completes NO route (dead-end branch) | candidate with no dst reachable | no glow, no route number (draw-cost readout only, mode Full) | — |
+| Assist modes | T key | Full→Glow_Only→Off→Full; Off = no routing visuals (glow/tie/route number); the assist-mode indicator + the draw-cost readout remain (the toggle's discoverability, not routing assist) | — |
+| Graduation nudge | N successful draws, mode Full, nudge unseen | one HUD line for nudge_ticks, once per run; any toggle dismisses | restart resets counter |
+| ECMP tie mid-DAG | packet's DAG branches | both branches glow (T2), one number (shared cost) | — |
+
+## Code Map
+
+- `app/render/assist.odin` -- NEW: Assist_Mode enum, Assist_Config load (#load
+  embed + fallback), Preview_Scratch (clone topo + what-if Routing_Table +
+  DAG buffers), `preview_compute` (clone → apply candidate → routing_rebuild →
+  first-affected-packet DAG walk), `draw_route_preview`/`draw_route_glow`
+  (halo over DAG bundles via `bundles_slot_for_pair`, tie labels, route
+  readout). Uses public pure `pp.routing_rebuild` + `pp.routing_equal_cost_hops`.
+- `app/main.odin` -- App fields (assist_mode, preview scratch, glow_until,
+  draws_since_nudge, nudge state); T toggle in handle_input; preview compute
+  during drag (mode != Off); commit → glow + nudge counter; draw_hud lines.
+- `data/assist.json` -- NEW: `default_mode` (full), `graduation_n` (8),
+  `glow_ticks` (120), `nudge_ticks` (120). Not hashed.
+- `data/palette.json` -- ADD keys only: `route_glow`, `route_tie` (+ fallback
+  fields in palette.odin). Existing values untouched.
+- `harness/assist_check.odin` -- NEW: `run_assist_check` — 3 scenarios
+  (fat-path shift, true tie, fixture route + a no-route negative): compute the
+  preview via the production helper, apply candidate + step, compare preview
+  DAG/cost/splits against the sim's rebuilt table + the packet's actual
+  hash-picked path.
+- `harness/main.odin` -- NEW verb `preview-check`.
+- `.github/workflows/ci.yml` -- add the preview-check step after W1.
+
+## Tasks & Acceptance
+
+**Execution:**
+- [x] `data/assist.json` -- new cosmetic-class config (default_mode /
+  graduation_n / glow_ticks / nudge_ticks) -- data-driven ODN-5 without
+  poisoning cat.hash.
+- [x] `data/palette.json` + `app/render/palette.odin` -- add route_glow +
+  route_tie keys (values only appended; fallback_palette mirrors) -- the glow
+  colors, T2-safe by construction.
+- [x] `app/render/assist.odin` -- the readability package (config load,
+  what-if preview, DAG walk, glow/tie/readout render) -- the R2a/R3/T2 core.
+- [x] `app/main.odin` -- assist state + T toggle + nudge + wiring -- the
+  playable surface.
+- [x] `harness/assist_check.odin` + `harness/main.odin` -- `preview-check`
+  verb -- the launchable cross-check (preview == sim).
+- [x] `.github/workflows/ci.yml` -- preview-check step -- the gate.
+
+**Acceptance Criteria:**
+- Given a valid drag in Full mode with an affected packet, when the ghost is
+  snapped, then the winning path DAG glows and ONE number ("route N") shows
+  near the cursor; no candidate spreadsheet anywhere.
+- Given a true ECMP tie on the preview DAG, when rendered, then BOTH paths are
+  marked with "equal cost - split by hash" (ASCII) at the split node.
+- Given a successful draw commit in Full/Glow_Only, when the sim steps, then
+  the winning path keeps glowing for glow_ticks (R3); assist Off shows no
+  routing visuals at any point.
+- Given N successful draws in Full mode with the nudge unseen, when N is
+  reached, then one opt-in HUD line appears once (never a modal, never
+  forced); any T press dismisses it.
+- Given the harness `preview-check` verb, when run, then every scenario's
+  preview DAG edge set + cost match the sim's rebuilt routing table and the
+  packet's actual hash-picked path (the cross-check).
+- Given the full gate suite, when run on this branch, then lint green, `odin
+  test core` green, `tools/harness.sh run` green (all 16 demos, T1+T2+replay),
+  `tools/harness.sh preview-check` green, app.bin builds, and `goldens/*.t1`
+  + `*.log.bin` byte-identical to baseline 69fc2e5 (sha256-compare).
+
+## Verification
+
+**Commands:**
+- `tools/lint.sh` -- all gates green (ASCII gate 6 included)
+- `odin test core` -- 126 tests green, unchanged
+- `tools/harness.sh run` -- 16 demos green (T1/T2/replay; goldens unchanged)
+- `tools/harness.sh preview-check` -- new verb green (preview == sim)
+- `odin build app -out:app.bin` -- links
+- `shasum -a 256 goldens/*.t1 goldens/*.log.bin` -- identical to the baseline
+  snapshot taken before any edit
+
+## Suggested Review Order
+
+**The what-if preview (the R2a core)**
+
+- Entry point: the what-if clone + first-affected-packet rule; ONE number, view-only
+  [`assist.odin:267`](../../app/render/assist.odin#L267)
+
+- The tight-edge DAG walk + T2 split detection (array-only, deterministic)
+  [`assist.odin:320`](../../app/render/assist.odin#L320)
+
+- The committed-glow copy (a cancelled drag can never corrupt the R3 glow)
+  [`assist.odin:178`](../../app/render/assist.odin#L178)
+
+- The shared glow/tie/readout renderer (Full vs Glow_Only gating)
+  [`assist.odin:391`](../../app/render/assist.odin#L391)
+
+**App wiring (toggle, glow lifecycle, nudge)**
+
+- The per-frame render gate: preview during drag, R3 glow after commit, Run-mode-only
+  [`main.odin:172`](../../app/main.odin#L172)
+
+- The T tier toggle (full -> glow-only -> off) + nudge engagement latch
+  [`main.odin:262`](../../app/main.odin#L262)
+
+- The commit path: glow copy + glow_until/gen + the graduation counter + nudge
+  [`main.odin:403`](../../app/main.odin#L403)
+
+- The assist indicator + nudge HUD lines (bottom-right, ASCII)
+  [`main.odin:745`](../../app/main.odin#L745)
+
+**The cross-check (preview == sim routing)**
+
+- The seven scenarios: fixture route, reachable-rival fat path, true tie, dead-end, mid-flight, first-packet-skip, parallel no-op
+  [`assist_check.odin:191`](../../harness/assist_check.odin#L191)
+
+- CI gate for the cross-check
+  [`ci.yml:97`](../../.github/workflows/ci.yml#L97)
+
+**Data (cosmetic-class, golden-safe)**
+
+- The assist config (NOT in balance.json — cat.hash is golden-poisoned; see the spec's Boundaries)
+  [`assist.json:1`](../../data/assist.json#L1)
+
+- The route-glow/tie palette additions (existing values untouched)
+  [`palette.json:37`](../../data/palette.json#L37)
diff --git a/app/main.odin b/app/main.odin
index bb96fb4..e23998e 100644
--- a/app/main.odin
+++ b/app/main.odin
@@ -69,6 +69,24 @@ App :: struct {
 	sel_class:   u16,
 	last_reject: pp.Edit_Error, // 3.2: the most recent QoS edit rejection (drawn while fresh)
 	reject_tick: u64,           // the tick the rejection landed (toast age)
+	// Job B (readability package, canon 2026-08-13): the R2a assist tiers +
+	// the R3 post-draw glow + the graduation nudge. TWO preview buffers:
+	// `preview` is the live drag what-if; `glow` is the COMMITTED DAG (copied
+	// at commit — a cancelled drag must never corrupt the running glow). Node
+	// ids recycle across runs, so both are released per run; the tier is a
+	// SETTING and persists across in-session restarts (a fresh launch starts
+	// at the config default — no settings I/O yet).
+	assist:            rnd.Assist_Config,   // data/assist.json (cosmetic — never in cat.hash)
+	assist_mode:       rnd.Assist_Mode,     // the tier (T cycles: full -> glow-only -> off)
+	preview:           rnd.Route_Preview,   // the live drag what-if DAG
+	glow:              rnd.Route_Preview,   // the committed R3 glow DAG (preview_copy at commit)
+	preview_scratch:   rnd.Preview_Scratch, // what-if buffers (persistent, frame-reused)
+	preview_live:      bool,                // a drag preview is active THIS frame
+	glow_until:        u64,                 // R3: post-draw glow expiry tick (0 = none)
+	glow_gen:          u32,                 // the live Topology.gen the glow DAG is valid for
+	nudge_until:       u64,                 // the graduation nudge HUD dwell (0 = none)
+	draws_since_nudge: u32,                 // successful draws since the run start
+	nudge_done:        bool,                // the nudge was shown or the tier engaged this run
 }
 
 main :: proc() {
@@ -91,6 +109,11 @@ main :: proc() {
 	app.lose_tick_cap = LOSE_TICK_CAP
 	app.sel_pipe = -1 // 3.2: no selection at startup (0 is a LIVE pipe id, not a sentinel)
 	app.sel_class = 0
+	// Job B: the assist config + the starting tier (full for beginners —
+	// canon; the tier persists across in-session restarts once toggled, and a
+	// fresh launch starts at the config default).
+	app.assist = rnd.assist_config_load()
+	app.assist_mode = app.assist.default_mode
 
 	// the first run: seed 42 (reproducible — matches the harness fixture). The
 	// session goal + cap are applied inside start_run. Restarts mint a fresh
@@ -146,6 +169,23 @@ main :: proc() {
 		defer rl.EndDrawing()
 		rl.ClearBackground(app.palette.canvas)
 		rnd.draw_world(&app.view, &app.state.topology, &app.state.bundles, &app.state.flow, &app.state.crisis, app.tick, app.drag, app.sel_pipe)
+		// Job B: the readability surface (view-only — never in the harness
+		// capture path, so T2 goldens cannot shift; gated to Run mode — a
+		// terminal run freezes ticks, so the glow must not linger behind the
+		// game-over toast). During a drag: the live R2a preview (glow + tie
+		// cues + the ONE number in Full mode). After a commit: the R3 glow
+		// for glow_ticks from the COMMITTED glow buffer, valid while the
+		// topology gen hasn't moved on (a QoS emphasis edit also bumps gen —
+		// the glow drops early, conservatively, never stale).
+		if app.mode == .Run && app.assist_mode != .Off {
+			if app.preview_live && app.preview.ok && app.drag.active {
+				rnd.draw_route_glow(&app.view, &app.state.topology, &app.state.bundles, &app.preview,
+					app.assist_mode == .Full, rnd.to_screen(&app.view, app.drag.wx, app.drag.wy))
+			} else if app.tick <= app.glow_until && app.state.topology.gen == app.glow_gen &&
+				!app.drag.active && app.glow.ok {
+				rnd.draw_route_glow(&app.view, &app.state.topology, &app.state.bundles, &app.glow, false, {})
+			}
+		}
 		draw_hud(&app)
 	}
 }
@@ -174,6 +214,18 @@ start_run :: proc(app: ^App, seed: u64) {
 	app.sel_class = 0
 	app.last_reject = .None
 	app.reject_tick = 0
+	// Job B: the readability state is run-scoped (node ids recycle across
+	// runs — a stale DAG must never survive; the assist TIER is a setting and
+	// persists across in-session restarts). The scratch buffers are reused
+	// across runs (no teardown).
+	rnd.preview_release(&app.preview)
+	rnd.preview_release(&app.glow)
+	app.preview_live = false
+	app.glow_until = 0
+	app.glow_gen = 0
+	app.nudge_until = 0
+	app.draws_since_nudge = 0
+	app.nudge_done = false
 	app.mode = .Run
 	app.run_live = true
 }
@@ -207,6 +259,22 @@ handle_input :: proc(app: ^App) {
 		return
 	}
 
+	// Job B: the assist tier toggle (T) — the R2a graduation control:
+	// full -> glow-only -> off -> full. Any engagement with the toggle
+	// dismisses the graduation nudge for this run (opt-in, never forced).
+	if rl.IsKeyPressed(.T) {
+		switch app.assist_mode {
+		case .Full:
+			app.assist_mode = .Glow_Only
+		case .Glow_Only:
+			app.assist_mode = .Off
+		case .Off:
+			app.assist_mode = .Full
+		}
+		app.nudge_done = true
+		app.nudge_until = 0
+	}
+
 	mx, my := rl.GetMouseX(), rl.GetMouseY()
 	wx, wy := rnd.from_screen(&app.view, f32(mx), f32(my))
 
@@ -277,6 +345,7 @@ handle_input :: proc(app: ^App) {
 			app.drag.valid = .None
 			app.drag.cost = 0
 			app.drag_to = 0
+			app.preview_live = false // Job B: no stale preview from a previous drag (recomputed on the move frames)
 		} else {
 			// 3.2: a press on empty space selects the nearest pipe within the
 			// hit radius (the emphasis dial's target); a press on pure canvas
@@ -302,6 +371,17 @@ handle_input :: proc(app: ^App) {
 			app.drag.valid = .None
 			app.drag.cost = 0
 		}
+		// Job B (R2a): the live what-if preview — while a valid candidate is
+		// snapped and assist is not off, compute the path packets WILL take
+		// (a pure what-if table on a scratch clone — view-only, ODN-12; the
+		// harness cross-checks this against the sim's own routing).
+		if app.drag_to != 0 && app.drag.valid == .None && app.assist_mode != .Off {
+			app.preview_live = rnd.preview_compute(&app.preview_scratch, &app.state.topology,
+				&app.state.flow, &app.cat,
+				pp.Cmd_Draw_Pipe{app.drag.from_node, app.drag_to, app.tier}, &app.preview)
+		} else {
+			app.preview_live = false
+		}
 		if rl.IsMouseButtonReleased(.LEFT) {
 			// commit if snapped to a legal target
 			if app.drag_to != 0 && app.drag.valid == .None {
@@ -313,6 +393,27 @@ handle_input :: proc(app: ^App) {
 						apply_tick = app.tick + 1,
 						kind = cmd,
 					})
+					// Job B: the R3 payoff + the graduation counter. The committed
+					// DAG (what-if over the committed topology) IS the post-commit
+					// winning path — copy it into the glow buffer (the live preview
+					// stays free for the next drag) and light it for glow_ticks.
+					// glow_gen is the POST-apply gen (== the clone's gen).
+					app.draws_since_nudge += 1
+					if app.preview_live && app.preview.ok {
+						rnd.preview_copy(&app.glow, &app.preview)
+						app.glow_until = app.tick + app.assist.glow_ticks
+						app.glow_gen = app.state.topology.gen
+					} else {
+						app.glow_until = 0
+					}
+					// the graduation nudge: after N successful draws in Full
+					// mode, ONE opt-in HUD line (never a modal, never forced;
+					// any T press latches nudge_done).
+					if app.assist_mode == .Full && !app.nudge_done &&
+						app.draws_since_nudge >= u32(app.assist.graduation_n) {
+						app.nudge_until = app.tick + app.assist.nudge_ticks
+						app.nudge_done = true
+					}
 				}
 			}
 			app.drag.active = false
@@ -324,6 +425,7 @@ handle_input :: proc(app: ^App) {
 		// cancels (above + the chip toggle). Never starts a link drag. A press
 		// that DRAGS past 6px is a no-op (not a place intent).
 		app.drag.active = true
+		app.preview_live = false // Job B: no routing preview in placement mode (a stale draw preview must not linger)
 		app.drag.placing = app.placing
 		app.drag.wx = wx
 		app.drag.wy = wy
@@ -626,16 +728,38 @@ draw_hud :: proc(app: ^App) {
 		}
 	}
 
-	// the cost readout on the drag ghost
+	// the cost readout on the drag ghost. Job B: in Full mode with a live
+	// route preview, the render draws the ONE route number instead (never two
+	// numbers at the cursor); Glow_Only shows no numbers at all; Off keeps the
+	// pre-Job-B readout.
 	if app.drag.active && app.drag_to != 0 {
-		cur := rnd.to_screen(&app.view, app.drag.wx, app.drag.wy)
-		if app.drag.valid == .None {
+		if app.drag.valid != .None {
+			draw_text(app, reject_label(app.drag.valid), 12, 76, 16, rl.Color{200, 60, 60, 255})
+		} else if app.assist_mode == .Off || (app.assist_mode == .Full && !(app.preview_live && app.preview.ok)) {
+			cur := rnd.to_screen(&app.view, app.drag.wx, app.drag.wy)
 			label := fmt.tprintf("cost %d", app.drag.cost)
 			draw_text(app, label, i32(cur.x)+12, i32(cur.y)-14, 16, p.ink)
-		} else {
-			draw_text(app, reject_label(app.drag.valid), 12, 76, 16, rl.Color{200, 60, 60, 255})
 		}
 	}
+
+	// Job B: the assist tier indicator (bottom-right — clear of the centered
+	// tray + the bottom-left SLA block) + the graduation nudge (ONE opt-in
+	// HUD line after N successful draws, never a modal, never forced; any T
+	// press dismisses it). ASCII only (the draw_text byte-truncation gate).
+	mode_label := "assist: full (T cycles)"
+	switch app.assist_mode {
+	case .Full:
+		mode_label = "assist: full (T cycles)"
+	case .Glow_Only:
+		mode_label = "assist: glow-only (T cycles)"
+	case .Off:
+		mode_label = "assist: off (T cycles)"
+	}
+	draw_text(app, mode_label, WIN_W - 320, WIN_H - 24, 14, p.ink_soft)
+	if app.nudge_until > 0 && app.tick <= app.nudge_until {
+		nudge := fmt.tprintf("tip: you've drawn %d pipes - press T for glow-only assist", app.draws_since_nudge)
+		draw_text(app, nudge, WIN_W - 320, WIN_H - 44, 14, p.state_strain)
+	}
 }
 
 // percent — the lane proportion readout: a lane's share of the allocated
diff --git a/app/render/assist.odin b/app/render/assist.odin
new file mode 100644
index 0000000..23f121e
--- /dev/null
+++ b/app/render/assist.odin
@@ -0,0 +1,471 @@
+package render
+
+// assist.odin — the Job-B readability package (canon 2026-08-13, R2a/R3/T2):
+// the live cost-sum flow preview while drawing + the assist graduation tiers +
+// the post-draw route glow + the equal-cost tie cue. STRICT ODN-12: everything
+// here is VIEW-ONLY — it reads the topology + flow + tier costs and NEVER
+// mutates sim state (the what-if table is built on an app-owned scratch CLONE
+// and discarded; nothing here feeds Run_State, so determinism is untouched by
+// construction — the harness T1/T2 goldens cannot see this package at all).
+//
+// R2a semantics: while the player drags a candidate pipe, the preview answers
+// "what path will the packets take if I commit this?" with a what-if routing
+// table: the LIVE topology is cloned, the candidate applied, and the SAME
+// public pure `core.routing_rebuild` the sim uses recomputes the table — so
+// the previewed paths are exactly the paths the sim WILL take after the draw
+// commits (the harness `preview-check` verb proves this end-to-end). The
+// FIRST live packet (spawn order) whose equal-cost DAG from its current node
+// to its dst contains the candidate edge AND reaches dst wins; the glow shows
+// the packet's FULL winning DAG (every tight edge — at an ECMP split BOTH
+// branches glow + the split node is marked "equal cost - split by hash", T2),
+// and the readout is ONE number (the path total — shared by every DAG path by
+// the ECMP invariant), never a candidate spreadsheet.
+
+import "core:encoding/json"
+import "core:fmt"
+import pp "../../core"
+import rl "vendor:raylib"
+
+// Assist_Mode — the R2a graduation tiers (canon: full assist DEFAULT for
+// beginners → glow-only → off for pros; T cycles in the app). Full = the
+// winning-path glow + the ONE number ("route N"); Glow_Only = glow + tie
+// cues, no numbers; Off = no routing visuals at all (pre-Job-B behavior).
+Assist_Mode :: enum u8 {
+	Full,
+	Glow_Only,
+	Off,
+}
+
+// Assist_Config — the data-driven assist tunables (data/assist.json, ODN-5).
+// COSMETIC-CLASS config: like palette.json it is loaded by the app/render
+// layer and NEVER folded into catalog_hash — balance.json folds every byte
+// into cat.hash, so a field addition there would re-bless ALL blessed goldens
+// (the golden-stability rule; same comment as PLACEMENT_MIN_SEP_TILES in
+// core/topology.odin). When the balance catalog next legitimately re-blesses,
+// this block can move there.
+Assist_Config :: struct {
+	default_mode:  Assist_Mode, // the tier at run start (full — beginners)
+	graduation_n:  i32,         // the graduation nudge fires after N successful draws (opt-in, never forced)
+	glow_ticks:    u64,         // R3 post-draw glow dwell @ logic_hz (120 = 6 s at 20 Hz)
+	nudge_ticks:   u64,         // the nudge HUD dwell
+}
+
+DEFAULT_ASSIST_JSON :: #load("../../data/assist.json")
+
+// assist_config_load — parse the cosmetic assist config; any parse problem
+// falls back to the inline defaults (palette pattern — the config is
+// view-only; a bad file must not brick the run, and must never touch the
+// catalog hash).
+assist_config_load :: proc(source: []byte = DEFAULT_ASSIST_JSON) -> Assist_Config {
+	c := default_assist_config()
+	v, err := json.parse(source, parse_integers = true)
+	if err != nil {
+		return c
+	}
+	obj, ok := v.(json.Object)
+	if !ok {
+		return c
+	}
+	switch ajstr(obj, "default_mode") {
+	case "glow_only":
+		c.default_mode = .Glow_Only
+	case "off":
+		c.default_mode = .Off
+	case:
+		c.default_mode = .Full
+	}
+	if n, okn := obj["graduation_n"].(json.Integer); okn && n > 0 {
+		c.graduation_n = i32(n)
+	}
+	if g, okg := obj["glow_ticks"].(json.Integer); okg && g >= 0 {
+		c.glow_ticks = u64(g)
+	}
+	if t, okt := obj["nudge_ticks"].(json.Integer); okt && t >= 0 {
+		c.nudge_ticks = u64(t)
+	}
+	return c
+}
+
+default_assist_config :: proc() -> Assist_Config {
+	return Assist_Config{default_mode = .Full, graduation_n = 8, glow_ticks = 120, nudge_ticks = 120}
+}
+
+// ajstr — the render-local JSON string accessor (palette.odin has only the
+// color accessors; core's jstr is not importable).
+ajstr :: proc(o: json.Object, key: string) -> string {
+	if v, ok := o[key].(json.String); ok {
+		return v
+	}
+	return ""
+}
+
+// Dag_Edge — one tight edge of the preview DAG: the equal-cost hop u→v toward
+// the destination (edge cost = the bundle's min tier cost — the fattest live
+// member, matching routing_rebuild's edge pricing).
+Dag_Edge :: struct {
+	u, v: u32, // node ids
+	cost: i32, // min tier cost among live pipes between u and v
+}
+
+// Route_Preview — the preview_compute result: the DAG of ALL equal-cost paths
+// from the affected packet's current node to its dst (per the what-if table
+// with the candidate applied), the total cost (ONE number — every DAG path
+// shares it by the ECMP invariant), the T2 split nodes, the affected packet,
+// and the candidate's tier (the render sizes the pre-commit halo from it).
+// The app keeps TWO of these: the live drag preview AND the committed R3 glow
+// (preview_copy — a cancelled drag must never corrupt the committed glow).
+Route_Preview :: struct {
+	ok:          bool, // a complete route exists AND the candidate edge is on it
+	pkt_idx:     int,  // the first affected packet (flow.packets order)
+	packet_src:  u32,  // the packet's current routing node (node id)
+	packet_dst:  u32,  // the packet's destination
+	cost:        i32,  // the winning path's total cost (shared by all DAG paths)
+	edges:       [dynamic]Dag_Edge, // tight edges (node ids), walk order
+	split_nodes: [dynamic]u32,      // nodes with >= 2 DAG children (T2 tie cue)
+	cand_tier:   u16,               // the candidate pipe's tier (render halo sizing)
+}
+
+// Preview_Scratch — the app-owned what-if buffers (persistent across frames —
+// cleared + reused, no per-frame allocation in the sim path; the app is
+// arena-free today, ODN-18 [LATER]). The clone is a faithful Topology copy
+// (every parallel array) + the candidate pipe applied; the what-if table is a
+// plain Routing_Table built by the PUBLIC pure routing_rebuild (called, never
+// modified — the Job-B scope guard is "no core changes", and calling a pure
+// public proc from the view is exactly the ODN-12 read contract).
+Preview_Scratch :: struct {
+	topo: pp.Topology,         // clone of the live topology + candidate
+	rt:   pp.Routing_Table,    // the what-if table over `topo`
+	seen: [dynamic]bool,       // DAG walk: visited slots
+	dist: [dynamic]i32,        // DAG walk: cost-so-far per slot (unique in the DAG)
+	queue: [dynamic]u32,       // DAG walk: slot BFS queue
+	alive: bool,               // buffers allocated (destroy guard)
+}
+
+preview_scratch_make :: proc(s: ^Preview_Scratch, allocator := context.allocator) {
+	context.allocator = allocator
+	pp.topology_make(&s.topo, allocator)
+	pp.routing_make(&s.rt, allocator)
+	s.seen = make([dynamic]bool, 0, 64, allocator)
+	s.dist = make([dynamic]i32, 0, 64, allocator)
+	s.queue = make([dynamic]u32, 0, 64, allocator)
+	s.alive = true
+}
+
+preview_scratch_destroy :: proc(s: ^Preview_Scratch) {
+	if !s.alive {
+		return
+	}
+	pp.topology_destroy(&s.topo)
+	pp.routing_destroy(&s.rt)
+	delete(s.seen)
+	delete(s.dist)
+	delete(s.queue)
+	s^ = {}
+}
+
+// preview_release — free a Route_Preview's owned arrays (the app/check call
+// this when the preview is replaced or the run ends; the DAG is run-scoped —
+// node ids recycle across runs, so a stale preview must never survive).
+preview_release :: proc(p: ^Route_Preview) {
+	delete(p.edges)
+	delete(p.split_nodes)
+	p^ = {}
+}
+
+// preview_copy — deep-copy `src` into `dst` (the committed R3 glow keeps its
+// own DAG so a later drag's preview can never corrupt it — the two-buffer
+// ownership split the review round demanded).
+preview_copy :: proc(dst: ^Route_Preview, src: ^Route_Preview) {
+	clear(&dst.edges)
+	clear(&dst.split_nodes)
+	for e in src.edges {
+		append(&dst.edges, e)
+	}
+	for s in src.split_nodes {
+		append(&dst.split_nodes, s)
+	}
+	dst.ok = src.ok
+	dst.pkt_idx = src.pkt_idx
+	dst.packet_src = src.packet_src
+	dst.packet_dst = src.packet_dst
+	dst.cost = src.cost
+	dst.cand_tier = src.cand_tier
+}
+
+// preview_clear — reset a Route_Preview for refill (keeps capacity).
+preview_clear :: proc(p: ^Route_Preview) {
+	clear(&p.edges)
+	clear(&p.split_nodes)
+	p.ok = false
+	p.pkt_idx = -1
+	p.packet_src = 0
+	p.packet_dst = 0
+	p.cost = 0
+}
+
+// topology_clone_into — faithful copy of every Topology array (the what-if
+// clone; resize + copy — deterministic, no per-frame allocation growth once
+// sized).
+topology_clone_into :: proc(dst: ^pp.Topology, src: ^pp.Topology) {
+	resize(&dst.node_alive, len(src.node_alive))
+	copy(dst.node_alive[:], src.node_alive[:])
+	resize(&dst.node_id, len(src.node_id))
+	copy(dst.node_id[:], src.node_id[:])
+	resize(&dst.node_kind, len(src.node_kind))
+	copy(dst.node_kind[:], src.node_kind[:])
+	resize(&dst.node_role, len(src.node_role))
+	copy(dst.node_role[:], src.node_role[:])
+	resize(&dst.node_type, len(src.node_type))
+	copy(dst.node_type[:], src.node_type[:])
+	resize(&dst.node_pos, len(src.node_pos))
+	copy(dst.node_pos[:], src.node_pos[:])
+	resize(&dst.pipe_alive, len(src.pipe_alive))
+	copy(dst.pipe_alive[:], src.pipe_alive[:])
+	resize(&dst.pipe_id, len(src.pipe_id))
+	copy(dst.pipe_id[:], src.pipe_id[:])
+	resize(&dst.pipe_a, len(src.pipe_a))
+	copy(dst.pipe_a[:], src.pipe_a[:])
+	resize(&dst.pipe_b, len(src.pipe_b))
+	copy(dst.pipe_b[:], src.pipe_b[:])
+	resize(&dst.pipe_tier, len(src.pipe_tier))
+	copy(dst.pipe_tier[:], src.pipe_tier[:])
+	resize(&dst.pipe_span, len(src.pipe_span))
+	copy(dst.pipe_span[:], src.pipe_span[:])
+	resize(&dst.pipe_weights, len(src.pipe_weights))
+	copy(dst.pipe_weights[:], src.pipe_weights[:])
+	resize(&dst.pipe_lane_over, len(src.pipe_lane_over))
+	copy(dst.pipe_lane_over[:], src.pipe_lane_over[:])
+	dst.next_node_id = src.next_node_id
+	dst.next_pipe_id = src.next_pipe_id
+	dst.gen = src.gen
+}
+
+// min_bundle_cost — the fattest-member edge cost between two node ids
+// (routing_rebuild's min semantics — the same scan the table's pass 1 uses,
+// so the DAG's edge costs price bundles identically to the sim).
+min_bundle_cost :: proc(t: ^pp.Topology, a, b: u32, cat: ^pp.Catalogs) -> i32 {
+	best := i32(1) << 30
+	for pi in 0..<len(t.pipe_alive) {
+		if !t.pipe_alive[pi] {
+			continue
+		}
+		if (t.pipe_a[pi] == a && t.pipe_b[pi] == b) || (t.pipe_a[pi] == b && t.pipe_b[pi] == a) {
+			c := cat.pipe_tiers[t.pipe_tier[pi]].cost
+			if c < best {
+				best = c
+			}
+		}
+	}
+	return best
+}
+
+// preview_compute — the R2a what-if (see the package header). `cand` is the
+// snapped, pre-validated candidate draw. Fills `out` (cleared first); returns
+// out.ok. The DAG walk is array-only + insertion-ordered (deterministic); the
+// candidate edge membership test covers both directions (packets may flow
+// either way through the drawn pipe).
+preview_compute :: proc(s: ^Preview_Scratch, topo: ^pp.Topology, flow: ^pp.Flow_State, cat: ^pp.Catalogs, cand: pp.Cmd_Draw_Pipe, out: ^Route_Preview) -> bool {
+	preview_clear(out)
+	if !s.alive {
+		preview_scratch_make(s)
+	}
+	// 1. the what-if topology: clone + candidate. The clone's gen == the live
+	// gen + 1 == the live gen AFTER the draw commits (apply bumps once) — the
+	// app stores this so the R3 glow validates against the committed topology.
+	topology_clone_into(&s.topo, topo)
+	if _, err := pp.topology_apply_edit(&s.topo, pp.Command{1, cand}, cat); err != .None {
+		return false // the candidate is illegal on the clone (app pre-validated; defensive)
+	}
+	// 2. the what-if table — the SAME pure rebuild the sim runs post-commit.
+	pp.routing_rebuild(&s.rt, &s.topo, cat)
+
+	// 3. first affected packet: the first live packet whose equal-cost DAG
+	// (current routing node -> dst) contains the candidate edge AND reaches
+	// dst. Spawn order = flow.packets order (deterministic).
+	for pkt_idx in 0..<len(flow.packets) {
+		p := &flow.packets[pkt_idx]
+		if p.delivered {
+			continue
+		}
+		start := p.at_node
+		if p.on_edge {
+			start = p.heading // the packet re-decides at its next junction (E29)
+		}
+		if start == p.dst {
+			continue // no onward routing decision (arriving / arrived)
+		}
+		if walk_dag(s, cat, start, p.dst, out) {
+			if dag_has_edge(out, cand.a, cand.b) {
+				out.ok = true
+				out.pkt_idx = pkt_idx
+				out.packet_src = start
+				out.packet_dst = p.dst
+				out.cand_tier = cand.tier
+				return true
+			}
+		}
+		// not this packet: the route is incomplete (partial DAG) OR the
+		// candidate is not on its paths — clear the partial edges before the
+		// next packet, or stale dead-end edges would pollute the winner's DAG
+		preview_clear(out)
+	}
+	return false
+}
+
+// walk_dag — BFS over the what-if table's hop sets from `start` toward `dst`:
+// every hop-set member of a visited node is a TIGHT edge (on some equal-cost
+// path — by the rebuild's own equality test), so the visited subgraph IS the
+// full DAG. Fills out.edges + out.split_nodes + out.cost (the cost-so-far at
+// dst — unique per node in the DAG). Returns true iff dst was reached.
+walk_dag :: proc(s: ^Preview_Scratch, cat: ^pp.Catalogs, start, dst: u32, out: ^Route_Preview) -> bool {
+	n := len(s.topo.node_alive)
+	resize(&s.seen, n)
+	resize(&s.dist, n)
+	for i in 0..<n {
+		s.seen[i] = false
+		s.dist[i] = 0
+	}
+	clear(&s.queue)
+	start_slot, ok := pp.node_slot(&s.topo, start)
+	if !ok {
+		return false
+	}
+	append(&s.queue, start_slot)
+	s.seen[start_slot] = true
+	s.dist[start_slot] = 0
+	head := 0
+	for head < len(s.queue) {
+		u := s.queue[head]
+		head += 1
+		u_id := s.topo.node_id[u]
+		offset, count, okl := pp.routing_equal_cost_hops(&s.rt, &s.topo, u_id, dst)
+		if !okl || count == 0 {
+			continue // no onward hops (a DAG leaf — dst has none by construction)
+		}
+		if count >= 2 {
+			append(&out.split_nodes, u_id) // T2: an ECMP branch point
+		}
+		for k in 0..<int(count) {
+			h := s.rt.hops[int(offset) + k]
+			v_id := h.node
+			v_slot, okv := pp.node_slot(&s.topo, v_id)
+			if !okv {
+				continue // defensive: the table is fresh, hop nodes are live
+			}
+			c := min_bundle_cost(&s.topo, u_id, v_id, cat)
+			append(&out.edges, Dag_Edge{u = u_id, v = v_id, cost = c})
+			if !s.seen[v_slot] {
+				s.seen[v_slot] = true
+				s.dist[v_slot] = s.dist[u] + c
+				append(&s.queue, v_slot)
+			}
+		}
+	}
+	dst_slot, oks := pp.node_slot(&s.topo, dst)
+	if !oks || !s.seen[dst_slot] {
+		return false // the route is incomplete — no complete path to predict
+	}
+	out.cost = s.dist[dst_slot]
+	return true
+}
+
+// dag_has_edge — does the DAG contain the (undirected) node pair?
+dag_has_edge :: proc(out: ^Route_Preview, a, b: u32) -> bool {
+	for e in out.edges {
+		if (e.u == a && e.v == b) || (e.u == b && e.v == a) {
+			return true
+		}
+	}
+	return false
+}
+
+// --- rendering ---------------------------------------------------------------
+
+// draw_route_glow — the shared R2a/R3 renderer: every DAG edge gets a
+// translucent route-colored halo OVER the pipes (pair → live bundle lookup
+// with a raw-line fallback — the candidate edge is not yet in the live bundle
+// view during a drag), every split node gets the T2 tie mark (a ring + the
+// rule caption — shape + color + text, never color alone), and in Full mode
+// the ONE number ("route N") draws near the cursor. Called ONLY by the app
+// (the harness capture path never invokes it — T2 goldens cannot shift).
+draw_route_glow :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, prev: ^Route_Preview, show_cost: bool, cursor: rl.Vector2) {
+	if !prev.ok {
+		return
+	}
+	p := v.palette
+	for e in prev.edges {
+		draw_glow_edge(v, topo, bundles, e.u, e.v, prev.cand_tier)
+	}
+	for sp in prev.split_nodes {
+		draw_tie_mark(v, topo, sp)
+	}
+	if show_cost {
+		label := fmt.aprintf("route %d", prev.cost, allocator = context.temp_allocator)
+		draw_text_c(v, label, i32(cursor.x) + 12, i32(cursor.y) - 14, 16, p.ink)
+	}
+}
+
+// draw_glow_edge — the halo for one DAG edge: the pair's live bundle if it
+// exists (the committed-edges case — width follows the bundle read), else a
+// raw halo line between the two node positions (the candidate edge pre-commit,
+// sized from the candidate's tier so the commit does not pop widths).
+draw_glow_edge :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, u, w: u32, cand_tier: u16) {
+	p := v.palette
+	col := p.route_glow
+	lo, hi := min(u, w), max(u, w)
+	if bi, ok := pp.bundles_slot_for_pair(bundles, lo, hi); ok {
+		sa, oka := pp.node_slot(topo, bundles.bundle_lo[bi])
+		sb, okb := pp.node_slot(topo, bundles.bundle_hi[bi])
+		if !oka || !okb {
+			return
+		}
+		a := node_screen(v, topo.node_pos[sa])
+		b := node_screen(v, topo.node_pos[sb])
+		width := (tier_pipe_width(v, bundles.bundle_tier[bi]) + f32(bundles.bundle_count[bi] - 1) * BUNDLE_EXTRA_WIDTH) * v.scale
+		halo := width + 6.0 * v.scale
+		rl.DrawLineEx(a, b, halo, col)
+		rl.DrawCircleV(a, halo * 0.5, col)
+		rl.DrawCircleV(b, halo * 0.5, col)
+		return
+	}
+	// the candidate edge (not yet a live bundle): a halo over the committed
+	// geometry (the snapped node pair, not the cursor), sized from the
+	// candidate's own tier width so the commit frame does not pop.
+	sa, oka := pp.node_slot(topo, u)
+	sb, okb := pp.node_slot(topo, w)
+	if !oka || !okb {
+		return
+	}
+	a := node_screen(v, topo.node_pos[sa])
+	b := node_screen(v, topo.node_pos[sb])
+	width := tier_pipe_width(v, cand_tier) * v.scale
+	halo := width + 6.0 * v.scale
+	rl.DrawLineEx(a, b, halo, col)
+	rl.DrawCircleV(a, halo * 0.5, col)
+	rl.DrawCircleV(b, halo * 0.5, col)
+}
+
+// draw_tie_mark — the T2 equal-cost cue at a split node: a warm ring around
+// the node + the rule caption ("equal cost - split by hash" — ASCII, gate 6;
+// a split never looks random: both branches glow and the node names the rule).
+draw_tie_mark :: proc(v: ^View, topo: ^pp.Topology, node_id: u32) {
+	p := v.palette
+	slot, ok := pp.node_slot(topo, node_id)
+	if !ok {
+		return
+	}
+	c := node_screen(v, topo.node_pos[slot])
+	s := v.tile_px * v.scale
+	col := p.route_tie
+	r := s * 0.62
+	th := 2.5 * v.scale
+	for k in 0..<i32(th) {
+		rl.DrawCircleLinesV(c, r - f32(k) * v.scale, col)
+	}
+	caption := "equal cost - split by hash"
+	fs := i32(max(11, s * 0.30))
+	cw := i32(len(caption)) * fs / 2
+	x := i32(c.x) - cw / 2
+	y := i32(c.y - r - s * 0.36) - fs / 2
+	draw_text_c(v, caption, x, y, fs, p.ink)
+}
diff --git a/app/render/palette.odin b/app/render/palette.odin
index c0f5a98..7babf6b 100644
--- a/app/render/palette.odin
+++ b/app/render/palette.odin
@@ -45,6 +45,10 @@ Palette :: struct {
 	// readout alongside position + stroke width. Per-mille of the true
 	// along-edge fraction (1000 = full speed, 0 = frozen). Cosmetic only.
 	lane_speeds: [3]i32, // [Express, Standard, Best-effort]
+	// Job B (readability package): the route-glow + tie-cue colors (R2a/R3/T2,
+	// canon 2026-08-13). Cosmetic only, like the rest of the palette.
+	route_glow: rl.Color, // the winning-path halo (translucent green)
+	route_tie:  rl.Color, // the equal-cost split-node mark (warm amber)
 }
 
 DEFAULT_PALETTE_JSON :: #load("../../data/palette.json")
@@ -118,6 +122,8 @@ palette_load :: proc(source: []byte = DEFAULT_PALETTE_JSON) -> Palette {
 	} else {
 		p.lane_speeds = {1000, 850, 700}
 	}
+	p.route_glow = jcol(obj, "route_glow", {86, 180, 110, 110})
+	p.route_tie = jcol(obj, "route_tie", {242, 181, 68, 235})
 	return p
 }
 
@@ -151,6 +157,8 @@ fallback_palette :: proc() -> Palette {
 	p.state_strain = {242, 181, 68, 255}
 	p.state_critical = {232, 69, 69, 255}
 	p.lane_speeds = {1000, 850, 700}
+	p.route_glow = {86, 180, 110, 110}
+	p.route_tie = {242, 181, 68, 235}
 	return p
 }
 
diff --git a/data/assist.json b/data/assist.json
new file mode 100644
index 0000000..7323667
--- /dev/null
+++ b/data/assist.json
@@ -0,0 +1,7 @@
+{
+  "_comment": "Assist catalog (Job B readability package, canon 2026-08-13 R2a/R3/T2 — ODN-5). COSMETIC-CLASS config: like palette.json it is loaded by the app layer and NEVER folded into catalog_hash — balance.json folds every byte into cat.hash, so a field addition there would re-bless ALL blessed goldens (see the PLACEMENT_MIN_SEP_TILES comment in core/topology.odin; when the balance catalog next legitimately re-blesses, this block can move there). default_mode = the R2a assist tier at run start (full for beginners; T cycles full -> glow-only -> off). graduation_n = the post-N-successful-draws graduation nudge (opt-in, NEVER forced; the nudge is a HUD line, no modal). glow_ticks = the R3 post-draw winning-path glow dwell @ logic_hz (120 = 6 s at 20 Hz). nudge_ticks = the nudge HUD dwell.",
+  "default_mode": "full",
+  "graduation_n": 8,
+  "glow_ticks": 120,
+  "nudge_ticks": 120
+}
diff --git a/data/palette.json b/data/palette.json
index 7f9d7f3..063baf0 100644
--- a/data/palette.json
+++ b/data/palette.json
@@ -28,5 +28,7 @@
   "lane_standard": [108, 122, 142, 255],
   "lane_best_effort": [88, 152, 108, 255],
   "lane_speeds":   [1000, 850, 700],
-  "sel_halo":      [232, 181, 68, 90]
+  "sel_halo":      [232, 181, 68, 90],
+  "route_glow":    [86, 180, 110, 110],
+  "route_tie":     [242, 181, 68, 235]
 }
diff --git a/harness/assist_check.odin b/harness/assist_check.odin
new file mode 100644
index 0000000..b082fbd
--- /dev/null
+++ b/harness/assist_check.odin
@@ -0,0 +1,478 @@
+package main
+
+// assist_check.odin — the Job-B launchable cross-check (spec acceptance: "the
+// preview path CROSS-CHECKED against actual sim routing"). It drives the
+// PRODUCTION preview helper (rnd.preview_compute — the exact code the app
+// calls during a drag) against the real sim and proves the previewed path
+// matches what the sim ACTUALLY does once the candidate draw commits:
+//
+//   (a) the preview DAG edge set + total cost + split nodes must equal the
+//       tight-edge DAG walked from the SIM's rebuilt routing table (the same
+//       data the flow forwards on) after the candidate is applied + stepped;
+//   (b) the affected packet's ACTUAL hash-picked path (ecmp_pick over the
+//       rebuilt table) must be a subset of the preview DAG;
+//   (c) the no-route negative: a candidate that completes no route yields
+//       ok=false (no preview, no number).
+//
+// Scenarios (mixed tiers — the 20/10/5 capacity-cost ladder):
+//   S1 fixture route — the app's playable loop: a packet waits at res until
+//      the second draw completes res->router->host (cost 10+10 = 20).
+//   S2 fat-path shift — a wide 0->1->3 (5+5 = 10) beats the narrow 0->2->3
+//      (20+20 = 40): the preview must show ONLY the fat path (the narrow legs
+//      are the negative pin) and the sim must take it.
+//   S3 true different-tier tie — standard(10)+wide(5) vs wide(5)+standard(10)
+//      = 15 == 15: BOTH paths in the DAG, split node marked (T2), and the
+//      packet's hash-picked path rides one of them.
+//   S4 dead-end negative — a candidate that completes no route: ok=false.
+//
+// The check never mutates the sim beyond the candidate apply + one step (the
+// same path the app's edit fast-path uses) — it is a read-only consumer of
+// the preview helper, exactly like the app.
+
+import "core:fmt"
+import pp "../core"
+import rnd "../app/render"
+
+// sim_dag — walk the SIM's routing table (the flow's own forwarding data)
+// from `start` toward `dst`: every hop-set member of a visited node is a
+// tight edge. Returns the normalized (lo, hi) edge pairs, the split nodes,
+// and the total cost (the cost-so-far at dst). This is the sim truth the
+// preview must match.
+sim_dag :: proc(t: ^pp.Topology, r: ^pp.Routing_Table, cat: ^pp.Catalogs, start, dst: u32) -> (edges: [dynamic]rnd.Dag_Edge, splits: [dynamic]u32, cost: i32, ok: bool) {
+	n := len(t.node_alive)
+	seen := make([]bool, n, context.temp_allocator)
+	dist := make([]i32, n, context.temp_allocator)
+	queue := make([dynamic]u32, context.temp_allocator)
+	defer delete(queue)
+	start_slot, oks := pp.node_slot(t, start)
+	if !oks {
+		return
+	}
+	append(&queue, start_slot)
+	seen[start_slot] = true
+	head := 0
+	for head < len(queue) {
+		u := queue[head]
+		head += 1
+		u_id := t.node_id[u]
+		offset, count, okl := pp.routing_equal_cost_hops(r, t, u_id, dst)
+		if !okl || count == 0 {
+			continue
+		}
+		if count >= 2 {
+			append(&splits, u_id)
+		}
+		for k in 0..<int(count) {
+			h := r.hops[int(offset) + k]
+			v_id := h.node
+			v_slot, okv := pp.node_slot(t, v_id)
+			if !okv {
+				continue
+			}
+			c := check_min_cost(t, u_id, v_id, cat)
+			append(&edges, rnd.Dag_Edge{u = u_id, v = v_id, cost = c})
+			if !seen[v_slot] {
+				seen[v_slot] = true
+				dist[v_slot] = dist[u] + c
+				append(&queue, v_slot)
+			}
+		}
+	}
+	dst_slot, okd := pp.node_slot(t, dst)
+	if !okd || !seen[dst_slot] {
+		return
+	}
+	cost = dist[dst_slot]
+	ok = true
+	return
+}
+
+// check_min_cost — the bundle's fattest-member edge cost (the same min
+// semantics as the routing rebuild + the preview helper).
+check_min_cost :: proc(t: ^pp.Topology, a, b: u32, cat: ^pp.Catalogs) -> i32 {
+	best := i32(1) << 30
+	for pi in 0..<len(t.pipe_alive) {
+		if !t.pipe_alive[pi] {
+			continue
+		}
+		if (t.pipe_a[pi] == a && t.pipe_b[pi] == b) || (t.pipe_a[pi] == b && t.pipe_b[pi] == a) {
+			c := cat.pipe_tiers[t.pipe_tier[pi]].cost
+			if c < best {
+				best = c
+			}
+		}
+	}
+	return best
+}
+
+// packet_path_matches — the affected packet's ACTUAL path: from its current
+// routing node toward its dst, the flow's own hash pick at every junction
+// (ecmp_pick — the real forwarding decision). Every FUTURE hop must be in the
+// preview DAG and the walk must reach dst. (The packet's CURRENT mid-edge leg
+// is the already-made junction decision — the preview only predicts future
+// decisions, so that first leg is exempt by design.)
+packet_path_matches :: proc(t: ^pp.Topology, r: ^pp.Routing_Table, p: ^pp.Packet, prev: ^rnd.Route_Preview) -> bool {
+	cur := p.at_node
+	if p.on_edge {
+		cur = p.heading
+	}
+	guard := 0
+	for cur != p.dst {
+		if guard > len(t.node_alive) {
+			return false // cycle guard — bounded by the graph size (dist strictly decreases, never happens)
+		}
+		guard += 1
+		offset, count, ok := pp.routing_equal_cost_hops(r, t, cur, p.dst)
+		if !ok || count == 0 {
+			return false // no route — the packet would wait
+		}
+		pick := pp.ecmp_pick(p.src, p.dst, u8(p.class), p.id, count)
+		hop := r.hops[int(offset) + int(pick)]
+		if !prev_has_edge(prev, cur, hop.node) {
+			return false // the actual hop is NOT on the previewed path — divergence
+		}
+		cur = hop.node
+	}
+	return true
+}
+
+prev_has_edge :: proc(prev: ^rnd.Route_Preview, a, b: u32) -> bool {
+	for e in prev.edges {
+		if (e.u == a && e.v == b) || (e.u == b && e.v == a) {
+			return true
+		}
+	}
+	return false
+}
+
+// edges_match — set equality: the preview's DAG edges (normalized to the
+// undirected (lo, hi) pair — both directions of a drawn pipe are the same
+// bundle) against the expected pair list.
+edges_match :: proc(actual: [dynamic]rnd.Dag_Edge, expected: [][2]u32) -> bool {
+	if len(actual) != len(expected) {
+		return false
+	}
+	for e in expected {
+		found := false
+		for a in actual {
+			pair := [2]u32{min(a.u, a.v), max(a.u, a.v)}
+			if pair == e {
+				found = true
+				break
+			}
+		}
+		if !found {
+			return false
+		}
+	}
+	return true
+}
+
+splits_match :: proc(actual: [dynamic]u32, expected: []u32) -> bool {
+	if len(actual) != len(expected) {
+		return false
+	}
+	for s in expected {
+		found := false
+		for a in actual {
+			if a == s {
+				found = true
+				break
+			}
+		}
+		if !found {
+			return false
+		}
+	}
+	return true
+}
+
+// run_assist_check — the scenarios; returns 0 when all green.
+run_assist_check :: proc(cat: ^pp.Catalogs) -> i32 {
+	std, oks := pp.pipe_tier_index(cat, "standard")
+	wide, okw := pp.pipe_tier_index(cat, "wide")
+	narrow, okn := pp.pipe_tier_index(cat, "narrow")
+	res, okr := pp.node_type_index(cat, "residential")
+	rt, okt := pp.node_type_index(cat, "router_basic")
+	host, okh := pp.node_type_index(cat, "content_host")
+	fails: [dynamic]string
+	defer delete(fails)
+	if !oks || !okw || !okn || !okr || !okt || !okh {
+		append(&fails, "preview-check: required catalog entries missing (tiers standard/wide/narrow, types residential/router_basic/content_host)")
+	}
+	if len(fails) > 0 {
+		for f in fails {
+			fmt.printf("  FAIL %s\n", f)
+		}
+		return 1
+	}
+
+	scratch: rnd.Preview_Scratch
+	defer rnd.preview_scratch_destroy(&scratch)
+	prev: rnd.Route_Preview
+	defer rnd.preview_release(&prev)
+
+	scenarios := 0
+
+	// --- S1: the fixture route (the app's playable loop) --------------------
+	{
+		state: pp.Run_State
+		pp.run_init(&state, 42, cat.hash, cat.balance.logic_hz)
+		defer pp.run_destroy(&state)
+		pp.topology_spawn_node(&state.topology, res, {8, 15}, cat)  // 0
+		pp.topology_spawn_node(&state.topology, rt, {20, 15}, cat)   // 1
+		pp.topology_spawn_node(&state.topology, host, {32, 15}, cat) // 2
+		pp.topology_apply_edit(&state.topology, pp.Command{1, pp.Cmd_Draw_Pipe{0, 1, std}}, cat) // fast-path
+		pp.flow_seed_demand(&state.flow, 1, 0, 2)
+		for tick in u64(1)..=5 {
+			pp.step(&state, tick, {}, cat) // the packet waits at res — no route to host
+		}
+		cand := pp.Cmd_Draw_Pipe{1, 2, std}
+		got := rnd.preview_compute(&scratch, &state.topology, &state.flow, cat, cand, &prev)
+		if !got || !prev.ok {
+			append(&fails, fmt.aprintf("S1: expected a preview, got ok=%v", got))
+		} else if prev.cost != 20 {
+			append(&fails, fmt.aprintf("S1: preview cost %d, want 20", prev.cost))
+		} else if !edges_match(prev.edges, {{0, 1}, {1, 2}}) {
+			append(&fails, fmt.aprintf("S1: preview edges %v, want {0-1,1-2}", prev.edges))
+		} else if len(prev.split_nodes) != 0 {
+			append(&fails, fmt.aprintf("S1: unexpected split nodes %v", prev.split_nodes))
+		} else {
+			// the cross-check: commit the candidate + step -> the sim's table
+			pp.topology_apply_edit(&state.topology, pp.Command{1, cand}, cat)
+			pp.step(&state, 6, {}, cat)
+			sim_edges, sim_splits, sim_cost, sim_ok := sim_dag(&state.topology, &state.routing, cat, prev.packet_src, prev.packet_dst)
+			if !sim_ok || sim_cost != prev.cost || !edges_match(sim_edges, {{0, 1}, {1, 2}}) || !splits_match(sim_splits, {}) {
+				append(&fails, fmt.aprintf("S1: sim table diverges from the preview (cost %d vs %d)", sim_cost, prev.cost))
+			} else if !packet_path_matches(&state.topology, &state.routing, &state.flow.packets[prev.pkt_idx], &prev) {
+				append(&fails, "S1: the packet's actual path is not on the previewed DAG")
+			}
+		}
+		scenarios += 1
+	}
+
+	// --- S2: the fat-path preference (wide wins over a REACHABLE narrow rival)
+	// Pre-draw the wide first leg + the narrow first leg (0-2); the narrow
+	// second leg (2-3) is drawn at the CROSS-CHECK step, so at preview time
+	// the packet waits at res (no route yet) AND the rival leg 0-2 exists in
+	// the graph. The cross-check then proves the tight-edge filter excludes
+	// the now-REACHABLE narrow rival (0-2-3 = 40 != 10) and the packet rides
+	// the fat path — the competition the spec's I/O matrix claims.
+	{
+		state: pp.Run_State
+		pp.run_init(&state, 42, cat.hash, cat.balance.logic_hz)
+		defer pp.run_destroy(&state)
+		pp.topology_spawn_node(&state.topology, res, {8, 15}, cat)  // 0
+		pp.topology_spawn_node(&state.topology, rt, {16, 11}, cat)   // 1 (m1, upper)
+		pp.topology_spawn_node(&state.topology, rt, {16, 19}, cat)   // 2 (m2, lower)
+		pp.topology_spawn_node(&state.topology, host, {24, 15}, cat) // 3
+		pp.topology_apply_edit(&state.topology, pp.Command{1, pp.Cmd_Draw_Pipe{0, 1, wide}}, cat)
+		pp.topology_apply_edit(&state.topology, pp.Command{1, pp.Cmd_Draw_Pipe{0, 2, narrow}}, cat)
+		// no 2-3 and no 1-3 yet: the packet waits at res (host unreachable)
+		pp.flow_seed_demand(&state.flow, 1, 0, 3)
+		for tick in u64(1)..=5 {
+			pp.step(&state, tick, {}, cat)
+		}
+		cand := pp.Cmd_Draw_Pipe{1, 3, wide}
+		got := rnd.preview_compute(&scratch, &state.topology, &state.flow, cat, cand, &prev)
+		if !got || !prev.ok {
+			append(&fails, fmt.aprintf("S2: expected a preview, got ok=%v", got))
+		} else if prev.cost != 10 {
+			append(&fails, fmt.aprintf("S2: preview cost %d, want 10", prev.cost))
+		} else if !edges_match(prev.edges, {{0, 1}, {1, 3}}) {
+			append(&fails, fmt.aprintf("S2: preview edges %v, want {0-1,1-3} (the narrow 0-2 leg excluded)", prev.edges))
+		} else {
+			// the cross-check: commit the candidate AND the narrow second leg
+			// (2-3), then step -> the sim's table must still exclude the now-
+			// REACHABLE narrow rival (0-2-3 = 40, the fat path = 10) and the
+			// packet must ride the fat path.
+			pp.topology_apply_edit(&state.topology, pp.Command{1, cand}, cat)
+			pp.topology_apply_edit(&state.topology, pp.Command{1, pp.Cmd_Draw_Pipe{2, 3, narrow}}, cat)
+			pp.step(&state, 6, {}, cat)
+			sim_edges, sim_splits, sim_cost, sim_ok := sim_dag(&state.topology, &state.routing, cat, prev.packet_src, prev.packet_dst)
+			if !sim_ok || sim_cost != prev.cost || !edges_match(sim_edges, {{0, 1}, {1, 3}}) || !splits_match(sim_splits, {}) {
+				append(&fails, fmt.aprintf("S2: sim table diverges from the preview (cost %d vs %d) — the reachable narrow rival must lose", sim_cost, prev.cost))
+			} else if !packet_path_matches(&state.topology, &state.routing, &state.flow.packets[prev.pkt_idx], &prev) {
+				append(&fails, "S2: the packet's actual path is not on the previewed DAG")
+			}
+		}
+		scenarios += 1
+	}
+
+	// --- S3: the true different-tier tie (15 == 15; the T2 split cue) --------
+	// The tie junction is DOWNSTREAM (id 1): the packet is observed in the
+	// between-ticks arrival window — it completes the 0->1 edge at the end of
+	// tick 3 and sits at 1 until tick 4's forward (std transit = 2 ticks:
+	// forward t1, consume t2-t3). Pre-draw only the upper branch
+	// (1->2->4 = 10+5 = 15); the candidate 1->3 wide completes the lower
+	// branch (5+10 = 15) — a TRUE different-tier tie at node 1.
+	{
+		state: pp.Run_State
+		pp.run_init(&state, 42, cat.hash, cat.balance.logic_hz)
+		defer pp.run_destroy(&state)
+		pp.topology_spawn_node(&state.topology, res, {32, 15}, cat)  // 0
+		pp.topology_spawn_node(&state.topology, rt, {40, 11}, cat)   // 1 (the tie junction)
+		pp.topology_spawn_node(&state.topology, rt, {44, 8}, cat)    // 2 (ra, upper)
+		pp.topology_spawn_node(&state.topology, rt, {44, 22}, cat)   // 3 (rb, lower)
+		pp.topology_spawn_node(&state.topology, host, {48, 15}, cat) // 4
+		pp.topology_apply_edit(&state.topology, pp.Command{1, pp.Cmd_Draw_Pipe{0, 1, std}}, cat)
+		pp.topology_apply_edit(&state.topology, pp.Command{1, pp.Cmd_Draw_Pipe{1, 2, std}}, cat)
+		pp.topology_apply_edit(&state.topology, pp.Command{1, pp.Cmd_Draw_Pipe{2, 4, wide}}, cat)
+		pp.topology_apply_edit(&state.topology, pp.Command{1, pp.Cmd_Draw_Pipe{3, 4, std}}, cat) // the lower branch's second leg (completes with the candidate)
+		pp.flow_seed_demand(&state.flow, 1, 0, 4)
+		for tick in u64(1)..=3 {
+			pp.step(&state, tick, {}, cat) // tick 3 end: the packet has ARRIVED at 1
+		}
+		cand := pp.Cmd_Draw_Pipe{1, 3, wide}
+		got := rnd.preview_compute(&scratch, &state.topology, &state.flow, cat, cand, &prev)
+		if !got || !prev.ok {
+			append(&fails, fmt.aprintf("S3: expected a preview, got ok=%v", got))
+		} else if prev.cost != 15 {
+			append(&fails, fmt.aprintf("S3: preview cost %d, want 15", prev.cost))
+		} else if !edges_match(prev.edges, {{1, 2}, {2, 4}, {1, 3}, {3, 4}}) {
+			append(&fails, fmt.aprintf("S3: preview edges %v, want both tied paths", prev.edges))
+		} else if !splits_match(prev.split_nodes, {1}) {
+			append(&fails, fmt.aprintf("S3: split nodes %v, want {1} (the T2 tie cue)", prev.split_nodes))
+		} else {
+			pp.topology_apply_edit(&state.topology, pp.Command{1, cand}, cat)
+			pp.step(&state, 4, {}, cat)
+			sim_edges, sim_splits, sim_cost, sim_ok := sim_dag(&state.topology, &state.routing, cat, prev.packet_src, prev.packet_dst)
+			if !sim_ok || sim_cost != prev.cost || !edges_match(sim_edges, {{1, 2}, {2, 4}, {1, 3}, {3, 4}}) || !splits_match(sim_splits, {1}) {
+				append(&fails, fmt.aprintf("S3: sim table diverges from the preview (cost %d vs %d)", sim_cost, prev.cost))
+			} else if !packet_path_matches(&state.topology, &state.routing, &state.flow.packets[prev.pkt_idx], &prev) {
+				append(&fails, "S3: the packet's actual hash-picked path is not on the previewed DAG")
+			}
+		}
+		scenarios += 1
+	}
+
+	// --- S4: the dead-end negative (no complete route -> no preview) --------
+	{
+		state: pp.Run_State
+		pp.run_init(&state, 42, cat.hash, cat.balance.logic_hz)
+		defer pp.run_destroy(&state)
+		pp.topology_spawn_node(&state.topology, res, {5, 15}, cat)   // 0
+		pp.topology_spawn_node(&state.topology, rt, {15, 15}, cat)   // 1
+		pp.topology_spawn_node(&state.topology, rt, {25, 15}, cat)   // 2 (dead end)
+		pp.topology_spawn_node(&state.topology, host, {35, 15}, cat) // 3
+		pp.topology_apply_edit(&state.topology, pp.Command{1, pp.Cmd_Draw_Pipe{0, 1, std}}, cat)
+		pp.flow_seed_demand(&state.flow, 1, 0, 3)
+		for tick in u64(1)..=5 {
+			pp.step(&state, tick, {}, cat)
+		}
+		cand := pp.Cmd_Draw_Pipe{1, 2, std}
+		got := rnd.preview_compute(&scratch, &state.topology, &state.flow, cat, cand, &prev)
+		if got || prev.ok {
+			append(&fails, "S4: expected NO preview for a dead-end candidate (route incomplete)")
+		}
+		scenarios += 1
+	}
+
+	// --- S5: a mid-flight packet's preview starts at its NEXT junction -------
+	// The packet is ON an edge when the candidate is dragged; its remaining
+	// routing decisions start at the heading node (E29). A candidate that only
+	// helps UPSTREAM of the packet's position must NOT fire the preview (the
+	// packet will never take it); the same topology with the packet at the
+	// junction does fire (S3 covers the junction case).
+	{
+		state: pp.Run_State
+		pp.run_init(&state, 42, cat.hash, cat.balance.logic_hz)
+		defer pp.run_destroy(&state)
+		pp.topology_spawn_node(&state.topology, res, {32, 15}, cat)  // 0
+		pp.topology_spawn_node(&state.topology, rt, {40, 11}, cat)   // 1 (the junction)
+		pp.topology_spawn_node(&state.topology, rt, {44, 8}, cat)    // 2 (ra, upper)
+		pp.topology_spawn_node(&state.topology, rt, {44, 22}, cat)   // 3 (rb, lower)
+		pp.topology_spawn_node(&state.topology, host, {48, 15}, cat) // 4
+		pp.topology_apply_edit(&state.topology, pp.Command{1, pp.Cmd_Draw_Pipe{0, 1, std}}, cat)
+		pp.topology_apply_edit(&state.topology, pp.Command{1, pp.Cmd_Draw_Pipe{1, 2, std}}, cat)
+		pp.topology_apply_edit(&state.topology, pp.Command{1, pp.Cmd_Draw_Pipe{2, 4, wide}}, cat)
+		pp.flow_seed_demand(&state.flow, 1, 0, 4)
+		pp.step(&state, 1, {}, cat) // end of tick 1: the packet is MID-EDGE on 0->1 (std, 2 ticks)
+		cand := pp.Cmd_Draw_Pipe{1, 3, wide} // helps only packets still UPSTREAM
+		got := rnd.preview_compute(&scratch, &state.topology, &state.flow, cat, cand, &prev)
+		if got || prev.ok {
+			append(&fails, "S5: expected NO preview for a mid-flight packet (its next junction does not reach the candidate)")
+		}
+		scenarios += 1
+	}
+
+	// --- S6: the first-packet-skip loop (an earlier unroutable packet loses) -
+	// Packet A (0->5) waits at a dead-end res; packet B (2->5) waits at res2
+	// whose route the candidate completes. The preview must skip A (its DAG
+	// never reaches the dst) and pick B — and the winner's DAG must contain NO
+	// stale edges from A's walk.
+	{
+		state: pp.Run_State
+		pp.run_init(&state, 42, cat.hash, cat.balance.logic_hz)
+		defer pp.run_destroy(&state)
+		pp.topology_spawn_node(&state.topology, res, {5, 15}, cat)   // 0 (dead-end res A)
+		pp.topology_spawn_node(&state.topology, rt, {15, 15}, cat)   // 1 (A's dead-end router)
+		pp.topology_spawn_node(&state.topology, res, {32, 15}, cat)  // 2 (res B)
+		pp.topology_spawn_node(&state.topology, rt, {40, 15}, cat)   // 3 (B's router)
+		pp.topology_spawn_node(&state.topology, host, {48, 15}, cat) // 4
+		pp.topology_apply_edit(&state.topology, pp.Command{1, pp.Cmd_Draw_Pipe{0, 1, std}}, cat)
+		pp.topology_apply_edit(&state.topology, pp.Command{1, pp.Cmd_Draw_Pipe{2, 3, std}}, cat)
+		pp.flow_seed_demand(&state.flow, 1, 0, 4) // A: waits (dead end)
+		pp.flow_seed_demand(&state.flow, 1, 2, 4) // B: waits (3->4 missing)
+		for tick in u64(1)..=5 {
+			pp.step(&state, tick, {}, cat)
+		}
+		cand := pp.Cmd_Draw_Pipe{3, 4, std}
+		got := rnd.preview_compute(&scratch, &state.topology, &state.flow, cat, cand, &prev)
+		if !got || !prev.ok {
+			append(&fails, fmt.aprintf("S6: expected a preview, got ok=%v", got))
+		} else if prev.pkt_idx != 1 {
+			append(&fails, fmt.aprintf("S6: affected packet %d, want 1 (packet B — A is unroutable and must be skipped)", prev.pkt_idx))
+		} else if prev.cost != 20 {
+			append(&fails, fmt.aprintf("S6: preview cost %d, want 20", prev.cost))
+		} else if !edges_match(prev.edges, {{2, 3}, {3, 4}}) {
+			append(&fails, fmt.aprintf("S6: preview edges %v, want {2-3,3-4} (no stale edges from packet A's walk)", prev.edges))
+		} else {
+			pp.topology_apply_edit(&state.topology, pp.Command{1, cand}, cat)
+			pp.step(&state, 6, {}, cat)
+			sim_edges, sim_splits, sim_cost, sim_ok := sim_dag(&state.topology, &state.routing, cat, prev.packet_src, prev.packet_dst)
+			if !sim_ok || sim_cost != prev.cost || !edges_match(sim_edges, {{2, 3}, {3, 4}}) || !splits_match(sim_splits, {}) {
+				append(&fails, fmt.aprintf("S6: sim table diverges from the preview (cost %d vs %d)", sim_cost, prev.cost))
+			} else if !packet_path_matches(&state.topology, &state.routing, &state.flow.packets[prev.pkt_idx], &prev) {
+				append(&fails, "S6: the packet's actual path is not on the previewed DAG")
+			}
+		}
+		scenarios += 1
+	}
+
+	// --- S7: a parallel-pipe candidate into an existing bundle -----------------
+	// Drawing a SECOND pipe between a connected pair fattens the bundle but
+	// the min tier cost is unchanged — a routing NO-OP. With the packet at the
+	// downstream junction (arrived end of tick 2), the pair (0-1) is UPSTREAM
+	// of its remaining DAG: the preview must NOT fire (the packet will never
+	// take the new pipe, and no other packet is affected) — no glow, no route
+	// number for a no-op draw.
+	{
+		state: pp.Run_State
+		pp.run_init(&state, 42, cat.hash, cat.balance.logic_hz)
+		defer pp.run_destroy(&state)
+		pp.topology_spawn_node(&state.topology, res, {8, 15}, cat)  // 0
+		pp.topology_spawn_node(&state.topology, rt, {16, 11}, cat)   // 1
+		pp.topology_spawn_node(&state.topology, host, {24, 15}, cat) // 3
+		pp.topology_apply_edit(&state.topology, pp.Command{1, pp.Cmd_Draw_Pipe{0, 1, wide}}, cat)
+		pp.topology_apply_edit(&state.topology, pp.Command{1, pp.Cmd_Draw_Pipe{1, 3, wide}}, cat)
+		pp.flow_seed_demand(&state.flow, 1, 0, 3)
+		pp.step(&state, 1, {}, cat) // tick 1: forward onto 0-1 (wide = 1 tick)
+		pp.step(&state, 2, {}, cat) // tick 2 end: arrives at 1
+		cand := pp.Cmd_Draw_Pipe{0, 1, std} // a SECOND pipe on the existing bundle (routing no-op)
+		got := rnd.preview_compute(&scratch, &state.topology, &state.flow, cat, cand, &prev)
+		if got || prev.ok {
+			append(&fails, "S7: expected NO preview for a parallel-pipe routing no-op (the pair is upstream of the packet's remaining DAG)")
+		}
+		scenarios += 1
+	}
+
+	if len(fails) > 0 {
+		for f in fails {
+			fmt.printf("  FAIL %s\n", f)
+		}
+		return 1
+	}
+	fmt.printf("assist preview-check: %d scenario(s) green (preview == sim routing)\n", scenarios)
+	return 0
+}
diff --git a/harness/main.odin b/harness/main.odin
index 4009e5f..623c02c 100644
--- a/harness/main.odin
+++ b/harness/main.odin
@@ -5,12 +5,15 @@ package main
 // it links the SAME package core + the SAME render package as the game, inits
 // the rlsw software renderer headless (no GPU/display), and exercises T1 state
 // hashes, the replay gate, T2 pixel goldens, and the W1 drift negative test.
+// Job B adds `preview-check`: the R2a what-if preview must equal the sim's
+// own routing once the candidate draw commits (assist_check.odin).
 //
 // Usage:
 //   odin run harness -- run [demo...]           T1 + replay gate + T2; non-zero on failure
 //   odin run harness -- save [demo...]          re-bless goldens (deliberate; PR-reviewed)
 //   odin run harness -- replay <demo> <log.bin> re-run from an action log; manifest must match
 //   odin run harness -- drift-check             W1: deliberately-drifted logs must be REJECTED
+//   odin run harness -- preview-check           Job B: the R2a preview == sim routing cross-check
 
 import "core:fmt"
 import "core:os"
@@ -49,6 +52,16 @@ main :: proc() {
 		pp.catalogs_destroy(&cat)
 		os.exit(int(code))
 	}
+	if verb == "preview-check" {
+		cat: pp.Catalogs
+		if e := load_catalogs(&cat); e != "" {
+			fmt.eprintfln("preview-check: %s", e)
+			os.exit(2)
+		}
+		code := run_assist_check(&cat)
+		pp.catalogs_destroy(&cat)
+		os.exit(int(code))
+	}
 	if verb != "run" && verb != "save" {
 		usage()
 	}
@@ -113,7 +126,7 @@ main :: proc() {
 }
 
 usage :: proc() {
-	fmt.eprintln("usage: harness run|save [demo...] | replay <demo> <log.bin> | drift-check")
+	fmt.eprintln("usage: harness run|save [demo...] | replay <demo> <log.bin> | drift-check | preview-check")
 	os.exit(2)
 }
 

--- END DIFF ---

## The PR (scope)
Job B (readability package, app layer) on PR #40, targets `v2`. R2a live cost-sum flow preview while drawing (the draw ghost shows the path packets WILL take per the cost-aware routing table + the best path's total cost — ONE number or the delta, never a spreadsheet) + assist graduation tiers (full assist sum+glow DEFAULT -> partial glow-only -> off; settings toggle T; graduation nudge after N successful draws, N data-driven via data/assist.json, opt-in never forced); R3 post-draw route glow (the winning path lights up for glow_ticks); T2 equal-cost tie cue (BOTH tied paths marked "equal cost - split by hash"). STRICT view-only (ODN-12): reads the routing table + tier costs, NEVER feeds sim state, NO core changes. New files: app/render/assist.odin + data/assist.json + harness/assist_check.odin; additive palette keys; app/main.odin wiring. The harness `preview-check` verb (7 scenarios) cross-checks the preview against the sim's own routing.

## ⚠️ CRITICAL lens-guards — READ BEFORE FILING ANYTHING (prevents false positives)
- 🚨 LOAD-BEARING — STRICT VIEW-ONLY (ODN-12). The assist reads the routing table + tier costs and NEVER feeds sim state; NO core changes in this PR (verify: core/ untouched in the diff; a core modification = a blocker). The preview must show what the routing table WILL do — the preview path is CROSS-CHECKED against actual sim routing (the minion claims a preview-check harness, 7/7 — verify it exists and compares real vs previewed). The what-if table lives on an app-owned scratch CLONE; calling the public pure pp.routing_rebuild + pp.routing_equal_cost_hops from the app is ALLOWED (read contract), never modifying them.
- 🚨 LOCKED — do NOT flag as defects: Job A's Dijkstra model + the splice-proof re-bless (settled); `ecmp_pick`/`ecmp_hash` (pure identity hash — the tie-break is LOCKED, the visual cue rides beside it); the derived-not-serialized table; static costs; Job C's forecast panel (C owns app/render/forecast.odin — do NOT demand it here); per-class routing preferences (full-game, out of scope); no win/lose (4.3's job).
- THE FOUR ACCEPTANCE SURFACES: (1) R2a live preview: ONE number or the delta (never a candidate spreadsheet) + the draw ghost shows the cost-aware path; (2) assist graduation tiers: full/glow-only/off toggle (T) + the data-driven nudge (opt-in, NEVER forced — no modal); (3) R3 post-draw glow: the winning path lights up after a commit; (4) T2 tie cue: BOTH tied paths marked on ECMP (a split never looks random). Each surface must actually function (a toggle that doesn't toggle or a glow that never renders = a real defect).
- GOLDEN-DISCIPLINE: goldens byte-identical claim (the minion: harness 16/16 + goldens byte-identical) — verify; ANY golden shift = a finding (the assist is cosmetic and must not touch the capture path).
- ODN-5: data/assist.json additive + validated (a malformed config must fall back, not break the app). NOTE: the briefing said "N in balance.json"; the minion deliberately put N in the NEW cosmetic-class data/assist.json instead (balance.json folds into catalog_hash -> a field addition would re-bless ALL goldens, violating the golden-stability rule) — the spec documents this deviation and flags it for the human. Do NOT block on the deviation itself; DO flag any validation gap (malformed JSON bricking the app).
- Scope guard: Job B ONLY (app layer) — NOT C's forecast panel, NOT 4.3, NO new player commands (LOG_VERSION stays 3 — verify). app/main.odin is shared-risk with C (C is a SEPARATE open PR; review THIS diff at the sha).
- BASE = v2 (Job A + 4.2 merged — 69fc2e5). Em-dashes are OK in PP. ASCII-only string literals in render/app (lint gate 6 — the tie caption uses a hyphen, never an em-dash).

## Legitimate findings here WOULD be
- A view-only violation: assist/render code that mutates Run_State/Flow/Topology in place (the scratch clone is the only legal mutation target), a core/ change in the diff, or an app code path that changes sim behavior (e.g. a preview that allocates into live state, a glow read that races the step).
- Preview divergence from sim routing: the preview DAG/cost computed differently from what routing_rebuild + the flow's real forward pass would do (wrong first-affected-packet semantics vs flow.packets order, wrong on-edge starting node vs the E29 re-decision, wrong edge cost vs the table's min-bundle pricing, a candidate-edge membership test that ignores direction, stale partial DAG edges leaking between candidate packets).
- A broken surface: the R3 glow never rendering after commit (gen/tick gate mismatch — glow_gen captured pre-apply, the gate `tick <= glow_until && gen == glow_gen` can never be true), the T toggle not cycling or not dismissing the nudge, the nudge firing repeatedly/modal/forced, a tie cue that never draws on a real ECMP split or draws on a false split (a parallel-pipe bundle is NOT a split — the table dedupes per neighbor node), the route number showing alongside the cost readout (never two numbers).
- A golden shift: any goldens/*.t1 or *.log.bin or PNG differing from baseline 69fc2e5, or the harness capture path invoking the new draw procs.
- A config-validation gap: assist.json with negative/zero graduation_n, malformed JSON, or a wrong default_mode string bricking the app instead of falling back to inline defaults.
- A determinism/perf concern in the hot path: per-frame topology clone + full routing_rebuild every frame during a drag on a large map (assess the scale), a non-deterministic walk (map iteration), an allocation leak (preview buffers never released across runs).
- An acceptance-matrix miss: e.g. "no packet affected -> no glow, no number" not honored, the dead-end negative not covered, LOG_VERSION bumped or a new command added.

## YOUR LENS
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, zero packets, no route, zero counts, max sizes), the live-drag vs committed-glow buffer interaction (cancel mid-drag, commit then re-drag, restart mid-glow), unhandled error paths in new code (JSON parse failures, node ids recycled across runs, a packet delivered mid-drag), off-by-one errors (tick/gate boundaries, glow expiry), state the new code doesn't account for (terminal run, no packets spawned yet, a dropped packet in the flow array), input the new code doesn't validate (config values).

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

## OUTPUT CONTRACT (follow exactly)
Write ONLY a valid JSON array to your output file: /Users/moses/code/_bmad-output/perkins/packet-plumber-routing-readability-assist/r1/edge.json
No prose, no markdown fencing, no preamble, no trailing commentary. `[]` is valid and expected when you find nothing — do NOT invent findings to fill a quota.
Each element MUST match this schema exactly:
{
  "source": "edge",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. view-only, preview-divergence, glow-lifecycle, tie-cue, golden-shift, config-validation, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the EXACT lines you READ from the file/diff that prove the claim, pasted verbatim. 'N/A' ONLY for findings with no possible code reference. Do not paraphrase; do not reconstruct from memory. If you cannot quote the lines, you have not done the work — drop the finding.>",
  "detail": "<why this is a problem, <=40 words; for acceptance findings quote the violated spec phrase>",
  "recommended_fix": "<the change to apply, <=40 words>"
}


ACCURACY MANDATE — the most important instruction: NO claim you make will be taken at face value. Every finding will be independently re-verified against the actual worktree before it reaches the report. Findings whose `evidence` cannot be located verbatim, or whose claim contradicts the code, are DISCARDED SILENTLY — no defense, no second chance. Therefore: OPEN the file, READ the cited lines. Quote them verbatim in `evidence`. Hedging ("might", "could", "possibly") signals you have NOT verified — either verify and report crisply, or drop it. Prefer fewer well-grounded findings over many speculative ones. An empty array is an honest, fine answer.