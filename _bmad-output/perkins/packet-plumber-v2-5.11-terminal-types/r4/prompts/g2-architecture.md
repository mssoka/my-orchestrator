You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. The repository checkout at the reviewed state is at:
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.11-terminal-types-r4
(all verification reads happen there; treat it as the source of truth).

Chunk orientation: This chunk contains the 8 largest re-blessed .t1 goldens as head/tail EXCERPTS (bodies elided mid-file with an explicit marker; full files are in the worktree under goldens/).

NOTE — round context: this is round 4 (fix-audit, cap lifted — loop until approved) on the SAME PR. The reviewed sha is the r3-fold head (0161c2b) — a CODE-ONLY fold on the r3-reviewed tree: the goldens/ tree is byte-identical to the r3-reviewed set (git-diff-empty, mechanically proven). Treat as EXPECTED, not findings:
- the wholesale .t1 re-bless / tick-1 shifts / catalog_hash-only diffs in .log.bin headers — the documented deliberate catalog-fold design; r1-r3 mechanically certified it (8-byte log.bin partition, 72-png byte identity, the splice proof independently reproduced). Do NOT re-flag the re-bless's existence; auditing its CAUSE documentation/consistency remains fair.
- every .png golden rendering the #67 procedural background tiles (rebased base).
- r3-certified SETTLED items — do not re-litigate: the honest W9 re-pin design (B1-r1: EXPECTED/window/campus-must-exist/campus-must-source, the grown-mesh start map doctrine), the r1 W1-W4 fixes (palcheck sprite scan, ratio-split windows, PR citations, inertness test), the rebase delta, the roster math + era gates, the #65 sprite wiring + canon shapes, the 7.1 sprite pipeline, the 5.9/5.10 accumulator contracts, the fair-crisis grown-mesh start-map, the fallback-model caveat.

