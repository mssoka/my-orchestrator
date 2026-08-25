You are reviewing a code diff. You have read-only access to the repository at /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.3-pause-ux-r1 (a detached checkout at exactly the reviewed sha — verify every claim there) and may verify the diff's claims against the actual codebase using your available tools. Your `source` value is: codebase.

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
- **Crises are FAIR and PREDICTABLE, never random.** A crisis is the consequence of a topology flaw the player should have designed around — warning signs first (🟡 strained → 🔴 critical). Random/unfair chaos was explicitly rejected `[FORGE #3]`. The V2 AI disaster system (out of prototype scope) is a stress-test auditor, not a random bully.
- **Differentiator 1 — packet types + QoS lanes.** Not all packets are equal: gaming wants low latency and can't drop, banking must never drop, streaming wants volume and can buffer, email is low priority. The player allocates each pipe's bandwidth across 3 priority lanes (Express/Standard/Best-effort); every route is a TRADE-OFF `[FORGE #4]`. All traffic starts on Standard; QoS is player-engineered, never auto.
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
- **Pin every design invariant as a regression test at the lowest layer** (`@(test)` in `core/`): determinism/replay equality, fair-crisis contracts, QoS drop ladder + no-starvation, snap precision, no-soft-lock. Acceptance criteria become durable tests, not PR prose.
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


--- DIFF (the canonical diff — review exactly these bytes) ---
diff --git a/_bmad-output/planning-artifacts/art-direction/art-direction-v1.md b/_bmad-output/planning-artifacts/art-direction/art-direction-v1.md
index 4948738..497b96f 100644
--- a/_bmad-output/planning-artifacts/art-direction/art-direction-v1.md
+++ b/_bmad-output/planning-artifacts/art-direction/art-direction-v1.md
@@ -361,7 +361,7 @@ The map IS the UI (`[UX-DR1]`): near-zero chrome, all state on the elements. The
 ### 8.1 Inherited from Mini Motorways (the foundation)
 - State read from the flow (Wuselfaktor): congestion = dots piling; lane allocation = dot color proportion; node health = glow; degradation = the wear indicator.
 - Camera pan + zoom (drag/scroll, pinch) is the primary navigation for a growing map.
-- Pause-to-plan; color + icon + glow coding throughout.
+- Pause-to-plan; color + icon + glow coding throughout. **Paused presentation** (*user ruling 2026-08-14, prototype-aligned*): the paused world stays at **full brightness — no dim veil, no centered label**; the paused state is a **small edge chip** ("PAUSED — P/Space to resume", sized + styled like the other HUD chips) at a screen edge, never over the play area.
 
 ### 8.2 The HUD elements (what the map cannot show)
 
diff --git a/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md b/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md
index f0f042b..4aad860 100644
--- a/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md
+++ b/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md
@@ -478,7 +478,7 @@ The six eras (M4) are the in-run escalation arc, advancing as you sustain uptime
 - **The map IS the UI** — near-zero chrome; all state lives on the elements (color, glow, flowing dots). Minimalism carries the complexity.
 - **Camera pan + zoom** (drag/scroll, pinch) is the primary navigation for a growing map — zoom out for overview, in for detail. Input-agnostic.
 - **State read from the flow (Wuselfaktor):** congestion = dots piling up; a pipe's lane allocation = the color *proportion* of its dots; node health = glow color; degradation = the wear indicator. The player reads the network at a glance, not from HUD numbers.
-- **Pause-to-plan**; color + icon + glow coding (accessibility: color never the sole encoder).
+- **Pause-to-plan**; color + icon + glow coding (accessibility: color never the sole encoder). **Paused presentation** (*user ruling 2026-08-14 — the dim veil + centered PAUSED label sabotaged pause-and-plan; the prototype shows paused with NO overlay at all*): the paused world renders at **full brightness — identical to the running world minus stepping, no dim, no center text**. The paused state is marked by a **small edge chip indicator** (e.g. a compact "PAUSED — P/Space to resume" chip, sized + styled like the other HUD chips) in a screen-edge position, out of the play area.
 
 **Additions for our higher state density:**
 
