diff --git a/core/flow.odin b/core/flow.odin
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