What is NEW at this reviewed head — the r3-fold delta, exactly 4 files (+138/-17), the fix fold answering r3's blocker + warning + notes. Delta-introduced regressions are exactly what this round hunts — scrutinize these hardest:
1. r3-B1 (was THE blocker): test_role_absent_demand_inert double-freed the trimmed era-3 entries (deferred delete(trimmed) ran LIFO against catalogs_destroy(cat2) on the aliased array; odin-test's tracking allocator masked it in-suite). The fold REMOVES the defer and documents ownership. Verify the ownership transfer is actually sound now (no leak, no double-free, no use-after-free).
2. r3-W1: W9's crowd floor was vacuous (fixture pre-seeds 14 streaming terminals; hosts>=8 held with growth dead). The fold adds a growth-born count (node_id >= 20 — fixture spawns 20 nodes first, ids monotonic E11) and pins growth_born >= 1. Verify the >= 20 threshold is actually correct against the fixture (count the seeded nodes) and the pin bites.
3. r3-N3: campus-half floor now quantitative: campus_window_spawns >= 10*WINDOW*95/100 (was existence-only > 0). Note the literal 10 (campus vol 1 x multiplier 10) — check consistency with the derived EXPECTED.
4. r3-N4: test_terminal_class_profiles' SURGE_AT now derives from the set-piece (was hardcoded 1200).
5. r3-N5: W9's EXPECTED now derives: sum of streaming-class entry volumes x surge.multiplier x WINDOW (was literal 20).
6. r3-N6: run_inert now captures + frees record_run's hash stream (was a 2x4.69KiB leak).
7. r3-N7: palcheck unit-pins sprite_index_building (content_host->4, small_biz->9, campus->10, residential->0) and raises pixel floors (>150 small_biz, >500 campus; measured 176/1100).
8. r3-N11: NEW harness subcommand `fold-check <prev-hash> <prev-tick1>` (harness/fold_check.odin + main.odin verb) — the re-runnable fold-splice verifier (exit 0 PASS / 1 FAIL / 2 usage). Scrutinize: the splice offset (33..40), the boot run setup (seed 42, era 0, fixture), parse/arg handling, exit-code paths, and whether it actually proves fold-only-ness.


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
diff --git a/goldens/audio.t1 b/goldens/audio.t1
index f9f922f..fcd51b3 100644
--- a/goldens/audio.t1
+++ b/goldens/audio.t1
@@ -3,1405 +3,1405 @@ t1 1
 demo audio
 seed 4243
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 1400
-1 109e052a6ceb06d7
-2 8cde695a7f4579b7
-3 c2c7c285f5a71c34
-4 5afff0f4891353f4
-5 c0c2251dcf2f31ac
-6 de036dafbd26e705
-7 18a3ad88329db721
-8 8ae81da3e05466df
-9 e36d5597a411ee54
-10 5046872da01415ff
-11 246b4ecd34a10435
-12 7ead7998688d4ede
-13 6156fca273e31445
-14 69c95f5450d309d3
-15 27c0dc14b1acd03b
-16 01fb2e5780a1a916
-17 f338f13e7b43fc85
-18 641a50d9e8a2a840
-19 a291588334e8bf29
-20 ff6b5c8a82bf9c5d
-21 854011211a5445fb
-22 30f182820e93d6d6
-23 cdfe45e0ba0b56fb
-24 7c2829660f838578
-25 c0314196fb3ea0b3
-26 a68e413aef0474ae
-27 0a16a8cbad98ed3d
-28 182cda49c0eb84a0
-29 56376e59f6127915
-30 132fb253ca0b9cd3
-31 2a55fa73b7f5cde6
-32 4a18203d3696b242
-33 be598318543b7182
-34 c96536947544400d
-35 6a1c44d2d8bdd89a
-36 8bc2fef796063524
-37 4c09eba8c05e95ec
-38 b9b61a0a292499f9
-39 3c41d7cfc88436eb
-40 ab7eef88e1ea7a5f
-41 8a34c17dec23424b
-42 51c40995948b0d33
-43 0061e75a766adc60
-44 e102d2d39ac8b952
-45 8e2422436a12f937
-46 f63140e6c0a16bfa
-47 3f1042e9e6382742
-48 37460c7582a9658a
-49 a8e20b524ce42dca
-50 1ff2ddd47fafd97c
-51 c3bea12907827d4c
-52 c6a3697cd27cd51c
-53 ea1ccdf871714035
-54 e0761fdd8a5739b8
-55 73efef7f6b3e69cd
-56 cf79a61053821b60
-57 fc2bdea9bd3245d8
-58 5bf6385a6987fe77
-59 b4823b0a187aa906
-60 22da5fa4b5cd8074
-61 d79f037c002376f8
-62 633caedb89f495f9
-63 4723309d82d09242
-64 06540eae6780fa82
-65 0dca6b3089032264
-66 9fe2e1bd9739426c
-67 62f84218e18000c4
-68 53245e172a14d38a
-69 564829a27db96336
-70 bc709c16f5c72a4b
-71 a691f05899c5d7c6
-72 af069231f018938d
-73 4916e2eda00b7008
-74 2a0c02b5b4005d48
-75 9bfbc33f83b09cdc
-76 81de54576053cfe4
-77 5676b9b861cf6fd9
-78 040e62cb9a64eb21
-79 528d808138503652
-80 a1e8863310ef8b7c
-81 3320bf2d2aa4c103
-82 364f40a5eaa378a0
-83 ab592c48ef69d25f
-84 10d3cc6f112de18c
-85 caf4ad88ae0baabc
-86 00fc9d6ee76b3c96
-87 1c800a700356167a
-88 1c3281f91dca6719
-89 0b9f664f577afef7
-90 a0b7ba6724def250
-91 e292f29aac84a179
-92 8076ad1e854bc5c3
-93 3b1afffba9db05d0
-94 8e0e69a0a00417ce
-95 26085f9f07b858ab
-96 a04c45302c5a703d
-97 587c1ef813c4c40f
-98 407dbc657e5da4ad
-99 93ab49955f72dbc7
-100 4abddab2f60ca48d
-101 3121701506ea1464
-102 2d64898966ce5761
-103 7e1f53047f1469e7
-104 c27b4d744ef59ebf
-105 6cfefa02ba4d6c88
-106 225f50fa3844bbc0
-107 6ad2f0a6873d230a
-108 89350ce1d4c5b139
-109 0d2d03ac0fbad77e
-110 9cd992579a799e62
-111 62bec33de6ea6bb7
-112 f7eafd9085726e7e
-113 70501f5ff9656327
-114 1abfbfc1521423ab
-115 e4e3dfa3aa9e9f9f
-116 b977c8b0b8a7f864
-117 bba1275e056f1b2b
-118 adc90c21c3217947
-119 d416a1a52bf1ea2a
-120 63840bdc890b3ea8
-121 d0f4812934e2305b
-122 cdcb2741e2eb65a4
-123 dddddc04d05604af
-124 788be92162770b78
-125 32b8456769877d07
-126 c3fc5b2eece5a77c
-127 8bdfccba7037feac
-128 d37bc28ffd5115df
-129 4a7eea2789badb12
-130 7234cb91cd290272
-131 41dda898f481e19a
-132 5a58fc61d232ff14
-133 9f05b3b93b2fe378
-134 e30a2cd3854362e3
-135 b6da6e94497db585
-136 8eca3ed8537fd7f2
-137 ffc07b9b40d54981
-138 11bffd1049ba306d
-139 13847b0517bf2476
-140 9fc6e1c8ec70f46d
-141 23f22ae7024099f9
-142 e904dca61cc58df4
-143 16df0d0d99a055ac
-144 30f939f2c94c9e07
-145 425f774c8fb27705
-146 3ff2a4d0b9545c6b
-147 b0479bf3ea02ed3d
-148 1660928a76dd8cf7
-149 b89d4224ab47f2d0
-150 647b8d78e66a9f77
-151 e19d575e881db984
-152 ca76fcb050a12542
-153 53446db7bfdb3e52
-154 c6325768569dd1ac
-155 9d2073c42fd6b5f6
-156 6fd7c991f3757a98
-157 15b7bebbeb7fc390
-158 51bfc9e4b5cd79cf
-159 f340a7a1a64d1b39
-160 c363e0c0a88cf4f5
-161 3dd29fc134e67d7b
-162 11cd4ad022a1f8bc
-163 3a213dfdac83a9d1
-164 aa5accf5d3190fd9
-165 255f7ef29d16e863
-166 c964a93c2973f604
-167 a01a75123af28a82
-168 cea104457e01db97
-169 ce575f1698c7e417
-170 822f21bfe6c8f8c5
-171 b874aba25d4a27a3
-172 ff6f69ce166df9e7
-173 a7fa67f15785de81
-174 09ad7eeacc8735cb
-175 063d9901acf68ccb
-176 46b016f84a2aea3d
-177 c43ac88e0dabc690
-178 f2234ed9cfc71425
-179 c28ea81353a9edf1
-180 e3e6ed124aaae1ad
-181 1a9d483dbbd988ad
-182 192a175377949531
-183 9e71024b673ff28c
-184 6196ff73c02cd71f
-185 dbb4fbcbc07492d5
-186 9cbd008b665011c7
-187 47bd4644e2542ab8
-188 4139785d41149de5
-189 22de9a196c0c0611
-190 f82f027eead79c5f
-191 1ef7d191f9418739
-192 c307125877b01f7a
-193 d3638ddc7c5aee37
-194 15a653225324cdaf
-195 27902f0cb7bd5630
-196 aa17e538aa82cb3f
-197 ce1ac5ca3e678ee7
-198 16d7a29ff1af684f
-199 d79078ccf070f55d
-200 c0770c08cfc6bcb2
-201 6a993b4c25f4ec72
-202 30dd0f282b424c55
-203 41bf19a8e52c80d4
-204 42b6e8dc863d5b42
-205 5496e868dc0ff8f9
-206 3cf1b3f14ac38cf6
-207 b5bf5dbd2d0bef84
-208 13f81861f734ee67
-209 2852a234b9c89b43
-210 c5d9fa01c7df672c
-211 0e1543290eac6adf
-212 f905852e21226df6
-213 3473582351667300
-214 2530916726147384
-215 92998d7977013751
-216 d2a5ee6701d041fc
-217 e065d8f3cb21081d
-218 2303cce799d61afe
-219 64348c9aebf3742a
-220 ff9dce09ad5283ee
-221 68649ef2859029c2
-222 482f1c70d2e32c0d
-223 cc6461dd36a72d15
-224 272830e328f46de2
-225 14e3ae8ac7cbd33f
-226 809f30c56b0eb3e1
-227 310d196cebbb51e5
-228 86137096b095461c
-229 705c84afb5488bff
-230 28f236daf3030d0e
-231 fd35041510ed6b60
-232 15f9b78963920e91
-233 1890c4306af5af5b
-234 bdde47c513c89f92
-235 648b9b256ecdf6dd
-236 944fadcae2af547d
-237 0dbcaf7da984154d
-238 5e5ac71b91382061
-239 d429a07a289062fe
-240 370be579c869f999
-241 a13e81e314cc3c8f
-242 fd57effd949893fd
-243 fe50f83655cc3edb
... [2458 lines elided from this golden's diff body — the FULL file is in the review worktree at goldens/audio.t1; read it there if needed] ...
+1302 ec086ea1d6a018b6
+1303 1b93842ebf47d694
+1304 7b404d7c04593a7f
+1305 ab86d96529e8aa41
+1306 2f23270250413ea9
+1307 0e10abce889fefd9
+1308 c855394634cefe3d
+1309 059d1407e3a79a18
+1310 b5d60ef34aaed9d6
+1311 33fea7d4d0a2a8ec
+1312 a2b411ca865e6720
+1313 c90408fc91382fed
+1314 979bbcdb3031952c
+1315 a3311b4c1f379802
+1316 76048ea4522461e6
+1317 eb22793a9bd71f30
+1318 dee6c9f6c167a369
+1319 d65c6985285489e8
+1320 70a11ad6c7668047
+1321 c8e5de226f45dac9
+1322 3d0d9cb7f64eca05
+1323 f4e5c59377cd6bbd
+1324 39ca99162ba41b9d
+1325 1eb6ed476bf5b1ab
+1326 681cf7fe1fc08790
+1327 ce64b9241fbe3cf4
+1328 5227ddf272730267
+1329 fd07fdbe6c6ee478
+1330 ba8a51a51ec864fd
+1331 1c36710217160c54
+1332 5e8baac706e80ad2
+1333 78f3c0d49807df07
+1334 bc51f36f3b5e504d
+1335 897b1aae525884e5
+1336 e26f8674b67e4a78
+1337 137dc85606246d10
+1338 72ca3dc6b228580f
+1339 e81123aae2b22705
+1340 95c0fa82c09ca3a3
+1341 171020328ea9102c
+1342 3b71befc2d21a14d
+1343 3fe496c69ebafc36
+1344 3d492a52908a666c
+1345 0d917f5a69d0c32d
+1346 0022d0003ced655f
+1347 e988d617da76b13e
+1348 3ff910c7761a37ef
+1349 39121bbae0abd163
+1350 17e533aef3765ab5
+1351 d2a0b0b66816dafd
+1352 ece9681db4821cd6
+1353 10968c0f8888db7d
+1354 fa794ecd17e91d8c
+1355 1e95f4ccb4fb106a
+1356 829fbb5b4452d0b5
+1357 1cab889b0532a8dd
+1358 bfa153252f1d2ba8
+1359 9019f73b2e9f9e0c
+1360 c61a09062eef056d
+1361 07f9047be3573d04
+1362 f09f81280cb2fe23
+1363 7002a02bdebfed5f
+1364 0da41d5c3275321d
+1365 be075fadad828405
+1366 59f4974e2ed42bbe
+1367 510ad4058fb6265c
+1368 d4caa8855831526b
+1369 02589e20c13dd166
+1370 f4802a0d0915d746
+1371 44b377598415c030
+1372 104ea0314606d25b
+1373 5c5d96f9677f0a16
+1374 d1be7bbdfef6d287
+1375 a14dec58811abf6e
+1376 a894576619df125d
+1377 e596388be4e00c06
+1378 698b282e9e1ca0e1
+1379 df537f44ea8641a8
+1380 71a6a1bc373dc28c
+1381 51c658a4d3c57cb3
+1382 ce409b211f6e5583
+1383 66fd1ba5ff0dda1a
+1384 ba78a77b22584716
+1385 23ee5de73744cf8b
+1386 26ad1eb515282b22
+1387 459a1bbe05f03a94
+1388 d246a21982265134
+1389 470f47d436c7688f
+1390 8daea7a7763bbb4b
+1391 219cd4060a6d398b
+1392 7d01777c10966978
+1393 c14f68544c2021db
+1394 722f17dd759a96c1
+1395 557f45ab43066d9b
+1396 3e9e2e4d986b9447
+1397 4e35600ec8512fc3
+1398 ee23a5285fc53aa6
+1399 dbe5b970abbb3e30
+1400 9869c8277fccf529

diff --git a/goldens/growth.t1 b/goldens/growth.t1
index 4b258cd..dcc893f 100644
--- a/goldens/growth.t1
+++ b/goldens/growth.t1
@@ -3,1805 +3,1805 @@ t1 1
 demo growth
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 1800
-1 30a74aca339a8bb1
-2 59bcbc0e15a2fdc4
-3 483243215a56ca2f
-4 e8ffa4a34f22bf52
-5 bb12324e7cdc2885
-6 24f35dc72f6fb088
-7 8a23955081368cc3
-8 65691e92be18eb56
-9 26715d03654c00d9
-10 309c4f2715658f2c
-11 6e3b88ebf3561857
-12 ca37bac2ccfc9c5a
-13 682c00b956221eb9
-14 097365c5d5afa4bc
-15 885ff683f6613857
-16 a8f8fe4ec5eaced2
-17 4c70ce7b2c0863f5
-18 ecb6269f622e0658
-19 da1db4c36a3c1f63
-20 8deab0c3a676b95e
-21 3080cb4630cf3263
-22 ab526a97e45a7340
-23 243e385cc5827e8d
-24 0a55965a05ef11d2
-25 4e49ac6695bd597f
-26 ad2d856ffe2ca27f
-27 f8c60c0ffaa6c76e
-28 df37dab1bb4cee01
-29 668c7a250ea9f0d0
-30 7705e68bab1ea07b
-31 6734a7dd6319797a
-32 87924806a9064a4d
-33 80d46bcda65c5b4c
-34 f01d3f96b67a9657
-35 39f6fa2d31317ee6
-36 9d2d391a37f6be19
-37 5bf944042b1dd848
-38 c042965272c0a013
-39 87fd0f2e46fbbb7f
-40 5583c2b6fc80b6da
-41 be26f9404d143e6b
-42 60e832a2895c2674
-43 17239df0befe12bd
-44 836c7b679441b1fe
-45 4d21a8120a85b63f
-46 871af41e18e926d8
-47 1165f440eba5fa01
-48 53be13c121c40332
-49 7b8e18b7d0e15af3
-50 e04e1bafc46b2e3c
-51 fad739060e429b73
-52 1f87edb101037362
-53 7b8c0170b3cf63ff
-54 214d953e7ba7d71a
-55 2a7ac456353d6701
-56 b40ea6659b3d2844
-57 79663d4e526d53e3
-58 729da2bf651f694e
-59 9fc411efb662e3f5
-60 e438636cab544e58
-61 16bbd71b99a56227
-62 c785be2674890182
-63 8b89845c33951329
-64 d4d36363ec09b8ac
-65 ad3f50daea1927a8
-66 326e099686350995
-67 e8cbd2dec27ebd06
-68 60efd51b5da1053b
-69 6147d44dd8fe84fc
-70 96071a601343abb9
-71 1b98e4b4faa4779a
-72 8170b06be3420e3f
-73 a70ae78928f0a620
-74 bb076499ea67fb8d
-75 dc7f81b2023c903e
-76 6df8b3bcd9b575f3
-77 09249ac2422c5054
-78 11d3a7883b47bef7
-79 eb3693d8526e8ec4
-80 1abf65bba7d2cd9a
-81 4dc66dfde1799fd7
-82 467a3a1c2289fa0c
-83 03e76b38b6f3cd99
-84 ee1d82f187227306
-85 f450bc32b0eb4ff3
-86 96ea08f3e755fdb8
-87 9e589dd2d0725555
-88 2863faff3015d0c2
-89 bf1cebebadd9e69f
-90 f1be90393da66474
-91 8ec9d3f8847aca46
-92 43eb3bbeb6990ffa
-93 21575d3d6d80798d
-94 f6b9841d6392ae0f
-95 6e7fe1a9a10050d1
-96 3c15e56e2f8ab987
-97 f576c765e0cc6195
-98 c0ce05ab6d9332bf
-99 3a2c9cc2f8ac54a1
-100 db247eeaf6df6177
-101 ee4121ecad98d65d
-102 d9b285e3e02888ff
-103 9e77dcbcc2010451
-104 e27fd4ef9a9ebf68
-105 ef887efc16dd9368
-106 750fb1647d6b2e23
-107 786aaeceba6b9e1a
-108 314ac4e81259ab05
-109 685579f0aa9cdb34
-110 a2da0230c269c2ff
-111 25522aba025b8f66
-112 52c156eb1fd62dc1
-113 272da27c96024720
-114 225a05ae2bf4aa1b
-115 42eb686bc92b7b82
-116 2c9353942b4baedd
-117 434a0381ec294e9a
-118 26c6a615b58e06f2
-119 0c4ee3fecce9683a
-120 83c9e70d44cd1f08
-121 4210fceac21b3130
-122 ab68b9c41390eef4
-123 59ee9226e96dbdec
-124 4c0047ed16809e40
-125 8eb4e48c67246c58
-126 2cab7c9ab401d8e4
-127 467fb08b1da7f7fc
-128 6a6cba4f80498878
-129 9743c568b9530260
-130 89c83176024b0964
-131 b39563a131b593cf
-132 f3025d2a63f1f03b
-133 61706ce00d9cd1db
-134 6b9905dfec562e29
-135 e0b765282d1316ef
-136 54cb36b40fabf1e9
-137 fa5effcf988f9e7b
-138 02625642a55a2dc9
-139 3b94b309314095e7
-140 8472f5c8299aef39
-141 1927168c49d81fdb
-142 13c51a7ba2adbf39
-143 ef2b11f0df229933
-144 186c8aea0938fa33
-145 f2b614962fdfa3ea
-146 1ce82f2188259d0a
-147 522df1ef5d49de76
-148 040c028016f0b5de
-149 cc358561f1a66d62
-150 eaaeed2fc14dacc2
-151 5b616265897a4c56
-152 7e3da1d5934418fe
-153 e1945f49c1d33b6a
-154 52eda64687285aea
-155 fd74ac8cd9e40986
-156 250e42bc940338ec
-157 bbfc2ac7c852b0e7
-158 4be7284894851666
-159 619cd9c512f12fb8
-160 0b9430d1c2bc0867
-161 d791677bb1a67039
-162 47018d277eb070a3
-163 0403bc1055e88ef9
-164 4a6fd350e0938227
-165 3d2976fc600d0d99
-166 2a252a55b1e9011b
-167 868d4bbcd31e0169
-168 9c916cbae1826f77
-169 e2754a29da3eb892
-170 911f4ac797c7d721
-171 ab87ea04d9fff464
-172 34685ac15725bf6a
-173 f44312f118bbb148
-174 92449e4ee936d203
-175 8256f82b242d7692
-176 3f3e356d9c54ee55
-177 ee5a584500b032b4
-178 7edf9ccd70efd437
-179 549734019e15471e
-180 f2b7b68cb9556299
-181 21ddc86e6d53cc00
-182 866c6a2be3c83852
-183 77e09a62d978871a
-184 f9cb1768ce911837
-185 73c920312d622615
-186 d1252ef9ff7887dd
-187 c564ef821a2bd195
-188 02d62cac5262fe3d
-189 2dbdc79da10ac2a5
-190 22178ae70ae8b8bd
-191 e0e5e090aeb7a7d5
-192 6e6019e934b8838d
-193 39decc2313d065d5
-194 e81818caaef044cd
-195 03ff03fd45d8d3da
-196 c68e12e6542bb1c3
-197 34fc1424ec9795ee
-198 26e8d3b8809e3164
-199 d0caf8bfdfe2ef93
-200 37370150dadd0053
-201 d4e06a97f6557404
-202 21f0b323f3ad9281
-203 3e7499caaee4136a
-204 e144a3f62ab70867
-205 bcac71ea59c09f08
-206 e9b2ef94be3007d5
-207 d71327e29b01da8e
-208 ab787d0a4df52f7f
-209 3dfbc2fc0ba42732
-210 e2393a8b63d0c4b4
-211 ea404c68d4ee47ea
-212 455cf1b73e213e8c
-213 3ad45e50e2aa8f46
-214 c3a7810b40351634
-215 7b4b98b748995182
-216 22d0260e649b33e4
-217 3907032bebdac2d6
-218 f0f754cb6caa8f3c
-219 e66c3b8bcd8df68a
-220 777073477a62420c
-221 3a145a2635b61702
-222 77616e22e1a03e48
-223 2459aaa8b4c12881
-224 9166561d71cee321
-225 ea1501db9c4dadac
-226 506625d4309ca233
-227 122206d2c20f7df6
-228 878d509f012632fd
-229 8bfdbdcf440bfb70
-230 d2c0e46124542e6f
-231 b330fc50d82f429a
-232 36bfeacc17f2d2b9
-233 45275a4f581f6634
-234 28090f4b55c9d999
-235 9dce104074a05d50
-236 77cf74628c161625
-237 14ed019ff5ad1bdc
-238 6b07433f697f6008
-239 c4dcb016490c44c4
-240 33e6300105b24017
-241 559016d88c5a9e63
-242 3106bca49efea547
-243 993ff3813b1c85ab
... [3258 lines elided from this golden's diff body — the FULL file is in the review worktree at goldens/growth.t1; read it there if needed] ...
+1702 44e04008cecc53b3
+1703 ed1da79f7ce710d8
+1704 aaca8746924d169a
+1705 8ec5a93d91640aae
+1706 1c0de227deb6890d
+1707 b6eec5210275108c
+1708 678b89f4422a5582
+1709 35ba112369c26525
+1710 e51cc7bd173114b2
+1711 0c35f061d6c18051
+1712 4fddbd161f22cbb2
+1713 208b416ef7ac87be
+1714 e2e4e3fd9fffea02
+1715 38ac34361883d40e
+1716 973aab44940b26db
+1717 54cf95a38cf8b4ff
+1718 642cd46e40f3e2dc
+1719 d69ed73547a4b0cd
+1720 38edc373f6061f73
+1721 0577a404adc2f7f0
+1722 1faa946aea23ad63
+1723 216d5a7bebb6a6a2
+1724 5d1f687106d385f6
+1725 3a626c91bcaeb3b4
+1726 061b218ba57097e4
+1727 087f8c6316b17c60
+1728 e2370d9fe36e6dba
+1729 b2ea3b63bfda81d1
+1730 87cb46b181a2b30f
+1731 2d2172d872e611a2
+1732 d5d31aad68120603
+1733 f59c0f9d19e1411a
+1734 8f7864a1ca9c9062
+1735 7075bdf5b81b3c1a
+1736 f163ff4ba34699b7
+1737 89e13cb8618d1f76
+1738 36fc2b1b28505800
+1739 35a07007a2d06685
+1740 15a96cf5404969c3
+1741 e58422e1b0266f6b
+1742 7128ed1433ee0ee0
+1743 399c4bf6a998a865
+1744 bca291d6917e9a2f
+1745 89b26a49f5abb682
+1746 8c17a90a9741a04b
+1747 b6923f48430dc30c
+1748 7efe797b3157bc10
+1749 db6b93f0424855c6
+1750 f6564ba422efcd8f
+1751 efaf28931acaa58c
+1752 e4a572be79e13205
+1753 b0e4233cc3d29687
+1754 27aa8d51392780c6
+1755 9b72e437edff8d5c
+1756 c8883a6ce17517a9
+1757 c1eb2dc48935ef22
+1758 84722d0fd83e5c95
+1759 0adb3c171e8c5e60
+1760 dd72ddec9baaae6a
+1761 ac314c642ed4b77f
+1762 21b75a14bcbd1021
+1763 2695389d87509061
+1764 66d674b78a10e53f
+1765 9f24574aac7d8207
+1766 0d241e6dfca8db55
+1767 cb45c559fb68c4fd
+1768 beb1da59eb552578
+1769 f09cc76ecb58fa0d
+1770 78e90cb6d1c13cdd
+1771 88dfa8ed1a4d1920
+1772 3b1beceb7831e41e
+1773 ea61eccbb8d3edc9
+1774 4fcaf8f4b24d2bbb
+1775 5ad08530949b45ad
+1776 5de4a204a8fac995
+1777 b02dcb2515728fc5
+1778 626ac28c7def6a3e
+1779 aef1cbd8d435cd99
+1780 c9ca41daa41e8a3b
+1781 8a4618243bb5c2f3
+1782 769a4ee9e0bc6094
+1783 5aeeefc8cf478550
+1784 b3dc7883f2b128d6
+1785 fd62d19e87f9859f
+1786 25f0f80b0e89fd07
+1787 41ef7069d327067c
+1788 5af7c55dec8e63fc
+1789 8ac077aad8eef5ec
+1790 7672778540473459
+1791 f23bf9e109038e1c
+1792 ffc933b96aa69ea2
+1793 c8235bd56cf71a5e
+1794 96fa743cdc85d7d8
+1795 e03ba149c7bb7fee
+1796 8d0a64d8abdfc990
+1797 c81a73280bdf8e28
+1798 95a56beb5fcfdcf5
+1799 f3d39d2865dbaf6a
+1800 b84f82fdce40c125

diff --git a/goldens/health_win.t1 b/goldens/health_win.t1
index e1ef0a8..8605b48 100644
--- a/goldens/health_win.t1
+++ b/goldens/health_win.t1
@@ -3,3045 +3,3045 @@ t1 1
 demo health_win
 seed 4243
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 3040
-1 49d1a54cd2701578
-2 f92092c1eafa59fc
-3 6c6f537bfbc6a47e
-4 ad6689c1ea5c9ae2
-5 a0ba2c08f52567a9
-6 3d83d599be2bccd1
-7 3dc42207e9883a9a
-8 caa2530ae4259ab4
-9 ef8f4f7ff1474417
-10 2c130a5a03a7d323
-11 500cc3a7729a13f3
-12 1f4950316b0534ef
-13 2d43f9a0b3fa6b88
-14 7964d5c1b7cf3dff
-15 8318a2077ef3e5a7
-16 3ddd89f687317e0f
-17 d911363b3bb354e7
-18 decf558d4068b4bc
-19 503242b06d1a3179
-20 88d7cecf4541279f
-21 8fbf4bb9d6dc7e5d
-22 c706eacf69fde297
-23 408f7942ab00c10b
-24 ab1f20422d0f159f
-25 9642bc37881ececd
-26 94741739e26cb3b8
-27 50a5192401a04919
-28 11d62f078968b1cf
-29 fc9341496a23f3ca
-30 79a0f49dcf1e2dc2
-31 44406e7ae3b288e7
-32 d5c3edd79067dfc5
-33 98f8b562504cbf12
-34 0085cac5614fed62
-35 fe47914960246701
-36 453f8138bc00fe79
-37 dd9bb57e77b9e101
-38 a994d137b1a463b8
-39 af3940da3525112f
-40 e6429178485b9331
-41 25283e3ee0b6b48a
-42 00734ab07206ae57
-43 96cad61f7fd38c39
-44 271a335be3298262
-45 64e0c7c9150bdd4b
-46 5ea20b8e8309e054
-47 903924a5785ee5dd
-48 95429e808804bdb9
-49 c10efba2cdf6dba6
-50 af41cdab76fd2f62
-51 01bc3d27027fc646
-52 ab8d4cae54c00eb2
-53 5641551480692dc2
-54 fd38aaef25d996ba
-55 c5cec50ea6f343b1
-56 516af67d1a0b0f3e
-57 32e4feeafef7fa38
-58 dfb5a52e71a37edb
-59 38e5e57757e9c9a4
-60 19d2717efac01ad9
-61 f7d829cae4339ae3
-62 8fe05692a41a3c4a
-63 d7da70e1b865fe38
-64 42739b373dc14b60
-65 d2effaf1f34ff8ab
-66 d3db1bb2f212c525
-67 bcb98ea08e23ed79
-68 4452cacea0983ddf
-69 349ca89b5531b62d
-70 21685332e4e325e1
-71 2ee2b18ec72ac44c
-72 8e55c72eda5575d0
-73 e7706c1ce53ddab4
-74 20b87d854332aa65
-75 7b870282a392d1b3
-76 e4acf5aec02bdedc
-77 95a9a6ff7114d06a
-78 d92f34157fa05a48
-79 6c2db0d5d8e10405
-80 c151c573f8d93b76
-81 73dc559fb7411bad
-82 346495cdebc58d21
-83 94c42f775cb20718
-84 5b11430e5850b8ea
-85 2f3c2aa45ba51eb7
-86 0c0ddf71ed7e046d
-87 e52fa5ed298cfc51
-88 1b7f1832b9ae1371
-89 8748d51dda34d5e8
-90 1198ea49b2befc9d
-91 1361bab57002b1c2
-92 c03c181b107c731b
-93 934418fa3db66f2a
-94 374bfad691a5cf21
-95 57e3263729b33345
-96 5602f5b7d2c63359
-97 f5c7b4b284857768
-98 b0c1b74f2042b9b6
-99 b5c3596ccf3139c2
-100 afbf81bcd28a149c
-101 8ac4457b7d15183f
-102 d5792910eb6870b4
-103 b2ee8cdade6c3e6f
-104 ccc5c9ac2ad4c0ac
-105 dd4be0eca275c5a8
-106 748b6f1075dc04b8
-107 7202487e8d18cb1c
-108 549194b3da3c9542
-109 930f9f30af10aa61
-110 90af3105cce0ca7b
-111 840c3e2981a9fc70
-112 3878a9711dfe1a4f
-113 57e9eb3a301b564a
-114 0c601582e38950da
-115 492c617948f86a28
-116 b15f0dad03e08f90
-117 baeaa20ac1fef7e5
-118 1fe394ec6497a31a
-119 a0fbe05209abd6c8
-120 bfcbf5bb9f51ff9d
-121 4ca8b21bdf10c636
-122 48c713a3c07a009d
-123 67143398f954cad1
-124 e78daeb753281918
-125 55945a6616a8b182
-126 696fce22c82f5a01
-127 96c731be62d55a78
-128 d1b48d34f596387c
-129 ea75fb7e40034042
-130 f9d267db28795714
-131 625a101c7ca60aef
-132 084bfd7e10153fdd
-133 629d2b3d57b72769
-134 1a16671feed5d6b0
-135 5005ad242a0f5c1a
-136 7b07ea7c19dccf20
-137 4079e35fd6b74fff
-138 3fbff1a0bfe14c3c
-139 09003b216eb56c7a
-140 6605d1ab2ec6e163
-141 81c076dc43ccaace
-142 97e1d1417d0d823d
-143 40b2097405a090a6
-144 88e4e867da11cb79
-145 847fa0e7e514f699
-146 f1aa2dee7e67d303
-147 f9bc4556f57d02d6
-148 875db736eb077e30
-149 fe65ba99b55cb333
-150 7eb0ce3f38ec9df6
-151 dcd9490cf96e7369
-152 e3ac40d5fa50daa9
-153 15dd443207ce8309
-154 edab250981c2a504
-155 c31aa599eb0f00a5
-156 60cb879f38c21d6d
-157 f6908a950a90ed33
-158 844204ad2e5cf6eb
-159 73b18a7a9ca4b5b0
-160 6b0306428a3229d8
-161 f436362096097bb0
-162 6f6f755745881708
-163 ad4c6c37abab273a
-164 288e8418b3438242
-165 3464090ff862711b
-166 c34bd85ed231fb55
-167 6d77fff21ec4b40d
-168 ab5e5243be7cf257
-169 20e4ac47a640a4b5
-170 d87d1c626279ecad
-171 cea2433eb168a3ed
-172 f57df877c5214c60
-173 9240581dd2d729b7
-174 b2ede2e3d637c03f
-175 065b36708a30cb43
-176 a2ec52461d1ee2b3
-177 37e0b3e0b130b0f6
-178 aacfec3ac51b189c
-179 49154aebe7af4b73
-180 201b26903c8b859b
-181 eccaa980cd7b1b80
-182 66ff39503d41d7b1
-183 0cc337f0fa9b7959
-184 4b8ab8455bfd0d86
-185 8d7d432250cc909a
-186 3a121b80400252d9
-187 328ea7f922109523
-188 93bbb47e2adcb0d9
-189 2f14052be60d6c08
-190 fbd16182d582a545
-191 26aa3aeaa13014d0
-192 e7309e5fc19c6646
-193 3e07752b82a7d7a9
-194 cc6c13bf97c9517a
-195 5cb5d3408c999444
-196 bcdcd4688da451d0
-197 e16d6ea02dbd3f3b
-198 d7d4b6da30e15f4f
-199 973dfdfcec2fc890
-200 ce59fa5f30847177
-201 f46227611e3cac23
-202 7ab075a847fb522f
-203 7299fa6adc09305f
-204 4df5860a6ce47f08
-205 65e7b6a0433e3cfd
-206 5d70782ed4f9ec75
-207 a78a446a860a66ef
-208 1b244a94dd4a87eb
-209 f522ddc17e467202
-210 8b7f4ddff38fb9cc
-211 502587a37e9d9fcb
-212 52b2929f2070d9fd
-213 f84f9158f21d2b4c
-214 1a24d2e51a06a0be
-215 aea3d000cefe33b6
-216 d776d7a9467d866c
-217 d52cb34cd1afb2f6
-218 1aa276e28631f39e
-219 a871a01a4cab450d
-220 baab46c581d84feb
-221 d2ab5bf226af07b9
-222 ca0981afed5c8fc8
-223 1033f3bc1e3f9f98
-224 2a1a9fe6fb87a67a
-225 004993dff4706ee6
-226 a20772cf55b2f527
-227 d107759f9ee36f08
-228 aeec6923fd3437bb
-229 f689c156aaf0608d
-230 77f7cd4e043f4318
-231 2ad34264fec55fee
-232 40188aade3e6a475
-233 60d7055759a17437
-234 fd108d55029756b2
-235 8ed73eb7f5449428
-236 b4a7fc5a4914766a
-237 033a8d6cee6025c3
-238 e7a30d1804cf600b
-239 ac143ae2803caa57
-240 faaaa6b74ed5a453
-241 c173458fa1948bae
-242 9e53e5c0ee8f15da
-243 da361f6cf5dcfd6b
... [5738 lines elided from this golden's diff body — the FULL file is in the review worktree at goldens/health_win.t1; read it there if needed] ...
+2942 4745f4cc47eae828
+2943 6897d20e912a1c9d
+2944 5b97a7d7ad9ca254
+2945 df3c1f5427012547
+2946 87183dbe25d39ee9
+2947 77ba9ecbe33b2add
+2948 9f3d0fdb44050675
+2949 bbc2b88b9b6f27fb
+2950 b091f14512cd51a5
+2951 2338078395e13865
+2952 87da1821fc212b31
+2953 7575b5ef13e7f21e
+2954 e1dc2a4bd9346ff5
+2955 301cb1e0c9e7492f
+2956 238428af9122f070
+2957 e20356d5ff36f998
+2958 15e82c74e390187b
+2959 6a63b67da297d6d5
+2960 2a7437dc5750daa1
+2961 c7f17f4cc97b387d
+2962 057e57c5ff5f658e
+2963 fb853d3298674e57
+2964 b0fd0c7fd8513c9e
+2965 c592ca63c01ee95f
+2966 6606dd998291a3ca
+2967 dc116b44cc6b7519
+2968 7253a117bc8cf2f2
+2969 fb21df1a0f11b185
+2970 f16688a46c13a08a
+2971 8bf25710210026ec
+2972 f3e09acd5167788a
+2973 b33508820413576e
+2974 06660f1e4ef988a7
+2975 560a9210816a8378
+2976 68fec937a397b0c1
+2977 4bea8afacf2f02b2
+2978 e157e4148ca68946
+2979 3f0952848f5f4e67
+2980 e39721cc16989146
+2981 1ef8a8668a83cadf
+2982 a108e6e76cb3723e
+2983 0d51cfe4ce7ec1b0
+2984 5d9e62e5585fce7b
+2985 107eccc62dcb6bc7
+2986 16a4a97c35ea0dd4
+2987 3a150a740e36c243
+2988 e051a259bf1ccc1f
+2989 7174f323924906cf
+2990 29a518580b61adb3
+2991 1f9dc62be5803aae
+2992 521e65b9356da370
+2993 695a3aea55db4d92
+2994 39ed675ea6fc49e6
+2995 f74f77cde0ae4b77
+2996 f674ceda608d7714
+2997 435dc336f48d3b32
+2998 6325f5716acb59d9
+2999 bebdc5b483ba443a
+3000 5aded1a259d05110
+3001 9350b4e377b8e56f
+3002 9350b4e377b8e56f
+3003 9350b4e377b8e56f
+3004 9350b4e377b8e56f
+3005 9350b4e377b8e56f
+3006 9350b4e377b8e56f
+3007 9350b4e377b8e56f
+3008 9350b4e377b8e56f
+3009 9350b4e377b8e56f
+3010 9350b4e377b8e56f
+3011 9350b4e377b8e56f
+3012 9350b4e377b8e56f
+3013 9350b4e377b8e56f
+3014 9350b4e377b8e56f
+3015 9350b4e377b8e56f
+3016 9350b4e377b8e56f
+3017 9350b4e377b8e56f
+3018 9350b4e377b8e56f
+3019 9350b4e377b8e56f
+3020 9350b4e377b8e56f
+3021 9350b4e377b8e56f
+3022 9350b4e377b8e56f
+3023 9350b4e377b8e56f
+3024 9350b4e377b8e56f
+3025 9350b4e377b8e56f
+3026 9350b4e377b8e56f
+3027 9350b4e377b8e56f
+3028 9350b4e377b8e56f
+3029 9350b4e377b8e56f
+3030 9350b4e377b8e56f
+3031 9350b4e377b8e56f
+3032 9350b4e377b8e56f
+3033 9350b4e377b8e56f
+3034 9350b4e377b8e56f
+3035 9350b4e377b8e56f
+3036 9350b4e377b8e56f
+3037 9350b4e377b8e56f
+3038 9350b4e377b8e56f
+3039 9350b4e377b8e56f
+3040 9350b4e377b8e56f

diff --git a/goldens/juice.t1 b/goldens/juice.t1
index b886067..2aa5236 100644
--- a/goldens/juice.t1
+++ b/goldens/juice.t1
@@ -3,1405 +3,1405 @@ t1 1
 demo juice
 seed 7
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 1400
-1 41b50ae1d09a7229
-2 3e435902bc369763
-3 6b1d57b4462b3e33
-4 a10eec92d94556ba
-5 accbe82da2b5277d
-6 aee90d4739d79822
-7 0dbe3367e4315982
-8 2200bf631503f377
-9 e5003544a0dba114
-10 dc4d381d255abc82
-11 a3afcbea29c07d66
-12 9ef10863043bd196
-13 6b3365bab4496d5c
-14 5d0d643a59fa7fa7
-15 45ea3a5a74086e84
-16 0ab36a27ad66f7e5
-17 9461753c96149909
-18 3f7dc0bed597e055
-19 267d5b116f97b4a5
-20 56c1faa613af6dcd
-21 0089d1f2564bcccc
-22 5bc24da3d3e0d510
-23 a2bfd7328c27cdca
-24 52ef43d0a444459d
-25 05fa0eb3f0d5593b
-26 10c9ca339285e241
-27 56235be0d0f79e30
-28 67dcef0d401622c8
-29 677b6968994e831e
-30 b03f34a4521d1ed0
-31 0aa0025e39f39275
-32 7c412755778357a4
-33 11968662b8ad9cc3
-34 8d51ed284455b75f
-35 6fa160eda207f93a
-36 7f29f88ad29430d8
-37 601a0d08d555a40e
-38 5891f7749665035a
-39 51fae35c31c0a59e
-40 ee3b512f892eb0d3
-41 70890be732299dd2
-42 54e3832de79722f1
-43 431b75ea025ab39a
-44 9992347fc01f29f0
-45 7930aa43fe0c30a5
-46 48896cdbad5520be
-47 310573312904b399
-48 3affb62c79e476d0
-49 f16e108eafd4d8da
-50 261cedc6c5dfed5b
-51 ec17f43bbeea4030
-52 3941d09f4dcb00aa
-53 f3728bbbe201e0d5
-54 d6175ad1f0671cd7
-55 f7721ef31bf134b8
-56 a75de0dc123c68c5
-57 3637ec2d0eecce12
-58 1785981d0098ebad
-59 ca1666dbe52fc526
-60 a490825844dc3f16
-61 91113ff0c026d2c1
-62 fe3733adc514cb56
-63 40fa6cca5d468654
-64 5d107e1a0cd62aaf
-65 ba6a462a7cd2f7d8
-66 3c44fc606d285aab
-67 a3844447242b25d7
-68 1a5004efe2737c0e
-69 ab595ab120032608
-70 207aede10f35e4fe
-71 ce0f465cdb58219e
-72 9e2e61e09ddef02c
-73 4ce247102bac6258
-74 10f2181d36502292
-75 3c49797887a4ec8a
-76 75ce789923e11637
-77 fb7fb430d2d32e5b
-78 49db0df34ec519e9
-79 1911e86948d3967b
-80 83ff9b616c2ab6a0
-81 9b3a1021264659cd
-82 241e28d43fcd9049
-83 28b7023883433ce1
-84 e40e1aaccc4cf8ac
-85 96ea45a99e98715e
-86 2fe9eefb2a9b9963
-87 9cb17ad25b64b947
-88 2ef157785d745d1e
-89 17534e31e78c865c
-90 f09390aa459e9635
-91 7f5bf9167d167219
-92 aaf8a67aafeb0e2c
-93 a3c51c1478edf491
-94 765ba78eb7b786e4
-95 3d9e4256f3470014
-96 79962d259c996ec6
-97 36e2a2a4e49e0e2a
-98 80dcb9881a08c584
-99 e38684dfe62f3786
-100 43a8e4b088e5e384
-101 f47205de94407639
-102 7c0c0473ce8d176c
-103 e89619a8499c2946
-104 149c10be974e1046
-105 534ef4e285910218
-106 91013013f7cdbbf5
-107 eb319a251660c4b6
-108 3895d6d50db0dc02
-109 9faeed87785cc1dd
-110 67483ecb20653f25
-111 20fe418fa2f99fa0
-112 57c8f7c45c5a8645
-113 2a1d6a2d7f89ab79
-114 0b92a2ac3094cbb2
-115 acf2007cbf571ac7
-116 b238eddecef1faac
-117 e37d805380bd19b6
-118 a12050969bd0fe95
-119 25401beb169f45b0
-120 b23c12db61f0795a
-121 36659edfb8de69da
-122 bdf8e0ad7d59c217
-123 5fc925a3e1ee8273
-124 b1588b628ec17fe5
-125 ee5949ba5d4c9372
-126 a1ced89dd6708b32
-127 111950432b77048b
-128 956bb70ab14f16d8
-129 8eae7e9987a5e35e
-130 0ed671d2214548d1
-131 ca01c64da5233c90
-132 b9aa4b96a8add6bc
-133 b9be987d41c913ff
-134 0061b736c5346446
-135 4aa308f33e3e6320
-136 8b2bbbafc94750a3
-137 6899fbf25402212d
-138 bf42be50f8e6c5b3
-139 2321f7d17fdd4b50
-140 c7fe792caba7e4ef
-141 4b4e1681b35a982b
-142 e14c1de4c97096cd
-143 4ac47b82fc3a04d3
-144 ed096203b0b136a9
-145 5e62398dd70741aa
-146 2e94ea6155f0754d
-147 0231830b061f7772
-148 fb2f2eddcb439297
-149 d4a35683526cd595
-150 b5ccbceed241a140
-151 ea7945cde3e28656
-152 8ada060e80647e6b
-153 1e8fa5f921cdc882
-154 6a994c72226a9510
-155 dd3253ba8aa12b27
-156 196a78c33674d6b0
-157 ebc753108f03d5fd
-158 9046086935399cec
-159 cf3f2722c7aaca28
-160 b5d4c2a2e513ed43
-161 4cbebfa0e348abf7
-162 47519717580310a1
-163 73b70f3269eadcb5
-164 10497fcc6d959fc1
-165 10e03dcf2ef71d80
-166 8fb79de65fde019d
-167 d6cd7ab742b25510
-168 1509e9187b7eeb8f
-169 9c2663bccadbe828
-170 ad21dbb9949eb727
-171 bad7d17d7f92beac
-172 2a77231e014a3328
-173 0a8f44a3132fc5d0
-174 3a2c1883d4475dd7
-175 fbc9e01e35f5aa7b
-176 c566441c7713d555
-177 9a6100d212330348
-178 3bb9482d9347eff1
-179 c17adedc2705a3ee
-180 a2733ab905422c41
-181 12d3f19a5ff70332
-182 9aed94bd80f3b474
-183 4076e520db0d95c7
-184 150a1e5da33dcd08
-185 c1238162fa124220
-186 63ba4b6d307d82e7
-187 c8353e13b63bf802
-188 a3172ec74f070562
-189 040dc478ef90b2c3
-190 d3d77eab24cac040
-191 090443a383db6847
-192 940c27dd31515289
-193 2cb84b9b210b8f8a
-194 fca776764651392f
-195 acab646db82b7355
-196 e8faf0de43b975c3
-197 31ff6c93425a8d5e
-198 2f39e7a39c0914cb
-199 568dd2b4ef166f54
-200 a868af64ea117a9a
-201 e09918a7bdbebcd6
-202 370f31ec23687068
-203 0b67d060914bbcb8
-204 04f1ee1205ea31b7
-205 3331e4f8bcdfd78a
-206 f3ad0b53b9242cbc
-207 c18d10d5d89feef0
-208 5218bffb0b44bd61
-209 adbf721ee1decb6c
-210 0d01c142c718c0a0
-211 9b086ff2bf356e4f
-212 2f5bfb3cbb68cd8f
-213 4a1e8c845664855d
-214 7cbaea5fd92f4029
-215 139519ac78203bed
-216 30e518594210a484
-217 d0158e0635d52595
-218 f0422f0b80222ae4
-219 4a1f880f19bb3076
-220 a6d9719ee18bdce0
-221 1c454290ac869f2a
-222 cbd299133fe53448
-223 17d190efe6a28eaa
-224 886491381db53e81
-225 a6d8c0fa46948ec2
-226 2562cb8f05727323
-227 22999bda6557e2d5
-228 769dc7de2d9d0f60
-229 50172eeda9fdf77c
-230 c0abe4dc5ce5d6e8
-231 bccb87c174ff3449
-232 5ec7938ca52eb27c
-233 89870aa04ad595ab
-234 f052b8dcef8756d3
-235 d5200d98fb2414a2
-236 5d78d66322939ade
-237 e491dec90d1d0104
-238 a701d73ea143da96
-239 c8006c1cdb680077
-240 dc6c0eeb28f49b54
-241 04a1939a5e852ba8
-242 6f5e14fe46c4e3f5
-243 10ae9662bcd1e823
... [2458 lines elided from this golden's diff body — the FULL file is in the review worktree at goldens/juice.t1; read it there if needed] ...
+1302 1c2d13c73c7d2608
+1303 ee7ed4c7cad8b9df
+1304 75d8e47b17a04120
+1305 b5cb93c212f69a60
+1306 615a6249c886d38e
+1307 a604af7f036bf8d2
+1308 340687ec04140fc3
+1309 93d661c9eb193909
+1310 a92c37a2524de6ef
+1311 3d0ebfac57ccc0fd
+1312 9fd17b8209679fbc
+1313 ad761fae538d0275
+1314 fa865f603c7e8864
+1315 caf95be07228e8ca
+1316 f60252abf8c06cd8
+1317 58b4f6998a2aac94
+1318 3e0bdecbb6ec1423
+1319 7b1a32cf16b5341d
+1320 ad4080e1deb010d4
+1321 bf71ea9ca4ac1ad7
+1322 53f00eaed5117693
+1323 8323498ba7353a5f
+1324 f37c7f007a9814f7
+1325 659d0574c7b9c5cd
+1326 d9d60e981c91a3af
+1327 e0e83074c368572f
+1328 eda243e309a5f87b
+1329 c5dc350d614eb92a
+1330 63db35f6fdbb6750
+1331 10114fd1f444ca77
+1332 a1eb3f9dbbbb8541
+1333 b44872f67a9893ee
+1334 fcf7f9386d0b03f2
+1335 9129fcc4a21399f0
+1336 ec2a2f7696ab49f8
+1337 600cad3011b0e9be
+1338 f3795c3ea92a91bd
+1339 b465960bb0ca883e
+1340 cc56e96f8ed66f93
+1341 4884fe6f74ecf7ff
+1342 626cc5c508ec055e
+1343 81814c64d205df93
+1344 efa36bc0f0c8774f
+1345 91c31ee2a098acff
+1346 dbab1fd3af03717b
+1347 9feffaedce65abf9
+1348 2b79434001c070e0
+1349 748a9323a1b0548f
+1350 94a9675e2f85e4d4
+1351 edcaa47a0149831a
+1352 cdff1bcda2dc6e25
+1353 c43e0c95d5bb7050
+1354 473557d3cee564d4
+1355 7a293c72111e1377
+1356 8a128448537635af
+1357 92092191cd2a7202
+1358 a2bb191a8319b0e1
+1359 523bdc0398339ea1
+1360 a9ee64024cebbf5e
+1361 7f78f65a01e3d1ef
+1362 75e39e60e989b7c6
+1363 d1f3baa6509dd9aa
+1364 cac8c4dda39e3538
+1365 dec60e4b05b938ad
+1366 95b1d58cea265efb
+1367 a303faef5389023a
+1368 d937ae39c76c112c
+1369 a1dea81cb3d8721e
+1370 346249d9c3bcf764
+1371 4a64954eb39faf72
+1372 306785be78b29e1c
+1373 e97c9c0feea9214a
+1374 1b483469ce5386c5
+1375 47fa1016ece40e39
+1376 2d0f314965c6c681
+1377 bbecc95bfaa1ba73
+1378 8e8024b7741dedaa
+1379 66a862ff43d27f4d
+1380 1ba88a6074623109
+1381 96a0143122541b68
+1382 f8c554eb537209b7
+1383 7cdbd5d19288864a
+1384 ba75437491028297
+1385 593155ab1bf34e4b
+1386 e49131f64ed060c9
+1387 19fd881f59e37cd2
+1388 7c4fc854c427cb1d
+1389 75389d69a32aa6be
+1390 a41cbe6a0db38be8
+1391 8479a6571cadbd45
+1392 5cf0d6b086246597
+1393 73260179f68c9669
+1394 545cac5dfac52fea
+1395 fc449f0d642e1310
+1396 7299fdf415f84d97
+1397 a61f5cb7dd92d9c1
+1398 b17d5e3d12f1fee8
+1399 4a7440ca70642f4e
+1400 76bb2e404de4a339

diff --git a/goldens/pause.t1 b/goldens/pause.t1
index 8767617..5faa0db 100644
--- a/goldens/pause.t1
+++ b/goldens/pause.t1
@@ -3,2005 +3,2005 @@ t1 1
 demo pause
 seed 4243
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 2000
-1 77468d742e2d507f
-2 29154667ceb01037
-3 43050cbc96fd31a8
-4 1eebe589a7a6b14e
-5 699be7995a363bd6
-6 b745cb2084cea1ff
-7 2b6cd3faca08c077
-8 837577469437a9cf
-9 d9e7535d0f1aa1a6
-10 30869c659b645fd5
-11 97ee6d893ba654f3
-12 caf4ca48c81cfbdc
-13 7bc638df1aee02a5
-14 acbe60e3b9249747
-15 9dbcaa81fab602ff
-16 2515c06f010de890
-17 3d8dc1051670a3f3
-18 7e8208c6f25d55ea
-19 e48f905deb141c1d
-20 9d3b2d2a87bf56ad
-21 249c3ccaf659f1d3
-22 ba46f35d90b6f42c
-23 4be6ce670d61ed51
-24 10125f561508942e
-25 90eec660d906d41b
-26 3bffe0c8db969ef4
-27 c472e85b958196b1
-28 da54810408f36e52
-29 369e80f030a7ebdb
-30 b4e4aa9714476c6b
-31 ca777d991362c970
-32 55014833ff694a98
-33 ef846d5cb8831cc4
-34 aa3e4b1108ec26f5
-35 45b013c12db08fb6
-36 b26f7fd4a6d81e2a
-37 f520bd860ffb8e22
-38 acaeaa7c9cb769e5
-39 e5c72813a9b72a67
-40 3531704305124709
-41 e7bf81a05e98ff19
-42 3edaf330c1598ad9
-43 cf74a0d68e594921
-44 a8004600359dd377
-45 9c4a28828f986246
-46 77552b50eec49f30
-47 15e10483e729bb4c
-48 f8d5beba7af0ee00
-49 46827b9688090e65
-50 84ad1843d416c29b
-51 d7c53687b8d8ce2d
-52 c3adbec9ced74e50
-53 e39863a5a25c404b
-54 a9914ad37d98ac64
-55 99da521f0142071e
-56 874deef5eb6faf75
-57 0aea2a419d68ab47
-58 f6158be51467c74b
-59 aa1992ba1e180cf4
-60 678e392a51fedc22
-61 b517f9e8dee6afe2
-62 4d4a917256236847
-63 f7f97128c8732bdd
-64 bf024ba630c41cac
-65 ae962b7900b7a0be
-66 5a90e57d41b4eb9a
-67 978ff40c1ced67e0
-68 428fe0394ca4c5c0
-69 e8bec39b934d871e
-70 3f4b59bc545e7d88
-71 7540225b27e24061
-72 876f987cbee0eb38
-73 c501641f3cad6037
-74 9d49d18e7f773e33
-75 f61be492ec165459
-76 ac33ff05637e00b1
-77 f8731e8258c4eba0
-78 fb2542a98856e1ec
-79 2aa55cd8e1c58e1a
-80 1e898bc75482ab5a
-81 7bbe5f5baf53cdc7
-82 cad9f0231ecd01e0
-83 622dd2ff03c124c7
-84 7cec96a61ae8673c
-85 f3439ce431efe7ee
-86 c8afca54be116630
-87 96d91a70f0afb2ec
-88 a28efff244fdba3e
-89 14f8600caaac76fc
-90 cf9ae7f47caf109f
-91 6c419fae7a7a08fe
-92 cd92bf5fb6a40ae2
-93 fa04d163ec55e3cb
-94 57f09c36f9851c1b
-95 a6a2741897f807f8
-96 2261fd39649166a0
-97 b03ee0f6fc7817a9
-98 3234a1f1fd462787
-99 d9c3a6a6ba8a5819
-100 b03f130ffc9e0fdd
-101 9bf92a013b914710
-102 c6d1f064c82f4901
-103 6789427826db1d7e
-104 bbc304d0e644559c
-105 558590de24878761
-106 726f51402b40547d
-107 07e70588c78978d1
-108 59f02e0b805b2a45
-109 f6fc2afec806b719
-110 da445ba18b50960f
-111 9a7d5a7dd5a89a68
-112 2ed67e9bd6c58d72
-113 d6fc213d6de508df
-114 0fc5789d68c5586d
-115 0e0dc6d7ed643a08
-116 02dd6f17ded6a4ef
-117 d54d2ffdb2e66b56
-118 5242cc0788213c02
-119 f26d42a0741d4dbd
-120 f09864997d99dec1
-121 8e56186a678e94bd
-122 011a925a7f284410
-123 d7eb17663cc002ad
-124 1711cfc1e424fd61
-125 8c504974b20b7344
-126 85a7d6b9b8b9da9b
-127 4ef23bc879c51b8f
-128 1ff7c95b4331d2a0
-129 611c4e01213bcb6b
-130 c834534c1e49dd0e
-131 1268a2666c28b11c
-132 f46afe381f81be14
-133 48b0806b31b307dc
-134 483ec3574771ee41
-135 d86a912dbd6cfbcf
-136 4d75831354a360f5
-137 873abe3a9345555c
-138 a41ab2de4d0face2
-139 4b12cf5798f12a2f
-140 893b91559718a6f8
-141 284f4d24813bc534
-142 ec07f9606dd8a048
-143 49d261dc0cb2f5ce
-144 478b3aa6950bd551
-145 430b1fb930e1f7e0
-146 1930f7d8564848e0
-147 0b669478a95dd522
-148 b69fa22345272a47
-149 534616b81a93e4dc
-150 74068efd2ae4dd87
-151 bbf35c882a503ef8
-152 608806cb00d145d2
-153 49a4c590fe132dae
-154 de2ab0a3f10f53e7
-155 bb21829f39bfa471
-156 fb2967409aeff979
-157 b32f0cd008d6337e
-158 3bbe8f7343fe2103
-159 c8bb6446ed88e1f9
-160 e47e2bea48028053
-161 27d9c9fae9a51c35
-162 820fa0db07c7bfb8
-163 81e0c90c4346a872
-164 9d13e4692ec9df2a
-165 43f0de19089e72fa
-166 c812850fa193f7cb
-167 bd4ec57065c6f103
-168 d69a1e80982fbaf4
-169 3985520c0d51b038
-170 344c02a26792bb82
-171 5a4b29606a12d7be
-172 12756c6dff85be25
-173 38545db34c278b03
-174 7aabd38ed6a767cd
-175 aa3f087100e95cdd
-176 27024b25cf0c36b9
-177 1fbbec7be4762550
-178 e88a75c08d239ce3
-179 ea1ef2d3791c8c93
-180 1296b36ac4434887
-181 8be0c57c4d2dd80a
-182 b0b6e9711579f082
-183 492d074e598067ff
-184 65867a21297f0229
-185 835ca20c48524477
-186 eaa4bb12a9a88df5
-187 eb70cdc882575a00
-188 9e564246ceaaa2fe
-189 6328aa717fa7dbde
-190 1e76f4b586b21242
-191 01a4c4012464922e
-192 cb1c135a0d740853
-193 9106d5c9acc5def6
-194 004f71ea902d05be
-195 d295052e34132f11
-196 484b29f4fc11e732
-197 fe127e6bf47ebb6c
-198 19f6a3243bae04cc
-199 5d5a8a83c269f4f4
-200 883e757aea604769
-201 b1c70a06f529e54f
-202 ab6ef77e635c2a45
-203 0be366af779ac9c2
-204 8e2c80624fe70dec
-205 d606c4ddbc281075
-206 b47cabddb01e52fa
-207 d9d99e2f67ab62ca
-208 0ade292cee5a3ba7
-209 80aa2f07de993b43
-210 cf37f0bcaf7cb1f6
-211 026237bcd5dda947
-212 6ce94c5657d42dc6
-213 49b1167bef837a96
-214 38628cdedf13e075
-215 d20b8d72b18ef470
-216 a43228cd09c2b3a7
-217 998584390dbd3a32
-218 95ee8ce247adf9ab
-219 afb6b4e436204e65
-220 7ac491ca02f8a164
-221 730ccd251573f848
-222 c951fe364e6fb6d5
-223 b02489ec2a5a6209
-224 5b66461afd7a4c8e
-225 15df8482355e515b
-226 810a6e77a8bcb1d5
-227 734a403c34331e21
-228 e79cd9f5c7ab89ba
-229 40c2b3ef8288fc0b
-230 8315dc938432835a
-231 6d1d35c8d84e0ce2
-232 78cdec85479b97f9
-233 c70b419e881ddf9f
-234 ba80ae78e55202e4
-235 cf91a473d062d009
-236 809d699273771a47
-237 55bc586099ff5255
-238 f52af1522ea28af4
-239 349a0827ff1ce957
-240 85957c9f3a1e642e
-241 bf937eb0b82d11fe
-242 034b276debfd0b58
-243 84401ae964f98d14
... [3658 lines elided from this golden's diff body — the FULL file is in the review worktree at goldens/pause.t1; read it there if needed] ...
+1902 f24cde7a5c34d792
+1903 240fd9dbc79b3eca
+1904 d7e6e861b90e2ff3
+1905 631679e80521caa9
+1906 39db834a07ac1a52
+1907 7fe5981c0eec7c29
+1908 1b33db72257de397
+1909 7c07ac46ff4c65cc
+1910 27f3c76ba3d4d824
+1911 b1cce691c346681f
+1912 c8129e7eccf36d53
+1913 231b9effd5d8dd1f
+1914 2127ecd993e3621e
+1915 336089b23d556908
+1916 78d7720a61c427fd
+1917 19a6f5c3e11acc86
+1918 72bb63b337f1aa1e
+1919 b6f0038c94e79178
+1920 6f5ad4f2e275d8a6
+1921 74e424ce1f09f19c
+1922 ea33ced798c897e7
+1923 b4336193819e8427
+1924 9765483f4494eb41
+1925 3869c9418241bef6
+1926 2f7181384b22de3c
+1927 75af9e8d09c9d34d
+1928 f52e76390f1a9789
+1929 6c29120227551309
+1930 43c7e17ae7288929
+1931 ec00bf7164cd1679
+1932 655f27f59bd4002c
+1933 0a08bb9bc1ba69ef
+1934 0dc5a8e1793d5a6f
+1935 2dbe03cf6745358f
+1936 ff84d7d38ddd71d0
+1937 41c4674fa33c29c6
+1938 564b6431a6096bad
+1939 3d356f5ce4c0a835
+1940 ff0b68584228533b
+1941 c4afad50685fd7b4
+1942 4f123ad568b23a0e
+1943 a07bca178a003898
+1944 0cf878e4b26ddee7
+1945 92e0a5c173655a49
+1946 e419ced4a437147d
+1947 03d1dbfb4055a3f7
+1948 7511a05d8b0957c1
+1949 2778707adc44377e
+1950 4f9d3602c3a94bce
+1951 551d4a9e36f44eb7
+1952 c3a45518da933b4b
+1953 6929e63778460766
+1954 8af6ef12f57afc76
+1955 af729cb6e8df894b
+1956 49b573a5d4707a84
+1957 ea4fecc86758d19b
+1958 6a3f43663c49837b
+1959 3d33aca35182da3a
+1960 8575a4917e9f0e12
+1961 cf32ec1e5e2ec2e1
+1962 ddc33ea391e7302a
+1963 780ea7af3f643500
+1964 13a4c8c2b389d955
+1965 97fe60ca1f445f1e
+1966 5f3d13e0e60692c2
+1967 8ddf8d4e4ce3d8c9
+1968 0cc4329689d77f3c
+1969 eff08fdf1930fb65
+1970 8a9ea53417eb153d
+1971 f59111d1b19de3f1
+1972 78656c45ab7b36d7
+1973 54a4e28e8fd9e181
+1974 4e36436496e155bc
+1975 a892577f72d84c37
+1976 f3832c806d9934b7
+1977 61e4cdf1edf82cbc
+1978 842cc11197014ab6
+1979 eca71e98951e2a0a
+1980 fa6c811003d68b49
+1981 7fdc641ab548633f
+1982 1594f710997b8ad0
+1983 369ebad1fbb35b44
+1984 c16b42393751cb6f
+1985 816a1ab4e49335db
+1986 3945981a744bb9f8
+1987 026863deebb46352
+1988 8a241fe5bef13b83
+1989 841ed5b17117938f
+1990 4b625841eb96fcb6
+1991 466c7b9fbd7b7fbf
+1992 0b734c057e2a3473
+1993 70ed9075a07e9cfb
+1994 51152c2b0add2157
+1995 bc6f76a61f86b481
+1996 0503201a6a5dd0ae
+1997 461d023b4e3fb998
+1998 78d68574dcbc7e47
+1999 f20619e3d84d9438
+2000 4c621c7fe96dd410

diff --git a/goldens/qos.t1 b/goldens/qos.t1
index 35b0efe..7231b80 100644
--- a/goldens/qos.t1
+++ b/goldens/qos.t1
@@ -3,1505 +3,1505 @@ t1 1
 demo qos
 seed 3003
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 1500
-1 a10c566565631017
-2 1227e9a7b82138b4
-3 2a5333e6aafda424
-4 51e235f70896e9f0
-5 75063a13062e28bd
-6 397b21acda24b91f
-7 d497b71a7e688d6c
-8 0bf7e38eadca8428
-9 9ccccfd42ef29b20
-10 42a3c1d97a272895
-11 0cf1dca258543453
-12 21bf64526d2687f9
-13 dd41a4601a6057dd
-14 0917af7717b4d1a7
-15 1d63d9a4c46f6391
-16 e0a3055cdcc2fadc
-17 17ac3e2df8c45b02
-18 459f3fde015e0c4d
-19 c4ec8519124698dc
-20 5fbe41895d959e13
-21 134dcacba241f641
-22 b876884c13d8f497
-23 eaf6d7f7ed90b263
-24 756623383c869dca
-25 9b7b413bd92f883a
-26 aed8edede1e3b1da
-27 63bde395528f859e
-28 6afeca7271c248b1
-29 1f4088cc43821b33
-30 1d82884b9dadd131
-31 75a6e5907d483568
-32 5f87551b8148aca6
-33 edc9b6915aafc349
-34 49d69e40085b4015
-35 9d894a8a67bb1663
-36 6ae6b19fa85fba0b
-37 158b4438093257a2
-38 dacc9dcacebd6912
-39 c9b7d425fbfe4acd
-40 8bfeb45e3598f307
-41 4bcb26b3b9c4cbc4
-42 ace3da23d8dcc9a3
-43 112586da3e16fc99
-44 4a10f113b56b487c
-45 32b6773fdbd6f1ac
-46 204c1ee78603be62
-47 029f79cf8708360e
-48 bcab6654a80afd4c
-49 51ac48f1764b4506
-50 3fec440da9737ae6
-51 523060fafc0e37da
-52 ac53f2fbeb735093
-53 573c12123af030e4
-54 a58e73d8ace33011
-55 3faecb1b9b986535
-56 529ad19b7c78be9c
-57 867282b08fd70150
-58 0bd668375825c085
-59 aa9cad772c571e2f
-60 8a2ca1a88f20ba65
-61 b7042d1faf858e92
-62 79372a3091d12272
-63 ac1bcfc820299937
-64 c44c7381a4fe7d46
-65 40378a12e364311d
-66 bc214bfe888706a9
-67 154f75c3098fd02a
-68 fc09766d3b6223ce
-69 d664350dda2151f5
-70 2975e330daa9de77
-71 75c6be8f237abf25
-72 8be00bdc8ad093d9
-73 64965bfba3b0eb17
-74 6b6eb6e697278015
-75 3ef0c80b271dbf54
-76 717545d8bda98fb7
-77 9785a9ee6fd76aab
-78 bfc55c4d1687c421
-79 9d8243375e389cab
-80 dbbd512339fe1edd
-81 a1d3a45f32f46cc7
-82 e866cf8b203d4c15
-83 d07795c7745dc688
-84 cf31cf01252337eb
-85 a6d6bdfcebc0a862
-86 0c26fda6593e38e0
-87 75578e5439ebcb4d
-88 c8a1b3d17a844f8a
-89 99ba50fc0cec45b1
-90 505405c47faadc70
-91 24a399424cde0de7
-92 1207e7f02f119c61
-93 bae63ff2a07f47bd
-94 a1df600c1dbfca58
-95 239a36c37739f304
-96 9dfba37a4e3ba54d
-97 b701b2b9de4ed0cf
-98 8432f1de00d01641
-99 5a9bf2ba4b0696b3
-100 4c7f0c4bea4e4f1e
-101 35bfed18caf41cff
-102 5ff553018ffa1ee7
-103 fcbe1e3dd981257b
-104 c62b61083aa84a53
-105 9d3dd09dc1873a5a
-106 99ebcc67322c9887
-107 e1c2e69cea13623e
-108 cd91f38e32770101
-109 0c3f678c233a515f
-110 2d6008cadc76281b
-111 3af4336abfbf65c5
-112 aabfebf7d26f5b5c
-113 55f61081257f6ec2
-114 2b935448c123fcdd
-115 6d8858840cab7a63
-116 36e14b59ce2b2812
-117 54c4de725a99ac40
-118 75f4d966827071da
-119 8b99dc88654c4a6c
-120 14f51fdc09642eba
-121 f05244740d12f328
-122 2121a67f07e4bdbe
-123 c74cb0d922916adf
-124 88659d114d3ba102
-125 ef82337341eeb948
-126 82a8ba7387bb95b5
-127 43eb7fe20867efe4
-128 645aaef45f7bc9c4
-129 4e9d8416fc025ea8
-130 8a88c40a0715ef17
-131 50724241b232efbc
-132 498895056ed015a7
-133 ab9918d397d352e0
-134 5c6d3b508b3df6bc
-135 8ce1cb312536f3ab
-136 b2e2472e376a522c
-137 61523927da765058
-138 a515f14cd154796a
-139 c0026350646fac8e
-140 aa14d3bdd7247a77
-141 efd710e87158efba
-142 1d02256000644a22
-143 cda53c5d70803edc
-144 cb4c040958e51fef
-145 1130bded04906483
-146 3b6091cf76d7f095
-147 db11dc473d8d411c
-148 4c592fe72772b7dc
-149 ae51064e2ed9d05b
-150 a24bfde219cef47b
-151 33001425fbc54cb4
-152 837c920a97020446
-153 691116da34296559
-154 4558b1f88972ea4b
-155 0e32ed1f80e52ec2
-156 386af0e6025776e6
-157 320ed0b1a0c3ee10
-158 1e04ebb9cadfbded
-159 b09513e314f7a359
-160 16fb1dfca7885352
-161 12ffc0fd6c675a16
-162 d134107265300281
-163 32e0dbdae5b285d1
-164 f2c7781ac08a2e6e
-165 3125e8e43ee36f56
-166 bbaed4aedf569ba1
-167 921ec2e45410704e
-168 640681dd7b056494
-169 dc5398fc7a4bb9c0
-170 6d9f81fae75b6d21
-171 2e2378023dc1dfe5
-172 e65280c35088ba96
-173 7fb4c9bf9759dba4
-174 b5ad18b22e9e9946
-175 d5a3d2628c3fbd29
-176 f452f972863c2291
-177 79be10d7301e2ead
-178 d074fd860cb0dea8
-179 10b4efb9e888b6c8
-180 764407bddd41d988
-181 7cf7960085de52c7
-182 13d3961f08cb405d
-183 343d875dbdb5fc47
-184 ca1055be91237e45
-185 425ff970ca3b5f85
-186 1bf04416651854e4
-187 c1878d4d31ff3a6e
-188 433d23fed2e1279a
-189 8358dd145d0cb922
-190 e225ebc5834ade56
-191 2099306843216298
-192 5aefa3ebf80bf694
-193 447ed5ec3949e3ec
-194 54f4d41976a75904
-195 7dc1e4f1984428ff
-196 9ea07ef39c758937
-197 7da07fa51333b82b
-198 8078cd6cc51e852f
-199 9a7477dbc1c2461c
-200 7e00fe545e37e793
-201 0ce79109e6120a90
-202 433ee9949ab5bab0
-203 4366d263d7967c8d
-204 6cc3af12ef64c8cb
-205 423dd7b9403135d2
-206 8a21d60a194c17b0
-207 c44aa8d35a7e2da3
-208 766102e4d9f53d8f
-209 fc9411ad432a3c79
-210 05aa5d567d8103c5
-211 ede8252bf980580c
-212 02331b583b0bfb37
-213 a5ad0d207eff8c9c
-214 64d99fa5d9e2673b
-215 a3f282a6bf221b68
-216 78818f7c124837a7
-217 5561991d1e2a1654
-218 a4599adfcee8e0d9
-219 896e80cc285b919b
-220 0fd5191bec206466
-221 91094953da1cc5a3
-222 0d5381da4faac354
-223 8f537854da8a08d2
-224 c61920d9e87954b5
-225 70afa9da7de95022
-226 febc6bb5ecf39398
-227 77a429f7ce8196d7
-228 5a9107e98e4b81d1
-229 2036a6f86cc56672
-230 094d4f1a8b8a217b
-231 ad61f56de3484429
-232 d5f1d777ce23598e
-233 6f87a32ba2c6aa59
-234 f655c0b66a948e96
-235 27bf475bf7080b14
-236 cccc7cd1f7adae91
-237 33951b81f7acfc0c
-238 f35fe30bf367b083
-239 ada7d9d0fbbd1f90
-240 efe2e08af215631b
-241 f5b1ae08ea7554f1
-242 10715aaeb504ad72
-243 678b0b537f1ce6c6
... [2658 lines elided from this golden's diff body — the FULL file is in the review worktree at goldens/qos.t1; read it there if needed] ...
+1402 6513146fe72cf0e3
+1403 9933bbb4a9446202
+1404 2594db2849b2547a
+1405 e2d3e00495b4e254
+1406 e32f207efbd4eef9
+1407 808ebad28451d650
+1408 72e91893229d7685
+1409 ab494b855de5279d
+1410 4e650c8c1414e086
+1411 937d3fa2baccfc2e
+1412 2612c296c9843cf4
+1413 64194174d5ca9364
+1414 1d2f68d708e8c7ef
+1415 9ab362a6f671326f
+1416 d5afa95825ed6fb4
+1417 457ce4417da8c673
+1418 f3a4df79b29b1967
+1419 694710b55e0e09c2
+1420 e0f54727ce30c11a
+1421 936327587a1b9619
+1422 fe3f8dba2c6a5d8b
+1423 a4a13c5db3ead8d8
+1424 26ee362d26e7c36c
+1425 cb5d9a7d2ad5501b
+1426 663be054aa984ff3
+1427 01ed50b32178adc8
+1428 c113a5e4c0ebafda
+1429 907977ae02fb56c0
+1430 677f49b5f909dbdf
+1431 84ea23e554d9b1f1
+1432 1f6510b411dc6a87
+1433 acf552dda1828a76
+1434 958a4d1fd41d88ea
+1435 52ff2590890ef46a
+1436 08c20199a9596281
+1437 5525fe3b066af405
+1438 ed73152d87e58bd7
+1439 b044c3d175b7f11f
+1440 85f66aec38d771bd
+1441 16684988251b7416
+1442 219e2aa150676977
+1443 3b7561d84b43233c
+1444 4db9bdb41b5eff68
+1445 b6fc0c54cbcc9426
+1446 8abec19c0040c580
+1447 dc2be53c86482745
+1448 4347b1fe68d1460e
+1449 5f195058965a913a
+1450 bf485cefd87ca71b
+1451 5194a44f7ee711a5
+1452 5c60eae35a615f3e
+1453 0a4760cbccab08c4
+1454 f4ac3964bfdd96ad
+1455 27dd7b525a2d1225
+1456 b28809c6c646f709
+1457 137e13c08c846cc6
+1458 eac401a84935d34d
+1459 b032b74f10b3b400
+1460 1b6fa10e1df6b102
+1461 c36662abfda84cd4
+1462 7733a0126db5d39b
+1463 44c571227fc51a01
+1464 b745a1749ec6bfbd
+1465 7314440cd5e078e3
+1466 bd97d01e99db9c54
+1467 d6e1e76be8d6187f
+1468 bad7f4de44e4b5b6
+1469 8ed09c56520b9d47
+1470 a1e7b3ef62bfc895
+1471 55de93275cb3fc97
+1472 3a11f9048b2a5e08
+1473 9ba43b48ec2f0177
+1474 a296e9a319e1ad4a
+1475 88524e9b19610771
+1476 8ff18d40c9a49fd7
+1477 501b617bf870b423
+1478 2c2eab5d6bda0ccf
+1479 0b0e00639ce23d95
+1480 fcf182bf7872827c
+1481 306950e04f403195
+1482 8d025de73f2b042d
+1483 ce88d51b4fb992a0
+1484 c60040e4331f1bd7
+1485 8f9caf9297c09d5e
+1486 7beee636a4d915a3
+1487 da3b311eb84c078a
+1488 0a13a4298aa2f95e
+1489 3bea788119419065
+1490 286c329ea2e3cd9c
+1491 3f130161a9575413
+1492 a702bc89e3166ccf
+1493 460d9548a844e957
+1494 3e1027cc039fd4f4
+1495 a5a9fd9970223cfc
+1496 c7df5554f132f0d8
+1497 c3d3115bfd7b9ef0
+1498 807a7b3e71d68312
+1499 7673631542b27664
+1500 feec63890e7e21ef

diff --git a/goldens/surge.t1 b/goldens/surge.t1
index fc97f52..1cfabec 100644
--- a/goldens/surge.t1
+++ b/goldens/surge.t1
@@ -3,4005 +3,4005 @@ t1 1
 demo surge
 seed 4243
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 4000
-1 d7a2404f81726b11
-2 7fadec9691b19de3
-3 f747e240c17cd4f6
-4 d48781d9e2ac591e
-5 265e5c045eb53478
-6 cad1b01b9b19b291
-7 233fe0aedda4335d
-8 6e11671f923b16ab
-9 bd38f32aefca4b60
-10 e4f78f18d94742a3
-11 59c21214b4111ac1
-12 2bb5acfe3704d12a
-13 e93c0e33797b9c89
-14 e10adfe0b96f5bc7
-15 d800e937134784e3
-16 a7759ac597472f66
-17 8fa4fe8e1189dce9
-18 41e306ab3173ed2c
-19 d12f2cbb03b0b211
-20 4240e1c9f6f1a4ed
-21 9b9e561f82b35c87
-22 68fb3f0187226252
-23 f79ed14cea0dabcb
-24 214fea9da89137c8
-25 4e3d980a2c1c9fdb
-26 a593dc9851f65d16
-27 3d8504664c41beb1
-28 66580f1ffd034894
-29 c4c8585c600e7b09
-30 107377e8a50bfc0f
-31 5e33bd8b16346ef2
-32 9df55c43a5d8a792
-33 918699002a3b76ba
-34 c5dc1b87120c1ef5
-35 79be3e85700d1c76
-36 015e169737cbf71c
-37 4c330937c05fb580
-38 da74bd161f3400d9
-39 e06d14092b70720b
-40 855c08d86244de49
-41 539ed951e1dd9f03
-42 9963923395785ad9
-43 a556a85a94c96295
-44 07c1725a22b3f14b
-45 db2586b1fdbdf318
-46 01dd5270f3a660f6
-47 00201980811b5720
-48 11fabfcbb4af4906
-49 dde56d57a8db6ec9
-50 5b8bca7204aca10b
-51 3d7f0d92eda48b6d
-52 9d091fd43b000a6e
-53 e8d12486a9fc5729
-54 8f74c845c6326b4a
-55 eca8372d0a7ff48c
-56 abe769fe141bd0a5
-57 732df6232fa3356b
-58 96b951c9bcfc1ecf
-59 388bd326c3d91570
-60 e111d33f7a9d87d4
-61 6eec191361305220
-62 2adfbc83b3e0da07
-63 a4a439941f96f59d
-64 4b99b106550ef402
-65 9c8f9b9488264cfa
-66 7d66c3cfabb7b2fc
-67 3eb6866b5e1bbb42
-68 8fa6bbe6e6ef89c2
-69 5f86c45d4e575810
-70 97b236818c74283e
-71 bb0f9abba7ba53db
-72 446512aa4123a99e
-73 e421640cc5a46177
-74 57bae3b406b62d43
-75 5b278d55eaf75629
-76 ea967d50201915f1
-77 71bcf8b604e6f570
-78 81d9f8803b8f77f2
-79 487d93b88b1dbec8
-80 80a39d156d18e400
-81 037479d85e3ccdab
-82 c7db8f7b3801dc3e
-83 e1404bae9337d055
-84 261a4ea06024f8ba
-85 95cd4355fc865c3c
-86 30a806a0ccd3ddca
-87 c0f3da734edb6f12
-88 d0193f9a1bf61ac8
-89 b085d8b88764a06c
-90 51c37832043aef93
-91 d319a3fd6924a54c
-92 24b9f9e35e424120
-93 39b115972e7f0b2f
-94 d0248435c6ec943f
-95 48778058853cc4ec
-96 33546ec7f77f7da6
-97 c27c0fccd3f4e78d
-98 c947a55865f31f87
-99 29a4dcd88a64abe9
-100 5de69ebc84fe638d
-101 7ae7b05aacd5e4d0
-102 7d3002a24f1e8c41
-103 d20522190974e40c
-104 7ee794ed8cb36d06
-105 281f3cf4745808a1
-106 8cd307a0dd3993ad
-107 23fd4e0d3755bab3
-108 974a47a1fdbe7895
-109 6f36e024b9851e9d
-110 40cafe7ac9cab55f
-111 16e3a27d1a2448be
-112 90858ad6d89bd54c
-113 4f718ef800b01955
-114 b61e83baa2c5732d
-115 5bc580103dc9dafa
-116 d4fcacbe50d619a3
-117 b019ac52fbaf2cb8
-118 e5c3116625003f5c
-119 61329590b2337d97
-120 4675069ac726f141
-121 f1334827d49a9311
-122 86f9fa05b6d3d692
-123 b42d4ce57adc482d
-124 026c6e1c9fc74ee1
-125 1bbfce905ee8a974
-126 e262463eae55717f
-127 be8e14fa6a4204ff
-128 383eeae34dfff8ea
-129 9fb562321cd8f78f
-130 7dc5525709297d40
-131 063d262677658e28
-132 cb81a4dce7a84402
-133 7f4e389d8b30093e
-134 32e071ef74277015
-135 3616bd030154c2a3
-136 898819f4d88fe0e5
-137 4c69698d82c8cfac
-138 4a63a4dfa25846d4
-139 3bde8566c85a60df
-140 45aee77874ec8cea
-141 e074468731e65bc2
-142 0d59c01cfe1edcfe
-143 f53a8f13d61b20de
-144 68e81630a3055bd1
-145 00f1ac5f859465e2
-146 f1d2596e6a106e22
-147 7a4f125b7767f794
-148 720e0af1c6c41f4b
-149 627c8c67f03f068c
-150 56bf2a784f562eab
-151 b7e261af84a429ea
-152 617da91757a10878
-153 48ff7f4d59507c18
-154 506989b8f49ff9ab
-155 d21360eac309ef13
-156 06851a70caa4a149
-157 ab9a1f978f0ae28c
-158 ca9f0d6dfc927103
-159 fe530e3e0a64f649
-160 50d1645a693f7aa7
-161 70e57b4ddf60ae6f
-162 8bf12573885c01d6
-163 a0ff9bc496a668f0
-164 739e75d94e9df9f8
-165 c094af5f4792665c
-166 319e5b126f0c945f
-167 f27c8aebf369b0d9
-168 63d8e7425e30e16a
-169 a4d364739358ee2a
-170 cb70aec3aacef000
-171 9e1eb382f1be9ab0
-172 90ace7fc2a0b23e5
-173 9c3979e664abd461
-174 2dbbdc10c2ace5dd
-175 cb90b80a083164e1
-176 7538628612f3e2b9
-177 22f25f174121fec6
-178 b3939b1618bb5a07
-179 fdf5bd29310c5911
-180 a61cc1ee4583bbfb
-181 e7c4829bd8055778
-182 b09f02a1227bf808
-183 bc8df27c999dfc33
-184 621da918856395e9
-185 22fca9faf1c6786d
-186 5e6ce72c503a9405
-187 3480da780f074b42
-188 2764597be115c12c
-189 fddfe16b0eed3e60
-190 4b642d9178d92f4c
-191 81d21ca8d09f71de
-192 7e70b26ceba84567
-193 b45110aa47189cb4
-194 69c14c6b49cf810c
-195 98e972cf9f1410d1
-196 3f2ff8b5d0a3e664
-197 35a13511ce42c13c
-198 a6c469002bf7ae42
-199 8ce487379978b746
-200 c85bfbc14d30e9b9
-201 4e4f259a376c5dc3
-202 b9342180b4495985
-203 13ab556efec59142
-204 c0a8299f92201cfa
-205 f2ca0223554ebc19
-206 c664854541368340
-207 2eab78018bf84684
-208 f062d51867e7ca2b
-209 bfb9d3a9acf63939
-210 a30e17c2c44d4448
-211 5647110efb7ee907
-212 197fe43fbc842af4
-213 a9b9b575588bc2b8
-214 5b896788d87243a5
-215 fd2458f686eceb74
-216 33e78864b0fa2b4b
-217 13f7716149d06df0
-218 1be87bf26fc12feb
-219 0d8dcabe734212b5
-220 b6bcc6822099b512
-221 a8a50d5f5e7a1608
-222 3afb486cddd58215
-223 0b9d3eabab92128d
-224 59c3a67c86309d54
-225 7d33e324a30d547f
-226 50eef9875bd4d755
-227 60476d8ec6966f73
-228 f33f6b1d8614e5ac
-229 3b9e8f91a23b1f7b
-230 91caf20c27782070
-231 4dab452ade377e8c
-232 43e6d7afcc6ea279
-233 58b1a09006d88605
-234 dcd2db39fc15e9b2
-235 e716d0e4674145cd
-236 0fbf332334aa2b1b
-237 9da62ff8e8250425
-238 722289070256225a
-239 9b2bbd5d707aaedd
-240 c47b2499964c05d8
-241 0ec2ef683a2453cc
-242 d9133b9ae28d524a
-243 dbe135c7009418f2
... [7658 lines elided from this golden's diff body — the FULL file is in the review worktree at goldens/surge.t1; read it there if needed] ...
+3902 29d0c45f6d5ab350
+3903 7d43ef86bbf2981f
+3904 9503578c75030f95
+3905 24fd82e4d845d73b
+3906 629e9b48fbe33264
+3907 d7088baaa99919fc
+3908 844fe69f5b72db86
+3909 0180c26f8a265631
+3910 1d042454585ab53e
+3911 f89846d4312617e6
+3912 3c1e516eb7e10037
+3913 7736e9c4c0130dbf
+3914 c2f2e506b7b44c7d
+3915 64f06bbbaf89b935
+3916 1b67c27dcc042cda
+3917 8b4044e42d8b4d4f
+3918 5ec8bbf2236c3d66
+3919 c29efec9e73c6bf9
+3920 b539bc734b5c007a
+3921 845cecab887fdbfe
+3922 5232159f1fdedab9
+3923 58e83e61c1545007
+3924 745936d63aff3c6e
+3925 3b7495bd8c472d59
+3926 509803a2f5977a40
+3927 3ad496b1796f73ec
+3928 4491f2edb27e00ae
+3929 e0b7b73dfda25928
+3930 2229231d3db6ddd7
+3931 a40a60756a7fe5d6
+3932 60a2c4f87485d827
+3933 7c5659a2e92d5c08
+3934 6c069aa1f572221f
+3935 e056354c042fce21
+3936 be48f9db211ea0a2
+3937 41fa085b1b989d4b
+3938 a42106cea72942a4
+3939 5c9263ccfc09dace
+3940 bebf9b2083f46c3d
+3941 7dad17b02f69ef83
+3942 fbfbd65c5a760e2c
+3943 bc109dca0e27848e
+3944 e591c697769cc341
+3945 6f0cce39e30e47bc
+3946 f1855121b6fb29c5
+3947 9ae03b934257cce1
+3948 51800667ff4bbc4d
+3949 7760dacdba3b73e7
+3950 6a33bf039e24ef52
+3951 3c2db858214abbcc
+3952 e2aa855f4b4e33d8
+3953 a09d95ba7188f0f3
+3954 b72d9458e5724de1
+3955 a95e182bde196ca0
+3956 f82605d6ba5c1c7a
+3957 920578b72d100d68
+3958 5f985e410c25a1f4
+3959 67d29783d1adeb79
+3960 38e33915d8b7256f
+3961 94e333dd7cf0cc9c
+3962 4d8d3f3ed4521f1c
+3963 c4acd3eadbce9530
+3964 b52ce905c6d76db7
+3965 e0140bf5aef6e3c9
+3966 b18c77a5569fa12c
+3967 807861b994c513d6
+3968 412efb2637d66a35
+3969 59d342964183c409
+3970 e6ca611df2630383
+3971 79379397ea3bd65d
+3972 439309350870e19b
+3973 1bf8a3e989834f23
+3974 b4ba45fba3e505cb
+3975 4f7955b11d75752e
+3976 166413b35653b08e
+3977 3effd66771f48d6d
+3978 efb440156d7294db
+3979 734a2ec832b50311
+3980 d8212cead260c9c4
+3981 4f50ec041a118461
+3982 a12ce2b020c56b88
+3983 dcc59d0305369cac
+3984 2a73ccdbba82bfcf
+3985 1b58961fb805a570
+3986 e0341c7a497812df
+3987 782c7f2def69177f
+3988 fee47b57b1cc7aa6
+3989 ecbed75dfdd2a508
+3990 6b5d07f37037ccee
+3991 470ca8ff7ab1b29d
+3992 68a4ae49dffa76a0
+3993 5ede019cb85b3953
+3994 aab0f2cb6a226147
+3995 7b7ef78a5dc8802b
+3996 c06e670fa8554bc4
+3997 af6e710e4dacf58a
+3998 06ac3adb0cb3ab58
+3999 898e02535211c6c7
+4000 98787b3aa70816bf

diff --git a/goldens/warn.t1 b/goldens/warn.t1
index 0042f0c..e18b982 100644
--- a/goldens/warn.t1
+++ b/goldens/warn.t1
@@ -3,1505 +3,1505 @@ t1 1
 demo warn
 seed 4243
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 1500
-1 f4af73011f3bc4ef
-2 4c15e05211ead2f7
-3 d95783b1e71c7de7
-4 ca43f31c216b8db1
-5 73dc38560b53863f
-6 5f5a2477144c044a
-7 141abb43d4fa160b
-8 e80fdd2e7c76835d
-9 20b3b64c95a37c84
-10 067b653eddedfa6e
-11 64ba7f8e14e6afef
-12 c7a1b0f2f656d427
-13 5ae2a7d224fdd13a
-14 919afa4c11e7ead7
-15 cb5f70d9c39b989e
-16 ad65f041178b4450
-17 7636c45dc459ce33
-18 c3e30b9aaaf829c4
-19 cfaccdc6b904734b
-20 e980aa5e8e0433c0
-21 ebfb2e9bd35a61c5
-22 3b2f05bb8629402d
-23 8164bca2458dab56
-24 dae0400fe1c1ee79
-25 ab3ab1f589e8f0fe
-26 0df5c412e426e8dd
-27 e70dfea53f8a49fe
-28 8b66be74d846decf
-29 8d0620f5afe77d49
-30 0c770216782749cd
-31 1459497b45c26695
-32 041cdbd8a31889b6
-33 5fa150587e1ef240
-34 f6c482411b66fd70
-35 e34c9e05a99369c9
-36 f84a4f8cdf1e4592
-37 d566430c89ee9a8a
-38 0c6d27fb9fffae1d
-39 431ebe5b2692f8b4
-40 98be990aead54cdd
-41 549e8963562719f7
-42 a67d7b0913bcefff
-43 324a7d646f49a11d
-44 9fa60148cbd6e5f6
-45 afbf97473bf2ff88
-46 a4977ab94718d52c
-47 8b94e8034130aee1
-48 f3cfcb9da157e67e
-49 62c2e030a123d6e4
-50 17c9e09bb0b53558
-51 842b8bd617a86a14
-52 22817be8d0fa6a2a
-53 e8d90e482555e67b
-54 4503f31302fcc65b
-55 4019e98da3b1b2aa
-56 e12fe7a1c5376c91
-57 39592081b7076a83
-58 6c0e2e139d6937da
-59 bb636cd17c4c4e5c
-60 d6ce0b53d9f5b93c
-61 734f8421ee478717
-62 54f0de979c349eb8
-63 4e0797912f182600
-64 e6b4913bf57a6b0c
-65 bec6846b818461a6
-66 0053aecf083ec54b
-67 f31c6d60bf8146b3
-68 21b851c992863b57
-69 40490121c9400bcb
-70 7e1bfab6e5c8165a
-71 329d742eaa876dbb
-72 072e1dd81f0ff86e
-73 62e0ea290a9c5643
-74 5cf1c9d1a02ec82c
-75 01b56cab0289e58d
-76 b7eb5bd7e9d6cc90
-77 422db0b813345c70
-78 d33615e32f18aa57
-79 560cb42220e36d2d
-80 e3bb8b67cc8bf3c2
-81 91571076d062b2fc
-82 34811346f41df02c
-83 7acbdb9fb68ccf4f
-84 babdd9297791db26
-85 bc78665b10d40d59
-86 9f628dfdf729bc9d
-87 cd9f18ad81757776
-88 035bf3b84a39f5d1
-89 5636099bb2247f85
-90 7b2b70573bc34dc7
-91 6d5602354891aa7d
-92 36d472010340a7cd
-93 71fb8ee0af903916
-94 0a2cc92dafc36eb1
-95 11cf312f4dd555f1
-96 daa1316c46a8cacc
-97 7ae753092682849e
-98 a6df362b9b84661c
-99 e7f6da2e1130a49d
-100 8b81312b944487af
-101 dc1832cd722d3a7c
-102 70ce6f349b973fb4
-103 344bedce8a087712
-104 1555a6434ddf1f1d
-105 4674e77a3b691aeb
-106 44063219a6caaae6
-107 cfb51e6afd55d87d
-108 a28af15aa65f394c
-109 cc801829d4da4809
-110 297e41eab4741411
-111 f41f47710c033494
-112 71f849af45bc1444
-113 ea5fad2bd0f7ba60
-114 f4ccf843be882c8b
-115 f080f3cea9988da0
-116 7d930389617bf853
-117 863c44b84a791649
-118 845d94382dddf51b
-119 94a26212ffbcd8cb
-120 0c8414dc51636a5d
-121 07e89fc460cc86e1
-122 986dcccde1199378
-123 a01b4d321301a111
-124 51383f056155249a
-125 82c63b27217fa9a6
-126 6a141de65686246d
-127 c44fc10497c739bd
-128 c9b2e1aec735e948
-129 50f7aabe7f00fc16
-130 115f0723f500736a
-131 f6bcdd112da0ea5a
-132 3866dcef3704fa95
-133 84fc6464806fab11
-134 adb7cb9520469987
-135 810a7e0a33c2ffcf
-136 c532ac6d7a355365
-137 ada295b3e6fe2629
-138 cd3602162db90076
-139 fb992e4dd8be2cf0
-140 57805378db2275c7
-141 c4a7eef58c1a7170
-142 29d53cd9106fcadc
-143 7675a99b80774425
-144 0af83204c3f279b9
-145 5bc69f691666213d
-146 404f24fa66b6d7bd
-147 16eb2618962faabb
-148 97bb23b8fa335fd2
-149 66db294297015787
-150 03ba96762ff06dac
-151 0e07e13534513a3c
-152 13d9d97e466805aa
-153 60b3eb21ce21ef91
-154 17ec797fdba54b60
-155 4a1736cec66d3cd8
-156 4958abe64189bef6
-157 0e558bfd70045698
-158 8370223bd634d898
-159 44ccca214eae373b
-160 212bce1a092c25b9
-161 9b8d4590830af27d
-162 28fc6866e618e90a
-163 f0c637ffccdbe9ce
-164 6b073b8bb6c4ea49
-165 42cf4c79f0faced8
-166 753ebc026b91bac2
-167 aebff3e2998cfff8
-168 f8e659202a2cba5e
-169 da160e738d27cdf9
-170 33cc1ec44e2f7ad5
-171 2aa3b3e1a86facd1
-172 6cb8399495b806b2
-173 73f5124bc70962ab
-174 3bb9d1b7f1fe82e7
-175 d6e5623e482dce02
-176 ac4201b699e398e8
-177 7df6fa48467da60e
-178 eab32d2f9dcb3996
-179 aabd8fc09a13c322
-180 d6e74808256dc0ed
-181 d50950f48ccb021f
-182 a3530f83af5a3d48
-183 673fa108b424a61e
-184 ab5be5851b42c3e8
-185 f5f9a9afa78480cd
-186 62ef172d1dc38e83
-187 21a55f87e800ce3a
-188 78613e0d26d36dd1
-189 329c0111e58f36d4
-190 2660f6796e4bee58
-191 c05b0e63ded027af
-192 7fcab2c8ca5bf451
-193 7e094083f16ecb25
-194 2474367ec8219018
-195 5cf8b2b5e2bffbb3
-196 ccf4d5527190f274
-197 53e22de9da9bda05
-198 c4f0a879fa9a2e98
-199 82cae2d7a5955626
-200 82fe6395f5cbcd9e
-201 ebfc2fe99da55b00
-202 2ddab7afd83ce18e
-203 a549ff1affce9093
-204 ed89a863226cf959
-205 116dd699d30c307b
-206 af63517f5c938a39
-207 579eded3dd0f3d5f
-208 81909fbaabe0cf9e
-209 09d82a2f710df356
-210 37281d72a5cc2092
-211 aceb716fd4f0976b
-212 1ea5ea66dc168e6b
-213 e07d6495e9d7bf64
-214 85297cc1dbd6b1aa
-215 f49e16eb6e17e4a9
-216 55d80329131a3efc
-217 ddc122de7f07a4ae
-218 d2305f128889cc02
-219 47f5992afc58718a
-220 def2db5c1d9e0f34
-221 6cc92f5759c0687f
-222 560e10cd5205f8c0
-223 e42d15dc0aea1b5e
-224 829d902cd338cb18
-225 d8ad2f2014487751
-226 e3b1b56ee0ea3a83
-227 bb9afaff045107a1
-228 fd16a76e4b509bc9
-229 2b296116feb51066
-230 fcb744ebed906a7f
-231 0b4b4392cc072c07
-232 5cbc184b7f622c63
-233 8ccade13f735718b
-234 8a2e9e61d2038776
-235 cfab7969e0633654
-236 c760f629f1877a2c
-237 7fa8f8c2e80d5174
-238 af9815117374f995
-239 a40a3cb2b661a8c7
-240 9f0071e44de286f3
-241 ad4f698de25e2334
-242 9a2505db572a5fec
-243 9c0bdcc3928b3d12
... [2658 lines elided from this golden's diff body — the FULL file is in the review worktree at goldens/warn.t1; read it there if needed] ...
+1402 3c01f1744712e871
+1403 c2ac73c987901e24
+1404 ad9478910127d3d6
+1405 5af46a91e3666e96
+1406 eabc934c5f9b59d7
+1407 19e53a4ec9d72818
+1408 5b7e9f1dc128855f
+1409 75456e291d5ba34f
+1410 0381626b32650502
+1411 22fcdc2282349a55
+1412 043bba8dcc11f5d1
+1413 ea3242e77456bc7c
+1414 2066867de167767f
+1415 50a95063806f4247
+1416 f45e1202f28086de
+1417 a76ee2e1eb947d96
+1418 44356094d6c80327
+1419 7082de10bf6010f1
+1420 d42b7924796d8336
+1421 535132d5f0928daf
+1422 eb194185a054e14f
+1423 e393aaf4bdc6d449
+1424 3c4e33e8457ce32c
+1425 1c5f1d39a9105ebc
+1426 a7a0ad31c4184c9b
+1427 cd7a4af8f3dc51ff
+1428 22b6150c67bc33c9
+1429 121a7dee57107c9d
+1430 92f4864b59871946
+1431 30e25c3ab6a0bccb
+1432 c4e3489642f1ece8
+1433 bbf88b88a49d1f3c
+1434 b6915be58c11c0b0
+1435 2ff19db7a864b945
+1436 cb4fc5c5e35f865f
+1437 3589dd99afc8d933
+1438 c4d9ad4195dfd149
+1439 63efefbde1bd8cd5
+1440 2bebd35cf6c06b16
+1441 05144a7722a4ab27
+1442 ba0fe1bce2e27db7
+1443 2bdc6f610b8bd2bc
+1444 3b04685b82f5661a
+1445 44185bfc04060ca8
+1446 676933671104ef4f
+1447 60ba47b19c178a65
+1448 7d917189e87fb4f6
+1449 01cc4c2dabd19567
+1450 69e15a73b67a768d
+1451 101cf3a565d6f2d8
+1452 c231dc9679808cc8
+1453 82c968dfd2a874e6
+1454 93b306292546d92d
+1455 990645a43eecffc4
+1456 504e1b66e7a806c4
+1457 547a26f0c1887c65
+1458 905b4435d5b38f52
+1459 95839b01ed5ebb2e
+1460 c489c4ccabf9217f
+1461 f4000ba2540c001e
+1462 ca7c4bd8086d4a86
+1463 8c92ecbb5086d759
+1464 22680b536adc0012
+1465 cdc6d955514e3feb
+1466 a306593d0384ea25
+1467 4152ef0720a2d372
+1468 f9ef67c87b671d60
+1469 621ce0dc619dc127
+1470 267dceb26645395b
+1471 1c3d513117180e8d
+1472 e1ebc5cdf29b0aa8
+1473 139bcb8b1e0b2f55
+1474 01294482ed539f0a
+1475 1e4338ad3066bab0
+1476 2999b6062cb12964
+1477 0457e22c6c084aca
+1478 d7ed918da4e0ba2a
+1479 b8ddcafc26821dfe
+1480 1b4e3e25fc1a9862
+1481 5a7fc896254b609e
+1482 cd0e9c9e36164b35
+1483 0a0e3a255695d33c
+1484 f78d733cffccc710
+1485 20fd8118edf17474
+1486 465745aeeab61bac
+1487 a34cccc42beabc3e
+1488 8cbee98c1ccea42e
+1489 7b83958a63c7d90f
+1490 35c52e1bfc32bdaa
+1491 9509b1348d834055
+1492 c3b167cd3aa325f8
+1493 943981475d2513ae
+1494 964d869835670b35
+1495 33ba73dff0ada416
+1496 76d08a84cbc9921c
+1497 a4e663a6c58458d0
+1498 aefdf1ca2cdb03ef
+1499 056250fe56c30e31
+1500 993aa05e7b9a7f70


--- SPEC / CONTEXT ---
The original job briefing (the spec for this work):

# Briefing — packet-plumber-v2-5.11-terminal-types (story 5.11 — diverse terminal types)

- **Job id:** `packet-plumber-v2-5.11-terminal-types`
- **Repo:** packet-plumber · **Base:** `v2` @ post-#65 merge head (HELD — Silas
  resolves the exact sha at release; see the hold note below) ·
  **Slug:** `v2-5.11-terminal-types`
- **HOLD (Silas):** do NOT dispatch on receipt. Release trigger = the
  `packet-plumber-terminal-assets-5.11` (#65) merge close-out — this job CONSUMES
  its approved sprite sheet + manifest. If #65's Perkins loop drags, the 5.12
  queue-swap stays your call. Record the hold on the row.
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any
  mega-minion you spawn launches with the same model — name it explicitly at
  every spawn.
- **Skills policy:** `gds-dev-story` (story execution) — the story card below IS
  the spec; `project-context.md` for code conduct. Your own adversarial pass
  uses `gds-code-review` layers (blind hunter + edge-case hunter).
- **Perkins:** `pr_review: 1` (catalog + director + growth — canon surface).
  **Loop ruling (user, 2026-08-17):** rounds run UNTIL APPROVED.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start;
  badge-out your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-v2-5.11-terminal-types <url>` yourself.
- **Story card:** `_bmad-output/planning-artifacts/sprints/stories-v2.md` §Story
  5.11 (relative to `/Users/moses/code/packet-plumber`). Read it + the design
  spec `_bmad-output/implementation-artifacts/spec-traffic-model.md` BEFORE
  designing.
- **Assets in place:** #65 ships the lavish-APPROVED sprites (small-biz +
  campus) in the sheet + manifest, with the palcheck gate. Your job wires them
  into the GAME. The shapes are canon — do not re-render or restyle them.
- **CI:** billing-blocked GH Actions — the LOCAL suite is ground truth;
  `tools/ci-local.sh` (10 gates) must pass.

## Mission — implement story 5.11 (homes trickle, campuses flood)

**The goal:** the terminal roster gains class analogues — **residential /
small-biz / campus** — each with a different, bounded demand profile (volume,
throughput; per-terminal cap = `cap_fraction_permille × throughput ÷
packet_bandwidth`, uniform per 5.9); a campus emits far more than a home. The
terminal spectrum reads at a glance (distinct shapes — the #65 sprites).

**Hard requirements (all pinned by the card):**

1. **The CODE touch points the card names** (a new terminal role is a CODE
   change — Perkins r1 W7): the `Terminal_Role` enum gains its variants
   (`core/catalog.odin:22`) + `role_from_name` (`core/catalog.odin:1011`) + the
   `collect_terminals` role selector (`core/flow.odin`) + the growth type-pick
   (`core/growth.odin`). Name each in the PR.
2. **The catalog roster.** `node_types.json` gains the new types: per-type
   throughput/volume/cap fields (data-driven; playtest-tunable), era gating, and
   the shape mapping to the #65 sprites. Era-gated type pick for growth.
3. **Bounded, distinct demand.** Each type emits its own bounded profile
   (campus >> home in volume AND cap); the 5.9 accumulator applies uniformly.
   The director's typed source/sink selectors resolve against the new types.
4. **Growth validity.** Every spawn of a new type satisfies `[E31]` validity +
   the 5.6 placement separation; growth stays fully seed-derived
   (derive-don't-record, no log entries).
5. **Readable without color `[E9.1]`.** Distinct shape/icon per type — the
   sprites do this; assert it in a golden: **a T2 frame with ALL THREE types
   visible** (the card's named golden).
6. **Replay + goldens.** Replay byte-identical `[E10]`; catalog fold → the
   slice's deliberate T1/T2 re-bless (cause-documented, `cat.hash` proof).

**Acceptance:**

1. Card's Given/When/Then verified — the launchable reads true: homes trickle,
   campuses flood, the roster reads as a spectrum.
2. Full local suite green (`tools/ci-local.sh` 10/10); determinism pinned; the
   all-three-types T2 golden added.
3. PR body: the touch-point list (enum/selector/growth), the per-type profile
   table (throughput/volume/cap + the math), the era gating, the re-bless cause
   chain, citations `[ODN-5]` `[ODN-7]` `[E10]` `[E31]` `[E9.1]`.
4. Story card status line updated in the same PR (the established pattern).

**Scope guard:** the 5.11 wiring ONLY. No group bias (5.12), no QoS/balance
changes beyond the per-type profile data, no new sprites (the #65 set is canon),
no UI beyond what the roster needs. If a sprite gap appears (a type the sheet
doesn't cover), FLAG it — never re-render canon on your own judgment.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-5.11-terminal-types
base: v2
model: deepseek/deepseek-v4-flash
pr_review: 1
```


The PR body (the implementing minion's claims — audit them):

## Story 5.11 — Diverse terminal types (schools, offices, homes)

The terminal roster gains its class analogues — **residential / small-biz / campus** — each with a different, bounded demand profile. A campus emits far more than a home; the roster reads as a spectrum. Slice 5B (E3.1/E2.1), systems: catalogs `[ODN-5]`, director `[ODN-7]`, growth (5.1 type pick).

### The code touch points (the card's named list — a new terminal role is a CODE change)

1. **`Terminal_Role` enum** (`core/catalog.odin:22`) — gains `Small_Biz` + `Campus`, **appended after the original pair** so the serialized role bytes (0/1/2) stay stable (the enum VALUE is a T1-visible byte, ODN-11).
2. **`role_from_name`** (`core/catalog.odin`) — resolves `"small_biz"` / `"campus"` at catalog load (pinned by the extended `NT_VALID` load baseline).
3. **`collect_terminals` role selector** (`core/flow.odin`) — role-generic by construction; the same scan now resolves the new roles (pinned by `test_terminal_class_profiles`'s selector assertions).
4. **The growth type-pick** (`core/growth.odin`) — `growth_terminal_roster` consumes the new types via the existing era-gated, TERMINAL-only, demand_weight-weighted draw (routers remain player-placed; every spawn E31-valid + 5.6-separated — pinned by `test_growth_e31_validity`).
5. **The #65 sprite wiring** (`app/render/sprites.odin`, `app/render/view.odin`) — role → sprite index + footprint: residential → house, small_biz → the small_biz sprite, campus → the campus sprite; the pre-sprite fallback also draws distinct primitive shapes (E9.1 even without the sheet).

### The catalog roster (`data/node_types.json` `[ODN-5]` — appended at the END so existing type indices stay stable)

Per-type profile = `throughput_units` (the cap input) + `demand_weight` (the volume attractor); the per-terminal cap is computed **uniformly** by the 5.9 accumulator: `cap = cap_fraction_permille × throughput ÷ packet_bandwidth` (500 permille, bandwidth 30).

| type | era | throughput | accrue (milli/tick) | cap (pkts/tick) | burst ceiling | demand_weight |
|---|---|---|---|---|---|---|
| residential | 1 | 5 u/s | 83 | 0.083 | 1 (none) | 1 |
| small_biz | 2 | 20 u/s | 333 | 0.333 (4× a home) | 1 (none) | 2 |
| content_host | 3 | 80 u/s | 1333 | 1.333 | 2 | 1 |
| **campus** | 3 | 150 u/s | 2500 | **2.5 (30× a home)** | 3 | 4 |

Era gating: small_biz unlocks at era 2, campus at era 3 — `growth_terminal_roster` spawns the era-unlocked subset (era 3 = the full spectrum), pinned by `test_growth_era_gating` (era 1 = 1 type, era 2 = 2, era 3 = 4).

### Bounded, distinct demand (`data/demand.json` — era 3 entries, `[ODN-7]`)

- `email` from **small_biz** → residential, volume 1 (offices email; bounded by their 0.333 cap)
- `streaming` from **campus** → residential, volume 1 (campuses flood; bounded by their 2.5 cap — the ×10 surge lands on campuses too, the honest aggregation event)
- Entries whose role has **no live terminal spawn nothing and draw no rng** — every pre-5.11 fixture is untouched by construction. **Pinned durably** (`test_role_absent_demand_inert`): era 3 on a no-small_biz/campus fixture, the full catalog vs the pre-5.11 entry set → identical spawn streams AND identical rng state.
- `test_terminal_class_profiles` pins the spectrum split by window (Perkins r1 W2 — the whole-run ratio is surge-inflated): **base window** (no surge) campus ≥ 4× home (measured 6.5×), **surge window** campus ≥ 10× home (measured 16.4×), campus fully served, every terminal inside `cap×W + burst`, credit ≤ MAX, and the typed selectors never pick outside their role.

### Readable without color `[E9.1]` — the all-three-types T2 golden

New `demos/terminal_types.dem` (era 3, growth on, `fixture off` + 7 explicit spawns — router_mid hub + 3 homes + host + one small_biz + one campus, all drawn to the hub): captures at 5000 ms and 30000 ms show the three classes as **distinct sprites** (house / office / campus — the #65 canon set, never re-rendered). Growth-born small_biz/campus join organically, each spawn E31-valid + min-separated (`test_growth_e31_validity` extended: 20 windows, both new types present + valid). **palcheck** (Perkins r1 W1) now scans the small_biz/campus canon hexes over the terminal_types frame — the positive E9.1 pin (a degenerate/cropped blit of the new shapes fails the gate).

### The honest surge-lands re-pin (Perkins r1 B1 — `test_w9_surge_lands_under_caps`)

The 5.11 roster **doubles** the era-3 streaming ask: TWO streaming entries (content_host + campus), each ×10 by the surge → **20/tick** in the window. The pre-5.11 pin (`EXPECTED := 10*WINDOW`) was stale: it passed a campus-silent regression at ~47.5% of the honest floor. The re-pin:

- `EXPECTED := 20*WINDOW` (the doubled ask); `stream_spawned` counts the **surge window only** (`[SURGE_START, SURGE_END)` — also fixing the inclusive off-by-one); the stale "(2 = ceil_cap)" message → the per-type ceiling wording.
- **Campus half hard-pinned**: ≥1 campus must exist AND source in the window (a campus-silent pass is a regression), and the campus half lands fully (measured 100%).
- The start map is a **grown aggregation crowd** (2 routers + 8 content_hosts + 6 campuses + 4 homes — the player's pre-surge mesh per the 5.1 build-out loop): a single-router map tops out at ~5-6 hosts (the campus weight 4/8 dilutes the host crowd + the E31 min-separation crowds the grid), so a thin map legitimately lands a partial surge — the fair-crisis doctrine; this pin proves the **landable ceiling** on a grown mesh. Total lands at ≥95% of the honest ask (measured 100%).
- The per-tick burst check now runs **every tick** (base + window), per-type ceilings.

### The deliberate re-bless (the slice's cause chain — 4.3 discipline)

The catalog fold (`node_types.json` + `demand.json` content AND comment bytes change the folded hash):

- **Fold chain:** `66c4324a06058860` (pre-5.11) → `250679b1940fb87b` (5.11 data) → `17d3baf8c6e1df7f` (comment-accuracy fold, same PR).
- **Fold-only proof (boot):** the tick-1 state dump under the final code, with the previous hash spliced at the fold position (bytes 33..40), FNV-hashes to the previous golden tick-1 **exactly** (`ab1fb0d04a90026c`); the un-spliced dump hashes to the blessed tick-1 (`d1d2e53b7b1037ce`). The era-0/no-demand shift is the fold alone.
- **Logs:** all 32 pre-existing `.log.bin` byte-verified — they differ from `v2` ONLY in the 8-byte catalog_hash header field (bytes 17-24). (The new `terminal_types.log.bin` joins the set.)
- **T2 partition:** pixels moved **only** in `node_health` (10000 ms / 20000 ms — the era-3 growth now spawns the new terminal classes + the era-3 demand sources from them, behavioral + cause-documented) and the new `terminal_types` frames; **every other demo's frames are byte-identical to #67's** (the fold does not shift pixels).
- Input-parity manifests re-saved (the same fold).

### Verification

- `tools/ci-local.sh --mac`: **10/10 gates green** (lint, **194 core tests**, app build, golden harness ×33 demos + replay gate, palcheck incl. the 5.11 sprite scan, W1 drift-rejection 233/233, preview cross-check, PP_DEBUG builds, stats replay-identity, input parity 24/24).
- Replay is byte-identical `[E10]` — the harness replay gate re-sims every blessed log (33 demos) + the era-3 growth replay-identity test (`test_growth_same_seed_identical_and_diverges`).
- Every spawned terminal satisfies `[E31]` validity + the 5.6 placement separation — `test_growth_e31_validity` (20 windows, both new types present + valid).
- Story card status line updated in `stories-v2.md` (the established pattern).

### Decisions & rationale

- **Role/type index stability:** both the enum and the `node_types.json` array **append** the new entries. An earlier mid-list JSON insert shifted `content_host`/`router_basic`'s serialized type indices (T1-visible bytes) — caught by the fold-only proof and fixed; the final fold is pure.
- **Profiles:** small_biz 20 u/s (4× a home, cap 0.333 — a middle rung with no burst, same latency discipline as homes), campus 150 u/s (the spec's cited example: cap 2.5 pkts/tick, ceiling 3 — the flood site).
- **Era picks:** small_biz at era 2 (the office class arrives mid-progression), campus at era 3 (the streaming era). Eras 1/2 demand is deliberately UNCHANGED (dormant in the MVP — the era-FSM story owns their re-tune).
- **The surge landability:** the 5.11 campus weight dilutes the host crowd, so the era-3 ×10 surge's host share exceeds a thin map's host capacity — the honest floor is per-role (campus half 100%, total ≥95% on a grown mesh). The W9 start map is the player's grown mesh (the 5.1 build-out loop), not the bare 1-router start: a partial surge on a thin map is fair + telegraphed, not a silent cap-throttle.
- **`dc` sprite left unwired** — no catalog type maps to it; a future data-center role is its own story (flagged, never re-rendered canon).
- **No 5.12 scope:** no group bias, no QoS/balance changes beyond the per-type profile data, no new sprites.


--- YOUR LENS ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "architecture",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use N/A ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract:
- Write ONLY the JSON array (no prose, no markdown fencing, no preamble) to the file named in the FILE-OUTPUT line below using your file-writing tool, then stop.
- Also return ONLY the JSON array as your final answer. Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

FILE-OUTPUT: write ONLY your JSON array to the file
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.11-terminal-types/r4/lens-out/architecture-g2.json
using your file-writing tool, then stop. (Your source value is: architecture)