You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. The repository checkout at your current working directory IS the exact reviewed state — trust it. (Exception: you may write exactly one file — your output JSON file named at the end of this prompt.)

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
- **Compile-time debug gates.** Debug tools behind `-define:PP_DEBUG=true` (real conditional compilation); release builds contain no cheat/debug code.
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
diff --git a/_bmad-output/design-analysis/pop/growth-88000-thumb.png b/_bmad-output/design-analysis/pop/growth-88000-thumb.png
new file mode 100644
index 0000000..1f51d5d
Binary files /dev/null and b/_bmad-output/design-analysis/pop/growth-88000-thumb.png differ
diff --git a/_bmad-output/design-analysis/pop/juice-30000-thumb.png b/_bmad-output/design-analysis/pop/juice-30000-thumb.png
new file mode 100644
index 0000000..97f64ea
Binary files /dev/null and b/_bmad-output/design-analysis/pop/juice-30000-thumb.png differ
diff --git a/_bmad-output/design-analysis/pop/juice-calm-surge.png b/_bmad-output/design-analysis/pop/juice-calm-surge.png
new file mode 100644
index 0000000..9f5be49
Binary files /dev/null and b/_bmad-output/design-analysis/pop/juice-calm-surge.png differ
diff --git a/_bmad-output/design-analysis/pop/router_tiers-02500-thumb.png b/_bmad-output/design-analysis/pop/router_tiers-02500-thumb.png
new file mode 100644
index 0000000..231470b
Binary files /dev/null and b/_bmad-output/design-analysis/pop/router_tiers-02500-thumb.png differ
diff --git a/_bmad-output/design-analysis/pop/saturation-evidence.md b/_bmad-output/design-analysis/pop/saturation-evidence.md
new file mode 100644
index 0000000..7d9c0fc
--- /dev/null
+++ b/_bmad-output/design-analysis/pop/saturation-evidence.md
@@ -0,0 +1,102 @@
+# v2-network-pop — saturation + thumbnail evidence
+
+Job: packet-plumber-v2-network-pop (2026-08-22). User ruling: "networking is
+boring… has to make good attention-grabbing thumbnails." Measured root cause
+(design-audit): the v2-look-polish LEFOU system-tone pass muted the pipe
+tiers to gray-blue, killing the saturation ceiling (0.51–0.57 calm vs MM
+0.91–1.00). This pass reverses the mute **in palette tokens only** — no
+geometry, no sim, no LOG_VERSION.
+
+## Method (reproduction-pinned)
+
+The audit's metric: **HSL saturation, mean of the top-2% pixels** ("top-2%
+saturation ceiling"). Reproduced to ±0.004 on the audit's own stills
+(juice-30000: 0.571 vs audit 0.570; juice-65000: 0.825 vs 0.825;
+terminal_types-05000: 0.574 vs 0.572) with
+`python3 - <<EOF` + PIL `colorsys.rgb_to_hls`. Same script re-measures the
+re-blessed goldens (same demos, same pinned sha base).
+
+## The change (data/palette.json + palette.odin mirrors)
+
+| Token | Before (muted) | After (vivid) | HSL sat | Hue ° |
+|---|---|---|---|---|
+| pipe_copper (narrow) | #968E84 warm gray | #F06E00 copper-orange | 1.00 | 27.5 |
+| pipe_steel (standard) | #7E8692 neutral | #0096F0 cyan | 1.00 | 202.5 |
+| pipe_fiber (wide) | #586E8E slate | #FFD700 gold (the direction's anchor) | 1.00 | 50.6 |
+| lane_standard | #6C7A8E | #3882C8 steel-blue | 0.73 | 212 |
+| lane_best_effort | #58986C | #30B260 green | 0.74 | 140 |
+| router_led | #2E8B57 | #00CD5A vivid LED green | 0.76 | 145 |
+| packet_dot / packet_dark | #408CDC / #1C4678 | #0082FF / #003C96 | — | — |
+
+Untouched (the calm board + canon pins): canvas, grid, water, coast, park,
+ink, house/host/roofs, router_body/dark, pipe_unalloc, lane_express
+(the palcheck LANE_AMBER pin), state triad, sel_halo, route tokens, the a11y
+mode tables, the packet catalog (cat.hash is golden-poison — packets already
+render at catalog maxima: streaming #1E4A98 is the saturated core, email
+#5A6270 is look-book canon grey D4).
+
+Tier hues are pairwise-separated 23°/152°/175° (≥ the audit's 15° blur-test
+standard). Network layer hue split by band area (narrow 3.5² + standard 5.5²
++ wide 8.5² → 74% warm-gold family / 26% cool-cyan): the direction's
+"network 70% warm-gold / 30% cool-cyan" executed with real geometry, not a
+ratio in the head.
+
+## Re-measurement (re-blessed goldens at the pinned sha, same demos)
+
+| Frame | Before (audit) | After | Δ |
+|---|---|---|---|
+| juice-30000ms (calm busy neighborhood — the thumbnail hero) | 0.570 | **0.886** | +0.316 |
+| juice-65000ms (surge) | 0.825 | **0.879** | +0.054 |
+| estate_surge-25000ms | 0.532 | **0.913** | +0.381 |
+| estate_surge-75000ms | 0.833 | **0.899** | +0.066 |
+| growth-88000ms (late dense) | 0.687 | 0.826 | +0.139 |
+| terminal_types-05000ms | 0.572 | 0.715 | +0.143 |
+| router_tiers-02500ms | 0.513 | 0.698 | +0.185 |
+| growth-01500ms (1 puck, no pipes) | 0.513 | 0.513 | ±0.000 |
+
+The audit's pop-mock (its own saturated-network approximation) measured
+0.685 on the right half; the shipped build exceeds the mock on every
+network-bearing frame.
+
+## Why the sparse frames stop short of 0.85 (surface physics, not choice)
+
+The ceiling is the mean of the top 2% of pixels (18,432 px @ 1280×720).
+Frames whose network surface is smaller than that population cannot reach
+0.85 — the boundary falls into the canvas mass (HSL 0.51) once the saturated
+pixels run out. Measured saturated population (sat ≥ 0.85) after the change:
+router_tiers-02500 = 8,329 px, terminal_types-05000 = 7,816 px — both far
+below 18,432 even with every pipe at sat 1.0 (the cyan pipes already are).
+The only token lever that would close the gap is saturating the BOARD
+(canvas/water) — explicitly forbidden by the briefing's rule 3 (the 70/30
+split; "a fully-saturated board fails the direction's own standard") and
+canon D9 ("water/parks are soft, never saturated"). Raising the ceiling
+there requires more saturated network surface = art/geometry, out of the
+token-only scope. The dense frames — the ones a thumbnail actually shows —
+all cross 0.85.
+
+## Thumbnail hero-read (427×240, streamer-card scale)
+
+Vision (glm-4.6v, the standing KYLE model) on the downscaled frames:
+- juice-30000: "the right side's network absolutely reads as the hero
+  element. The vibrant pipes stand out dramatically against the calm,
+  desaturated background board… The board has stayed calm… no garish or
+  broken colors."
+- terminal_types/router_tiers: "the network is the most eye-catching
+  element in both thumbnails… the board is calm (desaturated paper-like)."
+- Full-res calm + surge: "three tiers clearly distinguishable (orange,
+  blue, yellow) + thickness… dark rim + bright band, no muddy… crisis red
+  still stands out against the saturated network."
+
+Strips: `pop/juice-30000-thumb.png` (left = pre-change 427×240, right =
+post-change), `pop/terminal_types-05000-thumb.png`, `pop/router_tiers-
+02500-thumb.png`, `pop/growth-88000-thumb.png`, `pop/juice-calm-surge.png`,
+`pop/tt-rt-new.png`.
+
+## 70/30 verification
+
+- Board tokens (canvas/water/coast/park/grid) byte-identical — the paper
+  stays quiet by construction.
+- Network tokens all sat ≥ 0.73; band-area warm-gold share 74% ≈ the
+  direction's 70.
+- Vivid share (sat ≥ 0.45) rose 0.346 → 0.369 on juice-30000 (MM 0.585) —
+  the network now carries the saturation; the board still doesn't.
diff --git a/_bmad-output/design-analysis/pop/terminal_types-05000-thumb.png b/_bmad-output/design-analysis/pop/terminal_types-05000-thumb.png
new file mode 100644
index 0000000..8d545e2
Binary files /dev/null and b/_bmad-output/design-analysis/pop/terminal_types-05000-thumb.png differ
diff --git a/_bmad-output/design-analysis/pop/tt-rt-new.png b/_bmad-output/design-analysis/pop/tt-rt-new.png
new file mode 100644
index 0000000..2a373de
Binary files /dev/null and b/_bmad-output/design-analysis/pop/tt-rt-new.png differ
diff --git a/app/render/palette.odin b/app/render/palette.odin
index 0604615..c1cacf9 100644
--- a/app/render/palette.odin
+++ b/app/render/palette.odin
@@ -6,7 +6,16 @@ package render
 // token lifts #E8DDC2 → #EDE2C8 — the UE slice-1 warm-paper step (the
 // slice-1 reference reads ~#F2EEE3/#F7F3EA; the lift is a partial, canon-
 // keeping step — the map-token contrast + the a11y separation both hold,
