package vocab_capture

// vocab_sheet.odin — the shape-vocabulary candidate sheet (evidence render for
// packet-plumber-v2-viscomm-shape-vocab; READ-ONLY scratch, never committed).
//
// One block per packet class (canon roster order, art-direction §5.1); each
// block shows its shape candidates at the THREE LOOK-SPEC zoom rungs
// (CORE zoom 1.0 -> r 9.7px / DISTRIBUTION 1.4 -> r 13.6 / ACCESS 2.0 -> r
// 19.4; r = tile26 x zoom x 0.24 x 1.35 x PACKET_R_FACTOR 1.15 — the shipped
// view.odin chain) plus a single-file rider strip on a neutral link band.
// Colors are the CANON §5.1 catalog hexes, ILLUSTRATIVE ONLY — the class
// color system is Fork 8 (5 CVD anchors), ruled separately.
//
// §10.4 discipline: all polygons come from the PINNED tables below (no
// transcendentals in the draw path); deterministic frame to frame.

import "core:fmt"
import "core:os"
import "core:strings"
import rl "vendor:raylib"
import pp "../../../../packet-plumber/core"
import rnd "../../../../packet-plumber/app/render"

// --- pinned vertex tables (normalized unit radius) ---------------------------

pill16 := [16][2]f32{
	{+0.540468, -0.598874}, {+0.818406, -0.438406}, {+0.978874, -0.160468}, {+0.978874, +0.160468},
	{+0.818406, +0.438406}, {+0.540468, +0.598874}, {+0.000000, +0.620000}, {-0.000000, +0.620000},
	{-0.540468, +0.598874}, {-0.818406, +0.438406}, {-0.978874, +0.160468}, {-0.978874, -0.160468},
	{-0.818406, -0.438406}, {-0.540468, -0.598874}, {-0.000000, -0.620000}, {+0.000000, -0.620000},
}

rsq12 := [12][2]f32{
	{+1.000000, +0.650000}, {+0.953109, +0.825000}, {+0.825000, +0.953109},
	{-0.650000, +1.000000}, {-0.825000, +0.953109}, {-0.953109, +0.825000},
	{-1.000000, -0.650000}, {-0.953109, -0.825000}, {-0.825000, -0.953109},
	{+0.650000, -1.000000}, {+0.825000, -0.953109}, {+0.953109, -0.825000},
}

star10 := [10][2]f32{
	{+0.000000, +1.000000}, {-0.264503, +0.364058}, {-0.951057, +0.309017}, {-0.427975, -0.139058},
	{-0.587785, -0.809017}, {-0.000000, -0.450000}, {+0.587785, -0.809017}, {+0.427975, -0.139058},
	{+0.951057, +0.309017}, {+0.264503, +0.364058},
}

hex6 := [6][2]f32{
	{+1.000000, +0.000000}, {+0.500000, +0.866025}, {-0.500000, +0.866025},
	{-1.000000, +0.000000}, {-0.500000, -0.866025}, {+0.500000, -0.866025},
}

blob16 := [16][2]f32{
	{+1.000000, +0.000000}, {+0.776059, +0.321454}, {+0.664680, +0.664680}, {+0.298493, +0.720626},
	{+0.000000, +0.970000}, {-0.329108, +0.794536}, {-0.707107, +0.707107}, {-0.739104, +0.306147},
	{-0.920000, +0.000000}, {-0.711387, -0.294666}, {-0.671751, -0.671751}, {-0.325281, -0.785298},
	{-0.000000, -1.000000}, {+0.309974, -0.748342}, {+0.636396, -0.636396}, {+0.729865, -0.302320},
}

// draw_fan — triangle fan of a pinned table scaled by r (outline), then the
// same table at inner_scale (body). The draw_packet_shape 0.78 idiom.
draw_fan :: proc(pos: rl.Vector2, table: [][2]f32, r, inner: f32, body, outline: rl.Color) {
	n := len(table)
	for i in 0..<n {
		j := (i + 1) % n
		rl.DrawTriangle(
			rl.Vector2{pos.x + table[j][0] * r, pos.y + table[j][1] * r},
			rl.Vector2{pos.x + table[i][0] * r, pos.y + table[i][1] * r},
			pos, outline,
		)
		rl.DrawTriangle(
			rl.Vector2{pos.x + table[j][0] * r * inner, pos.y + table[j][1] * r * inner},
			rl.Vector2{pos.x + table[i][0] * r * inner, pos.y + table[i][1] * r * inner},
			pos, body,
		)
	}
}


// --- color helpers (deterministic integer mixes — the §10.4 spirit) ---------

