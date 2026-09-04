package vocab_capture

// fork_sheet.odin — the SILHOUETTE-COUNT FORK strips (user annotation 2026-08-28:
// "what if they are all the same pill shape but different colours. the different
// shapes seems noisy."). Three options rendered through the real renderer:
//   S1 — ONE uniform pill body, 9 class colors (the annotation's proposal);
//   S2 — THREE shape families by the GDD's own 3-lane DiffServ temperament
//        (Best-effort {email,iot,ai} = circle / Standard {streaming,web,voice}
//        = triangle / Express {gaming,banking} = chevron-dart), class color
//        within the family (email circle + streaming triangle survive shipped);
//   S3 — the NINE-shape canon roster (the menu as served).
// Read at DISTRIBUTION size (r 13.6) on a neutral rider band — the at-a-glance
// in-play scale. READ-ONLY scratch, never committed.

import "core:fmt"
import rl "vendor:raylib"
import pp "../../../../packet-plumber/core"
import rnd "../../../../packet-plumber/app/render"

Fork_Class :: struct {
	name:  string,
	shape: string, // vocab_shape name
	col:   rl.Color,
}

fork_sheet :: proc(rc: ^Render_Ctx, cat: ^pp.Catalogs, outdir: string) {
	v := &rc.view
	p := &rc.palette
	_ = cat
	rl.ClearBackground(p.canvas)

	ink := p.ink
	soft := p.ink_soft

	email := rl.Color{90, 98, 112, 255}
	streaming := rl.Color{30, 74, 152, 255}
	web := rl.Color{176, 122, 82, 255}
	gaming := rl.Color{55, 214, 122, 255}
	banking := rl.Color{245, 200, 66, 255}
	voice := rl.Color{157, 123, 224, 255}
	multicast := rl.Color{255, 158, 61, 255}
	iot := rl.Color{54, 197, 216, 255}
	ai := rl.Color{240, 98, 146, 255}

	r := f32(26.0 * 1.4 * 0.24 * 1.35 * 1.15) // DISTRIBUTION r 13.55

	outline_of :: proc(c: rl.Color) -> rl.Color {
		return rl.Color{u8(f32(c.r) * 0.55), u8(f32(c.g) * 0.55), u8(f32(c.b) * 0.55), 255}
	}

	// one rider band with shapes+labels along it
	band :: proc(v: ^rnd.View, p: ^rnd.Palette, ink, soft: rl.Color, y: f32, r: f32, items: []Fork_Class, group_labels: [][]string) {
		neutral := mix_col(p.canvas, p.pipe_steel, 0.55)
		cc := casing_color(p, neutral)
		rl.DrawLineEx({40, y}, {1240, y}, 26, cc)
		rl.DrawLineEx({40, y}, {1240, y}, 20, neutral)
		n := len(items)
		for it, i in items {
			x := 40.0 + f32(i+1) * (1200.0 / f32(n+1))
			vocab_shape({x, y}, r, it.col, outline_of(it.col), it.shape)
			rnd.draw_text_c(v, it.name, i32(x) - 34, i32(y + 30), 13, soft)
		}
		if len(group_labels) > 0 {
			rnd.draw_text_c(v, group_labels[0][0], 48, i32(y - 44), 13, ink)
		}
	}

	rnd.draw_text_c(v, "THE SILHOUETTE-COUNT FORK — one axis, three options (rendered at DISTRIBUTION size r 13.6 on a rider band; canon §5.1 colors, illustrative)", 20, 16, 17, ink)

	// S1 — uniform pill
	rnd.draw_text_c(v, "S1 · ONE BODY (the annotation: same pill, different colours) — calmest; class = color ONLY", 20, 52, 15, ink)
	s1 := [9]Fork_Class{
		{"email", "pill", email}, {"streaming", "pill", streaming}, {"web", "pill", web},
		{"gaming", "pill", gaming}, {"banking", "pill", banking}, {"voice", "pill", voice},
		{"multicast", "pill", multicast}, {"iot", "pill", iot}, {"ai", "pill", ai},
	}
	band(v, p, ink, soft, 140, r, s1[:], nil)

	// S2 — three families by the GDD's 3-lane temperament
	rnd.draw_text_c(v, "S2 · THREE FAMILIES (GDD's own 3-lane collapse: shape = temperament, color = class) — MM-calm + CVD-safe spine", 20, 212, 15, ink)
	s2 := [9]Fork_Class{
		{"email", "circle", email}, {"iot", "circle", iot}, {"ai", "circle", ai},
		{"streaming", "triangle", streaming}, {"web", "triangle", web}, {"voice", "triangle", voice},
		{"multicast", "triangle", multicast},
		{"gaming", "chevron", gaming}, {"banking", "chevron", banking},
	}
	band(v, p, ink, soft, 300, r, s2[:], [][]string{{"BEST-EFFORT · tolerant — safe to shed      |      STANDARD · steady — may buffer      |      EXPRESS · fragile — never drop/lag"}})

	// S3 — nine shapes
	rnd.draw_text_c(v, "S3 · NINE SHAPES (the menu as served; canon roster) — max per-class affordance, the noisiest", 20, 372, 15, ink)
	s3 := [9]Fork_Class{
		{"email", "circle", email}, {"streaming", "triangle", streaming}, {"web", "rounded_square", web},
		{"gaming", "diamond", gaming}, {"banking", "hexagon", banking}, {"voice", "pill", voice},
		{"multicast", "star", multicast}, {"iot", "tiny_square", iot}, {"ai", "blob", ai},
	}
	band(v, p, ink, soft, 460, r, s3[:], nil)

	rnd.draw_text_c(v, "the measured wall behind this fork: 9-way distinct color fails CVD (Machado 1.0, T=48 — search caps at ~5 anchors) — on S1 some pairs collapse exactly where it hurts (banking never-drops vs email drop-freely); S2 asks color for only 3-way within-family reads", 20, 560, 13, soft)
	rnd.draw_text_c(v, "geometry: pinned tables through the real render package (rlsw) — same evidence chain as the per-class sheet", 20, 582, 13, soft)

	img := rl.LoadImageFromScreen()
	rl.ImageFlipVertical(&img)
	swizzle_rb(&img)
	out := fmt.tprintf("%s/fork-sheet.png", outdir)
	rl.ExportImage(img, strings_clone_cstr_local(out))
	rl.UnloadImage(img)
	fmt.eprintfln("wrote %s", out)
}

strings_clone_cstr_local :: proc(s: string) -> cstring {
	buf := make([^]u8, len(s) + 1)
	copy(buf[:len(s)], s)
	buf[len(s)] = 0
	return cstring(buf)
}
