You are reviewing a code diff. You have read-only access to the repository (the checkout at /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-motion-readability-r4 is exactly the reviewed state) and may verify the diff's claims against the actual codebase using your available tools. You are a review lens: report findings only — never edit, fix, or write any repository file (the ONLY file you may write is your output JSON file named below).

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
diff --git a/.github/workflows/ci.yml b/.github/workflows/ci.yml
index 07b0ec0a..55ce1be4 100644
--- a/.github/workflows/ci.yml
+++ b/.github/workflows/ci.yml
@@ -69,6 +69,13 @@ jobs:
       - name: Core unit tests (the determinism + topology contracts)
         run: odin test core
 
+      # The app/render + app/input + app/audio + harness unit suites (the
+      # motion-readability pins live here: motion_test.odin's 13 interp
+      # pins + trails_active + the activation derivation — Perkins r3 W1:
+      # the local mirror ran them, the workflow didn't).
+      - name: Render/input/audio/harness unit tests (incl. the motion-readability pins)
+        run: mkdir -p bin && odin test app -out:bin/app-test && odin test app/render -out:bin/render-test && odin test app/input -out:bin/input-test && odin test app/audio -out:bin/audio-test && odin test harness -out:bin/harness-test
+
       # Story 1.2: the first runnable app.bin compiles + links (the shipped
       # artifact — GPU raylib; the playable surface).
       - name: Game builds (app.bin compiles + links)
@@ -82,6 +89,13 @@ jobs:
       - name: Golden harness (T1 hashes + T2 software pixels + replay gate)
         run: tools/harness.sh run
 
+      # 2.1 motion-readability ACTIVATION (Perkins r3 B1): the rlsw pixel
+      # assertion — the alpha=0.5 drawn packet is the snapshot midpoint. A
+      # dropped interp_alpha at the call site compiles green and kills the
+      # glide; this gate catches it remotely.
+      - name: Motion-readability activation (rlsw pixel midpoint)
+        run: tools/harness.sh motion-pixel
+
       # 7.1: the palette-presence gate — a mechanical scan that the look-book
       # §2 canon hexes are objectively present in the blessed juice frames
       # (the B1 sprite-crop lesson: pixels lie to vision; exact-color counts
