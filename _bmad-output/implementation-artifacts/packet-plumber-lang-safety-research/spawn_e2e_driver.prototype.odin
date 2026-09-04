// PP_SPAWN_E2E — the scripted app-driver prototype (lang-safety-research P2 seed).
// Env-gated (PP_SPAWN_E2E=1) frame-script that drives the REAL input pipeline:
// places routers, waits for growth-spawned terminals, drag-connects each
// (press on terminal -> move/release on router) — the playtest surface as a
// gate. This caught the box crash RED and proved the fix GREEN (8 connects).
// Wiring (3 hunks): this block before handle_input; `spawn_e2e.on = os.get_env_alloc("PP_SPAWN_E2E", context.allocator) != ""` at boot; `spawn_e2e_inject(&app... app, ictx)` in handle_input after the cam_e2e injection. USER ruling: nightly windowed mac runner.
// --- PP_SPAWN_E2E (lang-safety-research repro copy ONLY — never ships) ------
// Drives the REAL input pipeline: places routers, waits for growth-spawned
// terminals, connects each with a real drag (press-on-node → move → release),
// like the user's playtest. Env-gated: PP_SPAWN_E2E=1.
Spawn_E2E :: struct {
	on:       bool,
	frame:    int,
	stage:    int, // 0 settle, 1 router-press, 2 router-release, 3 hunt, 4 move, 5 release, 6 done
	fixture:  u32,
	routers:  [dynamic]u32,
	tile:     [2]i32,
	term:     u32,
	router_to: u32,
	connects: int,
	placed:   int,
}

spawn_e2e : Spawn_E2E

spawn_e2e_tile_screen :: proc(app: ^App, tx, ty: i32) -> rl.Vector2 {
	px := f32(app.cat.balance.tile_px)
	return rnd.to_screen(&app.view, f32(tx)*px + px*0.5, f32(ty)*px + px*0.5)
}

spawn_e2e_node_screen :: proc(app: ^App, id: u32) -> rl.Vector2 {
	ps, ok := pp.node_slot(&app.state.topology, id)
	if !ok { return {0, 0} }
	return rnd.node_screen(&app.view, app.state.topology.node_pos[ps])
}

spawn_e2e_find_tile :: proc(app: ^App, near: [2]i32) -> ([2]i32, bool) {
	// spiral out from `near` for a validate_place-OK tile within standard span
	std, _ := pp.pipe_tier_index(&app.cat, "standard")
	maxs := i32(app.cat.pipe_tiers[std].max_span)
	for r in 0 ..< maxs {
		for dy in -r ..= r {
			for dx in -r ..= r {
				if max(i32(dx < 0 ? -dx : dx), i32(dy < 0 ? -dy : dy)) != r { continue }
				tx, ty := near[0] + dx, near[1] + dy
				cmd := pp.Cmd_Place_Router{type_idx = 0, pos = {tx, ty}}
				// node-type idx patched by caller context; use a found junction idx
				for nt, i in app.cat.node_types {
					if nt.kind != .Junction { continue }
					cmd.type_idx = u16(i)
					if pp.validate_place(&app.state.topology, cmd, &app.cat) == .None {
						if pp.span_between({tx, ty}, near) <= maxs {
							return {tx, ty}, true
						}
					}
				}
			}
		}
	}
	return {}, false
}

