You are reviewing a code diff. You have read-only access to the repository (the checkout at /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-motion-readability-r3 is exactly the reviewed state) and may verify the diff's claims against the actual codebase using your available tools. You are a review lens: report findings only — never edit, fix, or write any repository file (the ONLY file you may write is your output JSON file named below).

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
diff --git a/_bmad-output/field-notes/packet-plumber-v2-motion-readability.md b/_bmad-output/field-notes/packet-plumber-v2-motion-readability.md
new file mode 100644
index 0000000..434e3c7
--- /dev/null
+++ b/_bmad-output/field-notes/packet-plumber-v2-motion-readability.md
@@ -0,0 +1,27 @@
+# Field notes — packet-plumber-v2-motion-readability (2026-08-22)
+
+- **The view-layer interp cache must be keyed by packet id and lazily made**
+  (`if v.pkt_interp == nil { make(...) }` INSIDE the alpha<1 path): the
+  harness renders snapshot-exact (alpha=1.0 default param) and must never
+  allocate/touch it — that's what keeps 45 T2 goldens byte-identical with
+  zero re-bless. Any future view-layer effect that is app-only should gate
+  itself the same way (a default param = golden-stable by construction).
+- **rlsw DOES alpha-blend filled circles/triangles** (probe: red circle
+  a=100 over white → blended 255,154,154) — only LINE primitives render
+  alpha as opaque (the 7.1 trap). So low-alpha packet trails render
+  truthfully in rlsw motion-strip evidence captures; trails can ship
+  app-gated without a golden divergence.
+- **Pixel-measuring interpolated motion needs an EXACT-color gate (tol=0)**:
+  trail echoes blend toward the canvas and land within tol=18 of the body
+  color, and a static exact-color building cluster (640,358) polluted the
+  centroid — the first "after" readings looked erratic (backward jumps)
+  until the exact-color-only gate isolated the live packet. Also: motion
+  strips must render mid-tick (25ms/16.7ms cadence), not tick-aligned
+  (100ms) — a 100ms strip samples only tick boundaries and shows the same
+  stepping in both modes; the 60Hz displacement table is the decisive
+  before/after proof.
+
+r1 addendum (2026-08-22, Perkins round 2):
+- **In a `git rebase`, `--theirs` = the REPLAYED commit (yours), `--ours` = upstream** — the OPPOSITE of merge. Resolving PNG conflicts with `checkout --theirs` silently kept my old-palette goldens; caught it because the diff bundle showed OLD pipe colors (the packet-only signature was gone). Re-resolved with `git checkout origin/v2 -- <files>`. When a palette wave merges underneath a re-blessed-golden PR: resolve conflicts to the NEW base, then `harness save` the affected demos to re-render under the COMBINED code, and re-verify T1/log.bin byte-identity (70/70 stayed identical across the rebase).
+- **Perkins requires unit pins for view-layer code the golden gates never execute** (the interp path runs only at alpha<1; T1/T2/replay all render snapshot-exact). The render package's `@(test)` convention (hud_test/wire_path_test) is the right home: `motion_test.odin` pins interp_continuous's 4 continuous kinds + every teleport snap + the row-roll alpha endpoints + prune/reset + the reduced-motion echo predicate. Extract any gate the goldens can't reach into a pure predicate (`trails_active`) so it IS testable.
+- The measure tool + motion-strip verb get review-hardened: ExportImage bool checked + frame counted only on success, prime renders UnloadImage'd, exact-`snapshot` arg validation, frame-name-mismatch exit 2, lost-track ≠ hold, both mean-jump lists guarded.
diff --git a/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/README.md b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/README.md
new file mode 100644
index 0000000..2a4d806
--- /dev/null
+++ b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/README.md
@@ -0,0 +1,93 @@
+# packet-plumber-v2-motion-readability — evidence
+
+Sub-tick packet interpolation + fading trails + +15% packet size (the §4
+motion canon — "interpolate position between sim snapshots for 60 fps
+smoothness"; MM image_01/03/05/07 "consistent speed" read).
+
+## The fix (view-layer only, ODN-1)
+
+`app/render/view.odin` — `draw_packets` gained `tick` + `interp_alpha`
+(the render frame's fractional progress within the tick = the app's
+accum/tick_seconds). The packet's drawn position is lerped in WORLD space
+between the last two 20 Hz snapshot positions, cached per packet id
+(`View.pkt_interp`). Identity-guarded: the lerp runs only for continuous
+motion (same-edge travel, arrival, forward, waiting); sim teleports
+(spawn, sever, reroute) snap. 3-echo fading trails (`TRAIL_FADES`) draw
+under the live packet; reduced-motion pins them off. `PACKET_R_FACTOR`
+= ×1.15 packet radius.
+
+**T2-safe by construction**: the harness renders snapshot-exact
+(`interp_alpha` defaults to 1.0 — the exact pre-2.1 draw path), so the
+interpolation + trails never touch goldens. The ONLY golden shift is the
+deliberate +15% packet-size re-bless (rule 2: "a capture tick legitimately
+moves"; cause documented below).
+
+## Rule-4 measurement: frame-to-frame displacement at 60 Hz
+
+`harness motion-strip motion 2200 2600 17 <dir> [snapshot]` renders the
+single-packet motion.dem at 60 Hz; `tools/measure_packet_motion.py` tracks
+the exact-color live packet (trail echoes are canvas-blended, never exact):
+
+| metric | BEFORE (snapshot) | AFTER (interp) |
+|---|---|---|
+| holds (<0.5px/frame) | 21 of 24 | 10 of 24 (post-arrival) |
+| mean jump when moving | 30.6 px | 11.2 px |
+
+BEFORE: the packet holds ~3 frames (50 ms) then jumps ~30 px (the 20 Hz
+step). AFTER: it moves ~10 px every 16.7 ms frame — a continuous glide.
+(Full table: `tools/measure_packet_motion.py bin/motion-evidence/m60-before
+bin/motion-evidence/m60-after`.)
+
+## Visual evidence (Kyle, glm-4.6v)
+
+- `strip-contact-60hz.png` — 8-frame 60 Hz contact sheet, BEFORE vs AFTER:
+  Kyle: top row "stops-and-jumps... holding still for ~3 frames"; bottom
+  row "continuous motion with visible trails... smooth motion blur".
+- `glide-compare-2251.png` + `trail-closeup-2234.png` — single-frame
+  before/after + trail echo close-up.
+- `size-compare-core.png` + `size-compare-corridor.png` — r≈8px vs r≈9.2px
+  (+15%) on the dense core @30000ms and the corridor @30600ms: Kyle verdict
+  on BOTH crops: "HELP ... more readable and trackable ... no significant
+  overlap or clutter issues."
+
+## The documented re-bless
+
+38 demos' T2 PNGs re-blessed (`harness save`) — the +15% packet radius
+legitimately moves packet pixels in every packet-bearing capture (rule 2).
+Verified: ALL 76 T1 manifests + `.log.bin` files are byte-identical
+(`cmp` against the pre-bless copies) — the sim is untouched. The diff
+bundles show only packet colors (outline 49,53,61 / body 90,98,112 /
+glint 250,246,238) within packet-sized bboxes. `motion.dem` is a NEW
+T1-only golden (no captures — the motion read is pinned by the strip verb,
+never a golden).
+
+## Automated coverage (Perkins r1 B1/B2)
+
+`app/render/motion_test.odin` (13 new `@(test)`s, in the gate-2 render test
+run) pins the interp core that the golden gates never execute (T1/T2/replay
+all render alpha=1.0 snapshot-exact):
+
+- `interp_continuous` — the four continuous kinds (same-edge, arrival,
+  forward, waiting) TRUE; every teleport (sever drop-back, ECMP reroute,
+  spawn, delivery) FALSE (the snap).
+- row-roll alpha endpoints — alpha=0 draws the T-1 position (glide base),
+  alpha=1 draws the T position (glide target), alpha=0.5 the midpoint; the
+  row rolls tick-1 → tick.
+- snap paths — missing row (spawn), tick gap (catch-up/pause), anchor
+  mismatch (sever): drawn at the snapshot position, no ghost.
+- cache lifecycle — reset empties, prune drops delivered ids and keeps live
+  ones (seeded past the max(128, live*2+64) bound).
+- `trails_active` (W6) — the reduced-motion echo gate as a pure predicate:
+  echoes off under reduced_motion regardless of the ring; the live packet +
+  glide are never gated.
+
+## Reproduce
+
+```bash
+tools/harness.sh run                       # 46 demos green (T1+T2+replay)
+./bin/harness motion-strip motion 2200 2600 17 bin/m60-before snapshot
+./bin/harness motion-strip motion 2200 2600 17 bin/m60-after
+python3 tools/measure_packet_motion.py bin/m60-before bin/m60-after
+./bin/harness motion-strip juice 29800 30800 100 bin/ms-before snapshot
+./bin/harness motion-strip juice 29800 30800 100 bin/ms-after
+```
diff --git a/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/glide-compare-2251.png b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/glide-compare-2251.png
new file mode 100644
index 0000000..a4e49b2
Binary files /dev/null and b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/glide-compare-2251.png differ
diff --git a/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/size-compare-core.png b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/size-compare-core.png
new file mode 100644
index 0000000..786e92a
Binary files /dev/null and b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/size-compare-core.png differ
diff --git a/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/size-compare-corridor.png b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/size-compare-corridor.png
new file mode 100644
index 0000000..c65bcbc
Binary files /dev/null and b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/size-compare-corridor.png differ
diff --git a/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/strip-contact-60hz.png b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/strip-contact-60hz.png
new file mode 100644
index 0000000..2f9d6c8
Binary files /dev/null and b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/strip-contact-60hz.png differ
diff --git a/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/trail-closeup-2234.png b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/trail-closeup-2234.png
new file mode 100644
index 0000000..70fa6ed
Binary files /dev/null and b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/trail-closeup-2234.png differ
diff --git a/_bmad-output/pr-bodies/v2-motion-readability.md b/_bmad-output/pr-bodies/v2-motion-readability.md
new file mode 100644
index 0000000..e9b25dc
--- /dev/null
+++ b/_bmad-output/pr-bodies/v2-motion-readability.md
@@ -0,0 +1,115 @@
+# 2.1 Motion readability — sub-tick interpolation + fading trails + +15% packet size
+
+The user's complaint ("packets move too fast to follow") had a view-layer root cause: packets
+rendered at **20 Hz quantized positions** — the draw read `packet_progress_frac` (a sim-state
+value that only changes per tick), so on a 60 Hz display a packet held still for 2–3 frames then
+jumped ~⅓ of an edge. The pace-tuning job owns speed; this job makes the motion READ smooth.
+
+## What ships (all view-layer, ODN-1 — the sim's 20 Hz truth is untouched)
+
+1. **Sub-tick interpolation (the core fix)** — `draw_packets` now lerps each packet between the
+   last two snapshot positions using the render frame's fractional progress (the app's
+   `accum/tick_seconds`). The lerp is WORLD-space (camera-independent: the focus-zoom ease moves
+   the camera between ticks, so a screen-space lerp would smear). A per-packet cache on the View
+   holds the previous tick's drawn position; the identity guard snaps on sim teleports (spawn,
+   sever drop-back, reroute) so the sim's truth never smears across the map.
+2. **Fading trails (the MM "consistent speed" read)** — a 3-echo ring drawn under the live packet
+   in its own body color at low alpha (`TRAIL_FADES` 0.30/0.20/0.12), only while the packet is
+   moving. Reduced-motion pins the echoes off (E9.2 decoration gate); the live packet + the glide
+   stay — packet motion is a gameplay readout, never disabled (7.3 canon).
+3. **Packet size +15%** (`PACKET_R_FACTOR` 1.15 — r≈8px → ~9.2px at fit, the §4 direction) —
+   verified against the dense-core + corridor crops: **HELP on both** (Kyle), no overlap
+   regression. This legitimately moves packet pixels in every packet-bearing T2 golden → a
+   documented re-bless (see below).
+
+## The motion-strip evidence (rule 4: frame-to-frame displacement at 60 Hz)
+
+**Acceptance wording (Perkins r1 N13):** the AC's literal "100 ms" strip is
+tick-aligned (100 ms = 2 ticks), so a 100 ms cadence samples only tick
+boundaries and steps identically before/after — it cannot show the glide.
+The decisive evidence is the **60 Hz (17 ms) cadence** substitution below
+(3 sub-tick samples per tick): before holds ~3 frames then jumps, after
+moves every frame. The 100 ms strips are still produced for the visual
+(see the evidence pack), but the displacement table is the measurement.
+
+New harness verb `motion-strip <demo> <start_ms> <end_ms> <step_ms> <outdir> [snapshot]` renders
+a demo at arbitrary wall-clock cadence with the live interpolation alpha (deterministic: alpha is
+a pure function of the wall ms). `snapshot` reproduces the pre-2.1 render byte-identically — the
+same verb makes both the before and after strips. New T1-only golden `motion.dem` (one packet on a
+long straight pipe) + `tools/measure_packet_motion.py` (exact-color tracking — trail echoes blend
+toward the canvas and never match).
+
+```
+frame | BEFORE (px) | AFTER (px)
+2200  |     0.0     |     0.0
+2217  |     0.0     |    10.2
+2234  |     0.0     |    10.7
+2251  |    30.7     |    10.3
+2268  |     0.0     |    10.1
+2285  |     0.0     |    10.7
+2302  |    30.8     |    10.2
+...
+holds (<0.5px): BEFORE=21/24  AFTER=10/24 (post-arrival)
+mean jump when moving: BEFORE=30.6px  AFTER=11.2px
+```
+
+**Before**: holds ~3 frames (50 ms) then jumps ~30 px. **After**: ~10 px every 16.7 ms frame —
+a continuous glide. Kyle's read of the 60 Hz contact sheet (`strip-contact-60hz.png`): top row
+"stops-and-jumps... holding still for ~3 frames"; bottom row "continuous motion with visible
+trails". Evidence pack: `_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/`.
+
+## T2 safety — goldens
+
+- **Interpolation + trails: ZERO golden impact by construction.** The harness renders
+  snapshot-exact (`interp_alpha` defaults to 1.0 — the exact pre-2.1 draw path; the cache is
+  never allocated/touched on that path). `harness run` was green against the blessed goldens
+  before the size change.
+- **The documented re-bless**: the +15% packet radius legitimately moves packet pixels in every
+  packet-bearing capture (rule 2: "goldens re-bless only if a capture tick legitimately moves;
+  document cause"). 38 demos re-blessed via `harness save`. Verified: **all 76 T1 manifests +
+  `.log.bin` files are byte-identical** (cmp against pre-bless copies — the sim is untouched);
+  the diff bundles show only packet colors (outline 49,53,61 / body 90,98,112 / glint
+  250,246,238) inside packet-sized bboxes.
+
+## Files changed
+
+| File | Change |
+|---|---|
+| `app/render/view.odin` | interp cache + `packet_interp_pos` (world-space lerp, identity guard) + trail echoes + `PACKET_R_FACTOR`; `draw_world`/`draw_packets` gain `interp_alpha: f32 = 1.0` |
+| `app/main.odin` | passes `accum/tick_seconds` (snapshot-exact when paused/game-over); resets the interp cache on run start |
+| `harness/motion_strip.odin` | NEW — the motion-strip evidence verb |
+| `harness/main.odin`, `harness/goldens.odin` | verb wiring; `capture_frame` gains the alpha passthrough |
+| `demos/motion.dem` + `goldens/motion.{t1,log.bin}` | NEW T1-only golden (the measurement scene) |
+| `tools/measure_packet_motion.py` | NEW — the 60 Hz displacement measurement |
+| `goldens/*/*.png` | 38 demos re-blessed (documented cause above) |
+
+## Decisions & rationale
+
+- **N15 (deferred, by design): `run_motion_strip` re-uses the demo
+  setup/driver orchestration instead of extracting shared helpers from
+  `run_demo`.** The strip verb is evidence tooling, not a golden path: it
+  renders the SAME sim timeline the blessed demos pin (the T1 manifest +
+  replay gate), and the measurement scene (`motion.dem`) is itself a
+  T1-pinned golden — so a drift in the strip driver would fail `harness
+  run` (the blessed manifest) before it could mislead a measurement.
+  Extracting the run_demo driver into shared helpers is a harness-wide
+  refactor with golden risk (run_demo is the golden path itself); the
+  briefing scoped this job to the view layer + evidence. Flagged for a
+  future harness-cleanup story.
+
+- **World-space lerp over screen-space**: the camera eases between ticks (focus-zoom), so a
+  screen-space prev/cur pair would be in different camera frames → smear. World-space is
+  camera-independent; the harness path (alpha=1.0) never round-trips.
+- **Identity guard (snap on teleport)**: sever drop-back, ECMP reroute, and spawn are sim
+  discontinuities; lerping them would draw fast smears across the map. The guard keeps the glide
+  for the four continuous kinds (same-edge, arrival, forward, waiting) and snaps everything else.
+- **Render-behind, one-tick lag**: the display glides from the T-1 position to the T position
+  across the tick (alpha 0→1), so it lags the sim by ≤1 tick — the standard fixed-timestep
+  convention; imperceptible and perfectly smooth (the strips prove it).
+- **Trails only while moving** (0.5 px gate): a queued dot would stack echoes at one spot and
+  read as a smudge.
+- **`motion.dem` is T1-only** (no captures): the motion read is pinned by the strip verb's
+  measurement, never a golden — the interpolation is inherently a sub-tick, between-golden
+  phenomenon.
+- **Reduced-motion**: echoes off (decoration); interpolation + live packet stay (gameplay
+  readout, 7.3 canon).
diff --git a/app/main.odin b/app/main.odin
index 42d8674..48748d1 100644
--- a/app/main.odin
+++ b/app/main.odin
@@ -455,7 +455,16 @@ main :: proc() {
 		rl.BeginDrawing()
 		defer rl.EndDrawing()
 		rl.ClearBackground(app.palette.canvas)
-		rnd.draw_world(&app.view, &app.state.topology, &app.state.bundles, &app.state.flow, &app.state.crisis, app.tick, app.input.drag, app.input.sel_pipe, app.focus_class, app.state.seed)
+		// 2.1 motion-readability: the sub-tick packet glide — the render
+		// frame's fractional progress within the current tick (the accumulator
+		// leftover after the step loop, 0..1). Paused/Game_Over render
+		// snapshot-exact (alpha=1) — a frozen sim shows the sim's own
+		// positions, deterministic.
+		interp_alpha: f32 = 1.0
+		if app.mode == .Run {
+			interp_alpha = f32(min(app.accum / tick_seconds, 1.0))
+		}
+		rnd.draw_world(&app.view, &app.state.topology, &app.state.bundles, &app.state.flow, &app.state.crisis, app.tick, app.input.drag, app.input.sel_pipe, app.focus_class, app.state.seed, interp_alpha)
 		// v2-visibility (gap 2): the drop-site markers — drawn with the world
 		// (world-anchored at the shed bundle's midpoint) but APP-LAYER ONLY:
 		// the harness T2 capture path never calls this line (capture_frame
@@ -612,6 +621,11 @@ start_run :: proc(app: ^App, seed: u64) {
 	// events watermark resets with the fresh buffer (run_init re-makes it).
 	app.audio_mark = 0
 	au.audio_reset_run(&app.audio)
+	// 2.1 motion-readability: a fresh run drops the sub-tick packet cache —
+	// packet ids recycle across runs, so a stale row would anchor a fresh
+	// run's glide on a previous run's position (the continuity guard snaps
+	// anyway, but the honest reset is a clean table).
+	rnd.packet_interp_reset(&app.view)
 	// 7.1: a fresh run starts at the bird's-eye fit (the camera snaps, not
 	// eases, across a run boundary) + no class focus + no stale selection diff.
 	camera_set_fit(app)
diff --git a/app/render/motion_test.odin b/app/render/motion_test.odin
new file mode 100644
index 0000000..b29ca1a
--- /dev/null
+++ b/app/render/motion_test.odin
@@ -0,0 +1,404 @@
+package render
+
+// motion_test.odin — the 2.1 sub-tick interpolation core's durable pins
+// (Perkins r1 B1/B2: the interp path never executes under the golden gates —
+// T1/T2/replay all render alpha=1.0 snapshot-exact, and motion-strip is an
+// on-demand evidence verb, not a CI gate — so the identity-guarded-snap /
+// no-ghost invariant MUST be pinned here, at the lowest testable layer).
+//
+// Covers:
+//   (a) interp_continuous — the FOUR continuous kinds (same-edge travel,
+//       arrival, forward, waiting) are TRUE; every teleport (spawn, sever
+//       drop-back, ECMP reroute, delivery) is FALSE (the snap).
+//   (b) row-roll alpha endpoints — packet_interp_pos at alpha=0 returns the
+//       PREVIOUS tick's position (the glide base); at alpha=1 the CURRENT
+//       tick's position (the glide target); the row rolls tick-1 → tick and
+//       a mid-tick alpha lerps between the two snapshot positions.
+//   (c) the snap paths — a missing row (spawn), a tick gap (catch-up /
+//       pause-resume), and an anchor mismatch all draw the current snapshot
+//       position with NO ghost (the returned pos == the snapshot pos).
+//   (d) packet_interp_reset empties the cache; packet_interp_prune drops
+//       delivered (absent) ids and keeps live ones.
+//   (e) the reduced-motion echo gate (W6): trails_active() is FALSE under
+//       reduced_motion regardless of trail_n, TRUE otherwise.
+//
+// Run: odin test app/render   (the established render-test gate, gate 2).
+
+import "core:testing"
+import rl "vendor:raylib"
+import pp "../../core"
+
+// motion_test_catalog — a minimal catalog for the interp tests (mirrors the
+// wire_path_test catalog: 26px tiles, standard tier, packet_bandwidth 120).
+motion_test_catalog :: proc(cat: ^pp.Catalogs, allocator := context.allocator) {
+	cat^ = {}
+	cat.hash = 0x0BAD5EEDCAFE1234
+	cat.node_types = make([dynamic]pp.Node_Type, 0, 4, allocator)
+	append(&cat.node_types, pp.Node_Type{id = "residential", display = "Residential", kind = .Terminal, terminal_role = .Residential, throughput_units = 5, port_capacity = 0, demand_weight = 1, era_introduced = 1})
+	append(&cat.node_types, pp.Node_Type{id = "router_basic", display = "Basic Router", kind = .Junction, terminal_role = .None, throughput_units = 40, port_capacity = 4, era_introduced = 1})
+	cat.pipe_tiers = make([dynamic]pp.Pipe_Tier, 0, 4, allocator)
+	append(&cat.pipe_tiers, pp.Pipe_Tier{id = "standard", display = "Standard Line", capacity_units = 15, cost = 10, clean_span = 10, max_span = 14, cost_per_tile = 12, era_introduced = 1})
+	cat.balance = pp.Balance{logic_hz = 20, max_ticks = 100000, snap_radius = 36, map_w_tiles = 40, map_h_tiles = 30, tile_px = 26, packet_bandwidth = 120}
+	cat.balance.placement = pp.Placement_Balance{router_router_sep_tiles = 4, router_terminal_sep_tiles = 2}
+	cat.balance.lane_presets = make([dynamic]pp.Lane_Preset, 0, 2, allocator)
+	append(&cat.balance.lane_presets, pp.Lane_Preset{id = "balanced", display = "Balanced", weights = {1, 1, 1}})
+	cat.balance.default_preset_idx = 0
+}
+
+// motion_test_view — a minimal View for the interp math: identity camera
+// (scale 1, no offset) so world == screen and the lerp is trivially
+// checkable. Mirrors the wire_path_test view.
+motion_test_view :: proc(v: ^View, cat: ^pp.Catalogs) {
+	v^ = {}
+	v.catalogs = cat
+	v.tile_px = 26.0
+	v.world_w = 40 * 26.0
+	v.world_h = 30 * 26.0
+	v.scale = 1.0
+	v.off_x = 0
+	v.off_y = 0
+	v.sprites.ok = false
+}
+
+// motion_test_network — a tiny drawn network: residential A @{10,10} —
+// router B @{20,10} — residential C @{30,10} (two pipes, one hop each).
+// Returns the pipe id of A→B.
+motion_test_network :: proc(topo: ^pp.Topology, cat: ^pp.Catalogs, allocator := context.allocator) -> u32 {
+	pp.topology_make(topo, allocator)
+	res_idx, _ := pp.node_type_index(cat, "residential")
+	rt_idx, _ := pp.node_type_index(cat, "router_basic")
+	a := pp.topology_spawn_node(topo, res_idx, {10, 10}, cat)
+	b := pp.topology_spawn_node(topo, rt_idx, {20, 10}, cat)
+	c := pp.topology_spawn_node(topo, res_idx, {30, 10}, cat)
+	pp.topology_apply_edit(topo, pp.Command{kind = pp.Cmd_Draw_Pipe{a = a, b = b, tier = 0}}, cat)
+	pp.topology_apply_edit(topo, pp.Command{kind = pp.Cmd_Draw_Pipe{a = b, b = c, tier = 0}}, cat)
+	return 0 // pipe id 0 = A→B
+}
+
+// motion_test_packet — a packet on pipe 0 heading B (the A→B traversal).
+motion_test_packet :: proc(p: ^pp.Packet, id: u64 = 7) {
+	p^ = {}
+	p.id = id
+	p.class = 0 // email
+	p.src = 0
+	p.dst = 2
+	p.on_edge = true
+	p.edge = 0
+	p.heading = 1
+	p.progress_units = 60 // half of packet_bandwidth 120 → frac 0.5
+}
+
+// ---------------------------------------------------------------- (a) the
+// continuity guard: four continuous kinds TRUE, every teleport FALSE.
+
+@(test)
+interp_continuous_same_edge :: proc(t: ^testing.T) {
+	cat: pp.Catalogs
+	motion_test_catalog(&cat, context.temp_allocator)
+	topo: pp.Topology
+	motion_test_network(&topo, &cat, context.temp_allocator)
+
+	p: pp.Packet
+	motion_test_packet(&p) // on edge 0, heading 1
+
+	// same edge + same heading → mid-edge travel is continuous
+	testing.expect(t, interp_continuous(&topo, 0, 1, 0, true, &p), "same-edge travel must be continuous")
+}
+
+@(test)
+interp_continuous_arrival :: proc(t: ^testing.T) {
+	cat: pp.Catalogs
+	motion_test_catalog(&cat, context.temp_allocator)
+	topo: pp.Topology
+	motion_test_network(&topo, &cat, context.temp_allocator)
+
+	p: pp.Packet
+	motion_test_packet(&p)
+	// arrival: was heading toward node 1, now sits at node 1
+	p.on_edge = false
+	p.at_node = 1
+	testing.expect(t, interp_continuous(&topo, 0, 1, 0, true, &p), "arrival (heading == at_node) must be continuous")
+}
+
+@(test)
+interp_continuous_forward :: proc(t: ^testing.T) {
+	cat: pp.Catalogs
+	motion_test_catalog(&cat, context.temp_allocator)
+	topo: pp.Topology
+	motion_test_network(&topo, &cat, context.temp_allocator)
+
+	p: pp.Packet
+	motion_test_packet(&p)
+	// forward: was at node 0 (the departure of edge 0), now on edge 0
+	p.on_edge = true
+	p.edge = 0
+	p.heading = 1
+	testing.expect(t, interp_continuous(&topo, 0, 0, 0, false, &p), "forward (at_node == edge departure) must be continuous")
+}
+
+@(test)
+interp_continuous_waiting :: proc(t: ^testing.T) {
+	cat: pp.Catalogs
+	motion_test_catalog(&cat, context.temp_allocator)
+	topo: pp.Topology
+	motion_test_network(&topo, &cat, context.temp_allocator)
+
+	p: pp.Packet
+	motion_test_packet(&p)
+	// waiting: at node 2 both ticks
+	p.on_edge = false
+	p.at_node = 2
+	testing.expect(t, interp_continuous(&topo, 0, 0, 2, false, &p), "waiting (same at_node) must be continuous")
+}
+
+@(test)
+interp_continuous_sever_snaps :: proc(t: ^testing.T) {
+	cat: pp.Catalogs
+	motion_test_catalog(&cat, context.temp_allocator)
+	topo: pp.Topology
+	motion_test_network(&topo, &cat, context.temp_allocator)
+
+	p: pp.Packet
+	motion_test_packet(&p)
+	// E29 severed drop-back: was on edge 0 heading 1 (B), now at node 0
+	// (the DEPARTURE — NOT the heading) → the position teleported → snap.
+	p.on_edge = false
+	p.at_node = 0
+	testing.expect(t, !interp_continuous(&topo, 0, 1, 0, true, &p), "sever drop-back (at_node != heading) must snap")
+}
+
+@(test)
+interp_continuous_reroute_snaps :: proc(t: ^testing.T) {
+	cat: pp.Catalogs
+	motion_test_catalog(&cat, context.temp_allocator)
+	topo: pp.Topology
+	motion_test_network(&topo, &cat, context.temp_allocator)
+
+	p: pp.Packet
+	motion_test_packet(&p)
+	// ECMP reroute: was on edge 0 heading 1, now on edge 1 (B→C) — a
+	// different edge entirely → snap (the packet was never on edge 1).
+	p.edge = 1
+	p.heading = 2
+	testing.expect(t, !interp_continuous(&topo, 0, 1, 0, true, &p), "edge change mid-flight must snap")
+}
+
+@(test)
+interp_continuous_spawn_snaps :: proc(t: ^testing.T) {
+	cat: pp.Catalogs
+	motion_test_catalog(&cat, context.temp_allocator)
+	topo: pp.Topology
+	motion_test_network(&topo, &cat, context.temp_allocator)
+
+	// a spawn: the packet appears at a node it was never heading toward
+	// (the at_node change is not an arrival — the anchor is new)
+	p: pp.Packet
+	motion_test_packet(&p)
+	p.on_edge = false
+	p.at_node = 2
+	testing.expect(t, !interp_continuous(&topo, 0, 0, 0, false, &p), "fresh at_node (no prior edge) must snap")
+}
+
+@(test)
+interp_continuous_delivery_snaps :: proc(t: ^testing.T) {
+	cat: pp.Catalogs
+	motion_test_catalog(&cat, context.temp_allocator)
+	topo: pp.Topology
+	motion_test_network(&topo, &cat, context.temp_allocator)
+
+	// delivery: the packet vanished (delivered=true) — it is not drawn at
+	// all. The guard must snap (no row update → the stale row is pruned).
+	p: pp.Packet
+	motion_test_packet(&p)
+	p.delivered = true
+	// a delivered packet's anchor is irrelevant — the draw loop skips it
+	// BEFORE the interp; the guard's job is to snap any attempted transition
+	p.on_edge = false
+	p.at_node = 2
+	testing.expect(t, !interp_continuous(&topo, 0, 1, 0, true, &p), "delivered transition must snap")
+}
+
+// ---------------------------------------------------------------- (b) the
+// row roll + alpha endpoints: the glide between the two snapshot positions.
+
+@(test)
+interp_pos_row_roll_and_alpha_endpoints :: proc(t: ^testing.T) {
+	cat: pp.Catalogs
+	motion_test_catalog(&cat, context.temp_allocator)
+	topo: pp.Topology
+	motion_test_network(&topo, &cat, context.temp_allocator)
+
+	v: View
+	motion_test_view(&v, &cat)
+	defer delete(v.pkt_interp)  // the interp map is default-allocated (the temp arena would leak it)
+
+	// the packet on edge 0 at frac 0.5: world x = 10*26 + 0.5*(20-10)*26 = 390
+	p: pp.Packet
+	motion_test_packet(&p)
+	p.progress_units = 60 // frac 0.5 → x 390
+
+	// frame 1 at tick 44: the packet's snapshot pos (screen) is x 390
+	pos := node_screen(&v, topo.node_pos[1]) // hmm — compute the actual position
+	_ = pos
+	// compute the current snapshot position the way draw_packets does
+	depart := node_screen(&v, topo.node_pos[0])
+	arrive := node_screen(&v, topo.node_pos[1])
+	snap := rl.Vector2{depart.x + (arrive.x - depart.x) * 0.5, depart.y + (arrive.y - depart.y) * 0.5}
+
+	// first frame at tick 44 (no row) → snap: drawn at the snapshot position
+	drawn, _, _ := packet_interp_pos(&v, &topo, &p, snap, 44, 0.0)
+	testing.expect(t, abs(drawn.x - snap.x) < 0.001, "spawn frame draws the snapshot position (no ghost)")
+	row, ok := v.pkt_interp[p.id]
+	testing.expect(t, ok, "row created on the spawn frame")
+	testing.expect(t, row.tick == 44, "row tick is the spawn tick")
+
+	// the packet advances to frac 0.75 (x = 10*26 + 0.75*260 = 455) at tick 45
+	p.progress_units = 90 // frac 0.75
+	new_snap := rl.Vector2{depart.x + (arrive.x - depart.x) * 0.75, depart.y + (arrive.y - depart.y) * 0.75}
+
+	// alpha=0 → the glide BASE: the PREVIOUS tick's position (390)
+	drawn0, _, _ := packet_interp_pos(&v, &topo, &p, new_snap, 45, 0.0)
+	testing.expect(t, abs(drawn0.x - snap.x) < 0.001, "alpha=0 draws the previous tick position (glide base)")
+	row, ok = v.pkt_interp[p.id]
+	testing.expect(t, ok && row.tick == 45, "row rolled to tick 45")
+	testing.expect(t, abs(row.prev.x - snap.x) < 0.001, "row.prev is the T-1 position")
+	testing.expect(t, abs(row.cur.x - new_snap.x) < 0.001, "row.cur is the T position")
+
+	// alpha=1 → the glide TARGET: the CURRENT tick's position (455)
+	drawn1, _, _ := packet_interp_pos(&v, &topo, &p, new_snap, 45, 1.0)
+	testing.expect(t, abs(drawn1.x - new_snap.x) < 0.001, "alpha=1 draws the current tick position (glide target)")
+
+	// mid-tick alpha=0.5 → exactly between the two snapshot positions
+	drawnm, _, _ := packet_interp_pos(&v, &topo, &p, new_snap, 45, 0.5)
+	want := (snap.x + new_snap.x) * 0.5
+	testing.expect(t, abs(drawnm.x - want) < 0.001, "alpha=0.5 is the midpoint of the two snapshot positions")
+}
+
+// ---------------------------------------------------------------- (c) the
+// snap paths: missing row (spawn), tick gap, anchor mismatch — no ghost.
+
+@(test)
+interp_pos_tick_gap_snaps :: proc(t: ^testing.T) {
+	cat: pp.Catalogs
+	motion_test_catalog(&cat, context.temp_allocator)
+	topo: pp.Topology
+	motion_test_network(&topo, &cat, context.temp_allocator)
+
+	v: View
+	motion_test_view(&v, &cat)
+	defer delete(v.pkt_interp)  // the interp map is default-allocated (the temp arena would leak it)
+
+	p: pp.Packet
+	motion_test_packet(&p)
+	depart := node_screen(&v, topo.node_pos[0])
+	arrive := node_screen(&v, topo.node_pos[1])
+	snap := rl.Vector2{depart.x + (arrive.x - depart.x) * 0.5, depart.y + (arrive.y - depart.y) * 0.5}
+
+	// seed a row at tick 44
+	packet_interp_pos(&v, &topo, &p, snap, 44, 0.0)
+	// the sim jumped 3 ticks (multi-step catch-up): tick 48 — the row is
+	// older than tick-1 → snap at the CURRENT snapshot position
+	p.progress_units = 90
+	new_snap := rl.Vector2{depart.x + (arrive.x - depart.x) * 0.75, depart.y + (arrive.y - depart.y) * 0.75}
+	drawn, _, _ := packet_interp_pos(&v, &topo, &p, new_snap, 48, 0.5)
+	testing.expect(t, abs(drawn.x - new_snap.x) < 0.001, "tick gap snaps to the current snapshot (no ghost)")
+}
+
+@(test)
+interp_pos_anchor_mismatch_snaps :: proc(t: ^testing.T) {
+	cat: pp.Catalogs
+	motion_test_catalog(&cat, context.temp_allocator)
+	topo: pp.Topology
+	motion_test_network(&topo, &cat, context.temp_allocator)
+
+	v: View
+	motion_test_view(&v, &cat)
+	defer delete(v.pkt_interp)  // the interp map is default-allocated (the temp arena would leak it)
+
+	p: pp.Packet
+	motion_test_packet(&p)
+	depart := node_screen(&v, topo.node_pos[0])
+	arrive := node_screen(&v, topo.node_pos[1])
+	snap := rl.Vector2{depart.x + (arrive.x - depart.x) * 0.5, depart.y + (arrive.y - depart.y) * 0.5}
+
+	// seed a row: the packet ON edge 0 heading 1 at tick 44
+	packet_interp_pos(&v, &topo, &p, snap, 44, 0.0)
+	// the packet SEVERED back to node 0 (the departure) at tick 45 — the
+	// anchor mismatch must snap to the node position, never glide mid-edge
+	p.on_edge = false
+	p.at_node = 0
+	p.progress_units = 0
+	node0 := node_screen(&v, topo.node_pos[0])
+	drawn, _, _ := packet_interp_pos(&v, &topo, &p, node0, 45, 0.5)
+	testing.expect(t, abs(drawn.x - node0.x) < 0.001 && abs(drawn.y - node0.y) < 0.001,
+		"anchor mismatch snaps to the node position (no ghost)")
+}
+
+// ---------------------------------------------------------------- (d) cache
+// lifecycle: reset empties, prune drops absent ids and keeps live ones.
+
+@(test)
+interp_reset_and_prune :: proc(t: ^testing.T) {
+	cat: pp.Catalogs
+	motion_test_catalog(&cat, context.temp_allocator)
+	topo: pp.Topology
+	motion_test_network(&topo, &cat, context.temp_allocator)
+
+	v: View
+	motion_test_view(&v, &cat)
+	defer delete(v.pkt_interp)  // the interp map is default-allocated (the temp arena would leak it)
+
+	p: pp.Packet
+	motion_test_packet(&p)
+	depart := node_screen(&v, topo.node_pos[0])
+	arrive := node_screen(&v, topo.node_pos[1])
+	snap := rl.Vector2{depart.x + (arrive.x - depart.x) * 0.5, depart.y + (arrive.y - depart.y) * 0.5}
+
+	// two packets' rows
+	p2: pp.Packet
+	motion_test_packet(&p2, 8)
+	packet_interp_pos(&v, &topo, &p, snap, 44, 0.0)
+	packet_interp_pos(&v, &topo, &p2, snap, 44, 0.0)
+	// seed enough DISTINCT ids to exceed the prune bound (max(128, live*2+64)
+	// with 1 live packet → 128 rows needed before the prune engages)
+	for id in u64(100) ..< 100 + 130 {
+		pp2: pp.Packet
+		motion_test_packet(&pp2, id)
+		packet_interp_pos(&v, &topo, &pp2, snap, 44, 0.0)
+	}
+	testing.expect(t, len(v.pkt_interp) > 128, "seeded the prune threshold")
+
+	// prune with only packet 7 live → every other row (delivered) drops
+	flow: pp.Flow_State
+	flow.packets = make([dynamic]pp.Packet, 0, 2, context.temp_allocator)
+	append(&flow.packets, p)
+	packet_interp_prune(&v, &flow)
+	testing.expect(t, len(v.pkt_interp) == 1, "prune drops delivered ids")
+	_, ok := v.pkt_interp[p.id]
+	testing.expect(t, ok, "prune keeps live ids")
+
+	// reset empties the cache entirely
+	packet_interp_reset(&v)
+	testing.expect(t, len(v.pkt_interp) == 0, "reset empties the cache")
+}
+
+// ---------------------------------------------------------------- (e) the
+// reduced-motion echo gate (W6): trails_active() is the single predicate.
+
+@(test)
+trails_gate_reduced_motion :: proc(t: ^testing.T) {
+	cat: pp.Catalogs
+	motion_test_catalog(&cat, context.temp_allocator)
+	v: View
+	motion_test_view(&v, &cat)
+	defer delete(v.pkt_interp)  // the interp map is default-allocated (the temp arena would leak it)
+
+	// echoes on when moving + not reduced
+	testing.expect(t, trails_active(&v, 3), "trails active with echoes and no reduced-motion")
+	// reduced-motion pins echoes off REGARDLESS of the ring
+	v.reduced_motion = true
+	testing.expect(t, !trails_active(&v, 3), "reduced-motion pins echoes off even with a full ring")
+	// an empty ring draws nothing either way
+	v.reduced_motion = false
+	testing.expect(t, !trails_active(&v, 0), "empty ring draws no echoes")
+}
diff --git a/app/render/view.odin b/app/render/view.odin
index e29b87f..ce8849f 100644
--- a/app/render/view.odin
+++ b/app/render/view.odin
@@ -71,6 +71,18 @@ View :: struct {
 	// int helper's factor — keep reads through hud()/hud_f() so draw +
 	// hit-test can never diverge (the single-source rect rule).
 	ui_scale: f32,
+	// 2.1 motion-readability (packet-plumber-v2-motion-readability): the
+	// SUB-TICK packet cache — per in-flight packet id, the packet's drawn
+	// WORLD position at the previous tick (prev) + at the current tick (cur)
+	// + its location anchor, so the render can lerp between the last two
+	// 20 Hz snapshots (the look-book §4 motion canon — "interpolate position
+	// between sim snapshots for 60 fps smoothness"). View-owned presentation
+	// state (ODN-1 — the sim never sees it; T1 hashes ignore it). Touched
+	// ONLY when interp_alpha < 1.0 (the app path): the harness renders
+	// snapshot-exact (alpha=1.0 default) and never allocates/reads it, so T2
+	// goldens stay byte-identical by construction. Lazily made; pruned to the
+	// live packet set (ids are monotonic — delivered ids would linger).
+	pkt_interp: map[u64]Packet_Interp_Entry,
 }
 
 // Drag_State — the live drag preview state, owned by the app. The view only
@@ -88,6 +100,253 @@ Drag_State :: struct {
 	placing:   i32, // 3.5: node-type index in placement mode, else -1
 }
 
+// Packet_Interp_Entry — the 2.1 sub-tick cache row: one per in-flight packet
+// id, holding the packet's drawn WORLD position at the previous tick (`prev`)
+// and at the current tick (`cur`) + its location anchor, so the render can
+// lerp between the last two 20 Hz snapshots (the §4 motion canon). `tick` is
+// the sim tick `cur` belongs to. `trail` is the 3-echo fading trail ring
+// (the MM "consistent speed" read — image_01/03/05/07): the last drawn
+// positions, rendered as low-alpha echoes under the live packet. World-space
+// throughout (camera-independent — a pan/zoom ease mid-tick must not smear
+// the glide). Presentation-only (ODN-1); never serialized.
+Packet_Interp_Entry :: struct {
+	tick:   u64,
+	prev:   rl.Vector2, // world pos at tick-1 (the lerp base)
+	cur:    rl.Vector2, // world pos at tick (the lerp target)
+	// the location anchor when the row was written — the continuity guard:
+	// the lerp runs only for identity-continuous motion (same edge / arrival /
+	// forward / waiting); anything else (spawn, sever, reroute, delivery)
+	// snaps, so a sim teleport never smears across the map.
+	on_edge: bool,
+	edge:    u32,
+	heading: u32,
+	at_node: u32,
+	// the fading echo ring (drawn world positions, newest last).
+	trail:   [3]rl.Vector2,
+	trail_n: u32,
+}
+
+// interp_identity — the packet's location anchor as a comparable row (the
+// continuity-guard input).
+interp_identity :: proc(p: ^pp.Packet) -> (on_edge: bool, edge, heading, at_node: u32) {
+	return p.on_edge, p.edge, p.heading, p.at_node
+}
+
+// interp_continuous — may the render lerp between the row's anchor (the
+// previous tick) and the packet's anchor (this tick)? TRUE for the four
+// ordinary motion kinds — mid-edge travel (same edge + heading), arrival
+// (was heading toward the node it now sits at), forward (was at the node the
+// edge departs from), waiting (same node) — and FALSE for every teleport
+// (spawn, sever drop-back, reroute, delivery), which snaps instead. The
+// arrival/forward cases are position-continuous in world space (the node is
+// the edge's endpoint), so the glide stays honest there.
+interp_continuous :: proc(
+	topo: ^pp.Topology,
+	entry_edge, entry_heading, entry_at_node: u32,
+	entry_on_edge: bool,
+	p: ^pp.Packet,
+) -> bool {
+	if entry_on_edge == p.on_edge {
+		if p.on_edge {
+			return entry_edge == p.edge && entry_heading == p.heading
+		}
+		return entry_at_node == p.at_node
+	}
+	if entry_on_edge {
+		// arrival: was heading toward the node it now sits at
+		return entry_heading == p.at_node
+	}
+	// forward: was at the node this edge departs from (the endpoint that
+	// is NOT `heading`)
+	ps, ok := pp.pipe_slot(topo, p.edge)
+	if !ok {
+		return false
+	}
+	a_id := topo.pipe_a[ps]
+	b_id := topo.pipe_b[ps]
+	depart := b_id if a_id == p.heading else a_id
+	return entry_at_node == depart
+}
+
+// packet_interp_reset — drop every sub-tick cache row (called on run start:
+// packet ids recycle across runs — a stale row would anchor a fresh run's
+// glide on a previous run's position; the continuity guard would snap anyway,
+// but a clean table is the honest reset). App-only; the harness never calls
+// it (its snapshot renders never touch the table).
+packet_interp_reset :: proc(v: ^View) {
+	clear(&v.pkt_interp)
+}
+
+// packet_interp_prune — keep the table bounded: delivered packets vanish
+// from flow.packets but their ids are monotonic, so stale rows would
+// accumulate for a long session. When the table outgrows the live set by a
+// margin, rebuild it keeping only live ids. Draw-order-independent (lookup
+// only — never iterated in the draw pass).
+packet_interp_prune :: proc(v: ^View, flow: ^pp.Flow_State) {
+	live := len(flow.packets)
+	if len(v.pkt_interp) <= max(128, live*2+64) {
+		return
+	}
+	fresh := make(map[u64]Packet_Interp_Entry, live+16)
+	for p in flow.packets {
+		if e, ok := v.pkt_interp[p.id]; ok {
+			fresh[p.id] = e
+		}
+	}
+	delete(v.pkt_interp)
+	v.pkt_interp = fresh
+}
+
+// PACKET_R_FACTOR — the 2.1 packet-size read: ×1.15 (+15%, r≈8px → ~9.2px
+// at fit). The §4 motion-readability direction verbatim ("packet size +15%...
+// glint tuning for speed perception"); verified against the dense-core +
+// corridor crops 2026-08-22 (Kyle: HELP on both, no overlap regression).
+// View-layer only (ODN-1). Re-blesses every packet-bearing T2 golden with a
+// documented cause (packet pixels legitimately move); T1 + log.bin untouched.
+PACKET_R_FACTOR :: 1.15
+
+// TRAIL_FADES — the 3-echo trail alpha ladder (the MM "consistent speed"
+// read: the newest echo is the strongest, the oldest is a ghost). Drawn in
+// the packet's own body color at low alpha — the §4 direction verbatim
+// ("trail = the packet color at low alpha"). Reduced-motion pins the echoes
+// off (E9.2 decoration gate); the live packet + interpolation stay (packet
+// motion is a gameplay readout, never disabled — the 7.3 canon).
+TRAIL_FADES :: [3]f32{0.30, 0.20, 0.12}
+
+// trails_active — the echo-ring gate (Perkins r1 W6: golden captures render
+// at alpha=1.0 so trail_n is always 0 and the reduced-motion branch never
+// evaluates under the golden gates — extracted as a pure predicate so the
+// motion tests can pin it): echoes draw ONLY when the ring has entries AND
+// reduced-motion is off. The live packet + the glide are NEVER gated here.
+trails_active :: proc(v: ^View, trail_n: u32) -> bool {
+	return trail_n > 0 && !v.reduced_motion
+}
+
+// packet_interp_pos — the 2.1 sub-tick glide: lerp the packet's drawn
+// position between the last two 20 Hz snapshot positions using the render
+// frame's fractional progress (alpha = the app's accum/tick_seconds ∈ [0,1)).
+// `pos` is the CURRENT snapshot's screen position (the lerp TARGET — the
+// existing draw math, unchanged); the cache row holds the packet's drawn
+// WORLD position at the previous tick (`prev`) and at the current tick
+// (`cur`). World-space lerp: the focus-zoom camera eases BETWEEN ticks, so a
+// screen-space lerp would smear; world-space is camera-independent.
+// Returns the lerped screen position + the fading echo ring (the previous
+// frames' drawn world positions — the MM trail read, §4).
+//
+// Row semantics per frame at sim tick T:
+//   - row.tick == T (later render frames within the same tick — 60 Hz render
+//     vs 20 Hz sim): lerp between the stored prev/cur pair.
+//   - row.tick == T-1 (the FIRST frame after a step): roll the row — prev :=
+//     row.cur (the position at T-1), cur := current — then lerp.
+//   - row missing / row.tick < T-1 (spawn, delivered, multi-step catch-up,
+//     pause/resume): snap — prev = cur = current (the packet appears at its
+//     snapshot position; no smear across a gap).
+// Identity guard: the lerp is valid ONLY for identity-continuous motion
+// (interp_continuous — same-edge travel, arrival, forward, waiting). A sim
+// teleport (severed drop-back, ECMP reroute, spawn) snaps, so the sim's
+// truth never smears across the map. Presentation-only (ODN-1).
+packet_interp_pos :: proc(
+	v: ^View,
+	topo: ^pp.Topology,
+	p: ^pp.Packet,
+	pos: rl.Vector2,
+	tick: u64,
+	alpha: f32,
+) -> (rl.Vector2, [3]rl.Vector2, u32) {
+	wx, wy := from_screen(v, pos.x, pos.y)
+	cur := rl.Vector2{wx, wy}
+	on_edge, edge, heading, at_node := interp_identity(p)
+
+	out := pos
+	trail: [3]rl.Vector2
+	trail_n: u32 = 0
+
+	row, ok := v.pkt_interp[p.id]
+
+	// the cache map is lazily created on FIRST interpolated use — the harness
+	// renders snapshot-exact (alpha=1.0) and never reaches here, so goldens
+	// never allocate or touch it (zero golden impact by construction).
+	if v.pkt_interp == nil {
+		v.pkt_interp = make(map[u64]Packet_Interp_Entry, 64)
+		ok = false
+	}
+
+	// snap helpers — a fresh row at the current snapshot position (no smear)
+	snap := proc(row: ^Packet_Interp_Entry, tick: u64, cur: rl.Vector2, on_edge: bool, edge, heading, at_node: u32) {
+		row^ = Packet_Interp_Entry{
+			tick = tick, prev = cur, cur = cur,
+			on_edge = on_edge, edge = edge, heading = heading, at_node = at_node,
+		}
+	}
+
+	if !ok || row.tick < tick - 1 {
+		// new packet or a tick gap (spawn, delivered, multi-step catch-up,
+		// pause/resume) — snap at the snapshot position
+		snap(&row, tick, cur, on_edge, edge, heading, at_node)
+		v.pkt_interp[p.id] = row
+		return out, trail, trail_n
+	}
+
+	// the row's anchor vs the packet's anchor — the continuity guard
+	if !interp_continuous(topo, row.edge, row.heading, row.at_node, row.on_edge, p) {
+		// a sim teleport (sever drop-back, ECMP reroute) — snap
+		snap(&row, tick, cur, on_edge, edge, heading, at_node)
+		v.pkt_interp[p.id] = row
+		return out, trail, trail_n
+	}
+
+	if row.tick == tick - 1 {
+		// the FIRST frame after a step: roll the row — prev := the position
+		// at T-1 (row.cur), cur := the position at T (current)
+		row.prev = row.cur
+		row.cur = cur
+		row.tick = tick
+		row.on_edge = on_edge
+		row.edge = edge
+		row.heading = heading
+		row.at_node = at_node
+	}
+
+	// lerp between the last two snapshot positions (world space)
+	lx := row.prev.x + (row.cur.x - row.prev.x) * alpha
+	ly := row.prev.y + (row.cur.y - row.prev.y) * alpha
+	out = to_screen(v, lx, ly)
+
+	// the fading echo ring: the previously DRAWN positions (this frame's
+	// drawn pos pushes at the end — the draw reads the ring BEFORE the push,
+	// so echoes lag the live packet). Only moving packets push (a stationary
+	// dot would stack echoes at one spot and read as a smudge).
+	// Ring invariant: filled slots are [0..n-1], 0 = oldest, n-1 = newest.
+	echo_trail := row.trail
+	echo_n := row.trail_n
+	moved := echo_n == 0
+	if echo_n > 0 {
+		nw := row.trail[echo_n - 1]
+		moved = rl.Vector2Distance(out, to_screen(v, nw.x, nw.y)) > 0.5
+	}
+	if moved {
+		// the DRAWN world position (the lerped one — echoes lag the live
+		// packet by the same glide)
+		dwx, dwy := from_screen(v, out.x, out.y)
+		trail := row.trail
+		if row.trail_n < len(trail) {
+			// append at [n] — 0 is the oldest, n-1 the newest
+			trail[row.trail_n] = {dwx, dwy}
+			row.trail_n += 1
+		} else {
+			// full — drop the oldest, shift, newest at the last slot (the
+			// capacity is len(trail) — never a hardcoded index; Perkins r1 N9)
+			for k in 0..<len(trail) - 1 {
+				trail[k] = trail[k + 1]
+			}
+			trail[len(trail) - 1] = {dwx, dwy}
+		}
+		row.trail = trail
+	}
+	v.pkt_interp[p.id] = row
+	return out, echo_trail, echo_n
+}
+
 // view_compute — camera-fit the world (map_w×map_h tiles) into the window like
 // GL5.2's aspect=expand: wider/taller windows reveal more map. Pure float div.
 view_compute :: proc(v: ^View, win_w, win_h: i32, bal: ^pp.Balance) {
@@ -133,8 +392,11 @@ node_screen :: proc(v: ^View, pos: [2]i32) -> rl.Vector2 {
 // the selected pipe id (app interaction; -1 = none — the harness passes the
 // default, so goldens never carry selection UI). `seed` is the RUN seed — the
 // procedural map derives from it (7.4/canon D9; same seed → byte-identical
-// map, presentation-only, never perturbs the sim).
-draw_world :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^pp.Flow_State, crisis: ^pp.Crisis_State, tick: u64, drag: Drag_State, sel: i64 = -1, focus_class: i32 = -1, seed: u64) {
+// map, presentation-only, never perturbs the sim). `interp_alpha` is the
+// render frame's fractional progress within the current tick (the app's
+// accum/tick_seconds, 0..1) — the 2.1 sub-tick packet glide. The harness
+// leaves the default 1.0 (snapshot-exact — T2 goldens byte-identical).
+draw_world :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^pp.Flow_State, crisis: ^pp.Crisis_State, tick: u64, drag: Drag_State, sel: i64 = -1, focus_class: i32 = -1, seed: u64, interp_alpha: f32 = 1.0) {
 	map_draw(v, seed)
 	// 7.5: the DRAWN wire paths — computed once per frame ONLY when a wire
 	// aesthetic is active (routing or anchors). The shipped verdict keeps both
@@ -146,7 +408,7 @@ draw_world :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^pp
 	}
 	draw_bundles(v, topo, bundles, flow, crisis, paths[:])
 	draw_nodes(v, topo, crisis, tick)
-	draw_packets(v, topo, bundles, flow, focus_class, paths[:])
+	draw_packets(v, topo, bundles, flow, tick, focus_class, interp_alpha, paths[:])
 	// 4.2: the crisis bottleneck outline — the named bundle's member pipes
 	// (pulsing red stroke, on top of the pipes so the highlight reads).
 	draw_crisis_outlines(v, topo, bundles, crisis, tick, paths[:])
@@ -1068,6 +1330,34 @@ draw_tier_ring :: proc(v: ^View, c: rl.Vector2, dst: rl.Rectangle, tier: rl.Colo
 	}
 }
 
+// draw_packet_shape — ONE definition of the packet body geometry (Perkins r1
+// N14: the echo ring used to duplicate the live shape's switch — a restated
+// copy drifts). Draws outline + body for both shapes: streaming = an
+// equilateral triangle (apex up), everything else = the 1.3 dot (circle).
+// The GLINT is NOT part of the body — it is the live packet's read, drawn
+// by the caller (echoes carry no sparkle).
+draw_packet_shape :: proc(pos: rl.Vector2, r: f32, body, outline: rl.Color, shape: pp.Packet_Shape) {
+	#partial switch shape {
+	case .Triangle:
+		half := r * 0.866
+		rl.DrawTriangle(
+			rl.Vector2{pos.x, pos.y - r},
+			rl.Vector2{pos.x - half, pos.y + r * 0.5},
+			rl.Vector2{pos.x + half, pos.y + r * 0.5},
+			outline,
+		)
+		rl.DrawTriangle(
+			rl.Vector2{pos.x, pos.y - r * 0.78},
+			rl.Vector2{pos.x - half * 0.78, pos.y + r * 0.5 * 0.78},
+			rl.Vector2{pos.x + half * 0.78, pos.y + r * 0.5 * 0.78},
+			body,
+		)
+	case: // Circle + the not-yet-rendered shapes fall back to the 1.3 dot
+		rl.DrawCircleV(pos, r, outline)
+		rl.DrawCircleV(pos, r * 0.78, body)
+	}
+}
+
 // draw_packets — the packet dots (1.3 render pass 5). Each in-flight packet
 // is drawn at a lerped position: on-edge packets sit `progress` of the way
 // along their current pipe (departure node -> heading); at-node packets sit on
@@ -1082,7 +1372,14 @@ draw_tier_ring :: proc(v: ^View, c: rl.Vector2, dst: rl.Rectangle, tier: rl.Colo
 // Best-effort crawls). 7.1: queued packets (on-edge, progress ~0) wait at the
 // departure building's DOORSTEP (a deterministic fan — the serialization
 // visual, off the roof).
-draw_packets :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^pp.Flow_State, focus_class: i32 = -1, paths: []Wire_Path = nil) {
+//
+// 2.1 motion-readability: `tick` is the sim tick the snapshot belongs to;
+// `interp_alpha` is the render frame's fractional progress within the tick
+// (the app's accum/tick_seconds ∈ [0,1)) — the packet glides between the
+// last two 20 Hz snapshots (the §4 motion canon: "interpolate position
+// between sim snapshots for 60 fps smoothness"). The harness leaves the
+// default 1.0 (snapshot-exact) → T2 goldens byte-identical by construction.
+draw_packets :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^pp.Flow_State, tick: u64, focus_class: i32 = -1, interp_alpha: f32 = 1.0, paths: []Wire_Path = nil) {
 	bandwidth := u32(v.catalogs.balance.packet_bandwidth)
 	for i in 0..<len(flow.packets) {
 		p := &flow.packets[i]
@@ -1224,8 +1521,28 @@ draw_packets :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
 				pos.y += 0.62 * s + ky
 			}
 		}
+		// 2.1 motion-readability: the SUB-TICK GLIDE — view-layer lerp between
+		// the last two snapshot positions using the render frame's fractional
+		// progress. Snapshot-exact when interp_alpha >= 1.0 (the harness — the
+		// cache is never touched, so goldens stay byte-identical). World-space
+		// lerp (camera-independent: the focus-zoom ease moves the camera
+		// BETWEEN ticks, so a screen-space lerp would smear). Presentation-
+		// only (ODN-1 — the sim's 20 Hz truth is untouched; T1 ignores it).
+		// Returns the lerped screen pos + the fading echo ring (the MM
+		// "consistent speed" read — the packet's color at low alpha, §4).
+		trail_world: [3]rl.Vector2
+		trail_n: u32 = 0
+		if interp_alpha < 1.0 {
+			pos, trail_world, trail_n = packet_interp_pos(v, topo, p, pos, tick, interp_alpha)
+		}
 		// 7.1: the MM car read — packets are bigger than the 1.3 dots.
-		r := v.tile_px * v.scale * 0.24 * 1.35
+		// 2.1 motion-readability: PACKET_R_FACTOR = ×1.15 (+15% — the §4
+		// direction "packet size +15% (from 8px to 9.2px)", verified on the
+		// dense-core + corridor crops 2026-08-22: HELP on both, no overlap
+		// regression). A VIEW constant — the sim never sees it (ODN-1). This
+		// legitimately moves packet pixels in every packet-bearing T2 golden
+		// (a documented re-bless; T1 manifests + log.bin stay byte-identical).
+		r := v.tile_px * v.scale * 0.24 * 1.35 * PACKET_R_FACTOR
 		// 3.1: per-class packet rendering — SHAPE is the primary distinguisher
 		// ([UX-DR4]: never color alone; accessibility), the catalog color_rgba the
 		// secondary cue. Unknown/absent classes fall back to the 1.3 dot.
@@ -1251,39 +1568,44 @@ draw_packets :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
 			body.a = u8(f32(body.a) * 0.22)
 			outline.a = u8(f32(outline.a) * 0.22)
 		}
+		// 2.1: the fading echo ring (app path only — the harness renders
+		// snapshot-exact, so goldens never see it). Drawn UNDER the live
+		// packet: the packet's own body color at low alpha, oldest first,
+		// newest-echo strongest (the MM "consistent speed" trail read — §4).
+		// Reduced-motion pins the echoes off (E9.2 decoration gate — the live
+		// packet + the glide stay: packet motion is a gameplay readout, never
+		// disabled).
+		if trails_active(v, trail_n) {
+			fades := TRAIL_FADES // local copy — a constant can't be indexed by a runtime index
+			for k in 0..<trail_n {
+				e := to_screen(v, trail_world[k].x, trail_world[k].y)
+				// the newest echo (highest k) is the strongest
+				fade := fades[trail_n - 1 - k]
+				ebody := rl.Color{u8(f32(body.r) * fade), u8(f32(body.g) * fade), u8(f32(body.b) * fade), u8(f32(body.a) * fade)}
+				eout := rl.Color{u8(f32(outline.r) * fade), u8(f32(outline.g) * fade), u8(f32(outline.b) * fade), u8(f32(outline.a) * fade)}
+				draw_packet_shape(e, r, ebody, eout, shape)
+			}
+		}
+		draw_packet_shape(pos, r, body, outline, shape)
+		// 8.x the glint (v2-look-polish, user gate): the warm-cream highlight
+		// that makes the 7.1 car-size dots read as polished at bird's-eye — the
+		// stream glint sits just below the apex, the circle glint up-left of
+		// center. Alpha follows body.a so a focused-out ghost packet dims its
+		// glint too (the never-color-alone + ghost-read rules). Echoes carry NO
+		// glint — the sparkle is the LIVE packet's read.
 		#partial switch shape {
 		case .Triangle:
-			// streaming: an equilateral triangle (apex up), outline + body like the dot
-			half := r * 0.866
-			rl.DrawTriangle(
-				rl.Vector2{pos.x, pos.y - r},
-				rl.Vector2{pos.x - half, pos.y + r * 0.5},
-				rl.Vector2{pos.x + half, pos.y + r * 0.5},
-				outline,
-			)
-			rl.DrawTriangle(
-				rl.Vector2{pos.x, pos.y - r * 0.78},
-				rl.Vector2{pos.x - half * 0.78, pos.y + r * 0.5 * 0.78},
-				rl.Vector2{pos.x + half * 0.78, pos.y + r * 0.5 * 0.78},
-				body,
-			)
-			// 8.x the stream glint (v2-look-polish, user gate): the streaming
-			// triangles get the SAME warm-cream highlight as the circular dots
-			// ("the stream might need the same touch up") — placed just below
-			// the apex, inside the body. Alpha follows body.a (ghost dims).
 			rl.DrawCircleV({pos.x - r * 0.16, pos.y - r * 0.34}, r * 0.20, rl.Color{250, 246, 238, body.a})
-		case: // Circle + the not-yet-rendered shapes fall back to the 1.3 dot
-			rl.DrawCircleV(pos, r, outline)
-			rl.DrawCircleV(pos, r * 0.78, body)
-			// 8.x the MM-car glint (v2-look-polish): a small warm-cream
-			// highlight up-left of the dot center — the flat-2D glass read
-			// that makes the 7.1 car-size dots read as polished at bird's-eye.
-			// Circles only (the triangle keeps its clean apex shape). The
-			// alpha follows body.a so a focused-out ghost packet dims its
-			// glint too (the never-color-alone + ghost-read rules).
+		case:
 			rl.DrawCircleV({pos.x - r * 0.34, pos.y - r * 0.34}, r * 0.22, rl.Color{250, 246, 238, body.a})
 		}
 	}
