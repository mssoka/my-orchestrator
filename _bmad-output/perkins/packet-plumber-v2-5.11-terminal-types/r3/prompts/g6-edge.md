You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. The repository checkout at the reviewed state is at:
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.11-terminal-types-r3
(all verification reads happen there; treat it as the source of truth).

Chunk orientation: This chunk contains re-blessed golden .t1 tick-hash dumps: router_tiers, router_ceiling, place, ecmp, ecmp_cost, demolish, demolish_bundle, audio_throttle, bundle, demolish_node, boot, forecast_shift. Part of the canonical PR diff (big-diff chunking).

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
diff --git a/goldens/router_tiers.t1 b/goldens/router_tiers.t1
index 7dccfd4..e6b9e98 100644
--- a/goldens/router_tiers.t1
+++ b/goldens/router_tiers.t1
@@ -3,85 +3,85 @@ t1 1
 demo router_tiers
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 80
-1 eaf03b953d5ed728
-2 0a1cc06ee1f6d269
-3 94c2903145fe4f72
-4 92daddde9f083513
-5 b74ae457e17ed674
-6 f3c0118bf8b884e5
-7 855a59039abca53e
-8 82f5cd5af7d38c5f
-9 e1822e2848391517
-10 6e3f2e8d47e74074
-11 fb97f72053ee6d32
-12 52bb3913d07b6127
-13 5daebca4a2359ecc
-14 11257ddb0ece850f
-15 cd33be95b4406a43
-16 8aa8a2eab7368806
-17 3d947daffb8c25d7
-18 d91b2e9a86dd2980
-19 a690ad38d5820b25
-20 b7b7e978723775ce
-21 ba689e31a17c0c7b
-22 9bc9f087e5756b34
-23 2ef371c1a2dde249
-24 99f18503d40d1632
-25 784afc549e8b2b4f
-26 588ed2e48acbbab8
-27 d8b2a061fcbf0bfd
-28 8651b2d38ec9b146
-29 cb1d973d3c9eac73
-30 3c39c82e0db2c20c
-31 f552d8480a5ba001
-32 9d91eae951f37b6a
-33 e10e7debe48b2487
-34 b481d4d6bc208db0
-35 156834f3e9a562d5
-36 2541e07214bba33e
-37 5d5994984173746b
-38 d64fa1cd02615ce4
-39 5841c8bb46309e79
-40 32e25fb632737ee2
-41 546d2387ddaf6a3f
-42 e132377505880368
-43 b6377bc7cc15352d
-44 06844fb95c0fa436
-45 b91bc4a2c2405ba3
-46 29579e4665917c3c
-47 1b937facb6b77e71
-48 120ce8b4de807cda
-49 21980df2a46666b7
-50 02de625d02c38ee0
-51 82edcbc17047ff85
-52 b9eec7211699ca2e
-53 7a3f5f5060a29d5b
-54 a04c3fdcc5761394
-55 e635918be096e3a9
-56 386dadd1abc14692
-57 e871e94ef819282f
-58 13a7b5d450266198
-59 82b2536c5ab2c05d
-60 d8259b5edd9bc2a6
-61 8288743e2ae7bed3
-62 d73c0e1cafe5f66c
-63 d5d0a60c1a007be1
-64 79c9e584e9ea0c4a
-65 6e38c6edd010fa67
-66 1854153cd1c19710
-67 0f78c399b595a2b5
-68 e5fadd31502cbc1e
-69 7f1bde72f676cdcb
-70 9e24d42f3a1eef44
-71 54f32860d5b5d2d9
-72 e45e5ecca47e45c2
-73 60f395702ec4d91f
-74 c30011515c9705c8
-75 1199f89eb0dd048d
-76 2adec566ef805796
-77 1961cf5a491fd003
-78 3d12d239a77bf19c
-79 57294573036d1d51
-80 d27a5642638f6a3a
+1 d0db8519dea92a28
+2 9f3ccf866f37463d
+3 2bf05d6456e038a2
+4 ef9db228f411dc27
+5 e2fe2ce249f0d3e4
+6 6be3c7a241ded649
+7 bfb6708199fe427e
+8 549f82e35bb91dc3
+9 f5f51c8cd07974b7
+10 7aa31c27231b66f0
+11 6b501b38ccfb5042
+12 d143dc325b7ebe9b
+13 fe9996a8d37dbd7c
+14 bc019ca7e5a4551b
+15 9e2a5ab0becbc363
+16 8ea4ce03d086d64a
+17 40def70a7eafabf7
+18 c6341334a6d3585c
+19 23615914cca189d5
+20 db7c2467fcc9ba4a
+21 49988092c390f46b
+22 d16dd6e41f8e7e40
+23 7c26806f848fc329
+24 066c0b0d2fe4397e
+25 42b89ab25604d4cf
+26 7767de22e8501f34
+27 d919d1487eeb524d
+28 b7eaa26492c8b422
+29 c29bb67b02f44483
+30 5575b048ac420738
+31 bd1d0f1b92d18501
+32 fe38a0957744e436
+33 a6fb865aa2394ec7
+34 5a5bd7043ccfa46c
+35 091232f11c0c1125
+36 41ef9313b791ec1a
+37 cac15de14c940b7b
+38 726842304e4bfb10
+39 9d402c037c645a79
+40 8ccec6f5f1195d4e
+41 6419b8949fe2271f
+42 ace9d9edecf6e744
+43 90e0f870046586dd
+44 6b5cada11a73ccb2
+45 2d3b315e4d661013
+46 1ef8548ae5ba7d88
+47 1197a775a7f23611
+48 15d0d99893c9de06
+49 d2a3ac0e72feb697
+50 28379a0183e1027c
+51 094299c6c7cee6f5
+52 9712d4558606166a
+53 dc2a2ca4bd29d60b
+54 fd4a6fa0ba817660
+55 ec2083527fbe3c49
+56 2ebbcecef3793f9e
+57 e39c7755bba924ef
+58 74e6da248fa9add4
+59 de6b360c8e43476d
+60 6c66d77703943942
+61 da24ec465cb12e23
+62 55408e713a940d58
+63 8b2ac8098dbc6ea1
+64 b1f4183f176499d6
+65 52e4d787642d1367
+66 ef0fb5ff5571500c
+67 32eb01e301989dc5
+68 5f360a3c2939a6ba
+69 3abb83158220c21b
+70 6a28cf5c4cedffb0
+71 41e06ac71d1b2699
+72 8a198bd2d9a442ee
+73 42cde0a0d0caa9bf
+74 315c43d2953d2a64
+75 090ebb160e07037d
+76 68dab750924335d2
+77 4ef8dfddf9680633
+78 3e37656022622aa8
+79 51c83d704eee1ab1
+80 ee54de45e8838726
diff --git a/goldens/router_ceiling.t1 b/goldens/router_ceiling.t1
index f7fde0c..5fc4ce5 100644
--- a/goldens/router_ceiling.t1
+++ b/goldens/router_ceiling.t1
@@ -3,85 +3,85 @@ t1 1
 demo router_ceiling
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 80
-1 50bbf55058adfd6d
-2 c6735c9322562f7e
-3 e73e064a081082b7
-4 038d7efa25439280
-5 702b2f69e832e179
-6 59d43036f54b224a
-7 42ed9ad9c6c7da73
-8 7b45b4836b874d2c
-9 198f7db20b4d6984
-10 682c86e5b52f4f79
-11 66a24fa6dfd3ddf7
-12 2895a2cf216f6734
-13 8575b1a7c006ed45
-14 6614ec00c101a38a
-15 cf0d67d45f499113
-16 266120d5ddf81f88
-17 fb856388861eb651
-18 b5a578628c1c9136
-19 c738041d8f48b12f
-20 086a7c3b3b685784
-21 a6acc8111faf4fed
-22 9924450bf41df992
-23 748e48ad4e8fd0bb
-24 f584a95f268f8bd0
-25 fdcdb64808515ff9
-26 ee5cb0bfa79bc89e
-27 d64c26813772f3f7
-28 c4f31c3f259f6e2c
-29 ee44ce86c27969d5
-30 23ddd665cdebf1ba
-31 d190e691b8c3b443
-32 495563ed9b30bcb8
-33 b8b912d60ca25bc1
-34 17dae2e6feee4fa6
-35 0a814bc25078d0df
-36 c3bcf548dcd80274
-37 53748146c97580dd
-38 8e1a36939d16ca82
-39 24ea91d142059bab
-40 7e4eda8796af40c0
-41 6aecb28a27ddfd69
-42 4c9735d194412a8e
-43 ccebcd2b249cf7a7
-44 fa362418c8ff825c
-45 a0a48dee6cba8b85
-46 fa5dc3ac5f6b93ea
-47 11f894465c0a5473
-48 d324691353fac068
-49 b0044c3e13c45c31
-50 07af8eef0b588796
-51 44efd6ddd4501e8f
-52 eba701009f4524e4
-53 e7e15f1cdb40c5cd
-54 3212c584336efaf2
-55 075f669305c7031b
-56 8b952f498eb4d530
-57 260a70953f9e61d9
-58 e4d4c17976a4647e
-59 2f095868b8922157
-60 0d9977cec3e1308c
-61 f0495c92d93bc535
-62 a86a29cca87e9f1a
-63 ab82ce4efb3afd23
-64 5ccbec2dbb123298
-65 84aee3f485490ea1
-66 baf1e87042da4a06
-67 13855ab618e2ddbf
-68 11f004d7367cc054
-69 d1d82ae37f734b3d
-70 58095fbf3ef9a5e2
-71 515cbe8e049a490b
-72 18c784bfb71afca0
-73 fba51a5617502149
-74 d7de2773193ff5ee
-75 d6d70d5899bb4807
-76 bcff94278b7216bc
-77 3c812493f67f78e5
-78 22245fa3f1251a4a
-79 7731c1c8f0692853
-80 999fb56abff7fec8
+1 d82653cc11491e6d
+2 b6039fa9c1676202
+3 3aa4519885736187
+4 9473f8d34847c034
+5 e06feaabf4dbd589
+6 abda2b48977b541e
+7 51db6c5a6e249833
+8 d795279477573b90
+9 9a60da1549003364
+10 37bacef5618e2fb5
+11 bf008b06b41e9367
+12 e8cda813ca7e2948
+13 dd6ae36b91c25b75
+14 8d2cbeeafca6fe6e
+15 3b60dfc73dfc8a73
+16 a872fccb5ec9e6cc
+17 748a590c308bff71
+18 be7538108a90430a
+19 5c5c9b8b68f31fdf
+20 624e6816adaf3098
+21 d07127fc3a9700dd
+22 a3ab8fc28974f7f6
+23 5b2c466268b4169b
+24 1c77f94f5fc80eb4
+25 77d28c95ddc12d79
+26 36ce930ce3078d92
+27 34f123ce30fd7fc7
+28 7521230926895400
+29 801c0894ac1d9965
+30 27f57ef8a7cc011e
+31 9252163df1fe9143
+32 5d0359a7f912c25c
+33 0025ec034a7bdc01
+34 cbda395e55159d1a
+35 d29363d2760c472f
+36 8f896deaac4d7da8
+37 bd8c6abb65a5b6ed
+38 054575c78d740e06
+39 b8e87ade352cf7ab
+40 b851c7b457a33304
+41 ffb6acf89661bf49
+42 78b13f0b5f04dde2
+43 f8096ffc1d2143d7
+44 3fd1ca8c30991e50
+45 d8953bd41b439475
+46 c779ce7aa31247ae
+47 a67c26efc895b313
+48 825d9ceec5eeecec
+49 4cded92450aff911
+50 a0b90afa5591102a
+51 15c2c24580b8e7ff
+52 44748e6a480a5fb8
+53 08c8c4aa7353797d
+54 6f2a1fbf7f0f6316
+55 457a9a9f00bf9abb
+56 aa1dc4e00f8ad7d4
+57 4df2a8a0b1b13099
+58 89f0989fcc786b32
+59 912a9e0bc1d01fe7
+60 1be4de0f6efd0420
+61 6420b09f996ada05
+62 3a9183d11f83ca3e
+63 21672577a1c9d1e3
+64 86ee61ff8ab7eefc
+65 951ef9498a8cffa1
+66 4b5c405f6c9ccfba
+67 93d98d76b834f2cf
+68 b335b3356122a748
+69 207d1f8aa5d17c8d
+70 f03d0345d7e971a6
+71 8edb3ab18c2516cb
+72 2d7623e75e880fa4
+73 0e2a9a5efcb670e9
+74 b5b7fa386bd21c02
+75 a8444b93aebd5f77
+76 3e80ba3a0fc41270
+77 e8a5cc1bcb11cd95
+78 7582f2da2541dfce
+79 a624cc865ea1f6b3
+80 e43b962d2f5a210c
diff --git a/goldens/place.t1 b/goldens/place.t1
index 65fc213..1969674 100644
--- a/goldens/place.t1
+++ b/goldens/place.t1
@@ -3,85 +3,85 @@ t1 1
 demo place
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 80
-1 2c6be049ef42d495
-2 da7785f73d4ae11e
-3 7abde2ee68ec2553
-4 02ba07474be7d234
-5 213c10956c6b99b9
-6 db30971736b0d842
-7 75ce76dd3b8cae37
-8 c1928feb61f13768
-9 929a3beeeefcd68d
-10 639162283d327dd6
-11 47fcd51991e999fb
-12 f2067109e42fab8a
-13 8141ebebf33dc495
-14 bda5ca94e0aa4c9c
-15 6ec1fac7db49b467
-16 86c7f279e269b816
-17 cfde1b6bb5bb82d1
-18 737cacae45133fe8
-19 1e43589ea47e5723
-20 c514ddc8c291cb72
-21 4cab3e1fa00999fd
-22 5974da961ea76504
-23 8bfe4b6a031c99ef
-24 7d92f6cc0af5eede
-25 d46e82d2d438d4b9
-26 a5e599be7a340c10
-27 0537879dcb0721cb
-28 f4930685939f3c5a
-29 9912671d6f59d4e5
-30 12e8c51ab90d756c
-31 a1c196a4ff805ccf
-32 7db8461994a5e784
-33 37813e7d67dd9535
-34 872e17ef2ff75fca
-35 88636c2f5c93b853
-36 0bdafe8f9cab1988
-37 9a61c4aee54b7f49
-38 9989f1d9c0ab0b7e
-39 fd18989eff4359d7
-40 1d3dd6d5c6b36aec
-41 a757e07c8f20665d
-42 089a507d95a98eb2
-43 208e9546ffc7661b
-44 36f23df397aee030
-45 3646f7269586c291
-46 4f6c4d856d6925e6
-47 e612a73111d191ff
-48 98d67cbec037b9f4
-49 77f8897b0f93c365
-50 80649eea5cebbeba
-51 5bcfa19af8818383
-52 d5c72079ba9ded38
-53 482672f409abd639
-54 f48d4b989b6e1a6e
-55 05e4d967054ff507
-56 b052e86c4778afdc
-57 673aa79d532576cd
-58 6f794780085d5f62
-59 4c90ee909b84038b
-60 28fdd434ee36bc60
-61 6895b9428e002701
-62 0413dd8d92ed1416
-63 1535530aac33942f
-64 699da694baf3f064
-65 fa5f535eaa2c4695
-66 fb43ae642be9012a
-67 ac8d27f54b0353b3
-68 eba5c6023cc5aa68
-69 c61d95473d614d29
-70 4b0db999c8ef525e
-71 56e9d2191523c2b7
-72 231fe5093cc729cc
-73 9f0de1d0c158cd3d
-74 12e3bcfeb13b4592
-75 3edad0e0fd954d7b
-76 3ecc84067b448810
-77 484527f9bad16b71
-78 a0f377c770950fc6
-79 c4462ca68bd628df
-80 135f61985f5a62d4
+1 5a567e9bb42cd595
+2 40e45b9ac0aed8aa
+3 5c786b6cfb2a6b83
+4 1791583eacd0f0c0
+5 d1b8af5899f5c929
+6 a354b1209d2b51be
+7 2663a75f4bd6f3f7
+8 13a9fb53c07b1264
+9 b4142d904175992d
+10 93df91a0e61a24e2
+11 f5d05c1a3739378b
+12 192a156b3696987e
+13 745f254d13360b65
+14 0d11a54fedc394a0
+15 a69b463bae141587
+16 601fa0e057dda13a
+17 28beb3932cdad531
+18 a9433b8f4c2d259c
+19 828ca843c0c8bd33
+20 4b9daadf12c13406
+21 edf88471b1b3004d
+22 ce0a3d302283be28
+23 2f5ded84e2677c8f
+24 944a4f75b6020202
+25 bb959b1a2b5ed139
+26 03232ca1916f8104
+27 752625fae71b6dfb
+28 2aa75fd1df0e806e
+29 6047a035d81fa9d5
+30 956b35aa10a1f190
+31 470d2f302d1d81cf
+32 e21ee1ce93b42030
+33 6d12d4227037cf75
+34 3fde3cbf33364216
+35 974780c9618dbd23
+36 e6fdeb6feab47934
+37 21af7abaf47d68d9
+38 73fa88dda7a4652a
+39 d4d10d3bfc8e15d7
+40 29c2577b32192bd8
+41 423b53a3827d9b3d
+42 7526b77851154a5e
+43 22422daad9f76a0b
+44 ba797ca32ac5a17c
+45 9caa172dd48e4841
+46 2de7598b44072d52
+47 d282cb67a441f19f
+48 7c63932d8985efc0
+49 4ab0787f0d5d4b45
+50 6ee754f664a3bc26
+51 720a610ceaeb27f3
+52 7a554e1800b14284
+53 0fb0a1815f0be569
+54 c16e4f9c4f08863a
+55 33d6917d44ab35a7
+56 16f4019247800de8
+57 cb6260bf34ed238d
+58 db2148d36949c4ae
+59 9bd3d273da8b885b
+60 dd9426966546fd4c
+61 a1538cca71433511
+62 f252c4b307787b22
+63 48481530c448b6ef
+64 02a01df6716ada50
+65 7a1d9bc96d749f95
+66 32d6082389107236
+67 2d2e7f918b1331c3
+68 d69841c5afc6bf54
+69 3b87166b6c5baaf9
+70 d1bafc8f97ed51ca
+71 bca082ec27908677
+72 6c071740492715f8
+73 ed9b7770698085dd
+74 d10c0f5bbb2338fe
+75 a9ee433f2abbab2b
+76 268fd13f8685ef1c
+77 87f8c09b3ca6a9e1
+78 8995c96645ed05f2
+79 3a36fbc84c9cbe3f
+80 e289553c8cf2a0e0
diff --git a/goldens/ecmp.t1 b/goldens/ecmp.t1
index 1c5e6d3..ca3ff65 100644
--- a/goldens/ecmp.t1
+++ b/goldens/ecmp.t1
@@ -3,85 +3,85 @@ t1 1
 demo ecmp
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 80
-1 23362f40cf4a042a
-2 2f48b59ff12e1997
-3 29f5f003b86ec354
-4 a3a93d1f73f177e9
-5 dceefc742ee8daee
-6 3215ca49a6f619cb
-7 a13faf22d3e8ae68
-8 a261cd9cd29c7e5d
-9 440dc4c1649dff52
-10 1f6aa87a917f24bf
-11 fcae2200608ff58e
-12 4079b3e4e60ad0ff
-13 59da11c9750234d8
-14 46d33ff212ef0621
-15 5bc7ec6d02ea2872
-16 1b6c519f70e1a403
-17 33b1da222106f9ec
-18 87775bebee335cc5
-19 b9f99bbdaef85df6
-20 934f4115296be7c5
-21 34725123d562d537
-22 356b81ca3d0f8086
-23 4e33504b2dbc31c8
-24 0a7fff5858ae35fa
-25 2200382714a45db9
-26 e55b4fa0c804b516
-27 e73847895889edb0
-28 07dbd1886e3b56ac
-29 a1c6612f1bb1ec5f
-30 2f0e04c4e0534194
-31 e55a61e96e47bf73
-32 3df9a3682fb6afb7
-33 6df47b3ade11c574
-34 a54ae6b751baf06d
-35 524603d59aab39c2
-36 147827a356f1460b
-37 2940dee55ca23ac8
-38 61788ad7551c9851
-39 6dd1bf69352ab866
-40 13d5ddb7317bb2cf
-41 1e200120e52a8aec
-42 d38daf0200f8c765
-43 4f60d34cdff23b7a
-44 4ecd984df9579b03
-45 9e61397079f6d760
-46 1b8707ce4ef0e929
-47 e7cff08c7575f03e
-48 e8397a51c676c767
-49 0541ecdc199a00a4
-50 1d9eadc05ae8fa5d
-51 d53a8aff6372acf2
-52 1a6b78a45e1852fb
-53 251819027a906278
-54 3ef4c678b6484581
-55 88b5dbe4d6eeb6d6
-56 e3b35564ae90f63f
-57 1b9d7770ea035f9c
-58 70b14507b53a8155
-59 bbff17ace5cec86a
-60 8109d9bb46a3f2f3
-61 bf1c5338bc2ffc10
-62 ce525364560e0319
-63 c5291d30b2569b2e
-64 6b50392399356d17
-65 e5f55762504379d4
-66 e7c7746f0b9cc1cd
-67 31293e0c8e44fc22
-68 20a2d31acef61b6b
-69 f3bf9c23222806a8
-70 378b30b03ccd1db1
-71 524cb0ef5937d5c6
-72 c2c92d3a165c642f
-73 bb34e8295296744c
-74 32bf9286e3ac9645
-75 5adfae4f4fdd0eda
-76 f81bd7cf65cb6d63
-77 6a83115a5cb30c40
-78 66d9cbd4ebde6f89
-79 90560960f4d9921e
-80 9a5c283d14f986c7
+1 4f89fdb016c37f2a
+2 87dffe85819a9e63
+3 02c606b324feb0e4
+4 f262151e995520e5
+5 c901a561242c9cbe
+6 c81d72bc8cb0ab77
+7 067943235f5771a8
+8 99240d8c0b89fe79
+9 706444b586689db2
+10 b97253b246ae5fab
+11 25b1e334f1876e7e
+12 a6d73138cd1abf0b
+13 4abf414902381d48
+14 abb670df9754c37d
+15 f5dafe021ef79612
+16 94959e7cd6d989cf
+17 df5de65bb1fb5bcc
+18 15cca40e5db3a721
+19 caa6f8b5889f29a6
+20 a8fb831c937f22f9
+21 99264e22f6cc3d87
+22 7b5ba35983ee6072
+23 242780589aa95be8
+24 d4404adee805370e
+25 0be53b773f0b1c39
+26 b8d18e6e80bc7aaa
+27 14aee69cbc7f39a0
+28 4c98ac4dc904f580
+29 799856a8f452000f
+30 8451f09d8d85e4d8
+31 a63079f2dbc9f473
+32 caea658f05515b03
+33 eae496d8b9e94eb4
+34 1a63faacae7cfd19
+35 ed0a0db71febba12
+36 ed175412fff907a7
+37 2b8536762baf4298
+38 8dd9501793560dcd
+39 f1fa5e627714cc66
+40 3e5845f0da82ff9b
+41 879f6673db554e4c
+42 960bc3da9756c5b1
+43 4dffe0cc19c71eea
+44 e67356af0ad6cd5f
+45 efb6a24776d77250
+46 7d1c6891551e8305
+47 eefe0ed015ed29de
+48 5d0a84ea92822c53
+49 d9af25abfde87304
+50 fdf0c3a720ff4469
+51 0ce75380233f0162
+52 21bd658273a498b7
+53 e309f85da54d99e8
+54 1df38ec3856b7bdd
+55 6c39f67770c210f6
+56 f6531fc4de9372eb
+57 9c06b740da35c35c
+58 ad6f015c7efe7cc1
+59 efa0a9ef4f0d9aba
+60 07d6318429c469af
+61 e4add0aa74b6b1e0
+62 723b909d1a2faa15
+63 1bb9cb0a150032ee
+64 6de96f0470affea3
+65 03a87a9dfe8a4cd4
+66 4347c661ece0e839
+67 f60ac3bebc883232
+68 4b349c90bc466f47
+69 21ff05f022347e38
+70 fbdb145ab562566d
+71 dec07a0c2ca73686
+72 a0daaf03d68f0abb
+73 d72fc623b19af66c
+74 848e6ca69e7e7bd1
+75 aa39541f388de70a
+76 17cae4378bc8b67f
+77 229e532007cb9ff0
+78 bcd1fccdf52cefa5
+79 e067f4d2393ddf7e
+80 68ab453ebcf4d573
diff --git a/goldens/ecmp_cost.t1 b/goldens/ecmp_cost.t1
index 7e3d6f6..243c094 100644
--- a/goldens/ecmp_cost.t1
+++ b/goldens/ecmp_cost.t1
@@ -3,45 +3,45 @@ t1 1
 demo ecmp_cost
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 40
-1 3cd65644e63a8022
-2 61fb6e5b56fae90b
-3 e1d6a040e6d8ad98
-4 e1ee1b00946a2431
-5 71ccad28f7a0264e
-6 2fa7cc3d3a6720b7
-7 f93f0abffc481674
-8 de52cb4cb1b1f1ad
-9 f8836404446d484a
-10 636f207972e1d373
-11 0b635f8cb2f8e9de
-12 97eb9f270acc326f
-13 66e2b416906476dc
-14 debda322c6bfa775
-15 aaf8f822074acb5a
-16 ea53e6531091fc6b
-17 d002eaee1a6c01c8
-18 455df99b2b55fa21
-19 0483414001f6dc46
-20 948bc17ee55a762b
-21 eff780a6ecb70ac4
-22 646560f3280525d9
-23 d81b6aed2898f62b
-24 b8c3f67e227a26d3
-25 55b8db9d81abfb82
-26 70112f29630b8643
-27 2f6fcce02a0a75ea
-28 987d720a1a9ea575
-29 e66360bf4f60e388
-30 f8bbefcd54e9f1c8
-31 591dfa7e153b9b33
-32 6ebb3c5848aa76ae
-33 ce799e42869a1521
-34 c481441f86a3dce4
-35 e8807b700a0b3e0f
-36 17d452a38961484a
-37 9fdbfdeccf75378d
-38 dcd7285a1dfa2620
-39 ef7546aadea4fc8b
-40 94ebb7d204e8bd66
+1 e43aedb3b3411b22
+2 b8a6a4d115f6226f
+3 ba6966ae391f0cc8
+4 7fc2fe872c430955
+5 4ef6f9b0aded01be
+6 e092d9a945dc1a2b
+7 714584256a7a51b4
+8 3efc1d80b5d92521
+9 eb0796c0d289726a
+10 f4f2a738585cd857
+11 fe429bb91cd6b12e
+12 e95ef9834375e4d3
+13 050a6939c6adf02c
+14 9441f6d10de53b19
+15 430cc81ad156fa3a
+16 52a6b77ac211cb5f
+17 3d984656fc5341e8
+18 3417107ac2f75875
+19 936e0505ac14ad56
+20 42dcf32802c64307
+21 7e2c41c09b816314
+22 2ae5fa2cd2fa40a5
+23 2242cb15de56f9cb
+24 1a1ef6c7ccc7c4af
+25 43c276216a2d4002
+26 6035b12c043589cf
+27 0d759a70d18e25fa
+28 0dad69fa600d13c9
+29 3720666ad57e8df8
+30 a6e3fe242a482ecc
+31 51d3833226d3a233
+32 c294c7a258f5cdc2
+33 44a525a8414c21e1
+34 a23293f60adb5528
+35 175f1d71a16780bf
+36 54acd4e9c7e476be
+37 760a3165586b713d
+38 e01c63c531369cc4
+39 ffe6ec6edfe4508b
+40 62de3bfa9537217a
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
diff --git a/goldens/bundle.t1 b/goldens/bundle.t1
index 339c632..8d5b0b6 100644
--- a/goldens/bundle.t1
+++ b/goldens/bundle.t1
@@ -3,75 +3,75 @@ t1 1
 demo bundle
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 70
-1 3d2125c7462b145c
-2 a4935ac2bd28c205
-3 f266de086fa3d592
-4 5b38fd18e1bd9c83
-5 345cc16f5a072e38
-6 11f7b265a7cbee41
-7 77d5721d8e9961ce
-8 89b7a67cfff2fa7f
-9 5d418cddaa644104
-10 58a78c8e745f77ad
-11 99ebce5d9c4f16bb
-12 34099c0de3d546a4
-13 7576348cea95e47d
-14 3d34b790ed035b76
-15 72cee29728668877
-16 2ecd58f54cdad6e0
-17 26c223fca2341be9
-18 a887875a891ebe72
-19 7da5f4cddfdc90a3
-20 0cb64c24bc71e16c
-21 3150602d47fa3d85
-22 cb4796ae7b5cb51e
-23 351d63f883035aff
-24 4e493f7e5c8305e8
-25 3f224ea99dfb3911
-26 28bca67a5977737a
-27 6a63a7350addf5ab
-28 c982e97ae5385454
-29 9bf7af1145fd29ad
-30 56c33ff1c5c9d266
-31 47693ea8ceacd4a9
-32 b5f6033400cf7744
-33 5a29723089cfe69b
-34 8b1f3c1378647b4e
-35 099b03d6ddcb41b5
-36 23d6478b7000cb70
-37 eca1a33a01c665a7
-38 0c2815421491681a
-39 cbd0c0795ac87c11
-40 482207504b3802ac
-41 b5183834f9e70b63
-42 57b3bf13d2825f76
-43 70214d992713855d
-44 7aa20c5ac1d48398
-45 5383fb2037a2f50f
-46 141181bf9e4000a2
-47 60d21b0e3743e879
-48 863c67807b5afe14
-49 b000d4e6bd98592b
-50 4e5389fb45fe879e
-51 accb7edf587c3e72
-52 342fb1eaeab20181
-53 2751d7aac633f730
-54 50235cce70696df2
-55 6bcf1049fdda894c
-56 bbb11a77031c9e92
-57 e452304dc50dc51a
-58 90479160ab86994a
-59 043aeec729b32929
-60 4e215e26d946368a
-61 115dfcea1cba2a47
-62 45308a2e1505ac70
-63 664c3aa079153e85
-64 67f22c988cdfc786
-65 4e9ec474d71f2c63
-66 a8b0e870ceb2c43c
-67 12e5b0e2386b6b81
-68 7cbfaaa93290a0c2
-69 fd8f303fb836f63f
-70 a85528b9ce78fd48
+1 c5f995becf04f75c
+2 8e481bee0a6c3239
+3 18cc2fbf29e11442
+4 401e8854ee0986e7
+5 5fa5c184a95a6428
+6 be62e9abf2699265
+7 1e31676e71807b0e
+8 bbde00bfa41625b3
+9 7be8f323ca2ad4e4
+10 85e052b5850f9f21
+11 001369ae0b2bb0eb
+12 740477830ac8d148
+13 3d7747a37c44892d
+14 0e568fb65152a6ea
+15 7b06c890e6759157
+16 728c2f35977a8474
+17 5997f533ad2f1409
+18 8dabb1e81a867e76
+19 660288c6957fb153
+20 5435a69c843c0230
+21 bb83daf300b71a75
+22 bd85b926ad9b9f32
+23 9cc21614cd363e5f
+24 0f439f913f7d655c
+25 a4e1f148737bfa91
+26 7a7f1779707ea91e
+27 2748340b5d0572bb
+28 4aa76a29100e4a58
+29 2fc13d923e62623d
+30 4da9731b038807fa
+31 7eceeec54388fba9
+32 eb6304e9d7b24398
+33 84267eebd7629b5b
+34 f2ae69c156d64572
+35 3822904d30ac6d25
+36 7eb2bb836932f9d4
+37 f9e99fb0c2062317
+38 e2e2d075bc56de6e
+39 db5922dc4c595011
+40 23ce55e27872cd20
+41 df0cfca118175d03
+42 7ac400c7ba7840ba
+43 6ca78c9d5232d8ad
+44 6cbc25552f625b1c
+45 813b63e29757d69f
+46 7990b5813cf9e1d6
+47 40a3278c17dd8f59
+48 0d2dbdb420bfddc8
+49 168e5ac5e09cca4b
+50 09648f7b7d936962
+51 44becb6db5e29fe2
+52 87e35645e081e715
+53 d65b6d13b1a9fee0
+54 27b10a3311417b1e
+55 a11602f86aa11a2c
+56 d17e23f9056c40ee
+57 53c40b64632f93da
+58 9d89d1c947cf6936
+59 b24c205773d8fd39
+60 4838bd0867f3cdbe
+61 4a99ee9383900797
+62 7264f4ff59960444
+63 9040f706278ea1c5
+64 ae7da9478dfd05fa
+65 8a5777c4e7ba5d63
+66 47c3a0da6d53c090
+67 1a42764551e4fe11
+68 d677578bf95bceb6
+69 391ca061e8dc7b8f
+70 f5c938613372095c
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
diff --git a/goldens/boot.t1 b/goldens/boot.t1
index cac995a..4f45f38 100644
--- a/goldens/boot.t1
+++ b/goldens/boot.t1
@@ -3,105 +3,105 @@ t1 1
 demo boot
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 100
-1 6c24e9cec592aece
-2 a5a46d7357fd7db5
-3 3a226974d2bfdf00
-4 404cdb5979889fcf
-5 3ef5b23b06387352
-6 e2b69da435f26579
-7 8a8c1fac2d0e5644
-8 7f2196b36f6a0c03
-9 59db89b611fb4366
-10 dfaaa75c9928102d
-11 d35ada4a5e925b58
-12 a34e540d25067527
-13 9cd1e2db517bb82a
-14 fc2e064504ab0ef1
-15 e29ab80e79b245bc
-16 5b0ce3bef31a4a5b
-17 23bc551073fe65de
-18 4e71903f426fed45
-19 a8748623b6576a90
-20 f2c0f011af39505f
-21 9a3986f14a6dcee2
-22 cc68a210331a40c9
-23 89324b2dc6375194
-24 e7072c6c3de42dd3
-25 57a286e2ea2a2136
-26 74d5561baec1573d
-27 749a358ee56f33a8
-28 c31aa09da747ea37
-29 b9dbd69ac1e988fa
-30 b2ef05ef5cbc9541
-31 d0b566314919c10c
-32 4ac3fff0674f026b
-33 22d9be8e8946772e
-34 d19cf9c93a0ca295
-35 42b6ca263c852ae0
-36 9ccf507d71a26a2f
-37 5b264594ff7a0432
-38 ec6f83200dea10d9
-39 cce9e5110d48e324
-40 b035907601d8e2e3
-41 96035a5b348a0ec6
-42 22da058ec773888d
-43 5623d96110aa3b38
-44 5868ca48dd718d07
-45 bab9a2192731020a
-46 f8ff452202944e51
-47 65b8a3b0a9bee51c
-48 cfc196086cfa373b
-49 e2df8b333914f03e
-50 ee6849b3d7759fa5
-51 d9e9ef31da78f3f0
-52 c2eda250bd4c39bf
-53 cbd9da0eb5f3b0c2
-54 ba1a10bc3949de29
-55 6b653bcf6e95bff4
-56 c37f4d5280651333
-57 93fae5ce571c9696
-58 308aae1c6ab21f1d
-59 36bf20df09020488
-60 3a9a31dc27e96117
-61 a9e8644b88e6c05a
-62 6672e2c39df15ea1
-63 409fa822dae755ec
-64 af09c36aa2235ccb
-65 914dbbfe2609b60e
-66 4585c93df3ecd8f5
-67 10f65994e0a98b40
-68 c156cefecc18940f
-69 fac314b750ae0a92
-70 92b3926f725640b9
-71 450b80c54bbfac84
-72 82cce696755f4343
-73 37689ff456295ea6
-74 7d906158cfd1a86d
-75 9fbcdca7758e8798
-76 e895a91ae0fc9d67
-77 16d3476bad800b6a
-78 0b4e8a07c1300931
-79 f81e8583db18e4fc
-80 64ba1bbc385e319b
-81 0c75ead52aaeb01e
-82 284b094574158585
-83 ccf100bc7f50d8d0
-84 a869eff2a3ccdf9f
-85 89bd913e5c9e9122
-86 918162c5147fe409
-87 3c62e32fddf1a4d4
-88 17a89214d8be4013
-89 42284f7c5c3acd76
-90 1d9c02ee96534c7d
-91 b4e12a4551af92e8
-92 fcf538e76a299a77
-93 4fbcb638ea73473a
-94 5c771c237e4cb081
-95 f701c232f47cc84c
-96 9636307dfe8233ab
-97 0a0fc629fd4fc06e
-98 3a2035524b20a5d5
-99 e540b45746657020
-100 8bbcb41172ecd56f
+1 d1d2e53b7b1037ce
+2 bf1669a17397cf01
+3 d4e27567ce5ec7f0
+4 59a09681c72aabdb
+5 d86fabc8b993cb42
+6 5723a44c3253a355
+7 ae2fd009138eea04
+8 d17597176675c03f
+9 fc8ff7eea94b4b06
+10 c65871e75a1a4719
+11 0575df6525c010e8
+12 540a1f4eb9f32c33
+13 431c45652275147a
+14 43c4a7b013c4f78d
+15 6361e2886c2edb1c
+16 7677eca637827f57
+17 99ba3d26b5a31b7e
+18 caf376cfec8c29f1
+19 d1038f076c06d9e0
+20 9fea7fe70fcb1acb
+21 c24df5c3348b8432
+22 1353eb83616c0c05
+23 7806c22410320374
+24 dd8352d3fa349e6f
+25 15a3f828b0415eb6
+26 d15d57ee2dc854c9
+27 20ba9a5f0f411758
+28 36a31c808d5f7e23
+29 81e5e7d1d5777bea
+30 4d880aacdd89dfbd
+31 62206ba95640be0c
+32 6a8f44c57a0ccd07
+33 57bef373c7329f6e
+34 c053b645c5d31ca1
+35 6f2dac14de34c090
+36 601cb8d98007bc7b
+37 6aed7fee59ea95e2
+38 e0eb0dab52491cf5
+39 c540606920a1bf24
+40 9f762ce9e8905bdf
+41 1346a4677769bca6
+42 3b907e77859478b9
+43 2b520217e99fb708
+44 1bd2ad4df0e25053
+45 3a7db88f3a88979a
+46 40807e85cc28922d
+47 e450fbec04e7a7bc
+48 6188ead5d69a20f7
+49 40f826873a54e09e
+50 5d5c6b628e21f291
+51 ed67b11e90cc7d80
+52 a957223a1a0c856b
+53 7fe28ae39a99a0d2
+54 f7c12412edc8ab25
+55 070cd28781295b94
+56 1370ba4a14a05b8f
+57 d71a8d23fb641d56
+58 77fec76a67bbf669
+59 b96715013a890b78
+60 053ded5be090fac3
+61 e7def4a3f663608a
+62 819015c5cb0a9cdd
+63 f0dc6af3b46aa2ac
+64 420b697a8b7c1da7
+65 0e4f6d6739ae470e
+66 58765d6e39a43341
+67 88cf17f970ccf030
+68 2b3b3c7e65072a1b
+69 f19a8ea0807a1f82
+70 0b4fd3a058510495
+71 e2e5ed22bbf49244
+72 78b83bb8cbed5c7f
+73 087f4176dcedb246
+74 5eb8a63ae1a75259
+75 070e0a04072fcf28
+76 ec42478dceff1873
+77 7949309a4685c4ba
+78 9e062757279a05cd
+79 936be6d769926f5c
+80 b12ce9b2e29da197
+81 9d60411a12d620be
+82 a681967a549a4131
+83 8969c520a5a7ad20
+84 8c0c8d5a39c0be0b
+85 0b3332876c970d72
+86 739cd8bdb0838b45
+87 4f57de26b73791b4
+88 22fdda944004b1af
+89 1b48443ed6db26f6
+90 8ec5e43fe598f809
+91 f4eb4a95ec28db98
+92 744959a12ba07163
+93 f46c23cd1adaae2a
+94 35644ec12545dbfd
+95 751e91a8fa9c9b4c
+96 2350f044c4685047
+97 1c89f50967565bae
+98 4764d4181a9333e1
+99 eb2ed49cdf7028d0
+100 7dc962e641febcbb
diff --git a/goldens/forecast_shift.t1 b/goldens/forecast_shift.t1
index 263f19e..efb5c87 100644
--- a/goldens/forecast_shift.t1
+++ b/goldens/forecast_shift.t1
@@ -3,63 +3,63 @@ t1 1
 demo forecast_shift
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 58
-1 428fb45ce9827e10
-2 bc98096c22c9eed9
-3 af0530b64eee6f26
-4 05d8d2a6f55f3a7f
-5 03d77b5b74d8cafc
-6 0c9f19d7dc1cf415
-7 ea1ceda99d945aa2
-8 8f10cd61807c6f6b
-9 a66c76fa66fb7f88
-10 8148ac414f4dff71
-11 e2df22414471c706
-12 d0ce54df579e7ec7
-13 51dd98bd2f504ba4
-14 4bef06d85367d055
-15 238dd3db0415d1e2
-16 cf75c65a29dd7f03
-17 5d482fb3451db140
-18 babfe96c84765791
-19 61e61930ece6c51e
-20 42070fc7250f72c3
-21 a9b71076b53b47ad
-22 3a0adedc83dc5939
-23 05bf19c647511797
-24 f0a8493bafe1f1fa
-25 cb1233f25e3cdecd
-26 c706e00dc72a55fb
-27 0c4a4d67c6356044
-28 8c6f408c8d7de979
-29 c1025d2d14051980
-30 59992da92d2f8fef
-31 9631e31bffe121c4
-32 81550a0f47944bd8
-33 07ecfeb2051f21bb
-34 39af0709214377c6
-35 2718b2c18afbf39d
-36 561ab56b4c72676a
-37 ac0faeb7cf04d1c4
-38 3cc4c8fdd9fcc7ee
-39 03b9ff3cf6a9b479
-40 d74e37e93481109f
-41 a6de429e4fd29d4e
-42 b2a750fc0ae38bf2
-43 79d066f599da3bef
-44 304dcfe82747e51b
-45 3450c26786fb0a69
-46 750041993be33961
-47 f3e030309a69f05d
-48 76203a507515cb3c
-49 fbbe3e2de0d1320f
-50 e6fa66bf74ef5250
-51 1b1bfb953e18d234
-52 d80ad517c87c6baf
-53 083a49d7a4a990b0
-54 4e8ef463cab9cb95
-55 2f92c5e06bc1148c
-56 353e04506e187992
-57 ab9311976cd5a6a1
-58 20960185666ac918
+1 18871c2188758910
+2 6c86e1707043669d
+3 1396f91fc7276b76
+4 c88c27b2856506a3
+5 29a37eb8c2ec438c
+6 95b19c1bba0b59f9
+7 3a2973c34faa19e2
+8 71d7eb8c1a27c98f
+9 b64d7b9fefbb8828
+10 4691475d77ec1bb5
+11 e40d5bb85af33236
+12 2653756eecf6735b
+13 a040d9976227c594
+14 32de7c542e2a70f9
+15 a81fb87f17e61cc2
+16 2531441458219c57
+17 474f6077f95dbfe0
+18 0a2a932a461ad155
+19 fc0ad029486cb94e
+20 7b79c192096db94f
+21 9586e7d64b548ddd
+22 39befeb673b38f25
+23 2d3835c4c7653ef7
+24 1a8682c413d56f0e
+25 4b1a0e648423f74d
+26 64727f5b4353116f
+27 e2c1fd6c41a32a34
+28 74296b901d9ed8dd
+29 b4aa2f8e00b55b70
+30 1f161e052313f88b
+31 69c145d70bac58c4
+32 576420ff1250578c
+33 19e883b6111097fb
+34 faf90160815ac392
+35 9848ca0537cf6dcd
+36 b405d51cf5b94226
+37 f2883dfe34ff41f4
+38 dd8431e73945344a
+39 59afeae8f84ad079
+40 40d347fb9e91a31b
+41 c22131df053343ae
+42 3edbe5339e7e0bae
+43 b9383cac65611edf
+44 4c316c4ee75ebb6f
+45 18a06760bcbec879
+46 7dd0943007cadafd
+47 db4599f2e8b80dbd
+48 dd30793b28c04458
+49 b3267521eb9a07af
+50 6b0c12abdb35ddb4
+51 252f95958fb16224
+52 53825888a82a83e3
+53 51c3af6992702e80
+54 afcb245c7c878431
+55 7508cfff40c6eeac
+56 2cb03f826c45f3fe
+57 0b33dfb260069561
+58 159a26f3396fca14

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
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.11-terminal-types/r3/lens-out/edge-g6.json
using your file-writing tool, then stop. (Your source value is: edge)