spawn_e2e_inject :: proc(app: ^App, ictx: ^inp.Input) {
	if !spawn_e2e.on { return }
	sp := &spawn_e2e
	sp.frame += 1
	f := sp.frame
	logf :: proc(fr: int, s: string) { fmt.eprintfln("SPAWN_E2E[f=%d] %s", fr, s) }

	if sp.fixture == 0 {
		n: u32 = 0
		for alive in app.state.topology.node_alive {
			if alive { n += 1 }
		}
		sp.fixture = n
		logf(f, fmt.aprintf("baseline fixture nodes=%d", n))
		return
	}

	switch sp.stage {
	case 0:
		if f >= 60 {
			// pick the first router tile near map center
			if t, ok := spawn_e2e_find_tile(app, {16, 12}); ok {
				sp.tile = t
				idx := -1
				for nt, i in app.cat.node_types {
					if nt.id == "router_basic" { idx = i }
				}
				ictx.placing = i32(idx)
				p := spawn_e2e_tile_screen(app, t[0], t[1])
				append(&ictx.events, inp.Device_Event(inp.Mouse_Press{pos = p, button = .Left}))
				logf(f, fmt.aprintf("placement press at tile %v", t))
				sp.stage = 1
			}
		}
	case 1:
		p := spawn_e2e_tile_screen(app, sp.tile[0], sp.tile[1])
		append(&ictx.events, inp.Device_Event(inp.Mouse_Release{pos = p, button = .Left}))
		for i in 0 ..< len(app.state.topology.node_alive) {
			if !app.state.topology.node_alive[i] { continue }
			if app.state.topology.node_id[i] < sp.fixture { continue }
			if app.cat.node_types[app.state.topology.node_type[i]].kind == .Junction {
				append(&sp.routers, app.state.topology.node_id[i])
			}
		}
		if len(sp.routers) == 0 {
			logf(f, fmt.aprintf("router placement FAILED last_reject=%v alive=%d placing=%d dragactive=%v dragvalid=%v", ictx.last_reject, len(app.state.topology.node_alive), ictx.placing, ictx.drag.active, ictx.drag.valid))
			sp.stage = 0 // retry next beat
			sp.frame = 30
			return
		}
		if len(sp.routers) > 0 {
			sp.placed += 1
			logf(f, fmt.aprintf("router placed id=%d (total junctions %d)", sp.routers[len(sp.routers)-1], len(sp.routers)))
			sp.stage = 2
		} else {
			logf(f, fmt.aprintf("router placement FAILED last_reject=%v alive=%d placing=%d dragactive=%v", ictx.last_reject, len(app.state.topology.node_alive), ictx.placing, ictx.drag.active))
			sp.stage = 0
			sp.frame = 30
		}
	case 2: // hunt for the next unconnected spawned terminal
		ictx.placing = -1 // the placement release has landed by now
		if f % 30 != 0 { return } // poll every half second
		std, _ := pp.pipe_tier_index(&app.cat, "standard")
		maxs := i32(app.cat.pipe_tiers[std].max_span)
		best_id: u32 = 0
		best_span: i32 = 0x7fffffff
		found := false
		for i in 0 ..< len(app.state.topology.node_alive) {
			if !app.state.topology.node_alive[i] { continue }
			id := app.state.topology.node_id[i]
			if id < sp.fixture { continue }
			if app.cat.node_types[app.state.topology.node_type[i]].kind != .Terminal { continue }
			// connected already? any live incident pipe
			has_pipe := false
			for pi in 0 ..< len(app.state.topology.pipe_alive) {
				if !app.state.topology.pipe_alive[pi] { continue }
				_, is_end := pp.pipe_other(&app.state.topology, u32(pi), id)
				if is_end { has_pipe = true }
			}
			if has_pipe { continue }
			tpos := app.state.topology.node_pos[i]
			for r in sp.routers {
				rs, _ := pp.node_slot(&app.state.topology, r)
				s := i32(pp.span_between(tpos, app.state.topology.node_pos[rs]))
				if s < best_span {
					best_span, best_id, found = s, id, true
				}
			}
		}
		if !found {
			if f > 5400 { // ~90 s with no more spawns — done
				logf(f, fmt.aprintf("DONE connects=%d routers=%d", sp.connects, sp.placed))
				os.exit(0)
			}
			return
		}
		if best_span > maxs {
			// out of span of every router — place a new router near it first
			ps_, _ := pp.node_slot(&app.state.topology, best_id)
			if t, ok := spawn_e2e_find_tile(app, app.state.topology.node_pos[ps_]); ok {
				sp.tile = t
				idx := -1
				for nt, i in app.cat.node_types {
					if nt.id == "router_basic" { idx = i }
				}
				ictx.placing = i32(idx)
				p := spawn_e2e_tile_screen(app, t[0], t[1])
				append(&ictx.events, inp.Device_Event(inp.Mouse_Press{pos = p, button = .Left}))
				sp.stage = 1
				sp.term = best_id
				logf(f, fmt.aprintf("out-of-span (span=%d) — placing router near terminal %d at %v", best_span, best_id, t))
			}
			return
		}
		sp.term = best_id
		sp.router_to = 0
		ps_, _ := pp.node_slot(&app.state.topology, best_id)
		tpos := app.state.topology.node_pos[ps_]
		bs: i32 = 0x7fffffff
		for r in sp.routers {
			rs, _ := pp.node_slot(&app.state.topology, r)
			s := i32(pp.span_between(tpos, app.state.topology.node_pos[rs]))
			if s < bs { bs = s; sp.router_to = r }
		}
		p := spawn_e2e_node_screen(app, best_id)
		append(&ictx.events, inp.Device_Event(inp.Mouse_Press{pos = p, button = .Left}))
		logf(f, fmt.aprintf("drag press on terminal %d (span=%d, connect #%d, router %d)", best_id, best_span, sp.connects + 1, sp.router_to))
		sp.stage = 3
	case 3:
		p := spawn_e2e_node_screen(app, sp.router_to)
		append(&ictx.events, inp.Device_Event(inp.Mouse_Move{pos = p}))
		sp.stage = 4
	case 4:
		p := spawn_e2e_node_screen(app, sp.router_to)
		append(&ictx.events, inp.Device_Event(inp.Mouse_Release{pos = p, button = .Left}))
		sp.connects += 1
		logf(f, fmt.aprintf("release — connect #%d (terminal %d)", sp.connects, sp.term))
		if sp.connects >= 8 {
			logf(f, fmt.aprintf("DONE connects=%d routers=%d — NO CRASH", sp.connects, sp.placed))
			os.exit(0)
		}
		sp.stage = 2
	case:
	}
}

