You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- WORKTREE (the repository at exactly the reviewed state — read-only) ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-pp-traffic-model-design-r1
Verify every claim against files under this path. Never modify anything. This is a detached worktree at exactly the reviewed sha — trust it, not any branch.

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

--- DIFF ---
diff --git a/_bmad-output/implementation-artifacts/spec-traffic-model.md b/_bmad-output/implementation-artifacts/spec-traffic-model.md
new file mode 100644
index 0000000..eeab7bc
--- /dev/null
+++ b/_bmad-output/implementation-artifacts/spec-traffic-model.md
@@ -0,0 +1,296 @@
+# Spec — Traffic Model: Access Tier, Bounded Demand, Aggregation, Terminal Diversity
+
+- **Job:** `packet-plumber-traffic-model-design` · branch `pp-traffic-model-design` (base `v2`)
+- **Status:** design spec — lavish review BEFORE the PR; story cards + GDD amendment accompany it
+- **Source (the ruling):** user ruling 2026-08-15 — the surge-explainer §Section B design notes are
+  **tasks to be done**: the traffic model gains realism so congestion lives where it does in real
+  networks. Primary source artifact: `surge-explainer.html` §B (the "Your design — narrow as
+  residential access" block, with the 1G/40G/100G → u/tick math).
+- **Scope guard:** design docs + story cards ONLY. No code, no balance.json changes, no
+  implementation — those are the story cards' jobs (cards at the bottom of this file's family:
+  stories-v2.md slice 5B).
+
+---
+
+## 1. The problem, one line
+
+**Today an endpoint can be its own chokepoint** — the demand director spawns map-wide volume with
+no per-terminal gate, so on a small map a single residential (throughput 5 u/s = 0.167 packets/tick)
+can be asked to source 4/tick, and packets drop at its own spawn (pool E22) and its own
+serialization (queue E9). In real networks that never happens: one FTTH subscriber cannot congest
+their own drop. **Congestion is an aggregation event.** This spec turns that sentence into four
+mechanics (the four threads), each a story card.
+
+Ground truth (shipped, verified in code):
+
+| Fact | Value | Where |
+|---|---|---|
+| Packet transit cost | 30 u/hop, **flat for every class** (`bandwidth_demand` loaded, not consumed) | `core/flow.odin:405`, `data/packet_types.json` |
+| Pipe tiers | narrow 5 / standard 15 / wide 40 u/s; routing cost 20/10/5 | `data/pipe_tiers.json` |
+| Residential node throughput | 5 u/s (= 0.167 pkts/tick) | `data/node_types.json` |
+| Era-3 demand | email 4/tick + streaming 2/tick = 6 arrivals/tick = 180 u/s | `data/demand.json` |
+| Director spawn | typed source/sink selectors → seeded weighted-random pick, `effective_volume` per spec | `core/flow.odin:600+`, `core/demand.odin` |
+| Pool cap (E22) | 512 in-flight; ladder shed BE→S→E; arrival self-drops when lowest candidate | `core/flow.odin:476` |
+| Lane bound (E9) | 6/lane; same ladder at admission | `core/flow.odin:710` |
+| Map growth (5.1) | one terminal / 120 ticks, TERMINALS only, E31 validity, rejection-sampled, seed-derived | `core/growth.odin` |
+
+The GDD's M1 table still shows aspirational tiers (narrow 10 / standard 25 / wide 50 / backbone 120);
+the **shipped catalog is the ground truth this spec and its cards target** (5/15/40). Flagging the
+discrepancy once here; the cards and the GDD M6 amendment use the shipped numbers.
+
+---
+
+## 2. The real-world scale math (cited from the explainer)
+
+1 u = the transit work of one 1500-byte frame crossing one hop. At 20 Hz logic:
+
+| Line rate | Packets/sec | u/tick |
+|---|---|---|
+| 1 G (FTTH drop) | 83,333 pps | **4,167** |
+| 40 G (metro) | 3.33 M pps | **166,667** |
+| 100 G (core) | 8.33 M pps | **416,667** |
+
+Ratios **1 : 40 : 100** — the FTTH ladder. The 512-packet pool ≈ 768 KB ≈ 6 ms of 1-Gbps line rate:
+**real-router buffer scale** (a packet count, independent of the unit scale). The catch the design
+must hold: today's demand (6–24 pkts/tick ≈ 1.4–5.8 Mbps aggregate) is 100–1,000× below a single
+1-G link — **nothing would ever congest at literal scale**. The sim is playable because its tiers
+(5/15/40 u/s) compress the ratio scale ~1,000× and the demand saturates them.
+
+**Design shape (the explainer's own):** narrow = the last-mile drop to a residential, sized so ONE
+subscriber's traffic never congests it — narrow ≈ **8–10 u/s** (0.27–0.33 pkts/tick per edge) and a
+residential emitting ~**0.2 pkts/tick** (its share of 6/tick across ~30 terminals) fits with
+**~1.5× headroom**; the access link stops being the choke. Congestion appears where it should: when
+many residentials' flows aggregate onto a metro/backbone link (standard 15 / wide 40), and the ×10
+surge is an **aggregation event** — every subscriber streaming one event saturates the shared core,
+not the access drops.
+
+---
+
+## 3. The four threads (each = one mechanic = one story card)
+
+### Thread 1 — Narrow as residential access (the access tier)
+
+**Mechanic (Given/When/Then):**
+- **Given** a residential terminal connected by a single narrow pipe to its aggregation point;
+- **When** that residential's own traffic (bounded per Thread 2) flows;
+- **Then** the narrow access link **never** congests from the one subscriber — its headroom vs the
+  per-terminal cap is ≥ ~1.3–1.5× — and congestion appears only where many subscribers' flows
+  **aggregate** onto shared links (standard/wide).
+
+**Real-world rationale:** real FTTH — a 1-G drop does not congest from your own streaming; congestion
+lives where many subscribers share a link. The 1 : 40 : 100 u/tick ratio makes narrow/standard/wide
+the access/metro/core tiers of the same topology.
+
+**Balance levers (data-driven per canon):**
+- `data/pipe_tiers.json` → narrow `capacity_units` 5 → **~8–10** (proposed starting point;
+  playtest-tunable). `cost` stays 20 — the routing-cost ladder is **moot on access links** (a single
+  path; the ladder only matters between routers where alternatives exist — the capacity-cost ruling
+  2026-08-13 is untouched; between routers, flows still prefer fat pipes).
+- Optional: narrow `display_name`/canon role → "access" flavor (wording is the terminology audit's
+  lane — cards do not rename; they add canon role via the GDD M6 entry).
+
+**Determinism constraints:** pure catalog change → `cat.hash` folds every catalog byte → **legitimate
+deliberate re-bless** of T1/T2 goldens (the 4.3 discipline: byte-verify `.log.bin` differs only in
+the version field, splice the old catalog_hash, cause-document). No new commands → **no LOG_VERSION
+bump**.
+
+**Canon interactions:** E22 pool — unchanged (the pool still backstops the map; it no longer sheds
+endpoint self-congestion because there is none); E9 lane bounds — unchanged; 4.1 strain — a strained
+narrow now *genuinely* means an undersized access link (honest diagnosis, the readability payoff);
+5.8 QoS — access links carry the same 3 lanes; aggregation (Thread 3) is where the lane call matters.
+
+### Thread 2 — Per-terminal demand caps (endpoints never self-congest)
+
+**Mechanic (Given/When/Then):**
+- **Given** a live terminal of role R and the demand director's spawn pass for a spec;
+- **When** the director's volume would assign more spawns to one terminal than its per-terminal cap
+  this tick;
+- **Then** the capped terminal is **skipped** (deterministic, array-order) and the volume lands on
+  other terminals (or waits) — **no endpoint can ever be asked to source more than a small fraction
+  of its access capacity**, so no endpoint self-congests.
+
+**Why it's the load-bearing invariant:** everything else in this spec assumes "endpoints never
+self-congest". Without it, a small map makes the endpoint the chokepoint (drops at spawn E22 + at
+serialization E9 at its own drop) — the exact noise the surge explainer diagnosed at 10:04.
+
+**Balance levers:**
+- `data/balance.json` → new `max_packets_per_terminal` (or per-type, see Thread 4). Proposed
+  starting point: **~0.2 pkts/tick** for a residential ≈ 6 u/s demand vs the ~8–10 u/s access link
+  (~1.5× headroom). Playtest-tunable.
+- The cap is a **hard bound on the variance**, not the average: the director's weighted-random pick
+  already shares volume across terminals; the cap stops small-map concentration (the MVP's 4–6-node
+  map is exactly the pathological case).
+- Corollary (deliberate): with caps, the surge's 20/tick **needs ≥ (20 ÷ cap) terminals to land** —
+  the map must grow (5.1) or the demand is shed. This is *by design*: it turns map growth into a
+  first-class pressure and makes the surge an aggregation problem, not a one-endpoint flood.
+- **Consequence the cards must carry (explicit, not hidden):** the era-3 demand signature (email
+  4/tick + streaming 2/tick, tuned for the 4–6-node map) and the 5.1 growth pacing must be
+  **re-validated together** — with caps in place the MVP map cannot carry era-3 volume until growth
+  has provided enough terminals. Card 5.9 owns this: the cap is **per-type** (a content_host
+  sourcing the streaming surge caps against ITS throughput ~2.67 pkts/tick, NOT the residential
+  0.2), and the growth pacing is re-checked so era 3 has the terminal count. The invariant is
+  canon; the values are playtest tuning. If the surge silently stops landing, that is a fail, not a
+  feature.
+
+**Determinism constraints:** cap lives in the catalog (→ legitimate re-bless) or derived from live
+topology (terminal count — deterministic). Spawn sequence changes (the (class, src, dst) stream is
+rng-drawn per pick; skips shift it) → **deliberate re-bless**, cause-documented. All seed-derived;
+**no wall-clock**. No new commands → no LOG_VERSION bump.
+
+**SLA-accounting seam (must be pinned by the card):** a capped spawn is **skipped before
+`flow_try_spawn`** — it is NOT a demand event (never reaches `sla_count_demand`); a pool-dropped
+arrival IS (it counts demand then drops). The invariant `demand_seen == delivered + dropped + live`
+(E24) must hold under both paths — the card pins it with a test.
+
+**Canon interactions:** E22 — spawn drops become aggregation drops, never endpoint self-drops (the
+pool cap 512 stays); E9 — admission shed at the shared uplink, not the endpoint; 4.1 — a residential
+node no longer shows strain from its own spawns (strain on a terminal = undersized access, honest);
+5.1 growth — growth lowers per-terminal load (more terminals share the volume; the cap is the floor
+that keeps it honest on small maps).
+
+### Thread 3 — Aggregation groups (congestion lives at the shared uplink)
+
+**Mechanic (Given/When/Then):**
+- **Given** a cluster of nearby terminals (a neighborhood analogue) whose flows share one
+  player-built uplink;
+- **When** aggregate demand from the cluster rises (base or the ×10 surge);
+- **Then** the shared uplink — not any member terminal and not any access drop — is where congestion
+  appears, and the player's router/tier/bundle/QoS decisions on that uplink are what relieve it.
+
+**Real-world rationale:** the honest choke is "a handful of residentials sharing one uplink". The ×10
+surge is an **aggregation event** — every subscriber streaming one event saturates the shared core.
+
+**Balance levers:**
+- Growth (5.1) gains a **group-bias term** in the placement draw: a spawned terminal is drawn near an
+  existing cluster member (a group radius + a group-size cap), so clusters actually concentrate.
+- The demand director gains a **group-scoped weight**: members of the same group share an uplink
+  target (flows from a cluster land on the cluster's aggregation point), so the surge stresses the
+  group uplink.
+- Proposed starting shape: 3–8 terminals per group; group radius ~2–3 tiles (see the conflict
+  resolution below). Data-driven (balance.json) at the legitimate re-bless; core consts until then
+  (the growth precedent — 5.1's tuning lives as consts for exactly this reason).
+
+**Conflict resolution — growth-spawn validity (E31) vs group placement (EXPLICIT):**
+- E31 (hard contract, untouched): every spawned terminal is (a) connectable-within-span of a live
+  junction, (b) min-separated from nodes AND pipe segments, (c) inside the grid; invalid candidates
+  rejection-sample from the rng stream within a bounded budget.
+- **Resolution:** the group bias is a **soft preference inside the E31 validity envelope** — the
+  bias draw runs first, the E31 validity test runs on the biased candidate, and rejection-sampling
+  (which can land outside the group) is unchanged. A group never forces a placement that violates
+  E31, and E31 never re-routes a group. **The uplink itself is never forced** — the player wires it
+  (the group concentrates *demand*; the player builds the fat pipe). This keeps E31 byte-stable in
+  contract while making clusters emergent from the seed.
+- Rejected alternative (recorded): demand-side-only grouping (no topology bias) would concentrate
+  flows without a shared link — the "congestion" would smear across whichever routes exist and the
+  honest aggregation picture never forms.
+
+**Determinism constraints:** groups are derived from the seed (growth placement draws + the type
+pick) + the live topology — fully seed-derived, no wall-clock, no log entries (growth is already
+log-free; the bias extends the same derive-don't-record rule). T1 shifts (spawn sequence + topology)
+→ deliberate re-bless.
+
+**Canon interactions:** 5.1 growth (the bias extends the growth draw — the card must keep
+"existing goldens unshifted" provable at the growth-const level and cause the single deliberate
+re-bless at the slice boundary); 4.2 surge (the surge = the aggregation event; crisis engine's
+`preventive_redesign` copy already says "add a parallel pipe or a higher tier on the spike's path" —
+now that path is the group uplink); 5.8 QoS (lane assignment at the group uplink is the lever);
+E31 (hard floor preserved, above).
+
+### Thread 4 — Diverse terminal types (schools, offices, homes)
+
+**Mechanic (Given/When/Then):**
+- **Given** the terminal roster carrying multiple class analogues (residential / small-biz / campus);
+- **When** the director and growth spawn/weight terminals;
+- **Then** each type emits a **different, bounded demand profile** (volume, per-terminal cap,
+  throughput) — a campus emits far more than a home — and the type is readable without color.
+
+**Real-world rationale:** schools, universities, and data centers emit far more than a home; the
+terminal roster is the honest spectrum. The roster is catalog data — **a data change, not a code
+change** (`node_types.json`).
+
+**Balance levers:** `data/node_types.json` — new entries (e.g. `small_biz`, `campus`) with
+`terminal_role`, `throughput_units`, `demand_weight`, `era_introduced`, and the per-type cap/profile
+fields Thread 2 introduces. Distinct shapes/icons (never color alone — the a11y invariant, E9.1).
+
+**Determinism constraints:** catalog data → `cat.hash` fold → deliberate re-bless. New types respect
+E31 spawn validity + the 5.6 placement separation. The growth type-pick and the director's
+source_role selectors are rng/topology-derived — deterministic.
+
+**Canon interactions:** 5.1 growth (which types growth spawns, and when — era gating); demand
+director (source_role selectors resolve against the new types); E31 (validity applies per type);
+5.6 placement (terminals never block router placement — holds for every new type).
+
+**Related-but-out-of-scope (flagged, not a fifth thread):** `bandwidth_demand` (streaming's ×2) is
+loaded but **not consumed** — every packet costs the flat 30 u/hop. Thread 4 makes per-class transit
+cost meaningful, but wiring `bandwidth_demand` is a separate balance decision (it changes every
+transit-time number and the ECMP/economics); it is deliberately left for a future decision, named
+here so nobody mistakes the omission for an oversight.
+
+---
+
+## 4. Interaction matrix (the four threads × existing canon)
+
+| Canon | Thread 1 (access) | Thread 2 (caps) | Thread 3 (groups) | Thread 4 (types) |
+|---|---|---|---|---|
+| **E22 pool (512)** | unchanged | spawn drops become aggregation drops, never endpoint self-drops | unchanged (aggregation shed at the uplink) | unchanged |
+| **E9 lane bound (6)** | unchanged | admission shed at the shared uplink, not the endpoint | the shared uplink is where the shed fires | unchanged |
+| **4.1 strain** | strained narrow = honest undersized-access signal | residential strain = undersized access, not own spawns | strain localizes to the group uplink/router | per-type throughput feeds the ring |
+| **5.1 growth (E31)** | access tier is the growth target's natural link | growth lowers per-terminal load; cap keeps small maps honest | **group bias inside the E31 envelope (explicit resolution)** | growth type-pick + era gating |
+| **5.8 QoS** | access links carry 3 lanes | — | the group uplink is where lane assignment matters most | — |
+| **Capacity-cost routing (2026-08-13)** | cost ladder moot on access (single path); untouched between routers | — | — | — |
+| **4.2 surge** | — | surge needs ≥(20÷cap) terminals → growth pressure | the surge IS the aggregation event | — |
+| **SLA accounting (E24)** | — | **capped skip ≠ demand event; pool-drop IS — pin both** | — | per-type profiles feed SLA |
+
+**Determinism spine:** every thread is seed-derived (rng draws from `state.rng`), topology-derived,
+or catalog data — no wall-clock anywhere; replay stays byte-identical with **one deliberate,
+cause-documented re-bless** at the slice boundary (all four threads shift the (class, src, dst)
+spawn stream and/or the catalog hash). No new command kinds → **no LOG_VERSION bump**. New tuning
+values follow the growth precedent (core consts → balance.json at the legitimate re-bless).
+
+---
+
+## 5. Sequencing proposal — story cards in stories-v2
+
+**Proposal: a new slice between 5 and 6 — "Slice 5B — Traffic realism", stories 5.9–5.12** (story
+numbers continue slice 5's sequence; no existing card renumbered).
+
+| Card | Thread | Order rationale |
+|---|---|---|
+| **5.9 — Per-terminal demand caps** | 2 | The invariant everything else assumes ("endpoints never self-congest"). Smallest, surgical; unblocks the honest surge. |
+| **5.10 — Narrow as residential access** | 1 | Sizing + canon role; its headroom math needs 5.9's bounded demand. |
+| **5.11 — Diverse terminal types** | 4 | Profiles need the cap machinery (5.9) + the access canon (5.10) to mean anything. |
+| **5.12 — Aggregation groups** | 3 | The payoff — congestion lives at the shared uplink; needs caps + access + diversity. |
+
+**Why not the alternatives (each rejected with reason):**
+- **Fold into slice 6 (era transition):** rejected — slice 6 is the E5 era-FSM/modernization epic;
+  these threads are E2.1/E3.1/E3.2 demand+topology work (the slice-5 systems cluster's natural
+  completion). Folding muddles the epic mapping and bloats an already-tight slice.
+- **Post-fun-gate (slice 8+):** rejected — the slice-7 playtest gate must measure the **honest**
+  congestion model ("why is my endpoint dropping packets?" must be a readable statement about the
+  network — the fun-test question). Testing the current endpoint-self-congestion noise would
+  validate the wrong game.
+- **Renumber as slice 6 (shifting era transition to 7):** rejected — destructive renumbering of
+  shipped references for zero gain; 5.9–5.12 keeps the story ids monotonic.
+- **"Post-5.4" strictly (before 5.5–5.8):** rejected — the threads depend on 5.1 growth + 5.8 QoS
+  (merged); 5.4 input parity is orthogonal. Slotting after the slice-5 cluster (post-5.8) satisfies
+  the briefing's "post-5.4" intent with the real dependency order.
+
+**Gate ordering:** landing 5B before slice 6/7 means the era-transition story and the playtest
+exercise the honest aggregation model from the start, and the deliberate golden re-bless batches at
+the 5B boundary instead of interleaving with slice-6/7 churn.
+
+**Sprint-plan note:** `sprint-plan-v2.md`'s slice map gains a 5B row at ratification (included in
+this job's PR so the plan and the stories don't contradict).
+
+---
+
+## 6. Deliverables in this job
+
+1. This design spec (lavish-reviewed, in the artifact).
+2. Story cards 5.9–5.12 appended to `stories-v2.md` (existing card format).
+3. GDD amendment: a new **M6 — Traffic realism** mechanics block (section-additive, after M5,
+   before Controls) + a decision-log entry (append-only) — no terminology rewrites, no edits to
+   existing GDD text (the coordination constraint: the p1P8 terminology audit serializes behind
+   this job's GDD edits; Silas serializes the PRs).
+4. `sprint-plan-v2.md` slice-map row (5B).
+5. The lavish artifact presenting all of it; the PR opens only after approval.
diff --git a/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/decision-log.md b/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/decision-log.md
index c311a6c..69a37bb 100644
--- a/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/decision-log.md
+++ b/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/decision-log.md
@@ -727,3 +727,82 @@ Lavish review of `gdd.md` + `epics.md` → on approval, commit/push/PR to
   package (draw-time flow preview, post-draw route glow, tie cues — Job B),
   the forecast flow-shift prediction (Job C), per-class routing preferences
   (full-game idea, not this ruling).
+
+---
+
+## 2026-08-15 — Traffic realism: access tier + bounded demand + aggregation (user ruling, the Section B design threads)
+
+- **Origin:** the surge-explainer (§Section B design notes, artifact
+  `_bmad-output/implementation-artifacts/surge-explainer/surge-explainer.html`)
+  diagnosed that the sim's endpoints can be their own chokepoints — the demand
+  director spawns map-wide volume with NO per-terminal gate, so on a small map a
+  residential (throughput 5 u/s = 0.167 pkts/tick) can be asked to source 4/tick
+  and drops at its own spawn (pool E22) + its own serialization (queue E9). The
+  user ruled (2026-08-15): **the Section B design notes are TASKS to be done** —
+  the traffic model gains realism so congestion lives where it does in real
+  networks.
+- **Decision — four coupled mechanics, canonized (GDD M6, section-additive; story
+  cards 5.9–5.12 in stories-v2 slice 5B; design spec `spec-traffic-model.md`):**
+  1. **Per-terminal demand caps** — the demand director bounds each terminal's
+     spawn rate (per-terminal cap, proposed ~0.2 pkts/tick ≈ 6 u/s for a
+     residential, ~1.5× headroom under its access link; playtest-tunable in
+     `balance.json`): no endpoint ever sources more than a small fraction of its
+     access capacity — **endpoints never self-congest** (the load-bearing
+     invariant). The cap is **per-type** (a content_host sourcing the streaming
+     surge caps against ITS throughput ≈ 2.67 pkts/tick); era-3 demand + 5.1
+     growth pacing are **re-validated together** so the MVP surge still lands.
+     Capped skips are NOT demand events (SLA-accounting seam, E24,
+     test-pinned); a pool-dropped arrival still IS.
+  2. **Narrow as residential access** — narrow is the **last-mile access tier**;
+     `capacity_units` 5 → ~8–10 (playtest-tunable), sized so ONE subscriber's
+     traffic never congests it. The routing-cost ladder (narrow 20) is **moot on a
+     single-path access link** and unchanged between routers — the 2026-08-13
+     capacity-cost ruling stands untouched. Congestion lives on the shared
+     standard/wide links where flows **aggregate**.
+  3. **Aggregation groups** — terminals cluster into neighborhoods whose flows
+     share one **player-built uplink** (the honest choke). Growth gains a
+     **group-bias draw inside the E31 validity envelope** (soft preference —
+     bias first, E31 validity on the biased candidate, rejection-sampling
+     unchanged; E31 stays the hard contract; the uplink is never forced). The
+     demand director weights group-scoped demand; the ×10 surge is an
+     **aggregation event** at the group uplink.
+  4. **Diverse terminal types** — the roster gains class analogues (residential /
+     small-biz / campus) with different **bounded** demand profiles; campus >>
+     home. Roster is catalog data (`node_types.json`) — a data change, not a code
+     change; distinct shape/icon per type, never color alone `[E9.1]`.
+- **The real-world math (cited from the explainer):** 1 u = one 1500-byte frame's
+  transit work. At 20 Hz: 1 G = 4,167 u/tick · 40 G = 166,667 · 100 G = 416,667 —
+  ratios 1:40:100, the FTTH ladder. The 512-pool ≈ 768 KB ≈ 6 ms of 1-Gbps line
+  rate (real-router buffer scale). Today's demand (6–24 pkts/tick ≈ 1.4–5.8 Mbps)
+  is 100–1,000× below a single 1-G link; the sim's tiers (5/15/40) compress the
+  ratio scale ~1,000× — the design keeps that compression, just honest: access
+  never chokes on one subscriber; aggregation chokes on many.
+- **What this does NOT change:** E22 pool cap (512), E9 lane bound (6/lane), the
+  drop ladders, the 4.1 strain formula, 5.8 QoS lanes (access links carry the same
+  3 lanes), the capacity-cost routing ruling, the 5.1 growth E31 contract
+  (group bias is a soft preference inside it), the era FSM. No new command kinds.
+- **Determinism:** all four are seed-derived (rng draws from `state.rng`),
+  topology-derived, or catalog data — no wall-clock anywhere; replay stays
+  byte-identical with **one deliberate, cause-documented golden re-bless** at the
+  slice-5B boundary (catalog + spawn-stream changes fold `cat.hash`; the
+  traffic-model change IS the "legitimate re-bless" event the 4.3 golden
+  discipline reserves for). **No LOG_VERSION bump.**
+- **Sequencing (stories-v2 slice 5B, between slice 5 and slice 6):** 5.9
+  per-terminal caps (the invariant first) → 5.10 narrow-as-access (sizing needs
+  the caps) → 5.11 terminal diversity (profiles need the caps + access canon) →
+  5.12 aggregation groups (the payoff). Rejected alternatives recorded in the
+  spec: fold into slice 6 (era-FSM epic mismatch), post-fun-gate slice 8+ (the
+  playtest gate must measure the honest congestion model), renumber-as-slice-6
+  (destructive). Landing pre-gate means the era transition + playtest exercise the
+  honest aggregation model from the start.
+- **Related-but-out-of-scope (flagged, not a fifth thread):** `bandwidth_demand`
+  (streaming's ×2) is loaded but not consumed — every packet costs the flat 30
+  u/hop. Thread 4 makes per-class transit meaningful, but wiring
+  `bandwidth_demand` is a separate balance decision, deliberately left for a
+  future ruling.
+- **Applied (this job):** GDD — new `#### M6 — Traffic realism` mechanics block
+  (section-additive, after M5, before Controls; no terminology rewrites — the
+  p1P8 terminology audit serializes behind this job's GDD edits); stories-v2.md —
+  slice 5B + cards 5.9–5.12; sprint-plan-v2.md — slice-map row; design spec at
+  `_bmad-output/implementation-artifacts/spec-traffic-model.md` (lavish-reviewed
+  before the PR opens).
diff --git a/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md b/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md
index 4aad860..cbe4817 100644
--- a/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md
+++ b/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md
@@ -290,6 +290,42 @@ The V2 **AI stress-test system** (deferred — full-game replayability, forge we
 
 **Demand director — bespoke per-era crisis rhythm (P3, *user-ratified addition, lavish review 2026-08-10*).** Crisis pacing is **hand-tuned per era**, not a flat difficulty curve: a demand director scripts each era's surges to an authored rhythm — a tension peak climbing through staged thresholds (the Hades 2 wave-gate principle: 50 / 70 / 90%), broken by an *earned* breath where gauges recover and the player banks the era's reward. The rhythm kills dead time (a lull is always about to break) and makes the breath *relieving* rather than empty. Each era's signature demand (M4) gets its own cadence — the streaming surge is a single 10× wall, the real-time era is rapid multi-class triage, the cloud era is long sustained pressure. This is the *pacing* layer of the crisis model: crises stay *fair* (every spike forecast, every flaw preventable, per the fairness rules) while their *timing* is authored for feel. `[ASSUMPTION: prototype tuning — per-era threshold curves and breath windows are authored at balance time.]` *(Full-game `[FULL]`; the MVP ships one fixed surge set-piece.)*
 
+#### M6 — Traffic realism: access tier, bounded demand, aggregation (P1, P3, *user ruling 2026-08-15*)
+
+Congestion lives where it does in real networks — **at aggregation points, never at endpoints**. A
+single subscriber cannot congest their own drop (real FTTH: your 1-G drop doesn't congest from your
+own streaming); congestion appears where many subscribers share a link. The traffic model encodes
+that in four coupled mechanics (provenance: `decision-log.md` 2026-08-15; design spec
+`spec-traffic-model.md`; the real-world-scale math — 1 u = one 1500-byte frame's transit work; 1 G =
+4,167 u/tick, 40 G = 166,667, 100 G = 416,667 @ 20 Hz, ratios 1:40:100 — the sim compresses the
+ratio scale ~1,000× onto the shipped tiers narrow 5 / standard 15 / wide 40):
+
+1. **Per-terminal demand caps** — the demand director bounds each terminal's spawn rate (proposed
+   ~0.2 pkts/tick ≈ 6 u/s for a residential, ~1.5× headroom under its ~8–10 u/s access link;
+   playtest-tunable in `balance.json`): no endpoint can be asked to source more than a small
+   fraction of its access capacity, so **endpoints never self-congest** — the invariant everything
+   else rests on. Spawn drops become aggregation drops (E22 pool unchanged).
+2. **Narrow as residential access** — narrow is the **last-mile access tier** (capacity 5 → ~8–10,
+   playtest-tunable), sized so one subscriber's traffic never congests it; the routing-cost ladder
+   (narrow 20) is moot on a single-path access link and unchanged between routers (the 2026-08-13
+   capacity-cost ruling stands). Congestion lives on the shared metro/backbone links (standard/wide)
+   where flows **aggregate**.
+3. **Aggregation groups** — terminals cluster into neighborhoods whose flows share one player-built
+   uplink (growth gains a group-bias draw **inside the E31 validity envelope** — soft preference,
+   never a hard floor; the uplink is never forced, the player wires it); the demand director
+   weights group-scoped demand, and the ×10 surge is an **aggregation event** at the group uplink.
+4. **Diverse terminal types** — the terminal roster gains class analogues (residential / small-biz /
+   campus) with different **bounded** demand profiles; a campus emits far more than a home. Roster is
+   catalog data (`node_types.json`) — a data change, not a code change; distinct shape/icon per type,
+   never color alone `[E9.1]`.
+
+All four are **seed-derived or catalog data — no wall-clock**; replay stays byte-identical with one
+**deliberate, cause-documented golden re-bless** at the story-slice boundary (catalog + spawn-stream
+changes; no new command kinds → no LOG_VERSION bump). The payoff (the player-facing problem): once
+endpoints cannot self-congest, drops localize to the network layer — access / aggregation / core —
+which is precisely the player's buildable domain; "why is my endpoint dropping packets?" becomes a
+readable statement about the network feeding it.
+
 ### Controls and Input
 
 **Cross-platform same-game doctrine `[FORGE #6]`:** draw-between-nodes is input-agnostic — one game, three inputs, identical play.
diff --git a/_bmad-output/planning-artifacts/sprints/sprint-plan-v2.md b/_bmad-output/planning-artifacts/sprints/sprint-plan-v2.md
index d58c85b..39e9165 100644
--- a/_bmad-output/planning-artifacts/sprints/sprint-plan-v2.md
+++ b/_bmad-output/planning-artifacts/sprints/sprint-plan-v2.md
@@ -74,6 +74,7 @@ equality golden are **proven** in 1.1 (not just scaffolded) before any feature d
 | **3** | QoS — 2 packet types + 3 lanes (the differentiator) | route email+streaming; emphasis dial; contention drops best-effort first | — | ✅ |
 | **4** | Surge-survival loop — forecast + Surge + Network Health + win/lose/retry | **predict the surge, survive it, win/lose/retry** | **✅ earliest** | ✅ |
 | **5** | Growing map + health telegraph + input parity | nodes grow; 🔴 traceable; pause; touch/controller | deeper | ✅ |
+| **5B** | Traffic realism — access tier + bounded demand + aggregation (user ruling 2026-08-15, the Section B threads) | endpoints never self-congest; congestion lives at the shared uplink the player builds | deeper | ✅ |
 | **6** | One era transition — Email→Streaming (modernization) | experience the internet evolving; modernize or suffocate | deeper | ✅ |
 | **7** | Juice + accessibility (**MVP done**) | feels+sounds like saving the internet; playable by everyone | **✅ MVP test** | ✅ |
 | **8+** | The six GDD mechanics (post-fun-gate) | each deepens the proven loop at its natural home | full-game | ❌ |
diff --git a/_bmad-output/planning-artifacts/sprints/stories-v2.md b/_bmad-output/planning-artifacts/sprints/stories-v2.md
index b4abaca..a4d6abf 100644
--- a/_bmad-output/planning-artifacts/sprints/stories-v2.md
+++ b/_bmad-output/planning-artifacts/sprints/stories-v2.md
@@ -634,6 +634,130 @@ inputs, placeable router tiers, demolish-and-redesign, a telemetry X-ray, legibl
 
 ---
 
+## Slice 5B — Traffic realism: the honest congestion model (access tier + bounded demand)
+
+*The Section B design threads (user ruling 2026-08-15): congestion lives where it does in real
+networks — at aggregation points, never at endpoints. Source: `surge-explainer.html` §B (the
+1G/40G/100G → u/tick math) + `spec-traffic-model.md`. Design spec: `_bmad-output/implementation-
+artifacts/spec-traffic-model.md`. Sequencing rationale (post-slice-5 systems cluster, before the
+slice-6 era transition + the slice-7 playtest gate) lives in that spec §5 — each card is sized for
+one fresh minion, dispatched in order 5.9 → 5.12 (the invariant first, the payoff last).*
+
+### Story 5.9 — Per-terminal demand caps (endpoints never self-congest)
+
+- **Slice:** 5B · **Epic(s):** E2.1, E3.1 · **Systems:** director `[ODN-7]` (demand.odin spawn
+  pass), catalogs `[ODN-5]`.
+- **Goal.** The demand director bounds each terminal's spawn rate — a per-terminal cap (packets/tick)
+  stops any endpoint from being asked to source more than a small fraction of its access capacity
+  (proposed start ~0.2 pkts/tick for a residential ≈ 6 u/s vs the ~8–10 u/s access link, ~1.5×
+  headroom; playtest-tunable). Endpoints never self-congest; spawn drops become aggregation drops.
+
+**Given/When/Then:**
+- **Given** the director's spawn pass and a per-terminal cap (catalog value, data-driven; core const
+  until the slice's legitimate re-bless — the growth precedent);
+- **When** a spec's volume would assign more spawns to one terminal than its cap this tick;
+- **Then** the capped terminal is **skipped** (deterministic, array-order — no map iteration, no rng
+  draw for the skip) and the volume lands on other terminals; no endpoint can ever self-congest (a
+  residential is never asked to source more than its cap); the (class, src, dst) spawn sequence is
+  byte-identical for a fixed seed `[E10]`; **a capped skip is NOT a demand event** (never reaches
+  `sla_count_demand`) while a pool-dropped arrival IS — the `demand_seen == delivered + dropped +
+  live` invariant (E24) holds under both paths (test-pinned); the surge's 20/tick needs ≥ (20 ÷ cap)
+  terminals to land — growth pressure by construction; **the cap is PER-TYPE** (a content_host
+  sourcing the streaming surge caps against ITS throughput ≈ 2.67 pkts/tick, not the residential
+  ~0.2); era-3 demand + 5.1 growth pacing are **re-validated together** so the MVP surge still
+  lands (silent non-landing is a fail, not a feature).
+
+- **Edge-case contracts:** `[E10]` replay, `[E24]` SLA accounting under capped skips, E22 pool
+  unchanged. **Golden:** T1 (spawn sequence shift — **deliberate, cause-documented re-bless** per the
+  4.3 discipline; byte-verify `.log.bin` differs only in the version field, splice the old
+  catalog_hash, cause-document); existing goldens unshifted at the const level.
+- **Launchable increment:** run the app on a small map — no residential is ever the drop site; drops
+  (if any) sit at the aggregation/uplink, not the endpoint's spawn.
+
+### Story 5.10 — Narrow as residential access (the access tier)
+
+- **Slice:** 5B · **Epic(s):** E3.1 · **Systems:** catalogs `[ODN-5]` (pipe_tiers), topology (S1).
+- **Goal.** Narrow's canon role is the **last-mile access drop**, sized so ONE subscriber's traffic
+  never congests it: narrow `capacity_units` 5 → **~8–10** (proposed start; playtest-tunable) with
+  the routing-cost ladder (20) untouched — cost is moot on a single-path access link, and the
+  2026-08-13 capacity-cost ruling is unchanged between routers (flows still prefer fat pipes).
+
+**Given/When/Then:**
+- **Given** a residential wired to its aggregation point by one narrow pipe, with bounded per-terminal
+  demand (5.9);
+- **When** the residential's own traffic flows (base or surge);
+- **Then** the narrow access link carries it with **~1.3–1.5× headroom** (cap ≈ 6 u/s vs narrow
+  ~8–10 u/s) — the access link never congests from the one subscriber; congestion appears only where
+  flows **aggregate** onto shared standard/wide links; a strained narrow now genuinely signals an
+  undersized access link (the honest 4.1 reading); replay is byte-identical `[E10]`; the tier change
+  folds `cat.hash` → the slice's **deliberate re-bless** (proven discipline).
+
+- **Edge-case contracts:** `[E10]` replay, capacity-cost ruling untouched, `[E3]` span rules
+  unchanged. **Golden:** T1/T2 re-bless (cause-documented, the slice boundary's legitimate re-bless).
+- **Launchable increment:** run the app — a single residential on a narrow never drops its own
+  traffic; stress appears when many homes share a link.
+
+### Story 5.11 — Diverse terminal types (schools, offices, homes)
+
+- **Slice:** 5B · **Epic(s):** E3.1, E2.1 · **Systems:** catalogs `[ODN-5]` (node_types), director
+  `[ODN-7]` (source_role selectors), growth (5.1 type pick).
+- **Goal.** The terminal roster gains class analogues — residential / small-biz / campus — each with
+  a **different, bounded demand profile** (volume, per-terminal cap, throughput); a campus emits far
+  more than a home. Roster is catalog data (`node_types.json`) — **a data change, not a code change**;
+  distinct shape/icon per type (never color alone `[E9.1]`).
+
+**Given/When/Then:**
+- **Given** the extended `node_types.json` roster (new `terminal_role`s + per-type cap/profile
+  fields) and the demand specs whose source/sink selectors resolve against it;
+- **When** the director spawns and growth (5.1) places terminals of the new types;
+- **Then** each type emits its own bounded profile (campus >> home in volume and cap); the director's
+  typed selectors resolve against the new types (era-gated); growth spawns the new types per its
+  era gating, every spawn satisfying E31 validity + the 5.6 placement separation; the type is
+  readable without color; replay is byte-identical `[E10]`; catalog fold → the slice's deliberate
+  re-bless.
+
+- **Edge-case contracts:** `[E10]` replay, `[E31]` spawn validity per type, `[E9.1]` never-color-
+  alone. **Golden:** T1/T2 re-bless + a T2 frame with all three types visible.
+- **Launchable increment:** run the app — homes trickle, campuses flood; the terminal roster reads
+  as a spectrum.
+
+### Story 5.12 — Aggregation groups (congestion lives at the shared uplink)
+
+- **Slice:** 5B · **Epic(s):** E3.2, E4.2 · **Systems:** growth (5.1 group-bias draw), director
+  `[ODN-7]` (group-scoped demand weight), crisis Surge (S4).
+- **Goal.** The payoff: terminals cluster into groups (neighborhood analogues) whose flows share one
+  player-built uplink — the honest choke. The demand director weights group-scoped demand; the ×10
+  surge is an **aggregation event** at the group uplink. **Explicit conflict resolution:** the group
+  bias is a **soft preference inside the E31 validity envelope** (bias draw first, E31 validity on
+  the biased candidate, rejection-sampling unchanged); the uplink is never forced — the player wires
+  it. E31 stays the hard contract.
+
+**Given/When/Then:**
+- **Given** a group-bias growth draw (spawn near an existing cluster member within a group radius;
+  proposed 3–8 members, radius ~2–3 tiles — playtest-tunable) and a group-scoped demand weight;
+- **When** aggregate demand from a cluster rises (base or the ×10 surge);
+- **Then** the shared uplink — not any member terminal, not any access drop — is where congestion
+  appears; every spawned terminal still satisfies E31 (connectable-within-span, min-separated,
+  in-grid) and growth stays fully seed-derived (no log entries, derive-don't-record); the surge
+  stresses the group uplink (the crisis engine's `preventive_redesign` — "add a parallel pipe or a
+  higher tier on the spike's path" — now names the group uplink); replay is byte-identical `[E10]`;
+  deliberate re-bless at the slice boundary.
+
+- **Edge-case contracts:** `[E10]` replay, `[E31]` hard floor preserved (group bias never violates
+  it), `[E9]`/`[E22]` unchanged. **Golden:** T1/T2 re-bless + a T2 frame of a clustered topology
+  under surge (drops at the uplink).
+- **Launchable increment:** run the app — a handful of homes share one uplink; the surge saturates
+  the shared link, and the player's router/tier/bundle/QoS call on it decides who lives.
+
+**→ Slice 5B exit:** the traffic model is honest — endpoints never self-congest (5.9), access is
+real last-mile (5.10), terminals read as a spectrum (5.11), and congestion lives where it does in
+real networks — at the shared uplink the player builds (5.12). The slice-6 era transition and the
+slice-7 playtest gate exercise the honest aggregation model from the start. **(One deliberate,
+cause-documented golden re-bless lands at this slice's boundary — the traffic-model change is
+precisely the "legitimate re-bless" event the 4.3 discipline reserves for.)**
+
+---
+
 ## Slice 6 — One era transition: Email → Streaming (modernization)
 
 *The GDD MVP (E1–E9) includes E5 (lavish choice 3A: keep slice 6). A minimal single-

--- SPEC / CONTEXT ---
# Briefing — packet-plumber-traffic-model-design (canon: the Section B design thread becomes story cards)

- **Job id:** `packet-plumber-traffic-model-design`
- **Repo:** packet-plumber · **Base:** `v2` @ latest · **Slug:** `pp-traffic-model-design`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Mega-minions same —
  name explicitly at every spawn.
- **Skills policy:** `gds-agent-game-designer` (story-card + canon authorship) +
  `lavish` (the user reviews the design in-browser BEFORE the PR — docs loop).
- **Perkins:** `pr_review: 1` (canon-surface PR).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out
  your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-traffic-model-design <url>` yourself.
- **Source material (the thread is already decision-ready — read first):**
  `_bmad-output/implementation-artifacts/surge-explainer/surge-explainer.html`
  §Section B design notes + the real-world-scale math (1G/40G/100G → u/tick).
- **Coordination:** the terminology audit (p1P8) may amend GDD wording and its
  phase-2 rename PR serializes behind 5.2's merge — your GDD edits must be
  SECTION-additive (mechanics/decision-log entries), not terminology rewrites, so
  the diffs don't collide. Silas serializes the PRs.

## Mission — turn the explainer's Section B design thread into canon + story cards

**User ruling (2026-08-15):** the Section B design notes are TASKS to be done:
the traffic model gains realism so congestion lives where it does in real networks.

**The four design threads (from the explainer, user-endorsed):**

1. **Narrow as residential access** — narrow pipes are the access tier (the
   last-mile); congestion is an AGGREGATION event (at routers/cores), endpoints
   never self-congest.
2. **Per-terminal demand caps** — terminals emit bounded, realistic demand; no
   single endpoint saturates a network alone.
3. **Aggregation groups** — the demand director spawns/weights terminals in
   clusters so surge stress lands on aggregation points (where the player's
   router/tier/bundle decisions matter).
4. **Diverse terminal types** — terminal variety (residential/small-biz/campus
   class analogues) with different demand profiles per type.

**Deliverables:**

1. **Design spec (lavish-reviewed):** for each thread — the mechanic in Given/When/
   Then shape, the real-world rationale (cite the explainer's 1G/40G/100G math),
   the balance levers (catalog/balance.json placement — data-driven per canon),
   determinism constraints (all seed-derived; no wall-clock; replay byte-identical
   or deliberate LOG_VERSION), and interaction with existing canon (E22 pool, E9
   bounds, 4.1 strain, 5.1 growth spawning, 5.8 QoS). Resolve conflicts EXPLICITLY
   (e.g. growth-spawn validity vs aggregation groups).
2. **Story cards** appended to stories-v2 (the existing card format): where they
   slot in the slice line (post-5.4? fold into slice 6?) — propose the sequencing
   with rationale.
3. **GDD decision-log amendment**: the traffic-realism ruling + the four mechanics,
   section-additive.
4. The lavish artifact presents ALL of it for the user's verdict; the PR opens only
   after approval.

**Scope guard:** design docs + story cards ONLY. No code, no balance.json changes,
no implementation — those are the story cards' jobs.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: pp-traffic-model-design
base: v2
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1
```

(Reviewer context from the review round briefing — scope + lens-guards:)

# Perkins briefing — round 1: packet-plumber-traffic-model-design

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/53 (targets `v2`)
- **Reviewed sha:** `72142044dac0b7f661355c9d4c139fbbd2123bda` (short `7214204`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-pp-traffic-model-design-r1` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-traffic-model-design.md` + the source design thread at `/Users/moses/code/_bmad-output/implementation-artifacts/surge-explainer/surge-explainer.html` (§Section B design notes — the user-endorsed thread) + the user ruling (2026-08-15: the Section B notes are TASKS). The lavish review approved this design — the PR ships it to canon.
- **Model:** `zai-coding-cn/glm-5.3` (Perkins reasoning tier — live). Launch EVERY lens pane with `pi --model zai-coding-cn/glm-5.3`. Interim fallback: `deepseek/deepseek-v4-pro`.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **CI note:** CI billing is FIXED (checks green). Local verification at the sha remains ground truth.

## What the PR does (review scope)

**DOCS/CANON-ONLY** (no code, no balance.json changes — those are the story cards'
jobs): the surge-explainer's Section B design thread becomes canon + story cards.
- **Design spec:** the four threads (1 narrow-pipes = residential access tier —
  congestion is an AGGREGATION event, endpoints never self-congest; 2 per-terminal
  demand caps — no single endpoint saturates alone; 3 aggregation groups — the
  demand director clusters terminals so surge stress lands on aggregation points;
  4 diverse terminal types — residential/small-biz/campus analogues) in
  Given/When/Then shape, real-world rationale (1G/40G/100G math), balance levers
  (catalog/balance.json placement), determinism constraints (seed-derived, no
  wall-clock, replay byte-identical or deliberate LOG_VERSION), explicit
  interaction with existing canon (E22 pool, E9 bounds, 4.1 strain, 5.1 growth
  spawning, 5.8 QoS) — conflicts resolved explicitly (growth-spawn validity vs
  aggregation groups).
- **Story cards 5.9–5.12** appended to stories-v2 with proposed sequencing
  (post-5.4 / slice-6 rationale).
- **GDD decision-log amendment** (M6 + decision-log entries): the traffic-realism
  ruling + the four mechanics — SECTION-ADDITIVE, no terminology rewrites
  (coordinated with the parallel terminology audit — Phase 2 rename PR serializes
  behind 5.2's merge).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 LOAD-BEARING — section-additive, no terminology rewrites.** The GDD edits must
  be ADDITIVE (new sections/decision-log entries) — this diff must NOT rewrite
  existing terminology (the terminology audit owns that; its Phase-2 rename PR is
  serialized behind 5.2's merge). A terminology rewrite hiding in this docs PR =
  a conflict-with-a-queued-job blocker (it would collide with the audit's PR).
- **Canon coherence:** the four threads' mechanics must be consistent with EXISTING
  canon — E22 pool, E9 bounds, 4.1 strain/forecast, 5.1 growth spawning, 5.8 QoS —
  and explicit about the resolved conflicts (growth-spawn validity vs aggregation
  groups is the named one). A silent contradiction = a blocker.
- **Determinism constraints stated correctly:** all four threads seed-derived, no
  wall-clock, replay byte-identical OR a deliberate LOG_VERSION bump — the spec
  must state which per thread (the 5.1 derive-don't-record and 5.8 golden-fold
  disciplines are settled canon to follow).
- **Story cards are complete + sequenced with rationale** (post-5.4? slice-6?) —
  missing load-bearing card content (Given/When/Then, balance levers, acceptance)
  = a finding.
- **Base = `v2`** — full shipped line. Carry-forward only; do NOT re-open settled
  findings.
- **Scope guard:** design docs + story cards ONLY — no code, no balance.json
  changes (a code change in this docs PR = a blocker).


(Additional context docs, readable in the worktree: the source design thread `_bmad-output/implementation-artifacts/surge-explainer/surge-explainer.html` §Section B — the user-endorsed design notes this diff canonizes; the GDD at `_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md` + `decision-log.md`; stories at `_bmad-output/planning-artifacts/sprints/stories-v2.md`; sprint plan at `_bmad-output/planning-artifacts/sprints/sprint-plan-v2.md`.)

--- YOUR LENS ---
Your assigned source tag: "edge"

You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "<your assigned source tag>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

FILE-OUTPUT CONTRACT (MANDATORY — replaces printing the array):
Write ONLY your JSON array to this exact absolute path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r1/edge.json
The file must contain the JSON array and nothing else — no prose, no markdown fencing, no preamble. Do not derive or alter the path; use it verbatim as given. After writing the file, STOP — you are done.

Output contract:
- ONLY the JSON array in that file. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
