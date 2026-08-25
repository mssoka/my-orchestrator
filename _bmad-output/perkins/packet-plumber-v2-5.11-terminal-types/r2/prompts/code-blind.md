You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

This chunk contains ALL code, data, demo-fixture and documentation changes of the PR (every non-goldens file).

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)

BLINDNESS RULE: this prompt and the diff embedded below are your ONLY permitted input. Do NOT read any other file, do NOT list directories, do NOT inspect any repository or run exploratory commands — reading anything beyond this prompt invalidates your lens. Your ONLY permitted tool use is writing your output file named below.

--- DIFF ---
diff --git a/_bmad-output/planning-artifacts/sprints/stories-v2.md b/_bmad-output/planning-artifacts/sprints/stories-v2.md
index f5097e1..4a94fae 100644
--- a/_bmad-output/planning-artifacts/sprints/stories-v2.md
+++ b/_bmad-output/planning-artifacts/sprints/stories-v2.md
@@ -810,6 +810,11 @@ one fresh minion, dispatched in order 5.9 → 5.12 (the invariant first, the pay
   alone. **Golden:** T1/T2 re-bless + a T2 frame with all three types visible.
 - **Launchable increment:** run the app — homes trickle, campuses flood; the terminal roster reads
   as a spectrum.
+- **Status:** implemented 2026-08-18 — PR open (the class analogues wired: `Terminal_Role` gains
+  `Small_Biz`/`Campus` (`core/catalog.odin:22`) + `role_from_name`; `node_types.json` gains the
+  per-type profile entries (throughput/demand_weight/era) + the era-3 demand entries sourcing from
+  them; the #65 sprites wired per role in the render (never color alone `[E9.1]`); the all-three-types
+  T2 golden (`terminal_types.dem`); the slice's deliberate T1/T2 re-bless, fold-proofed + byte-verified).
 
 ### Story 5.12 — Aggregation groups (congestion lives at the shared uplink)
 
diff --git a/_bmad-output/pr-bodies/5.11.md b/_bmad-output/pr-bodies/5.11.md
new file mode 100644
index 0000000..2f3b529
--- /dev/null
+++ b/_bmad-output/pr-bodies/5.11.md
@@ -0,0 +1,58 @@
+## Story 5.11 — Diverse terminal types (schools, offices, homes)
+
+The terminal roster gains its class analogues — **residential / small-biz / campus** — each with a different, bounded demand profile. A campus emits far more than a home; the roster reads as a spectrum. Slice 5B (E3.1/E2.1), systems: catalogs `[ODN-5]`, director `[ODN-7]`, growth (5.1 type pick).
+
+### The code touch points (the card's named list — a new terminal role is a CODE change)
+
+1. **`Terminal_Role` enum** (`core/catalog.odin:22`) — gains `Small_Biz` + `Campus`, **appended after the original pair** so the serialized role bytes (0/1/2) stay stable (the enum VALUE is a T1-visible byte, ODN-11).
+2. **`role_from_name`** (`core/catalog.odin`) — resolves `"small_biz"` / `"campus"` at catalog load.
+3. **`collect_terminals` role selector** (`core/flow.odin`) — role-generic by construction; the same scan now resolves the new roles (commented + pinned by `test_terminal_class_profiles`'s selector assertions).
+4. **The growth type-pick** (`core/growth.odin`) — `growth_terminal_roster` consumes the new types via the existing era-gated, TERMINAL-only, demand_weight-weighted draw (routers remain player-placed; every spawn E31-valid + 5.6-separated).
+5. **The #65 sprite wiring** (`app/render/sprites.odin`, `app/render/view.odin`) — role → sprite index + footprint: residential → house, small_biz → the small_biz sprite, campus → the campus sprite; the pre-sprite fallback also draws distinct primitive shapes (E9.1 even without the sheet).
+
+### The catalog roster (`data/node_types.json` `[ODN-5]` — appended at the END so existing type indices stay stable)
+
+Per-type profile = `throughput_units` (the cap input) + `demand_weight` (the volume attractor); the per-terminal cap is computed **uniformly** by the 5.9 accumulator: `cap = cap_fraction_permille × throughput ÷ packet_bandwidth` (500 permille, bandwidth 30).
+
+| type | era | throughput | accrue (milli/tick) | cap (pkts/tick) | burst ceiling | demand_weight |
+|---|---|---|---|---|---|---|
+| residential | 1 | 5 u/s | 83 | 0.083 | 1 (none) | 1 |
+| small_biz | 2 | 20 u/s | 333 | 0.333 (4× a home) | 1 (none) | 2 |
+| content_host | 3 | 80 u/s | 1333 | 1.333 | 2 | 1 |
+| **campus** | 3 | 150 u/s | 2500 | **2.5 (30× a home)** | 3 | 4 |
+
+Era gating: small_biz unlocks at era 2, campus at era 3 — `growth_terminal_roster` spawns the era-unlocked subset (era 3 = the full spectrum), pinned by `test_growth_era_gating`.
+
+### Bounded, distinct demand (`data/demand.json` — era 3 entries, `[ODN-7]`)
+
+- `email` from **small_biz** → residential, volume 1 (offices email; bounded by their 0.333 cap)
+- `streaming` from **campus** → residential, volume 1 (campuses flood; bounded by their 2.5 cap — the ×10 surge lands on campuses too, the honest aggregation event)
+- Entries whose role has **no live terminal spawn nothing and draw no rng** — every pre-5.11 fixture is untouched by construction (verified: all 32 existing `.log.bin` files differ from HEAD **only** in the 8-byte catalog_hash header field).
+- `test_terminal_class_profiles` pins the spectrum: campus fully served (≈window), campus > 10× home in volume, every terminal inside `cap×W + burst`, credit ≤ MAX, and the typed selectors never pick outside their role.
+
+### Readable without color `[E9.1]` — the all-three-types T2 golden
+
+New `demos/terminal_types.dem` (era 3, growth on, fixture + one small_biz + one campus): captures at 5000 ms and 30000 ms show the three classes as **distinct sprites** (house / office / campus — the #65 canon set, never re-rendered). Growth-born small_biz/campus join organically, each spawn E31-valid + min-separated (`test_growth_e31_validity` extended: 20 windows, both new types present + valid).
+
+### The deliberate re-bless (the slice's cause chain — 4.3 discipline)
+
+The catalog fold (`node_types.json` + `demand.json` change the folded bytes):
+
+- **Fold:** `66c4324a06058860 → 250679b1940fb87b`.
+- **Fold-only proof (boot):** the new tick-1 state dump under the new code, with the OLD hash spliced at the fold position (bytes 33..40), FNV-hashes to the OLD golden tick-1 **exactly** (`6c24e9cec592aece`); the un-spliced dump hashes to the blessed tick-1 (`ab1fb0d04a90026c`). The era-0/no-demand shift is the fold alone.
+- **Logs:** all **32 existing `.log.bin`** byte-verified — they differ from HEAD ONLY in the 8-byte catalog_hash header field (bytes 17-24). (The new `terminal_types.log.bin` joins the set.)
+- **T2 partition:** pixels moved **only** in `node_health` (10000 ms / 20000 ms) — the era-3 growth now spawns the new terminal classes + the era-3 demand sources from them (behavioral, cause-documented); the 50 ms frame (pre-growth) and **every other demo's frames are byte-identical** (the fold does not shift pixels).
+- **W9 re-pin** (`test_w9_surge_lands_under_caps`): the 5.9 surge-lands pin now counts the **streaming-capable crowd** (content_hosts + campuses, the 5.11 roster's honest evolution) with **per-type** burst ceilings + envelopes (the crowd floor 8, MIN_LAND, credit/rate bounds all re-verified from the sim). Input-parity manifests re-saved (the same fold).
+
+### Verification
+
+- `tools/ci-local.sh --mac`: **10/10 gates green** (lint, 193 core tests, app build, golden harness ×33 demos + replay gate, palcheck, W1 drift-rejection 233/233 mutations, preview cross-check, PP_DEBUG builds, stats replay-identity, input parity 24/24).
+- Story card status line updated in `stories-v2.md` (the established pattern).
+
+### Decisions & rationale
+
+- **Role/type index stability:** both the enum and the `node_types.json` array **append** the new entries. An earlier mid-list JSON insert shifted `content_host`/`router_basic`'s serialized type indices (T1-visible bytes) — caught by the fold-only proof and fixed; the final fold is pure.
+- **Profiles:** small_biz 20 u/s (4× a home, cap 0.333 — a middle rung with no burst, same latency discipline as homes), campus 150 u/s (the spec's cited example: cap 2.5 pkts/tick, ceiling 3 — the flood site).
+- **Era picks:** small_biz at era 2 (the office class arrives mid-progression), campus at era 3 (the streaming era). Eras 1/2 demand is deliberately UNCHANGED (dormant in the MVP — the era-FSM story owns their re-tune).
+- **`dc` sprite left unwired** — no catalog type maps to it; a future data-center role is its own story (flagged, never re-rendered canon).
+- **No 5.12 scope:** no group bias, no QoS/balance changes beyond the per-type profile data, no new sprites.
diff --git a/app/render/sprites.odin b/app/render/sprites.odin
index b42dee1..3ffec7b 100644
--- a/app/render/sprites.odin
+++ b/app/render/sprites.odin
@@ -129,13 +129,17 @@ sprites_parse_boxes :: proc(sh: ^Sprite_Sheet) -> bool {
 	return true
 }
 
-// sprite_index_building — the sprite index for a terminal: the house variant
-// (id % 4) or the host. The dc + story-5.11 (small_biz, campus) sprites exist
-// in the sheet for the roster's future; the two live terminal roles map to
-// house/host. (5.11 wires the new roles — story-owned, not here.)
+// sprite_index_building — the sprite index for a terminal role (5.11 wires
+// the story's class analogues): residential -> the house variant (id % 4),
+// content_host -> host (4), small_biz -> the small_biz sprite (9), campus ->
+// the campus sprite (10) — the #65 canon set, distinct shapes per type
+// (never color alone, E9.1). The dc sprite (5) stays unwired (no catalog
+// type maps to it yet — a future data-center role's job, not this story's).
 sprite_index_building :: proc(id: u32, role: pp.Terminal_Role) -> int {
-	if role == .Content_Host {
-		return 4
+#partial switch role {
+	case .Content_Host: return 4
+	case .Small_Biz:    return 9
+	case .Campus:       return 10
 	}
 	return int(id % 4)
 }
@@ -173,8 +177,12 @@ sprite_blit :: proc(sh: ^Sprite_Sheet, idx: int, c: rl.Vector2, target_w: f32) {
 }
 
 // sprite_target_w — the in-game footprint widths (tiles * tile_px * scale).
+// 5.11: the class analogues size by role — an office block reads bigger than
+// a house, a campus footprint reads biggest (the honest spectrum at a glance).
 sprite_house_target :: proc(v: ^View) -> f32 { return 1.50 * v.tile_px * v.scale }
 sprite_host_target :: proc(v: ^View) -> f32  { return 1.75 * v.tile_px * v.scale }
+sprite_small_biz_target :: proc(v: ^View) -> f32 { return 1.60 * v.tile_px * v.scale }
+sprite_campus_target :: proc(v: ^View) -> f32 { return 2.20 * v.tile_px * v.scale }
 sprite_puck_target :: proc(v: ^View, port_capacity: i32) -> f32 {
 	sh := v.sprites
 	idx := sprite_index_puck(port_capacity)
diff --git a/app/render/view.odin b/app/render/view.odin
index 5e93b0c..4422352 100644
--- a/app/render/view.odin
+++ b/app/render/view.odin
@@ -496,14 +496,19 @@ draw_health_ring :: proc(v: ^View, lvl: pp.Congestion_Level, node_id: u32, c: rl
 	draw_text_c(v, glyph, x, y, fs, col)
 }
 
-// residential = peaked-roof house (varied cheerful body); content_host = server
-// block with a play glyph (YouTune). Variant keyed by id so it's stable.
+// draw_building — the terminal sprite draw (7.1 pipeline). Role -> sprite
+// index + footprint (5.11: the class analogues — see sprite_index_building).
+// The fallback below is the pre-7.1 primitive path (belt-and-braces when the
+// sheet is missing) — it keeps a DISTINCT shape per role so E9.1 (never color
+// alone) holds even without the sprites.
 draw_building :: proc(v: ^View, id: u32, role: pp.Terminal_Role, c: rl.Vector2) {
 	if v.sprites.ok {
 		idx := sprite_index_building(id, role)
 		target := sprite_house_target(v)
-		if role == .Content_Host {
-			target = sprite_host_target(v)
+		#partial switch role {
+		case .Content_Host: target = sprite_host_target(v)
+		case .Small_Biz:    target = sprite_small_biz_target(v)
+		case .Campus:       target = sprite_campus_target(v)
 		}
 		sprite_blit(&v.sprites, idx, c, target)
 		return
@@ -534,6 +539,42 @@ draw_building :: proc(v: ^View, id: u32, role: pp.Terminal_Role, c: rl.Vector2)
 	h := s * 0.62
 	left := c.x - w/2
 	top := c.y - h * 0.15
+	if role == .Small_Biz || role == .Campus {
+		// 5.11 fallback: flat-roof blocks (office / campus) — a DISTINCT shape
+		// from the peaked-roof house (E9.1 even on the primitive path). Small
+		// biz = a square block with a window grid; campus = a wider block with
+		// a central tower.
+		ww := s * 1.1
+		hh := s * 0.6
+		if role == .Campus {
+			ww = s * 1.6
+			hh = s * 0.7
+		}
+		bx := c.x - ww/2
+		by := c.y - hh * 0.15
+		rl.DrawRectangleV({bx, by}, {ww, hh}, body)
+		// the window grid (2x2 for small biz, 3x2 for campus) — shape, not color
+		cols := 2
+		if role == .Campus {
+			cols = 3
+		}
+		win := ww * 0.16
+		gapx := (ww - f32(cols) * win) / f32(cols + 1)
+		gapy := hh * 0.14
+		for r in 0..<2 {
+			for cc in 0..<cols {
+				wx := bx + gapx + f32(cc) * (win + gapx)
+				wy := by + gapy + f32(r) * (hh*0.35 + gapy)
+				rl.DrawRectangleV({wx, wy}, {win, hh * 0.2}, roof)
+			}
+		}
+		if role == .Campus {
+			// the tower: a tall center block above the roof line
+			tw := ww * 0.22
+			rl.DrawRectangleV({c.x - tw/2, by - s * 0.28}, {tw, s * 0.28}, roof)
+		}
+		return
+	}
 	rl.DrawRectangleV({left, top}, {w, h}, body)
 	r1 := rl.Vector2{left - s * 0.06, top}
 	r2 := rl.Vector2{left + w + s * 0.06, top}
diff --git a/core/catalog.odin b/core/catalog.odin
index e7fd7fa..7efc55e 100644
--- a/core/catalog.odin
+++ b/core/catalog.odin
@@ -19,7 +19,13 @@ import "core:fmt"
 
 Node_Kind :: enum u8 { Terminal, Junction }
 
-Terminal_Role :: enum u8 { None, Residential, Content_Host }
+// Terminal_Role — the closed terminal-role enum (story 5.11 adds the class
+// analogues — a NEW role is a CODE change, Perkins r1 W7; catalog rows map
+// into it via role_from_name). Small_Biz + Campus are appended AFTER the
+// original pair so existing serialized role bytes (0/1/2) stay stable — the
+// enum VALUE is the T1-visible byte (ODN-11), adding at the end never shifts
+// an old golden.
+Terminal_Role :: enum u8 { None, Residential, Content_Host, Small_Biz, Campus }
 
 // --- catalog row types -------------------------------------------------------
 
@@ -1036,6 +1042,8 @@ role_from_name :: proc(name: string) -> Terminal_Role {
 	switch name {
 	case "residential":  return .Residential
 	case "content_host": return .Content_Host
+	case "small_biz":   return .Small_Biz
+	case "campus":      return .Campus
 	}
 	return .None
 }
diff --git a/core/demand_test.odin b/core/demand_test.odin
index dff2710..c1eab52 100644
--- a/core/demand_test.odin
+++ b/core/demand_test.odin
@@ -351,7 +351,9 @@ test_era0_legacy_no_rng_draws :: proc(t: ^testing.T) {
 // accrue = cap_fraction_permille × throughput ÷ packet_bandwidth (integer
 // milli-packets/tick); MAX_CREDIT_MILLI = 1000 × max(1, ceil(cap)) —
 // type-relative (r2 W4), residential ceiling 1 (NO burst), content_host
-// ceiling 2 (a ≤2/tick burst).
+// ceiling 2 (a ≤2/tick burst). 5.11: the class analogues join the table —
+// small_biz 333 (0.333/tick, 4× a home), campus 2500 (2.5/tick, 30× a home,
+// ceiling 3 — campuses flood).
 @(test)
 test_credit_accrue_and_max :: proc(t: ^testing.T) {
 	cat_storage: Catalogs
@@ -359,6 +361,8 @@ test_credit_accrue_and_max :: proc(t: ^testing.T) {
 	defer catalogs_destroy(cat)
 	res_idx, _ := node_type_index(cat, "residential")
 	host_idx, _ := node_type_index(cat, "content_host")
+	sb_idx, _ := node_type_index(cat, "small_biz")
+	camp_idx, _ := node_type_index(cat, "campus")
 
 	// residential: 500 × 5 ÷ 30 = 83 milli/tick (0.083 pkts/tick)
 	testing.expect_value(t, spawn_credit_accrue_milli(cat, res_idx), u32(83))
@@ -370,9 +374,21 @@ test_credit_accrue_and_max :: proc(t: ^testing.T) {
 	// MAX = 1000 × ceil(1333/1000) = 2000 — ceiling 2: burst ≤ 2/tick
 	testing.expect_value(t, spawn_credit_max_milli(cat, host_idx), u32(2000))
 
+	// 5.11: small_biz — 500 × 20 ÷ 30 = 333 milli/tick (0.333 pkts/tick,
+	// 4× a home); ceiling max(1, ceil(0.333)) = 1 → NO burst (like a home)
+	testing.expect_value(t, spawn_credit_accrue_milli(cat, sb_idx), u32(333))
+	testing.expect_value(t, spawn_credit_max_milli(cat, sb_idx), u32(1000))
+
+	// 5.11: campus — 500 × 150 ÷ 30 = 2500 milli/tick (2.5 pkts/tick, 30× a
+	// home); ceiling ceil(2.5) = 3 → a ≤3/tick burst (the flood site)
+	testing.expect_value(t, spawn_credit_accrue_milli(cat, camp_idx), u32(2500))
+	testing.expect_value(t, spawn_credit_max_milli(cat, camp_idx), u32(3000))
+
 	// the ceiling math is the spec's (accrue + 999) ÷ 1000, floored at 1
 	testing.expect_value(t, (u32(83) + 999) / 1000, u32(1))
+	testing.expect_value(t, (u32(333) + 999) / 1000, u32(1))
 	testing.expect_value(t, (u32(1333) + 999) / 1000, u32(2))
+	testing.expect_value(t, (u32(2500) + 999) / 1000, u32(3))
 
 	// a zero-throughput terminal (defensive) ceilings at 1
 	nt := &cat.node_types[res_idx]
@@ -381,6 +397,94 @@ test_credit_accrue_and_max :: proc(t: ^testing.T) {
 	testing.expect_value(t, spawn_credit_max_milli(cat, res_idx), u32(1000))
 }
 
+// 5.11 — the class-analogue profiles (spec-traffic-model Thread 4): each type
+// emits its OWN bounded profile — campus >> home in volume AND cap; the typed
+// source selectors resolve against the new roles (collect_terminals); the 5.9
+// accumulator applies uniformly (every terminal stays inside cap×W + burst,
+// credit <= MAX — the honest-traffic invariant holds for the new types too).
+// One terminal per role (the weighted pick is then deterministic — the pick's
+// rng draw picks the only candidate), so the per-role counts are the profile.
+@(test)
+test_terminal_class_profiles :: proc(t: ^testing.T) {
+	cat_storage: Catalogs
+	cat := test_catalog(&cat_storage)
+	defer catalogs_destroy(cat)
+	cat.balance.pool_max_packets = 100000 // the E22 backstop is not under test
+
+	s: Run_State
+	defer run_destroy(&s)
+	run_init(&s, 7, cat.hash, TEST_LOGIC_HZ)
+	s.era = 3 // the app's era — every 5.11 entry active
+
+	res_idx, _ := node_type_index(cat, "residential")
+	sb_idx, _ := node_type_index(cat, "small_biz")
+	camp_idx, _ := node_type_index(cat, "campus")
+	host_idx, _ := node_type_index(cat, "content_host")
+	topology_spawn_node(&s.topology, res_idx, {6, 15}, cat)   // res 0 — sink + email source
+	topology_spawn_node(&s.topology, sb_idx, {12, 15}, cat)   // small_biz 1 — email source
+	topology_spawn_node(&s.topology, res_idx, {18, 15}, cat)  // res 2 — the second sink (dst != src)
+	topology_spawn_node(&s.topology, camp_idx, {24, 15}, cat) // campus 3 — streaming source
+	topology_spawn_node(&s.topology, host_idx, {30, 15}, cat) // host 4 — streaming source
+
+	W :: u64(2000)
+	// per-role spawn counts: 0 residential, 1 small_biz, 2 content_host, 3 campus
+	per_role := [4]u64{}
+	per_terminal := make(map[u32]u64, 16)
+	defer delete(per_terminal)
+	selector_ok := true
+	credit_ok := true
+	envelope_ok := true
+	for tick in u64(1)..=W {
+		step(&s, tick, {}, cat)
+		for p in s.flow.packets {
+			if p.spawn_tick != tick { continue }
+			per_terminal[p.src] += 1
+			slot := node_slot_raw(&s.topology, p.src)
+			role := s.topology.node_role[slot]
+			#partial switch role {
+			case .Residential:  per_role[0] += 1
+			case .Small_Biz:    per_role[1] += 1
+			case .Content_Host: per_role[2] += 1
+			case .Campus:       per_role[3] += 1
+			}
+			// the typed selectors resolve against the new roles: email (0)
+			// sources are residential/small_biz ONLY, streaming (1) sources
+			// are content_host/campus ONLY — a role-typed spec can never pick
+			// a source outside its selector (collect_terminals contract).
+			if p.class == 0 && role != .Residential && role != .Small_Biz {
+				selector_ok = false
+			}
+			if p.class == 1 && role != .Content_Host && role != .Campus {
+				selector_ok = false
+			}
+		}
+	}
+	// the uniform accumulator: every terminal stays inside its own envelope
+	// (ceil_cap + W×accrue/1000) and credit <= MAX — the 5.9 invariant holds
+	// for the new types by the same mechanism (campus included: 2.5/tick cap).
+	for ns in 0..<len(s.topology.node_alive) {
+		if !s.topology.node_alive[ns] { continue }
+		if s.topology.node_kind[ns] != .Terminal { continue }
+		accrue := u64(spawn_credit_accrue_milli(cat, s.topology.node_type[ns]))
+		max_credit := u64(spawn_credit_max_milli(cat, s.topology.node_type[ns]))
+		if u64(s.flow.spawn_credit_milli[ns]) > max_credit { credit_ok = false }
+		ceil_cap := (accrue + 999) / 1000
+		bound := ceil_cap + accrue * W / 1000
+		if per_terminal[s.topology.node_id[ns]] > bound { envelope_ok = false }
+	}
+	testing.expect(t, selector_ok, "a role-typed demand spec must never source from a terminal outside its selector")
+	testing.expectf(t, per_role[3] >= W*9/10,
+		"campus must be fully served (the flood): sourced %d over %d ticks, want >= %d", per_role[3], W, W*9/10)
+	testing.expectf(t, per_role[3] > 10*per_role[0],
+		"campus >> home in volume: campus %d vs residential %d (want > 10x)", per_role[3], per_role[0])
+	testing.expectf(t, per_role[1] > per_role[0],
+		"small_biz emits more than a home: %d vs %d (cap 0.333 vs 0.083)", per_role[1], per_role[0])
+	testing.expectf(t, per_role[1] < per_role[3],
+		"campus emits more than small_biz (the spectrum reads): %d vs %d", per_role[3], per_role[1])
+	testing.expect(t, credit_ok, "every terminal's credit must stay <= MAX_CREDIT (uniform 5.9 accumulator)")
+	testing.expect(t, envelope_ok, "every terminal's window spawns must stay <= cap×W + burst (uniform 5.9 accumulator)")
+}
+
 // W9 — post-cap surge-lands (Perkins r1 W9 + r2 W6 pin): on a known seed,
 // era 3 + growth on + the streaming-surge window — the window's streaming
 // spawn count is >= the re-tuned expected volume × 0.95 (10/tick × the
@@ -431,32 +535,55 @@ test_w9_surge_lands_under_caps :: proc(t: ^testing.T) {
 			}
 		}
 		step(&s, tick, batch[:], cat)
-		// the in-window per-tick per-host burst ceiling (ceil_cap = 2)
+		// the in-window per-tick per-source burst ceiling — TYPE-RELATIVE
+		// (5.11: the streaming crowd is content_hosts + campuses; the ceiling
+		// is ceil(cap) per type — host 2, campus 3)
 		per_tick_host_burst := make(map[u32]u32, 16, context.temp_allocator)
 		for p in s.flow.packets {
 			if p.class == 1 && p.spawn_tick == tick {
 				stream_spawned += 1
-				per_tick_host_burst[p.src] += 1
-				per_host_spawns[p.src] += 1
+				if tick >= SURGE_START {
+					// the per-terminal envelope counts the SURGE WINDOW only (the W
+					// in the bound formula — the pre-surge base accrual is bounded
+					// by the same cap mechanism + the director caps pin above).
+					per_tick_host_burst[p.src] += 1
+					per_host_spawns[p.src] += 1
+				}
 			}
 		}
 		for src, n in per_tick_host_burst {
-			if n > 2 { burst_ok = false }
+			src_slot := node_slot_raw(&s.topology, src)
+			if int(src_slot) >= len(s.topology.node_alive) || !s.topology.node_alive[src_slot] {
+				continue
+			}
+			acc := u64(spawn_credit_accrue_milli(cat, s.topology.node_type[src_slot]))
+			ceil_cap := (acc + 999) / 1000
+			if u64(n) > ceil_cap {
+				burst_ok = false
+			}
 		}
 		delete(per_tick_host_burst)
 		free_all(context.temp_allocator)
 	}
-	// count the growth-born hosts + the seed fixture host
+	// count the streaming-capable crowd (growth-born + the seed fixture): the
+	// 5.11 roster gives BOTH content_hosts and campuses the streaming
+	// source_role, so the aggregation crowd is the union (W9's semantic — the
+	// surge spreads across every terminal that can source it).
 	for ns in 0..<len(s.topology.node_alive) {
 		if !s.topology.node_alive[ns] { continue }
-		if s.topology.node_kind[ns] == .Terminal && s.topology.node_role[ns] == .Content_Host {
-			hosts += 1
+		if s.topology.node_kind[ns] != .Terminal { continue }
+		if s.topology.node_role[ns] != .Content_Host && s.topology.node_role[ns] != .Campus {
+			continue
 		}
+		hosts += 1
 	}
-	// per-terminal window spawns + credit bounds (the W9 envelope)
+	// per-terminal window spawns + credit bounds (the W9 envelope) — checked
+	// for the streaming-capable crowd only, per-type bounds (5.11).
 	for ns in 0..<len(s.topology.node_alive) {
 		if !s.topology.node_alive[ns] { continue }
-		if s.topology.node_role[ns] != .Content_Host { continue }
+		if s.topology.node_role[ns] != .Content_Host && s.topology.node_role[ns] != .Campus {
+			continue
+		}
 		if int(s.topology.node_type[ns]) >= len(cat.node_types) { continue }
 		accrue := u64(spawn_credit_accrue_milli(cat, s.topology.node_type[ns]))
 		max_credit := u64(spawn_credit_max_milli(cat, s.topology.node_type[ns]))
@@ -466,7 +593,7 @@ test_w9_surge_lands_under_caps :: proc(t: ^testing.T) {
 		bound := ceil_cap + accrue * WINDOW / 1000
 		if per_host_spawns[s.topology.node_id[ns]] > bound { credit_ok = false }
 	}
-	testing.expectf(t, hosts >= 8, "growth must place >= 8 content_hosts by the surge window (got %d) — the aggregation crowd", hosts)
+	testing.expectf(t, hosts >= 8, "growth must place >= 8 streaming-capable terminals (content_hosts + campuses) by the surge window (got %d) — the aggregation crowd", hosts)
 	testing.expectf(t, stream_spawned >= MIN_LAND,
 		"W9 FAIL: the surge must LAND — streaming window spawns %d < %d (expected × 0.95); the capped map cannot source the surge", stream_spawned, MIN_LAND)
 	testing.expectf(t, burst_ok, "no per-tick burst beyond the ceiling (2 = ceil_cap) may occur")
diff --git a/core/determinism_test.odin b/core/determinism_test.odin
index 0a8b224..65dd56f 100644
--- a/core/determinism_test.odin
+++ b/core/determinism_test.odin
@@ -38,6 +38,13 @@ test_catalog :: proc(cat: ^Catalogs, allocator := context.allocator) -> ^Catalog
 	// auto-chips every junction kind; the port ceilings (8/16) enforce per tier.
 	append(&cat.node_types, Node_Type{id = "router_mid", display = "Mid Router", kind = .Junction, terminal_role = .None, throughput_units = 80, port_capacity = 8, era_introduced = 3})
 	append(&cat.node_types, Node_Type{id = "router_high", display = "High Router", kind = .Junction, terminal_role = .None, throughput_units = 160, port_capacity = 16, era_introduced = 3})
+	// 5.11: the class analogues (mirror data/node_types.json — the per-type
+	// profile is throughput_units + demand_weight; the cap derives uniformly
+	// via the 5.9 formula). Appended LAST so existing type indices 0..4 stay
+	// stable (node_type_index is order-based; a mid-list insert would shift
+	// serialized type bytes). small_biz = era 2, campus = era 3 (era gating).
+	append(&cat.node_types, Node_Type{id = "small_biz", display = "Small Business", kind = .Terminal, terminal_role = .Small_Biz, throughput_units = 20, port_capacity = 0, demand_weight = 2, era_introduced = 2})
+	append(&cat.node_types, Node_Type{id = "campus", display = "Campus", kind = .Terminal, terminal_role = .Campus, throughput_units = 150, port_capacity = 0, demand_weight = 4, era_introduced = 3})
 	cat.pipe_tiers = make([dynamic]Pipe_Tier, 0, 8, allocator)
 	append(&cat.pipe_tiers, Pipe_Tier{id = "narrow", display = "Narrow Copper", capacity_units = 10, cost = 20, clean_span = 8, max_span = 10, cost_per_tile = 5, era_introduced = 1})
 	append(&cat.pipe_tiers, Pipe_Tier{id = "standard", display = "Standard Line", capacity_units = 15, cost = 10, clean_span = 10, max_span = 14, cost_per_tile = 12, era_introduced = 1})
@@ -112,6 +119,13 @@ test_catalog :: proc(cat: ^Catalogs, allocator := context.allocator) -> ^Catalog
 			// (was 2 — the capped MVP cannot source 2/tick from one host at 500
 			// permille; the surge stays ×10 → 10/tick)
 			append(&e.entries, Demand_Entry{class = 1, source_role = .Content_Host, sink_role = .Residential, volume = 1, default_lane = 1, selection = .Weighted_Random, demand_weight = 1})
+			// 5.11: the era-3 entries for the class analogues (mirror
+			// demand.json) — email from small_biz, streaming from campus. They
+			// fire only where the new terminal roles exist (empty source sets
+			// skip with no rng draw — the pre-5.11 fixtures' streams are
+			// unchanged by construction).
+			append(&e.entries, Demand_Entry{class = 0, source_role = .Small_Biz, sink_role = .Residential, volume = 1, default_lane = 1, selection = .Weighted_Random, demand_weight = 1})
+			append(&e.entries, Demand_Entry{class = 1, source_role = .Campus, sink_role = .Residential, volume = 1, default_lane = 1, selection = .Weighted_Random, demand_weight = 1})
 			append(&e.set_pieces, Set_Piece{id = "streaming_surge", class = 1, multiplier = 10, start_tick = 1200, duration_ticks = 1800, forecast_lead_ticks = 600, archetype_idx = 0})
 		}
 		append(&cat.demand.eras, e)
diff --git a/core/flow.odin b/core/flow.odin
index 1a641a3..da15c6a 100644
--- a/core/flow.odin
+++ b/core/flow.odin
@@ -575,6 +575,9 @@ weighted_pick_excluding :: proc(rng: ^Rng, ids: []u32, weights: []i32, exclude:
 // its node_type) and its NODE SLOT (the 5.9 spawn-credit index — parallel to
 // the ids array). Scratch-allocated; the caller frees all three arrays.
 // Resolves a DemandSpec's typed source/sink selectors against the live topology.
+// 5.11: the selector is ROLE-GENERIC — the enum gains the class analogues
+// (Small_Biz, Campus) and the same scan resolves them (the era-3 demand
+// entries source from them; pinned by test_terminal_class_profiles).
 collect_terminals :: proc(t: ^Topology, cat: ^Catalogs, role: Terminal_Role,
                           alloc := context.temp_allocator) -> (ids: [dynamic]u32, weights: [dynamic]i32, slots: [dynamic]u32) {
 	ids = make([dynamic]u32, 0, 8, alloc)
diff --git a/core/growth_test.odin b/core/growth_test.odin
index 99d72c6..4b27afb 100644
--- a/core/growth_test.odin
+++ b/core/growth_test.odin
@@ -151,9 +151,11 @@ test_growth_e31_validity :: proc(t: ^testing.T) {
 	append(&s.action_log, Command{apply_tick = 20, kind = Cmd_Draw_Pipe{a = rt, b = 3, tier = std}})
 	append(&s.action_log, Command{apply_tick = 30, kind = Cmd_Draw_Pipe{a = res, b = rt, tier = std}})
 
-	run_growth(&s, 10*GROWTH_INTERVAL_TICKS, cat)
+	run_growth(&s, 20*GROWTH_INTERVAL_TICKS, cat)
 	span := growth_connect_span(cat, 3)
 	spawned := 0
+	has_small_biz := false
+	has_campus := false
 	for i in 0..<len(s.topology.node_alive) {
 		if !s.topology.node_alive[i] || s.topology.node_kind[i] != .Terminal {
 			continue
@@ -165,10 +167,17 @@ test_growth_e31_validity :: proc(t: ^testing.T) {
 			continue
 		}
 		spawned += 1
+		// 5.11: the class analogues join the era-3 roster — the E31 audit
+		// covers every spawn regardless of type (the separation floor 3 also
+		// clears the 5.6 router↔terminal floor 2 by construction).
+		if s.topology.node_role[i] == .Small_Biz { has_small_biz = true }
+		if s.topology.node_role[i] == .Campus { has_campus = true }
 		testing.expectf(t, e31_recheck(&s.topology, cat, u32(i), pos, span),
 			"growth spawn at %v violates E31 (bounds/separation/connectability) vs the final topology", pos)
 	}
-	testing.expectf(t, spawned > 0, "10 growth windows must spawn at least one terminal, got %d", spawned)
+	testing.expectf(t, spawned > 0, "20 growth windows must spawn at least one terminal, got %d", spawned)
+	testing.expectf(t, has_small_biz, "era-3 growth must spawn small_biz (the office class analogue)")
+	testing.expectf(t, has_campus, "era-3 growth must spawn campus (the campus class analogue)")
 	testing.expect(t, !s.replay_error, "growth run must not latch replay_error")
 }
 
@@ -252,7 +261,8 @@ test_growth_era_gating :: proc(t: ^testing.T) {
 	// era gates: growth_connect_span uses only era-unlocked tiers (era 1 ->
 	// standard 14; era 3 -> wide 18; era 0 -> 0 = no growth), and the spawn
 	// roster holds only era-unlocked TERMINALS (era 1 -> residential only;
-	// era 3 -> residential + content_host).
+	// 5.11: era 2 adds small_biz; era 3 adds content_host + campus — the
+	// class analogues arrive with their eras).
 	cat_storage: Catalogs
 	cat := test_catalog(&cat_storage)
 	defer catalogs_destroy(cat)
@@ -260,6 +270,7 @@ test_growth_era_gating :: proc(t: ^testing.T) {
 	testing.expectf(t, growth_connect_span(cat, 1) == 14, "era 1 must unlock the standard span 14, got %d", growth_connect_span(cat, 1))
 	testing.expectf(t, growth_connect_span(cat, 3) == 18, "era 3 must unlock the wide span 18, got %d", growth_connect_span(cat, 3))
 
+	// era 1: residential only
 	r1, w1 := growth_terminal_roster(cat, 1)
 	defer {
 		delete(r1)
@@ -270,12 +281,32 @@ test_growth_era_gating :: proc(t: ^testing.T) {
 		testing.expectf(t, cat.node_types[ti].kind == .Terminal, "growth roster must never hold a junction kind (routers are player-placed)")
 		testing.expectf(t, cat.node_types[ti].era_introduced <= 1, "era-1 roster must hold only era-1 types")
 	}
+	// era 2: residential + small_biz (the office class unlocks at era 2)
+	r2, w2 := growth_terminal_roster(cat, 2)
+	defer {
+		delete(r2)
+		delete(w2)
+	}
+	has_small_biz := false
+	for ti in r2 {
+		if cat.node_types[ti].terminal_role == .Small_Biz { has_small_biz = true }
+		testing.expectf(t, cat.node_types[ti].era_introduced <= 2, "era-2 roster must hold only era-<=2 types")
+	}
+	testing.expectf(t, len(r2) == 2 && has_small_biz, "era-2 roster must hold residential + small_biz, got %d types", len(r2))
+	// era 3: the full terminal spectrum — residential + small_biz +
+	// content_host + campus (campus unlocks at era 3)
 	r3, w3 := growth_terminal_roster(cat, 3)
 	defer {
 		delete(r3)
 		delete(w3)
 	}
-	testing.expectf(t, len(r3) == 2, "era-3 roster must hold residential + content_host, got %d types", len(r3))
+	has_campus := false
+	for ti in r3 {
+		if cat.node_types[ti].terminal_role == .Campus { has_campus = true }
+		testing.expectf(t, cat.node_types[ti].kind == .Terminal, "growth roster must never hold a junction kind")
+		testing.expectf(t, cat.node_types[ti].era_introduced <= 3, "era-3 roster must hold only era-<=3 types")
+	}
+	testing.expectf(t, len(r3) == 4 && has_campus, "era-3 roster must hold the full terminal spectrum (residential + small_biz + content_host + campus), got %d types", len(r3))
 }
 
 @(test)
diff --git a/data/demand.json b/data/demand.json
index 086bf65..99ba818 100644
--- a/data/demand.json
+++ b/data/demand.json
@@ -1,5 +1,5 @@
 {
-  "_comment": "Demand catalog (v1 §3, ODN-5) — per-era DemandSpecs (base, always active) + SetPieces (forecast events). The Surge = streaming x10 (the Era-3 climax the slice-4 crisis engine fires on schedule). Ported from the Godot prototype's tuned demand.json (prototype-fun-gate); eras are an ARRAY (insertion-ordered, map-free per ODN-10 — Odin-native vs the prototype's object-keyed form). selection = weighted_random (the MVP default — seeded weighted-random dst pick, v1 §3.3). Story 3.1: scripted_plan_pressure returns the active era's entries + any active set-piece each tick; flow_step spawns per spec. set_piece.multiplier amplifies its class's spawn volume while active (effective_volume). growth_roles is [LATER] (map growth, slice 5.1). 5.9 re-tune (spec-traffic-model Thread 2 — the surge-revalidation, owned by story 5.9): the era-3 base volumes are SCALED to the capped MVP (email 4→1, streaming 2→1 per tick — the honest-traffic doctrine bounds every terminal's source rate to a fraction of its own throughput, so the base demand lands on the grown map instead of being silently skipped); the surge stays x10 the streaming base (10/tick) and lands as an AGGREGATION event across the content_hosts the 5.1 growth has placed by tick 1200. Eras 1/2 are UNCHANGED (dormant in the MVP — the app runs era 3 from tick 1; the era-FSM story owns their re-tune).",
+  "_comment": "Demand catalog (v1 §3, ODN-5) — per-era DemandSpecs (base, always active) + SetPieces (forecast events). The Surge = streaming x10 (the Era-3 climax the slice-4 crisis engine fires on schedule). Ported from the Godot prototype's tuned demand.json (prototype-fun-gate); eras are an ARRAY (insertion-ordered, map-free per ODN-10 — Odin-native vs the prototype's object-keyed form). selection = weighted_random (the MVP default — seeded weighted-random dst pick, v1 §3.3). Story 3.1: scripted_plan_pressure returns the active era's entries + any active set-piece each tick; flow_step spawns per spec. set_piece.multiplier amplifies its class's spawn volume while active (effective_volume). growth_roles is [LATER] (map growth, slice 5.1). 5.9 re-tune (spec-traffic-model Thread 2 — the surge-revalidation, owned by story 5.9): the era-3 base volumes are SCALED to the capped MVP (email 4→1, streaming 2→1 per tick — the honest-traffic doctrine bounds every terminal's source rate to a fraction of its own throughput, so the base demand lands on the grown map instead of being silently skipped); the surge stays x10 the streaming base (10/tick) and lands as an AGGREGATION event across the content_hosts the 5.1 growth has placed by tick 1200. Eras 1/2 are UNCHANGED (dormant in the MVP — the app runs era 3 from tick 1; the era-FSM story owns their re-tune). 5.11 adds the era-3 entries for the new terminal classes (spec-traffic-model Thread 4 — each type emits its own bounded profile): email from small_biz (offices email; cap 0.333 pkts/tick) + streaming from campus (campuses flood — cap 2.5 pkts/tick, 30x a home; the surge's x10 lands on campuses too, the honest aggregation event). The selectors resolve against the new roles via collect_terminals; entries whose role has NO live terminal spawn nothing and draw no rng (existing fixtures untouched).",
   "eras": [
     {
       "era": 1,
@@ -51,6 +51,24 @@
           "default_lane": 1,
           "selection": "weighted_random",
           "demand_weight": 1
+        },
+        {
+          "class_id": "email",
+          "source_role": "small_biz",
+          "sink_role": "residential",
+          "volume": 1,
+          "default_lane": 1,
+          "selection": "weighted_random",
+          "demand_weight": 1
+        },
+        {
+          "class_id": "streaming",
+          "source_role": "campus",
+          "sink_role": "residential",
+          "volume": 1,
+          "default_lane": 1,
+          "selection": "weighted_random",
+          "demand_weight": 1
         }
       ],
       "set_pieces": [
diff --git a/data/node_types.json b/data/node_types.json
index 92a8f01..817c541 100644
--- a/data/node_types.json
+++ b/data/node_types.json
@@ -1,5 +1,5 @@
 {
-  "_comment": "Node-type catalog (GDD § M3, ODN-5). Story 1.2 ships a minimal roster: residential (terminal source), content_host (terminal sink), router_basic (junction). kind: terminal | junction. terminal_role: residential | content_host | none. throughput_units = node throughput ceiling. port_capacity 0 = unlimited (terminals); routers are port-scaled (canon #14: basic 4 / mid 8 / high 16). demand_weight (Story 3.1) = the terminal's relative attractor weight for weighted-random dst selection (v1 §3.3); terminals only, default 1 (uniform). Story 5.6 adds router_mid + router_high (GDD M3 tiers, user ruling 2026-08-14): free-placement hardware until the economy/8.6 story.",
+  "_comment": "Node-type catalog (GDD § M3, ODN-5). Story 1.2 ships a minimal roster: residential (terminal source), content_host (terminal sink), router_basic (junction). kind: terminal | junction. terminal_role: residential | content_host | none. throughput_units = node throughput ceiling. port_capacity 0 = unlimited (terminals); routers are port-scaled (canon #14: basic 4 / mid 8 / high 16). demand_weight (Story 3.1) = the terminal's relative attractor weight for weighted-random dst selection (v1 §3.3); terminals only, default 1 (uniform). Story 5.6 adds router_mid + router_high (GDD M3 tiers, user ruling 2026-08-14): free-placement hardware until the economy/8.6 story. Story 5.11 adds the class analogues (spec-traffic-model Thread 4 — the honest spectrum): small_biz (office, era 2) + campus (era 3). Per-type profile = throughput_units (the cap input) + demand_weight (the volume attractor); the per-terminal cap is computed uniformly by 5.9: cap = cap_fraction_permille × throughput ÷ packet_bandwidth — residential 500×5÷30 = 83 milli/tick (0.083 pkts/tick), small_biz 500×20÷30 = 333 (0.333, 4× a home), content_host 1333 (1.333), campus 500×150÷30 = 2500 (2.5, 30× a home — campuses flood). Shapes (never color alone, E9.1): the 5.11 sprite wiring maps residential → house, small_biz → the small_biz sprite, campus → the campus sprite (#65 set — canon, not re-rendered).",
   "entries": [
     {
       "id": "residential",
@@ -52,6 +52,28 @@
       "lb_mode_capable": false,
       "era_introduced": 3,
       "port_capacity": 16
+    },
+    {
+      "id": "small_biz",
+      "display_name": "Small Business",
+      "kind": "terminal",
+      "terminal_role": "small_biz",
+      "throughput_units": 20,
+      "demand_weight": 2,
+      "lb_mode_capable": false,
+      "era_introduced": 2,
+      "port_capacity": 0
+    },
+    {
+      "id": "campus",
+      "display_name": "Campus",
+      "kind": "terminal",
+      "terminal_role": "campus",
+      "throughput_units": 150,
+      "demand_weight": 4,
+      "lb_mode_capable": false,
+      "era_introduced": 3,
+      "port_capacity": 0
     }
   ]
 }
diff --git a/demos/node_health.dem b/demos/node_health.dem
index f0f2ca3..41dacf4 100644
--- a/demos/node_health.dem
+++ b/demos/node_health.dem
@@ -3,11 +3,13 @@
 # Era 3 + growth on (5.1 coherence): the connected legs (res->router) flow
 # email from tick 3; the HOST pipe is DELAYED to 20s so the host's streaming
 # spawns pile (the drowning case — amber at 2 stuck = 75% of the 80 u/s host
-# throughput, red at 4+ = 150%); growth spawns content_hosts the player has
-# NOT connected — their streaming piles too (the "growth-born nodes included"
-# canon). The telegraph is icon + outline + pulse (ring + "!"/"!!" glyph),
-# NEVER color alone; healthy nodes draw NOTHING (quiet at green — the
-# connected legs stay silent under flowing traffic).
+# throughput, red at 4+ = 150%); growth spawns terminals the player has NOT
+# connected — their demand piles too (the "growth-born nodes included" canon;
+# 5.11: the era-3 roster now includes small_biz + campus, so growth-born
+# buildings of every class pile the same way). The telegraph is icon + outline
+# + pulse (ring + "!"/"!!" glyph), NEVER color alone; healthy nodes draw
+# NOTHING (quiet at green — the connected legs stay silent under flowing
+# traffic).
 #
 # Verified surface (deterministic — same seed + commands reproduce it):
 #   tick 1 (50ms):   the pre-draw pile — residentials red (email spawns, no
diff --git a/demos/terminal_types.dem b/demos/terminal_types.dem
new file mode 100644
index 0000000..86656bf
--- /dev/null
+++ b/demos/terminal_types.dem
@@ -0,0 +1,40 @@
+# terminal_types.dem — Story 5.11: the terminal-class spectrum (residential /
+# small-biz / campus) — the card's named golden: "a T2 frame with ALL THREE
+# types visible". `fixture off` + explicit spawn_node directives lay out the
+# spectrum (run setup — re-created identically on every replay, like the
+# fixture; era gating is a GROWTH rule, spawn_node is explicit): res(1),
+# host(2), two more homes (3, 4), one small_biz (5) and one campus (6) fan out
+# from a mid router (0, 8 ports — the hub the player's mesh grows from). Era 3
+# + growth on: the director's era-3 demand is live (email from homes +
+# small_biz, streaming from hosts + campuses — the 5.11 entries, "homes
+# trickle, campuses flood") and growth places the new types organically
+# (small_biz era 2, campus era 3 — the era-unlocked roster), every spawn
+# E31-valid + min-separated. The captures read the roster as a spectrum —
+# distinct shapes per type (the #65 sprites, never color alone, E9.1): 5000 ms
+# (the three guaranteed types + the first growth windows) and 30000 ms (the
+# grown map).
+#
+# T1 pins (replay gate + manifest): every per-tick hash, including the growth
+# windows + the era-3 demand spawns from the new types (replay byte-identical
+# [E10]).
+seed 42
+era 3
+run 32000ms
+fixture off
+growth on
+spawn_node router_mid 20 15
+spawn_node residential 8 15
+spawn_node content_host 32 15
+spawn_node residential 14 22
+spawn_node residential 26 22
+spawn_node small_biz 12 10
+spawn_node campus 30 10
+at 500ms draw 1 0 standard
+at 500ms draw 0 2 standard
+at 500ms draw 3 0 standard
+at 500ms draw 0 4 standard
+at 700ms draw 5 0 standard
+at 900ms draw 0 6 standard
+capture at 5000ms
+capture at 30000ms
+expect hash stable

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "blind",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact diff lines that prove the claim, pasted verbatim from the diff above. Use 'N/A' only when the claim is about something genuinely absent from the diff (e.g. a missing test file). Paraphrased or reconstructed evidence is hallucination — drop the finding instead.>",
  "detail": "<=40 words>",
  "recommended_fix": "<=40 words>"
}

Output contract: write ONLY the JSON array (no prose, no fencing, no preamble) to the file
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.11-terminal-types/r2/lens-out/blind-code.json
using your file-writing tool, then stop. Also return the JSON array as your final answer. [] is valid.

ACCURACY MANDATE: no claim you make will be taken at face value. Every finding will be cross-checked against the actual diff before reporting. Findings whose evidence cannot be located in the diff above, or whose claims contradict what the diff actually shows, are DISCARDED silently. Quote the exact diff lines in evidence. Speculation without quoted evidence is dropped. Accuracy > volume — an empty array is an honest answer when nothing is wrong.
