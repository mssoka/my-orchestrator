diff --git a/app/render/sprites.odin b/app/render/sprites.odin
index b42dee1..88503ba 100644
--- a/app/render/sprites.odin
+++ b/app/render/sprites.odin
@@ -29,8 +29,8 @@ SPRITES_JSON :: #load("../../assets/sprites/sprites.json")
 
 // SPRITE_COUNT — the sheet size (order in sprites.json).
 // 9 canon (7.1) + 2 story-5.11 terminal shapes (small_biz, campus) appended
-// AFTER the canon set so existing indices 0-8 stay stable (loaded but not yet
-// wired to any role — the 5.11 enum/draw wiring belongs to story 5.11).
+// AFTER the canon set so existing indices 0-8 stay stable. Wired since 5.11:
+// sprite_index_building maps the class analogues onto them (see below).
 SPRITE_COUNT :: 11
 
 // sprite order (the sprites.json `order` array):
@@ -129,14 +129,23 @@ sprites_parse_boxes :: proc(sh: ^Sprite_Sheet) -> bool {
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
+	case .None:         // unreachable for terminals (kind != .Terminal never draws)
 	}
+	// DEFENSIVE: an unwired future role falls back to the house variant — the
+	// E9.1 distinct-shape contract for a new role is the role's own story's
+	// wiring (a future role must map its sprite HERE, never rely on this
+	// fallback silently). palcheck pins the wired roles positively.
 	return int(id % 4)
 }
 
@@ -173,8 +182,12 @@ sprite_blit :: proc(sh: ^Sprite_Sheet, idx: int, c: rl.Vector2, target_w: f32) {
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