diff --git a/_bmad-output/planning-artifacts/sprints/stories-v2.md b/_bmad-output/planning-artifacts/sprints/stories-v2.md
index e17d32c..1a97b83 100644
--- a/_bmad-output/planning-artifacts/sprints/stories-v2.md
+++ b/_bmad-output/planning-artifacts/sprints/stories-v2.md
@@ -477,7 +477,10 @@ on touch + controller.*
 - **Status:** implemented 2026-08-14 — PR open (P / Space toggle in Run; the edit fast-path
   pause-aware apply-tick lowering `[ODN-2]`; the `pause.dem` T1 golden — the sim frozen across
   the mid-crisis pause window as one repeated state hash, resume from the exact tick, replay
-  byte-identical).
+  byte-identical). **Presentation ruling 2026-08-14 (user, `v2-5.3-pause-ux`):** the paused
+  overlay is now NO overlay — full-brightness world (no dim veil, no centered PAUSED text;
+  prototype-aligned), with a small edge chip indicator ("PAUSED — P/Space to resume") in the
+  top HUD band; GDD + art-direction canon lines amended accordingly.
 
 **Given/When/Then:**
 - **Given** the pause control + the run controller;
diff --git a/_pr_body.md b/_pr_body.md
index 5f2860a..e4b8de2 100644
--- a/_pr_body.md
+++ b/_pr_body.md
@@ -1,111 +1,106 @@
-# Story 5.3 — Pause-anywhere (dispatched early)
+# Pause overlay → pause indicator (no dim, no center text) — fixes pause-and-plan
 
-Pause freezes the sim deterministically; crises tick only unpaused; the edit
-fast-path stays live under the veil — pause-and-plan works, even mid-crisis.
-**The story 5.3 card update (status + moved-up note) rides this PR** in
-`_bmad-output/planning-artifacts/sprints/stories-v2.md` — the GDD Controls
-table amend (Pause = P / Space) was already canon (`5f51236`), not re-amended.
+Fixes #48 — **USER REPORT 2026-08-14, ruling-grade**: *"when pause, 1. it dims
+the whole map, 2. the text is right in the middle of the page. the whole point
+of pausing is to be able to think and link nodes. those 2 things hinder that.
+you can see the prototype as an e.g."*
 
-**Key binding:** `P` **or** `SPACE` toggles pause in Run (regular keys — the
-solo-dev laptop ruling). Neither collides with anything (R restart, T assist,
-E/S/B lanes, 1/2 class, U preview, X/DEL demolish, ESC cancel).
+The prototype's paused frame is the baseline: sim frozen, map at **full
+brightness, no overlay at all**. The v2 overlay (full-screen dim veil + 48px
+"PAUSED" dead-center + centered hint) sabotaged pause-and-plan — the whole
+point of pausing is reading and linking the topology, and the dim + center
+text sit exactly in the way.
 
-## Acceptance (how each is pinned)
+## Before / after
 