+	// 2.1: keep the sub-tick cache bounded to the live packet set (delivered
+	// ids are monotonic and would otherwise accumulate for a long session).
+	// App path only — the harness (alpha=1.0) never allocates the map.
+	if interp_alpha < 1.0 {
+		packet_interp_prune(v, flow)
+	}
 }
 
 // draw_ghost — the drag preview: a line from the source node to the cursor,
diff --git a/demos/motion.dem b/demos/motion.dem
new file mode 100644
index 0000000..d6bfd62
--- /dev/null
+++ b/demos/motion.dem
@@ -0,0 +1,24 @@
+# motion.dem — 2.1 motion-readability: ONE packet on a long straight pipe,
+# mid-traversal for most of the strip window — the cleanest possible sub-tick
+# interpolation probe (a single dot on a single edge; no cluster ambiguity in
+# the displacement measurement). The 1.2 fixture is residential(0) <-
+# router(1) -> content_host(2), 12 tiles apart on row y=15. Draw source->
+# router then router->sink at the 'standard' tier; spawn one packet at
+# 2050ms. At the post-pace-tuning bandwidth (120) a standard pipe (cap 15)
+# takes 8 ticks/edge = 400 ms: the packet crosses edge0 from ~t42 to ~t50,
+# arrives at the router ~2450ms, and re-forwards toward the sink from there.
+# The 2200..2450ms strip window is therefore the pure mid-edge glide; the
+# tail of the window (2450ms+) is the post-arrival doorstep phase — the
+# displacement delta (steps vs glide) reads unmixed in the mid-edge part and
+# the arrival is visible as the packet's motion stopping (Perkins r1 W8: the
+# comment previously claimed "no arrivals" — ~10 of 24 AFTER frames are
+# post-arrival by this timeline).
+#
+# T1-only golden (no captures): the manifest + log pin the sim timeline; the
+# T2 pixels are the motion-strip verb's output (bin/motion-*), never a golden.
+seed 42
+run 3000ms
+at 500ms draw 0 1 standard
+at 1500ms draw 1 2 standard
+at 2050ms spawn 0 2
+expect hash stable
diff --git a/goldens/a11y_deutan/30000ms.png b/goldens/a11y_deutan/30000ms.png
index fcb0e96..d67e0a6 100644
Binary files a/goldens/a11y_deutan/30000ms.png and b/goldens/a11y_deutan/30000ms.png differ
diff --git a/goldens/a11y_deutan/65000ms.png b/goldens/a11y_deutan/65000ms.png
index 8b8a8d2..c72794f 100644
Binary files a/goldens/a11y_deutan/65000ms.png and b/goldens/a11y_deutan/65000ms.png differ
diff --git a/goldens/a11y_protan/30000ms.png b/goldens/a11y_protan/30000ms.png
index fcb0e96..d67e0a6 100644
Binary files a/goldens/a11y_protan/30000ms.png and b/goldens/a11y_protan/30000ms.png differ
diff --git a/goldens/a11y_protan/65000ms.png b/goldens/a11y_protan/65000ms.png
index 8b8a8d2..c72794f 100644
Binary files a/goldens/a11y_protan/65000ms.png and b/goldens/a11y_protan/65000ms.png differ
diff --git a/goldens/a11y_reduced/30000ms.png b/goldens/a11y_reduced/30000ms.png
index 24d9527..6a9d69d 100644
Binary files a/goldens/a11y_reduced/30000ms.png and b/goldens/a11y_reduced/30000ms.png differ
diff --git a/goldens/a11y_reduced/65000ms.png b/goldens/a11y_reduced/65000ms.png
index 04381e9..9640f0c 100644
Binary files a/goldens/a11y_reduced/65000ms.png and b/goldens/a11y_reduced/65000ms.png differ
diff --git a/goldens/a11y_scale/30000ms.png b/goldens/a11y_scale/30000ms.png
index be2803c..30d4e77 100644
Binary files a/goldens/a11y_scale/30000ms.png and b/goldens/a11y_scale/30000ms.png differ
diff --git a/goldens/a11y_scale/65000ms.png b/goldens/a11y_scale/65000ms.png
index f9f8d00..03e61c6 100644
Binary files a/goldens/a11y_scale/65000ms.png and b/goldens/a11y_scale/65000ms.png differ
diff --git a/goldens/a11y_tritan/30000ms.png b/goldens/a11y_tritan/30000ms.png
index 939dfaa..2c54971 100644
Binary files a/goldens/a11y_tritan/30000ms.png and b/goldens/a11y_tritan/30000ms.png differ
diff --git a/goldens/a11y_tritan/65000ms.png b/goldens/a11y_tritan/65000ms.png
index 967c499..5c9945c 100644
Binary files a/goldens/a11y_tritan/65000ms.png and b/goldens/a11y_tritan/65000ms.png differ
diff --git a/goldens/advance_block_legacy/15000ms.png b/goldens/advance_block_legacy/15000ms.png
index c072c14..cf61b3e 100644
Binary files a/goldens/advance_block_legacy/15000ms.png and b/goldens/advance_block_legacy/15000ms.png differ
diff --git a/goldens/advance_block_legacy/60000ms.png b/goldens/advance_block_legacy/60000ms.png
index ffabceb..9db37af 100644
Binary files a/goldens/advance_block_legacy/60000ms.png and b/goldens/advance_block_legacy/60000ms.png differ
diff --git a/goldens/advance_block_sla/15000ms.png b/goldens/advance_block_sla/15000ms.png
index 22fd8be..27ef0fe 100644
Binary files a/goldens/advance_block_sla/15000ms.png and b/goldens/advance_block_sla/15000ms.png differ
diff --git a/goldens/advance_block_sla/60000ms.png b/goldens/advance_block_sla/60000ms.png
index 5032bac..b835ca8 100644
Binary files a/goldens/advance_block_sla/60000ms.png and b/goldens/advance_block_sla/60000ms.png differ
diff --git a/goldens/advance_fire/15000ms.png b/goldens/advance_fire/15000ms.png
index e99ff44..b8ae3e2 100644
Binary files a/goldens/advance_fire/15000ms.png and b/goldens/advance_fire/15000ms.png differ
diff --git a/goldens/advance_fire/60000ms.png b/goldens/advance_fire/60000ms.png
index b1b54b9..578985e 100644
Binary files a/goldens/advance_fire/60000ms.png and b/goldens/advance_fire/60000ms.png differ
diff --git a/goldens/bundle/02850ms.png b/goldens/bundle/02850ms.png
index 35d443d..b412391 100644
Binary files a/goldens/bundle/02850ms.png and b/goldens/bundle/02850ms.png differ
diff --git a/goldens/demolish/01050ms.png b/goldens/demolish/01050ms.png
index fada3a5..d363f11 100644
Binary files a/goldens/demolish/01050ms.png and b/goldens/demolish/01050ms.png differ
diff --git a/goldens/demolish/01250ms.png b/goldens/demolish/01250ms.png
index b998da9..730b863 100644
Binary files a/goldens/demolish/01250ms.png and b/goldens/demolish/01250ms.png differ
diff --git a/goldens/demolish/01300ms.png b/goldens/demolish/01300ms.png
index 3c75357..532e1ad 100644
Binary files a/goldens/demolish/01300ms.png and b/goldens/demolish/01300ms.png differ
diff --git a/goldens/demolish_bundle/01100ms.png b/goldens/demolish_bundle/01100ms.png
index 568aa30..0db1e26 100644
Binary files a/goldens/demolish_bundle/01100ms.png and b/goldens/demolish_bundle/01100ms.png differ
diff --git a/goldens/demolish_bundle/01500ms.png b/goldens/demolish_bundle/01500ms.png
index 97a7015..97e2ce1 100644
Binary files a/goldens/demolish_bundle/01500ms.png and b/goldens/demolish_bundle/01500ms.png differ
diff --git a/goldens/demolish_node/01250ms.png b/goldens/demolish_node/01250ms.png
index 6196f9c..1a92637 100644
Binary files a/goldens/demolish_node/01250ms.png and b/goldens/demolish_node/01250ms.png differ
diff --git a/goldens/demolish_node/01450ms.png b/goldens/demolish_node/01450ms.png
index e77c37a..a9e23ae 100644
Binary files a/goldens/demolish_node/01450ms.png and b/goldens/demolish_node/01450ms.png differ
diff --git a/goldens/ecmp/01250ms.png b/goldens/ecmp/01250ms.png
index 9b01b9d..e1ba2d0 100644
Binary files a/goldens/ecmp/01250ms.png and b/goldens/ecmp/01250ms.png differ
diff --git a/goldens/ecmp/01350ms.png b/goldens/ecmp/01350ms.png
index 22fcdae..6969b6b 100644
Binary files a/goldens/ecmp/01350ms.png and b/goldens/ecmp/01350ms.png differ
diff --git a/goldens/ecmp_cost/01150ms.png b/goldens/ecmp_cost/01150ms.png
index a2414c5..3d7118c 100644
Binary files a/goldens/ecmp_cost/01150ms.png and b/goldens/ecmp_cost/01150ms.png differ
diff --git a/goldens/ecmp_cost/01450ms.png b/goldens/ecmp_cost/01450ms.png
index 23445e8..fe8dd9a 100644
Binary files a/goldens/ecmp_cost/01450ms.png and b/goldens/ecmp_cost/01450ms.png differ
diff --git a/goldens/era_advance/10000ms.png b/goldens/era_advance/10000ms.png
index f742134..ea015ef 100644
Binary files a/goldens/era_advance/10000ms.png and b/goldens/era_advance/10000ms.png differ
diff --git a/goldens/era_advance/55000ms.png b/goldens/era_advance/55000ms.png
index bb18228..6c0ce22 100644
Binary files a/goldens/era_advance/55000ms.png and b/goldens/era_advance/55000ms.png differ
diff --git a/goldens/estate_surge/25000ms.png b/goldens/estate_surge/25000ms.png
index ba53dfb..f2d6536 100644
Binary files a/goldens/estate_surge/25000ms.png and b/goldens/estate_surge/25000ms.png differ
diff --git a/goldens/estate_surge/75000ms.png b/goldens/estate_surge/75000ms.png
index 4f86c21..aa5ee15 100644
Binary files a/goldens/estate_surge/75000ms.png and b/goldens/estate_surge/75000ms.png differ
diff --git a/goldens/flow/02100ms.png b/goldens/flow/02100ms.png
index 73af400..a938eee 100644
Binary files a/goldens/flow/02100ms.png and b/goldens/flow/02100ms.png differ
diff --git a/goldens/flow/02150ms.png b/goldens/flow/02150ms.png
index 1dd3859..ae47826 100644
Binary files a/goldens/flow/02150ms.png and b/goldens/flow/02150ms.png differ
diff --git a/goldens/flow/02250ms.png b/goldens/flow/02250ms.png
index 216a0a8..7d1ee2b 100644
Binary files a/goldens/flow/02250ms.png and b/goldens/flow/02250ms.png differ
diff --git a/goldens/forecast_preview/30000ms.png b/goldens/forecast_preview/30000ms.png
index 9da70ee..37ffa80 100644
Binary files a/goldens/forecast_preview/30000ms.png and b/goldens/forecast_preview/30000ms.png differ
diff --git a/goldens/forecast_preview/31000ms.png b/goldens/forecast_preview/31000ms.png
index 0d7ae9a..3f9431c 100644
Binary files a/goldens/forecast_preview/31000ms.png and b/goldens/forecast_preview/31000ms.png differ
diff --git a/goldens/forecast_preview/32000ms.png b/goldens/forecast_preview/32000ms.png
index ab45297..859a5a0 100644
Binary files a/goldens/forecast_preview/32000ms.png and b/goldens/forecast_preview/32000ms.png differ
diff --git a/goldens/forecast_preview/33000ms.png b/goldens/forecast_preview/33000ms.png
index d0a419d..46dfcef 100644
Binary files a/goldens/forecast_preview/33000ms.png and b/goldens/forecast_preview/33000ms.png differ
diff --git a/goldens/forecast_shift/01300ms.png b/goldens/forecast_shift/01300ms.png
index 98aa5eb..2bce2b2 100644
Binary files a/goldens/forecast_shift/01300ms.png and b/goldens/forecast_shift/01300ms.png differ
diff --git a/goldens/forecast_shift/02800ms.png b/goldens/forecast_shift/02800ms.png
index 78d0bcd..828b0d1 100644
Binary files a/goldens/forecast_shift/02800ms.png and b/goldens/forecast_shift/02800ms.png differ
diff --git a/goldens/growth/15000ms.png b/goldens/growth/15000ms.png
index 1b40814..c7f3386 100644
Binary files a/goldens/growth/15000ms.png and b/goldens/growth/15000ms.png differ
diff --git a/goldens/growth/45000ms.png b/goldens/growth/45000ms.png
index 0e9ea5f..3f167b3 100644
Binary files a/goldens/growth/45000ms.png and b/goldens/growth/45000ms.png differ
diff --git a/goldens/growth/88000ms.png b/goldens/growth/88000ms.png
index 808f877..9b5e055 100644
Binary files a/goldens/growth/88000ms.png and b/goldens/growth/88000ms.png differ
diff --git a/goldens/health_lose/05000ms.png b/goldens/health_lose/05000ms.png
index 84fac0f..9a2a296 100644
Binary files a/goldens/health_lose/05000ms.png and b/goldens/health_lose/05000ms.png differ
diff --git a/goldens/health_lose/21000ms.png b/goldens/health_lose/21000ms.png
index e0adf09..54a86f5 100644
Binary files a/goldens/health_lose/21000ms.png and b/goldens/health_lose/21000ms.png differ
diff --git a/goldens/health_lose/23000ms.png b/goldens/health_lose/23000ms.png
index 718f6d0..07be87a 100644
Binary files a/goldens/health_lose/23000ms.png and b/goldens/health_lose/23000ms.png differ
diff --git a/goldens/health_win/150500ms.png b/goldens/health_win/150500ms.png
index cf57553..5afd80d 100644
Binary files a/goldens/health_win/150500ms.png and b/goldens/health_win/150500ms.png differ
diff --git a/goldens/health_win/30000ms.png b/goldens/health_win/30000ms.png
index fa1d98b..2f4d3b2 100644
Binary files a/goldens/health_win/30000ms.png and b/goldens/health_win/30000ms.png differ
diff --git a/goldens/health_win/75000ms.png b/goldens/health_win/75000ms.png
index 9670559..5271e71 100644
Binary files a/goldens/health_win/75000ms.png and b/goldens/health_win/75000ms.png differ
diff --git a/goldens/juice/30000ms.png b/goldens/juice/30000ms.png
index 24d9527..6a9d69d 100644
Binary files a/goldens/juice/30000ms.png and b/goldens/juice/30000ms.png differ
diff --git a/goldens/juice/65000ms.png b/goldens/juice/65000ms.png
index 4092d3e..5dba6a9 100644
Binary files a/goldens/juice/65000ms.png and b/goldens/juice/65000ms.png differ
diff --git a/goldens/legacy_decay/15000ms.png b/goldens/legacy_decay/15000ms.png
index e99ff44..b8ae3e2 100644
Binary files a/goldens/legacy_decay/15000ms.png and b/goldens/legacy_decay/15000ms.png differ
diff --git a/goldens/legacy_decay/60000ms.png b/goldens/legacy_decay/60000ms.png
index b1b54b9..578985e 100644
Binary files a/goldens/legacy_decay/60000ms.png and b/goldens/legacy_decay/60000ms.png differ
diff --git a/goldens/legacy_modernized/15000ms.png b/goldens/legacy_modernized/15000ms.png
index e99ff44..b8ae3e2 100644
Binary files a/goldens/legacy_modernized/15000ms.png and b/goldens/legacy_modernized/15000ms.png differ
diff --git a/goldens/legacy_modernized/60000ms.png b/goldens/legacy_modernized/60000ms.png
index 250f669..cb3f3ba 100644
Binary files a/goldens/legacy_modernized/60000ms.png and b/goldens/legacy_modernized/60000ms.png differ
diff --git a/goldens/lose/03000ms.png b/goldens/lose/03000ms.png
index 79be502..40dad45 100644
Binary files a/goldens/lose/03000ms.png and b/goldens/lose/03000ms.png differ
diff --git a/goldens/motion.log.bin b/goldens/motion.log.bin
new file mode 100644
index 0000000..65e458a
Binary files /dev/null and b/goldens/motion.log.bin differ
diff --git a/goldens/motion.t1 b/goldens/motion.t1
new file mode 100644
index 0000000..670738e
--- /dev/null
+++ b/goldens/motion.t1
@@ -0,0 +1,67 @@
+# t1 manifest — per-tick FNV-1a-64 state hashes (full sim state)
+t1 1
+demo motion
+seed 42
+logic_hz 20
+catalog_hash 0db1a08de26124e6
+ticks 60
+1 d323813cf1cceb31
+2 1211823371b28812
+3 9309153d7588f6d7
+4 16b76e0cb7d3e338
+5 081e0bf6fdd89d7d
+6 4d3eff25f9473a1e
+7 16c8c7a0ab553273
+8 d01f679208f65f94
+9 0ef6ed0a7b8fbbb9
+10 60391ae8283b575a
+11 ba50411869228ec3
+12 6372097cbd357cb1
+13 f55beb98926b2c86
+14 f245267561acc2db
+15 11cd78f43de2e2e0
+16 13b69a93325e25ad
+17 4cb77b274dbff7e2
+18 0d0c733082d1ac47
+19 06ebd12594e01ecc
+20 4e392981555fbc19
+21 91608a641010970e
+22 9c7d337962566683
+23 c7bb9751e46703c8
+24 6504a57d1e9c3515
+25 1200dbed7dd935ea
+26 82d32b0f9e352a2f
+27 bbe4a54fde0a69b4
+28 0deb43f7c0befb01
+29 c0b2497ccadd5716
+30 8ed3885f743a8cab
+31 df15082c70a53a05
+32 8fb76bfc5dc65f79
+33 7728c4db29509f58
+34 6d5b2f43764fd8fb
+35 418f35198b6b6e12
+36 40c4ebf095de1765
+37 a05af295c39dc374
+38 f14c2c5030e11f17
+39 bf9aa99e439f5c2e
+40 0fa5f853a5969881
+41 ec5a7f69fd3579fa
+42 5111755a701177ca
+43 b282f91ccaf721e2
+44 4dd6d47658b5be12
+45 28fd5dfb049ff69a
+46 b369f2c46d368cda
+47 03fde1f219075822
+48 af68c9ec1008dcb2
+49 a5824b29f0656eb4
+50 ca19c9dd7a02012e
+51 f2e3a08c18b3b24c
+52 4ee59769e791e24a
+53 9711f5a16aa9c564
+54 104beedc9eb27536
+55 70374f6b27fe20cc
+56 b759d5ba8cf43e8a
+57 7b2df4cfac4abd84
+58 efd87cb516bace31
+59 32320b1721e2d8a8
+60 569dfbb7b93b41d3
diff --git a/goldens/node_health/10000ms.png b/goldens/node_health/10000ms.png
index 46cb3b9..285a927 100644
Binary files a/goldens/node_health/10000ms.png and b/goldens/node_health/10000ms.png differ
diff --git a/goldens/node_health/20000ms.png b/goldens/node_health/20000ms.png
index 0705430..40ff2c5 100644
Binary files a/goldens/node_health/20000ms.png and b/goldens/node_health/20000ms.png differ
diff --git a/goldens/pause/65000ms.png b/goldens/pause/65000ms.png
index c5313d7..2908438 100644
Binary files a/goldens/pause/65000ms.png and b/goldens/pause/65000ms.png differ
diff --git a/goldens/pause/80000ms.png b/goldens/pause/80000ms.png
index 5cd6a54..75b2ac0 100644
Binary files a/goldens/pause/80000ms.png and b/goldens/pause/80000ms.png differ
diff --git a/goldens/qos/01000ms.png b/goldens/qos/01000ms.png
index a8d9e3b..b6789d8 100644
Binary files a/goldens/qos/01000ms.png and b/goldens/qos/01000ms.png differ
diff --git a/goldens/qos/65000ms.png b/goldens/qos/65000ms.png
index b3b6895..218d608 100644
Binary files a/goldens/qos/65000ms.png and b/goldens/qos/65000ms.png differ
diff --git a/goldens/qos_auto/01000ms.png b/goldens/qos_auto/01000ms.png
index a8d9e3b..b6789d8 100644
Binary files a/goldens/qos_auto/01000ms.png and b/goldens/qos_auto/01000ms.png differ
diff --git a/goldens/qos_auto/06000ms.png b/goldens/qos_auto/06000ms.png
index 7f3ef99..35e8085 100644
Binary files a/goldens/qos_auto/06000ms.png and b/goldens/qos_auto/06000ms.png differ
diff --git a/goldens/qos_contention/01000ms.png b/goldens/qos_contention/01000ms.png
index f6910a8..34182bd 100644
Binary files a/goldens/qos_contention/01000ms.png and b/goldens/qos_contention/01000ms.png differ
diff --git a/goldens/qos_contention/03000ms.png b/goldens/qos_contention/03000ms.png
index f4a52a9..8b516ad 100644
Binary files a/goldens/qos_contention/03000ms.png and b/goldens/qos_contention/03000ms.png differ
diff --git a/goldens/qos_contention/10000ms.png b/goldens/qos_contention/10000ms.png
index 33613df..8494c5e 100644
Binary files a/goldens/qos_contention/10000ms.png and b/goldens/qos_contention/10000ms.png differ
diff --git a/goldens/qos_emphasis/01000ms.png b/goldens/qos_emphasis/01000ms.png
index a8d9e3b..b6789d8 100644
Binary files a/goldens/qos_emphasis/01000ms.png and b/goldens/qos_emphasis/01000ms.png differ
diff --git a/goldens/qos_emphasis/05000ms.png b/goldens/qos_emphasis/05000ms.png
index 496b20b..b909a12 100644
Binary files a/goldens/qos_emphasis/05000ms.png and b/goldens/qos_emphasis/05000ms.png differ
diff --git a/goldens/qos_emphasis/12000ms.png b/goldens/qos_emphasis/12000ms.png
index 440d466..d47618f 100644
Binary files a/goldens/qos_emphasis/12000ms.png and b/goldens/qos_emphasis/12000ms.png differ
diff --git a/goldens/qos_manual/01000ms.png b/goldens/qos_manual/01000ms.png
index a8d9e3b..b6789d8 100644
Binary files a/goldens/qos_manual/01000ms.png and b/goldens/qos_manual/01000ms.png differ
diff --git a/goldens/qos_manual/06000ms.png b/goldens/qos_manual/06000ms.png
index 43ae5de..2675ed1 100644
Binary files a/goldens/qos_manual/06000ms.png and b/goldens/qos_manual/06000ms.png differ
diff --git a/goldens/sla/01000ms.png b/goldens/sla/01000ms.png
index 344012a..f322d39 100644
Binary files a/goldens/sla/01000ms.png and b/goldens/sla/01000ms.png differ
diff --git a/goldens/sla/04000ms.png b/goldens/sla/04000ms.png
index 30ecb48..0d11b64 100644
Binary files a/goldens/sla/04000ms.png and b/goldens/sla/04000ms.png differ
diff --git a/goldens/sla/10000ms.png b/goldens/sla/10000ms.png
index baaf1d6..584cd1a 100644
Binary files a/goldens/sla/10000ms.png and b/goldens/sla/10000ms.png differ
diff --git a/goldens/surge/119500ms.png b/goldens/surge/119500ms.png
index 50b5466..6b34f18 100644
Binary files a/goldens/surge/119500ms.png and b/goldens/surge/119500ms.png differ
diff --git a/goldens/surge/149000ms.png b/goldens/surge/149000ms.png
index 058d0eb..4b36e90 100644
Binary files a/goldens/surge/149000ms.png and b/goldens/surge/149000ms.png differ
diff --git a/goldens/surge/170000ms.png b/goldens/surge/170000ms.png
index e133476..a3ba80c 100644
Binary files a/goldens/surge/170000ms.png and b/goldens/surge/170000ms.png differ
diff --git a/goldens/surge/30000ms.png b/goldens/surge/30000ms.png
index 723af5c..648a5a7 100644
Binary files a/goldens/surge/30000ms.png and b/goldens/surge/30000ms.png differ
diff --git a/goldens/surge/65000ms.png b/goldens/surge/65000ms.png
index c582ccf..9ada5db 100644
Binary files a/goldens/surge/65000ms.png and b/goldens/surge/65000ms.png differ
diff --git a/goldens/terminal_types/05000ms.png b/goldens/terminal_types/05000ms.png
index 70322b5..d31e8c8 100644
Binary files a/goldens/terminal_types/05000ms.png and b/goldens/terminal_types/05000ms.png differ
diff --git a/goldens/terminal_types/30000ms.png b/goldens/terminal_types/30000ms.png
index 9fa3c53..0288513 100644
Binary files a/goldens/terminal_types/30000ms.png and b/goldens/terminal_types/30000ms.png differ
diff --git a/goldens/warn/01500ms.png b/goldens/warn/01500ms.png
index bb754ef..3303584 100644
Binary files a/goldens/warn/01500ms.png and b/goldens/warn/01500ms.png differ
diff --git a/goldens/warn/45000ms.png b/goldens/warn/45000ms.png
index cda163f..a81bafe 100644
Binary files a/goldens/warn/45000ms.png and b/goldens/warn/45000ms.png differ
diff --git a/goldens/warn/65000ms.png b/goldens/warn/65000ms.png
index c71426b..796278d 100644
Binary files a/goldens/warn/65000ms.png and b/goldens/warn/65000ms.png differ
diff --git a/goldens/win/02300ms.png b/goldens/win/02300ms.png
index b998da9..730b863 100644
Binary files a/goldens/win/02300ms.png and b/goldens/win/02300ms.png differ
diff --git a/harness/goldens.odin b/harness/goldens.odin
index e347add..7e17b01 100644
--- a/harness/goldens.odin
+++ b/harness/goldens.odin
@@ -100,9 +100,9 @@ render_setup :: proc(rc: ^Render_Ctx, cat: ^pp.Catalogs) {
 // non-nil `preview` (the app's Upgrade_Preview) draws the upgrade-preview
 // card below the weather report — the acceptance-2 panel golden (Perkins B1);
 // nil (every pre-R4 capture) draws zero extra pixels.
-capture_frame :: proc(rc: ^Render_Ctx, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^pp.Flow_State, crisis: ^pp.Crisis_State, health: ^pp.Health_State, health_on: bool, tick: u64, era: u8, seed: u64, preview: ^rnd.Upgrade_Preview = nil) -> rl.Image {
+capture_frame :: proc(rc: ^Render_Ctx, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^pp.Flow_State, crisis: ^pp.Crisis_State, health: ^pp.Health_State, health_on: bool, tick: u64, era: u8, seed: u64, preview: ^rnd.Upgrade_Preview = nil, interp_alpha: f32 = 1.0) -> rl.Image {
 	rl.BeginDrawing()
-	rnd.draw_world(&rc.view, topo, bundles, flow, crisis, tick, {}, -1, -1, seed)
+	rnd.draw_world(&rc.view, topo, bundles, flow, crisis, tick, {}, -1, -1, seed, interp_alpha)
 	rnd.draw_forecast_panel(&rc.view, crisis, rc.view.catalogs, era, preview)
 	rnd.draw_health_meter(&rc.view, health, rc.view.catalogs, health_on)
 	banner_y: i32 = 10
diff --git a/harness/main.odin b/harness/main.odin
index 9527f98..5aabf17 100644
--- a/harness/main.odin
+++ b/harness/main.odin
@@ -125,6 +125,38 @@ main :: proc() {
 		pp.catalogs_destroy(&cat)
 		os.exit(int(code))
 	}
+	// 2.1 motion-readability: the sub-tick evidence verb — render a demo's
+	// frames at an arbitrary wall-clock cadence with the LIVE interpolation
+	// alpha (the app's accum/tick_seconds), proving packets glide between
+	// the 20 Hz snapshots (vs the pre-2.1 quantized steps). Usage:
+	//   harness motion-strip <demo> <start_ms> <end_ms> <step_ms> <outdir> [snapshot]
+	// The optional `snapshot` forces alpha=1.0 — the pre-2.1 render, byte-
+	// identical (the golden path's draw); the before/after pair is the PR
+	// evidence. Deterministic: the sim steps on the same tick grid; alpha is
+	// a pure function of the wall ms.
+	if verb == "motion-strip" {
+		if len(rest) < 5 || len(rest) > 6 {
+			usage()
+		}
+		// Perkins r1 N10: only the exact token `snapshot` selects snapshot
+		// mode — a typo'd 6th arg is a usage error, never a silent interp run.
+		if len(rest) == 6 && rest[5] != "snapshot" {
+			usage()
+		}
+		cat: pp.Catalogs
+		if e := load_catalogs(&cat); e != "" {
+			fmt.eprintfln("motion-strip: %s", e)
+			os.exit(2)
+		}
+		rl.SetTraceLogLevel(.ERROR)
+		rl.InitWindow(1280, 720, "pp-motion-strip")
+		rc: Render_Ctx
+		render_setup(&rc, &cat)
+		code := run_motion_strip(rest[0], rest[1], rest[2], rest[3], rest[4], len(rest) == 6 && rest[5] == "snapshot", &cat, &rc)
+		rl.CloseWindow()
+		pp.catalogs_destroy(&cat)
+		os.exit(int(code))
+	}
 	if verb == "stats-check" {
 		if len(rest) != 1 {
 			usage()
@@ -293,7 +325,7 @@ main :: proc() {
 }
 
 usage :: proc() {
-	fmt.eprintln("usage: harness run|save [demo...] [--stats-out <path>] | replay <demo> <log.bin> | drift-check | preview-check | stats-check <demo> | input-parity [save] | palcheck | map-preview <seed> [out.png] | wire-preview [outdir]")
+	fmt.eprintln("usage: harness run|save [demo...] [--stats-out <path>] | replay <demo> <log.bin> | drift-check | preview-check | stats-check <demo> | input-parity [save] | palcheck | map-preview <seed> [out.png] | wire-preview [outdir] | motion-strip <demo> <start_ms> <end_ms> <step_ms> <outdir> [snapshot]")
 	when #config(PP_DEBUG, false) {
 		fmt.eprintln("       PP_DEBUG: overlay-check <demo> <ms>")
 	}
diff --git a/harness/motion_strip.odin b/harness/motion_strip.odin
new file mode 100644
index 0000000..e194b90
--- /dev/null
+++ b/harness/motion_strip.odin
@@ -0,0 +1,208 @@
+package main
+
+// motion_strip.odin — the 2.1 motion-readability evidence verb. Renders a
+// demo's frames at an arbitrary wall-clock cadence WITH the live sub-tick
+// interpolation alpha (the app's accum/tick_seconds ∈ [0,1)) — the before/
+// after proof that packets GLIDE between the 20 Hz snapshots instead of
+// stepping in 50 ms jumps.
+//
+// Usage: harness motion-strip <demo> <start_ms> <end_ms> <step_ms> <outdir> [snapshot]
+//   - exports frames at start_ms, start_ms+step_ms, ... < end_ms
+//   - `snapshot` forces alpha=1.0 — the PRE-2.1 render, byte-identical to
+//     the golden path (the harness's draw_world default) — so the same verb
+//     produces both the "before" (quantized) and "after" (interpolated)
+//     strips from the SAME sim timeline.
+//
+// Interpolation correctness: the sub-tick cache rolls on the SIM TICK
+// (draw_packets' `tick`), so every tick boundary inside the window is
+// rendered INTERNALLY (alpha=0) to prime the cache — only the requested
+// cadence times are exported. A frame at wall time t (tick T = floor(t/50))
+// draws lerp(pos(T-1), pos(T), (t - T*50)/50) — the render-behind glide the
+// app shows. Deterministic: the sim steps on the same tick grid; alpha is a
+// pure function of the wall ms. T1 manifest + replay gate are NOT re-verified
+// here (run_demo does that) — this verb is a RENDER-ONLY evidence tool; it
+// never touches goldens.
+import "core:fmt"
+import "core:os"
+import "core:strconv"
+import "core:strings"
+import rl "vendor:raylib"
+import pp "../core"
+import rnd "../app/render"
+
+run_motion_strip :: proc(
+	demo_name, start_ms_s, end_ms_s, step_ms_s, outdir: string,
+	snapshot: bool,
+	cat: ^pp.Catalogs,
+	rc: ^Render_Ctx,
+) -> int {
+	start_ms, ok_s := strconv.parse_i64(start_ms_s, 10)
+	end_ms, ok_e := strconv.parse_i64(end_ms_s, 10)
+	step_ms, ok_t := strconv.parse_i64(step_ms_s, 10)
+	if !ok_s || !ok_e || !ok_t || start_ms < 0 || end_ms <= start_ms || step_ms <= 0 {
+		fmt.eprintln("motion-strip: need 0 <= start_ms < end_ms and step_ms > 0")
+		return 2
+	}
+
+	text_bytes, rerr := os.read_entire_file_from_path(fmt.tprintf("demos/%s.dem", demo_name), context.temp_allocator)
+	if rerr != nil {
+		fmt.eprintfln("motion-strip: cannot read demos/%s.dem", demo_name)
+		return 2
+	}
+	demo, perr := parse_demo(demo_name, string(text_bytes))
+	if perr != "" {
+		fmt.eprintfln("motion-strip: %s", perr)
+		return 2
+	}
+	defer demo_destroy(&demo)
+
+	// run setup — the SAME pieces run_demo applies (fixture + nodes + spawns
+	// + session + growth + era), so the strip's sim timeline is the blessed
+	// one (the T1 manifest pins it; this verb just renders it).
+	state: pp.Run_State
+	defer pp.run_destroy(&state)
+	pp.run_init(&state, demo.seed, cat.hash, cat.balance.logic_hz)
+	state.era = demo.era
+	cfg := Demo_Replay{
+		name = demo_name,
+		use_fixture = demo.use_fixture,
+		qos_fixture = demo.qos_fixture,
+		growth_on = demo.growth_on,
+		advance_gate_on = demo.advance_gate_on,
+		session = {goal = demo.win_goal, cap_ms = demo.lose_cap_ms, health_on = demo.health_on, surge_win_pct = demo.surge_win_pct},
+	}
+	defer {
+		delete(cfg.nodes)
+		delete(cfg.spawns)
+		delete(cfg.pauses)
+	}
+	for n in demo.nodes { append(&cfg.nodes, n) }
+	for s in demo.spawns { append(&cfg.spawns, s) }
+	for p in demo.pauses { append(&cfg.pauses, p) }
+	if e := demo_apply_setup(&state, &cfg, cat); e != "" {
+		fmt.eprintfln("motion-strip: %s", e)
+		return 2
+	}
+	if e := lower_intents(&state, &demo, cat); e != "" {
+		fmt.eprintfln("motion-strip: %s", e)
+		return 2
+	}
+	// a11y directives are View-only — apply them so the strip renders what
+	// the demo's own goldens render (reduced-motion strips echo the a11y pin).
+	a11y_reset(rc)
+	apply_demo_a11y(rc, &demo)
+
+	hz := cat.balance.logic_hz
+	tick_ms := i64(1000) / i64(hz)
+	mkdir_p(outdir)
+	mode := "interp" if !snapshot else "snapshot"
+
+	// walk the wall clock tick-by-tick (the 5.3 pause schedule included —
+	// paused wall ticks don't step, so a strip inside a pause window renders
+	// the frozen sim snapshot-exact). Every tick boundary in the window is
+	// rendered INTERNALLY (alpha=0 — the cache roll) + the requested cadence
+	// times are exported.
+	sim_tick: u64 = 0
+	ticks := demo_run_ticks(&demo, hz)
+	end_tick := u64(max(0, i64(end_ms) * i64(hz) / 1000))
+	// prime from one tick before the window so the FIRST exported frame has
+	// a rolled cache (the row-roll rule needs tick-1 rendered).
+	prime_from := u64(max(0, i64(start_ms) * i64(hz) / 1000))
+	if prime_from > 1 {
+		prime_from -= 1
+	}
+	frames := 0
+	rnd.packet_interp_reset(&rc.view) // a fresh cache per invocation (belt+braces)
+	for w in u64(1)..=ticks {
+		if w > end_tick {
+			break
+		}
+		win_start := i64(w - 1) * tick_ms
+		win_end := i64(w) * tick_ms
+		if win_start >= end_ms {
+			break
+		}
+		paused := paused_at(cfg.pauses[:], w, hz)
+		if !paused {
+			sim_tick += 1
+			batch := make([dynamic]pp.Command, 0, 4, context.temp_allocator)
+			for cmd in state.action_log {
+				if cmd.apply_tick == sim_tick {
+					append(&batch, cmd)
+				}
+			}
+			pp.step(&state, sim_tick, batch[:], cat)
+		}
+		// internal prime: the tick-boundary render (alpha=0 — the snapshot
+		// just landed; the row rolls to sim_tick so the next frame's glide
+		// has its base). Skipped when the boundary is itself a cadence time
+		// (the cadence pass exports it with the same alpha).
+		if i64(w) >= i64(prime_from) {
+			if (win_start - start_ms) % step_ms != 0 || win_start < start_ms {
+				alpha: f32 = 1.0
+				if !snapshot && !paused {
+					alpha = 0.0
+				}
+				img := capture_frame(rc, &state.topology, &state.bundles, &state.flow, &state.crisis, &state.health,
+					state.health_enabled, sim_tick, state.era, state.seed, nil, alpha)
+				rl.UnloadImage(img) // Perkins r1 N16: every other call site unloads
+			}
+		}
+		// exported cadence times inside this window
+		t := win_start
+		if t < start_ms {
+			t = start_ms
+		}
+		for t < win_end && t < end_ms {
+			if (t - start_ms) % step_ms == 0 {
+				alpha: f32 = 1.0
+				if !snapshot && !paused {
+					// the render-behind glide: base = pos(T-1), target =
+					// pos(T); alpha = the fraction of the tick elapsed
+					alpha = f32(t - win_start) / f32(tick_ms)
+					alpha = min(alpha, 1.0)
+				}
+						if !render_strip_frame(rc, &state, outdir, demo_name, t, sim_tick, alpha, &frames) {
+				// Perkins r1 W5: an export failure is fatal — a strip with missing
+				// frames would silently mislead the displacement measurement
+				fmt.eprintfln("motion-strip: export failed at %dms — aborting", t)
+				return 2
+			}
+			}
+			t += 1
+		}
+		clear(&state.events)
+		free_all(context.temp_allocator)
+	}
+	if frames == 0 {
+		fmt.eprintln("motion-strip: no frames rendered (window outside the demo run?)")
+		return 2
+	}
+	fmt.printf("motion-strip: %s %s %dms..%dms step %dms -> %d frame(s) (%s)\n",
+		demo_name, mode, start_ms, end_ms, step_ms, frames, outdir)
+	return 0
+}
+
+// render_strip_frame — one exported strip frame: capture_frame with the given
+// interp alpha (1.0 = snapshot-exact — the pre-2.1 render). The capture path
+// draws world + forecast + health + banner, exactly like the goldens.
+render_strip_frame :: proc(
+	rc: ^Render_Ctx,
+	state: ^pp.Run_State,
+	outdir, demo_name: string,
+	ms: i64,
+	sim_tick: u64,
+	alpha: f32,
+	frames: ^int,
+) -> bool {
+	img := capture_frame(rc, &state.topology, &state.bundles, &state.flow, &state.crisis, &state.health,
+		state.health_enabled, sim_tick, state.era, state.seed, nil, alpha)
+	defer rl.UnloadImage(img)
+	path := fmt.tprintf("%s/%s-%06dms.png", outdir, demo_name, ms)
+	if !rl.ExportImage(img, strings.clone_to_cstring(path, context.temp_allocator)) {
+		fmt.eprintfln("motion-strip: export failed: %s", path)
+		return false
+	}
+	frames^ += 1
+	return true
+}
diff --git a/tools/measure_packet_motion.py b/tools/measure_packet_motion.py
new file mode 100644
index 0000000..fce22de
--- /dev/null
+++ b/tools/measure_packet_motion.py
@@ -0,0 +1,129 @@
+#!/usr/bin/env python3
+"""measure_packet_motion.py — the 2.1 motion-readability measurement (rule 4):
+frame-to-frame packet displacement at 60 Hz from motion-strip captures.
+
+Usage:
+  python3 tools/measure_packet_motion.py <before_dir> <after_dir> [--xmax 600]
+
+Scans each strip PNG for the EXACT packet body color (90,98,112 = email; the
+canvas-blended trail echoes never match exactly, so the live packet is the
+only exact-color cluster) and prints the per-frame centroid displacement.
+The before/after delta is the PR evidence: before = holds then jumps (~30px
+every 50ms tick); after = continuous glide (~10px every 16.7ms frame).
+
+The xmax guard excludes unrelated exact-color HUD/building pixels right of
+the corridor (the fixture scenes used for the measurement are corridor-only).
+
+Robustness (Perkins r1 W3/W4/W7/W12): a frame with NO live packet (lost
+track — the packet arrived/delivered) prints `lost` instead of a fake hold
+(W7); both mean-jump guards cover empty step lists (W3); the before/after
+dirs must contain the SAME frame names or the tool exits 2 (W4); missing
+dirs and non-PNG entries are reported, not traced back (W12).
+"""
+import os
+import sys
+from PIL import Image
+
+BODY = (90, 98, 112)  # email packet body color (data/packet_types.json)
+
+
+def live_centroid(path: str, tol: int = 0, xmax: int = 600):
+    img = Image.open(path).convert("RGB")
+    px = img.load()
+    xs, ys = [], []
+    for y in range(img.height):
+        for x in range(min(xmax, img.width)):
+            c = px[x, y]
+            if abs(c[0] - BODY[0]) <= tol and abs(c[1] - BODY[1]) <= tol and abs(c[2] - BODY[2]) <= tol:
+                xs.append(x)
+                ys.append(y)
+    if not xs:
+        return None
+    return (sum(xs) / len(xs), sum(ys) / len(ys))
+
+
+def table(d: str, xmax: int) -> list:
+    """Per-frame (name, displacement-px-or-None). None = the packet was not
+    found (lost track — arrived/delivered) — NOT a hold (W7)."""
+    rows = []
+    prev = None
+    for f in sorted(os.listdir(d)):
+        if not f.endswith(".png"):
+            print(f"  note: skipping non-PNG entry {f}", file=sys.stderr)
+            continue
+        c = live_centroid(os.path.join(d, f), xmax=xmax)
+        if prev and c:
+            disp = ((c[0] - prev[0]) ** 2 + (c[1] - prev[1]) ** 2) ** 0.5
+        elif c:
+            disp = 0.0  # the first frame has no predecessor
+        else:
+            disp = None  # lost track — never a hold
+        rows.append((f, disp))
+        if c:
+            prev = c
+    return rows
+
+
+def main() -> int:
+    if len(sys.argv) < 3:
+        print(__doc__)
+        return 2
+    before_dir, after_dir = sys.argv[1], sys.argv[2]
+    xmax = 600
+    if "--xmax" in sys.argv:
+        xmax = int(sys.argv[sys.argv.index("--xmax") + 1])
+
+    for d in (before_dir, after_dir):
+        if not os.path.isdir(d):
+            print(f"error: not a directory: {d}", file=sys.stderr)
+            return 2
+
+    before = table(before_dir, xmax)
+    after = table(after_dir, xmax)
+    b_names = [n for n, _ in before]
+    a_names = [n for n, _ in after]
+    if b_names != a_names:
+        print(
+            f"error: frame-name mismatch — BEFORE has {len(b_names)} frames, "
+            f"AFTER has {len(a_names)}; the strips must come from the SAME "
+            f"cadence/window (run both motion-strip invocations with the same "
+            f"<demo> <start_ms> <end_ms> <step_ms>).",
+            file=sys.stderr,
+        )
+        only_b = sorted(set(b_names) - set(a_names))
+        only_a = sorted(set(a_names) - set(b_names))
+        if only_b:
+            print(f"  only in BEFORE: {only_b[:5]}", file=sys.stderr)
+        if only_a:
+            print(f"  only in AFTER: {only_a[:5]}", file=sys.stderr)
+        return 2
+
+    print("frame | BEFORE (px) | AFTER (px)")
+    for (fb, db), (fa, da) in zip(before, after):
+        b_s = f"{db:6.1f}" if db is not None else "  lost"
+        a_s = f"{da:6.1f}" if da is not None else "  lost"
+        print(f"{fb} | {b_s} | {a_s}")
+    b_holds = sum(1 for _, d in before if d is not None and d < 0.5)
+    a_holds = sum(1 for _, d in after if d is not None and d < 0.5)
+    b_lost = sum(1 for _, d in before if d is None)
+    a_lost = sum(1 for _, d in after if d is None)
+    b_steps = [d for _, d in before if d is not None and d >= 0.5]
+    a_steps = [d for _, d in after if d is not None and d >= 0.5]
+    print(f"\nholds (<0.5px): BEFORE={b_holds}/{len(before)}  AFTER={a_holds}/{len(after)}")
+    print(f"lost track (packet absent): BEFORE={b_lost}  AFTER={a_lost}")
+    # W3: both lists can be empty (all-holds dirs) — guard each mean
+    if b_steps:
+        print(f"mean jump when moving: BEFORE={sum(b_steps)/len(b_steps):.1f}px", end="")
+        if a_steps:
+            print(f"  AFTER={sum(a_steps)/len(a_steps):.1f}px")
+        else:
+            print("  AFTER=no moving frames")
+    elif a_steps:
+        print(f"mean jump when moving: BEFORE=no moving frames  AFTER={sum(a_steps)/len(a_steps):.1f}px")
+    else:
+        print("mean jump when moving: no moving frames in either strip")
+    return 0
+
+
+if __name__ == "__main__":
+    sys.exit(main())

--- SPEC / CONTEXT ---
# packet-plumber-v2-motion-readability

## Task

Packets currently render at 20 Hz quantized positions — NO sub-tick
interpolation (code-verified in app/render/view.odin draw_packets /
core/flow.odin packet_progress_frac: packets only move when the sim
ticks, so on a 60 Hz display they jump in 50 ms steps). The user's
original complaint "packets move too fast to follow" + the visual-read
side: the jumpiness is a view-layer artifact, fixable without touching
sim speed (the pace job owns speed).

1. **Sub-tick interpolation (the core fix)**: view-layer lerp between
   the last two snapshot positions using the render-frame's fractional
   progress — packets glide smoothly between ticks. This is the
   look-book's own promise (motion canon).
2. Optional (verify against captures): short motion trails — 2–4-frame
   fading echo per packet, MM-style "consistent speed" read (MM
   image_01/03/05/07); trail = the packet color at low alpha.
3. Size + glint tuning: packets are r≈8 px at fit; +15% (~9.2 px) with
   the existing glint; verify readability on the dense-core and
   corridor crops.

## Rules (hard)

1. View-layer only (ODN-1: view never writes back to sim state). The
   interpolation reads snapshots; the sim's 20 Hz truth is untouched.
   LOG_VERSION untouched.
2. T2-safe: capture at the pinned sha before/after to prove the motion
   read changed without altering sim behavior (goldens re-bless only if
   a capture tick legitimately moves; document cause).
3. Don't change packet SPEED — that's the parallel pace-tuning job's
   knob. This job is about how motion READS (smoothness, trail, size).
4. Measure: frame-to-frame packet displacement at 60 Hz before (steps)
   vs after (continuous) — PR body shows the delta.

## Acceptance

- Sub-tick interpolation live; packets glide between ticks (motion
  strip captures at 100 ms show continuous progression, no 50 ms jumps).
- Trails/size tuned if they help; no regression on dense-core
  readability.
- Local test suite green; goldens documented.
- pr_review: 1 (Perkins before merge).

## Skills policy

bmad-quick-dev.

## Model policy

deepseek-v4-flash, --thinking max.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-motion-readability
- base: v2
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- parallel-safe with the whole v2 visual wave (view-layer; merge order =
  wave's final re-bless)
- source of truth: kyle-design-directions.md §4 + design-audit.html Q3

Context docs referenced by the spec (kyle-design-directions.md §4, design-audit.html Q3) live under _bmad-output/ in the repo if you need them.

--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "<see YOUR LENS for your assigned value>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Your assigned "source" value is: "codebase"

Output contract:
- Write ONLY your JSON array (nothing else — no prose, no markdown fencing) to this exact file: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-motion-readability/r3/codebase.json
- Use the write tool with that absolute path verbatim. Do not derive or transform the path.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- When the file is written, STOP. Your work is done — reply with a single line: DONE.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
