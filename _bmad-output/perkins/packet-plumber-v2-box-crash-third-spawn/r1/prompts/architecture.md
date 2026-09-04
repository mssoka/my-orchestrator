You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
---
project_name: 'Packet Plumber'
user_name: 'Moses'
date: '2026-08-08'
sections_completed: ['technology_stack', 'engine_rules', 'design_locks', 'performance_rules', 'organization_rules', 'testing_rules', 'platform_rules', 'anti_patterns']
status: 'complete'
optimized_for_llm: true
forge: '_bmad-output/planning-artifacts/forge-packet-plumber-2026-08-05/forged-idea.md'
brief: '_bmad-output/planning-artifacts/briefs/brief-Packet-Plumber-2026-08-05/brief.md'
architecture: '_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md'
supersedes: 'the Godot 4.7.1 pin (pre-pivot revision of this file); the engine pivot to Odin + Raylib was decided by the user on 2026-08-08'
---

# Project Context for AI Agents

_This file contains critical rules and patterns that AI agents must follow when implementing game code in this project. Focus on unobvious details that agents might otherwise miss. The forge governs locked design decisions; the game brief is the design source of truth; the Odin architecture governs technical structure; this file governs how code gets written._

**Project:** Packet Plumber — a top-down routing puzzle where you are a network engineer keeping the internet alive: draw pipes between nodes, route colored packets by type, predict and survive fair crises, and upgrade infrastructure as the internet evolves through eras. Mini Motorways **light-daytime** visual style (art-direction amendment A1); **desktop-first launch** (Steam PC/Mac; mobile follows when the Odin+raylib toolchain matures — FORGE #6 amended by user ruling, lavish 2026-08-08). At this stage the project is in the **Odin pivot**: the Godot prototype (PR #11/#12) proved the fun and is preserved as the `prototype-fun-gate` tag (removed from main on the first Odin code PR — ruled 2026-08-08); the Odin build (packages at the repo root: `core/`, `app/`, `harness/`) is the real codebase, per `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md`.

**Citation tags:** `[FORGE #n]` = a sealed decision from the forge (`_bmad-output/planning-artifacts/forge-packet-plumber-2026-08-05/forged-idea.md`); `[BRIEF]` = sealed at the game-brief level; `[ODN-n]` = an architectural decision in the Odin architecture; `[LOOK]` = look-book v1 visual canon.

## Technology Stack & Versions

- **Language:** Odin **`dev-2026-08`** (pin exact; `.odin-version` + CI enforce; recheck at phase boundaries). Verified against upstream releases 2026-08-08.
- **Renderer/platform lib:** **raylib 6.0** via Odin's shipped `vendor:raylib` bindings (6.0-binding fixes landed in Odin dev-2026-07a). No third-party package manager.
- **Harness raylib build:** the golden-image harness builds raylib from source with the **software renderer (`rlsw`) + memory platform** (`tools/build_raylib_sw.sh`) so pixel goldens are bit-identical on every machine with no GPU/display. The game binary uses the stock `vendor:raylib` GPU build.
- **Viewport & framing:** 1280×720 landscape **design grid**; resizable window reveals more map (camera-fit calculation in the render layer — the GL5.2 `aspect=expand` doctrine re-implemented). Landscape-only doctrine unchanged [RULING — user, 2026-08-05].
- **Typing:** Odin is statically typed by construction; use explicit integer widths (`i32/u32/u64`) on all sim state.
- **Tests:** `odin test` (`core:testing`, `@(test)`) for the pure core; the golden-image harness (`harness/`, ODN-17) for scripted scenarios + visual regression. Everything testable headless, is.
- **Reference build:** `game/` is the frozen Godot prototype — behavioral reference only; never ported line-by-line, never extended.

## Critical Implementation Rules

### Stack-Specific Rules (Odin + raylib — the pivot trap set)

- **The core is pure.** `core/` imports only whitelisted `core:*` packages — never `vendor:*`, never `core:os`, never `core:time` (ODN-1). The sim steps only via `core.step(state, tick, commands)`; nothing in core reads a clock, a file, or a device. CI compile-checks this.
- **Integer-only sim paths.** All state-affecting math is integer or explicit fixed-point (ODN-10). Floats exist only in the view (interpolation, pulses) and never flow back into state. Catalog sim values are integers; cosmetic floats are labeled.
- **Never iterate a `map` in core.** Odin map order is unspecified — core iterates arrays/slices/`#soa` only (insertion-ordered, stable). Maps are lookup-only. Equal-candidate tie-breaks draw from `state.rng` (ODN-9/10).
- **RNG is owned, never global.** Sim randomness comes only from the `Rng` held in `Run_State` (owned splitmix64→PCG32 XSH-RR, test vectors pinned — ODN-9). Cosmetic randomness (SFX variants, jitter) comes only from the app-owned second stream (ODN-15). `core:math/rand` is not used for sim — its internals may drift between Odin releases.
- **Arena discipline (ODN-18).** Three arenas: run (per-run state), snapshot (ping-pong per tick), frame (reset per frame). Core code never calls `new`/`make` without an explicit allocator argument. Dev builds run the tracking allocator; leaks are CI failures.
- **No globals / singletons.** Everything hangs off `App` → `Run_State`, passed by pointer (ODN-13). Per-run reset = create a fresh run context in a fresh arena; never "clean up and reuse."
- **Events, not callbacks.** Cross-layer communication is the per-tick `Event` tagged-union buffer on `Run_State`, drained by the app after each step (ODN-14). No function-pointer webs, no global bus.
- **Errors are values.** Fallible procs return `(T, Error)` with typed error enums; a dropped error return is a CI lint failure (§7.1 of the architecture). Never catch-and-ignore.
- **Save/log is binary, little-endian, versioned** (ODN-11) — no JSON for state (the JSON-int-to-float trap class is deleted at the root). JSON is for catalogs only, loaded once, fail-fast validated, embedded via `#load()` in release.
- **Runtime-gated debug surface.** The v2-noc NOC dashboard ships in the NORMAL build (2026-08-23 user ruling: useful for players), gated at RUNTIME — panel OFF by default (zero pixels until D), D key gated by the availability flag (settings row "NOC PANEL (D)", default ON, in-session only); removal = one-line default flip. The harness `overlay-check` verb remains behind `-define:PP_DEBUG=true` (a harness dev tool); the capture path never calls the overlay, so goldens cannot shift.
- **Raylib idioms:** immediate-mode drawing only inside `BeginDrawing/EndDrawing`; the static map caches into a `RenderTexture` (redraw on pan/zoom); packets are per-frame draw calls from snapshot arrays — there are no per-entity view objects to pool or free. The harness renders to texture / memory framebuffer, never to screen.

### Game-Rules-as-Code (locked design — enforce in every implementation)

- **Core mechanic is Draw + React, not construct.** PRIMARY: draw pipes between nodes, snapping to nodes (no pixel precision — Mini Metro / Mini Motorways model). SECONDARY: react to PREDICTABLE crises the player saw coming. NOT a Factorio-style construction sim (no material selection, production chains, zoning) `[FORGE #2]`.
- **Terminals connect via routers only — never terminal-to-terminal** (art-direction amendment A6 / look-book D11). Houses are leaves; routers are the interconnect. The Command_Bus rejects terminal↔terminal draws.
- **Crises are FAIR and PREDICTABLE, never random.** A crisis is the consequence of a topology flaw the player should have designed around — warning signs first (🟡 congested → 🔴 critical). Random/unfair chaos was explicitly rejected `[FORGE #3]`. The V2 AI disaster system (out of prototype scope) is a stress-test auditor, not a random bully.
- **Differentiator 1 — packet types + QoS class queues.** Not all packets are equal: gaming wants low latency and can't drop, banking must never drop, streaming wants volume and can buffer, email is low priority. The player allocates each pipe's bandwidth across 3 class queues (Express/Standard/Best-effort); every route is a TRADE-OFF `[FORGE #4]`. All traffic starts on Standard; QoS is player-engineered, never auto.
- **Differentiator 2 — era progression + infrastructure lifecycle.** The internet evolves (ARPANET → email → web → streaming → …); old infrastructure obsoletes and must be upgraded or it suffocates `[FORGE #4]`.
- **Visual style is the look-book light canvas:** warm-cream map, literal buildings (6 terminal types), round capacity-scaled router pucks, smooth bezier pipes (glowing cores on fiber/backbone), blue/grey packets with distinct shapes, procedural land/ocean/parks map, warm colors reserved for danger `[LOOK]`. Color is never the sole encoder (shape + icon + pulse).
- **Cross-platform same-game doctrine:** one game, input-agnostic `[FORGE #6]` — amended 2026-08-08 to desktop-first sequencing: ship Steam PC/Mac first, mobile follows at toolchain maturity; the intent-layer input model keeps all inputs additive.
- **Brand satire, never real brand names.** YouTune / Amazoom / Goggle / Glitch (Netflix and Discord are kept) `[FORGE rejections]`.
- **Name is Packet Plumber** `[FORGE #8]`.

### Performance Rules

- **Target: 60 fps sustained** on desktop; optional unlocked-framerate toggle (off by default on battery devices) `[GDD § Performance]`.
- Fixed 20 Hz logic tick + render interpolation (ODN-2); no per-frame work that the tick model can own. SOA hot loops; zero per-frame heap churn (frame arena).

### Code Organization Rules

- Odin packages live at the repo root (the Odin-native convention, ruled 2026-08-08). **Layout:** `core/` (pure sim), `app/` (game executable: `render/`, `ui/`), `harness/` (golden runner), `demos/`, `data/` (JSON catalogs), `goldens/`, `tools/` (see the architecture §16.2). One directory = one Odin package.
- Naming (Odin stdlib style): types/constants `Ada_Case` · procs/vars `snake_case` · files `snake_case.odin` · privates `_prefixed` where needed.
- **Numbers single-source:** balance numbers live in `data/*.json`, never restated in code (ODN-5).
- Keep all catalog data integer-only for sim values; absent fields use explicit load-time defaults (no sentinel values).

### Testing Rules

- **The golden harness is the verification foundation** (ODN-17): built before feature stories; `harness run` must be green before any PR; `harness save` re-blesses goldens only deliberately and is reviewed like code.
- **Pin every design invariant as a regression test at the lowest layer** (`@(test)` in `core/`): determinism/replay equality, fair-crisis contracts, QoS drop precedence + no-starvation, snap precision, no-soft-lock. Acceptance criteria become durable tests, not PR prose.
- Two golden tiers (architecture §10.2): T1 state-hash goldens (every platform, no GPU) + T2 pixel goldens (software renderer, zero-tolerance). On mismatch the harness emits an agent-readable diff bundle (diff PNG + `diff.json` + replay demo) — read it before theorizing.

### Platform & Build Rules

- **Targets:** Steam PC/Mac first (Windows, macOS builds via `odin build -target:...`; native CI runners per OS × amd64/arm64). **Desktop-first launch (ruled 2026-08-08)** — mobile (Android/iOS) is deferred until the Odin+raylib toolchain matures; do not claim mobile support until a maturity spike lands it. Web/wasm is a possible stopgap, not a launch platform. No console `[BRIEF]`.
- Keep `.odin-version`, the CI matrix, and this file's Technology Stack in sync. Version bumps are deliberate, reviewed events (the PRNG/replay contracts depend on toolchain stability).
- No purchased assets before the playtest gate; placeholder art = colored rects + emoji + system shapes drawn with raylib primitives (the prototype is reference, not shippable).
- **Audio/music:** Suno-generated, owned outright by Moses — paid-tier generations only (commercial rights; Content-ID-free for streamer monetization). Soundtrack is a candidate parallel DistroKid release (owned IP).
- Env files are read-only in worktrees and NEVER committed; any API key (future server features) comes from env only.

### Critical Don't-Miss Rules (anti-patterns)

- **Never use real brand names** — trademark risk; use the satire set `[FORGE rejections]`.
- **Never make a crisis random or unfair** — the player must always be able to say "I should have seen this coming" `[FORGE #3]`.
- **Never build a Factorio-style construction layer** — draw + react is the mechanic `[FORGE #2]`.
- **Never soft-lock the player** — there is always a way to reroute or upgrade out of a crisis.
- **Never let the view touch the sim** — presentation reads immutable snapshots only; input reaches the core only as validated Commands (ODN-1/12).
- **Never sample real time in a test** — the harness drives a virtual clock; demos are deterministic by construction.
- **Never catch-and-ignore** — every error path either recovers (logged) or surfaces.
- **Never re-litigate a locked forge decision.** If a task conflicts with a `[FORGE #n]` lock, STOP and surface it. For everything else, when in doubt, prefer the more restrictive reading.

---

## Usage Guidelines

**For AI Agents:** Read this file before implementing any game code; read the forge and brief for design intent, and the Odin architecture for structure. Follow ALL rules exactly. This is a living document — when the prototype reveals new traps or the architecture pins new structure, update it.

**For Humans:** Source of truth for locked design = the forge; for the design narrative = the game brief; for technical structure = the Odin architecture; for code conduct = this file. Keep this lean and focused on agent needs.

Last Updated: 2026-08-08 (Odin pivot — engine pin redone from Godot 4.7.1 to Odin dev-2026-08 + raylib 6.0)


--- DIFF ---
diff --git a/app/render/spawn_fx.odin b/app/render/spawn_fx.odin
index 566c9ba..f50532c 100644
--- a/app/render/spawn_fx.odin
+++ b/app/render/spawn_fx.odin
@@ -247,6 +247,17 @@ shadow_clone :: proc(src: ^pp.Run_State, allocator := context.allocator) -> pp.R
 	c.era_gate.win_dropped = clone_dyn(g.win_dropped, allocator)
 	c.era_gate.prev_delivered = clone_dyn(g.prev_delivered, allocator)
 	c.era_gate.prev_dropped = clone_dyn(g.prev_dropped, allocator)
+	bx := &src.box
+	c.box.pieces = clone_dyn(bx.pieces, allocator)
+	c.box.spools = clone_dyn(bx.spools, allocator)
+	// ^ THE 2026-08-28 PLAYTEST ABORT (job packet-plumber-v2-box-crash-third-
+	// spawn): the Box (#107) shipped without these two lines — the clone's box
+	// headers aliased the live buffers, the shadow's run_destroy freed them
+	// (predict #1), and the next mid-window connection re-predicted → double
+	// free → libmalloc "pointer being freed was not allocated" SIGABRT. The
+	// box-OFF fixtures above hid it (nil headers delete harmlessly). The gate:
+	// test_spawn_fx_shadow_clone_box_owns_every_array (every owned array
+	// pinned) + test_spawn_fx_predict_box_economy_leg (the playtest leg).
 	return clone
 }
 
