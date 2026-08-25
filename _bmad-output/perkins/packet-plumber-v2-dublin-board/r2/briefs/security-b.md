You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. You are REVIEW-ONLY: never edit files, never fix anything, never commit — findings only.

Your cwd is the reviewed worktree at exactly the reviewed sha — every verification read happens here.

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
The diff under review is saved at:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-board/r2/diff-chunkB-goldens.patch
Read that file COMPLETELY first (read it in sequential chunks until EOF — it is ~1825 lines). Those bytes are the canonical diff for this review.
Chunking note: this is chunk B of 2 (chunk B = goldens/ data: the dublin_board T1 manifest + binary captures; chunk A = code, reviewed separately). Findings about files absent from this diff are out of scope for you.

--- SPEC / CONTEXT ---
# packet-plumber-v2-dublin-board

## Task

Stage 1 of the real-maps arc: wire the baked Dublin cross-section
(data/maps/dublin.json, merged in #90) INTO the game as the board.
User: "when do we get the dublin map? not in local v2." The spike
shipped look-only; this ships the city. Per user rulings (2026-08-23):
curated Dublin cross-section + streets-constrain-pipes — THIS job is
the board + spawns; streets-constrain-pipes is stage 2 (separate).

## Scope

1. **Board underlay**: render dublin.json — water (Liffey, bay,
   canals), parks (Phoenix Park), coastline, street skeleton — in the
   game's paper-map aesthetic (match the #90 gallery the user blessed;
   palette tokens, IBM Plex labels for districts). The board REPLACES
   the procedural terrain when the map source = dublin.
2. **Map source = first-class determinism input**: named tunable
   (map: dublin | procedural). Demos/replays PIN the map id — the map
   is part of the run state, hashed like a seed (LOG_VERSION-safe:
   old replays on procedural still run; new runs default dublin).
3. **Spawn anchoring**: growth SEED/ATTACH draws from dublin.json's
   street-adjacent spawn candidates at the 1-in-6 density (user's
   blessed level). Districts become the estate anchors
   (growth_groups interplay: cluster radius/caps apply WITHIN
   districts; document the exact interplay).
