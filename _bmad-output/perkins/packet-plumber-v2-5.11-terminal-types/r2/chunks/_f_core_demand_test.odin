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
