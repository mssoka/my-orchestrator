You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. The repository checkout at the reviewed state is at:
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.11-terminal-types-r3
(all verification reads happen there; treat it as the source of truth).

Chunk orientation: This chunk contains re-blessed golden .t1 tick-hash dumps: qos_manual, qos_emphasis, qos_auto, sla, qos_contention. Part of the canonical PR diff (big-diff chunking).

NOTE — round context: this is round 3 (fix-audit) of review on the SAME PR. Rounds 1-2 settled the background — treat as EXPECTED, not findings: every re-blessed golden .png renders the #67 procedural background tiles (rebased base); the .t1/.log.bin re-bless is the documented deliberate catalog-fold re-bless (the 5.11 catalog change alters the catalog_hash field at fixed offsets in otherwise-identical dumps — cause-documented in the PR body); node_health/terminal_types goldens differ because those demos spawn the new terminal types. Audit the re-bless CAUSE documentation and consistency, not its existence. What is NEW at this reviewed head (d0c2c38, the round-2 fix fold): the honest W9 surge re-pin and a new role-absent inertness test in core/demand_test.odin, split base/surge ratio windows, the palcheck sprite-canon scan (harness/palcheck.odin), catalog_test additions, and header-comment fixes — plus the fresh full golden re-bless that accompanies them. Delta-introduced regressions (a fix that misses what it meant to fix, a re-pin that silently stops biting, a scan that is a no-op, a re-bless that changes MORE than the cause chain explains) are exactly what this round hunts — scrutinize the changed test/gate logic hardest.

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
diff --git a/goldens/qos_manual.t1 b/goldens/qos_manual.t1
index c622dea..7e44bbd 100644
--- a/goldens/qos_manual.t1
+++ b/goldens/qos_manual.t1
@@ -3,305 +3,305 @@ t1 1
 demo qos_manual
 seed 3003
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 300
-1 f0cfd431af0a9769
-2 77a12cc8b819136a
-3 2be1d73184d79eda
-4 37f844370b0f9460
-5 09950cf6d2a227c7
-6 ceb4516259217355
-7 58f581786be4ee84
-8 3582d970e1b55848
-9 44b212bfd3771d80
-10 29cd0e71375e3ac5
-11 7d03e72318e35573
-12 2c79404d2f9c2171
-13 15ed7bab23f99f6d
-14 38c1cb144e563bcf
-15 ca40917fd3539ee1
-16 24230c5e76c3f83e
-17 aebbab6e79fd46f0
-18 7d5190e961826bad
-19 5c645b5579d06a42
-20 7f379a76630d1ca3
-21 787f783d33925429
-22 331f7fbc0ccac97f
-23 74d28e7901b131a9
-24 df85dac1ed1ae3fc
-25 5c08a62f3c583348
-26 17dd169a3ef4da9c
-27 3dde274647b9f2a4
-28 dfc823ad19fc5799
-29 eefa2fcde9809095
-30 b447fff815299cd1
-31 de8e74b4e08b7190
-32 a83cc3167d5e7820
-33 cef1e3e7caef4fd1
-34 9df5c8948c9dfe05
-35 1056bfec7ade5483
-36 a26b642a4c087e2b
-37 37592b2865b85168
-38 b6cb20ed27199c5c
-39 2d0a71cbbd292c45
-40 8223c6fdfce496ef
-41 2b9a7a4f9928b30e
-42 202d4d9cb8d84af3
-43 08c3d583df8b8d3f
-44 14c318a7ac24f2a6
-45 f20dc7a52a134604
-46 8ece7772c54242fc
-47 f3bf2d38247c5bf6
-48 982ebc85b25d122e
-49 2ff15bb44f8cfadc
-50 54c52f0c83481e10
-51 d0a8ca25cf805228
-52 7b41a129a125cde3
-53 29c3a41a42e71702
-54 c5c32632e5dc1d21
-55 0f0ffc3cc7c2b673
-56 3bd609e0c7f7ca6e
-57 2f27fbb643c4f2fe
-58 53f9f0e472b91b75
-59 60ca87176c433565
-60 d610e914512f432d
-61 cca38c384d6d891a
-62 dac656c0651b5216
-63 978adf12fd747ea9
-64 c31c9d77b64658b2
-65 9278fad587545253
-66 7c693b3abee8b5e3
-67 8afb9dd135c342ca
-68 b31ea377a7b14c0a
-69 fe2e3dfc258bb073
-70 58e43b1d290a34dd
-71 acb2e57b5554bee9
-72 937c38874679f0c3
-73 09e168dabd4ce5a1
-74 deeacd7f60cdf02b
-75 1c73f887b8d38f3e
-76 2e5f9889a7d72e0d
-77 edfdd5d3378d8245
-78 607c39b7c19ec1ab
-79 62a463c24a3de305
-80 f0dbbfda6bc408cf
-81 2733db277af03061
-82 8492457efb1d5b77
-83 2a43dadacd81132a
-84 fb5aa09ba86e6119
-85 93b5c057b930bcf8
-86 6b6e1136f1da9580
-87 e3e11de9cc73737b
-88 e70ae4a5e3a7568e
-89 9e602cb1620356d9
-90 1f3de0af1fe15190
-91 843d725b098e4011
-92 3b866776f14a3b3b
-93 5a93cd5a901c36ab
-94 11e9478b71a24a78
-95 62c7f19ab26a31e8
-96 c14f302c84988b3f
-97 80da7545411c4ca9
-98 ea55e0ec2885674f
-99 2f1b69a0df78a255
-100 852acabb13fbefda
-101 1d85db9e461d4f21
-102 497f9016406fe8cd
-103 2fa27efd5f4115db
-104 2e795e2144af809d
-105 bbcb5cf0e0f561e2
-106 91d993970f18ea5d
-107 9a372a4780ad8be6
-108 aa66b1c9b358719b
-109 e20836225a8cde01
-110 2cee678c54c18c39
-111 7479780298ccbf59
-112 f958a214a1353f80
-113 108eaeff9640c3c0
-114 7114aa4a9aedaf3f
-115 9cfb98d189ce8885
-116 0e3b1fccd9396df6
-117 01619fa3e5e86c34
-118 291b95f11c0465d6
-119 662d9af904cccee0
-120 5717337cbf6e15fe
-121 cefc446a89583b1c
-122 49a0b617a5134e5a
-123 0712d47ee9c52589
-124 12cc52c7848167d6
-125 340fc14714cdf4bc
-126 b6675996ed7fcd7b
-127 73899bc77b18a936
-128 21d58d4d4899dfe4
-129 83c706aeec39ac1c
-130 148c27050db4a52d
-131 26ebbf8877023ee0
-132 5ec71cf1e17132fd
-133 19cc6ef572d4ecd4
-134 667f20064ed78f94
-135 58f4423c2e10234b
-136 095094f29fb286cc
-137 3d0a8938ee763452
-138 12d8624ae5f69926
-139 fff86c86aca4a936
-140 800acc03d34c7bcd
-141 467d6e0492490882
-142 6ccb6e85510606de
-143 44a34dda3ccd67e0
-144 310f5b250cedcf95
-145 7ca666750108da75
-146 c1d7fe88685cb83b
-147 5319808e3e4af260
-148 6b7622fdddf6083c
-149 dd2a3d2405435245
-150 99a3fac25e711059
-151 970d58a144a3ef08
-152 9aa25c4c7420e726
-153 95cae80ba55716e7
-154 9c5b4a9cfe3b9c5d
-155 192745cc8cf85ba2
-156 ac4eb12eec0523fe
-157 c72a93824b4352c4
-158 71846b63c9cd8b5f
-159 ab7301f11d7c4d8f
-160 1caff70595f5bca6
-161 bca7bd24468fad76
-162 c4fc1aa3fb1ded8f
-163 5865d93aa2d79a7f
-164 d63e5795ee9839ea
-165 c38800b88cabddb6
-166 b6778a8b0d8ab897
-167 e42412c3beea1516
-168 3cf91e3b452124b4
-169 e0bb4e89a4597ab4
-170 981e6971c887db1b
-171 5b58588896729b9b
-172 0848e637184c6d22
-173 bd58de0fa757f4f0
-174 522d1aebf8017b62
-175 5094dacbddbdbdbf
-176 7a9f2729f498c6d7
-177 b73f5225f8d02243
-178 d21f206152bd5848
-179 4c5946463fa1b784
-180 6ea9260858eb0520
-181 2152d473af41b09b
-182 7a26cfb191ace72f
-183 eeac8a0932ff4bb9
-184 f55017dba024ed17
-185 52303c9f24731efb
-186 7f067a8348e0c83c
-187 d29a75aff7a5b376
-188 3ec2a14f6ef6ac7a
-189 65d2d33d821d9eea
-190 2f102e433e107c52
-191 6bfc2a88091dc834
-192 690d191dacf392b8
-193 9ae1c598c8f7b498
-194 d971d0044498479c
-195 3d79fc6f9dfab4b9
-196 3bc9f212d66e6f0d
-197 9554f30a7c126e55
-198 8c81bdc2270873d5
-199 fc6aea9b6ed04390
-200 0a41901e2a29c931
-201 973910f5c1c79604
-202 a2c03bc037c20d50
-203 24b947d950d5eb63
-204 926e1fda52c83959
-205 b3e4f82c10235098
-206 16d7b3278f6d72d0
-207 b94ae352096bc2dd
-208 db7cafe0f51801b5
-209 2017173fb7a09c17
-210 70bea35d038b04e7
-211 a1333c9f710d4350
-212 be84452d9d34440d
-213 7582cf7bd686b3c8
-214 d7e07358a935f52d
-215 e1c21e997e2f0514
-216 77b2af4e3a7bc78d
-217 d307c1e2d6906360
-218 a5517b8735e85257
-219 6c46db42f78627fd
-220 c071879523a3d5b2
-221 f7a14053f3ae06dd
-222 cbb9380ca476ca8c
-223 d2e4b2c2c75a6240
-224 b7137fbbbc6e9067
-225 fc86b657e8ce754a
-226 178191f3d4bfeab8
-227 02465471d8f49dd1
-228 3ac54d6190ede60b
-229 5e91ce47f80430ba
-230 65426bbc04433219
-231 b8bb8b86d9d478df
-232 1c0f5bcc66febb2e
-233 c6fada91771f4ec7
-234 abafa88ccf4d3b3a
-235 c579fa46ad8fd9e8
-236 62d3aa24a544af37
-237 52ad8b64c94c1778
-238 4325c92abbc97421
-239 39cba773c5de5e2c
-240 e958b4bf12690735
-241 40462732e1ea7e8f
-242 a780f4f784726df6
-243 f9b9bc9bd0827a8e
-244 8e7efc37711dcdfd
-245 bea58b080bf593bb
-246 cc6b79f40670388b
-247 931a28c8797d0894
-248 55a70ddafce3940a
-249 f9f6a9aab9bbda93
-250 560d5316ac617898
-251 5c2ccf57cd789d03
-252 e7d670ef88eff9a0
-253 89fd167ef2b6f83e
-254 566ed4b8a3bcf79b
-255 f8ff6758d9ecb4c7
-256 b2fa9b62eb759b21
-257 35fef33aee2b1433
-258 d517d994847333df
-259 904ba94e7e32ef64
-260 1e9c55fe94ca0e3b
-261 b936939d1633eec9
-262 089b77713f5868c9
-263 ee92e493bfb09480
-264 c50b046044057ab1
-265 0216f12b89c93fcb
-266 8f221919b217786a
-267 79aa1c95ea464713
-268 e0d3de1a47dfc90d
-269 46198b1b148a07f0
-270 3effa28487e122c7
-271 a8998d1c8a6c38c5
-272 f00c02bbc2df8411
-273 52cb5450c549fa0a
-274 7d84f17f376b26ef
-275 f938dfb9d92c6e35
-276 6151df05bb85afe5
-277 713f674cd6e0218f
-278 ab6c39a3e905cb29
-279 d3cbe36353347c4b
-280 e173fd608a5114e9
-281 70f64f00f55ba92f
-282 f2de4adbd0d4a48a
-283 7c8f54094d7b5de5
-284 9ef62bb6dd152e50
-285 f6eeef523c22e928
-286 4d8590a460bb4a34
-287 d3d42bdfb7f5022a
-288 3c405f79b95cafd3
-289 b2563c79d8b9e14a
-290 95b0745129afadd0
-291 47cf8a1e3f0342f8
-292 65bbe41e1b4b17a9
-293 8dfaeae7190bd43e
-294 af46b6e3720ee316
-295 b5e65b728703a52b
-296 54e6d9aad4a988c1
-297 d4a85a1aad4ba6c6
-298 02f12fa32ea32424
-299 11031c7638d07e7c
-300 32de90158da0d44d
+1 199041449bdca439
+2 d0829902bbf7de5a
+3 4b370a7cd7963f16
+4 6302d449a56f4964
+5 0fe0cc3388743307
+6 cd1bffe6d41589a5
+7 9b85f0bbfb249924
+8 18d558ea3b0feeac
+9 ffe1de8d9797ef24
+10 d8e46eee454d2fb5
+11 9d59841e6c7a6383
+12 9c9db26275295071
+13 45b71d7253b43a91
+14 175800fe24237cd3
+15 ed86ba1e359518a1
+16 fc806ade3ed8f8ca
+17 6755c6e56e024020
+18 291b13cfa10c2e7d
+19 1fe9d5d293475e02
+20 2865d15647a9cc73
+21 36ed78e7e5e82729
+22 bdbca9d98d29c5ff
+23 681ffc256827963d
+24 56fb72b6976b03ec
+25 7c43ff87c0627c28
+26 184dbc4131b2ed18
+27 171842f56aa29e70
+28 00f2f8754c299ded
+29 4577010a805ed3b9
+30 6263862567ac4e51
+31 86d0faa7d6e8c0dc
+32 d4960e836852a680
+33 4d48fca15792afd5
+34 c9dbf415d49655d5
+35 19215abedf634d13
+36 45a3858cdc1144eb
+37 b24ac57072d4db54
+38 bb16b27cf4d1adb0
+39 83deb2e1c4eeafc9
+40 0495e4435337f7eb
+41 bf205b58c3d169ae
+42 810e3eba14022883
+43 7e2fde32e102c44f
+44 82a0edc3ca46cfba
+45 4af24b210e963e60
+46 971048312a85e84c
+47 f8bbcd3fbb2cd23a
+48 6fb11a4d1afad7be
+49 5f367238b110f39c
+50 7bd5fee8320a0f34
+51 fae2cac55fef5ddc
+52 96ac267ab71de333
+53 963adc5c8b942e16
+54 dc61423496b098f5
+55 50823e43b18da463
+56 a360725e2fb900be
+57 1b06d85c10ff10c2
+58 1f441ea66518c679
+59 5e984850cdb8f185
+60 7a2175b7788c4a81
+61 281524796da24446
+62 ea802bb11e2736e2
+63 8252d3362d55e5b9
+64 9a1a793a11a2781e
+65 3dff85170347cdbf
+66 c4f8a548046f3553
+67 318b6fe87f4bb326
+68 522f3aa3cf3a68ae
+69 e20ab52210cd20c3
+70 8a678b27090386d9
+71 6a04cb51da0ab8b9
+72 bd7ebcff84d4d29f
+73 78a7d7539126ab11
+74 c0c8cea0691c29ff
+75 3c0f04e86e03453a
+76 ae8747ada9c948bd
+77 e2ff925023455f55
+78 20525f40080441cf
+79 df2cb0ff9b24d589
+80 2de9105e839c5e6b
+81 ce9a49d52d6f9811
+82 2ac01cab0dff4b07
+83 751eadfe7806819e
+84 d4a797f9b7fd3329
+85 bc502d90e8ff44f8
+86 69d3904272cf1340
+87 382fe46764effe17
+88 fd2e76293abbf01e
+89 c65abde3810a93ad
+90 ea57abbd82a47f50
+91 f68a85078a19d461
+92 ac726e630b2060c7
+93 3edb2084fbc77f3b
+94 69e7a8f2c076fcac
+95 f35eb853562658fc
+96 70c8910e857cde33
+97 c02eb42d31a5d3c9
+98 649386f4805ab233
+99 6d34695ff065d029
+100 bda731c709ef0fca
+101 440da94ba2faebf5
+102 48022fede4a9c3ed
+103 3a700bf18146fbaf
+104 0f1f5b6c946b1fe9
+105 5dccfa5ed357457e
+106 5b28b596ea4756f1
+107 28c3615dabb61ad6
+108 d6f2f076ed58e15b
+109 e42cb4f26e9d57e5
+110 587872ac28abab85
+111 1be94e4849af53dd
+112 b0e58d3405f1ba10
+113 8343b96a1722b790
+114 9af88f41c2111dab
+115 b628a94dc3d47c11
+116 79aa120fe9a12d42
+117 e0b067467ebf9e64
+118 b2659e0d23d0bcca
+119 9f9f9e10a74a726c
+120 f13ec94f6e476672
+121 bd74cc4cbd0a78f0
+122 fddc75ac6aeaeb36
+123 64be66dc27dda295
+124 654be62dcf3a3b12
+125 bc2194b4ca0d25f8
+126 9931e47f9f616f5f
+127 7e02443bbd8fe3e6
+128 3cb415351d56d6e0
+129 90d0498b558875c0
+130 1818ff2a8da4af0d
+131 b5fd37fd4e0f317c
+132 240427c0461ea6c9
+133 620651d0c22d8a58
+134 22e437b843b539e8
+135 043a9dcafd0e270b
+136 94a1d76cc5a57cfc
+137 037bfbc688d16cce
+138 5d7322c0e691a0b6
+139 f95e10853c5770d6
+140 2839308045162d21
+141 28abeba8ea36da12
+142 af90e26058c1a082
+143 1218b0cd1c76a5c0
+144 5dc0e3f486fac959
+145 98a614108e700701
+146 b3dee4432067d02f
+147 015cc675bd4e48d0
+148 f58a20b52d75a06c
+149 ca3061983b4c7e61
+150 9eb85250219976a9
+151 04bdb7dc58481f18
+152 cf94ced5b6f9b142
+153 fa6e721e6fb04d03
+154 7f5420163cbfaedd
+155 c52d0640ab70a742
+156 e9cd71beb0703ffe
+157 d4c48fd710efbc54
+158 5a3547d7ba5d2b0b
+159 8133db3a97f272bf
+160 5b7928d51bd7f5b6
+161 a5e4b44d17894e02
+162 2d359c9cf84ac6e3
+163 342e72fb7fd3deaf
+164 bc4668ef32c1ffca
+165 f230eb35b58cc396
+166 638364cb914e08e7
+167 85aac1ec00d49d52
+168 4c966eaf12a61060
+169 3e96c756217e1284
+170 54f7bd17b067c70f
+171 55451a32c906637b
+172 d668d553c55e68de
+173 3fa28817755dc2a4
+174 df26d136bc2b9726
+175 ef07a80b6d0f40e3
+176 c4b13c6c44f61503
+177 124847331dfc1173
+178 a808532532a9e048
+179 0bee6aee035f9458
+180 c89f16e2ca3928f0
+181 548fdbeffe8b6bcb
+182 2b058389af516d8b
+183 315cd53f05f41a09
+184 bcf694aa2014e323
+185 c50b057ea39f46e7
+186 4abc885c96be5028
+187 e36b1c9f6f0e5372
+188 a7cd63cc5ebf35d6
+189 76c093f43d3374e6
+190 a3140df657b73b62
+191 c1201b406d6e03e0
+192 627ebd4a3399ac08
+193 f77f68333cde8678
+194 3a79f001fabdd1dc
+195 8afe66303a3b0ff9
+196 251c2d259bd0006d
+197 d652af135cd8a5d5
+198 a144cf242c6c8ca1
+199 26a312859f1987f0
+200 bbc5fd79907a62f5
+201 54f338926bcc19f4
+202 73785fd0e18ff080
+203 7fb99407b5b3143f
+204 ec824fd05acb453d
+205 2e85b5688fbd7124
+206 7d6ec4a368aff5a0
+207 15bb12dc2d24e139
+208 507fc09293b7d8a9
+209 4de571c462daedd7
+210 b4fc36fc72b3d1db
+211 49b3d829b25c60c0
+212 b60180397a9cedf1
+213 9375e98beff9ba88
+214 db0692314102d82d
+215 e1bae29005188028
+216 2897213d4ec6c69d
+217 a81f5a959de53220
+218 6496904dd7653447
+219 88b1f22b97a9ac09
+220 2ef4b2092baa9972
+221 75f49ea32ddd7179
+222 c7e60e7551a9a8fc
+223 9c8f54e150a1c200
+224 db605fa60671314b
+225 89da4004917a3ed6
+226 34f550aae8dea634
+227 84faad7664a26d85
+228 55ac715001535b77
+229 68cf98096859398a
+230 b2ebfe68b9eca2d9
+231 506c0021f45a268b
+232 e94416f82b29fab2
+233 57fea109bd9ff407
+234 7589a6443a681c4a
+235 e81270c5f87e1604
+236 56080bddd62ebcd7
+237 f59a7aa0681fbdf4
+238 1a788ed4f0f584fd
+239 4ece7b2a7914ad78
+240 9ec7e26104815039
+241 df597e315ea322d3
+242 1ad2191d2e9841da
+243 ce1abddb96f69f8e
+244 4b09aaeb670fdecd
+245 4bc9977f29b8fa3b
+246 84fa545d37f1d12b
+247 506bee06fae15874
+248 af38cdc8978ec66a
+249 84287156009f57e3
+250 7de0aff17d3ec8e4
+251 4caf6ba014f8d513
+252 b4bd95d7adb4c640
+253 22d0b59b64f322ee
+254 6845b1de4bab17ef
+255 6d9a2bf3eb9471a3
+256 d21d122801a6a771
+257 e9327513494a470f
+258 2e4a303ad139021f
+259 a729e86235406ca0
+260 1b4cb62a92bdb48b
+261 902780dec3302c19
+262 5d914f14e9d9a1e5
+263 ee127ce4f29d4144
+264 b279709b8d99aab1
+265 8611a37faee3cc67
+266 de21cad7f416417e
+267 584740dd54d8bacf
+268 29a053a46d7a76ed
+269 5911441079d79a00
+270 d53dc054f7693b87
+271 9a2f54508b7ca021
+272 bf632bb0efd97351
+273 4ae07ad969b2924a
+274 17d6369207f82def
+275 2ad58e1bcb65fa71
+276 d2f57fd1d5d60121
+277 e7e460e63fc66763
+278 c219df37000a6119
+279 b88589974ea9d27b
+280 0e6dfb27959cece9
+281 e74cbf21b771638f
+282 1b7f88d60389f9fe
+283 a582cbdea4cc0bf1
+284 268e5b0cffdfc8c0
+285 d8c372425432f238
+286 3880d1d17cd3f274
+287 8cc305ebb37096fa
+288 c17b78a286b29cf7
+289 33d53571685fb346
+290 9c8a2d449833d1dc
+291 f39dc1d78ab542ec
+292 6ab88d177935066d
+293 0cd4f1dbc4e06b9e
+294 89a7cf6240b33f3a
+295 f346bc71f4684a8b
+296 b0440d380fd2cd65
+297 99d699b9153fabc6
+298 97460b9c03a19604
+299 b79354f01b9e303c
+300 9e3d30e46702b3b1
diff --git a/goldens/qos_emphasis.t1 b/goldens/qos_emphasis.t1
index c4f7eb8..e672812 100644
--- a/goldens/qos_emphasis.t1
+++ b/goldens/qos_emphasis.t1
@@ -3,305 +3,305 @@ t1 1
 demo qos_emphasis
 seed 3003
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 300
-1 ee65d23c7b0a9f9f
-2 8175deb20ba250dc
-3 7c17d7c8f2c6a02c
-4 cc7b0317d21aaa64
-5 6aee18a2eac626d5
-6 a9cf00814d4db647
-7 d142892e31e1b3a0
-8 7d757448b2c2cbdc
-9 4c8c7a40c4871484
-10 d39bb16178e88359
-11 bd7d758308ed0687
-12 ad156b6358a9489d
-13 882dc085d7f752e1
-14 156aeeb7bbcede4b
-15 ad8a6ed806b94de5
-16 56ca4a9b7c57f504
-17 1a5e846eceab348a
-18 22f52278746b4e61
-19 141efc88e1a897c4
-20 50c0306e851ce447
-21 1b850655e9accf15
-22 97dc5a8c785f446b
-23 40f2d040a4bf14eb
-24 3265f44b1e5a7562
-25 7b0cb548b908e302
-26 eff9d69b4374f5d2
-27 6a13c7129ca13ca6
-28 a27d0e267b3f3315
-29 67f9aed7bb35cbbb
-30 69cae1ccd3423e25
-31 80b6edc0b765457c
-32 5f8918331b03fc5e
-33 992eeb3c39a543ed
-34 102af69317fbc189
-35 a32a6a58f2ece207
-36 33520884d916796f
-37 7f4cc1acbeeca04a
-38 0d7435a8b527a86a
-39 6cfc7084622fbdc1
-40 f06b5cc1f26bafbb
-41 4af8ac7c3200137c
-42 9572bb96b1c21587
-43 b3d54f15f9188be1
-44 d5665b6591758e64
-45 e175bb4f2daad330
-46 1e7daaa1e80f711a
-47 66b792124b402562
-48 8f50a41b58236a14
-49 e03d8fb3caa7d21e
-50 ef604787cdf430fe
-51 510a774025070012
-52 7b682e8061ce6117
-53 cdf5039c11cea06c
-54 671c7057c0287235
-55 75a1c58486db426d
-56 73f279449b1d49c4
-57 cdfbd5b9aa113d18
-58 544bdeb360461649
-59 3d8411e90da96227
-60 6929c4dc347d18a9
-61 4895134764c3f558
-62 552b50bef992550c
-63 2dc9beb8432949df
-64 612562e0ce999358
-65 30ee52d62e73179d
-66 81e813ceca040939
-67 8c1db170d1f44520
-68 d89f299191646178
-69 5d2573367bc86d75
-70 9537e976375fbe1f
-71 64e1805989b8ff13
-72 5821b126982473f9
-73 fd0399779a2150cf
-74 7dfcc3d0acc92c9d
-75 c1003e8698a2f80c
-76 1b4e990df27481af
-77 dd18fcea568e32f3
-78 9aa8c268989d1e31
-79 0651a628aa3502b3
-80 11049f32c92bb1ed
-81 2d49ef7068c14abf
-82 bacd4f29f04002a5
-83 f621c5e57b3e6d28
-84 864585e3cf1bf663
-85 b800b45aaef7948a
-86 340eed6a714ba4fa
-87 aadefb0bdb73cd6d
-88 677f2915abc4d98c
-89 7003c5e523bae243
-90 498fdd94a1c5ae12
-91 c85d71234aa6781f
-92 0deb87d773d54601
-93 df748acb721e1e2d
-94 8dcee03b0e145442
-95 0c294a5558f0d102
-96 9eece9476cc48c1d
-97 a5457906607d2517
-98 c0cdd360d82629b9
-99 f3fdb1d003bba6fb
-100 6e6bac256f1e6bc8
-101 72b1caabfdaf0bc7
-102 99db37b0eb62d00f
-103 cc7c4a0af53b7969
-104 67901fcc9155b26b
-105 a7093a3da9bfb188
-106 d8f090df42cf5eff
-107 8715999f1640baa4
-108 1b2cc1b06b5710a1
-109 065755d99f638707
-110 e1c99b30436b99e3
-111 5ad941345fca8143
-112 9ff18c0e425cc902
-113 52443b3d902706ca
-114 01b828fb0e963e5d
-115 cf810d003064294b
-116 330207d14395ef1c
-117 1152e0000a4458a6
-118 c2d1812796ef8eec
-119 9f1b5784d8a39afa
-120 96ea32318e43aa3c
-121 903cec6d9c4999d6
-122 85a144ace7193438
-123 b228ba08221cc407
-124 1c3700e7c59f219c
-125 6c7207fe4a4cd12e
-126 e25c04d49385697d
-127 5643c7b5d1dca15c
-128 4c1da9d23071264e
-129 ac757640f7cc0e16
-130 a5ef9ef1e011794f
-131 c69df45876b039f2
-132 d3d1dd50c4741e1f
-133 4a9a1a733cba73e6
-134 2ea896186ceb7116
-135 7c92a697c5ac6899
-136 2681d47efdc1b356
-137 b2664cc21ba80f38
-138 0f6eb71207d5b3c4
-139 4b7e76866544f574
-140 ab3fd5dd5ac4a16f
-141 2114ca09eb0454b0
-142 eb9dac1449048554
-143 3ee263d5f9f575ea
-144 fe5e0ee5b85e1947
-145 2491ec68d93c4b1b
-146 0c75ab7bce40febd
-147 dcab24055f021e92
-148 07f7a720b1aea1fe
-149 836b20d936f1f123
-150 e570cfb319150443
-151 1bf168e5c0671152
-152 a210001c9593f854
-153 dddb88d437512e09
-154 563855567f7a876b
-155 7646a679de62ffc8
-156 1dc429014ca4460c
-157 1de4c0c4c1cb9c46
-158 ca6e05889e69873d
-159 bce79eba7c19d599
-160 1f62e0f38d9481e4
-161 a1c68b3e14235e94
-162 fdad08b243a584f9
-163 bfdd6ed88943d1c1
-164 1192ef18a4cfdc98
-165 470ed7dbb3054b9c
-166 64d61b4a60ca52a1
-167 94fe7ac7db4c855c
-168 390379713e13940e
-169 8fb2e67a1a6fd45e
-170 1b1b16d3e9ac2781
-171 0cc92307a74fc355
-172 7ea904e17501f6d0
-173 af4a53f838f8436a
-174 4a0eaad4b1224320
-175 0cf6f52be15e5229
-176 9ce4b6f0c874d8b1
-177 a65e60aacf7c4f6d
-178 58e3296a80b0864a
-179 8ef6d04920621f7e
-180 358447fa7b52290a
-181 ca21330b73ee9cc1
-182 509bb6f4cd0b278d
-183 f3278415d75a99af
-184 be36039efa8adb65
-185 5852aab57c1323d5
-186 dec2548b0245fd16
-187 ea3a17797cb0ac54
-188 14894c5da6131350
-189 00bdcecd214c77c8
-190 cf245211212bd010
-191 926d6d12c79ceb46
-192 f63d42f412a8e5aa
-193 79d2f79bbb57050a
-194 9453809949d2c0b6
-195 118c564cf494a987
-196 8dd299fcfedf600f
-197 9caefc00a782b4b3
-198 f604c1fcd3139887
-199 90299d23f3a813ea
-200 6f36dd30d793d94b
-201 08b2fe07558212ce
-202 1467d723fe21e4ae
-203 9f0476adca6d30cd
-204 19358a9ffd9564e3
-205 07c7aee77af0b3fa
-206 92843fec27e7ee2a
-207 6b71ce24c21c8d5b
-208 8ff8d1fecfdd1b87
-209 842db51c0c7b0f09
-210 e043af853614cfb5
-211 05cfd632c4a011e2
-212 81f9c2f987e8f88f
-213 fc58d1da80c2f2f2
-214 47a490eaf02c315b
-215 8920dcec57b77626
-216 779fc343fd94b26f
-217 c149972799580fb2
-218 fddb0e5a40891541
-219 d786d7d2ea751553
-220 c83304f77c275ee0
-221 0da466dd98224efb
-222 8b0578f17f0a880e
-223 7ec45bb8524270b2
-224 50024172fed00d55
-225 6233bd7586167d70
-226 a859f098aa82679a
-227 8215c3843ccc36af
-228 c7f47fae6e105e11
-229 151e93cf21225f58
-230 d7d1f50c5f0ac023
-231 4a04a217369eb049
-232 d2d31d5865eba14c
-233 e14a934e2158dde9
-234 9313d1d084efa140
-235 2bbef127b5d0172a
-236 24f4366a70e670b1
-237 bfa7f75c03ab1ca2
-238 290cb3eaad03e6bb
-239 270d6563b9f52e8e
-240 1eb5d4ffcc326623
-241 c2e7094a5f4d7731
-242 a7df13235958b0ec
-243 5b067ad05494dfcc
-244 0fcc54b1b3d5e0bf
-245 8935f2c1c8b327cd
-246 af7ca578a0033e5d
-247 0df88a9078157ea6
-248 f4fc82a5a69238b0
-249 2a301612c95bfafd
-250 9d7d26be4546e9aa
-251 eb108607addff44d
-252 0309904ef261c7ba
-253 31fc0db84291e1c4
-254 37777458b178a741
-255 00402cc8b11d669d
-256 a631dec6f4f7f4c3
-257 c1b6709216525395
-258 c9aed5feee3bbe81
-259 a13050390e0a5f36
-260 2186e9f83b122c55
-261 10ae53ec9b180dd7
-262 dc9a86a37b14e337
-263 859951ac7810c9aa
-264 73a496fb5cb52b9f
-265 04683c1432a5f74d
-266 26ca68b39e3eed8c
-267 be3c32db4569035d
-268 742f53e6f938db93
-269 392beffc100a27ea
-270 90ea63524c1a0689
-271 96730a93f2cc83f3
-272 3a5345339595f72f
-273 bd3a21b3b14e1088
-274 0b5264113906e671
-275 fc86dc0cde5f648b
-276 232a19390024996b
-277 5256bf8d23400869
-278 8ca54a5ccdf3b317
-279 be610517fcedb7f5
-280 9f4dbc167e0ad84b
-281 dbdb74f84c5ef8a9
-282 58a0bd27c5aebe6c
-283 01d404a5531cbd83
-284 286e405ea0c1975e
-285 6d2463de2368e4d2
-286 cb55ceb07b18388a
-287 6d319cc579db3e88
-288 9a1d8bc15d1b0d7d
-289 85b27c0e2233cc28
-290 45e5c1e0b42e2946
-291 b102e081425afea2
-292 2d5d244f5443a343
-293 f7df5499a853cec4
-294 f48320a545fc3500
-295 0c4fac6cf3f79edd
-296 e3f8fe6fcb841553
-297 edde502d74d9e5dc
-298 8362504890be0832
-299 20b150978d1e254e
-300 c07854bba36e5493
+1 ca7d672af06e798f
+2 541a46b103c081ac
+3 23a6cf6ff1c4ee40
+4 9ab2d2af5b405200
+5 87e5e71873c75c95
+6 d5c76b41ad0ba7b7
+7 0a224d42a1dd5d40
+8 10e72242aafca2f8
+9 79a5b30562acd9e0
+10 c6ca1b267f51c929
+11 de8cc3759f39fe77
+12 7beaa4c802cc459d
+13 070c4513bcd9b41d
+14 889174e350f57587
+15 fe927ef52d287725
+16 cd29f45986eadbe8
+17 96f63cc1c6ea295a
+18 78e453e90b3e67d1
+19 a86906a7d25fda04
+20 915b29505ef919f7
+21 3087e56aad61f815
+22 6c6261b8404030eb
+23 85f2a6f4feab97e7
+24 e5ef1308c0fdadf2
+25 630d673b034cbf62
+26 0a4edf8b9dbfe726
+27 541ccec3efb6478a
+28 b0dbb1e58e61a901
+29 e73a2ee83e00ff57
+30 6a4902673eaef5a5
+31 1c16a522addf4930
+32 9f9cfd06dd64163e
+33 0946b76724e1e149
+34 f5d2d4a8bf58f9b9
+35 5e7d8e8bc5be2037
+36 73a2f62372776aaf
+37 721ff2cac979384e
+38 20ae3c2dd411b386
+39 ac0118c1e8200a7d
+40 dd4aff868d73e19f
+41 6497370a81c1b49c
+42 332545d9b51aad37
+43 8593eaed80994b11
+44 78cb33b2229ea760
+45 77275721abffee74
+46 3c935cc16238284a
+47 e7407d74dded2dde
+48 a3f3029687a81744
+49 532277446c79dd5e
+50 2b21b84a26ae1aba
+51 8ef375260c62303e
+52 c145704396216b07
+53 b7453b5d89472568
+54 ebce99928f699a01
+55 54f945bfa5616bbd
+56 8ee63e4411ad02b4
+57 e95581efba7f59e4
+58 f870c7f99b8347a5
+59 3f26d19ae52f7047
+60 46765abf710b0e15
+61 5a4271d32db3933c
+62 c287b37f862f7c40
+63 473402695e2a63af
+64 c3a9dc84b5a36dac
+65 038fbc6472a29de1
+66 42a38d7a79354ca9
+67 0b16878b9bc311f4
+68 e9558a3e0d56c924
+69 4e6d611775044a05
+70 325aeec9d34886c3
+71 ca5fe5c380ebf5a3
+72 8db7039712a5025d
+73 e3e897c45fcacf3f
+74 bd42b2763d6220d9
+75 fea5944b86333c20
+76 9b1cf6aa7985711f
+77 ed0079c0d0edcd43
+78 98e15d867169e76d
+79 d21537ac36c5261f
+80 6fe919097d987cf1
+81 7d2b8e5556eaafaf
+82 be88b777edd3ea35
+83 4b98ce821e183d24
+84 7a013cbb52150b33
+85 78697b675ed89c8a
+86 1c744e2702fd4eba
+87 63d63fa1bc891b71
+88 d3a11f6c21f8d9dc
+89 28421ae68b1d58af
+90 18ed8c648f2681d2
+91 d791736d43fce9ef
+92 25e2b4429fd6c9f5
+93 7435bf5df81b5b7d
+94 86cffd0466bf974e
+95 661c0bb051bbc3be
+96 2026d11d400c00a9
+97 29d21e4914fe6eb7
+98 8db246c39552a885
+99 f84f0f7ae9f08597
+100 439be22493e6fef8
+101 8f6f40c9be6a5a33
+102 e828d651afa8e32f
+103 ad11449504380135
+104 cbbf7d2c5b69fb6f
+105 70f9ff4f1f3e116c
+106 75174484922a43ab
+107 3b188031d43cde14
+108 45443f3fedb47b61
+109 90529731c1f09c53
+110 8c9c243118e785f7
+111 453c1a1373868bcf
+112 d3642ad96d747892
+113 6810a3b3af87a31a
+114 3236ffb86457b5b1
+115 96d741cab5ececef
+116 930acabfd9675be0
+117 611e9f536ba2d2d6
+118 3361ac1e5a84b028
+119 23561872e1ac6d2e
+120 75829c5e97a03c58
+121 3293afa684676862
+122 66bf22d74ac3f5dc
+123 e0eb7d5ae08d123b
+124 ad42a013ee572c20
+125 09ee16a2c8d78882
+126 64eca7473f7a3049
+127 a18f7bb9a93bc78c
+128 84197c5463a2a612
+129 d892061e767d1ac2
+130 b06874eb3c5c992f
+131 3729fbb2462caea6
+132 b6d96e6ab7f5d293
+133 d301f5c03f14a5e2
+134 0127cf9b2d05c1b2
+135 1038fbea0533c059
+136 9616de5b5ab3c386
+137 54cdd3e3438c04ac
+138 513d9abc0f74c254
+139 f88420fe21f11a14
+140 e3845d1379f69abb
+141 6ff7f4d2b1dc5540
+142 39aacfe59a7d8150
+143 812c0335da8e904a
+144 1209ea8eaabf4a83
+145 676ff8bc52b33f5f
+146 f6c8d77caf4e4bf9
+147 888deb9c67a3b342
+148 47485c1a2e356f2e
+149 0f81482e82cbc4e7
+150 ffeb2252a78e9e93
+151 9db3a8cfd7ee3c62
+152 89ca6f47abb6ba18
+153 3775e69ff0ea3e8d
+154 8da0fd13a4a156eb
+155 23b7cc5bb4f17c68
+156 d93db2a60924220c
+157 135823d1fb5d1956
+158 83fff14b563d0c11
+159 4b6647d83bc8ca49
+160 ebe4324c70151374
+161 08d9b2867c0302f8
+162 4384d35605d372f5
+163 e67b5e024def2031
+164 be999b8049d055f8
+165 3458bbe1dc54e0fc
+166 091655320cfb07f1
+167 0266a6e0df5c3400
+168 06aa49f0e4229bf2
+169 3736ccc589a850ee
+170 cc3bb8e74333822d
+171 58a873c690c7cb35
+172 6c795cb30264fd34
+173 c576e55d7478bc26
+174 b1af16579df4a77c
+175 73bc52ea4cfee1f5
+176 fcb35c91c03678b5
+177 8aa0eb2d323441dd
+178 6c0097d0c80f8e4a
+179 3f7868b908752e3a
+180 a8947bfe101e94da
+181 d34b26cb2ef5b571
+182 b7f5f8b77a12be71
+183 99095cd2621989bf
+184 c65038c1549d41f9
+185 4044dd5fe11161a9
+186 f11ef3d9e018c27a
+187 a360cf4389896c78
+188 5803d0f7d78a3e14
+189 cda9c716a2c14efc
+190 762b8aebd3a959a0
+191 dfbba2b9def0040a
+192 801e5be60e1070fa
+193 7cae57643e7d8f6a
+194 fffca7ff0bdabaf6
+195 37174feb2d1bd3c7
+196 e969ffdf0e810def
+197 f500e432b5886733
+198 c265a1cbf4e8977b
+199 4989cfe077bb9f4a
+200 01ebf5495c005767
+201 be6ea1ef3fe013be
+202 29c769155bb3029e
+203 6166bbc2878c78d1
+204 66ddac1f0f39673f
+205 b26910ee359a41ae
+206 149f6e40259572ba
+207 9e14b185470c73ef
+208 72baf8e41f301bf3
+209 00904f453ec085c9
+210 b6c83d1b6be71d81
+211 93cfbf781195ce12
+212 6507845797fbd9cb
+213 46e593ab9fc1a3b2
+214 4d243e419b43045b
+215 12e2af4e5587b492
+216 80e11270f8b15b7f
+217 7cf792a6d8eef372
+218 d87d1f3c77cdc8f1
+219 c9d712ecef9a4e27
+220 569ac803e88d18a0
+221 9def230277af0e4f
+222 3ab06b708da1447e
+223 f9a42daab4cb9272
+224 ff942a8bbb350af1
+225 aa1aec16e644b394
+226 ebd95bfb5adc987e
+227 a14e0721122e8e0b
+228 cf42f782c286d005
+229 dce0f83a99562f68
+230 cae12621565ddde3
+231 499617948be7935d
+232 3042253eb36218a8
+233 95a9d70829ee4029
+234 679c903d25897d50
+235 0a288bc8fe90ea4e
+236 15a0e8ca6330bcd1
+237 f8b0f94385d69816
+238 0d41a1d3478cb7ff
+239 c5c95c2b95273e12
+240 89007bd214faba2f
+241 424d59b768b7931d
+242 b505bdcb543bd688
+243 be707dbbce1994cc
+244 72b41bb37b8e1a4f
+245 e46f2e24658abd4d
+246 6f49cbf4869d7b7d
+247 757f443065301c86
+248 fd9235a6c8a61f10
+249 233b843c2ab4600d
+250 2af7045550b10dae
+251 6b414714424edbdd
+252 6c9cc8bf3579095a
+253 0b131ff0d2a72df4
+254 eecfe2f424c7106d
+255 9e387fd32b1ed6b1
+256 500cbfde10860813
+257 54e6e40f87283ad9
+258 9ef177ac5be840c1
+259 5591ac260b975d5a
+260 a879129645bcaa65
+261 77cd53443b7e5a27
+262 9aff30321d9d7ceb
+263 ed9225a133edd966
+264 5ec982815ec85b9f
+265 3d4cd90061b1f751
+266 1d4901f3848a1798
+267 393e0a984a7b2961
+268 f661cb4705936ff3
+269 313632a3f713fafa
+270 e017cbf9fae82c49
+271 fdce8bae4106b777
+272 5af759bfb50f7b6f
+273 7b2a39421a1387c8
+274 9d8bbb38558d1d71
+275 bded3d4ea5cb252f
+276 d297fb5f2d7ba21f
+277 fd30900694b59bd5
+278 3836f24a6b042087
+279 f8888cdadff925e5
+280 856dc26627e2304b
+281 78b285182777cb89
+282 6a7a4786110d4a38
+283 50297c367a422797
+284 c4d05a4b6a12230e
+285 f3be431f7d7bf1e2
+286 5f5810d9c72345ca
+287 8c836123334ebf98
+288 10a0aac5ce9805e9
+289 4269e27488dd758c
+290 45423093e3f7c6aa
+291 1727ffdfb53e028e
+292 1f7c41bb6b27366f
+293 616bd29711c827a4
+294 fca9e533854da6bc
+295 ba7246601c103e3d
+296 575b41d1ce1ac55f
+297 e6cfef3bc3b47adc
+298 21780bfdd0efec92
+299 1015c494309d230e
+300 1e0bf142671875ff
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
diff --git a/goldens/sla.t1 b/goldens/sla.t1
index 6f183dd..411599b 100644
--- a/goldens/sla.t1
+++ b/goldens/sla.t1
@@ -3,245 +3,245 @@ t1 1
 demo sla
 seed 4243
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 240
-1 cb3d2651ee808e42
-2 6216cc74cd6fa085
-3 1353f4c30de9f17e
-4 13e32385c59cd965
-5 3001ec2d7791739c
-6 b76084a0bdab079b
-7 eef84f5815f14942
-8 4f5d65ebda2db4a9
-9 67a80d8961c27010
-10 ab1a22a9102805b0
-11 1c244332f3e761c0
-12 45fa0ecfeba12554
-13 7a737d6a54852d47
-14 e9bd9c0efdf3ab0e
-15 054ac5752c578bae
-16 3327d6f368ac22f5
-17 c1f5823249707373
-18 f99ee5584e51f9e0
-19 7e7125d6d37f57f7
-20 5e1164d21fb07ddc
-21 7cf50a8f504fcd67
-22 bcd37091d3ce0f47
-23 be056af9966c2a68
-24 3314cffe6d6b0473
-25 9ba8b5f4645e155b
-26 c4fc8592f06007ea
-27 4043a3bd9c1ed3c5
-28 dd716288d45409cf
-29 780bfc89226c9adc
-30 39847c7c7bd21749
-31 79fc6c57d8647bb8
-32 5da9fb94857bb553
-33 27bf1daa1e3a56fe
-34 d683b3e8ef402166
-35 ac028bf916697742
-36 5395ae2d0bfe4911
-37 0bde81966e262cda
-38 2035d52a26c32441
-39 46398b85f53393e4
-40 2a2f5159aa5cd2f2
-41 7301cf0177a8fd5b
-42 f9df82c7e9dbcaa8
-43 a98aee4dd25c679d
-44 b5b95e14bad46809
-45 f56be6faca08f87c
-46 c041c3242efbbb90
-47 a4542b4b0ac69762
-48 a03fe1a52c33eee9
-49 20d8e02e9fac59f9
-50 85e7e9d086c339c7
-51 95c9264841529506
-52 10f277c3eb6c34e0
-53 4aa1259ee1581918
-54 af0d001a4244f1c5
-55 839630ab8a307533
-56 734503842aafaa32
-57 23022c25e4c94c09
-58 f0945c3edf14a489
-59 ee987963b8e3e91d
-60 c5b74ddd33a46154
-61 39c9d491a8dbf8e6
-62 f71518dae92e48f6
-63 f40e913354b0a131
-64 5b61f3fee02451ab
-65 64a24851b73cbd29
-66 04db63cf702ef8fa
-67 65d92251fa425015
-68 1e5970c1a3f3be10
-69 723da104d2d9d1bb
-70 04097915cb4057af
-71 b98762c1d5838cbb
-72 2ef01ba495f7fce2
-73 5c61ecb9811485d7
-74 b9b1304f66739ce1
-75 68784d212fecfc10
-76 f3421cf0a5465d12
-77 c3ec1fbd997963f2
-78 b5795ced8142e853
-79 3f646cb30824df1f
-80 cf4589350797a2cf
-81 15d3a4461a96047e
-82 e009929f26c42266
-83 b9e149aecfd64eb4
-84 44c5bb954ae9fe7f
-85 1d4d047b10fc0f3a
-86 33437d233a86d723
-87 00e503afdc4eba3a
-88 95e53c37fb2ac800
-89 725a6b178b98a8f0
-90 ccaeeb99d8a6d5a1
-91 6d1c1e1c45e98f31
-92 925bd17f8dde781b
-93 fe39fdc1ab357f16
-94 298736020a4e4fd2
-95 07b4f4633af6a844
-96 c6001af2cf18a397
-97 593c817c7f9ab3c8
-98 c512696af4f1f31d
-99 9e77bb43148edfe0
-100 3fd547536aa1e122
-101 2c8c4ac5a7f76956
-102 3030c32dfe9cfc57
-103 a7c4d64cee26ce5b
-104 e2c53b53c3694417
-105 c073e560daf9cfb2
-106 35ff6dbb416a144a
-107 cef1887a9a8c951c
-108 e207b0691c5e0a7f
-109 28da299cac52e1de
-110 34bcd0ccb963e0ac
-111 574f9e12ee05b09b
-112 c63dd0bcd006c189
-113 380304f18b24c59b
-114 1b3ca1b335c4edb8
-115 165aaf469ed34935
-116 90619ba053b598d8
-117 6b460361b0e98393
-118 62395fbdb6f6457f
-119 f30d579e0485fb1b
-120 1849a28ce11e0972
-121 6a676d9c2291dfc4
-122 66c83fa0815dfe20
-123 2743387c10a5e39b
-124 ab8938dcd2f32a81
-125 7bc70d0b94635997
-126 df2a0b2e481f8b50
-127 4857768af996e937
-128 1b6a3df8e93aaf9e
-129 98c4a0e5b1d19165
-130 c40d0b41ef557c7d
-131 50f39f2c8736d197
-132 56fea2c829d67b0f
-133 67037b890004db07
-134 250c7c2d831ebc6a
-135 005243c1054d875f
-136 485c7218e42e6bde
-137 3ef48055df97610a
-138 81385d0d92abd35e
-139 f3ca138b70846103
-140 5a2417e78e7f1a55
-141 4809235f1d957cba
-142 c38e658810c6b071
-143 ea4d30e583869129
-144 064cd8d5a7404a39
-145 563c6eb38c2be4ea
-146 c735e03ca2db36a3
-147 6f3ed1de91cc64a9
-148 935b527e23be3943
-149 f2b137d0e1911628
-150 d779ebc9158007ab
-151 3ec9eecc3f3a25dc
-152 09a1e35901ff0795
-153 4d224b572d02813c
-154 eb381b2b58acb44b
-155 d8884d2aeabed9ad
-156 7361a07010ebe034
-157 e827fcfc28bd5236
-158 a70e49729c712ff1
-159 04b22c8bcee4345b
-160 f7d6c97a35ef313f
-161 1c477bf9aaf0f542
-162 f64f381f0592a219
-163 06cabe94c71cf7d4
-164 f5bd61dc7830e592
-165 0b028ff400f46dd9
-166 b5e170d798e4c632
-167 5934f3c2d2f0ef28
-168 3570656e6802e1d9
-169 e9dc3b29e7c2c5ab
-170 6c8e3d418b6afbe1
-171 ec13ff207c0fd69b
-172 e6e2eb5347c920ea
-173 675078b977382674
-174 4620fd4bca9e08d0
-175 ddeb5283a244ca63
-176 debe15120ad93ace
-177 3471b60c8bfcbb08
-178 dd434342c906acfd
-179 50e1605a8cc27597
-180 838ae17f0187c111
-181 d2ce634dd3a3eb25
-182 bd4f614b2e12cc88
-183 a0dbc6a5b6962c5a
-184 1099b80ed3c95eca
-185 c509f4a72ac93325
-186 461458b8bec50a52
-187 76022ae7c3c271e8
-188 16bbe1dbf4cfdb31
-189 4aed12d586dff8c3
-190 0a98316bb4622665
-191 07467f5cd97c3443
-192 38d2aa4733ab8e92
-193 b1a86ae9753bee44
-194 e7b46e4dd44cc1b0
-195 8a42f79576c4069b
-196 15e2f4a61b81c4e2
-197 66195a4a942906dc
-198 f4cd3bd580589c51
-199 ad30d511b5235a33
-200 0e3230ef71c5c765
-201 c340c3ecd5d496c5
-202 def4895c630e9f28
-203 c0b1d308bd2d7e3a
-204 df2dd0829bb3c012
-205 ea6798b7a0937f19
-206 7f10e1d8d31b209a
-207 4cf992a336d61c1c
-208 542e0a9c00579679
-209 d833c1706a2eb7a3
-210 b25d822bbc6c6ea9
-211 e5dd4f5a567f1a7b
-212 e2ee2cb5a60fc326
-213 b074a23904b690d4
-214 ea6bab49d51ef020
-215 c8879e8fa53fe3bf
-216 bca2056ef0ee6082
-217 43bba64a72762578
-218 1b6efedbd926e201
-219 aac7002434bea1ab
-220 5dfd815c3432118d
-221 3db37d9ff66db1c1
-222 bb11393862819750
-223 101e6ed03e6a5c86
-224 d6ae5cec4679e696
-225 36023cc7731d08cd
-226 b62612812ae13a82
-227 b217012ee7e6fa4c
-228 03c3658ff5ee5871
-229 2aed1bdc4bce2043
-230 74e3967eba515e95
-231 aec26c2960c6c763
-232 73dd723ca176a006
-233 f708c921db972b3c
-234 cefc316d40e2a7a8
-235 4c9df774760859b7
-236 1f1cb268a2791f0e
-237 4080fb6e855ce624
-238 3b48f7b1046d9315
-239 0d00fabf47c78e8f
-240 7c856f6ba0eaed1f
+1 584afcf609042a56
+2 09b36e002f204ee5
+3 57177be29b74cb6a
+4 4bed69778e553435
+5 4d3be62f85f15188
+6 3a55a7959f74302b
+7 379a94499503efde
+8 caa193cdfa0df049
+9 534880e5201e572c
+10 39037243faf028b0
+11 6a5f77a181c5b914
+12 a03f555855de0324
+13 f0e423740b0a8fab
+14 ea9e0fa6a69c903e
+15 fc553806468197a2
+16 7e16418c647d3135
+17 2cf092e4cf0b9827
+18 7808b04a5fd91820
+19 c669efbd211c6493
+20 3a34c07284eecf8c
+21 2612ac0feba80923
+22 c2de8a3980d5a517
+23 19ae0ce4a99fe21c
+24 67d1a52384432773
+25 d070f4b55fcb50ef
+26 9e41b083117bc90a
+27 32fe78f0cabbd4f1
+28 eddb012c1ec65abf
+29 bf09e6cf6ce3a098
+30 756ce7738e9df419
+31 8c1e9542fc803b4c
+32 3521d94d5599f073
+33 94460157b65f72fa
+34 cbde7fef1379a206
+35 f5c18e35e76d4ee6
+36 ae5eb8998aab5221
+37 412a69c61de9584e
+38 5189eca1ee110f91
+39 b0cd1ecaf22c6d30
+40 409b036b34e49f12
+41 07b2b7f63c0ee407
+42 7c3f2676d1e320e8
+43 7fa9fd59a0b47631
+44 501f3abde75d95b9
+45 eaaa5288aff44a60
+46 38fb089c7b0eb720
+47 1a282f59232aa1ce
+48 ecfcb1b2a5cc6469
+49 0df7efe7e85260e5
+50 5ac7259ebda3adc7
+51 07b1d2cb24755712
+52 793436d46a040c50
+53 abfa01c1d479ac34
+54 0f2673fe7fde13d5
+55 c5d7522bdc7cc45f
+56 3366bd69d7f64672
+57 d4701f9cda77b035
+58 eb5af35b17561369
+59 530571ff840c54d1
+60 752140a5e8d15c04
+61 639954c491a2a642
+62 365e9781d52540c6
+63 25bb588002867c9d
+64 d96ae4c2e025bf4b
+65 d81337e2a600cff5
+66 f369ac951ed6759a
+67 adc528ae5421d189
+68 7e51bf6b0a7db980
+69 c0c61d2d05f2b7ff
+70 d80361c7dc67c31f
+71 e9c6cf506e4cd9e7
+72 b69d79acd7df9942
+73 74c7343027730443
+74 5b4a8f80a9b1bbe1
+75 d9dbf2847e389d7c
+76 5a5aaf83ac2cc562
+77 b4553b042b0b6e9e
+78 eb92f185e431f963
+79 16127b58451efe8b
+80 8b53d7c5d4c7a30f
+81 a83d2bd35a9c28da
+82 5b3e211ba9c8b9a6
+83 992a5f26883ace38
+84 7a8c890e29c2522f
+85 26d0b1d22d954fae
+86 c065ba2494b7eef3
+87 51f589d73c0db506
+88 801debbf5dbc5500
+89 cc16fd3a07b59d7c
+90 a0160e52ff493fc1
+91 e1a45021a7fb86f5
+92 c21f7581fd7e144b
+93 5ea5056330f19f6a
+94 d3adead5c2055d42
+95 3eb86c1edc88d930
+96 92b52d44f03a51f7
+97 2d0662bc980531f4
+98 a850b45ac5f02b3d
+99 26813824f030042c
+100 08161adb7f28f132
+101 7ef870759b883da2
+102 68df87d06b99cbe7
+103 5ec795920ac8d227
+104 fa3d4086bfa201f7
+105 4b4bf6ab9cebe326
+106 da741bd21e47130a
+107 be745e6277f33968
+108 c731de0cf8ddbf0f
+109 bf9145b2088cc232
+110 c498af7c68491fbc
+111 699e8813f96a3867
+112 c74a70569ea71a09
+113 039534e89716b5f7
+114 edfb5064e30e05b8
+115 a95e2ecec1049ed9
+116 a842e95f9cf80468
+117 32b5c14929a14747
+118 1a2cb9c450532eef
+119 fba69fd2ebf8cb07
+120 87eaed191e7371b2
+121 dc5eccd530d95980
+122 45a1d880ca985c80
+123 5eae7253beb3afe7
+124 349287f32e0854f1
+125 0d7800c516ac10a3
+126 0b4cddad067736a0
+127 4b9e04256e849ffb
+128 d0bfc14476730ffe
+129 465f5521e66b6949
+130 19ef85f7d557dddd
+131 0cd0df14016bd29b
+132 e78688d3795ac1ff
+133 42cc227aeed21b0b
+134 ae8bed6759266afa
+135 8d97affd047671bb
+136 652f6675f59c517e
+137 f9f4cd0505008a46
+138 e7043d0e0318205e
+139 4fd1b0f84e2be06f
+140 25b1308f662c2185
+141 5a9f0289bf6e512e
+142 9ce4cb2830365501
+143 c66fed148c5a5c05
+144 c6c16660333552f9
+145 04974c8df398621e
+146 e75f40263dc826e3
+147 4da5c1c59a57afb5
+148 9d27c078b08bf773
+149 c0f03c17134d07fc
+150 32e9fd96862ac2db
+151 f62e1034c9be2300
+152 209960170f399a95
+153 14bf4467cba5b860
+154 78c8e3009d54fb6b
+155 2cee44152bb603a1
+156 a03bfd31dc672784
+157 b2e9e0303e63c722
+158 5994ceb993ebc621
+159 cff9f8aa0382c2b7
+160 d85989ffb9baf9df
+161 a1b9a65cf3af2246
+162 66204dc45b00b179
+163 5f3ccc2597460a98
+164 596cbabc6662de42
+165 1da12c430848c095
+166 b38a6439bfd12e42
+167 02f069d81e8add24
+168 85c00e66fa7dd139
+169 fa293a9c74fb735f
+170 8ef4ee135fc0d321
+171 9069349a075324df
+172 5646b00831f731ba
+173 6b984b881ac58470
+174 1253134f03bc7360
+175 c9d8b5a9ddfbb927
+176 8594548ee5e18a4e
+177 5aaa0e7d035ad51c
+178 84f02d7ec85ec4fd
+179 5df1c34c4a898e83
+180 fbcbf01fa25121c1
+181 ae428213d4c320b1
+182 762f28789471dbf8
+183 0e146ca37340dcbe
+184 8cf11ec28008880a
+185 9da686ef63288da9
+186 f41f88eeb7e67672
+187 f9d1905c9fe87954
+188 7966f9bbb29f7401
+189 3e0cc59b3a8e5237
+190 6cedfc3827d0a2d5
+191 4eba7c12e5d5615f
+192 129cb55a6344b5f2
+193 ccbc3ba33302f058
+194 013ffa219eef15d0
+195 a41fd9239aa39b7f
+196 6262f85a585b02b2
+197 19ef9d7d0b698198
+198 c6bff000f153ea21
+199 7a6fbd5259f9f4d7
+200 60017df3304778c5
+201 c4bbe6df965dd459
+202 6bc9a08bae433428
+203 b9e3151ff39bc546
+204 eb9f4bb5b9dd4502
+205 3c8a2a1ec3ba7935
+206 64c67608b583704a
+207 40c09f99a3071178
+208 e2b41b445f7939b9
+209 fd4b2796876c0d37
+210 d86b2d91224fa3e9
+211 80cccd98b87592df
+212 cb91c486b5280d16
+213 bd1da3c859f66860
+214 c7a052dc0bfaa9d0
+215 a8acdc8d3ff355a3
+216 f8f9500a0d091982
+217 22a8495156c92bec
+218 341417d9bc2249a1
+219 ef9dc0d8c8c86027
+220 4951104440653c3d
+221 a7225fe804db2b7d
+222 8c7503b133e04540
+223 2394779d4708bfda
+224 35659a2b9fb32e36
+225 cade61351b9f5fc1
+226 eb66362bbbd60422
+227 07ae6476a3937348
+228 61551f9708392a21
+229 339f4e643ad56347
+230 7d3eee03796ebf25
+231 0d7b49dadd1c8fff
+232 f6f4fbf0cd8bb966
+233 ae6fd3e7faebe3b0
+234 a4b8d795c685e0e8
+235 e7d00ddad42c035b
+236 5fbdd08ac27f5f9e
+237 ec5143a650ad89a0
+238 4095cf01996522e5
+239 1be7794a92a35403
+240 327e6f6adff95d9f
diff --git a/goldens/qos_contention.t1 b/goldens/qos_contention.t1
index 02a3963..b94e28f 100644
--- a/goldens/qos_contention.t1
+++ b/goldens/qos_contention.t1
@@ -3,245 +3,245 @@ t1 1
 demo qos_contention
 seed 4242
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 240
-1 ca77980ad92827e8
-2 25811c658ed571fb
-3 c1e6ec5dc1745348
-4 8ce07260a67cad7f
-5 60f9f3cefd5bc19a
-6 9994989e79f76f79
-7 f065264a0487d4c4
-8 738784115d1c22ab
-9 87cdfce1dcf74fb6
-10 b035dab972991366
-11 49e3a46ee4881afe
-12 d7037f156e104146
-13 da211cff33312c11
-14 d1558a30aabc4fcc
-15 9b3dc21f94724394
-16 d53e99f8fda65837
-17 91f042bdb74ad1ed
-18 4969341c07215f82
-19 c45253a9018a87e1
-20 01d9e125aa299516
-21 e6d4c55ef5711949
-22 b69bc72a81bdaea5
-23 d7f750a7d0e72c6a
-24 561c3da0c68d1da1
-25 df4f1a26d3a8c9e1
-26 300a75604581652c
-27 7b3b69e70d9e908b
-28 0bb2b068f7d77e45
-29 7c1be1bd4f1ac3ce
-30 06ef091693cfd763
-31 68ceb93db65a0d5a
-32 7b32868d1a9bad91
-33 e84d24825c7050dc
-34 b670c0b5cc69a7e0
-35 2d15f29b7399cd7c
-36 c8de9ad248a0f087
-37 dda2044065234a54
-38 7a2dda6e18b2c853
-39 30a92fd5afe5bc92
-40 27bd88f15a115c48
-41 4136e2a1f3ec141d
-42 eb4ea68be9af2bda
-43 8a7abf5217fbd5c3
-44 ef62f0d693ce4d8b
-45 de04c842539cb146
-46 75606ffba4e15536
-47 c51271117ea30ea0
-48 520a6023e5240173
-49 e81da8766ac401c3
-50 571fe0a54ceefc11
-51 4d9993a8ca35cd94
-52 807374a89ade0c4e
-53 4649488e82d1cc92
-54 016eac7b331d53d7
-55 2431953768748d5d
-56 92a56e902d5dd16c
-57 3b8c860dffdefa53
-58 2ea199066a19d347
-59 70ea559654f930eb
-60 2c571c8e536b61f6
-61 e251a248ece94f7c
-62 a146425c28b97fc8
-63 db84bfd76aa5c72f
-64 d66356149d6c1b31
-65 159a6fdd06bab6cb
-66 46f5235a1d789e3c
-67 1e78fd67f5f66e23
-68 15fe9c89cc750afe
-69 c7f9d848bec1a291
-70 63ee6bf140f83f09
-71 1095c6eed9ad4795
-72 53b604d4391f5280
-73 6c43fa068eff9559
-74 61e9f694dd7043db
-75 f4ba46528d6bcf8e
-76 35b05dd0602d2de0
-77 ecaca73dda97309c
-78 1da0d3d07ea61fcd
-79 ca8b95b72caa67c1
-80 2fc664f27682d85d
-81 4e5b83feca5d116c
-82 ff60b6fd08732ad0
-83 42dca32d8d199196
-84 5f06744f6c934d5d
-85 d1487db099109bd8
-86 2949658d3721ad09
-87 629571ee2e975dd4
-88 5e86f43ed8803f62
-89 f08f3d5bb7b25c6e
-90 c15660996c2b6a4f
-91 5090ff29b8e1080f
-92 52efd265247bea41
-93 418d2ab9275660fc
-94 d69064987dd13024
-95 13dca74b36584f3e
-96 8a8a04aaf748f9ed
-97 e5030ffeccf348ca
-98 5c04e00c847cfdb7
-99 acdd527f6a4abdc6
-100 50c08cf6e216ca40
-101 2cf7aab87e67b7a8
-102 9e308fb8b0b8bc01
-103 a1b3a4c49f967b4d
-104 f00e7115c0d7efa5
-105 5179dd348c089da0
-106 3242b4c4a4e9e254
-107 373d5d18bc447b9e
-108 246cda2c31f8471d
-109 7259503cdfa51b34
-110 e49e4af9e4200012
-111 1015eb46a7a9c655
-112 d32cc910cfe2a553
-113 887f6d4ba8709d69
-114 53cd2084018ec64e
-115 4b9130182580d573
-116 923d98a68cc988c6
-117 83a852535aecf1a1
-118 c299894ed8742aa1
-119 afda36ae17345eb5
-120 124bf50e86a7c5b0
-121 2220795995e8341e
-122 26388c0c2629246e
-123 119942edab0f8945
-124 cacf57f78a51b243
-125 b1404394f617ed15
-126 69a0ec2e289e75a6
-127 26593a315032efe9
-128 76ad6d60167b2290
-129 298f5af169b7ef87
-130 1a33088b571eef03
-131 28711e3e885b69f7
-132 2fe2445e272bacf2
-133 4c4008b4bd7027d8
-134 2ddde12c27ac83be
-135 4cdb22705f5cacd5
-136 98ce61e66f7a97ab
-137 5fcb164d4f77529a
-138 6d7668a8f48f753b
-139 79678c7d8bf6dca8
-140 67692574f4f36932
-141 a150bce181e69578
-142 05679978a9804ea8
-143 a10b0fee2254531c
-144 55d3bb0816c9dc1f
-145 b996153a2947c53e
-146 621104cabeb2523c
-147 7bdd4a3685b1ed26
-148 49027d9f5c281584
-149 027adde288b68777
-150 2142dc35f954dad4
-151 bca1a5f5acf57682
-152 a53f50af03d45067
-153 27637fe2155778df
-154 33bb355e9b762cb7
-155 b1b9e6cf0a6cd198
-156 c5c4e37e397a026b
-157 92c49f5844f304d4
-158 a742d36d9b3b6b56
-159 bf5c0f213963dac4
-160 eb24093dfaf0f79e
-161 0ff1b3cb3238c7f6
-162 a37437441c0bd703
-163 d565d5661bc8b56f
-164 10880e47f8655867
-165 73bbce054a7343e3
-166 21b95e8de3981897
-167 546962c5781b77a7
-168 349c4b15cfdd4236
-169 8134a66995bc12b1
-170 90ecaa62f5832a1c
-171 398a793bffe9cd02
-172 84f5704f2ad48768
-173 9e4c3a32d35d850f
-174 881456f238c0fef0
-175 c668eced4cd31f2a
-176 1275043eaec1dd47
-177 d64b662818c53eef
-178 475385c929d4ea43
-179 c0a5dadeba483593
-180 b2d7449bd899388a
-181 d851fdb0c732af4c
-182 695762b3e9a9f274
-183 c88834b691e4b59a
-184 7fa46e8de6278628
-185 4d4ef135e5659e50
-186 eb170f2514271765
-187 0cdf5886cfaffc63
-188 8259f2684fb99a12
-189 3991fe4eb90513e8
-190 8ab022adafeec760
-191 0a5942486f58f2a2
-192 813b90ecb30ab1fd
-193 a6fb58c23d331b46
-194 21c77fe709e2721c
-195 b57b90d06cbcf57a
-196 bcd4a0edc999dac8
-197 5ba56de7bb3441c0
-198 848af021cdcc82b1
-199 5f066ce1568c37e9
-200 caa596cba1f51e04
-201 71ae6f2481a74952
-202 7359ba2ce017e0ee
-203 5f64114e52df9344
-204 3c68761c4ecc83c7
-205 6b61b02223c4d284
-206 9f4300768079cc41
-207 ef81f2233163da01
-208 9ea12bf34085c53b
-209 82839a9655d382dd
-210 8a14ac61496b770e
-211 d460079c13b6e3e2
-212 bf72790b17ae70f0
-213 4d9de46ef351ddc2
-214 c1d0f6cafc25210e
-215 2cc0781cbd0dd8a4
-216 34aebae9e78cd107
-217 6721113d2e04b03c
-218 d79f15f6a68ddf75
-219 20ae555a1a805c25
-220 84dfe7d268c2e917
-221 24ea2bb4356bb759
-222 d7586c634e64995e
-223 0f6cf6fb5d586450
-224 d5a06e137acf2f5c
-225 cbf546ae84b2d626
-226 22108ae7f9ea63de
-227 bc1815885c2d67ec
-228 afde4e321dc971b7
-229 d88f61bc08bcad2d
-230 f2fe565bff5beb44
-231 fa114e64b87c8c26
-232 d899949d1effb8cc
-233 e9de39465ae123f8
-234 34ba7d1f876f37c1
-235 e99a022198dae9ae
-236 2e864ff4cc2d3494
-237 88b098cdd51dfb0a
-238 9013ffedb513952e
-239 380a3a235fdeabe8
-240 32d5654b01416795
+1 f1cde257a0e4c638
+2 b2ab7a1f19157fef
+3 950438480d50d488
+4 072f52725ec3c94b
+5 3d7a968db8b1107a
+6 74a866850fcfebf5
+7 c6154beba3044f94
+8 18b81f5c5338fa77
+9 caff2e31128eb7e6
+10 cac6d125b5b83b42
+11 534d536e5e6bb6be
+12 e479f572791e72da
+13 6e9612dbe070c331
+14 e4fecf467066f6f8
+15 738a7595866c1004
+16 e7af6e816891d153
+17 d1baaf38a9a815fd
+18 7494994955506d4e
+19 ed8ea357dbcf5181
+20 2b1dfa96e05dc732
+21 5bea0414a8c2e649
+22 1a744d3056681b39
+23 ef1915efae5401da
+24 d34f1ff8b354a8fd
+25 e0c5e19fcdff6791
+26 3281d93d7d0b3f98
+27 fa1b85e5a315b02b
+28 2926b3769ff794a9
+29 df8ccf8c8687688e
+30 44ceb02594119b8f
+31 8481322fa433274a
+32 323191a16cb706e5
+33 d93b7dd58c63b24c
+34 89d872c38c1ea8fc
+35 f76c989d72c831fc
+36 d288f073a8849083
+37 9c3a0084ece31ab4
+38 c35aeb18bc7546bf
+39 a52d086e226a67a2
+40 8576c68540ba8a3c
+41 14d0cb8ef7fd4a4d
+42 1de557d8eff670de
+43 1f8dbbd708acd0c3
+44 2f29145db04b58cf
+45 08ece3e34bc9a4e6
+46 883474c8bf786202
+47 c122af74ea8b4770
+48 b0c7df0b91832627
+49 5c8179ab020c7933
+50 b5b455b73b0febed
+51 3e8a177f9a5f0974
+52 35d284901b8d9492
+53 ccf68345805d4c52
+54 8617a289f2e2e953
+55 73060d7cba8538cd
+56 497f5ff533da4690
+57 f493deb6901d6963
+58 6fa3be9247443d13
+59 57b8c242f4a5764b
+60 651cd1152e035572
+61 44e9bba8bac6577c
+62 4a330f486d055894
+63 74dd00f0aec4749f
+64 f9facfb4bbb484d5
+65 aca8707064a55ddb
+66 d66bb1a960b44130
+67 456a645c262a02e3
+68 a1e412198e8babc2
+69 ec66e7edb2f8c471
+70 aea6d37b388d45a5
+71 d3c8587a1c912c25
+72 07fb8d8671d9dad4
+73 88b4c6537658eb29
+74 cf3ecfc898d62b77
+75 2bb364f4c000384e
+76 4a1d3c01d1840744
+77 a8cd49bc58e75a7c
+78 7c3f2d69a69b2c49
+79 ce7cc1e53b7e7591
+80 252b45a59b11a3b1
+81 a61f98b18fefec1c
+82 40faed62467742cc
+83 9364bdc45dafed36
+84 407b6887a32d2609
+85 89a7a46046ed72d8
+86 ac3b8bf8072845a5
+87 d52a65dae1792884
+88 69a08b96995b0656
+89 9f79212eaecb8d3e
+90 631e1a380c32dc03
+91 3fc520817a15a46f
+92 3ee59d2ec61b7ba5
+93 f07988f7b732f9bc
+94 ed052d01fa258760
+95 2715bdfd672f692e
+96 f666396fbbd0d311
+97 c48d2bedf6c4b8fa
+98 978b4770ddb96b83
+99 9089656aed33d946
+100 6598281132a64614
+101 ad8301ae6ff76708
+102 44f7e9c787258b5d
+103 3348809136b9d3bd
+104 b945ec98b5e5bcf1
+105 4ff6a8f6b040e5b0
+106 239dc996cedaf7d8
+107 6182350b1066969e
+108 ec6918aaa14e2a41
+109 61b570907e225954
+110 b36f554af59f78ee
+111 0664af7440baa385
+112 c115ea1199003397
+113 95ccfcca7647f859
+114 9dedacf867aa7612
+115 2b6426de38d482d3
+116 dc3c83298cb0c2ea
+117 1af2f67e63ebcce1
+118 bad9a45a9b01405d
+119 c3a0f96677e65605
+120 59f301a7b2befa24
+121 2d1b69911adaedee
+122 e3fa641f8399e7fa
+123 0c72ecc797216765
+124 1bc82cdc5bdb4337
+125 542415d3e385e115
+126 d3e1ff7cc4ab8642
+127 424d835096bee3f9
+128 9350b4cb102d7e5c
+129 487b51e34fc12bb7
+130 5ab6058e82028ea7
+131 055aa0857d1b69b7
+132 101177e74bff0b06
+133 39aa5c61b7421e78
+134 403d0887e9e5da7a
+135 3e56d2585bc66c45
+136 05455a88f1caed4f
+137 49458fd29826a40a
+138 0881efb0906b0d4f
+139 adc23cb8630a7d68
+140 68f2f4598900cc26
+141 d3be9b49cf6a0a18
+142 c0604c1af90b75b4
+143 1e8f3a033c82186c
+144 584a11084c70d5fb
+145 feef2bcaa1792a8e
+146 53579eb08834e120
+147 b9ca65d17810ddc6
+148 8fbad11299f52720
+149 734d77622e403877
+150 890686d155793058
+151 25efb59ae3081cb2
+152 81f1d0bcb4c712d3
+153 2d181dd7c937b7ef
+154 52f43be162d9871b
+155 3f4d2912ad6715f8
+156 38a3bc50df6b98ff
+157 2f0ddf9f4274d894
+158 a44f3f4c6ae28402
+159 682bc3d745582054
+160 f241197be94b5592
+161 b1c824bd842f66e6
+162 e986a1bbc118f067
+163 eeef01b1e66b66ef
+164 1b55faf4daa557ab
+165 db1be278e04aee43
+166 75e8c5718ba83c03
+167 2c464c70b1a0bd97
+168 b61acd3449814cda
+169 385fbd002173d0c1
+170 76b81aabfbf1f9d0
+171 d856c3520cb1d202
+172 a41bc999efb64f04
+173 7c9dbf6c75d032af
+174 05d6b4e5ec227ae4
+175 8f245851486a063a
+176 98c56b827d3b8493
+177 5cc35514512f6aff
+178 069d8a5f46e6eba7
+179 f6563abdd88c4433
+180 fac97e27e374477e
+181 9b208fed915b950c
+182 d56ab3f9775a4038
+183 b89f67db4a509c2a
+184 debaf16b78ead874
+185 5a1d5b180aa8cf80
+186 b610e61fcffd9ad1
+187 a2b39f1bcfa761c3
+188 2c80def5e004af3e
+189 dd024df53f2ca3e8
+190 3da6e5c617ae73e4
+191 639525f200016952
+192 2c2a747de5b4d029
+193 4e2c22b7c260dd16
+194 0b2df99bb5e72fe0
+195 3de1d840d094343a
+196 2a241fab6f3fdb24
+197 cfb0a366a6f15760
+198 385e1cac8e483b75
+199 e82c6d6218084759
+200 db9e1cf4da41eb20
+201 331700b6c4a7e382
+202 eefa72903d1a2872
+203 1c2176b84c576b04
+204 0a34efecbbeccefb
+205 53b7bdad4c6ef5e4
+206 a1309c9acf2c9fad
+207 dd3c0325ac38b311
+208 d35af1c9054be29f
+209 ec045b823611d7cd
+210 9e599e0f21b60062
+211 d697d367f36e6742
+212 828ed22b199d8b8c
+213 55648244680db2c2
+214 a2961d99f3ceee82
+215 0d84806128c66e54
+216 2bdae4b4dfff90e3
+217 a0182ab8db6b246c
+218 7c57c14b8cc27899
+219 6e5a9968510a33c5
+220 dd2afb0d7ce454c3
+221 1e6b4f0dec846299
+222 a3062e9b1f6259a2
+223 ab3929f465e422e0
+224 2938650c8c1ff730
+225 01826d470e0d4f36
+226 47b3e9aed7a708da
+227 33f153880ab7796c
+228 1e230d8de5ae7293
+229 b1a112a3ee11da8d
+230 671ea0148d706818
+231 aec472d0fd1229d6
+232 21bf2f55d6b232b8
+233 39df9b17a0dc3dc8
+234 8c624841c061532d
+235 092c21e2e33b8aae
+236 b79403e5b66a9bc0
+237 f09bc249c8b4e92a
+238 01376301330dbc42
+239 0f2256428f85a058
+240 370b2feb6fa058d1

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
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
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
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.11-terminal-types/r3/lens-out/architecture-g2.json
using your file-writing tool, then stop. (Your source value is: architecture)
