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