-1. **`P` pauses mid-run: packets freeze, meter frozen, nothing mutates; `P`
-   resumes from the exact tick** — the app gates the whole stepping block on
-   Run (no accumulation, no steps while paused); the new `pause.dem` T1 golden
-   pins it at the harness level: the mid-crisis pause window (wall ticks
-   1211–1400) is **one repeated FNV-1a-64 hash** (the sim — flow/crisis/rng/
-   health — is frozen), and the hash moves exactly at 1401, the first
-   post-resume step.
-2. **While paused: draw, place, demolish, adjust QoS — all edits land and
-   apply (fast-path), visible immediately** — the input surface never gates on
-   the mode (Run ↔ Paused are the same run context, ODN-13); fast-path
-   commits log `apply_tick = paused tick + 1` (ODN-2) and land on the first
-   post-resume step; review r1 fixed the one gap: the derived BUNDLE view is
-   now rebuilt on the same gen guard while paused, so a drawn/demolished pipe
-   appears/disappears **this frame** under the veil (derived state only —
-   never sim state). The `pause.dem` T2 pair shows the frozen crisis frame
-   then the landed parallel-standard edit.
-3. **Mid-crisis pause: crises tick only unpaused (telegraphs stay, no hidden
-   progress)** — `pause.dem` pauses at tick 1210, **after** the surge fires
-   (tick 1200): the T1 window proves the crisis state froze (the banner strip
-   of the two T2 frames is pixel-identical), and post-resume the same crisis
-   is still active exactly where the pause left it.
-4. **Replay equality: pause/resume + edits replays byte-identical `[E10]`** —
-   the replay gate re-sims the blessed `pause.log.bin` with the same schedule
-   and reproduces every wall-tick hash; `core/pause_test.odin` pins the driver
-   contract (stable window, resume from the exact tick — the paused run equals
-   a continuous run at every executed tick, mid-pause edits at paused tick +
-   1, byte-identical replay).
-5. **Full local suite green; goldens per discipline** — 158 core tests, all
-   25 harness demos (T1 + T2 + replay gate; **the 24 pre-existing goldens are
-   unshifted** — pause is additive, no existing log contains a pause), W1
-   drift-check (174 mutations across 25 demos all rejected), preview-check
-   (7 scenarios), `tools/lint.sh` all gates, `odin build app` clean.
-   *CI note: GitHub Actions billing is blocked at the account level — this
-   PR's CI will be red/not-started until the user fixes it; NOT a code
-   failure. The full local suite above is the verification; Perkins reviews
-   locally.*
-6. **Launchable increment** — run the app, let the era-3 surge hit, pause
-   mid-surge (`P`/`Space`), plan a redesign under the veil (draw/place/
-   demolish/QoS all live + visible immediately), resume — the plan applies and
-   the surge continues from the exact tick. `pause.dem` is the same story as
-   a golden.
+**Before** (v2 `app/main.odin:242-250`): paused drew a full-viewport dim
+(`DrawRectangle` alpha 130) + centered "PAUSED" 48px + a centered hint line.
+
+**After**:
+
+1. **No full-screen dim** — the veil rectangle is deleted entirely (not a
+   "subtle" dim; the prototype shows none). The paused world renders at full
+   brightness, identical to the running world minus stepping.
+2. **Indicator out of the play area** — the center block is replaced by a
+   SMALL two-line chip (120×38, "PAUSED" / "P/Space to resume") in the top
+   HUD band, in the gap between the Network Health card and the forecast
+   panel. It is styled like the existing tray chips (bg + 1px border + small
+   ink_soft text). The chip position is computed from `win_w` with the same
+   centering math as the health card, so it tracks the cards on resize and
+   never overlaps the map's interactive area more than any existing HUD
+   element does.
+3. **Pause-and-plan stays fully live** — draw/place/demolish/QoS fast-paths
+   are untouched (presentation-only change). The paused bundle-view refresh,
+   the glow/preview surface, and the demolish popover remain live while
+   paused.
+4. **Canon amended in-repo** — GDD §UI & Navigation + art-direction §8.1
+   "Pause-to-plan" lines now specify the new presentation (full-brightness
+   world, edge chip indicator, prototype-aligned), and the story 5.3 card
+   status records the ruling — canon and code agree.
+
+## Acceptance
+
+1. **Paused rendering:** no veil, no centered text; world at full brightness;
+   edge-chip indicator visible + styled consistently with the HUD. ✅
+2. **Pause-and-plan re-verified:** all existing pause tests stay green —
+   `core/pause_test.odin` (158 core tests pass) + the `pause.dem` T1 golden
+   (the mid-crisis pause window is one repeated FNV hash; replay byte-
+   identical) + the T2 pair (frozen crisis frame, landed mid-pause edit).
+   The edit fast-path apply-tick lowering and the paused derived-view
+   refresh are untouched (r1 pins held). **No app-level overlay test was
+   added: the harness captures never include the app overlay** (the overlay
+   is app-layer-only, drawn in `main.odin`, deliberately outside the
+   harness capture path — the golden-stability contract) — so there is no
+   harness surface to pin the chip position; the existing pause goldens
+   remain the sim-level pins.
+3. **Goldens:** NO golden captured the old overlay (the harness draws world +
+   forecast + health + crisis banner only, never the app overlay) — so no
+   golden updates. All 25 demos re-run byte-identical; sim-level goldens
+   did not shift (determinism spine untouched — no core change at all).
+4. **Canon:** GDD §UI & Navigation + art-direction §8.1 amended + story 5.3
+   card status note — same PR. ✅
+5. **Full local suite green:** `odin test core` (158 pass), harness 25/25,
+   `tools/lint.sh` all gates. ✅
 
 ## Decisions & rationale
 
