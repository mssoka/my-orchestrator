You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. The repository checkout at the reviewed state is at:
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.11-terminal-types-r4
(all verification reads happen there; treat it as the source of truth).

Chunk orientation: This chunk contains re-blessed .t1 goldens (qos_emphasis, qos_auto, sla, qos_contention, demolish_node, router_tiers, router_ceiling, place), whole.

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
diff --git a/goldens/demolish_node.t1 b/goldens/demolish_node.t1
index cd06da2..99569eb 100644
--- a/goldens/demolish_node.t1
+++ b/goldens/demolish_node.t1
@@ -3,105 +3,105 @@ t1 1
 demo demolish_node
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 100
-1 2dcf8812220aae53
-2 d31598a648c7e9bc
-3 0cc09943b127b165
-4 71191d82346a384e
-5 c966cde9455db1e7
-6 061265e7bb8a3f00
-7 c7268c20a1e07ca9
-8 0e1707a8c6a2bec2
-9 4384bb4032802e3e
-10 04999d50233f5ef3
-11 f71fce1891452e11
-12 8198bb1909552190
-13 37e6954c30a8af1f
-14 6b0005a4d581afd6
-15 4bfac22263c5b665
-16 3be25ad31791be24
-17 c086df5e1b474f03
-18 e4cda604ad45fdca
-19 67dd45b8eaa5ae69
-20 a9f02c6a67e48f0d
-21 923f418e56f0ec97
-22 8da6f6f061b767e5
-23 bd955c5bf14b4e76
-24 dafa07c69032ddc4
-25 5984b7a29d4248af
-26 a0683eb196e09e07
-27 a3d795b7130d3ad2
-28 0e655006ade3b9f0
-29 00cd629c9a6aff87
-30 14dea7ef72180b52
-31 2a56d68a8b838979
-32 1897e0180639a3ec
-33 7cb32e53f691acb3
-34 41dfd8609ac4f19e
-35 5c549518d4329db5
-36 35bde74ac13dd7f8
-37 dbbaed744281a02f
-38 6e801e17e83b64fa
-39 3264ef2c07509dc1
-40 d8431348337fe494
-41 76af9ace2715d3f1
-42 3577fe6126344328
-43 c6a09d106b9c6d3b
-44 17330aaa6d548f3a
-45 c36e0f3106896a2d
-46 7fe861d79fd08444
-47 71151399cf860d27
-48 27a291402bebceb6
-49 e2655dcf8ba3fbb9
-50 3d09f1f2e6258770
-51 d0684f2dae6ab603
-52 971be25071005262
-53 ba930eca0127f055
-54 7786f2821e77e3ac
-55 fdf612d67ad7c94f
-56 bd24cdda37545e3e
-57 a4767a0fd8114c21
-58 fb9f172211140c98
-59 7982ebde227eb16b
-60 f78a0cc8fb5094ea
-61 8c9b0b33232e331d
-62 35766de48479abf4
-63 46160f6f430d9dd7
-64 0561b42d0d1ba1e6
-65 3d7a11c1a884aba9
-66 0279f7e5aa6e07e0
-67 650369fccd348f73
-68 a82c689504d7cfd2
-69 485a261a2c9601c5
-70 c5f27e38a7d86edc
-71 f1e271de8c4fe3bf
-72 25aa0c8fe37d2e6e
-73 ecb79847e69ab351
-74 f7d8e03bd01cc408
-75 ef939dd8d1e8cf9b
-76 7d54f1d9e4c60b9a
-77 721a1e46b73a728d
-78 c5683856cf3206a4
-79 3c70bbdc33191607
-80 6bfb90ed7da13c96
-81 6d84dfdcfaecab19
-82 fbed8970948878d0
-83 6194d36ec2da4f63
-84 1ffcf20e3867a6c2
-85 af06af673b3756b5
-86 dd6d516ded42d48c
-87 c690cf5721b779af
-88 3c69dc35fa8ba69e
-89 2de3cf7f4839da01
-90 69f2839f37a41278
-91 467bb2f7bfa6dacb
-92 f1be175c6475c44a
-93 fe2b9f3354aba27d
-94 abe2e5db03558154
-95 3be25035c9da1937
-96 745a3d938f946f46
-97 bf80a200ad86b789
-98 88bcd46d2b2f0740
-99 f86c1a0585923fd3
-100 3bb57f55348748b2
+1 e667b2e995c00f53
+2 9823165cf534cb08
+3 5f6345a9c48d0a55
+4 b75737805e68b51a
+5 c5ae71335fd73f97
+6 1f1543798365651c
+7 e6fe3b0402c42a69
+8 88cfd177e919943e
+9 c91c7d0d261b465e
+10 5ade3b260f2f755f
+11 b166b519e057c961
+12 f182b607ffee5c3c
+13 996f00d126f4d1af
+14 9584a3539c09bb52
+15 5c57a6b654307fc5
+16 f4d49599ed62d000
+17 a686d6aff67c79a3
+18 04a32d99150118d6
+19 f87d5b3e2e5f37b9
+20 a135747abbef55b1
+21 efb531928401d547
+22 c03e0858c6e06f49
+23 1d7405c9418ad456
+24 1a8a6f69c312b608
+25 12a06266364fb52f
+26 003c25cd763e4113
+27 ecf8d634e30e36e2
+28 d85a2684dc6333d4
+29 04cf7b1597c10117
+30 c319df56dbd4f0f6
+31 a42b07f4f5bc1879
+32 3d9beb82ef78fba0
+33 b36d9391654cbaf3
+34 f46a94150141c6b2
+35 ba6382fdf99e5805
+36 b30eb74998ea271c
+37 2f76ee14c86f117f
+38 b54ecfbf97d8e57e
+39 f81bebf17dde51c1
+40 ba29b9a483b6b188
+41 195d106d91e5dd51
+42 b00ba08088f556dc
+43 0eb699dacab5f4eb
+44 bed87c8f060b2cde
+45 85118f91c3ec675d
+46 9d5b9eba79ad5bc8
+47 36059696050edfc7
+48 c8ffb6a963cce3ca
+49 d8265d77a5b67899
+50 495d78f06a273784
+51 5672b864b995bcb3
+52 3ab7b9a24ab6ee06
+53 de930b9d4778ea05
+54 b622f77e15578df0
+55 83007e5ef80e7f6f
+56 43bd451b6a1c2a52
+57 d2989fc258d141e1
+58 186f449a970652ec
+59 5d4269675696337b
+60 6e68e07fa257d8ee
+61 d98403a3cedb51ad
+62 5bf2e23fbefac058
+63 d04edf7ad04bb597
+64 3e41ebd4e5a461da
+65 e00d8179a4a756a9
+66 6aa24296d6489c14
+67 6f0c89b3d4dca043
+68 9b80de1f37892216
+69 6288d64218926f15
+70 b343df33fc2fd600
+71 55eb580d01848f7f
+72 72591affc1f34d22
+73 ee1d6581c8d8e271
+74 db6a5702a8cdc4fc
+75 e36695ceec9b850b
+76 4058acd7d8f59b7e
+77 5baf320f6d4b6efd
+78 bfecf344f2543968
+79 2d34ccb42a584267
+80 cb0afeb8dbec126a
+81 75b0bc93ec66c939
+82 410034747172eea4
+83 2c9ea9a2de228ed3
+84 c4a4771658b61326
+85 7f8a3765e39c93a5
+86 6ae1b9c4d24f8490
+87 c6fb5b72234dd90f
+88 0e204d7d7ef5d2f2
+89 36dbc0d9eede5a81
+90 6c3a9714b363708c
+91 1474c2f0fe632b9b
+92 dee5ab90b3acb60e
+93 4a85f79b9944dc4d
+94 d4a53ff2f8fe84f8
+95 a9d3671581777a37
+96 4fc75955cccc277a
+97 5cb17797a97317c9
+98 b13d90cc63abd934
+99 95aa4e1c6935bf63
+100 ca63cec3cedd7336
diff --git a/goldens/audio_throttle.t1 b/goldens/audio_throttle.t1
index 629bd63..e24530a 100644
--- a/goldens/audio_throttle.t1
+++ b/goldens/audio_throttle.t1
@@ -3,85 +3,85 @@ t1 1
 demo audio_throttle
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 80
-1 8409ccca80693a0b
-2 f0d8c37ecc1bb89e
-3 958141b0e3f25bb0
-4 8dd483041f600d3c
-5 0f3dda6a84fa84f8
-6 425fe4246d4c9722
-7 be5ff1fc1eb6080b
-8 35f91099281ab462
-9 c0f683b7a5341175
-10 d09bd224f56957b3
-11 a772043a9ff09e1a
-12 7b4e3add7f951adb
-13 1dccf845770b45c6
-14 f7707d7d0b0a69ed
-15 980c8fa775d80916
-16 41295814b8d968c6
-17 fc12e8fb6df5ff29
-18 c5e70334ee1f0250
-19 fdee89f16182db0c
-20 2825fb3e72a1a250
-21 65ca1e4e25bfc4b7
-22 8a84bc3151593d3a
-23 972b88524fe8f39b
-24 0c01966545088cdf
-25 155d7ac2673db331
-26 55881c106774e985
-27 69c2d74dde4f63d6
-28 55f64b2b44f4e97a
-29 fde4bb8ab21df5f6
-30 377098b3e941969e
-31 1d82cf3e750d437e
-32 f49196b3c2937d43
-33 af47de04cd337545
-34 d17c70f45990ced7
-35 55497d0d8077cf61
-36 57c1ca56ee2431bd
-37 6ea40ab17ff3457e
-38 59e81789a9d2c69b
-39 b57ba27e41d270df
-40 368d1c2e16b649de
-41 5743cc062a12d665
-42 a604f99e94d9d3a9
-43 c5caa3a7e0fbee85
-44 2d7ea5b20c6784ee
-45 c82547293273deea
-46 fc920762ddb01965
-47 66270d21f982cf1c
-48 ef418d347176a932
-49 b239234eb6aa9b7e
-50 9241c886431dc035
-51 3c578bd4c45e061e
-52 f10f3b7fdaf80205
-53 ac866e61b3282860
-54 383a0a77c2f45f01
-55 f71284ea30efacd5
-56 26908a74412a4ccc
-57 b924dbecbbad93c9
-58 2dfbca6b0cc647c3
-59 a1df18156b6b7a24
-60 ba6bc7d118dc1a4c
-61 087a551a1c692fdd
-62 a823168ece2a7969
-63 6275bac088803771
-64 85726535d6e9b029
-65 0787526885b5829b
-66 09626f24d6436159
-67 8d2887266c7603c6
-68 30d506f5652439ac
-69 22269adc68db45a5
-70 132f6d2183ac00a2
-71 0a61695c884b9454
-72 1b942d34c18daa35
-73 7976bf47eaf0345c
-74 b6f2225c9494b53d
-75 8fcc87bb773bd419
-76 93f2ad854f5d46f4
-77 6f7a0b12c04ef71f
-78 0ee15b04c7693c7b
-79 b920bf38c02a5bc7
-80 bc165fb77e12f08d
+1 85992034b1fcf1eb
+2 57055701b46a212e
+3 3e387ec0a0f126c4
+4 fc772ac2a43783e0
+5 4aef876f812d2c58
+6 072ae10c76a4cce2
+7 b7161452ff806cdb
+8 cbb90cd9d31c152e
+9 a0c01eed9d0997e5
+10 2b5025426e67097f
+11 611126432722207e
+12 31ee12b3ba310a2b
+13 b64167eb90ed98c6
+14 22e57fdb9fd1b05d
+15 ff10ee5f8e0c22b2
+16 0352cc0950e707c6
+17 dd8819da05c51d79
+18 953d40c91befcfa4
+19 408f1a9051435f7c
+20 02a599a2b4554b44
+21 63596e2026560173
+22 4e51a5c036307bfa
+23 5f7c2016644a9c77
+24 1faddd2ba4361c8f
+25 dd767329e4b771a1
+26 2052aeadbb40e025
+27 1d8ac21098ac232a
+28 268102bd5e0a362a
+29 87736698b4c0764a
+30 ae77d27a8d948152
+31 cb1a0dfe8fba5b1e
+32 f8a3718241eba9d7
+33 df21ddf72559a905
+34 17efed79c0d82d07
+35 d069c95c2c1757a1
+36 7184af75477a1c21
+37 cdba18854a1e488e
+38 2272f4aaf171ecfb
+39 b3a37dcd754acb2f
+40 3e29d5d87806aad2
+41 49233b027e52a7b1
+42 65b912e9ac612925
+43 56f5406e01ed7a05
+44 5cefb4defab98c7a
+45 da5816621751219a
+46 52a7816f1265eb09
+47 76b2e9eda825608c
+48 7aeee8c2f690b0be
+49 8357a407c35adaa2
+50 137af5d07d1b97e9
+51 63aa23346c8030fe
+52 ce7d666f32143a99
+53 f4ca46f0dc4f5dbc
+54 31c573924c9922f1
+55 6442ba1f3f8a3419
+56 b19d5b92d63a101c
+57 0ab1cb93a5bc9e89
+58 d1f97b67caa266a3
+59 623f6f6a276d4000
+60 f9b5f78a677a8a7c
+61 ab074907c265b179
+62 f8ca72bd44db2969
+63 62667cc1feb88821
+64 48705099a4b7a939
+65 f9ba33f2fca65faf
+66 c38d88844a17ae4d
+67 e5611d6d5fa1a38a
+68 95e434991c1f93e8
+69 2baac0d2b2e815c5
+70 a758d6ea19b2c052
+71 23d6ba3bb22630e4
+72 07dd81debaf959e5
+73 f407ba132cbd0c68
+74 023849c1599c52c9
+75 beb8dae56f5ec94d
+76 39ac40c57daab1c4
+77 0be181db95c2aeef
+78 0bf356334ed9db7b
+79 34b533c55c59e5c3
+80 d96f8ba2b017e649
diff --git a/goldens/demolish.t1 b/goldens/demolish.t1
index 1c64a02..8847588 100644
--- a/goldens/demolish.t1
+++ b/goldens/demolish.t1
@@ -3,85 +3,85 @@ t1 1
 demo demolish
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 80
-1 73899e3bbfcc16fa
-2 4a6af6d4531489a1
-3 d2ee1a983391d568
-4 ba11c885b520efe7
-5 78b7a0427393f74e
-6 e3a3bfb44c18e025
-7 10ff779ec33c49fc
-8 403590870b75696b
-9 51e575ed85f97ff2
-10 06cb281e5b5b5959
-11 6782947d27d8c958
-12 9ca47051f550b599
-13 def825193854eab6
-14 ae966fa650a6eaaf
-15 2a6c32877a39195c
-16 6137b85636ccba3d
-17 ebd7df4f47a3f6aa
-18 2fcb4b27eab676f3
-19 d2f14e03925a9890
-20 9a279aadca6db9c4
-21 73ba55c37e229f0e
-22 b8a63b1e3effbedc
-23 85f3933fc60ae828
-24 396afbc798f8b499
-25 917fd0e21d2ef87e
-26 192dafbe06a85056
-27 a617a4d5beece6c2
-28 279db0476a592560
-29 42278a9a15566c3f
-30 8d1b8c1c2a865c1a
-31 f0c7e1631d3f8219
-32 2b738732798c5f2c
-33 cd0cd0ae2a1822bb
-34 392d4d1747898096
-35 df198f6cfa9c4ba5
-36 a9c43c8450cdd6e8
-37 18af573d2b565227
-38 589cb6e223c50122
-39 5ec53286b98e4361
-40 67a0ba572bf89854
-41 12b7e94aea9524c3
-42 806ee3f7d5431bbe
-43 9be81a553f7588ed
-44 1326afa95a60d3f0
-45 dfa02a4423a5068f
-46 52ba25af85fcc46a
-47 9190052ddcfb6e69
-48 1ab70b5a203d823c
-49 5393ce3bddf7c8cb
-50 3ddf1c23cd60cf66
-51 4fc61dc2976f94f5
-52 c474c4f3c4f9f578
-53 509c29bca39391f7
-54 e517a2842fdf8672
-55 326d0602e43c28b1
-56 bbea7421fa3f3c24
-57 1bd27a59f5220b93
-58 b60cb2a6d8cb0b0e
-59 d37eb67afb5a3d7d
-60 dd419fbc437d0680
-61 03f13dde86fc395f
-62 b613721a628cc4ba
-63 ddc461bdd2f67d39
-64 702664f57d5344cc
-65 35de29a0e09a975b
-66 7ceb2c77b0bc8bb6
-67 5b7624371ce333c5
-68 b92262db31d71688
-69 eb4d35b1ab960fc7
-70 938bbfd9fa0c4e42
-71 dd2da885758ea101
-72 6336454b740c6174
-73 597e0666e46025e3
-74 1a2a097c8f29fd5e
-75 17f0703b61625a8d
-76 70449b2f3fd15510
-77 6df199feb989e8af
-78 ba4821f8a235b60a
-79 33a13f00df5d6e09
-80 c53578cda0121ddc
+1 12e7a84c7a3ffffa
+2 247420cb2c864eed
+3 6644209d81c3a698
+4 40ab655e560c4aa3
+5 33f91eae1de4433e
+6 a619fa14f7cb69c1
+7 72a6f65ee20d85bc
+8 de65e7abd09a8a97
+9 630fe9de5c6b8512
+10 dbafc236f4cba7c5
+11 2cdadba2e10e0048
+12 663c95f089fbc775
+13 39282406b73fc766
+14 830461b972e96e9b
+15 2ea70f7fbadeeffc
+16 a57c25e61e330e29
+17 a28f65583de8af8a
+18 02e09ac40b3a0baf
+19 21b1a106fb0ef580
+20 370ab5b1f9d431b8
+21 ad51dc313a34d95e
+22 2e968cee14ae9030
+23 7df04f5c0f40dbc8
+24 82b21bac8256f48d
+25 881edd6d1fe080fe
+26 16b83d9f46a17a82
+27 22883f4535ca24b2
+28 56e3f3f94b282d94
+29 ed66ae854aa78a2f
+30 9b5d57eb68af25ee
+31 5dc9eed1e8ec9919
+32 70ce75483fba93f0
+33 8a58d6a26eea7efb
+34 b6e4ef2f1c04beba
+35 012829da266b8f55
+36 770f4ef17de8157c
+37 00ae75d206b8df57
+38 c7a0886d8383d7b6
+39 6c2c5cdc035a5761
+40 845362ebf7a48a58
+41 ab2f5f657e57ffe3
+42 25027a277419f642
+43 13a9dcc3d997e4fd
+44 1c08405180347904
+45 d607559a8fe28b9f
+46 77c2753f15f0171e
+47 593f6b8e881d29c9
+48 de7dc45e899b4620
+49 a5bbdaf92df9fb6b
+50 7ada966b03809daa
+51 9db399f02753b705
+52 6db1f377d55cc82c
+53 b3f97e57d6277607
+54 2ffe4c9b3d2821e6
+55 248aa56448def011
+56 cf144e165d2a1d08
+57 f66d767bbfce9353
+58 65ad11ed55413bb2
+59 e7904c6adc18dd2d
+60 980b474b0f7337f4
+61 98142481b864320f
+62 380e2eed833a60ce
+63 54e554aba67e16f9
+64 f377855ed624b950
+65 eca951debce4ea5b
+66 3f86eac1067bf61a
+67 e7d72a218185ed35
+68 c72765f0fc49575c
+69 2c00d068fa855ab7
+70 ba5c6ebc3097e696
+71 63d5795211242ec1
+72 d045dfffedd45a38
+73 1094c9bf3d1d3f43
+74 d5ca28dae8d8b5a2
+75 3b9d5d8d2618575d
+76 835156428b5f4f64
+77 5226c6418a3c32ff
+78 464fd793a62b1ffe
+79 da8d3dcb070cb9a9
+80 f00f4e637a731800
diff --git a/goldens/demolish_bundle.t1 b/goldens/demolish_bundle.t1
index c990178..55bc77e 100644
--- a/goldens/demolish_bundle.t1
+++ b/goldens/demolish_bundle.t1
@@ -3,85 +3,85 @@ t1 1
 demo demolish_bundle
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 80
-1 a8303d12d95b7dc0
-2 d1940d7f05c97ba7
-3 d54efbb631d40b7e
-4 57fea704a3430d45
-5 d522125b7e9ddf24
-6 0e6e183c418d357b
-7 e4644d43ad1f6792
-8 265d9082bdfac049
-9 fe0432ac7ee4d168
-10 004f1e5a57c8f10f
-11 1f4e7c1403bb8ff4
-12 b5f475e630b3a21d
-13 92d5ff5ef53de58a
-14 9f1862d6aa8ea1bb
-15 bba85965c0ab7dd8
-16 8b70d403ffad9111
-17 a25eaeca62cffa6e
-18 3cf0fea540b836ff
-19 7954f3600a06d45c
-20 fd54f8e70eb4f288
-21 15efae0e31907e8a
-22 87a8a71c62d2f990
-23 55ed1b8be8aecf7c
-24 816377f57ce257c3
-25 e304be1cc381f5bd
-26 183d2bdf4fff2926
-27 37b82046bf45c0e4
-28 ef648a9eebd04e52
-29 184efc79e39ab8ca
-30 d30ca591ac6e11f6
-31 dd9d02435fd5bf32
-32 9811389d63e63418
-33 13dde3569688541f
-34 126256c83a058ee6
-35 83dcc1dc398fcc75
-36 e1eba485464fd644
-37 872fbaac3a3119cb
-38 87207635222fea22
-39 b8a8c7bb6937baf1
-40 bcce8319a3e751e0
-41 e5c0da832dd94947
-42 cdc765909333946e
-43 1fffc0eaccbdcfbd
-44 5d0a7002b356b56c
-45 dee9efe991321f33
-46 33f718ddd64d908a
-47 acb4b544a192bf79
-48 9256adeb7838d048
-49 dd0d65ab6d715b8f
-50 af813a7083bcb616
-51 b1c737efad4c23a5
-52 1fe3a53ad5513874
-53 50415d651eae8f3b
-54 ba597f1f5b8e1bd2
-55 efb0c141b0e0b6e1
-56 15d6cebea9991410
-57 43ab1a7ca2039f37
-58 e436cea4453eb45e
-59 eeefe1cb2df285ad
-60 84b694d6f5f31e9c
-61 bca01ae8b20453e3
-62 2b2a1f9f2b64577a
-63 36f46b6f0dafc929
-64 77d2565004806578
-65 dc820b66e833a27f
-66 469457c1b8e78ec6
-67 7136c2eb4b11d8d5
-68 4240317af54d8124
-69 e13dce8c57b98dab
-70 8e252c8db0546382
-71 7cb8699b4185ffd1
-72 931162555f9ea540
-73 861ea897289da6a7
-74 cc6ec558a242b14e
-75 6fd903cfede1191d
-76 924582fb18e3a54c
-77 4bbb7c00f03f2413
-78 8569d7aeb510586a
-79 40a752e6df2a4759
-80 fbedf75c2690e1a8
+1 bf410a3f8ef30ec0
+2 f2326866aa29a993
+3 6fff0425cc55e78e
+4 2f6033977b9ed1f1
+5 eba9265f0f5c6274
+6 94fdb7454b779ec7
+7 0460b7859bfba952
+8 d568ee9b30b974d5
+9 993c7c33dca74a08
+10 adc64249675ba01b
+11 c91bcc50bcba9584
+12 f33be0567091cbd9
+13 c07ce0c0d5b4695a
+14 1843000b91f64f77
+15 575d4803208968f8
+16 7dd6495d4772e70d
+17 ef17070af3b46ace
+18 ef372dc2850c2abb
+19 34f0161a85090dac
+20 1b8f77ca4dc4a42c
+21 f06e4cd99228007a
+22 180c422031437634
+23 16b60c35feb99f9c
+24 aaf07a2fd86564cf
+25 d6462d8727ba3e3d
+26 04f5f7a6af8165e2
+27 cd6f0d9cfb133e94
+28 a03d9c6673a9ec6e
+29 6d04597815e63a3a
+30 5f6281c0634884da
+31 f23bcc84ae6afc32
+32 f903d3a565e6756c
+33 208248f74943475f
+34 848ac6a63a7be17a
+35 3fa932bbdcb79645
+36 341ee081e1664088
+37 c4d6f074372c0cdb
+38 8d98c9146721bac6
+39 4bbf7ec1844feef1
+40 8b12d05910847314
+41 71c217c13b8810a7
+42 12457a8b78364b82
+43 88193af970a9422d
+44 4721f9c3aa79bb30
+45 56717881a218fc23
+46 040c028a092d360e
+47 99a804fa89775d19
+48 cfc5d620562339fc
+49 661584d44a3797ef
+50 270da3812e2197ca
+51 d7adfe12817a8815
+52 fe797ad756ee4518
+53 c0eb509e6e019aeb
+54 3c3ed96cc9c19596
+55 ecde63686645d901
+56 d48d799d0c2334a4
+57 58ee7398373b72f7
+58 0d9d61b0c0ad5f12
+59 eb503be0f5067afd
+60 438fa570f9a4a8c0
+61 efdd162b889bffb3
+62 81a0831c5defc31e
+63 42ac9efad24cece9
+64 4e6aa74762b2e08c
+65 f7c2aa0a4bcead7f
+66 5d33c73bcdcdc09a
+67 86d03decead572e5
+68 ef11beadc57e8028
+69 29d9de4eaa9fc8fb
+70 2b0e44f223eb64e6
+71 6a34d961fdfc0691
+72 80a6f47042b66e34
+73 9ee89b2cbcd830c7
+74 f96c376a5b72fba2
+75 340613d1116b544d
+76 dc52f93f84471650
+77 7cab5fdd3a199fc3
+78 568f29f8aaa52cae
+79 7c956493c3a488b9
+80 657ecdf48890431c

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
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.11-terminal-types/r4/lens-out/edge-g4.json
using your file-writing tool, then stop. (Your source value is: edge)