diff --git a/_bmad-output/field-notes/packet-plumber-v2-motion-readability.md b/_bmad-output/field-notes/packet-plumber-v2-motion-readability.md
new file mode 100644
index 00000000..434e3c7b
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
index 00000000..19794d94
--- /dev/null
+++ b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/README.md
@@ -0,0 +1,97 @@
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
+| holds (<0.5px/frame) | 9 of 24 | 1 of 24 |
+| lost track (packet absent — post-arrival) | 12 | 9 |
+| mean jump when moving | 30.6 px | 11.2 px |
+
+(21 = 9 holds + 12 lost; 10 = 1 hold + 9 lost — the hardened tool reports
+lost-track separately from holds, Perkins r3 N12.)
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
+tools/harness.sh run                       # 47 demos green (T1+T2+replay)
+./bin/harness motion-strip motion 2200 2600 17 bin/m60-before snapshot
+./bin/harness motion-strip motion 2200 2600 17 bin/m60-after
+python3 tools/measure_packet_motion.py bin/m60-before bin/m60-after
+./bin/harness motion-strip juice 29800 30800 100 bin/ms-before snapshot
+./bin/harness motion-strip juice 29800 30800 100 bin/ms-after
+```
diff --git a/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/glide-compare-2251.png b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/glide-compare-2251.png
new file mode 100644
index 00000000..a4e49b23
Binary files /dev/null and b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/glide-compare-2251.png differ
diff --git a/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/size-compare-core.png b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/size-compare-core.png
new file mode 100644
index 00000000..786e92a0
Binary files /dev/null and b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/size-compare-core.png differ
diff --git a/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/size-compare-corridor.png b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/size-compare-corridor.png
new file mode 100644
index 00000000..c65bcbc6
Binary files /dev/null and b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/size-compare-corridor.png differ
diff --git a/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/strip-contact-60hz.png b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/strip-contact-60hz.png
new file mode 100644
index 00000000..2f9d6c8e
Binary files /dev/null and b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/strip-contact-60hz.png differ
diff --git a/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/trail-closeup-2234.png b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/trail-closeup-2234.png
new file mode 100644
index 00000000..70fa6edf
Binary files /dev/null and b/_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/trail-closeup-2234.png differ
diff --git a/_bmad-output/pr-bodies/v2-motion-readability.md b/_bmad-output/pr-bodies/v2-motion-readability.md
new file mode 100644
index 00000000..cf9943ce
--- /dev/null
+++ b/_bmad-output/pr-bodies/v2-motion-readability.md
@@ -0,0 +1,153 @@
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
+## Perkins r3 fixes (head 44ebc25 → this push)
+
+**B1 — the interpolation ACTIVATION is now pinned end-to-end:**
+- `interp_alpha_from_accum(running, accum, tick_seconds)` — the ONE
+  derivation (was inline in main.odin; a dropped call-site arg compiles
+  green and kills the glide with every gate passing). The app call site
+  routes through it; the motion-strip verb derives its alpha through the
+  SAME helper (r3 N10: no duplicated derivation to drift).
+- `harness motion-pixel` — a real rlsw render asserting the alpha=0.5
+  drawn packet pixel is the SNAPSHOT MIDPOINT (476.2 → 501.8, alpha05 =
+  489.0 = (476.2+501.8)/2 exactly). Includes the negative control: equal
+  endpoints (a dropped alpha arg) FAIL the gate loudly. New CI gate
+  (local mirror #8 + the GH workflow) — the feature cannot silently die.
+- unit pins: the helper's contract (running clamp + paused snapshot-exact
+  + no div-by-zero) in motion_test.odin.
+
+**B2 — the advisory gate:** activation wiring pinned (B1) + trail-ring
+mechanics pinned (W2) + the pins now run in the REMOTE workflow (W1).
+
+**W1** — .github/workflows/ci.yml now runs `odin test app/render` (and the
+app/input/audio/harness suites) + the motion-pixel gate — the mirror's
+parity claim is real again.
+**W2** — trail ring mechanics pinned: ring order (0=oldest, n-1=newest),
+the snap-frame-no-push rule, drop-oldest shift at capacity, the 0.5px
+move gate, and the `fades[trail_n-1-k]` indexing (newest = strongest).
+**W3** — `interp_continuous` now READS `p.delivered` (delivery snaps —
+the pin tests the predicate, not an incidental anchor mismatch).
+**W4** — motion-strip now verifies every stepped tick against the blessed
+manifest PREFIX (`check_manifest_prefix`) and refuses to emit from a
+divergent timeline (verified: a corrupted manifest stops the verb).
+
+Notes: N1 dead scratch removed · N3 indentation fixed · N4 motion.dem
+comment matches the real window · N6 --xmax valueless → error · N7 ms-arg
+bound · N8 scale<=0 glide-base guard · N9 "pre-interpolation" wording ·
+N11 BODY overridable + selftest · N12 README table uses the hardened
+lost≠hold numbers · N13 demo count 47 · N14 `--selftest` for the measure
+tool.
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
index 42d86741..1674b7ac 100644
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
+		// positions, deterministic. The derivation is the pinned helper
+		// (Perkins r3 B1: interp_alpha is a default param — the activation
+		// must be a pinned call, not inline, or a dropped arg kills the glide
+		// with every gate green).
+		interp_alpha := rnd.interp_alpha_from_accum(app.mode == .Run, app.accum, tick_seconds)
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
index 00000000..00d2f2b1
--- /dev/null
+++ b/app/render/motion_test.odin
@@ -0,0 +1,546 @@
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
+	// frame 1 at tick 44: compute the packet's current snapshot position
+	// the way draw_packets does (the packet is at frac 0.5 along edge 0)
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
+
+// ---------------------------------------------------------------- (f) the
+// ACTIVATION derivation (Perkins r3 B1): interp_alpha_from_accum is the ONE
+// pinned derivation — a dropped call-site arg defaults to 1.0 and kills the
+// glide with every gate green; these pins lock the helper's contract so the
+// app call site can be reviewed against it.
+
+@(test)
+activation_running_clamps_accum_fraction :: proc(t: ^testing.T) {
+	// running: alpha = accum/tick_seconds, clamped to [0,1]
+	testing.expect(t, interp_alpha_from_accum(true, 0.0, 0.05) == 0.0, "accum 0 -> alpha 0 (the glide base)")
+	testing.expect(t, abs(interp_alpha_from_accum(true, 0.025, 0.05) - 0.5) < 1e-6, "half a tick -> alpha 0.5")
+	testing.expect(t, abs(interp_alpha_from_accum(true, 0.05, 0.05) - 1.0) < 1e-6, "a full tick -> alpha 1.0 (the glide target)")
+	// catch-up leftover beyond a tick clamps at 1.0
+	testing.expect(t, interp_alpha_from_accum(true, 0.2, 0.05) == 1.0, "catch-up leftover clamps at 1.0")
+	// negative accum (never happens, but the clamp is total)
+	testing.expect(t, interp_alpha_from_accum(true, -0.01, 0.05) == 0.0, "negative accum clamps at 0.0")
+}
+
+@(test)
+activation_not_running_snapshot_exact :: proc(t: ^testing.T) {
+	// paused / game-over: alpha 1.0 — the frozen sim shows its own positions
+	testing.expect(t, interp_alpha_from_accum(false, 0.0, 0.05) == 1.0, "paused -> snapshot-exact")
+	testing.expect(t, interp_alpha_from_accum(false, 0.025, 0.05) == 1.0, "paused mid-tick -> snapshot-exact")
+	// a zero/negative tick duration is a config error — never divide by zero
+	testing.expect(t, interp_alpha_from_accum(true, 0.025, 0.0) == 1.0, "zero tick_seconds -> snapshot-exact (no div-by-zero)")
+}
+
+// ---------------------------------------------------------------- (g) the
+// TRAIL RING mechanics (Perkins r3 W2): ring order (0=oldest, n-1=newest),
+// the drop-oldest shift when full, the 0.5px move gate, and the fades
+// indexing (newest echo = strongest fade).
+
+// trail_move — drive one packet through packet_interp_pos with a given
+// snapshot position at the next tick, returning the drawn position.
+trail_move :: proc(v: ^View, topo: ^pp.Topology, p: ^pp.Packet, pos: rl.Vector2, tick: u64, alpha: f32) -> rl.Vector2 {
+	drawn, _, _ := packet_interp_pos(v, topo, p, pos, tick, alpha)
+	return drawn
+}
+
+@(test)
+trail_ring_order_and_fill :: proc(t: ^testing.T) {
+	cat: pp.Catalogs
+	motion_test_catalog(&cat, context.temp_allocator)
+	topo: pp.Topology
+	motion_test_network(&topo, &cat, context.temp_allocator)
+	v: View
+	motion_test_view(&v, &cat)
+	defer delete(v.pkt_interp)
+
+	p: pp.Packet
+	motion_test_packet(&p)
+	depart := node_screen(&v, topo.node_pos[0])
+	arrive := node_screen(&v, topo.node_pos[1])
+	// four successive moving snapshots: frac 0.3 → 0.5 → 0.7 → 0.9 (each
+	// >0.5px apart — the move gate passes). The FIRST frame (frac 0.3) is a
+	// SNAP (no row yet) — and a snap does NOT push an echo (no ghost on
+	// spawn/teleport): the ring starts filling from the second frame.
+	fracs := [4]f32{0.3, 0.5, 0.7, 0.9}
+	for i in 0..<4 {
+		pos := rl.Vector2{depart.x + (arrive.x - depart.x) * fracs[i], depart.y + (arrive.y - depart.y) * fracs[i]}
+		trail_move(&v, &topo, &p, pos, u64(50 + i), 1.0)
+		row, ok := v.pkt_interp[p.id]
+		testing.expect(t, ok, "row exists after a move")
+		if !ok { continue }
+		// the ring holds the PREVIOUS frames' drawn positions, oldest at 0;
+		// the snap frame (i=0) does not push, so the ring fills i-1 slots
+		testing.expect(t, row.trail_n == u32(min(i, 3)), "ring fills to capacity 3")
+		if row.trail_n > 0 {
+			// slot 0 = the FIRST pushed position (frac 0.5's frame — the snap
+			// at 0.3 never enters the ring)
+			testing.expect(t, abs(row.trail[0].x - (depart.x + (arrive.x-depart.x)*0.5)) < 0.01,
+				"ring slot 0 = the first pushed (post-snap) position")
+		}
+	}
+	// after 4 moves the ring is full (3 slots): [0.5, 0.7, 0.9] — the snap
+	// frame (0.3) never entered, and the 0.5 entry is the oldest
+	row, ok := v.pkt_interp[p.id]
+	testing.expect(t, ok && row.trail_n == 3, "full ring keeps 3 echoes")
+	testing.expect(t, abs(row.trail[0].x - (depart.x + (arrive.x-depart.x)*0.5)) < 0.01,
+		"oldest echo is the frac-0.5 frame (the snap never entered)")
+	testing.expect(t, abs(row.trail[2].x - (depart.x + (arrive.x-depart.x)*0.9)) < 0.01,
+		"newest echo is the last pushed position (frac 0.9)")
+}
+
+@(test)
+trail_ring_stationary_no_push :: proc(t: ^testing.T) {
+	cat: pp.Catalogs
+	motion_test_catalog(&cat, context.temp_allocator)
+	topo: pp.Topology
+	motion_test_network(&topo, &cat, context.temp_allocator)
+	v: View
+	motion_test_view(&v, &cat)
+	defer delete(v.pkt_interp)
+
+	p: pp.Packet
+	motion_test_packet(&p)
+	depart := node_screen(&v, topo.node_pos[0])
+	arrive := node_screen(&v, topo.node_pos[1])
+	pos := rl.Vector2{depart.x + (arrive.x - depart.x) * 0.5, depart.y + (arrive.y - depart.y) * 0.5}
+	// a moving frame seeds the ring
+	trail_move(&v, &topo, &p, pos, 50, 1.0)
+	// the SAME position again (a queued/stationary dot — within the 0.5px
+	// move gate) must NOT push a duplicate echo
+	trail_move(&v, &topo, &p, pos, 51, 1.0)
+	row, ok := v.pkt_interp[p.id]
+	testing.expect(t, ok && row.trail_n == 1, "stationary dot does not push echoes")
+	// a 1px move DOES push (the gate is >0.5px)
+	pos2 := rl.Vector2{pos.x + 2, pos.y}
+	trail_move(&v, &topo, &p, pos2, 52, 1.0)
+	row, ok = v.pkt_interp[p.id]
+	testing.expect(t, ok && row.trail_n == 2, "a >0.5px move pushes an echo")
+}
+
+@(test)
+trail_fades_newest_strongest :: proc(t: ^testing.T) {
+	// the draw indexes TRAIL_FADES[trail_n-1-k]: the newest echo (highest
+	// k) gets the strongest fade (index 0). Pin the indexing contract so a
+	// reorder can't silently swap the ladder.
+	fades := TRAIL_FADES
+	// the draw indexes fades[trail_n - 1 - k]: k=0 (oldest) → the LAST slot
+	// (weakest), k=n-1 (newest) → slot 0 (strongest). Pin the mapping.
+	for n in u32(1)..=3 {
+		for k in u32(0)..<n {
+			got := fades[n - 1 - k]
+			// the oldest echo (k=0) is the weakest: index n-1
+			if k == 0 {
+				testing.expect(t, got == fades[n-1], "oldest echo gets the weakest fade")
+			}
+			// the newest echo (k=n-1) is the strongest: index 0
+			if k == n - 1 {
+				testing.expect(t, got == fades[0], "newest echo gets the strongest fade")
+			}
+			// monotone: older echoes never exceed newer ones
+			if k > 0 {
+				prev := fades[n - k] // the next-older echo's fade
+				testing.expect(t, got >= prev, "the ladder is monotone (older <= newer)")
+			}
+		}
+	}
+	// the explicit ladder order: strongest → weakest
+	testing.expect(t, TRAIL_FADES[0] > TRAIL_FADES[1] && TRAIL_FADES[1] > TRAIL_FADES[2],
+		"the fade ladder descends (newest strongest)")
+}
diff --git a/app/render/view.odin b/app/render/view.odin
index e29b87f0..41f77a83 100644
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
@@ -88,6 +100,290 @@ Drag_State :: struct {
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
+// interp_alpha_from_accum — the ONE interpolation-activation derivation
+// (Perkins r3 B1: interp_alpha is a default param, so a dropped call-site
+// arg compiles green and kills the glide with every gate passing — the
+// derivation must be a pinned helper, not inline). Given the sim mode
+// (running = .Run) + the accumulator leftover + the tick duration:
+// running → clamp(accum/tick_seconds, 0, 1) — the render frame's
+// fractional progress within the current tick; NOT running (paused /
+// game-over) → 1.0 snapshot-exact (the sim is frozen; the view shows the
+// sim's own positions, deterministic). The motion-strip verb derives its
+// alpha through the SAME helper (N10: one derivation, app + evidence).
+interp_alpha_from_accum :: proc(running: bool, accum, tick_seconds: f64) -> f32 {
+	if !running {
+		return 1.0
+	}
+	if tick_seconds <= 0 {
+		return 1.0
+	}
+	a := f32(accum / tick_seconds)
+	// clamp BOTH ends: a negative accum (never happens — dt is clamped >= 0,
+	// but the clamp is total) must not produce a negative alpha
+	return max(0.0, min(a, 1.0))
+}
+
+interp_continuous :: proc(
+	topo: ^pp.Topology,
+	entry_edge, entry_heading, entry_at_node: u32,
+	entry_on_edge: bool,
+	p: ^pp.Packet,
+) -> bool {
+	// a delivered packet is never drawn (draw_packets skips it BEFORE the
+	// interp) — but the guard must still snap if anything ever routes one
+	// here: delivery is the terminal teleport (Perkins r3 W3: the predicate
+	// must READ the flag for the 'delivery snap' pin to be real).
+	if p.delivered {
+		return false
+	}
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
+	// N8 (Perkins r3): a scale<=0 frame (minimized window) would make
+	// from_screen return (0,0) and poison the glide base — snap without
+	// touching the cache (the next valid frame rolls normally; self-healing
+	// by construction).
+	if v.scale <= 0 {
+		return pos, {}, 0
+	}
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
@@ -133,8 +429,11 @@ node_screen :: proc(v: ^View, pos: [2]i32) -> rl.Vector2 {
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
@@ -146,7 +445,7 @@ draw_world :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^pp
 	}
 	draw_bundles(v, topo, bundles, flow, crisis, paths[:])
 	draw_nodes(v, topo, crisis, tick)
-	draw_packets(v, topo, bundles, flow, focus_class, paths[:])
+	draw_packets(v, topo, bundles, flow, tick, focus_class, interp_alpha, paths[:])
 	// 4.2: the crisis bottleneck outline — the named bundle's member pipes
 	// (pulsing red stroke, on top of the pipes so the highlight reads).
 	draw_crisis_outlines(v, topo, bundles, crisis, tick, paths[:])
@@ -1068,6 +1367,34 @@ draw_tier_ring :: proc(v: ^View, c: rl.Vector2, dst: rl.Rectangle, tier: rl.Colo
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
@@ -1082,7 +1409,14 @@ draw_tier_ring :: proc(v: ^View, c: rl.Vector2, dst: rl.Rectangle, tier: rl.Colo
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
@@ -1224,8 +1558,28 @@ draw_packets :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
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
@@ -1251,39 +1605,44 @@ draw_packets :: proc(v: ^View, topo: ^pp.Topology, bundles: ^pp.Bundles, flow: ^
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
index 00000000..5bb6e053
--- /dev/null
+++ b/demos/motion.dem
@@ -0,0 +1,25 @@
+# motion.dem — 2.1 motion-readability: ONE packet on a long straight pipe,
+# mid-traversal for most of the strip window — the cleanest possible sub-tick
+# interpolation probe (a single dot on a single edge; no cluster ambiguity in
+# the displacement measurement). The 1.2 fixture is residential(0) <-
+# router(1) -> content_host(2), 12 tiles apart on row y=15. Draw source->
+# router then router->sink at the 'standard' tier; spawn one packet at
+# 2050ms. At the post-pace-tuning bandwidth (120) a standard pipe (cap 15)
+# takes 8 ticks/edge = 400 ms: the packet crosses edge0 from ~t42 to ~t50,
+# arrives at the router ~2450ms, and re-forwards toward the sink from there.
+# The strip commands run 2200..2600ms (the PR's 17ms-cadence window): the
+# 2200..~2450ms part is the pure mid-edge glide; the tail (2450ms+) is the
+# post-arrival doorstep phase — the displacement delta (steps vs glide)
+# reads unmixed in the mid-edge part and the arrival is visible as the
+# packet's motion stopping (Perkins r1 W8: the comment previously claimed
+# "no arrivals" — ~10 of 24 AFTER frames are post-arrival by this timeline;
+# Perkins r3 N4: the comment now matches the actual command window).
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
index fcb0e96b..d67e0a6d 100644
Binary files a/goldens/a11y_deutan/30000ms.png and b/goldens/a11y_deutan/30000ms.png differ
diff --git a/goldens/a11y_deutan/65000ms.png b/goldens/a11y_deutan/65000ms.png
index 8b8a8d26..c72794f0 100644
Binary files a/goldens/a11y_deutan/65000ms.png and b/goldens/a11y_deutan/65000ms.png differ
diff --git a/goldens/a11y_protan/30000ms.png b/goldens/a11y_protan/30000ms.png
index fcb0e96b..d67e0a6d 100644
Binary files a/goldens/a11y_protan/30000ms.png and b/goldens/a11y_protan/30000ms.png differ
diff --git a/goldens/a11y_protan/65000ms.png b/goldens/a11y_protan/65000ms.png
index 8b8a8d26..c72794f0 100644
Binary files a/goldens/a11y_protan/65000ms.png and b/goldens/a11y_protan/65000ms.png differ
diff --git a/goldens/a11y_reduced/30000ms.png b/goldens/a11y_reduced/30000ms.png
index 24d95272..6a9d69df 100644
Binary files a/goldens/a11y_reduced/30000ms.png and b/goldens/a11y_reduced/30000ms.png differ
diff --git a/goldens/a11y_reduced/65000ms.png b/goldens/a11y_reduced/65000ms.png
index 04381e91..9640f0ce 100644
Binary files a/goldens/a11y_reduced/65000ms.png and b/goldens/a11y_reduced/65000ms.png differ
diff --git a/goldens/a11y_scale/30000ms.png b/goldens/a11y_scale/30000ms.png
index be2803c4..30d4e771 100644
Binary files a/goldens/a11y_scale/30000ms.png and b/goldens/a11y_scale/30000ms.png differ
diff --git a/goldens/a11y_scale/65000ms.png b/goldens/a11y_scale/65000ms.png
index f9f8d001..03e61c6a 100644
Binary files a/goldens/a11y_scale/65000ms.png and b/goldens/a11y_scale/65000ms.png differ
diff --git a/goldens/a11y_tritan/30000ms.png b/goldens/a11y_tritan/30000ms.png
index 939dfaa4..2c549711 100644
Binary files a/goldens/a11y_tritan/30000ms.png and b/goldens/a11y_tritan/30000ms.png differ
diff --git a/goldens/a11y_tritan/65000ms.png b/goldens/a11y_tritan/65000ms.png
index 967c4990..5c9945c2 100644
Binary files a/goldens/a11y_tritan/65000ms.png and b/goldens/a11y_tritan/65000ms.png differ
diff --git a/goldens/advance_block_legacy/15000ms.png b/goldens/advance_block_legacy/15000ms.png
index c072c143..cf61b3ee 100644
Binary files a/goldens/advance_block_legacy/15000ms.png and b/goldens/advance_block_legacy/15000ms.png differ
diff --git a/goldens/advance_block_legacy/60000ms.png b/goldens/advance_block_legacy/60000ms.png
index ffabceb6..9db37af7 100644
Binary files a/goldens/advance_block_legacy/60000ms.png and b/goldens/advance_block_legacy/60000ms.png differ
diff --git a/goldens/advance_block_sla/15000ms.png b/goldens/advance_block_sla/15000ms.png
index 22fd8be7..27ef0fe5 100644
Binary files a/goldens/advance_block_sla/15000ms.png and b/goldens/advance_block_sla/15000ms.png differ
diff --git a/goldens/advance_block_sla/60000ms.png b/goldens/advance_block_sla/60000ms.png
index 5032bac6..b835ca8c 100644
Binary files a/goldens/advance_block_sla/60000ms.png and b/goldens/advance_block_sla/60000ms.png differ
diff --git a/goldens/advance_fire/15000ms.png b/goldens/advance_fire/15000ms.png
index e99ff441..b8ae3e21 100644
Binary files a/goldens/advance_fire/15000ms.png and b/goldens/advance_fire/15000ms.png differ
diff --git a/goldens/advance_fire/60000ms.png b/goldens/advance_fire/60000ms.png
index b1b54b9e..578985e1 100644
Binary files a/goldens/advance_fire/60000ms.png and b/goldens/advance_fire/60000ms.png differ
diff --git a/goldens/bundle/02850ms.png b/goldens/bundle/02850ms.png
index 35d443da..b4123915 100644
Binary files a/goldens/bundle/02850ms.png and b/goldens/bundle/02850ms.png differ
diff --git a/goldens/demolish/01050ms.png b/goldens/demolish/01050ms.png
index fada3a5f..d363f119 100644
Binary files a/goldens/demolish/01050ms.png and b/goldens/demolish/01050ms.png differ
diff --git a/goldens/demolish/01250ms.png b/goldens/demolish/01250ms.png
index b998da90..730b863f 100644
Binary files a/goldens/demolish/01250ms.png and b/goldens/demolish/01250ms.png differ
diff --git a/goldens/demolish/01300ms.png b/goldens/demolish/01300ms.png
index 3c753570..532e1ad9 100644
Binary files a/goldens/demolish/01300ms.png and b/goldens/demolish/01300ms.png differ
diff --git a/goldens/demolish_bundle/01100ms.png b/goldens/demolish_bundle/01100ms.png
index 568aa300..0db1e265 100644
Binary files a/goldens/demolish_bundle/01100ms.png and b/goldens/demolish_bundle/01100ms.png differ
diff --git a/goldens/demolish_bundle/01500ms.png b/goldens/demolish_bundle/01500ms.png
index 97a70154..97e2ce10 100644
Binary files a/goldens/demolish_bundle/01500ms.png and b/goldens/demolish_bundle/01500ms.png differ
diff --git a/goldens/demolish_node/01250ms.png b/goldens/demolish_node/01250ms.png
index 6196f9c8..1a926370 100644
Binary files a/goldens/demolish_node/01250ms.png and b/goldens/demolish_node/01250ms.png differ
diff --git a/goldens/demolish_node/01450ms.png b/goldens/demolish_node/01450ms.png
index e77c37ab..a9e23aef 100644
Binary files a/goldens/demolish_node/01450ms.png and b/goldens/demolish_node/01450ms.png differ
diff --git a/goldens/ecmp/01250ms.png b/goldens/ecmp/01250ms.png
index 9b01b9dd..e1ba2d08 100644
Binary files a/goldens/ecmp/01250ms.png and b/goldens/ecmp/01250ms.png differ
diff --git a/goldens/ecmp/01350ms.png b/goldens/ecmp/01350ms.png
index 22fcdae5..6969b6b4 100644
Binary files a/goldens/ecmp/01350ms.png and b/goldens/ecmp/01350ms.png differ
diff --git a/goldens/ecmp_cost/01150ms.png b/goldens/ecmp_cost/01150ms.png
index a2414c55..3d7118c1 100644
Binary files a/goldens/ecmp_cost/01150ms.png and b/goldens/ecmp_cost/01150ms.png differ
diff --git a/goldens/ecmp_cost/01450ms.png b/goldens/ecmp_cost/01450ms.png
index 23445e88..fe8dd9ab 100644
Binary files a/goldens/ecmp_cost/01450ms.png and b/goldens/ecmp_cost/01450ms.png differ
diff --git a/goldens/era_advance/10000ms.png b/goldens/era_advance/10000ms.png
index f7421343..ea015ef6 100644
Binary files a/goldens/era_advance/10000ms.png and b/goldens/era_advance/10000ms.png differ
diff --git a/goldens/era_advance/55000ms.png b/goldens/era_advance/55000ms.png
index bb18228e..6c0ce22d 100644
Binary files a/goldens/era_advance/55000ms.png and b/goldens/era_advance/55000ms.png differ
diff --git a/goldens/estate_surge/25000ms.png b/goldens/estate_surge/25000ms.png
index ba53dfb7..f2d6536f 100644
Binary files a/goldens/estate_surge/25000ms.png and b/goldens/estate_surge/25000ms.png differ
diff --git a/goldens/estate_surge/75000ms.png b/goldens/estate_surge/75000ms.png
index 4f86c212..aa5ee15e 100644
Binary files a/goldens/estate_surge/75000ms.png and b/goldens/estate_surge/75000ms.png differ
diff --git a/goldens/flow/02100ms.png b/goldens/flow/02100ms.png
index 73af400e..a938eeeb 100644
Binary files a/goldens/flow/02100ms.png and b/goldens/flow/02100ms.png differ
diff --git a/goldens/flow/02150ms.png b/goldens/flow/02150ms.png
index 1dd3859c..ae478267 100644
Binary files a/goldens/flow/02150ms.png and b/goldens/flow/02150ms.png differ
diff --git a/goldens/flow/02250ms.png b/goldens/flow/02250ms.png
index 216a0a8f..7d1ee2bf 100644
Binary files a/goldens/flow/02250ms.png and b/goldens/flow/02250ms.png differ
diff --git a/goldens/forecast_preview/30000ms.png b/goldens/forecast_preview/30000ms.png
index 9da70eea..37ffa809 100644
Binary files a/goldens/forecast_preview/30000ms.png and b/goldens/forecast_preview/30000ms.png differ
diff --git a/goldens/forecast_preview/31000ms.png b/goldens/forecast_preview/31000ms.png
index 0d7ae9a4..3f9431cb 100644
Binary files a/goldens/forecast_preview/31000ms.png and b/goldens/forecast_preview/31000ms.png differ
diff --git a/goldens/forecast_preview/32000ms.png b/goldens/forecast_preview/32000ms.png
index ab45297e..859a5a09 100644
Binary files a/goldens/forecast_preview/32000ms.png and b/goldens/forecast_preview/32000ms.png differ
diff --git a/goldens/forecast_preview/33000ms.png b/goldens/forecast_preview/33000ms.png
index d0a419d9..46dfcef3 100644
Binary files a/goldens/forecast_preview/33000ms.png and b/goldens/forecast_preview/33000ms.png differ
diff --git a/goldens/forecast_shift/01300ms.png b/goldens/forecast_shift/01300ms.png
index 98aa5eba..2bce2b2c 100644
Binary files a/goldens/forecast_shift/01300ms.png and b/goldens/forecast_shift/01300ms.png differ
diff --git a/goldens/forecast_shift/02800ms.png b/goldens/forecast_shift/02800ms.png
index 78d0bcdd..828b0d16 100644
Binary files a/goldens/forecast_shift/02800ms.png and b/goldens/forecast_shift/02800ms.png differ
diff --git a/goldens/growth/15000ms.png b/goldens/growth/15000ms.png
index 1b408146..c7f33866 100644
Binary files a/goldens/growth/15000ms.png and b/goldens/growth/15000ms.png differ
diff --git a/goldens/growth/45000ms.png b/goldens/growth/45000ms.png
index 0e9ea5ff..3f167b3a 100644
Binary files a/goldens/growth/45000ms.png and b/goldens/growth/45000ms.png differ
diff --git a/goldens/growth/88000ms.png b/goldens/growth/88000ms.png
index 808f8773..9b5e0553 100644
Binary files a/goldens/growth/88000ms.png and b/goldens/growth/88000ms.png differ
diff --git a/goldens/health_lose/05000ms.png b/goldens/health_lose/05000ms.png
index 84fac0fc..9a2a2967 100644
Binary files a/goldens/health_lose/05000ms.png and b/goldens/health_lose/05000ms.png differ
diff --git a/goldens/health_lose/21000ms.png b/goldens/health_lose/21000ms.png
index e0adf09c..54a86f55 100644
Binary files a/goldens/health_lose/21000ms.png and b/goldens/health_lose/21000ms.png differ
diff --git a/goldens/health_lose/23000ms.png b/goldens/health_lose/23000ms.png
index 718f6d0c..07be87a0 100644
Binary files a/goldens/health_lose/23000ms.png and b/goldens/health_lose/23000ms.png differ
diff --git a/goldens/health_win/150500ms.png b/goldens/health_win/150500ms.png
index cf57553f..5afd80d8 100644
Binary files a/goldens/health_win/150500ms.png and b/goldens/health_win/150500ms.png differ
diff --git a/goldens/health_win/30000ms.png b/goldens/health_win/30000ms.png
index fa1d98b3..2f4d3b28 100644
Binary files a/goldens/health_win/30000ms.png and b/goldens/health_win/30000ms.png differ
diff --git a/goldens/health_win/75000ms.png b/goldens/health_win/75000ms.png
index 9670559d..5271e71f 100644
Binary files a/goldens/health_win/75000ms.png and b/goldens/health_win/75000ms.png differ
diff --git a/goldens/juice/30000ms.png b/goldens/juice/30000ms.png
index 24d95272..6a9d69df 100644
Binary files a/goldens/juice/30000ms.png and b/goldens/juice/30000ms.png differ
diff --git a/goldens/juice/65000ms.png b/goldens/juice/65000ms.png
index 4092d3ef..5dba6a99 100644
Binary files a/goldens/juice/65000ms.png and b/goldens/juice/65000ms.png differ
diff --git a/goldens/legacy_decay/15000ms.png b/goldens/legacy_decay/15000ms.png
index e99ff441..b8ae3e21 100644
Binary files a/goldens/legacy_decay/15000ms.png and b/goldens/legacy_decay/15000ms.png differ
diff --git a/goldens/legacy_decay/60000ms.png b/goldens/legacy_decay/60000ms.png
index b1b54b9e..578985e1 100644
Binary files a/goldens/legacy_decay/60000ms.png and b/goldens/legacy_decay/60000ms.png differ
diff --git a/goldens/legacy_modernized/15000ms.png b/goldens/legacy_modernized/15000ms.png
index e99ff441..b8ae3e21 100644
Binary files a/goldens/legacy_modernized/15000ms.png and b/goldens/legacy_modernized/15000ms.png differ
diff --git a/goldens/legacy_modernized/60000ms.png b/goldens/legacy_modernized/60000ms.png
index 250f6699..cb3f3bad 100644
Binary files a/goldens/legacy_modernized/60000ms.png and b/goldens/legacy_modernized/60000ms.png differ
diff --git a/goldens/lose/03000ms.png b/goldens/lose/03000ms.png
index 79be5025..40dad45d 100644
Binary files a/goldens/lose/03000ms.png and b/goldens/lose/03000ms.png differ
diff --git a/goldens/motion.log.bin b/goldens/motion.log.bin
new file mode 100644
index 00000000..65e458a8
Binary files /dev/null and b/goldens/motion.log.bin differ
diff --git a/goldens/motion.t1 b/goldens/motion.t1
new file mode 100644
index 00000000..670738e5
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
index 46cb3b9b..285a927f 100644
Binary files a/goldens/node_health/10000ms.png and b/goldens/node_health/10000ms.png differ
diff --git a/goldens/node_health/20000ms.png b/goldens/node_health/20000ms.png
index 07054309..40ff2c52 100644
Binary files a/goldens/node_health/20000ms.png and b/goldens/node_health/20000ms.png differ
diff --git a/goldens/pause/65000ms.png b/goldens/pause/65000ms.png
index c5313d7c..29084389 100644
Binary files a/goldens/pause/65000ms.png and b/goldens/pause/65000ms.png differ
diff --git a/goldens/pause/80000ms.png b/goldens/pause/80000ms.png
index 5cd6a54b..75b2ac0f 100644
Binary files a/goldens/pause/80000ms.png and b/goldens/pause/80000ms.png differ
diff --git a/goldens/qos/01000ms.png b/goldens/qos/01000ms.png
index a8d9e3bd..b6789d88 100644
Binary files a/goldens/qos/01000ms.png and b/goldens/qos/01000ms.png differ
diff --git a/goldens/qos/65000ms.png b/goldens/qos/65000ms.png
index b3b6895a..218d6080 100644
Binary files a/goldens/qos/65000ms.png and b/goldens/qos/65000ms.png differ
diff --git a/goldens/qos_auto/01000ms.png b/goldens/qos_auto/01000ms.png
index a8d9e3bd..b6789d88 100644
Binary files a/goldens/qos_auto/01000ms.png and b/goldens/qos_auto/01000ms.png differ
diff --git a/goldens/qos_auto/06000ms.png b/goldens/qos_auto/06000ms.png
index 7f3ef99b..35e80852 100644
Binary files a/goldens/qos_auto/06000ms.png and b/goldens/qos_auto/06000ms.png differ
diff --git a/goldens/qos_contention/01000ms.png b/goldens/qos_contention/01000ms.png
index f6910a8e..34182bd3 100644
Binary files a/goldens/qos_contention/01000ms.png and b/goldens/qos_contention/01000ms.png differ
diff --git a/goldens/qos_contention/03000ms.png b/goldens/qos_contention/03000ms.png
index f4a52a91..8b516ada 100644
Binary files a/goldens/qos_contention/03000ms.png and b/goldens/qos_contention/03000ms.png differ
diff --git a/goldens/qos_contention/10000ms.png b/goldens/qos_contention/10000ms.png
index 33613df8..8494c5e8 100644
Binary files a/goldens/qos_contention/10000ms.png and b/goldens/qos_contention/10000ms.png differ
diff --git a/goldens/qos_emphasis/01000ms.png b/goldens/qos_emphasis/01000ms.png
index a8d9e3bd..b6789d88 100644
Binary files a/goldens/qos_emphasis/01000ms.png and b/goldens/qos_emphasis/01000ms.png differ
diff --git a/goldens/qos_emphasis/05000ms.png b/goldens/qos_emphasis/05000ms.png
index 496b20ba..b909a122 100644
Binary files a/goldens/qos_emphasis/05000ms.png and b/goldens/qos_emphasis/05000ms.png differ
diff --git a/goldens/qos_emphasis/12000ms.png b/goldens/qos_emphasis/12000ms.png
index 440d4660..d47618f3 100644
Binary files a/goldens/qos_emphasis/12000ms.png and b/goldens/qos_emphasis/12000ms.png differ
diff --git a/goldens/qos_manual/01000ms.png b/goldens/qos_manual/01000ms.png
index a8d9e3bd..b6789d88 100644
Binary files a/goldens/qos_manual/01000ms.png and b/goldens/qos_manual/01000ms.png differ
diff --git a/goldens/qos_manual/06000ms.png b/goldens/qos_manual/06000ms.png
index 43ae5deb..2675ed19 100644
Binary files a/goldens/qos_manual/06000ms.png and b/goldens/qos_manual/06000ms.png differ
diff --git a/goldens/sla/01000ms.png b/goldens/sla/01000ms.png
index 344012a9..f322d39c 100644
Binary files a/goldens/sla/01000ms.png and b/goldens/sla/01000ms.png differ
diff --git a/goldens/sla/04000ms.png b/goldens/sla/04000ms.png
index 30ecb486..0d11b64b 100644
Binary files a/goldens/sla/04000ms.png and b/goldens/sla/04000ms.png differ
diff --git a/goldens/sla/10000ms.png b/goldens/sla/10000ms.png
index baaf1d60..584cd1a5 100644
Binary files a/goldens/sla/10000ms.png and b/goldens/sla/10000ms.png differ
diff --git a/goldens/surge/119500ms.png b/goldens/surge/119500ms.png
index 50b54660..6b34f186 100644
Binary files a/goldens/surge/119500ms.png and b/goldens/surge/119500ms.png differ
diff --git a/goldens/surge/149000ms.png b/goldens/surge/149000ms.png
index 058d0eb0..4b36e901 100644
Binary files a/goldens/surge/149000ms.png and b/goldens/surge/149000ms.png differ
diff --git a/goldens/surge/170000ms.png b/goldens/surge/170000ms.png
index e1334765..a3ba80c6 100644
Binary files a/goldens/surge/170000ms.png and b/goldens/surge/170000ms.png differ
diff --git a/goldens/surge/30000ms.png b/goldens/surge/30000ms.png
index 723af5c7..648a5a7e 100644
Binary files a/goldens/surge/30000ms.png and b/goldens/surge/30000ms.png differ
diff --git a/goldens/surge/65000ms.png b/goldens/surge/65000ms.png
index c582ccf9..9ada5dba 100644
Binary files a/goldens/surge/65000ms.png and b/goldens/surge/65000ms.png differ
diff --git a/goldens/terminal_types/05000ms.png b/goldens/terminal_types/05000ms.png
index 70322b5b..d31e8c8e 100644
Binary files a/goldens/terminal_types/05000ms.png and b/goldens/terminal_types/05000ms.png differ
diff --git a/goldens/terminal_types/30000ms.png b/goldens/terminal_types/30000ms.png
index 9fa3c53f..02885134 100644
Binary files a/goldens/terminal_types/30000ms.png and b/goldens/terminal_types/30000ms.png differ
diff --git a/goldens/warn/01500ms.png b/goldens/warn/01500ms.png
index bb754ef8..3303584d 100644
Binary files a/goldens/warn/01500ms.png and b/goldens/warn/01500ms.png differ
diff --git a/goldens/warn/45000ms.png b/goldens/warn/45000ms.png
index cda163ff..a81bafea 100644
Binary files a/goldens/warn/45000ms.png and b/goldens/warn/45000ms.png differ
diff --git a/goldens/warn/65000ms.png b/goldens/warn/65000ms.png
index c71426bd..796278d5 100644
Binary files a/goldens/warn/65000ms.png and b/goldens/warn/65000ms.png differ
diff --git a/goldens/win/02300ms.png b/goldens/win/02300ms.png
index b998da90..730b863f 100644
Binary files a/goldens/win/02300ms.png and b/goldens/win/02300ms.png differ
diff --git a/harness/goldens.odin b/harness/goldens.odin
index e347add1..7e17b010 100644
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
index 9527f987..fcf0bdda 100644
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
@@ -193,6 +225,28 @@ main :: proc() {
 			os.exit(int(code))
 		}
 	}
+	// 2.1 ACTIVATION pin (Perkins r3 B1): the rlsw pixel assertion — the
+	// alpha=0.5 drawn packet is the snapshot midpoint. Runs in the local CI
+	// gates + the GH workflow (a dropped interp_alpha at the call site
+	// compiles green and kills the glide; this gate catches it).
+	if verb == "motion-pixel" {
+		if len(rest) != 0 {
+			usage()
+		}
+		cat: pp.Catalogs
+		if e := load_catalogs(&cat); e != "" {
+			fmt.eprintfln("motion-pixel: %s", e)
+			os.exit(2)
+		}
+		rl.SetTraceLogLevel(.ERROR)
+		rl.InitWindow(1280, 720, "pp-motion-pixel")
+		rc: Render_Ctx
+		render_setup(&rc, &cat)
+		code := run_motion_pixel(&cat, &rc)
+		rl.CloseWindow()
+		pp.catalogs_destroy(&cat)
+		os.exit(int(code))
+	}
 	if verb != "run" && verb != "save" {
 		usage()
 	}
@@ -293,7 +347,7 @@ main :: proc() {
 }
 
 usage :: proc() {
-	fmt.eprintln("usage: harness run|save [demo...] [--stats-out <path>] | replay <demo> <log.bin> | drift-check | preview-check | stats-check <demo> | input-parity [save] | palcheck | map-preview <seed> [out.png] | wire-preview [outdir]")
+	fmt.eprintln("usage: harness run|save [demo...] [--stats-out <path>] | replay <demo> <log.bin> | drift-check | preview-check | stats-check <demo> | input-parity [save] | palcheck | map-preview <seed> [out.png] | wire-preview [outdir] | motion-strip <demo> <start_ms> <end_ms> <step_ms> <outdir> [snapshot] | motion-pixel")
 	when #config(PP_DEBUG, false) {
 		fmt.eprintln("       PP_DEBUG: overlay-check <demo> <ms>")
 	}
diff --git a/harness/manifest.odin b/harness/manifest.odin
index ba0aed70..a23d041b 100644
--- a/harness/manifest.odin
+++ b/harness/manifest.odin
@@ -143,3 +143,57 @@ check_manifest :: proc(demo_name: string, demo: ^Demo, catalog_hash: u64, logic_
 	}
 	return ok
 }
+
+// check_manifest_prefix — the motion-strip verb's drift net (Perkins r3 W4):
+// verify the header (version/seed/catalog_hash/logic_hz) + the PREFIX of the
+// blessed manifest against a PARTIAL run's hashes (the strip renders only
+// the window [start,end), so it stepped fewer ticks than the full golden
+// run). Header drift or ANY prefix mismatch fails loudly — the strip refuses
+// to emit from a divergent timeline.
+check_manifest_prefix :: proc(demo_name: string, demo: ^Demo, catalog_hash: u64, logic_hz: i32,
+                              hashes: []u64, fails: ^[dynamic]string) -> bool {
+	path := manifest_path(demo_name)
+	if !os.exists(path) {
+		append(fails, fmt.tprintf("T1: no manifest at %s (bless with `harness save %s`)",
+			path, demo_name))
+		return false
+	}
+	m, okm := read_manifest(path)
+	if !okm {
+		append(fails, "T1: unreadable manifest")
+		return false
+	}
+	ok := true
+	if m.version != 1 {
+		append(fails, fmt.tprintf("T1: manifest version %d (want 1)", m.version))
+		ok = false
+	}
+	if m.seed != demo.seed {
+		append(fails, fmt.tprintf("T1: seed drift — manifest %d vs demo %d", m.seed, demo.seed))
+		ok = false
+	}
+	if m.catalog_hash != catalog_hash {
+		append(fails, fmt.tprintf("T1: catalog drift — manifest %016x vs current %016x (re-bless deliberately)",
+			m.catalog_hash, catalog_hash))
+		ok = false
+	}
+	if m.logic_hz != i64(logic_hz) {
+		append(fails, fmt.tprintf("T1: logic_hz drift — manifest %d vs current %d", m.logic_hz, logic_hz))
+		ok = false
+	}
+	if len(hashes) > len(m.hashes) {
+		append(fails, fmt.tprintf("T1: prefix longer than the golden run (%d > %d)",
+			len(hashes), len(m.hashes)))
+		ok = false
+	} else {
+		for i in 0..<len(hashes) {
+			if hashes[i] != m.hashes[i] {
+				append(fails, fmt.tprintf("T1: STATE DIVERGENCE at tick %d: %016x != golden %016x",
+					i+1, hashes[i], m.hashes[i]))
+				ok = false
+				break
+			}
+		}
+	}
+	return ok
+}
diff --git a/harness/motion_pixel.odin b/harness/motion_pixel.odin
new file mode 100644
index 00000000..8f28d739
--- /dev/null
+++ b/harness/motion_pixel.odin
@@ -0,0 +1,181 @@
+package main
+
+// motion_pixel.odin — the 2.1 ACTIVATION pin (Perkins r3 B1): a real rlsw
+// render asserting the drawn packet pixel at alpha=0.5 is the MIDPOINT of
+// the alpha=0 (glide base — the T-1 snapshot position) and alpha=1 (glide
+// target — the T snapshot position). The golden gates never exercise the
+// interp path (they render snapshot-exact), and the unit pins call
+// packet_interp_pos directly — this verb closes the gap: it drives the REAL
+// capture pipeline (draw_world + rlsw software rasterizer) and asserts
+// pixels on disk, so a dropped interp_alpha at the call site (the B1
+// failure mode: compiles green, kills the glide) is caught here.
+//
+// Usage: harness motion-pixel   (exit 0 = the glide is live; nonzero = B1)
+//
+// Scene: the motion.dem single-packet corridor — one packet mid-edge0 at a
+// known snapshot position. Renders the SAME sim tick at alpha 0 / 0.5 / 1,
+// pixel-scans the packet's centroid, asserts the alpha=0.5 centroid is
+// between the endpoints (exactly half — the world-space lerp is linear).
+import "core:fmt"
+import "core:os"
+import "core:strings"
+import rl "vendor:raylib"
+import pp "../core"
+import rnd "../app/render"
+
+// motion_pixel_body — the email packet body color (data/packet_types.json).
+motion_pixel_body :: [3]u8{90, 98, 112}
+
+// motion_pixel_centroid — the centroid of exact body-color pixels in the
+// rendered frame's corridor band (the trail echoes blend toward the canvas
+// and never match exactly; the live packet is the only exact-color cluster
+// IN THE BAND — the HUD + building sprites have exact-color pixels too, so
+// the scan is bounded to the pipe's y-band [y0, y1), which isolates the
+// packet). Returns (x, y, found).
+motion_pixel_centroid :: proc(img: rl.Image, x0, x1, y0, y1: i32) -> (f32, f32, bool) {
+	px := rl.LoadImageColors(img)
+	defer rl.UnloadImageColors(px)
+	sx: i64 = 0
+	sy: i64 = 0
+	count: i64 = 0
+	for y in y0..<y1 {
+		for x in x0..<x1 {
+			p := px[y * i32(img.width) + x]
+			if abs(i32(p.r) - i32(motion_pixel_body[0])) <= 6 &&
+				abs(i32(p.g) - i32(motion_pixel_body[1])) <= 6 &&
+				abs(i32(p.b) - i32(motion_pixel_body[2])) <= 6 {
+				sx += i64(x)
+				sy += i64(y)
+				count += 1
+			}
+		}
+	}
+	if count == 0 {
+		return 0, 0, false
+	}
+	return f32(sx) / f32(count), f32(sy) / f32(count), true
+}
+
+// motion_pixel_setup — the motion.dem single-packet corridor, settled: the
+// 1.2 fixture residential(0) <- router(1) -> content_host(2) drawn standard,
+// one packet spawned and advanced to the MIDDLE of edge0 (progress_units =
+// 60 of packet_bandwidth 120 → frac 0.5). Deterministic (no growth, no rng).
+motion_pixel_setup :: proc(state: ^pp.Run_State, cat: ^pp.Catalogs) {
+	res, _ := pp.node_type_index(cat, "residential")
+	rt, _ := pp.node_type_index(cat, "router_basic")
+	std, _ := pp.pipe_tier_index(cat, "standard")
+	a := pp.topology_spawn_node(&state.topology, res, {10, 10}, cat)
+	b := pp.topology_spawn_node(&state.topology, rt, {20, 10}, cat)
+	c := pp.topology_spawn_node(&state.topology, res, {30, 10}, cat)
+	pp.topology_apply_edit(&state.topology, pp.Command{kind = pp.Cmd_Draw_Pipe{a = a, b = b, tier = std}}, cat)
+	pp.topology_apply_edit(&state.topology, pp.Command{kind = pp.Cmd_Draw_Pipe{a = b, b = c, tier = std}}, cat)
+	pp.flow_seed_demand(&state.flow, 1, a, c, 0)
+	// tick 1: spawn + forward onto edge0 (progress 0). tick 2: serve 15.
+	// tick 5: progress 60 → frac 0.5 — the MID-EDGE moment the pixel pin
+	// needs (both snapshot positions are on the same straight edge, so the
+	// alpha=0.5 midpoint is exactly the arithmetic center).
+	// the packet state is set DIRECTLY (no sim-timing dependency: the real
+	// catalog's standard pipe serves the full demand in one tick, so stepping
+	// would not give a stable mid-edge moment). At tick 4 the packet sits at
+	// frac 0.375 (progress 45 of 120); at tick 5 it advances to frac 0.5
+	// (progress 60) — the two snapshot positions the lerp must bridge.
+	bw := u32(cat.balance.packet_bandwidth)
+	pp.flow_try_spawn(state, cat, 0, a, c, 4) // the packet's spawn_tick is 4
+	pk := &state.flow.packets[0]
+	pk.on_edge = true
+	pk.edge = 0
+	pk.heading = b
+	pk.at_node = 0
+	pk.progress_units = (bw * 3) / 8 // frac 0.375 at tick 4
+	_ = bw
+}
+
+// run_motion_pixel — render the settled mid-edge moment at alpha 0 / 0.5 / 1
+// and assert the alpha=0.5 centroid is the midpoint. The packet at frac 0.5
+// sits at the exact edge center: alpha=0 draws the T-1 position (frac 0.375),
+// alpha=1 the T position (frac 0.5) — hmm, no: the row rolls per tick, so
+// the alpha=0/1 pair for the SAME tick must share the tick's prev/cur. The
+// verb renders tick 5 with the row primed by tick 4, so:
+//   prev = pos(tick 4) = frac 0.375, cur = pos(tick 5) = frac 0.5
+//   alpha=0 → frac 0.375, alpha=0.5 → frac 0.4375, alpha=1 → frac 0.5
+// The midpoint assertion uses the alpha=0 and alpha=1 centroids (the
+// endpoints of the lerp), independent of the absolute fracs.
+run_motion_pixel :: proc(cat: ^pp.Catalogs, rc: ^Render_Ctx) -> int {
+	state: pp.Run_State
+	defer pp.run_destroy(&state)
+	pp.run_init(&state, 42, cat.hash, cat.balance.logic_hz)
+	motion_pixel_setup(&state, cat)
+	if len(state.flow.packets) != 1 {
+		fmt.eprintfln("motion-pixel: expected 1 packet, got %d", len(state.flow.packets))
+		return 2
+	}
+	p := &state.flow.packets[0]
+	bw := u32(cat.balance.packet_bandwidth)
+	if !p.on_edge || p.progress_units != (bw * 3) / 8 {
+		fmt.eprintfln("motion-pixel: packet not at the mid-edge snapshot (on_edge=%v progress=%d want=%d)",
+			p.on_edge, p.progress_units, (bw*3)/8)
+		return 2
+	}
+	// prime the interp cache: render tick 4 (the row snaps to tick 4 with
+	// prev=cur=pos(4)); then advance the packet to frac 0.5 for tick 5 — the
+	// tick-5 renders below roll the row (prev=pos(4), cur=pos(5)) and the
+	// alpha=0.5 frame must land exactly between the two.
+	rnd.packet_interp_reset(&rc.view)
+	img0 := capture_frame(rc, &state.topology, &state.bundles, &state.flow, &state.crisis, &state.health,
+		state.health_enabled, 4, state.era, state.seed, nil, 0.0)
+	rl.UnloadImage(img0) // the prime is cache-roll only — discarded
+	state.flow.packets[0].progress_units = bw / 2 // frac 0.5 at tick 5
+
+	// the three assertion frames at tick 5. The corridor band: the pipe runs
+	// along world y=10 (screen y ≈ 240 at the fit camera) — scan y 190..300
+	// isolates the packet from the HUD (top ~150px) + buildings.
+	pos := [3][2]f32{}
+	alphas := [3]f32{0.0, 0.5, 1.0}
+
+	for i in 0..<3 {
+		img := capture_frame(rc, &state.topology, &state.bundles, &state.flow, &state.crisis, &state.health,
+			state.health_enabled, 5, state.era, state.seed, nil, alphas[i])
+		cx, cy, ok := motion_pixel_centroid(img, 430, 610, 225, 255)
+		rl.UnloadImage(img)
+		if !ok {
+			fmt.eprintfln("motion-pixel: no packet pixels at alpha=%.1f — the glide is NOT live (B1)", alphas[i])
+			return 2
+		}
+		pos[i] = {cx, cy}
+	}
+	// the midpoint assertion: x(0.5) == (x(0) + x(1)) / 2 within a 2px
+	// rasterization tolerance (the world-space lerp is linear; the circle
+	// rasterizer rounds ±1px). pos[0]=alpha0 (glide base), pos[2]=alpha1
+	// (glide target), pos[1]=alpha05 — the midpoint of the TWO ENDPOINTS.
+	// NEGATIVE CONTROL (the B1 failure mode): a dropped interp_alpha at the
+	// call site defaults to 1.0 → every frame draws the SNAPSHOT position →
+	// all three centroids identical → the midpoint assertion passes vacuously.
+	// The endpoints MUST differ: the alpha=0 base is the T-1 snapshot, the
+	// alpha=1 target is the T snapshot — equal endpoints prove the interp
+	// path never ran (no roll, no lerp).
+	// NEGATIVE CONTROL (the B1 failure mode): a dropped interp_alpha at the
+	// call site defaults to 1.0 → every frame draws the SNAPSHOT position →
+	// all three centroids identical → the midpoint assertion passes vacuously.
+	// The endpoints MUST differ: the alpha=0 base is the T-1 snapshot, the
+	// alpha=1 target is the T snapshot — equal endpoints prove the interp path
+	// never ran (no roll, no lerp). The comparison is the COMBINED distance —
+	// a horizontal glide has identical y at both endpoints, so a per-axis
+	// check would false-fire on the equal axis.
+	endpoint_dist := rl.Vector2Distance(pos[0], pos[2])
+	if endpoint_dist < 1.0 {
+		fmt.eprintln("motion-pixel: alpha0 == alpha1 — the glide never ran (dropped interp_alpha? B1)")
+		return 2
+	}
+	want := (pos[0][0] + pos[2][0]) * 0.5
+	got := pos[1][0]
+	dx := abs(got - want)
+	dy := abs(pos[1][1] - (pos[0][1] + pos[2][1]) * 0.5)
+	fmt.printf("motion-pixel: alpha0=(%.1f,%.1f) alpha1=(%.1f,%.1f) alpha05=(%.1f,%.1f) want=(%.1f,%.1f)\n",
+		pos[0][0], pos[0][1], pos[2][0], pos[2][1], pos[1][0], pos[1][1], want, (pos[0][1]+pos[2][1])*0.5)
+	if dx > 2.0 || dy > 2.0 {
+		fmt.eprintfln("motion-pixel: alpha=0.5 pixel NOT the midpoint (dx=%.1f dy=%.1f) — the glide is broken (B1)", dx, dy)
+		return 2
+	}
+	fmt.println("motion-pixel: PASS — the alpha=0.5 packet pixel is the snapshot midpoint (the glide is live)")
+	return 0
+}
diff --git a/harness/motion_strip.odin b/harness/motion_strip.odin
new file mode 100644
index 00000000..1d4db01c
--- /dev/null
+++ b/harness/motion_strip.odin
@@ -0,0 +1,247 @@
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
+//   - `snapshot` forces alpha=1.0 — the pre-INTERPOLATION render (the
+//     snapshot positions at the capture ms; the +15% packet size applies in
+//     both modes — only the glide differs)
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
+	// N7 (Perkins r3): parse_i64 already rejects overflow (ok=false); the
+	// upper bound keeps absurd-but-parseable values from spinning the loop.
+	max_ms := i64(1 << 31) // ~24 days of sim — far beyond any demo
+	if !ok_s || !ok_e || !ok_t || start_ms < 0 || end_ms <= start_ms || step_ms <= 0 ||
+		end_ms > max_ms {
+		fmt.eprintln("motion-strip: need 0 <= start_ms < end_ms <= 2^31 and step_ms > 0")
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
+	// W4 (Perkins r3): the strip path gets the SAME drift safety net as
+	// run_demo — per-stepped-tick state hashes compared against the blessed
+	// .t1 manifest (the 'T1 pins the timeline' claim made real). The hashes
+	// are collected exactly like run_demo's (events slice before the step,
+	// drained after) and checked at the end; a drift fails the verb LOUDLY
+	// instead of silently rendering a divergent timeline.
+	hashes := make([dynamic]u64, 0, demo_run_ticks(&demo, hz))
+	defer delete(hashes)
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
+			before := len(state.events)
+			batch := make([dynamic]pp.Command, 0, 4, context.temp_allocator)
+			for cmd in state.action_log {
+				if cmd.apply_tick == sim_tick {
+					append(&batch, cmd)
+				}
+			}
+			pp.step(&state, sim_tick, batch[:], cat)
+			// W4: the per-tick hash (the same slice convention as run_demo —
+			// this tick's events only; the buffer is drained after).
+			append(&hashes, pp.state_hash(&state, state.events[before:], cat, context.temp_allocator))
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
+					// pos(T); alpha = the fraction of the tick elapsed — the
+					// SAME derivation the app uses (N10: one pinned helper).
+					alpha = rnd.interp_alpha_from_accum(true, f64(t - win_start), f64(tick_ms))
+				}
+				if !render_strip_frame(rc, &state, outdir, demo_name, t, sim_tick, alpha, &frames) {
+					// Perkins r1 W5: an export failure is fatal — a strip with
+					// missing frames would silently mislead the measurement
+					fmt.eprintfln("motion-strip: export failed at %dms — aborting", t)
+					return 2
+				}
+			}
+			t += 1
+		}
+		clear(&state.events)
+		free_all(context.temp_allocator)
+	}
+	// W4: the drift safety net — every STEPPED tick's hash must match the
+	// blessed manifest's PREFIX (the strip legitimately renders only the
+	// window [start,end), so it steps fewer ticks than the full run; the
+	// stepped prefix is exactly what the golden run produced for those ticks).
+	// A drift means the strip rendered a timeline that diverges from the
+	// golden one — fail loud instead of silently emitting a lying strip.
+	if len(hashes) > 0 {
+		fails: [dynamic]string
+		defer delete(fails)
+		check_manifest_prefix(demo_name, &demo, cat.hash, hz, hashes[:], &fails)
+		if len(fails) > 0 {
+			for m in fails {
+				fmt.eprintfln("motion-strip: T1 drift — %s", m)
+			}
+			fmt.eprintln("motion-strip: refusing to emit a strip from a divergent timeline (re-bless deliberately)")
+			return 2
+		}
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
+// interp alpha (1.0 = snapshot-exact — the pre-INTERPOLATION render; N9:
+// the +15% radius is a separate view change and applies in BOTH modes —
+// only the sub-tick glide differs). The capture path
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
diff --git a/tools/ci-local.sh b/tools/ci-local.sh
index 155b0d59..8a55aaa4 100755
--- a/tools/ci-local.sh
+++ b/tools/ci-local.sh
@@ -59,6 +59,7 @@ GATES=(
   "Sprite/palette presence scan (the look-book §2 palette oracle — 7.1)|tools/harness.sh palcheck"
   "W1 drift-rejection negative test|tools/harness.sh drift-check"
   "Assist preview cross-check (R2a preview == sim routing)|tools/harness.sh preview-check"
+  "Motion-readability activation (rlsw pixel: the alpha=0.5 glide midpoint)|tools/harness.sh motion-pixel"
   "PP_DEBUG overlay builds (compile gate)|odin build app -define:PP_DEBUG=true -out:app-debug.bin && odin build harness -define:PP_DEBUG=true -out:bin/harness-debug"
   "Stats stream replay-identity (live == replay)|tools/harness.sh stats-check pause && tools/harness.sh stats-check qos_contention"
   "Input parity (T1 across inputs — mouse == touch == controller + CLI arg-validation leg)|tools/harness.sh input-parity && [ -x ./bin/harness ] && ! ./bin/harness input-parity bogus >/dev/null 2>&1"
diff --git a/tools/measure_packet_motion.py b/tools/measure_packet_motion.py
new file mode 100644
index 00000000..6ef1422a
--- /dev/null
+++ b/tools/measure_packet_motion.py
@@ -0,0 +1,188 @@
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
+# N11 (Perkins r3): the body color is overridable — a palette change should
+# not require editing the tool. Default = the email packet body color
+# (data/packet_types.json); --body R,G,B or PP_MEASURE_BODY overrides.
+BODY = (90, 98, 112)
+
+
+def parse_body(spec: str):
+    parts = [p.strip() for p in spec.split(",")]
+    if len(parts) != 3:
+        raise ValueError(f"bad --body {spec!r} (want R,G,B)")
+    return tuple(int(p) for p in parts)
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
+def selftest() -> int:
+    """Synthetic-frame self-test (Perkins r3 N14): two frames in one dir with
+    a known 10px packet displacement → the tool must report ~10px."""
+    import tempfile
+    with tempfile.TemporaryDirectory() as d:
+        w = h = 64
+        for x in (10, 20):  # the packet moves 10px between the frames
+            img = Image.new("RGB", (w, h), (233, 222, 195))
+            px = img.load()
+            for dy in range(-2, 3):
+                for dx in range(-2, 3):
+                    px[x + dx, 32 + dy] = BODY
+            img.save(os.path.join(d, f"frame-{x:06d}ms.png"))
+        rows = table(d, 600)
+        if len(rows) != 2:
+            print("selftest FAIL: expected 2 frames", file=sys.stderr)
+            return 1
+        disp = rows[1][1]
+        if disp is None or abs(disp - 10.0) > 0.5:
+            print(f"selftest FAIL: expected ~10px displacement, got {disp}", file=sys.stderr)
+            return 1
+    print("selftest PASS")
+    return 0
+
+
+def main() -> int:
+    if "--selftest" in sys.argv:
+        return selftest()
+    if len(sys.argv) < 3:
+        print(__doc__)
+        return 2
+    before_dir, after_dir = sys.argv[1], sys.argv[2]
+    xmax = 600
+    if "--xmax" in sys.argv:
+        i = sys.argv.index("--xmax")
+        if i + 1 >= len(sys.argv) or sys.argv[i + 1].startswith("--"):
+            print("error: --xmax requires a value (e.g. --xmax 600)", file=sys.stderr)
+            return 2
+        try:
+            xmax = int(sys.argv[i + 1])
+        except ValueError:
+            print(f"error: --xmax value {sys.argv[i+1]!r} is not an integer", file=sys.stderr)
+            return 2
+    body_spec = os.environ.get("PP_MEASURE_BODY")
+    if "--body" in sys.argv:
+        bi = sys.argv.index("--body")
+        if bi + 1 >= len(sys.argv):
+            print("error: --body requires a value (R,G,B)", file=sys.stderr)
+            return 2
+        body_spec = sys.argv[bi + 1]
+    if body_spec:
+        try:
+            global BODY
+            BODY = parse_body(body_spec)
+        except ValueError as e:
+            print(f"error: {e}", file=sys.stderr)
+            return 2
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

--- RE-REVIEW CONTEXT (round 4 = fix-audit of round 3) ---

This is round 4 of a review loop. Round 3 (at parent sha 44ebc25) posted the findings below; the implementing agent then pushed fix commit 8f2ae3b claiming all of them folded. Your job has TWO parts:

PART 1 — FIX AUDIT (do this first): for each prior finding that falls in your lens, re-read the cited code at the current worktree state and classify it `fixed` or `still-present`. Do NOT trust the prior wording or the commit message — re-verify by reading the code and, where you can, by RUNNING the tests. Emit each still-present finding as a finding in your JSON with its title prefixed `[still present since r3]`; emit a genuinely-fixed prior BLOCKER/WARNING as a note titled `[fixed since r3] <short title>` (evidence = the fixing code) ONLY for the two r3 blockers B1/B2 and warnings W1-W4; fixed notes need not be reported.

PART 2 — FRESH PASS: review the whole diff at this sha with your lens as normal. The fix commit 8f2ae3b itself introduced new code (activation helper + render test in app/main.odin/app/render, trail-ring pins, harness/motion_pixel.odin ~181 new lines, harness/manifest.odin ~54 new lines, CI wiring) — delta-introduced blockers are the norm in fix rounds: scrutinize the FIX code at least as hard as the original code.

Prior r3 findings (JSON; fix-audit targets marked B1/B2/W1-W4 in evidence_ref):

{
 "job": "packet-plumber-v2-motion-readability",
 "round": 3,
 "pr": "https://github.com/solarity-services/Packet-Plumber/pull/82",
 "reviewed_sha": "44ebc25182906b5bcb6a7e88bad9c59bc701eec4",
 "head_at_post": "44ebc25182906b5bcb6a7e88bad9c59bc701eec4",
 "reviewers_completed": 7,
 "reviewers_total": 7,
 "failed_layers": [],
 "total_findings": 27,
 "confirmed": 27,
 "rejected": 0,
 "unverifiable": 0,
 "merged_duplicates": 7,
 "unique_findings": 20,
 "fix_audit": {
  "B1_r1_F19_interp_core_zero_coverage": "FIXED \u2014 app/render/motion_test.odin: 13 @(test)s pin interp_continuous's four continuous kinds + spawn/sever/reroute/(delivery-see W3) snaps + row-roll alpha endpoints + tick-gap/anchor-mismatch no-ghost + prune bound/reset + trails_active predicate. `odin test app/render` 28/28 green at the reviewed sha (Perkins-run).",
  "B2_r1_F23_gate_FAIL": "P0 NOW 100% (the interp core is pinned) \u2014 but the recomputed advisory gate still FAILs on the P1 activation-wiring gap (r3 B1 below). The lens-level fix landed; the gate's threshold moves with newly-classified P1s.",
  "W_F8_mean_guard": "FIXED \u2014 both mean lists guarded (W3).",
  "W_F9_zip_truncation": "FIXED \u2014 frame-name mismatch exits 2 (W4).",
  "W_F12_ExportImage_bool": "FIXED \u2014 render_strip_frame returns bool; failure aborts with exit 2 (W5).",
  "W_F17_reduced_motion_untestable": "FIXED \u2014 trails_active extracted as a pure predicate + pinned (test e).",
  "N_F2_lost_as_hold": "FIXED \u2014 disp=None never a hold; lost reported separately (exposed N12: README table predates the hardening).",
  "N_F3_motion_dem_no_arrivals": "FIXED \u2014 comment rewritten with the arrival timeline (residual wording sloppiness = N4).",
  "N_F4_trail2_hardcode": "FIXED \u2014 length-generic shift (trail[len(trail)-1], r1 N9 note in code).",
  "N_F5_sixth_arg_silent": "FIXED \u2014 exact-token `snapshot` guard + usage() (r1 N10 note in code).",
  "N_F7_dead_cat_param": "FIXED \u2014 parameter dropped.",
  "N_F10_dir_validation": "FIXED \u2014 isdir guard + non-PNG reported (W12).",
  "N_F14_shape_duplication": "FIXED \u2014 draw_packet_shape shared proc called from both blocks; 47/47 T2 goldens green proves byte-identity held (briefing flag verified).",
  "N_F16_prime_unload": "FIXED \u2014 prime render UnloadImage'd (r1 N16 note in code).",
  "N_F22_prune_coverage": "FIXED \u2014 test (d) seeds >128 rows, asserts prune keeps live ids + reset empties.",
  "N_F13_ac_100ms_letter": "STILL PRESENT (N5) \u2014 documented substitution stands; AC wording unamended."
 },
 "positive_verifications": [
  "View-layer only (ODN-1) on the TRUE head: `git diff origin/v2..HEAD -- core/` is EMPTY \u2014 zero sim files touched; LOG_VERSION untouched",
  "B1 fix verified by execution: odin test app/render = 28 tests, all successful (13 new motion pins + 15 pre-existing)",
  "Golden harness 47/47 demos green (T1 hashes + T2 software pixels + replay gate) at the reviewed sha \u2014 Perkins-run",
  "46/47 sim-truth byte-identical vs merged v2 (only motion.t1 + motion.log.bin differ); the branch touches no core/ file, so the delta is base-side by construction; catalog_hash itself changed on the base (dfe3e342->0db1a08d), consistently re-hashing all 60 motion.t1 lines \u2014 the re-bless is legitimate",
  "Rule-4 measurement reproduces EXACTLY: mean jump when moving BEFORE=30.6px AFTER=11.2px (fresh strips, Perkins-run at the reviewed sha)",
  "r1 fix-fold claims spot-checked in code: W3/W4/W5/W12 guards, N9/N10/N16 notes all present at the cited sites"
 ],
 "counts": {
  "blocker": 2,
  "warning": 4,
  "note": 14
 },
 "verdict": "NEEDS CHANGES",
 "findings": [
  {
   "source": [
    "tests"
   ],
   "severity": "blocker",
   "category": "coverage-gap",
   "title": "Interpolation ACTIVATION wiring (draw_packets alpha branch + main.odin accum->alpha) has no automated pin \u2014 the feature can silently deactivate with every gate green",
   "location": "app/render/view.odin:1535 + app/main.odin:461-465",
   "detail": "P1: the 13 new pins call packet_interp_pos directly; goldens render alpha=1.0. draw_packets' `interp_alpha: f32 = 1.0` is a DEFAULT PARAM \u2014 dropping the arg at the call site compiles green, kills the glide, and passes every gate. The PR's entire purpose is unpinned liveness.",
   "recommended_fix": "Pin the activation: extract main.odin's alpha computation into a testable helper + unit pin, and add an rlsw-driven render test asserting the drawn pixel position at alpha=0.5 (catches branch/arg removal).",
   "verification": "confirmed",
   "evidence_ref": "B1"
  },
  {
   "source": [
    "tests"
   ],
   "severity": "blocker",
   "category": "coverage-gate",
   "title": "Advisory test gate: FAIL",
   "location": "N/A",
   "detail": "P0 100% (4/4: snapshot-exact default \u2014 47 demos green; +15% size \u2014 38 re-blessed T2s; motion.dem T1; interp core pins). P1 67% (4/6 \u2014 activation wiring + app alpha computation untested). Overall 57% (8/14 \u2014 trail ring, echo draw, tooling at 0%). P1 <80%, overall <80% -> FAIL.",
   "recommended_fix": "Deliver B1's activation pin + W2's trail-ring assertions; wire `odin test app/render` into .github/workflows/ci.yml (W1). P1 -> >=90%, overall -> >=80%: PASS.",
   "verification": "confirmed",
   "evidence_ref": "B2"
  },
  {
   "source": [
    "tests"
   ],
   "severity": "warning",
   "category": "ci-wiring",
   "title": "The new motion pins run only in the LOCAL CI mirror \u2014 the GitHub workflow never executes `odin test app/render`",
   "location": ".github/workflows/ci.yml:69-70",
   "detail": "ci.yml's only unit-test step is `odin test core`; the 13 pins (all 28 render tests) execute via tools/ci-local.sh gate 2 only. Remote green does not enforce them, and ci-local.sh's step-for-step mirror claim is already divergent (pre-existing for hud/wire_path; this PR adds claim-relevant pins to the unenforced side).",
   "recommended_fix": "Add `odin test app/render` (with app/input, app/audio, harness test suites) to ci.yml, or reconcile the mirror claim. Briefing-flagged: verified the tests are NOT dead files \u2014 they run locally and pass.",
   "verification": "confirmed",
   "evidence_ref": "W1"
  },
  {
   "source": [
    "tests"
   ],
   "severity": "warning",
   "category": "coverage-gap",
   "title": "Trail echo ring mechanics have zero automated coverage \u2014 r1 B2's fix prescription explicitly listed 'trail order' and it was not delivered",
   "location": "app/render/view.odin:315-347",
   "detail": "Ring fill order, drop-oldest shift, the 0.5px move gate, echo lag, and fades[trail_n-1-k] indexing never run under any gate (goldens alpha=1.0; motion_test binds the trail returns with `_`). A regression ships silently.",
   "recommended_fix": "Extend motion_test: drive packet_interp_pos across successive frames asserting trail_n growth, ring order (oldest..newest), lag behind the live pos, stationary no-push, and full-ring shift.",
   "verification": "confirmed",
   "evidence_ref": "W2"
  },
  {
   "source": [
    "blind"
   ],
   "severity": "warning",
   "category": "test-integrity",
   "title": "The 'delivery snap' pin doesn't test delivery \u2014 interp_continuous never reads p.delivered; the assertion passes via the anchor mismatch",
   "location": "app/render/motion_test.odin:interp_continuous_delivery_snaps + app/render/view.odin:143-168",
   "detail": "The delivered flag is inert in the predicate; the test passes only because at_node(2) != entry_heading(1). Production is SAFE (draw_packets:1386 `if p.delivered { continue }` skips before interp), but the file-header claim 'every teleport (\u2026delivery) is FALSE' is not what the test pins.",
   "recommended_fix": "Either add `if p.delivered { return false }` to interp_continuous + a test with at_node == heading, or rename the test (e.g. anchor-mismatch-at-node) and drop the delivery claim from the header/README.",
   "verification": "confirmed",
   "evidence_ref": "W3"
  },
  {
   "source": [
    "architecture",
    "codebase"
   ],
   "severity": "warning",
   "category": "duplication",
   "title": "STILL PRESENT since r1, sharpened: motion-strip's third Demo_Replay/driver copy has NO mechanical drift safety net \u2014 the 'T1 manifest pins it' comment is aspirational on this path",
   "location": "harness/motion_strip.odin:59-133",
   "detail": "r1 F15 flagged the copy; the strip path still never hashes (zero state_hash references in motion_strip.odin) \u2014 `harness run` exercises run_demo's driver, not the strip's, so strip-driver drift misleads evidence silently. The comment claims the manifest pins the timeline but nothing verifies it here.",
   "recommended_fix": "Extract a shared demo_replay_of builder + boot/step helper for run_demo/overlay/motion_strip, OR have motion-strip compare pp.state_hash against the blessed .t1 while rendering (cheapest mechanical net).",
   "verification": "confirmed",
   "evidence_ref": "W4"
  },
  {
   "source": [
    "blind",
    "architecture",
    "codebase"
   ],
   "severity": "note",
   "category": "dead-code",
   "title": "Leftover scratch in committed test: unused `pos` binding with a literal 'hmm' comment",
   "location": "app/render/motion_test.odin:241-242",
   "detail": "`pos := node_screen(...) // hmm \u2014 compute the actual position` + `_ = pos` shipped in the new gate-2 file; the real snap computation follows immediately. Reads as unfinished review.",
   "recommended_fix": "Delete both lines.",
   "verification": "confirmed",
   "evidence_ref": "N1"
  },
  {
   "source": [
    "blind",
    "codebase"
   ],
   "severity": "note",
   "category": "comment-vs-code",
   "title": "Trail echoes multiply RGB by the fade factor in addition to alpha \u2014 a darkened color, not the stated 'packet's own body color at low alpha'",
   "location": "app/render/view.odin:1584-1585",
   "detail": "ebody/eout scale r,g,b AND a by fade (fade-squared visibility, ~9% for the 0.30 echo) while the comment and \u00a74 direction say 'packet color at low alpha'. Aesthetic verdict deferred to the k3 re-check (vision caveat); the mechanical mismatch stands.",
   "recommended_fix": "Scale alpha only (spec-literal) \u2014 or fix the comment to state the deliberate double-fade. Verify on Kyle crops at k3.",
   "verification": "confirmed",
   "evidence_ref": "N2"
  },
  {
   "source": [
    "blind",
    "codebase"
   ],
   "severity": "note",
   "category": "code-hygiene",
   "title": "Mangled indentation in motion_strip's r1-W5 export-failure guard \u2014 the if-line sits at the wrong nesting depth",
   "location": "harness/motion_strip.odin:165-171",
   "detail": "`if !render_strip_frame(...)` at six tabs under a four-tab block with misaligned body/closers; braces balance (it compiles) but the cadence-loop scope reads wrong \u2014 looks like an unreviewed hand-merge of the W5 fix.",
   "recommended_fix": "Reindent the guard one level inside the cadence `if`.",
   "verification": "confirmed",
   "evidence_ref": "N3"
  },
  {
   "source": [
    "blind"
   ],
   "severity": "note",
   "category": "docs-consistency",
   "title": "motion.dem header calls 2200..2450 'the strip window' while every reproduce command runs 2200..2600",
   "location": "demos/motion.dem:15-16",
   "detail": "Self-contradictory wording: 'the 2200..2450ms strip window is therefore the pure mid-edge glide; the tail of the window (2450ms+)\u2026' \u2014 the window is 2200..2600; only the glide sub-range ends at 2450. Residual sloppiness from the r1 F3 rewrite.",
   "recommended_fix": "Reword: 'the 2200..2600ms strip window: 2200..2450 is the pure mid-edge glide; 2450+ the post-arrival tail'.",
   "verification": "confirmed",
   "evidence_ref": "N4"
  },
  {
   "source": [
    "blind",
    "edge",
    "security"
   ],
   "severity": "note",
   "category": "input-validation",
   "title": "measure_packet_motion.py: --xmax without a value crashes with a raw IndexError traceback (reproduced)",
   "location": "tools/measure_packet_motion.py:73-74",
   "detail": "`int(sys.argv[sys.argv.index(\"--xmax\") + 1])` \u2014 trailing --xmax raises IndexError (non-numeric: ValueError) despite the documented W3/W4/W7/W12 hardening pass. Perkins reproduced the crash live.",
   "recommended_fix": "Guard arity + int-parse with a clean stderr message, return 2 (or argparse).",
   "verification": "confirmed",
   "evidence_ref": "N6"
  },
  {
   "source": [
    "edge"
   ],
   "severity": "note",
   "category": "boundary",
   "title": "motion-strip ms args have no upper bound \u2014 i64 overflow wraps end_tick/prime_from",
   "location": "harness/motion_strip.odin:41-44,107-110",
   "detail": "Validation bounds only the lower end; end_ms \u2273 4.6e17 makes i64(end_ms)*20 wrap negative -> max(0,..)=0 -> premature 'no frames rendered' exit. Degenerate-input note.",
   "recommended_fix": "Reject ms args above a sane ceiling (end_ms*hz within i64) alongside the range check.",
   "verification": "confirmed",
   "evidence_ref": "N7"
  },
  {
   "source": [
    "edge"
   ],
   "severity": "note",
   "category": "state-pollution",
   "title": "packet_interp_pos persists the from_screen (0,0) fallback when scale <= 0, smearing the next tick's glide base",
   "location": "app/render/view.odin:256-257,374-377",
   "detail": "A zero-size/minimized window during Run (alpha<1) stores cur=(0,0) world; after restore the identity-continuous packet lerps from the map corner for one tick (anchors unchanged -> no snap). Self-heals on the next roll.",
   "recommended_fix": "Skip the cache write when v.scale <= 0 (render snapshot-exact, like alpha=1) so a degraded frame never seeds the glide base.",
   "verification": "confirmed",
   "evidence_ref": "N8"
  },
  {
   "source": [
    "acceptance"
   ],
   "severity": "note",
   "category": "spec-letter-deviation",
   "title": "STILL PRESENT since r1: AC's literal '100 ms' motion-strip evidence is unmet; the documented 60 Hz substitution is used instead",
   "location": "_bmad-output/pr-bodies/v2-motion-readability.md:27-32",
   "detail": "100 ms cadence is tick-aligned (2x50ms) and steps identically before/after \u2014 the specified evidence cannot show the fix; the 17 ms strip + displacement table carries the intent, deviation documented in the PR body. AC wording never amended.",
   "recommended_fix": "Amend the acceptance line to '60 Hz (17 ms cadence) strip captures show continuous progression' or leave as the documented deviation.",
   "verification": "confirmed",
   "evidence_ref": "N5"
  },
  {
   "source": [
    "acceptance"
   ],
   "severity": "note",
   "category": "doc-accuracy",
   "title": "`snapshot` strip mode is claimed 'the PRE-2.1 render' but still applies the +15% packet radius",
   "location": "harness/motion_strip.odin:10-13",
   "detail": "Snapshot strips render at the current sha with PACKET_R_FACTOR \u2014 byte-identical to TODAY'S golden path, not to actual pre-2.1 pixels. Only interpolation is isolated; the centroid displacement measurement is unaffected.",
   "recommended_fix": "Reword to 'the current golden-path snapshot render (includes the +15% size)'; note before-strips differ from true pre-2.1 by packet radius.",
   "verification": "confirmed",
   "evidence_ref": "N9"
  },
  {
   "source": [
    "architecture"
   ],
   "severity": "note",
   "category": "duplication",
   "title": "The interp-alpha derivation exists in two implementations (app accum-based vs strip wall-ms-based) with no shared definition or equivalence pin",
   "location": "app/main.odin:463-465 + harness/motion_strip.odin:164-166",
   "detail": "The evidence verb re-implements the alpha semantic it claims to prove. If the app's convention changes (clamping, render-ahead), strips silently diverge from shipped behavior; motion_test pins packet_interp_pos endpoints, not this derivation.",
   "recommended_fix": "Hoist one interp_alpha_of(elapsed, tick_len) proc into app/render next to packet_interp_pos; call from both sites; pin with a unit test (pairs naturally with B1's fix).",
   "verification": "confirmed",
   "evidence_ref": "N10"
  },
  {
   "source": [
    "architecture"
   ],
   "severity": "note",
   "category": "tooling-single-source",
   "title": "measure_packet_motion.py hardcodes the catalog packet color and exits 0 on total tracking failure \u2014 evidence pipeline can silently go vacuous",
   "location": "tools/measure_packet_motion.py:27,118-125",
   "detail": "BODY restates a catalog value (ODN-5 spirit); a palette change degrades every frame to `lost` while the tool still exits 0 \u2014 the documented reproduce flow yields vacuous evidence without a failure signal.",
   "recommended_fix": "Exit non-zero when zero frames tracked in either strip; read the email color from data/packet_types.json.",
   "verification": "confirmed",
   "evidence_ref": "N11"
  },
  {
   "source": [
    "codebase"
   ],
   "severity": "note",
   "category": "evidence-drift",
   "title": "README's headline metric (21/24, 10/24 holds) cannot be produced by the shipped tool \u2014 arithmetic proof: 21=9+12, 10=1+9",
   "location": "_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/README.md:33",
   "detail": "The r1-hardened tool excludes lost frames from holds; Perkins' fresh run prints holds BEFORE=9/24 AFTER=1/24, lost 12/9 \u2014 the README table predates the hardening (lost counted as holds). Mean-jump headline (30.6->11.2px) reproduces exactly.",
   "recommended_fix": "Regenerate the summary table from the shipped tool (holds + lost reported separately).",
   "verification": "confirmed",
   "evidence_ref": "N12"
  },
  {
   "source": [
    "codebase"
   ],
   "severity": "note",
   "category": "doc-drift",
   "title": "README reproduce block says 46 demos green; this tree has 47 and runs 47",
   "location": "_bmad-output/implementation-artifacts/packet-plumber-v2-motion-readability/README.md:87",
   "detail": "Stale count from before the #80/#81 rebases (v2 gained audio_spawn); a reviewer running the reproduce step sees 47.",
   "recommended_fix": "Update to 47 (or drop the hardcoded count).",
   "verification": "confirmed",
   "evidence_ref": "N13"
  },
  {
   "source": [
    "tests"
   ],
   "severity": "note",
   "category": "coverage-gap",
   "title": "Evidence tooling (motion-strip verb, measure_packet_motion.py) hardened by review but untested",
   "location": "harness/motion_strip.odin:166-169",
   "detail": "P3 dev tooling: the r1 guards (export abort, frames==0, arg validation, mismatch exit 2) are code-only; a regression silently corrupts Rule-4 evidence, not shipped behavior.",
   "recommended_fix": "CLI smoke tests: bad args / mismatched dirs exit 2; a small python unit test for the tool's table + guards.",
   "verification": "confirmed",
   "evidence_ref": "N14"
  }
 ]
}
--- YOUR LENS ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

r4 fix-audit targets in your lane: (W4) the new harness/manifest.odin verification — does it actually bite on divergent timelines, and is it wired where the strip path runs? (r3 N10) the interp-alpha derivation duplication (app accum-based vs strip wall-ms-based) — the fix commit touched both sites; check whether a shared definition emerged or the duplication persists.

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

Your assigned "source" value is: "architecture"

Output contract:
- Write ONLY your JSON array (nothing else — no prose, no markdown fencing) to this exact file: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-motion-readability/r4/architecture.json
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
