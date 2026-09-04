You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)

--- DIFF ---
diff --git a/app/render/crisis.odin b/app/render/crisis.odin
index 727e1c6c..291844d3 100644
--- a/app/render/crisis.odin
+++ b/app/render/crisis.odin
@@ -66,6 +66,202 @@ crisis_banner_rect :: proc(v: ^View, crisis: ^pp.Crisis_State, y_base: i32) -> (
 	return {f32(x - pad), f32(y_base - pad), f32(card_w + 2 * pad), f32(h)}, true
 }
 
+// v2-viscomm-crisis-duck (user design ruling 2026-08-25, viscomm audit
+// finding C): CRISIS-TIME DESATURATION of the non-involved network. When
+// everything screams, nothing reads as urgent — during an active crisis the
+// non-involved network elements recede toward the board's calm register
+// (the canvas paper), so the crisis zone is the ONLY saturated thing on the
+// board. This reuses the v2-network-pop mechanism dynamically: vibrant
+// network on calm paper, INVERTED under crisis (the non-involved network
+// joins the paper).
+//
+// Contracts (the briefing's, pinned by tests + palcheck section 7):
+// - RENDER-SIDE ONLY, pure derivation: the factor is a pure function of
+//   (crisis rows, tick) — NO app-fed View state (unlike the gauges, the
+//   harness capture path must render it: crisis goldens carry the desat).
+// - BYTE-IDENTICAL WHEN INERT: zero active crises => factor exactly 0 and
+//   every recede call is a passthrough guard — every inert render is
+//   byte-identical to pre-change (the wire-aesthetics standard).
+// - Involvement (the final predicate, named in the PR): a BUNDLE is involved
+//   iff it is the named canonical (bundle_lo, bundle_hi) pair of an active
+//   Saturated_Bundle crisis; a NODE iff it is an endpoint of an involved
+//   bundle; a PACKET iff it rides an involved bundle (on-edge) or sits at an
+//   involved node (at-node). Pool_Exhaustion is map-wide — the whole network
+//   IS the crisis zone, so nothing recedes.
+// - NEVER recede: the state triad / warning halos / health rings / the
+//   crisis outline / the banner (the telegraph family stays live), the drag
+//   ghost, selection/spawn/route-assist surfaces, and the router LED (the
+//   alive semantic, sub-pixel). Only the network IDENTITY colors recede:
+//   tier bands + casings + lane stripes, packet bodies, family washes +
+//   chip glyphs, router tier washes/rings.
+// - Reduced-motion (7.3/E9.2): the TRANSITION is pinned — factor reads 1.0
+//   while any crisis is active (the static desat itself is NOT gated; only
+//   its ramp is motion).
+// - Engage: eased over 16 ticks from the EARLIEST active onset (a later
+//   overlapping onset never resets the phase). Resolve: INSTANT snap-back
+//   to 0 — the color flood IS the "you fixed it" relief read, and it
+//   guarantees resolved captures return to the canon bytes exactly
+//   (surge@119500ms stays blessed; documented in the PR's Decisions).
+
+// CRISIS_DESAT_MIX — the recede depth: the fraction of the way a
+// non-involved color travels toward the canvas paper at full engagement
+// (the briefing's 60-75% range, pinned at 65%). Plain arithmetic lerp —
+// NO transcendentals in the draw path (§10.4).
+CRISIS_DESAT_MIX :: f32(0.65)
+
+// CRISIS_FADE16 — the pinned 16-entry engage ramp (the PULSE16/EASE16
+// pattern: a precomputed ease-out, indexed by a tick-derived integer
+// phase). [0] == 0 pins engage-start continuity; [15] == 1 pins EXACT full
+// engagement (a finished ramp reads the static mix to the byte). One table
+// entry per tick = a 16-tick engage = 0.8 s at 20 Hz logic.
+CRISIS_FADE16 :: [16]f32{
+	0.000, 0.129, 0.249, 0.360, 0.462, 0.556, 0.640, 0.716,
+	0.782, 0.840, 0.889, 0.929, 0.960, 0.982, 0.996, 1.000,
+}
+
+// compile-time integrity pins (the `when <bad> { BROKEN :: 1/0 }` idiom).
+when CRISIS_FADE16[0] != 0.0 {
+	CRISIS_FADE16_START_BROKEN :: 1 / 0
+}
+when CRISIS_FADE16[len(CRISIS_FADE16) - 1] != 1.0 {
+	CRISIS_FADE16_END_BROKEN :: 1 / 0
+}
+when CRISIS_DESAT_MIX <= 0.0 || CRISIS_DESAT_MIX >= 1.0 {
+	CRISIS_DESAT_MIX_BROKEN :: 1 / 0
+}
+
+// crisis_desat_factor — the ONE desat derivation seam (the
+// interp_alpha_from_accum doctrine: a default param or an inline copy is
+// bypassable; every consumer reads this). Pure function of the serialized
+// crisis rows + the tick — the harness renders it from sim state alone
+// (no app feeding, ODN-1: presentation reads immutable snapshots only).
+crisis_desat_factor :: proc(v: ^View, crisis: ^pp.Crisis_State, tick: u64) -> f32 {
+	if len(crisis.active) == 0 {
+		return 0 // the inert contract: byte-identical render, no exceptions
+	}
+	// ONLY a Saturated_Bundle crisis carves a crisis ZONE. A Pool_Exhaustion
+	// row is map-wide (the whole network IS the flaw — the empirical dublin
+	// golden proved the era-3 growth scene fires one at 90s): with no
+	// non-involved network, receding everything would desaturate the very
+	// packet-pile evidence of the crisis — so a pool-only crisis engages
+	// NOTHING (the pool gauge's SHEDDING tag + the banner carry it).
+	earliest := u64(0)
+	found := false
+	for ac in crisis.active {
+		if ac.kind != .Saturated_Bundle {
+			continue
+		}
+		if !found || ac.triggered_tick < earliest {
+			earliest = ac.triggered_tick
+			found = true
+		}
+	}
+	if !found {
+		return 0 // pool-only (or unknown-kind) active rows: no zone, no recede
+	}
+	// 7.3/E9.2 (review r1 blocker fix): pin the RAMP only — and only now that
+	// a zone exists. The first cut returned 1 on reduced_motion BEFORE the
+	// pool carve-out, so a reduced-motion player in a pool-only crisis
+	// desaturated the whole map (the packet-pile evidence of the very
+	// crisis) — the a11y_reduced golden never caught it because its frame is
+	// a Saturated_Bundle one.
+	if v.reduced_motion {
+		return 1
+	}
+	if tick <= earliest {
+		return CRISIS_FADE16[0] // 0.0 — defensive (the trigger tick itself)
+	}
+	phase := tick - earliest
+	if phase >= u64(len(CRISIS_FADE16)) {
+		return CRISIS_FADE16[len(CRISIS_FADE16) - 1] // fully engaged
+	}
+	table := CRISIS_FADE16 // local copy — a constant can't be indexed by a runtime index
+	return table[int(phase)]
+}
+
+// crisis_bundle_involved — is this bundle (by canonical pair — the B1-stable
+// identity, never the compaction-prone slot) the named bottleneck of an
+// active Saturated_Bundle crisis? Pool_Exhaustion rows name no bundle (the
+// whole network is the flaw) — they involve nothing here, so a pool-only
+// crisis desaturates nothing.
+crisis_bundle_involved :: proc(crisis: ^pp.Crisis_State, lo, hi: u32) -> bool {
+	for ac in crisis.active {
+		if ac.kind == .Saturated_Bundle && ac.bundle_lo == lo && ac.bundle_hi == hi {
+			return true
+		}
+	}
+	return false
+}
+
+// crisis_node_involved — is this node an endpoint of an involved bundle?
+crisis_node_involved :: proc(crisis: ^pp.Crisis_State, node_id: u32) -> bool {
+	for ac in crisis.active {
+		if ac.kind != .Saturated_Bundle {
+			continue
+		}
+		if ac.bundle_lo == node_id || ac.bundle_hi == node_id {
+			return true
+		}
+	}
+	return false
+}
+
+// crisis_packet_involved — is this packet in the crisis zone? (on-edge:
+// its pipe's bundle is the named pair; at-node: it sits at an endpoint).
+// Extracted from draw_packets at review r1 so the CHAIN (pipe_slot ->
+// pipe_bundle -> canonical pair) is unit-pinnable — the pixel pin covers
+// the wiring, this covers the resolution.
+crisis_packet_involved :: proc(crisis: ^pp.Crisis_State, topo: ^pp.Topology, bundles: ^pp.Bundles, p: ^pp.Packet) -> bool {
+	if p.on_edge {
+		bslot, ok := pp.pipe_slot(topo, p.edge)
+		if !ok || int(bslot) >= len(bundles.pipe_bundle) || bundles.pipe_bundle[bslot] == pp.NO_BUNDLE {
+			return false
+		}
+		bi := bundles.pipe_bundle[bslot]
+		if int(bi) >= len(bundles.bundle_lo) || int(bi) >= len(bundles.bundle_hi) {
+			return false
+		}
+		return crisis_bundle_involved(crisis, bundles.bundle_lo[bi], bundles.bundle_hi[bi])
+	}
+	return crisis_node_involved(crisis, p.at_node)
+}
+
+// crisis_recede — the color mix: `col` travels CRISIS_DESAT_MIX * f of the
+// way toward the canvas paper (the board's calm register — a canvas mix,
+// not a gray mix: gray pipes would read COLDER than the warm board and
+// stick out the other way; hue families survive at reduced chroma). The
+// alpha byte passes through untouched (fills alpha-blend in rlsw; alpha is
+// the wash layers' own strength — see crisis_recede_scale). f == 0 is a
+// guarded passthrough: the inert render is BYTE-identical, not
+// float-identical (the wire-aesthetics standard).
+crisis_recede :: proc(v: ^View, f: f32, col: rl.Color) -> rl.Color {
+	if f <= 0 {
+		return col
+	}
+	k := CRISIS_DESAT_MIX * f
+	if k >= 1 {
+		k = 1
+	}
+	c := v.palette.canvas
+	return rl.Color{
+		u8(f32(col.r) * (1.0 - k) + f32(c.r) * k),
+		u8(f32(col.g) * (1.0 - k) + f32(c.g) * k),
+		u8(f32(col.b) * (1.0 - k) + f32(c.b) * k),
+		col.a,
+	}
+}
+
+// crisis_recede_scale — the ALPHA-layer twin (family washes, tier markers,
+// chip glyphs): the recede fades the accent's strength by the same budget
+// (a wash at 35% strength reads receded without touching the sprite bytes
+// beneath — the baked sprites are already the board's muted paper tones).
+crisis_recede_scale :: proc(f: f32) -> f32 {
+	if f <= 0 {
+		return 1
+	}
+	return max(0, 1 - CRISIS_DESAT_MIX * f)
+}
+
 // draw_crisis_banner — the top-center crisis card (clear of the top-left run
 // HUD + the top-right forecast panel). One title line + one redesign line per
 // active crisis; catalog display strings throughout (a future archetype