-// proven by palcheck).
+// proven by palcheck). v2-network-pop (2026-08-22, user ruling: "make the
+// network pop"): the LEFOU system-tone mute is REVERSED IN THE NETWORK LAYER
+// ONLY — pipes back to a vivid tier family (copper-orange / cyan / gold —
+// each tier a distinct saturated hue, pairwise hue-separated ≥ 15°), packets
+// stay at catalog maxima (the look-book shades; the catalog is untouched —
+// cat.hash is golden-poison), node accents up (router LED token). The CALM
+// BOARD tokens (canvas/water/coast/park/grid) are untouched — the Brush
+// 70/30 done right: quiet paper board (the 70), saturated network (the 30,
+// warm-gold dominant). a11y mode tables untouched (they override the signal
+// set under CVD; their separation contract is palcheck-pinned).
 
 import "core:encoding/json"
 import "core:strings"
@@ -187,18 +196,18 @@ palette_load :: proc(source: []byte = DEFAULT_PALETTE_JSON) -> Palette {
 	p.host_roof = jcol(obj, "host_roof", {38, 76, 142, 255})
 	p.router_body = jcol(obj, "router_body", {94, 110, 128, 255})
 	p.router_dark = jcol(obj, "router_dark", {62, 74, 92, 255})
-	p.router_led = jcol(obj, "router_led", {46, 139, 87, 255})
-	p.pipe_copper = jcol(obj, "pipe_copper", {150, 142, 132, 255})
-	p.pipe_steel = jcol(obj, "pipe_steel", {126, 134, 146, 255})
-	p.pipe_fiber = jcol(obj, "pipe_fiber", {88, 110, 142, 255})
+	p.router_led = jcol(obj, "router_led", {0, 205, 90, 255})
+	p.pipe_copper = jcol(obj, "pipe_copper", {240, 110, 0, 255})
+	p.pipe_steel = jcol(obj, "pipe_steel", {0, 150, 240, 255})
+	p.pipe_fiber = jcol(obj, "pipe_fiber", {255, 215, 0, 255})
 	p.pipe_unalloc = jcol(obj, "pipe_unalloc", {58, 74, 92, 255})
-	p.packet_dot = jcol(obj, "packet_dot", {64, 140, 220, 255})
-	p.packet_dark = jcol(obj, "packet_dark", {28, 70, 120, 255})
+	p.packet_dot = jcol(obj, "packet_dot", {0, 130, 255, 255})
+	p.packet_dark = jcol(obj, "packet_dark", {0, 60, 150, 255})
 	p.ghost_ok = jcol(obj, "ghost_ok", {120, 128, 140, 200})
 	p.ghost_bad = jcol(obj, "ghost_bad", {232, 69, 69, 200})
 	p.lane_express = jcol(obj, "lane_express", {224, 138, 46, 255})
-	p.lane_standard = jcol(obj, "lane_standard", {108, 122, 142, 255})
-	p.lane_best_effort = jcol(obj, "lane_best_effort", {88, 152, 108, 255})
+	p.lane_standard = jcol(obj, "lane_standard", {56, 130, 200, 255})
+	p.lane_best_effort = jcol(obj, "lane_best_effort", {48, 178, 96, 255})
 	p.sel_halo = jcol(obj, "sel_halo", {232, 181, 68, 90})
 	p.state_healthy = jcol(obj, "state_healthy", {55, 214, 122, 255})
 	p.state_congested = jcol(obj, "state_congested", {242, 181, 68, 255})
@@ -260,18 +269,18 @@ fallback_palette :: proc() -> Palette {
 	p.host_roof = {38, 76, 142, 255}
 	p.router_body = {94, 110, 128, 255}
 	p.router_dark = {62, 74, 92, 255}
-	p.router_led = {46, 139, 87, 255}
-	p.pipe_copper = {150, 142, 132, 255}
-	p.pipe_steel = {126, 134, 146, 255}
-	p.pipe_fiber = {88, 110, 142, 255}
+	p.router_led = {0, 205, 90, 255}
+	p.pipe_copper = {240, 110, 0, 255}
+	p.pipe_steel = {0, 150, 240, 255}
+	p.pipe_fiber = {255, 215, 0, 255}
 	p.pipe_unalloc = {58, 74, 92, 255}
-	p.packet_dot = {64, 140, 220, 255}
-	p.packet_dark = {28, 70, 120, 255}
+	p.packet_dot = {0, 130, 255, 255}
+	p.packet_dark = {0, 60, 150, 255}
 	p.ghost_ok = {120, 128, 140, 200}
 	p.ghost_bad = {232, 69, 69, 200}
 	p.lane_express = {224, 138, 46, 255}
-	p.lane_standard = {108, 122, 142, 255}
-	p.lane_best_effort = {88, 152, 108, 255}
+	p.lane_standard = {56, 130, 200, 255}
+	p.lane_best_effort = {48, 178, 96, 255}
 	p.sel_halo = {232, 181, 68, 90}
 	p.state_healthy = {55, 214, 122, 255}
 	p.state_congested = {242, 181, 68, 255}
diff --git a/app/render/palette_polish_test.odin b/app/render/palette_polish_test.odin
index 5dd54b5..551b4d3 100644
--- a/app/render/palette_polish_test.odin
+++ b/app/render/palette_polish_test.odin
@@ -40,9 +40,11 @@ casing_color_is_opaque_darker_and_deterministic :: proc(t: ^testing.T) {
 	// the exact shipped blends (the PR's pixel-verify anchor): the blend is
 	// band*0.78 + ink*0.22, u8-truncated — the juice-golden rim pixels land
 	// on these exact values (the PR diff scan measured them ±0).
-	expect_color(t, casing_color(&p, p.pipe_copper), {128, 125, 120, 255})
-	expect_color(t, casing_color(&p, p.pipe_steel), {109, 118, 131, 255})
-	expect_color(t, casing_color(&p, p.pipe_fiber), {79, 100, 128, 255})
+	// v2-network-pop (2026-08-22): re-pinned to the vivid tier family —
+	// copper-orange {240,110,0} / cyan {0,150,240} / gold {255,215,0}.
+	expect_color(t, casing_color(&p, p.pipe_copper), {198, 100, 17, 255})
+	expect_color(t, casing_color(&p, p.pipe_steel), {11, 131, 204, 255})
+	expect_color(t, casing_color(&p, p.pipe_fiber), {210, 182, 17, 255})
 }
 
 @(test)
diff --git a/data/palette.json b/data/palette.json
index ed4f6cf..e5cfdec 100644
--- a/data/palette.json
+++ b/data/palette.json
@@ -1,5 +1,5 @@
 {
-  "_comment": "Palette catalog (look-book v1, art-direction v1.2 — the light-canvas canon). ALL values cosmetic (RGBA quads 0-255); the core never reads this file. The render layer loads it so art tuning is data (ODN-5). 7.4/canon D9: water/coast/park are the procedural-map tokens (story 7.4 — the look-book §2 palette oracle; the palcheck gate scans the blessed juice golden for them). 7.3: 'modes' = the colorblind remap tables (deutan/protan/tritan — simulator-derived by tools/derive_a11y_palettes.py, Machado 2009 severity-1.0; palcheck re-verifies pairwise separation under simulation). Partial tables: absent tokens keep base values; 'packet_classes' remaps catalog class colors at DRAW time (the catalog itself is never edited — cat.hash is golden-poison).",
+  "_comment": "Palette catalog (look-book v1, art-direction v1.2 — the light-canvas canon). ALL values cosmetic (RGBA quads 0-255); the core never reads this file. The render layer loads it so art tuning is data (ODN-5). 7.4/canon D9: water/coast/park are the procedural-map tokens (story 7.4 — the look-book §2 palette oracle; the palcheck gate scans the blessed juice golden for them). 7.3: 'modes' = the colorblind remap tables (deutan/protan/tritan — simulator-derived by tools/derive_a11y_palettes.py, Machado 2009 severity-1.0; palcheck re-verifies pairwise separation under simulation). Partial tables: absent tokens keep base values; 'packet_classes' remaps catalog class colors at DRAW time (the catalog itself is never edited — cat.hash is golden-poison). v2-network-pop (2026-08-22, user ruling: networking must pop): the LEFOU system-tone mute is REVERSED IN THE NETWORK LAYER ONLY — pipe tiers back to a vivid family (narrow = saturated copper-orange #F06E00, standard = cyan #0096F0, wide/fiber = the direction's warm-gold #FFD700; pairwise hue separation >= 15 deg), packets stay at catalog maxima (the look-book shades, draw-time), node accents up (router LED token). The CALM BOARD tokens (canvas/water/coast/park/grid) are untouched — the Brush 70/30 done right: quiet paper board (the 70), saturated warm-gold-dominant network (the 30 by band area). a11y mode tables untouched (they override the signal set under CVD).",
   "canvas":        [237, 226, 200, 255],
   "grid":          [194, 182, 148, 255],
   "water":         [179, 205, 224, 255],
@@ -17,19 +17,19 @@
   "host_roof":     [38, 76, 142, 255],
   "router_body":   [94, 110, 128, 255],
   "router_dark":   [62, 74, 92, 255],
-  "router_led":    [46, 139, 87, 255],
-  "pipe_copper":   [150, 142, 132, 255],
-  "pipe_steel":    [126, 134, 146, 255],
-  "pipe_fiber":    [88, 110, 142, 255],
+  "router_led":    [0, 205, 90, 255],
+  "pipe_copper":   [240, 110, 0, 255],
+  "pipe_steel":    [0, 150, 240, 255],
+  "pipe_fiber":    [255, 215, 0, 255],
   "pipe_core":     [122, 168, 230, 255],
   "pipe_unalloc":  [58, 74, 92, 255],
-  "packet_dot":    [64, 140, 220, 255],
-  "packet_dark":   [28, 70, 120, 255],
+  "packet_dot":    [0, 130, 255, 255],
+  "packet_dark":   [0, 60, 150, 255],
   "ghost_ok":      [120, 128, 140, 200],
   "ghost_bad":     [232, 69, 69, 200],
   "lane_express":  [224, 138, 46, 255],
-  "lane_standard": [108, 122, 142, 255],
-  "lane_best_effort": [88, 152, 108, 255],
+  "lane_standard": [56, 130, 200, 255],
+  "lane_best_effort": [48, 178, 96, 255],
   "lane_speeds":   [1000, 850, 700],
   "sel_halo":      [232, 181, 68, 90],
   "route_glow":    [86, 180, 110, 110],
diff --git a/goldens/a11y_reduced/30000ms.png b/goldens/a11y_reduced/30000ms.png
index d8c1a6c..046fa11 100644
Binary files a/goldens/a11y_reduced/30000ms.png and b/goldens/a11y_reduced/30000ms.png differ
diff --git a/goldens/a11y_reduced/65000ms.png b/goldens/a11y_reduced/65000ms.png
index f85ab36..a878b0d 100644
Binary files a/goldens/a11y_reduced/65000ms.png and b/goldens/a11y_reduced/65000ms.png differ
diff --git a/goldens/a11y_scale/30000ms.png b/goldens/a11y_scale/30000ms.png
index bc3c51b..50de906 100644
Binary files a/goldens/a11y_scale/30000ms.png and b/goldens/a11y_scale/30000ms.png differ
diff --git a/goldens/a11y_scale/65000ms.png b/goldens/a11y_scale/65000ms.png
index fd92a42..f72fe90 100644
Binary files a/goldens/a11y_scale/65000ms.png and b/goldens/a11y_scale/65000ms.png differ
diff --git a/goldens/advance_block_legacy/15000ms.png b/goldens/advance_block_legacy/15000ms.png
index a762f9a..ec0099e 100644
Binary files a/goldens/advance_block_legacy/15000ms.png and b/goldens/advance_block_legacy/15000ms.png differ
diff --git a/goldens/advance_block_legacy/60000ms.png b/goldens/advance_block_legacy/60000ms.png
index 8124258..be3ae24 100644
Binary files a/goldens/advance_block_legacy/60000ms.png and b/goldens/advance_block_legacy/60000ms.png differ
diff --git a/goldens/advance_block_sla/15000ms.png b/goldens/advance_block_sla/15000ms.png
index 7218466..f603994 100644
Binary files a/goldens/advance_block_sla/15000ms.png and b/goldens/advance_block_sla/15000ms.png differ
diff --git a/goldens/advance_block_sla/60000ms.png b/goldens/advance_block_sla/60000ms.png
index ae109fd..d8a8d59 100644
Binary files a/goldens/advance_block_sla/60000ms.png and b/goldens/advance_block_sla/60000ms.png differ
diff --git a/goldens/advance_fire/15000ms.png b/goldens/advance_fire/15000ms.png
index b70b107..5c29459 100644
Binary files a/goldens/advance_fire/15000ms.png and b/goldens/advance_fire/15000ms.png differ
diff --git a/goldens/advance_fire/60000ms.png b/goldens/advance_fire/60000ms.png
index 060522e..ccf7dc3 100644
Binary files a/goldens/advance_fire/60000ms.png and b/goldens/advance_fire/60000ms.png differ
diff --git a/goldens/bundle/02550ms.png b/goldens/bundle/02550ms.png
index c7c1f3a..49ca469 100644
Binary files a/goldens/bundle/02550ms.png and b/goldens/bundle/02550ms.png differ
diff --git a/goldens/bundle/02850ms.png b/goldens/bundle/02850ms.png
index 0df0686..7add724 100644
Binary files a/goldens/bundle/02850ms.png and b/goldens/bundle/02850ms.png differ
diff --git a/goldens/demolish/01050ms.png b/goldens/demolish/01050ms.png
index f26089f..a70a42e 100644
Binary files a/goldens/demolish/01050ms.png and b/goldens/demolish/01050ms.png differ
diff --git a/goldens/demolish/01250ms.png b/goldens/demolish/01250ms.png
index 35480af..b91173a 100644
Binary files a/goldens/demolish/01250ms.png and b/goldens/demolish/01250ms.png differ
diff --git a/goldens/demolish/01300ms.png b/goldens/demolish/01300ms.png
index d977ade..5d90aa5 100644
Binary files a/goldens/demolish/01300ms.png and b/goldens/demolish/01300ms.png differ
diff --git a/goldens/demolish/03000ms.png b/goldens/demolish/03000ms.png
index 676b0ef..df041bf 100644
Binary files a/goldens/demolish/03000ms.png and b/goldens/demolish/03000ms.png differ
diff --git a/goldens/demolish_bundle/01100ms.png b/goldens/demolish_bundle/01100ms.png
index 8b6fedc..465f56e 100644
Binary files a/goldens/demolish_bundle/01100ms.png and b/goldens/demolish_bundle/01100ms.png differ
diff --git a/goldens/demolish_bundle/01500ms.png b/goldens/demolish_bundle/01500ms.png
index 4d13109..52e8986 100644
Binary files a/goldens/demolish_bundle/01500ms.png and b/goldens/demolish_bundle/01500ms.png differ
diff --git a/goldens/demolish_bundle/03000ms.png b/goldens/demolish_bundle/03000ms.png
index 676b0ef..df041bf 100644
Binary files a/goldens/demolish_bundle/03000ms.png and b/goldens/demolish_bundle/03000ms.png differ
diff --git a/goldens/demolish_node/01250ms.png b/goldens/demolish_node/01250ms.png
index a0d2889..c9d6f98 100644
Binary files a/goldens/demolish_node/01250ms.png and b/goldens/demolish_node/01250ms.png differ
diff --git a/goldens/demolish_node/01450ms.png b/goldens/demolish_node/01450ms.png
index 8ffcc43..07432a4 100644
Binary files a/goldens/demolish_node/01450ms.png and b/goldens/demolish_node/01450ms.png differ
diff --git a/goldens/demolish_node/02100ms.png b/goldens/demolish_node/02100ms.png
index ae474e6..d324e37 100644
Binary files a/goldens/demolish_node/02100ms.png and b/goldens/demolish_node/02100ms.png differ
diff --git a/goldens/demolish_node/04000ms.png b/goldens/demolish_node/04000ms.png
index ae474e6..d324e37 100644
Binary files a/goldens/demolish_node/04000ms.png and b/goldens/demolish_node/04000ms.png differ
diff --git a/goldens/draw/02500ms.png b/goldens/draw/02500ms.png
index 676b0ef..df041bf 100644
Binary files a/goldens/draw/02500ms.png and b/goldens/draw/02500ms.png differ
diff --git a/goldens/ecmp/01250ms.png b/goldens/ecmp/01250ms.png
index 9784652..2054d73 100644
Binary files a/goldens/ecmp/01250ms.png and b/goldens/ecmp/01250ms.png differ
diff --git a/goldens/ecmp/01350ms.png b/goldens/ecmp/01350ms.png
index 224287c..8352211 100644
Binary files a/goldens/ecmp/01350ms.png and b/goldens/ecmp/01350ms.png differ
diff --git a/goldens/ecmp/03000ms.png b/goldens/ecmp/03000ms.png
index f84e963..8bc01c1 100644
Binary files a/goldens/ecmp/03000ms.png and b/goldens/ecmp/03000ms.png differ
diff --git a/goldens/ecmp_cost/01150ms.png b/goldens/ecmp_cost/01150ms.png
index 2dead86..17777fd 100644
Binary files a/goldens/ecmp_cost/01150ms.png and b/goldens/ecmp_cost/01150ms.png differ
diff --git a/goldens/ecmp_cost/01450ms.png b/goldens/ecmp_cost/01450ms.png
index cbac427..f117965 100644
Binary files a/goldens/ecmp_cost/01450ms.png and b/goldens/ecmp_cost/01450ms.png differ
diff --git a/goldens/era_advance/10000ms.png b/goldens/era_advance/10000ms.png
index fab53ea..f196e9c 100644
Binary files a/goldens/era_advance/10000ms.png and b/goldens/era_advance/10000ms.png differ
diff --git a/goldens/era_advance/55000ms.png b/goldens/era_advance/55000ms.png
index d12c9fc..61e91f1 100644
Binary files a/goldens/era_advance/55000ms.png and b/goldens/era_advance/55000ms.png differ
diff --git a/goldens/estate_surge/25000ms.png b/goldens/estate_surge/25000ms.png
index bd64ab4..1b75a1a 100644
Binary files a/goldens/estate_surge/25000ms.png and b/goldens/estate_surge/25000ms.png differ
diff --git a/goldens/estate_surge/75000ms.png b/goldens/estate_surge/75000ms.png
index 7522ea2..0d6b10f 100644
Binary files a/goldens/estate_surge/75000ms.png and b/goldens/estate_surge/75000ms.png differ
diff --git a/goldens/flow/02100ms.png b/goldens/flow/02100ms.png
index 12f61d0..192997f 100644
Binary files a/goldens/flow/02100ms.png and b/goldens/flow/02100ms.png differ
diff --git a/goldens/flow/02150ms.png b/goldens/flow/02150ms.png
index 9cc760b..f4131e8 100644
Binary files a/goldens/flow/02150ms.png and b/goldens/flow/02150ms.png differ
diff --git a/goldens/flow/02250ms.png b/goldens/flow/02250ms.png
index 98ef5d2..a40ce79 100644
Binary files a/goldens/flow/02250ms.png and b/goldens/flow/02250ms.png differ
diff --git a/goldens/forecast_preview/30000ms.png b/goldens/forecast_preview/30000ms.png
index 557fcad..8d26b4b 100644
Binary files a/goldens/forecast_preview/30000ms.png and b/goldens/forecast_preview/30000ms.png differ
diff --git a/goldens/forecast_preview/31000ms.png b/goldens/forecast_preview/31000ms.png
index 3f5c294..294e5b9 100644
Binary files a/goldens/forecast_preview/31000ms.png and b/goldens/forecast_preview/31000ms.png differ
diff --git a/goldens/forecast_preview/32000ms.png b/goldens/forecast_preview/32000ms.png
index 67f5040..29ebd1d 100644
Binary files a/goldens/forecast_preview/32000ms.png and b/goldens/forecast_preview/32000ms.png differ
diff --git a/goldens/forecast_preview/33000ms.png b/goldens/forecast_preview/33000ms.png
index f231bbc..828f50e 100644
Binary files a/goldens/forecast_preview/33000ms.png and b/goldens/forecast_preview/33000ms.png differ
diff --git a/goldens/forecast_shift/01300ms.png b/goldens/forecast_shift/01300ms.png
index 7ee1fc8..c8bc4f3 100644
Binary files a/goldens/forecast_shift/01300ms.png and b/goldens/forecast_shift/01300ms.png differ
diff --git a/goldens/forecast_shift/02800ms.png b/goldens/forecast_shift/02800ms.png
index 325df83..3b59092 100644
Binary files a/goldens/forecast_shift/02800ms.png and b/goldens/forecast_shift/02800ms.png differ
diff --git a/goldens/growth/15000ms.png b/goldens/growth/15000ms.png
index f415bf7..41cdb9b 100644
Binary files a/goldens/growth/15000ms.png and b/goldens/growth/15000ms.png differ
diff --git a/goldens/growth/45000ms.png b/goldens/growth/45000ms.png
index f25dc8a..4d71ca8 100644
Binary files a/goldens/growth/45000ms.png and b/goldens/growth/45000ms.png differ
diff --git a/goldens/growth/88000ms.png b/goldens/growth/88000ms.png
index fbd387d..48e9326 100644
Binary files a/goldens/growth/88000ms.png and b/goldens/growth/88000ms.png differ
diff --git a/goldens/health_lose/05000ms.png b/goldens/health_lose/05000ms.png
index 603edfb..930347d 100644
Binary files a/goldens/health_lose/05000ms.png and b/goldens/health_lose/05000ms.png differ
diff --git a/goldens/health_lose/21000ms.png b/goldens/health_lose/21000ms.png
index b2fce52..d57510d 100644
Binary files a/goldens/health_lose/21000ms.png and b/goldens/health_lose/21000ms.png differ
diff --git a/goldens/health_lose/23000ms.png b/goldens/health_lose/23000ms.png
index bf62048..67f095c 100644
Binary files a/goldens/health_lose/23000ms.png and b/goldens/health_lose/23000ms.png differ
diff --git a/goldens/health_win/150500ms.png b/goldens/health_win/150500ms.png
index 64d8f0d..cf270e7 100644
Binary files a/goldens/health_win/150500ms.png and b/goldens/health_win/150500ms.png differ
diff --git a/goldens/health_win/30000ms.png b/goldens/health_win/30000ms.png
index edbfbf3..28fbc29 100644
Binary files a/goldens/health_win/30000ms.png and b/goldens/health_win/30000ms.png differ
diff --git a/goldens/health_win/75000ms.png b/goldens/health_win/75000ms.png
index c414f46..6cfc68a 100644
Binary files a/goldens/health_win/75000ms.png and b/goldens/health_win/75000ms.png differ
diff --git a/goldens/juice/30000ms.png b/goldens/juice/30000ms.png
index d8c1a6c..046fa11 100644
Binary files a/goldens/juice/30000ms.png and b/goldens/juice/30000ms.png differ
diff --git a/goldens/juice/65000ms.png b/goldens/juice/65000ms.png
index af330b1..953acb1 100644
Binary files a/goldens/juice/65000ms.png and b/goldens/juice/65000ms.png differ
diff --git a/goldens/legacy_decay/15000ms.png b/goldens/legacy_decay/15000ms.png
index b70b107..5c29459 100644
Binary files a/goldens/legacy_decay/15000ms.png and b/goldens/legacy_decay/15000ms.png differ
diff --git a/goldens/legacy_decay/60000ms.png b/goldens/legacy_decay/60000ms.png
index 060522e..ccf7dc3 100644
Binary files a/goldens/legacy_decay/60000ms.png and b/goldens/legacy_decay/60000ms.png differ
diff --git a/goldens/legacy_modernized/15000ms.png b/goldens/legacy_modernized/15000ms.png
index b70b107..5c29459 100644
Binary files a/goldens/legacy_modernized/15000ms.png and b/goldens/legacy_modernized/15000ms.png differ
diff --git a/goldens/legacy_modernized/60000ms.png b/goldens/legacy_modernized/60000ms.png
index 72b6e69..d1d81aa 100644
Binary files a/goldens/legacy_modernized/60000ms.png and b/goldens/legacy_modernized/60000ms.png differ
diff --git a/goldens/lose/03000ms.png b/goldens/lose/03000ms.png
index e455e9a..cda73af 100644
Binary files a/goldens/lose/03000ms.png and b/goldens/lose/03000ms.png differ
diff --git a/goldens/node_health/10000ms.png b/goldens/node_health/10000ms.png
index f66357d..22dedac 100644
Binary files a/goldens/node_health/10000ms.png and b/goldens/node_health/10000ms.png differ
diff --git a/goldens/node_health/20000ms.png b/goldens/node_health/20000ms.png
index 9f61ef3..e8bf0a7 100644
Binary files a/goldens/node_health/20000ms.png and b/goldens/node_health/20000ms.png differ
diff --git a/goldens/pause/65000ms.png b/goldens/pause/65000ms.png
index b54b838..547354e 100644
Binary files a/goldens/pause/65000ms.png and b/goldens/pause/65000ms.png differ
diff --git a/goldens/pause/80000ms.png b/goldens/pause/80000ms.png
index 77ab703..899e7d1 100644
Binary files a/goldens/pause/80000ms.png and b/goldens/pause/80000ms.png differ
diff --git a/goldens/place/02500ms.png b/goldens/place/02500ms.png
index fb6f58a..d2586a2 100644
Binary files a/goldens/place/02500ms.png and b/goldens/place/02500ms.png differ
diff --git a/goldens/place/03000ms.png b/goldens/place/03000ms.png
index fb6f58a..d2586a2 100644
Binary files a/goldens/place/03000ms.png and b/goldens/place/03000ms.png differ
diff --git a/goldens/qos/01000ms.png b/goldens/qos/01000ms.png
index 795e634..9087c3c 100644
Binary files a/goldens/qos/01000ms.png and b/goldens/qos/01000ms.png differ
diff --git a/goldens/qos/65000ms.png b/goldens/qos/65000ms.png
index e5b3448..1565747 100644
Binary files a/goldens/qos/65000ms.png and b/goldens/qos/65000ms.png differ
diff --git a/goldens/qos_auto/01000ms.png b/goldens/qos_auto/01000ms.png
index 795e634..9087c3c 100644
Binary files a/goldens/qos_auto/01000ms.png and b/goldens/qos_auto/01000ms.png differ
diff --git a/goldens/qos_auto/06000ms.png b/goldens/qos_auto/06000ms.png
index bc6f58d..bc2eb37 100644
Binary files a/goldens/qos_auto/06000ms.png and b/goldens/qos_auto/06000ms.png differ
diff --git a/goldens/qos_contention/01000ms.png b/goldens/qos_contention/01000ms.png
index 1ca0158..8673351 100644
Binary files a/goldens/qos_contention/01000ms.png and b/goldens/qos_contention/01000ms.png differ
diff --git a/goldens/qos_contention/03000ms.png b/goldens/qos_contention/03000ms.png
index bb5eaf6..7e57c7f 100644
Binary files a/goldens/qos_contention/03000ms.png and b/goldens/qos_contention/03000ms.png differ
diff --git a/goldens/qos_contention/10000ms.png b/goldens/qos_contention/10000ms.png
index d698a34..9656c44 100644
Binary files a/goldens/qos_contention/10000ms.png and b/goldens/qos_contention/10000ms.png differ
diff --git a/goldens/qos_emphasis/01000ms.png b/goldens/qos_emphasis/01000ms.png
index 795e634..9087c3c 100644
Binary files a/goldens/qos_emphasis/01000ms.png and b/goldens/qos_emphasis/01000ms.png differ
diff --git a/goldens/qos_emphasis/05000ms.png b/goldens/qos_emphasis/05000ms.png
index 5168e73..25e99b0 100644
Binary files a/goldens/qos_emphasis/05000ms.png and b/goldens/qos_emphasis/05000ms.png differ
diff --git a/goldens/qos_emphasis/12000ms.png b/goldens/qos_emphasis/12000ms.png
index db8296b..8774667 100644
Binary files a/goldens/qos_emphasis/12000ms.png and b/goldens/qos_emphasis/12000ms.png differ
diff --git a/goldens/qos_manual/01000ms.png b/goldens/qos_manual/01000ms.png
index 795e634..9087c3c 100644
Binary files a/goldens/qos_manual/01000ms.png and b/goldens/qos_manual/01000ms.png differ
diff --git a/goldens/qos_manual/06000ms.png b/goldens/qos_manual/06000ms.png
index a8deb1d..7d44eee 100644
Binary files a/goldens/qos_manual/06000ms.png and b/goldens/qos_manual/06000ms.png differ
diff --git a/goldens/router_ceiling/02500ms.png b/goldens/router_ceiling/02500ms.png
index 23e783f..e8a4b2a 100644
Binary files a/goldens/router_ceiling/02500ms.png and b/goldens/router_ceiling/02500ms.png differ
diff --git a/goldens/router_ceiling/03500ms.png b/goldens/router_ceiling/03500ms.png
index 23e783f..e8a4b2a 100644
Binary files a/goldens/router_ceiling/03500ms.png and b/goldens/router_ceiling/03500ms.png differ
diff --git a/goldens/router_tiers/02500ms.png b/goldens/router_tiers/02500ms.png
index fcfd832..6d387c9 100644
Binary files a/goldens/router_tiers/02500ms.png and b/goldens/router_tiers/02500ms.png differ
diff --git a/goldens/router_tiers/03500ms.png b/goldens/router_tiers/03500ms.png
index fcfd832..6d387c9 100644
Binary files a/goldens/router_tiers/03500ms.png and b/goldens/router_tiers/03500ms.png differ
diff --git a/goldens/sla/01000ms.png b/goldens/sla/01000ms.png
index ee26eca..825559d 100644
Binary files a/goldens/sla/01000ms.png and b/goldens/sla/01000ms.png differ
diff --git a/goldens/sla/04000ms.png b/goldens/sla/04000ms.png
index 5d6dc81..34745ad 100644
Binary files a/goldens/sla/04000ms.png and b/goldens/sla/04000ms.png differ
diff --git a/goldens/sla/10000ms.png b/goldens/sla/10000ms.png
index 9314e53..7adf12d 100644
Binary files a/goldens/sla/10000ms.png and b/goldens/sla/10000ms.png differ
diff --git a/goldens/surge/149000ms.png b/goldens/surge/149000ms.png
index 79ffa61..010faa1 100644
Binary files a/goldens/surge/149000ms.png and b/goldens/surge/149000ms.png differ
diff --git a/goldens/surge/170000ms.png b/goldens/surge/170000ms.png
index 460a2c2..ddd2d46 100644
Binary files a/goldens/surge/170000ms.png and b/goldens/surge/170000ms.png differ
diff --git a/goldens/surge/30000ms.png b/goldens/surge/30000ms.png
index 069be33..33b7d6e 100644
Binary files a/goldens/surge/30000ms.png and b/goldens/surge/30000ms.png differ
diff --git a/goldens/surge/65000ms.png b/goldens/surge/65000ms.png
index 07b6c12..3363453 100644
Binary files a/goldens/surge/65000ms.png and b/goldens/surge/65000ms.png differ
diff --git a/goldens/terminal_types/05000ms.png b/goldens/terminal_types/05000ms.png
index a1c6b69..0408770 100644
Binary files a/goldens/terminal_types/05000ms.png and b/goldens/terminal_types/05000ms.png differ
diff --git a/goldens/terminal_types/30000ms.png b/goldens/terminal_types/30000ms.png
index 0176da8..7435c99 100644
Binary files a/goldens/terminal_types/30000ms.png and b/goldens/terminal_types/30000ms.png differ
diff --git a/goldens/warn/01500ms.png b/goldens/warn/01500ms.png
index 7f8d0bf..6421613 100644
Binary files a/goldens/warn/01500ms.png and b/goldens/warn/01500ms.png differ
diff --git a/goldens/warn/45000ms.png b/goldens/warn/45000ms.png
index f2cffdd..d0834d4 100644
Binary files a/goldens/warn/45000ms.png and b/goldens/warn/45000ms.png differ
diff --git a/goldens/warn/65000ms.png b/goldens/warn/65000ms.png
index 30a39f3..2ea09de 100644
Binary files a/goldens/warn/65000ms.png and b/goldens/warn/65000ms.png differ
diff --git a/goldens/win/02300ms.png b/goldens/win/02300ms.png
index 35480af..b91173a 100644
Binary files a/goldens/win/02300ms.png and b/goldens/win/02300ms.png differ


--- SPEC / CONTEXT ---
# packet-plumber-v2-network-pop

## Task

Make the network POP — the user's mid-review correction (2026-08-22):
"networking is boring so we need to make it pop… has to make good
attention-grabbing thumbnails." Measured root cause: the v2-look-polish
LEFOU system-tone pass muted the pipe tiers (the network) to gray-blue,
killing the saturation ceiling — our top-2% saturation = 0.51–0.57
(calm frames) vs Mini Motorways 0.91–1.00 (image_01/05).

Reverse the mute **in palette tokens only** — no geometry, no sim change:

1. Pipes back to a vivid tier family (each tier a distinct saturated
   hue; MM's bright ribbons + saturated cores are the model).
2. Packets to catalog maxima (saturated cores, not muted).
3. Node accents up (router LEDs, tier rings).
4. **Calm board stays calm** — the Brush 70/30 done right: board 70%
   cool-cyan (#87CEEB), 30% warm-gold (#FFD700); network layer inverted
   70/30 (warm-gold dominant). MM = white roads + saturated nodes on a
   quiet paper board; our board keeps the paper quiet, the NETWORK pops.

## Rules (hard)

1. Palette-token changes only (data/palette.json + the tier colors the
   renderer reads in app/render/view.odin). No geometry, no sim, no
   LOG_VERSION.
2. **Thumbnail gate**: re-capture the same demos at the pinned sha,
   re-measure top-2% saturation ceiling — target ≥ 0.85 (from 0.51).
   Also render the streamer-card scale test (427×240) and check the
   network reads as the "hero" element.
3. Keep the 70/30 calm/pop split — a fully-saturated board fails the
   direction's own standard (DIRECTION.md §1).
4. Run palcheck (in-repo palette checker) if the repo has one; keep
   canon-adjacent tokens intact.

## Acceptance

- Saturation ceiling ≥ 0.85 on re-measure; network reads as the hero at
  427×240 thumbnail scale.
- 70/30 split verified: board stays calm, network pops.
- Local test suite + goldens green (golden re-bless documented if the
  look shifts — cause-documented).
- pr_review: 1 (Perkins before merge).

## Skills policy

bmad-quick-dev.

## Model policy

deepseek-v4-flash, --thinking max.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-network-pop
- base: v2
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- parallel-safe with the whole v2 visual wave (sibling worktrees; merge
  order = the wave's final re-bless, coordinated by Gru)
- source of truth: kyle-design-directions.md §2 + design-audit.html POP
  section (artifact dir of packet-plumber-v2-design-audit)


--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in location.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in location.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "codebase",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Your ONLY deliverable is the JSON file named below. No prose replies needed beyond a one-line confirmation.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

--- FILE OUTPUT (headless contract) ---
Write ONLY your JSON array to this exact absolute path: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-network-pop/r1/codebase.json
The directory already exists. The file must contain exactly the JSON array — no prose, no markdown fencing, no preamble. Write the file with a tool (your file-write capability or a shell heredoc), then STOP. Do not write to any other location. Do not derive or alter the path. Work autonomously — do not ask questions.