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
