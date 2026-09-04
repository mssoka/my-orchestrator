package vocab_capture

// main.odin — MINIMAL evidence harness for the shape-vocab candidate sheet.
// Modeled on the sibling link-vocab capture tool's plumbing, stripped to what
// vocab_sheet needs (the link-direction mock machinery drifted against v2 HEAD
// when the zoom-language revamp removed lane stripes — none of it is needed
// here). READ-ONLY scratch, never committed; run from the repo root.
//
// Usage: vocab-capture <outdir> vocab

import "core:fmt"
import "core:os"
import rl "vendor:raylib"
import pp "../../../../packet-plumber/core"
import rnd "../../../../packet-plumber/app/render"

load_catalogs :: proc(cat: ^pp.Catalogs) -> string {
	src: pp.Catalog_Sources
	nt, e1 := os.read_entire_file_from_path("data/node_types.json", context.temp_allocator)
	if e1 != nil { return fmt.tprintf("cannot read data/node_types.json: %v", e1) }
	pt, e2 := os.read_entire_file_from_path("data/pipe_tiers.json", context.temp_allocator)
	if e2 != nil { return fmt.tprintf("cannot read data/pipe_tiers.json: %v", e2) }
	bal, e3 := os.read_entire_file_from_path("data/balance.json", context.temp_allocator)
	if e3 != nil { return fmt.tprintf("cannot read data/balance.json: %v", e3) }
	pkt, e4 := os.read_entire_file_from_path("data/packet_types.json", context.temp_allocator)
	if e4 != nil { return fmt.tprintf("cannot read data/packet_types.json: %v", e4) }
	dem, e5 := os.read_entire_file_from_path("data/demand.json", context.temp_allocator)
	if e5 != nil { return fmt.tprintf("cannot read data/demand.json: %v", e5) }
	era, e7 := os.read_entire_file_from_path("data/eras.json", context.temp_allocator)
	if e7 != nil { return fmt.tprintf("cannot read data/eras.json: %v", e7) }
	cris, e6 := os.read_entire_file_from_path("data/crises.json", context.temp_allocator)
	if e6 != nil { return fmt.tprintf("cannot read data/crises.json: %v", e6) }
	src.node_types = nt
	src.pipe_tiers = pt
	src.balance = bal
	src.packet_types = pkt
	src.demand = dem
	src.eras = era
	src.crises = cris
	cerr := pp.catalogs_load(cat, &src)
	if cerr.file != "" {
		return pp.catalog_error_string(cerr)
	}
	return ""
}

Render_Ctx :: struct {
	palette: rnd.Palette,
	view:    rnd.View,
	ready:   bool,
}

render_setup :: proc(rc: ^Render_Ctx, cat: ^pp.Catalogs) {
	rc.palette = rnd.palette_load()
	rc.view.palette = &rc.palette
	rc.view.catalogs = cat
	if !rnd.load_fonts(&rc.view) {
		fmt.eprintln("vocab-capture: HUD font family failed to load (assets/fonts) — refusing to capture with the raylib default")
		os.exit(2)
	}
	rnd.view_compute(&rc.view, 1280, 1560, &cat.balance)
	rc.view.route_wires = false
	rc.view.wire_anchors = false
	rc.ready = true
}

main :: proc() {
	args := os.args
	if len(args) < 3 {
		fmt.eprintln("usage: vocab-capture <outdir> vocab")
		os.exit(1)
	}
	outdir := args[1]
	variant := args[2]
	if variant != "vocab" && variant != "forks" {
		fmt.eprintln("vocab-capture: variants are 'vocab' | 'forks'")
		os.exit(1)
	}

	cat: pp.Catalogs
	if e := load_catalogs(&cat); e != "" {
		fmt.eprintfln("vocab-capture: %s", e)
		os.exit(2)
	}
	defer pp.catalogs_destroy(&cat)

	rl.SetTraceLogLevel(.ERROR)
	win_h := i32(1560)
	if variant == "forks" { win_h = 640 }
	rl.InitWindow(1280, win_h, "pp-vocab-capture")
	defer rl.CloseWindow()

	rc: Render_Ctx
	render_setup(&rc, &cat)

	for present in 0..<2 {
		rl.BeginDrawing()
		if variant == "forks" {
			fork_sheet(&rc, &cat, outdir)
		} else {
			vocab_sheet(&rc, &cat, outdir)
		}
		rl.EndDrawing()
	}
}