@@ -310,6 +321,7 @@ spawn_fx_predict :: proc(v: ^View, state: ^pp.Run_State, cat: ^pp.Catalogs, tick
 			}
 		}
 		pp.step(&shadow, tt, batch[:], cat)
+		delete(batch) // per-tick scratch; temp-allocator frees are no-ops today, but the delete keeps this correct under a tracked allocator (review r1: an earlier comment misclaimed the leak report saw this)
 	}
 	if shadow.topology.next_node_id > nodes_before {
 		// exactly one spawn per window by construction (the growth branch
diff --git a/app/render/spawn_fx_test.odin b/app/render/spawn_fx_test.odin
index 45b5393..abb5d97 100644
--- a/app/render/spawn_fx_test.odin
+++ b/app/render/spawn_fx_test.odin
@@ -108,6 +108,292 @@ sfx_hash :: proc(s: ^pp.Run_State, cat: ^pp.Catalogs) -> u64 {
 	return pp.state_hash(s, {}, cat, context.temp_allocator)
 }
 
+// --- THE BOX SHADOW ALIAS GATE (the 2026-08-28 playtest abort) --------------
+//
+// User playtest SIGABRT (.ips app.bin-2026-08-28-211134/211400, libmalloc
+// "pointer being freed was not allocated" from Odin runtime::_heap_free) on
+// the third spawn-building connection: shadow_clone's hand-maintained array
+// list MISSED the Box arrays (#107) — the clone's box headers aliased the
+// LIVE state's buffers, run_destroy(&shadow) freed them out from under the
+// live sim (predict #1), and the next prediction (each connection bumps
+// topology.gen → re-predict) double-freed the same block → abort. The
+// box-OFF fixtures above hide the class: nil headers delete harmlessly.
+// These two tests make the whole class CI-visible: (1) every owned dynamic
+// array in a clone must be a PRIVATE buffer, with the box ENABLED (the nil
+// trap), and (2) the economy leg — ≥5 spawn windows crossed with
+// place/promote/teardown/resplice + a forced re-predict per connection (the
+// app's live pattern) — which pre-fix aborts exactly like the playtest.
+
+// sfx_no_alias — one field's private-buffer pin (empty headers may be nil on
+// both sides — nothing aliased, delete no-ops; skip them).
+sfx_no_alias :: proc(t: ^testing.T, a, b: [dynamic]$T, ctx, name: string) {
+	if len(a) == 0 {
+		return
+	}
+	testing.expectf(t, raw_data(a) != raw_data(b),
+		"%s: clone.%s aliases the LIVE state's buffer (shadow_clone missed-field class: the shadow's run_destroy frees live memory; the next predict double-frees, the 2026-08-28 playtest SIGABRT)",
+		ctx, name)
+}
+
+@(test)
+test_spawn_fx_shadow_clone_box_owns_every_array :: proc(t: ^testing.T) {
+	cat: pp.Catalogs
+	sfx_load_cat(&cat, context.temp_allocator)
+	defer pp.catalogs_destroy(&cat)
+
+	s: pp.Run_State
+	pp.run_init(&s, 42, cat.hash, cat.balance.logic_hz)
+	defer pp.run_destroy(&s)
+	sfx_fixture(&s, &cat)
+	s.era = 3 // the full kit era: pieces + fiber spools non-empty (the nil trap)
+	pp.box_enable(&s, &cat)
+	for tick in u64(1) ..= 65 {
+		pp.step(&s, tick, {}, &cat)
+	}
+
+	clone := shadow_clone(&s, context.temp_allocator)
+	defer pp.run_destroy(&clone)
+
+	// THE GATE: every step()-touched owned dynamic array is a private buffer.
+	// One line per array run_destroy frees — a NEW Run_State dynamic array
+	// must add (a) its clone line in shadow_clone AND (b) its pin line here.
+	ctx := "box-clone"
+	sfx_no_alias(t, clone.topology.node_alive, s.topology.node_alive, ctx, "topology.node_alive")
+	sfx_no_alias(t, clone.topology.node_id, s.topology.node_id, ctx, "topology.node_id")
+	sfx_no_alias(t, clone.topology.node_kind, s.topology.node_kind, ctx, "topology.node_kind")
+	sfx_no_alias(t, clone.topology.node_role, s.topology.node_role, ctx, "topology.node_role")
+	sfx_no_alias(t, clone.topology.node_type, s.topology.node_type, ctx, "topology.node_type")
+	sfx_no_alias(t, clone.topology.node_pos, s.topology.node_pos, ctx, "topology.node_pos")
+	sfx_no_alias(t, clone.topology.pipe_alive, s.topology.pipe_alive, ctx, "topology.pipe_alive")
+	sfx_no_alias(t, clone.topology.pipe_id, s.topology.pipe_id, ctx, "topology.pipe_id")
+	sfx_no_alias(t, clone.topology.pipe_a, s.topology.pipe_a, ctx, "topology.pipe_a")
+	sfx_no_alias(t, clone.topology.pipe_b, s.topology.pipe_b, ctx, "topology.pipe_b")
+	sfx_no_alias(t, clone.topology.pipe_tier, s.topology.pipe_tier, ctx, "topology.pipe_tier")
+	sfx_no_alias(t, clone.topology.pipe_span, s.topology.pipe_span, ctx, "topology.pipe_span")
+	sfx_no_alias(t, clone.topology.pipe_weights, s.topology.pipe_weights, ctx, "topology.pipe_weights")
+	sfx_no_alias(t, clone.topology.pipe_lane_over, s.topology.pipe_lane_over, ctx, "topology.pipe_lane_over")
+	sfx_no_alias(t, clone.routing.hop_offset, s.routing.hop_offset, ctx, "routing.hop_offset")
+	sfx_no_alias(t, clone.routing.hop_count, s.routing.hop_count, ctx, "routing.hop_count")
+	sfx_no_alias(t, clone.routing.hops, s.routing.hops, ctx, "routing.hops")
+	sfx_no_alias(t, clone.bundles.pipe_bundle, s.bundles.pipe_bundle, ctx, "bundles.pipe_bundle")
+	sfx_no_alias(t, clone.bundles.bundle_lo, s.bundles.bundle_lo, ctx, "bundles.bundle_lo")
+	sfx_no_alias(t, clone.bundles.bundle_hi, s.bundles.bundle_hi, ctx, "bundles.bundle_hi")
+	sfx_no_alias(t, clone.bundles.bundle_cap, s.bundles.bundle_cap, ctx, "bundles.bundle_cap")
+	sfx_no_alias(t, clone.bundles.bundle_count, s.bundles.bundle_count, ctx, "bundles.bundle_count")
+	sfx_no_alias(t, clone.bundles.bundle_tier, s.bundles.bundle_tier, ctx, "bundles.bundle_tier")
+	sfx_no_alias(t, clone.bundles.tx_slot_tick, s.bundles.tx_slot_tick, ctx, "bundles.tx_slot_tick")
+	sfx_no_alias(t, clone.bundles.tx_served, s.bundles.tx_served, ctx, "bundles.tx_served")
+	sfx_no_alias(t, clone.flow.packets, s.flow.packets, ctx, "flow.packets")
+	sfx_no_alias(t, clone.flow.demand, s.flow.demand, ctx, "flow.demand")
+	sfx_no_alias(t, clone.flow.sla, s.flow.sla, ctx, "flow.sla")
+	sfx_no_alias(t, clone.flow.sla_breach, s.flow.sla_breach, ctx, "flow.sla_breach")
+	sfx_no_alias(t, clone.flow.lane_caps, s.flow.lane_caps, ctx, "flow.lane_caps")
+	sfx_no_alias(t, clone.flow.spawn_credit_milli, s.flow.spawn_credit_milli, ctx, "flow.spawn_credit_milli")
+	sfx_no_alias(t, clone.flow.drop_sites, s.flow.drop_sites, ctx, "flow.drop_sites")
+	sfx_no_alias(t, clone.flow.serviced_this_tick, s.flow.serviced_this_tick, ctx, "flow.serviced_this_tick")
+	sfx_no_alias(t, clone.flow.residency.slot_tick, s.flow.residency.slot_tick, ctx, "flow.residency.slot_tick")
+	sfx_no_alias(t, clone.flow.residency.ticks, s.flow.residency.ticks, ctx, "flow.residency.ticks")
+	sfx_no_alias(t, clone.crisis.node_congestion, s.crisis.node_congestion, ctx, "crisis.node_congestion")
+	sfx_no_alias(t, clone.crisis.pipe_congestion, s.crisis.pipe_congestion, ctx, "crisis.pipe_congestion")
+	sfx_no_alias(t, clone.crisis.forecast, s.crisis.forecast, ctx, "crisis.forecast")
+	sfx_no_alias(t, clone.crisis.active, s.crisis.active, ctx, "crisis.active")
+	sfx_no_alias(t, clone.crisis.cooldowns, s.crisis.cooldowns, ctx, "crisis.cooldowns")
+	sfx_no_alias(t, clone.crisis.node_health, s.crisis.node_health, ctx, "crisis.node_health")
+	sfx_no_alias(t, clone.health.breach, s.health.breach, ctx, "health.breach")
+	sfx_no_alias(t, clone.health.grace, s.health.grace, ctx, "health.grace")
+	sfx_no_alias(t, clone.health.prev_delivered, s.health.prev_delivered, ctx, "health.prev_delivered")
+	sfx_no_alias(t, clone.health.prev_dropped, s.health.prev_dropped, ctx, "health.prev_dropped")
+	sfx_no_alias(t, clone.health.prev_latency, s.health.prev_latency, ctx, "health.prev_latency")
+	sfx_no_alias(t, clone.health.win_delivered, s.health.win_delivered, ctx, "health.win_delivered")
+	sfx_no_alias(t, clone.health.win_dropped, s.health.win_dropped, ctx, "health.win_dropped")
+	sfx_no_alias(t, clone.health.win_latency, s.health.win_latency, ctx, "health.win_latency")
+	sfx_no_alias(t, clone.health.ring, s.health.ring, ctx, "health.ring")
+	sfx_no_alias(t, clone.era_gate.ring, s.era_gate.ring, ctx, "era_gate.ring")
+	sfx_no_alias(t, clone.era_gate.win_delivered, s.era_gate.win_delivered, ctx, "era_gate.win_delivered")
+	sfx_no_alias(t, clone.era_gate.win_dropped, s.era_gate.win_dropped, ctx, "era_gate.win_dropped")
+	sfx_no_alias(t, clone.era_gate.prev_delivered, s.era_gate.prev_delivered, ctx, "era_gate.prev_delivered")
+	sfx_no_alias(t, clone.era_gate.prev_dropped, s.era_gate.prev_dropped, ctx, "era_gate.prev_dropped")
+	sfx_no_alias(t, clone.box.pieces, s.box.pieces, ctx, "box.pieces") // THE 2026-08-28 MISS
+	sfx_no_alias(t, clone.box.spools, s.box.spools, ctx, "box.spools") // THE 2026-08-28 MISS
+	// action_log/events are ZEROED in the clone by design (shadow_clone's
+	// contract) — asserted nil here so a future regression to aliasing (or a
+	// copy) of them is caught too.
+	testing.expect(t, raw_data(clone.action_log) == nil || len(clone.action_log) == 0, "clone.action_log must stay zeroed")
+	testing.expect(t, raw_data(clone.events) == nil || len(clone.events) == 0, "clone.events must stay zeroed")
+
+	// box-ON round trip: with the stock cloned, clone+step stays hash-identical
+	// (the box section rides the T1 hash when enabled — a missed box field
+	// drifts the telegraph exactly like the arrays above).
+	piece_ok := len(clone.box.pieces) == len(s.box.pieces)
+	testing.expectf(t, piece_ok, "clone box pieces must mirror the live shape")
+	pp.step(&s, 66, {}, &cat)
+	pp.step(&clone, 66, {}, &cat)
+	testing.expectf(t, sfx_hash(&clone, &cat) == sfx_hash(&s, &cat),
+		"box-ON clone+step must stay hash-identical to the live sim (a missed box field drifts the telegraph)")
+	testing.expect(t, !clone.replay_error, "the shadow must not latch replay_error")
+}
+
+// sfx_count_new_spawns — NODE_SPAWNED events in s.events[from:] (events
+// accumulate until the app drains — core never clears).
+sfx_count_new_spawns :: proc(s: ^pp.Run_State, from: int) -> u32 {
+	n: u32 = 0
+	for e in s.events[from:] {
+		if e.tag == pp.EVENT_TAG_NODE_SPAWNED {
+			n += 1
+		}
+	}
+	return n
+}
+
+// sfx_find_place_spot — the first valid placement spot on a fixed probe ring
+// around the fixture router (deterministic; no rng). Sentinel {-1,-1} when
+// nothing validates — placement_valid refuses the negative grid coordinate,
+// so the caller's apply assert fails loudly (review r1: {0,0} could
+// silently validate).
+sfx_find_place_spot :: proc(s: ^pp.Run_State, cat: ^pp.Catalogs, type_idx: u16) -> [2]i32 {
+	deltas := [][2]i32{{4, 0}, {-4, 0}, {0, 4}, {0, -4}, {5, 5}, {-5, 5}, {5, -5}, {-5, -5}, {6, 0}, {0, 6}, {-6, 0}, {0, -6}, {7, 3}, {-7, -3}, {3, 7}, {-3, -7}, {8, 0}, {0, 8}, {-8, 0}, {0, -8}, {9, 4}, {-9, -4}, {4, 9}, {-4, -9}, {10, 0}, {0, 10}, {-10, 0}, {0, -10}}
+	for d in deltas {
+		pos := [2]i32{12 + d[0], 10 + d[1]}
+		c := pp.Cmd_Place_Router{type_idx = type_idx, pos = pos}
+		if pp.box_check_place(s, c, cat) == .None {
+			return pos
+		}
+	}
+	return {-1, -1}
+}
+
+// sfx_connect_newest — a valid standard-tier draw from the newest spawned
+// terminal to the first junction that prices (the "connect the spawn
+// building" action the user was performing). Returns tier = 0xffff when no
+// pair validates (the caller's apply assert fails loudly).
+sfx_connect_newest :: proc(s: ^pp.Run_State, cat: ^pp.Catalogs) -> pp.Cmd_Draw_Pipe {
+	newest := s.topology.next_node_id - 1
+	for i in 0 ..< len(s.topology.node_alive) {
+		if !s.topology.node_alive[i] || s.topology.node_kind[i] != .Junction {
+			continue
+		}
+		c := pp.Cmd_Draw_Pipe{a = s.topology.node_id[i], b = newest, tier = 0}
+		if pp.box_check_draw(s, c, cat) == .None {
+			return c
+		}
+	}
+	return {a = 0, b = 0, tier = 0xffff}
+}
+
+@(test)
+test_spawn_fx_predict_box_economy_leg :: proc(t: ^testing.T) {
+	// The playtest repro as a gate: FIVE spawn windows, each crossed with a
+	// Box economy edit (place / connect / resplice / teardown / promote) and a
+	// FORCED telegraph re-predict per connection (the app's live pattern —
+	// every edit bumps topology.gen and main.odin re-predicts mid-window).
+	// Pre-fix, predict #1's shadow destroy frees the live Box buffers and
+	// predict #2 double-frees them: this leg ABORTS with the .ips signature.
+	cat: pp.Catalogs
+	sfx_load_cat(&cat, context.temp_allocator)
+	defer pp.catalogs_destroy(&cat)
+	interval := u64(cat.balance.terminal_spawn_interval_ticks)
+
+	s: pp.Run_State
+	pp.run_init(&s, 42, cat.hash, cat.balance.logic_hz)
+	defer pp.run_destroy(&s)
+	sfx_fixture(&s, &cat)
+	s.era = 3 // router_mid/high pieces + fiber spool: the full promote/resplice kit
+	pp.box_enable(&s, &cat)
+
+	v: View
+	v.catalogs = &cat
+
+	mid, _ := pp.node_type_index(&cat, "router_mid")
+	spawns: u32 = 0
+	t_prev := u64(0)
+	for w in u64(1) ..= 5 {
+		base := interval * w
+		lead := base - 5 // inside the 10-tick telegraph lead, like the playtest
+		for tick in t_prev + 1 ..= lead {
+			mark := len(s.events)
+			pp.step(&s, tick, {}, &cat)
+			spawns += sfx_count_new_spawns(&s, mark)
+		}
+		t_prev = lead
+
+		apply :: proc(t: ^testing.T, s: ^pp.Run_State, cat: ^pp.Catalogs, w: u64, kind: pp.Command_Kind) {
+			_, e := pp.box_apply_edit(s, pp.Command{apply_tick = 0, kind = kind}, cat)
+			testing.expectf(t, e == .None, "w%d economy edit refused: %v (the leg requires every edit to apply)", w, e)
+		}
+
+		// w1 PLACE a mid router; w2 CONNECT the newest spawn; w3 RESPLICE it to
+		// mid (fiber drains, standard refunds); w4 TEARDOWN that pipe (full
+		// refund); w5 PROMOTE: demolish the w1 router (piece + incident tiles
+		// refund) — the demolish+place promotion cycle's expensive half.
+		switch w {
+		case 1:
+			pos := sfx_find_place_spot(&s, &cat, mid)
+			apply(t, &s, &cat, w, pp.Cmd_Place_Router{type_idx = mid, pos = pos})
+		case 2:
+			draw := sfx_connect_newest(&s, &cat)
+			apply(t, &s, &cat, w, draw)
+		case 3:
+			pipe := s.topology.pipe_id[len(s.topology.pipe_id) - 1]
+			apply(t, &s, &cat, w, pp.Cmd_Set_Pipe_Tier{pipe = pipe, tier = 1})
+		case 4:
+			pipe := s.topology.pipe_id[len(s.topology.pipe_id) - 1]
+			apply(t, &s, &cat, w, pp.Cmd_Demolish_Pipe{pipe = pipe})
+		case 5:
+			// the highest PLACED junction id (monotonic ids; the fixture's id 1
+			// and 3 are junctions too — place went higher)
+			placed: u32 = 0
+			for i in 0 ..< len(s.topology.node_alive) {
+				if s.topology.node_alive[i] && s.topology.node_kind[i] == .Junction {
+					placed = max(placed, s.topology.node_id[i])
+				}
+			}
+			apply(t, &s, &cat, w, pp.Cmd_Demolish_Node{node = placed})
+		case:
+		}
+
+		// the re-predict the app fires on every mid-window connection
+		spawn_fx_predict(&v, &s, &cat, lead, {}, true)
+		// the leg's own teeth: the re-predict must leave the live Box buffers
+		// OWNED. Pre-fix, predict #1's shadow destroy already freed them — this
+		// pin fails deterministically here (the app's default heap aborts on the
+		// same state: the next predict double-frees — the .ips signature).
+		probe := shadow_clone(&s, context.temp_allocator)
+		sfx_no_alias(t, probe.box.pieces, s.box.pieces, "economy-leg", "box.pieces")
+		sfx_no_alias(t, probe.box.spools, s.box.spools, "economy-leg", "box.spools")
+		pp.run_destroy(&probe)
+		testing.expectf(t, v.spawn_fx.telegraph_valid, "w%d: lead tick %d is inside the telegraph window, a telegraph must be live", w, lead)
+		testing.expectf(t, v.spawn_fx.telegraph.spawn_tick == base, "w%d: telegraph window %d, want %d", w, v.spawn_fx.telegraph.spawn_tick, base)
+
+		// stock sanity after the shadow touched the run: every counter within
+		// [0, era cap] (a corrupted/aliased buffer shows up as heap garbage —
+		// the deterministic alias gate above is the exact pin; this is the net)
+		row, ok := pp.era_row(&cat, s.era)
+		testing.expect(t, ok, "era 3 must have a catalog row")
+		for i in 0 ..< len(s.box.pieces) {
+			cap := u32(0)
+			if i < len(row.box_pieces) {
+				cap = row.box_pieces[i]
+			}
+			testing.expectf(t, s.box.pieces[i] <= cap, "w%d: pieces[%d] = %d over cap %d (aliased/corrupted box stock)", w, i, s.box.pieces[i], cap)
+		}
+		for i in 0 ..< len(s.box.spools) {
+			cap := u32(0)
+			if i < len(row.box_spools) {
+				cap = row.box_spools[i]
+			}
+			testing.expectf(t, s.box.spools[i] <= cap, "w%d: spools[%d] = %d over cap %d (aliased/corrupted box stock)", w, i, s.box.spools[i], cap)
+		}
+	}
+	// finish the run through the last window so the real spawns land
+	for tick in t_prev + 1 ..= interval * 5 {
+		mark := len(s.events)
+		pp.step(&s, tick, {}, &cat)
+		spawns += sfx_count_new_spawns(&s, mark)
+	}
+	testing.expectf(t, spawns >= 5, "the leg must cross >= 5 spawn windows: got %d", spawns)
+	testing.expect(t, !s.replay_error, "the economy leg must stay replay-clean")
+}
+
 @(test)
 test_spawn_fx_shadow_clone_round_trips :: proc(t: ^testing.T) {
 	cat: pp.Catalogs


--- SPEC / CONTEXT ---
# Briefing: packet-plumber-v2-box-crash-third-spawn (URGENT)

BUG FIX — user's playtest (the fun-test gate on merged #107) is BLOCKED:
the game crashes when connecting the THIRD spawn building. Top priority;
the user is waiting to play.

## The evidence (in hand)

- TWO macOS crash reports, minutes apart (user reproduced twice):
  - `~/Library/Logs/DiagnosticReports/app.bin-2026-08-28-211134.ips`
  - `~/Library/Logs/DiagnosticReports/app.bin-2026-08-28-211400.ips`
- Signature (both): SIGABRT / Abort trap 6,
  `___BUG_IN_CLIENT_OF_LIBMALLOC_POINTER_BEING_FREED_WAS_NOT_ALLOCATED`
  raised from Odin `runtime::_heap_free` (heap_allocator_unix.odin).
  The app-level caller frames are lost to the abort path — you must
  reproduce to get the true stack.
- Repro: launch app.bin from merged v2 HEAD (396064b), connect spawn
  buildings — crash on the third connection.
- Timing: POST-#107-merge. The Box (typed pieces, spools, caps,
  promotion, teardown/resplice returns, era/milestone refill structures)
  is the prime suspect surface.

## Leading hypothesis (verify, do not assume)

The THIRD spawn is the tell: a dynamic array at capacity 2 growing to 4
— the grow/realloc path double-frees or frees an unallocated pointer
(stale capacity tracking, freed old buffer kept in a slice header,
manual free of a runtime-managed allocation). Audit every Box-owned
dynamic collection that grows on spawn connection: placed-piece arrays,
spool/ledger entries, refill-dot queues, per-spawn economy state.
Siblings to check: teardown/resplice return paths (piece returns to the
Box), and any `free`/`delete` on reslice.

## Method

1. Reproduce headlessly: script the repro in the sim/harness (connect 3
   spawns; the harness speaks scenarios). If headless doesn't trigger
   it, reproduce via app.bin under Odin's debug allocator
   (`-debug` build flags / ODIN allocator checks) to catch the invalid
   free AT THE CALL SITE with a real stack.
2. Fix the invalid free at its root (allocator discipline — no
   double-free, no freeing non-owned pointers; prefer runtime-managed
   growth over manual free/realloc).
3. Regression gate: a test/sim leg that connects >= 5 spawns across
   place/promote/teardown/resplice cycles — MUST crash (or fail the
   allocator check) RED before the fix and pass GREEN after
   (mutation-leg standard: the gate has to be able to fail).
4. Verify both user .ips signatures are explained by the root cause
   (same site or say why not).
5. Sweep the WHOLE Box surface for the same pattern (every manual free
   adjacent to growable state) — fix class-mates in the same PR, listed
   explicitly.

## Ops

- URGENT lane: the user is mid-playtest; fast correct beats slow
  perfect, but the regression gate is NOT optional.
- PR vs v2 (fresh head at dispatch), pr_review=1 (canon surface:
  economy/serialization semantics). check-pr-ready before close.
- CI billing-block signature (5s run / zero logs) = note-only; local
  gates are ground truth.
- bash 3.2 — no arrays in scripts.
- Perkins brief carries: crash reports paths, repro, this hypothesis.

## Skills policy

- `bmad-build` (step 04 review swarm MANDATORY).

## Model policy

- Minion: zai-coding-cn/glm-5.3-flash, --thinking max; mega-minions
  same pin.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-box-crash-third-spawn
- base: v2 (fresh head at dispatch — currently 396064b)
- model: zai-coding-cn/glm-5.3-flash --thinking max
- github_issue: (none)
- pr_review: 1


## Crash context (from the Perkins round briefing)

The merged #107 (The Box) shipped an invalid-free crash: the user's playtest SIGABRTs on the THIRD spawn-building connection — `___BUG_IN_CLIENT_OF_LIBMALLOC_POINTER_BEING_FREED_WAS_NOT_ALLOCATED` from Odin `runtime::_heap_free` (heap_allocator_unix.odin), twice reproduced (.ips files app.bin-2026-08-28-211134.ips and ...-211400.ips; app frames lost to the abort path). The fix commit (this diff, 396064b..444334d) claims the root cause: `shadow_clone` of Box-owned arrays created non-owning slices whose later free hit the allocator. The briefing's LEADING HYPOTHESIS (to verify, not assume) was a 2-to-4 grow/realloc double-free on the third spawn — check whether the diff's mechanism actually explains the evidence instead. Spec acceptance criteria from the job briefing: (1) fix the invalid free at its root — allocator discipline, no double-free, prefer runtime-managed growth; (2) regression gate: >=5 spawns across place/promote/teardown/resplice cycles, RED before fix / GREEN after; (3) both .ips signatures explained; (4) whole-Box-surface class sweep, class-mates fixed in the same PR and listed explicitly.

--- YOUR LENS ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests - use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract:
- ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE - this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY - they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination - drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume - an empty array is a fine and honest answer when nothing is wrong.


--- OUTPUT (FILE CONTRACT — overrides any instruction to print) ---
Write ONLY your JSON array (the findings, schema above) to this exact path, then stop:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-box-crash-third-spawn/r1/architecture.json
Use the write-file capability; the file content must be ONLY the JSON array — no prose, no markdown fencing, no preamble. Empty array [] is valid. After writing the file, end your turn.