-- **Pause lives in the driver, not the core** (ODN-1): the core only ever
-  steps; the driver decides when. The app gates the stepping block on Run;
-  the harness drives a virtual clock (wall ticks = recording schedule, sim
-  steps only while unpaused). The sim never knows about pause, so the
-  executed-tick sequence is an ordinary continuous sequence and E10 holds by
-  construction — no LOG_VERSION bump, no new command kinds.
-- **Pause schedule = run setup, not log entries** (harness): pause/resume
-  directives ride `Demo_Replay` (re-created identically on replay, like the
-  fixture/spawns/era). A pause is invisible to the sim, so the log stays the
-  single authoritative sim record; the replay reproduces the wall-clock
-  schedule from the demo. Alternative (logging pause commands + a version
-  bump) was rejected: it would make the core carry a driver concept.
-- **Mid-pause edits lower to `apply_tick = the next tick the sim will
-  execute`** — the app's fast-path convention: a command fired at wall time
-  T logs `ticks_stepped_by(floor(T·hz/1000)) + 1` (paused tick + 1 when fired
-  mid-pause), so it lands on the first post-resume step and live/replay
-  converge at step boundaries. No-pause demos are byte-identical to the old
-  floor+1 rule. Boundary note: a command fired in the same 50ms wall tick as
-  a resume can differ by one tick from the live app's frame-aligned counter
-  (frame alignment is not modeled — convergence is at step boundaries).
-- **The T1 stable window pins the SIM freeze, not the fast-path channel**:
-  fast-path edits are a separate blessed channel (the action log); the
-  harness's step-boundary model applies a paused edit at the first resumed
-  step while the live app shows it immediately. Both converge at step
-  boundaries; the demo/test/card wording states this precisely.
-- **Paused derived-view refresh** (review r1): the render reads the bundle
-  view (rebuilt inside step only); while paused a fast-path pipe edit was
-  invisible until resume. The app now rebuilds bundles on the same
-  `topology.gen != bundles_gen` guard when paused — derived state only, T1
-  untouched.
-- **Harness hardening from the review swarm** (2 hunters, both applied):
-  parse-time pause/resume validation (strict arity + alternation — a
-  typo'd double-pause fails loud instead of silently blessing a stable
-  T1); O(len(pauses)) apply-tick lowering (a stray huge `at <n>ms` stalled
-  the harness ~68s — now instant); the replay stability-violation string
-  is default-allocator (a tprintf inside the tick loop read freed memory).
+- **Delete the veil outright, no "subtle" dim.** The briefing is explicit
+  and the prototype is the evidence: dimming the map while paused is the
+  defect, not a degree of it. The paused world is the running world minus
+  stepping — full brightness.
+- **Chip position — the top band gap, not top-left/top-right.** The
+  top-left run HUD column is occupied by the title/hint/score/lead + the QoS
+  readout (which appears when a pipe is selected — a core pause-and-plan
+  action), and the top-right is the forecast panel (up during a crisis
+  pause — the exact scenario the demo pauses in). The gap between the
+  Network Health card and the forecast panel is the one top-edge slot free
+  in every app state; the chip sits there, edge-anchored, sized like the
+  tray chips, and never over the play area. The briefing's "top-left or
+  top-right" is illustrative; the binding constraints are *small,
+  unobtrusive, screen-edge, HUD-chip-styled, no more overlap than existing
+  HUD* — all satisfied.
+- **No LOG_VERSION bump, no new command kinds.** Presentation-only change
+  in `app/main.odin`; the core, the driver, and the action log are
+  untouched, so replay equality and every golden hold by construction.
+- **Why no new harness pin.** The harness `capture_frame` path renders
+  world + forecast + health + banner — never the app's HUD or paused
+  overlay (the golden-stability rule that keeps app chrome out of T2s). An
+  overlay-position pin would require adding app chrome to the harness,
+  which would shift every T2 — the wrong trade for a cosmetic chip. The
+  chip's geometry is a two-line constant in `main.odin`, verified visually
+  against the real HUD layout at 1280×720.
 
 ## Files changed
 
