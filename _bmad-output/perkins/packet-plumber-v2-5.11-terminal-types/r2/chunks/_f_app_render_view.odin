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
