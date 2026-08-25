diff --git a/core/demand_test.odin b/core/demand_test.odin
index dff2710..90f67d5 100644
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
@@ -381,14 +397,190 @@ test_credit_accrue_and_max :: proc(t: ^testing.T) {
 	testing.expect_value(t, spawn_credit_max_milli(cat, res_idx), u32(1000))
 }
 
-// W9 — post-cap surge-lands (Perkins r1 W9 + r2 W6 pin): on a known seed,
-// era 3 + growth on + the streaming-surge window — the window's streaming
-// spawn count is >= the re-tuned expected volume × 0.95 (10/tick × the
-// window), every terminal's spawns stay <= cap × window + burst allowance,
-// and every terminal's credit stays <= MAX_CREDIT (never silently zeroed).
-// The re-tuned trio (era-3 demand 1+1, surge ×10, growth interval 40) is
-// RE-VALIDATED TOGETHER here: the surge must land as an aggregation event —
-// spread across the growth-born content_hosts (silent non-landing is a fail).
+// 5.11 — the class-analogue profiles (spec-traffic-model Thread 4): each type
+// emits its OWN bounded profile — campus >> home in volume AND cap; the typed
+// source selectors resolve against the new roles (collect_terminals); the 5.9
+// accumulator applies uniformly (every terminal stays inside cap×W + burst,
+// credit <= MAX — the honest-traffic invariant holds for the new types too).
+// One terminal per ROLE for the new classes (the small_biz / campus / host
+// source sets are singletons — the pick's rng draw picks the only candidate)
+// + TWO residentials (the email dst pick needs a real sink set, dst != src —
+// both homes source email, aggregated into the home per-role count). The
+// per-role counts are the profile.
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
+	// per-role spawn counts: 0 residential, 1 small_biz, 2 content_host,
+	// 3 campus — split into the BASE window (ticks 1..<1200 — the era-3 base
+	// demand, no surge) and the SURGE window (1200..=W — the streaming surge
+	// ×10 is active, the "campuses flood" read). The base-window ratio is the
+	// SPECTRUM (W2: the whole-run ratio is surge-inflated and knife-edge).
+	per_role_base := [4]u64{}
+	per_role_surge := [4]u64{}
+	per_terminal := make(map[u32]u64, 16)
+	defer delete(per_terminal)
+	selector_ok := true
+	credit_ok := true
+	envelope_ok := true
+	SURGE_AT :: u64(1200) // the streaming surge's data start_tick
+	for tick in u64(1)..=W {
+		step(&s, tick, {}, cat)
+		in_surge := tick >= SURGE_AT
+		for p in s.flow.packets {
+			if p.spawn_tick != tick { continue }
+			per_terminal[p.src] += 1
+			slot := node_slot_raw(&s.topology, p.src)
+			role := s.topology.node_role[slot]
+			#partial switch role {
+			case .Residential:  if in_surge { per_role_surge[0] += 1 } else { per_role_base[0] += 1 }
+			case .Small_Biz:    if in_surge { per_role_surge[1] += 1 } else { per_role_base[1] += 1 }
+			case .Content_Host: if in_surge { per_role_surge[2] += 1 } else { per_role_base[2] += 1 }
+			case .Campus:       if in_surge { per_role_surge[3] += 1 } else { per_role_base[3] += 1 }
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
+	total_campus := per_role_base[3] + per_role_surge[3]
+	total_home := per_role_base[0] + per_role_surge[0]
+	total_sb := per_role_base[1] + per_role_surge[1]
+	// the base window = the SPECTRUM (the pure per-type profile, no surge):
+	// campus vs home >= 4x (the accrue constants are 2500 vs 83 milli/tick —
+	// 30x theoretical; 4x is the robust floor that bites on a ratio collapse)
+	testing.expectf(t, per_role_base[3] >= 4*per_role_base[0],
+		"base spectrum: campus %d vs home %d in the base window (want >= 4x)", per_role_base[3], per_role_base[0])
+	// the surge window = the flood: campus >> home (the ×10 streaming lands on
+	// campuses — the knife-edge whole-run ratio is split out; the surge window
+	// itself is >= 10x by a wide margin)
+	testing.expectf(t, per_role_surge[3] >= 10*per_role_surge[0],
+		"surge flood: campus %d vs home %d in the surge window (want >= 10x)", per_role_surge[3], per_role_surge[0])
+	// the campus half is fully served (the flood) over the whole run
+	testing.expectf(t, total_campus >= W*9/10,
+		"campus must be fully served (the flood): sourced %d over %d ticks, want >= %d", total_campus, W, W*9/10)
+	// the spectrum orders correctly across the run
+	testing.expectf(t, total_sb > total_home,
+		"small_biz emits more than a home: %d vs %d (cap 0.333 vs 0.083)", total_sb, total_home)
+	testing.expectf(t, total_campus > total_sb,
+		"campus emits more than small_biz (the spectrum reads): %d vs %d", total_campus, total_sb)
+	testing.expect(t, credit_ok, "every terminal's credit must stay <= MAX_CREDIT (uniform 5.9 accumulator)")
+	testing.expect(t, envelope_ok, "every terminal's window spawns must stay <= cap×W + burst (uniform 5.9 accumulator)")
+}
+
+// W4 (Perkins r1) — role-absent demand inertness, pinned durably: an era-3
+// demand entry whose role has NO live terminal spawns nothing AND draws NO
+// rng (the re-bless key invariant — the pre-5.11 fixtures' streams are
+// untouched by construction; verified one-time via log byte-compare in the
+// PR, now a standing pin). Era 3 on the qa_fixture (residentials + router +
+// content_host — no small_biz/campus): the full catalog and the pre-5.11
+// entry set must produce identical spawn streams AND identical rng state
+// (the "no rng" half — a stray draw would shift the stream).
+@(test)
+test_role_absent_demand_inert :: proc(t: ^testing.T) {
+	cat_storage: Catalogs
+	cat := test_catalog(&cat_storage)
+	defer catalogs_destroy(cat)
+	cat_storage2: Catalogs
+	cat2 := test_catalog(&cat_storage2)
+	defer catalogs_destroy(cat2)
+	// trim the two 5.11 era-3 entries (small_biz email + campus streaming)
+	e3 := &cat2.demand.eras[2]
+	trimmed := make([dynamic]Demand_Entry, 0, 4, context.allocator)
+	defer delete(trimmed)
+	for e in e3.entries {
+		if e.source_role == .Small_Biz || e.source_role == .Campus {
+			continue
+		}
+		append(&trimmed, e)
+	}
+	delete(e3.entries)
+	e3.entries = trimmed
+
+	run_inert :: proc(seed: u64, cat: ^Catalogs, ticks: u64) -> (by_class: [8]u64, src_hist: [8][64]u64, rng_state, rng_inc: u64) {
+		s: Run_State
+		defer run_destroy(&s)
+		run_init(&s, seed, cat.hash, TEST_LOGIC_HZ)
+		s.era = 3
+		qa_fixture(&s, cat) // residentials + router + content_host — no small_biz/campus
+		record_run(&s, ticks, cat)
+		by_class, _, src_hist, _ = spawn_histogram(&s.flow)
+		return by_class, src_hist, s.rng.state, s.rng.inc
+	}
+
+	full_b, full_sh, full_rng_s, full_rng_i := run_inert(7, cat, 600)
+	trim_b, trim_sh, trim_rng_s, trim_rng_i := run_inert(7, cat2, 600)
+	same := full_b == trim_b && full_sh == trim_sh && full_rng_s == trim_rng_s && full_rng_i == trim_rng_i
+	// the negative control: the trimmed run must still SPAWN (era-3 email +
+	// streaming from the fixture's residentials + host) — a no-spawn run would
+	// pass the equality vacuously.
+	spawned := full_b[0] + full_b[1]
+	testing.expectf(t, spawned > 0, "the control run must spawn era-3 demand (got %d spawns) — a vacuous pass is a regression", spawned)
+	testing.expect(t, same,
+		"role-absent entries must be inert: spawn stream + rng state must equal the pre-5.11 entry set")
+	testing.expectf(t, full_rng_s != 0 || full_rng_i != 0, "the runs must actually advance the rng (the equality is non-vacuous)")
+}
+
+// W9 — post-cap surge-lands (Perkins r1 W9 + r2 W6 pin; 5.11 honest re-pin,
+// Perkins r1 B1): on a known seed, era 3 + growth on + the streaming-surge
+// window — the window's streaming spawn count is >= the honest expected
+// volume × 0.95, every terminal's spawns stay <= cap × window + burst
+// allowance, and every terminal's credit stays <= MAX_CREDIT (never silently
+// zeroed). The re-tuned trio (era-3 demand 1+1, surge ×10, growth interval
+// 40) is RE-VALIDATED TOGETHER here: the surge must land as an aggregation
+// event — spread across the growth-born streaming crowd (content_hosts + the
+// 5.11 campuses) with at least one campus present and sourcing (a campus-
+// silent pass is a regression — the honest floor would be unverifiable).
+//
+// The honest ask is DOUBLED by the 5.11 roster: TWO era-3 streaming entries
+// (content_host vol 1 + campus vol 1), each amplified ×10 → 20/tick in the
+// window (Perkins probe: floor 34200 vs 31611 = 87.8% from an empty start —
+// the stale pin passed a campus-silent regression AND an under-asked floor).
+// The honest floor is per-role: the CAMPUS half must land fully (campuses are
+// plentiful — the 5.11 flood) and the total must land >=95% of the doubled
+// ask on a grown mesh (see the fixture note — the fair-crisis doctrine:
+// a thin map legitimately lands a partial surge; the grown mesh earns the
+// full event).
 @(test)
 test_w9_surge_lands_under_caps :: proc(t: ^testing.T) {
 	cat_storage: Catalogs
@@ -402,25 +594,52 @@ test_w9_surge_lands_under_caps :: proc(t: ^testing.T) {
 	defer run_destroy(&s)
 	run_init(&s, 4243, cat.hash, TEST_LOGIC_HZ)
 	s.era = 3
-	// the mesh: one player-placed router (growth proceeds outward from it).
+	// the start map = the PLAYER'S GROWN MESH + the aggregation crowd (the
+	// 5.1 build-out loop: the player places routers, growth spawns terminals
+	// outward from the mesh — the honest pre-surge state for the era-3 climax).
+	// Seeded deliberately rather than grown-to-time: a single-router map tops
+	// out at ~5-6 content_hosts (the 5.11 campus weight 4/8 dilutes the host
+	// crowd + the E31 min-separation crowds the grid), so the honest doubled
+	// ask (20/tick) is unlandable from an empty start — a partial surge is the
+	// fair, telegraphed reality on a thin map; this pin proves the LANDABLE
+	// CEILING once the mesh is grown (the crisis the player earns by building).
 	res_idx, _ := node_type_index(cat, "residential")
 	rt_idx, _ := node_type_index(cat, "router_basic")
 	host_idx, _ := node_type_index(cat, "content_host")
-	topology_spawn_node(&s.topology, res_idx, {20, 15}, cat) // the start map's one residential
-	topology_spawn_node(&s.topology, rt_idx, {20, 17}, cat)
-	topology_spawn_node(&s.topology, host_idx, {20, 13}, cat) // the start map's one host
+	camp_idx, _ := node_type_index(cat, "campus")
+	// two routers (the mesh anchors for growth + E31 connectability)
+	topology_spawn_node(&s.topology, rt_idx, {20, 15}, cat)
+	topology_spawn_node(&s.topology, rt_idx, {30, 25}, cat)
+	// 8 content_hosts — the host half of the streaming crowd (≥ the 8 needed
+	// for its ×10 share; the 5.9 aggregation canon: hosts source streaming)
+	host_pos := [8][2]i32{{8, 10}, {12, 8}, {16, 6}, {24, 6}, {28, 8}, {32, 10}, {36, 12}, {34, 20}}
+	for hp in host_pos { topology_spawn_node(&s.topology, host_idx, hp, cat) }
+	// 6 campuses — the 5.11 flood sites (the campus half of the crowd)
+	camp_pos := [6][2]i32{{6, 20}, {10, 26}, {18, 28}, {26, 28}, {34, 26}, {36, 18}}
+	for cp in camp_pos { topology_spawn_node(&s.topology, camp_idx, cp, cat) }
+	// 4 residentials — the sink set (weighted-random dst needs dst != src)
+	res_pos := [4][2]i32{{2, 2}, {38, 2}, {2, 28}, {38, 28}}
+	for rp in res_pos { topology_spawn_node(&s.topology, res_idx, rp, cat) }
 	s.growth_enabled = true
 
-	SURGE_START :: u64(1200)
-	SURGE_END :: u64(3000)
-	WINDOW := SURGE_END - SURGE_START
-	EXPECTED := 10 * WINDOW // the re-tuned surge: ×10 the era-3 streaming base (1/tick)
+	// the surge stays at the DATA start (1200 — the app's era-3 climax); the
+	// honest ask is the DOUBLED era-3 streaming volume (content_host vol 1 +
+	// campus vol 1, each ×10 by the surge → 20/tick in the window). The
+	// window is DERIVED from the set-piece so a future re-tune of the surge
+	// timing cannot silently drift this pin.
+	surge := &cat.demand.eras[2].set_pieces[0]
+	SURGE_START := u64(surge.start_tick)
+	SURGE_END := SURGE_START + surge.duration_ticks
+	WINDOW := SURGE_END - SURGE_START // the active window [start, start+duration)
+	EXPECTED := 20 * WINDOW // the doubled ask: 2 streaming entries × ×10 × WINDOW
 	MIN_LAND := EXPECTED * 95 / 100
 
 	hosts := 0
+	campuses := 0
 	credit_ok := true
 	burst_ok := true
 	stream_spawned: u64 = 0
+	campus_window_spawns: u64 = 0
 	per_host_spawns := make(map[u32]u64, 64) // outlives the tick loop (run arena)
 	defer delete(per_host_spawns)
 	for tick in u64(1)..=SURGE_END {
@@ -431,32 +650,70 @@ test_w9_surge_lands_under_caps :: proc(t: ^testing.T) {
 			}
 		}
 		step(&s, tick, batch[:], cat)
-		// the in-window per-tick per-host burst ceiling (ceil_cap = 2)
+		in_window := tick >= SURGE_START && tick < SURGE_END
+		// the per-tick per-source burst ceiling — TYPE-RELATIVE (5.11: the
+		// streaming crowd is content_hosts + campuses; the ceiling is
+		// ceil(cap) per type — host 2, campus 3). Checked EVERY tick (base
+		// and window — the pre-surge rate is bounded by the same ceiling).
 		per_tick_host_burst := make(map[u32]u32, 16, context.temp_allocator)
 		for p in s.flow.packets {
-			if p.class == 1 && p.spawn_tick == tick {
+			if p.class != 1 || p.spawn_tick != tick {
+				continue
+			}
+			per_tick_host_burst[p.src] += 1
+			if in_window {
+				// the land floor + the per-terminal envelope count the SURGE
+				// WINDOW only (the W in the bound formula — the pre-surge base
+				// accrual is bounded by the same cap mechanism + the director
+				// caps pin above).
 				stream_spawned += 1
-				per_tick_host_burst[p.src] += 1
 				per_host_spawns[p.src] += 1
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
+	// surge spreads across every terminal that can source it). Campuses are
+	// counted separately: the honest floor REQUIRES one to exist + source.
 	for ns in 0..<len(s.topology.node_alive) {
-		if !s.topology.node_alive[ns] { continue }
-		if s.topology.node_kind[ns] == .Terminal && s.topology.node_role[ns] == .Content_Host {
+		if !s.topology.node_alive[ns] || s.topology.node_kind[ns] != .Terminal {
+			continue
+		}
+		if s.topology.node_role[ns] == .Campus {
+			campuses += 1
+		}
+		if s.topology.node_role[ns] == .Content_Host || s.topology.node_role[ns] == .Campus {
 			hosts += 1
 		}
 	}
-	// per-terminal window spawns + credit bounds (the W9 envelope)
+	// campus in-window sourcing: which campuses actually sourced in the window
+	for ns in 0..<len(s.topology.node_alive) {
+		if !s.topology.node_alive[ns] || s.topology.node_role[ns] != .Campus {
+			continue
+		}
+		campus_window_spawns += per_host_spawns[s.topology.node_id[ns]]
+	}
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
@@ -466,11 +723,13 @@ test_w9_surge_lands_under_caps :: proc(t: ^testing.T) {
 		bound := ceil_cap + accrue * WINDOW / 1000
 		if per_host_spawns[s.topology.node_id[ns]] > bound { credit_ok = false }
 	}
-	testing.expectf(t, hosts >= 8, "growth must place >= 8 content_hosts by the surge window (got %d) — the aggregation crowd", hosts)
+	testing.expectf(t, hosts >= 8, "growth must place >= 8 streaming-capable terminals (content_hosts + campuses) by the surge window (got %d) — the aggregation crowd", hosts)
+	testing.expectf(t, campuses >= 1, "the honest surge floor requires a campus to exist (got %d) — a campus-silent pass is a regression", campuses)
+	testing.expectf(t, campus_window_spawns > 0, "the honest surge floor requires a campus to SOURCE in the window (got %d in-window campus spawns)", campus_window_spawns)
 	testing.expectf(t, stream_spawned >= MIN_LAND,
-		"W9 FAIL: the surge must LAND — streaming window spawns %d < %d (expected × 0.95); the capped map cannot source the surge", stream_spawned, MIN_LAND)
-	testing.expectf(t, burst_ok, "no per-tick burst beyond the ceiling (2 = ceil_cap) may occur")
-	testing.expectf(t, credit_ok, "every terminal's credit must stay <= MAX_CREDIT and its window spawns <= cap×W + burst")
+		"W9 FAIL: the surge must LAND — in-window streaming spawns %d < %d (the honest doubled ask × 0.95: 2 streaming entries × 10 × %d ticks); the capped map cannot source the surge", stream_spawned, MIN_LAND, WINDOW)
+	testing.expectf(t, burst_ok, "no per-tick burst beyond the type-relative ceiling (host 2 / campus 3 = ceil(cap)) may occur")
+	testing.expect(t, credit_ok, "every terminal's credit must stay <= MAX_CREDIT and its window spawns <= cap×W + burst")
 }
 
 // W10 — one-subscriber-at-cap zero-drop (r2 W6/W5 pin): on a known seed, over
