diff --git a/harness/palcheck.odin b/harness/palcheck.odin
index 730c319..4dc192a 100644
--- a/harness/palcheck.odin
+++ b/harness/palcheck.odin
@@ -29,6 +29,11 @@ import rnd "../app/render"
 // what the design emits, not what the palette defines).
 HOUSE_ROOFS := [4]rl.Color{{122, 46, 38, 255}, {122, 84, 24, 255}, {44, 106, 52, 255}, {38, 80, 126, 255}}
 HOST_ROOF := rl.Color{38, 76, 142, 255}
+// 5.11 (Perkins r1 W1): the class-analogue sprites' dominant canon tones — the
+// office block's warm paper-tan + the campus's brick red (measured from the
+// committed #65 sprites; the bilinear blit keeps interior flat areas exact).
+SMALL_BIZ_TAN := rl.Color{99, 87, 65, 255}
+CAMPUS_BRICK := rl.Color{99, 43, 34, 255}
 LED_GREEN := rl.Color{46, 139, 87, 255}
 LANE_AMBER := rl.Color{224, 138, 46, 255}
 STATE_CRITICAL := rl.Color{232, 69, 69, 255}
@@ -152,6 +157,21 @@ run_palcheck :: proc(cat: ^pp.Catalogs) -> int {
 	check(count_exact(calm, LED_GREEN) > 10, "puck LEDs", count_exact(calm, LED_GREEN))
 	check(count_near(calm, rl.Color{62, 74, 92, 255}, 12) > 200, "puck hardware tone", count_near(calm, rl.Color{62, 74, 92, 255}, 12))
 
+	// 1e. the 5.11 class-analogue sprites (the #65 canon set — Perkins r1 W1):
+	// the small_biz + campus shapes must be OBJECTIVELY present in the
+	// all-three-types golden (a degenerate/cropped blit — the B1 sprite-crop
+	// class — fails the way the play-marking canary fails a cropped host).
+	// This is also the positive E9.1 pin (distinct shapes render) the sprite-
+	// index mapping lacks at unit level.
+	term, ok3 := load_frame("goldens/terminal_types/05000ms.png")
+	if !ok3 {
+		fmt.eprintln("palcheck: cannot load the terminal_types golden (re-bless first)")
+		return 2
+	}
+	defer rl.UnloadImage(term)
+	check(count_exact(term, SMALL_BIZ_TAN) > 100, "small_biz sprite (5.11 office)", count_exact(term, SMALL_BIZ_TAN))
+	check(count_exact(term, CAMPUS_BRICK) > 100, "campus sprite (5.11 campus)", count_exact(term, CAMPUS_BRICK))
+
 	// 1d. the 7.4 procedural-map palette (canon D9 — the map renders on EVERY
 	// frame, so the blessed juice goldens carry it): the map tokens must be
 	// OBJECTIVELY present (the look-book §2 oracle — water/coast/park + the