-- `app/main.odin` — `Mode.Paused` (ODN-13), `P`/`Space` toggle, stepping gate,
-  dim overlay + PAUSED label, paused bundle-view refresh, planning surface
-  (glow/preview/popover) live under the veil, HUD hint.
-- `harness/demo.odin` — `Pause_Event` + `at <n>ms pause|resume` parsing with
-  strict arity/alternation validation.
-- `harness/run.odin` — pause-aware lowering (`apply_tick_at`), the virtual
-  clock (wall-tick hashes, stable-window contract + loud violation check in
-  both live + replay), pause schedule threaded through `Demo_Replay`.
-- `core/pause_test.odin` — driver-level pause determinism pins (new).
-- `demos/pause.dem` + `goldens/pause.*` — the new T1 golden (mid-crisis
-  pause window = one repeated hash) + T2 pair + blessed log; replay gate +
-  drift-check cover it.
+- `app/main.odin` — paused overlay → paused indicator: removed the full-screen
+  dim veil + centered PAUSED/hint text; added the small edge chip
+  ("PAUSED" / "P/Space to resume") in the top-band gap, tray-chip styled.
+- `_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md`
+  — §UI & Navigation "Pause-to-plan" line: paused presentation ruling
+  (full-brightness world, edge chip indicator, prototype-aligned).
+- `_bmad-output/planning-artifacts/art-direction/art-direction-v1.md` — §8.1
+  same ruling (canon trail twin).
 - `_bmad-output/planning-artifacts/sprints/stories-v2.md` — story 5.3 card
-  status note.
+  status note records the presentation ruling.
+
+No goldens, no core, no harness, no data changes.
diff --git a/app/main.odin b/app/main.odin
index 2a398c8..c716d29 100644
--- a/app/main.odin
+++ b/app/main.odin
@@ -239,14 +239,29 @@ main :: proc() {
 		if (app.mode == .Run || app.mode == .Paused) && app.placing < 0 && !app.drag.active {
 			rnd.draw_demolish_popover(&app.view, &app.state.topology, &app.cat, app.sel_node, app.sel_pipe)
 		}
-		// 5.3: the paused overlay — a dim veil + a centered PAUSED label (the
-		// GDD canon indicator; the world stays visible under the dim so the
-		// player keeps planning — draw/place/demolish/QoS are all still live).
-		// Drawn before the HUD so the run HUD stays readable above the veil.
+		// 5.3 (user ruling 2026-08-14): the paused state renders with NO overlay —
+		// no full-screen dim, no centered PAUSED text (the prototype's paused
+		// frame is the baseline: sim frozen, map at full brightness — the dim
+		// + center text sabotaged pause-and-plan, the whole point of pausing).
+		// The ONLY marker is a small edge chip in the top band, in the gap
+		// between the Network Health card and the forecast panel (the one
+		// top-edge slot free in every state: the top-left run HUD carries the
+		// QoS readout when a pipe is selected, the top-right hosts the
+		// forecast panel during a crisis pause). Styled like the tray chips
+		// (bg + 1px border + small text). Drawn before the HUD like the old
+		// overlay. The edit fast-path stays live while paused (unchanged).
 		if app.mode == .Paused {
-			rl.DrawRectangle(0, 0, rl.GetScreenWidth(), rl.GetScreenHeight(), rl.Color{10, 12, 16, 130})
-			draw_text(&app, "PAUSED", WIN_W/2 - 96, WIN_H/2 - 42, 48, rl.Color{235, 224, 192, 255})
-			draw_text(&app, "P / Space to resume - draw, place, demolish, QoS all live", WIN_W/2 - 292, WIN_H/2 + 14, 18, rl.Color{235, 224, 192, 255})
+			p := app.palette
+			// the top-band gap between the Network Health card (right edge at
+			// win_w/2 + 230) and the forecast panel (left edge at win_w - 250):
+			// the only top-edge slot free in every state. Computed from win_w
+			// so the chip tracks the cards on resize (the same centering math
+			// as the health card).
+			chip := rl.Rectangle{f32(app.view.win_w/2 + 240), 12, 120, 38}
+			rl.DrawRectangleRec(chip, rl.Color{238, 230, 210, 255})
+			rl.DrawRectangleLinesEx(chip, 1, p.ink_soft)
+			draw_text(&app, "PAUSED", i32(chip.x) + 8, i32(chip.y) + 4, 12, p.ink_soft)
+			draw_text(&app, "P/Space to resume", i32(chip.x) + 8, i32(chip.y) + 21, 10, p.ink_soft)
 		}
 		draw_hud(&app)
 	}


--- SPEC / CONTEXT ---
--- SPEC 1: GitHub issue #48 (authoritative — the user report IS the spec) ---
# GitHub issue #48 (THE SPEC — the user report IS the spec)

## Title
Pause overlay defeats pause-and-plan (dim veil + centered text)