mix_col :: proc(a, b: rl.Color, t: f32) -> rl.Color {
	return rl.Color{
		u8(f32(a.r) * (1 - t) + f32(b.r) * t),
		u8(f32(a.g) * (1 - t) + f32(b.g) * t),
		u8(f32(a.b) * (1 - t) + f32(b.b) * t),
		255,
	}
}

casing_color :: proc(p: ^rnd.Palette, col: rl.Color) -> rl.Color {
	return mix_col(col, p.ink, 0.45)
}

pp_shape_of :: proc(name: string) -> pp.Packet_Shape {
	if name == "triangle" { return .Triangle }
	return .Circle
}

// draw_shape_ext — the 7 proposed class shapes (the draw_packet_shape family,
// extended on the pinned tables). All deterministic polygon/ring builds.
draw_shape_ext :: proc(pos: rl.Vector2, r: f32, body, outline: rl.Color, name: string) {
	switch name {
	case "diamond": // web — the burst spark (4-gon on the 10° fan)
		verts := [4]rl.Vector2{{pos.x, pos.y - r}, {pos.x + r, pos.y}, {pos.x, pos.y + r}, {pos.x - r, pos.y}}
		for i in 0..<4 {
			j := (i + 1) % 4
			rl.DrawTriangle(verts[j], verts[i], {pos.x, pos.y}, outline)
		}
		rin := r * 0.78
		vi := [4]rl.Vector2{{pos.x, pos.y - rin}, {pos.x + rin, pos.y}, {pos.x, pos.y + rin}, {pos.x - rin, pos.y}}
		for i in 0..<4 {
			j := (i + 1) % 4
			rl.DrawTriangle(vi[j], vi[i], {pos.x, pos.y}, body)
		}
	case "square": // banking/IoT — the vault brick (4-gon, axis-aligned)
		rl.DrawRectangleV({pos.x - r, pos.y - r}, {r * 2, r * 2}, outline)
		rin := r * 0.78
		rl.DrawRectangleV({pos.x - rin, pos.y - rin}, {rin * 2, rin * 2}, body)
	case "octagon": // banking — the regulated stop-sign (8-gon on CIRCLE16)
		circle := rnd.CIRCLE16
		outer: [8]rl.Vector2
		inner: [8]rl.Vector2
		for k in 0..<8 {
			idx := (k * 2 + 6) % 16
			outer[k] = {pos.x + circle[idx][0] * r, pos.y + circle[idx][1] * r}
			inner[k] = {pos.x + circle[idx][0] * r * 0.8, pos.y + circle[idx][1] * r * 0.8}
		}
		for k in 0..<8 {
			j := (k + 1) % 8
			rl.DrawTriangle(outer[j], outer[k], pos, outline)
			rl.DrawTriangle(inner[j], inner[k], pos, body)
		}
	case "ring": // voice — the open channel (annulus, the tier-ring family)
		for k in 0..<i32(min(3.0, max(1.0, r * 0.22))) {
			rl.DrawCircleLinesV(pos, r - f32(k), outline)
		}
		rl.DrawCircleV(pos, max(1.0, r * 0.34), body)
	case "chevron": // gaming — the low-latency dart (2 triangles)
		h := r * 0.9
		rl.DrawTriangle({pos.x - h * 0.9, pos.y - h}, {pos.x - h * 0.9, pos.y + h}, {pos.x + h * 0.2, pos.y}, outline)
		rl.DrawTriangle({pos.x - h * 0.25, pos.y - h * 0.8}, {pos.x - h * 0.25, pos.y + h * 0.8}, {pos.x + h * 0.75, pos.y}, body)
	case "tridot": // multicast — one-to-many (3 dots, CIRCLE16 offsets)
		circle := rnd.CIRCLE16
		dr := max(1.6, r * 0.42)
		for k in 0..<3 {
			idx := (k * 5 + 9) % 16
			cp := rl.Vector2{pos.x + circle[idx][0] * r * 0.62, pos.y + circle[idx][1] * r * 0.62}
			rl.DrawCircleV(cp, dr, outline)
			rl.DrawCircleV(cp, dr * 0.72, body)
		}
	case "gear": // AI — the neural gear (8 alternating radii, CIRCLE16)
		circle := rnd.CIRCLE16
		outer: [16]rl.Vector2
		inner: [16]rl.Vector2
		for k in 0..<16 {
			rad := r
			if k % 2 == 1 { rad = r * 0.62 }
			outer[k] = {pos.x + circle[k][0] * rad, pos.y + circle[k][1] * rad}
			inner[k] = {pos.x + circle[k][0] * rad * 0.8, pos.y + circle[k][1] * rad * 0.8}
		}
		for k in 0..<16 {
			j := (k + 1) % 16
			rl.DrawTriangle(outer[j], outer[k], pos, outline)
			rl.DrawTriangle(inner[j], inner[k], pos, body)
		}
	case:
	rnd.draw_packet_shape(pos, r, body, outline, .Circle)
	}
}

