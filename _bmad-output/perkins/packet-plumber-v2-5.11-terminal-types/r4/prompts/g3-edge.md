You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. The repository checkout at the reviewed state is at:
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.11-terminal-types-r4
(all verification reads happen there; treat it as the source of truth).

Chunk orientation: This chunk contains re-blessed .t1 goldens (forecast_preview, health_lose, qos_manual), whole.

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
diff --git a/goldens/forecast_preview.t1 b/goldens/forecast_preview.t1
index 8386702..a9632aa 100644
--- a/goldens/forecast_preview.t1
+++ b/goldens/forecast_preview.t1
@@ -3,675 +3,675 @@ t1 1
 demo forecast_preview
 seed 7
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 670
-1 81d2b689ed930e03
-2 55f30714174a241e
-3 ffd1672f6546a420
-4 024047ea7a2168e4
-5 8c9fe353e2b82095
-6 213918ce307d34bf
-7 e335e5a487c654c8
-8 6cd1edcd830edb28
-9 df608ce96fef23c7
-10 3bcdee9a3ac72f9a
-11 19897671a113abea
-12 9c879884650a675f
-13 a9172db45c43a658
-14 3df2bb711f03bc7f
-15 0680f04f3efcf40c
-16 715e26e9f567eaf6
-17 21290dcdecd445ec
-18 83f494232a5e8729
-19 ce373801e1ee4510
-20 1b980d1a68a876d5
-21 602afca83a274fbe
-22 248d943929d13b51
-23 15106af17bfea9a6
-24 b1e68b165368909f
-25 cded74ed05af7f75
-26 8f67b5042bccaf80
-27 b8865ef9c188d315
-28 2c33163fc6a80728
-29 101332ec2cda211c
-30 cf5aa557459412e3
-31 1a57db5b10e6d088
-32 b9cccf97f407067c
-33 0e61b972ba1c95d1
-34 ab797a7ba75e7083
-35 397cdc69f398d513
-36 c9f50953d27f8fd1
-37 941f994457760a20
-38 5cf3e1cde0ee7183
-39 80bd2b7708e4ddbb
-40 1f7c5e05f19c7ae7
-41 4c798b3550f99c87
-42 ba9e49fad571bb87
-43 bcd8219233b854fb
-44 33d0ce5181481359
-45 b7f29dd1f3c2f7a7
-46 3d5a183c18544b95
-47 0d8db98e285a5d64
-48 764719c433d92ed3
-49 1d97be8f4a32a1e5
-50 dd6b75bf2051d744
-51 4d2a2d1e05cecd18
-52 43d5fe3193f9ab69
-53 ec458774f9ea2a73
-54 4f7536c861ffe864
-55 afd9c92814277327
-56 06de721db5dffca9
-57 6ccb5698f99401fa
-58 a007c6f641c0aa43
-59 663dda937d3f88e4
-60 c9e8fde47609b440
-61 e94cce4ea12ac79e
-62 16c22e94a70210ce
-63 af316e55ab8acb21
-64 f63357b5fe4d6648
-65 5d74f10485e92680
-66 1057f029d4944e23
-67 2ceb369a59cae905
-68 aa20416f77bbb504
-69 b62e8993dcb75bb5
-70 597132700d05b38c
-71 533d763231f61597
-72 2de746493ed5b356
-73 61230dde35b0d1ae
-74 61300966d86a8989
-75 5008d71068371d19
-76 988ecbc86af4d7ed
-77 8ab9d788dc31fbac
-78 a39cbe3cb2fd49cd
-79 56e79439c083d15d
-80 4beb3b6e5daee287
-81 5fd1891bec105529
-82 8b69e6d983068fcb
-83 b13fdc462fb51ad5
-84 1239d8863e2608a1
-85 c14de2180b66de2c
-86 97cbac53f4292fb7
-87 bf0aedbf6e48173b
-88 78a137fd01bf2516
-89 0b73bfb7a9d7ebb5
-90 f9fd14d4d74f8480
-91 7f9c0546df4baa87
-92 096533f8281af47f
-93 a9c0ea5f3c0c429d
-94 544207710bfbcbe0
-95 3bcb64c401c2590a
-96 89bee909dc0fe02e
-97 cc0848e662a53518
-98 aaf8a1d982eb17ec
-99 30332951d2167e5d
-100 cc4dfe7c6c3a804e
-101 ee512f982efec38b
-102 5604c994668849fd
-103 6dcfee3c6c132c23
-104 d7623f2347a0efa2
-105 ed19d962a4336da4
-106 f7f64b1aaad20e75
-107 718160b224cb3551
-108 3abc9841013a2c60
-109 0b1e4372e41b0ec2
-110 65899d1723111f78
-111 3e390bd5e5cfd2db
-112 7a466bdfcbe2e30b
-113 8f1a777fe3b48087
-114 2323cf4d1876a1f8
-115 f5d97d3fdbb0ffa6
-116 5918a30c7d96209d
-117 d1b01ec3b39c9549
-118 d060a06ca4017be0
-119 7d1708af17e4cd0d
-120 0d39064be2859539
-121 6e5fe3af3cd8e233
-122 ee48c77b8d78eca7
-123 f57f4bca70aad495
-124 f669228ae681b93a
-125 6a419723c1431532
-126 cb10286682070dfb
-127 836669289df341e8
-128 3c940d0242bb89f2
-129 71e42898f21fefb9
-130 f641c84558beb9c4
-131 10be5b16be7981a3
-132 e4ad1fc86e9e0017
-133 7ae48d750859a7c1
-134 ae282fa2d88af89b
-135 b407b4c073010346
-136 1d78d7f39fe9decc
-137 475b359777aa343d
-138 56fea83cc2a9c3ec
-139 9cd82f7e922a9911
-140 729b6fbb7d8ddc59
-141 80e22c25edd9e2d2
-142 d40f2b0d65c32f40
-143 59a4883f14a9fe83
-144 febef38845e35c09
-145 f24d4c8b881b9130
-146 01e78bfb2cd2b55e
-147 afa203e8378d0925
-148 dbeb4089214fece2
-149 b796da3912c8f557
-150 d067e43ae8453e47
-151 391b9dabef8ec298
-152 cb69b62e5bd307ae
-153 f23f9b6a3903d41c
-154 41395dc7321d6017
-155 886058141b6cd991
-156 b95deb191a989eb4
-157 05b4ba3a822f296a
-158 03c85bc262bfef4b
-159 dd854522ca84880b
-160 63589ae024d5b702
-161 ee54fced13e4e721
-162 0e105ffe4cd30409
-163 71f10374a3f537a5
-164 69e1527cd0053b77
-165 09272754df1ab35c
-166 c22b36599a47d069
-167 2f96b3b7bc671031
-168 b50415498eda9d2b
-169 9ad14a24323d8be2
-170 923ba661ff69576c
-171 b0909bb2ffbe6f7f
-172 a81616e563c2e26e
-173 9c34f053cb153962
-174 e6ee923f9cc9bfd4
-175 a88bb2aaf35af9b6
-176 5ce99add8446edab
-177 209da78842956610
-178 476b62ffb8b87646
-179 ddd0d175cf65c827
-180 e37b2f7f9dd50291
-181 3fb658a9c552c117
-182 07a795214b6888e7
-183 dff2e2af3b0874cf
-184 22b148a4703f7533
-185 e3d5f3bb1a6e21ea
-186 7635d60f010f84e3
-187 3848202af6b97085
-188 b8953c6c65d04c99
-189 dc3d7aa93b9f8c10
-190 6ada6e5d3768eda3
-191 e2487a32b5c0f8b3
-192 b6d5d3d7901e553d
-193 b7e0ff6dc82c11c3
-194 f98ed407ff33c8e6
-195 bc6d2502312cb8d6
-196 430ea99a2b79e28b
-197 d709a782cc3345fd
-198 e1fefb309c5c42d5
-199 5bc69f8284863cbe
-200 caf7d4b3a4f13fab
-201 bdc538f91bca62c6
-202 d19fb4ddc84ec875
-203 02099442157f9298
-204 092950af8c4d9d55
-205 756d24c8bd399be5
-206 fe7c61db008e09e4
-207 eadb4bac716aa144
-208 d58c8a6ff6dc8a06
-209 4d78cf1ed8c1f383
-210 353423c9cf7091a3
-211 8976fb8745503f30
-212 08675bb82236c78c
-213 baeee5e5a1989afb
-214 7a1193a59f68a987
-215 f478630229d1cbfe
-216 2ffd66332328c4b5
-217 caf088b0fd518d57
-218 86e63f9cd1f78188
-219 fb9d8d5a194aae55
-220 535a322977927679
-221 a85c8964eafeb914
-222 f16bfc0452ffd1c1
-223 e427b728a6e8b484
-224 012a487815794a93
-225 526dc4a592099f33
-226 cb157c5b39e50020
-227 7899fcf4503ddf41
-228 30e31b6fa40ac7ef
-229 6bc20340d0bf54a9
-230 f9b7f86036ba5173
-231 93301cb999a88386
-232 3708f201b8332047
-233 24851765dea4402e
-234 0b1dbaf41a7a55d1
-235 d64a0d4fa56a63ed
-236 930b2dc9bc32769c
-237 b4280eb591f881be
-238 36c77f6b1dac1ef3
-239 897bf12a95a49695
-240 cfc5862271d58a71
-241 f901e5a476dfa1a4
-242 e152cd64d15d7b76
-243 cc181e58d7832607
-244 097270a2331b6f28
-245 ee6cdac06a2c44a4
-246 2788eac9602ede02
-247 f29d18e6cee5b8bb
-248 54ae22c37ccf8987
-249 dec268d2d4ac30a4
-250 13d2db7a01e3bab6
-251 d622937083d89b93
-252 190538adaa4e7378
-253 7f51e64c33cf2019
-254 4e132bb410a4a383
-255 9a6847c4683dc59f
-256 ae165fc25f472814
-257 fabf5cb9a0b042b8
-258 46bb42aff57e8b28
-259 0290e5770b6cf391
-260 0b45327cc03dd41a
-261 9452abd79a8d0695
-262 054d25d998ef9e4a
-263 fdce68e742187643
-264 8bf104b285534802
-265 a3fbbc6644c8e0b5
-266 cb0a4ab2cbc499f3
-267 131ec926e0762a05
-268 95a51ea1683aa8f1
-269 b3848223c1c98d27
-270 8b6fb8ae40de4d50
-271 f3d797ab46f5ef5b
-272 b9525588e2823ba1
-273 355a652b318f3920
-274 8f319b2aaf9e5e19
-275 09a65e9e35ff8396
-276 60123126802fb75b
-277 46ff2cf52a1dd6f6
-278 49dbee99f4242719
-279 5f099f2a409354d4
-280 9b6685af4706a519
-281 ec8738fa3404d561
-282 0ff426407f227c42
-283 4e69b8e5f9bb9b2f
-284 099284d01199042d
-285 f4561dfce09c5ba2
-286 5323f150a90178bf
-287 c4a2cb760eb835d4
-288 b7536b6c4d36242a
-289 f46a5ab49487922c
-290 0da8561ce2704f78
-291 f1200fd7a23efcbd
-292 ad4ee0df009086bf
-293 8da4a35f38bb23ef
-294 7c4ba404e69dd7e0
-295 4cfe3cdf03eb7df4
-296 0b0a5c7ac074a90a
-297 7a4a94c0e33974ac
-298 549a902b938f7b83
-299 4410d8e126067d1f
-300 3e4d2ebead7f9d22
-301 aa505ca0a040ed4e
-302 3ec56b348f3b5ceb
-303 0b5a77dee966590d
-304 0e1bbcd6f85e5dc4
-305 35f2fdf98ac38a09
-306 f5390b5cf0f17353
-307 243e1602ecf15e5a
-308 28347906a5e884b6
-309 c46e17a0fd6e4b65
-310 8b628def199d3796
-311 c4a02e4b22a4a5f4
-312 a4f20c5f4d35e72f
-313 6687e32df9699a61
-314 7b25290170728766
-315 120598b608b49e06
-316 301ebceed115b24c
-317 3c07911e6704d0b3
-318 ee1d6395e6ab2f6c
-319 dc43ff8aead74341
-320 769a174dd0a7b318
-321 68d961ed08a7e638
-322 4b5e7b97bba1aecf
-323 6d57949715cd5356
-324 393bbbf2f11f7a49
-325 2521e1861322f2d2
-326 27227b83ccf28328
-327 55af8508df5fa5a1
-328 85517aef2aee37e3
-329 e46248aea1d3b3bc
-330 a5b333dd47ae957c
-331 01ed2f61cb5bb1b7
-332 f4baf2bc62465377
-333 3cfbf42a41dc759e
-334 4a437da82b6570f6
-335 6e5650efd082de60
-336 3516799aaf021c62
-337 83c44dc6ae366b44
-338 8e6b97c9a6901c43
-339 7abd8f495abac55f
-340 d667ce34f2508df2
-341 dd2f7c017266d6c1
-342 dfc5b846f27a6449
-343 871d7db7befafa1e
-344 2fea9fabe609d001
-345 8c203cf9e1a22f6a
-346 90d1360e75c1bc4f
-347 7700bdd2166035b4
-348 9d12205ba066faf9
-349 48b14193a3229105
-350 9ea08fc586c5421a
-351 a616351716cf8d6d
-352 ed7ac8e6cda94a56
-353 1d52495a37bde74c
-354 46820538b6f839d4
-355 724afd7c6540245a
-356 f3157a8e8d337836
-357 5a69534d8ae7bca1
-358 507b51efdb7bf43d
-359 15cb159de1a5af32
-360 082092f9d17e5103
-361 b581fbe4199eaafc
-362 e4bd00c1ccf271b9
-363 c7250a2ad50ef4d1
-364 13fdb94c03c1d706
-365 974c393c96d05f6a
-366 fd0d1b1ead81d863
-367 448dbc93a07b76c9
-368 da62973e8fbbc0b1
-369 6e195833c03d943a
-370 08691232d7cb58f0
-371 6e4df559259120a0
-372 0ecb7a3b0c86794a
-373 93b3213f5444d289
-374 54ff63b2f8349e0e
-375 58093b8c3cd16bfe
-376 e334fbcadaa87736
-377 d4084b35e37b23a3
-378 253e1f5abab685f6
-379 3c9ee02cb4fcfe40
-380 3e383abf435e8272
-381 c88ff2d797db1c2a
-382 2c0b9545c80ee8a5
-383 40e5bf55f0ec9ae3
-384 0b443867cb93e69c
-385 43d51e74ebae0444
-386 d56933274c4c452e
-387 f1c3705ccdff07f5
-388 aee717be39934df1
-389 c3599fbecb9764c7
-390 fb3f3b4e098229cf
-391 e09d3333a0af6491
-392 fbcb6d8f9b898f6b
-393 567e6c518e30a411
-394 86608e6875d41d52
-395 20b12176746e1d28
-396 92bab1376e431cce
-397 49f859e2ddde693a
-398 9e2fbf48c66d7cbf
-399 889a7e4dbd67edb4
-400 74ef36483fb5e3e5
-401 de7269e9666e9748
-402 a05770dcd3251220
-403 17ba3b95ad672fe8
-404 1eb6abd972b0b1f0
-405 164da79e33082409
-406 ddc5653bfb5b78d6
-407 253f1f7e06ca6fb4
-408 8a252104d51a178d
-409 a4b1316fadf93894
-410 fb42392aca556f24
-411 2163a3e7c8b5b4a5
-412 6fcf9b4d23518fec
-413 472d9b5666024fa4
-414 70d3b733ece1b82d
-415 fa1534c524373c71
-416 92a425a7d137a156
-417 5a2c737dda06327c
-418 7093bffb12d67f34
-419 a4c6fb8042a9575a
-420 1d6e8848bfcccb30
-421 e12b436a7c2f99a6
-422 e5196ea0f195bb64
-423 810ca6cf73e16639
-424 11380f89a5e47f66
-425 ad00253203a55a7f
-426 1eab9de1d9b150e1
-427 7d4dcfc75e60947d
-428 4b411d6a7013d1db
-429 9b4ab4ad96e34913
-430 1f394140498e9d1a
-431 525ee3035b080cb8
-432 e2fca23996aedc59
-433 37b1ca0e45dd0f7a
-434 f574244662c90372
-435 4a04fc8547485d8c
-436 1897568d3c62cff5
-437 abf28ab88d9d768a
-438 b47f6c242a20e6db
-439 5819bf3ebb086335
-440 2a615bf04fd1bcbf
-441 a1fda386d70735ac
-442 c5e2c068d3edc4e6
-443 9063e9e291b0d6bf
-444 c01039b723dabf38
-445 5f4d0fb1ce5ad13e
-446 161799f91d13e1bf
-447 e30602c69fb8fe5a
-448 d70ab2338633f3ec
-449 c3b5313633547e02
-450 322d501272aab2ce
-451 872e562cd8a03edf
-452 d20eb94d7d7f54f6
-453 9efdaf9e30cd3bcc
-454 d6015861ade03567
-455 e9ad1d87450eeba2
-456 d84831f1719b0f16
-457 9d6c9e332fa97319
-458 828ed345c9ee5abb
-459 bd33e54f5157c519
-460 8145b789d3eec87f
-461 df51f0fcc451bf32
-462 704fab929e51ff8a
-463 f77a2a44abaa4597
-464 956117c516b50567
-465 f8d90330206c5e13
-466 caf5ae252525c2b3
-467 a20fe17a699a77d2
-468 ca11a0239bf0beb2
-469 9f6a0211a9a0b7af
-470 204dbd9471eee23e
-471 d1f6ff5d12f7365e
-472 439633ec3ef67fdc
-473 ae1d24d32a5aaea4
-474 de2c2719964571d0
-475 f12bd1bf16aea9c9
-476 9638cc35bb17a37a
-477 ad1983f9fa4abf2f
-478 a9811412966ab857
-479 3f8a012e8d5a2441
-480 443beac1962d404b
-481 9dedc86e3c82481e
-482 4e4a826abb426d3d
-483 410361f3a96594e1
-484 e786c221c9e14fd7
-485 16b669bf89abe9a3
-486 23da1270f24076c0
-487 9daac9691f1bb2d5
-488 906bc33a1b32ceaa
-489 0eb0919fe79258df
-490 afd373f7e797a631
-491 05ac8a43aaacc059
-492 cbe927c693bf14fd
-493 4385e5fa220d57bb
-494 450b9b3dfd49b4bc
-495 4dcbc2fd0d07be15
-496 d7eca60fbdd803ed
-497 82f39278dc2ab3b0
-498 5823d5f274dbab21
-499 6345d3ce02eeb7a9
-500 644d70c4d34c9df0
-501 66f8a3fac8b1eeba
-502 9957cd906734147a
-503 1ac3577cc1db92f2
-504 f21a5bc5374034e8
-505 135f53c7c49cd70e
-506 ff7058d71d2976a7
-507 725584db611611b6
-508 d7a35cd96d966020
-509 b8d72320805d7feb
-510 f5c60ddb6925e9b5
-511 8f9e2ce815dfd9e5
-512 199c466672e9fa9c
-513 32c23f863b0f2d61
-514 6f43d364390c3089
-515 f2aed1eda1fc8e6b
-516 7f64ef95e1637a53
-517 306bd704fe792804
-518 fc816509c8669a01
-519 3985f647447a30c9
-520 9fa300a3ba049355
-521 cb55a960d6d7d211
-522 bf16bc72a2a90da6
-523 11690fc6fb44e11c
-524 fc1aa9c66aefbc49
-525 d30ff791212a81e8
-526 d0ec5014afec6515
-527 732ec88827902cd9
-528 ea2494ab22aa9208
-529 a56317e1711a5b31
-530 d67271fb4ecf682b
-531 5cd5da245b4ddc72
-532 64c8e477c749e403
-533 01697859001b4d3a
-534 d222578c93a93619
-535 60f3cbe2309f6b7e
-536 87f9298fc22408d0
-537 09fda608fef5ff4d
-538 3f243a984bdc4ac3
-539 8ba39efc46f1e42e
-540 d3e874d829f80ac7
-541 b064cee5995101ac
-542 14f4599b380947b3
-543 ad737bbf4524416e
-544 a98d121cb73a9582
-545 379a8ad9d2911851
-546 d1ce98332f683d83
-547 cab20f32c438e9cc
-548 2177a3f94860dc4d
-549 f8937ba94ebd7e35
-550 012cfbee10103d9a
-551 4174bd3682fc8ae4
-552 d93af351f15986eb
-553 c0a95b5c03e1ecfd
-554 26e1fddfceadbe5e
-555 ff2258009424f813
-556 56ff7c604abed684
-557 37bd149bb6d0100e
-558 f7d71b967a2fea08
-559 aae0283171e4830d
-560 48718058650813ff
-561 18e4683542084a57
-562 2f4cfc86fe771be0
-563 92cb2cb565eb59f7
-564 ce6b062bf69ebe08
-565 9a61d1a37eb35801
-566 e0ecdaf8746aa8ce
-567 13cd0c2a741345c2
-568 d2a77c8bd37085dd
-569 2e01ba16a427d049
-570 09698280058923e9
-571 b5089e3a88b833b8
-572 5f9dc2d44a53d1ec
-573 47eca9a099f6e4c6
-574 66b3eb9424436f9d
-575 4674114941011682
-576 10d7cdca5e372664
-577 89248b83613e1934
-578 bc7e6a4cd3f13d11
-579 c1f454433fa85f77
-580 cb84840dd9d59fa3
-581 be4756c85613ee2c
-582 fd845396337bf924
-583 ab6238d459f04295
-584 3bed32a8f34b9536
-585 c965284a6b6c25c3
-586 a00afd34abbe99da
-587 aa1d895e65263b2d
-588 9047aab5c1c7ba8d
-589 7da44409161311c1
-590 5be0664341107f32
-591 f9015798a7af4494
-592 aa72abe4f14e205b
-593 7d4c146343fbe4b6
-594 1fc7105c90bb6cac
-595 8ea98e1ade8e6d1a
-596 c06b46f7f0a41124
-597 e331c4a9081aa2fa
-598 c180b538346b326b
-599 032222a7cd6010f6
-600 be5a51fc0fd2a732
-601 49ce283e0eb44311
-602 7c48c7e6ec9a09a4
-603 873c2bd9d40e7809
-604 b2de50d988976500
-605 da5861cf62ee95e4
-606 04f906a8cb8838e0
-607 5ea4c9ce3554e671
-608 5002487d09a85231
-609 9b78b9226220f377
-610 5a308a677bddf6a7
-611 75db7660b2cf5d26
-612 426b17f1efb4dff4
-613 3eb279d0709dabe5
-614 0915c8d4beefc77f
-615 b07c75e8211c18d7
-616 f627868c60196703
-617 399e9ff77321485a
-618 e2ed950b8e29cffc
-619 ae1bf2ed56ad1d96
-620 bfa22aabf1229b1b
-621 5eeedec573496e92
-622 8bd26dc3982899a3
-623 080d375702b11eea
-624 56685894c4c90c83
-625 cc24e81bd7f80fc1
-626 0fd9cb5604f638a0
-627 35e7bf554d1faaca
-628 4f03b426d57048af
-629 4fc405146e49088e
-630 3959bd61cd501400
-631 506e7b3d8885ec41
-632 7f53c869e3cb5360
-633 e08822d61802ac64
-634 deccce1591c43b4e
-635 1f390fd61c637711
-636 7e1cbd9df29eab79
-637 949f05afdd713c9c
-638 ff971c99842052ef
-639 83c2d231f02e4677
-640 e43243b5e077c882
-641 0dfac6ccad17735c
-642 f0aab9af814b9b09
-643 9e4d85fbe863ce95
-644 1de43e9a6cca81bd
-645 deefe87384796ab6
-646 ab4e350ffc47c2e6
-647 ec21a67633be51f7
-648 ce80c407198417a7
-649 0f7a1c1e4b39818d
-650 2e9e96915709f4c6
-651 cd64a2235b30fe43
-652 c69ddbec78b01cc2
-653 b57fc1e6c5694ef2
-654 32dbe735fcb78342
-655 f6025714bcc580ee
-656 661bf090408f8f9b
-657 8296013d9784cbf6
-658 2a54857a5109477a
-659 6303a0a0dc8a1c19
-660 8538e0e3f91a4701
-661 bce506700f7adc42
-662 3553431c945738dc
-663 1dae22ddc9bbd63e
-664 e88785e69248d7d1
-665 aad8ab20d52c3bcc
-666 ff5c672ce4ea55b7
-667 352cb6edb01ebedb
-668 641d35771a0eae20
-669 cd8829ea927defb3
-670 565334a8f1da923b
+1 2e6761687d573e97
+2 357b8ef9cc7c2bba
+3 8e7c70f2555aa524
+4 eb3383b91a054718
+5 bed935ab32e02139
+6 ca86d16a87144aaf
+7 0178f26a8705f24c
+8 e1f88a415fd5decc
+9 914995d2af8079e3
+10 63b19480e07f45ca
+11 60538a24db9e0536
+12 a7755524d05d1693
+13 f76b5d72fb9800cc
+14 b97d65825b99363f
+15 98d18e5136611bbc
+16 11b3f984d4a58f06
+17 d75871d9ef2691fc
+18 94690629e8719935
+19 27cd430d140bed44
+20 f66d04d045da2db9
+21 f60e672e5e38208e
+22 58c3e18f1f9792b1
+23 8a4cea3679c199da
+24 3a75dde4e0dacd0f
+25 7e3d00f8595b9e21
+26 6f33bbb987f66414
+27 ac5a4773c72f8f31
+28 a7ebaf164377f028
+29 9b5840701c095e5c
+30 ddb3526ef43fa6df
+31 28d0c3a6f011f0ac
+32 15026281be4176cc
+33 9e2ef0aefaf6fd61
+34 3e1ef0bcb9701db3
+35 62f475b1ed386983
+36 efe6fe18123b9e5d
+37 512b3fe2c8d08810
+38 93835411d0647147
+39 7043d99a3aa937cb
+40 d4c988d740a27bd3
+41 5d724242225e24b7
+42 5d2716af875f9fe7
+43 04626a7421ade22f
+44 6989fecaeba5ea05
+45 c07f3bca0be3804b
+46 ce67397aea952b31
+47 b6556b1d59486854
+48 1ecd3a3134f3758f
+49 1d4747a225af0251
+50 84aa7ba65b8ab404
+51 6de3c32ef169f4e8
+52 2e55b4052e1bcf05
+53 19fd2cd16c8d3823
+54 623a834f7446e5a4
+55 57eccbb4c6d7af03
+56 b832f3f48d4620cd
+57 7110aa4828b7e48e
+58 bada2e7c4e3bf847
+59 24fd2078b011f3c4
+60 3a4dff334f55e43c
+61 a880fe9fde872152
+62 2d58b4938aafc73a
+63 291a0bcd58346071
+64 a627ec5b676847f4
+65 498a10ed36af1cac
+66 6c38f7d9ec8eb02f
+67 ef92db19c4843501
+68 50438ef7ee4e85c0
+69 32cc6749b3747145
+70 230ddaf8291e9e0c
+71 04a218c49bde62eb
+72 9234516761fc8366
+73 74e9871167d73d1a
+74 8365e0ff1d2ede19
+75 5e706145d6554b5d
+76 589af0ea6361a301
+77 ccc97b109a6513e0
+78 a9b3732a7785f19d
+79 22569284724cf609
+80 57be179bfb000493
+81 e3e37822057845e9
+82 84861a124738422f
+83 4dfa76cf3e4a3b99
+84 d875269040183bdd
+85 59b6397d8eaf092c
+86 a8efe7c39eb36a1b
+87 b5423e0aef4f9f3b
+88 5015b2e38d733b72
+89 658afaab6fd16075
+90 851973a75b2bc430
+91 b13c8042aadb3077
+92 ddfae45408f9b4cb
+93 85a7c7d33badb039
+94 1839f52911437834
+95 f4993078424c049e
+96 5f3135f19c60a022
+97 12a8551ca0770b2c
+98 df1fb13d7f9b08ec
+99 c76e3a6b2e9c47cd
+100 bd9c766995360d3e
+101 dd38052aaab430bf
+102 af595bcb67727199
+103 49093ed1815f7843
+104 5e8f53885b2fe0a2
+105 1cdee98e311ae6a8
+106 4d6741833ebd1fa1
+107 36772c65febdc611
+108 da515da9f79fd424
+109 a99bf5253d61b9c6
+110 9c9f7e6c56199d54
+111 630db458f7ec6edf
+112 d061fa0edec3948f
+113 42be1cd7063f4157
+114 e3867cb859ac62c8
+115 1cfdd6c20e940bc2
+116 b91747a570165c2d
+117 c49c0f3db961a229
+118 b8d1c301a5f4a4c0
+119 9205803b2e0ef02d
+120 773d1c932689a3a5
+121 dd403300f1a9022f
+122 bf28383ec5a33eb7
+123 b12041b0a9ff7735
+124 f22721485a01ac56
+125 29c8d09e2aa09f72
+126 b8090045880fdb8b
+127 652a958e26285188
+128 059d27e71f1fda82
+129 27e0fe7c2e7e57ad
+130 72a82eb896a2cc34
+131 cc89b5bd9da085d7
+132 03df0bef7daa0f47
+133 5cfd828a8607a2f5
+134 e9d9aa7310a76a6b
+135 5a2f974ace5541fa
+136 e8a5b5f77eb351e0
+137 259f36097d786ac1
+138 6a9f408f2b4cdb7c
+139 1c3918a9c2d47db1
+140 b372518b679246dd
+141 40297244b79f46f2
+142 43c66f13cbc9c4a0
+143 fe81b64798dadea3
+144 48d182368ce55649
+145 2f5e462d46b750b4
+146 d5258e92c6d571c2
+147 67492f931e4ce4e9
+148 f15d9e14dbbe648e
+149 0ed4a50e372b0ba3
+150 bfb7abfbce0fc717
+151 58282f4c32726944
+152 81c5e743bec8a4ae
+153 931784ba5a50c5e0
+154 61ba90cfb49d3bfb
+155 9103ecdef654c4ed
+156 1bdbf6629ef0d1e8
+157 f8cabb99d0850c6a
+158 ed4008ea60299ac7
+159 1e602cb42849b137
+160 124bdff8b64b2aae
+161 c4562bde7d75f011
+162 2109075884148c09
+163 97a1772dfb1f0129
+164 11501a3e778ecdab
+165 c1c7c870c86e2358
+166 da3d173e1f9988f5
+167 9570cf59393a464d
+168 1a30c1ddd9f3e367
+169 12ee3ee58e136842
+170 919c8027fabc0330
+171 0157bda9aeefc2b3
+172 f57f6ffebdf09f12
+173 6932a4f77fd60d32
+174 af6c3bd6ef4589a0
+175 857a40011d2305c2
+176 5f0bc94d35a489c7
+177 d171856019186c80
+178 5252a4402262b546
+179 99c7e135987f42c3
+180 59ef7c1befa0352d
+181 cfd03f21a694cb27
+182 e5a4da258d888d67
+183 3025d6aca220238f
+184 b17d5c4cb8d4e073
+185 e8a65291a9c5022e
+186 d59b1bc2831439ef
+187 62919dc719661245
+188 2e59def1bcdc5bad
+189 5750ced04fdbccd4
+190 7b56dcc1b7aee533
+191 0b7ccf504b770057
+192 c9e4fdd5a925de91
+193 be9acb02eb5bdca7
+194 06d9d7066d6e7fd6
+195 264d861c297268c6
+196 dbef157e5997db9b
+197 55f329b3e67e4329
+198 9e9f30668c76ce95
+199 8309710e02227082
+200 164a525e911e5ecf
+201 1c1e0e3245a96daa
+202 f07172507b8dd449
+203 81c87f11931c1f3c
+204 d689742fd146f561
+205 1100f32989b157a5
+206 d5d81829d1d26aa4
+207 b128079cfece1af8
+208 1d90abf095fe0526
+209 6adce954135641e7
+210 35703f918bd97373
+211 735581c4e7986cc0
+212 58d32fe97cc2df6c
+213 c34f4c2caf933187
+214 a55dad12caceffdb
+215 413ae1d1874c3e32
+216 c5cecc97c30890c1
+217 80266c3a013e9ba3
+218 e7e42a8211837d44
+219 fc682f1f7cac3035
+220 d5ad5fe030a762b9
+221 f2a63cf73ef26c78
+222 be2035e8c7437121
+223 cae3ccc7941f9754
+224 6c6ef8c5507b51cf
+225 9bc5e301c4740587
+226 606fe8c6d737ee74
+227 5976771f1310e651
+228 ed478258e4a1cf2f
+229 6b7f5a570e25e71d
+230 3c01b025942dc377
+231 2ffb19f640b42f0a
+232 c43209e02e7d6227
+233 4c04e17b7b30bd9e
+234 7465664951b1f1e5
+235 c5374b766197943d
+236 9d3ed2d25ae31e70
+237 b9dddefbb1e2e862
+238 11e08a972049a14f
+239 8286c4b4a647ee39
+240 d8d0442af5ea37d1
+241 d3628400a6bae220
+242 41f853251c61649a
+243 7717b5d288a2e9d7
+244 46c39400cfc60c58
+245 613387d18daa8ca4
+246 d5d77c4017da238e
+247 460d8c19b00b16eb
+248 32af8a707c3140d7
+249 54941e2bdde18d54
+250 c854ddb0e7ac4e76
+251 2df0e8f225c14bb3
+252 7cfb7238c41a5878
+253 b52e827ed0de4a25
+254 57a17bd94b785e27
+255 3909cd885f16cecf
+256 bacb40616f99aa04
+257 267ccdaf6b33b0e8
+258 0218fa5fdffe9e64
+259 ead2f6bb46f160bd
+260 aaae60b1c902b7aa
+261 c2696cf037f81575
+262 2e14cb71faf399aa
+263 7f0eb56999047747
+264 db1f3de0fa44845e
+265 79f410e0f0eeb785
+266 870b1d48daceef7f
+267 61e92a6ddb6b8715
+268 1acb8858c79140d1
+269 42fe896101780ee7
+270 d0e1c6dfd2d00470
+271 f4f81a4bf94a913b
+272 cf43d2dfe35ed881
+273 9aabaabc4ace059c
+274 4cab4dddcde2cc1d
+275 7236e96d2bda7b7a
+276 b23de104de424b0f
+277 22519cfac42393d6
+278 0d0fb781a3216d45
+279 8bbcb8679b8702e4
+280 051566a79bd57d6d
+281 066e6d48b9ccfaad
+282 f99d3333d5e5f5d2
+283 f5f35c2cd69fe8e3
+284 c26f928af3f6c4dd
+285 30ca0735b8f6ad46
+286 961b7b57763d7fdb
+287 3c85b26edbd14f70
+288 66fd6cbc562fbb66
+289 c0b8a3e252bbff2c
+290 6fabe313742c94e8
+291 710eeacd43e311ad
+292 365eb96dcd99b48f
+293 17f00a21a82957bf
+294 34979d6bbdcd4d1c
+295 1058b3739362dd08
+296 05cbe2e822a2ed5e
+297 f43787dbe942856c
+298 b6ae8628fcc657b3
+299 af445e3984beed6f
+300 ace25ea6b27cf762
+301 a1b4955d6c8ffaaa
+302 2031da4985d51b9f
+303 01f635954efa47a9
+304 c6c7d15fafb3b9e0
+305 b6317584c55396a9
+306 f910ae2f0533f2c3
+307 1f968b42913ae89e
+308 e75313112d3363ca
+309 efcb94ffce1e82b1
+310 74114ae8fc5432ba
+311 ca90c373f9574064
+312 4094051d5f7d8e0f
+313 c264c30ab4aac34d
+314 399bddbe899526c2
+315 211ae25b48437642
+316 5e3bac490eadcb08
+317 54b5f1a222bd5ad7
+318 415a9cfd619dd908
+319 ee1edef3e2fa83fd
+320 91e4f7ddd9587e9c
+321 3022a7ffd2a3939c
+322 acc67fed1702ac73
+323 9508e9348e0fe7f2
+324 48b3ddf606685989
+325 40eff847a7641fe6
+326 f9a9ed82b72597c8
+327 e4c46e8ba2b7eda1
+328 80fbb4a8bdfa1c73
+329 b2a06f48bfe1ffe8
+330 fc04e88f2d48c810
+331 bf7a09f8ff105c27
+332 9509ccce23bdbd97
+333 e04a54285cdc31be
+334 be2c5ed8cf6655b6
+335 4ada99ba3762e104
+336 ba339941b19cf712
+337 2e32b1b918d32f34
+338 d52706a6d9b99573
+339 88e9e8e5f30925cf
+340 17cac221d9d62736
+341 a9a5e8842d37bdf5
+342 eb46f9eded41a709
+343 18f45ea320089dbe
+344 486bdbdcc4c5f991
+345 9c7e598aba14a77e
+346 ff22a9e8d58ac5f3
+347 feac860f370a12b4
+348 0c246e655404805d
+349 9029de3065b0fd45
+350 f71ac895d12b7f6e
+351 807618a602a1510d
+352 0f5681bb6f382242
+353 9b0377a060391e80
+354 7f74ab88b97f4e50
+355 2f142e1a1babbf2a
+356 d668e1467da13812
+357 cf162d18c31e03d5
+358 b6b84c889569b4c1
+359 275bbd136c820cb6
+360 a430520b72e67543
+361 ad32d82daa501c40
+362 8e73c576d1c6e679
+363 63deceebdee46dbd
+364 5f071b838910ce62
+365 da95d1ecf4f6802a
+366 c02ca96d7d7b32d3
+367 06fb4cc59d9344c5
+368 eabd9a7b7f07a86d
+369 a35c0c6c5c41198a
+370 e8007049482700bc
+371 df68de35921b1354
+372 d7f9059582cbc4ea
+373 333a4e7092503b59
+374 cec6e6e979818f22
+375 62785d0a0686ea3a
+376 612c9e86749bba62
+377 c2c9621a227434d3
+378 52693b57b211e542
+379 093b9479e85b44f4
+380 fb671e4fa79636ce
+381 6cbc70ee4ca3e416
+382 6984514665ef1c49
+383 94ee823273e3bf37
+384 840b9fb0a0d141cc
+385 9138c3d5cd8b6a40
+386 4a3fb3f03886c3ea
+387 c0544d6b517d1239
+388 04cf64b84618f4c1
+389 80509246963d5aeb
+390 9f390d12caa63e83
+391 03802f3d9fa0a61d
+392 2e1fce5a342813f7
+393 78dd8bbb1ccd55b5
+394 402c684e9fd96dc6
+395 32f6a659b6aec508
+396 fa951cc3e67909ba
+397 dba77c0230dd193a
+398 3dc8a8c35d202353
+399 32f4e4958d8b3644
+400 ce313f3e65b4af55
+401 81045bb927504448
+402 34f64f658bb888e4
+403 62cb1df6cdc83308
+404 611d3fbb1364d29c
+405 0eba8afedc6f9d59
+406 c76cfd6068ee9236
+407 48cbac76420429d0
+408 af76ab799f7b6e2d
+409 1c87ef2742451558
+410 790163ef93113fd8
+411 43790cdcf827e099
+412 dd035be31bdabd5c
+413 ba82fd8e8b2e8270
+414 f68323c3426992e9
+415 5cbc8ea93dd5db1d
+416 b0161db1f7c70f06
+417 bb37756b806d3b20
+418 b362635a77e5bd84
+419 14e1ca6deef552aa
+420 eaccb3b70ecb8390
+421 e359b07df8357336
+422 a8e171a1c92506c4
+423 316467ff680e9a49
+424 8197dffe5edc743a
+425 1470aa1d66f2973b
+426 8c12031309a98091
+427 c50b6ddcdfc4236d
+428 047b6a393dcdec9b
+429 9578534e9f4a58bf
+430 7754305ce8c4c30a
+431 3a194203fd61f38c
+432 2046e97012b1f019
+433 9b4b7721481a6a16
+434 01d500d79ce07622
+435 9ff7d6d0f60243a0
+436 a96e9336571f8c81
+437 557d0b6b4fe3b81e
+438 ea3dd9bc270b5b9b
+439 335ee50ea4900f61
+440 0def31e0924969eb
+441 d4a10034b873b308
+442 8272f235092c3132
+443 e65fe2f33f76ba4f
+444 18f0a56679e0b03c
+445 7af806ce43fc91ea
+446 41ebd527971e366f
+447 e524f28b71d80e5a
+448 07864386e2be5478
+449 2488c7f3bbc794e2
+450 b6a2231763b87322
+451 43c95ef871bbab93
+452 fed44d5d7b38ff22
+453 8ba94120127d6f60
+454 66be0bfbf88dd2e3
+455 aefed24d2f1bcdbe
+456 f24aef6d3eceee56
+457 9066c241f4bd2fd9
+458 5b546ed5b45a9fc7
+459 9676442c7bc6c4c5
+460 8936016825d39b03
+461 b7d935dc20530906
+462 d81739f23ebb8e1a
+463 50427751541d0bc7
+464 ab834e47d9348db7
+465 4cfb046451a0c8e7
+466 4a5342aebd92a763
+467 500e8966c8b2351e
+468 9ef79765096c40d2
+469 7e8c25342dea539f
+470 3414a9adefdd14e2
+471 515b086239e797d2
+472 d415c9c0fc0585bc
+473 f230a7929172be94
+474 cfe87f5f3c0d1e30
+475 5d02b3e0f9c5f395
+476 15324d91b6b0629a
+477 0f263f97f2798c5f
+478 14cc3c81419da557
+479 e848675bb408e8b5
+480 a2f433bf791166ab
+481 38cfaa2e95adc85e
+482 72a7e66c010a38ed
+483 d09d55028d9f5d81
+484 e1ffa1f88710b303
+485 2b86fa2d2aec5c77
+486 d3a8f9cfb90aff1c
+487 f912f008e07f0381
+488 4119d4e66d3ef08e
+489 aabee4d99fdbc22f
+490 1d64ab5788ddace1
+491 67cbeb6e05492685
+492 65b1d5d5bb0c30ed
+493 0a54591f227a09fb
+494 468b8ef1e29a0d1c
+495 8ae6dd1b9b0eefc5
+496 04f8c8ad403a4ce1
+497 620a3720b404958c
+498 9d0bcf18e9f76c95
+499 8c219f181f96a319
+500 7abb079177e74824
+501 9ea232d8a502b78a
+502 00c83417df943c66
+503 171889dfb62ef252
+504 4239f0f3c7b55528
+505 32f150f42c94f42a
+506 3c3d3a6838a44107
+507 e91e1de8eba8f442
+508 2c19341ade6cb22c
+509 34cf8bddb5d8684f
+510 92d73307607fed85
+511 8cdb856e7ef48fd5
+512 f6ae7faef120e94c
+513 601fb351b304ba45
+514 b8a3898467bb0215
+515 948cd9e0a6648d1b
+516 67bf15a7ef039bbf
+517 05f369cf8f33e2c4
+518 b8e4851cc58ae1b1
+519 9b667df075be74ed
+520 b372d1f6fdd11439
+521 85f36d4eaf33e0b1
+522 135233076fea61a6
+523 4a9569e45a29f418
+524 494db0c8ae54ff79
+525 800f62cd74783284
+526 51912f3f70125165
+527 f7bb343407e1b839
+528 80df4dfc3731a574
+529 0f14bf79dbcdeb51
+530 af45845a973fb3d7
+531 c219d06bb4f83202
+532 2806a40e768ea453
+533 3526ea6ef1f203ba
+534 df688e36fd609289
+535 cb83ac1161e0354e
+536 bd72f5a16d7c2bb4
+537 155fc2ff7683e56d
+538 12f4ff80c40eb7d3
+539 d9c04864263967ee
+540 dba2a36eecf5ae8b
+541 a944875d1b32fabc
+542 5af1eb30c2fa9a77
+543 df979f2e323b693e
+544 e4927d24a11977de
+545 931eafb746639f31
+546 4274864108712ef3
+547 7b13a16c13488b1c
+548 00a86701f273e289
+549 631fe311648e75e1
+550 30edb8d602eefeba
+551 68f7971c95b25d00
+552 3bbc606b8d9076ff
+553 5114f3294bcc4acd
+554 f6aa26a83aeeff9e
+555 1c6fd6ef805fbd47
+556 b4a475806bee23e0
+557 33489fb3c1cf75fe
+558 232c683c5bb155c8
+559 84f1d9c37d547b3d
+560 1d037bf0ffd0946b
+561 cc155839e1ac1b4b
+562 f754432b9e4aec70
+563 402030a5fc5d6507
+564 0e0f2132198d7f4c
+565 8be8dc49250ce4b5
+566 fd11b20127e65d4e
+567 9a584601a0d76af2
+568 4fdfd74511601a89
+569 0c24640a672d3d3d
+570 73427bcaa43f176d
+571 b8aedee344db3244
+572 47512e985b3be3f0
+573 e76e3f6dbe84fa96
+574 29c5c64ed582220d
+575 ea9677b785bf147e
+576 ce8033ce405b34c0
+577 af30e4ada5e39f44
+578 f49b37836a4ae741
+579 93d489c5e8eb6f77
+580 c043faf00e67ad07
+581 ace76b7835f844cc
+582 4fc8539e3a2a8888
+583 7430fad5e87e9975
+584 930c114d0bd75656
+585 df1d8486ccae1397
+586 1177c9c77e80b13a
+587 b000df930b23db21
+588 170cebf7a642d001
+589 2735dfdb3ee5b4ad
+590 4a744a26c131931e
+591 4d9a0b92a6e8e744
+592 d4486e1e9fc6528f
+593 dbcb30a33deed926
+594 8c86a619442f83f8
+595 2350cd159f178f2a
+596 da602e0527a036c4
+597 e34c92832f58a18a
+598 dcaa06b2aa0bfd37
+599 80742d7e4bf36882
+600 ee97ba305d7f8b42
+601 5f7f6680869ced01
+602 ac2e6c638553a048
+603 a7306c85625c8065
+604 463e57f7e0c2648c
+605 d11c2f3b46e782c0
+606 8a51dcb5e896def0
+607 b80b95ab2401933d
+608 1dbf61b71ddcdc95
+609 0a17ce118c15f887
+610 5df02a9510bf12e7
+611 57926a6bbb2ae826
+612 2c5c7db3fa493e08
+613 4662640c5dd75dc1
+614 a199432df71bd27f
+615 14d7fc6f35acd487
+616 aba1a4ec58f0f5cf
+617 8f378859da757efa
+618 c430105cf942b570
+619 848920a2603eef36
+620 0d9a6b8ac13b0817
+621 357a1beee9afa866
+622 83f0968f3b72d643
+623 f356ecdefa0ba5fa
+624 4ec92c48abef2503
+625 387049967e3a10ed
+626 428468e5f8328ad0
+627 eb10808ee72969da
+628 ef9efc346884cf0b
+629 31b33cb67946cb5a
+630 ab37993af9a2a4dc
+631 59f00aaeb4e09d05
+632 b18fe2e50b31ce70
+633 dcdd9f4a358786b0
+634 1fa6a5d8a0ba8c4e
+635 d29be493a4514dc5
+636 48fca8718b24bb69
+637 495b459165ad6b0c
+638 b221c3f9014226cf
+639 a5775a309d0b6397
+640 b6d95c14bba906ee
+641 728d6fcf0970e030
+642 f855cbf2d5dcf789
+643 87826942c1c021f9
+644 1db3e72c67c0f9f1
+645 566fe4c0a1fe14a6
+646 bc2db819fc8c22c2
+647 5d07cae280b98ad7
+648 01654a70b31ad6c7
+649 f546a7423cd51479
+650 41f7fc96bf53568a
+651 e933c0d17c6ff7b7
+652 a35cbbfe9e8d01c2
+653 ffaea58e3d760542
+654 a3afa11ebf14e136
+655 9cbb2b3b78badaae
+656 7ad1bc7e64ab2f17
+657 874356dd146a15c2
+658 1090a937222d8c4e
+659 4b3c81c8a4415529
+660 3c935ebc248b8c21
+661 c5833f08632efd66
+662 633e640bb0c18c3c
+663 4da7584fd797530e
+664 eadb6c1ab7a24171
+665 515798fec6a7cdc8
+666 677b8bdbde2f37cb
+667 24f6585d773398ef
+668 5b844c9db11d0390
+669 2b6c7f10c9b33a63
+670 70b8440dec80ff87
diff --git a/goldens/health_lose.t1 b/goldens/health_lose.t1
index 152c208..4002b96 100644
--- a/goldens/health_lose.t1
+++ b/goldens/health_lose.t1
@@ -3,485 +3,485 @@ t1 1
 demo health_lose
 seed 4243
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 480
-1 13c6e731202cec69
-2 270807ecedeb1d69
-3 3ab986c2d92d4860
-4 9560948c496c696a
-5 36dd4235dfcfd85e
-6 c684a14bb3b34a97
-7 56fd39d5e339254f
-8 38ae952450467a14
-9 7fbae92dc79df24c
-10 ada25ad9180a51b8
-11 9c7ecdc6629b93af
-12 78a0dfd822a53c37
-13 ded6361fc6e24277
-14 80adaf1f60a6492e
-15 4dbc8a7e5ffad843
-16 4f69ed41eff3fc95
-17 5e9108718401007d
-18 8514c3e5ed514dbb
-19 2097ca24d2c73f9d
-20 eeb41de977af7c56
-21 6d2b0f619feba041
-22 a7f09c391693855b
-23 840f3c5bf9dbfcd9
-24 5a4fd8a620bdd4f1
-25 bb8718b7b81e5935
-26 87dfae171393a79d
-27 ca56e7e85729a1b1
-28 c4a23874674ed797
-29 83de1fe84965a251
-30 1a11252cdf76e3ea
-31 aa621553e5486790
-32 b518324593ea5bdb
-33 3a2a32f2fc40a786
-34 5bab9433a154110e
-35 6582a5e86064acce
-36 29bee2f0a8e55869
-37 1be32ffdd865aff0
-38 0656584ec7eaa7c4
-39 33f57babb9599bc3
-40 5fd3270fe7c21620
-41 c4c7243a170937ef
-42 f40900da73f25dcc
-43 749513eeb9d56821
-44 80ac87be4b304134
-45 923958838c45d040
-46 4ba33acb70c04167
-47 bfd580dbb534f630
-48 3e541c7fd386c4df
-49 7e352ff2b21dbdf3
-50 75976421fa722e36
-51 7ed766602aba21ad
-52 bfbf69b40bbdaa81
-53 0ea3a044905c31d9
-54 658dead0e920bd99
-55 a110e732e4839866
-56 6191e397c0f001ca
-57 dffc603eff36f429
-58 0a087bc391fc4fec
-59 8abd9df1a359f6a4
-60 e397d072b7642329
-61 fcf261a6ddd3aeb8
-62 9792697c85adf4be
-63 060de8c26333f0f1
-64 9f1008cfb6184329
-65 1bbdc8dcea8d454c
-66 607a6797a5b4145b
-67 716390a91f50c974
-68 8051244e9a5c457f
-69 7c1b58fe385dc230
-70 3eca4b06c2bb48f7
-71 69c24ca3ba7a7b39
-72 8b3f990cf74f53af
-73 c9de076ad1bf8189
-74 1aaf8397fc1c0ce6
-75 dfdbd658dced5849
-76 26ee383e7e9348dc
-77 1531659aef2cd4be
-78 1891fd49d65d4149
-79 d71b17e42b55056a
-80 73e74b3d986ff0c9
-81 316757ac44bae541
-82 ff4ffd99d56b94a3
-83 6af47917d65bd6f3
-84 0636c4e9246ef79f
-85 bf9a4f19e6cd84cc
-86 ed96626b359badd5
-87 5628c9bd6ac33c14
-88 80738f2ccb9c980f
-89 ffbbef41d31cfe76
-90 dbd7f2d22f4cf0ba
-91 1337b4fed17868a2
-92 9218640c2c1cd6e5
-93 1c076bb69ee19c41
-94 3ac5cf32da86f978
-95 c255513dbea6d70c
-96 f20ae5720e86f7cf
-97 dd8d208dbed4092f
-98 1589d076037ce46a
-99 64604de626e6c121
-100 69d9f0f8e2afedb0
-101 84b8a9145fe8ce16
-102 9b0ea12038ff8ba0
-103 a54ea47548024eb6
-104 ae2f1632d3986adf
-105 88cede5d0e9041ef
-106 2a5c2c139f862e0e
-107 9c5669450971e0bd
-108 51bd1686b626f212
-109 5c779b8570e3247b
-110 e5043118284fba56
-111 65f511d1c84fe598
-112 e6d4472bac434413
-113 b3ceca3606112a11
-114 12dad0c4209aeee0
-115 580c2304dcd6361c
-116 537443b276555164
-117 87726244a5e72648
-118 41915780dc98e921
-119 9380b47c3fc27695
-120 32f087508e6a35ea
-121 1307e23c46f4e973
-122 31bbd1b1699128b1
-123 697c805c635aab25
-124 d76afa8f6d2588dc
-125 4b4d553a8bad0492
-126 88c07b19a7a4d05a
-127 5d81ee5c20b0e523
-128 d10910269f249a73
-129 9361955e94b49a9d
-130 cda92eb3b956d279
-131 0287608b12af2e24
-132 1d4a1d02615aecf7
-133 f3db23fcb6d3227e
-134 b73ccf455d1e7770
-135 b182c21ccf67855b
-136 603150f0119ab2a4
-137 cab7cf6b7b7c0306
-138 a846af992660602b
-139 0f4fc8ae95fad47f
-140 1316c22f6953cfbf
-141 659870099c7562ba
-142 9e7df20401a8253f
-143 83eecb7c3c592cc2
-144 433eeab6aac7cc02
-145 5af3372e2b29791e
-146 89b5791418fc7709
-147 bd190a2567e5b23e
-148 5b83b75ef6c1e46e
-149 da28db94c3b2c402
-150 6add189fdf3da66e
-151 5276f7dbdb9e0310
-152 66eef9e34d29c646
-153 5693623ecb56d673
-154 29dbea326341fadd
-155 e997ed933392f632
-156 0a7c33ca80e9cb35
-157 eb7b11329f8cbc09
-158 873a2dd106da3ce1
-159 3fbea5762e12c6de
-160 0c56ab81f5aacc3f
-161 57362f66496b3724
-162 2eb1946c0e1b3d82
-163 15cfaea7a834010f
-164 09f92d53969fb5ba
-165 427ce92c9bb189db
-166 c83ccf78eaf7c0ed
-167 a82e59c4848a8d28
-168 91e817e5db2db64c
-169 c24ffd1b5b959653
-170 49f718401846f314
-171 2e5a3cba74ba1a09
-172 56a46cea1e7ec8a1
-173 c47f731b782a8042
-174 440d38185207b2b3
-175 fefde93d5e194918
-176 751bb14088729551
-177 80605848f987e841
-178 6ff5cbd9fb7175f9
-179 3a7f97aa0dae65b4
-180 a93974b80e2f8ccf
-181 e85017957dc016fd
-182 86a2008efa795900
-183 8d0ba9edda40bbf4
-184 6e6870ac596b8759
-185 308d748d0ac925da
-186 bc4569018c9a22df
-187 2ec29b3e58114385
-188 1d9957362a4fbb26
-189 111d8dcdacf34a97
-190 dead0daa5d3a109c
-191 4eded8b84a2bc285
-192 c89fc1cfaa729c4f
-193 7c9c54cb8e385615
-194 57d6270a4f1baab0
-195 e8aaab46fe231b5a
-196 a6f7047f73949e7e
-197 6cd56fb055ac2ed9
-198 464953f65ebaa05a
-199 bdacf14f8a97d575
-200 a8e181d012abffa9
-201 cf1de4312316fdba
-202 dbd379cbfc4d6653
-203 d544422eb4622b75
-204 165bb653f854cf60
-205 d40e430152ac02b2
-206 a763dc96c060d620
-207 6a0ec32a2fcee7d9
-208 d58a016200063d0b
-209 f6dbdd3678519936
-210 5de6faf7b61ea5a0
-211 4b1fc808820a90d6
-212 b3a86eb9e170aeb6
-213 766a4b4c2ca37497
-214 d1bff3d28280020f
-215 4f81af738d62556f
-216 cacfa958375952c3
-217 29d88cd7334af3d1
-218 79cb194508327d65
-219 3005a5e311bd6b5e
-220 8927defd447d59ec
-221 f279edf1c0e838bd
-222 7cba9c9c4aa146eb
-223 7f2f40549e1abd74
-224 c653d95f7eecf062
-225 d8fc114d78f41d56
-226 14eaf136999c524b
-227 6f66a67d9ba4b80a
-228 5d90bea1fc04914a
-229 4254612f7dc86494
-230 50233510507cb5b8
-231 c11a46de5bad1049
-232 255ed9b8fe2456f9
-233 0afb5c5989f25072
-234 ea084d2378f7451e
-235 4172dbf7566d0b20
-236 b9cd3d8e99cc0357
-237 ceb81a89fa84eab8
-238 d9fb4119f403d876
-239 7f5ee11d975eeee4
-240 7db15f16f9d6a54a
-241 a118719d033899dd
-242 529a786c0878b38a
-243 974486b657ae0b07
-244 a2de6b63b36eb14c
-245 8b8663ff9823e86f
-246 540830c4102bdd8e
-247 6146c1ce8f17f70a
-248 0bfec4af10bf969e
-249 c65e97108d768b92
-250 7f77ab8907b9e5dd
-251 f96d88e2ad7e579e
-252 be6271b2b8d5f376
-253 38a5b08c3fb10c6d
-254 c445cb909250393b
-255 e71a33a082fed6dc
-256 e55ce8e10f099d3d
-257 78e68940d7fd3962
-258 5edb44a3b3e9a10c
-259 dd0cfcb9a36bc6d5
-260 41f13cd24cef8056
-261 0fe7b7e982094dbf
-262 9962dcdb60578c4c
-263 1c38b99c622686a8
-264 1794fd33c73dbb29
-265 6a097c213e72b3b2
-266 bf961d2917426b9c
-267 b8ee8d64259315be
-268 9a269a9c9f2002ef
-269 5483f982d10178b2
-270 00d247172614a104
-271 4a666f4a35398905
-272 3d491c2a028962e5
-273 42b29cce2f0aca17
-274 8f17851398f93a5c
-275 70ff94f6fd334daf
-276 87d60cb7f9375f3e
-277 bb395c5d19be9821
-278 3cbfbbbcc5f4d5dc
-279 6b42d10f4e9a87d6
-280 721c68e4e5faa8c8
-281 715f61eab1361f6e
-282 60a167e0744adc8b
-283 a6cb57331dadfcb7
-284 e6b85bc5437c3590
-285 fcf8abe3a7f3f997
-286 af5d207e00858a6b
-287 7fef042952a4e41f
-288 2f82cdebd63480ca
-289 c1a511998dbe94b2
-290 29a69c0339ff82c2
-291 594b6dedde39ec67
-292 9c321ef135872642
-293 d1b29d24eb56c068
-294 08b74fb0db06dbf5
-295 3a5d9afccbcfe0c1
-296 afc5e6e9d4c43032
-297 2c0fb11741ce3762
-298 1757df504e68f703
-299 11175bd1247a7d95
-300 cc60a4e7e65d85bc
-301 87462b395b381726
-302 66233bf3f73c57a8
-303 87c20f8f3b6d2917
-304 a3118e54574a9ae2
-305 0314ec98330860f7
-306 c4e5a6a0dbc2c0d3
-307 ed72125e9c8722b9
-308 cf86c1a35fce76a2
-309 a927ba7636001982
-310 c427da68e4c0c673
-311 601d33f224a58c90
-312 a5af4d860e2f53f1
-313 36320bc3a63747a5
-314 6ee0715527e1fb3a
-315 c5deaa0cc83e690b
-316 a240900a36b58058
-317 e50a74b440e621c6
-318 de90d88a403c309c
-319 aef4312c2bdd9d43
-320 670d4e161d530fdf
-321 a85936b81f012e5d
-322 db142c6db36cb8ee
-323 b2ab873a7a662ac0
-324 998aef8f16d69011
-325 ced3da854d866200
-326 ebb9fb185cca7a7e
-327 f47b089778f87fb6
-328 7411e9dcf9d0900b
-329 5d410ead54bbe6c1
-330 701da7bc3279e377
-331 02b2569f1f59445e
-332 f7c9c23d45683eb9
-333 891b609b2cce436e
-334 a2670f3bc019a483
-335 aeec4275c7ba191c
-336 4f2093c955e23fd7
-337 b5e51a107534c7c7
-338 30718616485cb98d
-339 7fd343b7abc91ab8
-340 f7f4317c40ba05e6
-341 c6dce09bf85661f9
-342 ad1cc4431256efab
-343 22f7d7bc54e30930
-344 f5bcef8e8b8babc7
-345 c332fea8aadfe399
-346 eeb8be2bee7e2712
-347 e556d4f982ceb133
-348 75761e08a9c12312
-349 8c7ae31a64420e35
-350 9c99f4270a0d164c
-351 abecce5717afe7ed
-352 84091c643e2f1376
-353 b36bcc076d55b9b9
-354 6a1df42be0d2df68
-355 a809a56c0a404e57
-356 35858f930136e087
-357 58ee61ab60207fb3
-358 512a73dd6edb2a47
-359 b7402f393d2305f9
-360 a1adc6ee7989966a
-361 af9b227456489374
-362 31007d9c8ed50a0e
-363 418e3ed9ff71594b
-364 3aea0a19ffb99b66
-365 c7fad77dee4f73ed
-366 4df9e111dd65c776
-367 d0a8ae750cc0413c
-368 4469cc1dafd56efc
-369 e4128165ea5eee50
-370 72168a9ff4c9eb46
-371 d164b7c957af123c
-372 1c72ece392d02ef0
-373 f377139f69bc1e3a
-374 45fbdfa5d3784104
-375 9dad829f65ebc733
-376 82ef551385e8a0b0
-377 b58e89bec5c89e51
-378 60ea0f083ff7ef85
-379 adaa5c045fb64021
-380 a2fb8bb9f346401d
-381 9a6c322d332b446f
-382 aabe0e6a2d999245
-383 fcd3da26f8bfcdbd
-384 ec914fdae9bb7e98
-385 5524488a50422321
-386 63e97e6b5eb1fa0f
-387 a549fcbb5c0ea55a
-388 9ca017809cdde9e4
-389 cc46bc5704fc3765
-390 5a0980d60ffb3021
-391 0d0b1f1181de16ab
-392 12c8b3bbb25c4167
-393 9f3e16e73e956373
-394 bfbd864da9adffc2
-395 f242e2b0b8844fef
-396 994510d6eac14dbe
-397 2b58f9bad8484e45
-398 1640071753e7301c
-399 50be80ad067e5ee9
-400 52ae30413812f066
-401 66f02e0e95967be5
-402 174cb2ebe2d11981
-403 fd664104d53d30a9
-404 0be590dd8a4fb356
-405 00871850195535f4
-406 155975ec8607579e
-407 29c4c3b58bbe7d02
-408 6a320c1fa0809e42
-409 38196c73f7d11169
-410 79f7d5e6c6670d6c
-411 a6d4e9bb3049aa22
-412 014f3c68b0ca72bf
-413 4dd019aeb3970854
-414 2b9c7422b169b9f7
-415 a0d7a47da8043bd2
-416 5a3a6e30098daa4d
-417 ba74ac0ed366d51b
-418 fa30e43bf0a519d8
-419 0bce3aace9b9c228
-420 b5783294566ba5f3
-421 c40b0db97e620eec
-422 55978b145f2d473f
-423 db540d01c4569d2c
-424 e80b674589b27e94
-425 54bc4e68a0ba4de5
-426 64bb6ab968183221
-427 5c2dec1e1a2cfb87
-428 29ae56b8f98e1b71
-429 c00e3d5ab61206c0
-430 0db447bc2deb8e10
-431 880db9fd4da936c4
-432 c839ce5f917fd65a
-433 21295537e0f85876
-434 ac4d9bfc42f93120
-435 8f879928f3616642
-436 3162915dfc88f2ff
-437 5b0cbc577a7dcec4
-438 e8813c8cf07e22cb
-439 0ed53db1e14dd812
-440 c4915aec0b494d89
-441 4f9c2589fa53c871
-442 6fc0fbfa1ecfb34f
-443 cb42b9016f9493c8
-444 464cf5cfe3926e15
-445 a725c916e8f6912c
-446 9ff0b8171e14d343
-447 8dc3ecf01ab1f341
-448 63c37b194d13aae5
-449 d7e804070738e4ac
-450 daadf2ef41db0d8d
-451 81eaad57ee62bfa6
-452 95e4bd20a3aba2ff
-453 06d75eca5410a4fb
-454 9e39fdb3f083ac40
-455 7c12874e01116f71
-456 d32c1e228d4cd198
-457 ea6ab5fe3e7a84c2
-458 ea6ab5fe3e7a84c2
-459 ea6ab5fe3e7a84c2
-460 ea6ab5fe3e7a84c2
-461 ea6ab5fe3e7a84c2
-462 ea6ab5fe3e7a84c2
-463 ea6ab5fe3e7a84c2
-464 ea6ab5fe3e7a84c2
-465 ea6ab5fe3e7a84c2
-466 ea6ab5fe3e7a84c2
-467 ea6ab5fe3e7a84c2
-468 ea6ab5fe3e7a84c2
-469 ea6ab5fe3e7a84c2
-470 ea6ab5fe3e7a84c2
-471 ea6ab5fe3e7a84c2
-472 ea6ab5fe3e7a84c2
-473 ea6ab5fe3e7a84c2
-474 ea6ab5fe3e7a84c2
-475 ea6ab5fe3e7a84c2
-476 ea6ab5fe3e7a84c2
-477 ea6ab5fe3e7a84c2
-478 ea6ab5fe3e7a84c2
-479 ea6ab5fe3e7a84c2
-480 ea6ab5fe3e7a84c2
+1 83204ac19a69dabd
+2 03caa5fcb2adb709
+3 708a0acbeeb8d320
+4 aacfeb1a22c581da
+5 fc9def428642f5da
+6 a89e65505e143707
+7 e7839f8c8b974d53
+8 ff02371f1389c0a8
+9 a36382d1325ab81c
+10 1626b1d518f5d118
+11 71733bd0697c674b
+12 b0024fd57d6e0e2b
+13 69969404cb1e8aa3
+14 215f9f03a587813e
+15 795c35843085b373
+16 58684ff0a8ab6f11
+17 13fb61df2e82832d
+18 cd92d4c0475ddaeb
+19 40dc0e1391d84579
+20 2a6b79caf81a3dc6
+21 b3ea9fc7a6872451
+22 77d7ae6d30502b17
+23 017f7c77d902ef89
+24 ae8f8307002d5e31
+25 f51d0e1559e15eb5
+26 99e3ebd418cdc03d
+27 0c2cced430557ebd
+28 188d4e7a251f9a2b
+29 195f6407d4910571
+30 bf17a0a640a216fe
+31 ca9c6977a1729bdc
+32 2f30c6bcf781b70b
+33 2f0180a87f9a6f06
+34 67e4344ef4d74b9e
+35 5f10c7622043cdca
+36 ba088335168fb599
+37 198634841e51d54c
+38 e64f0674b583dcb8
+39 dcdd9cb1005b8a47
+40 ea1c39345d3f92e0
+41 ed426b444158fb2f
+42 2594d84dd64f8788
+43 fa57c50784497a75
+44 dcf2e06eec2f22a4
+45 9a1583d39ea13d94
+46 eff26bd508f859f7
+47 d133b3eca20526f0
+48 fa99f65367f2647b
+49 7e940e3218ce0b37
+50 26deb09a882a2ad6
+51 65a63f4ffdc9582d
+52 e921c385f17d47f1
+53 a5036c326bd54fc5
+54 17eaf7200992593d
+55 01d4233019442836
+56 6a05ab68414e77aa
+57 ba8d5167e688bbb9
+58 f401b6ae2a4e56f8
+59 40614a9fbc3ac294
+60 1726d6e43751cc7d
+61 7491e2c75dedb878
+62 32ac34b26cb00a9e
+63 bd5d70b523134651
+64 b33e0b30577f79e9
+65 902dff364c7c43bc
+66 01c9c89c47357517
+67 0ad799a4c0380b04
+68 4c685ea550f34443
+69 cf0471bd519b4b44
+70 905ffd09c45bf8c7
+71 36eb3f28991eb475
+72 c8739796347742bb
+73 ac1542f24649b889
+74 3557c33527bcedda
+75 cd7bd7123b9802e5
+76 3fb104ebf42dd46c
+77 90973811c6885aba
+78 e2174380af156c29
+79 57f1e44c8e5cee76
+80 ec0b58032cdec5c9
+81 14d632afe67b592d
+82 21eef21288ba454f
+83 235dffae6a528b83
+84 d193e47ea1f204af
+85 679f5aa69ea4e438
+86 aacf29f304def925
+87 91d198bf0d6d0cf4
+88 c3ca09cbbbb2e63b
+89 c0d249991a99b672
+90 8c5b1b01c2ab9266
+91 bf0415e19e5317b6
+92 89fbdfd281758f95
+93 430cfcfc113e7535
+94 1d82e9b11be5cf88
+95 9b8ddcc5097dd0b8
+96 d7ffe65203e292cf
+97 a7ddd246f5d4eb7f
+98 e3b547e875524f3e
+99 5d8a4168f85dd70d
+100 5e4a0a42e4a7de70
+101 41c17c2509d71b62
+102 2ecfae6ee4fe1674
+103 7dc71bb7038241b6
+104 ab990b7f7eaf1133
+105 96e74d5fb3b97e0f
+106 71f17803949439ca
+107 404c48bb0bf8ea09
+108 08c30695f224be82
+109 de7f40df215a7e67
+110 5668f26ea7fa8fe6
+111 70a9ba2f4c74b26c
+112 96bed4c8891ab343
+113 ca0c723f8e084ded
+114 9c545a594c3d94d0
+115 20acf7437d03e8dc
+116 d73403f2a13d4124
+117 f8048a2bc1f45d7c
+118 11fdcb18c0702671
+119 955cba51cfd3ede1
+120 4ff9a5952f09310a
+121 edb3f62c48f774a7
+122 5c7a3a97b000f985
+123 40b84154d9bc6145
+124 7e64de0c64a40d30
+125 1fdfc96d01851492
+126 2c3359f9c5c622ca
+127 2932c199cb0d393f
+128 b9de1c1935df0cc7
+129 9355f0bef41f1d5d
+130 a15ef39f322fad79
+131 76ef60602e81ce64
+132 a85df89317f94eeb
+133 fb457fb8137e6982
+134 82151fa44485404c
+135 f883c677bd929ab7
+136 56d12815ad0c95e4
+137 dc04feddb565a6aa
+138 5ff79c239b87dabb
+139 edce2b92361ad01f
+140 92bf1538ba40714f
+141 98afa1604563656a
+142 89a902c4e7545fab
+143 f1842fa758e52706
+144 020abeb1716641f6
+145 af95b0ac2eecc9ca
+146 dbbdf1417edc55e9
+147 978584bc6cc7ed7e
+148 430a1d4c4c5261ee
+149 53c1e04a714b7b06
+150 19c397d44f7f403a
+151 9d9400d296cbc284
+152 3e683868e68a3be6
+153 4ebad375c505e103
+154 c9502d7f297236fd
+155 7262e7e444321b02
+156 0f04791eb782bcc1
+157 bcacd1939b46f71d
+158 264533c999325d7d
+159 8205f2b14888381a
+160 d8de83b3e558038f
+161 d060e4a76857a404
+162 0638b18acea8cd82
+163 af376f8da84a325f
+164 e5bcd8e74b9870f6
+165 c3bd642b9b8ec5b7
+166 f0ff5e72a2ef3969
+167 734cdb4d5eec45dc
+168 19ebe10bf5d0ff80
+169 7887b4066fee6793
+170 9dccce5ee52853a0
+171 817df16f1588127d
+172 b9764f8040b178bd
+173 ff29a36b15962fa6
+174 36853bef42198fd3
+175 084af05c7d7755ac
+176 61eeb0877dcdb2f1
+177 d475d124caf9a0e5
+178 fad2ff8b7433cfed
+179 0def0d279c9cfd58
+180 d9573e20672cc75f
+181 6316c11d3f8d71ed
+182 b1dcd08758aebcdc
+183 2290004a6f1df5c4
+184 4c018c371fff048d
+185 7f66e8b313b8137e
+186 d5b5d390a37e4e3f
+187 d770d6c86017a4a5
+188 b16ce9fa63e07352
+189 64d173f8770600a3
+190 46c4bcb406ed056c
+191 bd5afb8a2baf9fa5
+192 316408a518ea186f
+193 385cc7fc05c33ff1
+194 f3d8b9ac7138a870
+195 cfa1569c256cedfe
+196 60ce497dd8c192ba
+197 a2ab4f5345577a6d
+198 b0ad835ae76764ca
+199 fa81024ff2dc6f89
+200 270612e5d8b3aa35
+201 7fc35bf07f50c6ce
+202 c4d14ded10927de7
+203 bad9a5c8e8fcfdb5
+204 e876b7d238cd0bbc
+205 c710ce98881dd6c6
+206 761ea349dac9fa7c
+207 133bda262ec8ef25
+208 d27595514138d4df
+209 4e49fa0805c0c59a
+210 479aef66a06971c4
+211 0952c6f4a72c22a2
+212 1245563a569949d2
+213 113ce9a207bbec13
+214 d84bebebd0deb6ab
+215 88ee11256cf948df
+216 3b6145652aa1e0e3
+217 ed9d17ab52080771
+218 611b751f294ed795
+219 0bbf6c95910adf7e
+220 e16ad4b34536e928
+221 81ca7d07f5163571
+222 575871d883b82a27
+223 b05df41cac78f674
+224 17385de5563d0362
+225 1af74893135c864a
+226 d3251a0b4463520b
+227 01f82b4a9c7c877a
+228 d8adb404a0cf724a
+229 b122a697cbbd3a74
+230 657a5953c6dce798
+231 e0bb0c48fe6450b9
+232 183fa560b8ce9239
+233 5fa49aa641fd0952
+234 945fdb7c93c1a2ee
+235 1f65a9e77db31280
+236 1544214cb55788a3
+237 c7f5aa0e61536384
+238 78480d7b23fdf202
+239 bc10c9e524e8f974
+240 37d4640bd818dffa
+241 93f212a9d61959f9
+242 5b0ed40892bb57aa
+243 92fe0e85df873d97
+244 0dc7c225a8f4c0e8
+245 72bffc4f3127ad33
+246 e87df0d1bd378a8e
+247 f11e5a76519095ea
+248 fea7f1415ae93fce
+249 188fea110e658696
+250 76b5de128c10b8c9
+251 ec01e7d9b235eeca
+252 1f2b46c240790d4a
+253 ca2a887e40d4cfcd
+254 3c69d85626bf0e3b
+255 463db961db2af01c
+256 121f5753be444a49
+257 77d4e7555e6f24d2
+258 2ec97ad07bc5a398
+259 e1089e140458e255
+260 78eba4b0a0e2a696
+261 00d985a267ac6303
+262 4ce7b5e6ed2dcbcc
+263 c593681b5726e3e8
+264 ac67641fc3c9c969
+265 1b0480f854cfb646
+266 930ff36d709f8d4c
+267 c273c6302646b47e
+268 707f55d413701453
+269 fb9b96a4df41eba2
+270 387083b914f290c8
+271 129b805de82343b5
+272 8389e7a75442dae9
+273 c928dfd7c5bf3b63
+274 e9ab0fb88bfd1dbc
+275 1856efacf5f55dfb
+276 3a3f11233f6d9bf2
+277 52838ef723a5ed81
+278 11c46a9dbacdd0ac
+279 f5182155ee981726
+280 13297fe3e4f69994
+281 c0d7710b5c9d583a
+282 d6e6b91ebb9cf9a7
+283 79ee6da883d0ca6b
+284 0213c4a10e057424
+285 e1b1dbc5910f2077
+286 225802029152451b
+287 881a94a711b0d05f
+288 6d56cd5cffb86a9a
+289 2bc1ff9ba7a1b942
+290 0589548269463d86
+291 3ae0b55012a61f37
+292 1f7610615f1436e6
+293 5d60d43a3371fc04
+294 fc2b3a2e051f6009
+295 c304f3a91148cb1d
+296 248185b7ef4e4e66
+297 4a59fe60c847f2fe
+298 cb0dec3b0b3c71e3
+299 50f03c871f7a8ae5
+300 71f17ec87c4879ec
+301 3c90b9f46a0974b6
+302 22b600c2e9bf720c
+303 c3a1c3eae7683c37
+304 b1a841a15f17c94e
+305 9851c5c78058c397
+306 2b29ec7d4ddb472f
+307 65d52008320d1e9d
+308 22e3ddd40cf76f26
+309 0375f6dadb2a1536
+310 eb83c71dc790a847
+311 a59872fbb243f990
+312 20bf29355188b241
+313 5727d1b9fcad1545
+314 3d4b7740be7a889a
+315 9ce336a2b22dd157
+316 1767fca10061d138
+317 d0b300036c562076
+318 965c7117124de2c0
+319 47b7086cf6a71c83
+320 a93b7e2b2c5add13
+321 95cf05987eb08399
+322 c3664e673f1cf2fe
+323 de8f00ab11582bc0
+324 32be48b2e91fb031
+325 dd8aec93bd7a3e3c
+326 2c9aff87fa133c6e
+327 8e038263e1538cb6
+328 6d768202e98bc6b7
+329 8dafcc540f2ce78d
+330 bf304a9f4ac33367
+331 2fe8ac1d19c59ef2
+332 0c113870ba00aefd
+333 fd0354a27b7ea33e
+334 fc90e9caba725537
+335 5216c78af0c2092c
+336 3420da1079bf6597
+337 8e84405a926b8e07
+338 3e5c843346127f61
+339 21e53bb5809c8588
+340 5023193c957c88aa
+341 b2ffdeeffb1e58d9
+342 82de26ec2a4a42ef
+343 2be6611c4c5a3da0
+344 0918df6d28962bd7
+345 b0bdd10f31b0eeb9
+346 0a1fe5cf583b894e
+347 995d43fa75ddbb83
+348 e5cf316891792162
+349 d89a6df5525aa5f1
+350 beae5111ea55bee0
+351 a29e7be6880ec34d
+352 adfba7db57907252
+353 89f2205ffa7593d9
+354 4fe74d6b50b5a228
+355 dc58b47d11917c2b
+356 e79c3ab2ffa76297
+357 a1f58100ddd6f0f3
+358 9f31e5b276651e27
+359 495e3566a7d000b9
+360 2bcc13d465c246aa
+361 6578852348135ba4
+362 a84b595aa3384492
+363 ccd2c8c3395b40bb
+364 0408951d4179df4a
+365 986b326189dc4add
+366 371a5d7c8c083c16
+367 03ff37c20116fc7c
+368 7639cad640864540
+369 46b727be7fecea7c
+370 6267048db2319a46
+371 8deecde56b8c8d3c
+372 3b3969873495629c
+373 66fe26a15e3dae1e
+374 9d790cb3af9213e4
+375 aaca6958c5260e2f
+376 be3dadafd1cfcc10
+377 1f47a3eb10fd89a5
+378 1e5045bd2b2226f5
+379 ded90fcc6e147921
+380 551e3f8a3f023949
+381 bcb2719d0a44085b
+382 1367fbec742f21a1
+383 5f198efd97bebd31
+384 1c34481dae71fccc
+385 8a9be91cba4cc9c1
+386 bcfc572da773082b
+387 59f1fa6ea6d58e1a
+388 b7fa98f505d92220
+389 5cfe19f345beff25
+390 54cf6ec40d83e501
+391 0b0fb0a55a3efa9b
+392 35c6bdbf83b0ce93
+393 8a21e67e28f29f47
+394 43dc566e38a40f92
+395 0390926182de7673
+396 34c5f6b4afb9344a
+397 3c20eb07eda1f329
+398 a09cd32a74c98028
+399 9a76154158bf13e9
+400 e15965f68b9e8bba
+401 eaf64b90033db135
+402 39a66a2394e3f825
+403 a570cf29209b07f5
+404 13a39fbcfc177ff2
+405 45089156797422b0
+406 03af33ed71afb34a
+407 7e26b79a40854e0e
+408 42d59b88444590fe
+409 05e396759f0f3069
+410 5e41585948d2e37c
+411 822507c3a71474b2
+412 01d2afebb28271a3
+413 836425a56bf74f44
+414 38e21480cae8f247
+415 7d845206c572ed1e
+416 559276f590b89d41
+417 ebc179549d11e4d7
+418 91a0e1a4f7e857f8
+419 2efa68cee9aded38
+420 7786f5c183bd01f3
+421 7ef0f66a985bbbb8
+422 3aac390341a1ba03
+423 b9c6f7d22fe67dac
+424 58e0f25e78ff9924
+425 d5b2c3374fa76c21
+426 489340cf76f490b1
+427 671e2120dfcb337b
+428 82eb5bfd3bc20fe1
+429 0f1b5af9b835e8f4
+430 bdf359dc48aa7df4
+431 2af60ecf57669080
+432 e7de253e0952b1da
+433 0cfd40d6893017b6
+434 93b77791ce8893d4
+435 654c1c8368ee568e
+436 264229de873751ef
+437 b281ef3f2608ad50
+438 3089a3a6691ad21f
+439 e5b6e8f6c711d242
+440 3a683753c06d7039
+441 9b498a49ecf0df01
+442 874833d0acb3f35f
+443 beb1e5d25ae188d4
+444 0577846749bd5229
+445 794372d30925f4ec
+446 571eff9a0b280403
+447 84b715cb4666eb91
+448 7ca030b09610ab35
+449 4c567410a9ab0ff8
+450 0e1da9f35a0e37a9
+451 680a28d073724bb6
+452 618bd7f7b091619f
+453 33e9413b9e51078b
+454 ea00ce028bcc97b4
+455 5c7e94086589a6c1
+456 1ca2917bd3411258
+457 59604a2ec9d42e82
+458 59604a2ec9d42e82
+459 59604a2ec9d42e82
+460 59604a2ec9d42e82
+461 59604a2ec9d42e82
+462 59604a2ec9d42e82
+463 59604a2ec9d42e82
+464 59604a2ec9d42e82
+465 59604a2ec9d42e82
+466 59604a2ec9d42e82
+467 59604a2ec9d42e82
+468 59604a2ec9d42e82
+469 59604a2ec9d42e82
+470 59604a2ec9d42e82
+471 59604a2ec9d42e82
+472 59604a2ec9d42e82
+473 59604a2ec9d42e82
+474 59604a2ec9d42e82
+475 59604a2ec9d42e82
+476 59604a2ec9d42e82
+477 59604a2ec9d42e82
+478 59604a2ec9d42e82
+479 59604a2ec9d42e82
+480 59604a2ec9d42e82
diff --git a/goldens/qos_auto.t1 b/goldens/qos_auto.t1
index 419ff45..5644e6b 100644
--- a/goldens/qos_auto.t1
+++ b/goldens/qos_auto.t1
@@ -3,305 +3,305 @@ t1 1
 demo qos_auto
 seed 3003
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 300
-1 f9d6c701e41f09e8
-2 a4287219b8d59883
-3 78750acf3907f293
-4 448e6328f05679fd
-5 eb01a3eaabbeb4d2
-6 07d6dd63ed847be4
-7 84a1ee2bd14a4891
-8 9fed011530496ed5
-9 a8d1f000f99fa55f
-10 dd26839a218b2c8e
-11 891d377385a3df3a
-12 01dd838118d82a66
-13 21e4f6fd1dee5450
-14 73421ed11494c824
-15 53d5a69b569442d4
-16 4b94904241cf965d
-17 33070293b6b53989
-18 b4cab95283736e46
-19 cd6f6400036c4b67
-20 73c2ed31979d1aba
-21 07be4e0ad2d6612c
-22 2434c31ba1a293a4
-23 8dee09def16021d2
-24 020f2f290a9ad0ef
-25 cb4a5cc5301ca131
-26 93a65d97134f21d3
-27 b18568488013008d
-28 b36979009cbc796e
-29 ae6b400ca8f6faf6
-30 00a52835cb8ffe74
-31 e2f24a06c4af282f
-32 221311820d850ca3
-33 565c7b6ad84ee23c
-34 b19348494ffd89de
-35 b0ddd33430a73f2a
-36 719fc9e2bb64b28c
-37 ac59ca64d70f7649
-38 744f5e5b51a6bb13
-39 0542a45721c1f5e8
-40 5a353b624adfcdd8
-41 f6321e3cc882933f
-42 5e8bf112e98e7398
-43 b5fb23f05c7021dc
-44 f0be4eb310bfbd85
-45 6feab2a4167620b3
-46 0166b1023191a1b3
-47 00cadda3c4c21fa1
-48 4a8638ee5c38f76d
-49 79677f3a314be3c5
-50 8d0e6bbebb909e07
-51 96bc55cd525a5f71
-52 4f228a867b82eb04
-53 ec37a3dac5e38a0f
-54 72262aa2b3d63e5c
-55 ad335df62dbd4400
-56 2ff5aaa0bd99d91d
-57 009b3a51f06cf733
-58 f087bc0bd320a35e
-59 fb0c8ee68c0dde0e
-60 5b80839e7d618b60
-61 91668f65c2777ac4
-62 c137b3ce6a18e28c
-63 7055a5b22349804f
-64 801fca805898e0a0
-65 0caf255875da2ef1
-66 abf0aa37ed424445
-67 adab5733a143b0a4
-68 3943d777c0d39d40
-69 60009673f593e5d9
-70 38c290777cc5d19f
-71 5afcadd9f9a93d93
-72 eca371f3cd661d85
-73 d98bfc16c5537d57
-74 f0999ebffa1a5995
-75 492915d426620b0c
-76 2e6af2babc21d17f
-77 adb69a1ca5989e63
-78 b82cd4648d9333dd
-79 d1cfe18dba30d4cb
-80 9add0500db7cd4c1
-81 6807bc72623e6d87
-82 4bd457d65e114fd9
-83 0349c4330c1f24b4
-84 1d02d84d4460a0cb
-85 5c525716152b670a
-86 abf62cac812cab9e
-87 7a51dc18959af1c9
-88 69336c68ac66010c
-89 b06249a2690f8f27
-90 b5915407400e2c86
-91 f53645d3eea0089f
-92 7c1fd77f29309add
-93 713160e5c5a149f1
-94 df3cc4cbcce9a696
-95 e779d73e995d9712
-96 8eb6a6bcf522a911
-97 461aa2dbe50b0d6f
-98 92ac3d3a050c1b39
-99 e69e4061cac67f53
-100 9a0a928e1232a810
-101 2e3ffc7697c7035f
-102 efbe1e55614bee0f
-103 5ecadf9c3f8385cd
-104 f14a95682e56699b
-105 847fb87ebcb19494
-106 ffa95d5ac1022e4f
-107 27b99da471793850
-108 4286ea831c59a25d
-109 19fa636285fa28ff
-110 cc071befc88fbb9b
-111 c33041f8286605f3
-112 4873d437fde1730a
-113 9fb94dd433bd2302
-114 b7d6bda4a19e8ce1
-115 b01a51b98cc977c3
-116 af0cc32c90f0471c
-117 02f7ecd1f6b4a836
-118 03be7246e4a84444
-119 1a6b91e24a74637a
-120 5664a150c6e2c23c
-121 43ecb7e2d3ff02d6
-122 f386da9909f3e4a8
-123 c16ed1687ccff577
-124 7bbb12f38f633b1c
-125 262ab7bea92c7fae
-126 1ce1fc858a15247d
-127 9a32439dc3810da4
-128 20d5d7fc13523662
-129 34beaf58d0b3db96
-130 0d9c6c15c3e4af1f
-131 6d43f3e398af0a82
-132 6a800de03a82ef6f
-133 944d05f8ac2a81f6
-134 8474404538cdbbc2
-135 a732e5ae3289bebd
-136 8f4098f0f0bba50a
-137 eb1aa0a9d10bbd2c
-138 765092f2c6f8bc7c
-139 df336085aadc6360
-140 9785b247db86f93f
-141 005562fdd5b527ec
-142 776e4eab086c3cdc
-143 a0ae3b1d8be3506a
-144 408c02d0792ed697
-145 d794916661af8a9b
-146 bc71263bc5d8c0b5
-147 9c45f042d54d3fe2
-148 6942d5bf193bcd32
-149 18c5fee79b8d9a13
-150 205da5134a2ca1fb
-151 3c8ffcfe4a308da2
-152 c6794a44f21c1f00
-153 a6573c09b1bc1375
-154 b9b7f80bda48004f
-155 9fe6d8d0b7a8eb8c
-156 9de7f3eb517a8e08
-157 28e1c72d793fb696
-158 62616032e9d9afb1
-159 1116ade97b32b7fd
-160 b11aa66f956dc0d4
-161 8ddacd5f434d3408
-162 54edf2de8a442679
-163 65d02ee450a9b5d5
-164 a0983f9d56bc8220
-165 259fa0afc7c101e0
-166 e3d399487eb76e3d
-167 7c485aeb97d35d08
-168 d65cc299fda95a92
-169 5240c71b6ef3f76e
-170 3b19bc69d7d3df2d
-171 078d275b5b01ebc1
-172 eed775287d17cc88
-173 7bbe192999ea90a2
-174 c4a6e5313a387658
-175 7bcdd434f60a958d
-176 96625495ffbea1f5
-177 5372af3825f2e3c1
-178 c51537ef0419a68e
-179 e3877c9990afcc26
-180 5adf095ca9ee3e66
-181 a50af6bbda8996f1
-182 cfdcb7731e9abe11
-183 560377ac7fe7c93f
-184 9adc6b1510462759
-185 afdb444bd86d5c89
-186 3ce32a3e0ad859e2
-187 661b93b03d20b020
-188 fd19e8a2c86b21a4
-189 dc0924712204b394
-190 18323a07907876e8
-191 ceb8c91159ec633e
-192 f23da57f7a2d5f62
-193 b13227e724553b72
-194 88c7305dcf6985a2
-195 3f30e65228723497
-196 d76fe1162a76cbbf
-197 f4fdc2f853fb7e43
-198 2ca08c7565f6eb37
-199 f54fa4e58dc7f94a
-200 98d5b5156c37a233
-201 1502148097024b3e
-202 bfb7931083c5526a
-203 764970f9fc9166c9
-204 c433233147ce316b
-205 560ec1ad735b0c2a
-206 f8e7e5b0c6e6850e
-207 a458de988539e7e3
-208 9b8f725394660b37
-209 c8c1e30b2623a205
-210 ed8c37ce6b34e849
-211 f7c5dfd377390612
-212 22d00ca06ead76bf
-213 369892ffb7d40eba
-214 4d08dab11aa10c1f
-215 b8a5b5c629a14d7e
-216 436f4d4055b5c64f
-217 ea48da14e12a41ea
-218 941fcff670def661
-219 8cffbcdaf72926db
-220 f518de4f40639498
-221 6e45d2cb14b6cf1b
-222 680ccb6d6f19f04a
-223 97ab63239d6a3036
-224 c586a531558ead59
-225 9a1314b7611375ac
-226 357274621bac393e
-227 ba5fcea8de76d74f
-228 9b768331a4d1439d
-229 bf80b613d9cd06e4
-230 9ec661984218b47b
-231 df6981ef02a977cd
-232 38842a7fcaeeb4a8
-233 3f451c0f2f3652f5
-234 543f2dbe6db53f60
-235 47be96f9a9e4f80a
-236 e6281fb57f83c035
-237 4920988e6770b26a
-238 152552c7d73d6d63
-239 6baded7aacb0e596
-240 b18a42e45276d513
-241 8afc12311470b3bd
-242 aad3c72ebad23624
-243 fefd91125b5000f8
-244 028058053a7a816f
-245 b28fcd6145f6a4e1
-246 fa2e8290351fdf4d
-247 6c9afee71f3b3efe
-248 e7bda9097aeaf344
-249 5f69c7fce3591881
-250 bc8e1bae971c52ee
-251 7582eef013f7bb49
-252 97c7afdffbba3666
-253 fc4f1e946c02df98
-254 ccb116d0f553982d
-255 1bacfd5ccfe09009
-256 41dbd12f16691933
-257 37a2f90f4589c499
-258 3d435cf1c8273ba9
-259 25da063e5a582d96
-260 0f0329c23c8d9c05
-261 f3df6a8bacf971db
-262 6856fea995892bd3
-263 1837f8ed90b1d592
-264 ce7dd78b09a6959b
-265 14c1a3cb549d4301
-266 351c89a2c8e90914
-267 7c833e7e820752e1
-268 48b77b5fd5f4c487
-269 63fdffd89a7147c2
-270 95dab67f41da23e1
-271 cc64a7e4f302c693
-272 29be3bbac51a728b
-273 1eb1f5605fd5b394
-274 a80bf7ac5d7fb859
-275 6b756c6ee1c42cf3
-276 20670f36730bcfef
-277 7852fee8236116a5
-278 687f61bcc9a6bed3
-279 bc3ac3b382178c79
-280 e0e133c43f367b9b
-281 9be8eda31215c645
-282 5fc09c84ffe9b1b4
-283 336544ddcc5b9023
-284 5d2cd8928dc2d37e
-285 7e9f74cd7e62e8ba
-286 ca49697c4fa2be2a
-287 e097a19012f22314
-288 02e67877832d815d
-289 f9e9897e6a3b4034
-290 a1835377447435ae
-291 4ad4ca933160a45a
-292 9abfd1103047b56b
-293 c5f5dcec0ae1a958
-294 d0f262b48aba5e5c
-295 51e2d7fb69596051
-296 fc3e1a11c01b9b73
-297 b6573caafcc99100
-298 f0b917bac1622ea6
-299 61ec5a76f23ceafe
-300 2b2fe31bb94b8c47
+1 a64ec8ad9e7bfa58
+2 2f2d13f2309b9353
+3 1f9071f232059dcf
+4 2b396ec624470371
+5 baea6d6c1ce66012
+6 2d23d45e694963d4
+7 58db9902cb143331
+8 35938406797c8fc9
+9 09155b59ae543d33
+10 5f6988386260469e
+11 7822b6217431e36a
+12 86bab9059abcd966
+13 90389a5c61cfb154
+14 2ba069492a8ad768
+15 4e327371b6829c94
+16 cbc663babfbb8279
+17 02098f01412e4559
+18 738af5296ecc9336
+19 b0ffa0754fcd1f27
+20 4fba80020ba95aaa
+21 940a90a2e6d5b42c
+22 186bae20b39fd024
+23 d87db5113c63d906
+24 a7de0906b019ac7f
+25 9ec42ffdef281691
+26 74531fcb80de1e6f
+27 385fa611f5179779
+28 41d96b097e1a0b92
+29 544e0f3d15c75e2a
+30 c0a990969ccb6ff4
+31 54d96e5fecb6d19b
+32 b470264a80d5b603
+33 78b3722d36a48be0
+34 d9fbbeb77782160e
+35 235669add883fdda
+36 c1314743fe00d94c
+37 e59b4665487b3c95
+38 6bc732cd9aa2b727
+39 4b746ee8528792dc
+40 357ee3c05428cb34
+41 e5390bc93af7325f
+42 d4a7e773347e8048
+43 745e6925f42ca2cc
+44 705c543ebeeec9a9
+45 17dbfd862970e83f
+46 104b2d6734beeda3
+47 32e44f0965857595
+48 6e6e7c90e2074c1d
+49 9b4b250adb7c3c85
+50 33911b3bb25b7e4b
+51 7d21eed81203efb5
+52 87906374e3c876b4
+53 ddc227ef932dac03
+54 1e8fa583ebb70b80
+55 bfa11e5489eddbd0
+56 ab8b5528f0da678d
+57 d74137963905ee97
+58 831646ae3bca6812
+59 bcf369a19a2f922e
+60 af41f7dee95071d4
+61 d0049732d265cac0
+62 b1861a6f79c25378
+63 dab6c1b053d03f1f
+64 25db05da9e49ac2c
+65 6cf7cca54e25afcd
+66 59e85ee3675278b5
+67 6a0b4e4b9b899650
+68 61b9303ea64e7154
+69 34129173296556e9
+70 55ddb7813c20c77b
+71 e9e81e097256ac23
+72 d3dbd6d2bb0e4081
+73 18e9b33bae062147
+74 98fd1c9183dc35c9
+75 5e808d63201a30f8
+76 f25b0a4588be156f
+77 6739773057a38033
+78 e0b199fd5605a381
+79 94e8448ec411dc0f
+80 28745f07238bd89d
+81 8a01c55c30e617b7
+82 5c1df900a806a269
+83 c4f4b0eedc764f18
+84 f0b5a0eed48bfb5b
+85 e726adefee6d2f0a
+86 8191106b8462c85e
+87 9d6d559470533a05
+88 868e535f8e54fd5c
+89 af2bf9ccffdb7f7b
+90 6f91ae30bc53a846
+91 d25209210d40c86f
+92 ebb22ee3026e11a9
+93 61c306e5d20ebb41
+94 30f2b24e8a22426a
+95 796adb2cc659e0c6
+96 906c4c3b7802bbc5
+97 9c2d7e8af0b4e18f
+98 c1a3a0413ef881ad
+99 2069c9555ab42f47
+100 0378177f50dad400
+101 c96fb366ed14eb23
+102 dcbd8099c6a2f9af
+103 3948b35cdb245a61
+104 a0393fe642db8647
+105 80f22b4e1ec77710
+106 0ee3f9d88f834243
+107 1f28be5364b7f640
+108 0b4e1a33fec6ed1d
+109 623977b4f9224003
+110 ccd30654bd7e0f47
+111 4ebced398c9be777
+112 ed795785c552121a
+113 566539d84d29f952
+114 39da4fa285a2bfed
+115 acf9f37e8d7e036f
+116 c59bca4624223a18
+117 30927498981ff6e6
+118 a6112674c8559ca8
+119 91c598d486d88956
+120 6c7538b87194e0a0
+121 d10712d89a60627a
+122 f47ad05f2952e294
+123 4feaa772274f75d3
+124 604c0ea9864d2b38
+125 afc212de26ab400a
+126 04681cc826ab0af1
+127 c437bf51dd271b54
+128 72d28d5ef1ec5f9e
+129 d02e9c19bcafb5da
+130 464c71d1618d52ff
+131 f59f178570260ebe
+132 2d7a22886e06f9db
+133 e6595b5bc321bd6a
+134 47b6f4062a2e1c26
+135 d8b092a06ef88e7d
+136 8195bd7080f06b3a
+137 d4c2b9337ce99b78
+138 3f0323fa0be3d48c
+139 71ab86f625464780
+140 f76c6a8277e40913
+141 809365ceb2f8f1fc
+142 33c871d35df92e80
+143 3d09c9224f51e9ca
+144 f66a4f09943fea3b
+145 71422922a51d6c27
+146 f932d2d3b468fef9
+147 651e96d26fbf6812
+148 1a17acbec19928e2
+149 38a5962dd1fc659f
+150 24395e17be0041cb
+151 ddcb4f1656f296b2
+152 9efb50645970eb3c
+153 4338338f6e1444f1
+154 7b2946b5a1a964cf
+155 6e3493e33f4e94ac
+156 835cb3f5fb330a08
+157 b1992cbc698f4f26
+158 0d788512a82b5d5d
+159 10b39dc813b9cd2d
+160 3a27985987288964
+161 49ceb4856a9ee1a4
+162 e363178f3cb923dd
+163 c322860e0927b5c5
+164 6f34d740ff9a9a80
+165 2de6faa916d70640
+166 b0479f5fbf98758d
+167 f659a9fb9fb85344
+168 798b6c831100c00e
+169 e015f7e8678f187e
+170 032492adee6f8e41
+171 69246fb36fda4c21
+172 43f48ab6e9ddd324
+173 9cb88a90baf00676
+174 90d9701bfcb39efc
+175 b48c0fa1e3cbd1e1
+176 a329bba797318eb1
+177 a18e19a04c201cb1
+178 7fdf5c5356a96e8e
+179 a8748e3456c6a2ba
+180 a2e7e882e4af4736
+181 1f3abbb9e1d76e21
+182 e5be871c1e9ae2ed
+183 843920f0e800adcf
+184 8bc573afa73fb905
+185 0143d73bb48ef375
+186 93389f65f5f5b43e
+187 f344a1dd00826b5c
+188 019c3bb0124fa320
+189 f68f2df929941560
+190 71a10e86f6a536f8
+191 eec6641d6452c9ea
+192 0fa0c77497eee032
+193 4283453d858f39d2
+194 668ddf5380360be2
+195 903510eacffb81d7
+196 677a84c008c1331f
+197 f14ab24cf5737fc3
+198 d3476d742c42a0a3
+199 3c78faa7d19846aa
+200 492b07178a425a97
+201 10f652f36cb9dbae
+202 3928659b16629b5a
+203 c1fc170efdee6c05
+204 d2d1e54d3714e2ef
+205 849629cacea92a06
+206 1c99fd025259829e
+207 1987ed15b0ac90ff
+208 cd7f0ef79090c68b
+209 7c5e164aa406c9c5
+210 974708515697091d
+211 771c2ec4b84e5242
+212 be6be9d15a0a17c3
+213 9026f0fd4d75c17a
+214 db659454f066a71f
+215 0e3f2de81eb967c2
+216 f6109a53de1ee6df
+217 db04d621e9bc2caa
+218 2d1602e8d97fbc91
+219 c6554d99e39aa8f7
+220 2c01209f93db1e58
+221 b3c7d8f511e803d7
+222 cbfa616c3639833a
+223 658cda1173511df6
+224 60055d87691b7e9d
+225 27e307805b64b368
+226 e8b1efca5ecbe83a
+227 693f83d600d22bc3
+228 12269a776a18f709
+229 f670e634381c19b4
+230 084b3ff95bd3a33b
+231 beabb317d6a049d9
+232 d5ba74feaacdba2c
+233 8bd907f0398c7a35
+234 4894e07360863ef0
+235 82cd416af6b12d56
+236 91e8f4a626441b55
+237 b156fcadc320ebc6
+238 e8daf2efd7b216df
+239 7de6447b4a877b82
+240 7b839f162e983c27
+241 c4b6504914e58f91
+242 92996d32613b3228
+243 e75f3d2f4382adf8
+244 deee4b4d2e6ec67f
+245 9102767d7d2c3d61
+246 613df9a0e4a0876d
+247 0ea8e35049d7e95e
+248 76b3dfce12d988a4
+249 16b9c44c05795d11
+250 d68d2ef59be2eb4a
+251 deebecbb50b54259
+252 2956e17b42afce06
+253 83b4021630185d48
+254 301ccfa84a955401
+255 034a53d4dc5baf35
+256 4220f41120279b03
+257 986af6c4091c3a55
+258 9c89bfc9026c33e9
+259 38bdbe8997748d42
+260 0d9821059c124e95
+261 489d7d82b573222b
+262 bc69e4cf0596c75f
+263 e4af5068d8a159c6
+264 ece5540f5c36459b
+265 1924b419403bcb9d
+266 e5e83ff674742bb8
+267 70fa668b5d73db5d
+268 8f5c604a3d29ac67
+269 de4795109f10e6d2
+270 b846ce92adab6aa1
+271 431972607384f41f
+272 7cdff729796a73cb
+273 3a9e32f794be85d4
+274 6e8e7d8d272a1759
+275 68374238c912443f
+276 50cad1ffcbfde3db
+277 be6a91c2571edf59
+278 134c0c08ed730883
+279 24b2ef0ddec04be9
+280 6857f6fc4856139b
+281 8322448ef9dc8aa5
+282 f9d64d07be3b32d8
+283 4c3342f55b85405f
+284 ea986906f256172e
+285 4d174e3a64651e8a
+286 be1719e51b5a206a
+287 ec9eb9f1992dc624
+288 201f03d774a6c691
+289 2594f99dfaa8e530
+290 74c15493648e47ca
+291 db736126323d293e
+292 17f8a8a520dcc28f
+293 1cce999f162fde38
+294 793470f6b7bcc840
+295 34c15c6ee4b862b1
+296 67986f76874ac557
+297 424bd441733f1e00
+298 2477fb7411927b06
+299 84ff07003cb772be
+300 f5d29df73d17439b

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
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "edge",
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
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.11-terminal-types/r4/lens-out/edge-g3.json
using your file-writing tool, then stop. (Your source value is: edge)