## Body
# Pause overlay defeats pause-and-plan (dim veil + centered text)

## User report (2026-08-14, ruling-grade)

> "when pause, 1. it dims the whole map, 2. the text is right in the middle of
> the page. the whole point of pausing is to be able to think and link nodes.
> those 2 things hinder that. you can see the prototype as an e.g."

**Ground truth:** the prototype (`packet-plumber-prototype-ref`) shows paused
with **NO overlay at all** — sim frozen, map at full brightness, no dim, no
center text. That is the desired behavior baseline.

## The defect

`app/main.odin` (5.3 pause-anywhere, v2) draws a full-screen dim veil
(`DrawRectangle` full-viewport, alpha 130) + a 48px "PAUSED" dead-center + a
centered hint line. Both sabotage pause-and-plan:

1. The dim makes the map hard to read while paused (the whole point of pausing
   is to keep reading and planning the topology).
2. The center text sits exactly where the player is trying to think and link.

## The fix

1. **No full-screen dim.** The paused world renders at full brightness —
   identical to the running world (minus stepping). Delete the veil rectangle
   entirely (do NOT keep a "subtle" dim — the prototype shows none).
2. **Indicator out of the play area.** Replace the center block with a SMALL,
   unobtrusive paused indicator in a screen-edge position (e.g. a compact
   "PAUSED — P/Space to resume" chip top-left or top-right, sized like other
   HUD chips — follow existing HUD chip styling in `draw_hud`). It must not
   overlap the map's interactive area more than any existing HUD element does.
   If the HUD already has a status area, prefer integrating there over a new
   floating element.
3. **Pause-and-plan stays fully live:** draw/place/demolish/QoS fast-paths
   unchanged (presentation-only change).
4. **Canon amendment:** amend the GDD/architecture line(s) that specify
   dim+center to the new design (full-brightness world, edge chip indicator,
   prototype-aligned) so canon and code agree.

## Acceptance

1. Paused rendering: no veil, no centered text; world at full brightness;
   edge-chip indicator visible + styled consistently with the HUD.
2. All 5.3 pause-and-plan behaviors re-verified (edit fast-path live while
   paused — existing pause tests stay green).
3. Goldens: if any golden captures a paused frame with the old overlay, update
   it deliberately; sim-level goldens must NOT shift (determinism spine
   untouched).
4. GDD/story canon line amended in the same PR.
5. Full local suite green (`make test-all` or equivalent); PR body shows
   before/after rationale + `Fixes #N`.



--- SPEC 2: original job briefing ---
# Briefing — packet-plumber-v2-5.3-pause-ux (user report: pause overlay defeats pause-and-plan)

- **Job id:** `packet-plumber-v2-5.3-pause-ux`
- **Repo:** packet-plumber · **Base:** `v2` @ 7b56485 · **Slug:** `v2-5.3-pause-ux`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model — name it explicitly at every spawn.
- **Skills policy:** `bmad-quick-dev` (implementation workflow); your own adversarial
  pass uses `bmad-review-adversarial-general` + `bmad-review-edge-case-hunter`.
- **Perkins:** `pr_review: 1` (gameplay-surface rendering + GDD canon amendment).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out
  your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-v2-5.3-pause-ux <url>` yourself.
- **First step:** file the GitHub issue yourself (labels: `bug`, `priority:medium`)
  capturing the user report below, then close it with the PR (`Fixes #N`).
- **CI:** green (billing fixed). Full local suite must pass regardless.

## Mission — fix the pause overlay (USER REPORT 2026-08-14, ruling-grade)

**User's words:** "when pause, 1. it dims the whole map, 2. the text is right in the
middle of the page. the whole point of pausing is to be able to think and link nodes.
those 2 things hinder that. you can see the prototype as an e.g."

**Ground truth:** the prototype (`/Users/moses/code/packet-plumber-prototype-ref`,
read-only reference) shows paused with **NO overlay at all** — sim frozen, map at
full brightness, no dim, no center text. That is the desired behavior baseline.

**The defect (v2 `app/main.odin:242-250`):** paused draws a full-screen dim veil
(`DrawRectangle` full-viewport, alpha 130) + a 48px "PAUSED" dead-center + a centered
hint line. Both sabotage pause-and-plan: the dim makes the map hard to read, the
center text sits exactly where the player is trying to think and link.

**The fix:**