// vocab_shape — every candidate silhouette on the sheet (shipped two route to
// the REAL renderer's draw_packet_shape — the sheet never re-states shipped
// geometry).
vocab_shape :: proc(pos: rl.Vector2, r: f32, body, outline: rl.Color, name: string) {
	switch name {
	case "circle", "triangle":
		s := pp_shape_of(name)
		rnd.draw_packet_shape(pos, r, body, outline, s)
	case "rounded_square":
		draw_fan(pos, rsq12[:], r, 0.78, body, outline)
	case "hexagon":
		draw_fan(pos, hex6[:], r, 0.78, body, outline)
	case "pill":
		draw_fan(pos, pill16[:], r, 0.78, body, outline)
	case "star":
		draw_fan(pos, star10[:], r, 0.78, body, outline)
	case "blob":
		draw_fan(pos, blob16[:], r, 0.78, body, outline)
	case "diamond", "square", "octagon", "ring", "chevron", "tridot", "gear":
		draw_shape_ext(pos, r, body, outline, name) // prior-session procs (main.odin)
	case "tiny_square":
		draw_shape_ext(pos, r * 0.72, body, outline, "square")
	case:
		rnd.draw_packet_shape(pos, r, body, outline, .Circle)
	}
}

// --- the sheet ---------------------------------------------------------------

Vocab_Cand :: struct {
	shape: string, // vocab_shape name
	label: string,
}
Vocab_Row :: struct {
	class_id:   string,
	title:      string,
	note:       string,
	color:      rl.Color,
	cands:      [2]Vocab_Cand, // second may be empty
}