@@ -73,6 +269,7 @@ crisis_banner_rect :: proc(v: ^View, crisis: ^pp.Crisis_State, y_base: i32) -> (
 // is empty (the capture-stability contract). `y_base` places the card (the
 // 4.3 meter card sits at y=10, so the banner drops below it when the meter
 // is live).
+
 draw_crisis_banner :: proc(v: ^View, crisis: ^pp.Crisis_State, cat: ^pp.Catalogs, era: u8, y_base: i32 = 10) {
 	if len(crisis.active) == 0 {
 		return
diff --git a/app/render/dublin.odin b/app/render/dublin.odin
index 7f408f99..bd3ecbd0 100644
--- a/app/render/dublin.odin
+++ b/app/render/dublin.odin
@@ -335,7 +335,7 @@ dublin_draw_attribution :: proc(v: ^View, b: ^pp.Map_Board) {
 // nearest street segment, family-washed, with the type chip riding the
 // top. `c` is the node's screen center; `reveal` scales the spawn reveal.
 // Returns the block's screen-space top y (the chip anchor).
-dublin_node_block_draw :: proc(v: ^View, c: rl.Vector2, fam: rl.Color, reveal_scale: f32) -> f32 {
+dublin_node_block_draw :: proc(v: ^View, c: rl.Vector2, fam: rl.Color, reveal_scale: f32, recede: f32 = 0.0) -> f32 {
 	tx, ty := dublin_screen_tile(v, c.x, c.y)
 	dx, dy, _d2, found := dublin_node_street(v, tx, ty)
 	if !found {
@@ -355,12 +355,20 @@ dublin_node_block_draw :: proc(v: ^View, c: rl.Vector2, fam: rl.Color, reveal_sc
 		{c.x + dx * hl - px * hw, c.y + dy * hl - py * hw},
 		{c.x - dx * hl - px * hw, c.y - dy * hl - py * hw},
 	}
-	// two CCW triangles (rlgl front face — the 08-23 field note)
-	col := fam
+	// two CCW triangles (rlgl front face — the 08-23 field note). The
+	// recede rides the RGB MIX like the frontage edge below — the alpha
+	// twin alone was INERT under rlsw (triangles render opaque there, the
+	// Perkins r1 B1 probe: deleting it kept the corpus green; the GPU app
+	// would have blended it, a silent renderer divergence).
+	col := crisis_recede(v, recede, fam)
+	col.a = u8(f32(fam.a) * crisis_recede_scale(recede))
 	rl.DrawTriangle(q[2], q[1], q[0], col)
 	rl.DrawTriangle(q[0], q[3], q[2], col)
-	// the street-facing edge line (the block's frontage read)
-	edge := fam
+	// the street-facing edge line (the block's frontage read). The recede
+	// rides the RGB mix (crisis_recede), NOT an alpha scale — line-alpha is
+	// inert under rlsw (the in-repo canon; a scale-only recede was a GPU-app
+	// no-op in the goldens — Perkins r1 N2).
+	edge := crisis_recede(v, recede, fam)
 	edge.a = 90
 	rl.DrawLineEx({q[0].x, q[0].y}, {q[1].x, q[1].y}, 1.5 * v.scale, edge)
 	// the block's top edge (screen-space) — the chip anchor
diff --git a/app/render/palette_polish_test.odin b/app/render/palette_polish_test.odin
index 040276d5..1f7dc0b3 100644
--- a/app/render/palette_polish_test.odin
+++ b/app/render/palette_polish_test.odin
@@ -12,9 +12,13 @@ package render
 //
 // Run: odin test app/render
 
+import "core:fmt"
+import "core:os"
 import "core:testing"
 import rl "vendor:raylib"
 
+import pp "../../core"
+
 @(test)
 casing_color_is_opaque_darker_and_deterministic :: proc(t: ^testing.T) {
 	p := palette_load()
@@ -240,3 +244,209 @@ fmt_tok :: proc(i: int) -> string {
 	case:    return "router_tier_high"
 	}
 }
+
+// --- v2-viscomm-crisis-duck: the crisis desaturation pins (2026-08-25) -----
+// The factor/predicate/mix procs are the desat's contract surface; the draw
+// path + the pixel truth live in palcheck section 7 (the vacuous-pin
+// doctrine: these pin the PURE procs, palcheck pins what RENDERS).
+
+@(test)
+crisis_desat_factor_purity :: proc(t: ^testing.T) {
+	v: View
+	cr: pp.Crisis_State
+	defer delete(cr.active)
+	// INERT: no rows -> exactly 0 (the byte-identity contract)
+	testing.expect(t, crisis_desat_factor(&v, &cr, 999) == 0, "no active crises must read exactly 0")
+	// POOL-ONLY: map-wide crisis -> no zone -> 0 (the dublin lesson: a pool
+	// crisis must not desaturate the packet-pile evidence of itself)
+	append(&cr.active, pp.Active_Crisis{kind = .Pool_Exhaustion, triggered_tick = 100})
+	testing.expect(t, crisis_desat_factor(&v, &cr, 999) == 0, "a pool-only crisis carves no zone")
+	// SATURATED BUNDLE: the pinned ramp from the earliest onset
+	append(&cr.active, pp.Active_Crisis{kind = .Saturated_Bundle, bundle_lo = 10, bundle_hi = 12, triggered_tick = 100})
+	testing.expect(t, crisis_desat_factor(&v, &cr, 100) == 0, "the trigger tick itself reads the table start (0.0)")
+	testing.expect(t, crisis_desat_factor(&v, &cr, 103) == CRISIS_FADE16[3], "mid-ramp reads the table entry")
+	testing.expect(t, crisis_desat_factor(&v, &cr, 115) == CRISIS_FADE16[15], "phase 15 is the last table entry")
+	testing.expect(t, crisis_desat_factor(&v, &cr, 1000) == 1.0, "past the table: fully engaged (exact 1.0)")
+	// a LATER overlapping onset never resets the phase
+	append(&cr.active, pp.Active_Crisis{kind = .Saturated_Bundle, bundle_lo = 3, bundle_hi = 4, triggered_tick = 500})
+	testing.expect(t, crisis_desat_factor(&v, &cr, 1000) == 1.0, "a later onset does not reset the ramp")
+	// the earliest onset WINS even when appended last
+	append(&cr.active, pp.Active_Crisis{kind = .Saturated_Bundle, bundle_lo = 5, bundle_hi = 6, triggered_tick = 50})
+	testing.expect(t, crisis_desat_factor(&v, &cr, 60) == CRISIS_FADE16[10], "the earliest active onset drives the phase")
+	// REDUCED MOTION: pinned at 1.0 while any zone crisis is active (7.3/E9.2
+	// — the static desat is not gated, only its transition)
+	v.reduced_motion = true
+	testing.expect(t, crisis_desat_factor(&v, &cr, 51) == 1.0, "reduced motion pins the factor at 1.0")
+	// ...including on the trigger tick itself (instant, not ramped)
+	testing.expect(t, crisis_desat_factor(&v, &cr, 50) == 1.0, "reduced motion applies instantly at onset")
+	// THE REVIEW-r1 BLOCKER PIN: reduced motion must NOT bypass the pool
+	// carve-out — the first cut returned 1 here and a reduced-motion player
+	// in a pool-only crisis desaturated the whole map.
+	cr2: pp.Crisis_State
+	defer delete(cr2.active)
+	append(&cr2.active, pp.Active_Crisis{kind = .Pool_Exhaustion, triggered_tick = 100})
+	testing.expect(t, crisis_desat_factor(&v, &cr2, 999) == 0, "reduced motion + pool-only crisis carves no zone (the r1 blocker)")
+	testing.expect(t, crisis_desat_factor(&v, &cr2, 100) == 0, "reduced motion + pool-only on the trigger tick: still no zone")
+	v.reduced_motion = false
+	// BASIS-SWITCH SEMANTICS (pinned decision, review r1; two-row pin per
+	// Perkins r1 N8): when the earliest of overlapping zone crises resolves
+	// mid-ramp of a later one, the phase basis switches to the SURVIVING
+	// row's own onset — the factor DIPS to that row's ramp position (a
+	// partial-relief read for the crisis that ended), then re-ramps. Inherent
+	// to the pure rows+tick derivation (a monotone hold needs view-owned
+	// history, which the golden capture-path contract forbids); the TWO-ROW
+	// pin discriminates the dip itself, not just a lone row's phase.
+	cr3: pp.Crisis_State
+	defer delete(cr3.active)
+	append(&cr3.active, pp.Active_Crisis{kind = .Saturated_Bundle, bundle_lo = 1, bundle_hi = 2, triggered_tick = 500}) // A: earliest
+	append(&cr3.active, pp.Active_Crisis{kind = .Saturated_Bundle, bundle_lo = 5, bundle_hi = 6, triggered_tick = 504}) // B: later, still ramping
+	table3 := CRISIS_FADE16 // local copy — a constant can't be indexed by a runtime index
+	f_before := crisis_desat_factor(&v, &cr3, 508)
+	testing.expect(t, f_before == table3[8], "both live, mid-ramp: the earliest onset (A@500) drives phase 8")
+	// A resolves (the engine's resolve path drops ITS row — pop() would take
+	// B (the last); swap-remove A so the SURVIVING row is B@504)
+	cr3.active[0] = cr3.active[1]
+	pop(&cr3.active)
+	f_after := crisis_desat_factor(&v, &cr3, 509)
+	testing.expect(t, f_after == table3[5], "the tick after A resolves: the basis switches to B's own onset — phase 5, the DIP")
+	testing.expect(t, f_after < f_before, "the dip is real: the post-resolve factor is LOWER than pre-resolve")
+	testing.expect(t, crisis_desat_factor(&v, &cr3, 520) == 1.0, "and it still arrives at exact full")
+	// table integrity: monotone non-decreasing, starts 0, ends exact 1
+	table := CRISIS_FADE16 // local copy — a constant can't be indexed by a runtime index
+	for i in 1..<len(table) {
+		testing.expectf(t, table[i] >= table[i-1], "CRISIS_FADE16 must be monotone at %d", i)
+	}
+}
+
+@(test)
+crisis_recede_is_byte_identity_when_inert :: proc(t: ^testing.T) {
+	p := palette_load()
+	v: View
+	v.palette = &p
+	cols := []rl.Color{p.pipe_copper, p.pipe_steel, p.pipe_fiber, p.packet_dot, {186, 94, 232, 235}, {0, 0, 0, 0}, {255, 255, 255, 90}}
+	for c in cols {
+		got := crisis_recede(&v, 0, c)
+		testing.expectf(t, got == c, "f=0 must be an exact byte passthrough, got {{%d,%d,%d,%d}}", got.r, got.g, got.b, got.a)
+	}
+	testing.expect(t, crisis_recede_scale(0) == 1, "the alpha scale must be an exact 1 at f=0")
+	testing.expect(t, crisis_recede_scale(-0.5) == 1, "negative factors are guarded passthroughs")
+}
+
+@(test)
+crisis_recede_reaches_the_calm_register :: proc(t: ^testing.T) {
+	p := palette_load()
+	v: View
+	v.palette = &p
+	// the exact shipped mix at full engagement: copper {240,110,0} toward
+	// canvas {237,226,200} at k=0.65, u8-truncated per channel; alpha passes
+	// through untouched (the wash layers own their alpha via the scale twin).
+	expect_color(t, crisis_recede(&v, 1, p.pipe_copper), {238, 185, 130, 255})
+	expect_color(t, crisis_recede(&v, 1, p.pipe_steel), {154, 199, 214, 255})
+	expect_color(t, crisis_recede(&v, 1, p.pipe_fiber), {243, 222, 130, 255})
+	// alpha passthrough at full engagement
+	tie := crisis_recede(&v, 1, rl.Color{186, 94, 232, 235})
+	testing.expectf(t, tie.a == 235, "alpha passes through untouched (got %d)", tie.a)
+	// the alpha-layer twin: full engagement keeps 35% of the accent strength
+	// (f32-tolerance: 1 - f32(0.65) is not bit-equal to f32(0.35))
+	testing.expectf(t, abs(crisis_recede_scale(1) - (1 - CRISIS_DESAT_MIX)) < 1e-6,
+		"scale(1) == 1 - CRISIS_DESAT_MIX (got %v)", crisis_recede_scale(1))
+	// the canvas itself is a fixed point (receding the calm register is a no-op
+	// modulo truncation: 0.35*c + 0.65*c == c exactly in f32 for u8 inputs)
+	expect_color(t, crisis_recede(&v, 1, p.canvas), p.canvas)
+}
+
+@(test)
+crisis_involvement_predicates :: proc(t: ^testing.T) {
+	cr: pp.Crisis_State
+	defer delete(cr.active)
+	append(&cr.active, pp.Active_Crisis{kind = .Saturated_Bundle, bundle_lo = 10, bundle_hi = 12, triggered_tick = 100})
+	// the named pair; canonical (lo,hi) storage means a reversed query
+	// simply does not match (the predicate is exact, not order-normalizing)
+	testing.expect(t, crisis_bundle_involved(&cr, 10, 12), "the named pair is involved")
+	testing.expect(t, !crisis_bundle_involved(&cr, 12, 10), "a reversed query does not match the canonical row")
+	testing.expect(t, !crisis_bundle_involved(&cr, 10, 11), "a different pair is not involved")
+	// endpoints only
+	testing.expect(t, crisis_node_involved(&cr, 10), "endpoint lo is involved")
+	testing.expect(t, crisis_node_involved(&cr, 12), "endpoint hi is involved")
+	testing.expect(t, !crisis_node_involved(&cr, 11), "a non-endpoint node is not involved")
+	// pool rows involve nothing (map-wide: no zone carve)
+	append(&cr.active, pp.Active_Crisis{kind = .Pool_Exhaustion, triggered_tick = 200})
+	testing.expect(t, !crisis_bundle_involved(&cr, 0, 1), "a pool row never names a bundle zone")
+	testing.expect(t, !crisis_node_involved(&cr, 0), "a pool row never names a node zone")
+}
+
+@(test)
+crisis_packet_involvement_chain :: proc(t: ^testing.T) {
+	// the resolution CHAIN the draw rides (review r1 finding 3: the pixel
+	// pin covers the wiring; this covers pipe_slot -> pipe_bundle -> pair)
+	// the on-disk catalogs (the spawn_fx_test load convention, self-contained)
+	read_cat :: proc(path: string) -> []u8 {
+		b, err := os.read_entire_file_from_path(path, context.allocator)
+		if err != nil {
+			fmt.eprintfln("crisis_chain_test: cannot read %s", path)
+		}
+		return b
+	}
+	src: pp.Catalog_Sources
+	src.node_types = read_cat("data/node_types.json")
+	src.pipe_tiers = read_cat("data/pipe_tiers.json")
+	src.balance = read_cat("data/balance.json")
+	src.packet_types = read_cat("data/packet_types.json")
+	src.demand = read_cat("data/demand.json")
+	src.eras = read_cat("data/eras.json")
+	src.crises = read_cat("data/crises.json")
+	defer {
+		delete(src.node_types)
+		delete(src.pipe_tiers)
+		delete(src.balance)
+		delete(src.packet_types)
+		delete(src.demand)
+		delete(src.eras)
+		delete(src.crises)
+	}
+	cat: pp.Catalogs
+	if e := pp.catalogs_load(&cat, &src); e.file != "" {
+		testing.expect(t, false, fmt.aprintf("catalog load failed: %s %s", e.file, e.rule))
+		return
+	}
+	defer pp.catalogs_destroy(&cat) // W2 (Perkins r1): the fixture owns its catalog
+	state: pp.Run_State
+	pp.run_init(&state, 7, cat.hash, cat.balance.logic_hz)
+	defer pp.run_destroy(&state)
+	res, _ := pp.node_type_index(&cat, "residential")
+	rtb, _ := pp.node_type_index(&cat, "router_basic")
+	std, _ := pp.pipe_tier_index(&cat, "standard")
+	n0 := pp.topology_spawn_node(&state.topology, res, {4, 15}, &cat)
+	n1 := pp.topology_spawn_node(&state.topology, rtb, {12, 15}, &cat)
+	n2 := pp.topology_spawn_node(&state.topology, res, {4, 21}, &cat)
+	n3 := pp.topology_spawn_node(&state.topology, rtb, {12, 21}, &cat)
+	pa, _ := pp.topology_apply_edit(&state.topology, pp.Command{kind = pp.Cmd_Draw_Pipe{a = n0, b = n1, tier = std}}, &cat)
+	pb, _ := pp.topology_apply_edit(&state.topology, pp.Command{kind = pp.Cmd_Draw_Pipe{a = n2, b = n3, tier = std}}, &cat)
+	pp.bundles_rebuild(&state.bundles, &state.topology, &cat, state.era)
+	psa, _ := pp.pipe_slot(&state.topology, pa.id)
+	pp.crisis_trigger(&state, 1000, 0, 0, .Saturated_Bundle, state.bundles.pipe_bundle[psa], 0, 10)
+	on_named := pp.Packet{on_edge = true, edge = pa.id, heading = n1}
+	on_other := pp.Packet{on_edge = true, edge = pb.id, heading = n3}
+	at_end := pp.Packet{on_edge = false, at_node = n0}
+	at_far := pp.Packet{on_edge = false, at_node = n2}
+	testing.expect(t, crisis_packet_involved(&state.crisis, &state.topology, &state.bundles, &on_named), "an on-edge rider on the named bundle is involved")
+	testing.expect(t, !crisis_packet_involved(&state.crisis, &state.topology, &state.bundles, &on_other), "an on-edge rider on another bundle is not")
+	testing.expect(t, crisis_packet_involved(&state.crisis, &state.topology, &state.bundles, &at_end), "an at-node packet at an endpoint is involved")
+	testing.expect(t, !crisis_packet_involved(&state.crisis, &state.topology, &state.bundles, &at_far), "an at-node packet elsewhere is not")
+}
+
+@(test)
+route_tie_inline_load_default_is_pinned :: proc(t: ^testing.T) {
+	// PR #99 r2 W3 (the Perkins mutation-proven coverage gap): the inline
+	// jcol default for route_tie on the STRIPPED-JSON load path had ZERO
+	// coverage — reverting the default to amber left 83/83 GREEN, vacuous.
+	// This leg pins the loaded default: a palette JSON that parses but omits
+	// route_tie must load the shipped info-violet bytes (the r2 value, byte
+	// twin of data/palette.json).
+	src := "{\"canvas\": [237, 226, 200, 255]}"
+	p := palette_load(transmute([]u8) src)
+	expect_color(t, p.route_tie, {186, 94, 232, 235})
+	// the fallback path mirrors it (a fully broken JSON)
+	f := fallback_palette()
+	expect_color(t, f.route_tie, {186, 94, 232, 235})
+}
diff --git a/app/render/view.odin b/app/render/view.odin
index e64accd2..f153c8cf 100644
--- a/app/render/view.odin
+++ b/app/render/view.odin
@@ -525,13 +525,17 @@ draw_world :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^pp
 	if v.route_wires || v.wire_anchors {
 		paths = wire_paths_compute(v, topo, bundles)
 	}
-	draw_bundles(v, topo, bundles, flow, crisis, paths[:])
+	// v2-viscomm-crisis-duck: the crisis desaturation factor, derived ONCE
+	// per frame from the serialized crisis rows + the tick (the pure seam in
+	// crisis.odin — the harness renders it from sim state alone, no feeding).
+	desat_f := crisis_desat_factor(v, crisis, tick)
+	draw_bundles(v, topo, bundles, flow, crisis, desat_f, paths[:])
 	// v2-spawn-feel: the PLACEMENT feedback — the pulse band over the pipes
 	// near a just-landed terminal (after the pipes, before the nodes — the
 	// highlight reads as "this node just joined the network").
 	spawn_fx_draw_highlight(v, topo, tick)
-	draw_nodes(v, topo, crisis, tick)
-	draw_packets(v, topo, bundles, flow, tick, focus_class, interp_alpha, paths[:])
+	draw_nodes(v, topo, crisis, tick, desat_f)
+	draw_packets(v, topo, bundles, flow, crisis, tick, desat_f, focus_class, interp_alpha, paths[:])
 	// 4.2: the crisis bottleneck outline — the named bundle's member pipes
 	// (pulsing red stroke, on top of the pipes so the highlight reads).
 	draw_crisis_outlines(v, topo, bundles, crisis, tick, paths[:])
@@ -819,7 +823,7 @@ bundle_congestion_level :: proc(topo: ^pp.Topology, bundles: ^pp.Bundles, crisis
 	return .None
 }
 
-draw_bundles :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^pp.Flow_State, crisis: ^pp.Crisis_State, paths: []Wire_Path) {
+draw_bundles :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^pp.Flow_State, crisis: ^pp.Crisis_State, desat: f32, paths: []Wire_Path) {
 	p := v.palette
 	for bi in 0..<int(bundles.n) {
 		lo, hi := bundles.bundle_lo[bi], bundles.bundle_hi[bi]
@@ -833,6 +837,18 @@ draw_bundles :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
 		tier := bundles.bundle_tier[bi]
 		count := bundles.bundle_count[bi]
 		col := tier_pipe_color(v, tier)
+		// v2-viscomm-crisis-duck: non-involved bundles recede toward the
+		// board's calm register while a crisis owns the saturation budget
+		// (the dynamic network-pop inversion). The NAMED bundle keeps its
+		// full saturation — the crisis zone is the only saturated thing on
+		// the board. The casing derives from the receded tier color below;
+		// warning halos never recede (their own tokens — the telegraph
+		// family stays live mid-crisis, never color alone).
+		recede_bundle := desat > 0 && !crisis_bundle_involved(crisis, lo, hi)
+		raw := col // the halo's blend base — warning colors NEVER recede (review r1: the halo was dragged ~37% toward canvas with the receded col)
+		if recede_bundle {
+			col = crisis_recede(v, desat, col)
+		}
 		caps := bundle_lane_caps_view(topo, bundles, flow, u32(bi))
 		band := band_width(v, tier, int(count))
 		// direction + perpendicular (the lateral axis the lanes stack along)
@@ -869,6 +885,11 @@ draw_bundles :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
 			inner := band - 2*gutter*v.scale
 			bands := lane_bands(caps, inner)
 			lane_cols := [3]rl.Color{p.lane_express, p.lane_standard, p.lane_best_effort}
+			if recede_bundle {
+				for i in 0..<3 {
+					lane_cols[i] = crisis_recede(v, desat, lane_cols[i])
+				}
+			}
 			if !v.lane_detail {
 				for i in 0..<3 {
 					lane_cols[i] = rl.Color{
@@ -897,9 +918,9 @@ draw_bundles :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
 					halo = p.state_critical
 				}
 				halo = rl.Color{
-					u8(f32(col.r) * 0.57 + f32(halo.r) * 0.43),
-					u8(f32(col.g) * 0.57 + f32(halo.g) * 0.43),
-					u8(f32(col.b) * 0.57 + f32(halo.b) * 0.43),
+					u8(f32(raw.r) * 0.57 + f32(halo.r) * 0.43),
+					u8(f32(raw.g) * 0.57 + f32(halo.g) * 0.43),
+					u8(f32(raw.b) * 0.57 + f32(halo.b) * 0.43),
 					255,
 				}
 				w := band + 5.0 * v.scale
@@ -942,6 +963,11 @@ draw_bundles :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
 		inner := band - 2*gutter*v.scale
 		bands := lane_bands(caps, inner)
 		lane_cols := [3]rl.Color{p.lane_express, p.lane_standard, p.lane_best_effort}
+		if recede_bundle {
+			for i in 0..<3 {
+				lane_cols[i] = crisis_recede(v, desat, lane_cols[i])
+			}
+		}
 		if !v.lane_detail {
 			for i in 0..<3 {
 				lane_cols[i] = rl.Color{
@@ -971,11 +997,19 @@ draw_bundles :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
 			apex_b, anchors_b := end_apex(v, topo, bundles, u32(bi), 1, a_world, band_w)
 			for anc in anchors_a {
 				stub_w := band_world(v, anc.tier, 1) * 0.6 // the member's own narrow read
-				draw_fan_stub(v, anc.pos, apex_a, stub_w, tier_pipe_color(v, anc.tier))
+				stub_col := tier_pipe_color(v, anc.tier)
+				if recede_bundle {
+					stub_col = crisis_recede(v, desat, stub_col)
+				}
+				draw_fan_stub(v, anc.pos, apex_a, stub_w, stub_col)
 			}
 			for anc in anchors_b {
 				stub_w := band_world(v, anc.tier, 1) * 0.6
-				draw_fan_stub(v, anc.pos, apex_b, stub_w, tier_pipe_color(v, anc.tier))
+				stub_col := tier_pipe_color(v, anc.tier)
+				if recede_bundle {
+					stub_col = crisis_recede(v, desat, stub_col)
+				}
+				draw_fan_stub(v, anc.pos, apex_b, stub_w, stub_col)
 			}
 		}
 
@@ -987,9 +1021,9 @@ draw_bundles :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
 				halo = p.state_critical
 			}
 			halo = rl.Color{
-				u8(f32(col.r) * 0.57 + f32(halo.r) * 0.43),
-				u8(f32(col.g) * 0.57 + f32(halo.g) * 0.43),
-				u8(f32(col.b) * 0.57 + f32(halo.b) * 0.43),
+				u8(f32(raw.r) * 0.57 + f32(halo.r) * 0.43),
+				u8(f32(raw.g) * 0.57 + f32(halo.g) * 0.43),
+				u8(f32(raw.b) * 0.57 + f32(halo.b) * 0.43),
 				255,
 			}
 			w := band + 5.0 * v.scale
@@ -1014,12 +1048,19 @@ draw_fan_stub :: proc(v: ^View, from, to: rl.Vector2, width_world: f32, col: rl.
 // marker), terminals via draw_building (the family wash + type chip). The
 // health telegraph rings draw on top (drawn after, so the ring + its glyph
 // own the top surface).
-draw_nodes :: proc(v: ^View, topo: ^pp.Topology, crisis: ^pp.Crisis_State, tick: u64) {
+draw_nodes :: proc(v: ^View, topo: ^pp.Topology, crisis: ^pp.Crisis_State, tick: u64, desat: f32 = 0) {
 	for i in 0..<len(topo.node_alive) {
 		if !topo.node_alive[i] {
 			continue
 		}
 		c := node_screen(v, topo.node_pos[i])
+		// v2-viscomm-crisis-duck: non-involved nodes recede their ACCENT
+		// layers (family wash + chip glyph + tier marker + primitive-path
+		// bodies); health rings/glyphs never do (the telegraph family).
+		recede_n := f32(0)
+		if desat > 0 && !crisis_node_involved(crisis, topo.node_id[i]) {
+			recede_n = desat
+		}
 		// 5.2 node-health telegraph: the ring + glyph + pulse surface, drawn on
 		// top of the node form. Renders ONLY on non-healthy states (a healthy
 		// node draws nothing — the canon's quiet-at-🟢 rule). Triple-redundant
@@ -1044,7 +1085,7 @@ draw_nodes :: proc(v: ^View, topo: ^pp.Topology, crisis: ^pp.Crisis_State, tick:
 				continue
 			}
 			nt := v.catalogs.node_types[topo.node_type[i]]
-			draw_router(v, topo.node_id[i], c, nt.port_capacity)
+			draw_router(v, topo.node_id[i], c, nt.port_capacity, recede_n)
 		} else {
 			// v2-spawn-feel: the reveal transform (scale 0.4→1 + fade over the
 			// 8 ticks from the growth tick) — pure view-layer; the node is
@@ -1053,7 +1094,7 @@ draw_nodes :: proc(v: ^View, topo: ^pp.Topology, crisis: ^pp.Crisis_State, tick:
 			if !rk {
 				rs, rf = 1, 1
 			}
-			draw_building(v, topo.node_id[i], topo.node_role[i], c, lvl, rs, rf)
+			draw_building(v, topo.node_id[i], topo.node_role[i], c, lvl, rs, rf, recede_n)
 		}
 		if lvl != .None {
 			draw_health_ring(v, lvl, topo.node_id[i], c, tick)
@@ -1118,7 +1159,7 @@ draw_health_ring :: proc(v: ^View, lvl: pp.Congestion_Level, node_id: u32, c: rl
 // shadow, the wash and the chip all ride the same transform; the node stays
 // gameplay-valid from the growth tick regardless (the reveal is cosmetic
 // timing only).
-draw_building :: proc(v: ^View, id: u32, role: pp.Terminal_Role, c: rl.Vector2, health: pp.Congestion_Level, reveal_scale: f32 = 1.0, reveal_fade: f32 = 1.0) {
+draw_building :: proc(v: ^View, id: u32, role: pp.Terminal_Role, c: rl.Vector2, health: pp.Congestion_Level, reveal_scale: f32 = 1.0, reveal_fade: f32 = 1.0, recede: f32 = 0.0) {
 	fam := terminal_family(v, role)
 	chip_visible := health == .None
 	// v2-dublin-map-beautify (amendment #2): on the Dublin board the
@@ -1126,9 +1167,9 @@ draw_building :: proc(v: ^View, id: u32, role: pp.Terminal_Role, c: rl.Vector2,
 	// grammar — buildings ON streets, no floating sprites); the type chip
 	// rides the block. The sprite path stays for the procedural map.
 	if v.map_source == u8(pp.Map_Source.Dublin) && v.board != nil {
-		top_y := dublin_node_block_draw(v, c, fam, reveal_scale)
+		top_y := dublin_node_block_draw(v, c, fam, reveal_scale, recede)
 		if chip_visible {
-			draw_type_chip(v, role, c, top_y, fam, reveal_scale, reveal_fade)
+			draw_type_chip(v, role, c, top_y, fam, reveal_scale, reveal_fade, recede)
 		}
 		return
 	}
@@ -1143,9 +1184,9 @@ draw_building :: proc(v: ^View, id: u32, role: pp.Terminal_Role, c: rl.Vector2,
 		dst, ok := sprite_blit_dst(&v.sprites, idx, c, target)
 		sprite_blit(&v.sprites, idx, c, target, shadow_for_role(role), {255, 255, 255, u8(255 * clamp01(reveal_fade))})
 		if ok {
-			draw_family_wash(v, dst, fam, reveal_fade)
+			draw_family_wash(v, dst, fam, reveal_fade, recede)
 			if chip_visible {
-				draw_type_chip(v, role, c, dst.y, fam, reveal_scale, reveal_fade)
+				draw_type_chip(v, role, c, dst.y, fam, reveal_scale, reveal_fade, recede)
 			}
 		}
 		return
@@ -1164,17 +1205,17 @@ draw_building :: proc(v: ^View, id: u32, role: pp.Terminal_Role, c: rl.Vector2,
 		w := s * 1.15
 		h := s * 0.95
 		foot = {c.x - w/2, c.y - h/2, w, h}
-		rl.DrawRectangleV({c.x - w/2, c.y - h/2 + s*0.12}, {w, h - s*0.12}, p.host_body)
-		rl.DrawRectangleV({c.x - w/2, c.y - h/2}, {w, s * 0.28}, p.host_roof)
+		rl.DrawRectangleV({c.x - w/2, c.y - h/2 + s*0.12}, {w, h - s*0.12}, crisis_recede(v, recede, p.host_body))
+		rl.DrawRectangleV({c.x - w/2, c.y - h/2}, {w, s * 0.28}, crisis_recede(v, recede, p.host_roof))
 		// play triangle (the YouTune brand glyph)
 		g := s * 0.22
 		v1 := rl.Vector2{c.x - g * 0.6, c.y - g * 0.8}
 		v2 := rl.Vector2{c.x - g * 0.6, c.y + g * 0.8}
 		v3 := rl.Vector2{c.x + g, c.y}
 		rl.DrawTriangle(v3, v2, v1, {250, 246, 238, 255})
-		draw_family_wash(v, foot, fam, reveal_fade)
+		draw_family_wash(v, foot, fam, reveal_fade, recede)
 		if chip_visible {
-			draw_type_chip(v, role, c, foot.y, fam, reveal_scale, reveal_fade)
+			draw_type_chip(v, role, c, foot.y, fam, reveal_scale, reveal_fade, recede)
 		}
 		return
 	}
@@ -1183,6 +1224,10 @@ draw_building :: proc(v: ^View, id: u32, role: pp.Terminal_Role, c: rl.Vector2,
 	variant := int(id) % 4
 	body := p.house_bodies[variant]
 	roof := p.house_roofs[variant]
+	if recede > 0 {
+		body = crisis_recede(v, recede, body)
+		roof = crisis_recede(v, recede, roof)
+	}
 	if role == .Small_Biz || role == .Campus {
 		// 5.11 fallback: flat-roof blocks (office / campus) — a DISTINCT shape
 		// from the peaked-roof house (E9.1 even on the primitive path). Small
@@ -1224,9 +1269,9 @@ draw_building :: proc(v: ^View, id: u32, role: pp.Terminal_Role, c: rl.Vector2,
 			tw := ww * 0.22
 			rl.DrawRectangleV({c.x - tw/2, by - s * 0.28}, {tw, s * 0.28}, roof)
 		}
-		draw_family_wash(v, foot, fam, reveal_fade)
+		draw_family_wash(v, foot, fam, reveal_fade, recede)
 		if chip_visible {
-			draw_type_chip(v, role, c, foot.y, fam, reveal_scale, reveal_fade)
+			draw_type_chip(v, role, c, foot.y, fam, reveal_scale, reveal_fade, recede)
 		}
 		return
 	}
@@ -1246,9 +1291,9 @@ draw_building :: proc(v: ^View, id: u32, role: pp.Terminal_Role, c: rl.Vector2,
 	// door
 	dw := s * 0.16
 	rl.DrawRectangleV({c.x - dw/2, top + h - s * 0.3}, {dw, s * 0.3}, roof)
-	draw_family_wash(v, foot, fam, reveal_fade)
+	draw_family_wash(v, foot, fam, reveal_fade, recede)
 	if chip_visible {
-		draw_type_chip(v, role, c, foot.y, fam, reveal_scale, reveal_fade)
+		draw_type_chip(v, role, c, foot.y, fam, reveal_scale, reveal_fade, recede)
 	}
 }
 
@@ -1275,14 +1320,14 @@ terminal_family :: proc(v: ^View, role: pp.Terminal_Role) -> rl.Color {
 // The wash is an alpha-blended FILL (rlsw-safe — the 7.1 field note: fills
 // alpha-blend in the software renderer; only LINE alpha is ignored). `fade`
 // (the spawn reveal) scales the wash strength with the sprite.
-draw_family_wash :: proc(v: ^View, dst: rl.Rectangle, fam: rl.Color, fade: f32 = 1.0) {
+draw_family_wash :: proc(v: ^View, dst: rl.Rectangle, fam: rl.Color, fade: f32 = 1.0, recede: f32 = 0.0) {
 	if fam.a == 0 {
 		return
 	}
 	w := dst.width * 0.92
 	h := dst.height * 0.92
 	c := fam
-	c.a = u8(f32(fam.a) * clamp01(fade))
+	c.a = u8(f32(fam.a) * clamp01(fade) * crisis_recede_scale(recede))
 	if c.a == 0 {
 		return
 	}
@@ -1291,12 +1336,14 @@ draw_family_wash :: proc(v: ^View, dst: rl.Rectangle, fam: rl.Color, fade: f32 =
 
 // draw_family_wash_disc — the puck variant: a CIRCLE wash (the puck sprite
 // is a disc; a rect wash would square off its corners).
-draw_family_wash_disc :: proc(v: ^View, dst: rl.Rectangle, fam: rl.Color) {
+draw_family_wash_disc :: proc(v: ^View, dst: rl.Rectangle, fam: rl.Color, recede: f32 = 0.0) {
 	if fam.a == 0 {
 		return
 	}
+	c := fam
+	c.a = u8(f32(fam.a) * crisis_recede_scale(recede))
 	r := min(dst.width, dst.height) * 0.5 * 0.94
-	rl.DrawCircleV({dst.x + dst.width / 2, dst.y + dst.height / 2}, r, fam)
+	rl.DrawCircleV({dst.x + dst.width / 2, dst.y + dst.height / 2}, r, c)
 }
 
 // draw_type_chip — the Q2a icon chip: a tiny paper chip above the terminal
@@ -1306,7 +1353,7 @@ draw_family_wash_disc :: proc(v: ^View, dst: rl.Rectangle, fam: rl.Color) {
 // never color alone). Skipped while a health ring is up (the ring + its
 // glyph own the node's top surface then). `reveal_scale`/`reveal_fade` (the
 // spawn reveal) scale the chip with the sprite + fade its inks.
-draw_type_chip :: proc(v: ^View, role: pp.Terminal_Role, c: rl.Vector2, top_y: f32, fam: rl.Color, reveal_scale: f32 = 1.0, reveal_fade: f32 = 1.0) {
+draw_type_chip :: proc(v: ^View, role: pp.Terminal_Role, c: rl.Vector2, top_y: f32, fam: rl.Color, reveal_scale: f32 = 1.0, reveal_fade: f32 = 1.0, recede: f32 = 0.0) {
 	s := v.tile_px * v.scale
 	cw := s * 0.54 * reveal_scale
 	ch := s * 0.36 * reveal_scale
@@ -1321,7 +1368,7 @@ draw_type_chip :: proc(v: ^View, role: pp.Terminal_Role, c: rl.Vector2, top_y: f
 	out.a = u8(255 * fade)
 	rl.DrawRectangleLinesEx({x0, y0, cw, ch}, max(1.0, s * 0.02 * reveal_scale), out)
 	glyph := fam
-	glyph.a = u8(255 * fade)
+	glyph.a = u8(255 * fade * crisis_recede_scale(recede))
 	#partial switch role {
 	case .Content_Host:
 		// the play-marking triangle (the host's own brand glyph)
@@ -1629,14 +1676,14 @@ router_tier_scale :: proc(port_capacity: i32) -> f32 {
 // host-blue family — the audit's router_mid<->content_host 9.9 deg failure);
 // the ring is the bird's-eye tier read (the LED count alone is sub-pixel at
 // fit). Size ladder unchanged (router_tier_scale).
-draw_router :: proc(v: ^View, id: u32, c: rl.Vector2, port_capacity: i32) {
+draw_router :: proc(v: ^View, id: u32, c: rl.Vector2, port_capacity: i32, recede: f32 = 0.0) {
 	if v.sprites.ok {
 		dst, ok := sprite_blit_dst(&v.sprites, sprite_index_puck(port_capacity), c, sprite_puck_target(v, port_capacity))
 		sprite_blit(&v.sprites, sprite_index_puck(port_capacity), c, sprite_puck_target(v, port_capacity), shadow_for_puck())
 		if ok {
 			tier := router_tier_family(v, port_capacity)
-			draw_family_wash_disc(v, dst, tier)
-			draw_tier_ring(v, c, dst, tier)
+			draw_family_wash_disc(v, dst, tier, recede)
+			draw_tier_ring(v, c, dst, tier, recede)
 		}
 		return
 	}
@@ -1644,8 +1691,8 @@ draw_router :: proc(v: ^View, id: u32, c: rl.Vector2, port_capacity: i32) {
 	p := v.palette
 	base := v.tile_px * v.scale * 0.5
 	r := base * 0.9 * router_tier_scale(port_capacity)
-	rl.DrawCircleV(c, r, p.router_body)
-	rl.DrawCircleV(c, r * 0.45, p.router_dark)
+	rl.DrawCircleV(c, r, crisis_recede(v, recede, p.router_body))
+	rl.DrawCircleV(c, r * 0.45, crisis_recede(v, recede, p.router_dark))
 	// tier 2+ glowing core: a soft inner ring hugging the dark core
 	if port_capacity >= 8 {
 		glow := p.router_led
@@ -1680,8 +1727,11 @@ draw_router :: proc(v: ^View, id: u32, c: rl.Vector2, port_capacity: i32) {
 	// the tier marker (the primitive path gets it too — same tokens): the
 	// wash over the puck disc + the ring.
 	tier := router_tier_family(v, port_capacity)
+	if recede > 0 {
+		tier.a = u8(f32(tier.a) * crisis_recede_scale(recede))
+	}
 	rl.DrawCircleV(c, r * 0.98, tier)
-	draw_tier_ring(v, c, {c.x - r, c.y - r, r * 2, r * 2}, tier)
+	draw_tier_ring(v, c, {c.x - r, c.y - r, r * 2, r * 2}, tier, recede)
 }
 
 // router_tier_family — the tier's marker token (basic steel / mid teal /
@@ -1703,8 +1753,8 @@ router_tier_family :: proc(v: ^View, port_capacity: i32) -> rl.Color {
 // (DrawCircleLinesV has no thickness — the health-ring pattern); full-alpha
 // colors only (the rlsw line-alpha trap). Radius rides the puck's dst rect
 // so the ring scales with the tier size ladder.
-draw_tier_ring :: proc(v: ^View, c: rl.Vector2, dst: rl.Rectangle, tier: rl.Color) {
-	ring := tier
+draw_tier_ring :: proc(v: ^View, c: rl.Vector2, dst: rl.Rectangle, tier: rl.Color, recede: f32 = 0.0) {
+	ring := crisis_recede(v, recede, tier)
 	ring.a = 255
 	r := min(dst.width, dst.height) * 0.5 * 1.10
 	th := max(1.0, v.tile_px * v.scale * 0.055)
@@ -1762,7 +1812,7 @@ draw_packet_shape :: proc(pos: rl.Vector2, r: f32, body, outline: rl.Color, shap
 // last two 20 Hz snapshots (the §4 motion canon: "interpolate position
 // between sim snapshots for 60 fps smoothness"). The harness leaves the
 // default 1.0 (snapshot-exact) → T2 goldens byte-identical by construction.
-draw_packets :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^pp.Flow_State, tick: u64, focus_class: i32 = -1, interp_alpha: f32 = 1.0, paths: []Wire_Path = nil) {
+draw_packets :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^pp.Flow_State, crisis: ^pp.Crisis_State, tick: u64, desat: f32 = 0, focus_class: i32 = -1, interp_alpha: f32 = 1.0, paths: []Wire_Path = nil) {
 	bandwidth := u32(v.catalogs.balance.packet_bandwidth)
 	for i in 0..<len(flow.packets) {
 		p := &flow.packets[i]
@@ -1939,6 +1989,17 @@ draw_packets :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
 			shape = pt.shape
 			body = mode_class_color(v.palette, pt.id, rl.Color{pt.color_rgba[0], pt.color_rgba[1], pt.color_rgba[2], pt.color_rgba[3]})
 		}
+		// v2-viscomm-crisis-duck: non-involved packets recede with their
+		// network (involved = riding an involved bundle / sitting at an
+		// involved node — ONE resolution chain, crisis_packet_involved);
+		// the outline derives from the receded body (one source), and the
+		// focus ghost + trail echoes compose after (alpha layers over the
+		// same body). The GLINT fades with the recede (review r1: a
+		// full-strength sparkle field on receded riders fought the desat).
+		recede_pkt := desat > 0 && !crisis_packet_involved(crisis, topo, bundles, p)
+		if recede_pkt {
+			body = crisis_recede(v, desat, body)
+		}
 		outline := rl.Color{
 			u8(f32(body.r) * 0.55),
 			u8(f32(body.g) * 0.55),
@@ -1975,12 +2036,18 @@ draw_packets :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
 		// stream glint sits just below the apex, the circle glint up-left of
 		// center. Alpha follows body.a so a focused-out ghost packet dims its
 		// glint too (the never-color-alone + ghost-read rules). Echoes carry NO
-		// glint — the sparkle is the LIVE packet's read.
+		// glint — the sparkle is the LIVE packet's read. v2-viscomm-crisis-duck
+		// (review r1): a receded rider dims its glint with the same scale —
+		// the packet recedes as a unit, sparkle included.
+		glint_a := body.a
+		if recede_pkt {
+			glint_a = u8(f32(glint_a) * crisis_recede_scale(desat))
+		}
 		#partial switch shape {
 		case .Triangle:
-			rl.DrawCircleV({pos.x - r * 0.16, pos.y - r * 0.34}, r * 0.20, rl.Color{250, 246, 238, body.a})
+			rl.DrawCircleV({pos.x - r * 0.16, pos.y - r * 0.34}, r * 0.20, rl.Color{250, 246, 238, glint_a})
 		case:
-			rl.DrawCircleV({pos.x - r * 0.34, pos.y - r * 0.34}, r * 0.22, rl.Color{250, 246, 238, body.a})
+			rl.DrawCircleV({pos.x - r * 0.34, pos.y - r * 0.34}, r * 0.22, rl.Color{250, 246, 238, glint_a})
 		}
 	}
 	// 2.1: keep the sub-tick cache bounded to the live packet set (delivered
diff --git a/goldens/a11y_deutan/65000ms.png b/goldens/a11y_deutan/65000ms.png
index d46aa141..b902d59e 100644
Binary files a/goldens/a11y_deutan/65000ms.png and b/goldens/a11y_deutan/65000ms.png differ
diff --git a/goldens/a11y_protan/65000ms.png b/goldens/a11y_protan/65000ms.png
index d46aa141..b902d59e 100644
Binary files a/goldens/a11y_protan/65000ms.png and b/goldens/a11y_protan/65000ms.png differ
diff --git a/goldens/a11y_reduced/65000ms.png b/goldens/a11y_reduced/65000ms.png
index 4a48da0c..a5166f0f 100644
Binary files a/goldens/a11y_reduced/65000ms.png and b/goldens/a11y_reduced/65000ms.png differ
diff --git a/goldens/a11y_scale/65000ms.png b/goldens/a11y_scale/65000ms.png
index 2a97b36c..635acaf7 100644
Binary files a/goldens/a11y_scale/65000ms.png and b/goldens/a11y_scale/65000ms.png differ
diff --git a/goldens/a11y_tritan/65000ms.png b/goldens/a11y_tritan/65000ms.png
index b8a62882..553098c0 100644
Binary files a/goldens/a11y_tritan/65000ms.png and b/goldens/a11y_tritan/65000ms.png differ
diff --git a/goldens/juice/65000ms.png b/goldens/juice/65000ms.png
index 5e284201..33764699 100644
Binary files a/goldens/juice/65000ms.png and b/goldens/juice/65000ms.png differ
diff --git a/harness/palcheck.odin b/harness/palcheck.odin
index 7d926ee9..414911f2 100644
--- a/harness/palcheck.odin
+++ b/harness/palcheck.odin
@@ -113,6 +113,21 @@ a11y_separation_check :: proc(cat: ^pp.Catalogs, base: ^rnd.Palette, mode: rnd.P
 	append(&pairs, [2]rl.Color{p.water, p.land})
 	append(&pairs, [2]rl.Color{p.park, p.land})
 	append(&pairs, [2]rl.Color{p.coast, p.land})
+	// v2-viscomm-crisis-duck: the crisis-separation pairs — an involved
+	// element (raw color) vs the SAME color receded toward canvas at full
+	// engagement (what a non-involved element renders mid-crisis), for the
+	// pipe tiers AND the effective packet-class bodies (the most numerous
+	// receded surface — review r1 note). NOT exactly affine in sim space
+	// (the Machado wrap includes sRGB<->linear gamma + the mix u8-truncates)
+	// — the empirical threshold check below is what actually holds; these
+	// rows put it in the oracle per mode.
+	vv: rnd.View
+	vv.palette = &eff
+	{
+		append(&pairs, [2]rl.Color{p.pipe_copper, rnd.crisis_recede(&vv, 1, p.pipe_copper)})
+		append(&pairs, [2]rl.Color{p.pipe_steel, rnd.crisis_recede(&vv, 1, p.pipe_steel)})
+		append(&pairs, [2]rl.Color{p.pipe_fiber, rnd.crisis_recede(&vv, 1, p.pipe_fiber)})
+	}
 	// packet classes: the effective draw-time color (mode override or catalog)
 	// — the draw path (mode_class_color) is the single source.
 	cls_eff: [dynamic]rl.Color
@@ -126,6 +141,11 @@ a11y_separation_check :: proc(cat: ^pp.Catalogs, base: ^rnd.Palette, mode: rnd.P
 			append(&pairs, [2]rl.Color{cls_eff[i], cls_eff[j]})
 		}
 	}
+	// the crisis-separation twins for the class bodies (same vv as the tier
+	// pairs above — effective color vs its full recede)
+	for i in 0 ..< len(cls_eff) {
+		append(&pairs, [2]rl.Color{cls_eff[i], rnd.crisis_recede(&vv, 1, cls_eff[i])})
+	}
 	// the pinned thresholds (the derivation's): 48 for the signal pairs,
 	// 40 for the map pairs (water/park/coast vs the warm land tint). The
 	// map-pair membership test checks BOTH ends (the r1 review finding: the
@@ -839,6 +859,283 @@ run_palcheck :: proc(cat: ^pp.Catalogs) -> int {
 		rnd.gauge_reset(&view.gauges)
 	}
 
+	// --- 7. the crisis-desat draw-path pin (v2-viscomm-crisis-duck) --------
+	// The gauge/tie lessons: predicate pins are bypassable at the call site —
+	// guard what RENDERS. This section renders the REAL draw_world with an
+	// ACTIVE Saturated_Bundle crisis (the row constructed via the engine's
+	// own crisis_trigger — never a hand-appended literal) and pixel-scans:
+	//   (a) a NON-INVOLVED bundle's tier band reads the RECESDED mix (65%
+	//       toward canvas at full engagement) and the RAW tier hex is ABSENT
+	//       across the band scan (the saturated-baseline distinguisher);
+	//   (b) the INVOLVED (named) bundle keeps its RAW tier hex;
+	//   (c) a NON-INVOLVED on-edge packet's body recedes with its pipe; the
+	//       INVOLVED pipe's rider stays raw;
+	//   (d) MID-RAMP: at onset+3 the non-involved band sits at the
+	//       CRISIS_FADE16[3]-predicted mix (three-way: neither raw nor full);
+	//   (e) REDUCED MOTION: the same mid-ramp tick pins at FULL desat.
+	// A bypass anywhere on the draw path (factor zeroed, predicate always
+	// involved, mix deleted) fails (a) or (c) — the mutation leg proves it.
+	{
+		sv_scale, sv_laned, sv_rm := view.scale, view.lane_detail, view.reduced_motion
+		sv_ox, sv_oy := view.off_x, view.off_y
+		defer {
+			view.scale = sv_scale
+			view.lane_detail = sv_laned
+			view.reduced_motion = sv_rm
+			view.off_x = sv_ox
+			view.off_y = sv_oy
+		}
+		state: pp.Run_State
+		pp.run_init(&state, 7, cat.hash, cat.balance.logic_hz)
+		res, _ := pp.node_type_index(cat, "residential")
+		rtb, _ := pp.node_type_index(cat, "router_basic")
+		std, _ := pp.pipe_tier_index(cat, "standard")
+		// PREMISE (review r1 note): the rider-position math below derives
+		// from lane_speeds[1] + the 8-tile fixture span — pin them so a
+		// future change fails HERE with a cause, not as a cryptic 0-px scan.
+		check(view.palette.lane_speeds[1] == 850, "section-7 premise: standard lane speed is the shipped 850 per-mille", int(view.palette.lane_speeds[1]))
+		// two DISJOINT horizontal pipes; bundle A (top) is NAMED by the
+		// crisis, bundle B (bottom) is non-involved (recedes).
+		n0 := pp.topology_spawn_node(&state.topology, res, {4, 15}, cat)
+		n1 := pp.topology_spawn_node(&state.topology, rtb, {12, 15}, cat)
+		n2 := pp.topology_spawn_node(&state.topology, res, {4, 21}, cat)
+		n3 := pp.topology_spawn_node(&state.topology, rtb, {12, 21}, cat)
+		pa, _ := pp.topology_apply_edit(&state.topology, pp.Command{kind = pp.Cmd_Draw_Pipe{a = n0, b = n1, tier = std}}, cat)
+		pb, _ := pp.topology_apply_edit(&state.topology, pp.Command{kind = pp.Cmd_Draw_Pipe{a = n2, b = n3, tier = std}}, cat)
+		bandw := u32(cat.balance.packet_bandwidth)
+		append(&state.flow.packets, pp.Packet{src = n0, dst = n1, on_edge = true, edge = pa.id, heading = n1, progress_units = bandw / 2, class = 0})
+		append(&state.flow.packets, pp.Packet{src = n2, dst = n3, on_edge = true, edge = pb.id, heading = n3, progress_units = bandw / 2, class = 0})
+		// at-node riders at the terminal DOORSTEPS (clear of the crisis
+		// outline's end-caps — the on-edge involved rider is untestable at
+		// pixels, the outline owns the band): id 3 keys the same doorstep
+		// fan offset on both, so the pair isolates involvement alone
+		// (review r1 finding 3: the packet chain needed a draw-level pin).
+		append(&state.flow.packets, pp.Packet{id = 3, src = n0, dst = n1, on_edge = false, at_node = n0, class = 0})
+		append(&state.flow.packets, pp.Packet{id = 3, src = n2, dst = n3, on_edge = false, at_node = n2, class = 0})
+		// bundles are DERIVED (rebuilt inside step) — rebuild explicitly for
+		// the render-only fixture (the same view step would produce; no
+		// stepping after, so the crisis row is never re-resolved).
+		pp.bundles_rebuild(&state.bundles, &state.topology, cat, state.era)
+		// the crisis row: the ENGINE's constructor names bundle A (the
+		// canonical pair + first member pipe resolve inside crisis_trigger;
+		// the 08-19 hand-append trap is about rows the engine then
+		// re-resolves mid-run — this fixture renders immediately).
+		psa, _ := pp.pipe_slot(&state.topology, pa.id)
+		pp.crisis_trigger(&state, 1000, 0, 0, .Saturated_Bundle, state.bundles.pipe_bundle[psa], 0, 10)
+		// camera: both pipes on screen, bands wide enough for clean sampling
+		view.scale = 2.0
+		view.lane_detail = false
+		view.reduced_motion = false
+		view.off_x = f32(view.win_w) / 2 - f32(8) * view.tile_px * view.scale
+		view.off_y = f32(view.win_h) / 2 - f32(18) * view.tile_px * view.scale
+		steel := view.palette.pipe_steel
+		full := rnd.crisis_recede(&view, 1.0, steel)
+		ma := rnd.node_screen(&view, {8, 15}) // bundle A midpoint (involved)
+		mb := rnd.node_screen(&view, {8, 21}) // bundle B midpoint (non-involved)
+		// scan_col — count pixels in a vertical column crossing a horizontal
+		// band that sit within `tol` of `col` (the band interior; casing rims
+		// sit outside the scan half-width).
+		scan_col :: proc(img: rl.Image, cx, cy, half: int, col: rl.Color, tol: i32) -> int {
+			px := rl.LoadImageColors(img)
+			defer rl.UnloadImageColors(px)
+			n := 0
+			if cx < 0 || cx >= int(img.width) { return 0 } // W3 (Perkins r1): both axes guarded (the scan_box guard, mirrored)
+			for dy in -half..=half {
+				yi := cy + dy
+				if yi < 0 || yi >= int(img.height) { continue }
+				p := px[yi * int(img.width) + cx]
+				if abs(i32(p.r) - i32(col.r)) <= tol && abs(i32(p.g) - i32(col.g)) <= tol && abs(i32(p.b) - i32(col.b)) <= tol {
+					n += 1
+				}
+			}
+			return n
+		}
+		// scan_box — count pixels in an anisotropic window around a node
+		// center (the chip zone sits ABOVE the sprite: tall upper half).
+		scan_box :: proc(img: rl.Image, cx, cy, half_w, up, down: int, col: rl.Color, tol: i32) -> int {
+			px := rl.LoadImageColors(img)
+			defer rl.UnloadImageColors(px)
+			n := 0
+			for dy in -up..=down {
+				for dx in -half_w..=half_w {
+					xi, yi := cx + dx, cy + dy
+					if xi < 0 || yi < 0 || xi >= int(img.width) || yi >= int(img.height) { continue }
+					p := px[yi * int(img.width) + xi]
+					if abs(i32(p.r) - i32(col.r)) <= tol && abs(i32(p.g) - i32(col.g)) <= tol && abs(i32(p.b) - i32(col.b)) <= tol {
+						n += 1
+					}
+				}
+			}
+			return n
+		}
+		// the riders' drawn positions (the draw's own math: standard-lane
+		// per-mille over the pipe's 8-tile span, no lateral offset — the
+		// fresh fixture's lane_caps are empty so the lane bands degenerate)
+		frac := 0.5 * f32(view.palette.lane_speeds[1]) / 1000.0
+		pkt_x := view.off_x + (f32(4) + 8.0 * frac) * view.tile_px * view.scale
+		pkt_y := view.off_y + f32(21) * view.tile_px * view.scale
+		pt0 := cat.packet_types[0]
+		raw_body := rl.Color{pt0.color_rgba[0], pt0.color_rgba[1], pt0.color_rgba[2], 255}
+		rec_body := rnd.crisis_recede(&view, 1.0, rnd.mode_class_color(view.palette, pt0.id, raw_body))
+		scan_dot :: proc(img: rl.Image, cx, cy: int, col: rl.Color, tol: i32) -> int {
+			px := rl.LoadImageColors(img)
+			defer rl.UnloadImageColors(px)
+			n := 0
+			for dy in -2..=2 {
+				for dx in -2..=2 {
+					xi, yi := cx + dx, cy + dy
+					if xi < 0 || yi < 0 || xi >= int(img.width) || yi >= int(img.height) { continue }
+					p := px[yi * int(img.width) + xi]
+					if abs(i32(p.r) - i32(col.r)) <= tol && abs(i32(p.g) - i32(col.g)) <= tol && abs(i32(p.b) - i32(col.b)) <= tol {
+						n += 1
+					}
+				}
+			}
+			return n
+		}
+
+		// (a)+(b)+(c): FULL ENGAGEMENT (render at onset+100)
+		rl.BeginDrawing()
+		rl.ClearBackground(rl.Color{237, 226, 200, 255})
+		rnd.draw_world(&view, &state.topology, &state.bundles, &state.flow, &state.crisis, 1100, {}, -1, -1, state.seed)
+		rl.EndDrawing()
+		img := rl.LoadImageFromScreen()
+		normalize(&img)
+		n_b_raw := scan_col(img, int(mb.x), int(mb.y), 14, steel, 10)
+		n_b_rec := scan_col(img, int(mb.x), int(mb.y), 14, full, 10)
+		check(n_b_rec >= 8 && n_b_raw == 0,
+			fmt.aprintf("non-involved band recedes (raw %d / receded %d px — a desat bypass reads raw)", n_b_raw, n_b_rec), n_b_rec)
+		// (b) the involved NON-RECEDE, pinned on the NODE-ACCENT surface: the
+		// involved bundle's band + its rider are OVERDRAWN by the pulsing
+		// crisis outline (by design — the bottleneck highlight owns those
+		// pixels; verified: neither raw nor receded tier hex is visible
+		// there), so the zone's non-recede is pinned one layer out — the
+		// type-chip glyph draws the family token at FULL alpha above the
+		// sprite (clear of the outline's ~23px end-caps): an involved
+		// endpoint KEEPS it; a non-involved endpoint fades it to 35%
+		// strength (the recede's alpha twin). The residential family is the
+		// probe. This is the over-broad-predicate guard (a predicate that
+		// matches everything kills check (a); one that matches NOTHING
+		// fails here).
+		fam_res := view.palette.residential_family
+		raw_fam := rl.Color{fam_res.r, fam_res.g, fam_res.b, 255}
+		s0, _ := pp.node_slot(&state.topology, n0)
+		s2, _ := pp.node_slot(&state.topology, n2)
+		c0 := rnd.node_screen(&view, state.topology.node_pos[s0])
+		c2 := rnd.node_screen(&view, state.topology.node_pos[s2])
+		tp := int(view.tile_px * view.scale)
+		n_chip_inv := scan_box(img, int(c0.x), int(c0.y), tp * 3 / 2, tp * 9 / 5, tp * 3 / 5, raw_fam, 12)
+		n_chip_non := scan_box(img, int(c2.x), int(c2.y), tp * 3 / 2, tp * 9 / 5, tp * 3 / 5, raw_fam, 12)
+		check(n_chip_inv >= 3 && n_chip_non == 0,
+			fmt.aprintf("node accents: involved keeps the full-strength chip glyph (%d px), non-involved fades it (%d px)", n_chip_inv, n_chip_non), n_chip_inv)
+		n_pkt_raw := scan_dot(img, int(pkt_x), int(pkt_y), raw_body, 25)
+		n_pkt_rec := scan_dot(img, int(pkt_x), int(pkt_y), rec_body, 25)
+		check(n_pkt_rec >= 8 && n_pkt_raw == 0,
+			fmt.aprintf("non-involved rider recedes (raw %d / receded %d px of the 5x5 body scan)", n_pkt_raw, n_pkt_rec), n_pkt_rec)
+		// the AT-NODE riders (the doorstep fan: c + (-0.67s, +0.62s) at
+		// id 3 — the draw's own kx/ky math): involved terminal keeps the
+		// raw body, non-involved recedes. This is the packet-path wiring
+		// pin the outline-covered on-edge rider cannot provide.
+		door_dx := -0.67 * view.tile_px * view.scale
+		door_dy := 0.62 * view.tile_px * view.scale
+		d0 := rl.Vector2{c0.x + door_dx, c0.y + door_dy}
+		d2 := rl.Vector2{c2.x + door_dx, c2.y + door_dy}
+		n_door_raw := scan_dot(img, int(d0.x), int(d0.y), raw_body, 25)
+		n_door_rec := scan_dot(img, int(d0.x), int(d0.y), rec_body, 25)
+		check(n_door_raw >= 8 && n_door_rec == 0,
+			fmt.aprintf("involved at-node rider stays saturated (raw %d / receded %d px)", n_door_raw, n_door_rec), n_door_raw)
+		n_door2_raw := scan_dot(img, int(d2.x), int(d2.y), raw_body, 25)
+		n_door2_rec := scan_dot(img, int(d2.x), int(d2.y), rec_body, 25)
+		check(n_door2_rec >= 8 && n_door2_raw == 0,
+			fmt.aprintf("non-involved at-node rider recedes (raw %d / receded %d px)", n_door2_raw, n_door2_rec), n_door2_rec)
+		rl.UnloadImage(img)
+
+		// (d): MID-RAMP at onset+3 — the band sits at the table-predicted mix
+		f3 := rnd.crisis_desat_factor(&view, &state.crisis, 1003)
+		pred3 := rnd.crisis_recede(&view, f3, steel)
+		rl.BeginDrawing()
+		rl.ClearBackground(rl.Color{237, 226, 200, 255})
+		rnd.draw_world(&view, &state.topology, &state.bundles, &state.flow, &state.crisis, 1003, {}, -1, -1, state.seed)
+		rl.EndDrawing()
+		img = rl.LoadImageFromScreen()
+		normalize(&img)
+		n_mid := scan_col(img, int(mb.x), int(mb.y), 14, pred3, 10)
+		n_mid_raw := scan_col(img, int(mb.x), int(mb.y), 14, steel, 10)
+		n_mid_full := scan_col(img, int(mb.x), int(mb.y), 14, full, 10)
+		check(n_mid >= 8 && n_mid_raw == 0 && n_mid_full == 0,
+			fmt.aprintf("mid-ramp band sits at the CRISIS_FADE16-predicted mix (pred %d / raw %d / full %d — a snap-to-full or no-ramp fails here)", n_mid, n_mid_raw, n_mid_full), n_mid)
+		rl.UnloadImage(img)
+
+		// (e): REDUCED MOTION at the same mid-ramp tick — pinned at FULL
+		view.reduced_motion = true
+		rl.BeginDrawing()
+		rl.ClearBackground(rl.Color{237, 226, 200, 255})
+		rnd.draw_world(&view, &state.topology, &state.bundles, &state.flow, &state.crisis, 1003, {}, -1, -1, state.seed)
+		rl.EndDrawing()
+		img = rl.LoadImageFromScreen()
+		normalize(&img)
+		n_rm_full := scan_col(img, int(mb.x), int(mb.y), 14, full, 10)
+		n_rm_mid := scan_col(img, int(mb.x), int(mb.y), 14, pred3, 10)
+		check(n_rm_full >= 8 && n_rm_mid == 0,
+			fmt.aprintf("reduced motion pins the desat at full (full %d / mid-ramp %d px)", n_rm_full, n_rm_mid), n_rm_full)
+		rl.UnloadImage(img)
+		view.reduced_motion = false
+
+		// (f) THE DUBLIN STREET BLOCK (Perkins r1 B1 — the mutation-vacuous
+		// surface): no Dublin demo renders a ZONE crisis (dublin_board
+		// captures pool-only, where the carve-out zeroes the factor), so the
+		// block recede had NO gate — deleting it kept the corpus 49/49. This
+		// leg renders the §7 fixture's TERMINAL nodes under map_source=Dublin
+		// (draw_nodes directly on a paper canvas — the block draw needs the
+		// board's street cache, not the map render) with the zone crisis
+		// live, and scans the block FILLS: the alpha-twin recede composite
+		// on the non-involved terminal, the raw composite on the involved
+		// one. Deleting the block recede (or the alpha twin) fails here.
+		bd, be := board_load(cat)
+		if be != "" {
+			check(false, "dublin board loads (the B1 leg premise)", 0)
+		} else {
+			sv_ms, sv_bd := view.map_source, view.board
+			view.map_source = u8(pp.Map_Source.Dublin)
+			view.board = bd
+			rnd.dublin_render_ensure(&view)
+			// The EMPIRICAL composites (measured on this renderer, then
+			// pinned): rlsw renders the block's DrawTriangle fill OPAQUE —
+			// the fam token's alpha byte (204) is inert on this surface, so
+			// the recede's RGB MIX carries the whole effect: the involved
+			// block reads the PURE family RGB; the receded block reads the
+			// crisis_recede mix (fam*0.35 + canvas*0.65, u8-truncated —
+			// ±1 in g/b from the f32 mix, tolerance 6). The frontage edge
+			// line (a=90, blended) lands near the receded mix too — hence
+			// the generous window + the exact-one-side-zero shape.
+			paper := rl.Color{237, 226, 200, 255}
+			fam := view.palette.residential_family
+			raw_blk := rl.Color{fam.r, fam.g, fam.b, 255}
+			rec_blk := rnd.crisis_recede(&view, 1.0, fam)
+			rl.BeginDrawing()
+			rl.ClearBackground(paper)
+			rnd.draw_nodes(&view, &state.topology, &state.crisis, 1100, 1.0)
+			rl.EndDrawing()
+			img := rl.LoadImageFromScreen()
+			normalize(&img)
+			// generous windows (the street-aligned block sits within ~20px of
+			// the node center; the chip glyph rides ~29px ABOVE it — the up
+			// window covers both; the wide probe measured 113 px per
+			// composite on exactly this fixture, interior-only ≈ 41)
+			n_blk_inv := scan_box(img, int(c0.x), int(c0.y), 20, 32, 18, raw_blk, 6)
+			n_blk_non_raw := scan_box(img, int(c2.x), int(c2.y), 20, 32, 18, raw_blk, 6)
+			n_blk_non_rec := scan_box(img, int(c2.x), int(c2.y), 20, 32, 18, rec_blk, 6)
+			check(n_blk_inv >= 60, fmt.aprintf("dublin: involved block keeps the raw family fill (%d px)", n_blk_inv), n_blk_inv)
+			check(n_blk_non_rec >= 60 && n_blk_non_raw == 0,
+				fmt.aprintf("dublin: non-involved block recedes (receded %d / raw %d px — deleting the block recede renders raw and fails here)", n_blk_non_rec, n_blk_non_raw), n_blk_non_rec)
+			rl.UnloadImage(img)
+			view.map_source = sv_ms
+			view.board = sv_bd
+		}
+
+		pp.run_destroy(&state)
+	}
+
 	if fails > 0 {
 		fmt.printfln("palcheck: %d check(s) FAILED", fails)
 		return 1


--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "blind",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact diff lines that prove the claim, pasted verbatim from the diff above. Use 'N/A' only when the claim is about something genuinely absent from the diff (e.g. a missing test file). Paraphrased or reconstructed evidence is hallucination — drop the finding instead.>",
  "detail": "<≤40 words>",
  "recommended_fix": "<≤40 words>"
}

Output contract: ONLY the JSON array. No prose, no fencing, no preamble. `[]` is valid.

ACCURACY MANDATE: no claim you make will be taken at face value. Every finding will be cross-checked against the actual diff before reporting. Findings whose `evidence` cannot be located in the diff above, or whose claims contradict what the diff actually shows, are DISCARDED silently. Quote the exact diff lines in `evidence`. Speculation without quoted evidence is dropped. Accuracy > volume — an empty array is an honest answer when nothing is wrong.

--- HEADLESS FILE-OUTPUT CONTRACT (overrides the reply channel) ---
Instead of returning the JSON array in your reply: WRITE ONLY the JSON array to this exact absolute path using your file-write tool:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-viscomm-crisis-duck/r2/blind-c2.json
Then stop. Do not write anything else anywhere. Do not create any other files. Do not read any repository file, do not explore any directory, do not run any repository command — the diff below is ALL the context you are permitted; reading anything beyond it invalidates your lens.