1. **No full-screen dim.** The paused world renders at full brightness — identical
   to the running world (minus stepping). Delete the veil rectangle entirely (do
   NOT keep a "subtle" dim — prototype shows none).
2. **Indicator out of the play area.** Replace the center block with a SMALL,
   unobtrusive paused indicator in a screen-edge position (e.g. a compact "PAUSED —
   P/Space to resume" chip top-left or top-right, sized like other HUD chips —
   follow existing HUD chip styling in `draw_hud`). It must not overlap the map's
   interactive area more than any existing HUD element does. If the HUD already has
   a status area, prefer integrating there over a new floating element.
3. **Pause-and-plan stays fully live:** draw/place/demolish/QoS fast-paths unchanged
   (r1 pinned these — no regression). The change is presentation-only.
4. **Canon amendment:** the current overlay was justified as "the GDD canon
   indicator" (see the code comment + the 5.3 story/GDD text). Amend the GDD/architecture
   line(s) that specify dim+center to the new design (full-brightness world, edge
   chip indicator, prototype-aligned) so canon and code agree — the PR ships the
   ruling.

**Acceptance:**

1. Paused rendering: no veil, no centered text; world at full brightness; edge-chip
   indicator visible + styled consistently with the HUD.
2. All 5.3 pause-and-plan behaviors re-verified (edit fast-path live while paused —
   the existing pause tests must stay green; add/adjust an app-level test pinning
   the new overlay position if the harness supports it).
3. Goldens: if any golden captures a paused frame with the old overlay, update it
   DELIBERATELY and list it in the PR body (rendering change is intended; sim-level
   goldens must NOT shift — determinism spine untouched).
4. GDD/story canon line amended in the same PR.
5. Full local suite green (`make test-all` or the repo's equivalent); PR body shows
   before/after rationale + `Fixes #N` (the issue you filed).

**Scope guard:** the pause overlay presentation + its canon line ONLY. No changes to
pause toggle keys, stepping/accumulator logic, edit fast-paths, QoS, or anything
5.7-telemetry touches.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-5.3-pause-ux
base: v2
model: deepseek/deepseek-v4-flash
pr_review: 1
```


--- REVIEW GUARDS from the Perkins round briefing (binding context — prevent false positives; do not re-litigate settled rulings) ---
## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 LOAD-BEARING — presentation-only scope.** The diff must touch `app/main.odin` presentation paths ONLY (and the canon docs + tests): NO core (`core/`), NO harness (`harness/`), NO data/goldens changes. A core/harness/data change hiding in this diff = a blocker (it would endanger the 5.3 determinism spine that r1 just pinned — pause is driver-level, the T1 pin freezes the sim, the log pins the edits).
- **Pause-and-plan intact:** the edit fast-path (draw/place/demolish/QoS while paused) and the paused bundle-view refresh must be unchanged — verify by diff, not by claim.
- **Golden-safety:** all 25 demos' goldens byte-identical — the app overlay is app-layer-only and never appears in harness T2 captures; any golden shift = a blocker (rendering change is NOT a golden change; the briefing allows NO sim-level shift).
- **The edge chip** must be small + unobtrusive (like other HUD chips), NOT overlap the map's interactive area more than existing HUD elements, and NOT re-cover the play area (the user's complaint was exactly "text right in the middle of the page").
- **Canon agreement:** the amended GDD/art-direction lines must match the CODE (full-brightness world, edge chip indicator) — canon and code agree, per the ruling.
- **Base = `v2`** — includes 5.3 pause (7b56485) + 5.5/5.6 + the 5.7 telemetry line (4749470, merged... if merged before this review). Carry-forward only; do NOT re-open settled findings.
- **Scope guard:** the pause overlay presentation + its canon line ONLY — no toggle-key changes, no stepping/accumulator logic, no fast-path changes, no QoS, nothing 5.7-telemetry touches.


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
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.


--- HEADLESS FILE-OUTPUT CONTRACT (overrides the in-reply output above) ---
You are running headless as a mega-minion pane. When done:
1. Write your JSON array (and NOTHING else — no prose, no fencing) to EXACTLY this absolute path: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.3-pause-ux/r1/codebase.json
   (use your file-writing tool; create the file, do not derive any other path).
2. Reply with a single line: DONE <lens>.
3. Stop. Do not fix anything, do not run tests beyond what your lens needs, do not spawn anything.