vocab_sheet :: proc(rc: ^Render_Ctx, cat: ^pp.Catalogs, outdir: string) {
	v := &rc.view
	p := &rc.palette
	_ = cat
	rl.ClearBackground(p.canvas)

	keep := Vocab_Cand{}
	rows := [9]Vocab_Row{
		Vocab_Row{"email", "EMAIL · era 1 · SHIPPED", "high tol / low vol — 'safe to drop, safe to delay'", {90, 98, 112, 255},
			[2]Vocab_Cand{Vocab_Cand{"circle", "KEEP — shipped circle"}, keep}},
		Vocab_Row{"streaming", "STREAMING · era 3 · SHIPPED", "medium tol / HIGH vol — 'buffers stall; viewers quit'", {30, 74, 152, 255},
			[2]Vocab_Cand{Vocab_Cand{"triangle", "KEEP — shipped triangle"}, keep}},
		Vocab_Row{"web", "WEB · era 2 · lands with era progression (#107)", "med tol / med vol — 'pages stall'", {176, 122, 82, 255},
			[2]Vocab_Cand{Vocab_Cand{"rounded_square", "A · CANON: the page/card"}, Vocab_Cand{"diamond", "B · prior: burst spark"}}},
		Vocab_Row{"gaming", "GAMING · era 4", "LOW latency, bursty — 'lag = rage-quit'", {55, 214, 122, 255},
			[2]Vocab_Cand{Vocab_Cand{"diamond", "A · CANON: agile spark"}, Vocab_Cand{"chevron", "B · prior: fast-forward dart"}}},
		Vocab_Row{"banking", "BANKING · era 4", "med latency, ZERO loss — 'transaction fail = critical'", {245, 200, 66, 255},
			[2]Vocab_Cand{Vocab_Cand{"hexagon", "A · CANON: the nut/vault"}, Vocab_Cand{"octagon", "B · prior: stop-sign regulated"}}},
		Vocab_Row{"voice", "VOICE · era 4", "LOW latency, continuous — 'call drops'", {157, 123, 224, 255},
			[2]Vocab_Cand{Vocab_Cand{"pill", "A · CANON: the handset"}, Vocab_Cand{"ring", "B · prior: open channel — RING-FAMILY FLAG"}}},
		Vocab_Row{"multicast", "MULTICAST · era 5", "1 -> many fan — 'stream to many fails'", {255, 158, 61, 255},
			[2]Vocab_Cand{Vocab_Cand{"star", "A · CANON: radiating broadcast"}, Vocab_Cand{"tridot", "B · prior: literal 1 -> many"}}},
		Vocab_Row{"iot", "IOT · era 5", "high tol / TINY x HUGE count — 'aggregate sensor loss'", {54, 197, 216, 255},
			[2]Vocab_Cand{Vocab_Cand{"tiny_square", "A · CANON: the chip (0.72x)"}, Vocab_Cand{"square", "B · prior: full-size brick"}}},
		Vocab_Row{"ai", "AI · era 6", "adaptive, self-shaping — 'shaping collapses'", {240, 98, 146, 255},
			[2]Vocab_Cand{Vocab_Cand{"blob", "A · CANON: self-shaping (static)"}, Vocab_Cand{"gear", "B · prior: compute gear"}}},
	}

	// rung radii: the shipped chain r = tile_px(26) x zoom x 0.24 x 1.35 x 1.15
	r_core := f32(26.0 * 1.0 * 0.24 * 1.35 * 1.15)  // 9.68 @ CORE fit 1.0
	r_dist := f32(26.0 * 1.4 * 0.24 * 1.35 * 1.15)  // 13.55 @ DISTRIBUTION mid 1.4
	r_accs := f32(26.0 * 2.0 * 0.24 * 1.35 * 1.15)  // 19.36 @ ACCESS default 2.0
	runes := [3]f32{r_core, r_dist, r_accs}

	ink := p.ink
	soft := p.ink_soft
	title := "PACKET SHAPE VOCAB — candidate sheet · r = tile26 x zoom x 0.24 x 1.35 x 1.15 (shipped chain)"
	rnd.draw_text_c(v, title, 20, 18, 20, ink)
	rnd.draw_text_c(v, "canon art-direction §5.1 colors, ILLUSTRATIVE — class colors ride Fork 8 (5 CVD anchors), ruled separately", 20, 44, 15, soft)

	y := f32(78)
	for row, ri in rows {
		bh := f32(156)
		// class title + function note
		rnd.draw_text_c(v, row.title, 20, i32(y + 6), 17, ink)
		rnd.draw_text_c(v, row.note, 20, i32(y + 28), 14, soft)

		// rung gutter labels on the first candidate-bearing row only
		if ri == 0 {
			gx := f32(330)
			rung_lbls := [3]string{"CORE 1.0", "DIST 1.4", "ACCESS 2.0"}
			for k in 0..<3 {
				rnd.draw_text_c(v, rung_lbls[k], i32(gx + f32(k) * 120 - 30), i32(y + 6), 13, soft)
			}
			rnd.draw_text_c(v, "riders, single-file", 1030, i32(y + 6), 13, soft)
		}

		// candidate cells
		cx := f32(330)
		for c in 0..<2 {
			cand := row.cands[c]
			if cand.shape == "" { continue }
			outline := rl.Color{u8(f32(row.color.r) * 0.55), u8(f32(row.color.g) * 0.55), u8(f32(row.color.b) * 0.55), 255}
			// trio at the three rungs
			for k in 0..<3 {
				vocab_shape({cx + f32(k) * 120, y + 78}, runes[k], row.color, outline, cand.shape)
			}
			// rider strip: neutral band + single-file riders at DIST size
			strip_x := cx + f32(360)
			neutral := mix_col(p.canvas, p.pipe_steel, 0.55)
			cc := casing_color(p, neutral)
			a := rl.Vector2{strip_x, y + 78}
			b := rl.Vector2{strip_x + 148, y + 78}
			rl.DrawLineEx(a, b, 26, cc)
			rl.DrawLineEx(a, b, 20, neutral)
			vocab_shape({strip_x + 34, y + 78}, r_dist, row.color, outline, cand.shape)
			vocab_shape({strip_x + 84, y + 78}, r_dist, row.color, outline, cand.shape)
			// candidate label
			rnd.draw_text_c(v, cand.label, i32(cx - 40), i32(y + 130), 14, ink)
			cx += f32(430)
		}

		// block separator
		rl.DrawLineEx({20, y + bh - 14}, {1260, y + bh - 14}, 1, soft)
		y += bh
	}

	rnd.draw_text_c(v, "geometry: pinned tables (RSQ12/HEX6/PILL16/STAR10/BLOB16 + prior draw_shape_ext + shipped draw_packet_shape) — no transcendentals", 20, i32(y + 4), 13, soft)

	img := rl.LoadImageFromScreen()
	rl.ImageFlipVertical(&img) // framebuffer readback is bottom-up (the T2 spine's normalization)
	swizzle_rb(&img)           // rlsw framebuffer is BGRA
	out := fmt.tprintf("%s/vocab-sheet.png", outdir)
	rl.ExportImage(img, strings.clone_to_cstring(out, context.temp_allocator))
	rl.UnloadImage(img)
	fmt.eprintfln("wrote %s", out)
}

swizzle_rb :: proc(img: ^rl.Image) {
	px := rl.LoadImageColors(img^)
	n := int(img.width) * int(img.height)
	for i in 0..<n {
		px[i].r, px[i].b = px[i].b, px[i].r
	}
	new_img: rl.Image
	new_img.data = raw_data(px)
	new_img.width = img.width
	new_img.height = img.height
	new_img.mipmaps = 1
	new_img.format = .UNCOMPRESSED_R8G8B8A8
	rl.UnloadImage(img^)
	img^ = new_img
}