4. **Camera fit**: the map.* design-grid world sizes to the Dublin
   board; zoom/pullback (#89) works over it; minimap stays.
5. **KYLE visual gate**: the board must match the blessed #90 gallery
   (KYLE grades a live capture vs the gallery previews — side-by-side
   in the PR body).

## Rules (hard)

1. Streets do NOT yet constrain pipes — existing placement rules
   unchanged (stage 2). Free drawing over the real map.
2. Full golden re-bless EXPECTED (the board legitimately changed) —
   cause-documented; determinism suite green on both map sources
   (dual-run: procedural pins old goldens, dublin re-blesses).
3. E31 packing floors + placement rules still apply (spawn candidates
   respect terminal_min_sep_tiles; document conflicts if a candidate
   violates — filter at bake-load, never place illegally).
4. The extract pipeline is untouched (tools/osm_extract.py stable).
5. IP/ODbL attribution renders in-game (about/credits line or map
   corner — "© OpenStreetMap contributors").

## Acceptance

- `odin run app` boots Dublin: terrain, districts labeled, spawns on
  real streets at 1-in-6, estates clustering per district.
- Procedural map still runs (tunable flip); old demos/replays pin and
  replay byte-identical on procedural.
- KYLE gate: live board vs blessed gallery — side-by-side PR body.
- Determinism: T1/T2/replay green on BOTH map sources; dublin goldens
  re-blessed cause-documented.
- pr_review: 1.

## Skills policy

bmad-quick-dev; KYLE for the visual gate.

## Model policy

deepseek-v4-flash, --thinking max. KYLE: glm-4.6v (remote; local
fallback lmstudio/zai-org/glm-4.6v-flash).

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-dublin-board
- base: v2 (fresh head — post-#92 if merged, else current)
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- stage 2 (streets-constrain-pipes) NOT in scope — follow-up job


--- PR CONTEXT (implementer-supplied evidence, NOT verified truth) ---
# The Dublin board (stage 1 of the real-maps arc)

The baked Dublin cross-section (`data/maps/dublin.json`, merged in #90) is
now the game board. The user asked "when do we get the dublin map? not in
local v2" — this ships the city: the board underlay, the map source as a
first-class determinism input, and growth spawns anchored to real streets.
Streets do NOT constrain pipes yet (stage 2, follow-up).

## The KYLE gate (the #90 ruling's visual bar)

The live board vs the blessed gallery — graded side-by-side by KYLE
(glm-4.6v), verdict quoted from the gate run:

> **PASS** — "The live game frame accurately matches the reference Dublin
> board layout with consistent streets, waterways, parks, and urban density.
> The ~18 growth-spawned terminal buildings are properly positioned on city
> streets rather than floating in empty areas. No visual artifacts are
> present."

![Live game frame vs the blessed gallery](docs/captures/dublin-board/game_vs_gallery.png)

![Live underlay vs the blessed gallery](docs/captures/dublin-board/underlay_vs_gallery.png)

![The ODbL attribution renders in the map corner](docs/captures/dublin-board/attribution.png)

## What shipped

**1. The board underlay** (`app/render/dublin.odin`) — replaces the
procedural noise map when the map source = dublin. The gallery's exact
draw order + tokens: canvas → terrain (water/coast/park) → grid (18%) →
streets (arterial heavier, local faint) → the 1-in-6 candidate dots →
district labels (IBM Plex, kind-priority + collision-avoided like the
gallery) → the ODbL credit (rule 5, bottom-left of the board).

The terrain is rasterized once per board into a per-world-px cell grid with
the **even-odd point-in-polygon rule — the SAME fill rule the gallery's
renderer (PIL) uses**. This matters: the OSM rings contain pinch/retrace
artifacts that make them self-intersecting (80/80 water rings fail the
simple-polygon test) — ear clipping silently drops them, even-odd fills
them exactly like the blessed previews. The © glyph renders from a
dedicated one-glyph font so the shared HUD atlas never changes.

**2. Map source = a named determinism input** (`core/map.odin`) —
`map: dublin | procedural` is run setup like the seed:
- serialized into the T1 hash **absent-when-procedural** (the zero value),
  so every legacy demo/replay stays byte-identical — LOG_VERSION-safe, the
  log format never changes;
- demos pin it: `map dublin` / `map procedural` in the `.dem` header
  (absent = procedural — every pre-board demo is unchanged);
- the app boots **dublin by default** ("new runs default dublin");
  `PP_MAP=procedural` flips the named tunable back.

**3. Spawn anchoring on real streets** (`core/growth.odin`) — growth
SEED/ATTACH draw from the board's street-adjacent tile pool at the 1-in-6
density (the user's blessed calm default): the stride-6 subsample, snapped
to the integer tile grid, deduped + grid-filtered **at bake-load** (rule 3
— the pool only ever contains legal tiles). The ATTACH family draws the
anchor's **street ring** (pool tiles within `[terminal_min_sep_tiles,
radius_tiles]` of a member — the exact ring the procedural compass draw
targets, expressed over the real streets; the strict-radius closure is
preserved: no strays). An estate is eligible only while its streets hold a
legally-placeable tile (E31 + connect span checked ahead) — a saturated
estate yields to the SEED family instead of stalling the window budget.
The E31 predicates themselves are unchanged — a pool tile is a candidate,
never a guaranteed placement; every spawn is rejection-sampled through the
same `growth_pos_valid` / `growth_connectable` gates.

**The exact growth_groups interplay (documented per the briefing — the
STREETS RULE):** the estate (the derived cluster) forms on the streets the
grid gives it — cluster radius/caps apply within the estate, and the
estate's seed district labels it (the nearest anchor). The district
assignment is label-anchored; a street crossing a district's Voronoi
boundary keeps its houses together — the streets are the geometry that
binds an estate. The briefing's "cluster radius/caps apply WITHIN
districts" is honored as the estate-level reading: a district-scoped DRAW
domain was measured and rejected (63% of pool tiles have zero same-district
attach-ring neighbors — the Voronoi cells are smaller than the estate
radius at the 1-in-6 snap; a scoped draw stalls estates across most of the
city). Every pool tile has ≥1 attach-ring neighbor globally (0% stall) —
hence the global ring + the ring-has-room eligibility.

**4. Camera fit** — the board is 40×30 tiles == the balance design grid,
so the fit + zoom/pullback (#89) and the NOC rail (#92) work over it
untouched.

## Determinism (the dual-run)

| Source | Proof |
|---|---|
| procedural | **all 48 pre-board demos byte-identical on their old goldens** (T1 manifests + T2 pixels + replay gates) — the absent-when-0 map byte + the untouched procedural draw path |
| dublin | `demos/dublin_board.dem` — the new named golden: `map dublin`, era 3, growth on, 2 routers on core street tiles + a wide fiber; T1 manifest + T2 captures + replay gate blessed + green |

**Re-bless cause-documented:** only the NEW demo's goldens were blessed
(`goldens/dublin_board.*`). Zero existing goldens changed — the board is
presentation + the map byte is absent-when-0; the procedural path draws
zero rng differently. The dublin demo's 90s run grows 18 terminals on pool
tiles, with estates of 5 forming along streets (the derived cluster view
unions them at the radius).

## Verification

- `tools/ci-local.sh --mac` — **13/13 gates green** (lint, 242 core unit
  tests incl. the board/loader/growth pins, 77 render tests incl. the
  map-source decision pins, builds, the full golden harness, palcheck,
  drift, preview, motion, PP_DEBUG, stats, input parity).
- The app boots: `app: map = dublin (data/maps/dublin.json, 720 spawn
  tiles at 1-in-6)`; `PP_MAP=procedural` → `app: map = procedural`.
- New unit pins (Perkins r1 B1's advisory-gate bar): the 1-in-6
  stride->snap->grid-filter->dedupe pipeline EXERCISED (the fixture's
  stride samples land out-of-grid + duplicate — both branches run), the
  district-anchors parse (name/kind/pos + the label-rank table), the
  fail-loud table (15 loader error paths: every one returns a named error
  + a ZERO board — no partial state), the PP_MAP tunable parse + BOTH
  corrupt-asset fallback branches (map_source_from_env /
  map_source_after_load — the pure app decision, unit-pinned), the E31
  pairwise separation asserted across the grown topology, and the ATTACH
  strict-radius closure (no strays).

## Decisions & rationale

- **Even-odd cell rasterization over vector triangulation** — the OSM
  rings are self-intersecting (pinch/retrace); ear clipping produced
  overlapping/wrong fills (triangulated area exceeded the polygon area 1.5–
  3.6×) and dropped rings outright. The cell grid is deterministic,
  immune, and pixel-exact at fit zoom (1 cell = 1 world px). Rejected
  alternatives: fan+centroid (boundary straddle errors at coarse rings),
  ring repair (general ring-splitting, high complexity).
- **Global street ring over district-scoped pools** — measured geometry:
  63% of pool tiles have zero same-district attach-ring neighbors (the
  Voronoi cells are smaller than the estate radius at the 1-in-6 snap), so
  a district-scoped draw stalls estates across most of the city. The
  global ring preserves the strict-radius closure while keeping estates
  where the streets allow. The per-candidate district machinery is NOT in
  the board (it would be dead data — the estate draw never reads it); the
  district ANCHORS (the render's labels + a seed's estate label) are. A
  future district-scoped policy re-adds the assignment + ranges as data
  (the loader's nearest-anchor math is one commit away).
- **The board is NOT part of the log format** — the map id rides the T1
  state hash (absent-when-0) and the demo/run setup (the fixture
  precedent), not the action-log header: adding it to the header would
  either break old-log parsing or need a LOG_VERSION bump that rejects
  them. "Old replays on procedural still run" is satisfied by construction.
- **The app default is dublin, the demo default is procedural** — the
  user's ruling ("new runs default dublin") applies to interactive runs;
  the demo default must stay procedural or every legacy golden shifts.
- **One-glyph © font** — adding U+00A9 to the shared codepoint set moved
  the ⚠ AA pixels (2–9 px/frame) across 18 demos' goldens; the dedicated
  font is additive and zero-impact.
- **`dublin-shot` harness verb** — the KYLE-gate capture tool (fit +
  zoomed underlay frames); kept as a permanent verb (the PP_DEBUG verbs'
  pattern) so the gate is re-runnable.
- **bmad-build waiver (canon note):** per the standing ruling, the
  quick-dev flow ran self-contained (the bmad-build render fails on this
  install with `ambiguous config token implementation_artifacts`; the
  waiver is documented in the field notes).

## Out of scope (stage 2, follow-up)

- Streets do NOT constrain pipe placement yet — free drawing over the
  real map (existing placement rules unchanged).
- The extract pipeline (`tools/osm_extract.py`) is untouched.


--- ROUND GUARDS (user rulings — these are NOT findings) ---
- The real-maps arc, the blessed #90 gallery aesthetic, the 1-in-6 spawn density, and districts-as-estates are USER-RULED design — never report them as defects.
- The dublin golden re-bless is legitimate and expected; the bar is the dual-run determinism proof, not re-litigating the re-bless.
- KYLE's PASS (live board vs gallery) is the job's own vision gate — treat it as minion-supplied evidence; verify mechanically where possible.
- Stage 2 (streets-constrain-pipes) being ABSENT is correct — it is a separate follow-up job, not a gap.
- This is ROUND 2 (fix-audit): the diff's final commit (330b952, "fix: Perkins r1") answers round-1 review findings (loader test pins, dead-district-machinery trim, doc honesty, loader leak, map-source extraction). Evaluate those hunks on merit like any other — a fix can itself be defective.
- k3 vision round: genuine visual judgment is allowed (no caveat); still prefer mechanical proof (byte/hash/capture-diff) where it exists.

--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps
--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "security",
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
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

FILE OUTPUT (headless contract): write ONLY your JSON array (no prose, no markdown fencing) to EXACTLY this absolute path using your file-write tool:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-board/r2/security-b.json
Do not derive or alter the path; do not write any other file. After the file is written, reply with a one-line confirmation and stop. Writing the JSON only into the transcript without writing the file is a FAILURE.
