You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. The repository checkout at the reviewed state is at:
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.11-terminal-types-r1
(all verification reads happen there; treat it as the source of truth).

Chunk orientation: This chunk contains re-blessed golden .t1 tick-hash dumps: router_tiers, router_ceiling, place, ecmp, ecmp_cost, demolish, demolish_bundle, audio_throttle, bundle, demolish_node, boot, forecast_shift. Part of the canonical PR diff (big-diff chunking).

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
diff --git a/goldens/router_tiers.t1 b/goldens/router_tiers.t1
index 7dccfd4..5703e8c 100644
--- a/goldens/router_tiers.t1
+++ b/goldens/router_tiers.t1
@@ -3,85 +3,85 @@ t1 1
 demo router_tiers
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 250679b1940fb87b
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
+1 6e1937dd469014b6
+2 bc21846678474f3b
+3 52fc2ad8b636c8c4
+4 10a77e24a7f14061
+5 c9b7d287f9bbbd22
+6 fe8d7e890addfd07
+7 1250669c54765a30
+8 b8f2a1f933aa4a2d
+9 10632201b4ccf3e9
+10 ee0e65a4f6db0b12
+11 ed90b8c19249a7c8
+12 c817e343a70346d1
+13 758e4a1c1413ebe2
+14 d7f281ac3ca71091
+15 39e0633c3e2f7295
+16 e711284463237634
+17 fbbfef848b76eed1
+18 e7bc08e7c59ab626
+19 780ad4db7149ca6b
+20 6c226218a67a0b68
+21 4bce3612f953eb35
+22 aceeb9da4f0dc98a
+23 062e82ad4c134f0f
+24 f5cd9d01459cd48c
+25 24b5cd6dace44929
+26 e530a4ad9d142bfe
+27 4e58102bdc8493c3
+28 191ee0d973148640
+29 c6a6e2c5ebabeb8d
+30 9903700cb6753a22
+31 9a1960747d0c72e7
+32 739c3b1fd7566cc4
+33 c903e66b9b1f7d41
+34 a0f675d33176f956
+35 52915f64ee7febdb
+36 b776d2395f4db318
+37 aaab63d8e8c82565
+38 7aa8ac0dc4e68bfa
+39 d125d15374720b7f
+40 a812d0e0b172303c
+41 37a7c786eab6a4d9
+42 1615ce57def56fae
+43 e1686fc3ac6424b3
+44 71a1998a25b1f930
+45 859f41390ed83d3d
+46 4a64147aea0b0392
+47 668626d576af31d7
+48 a76279aa9d864f34
+49 7d1ebf412f3aedb1
+50 947acd9ed8be5e86
+51 91efe6c2f334c6cb
+52 0f0a378f11133d48
+53 d7307b4cb3617b15
+54 3be496bcf86b22ea
+55 4ca4f192596ec7ef
+56 21e3bd22c33afbec
+57 969ec10a28041909
+58 54ad4da1f7974cde
+59 73dbd44cf89b6223
+60 e571c5b6bae95d20
+61 629025eee3d5fe6d
+62 b14f7b83d28a1802
+63 929c718251fc4d47
+64 db3dcb611c0fb824
+65 06a570b4fcc78ca1
+66 da1e63e3696c2fb6
+67 1acb494de464a9bb
+68 b40bb12b8ecf6c78
+69 94ea25abad217545
+70 65e2c0ced8221f5a
+71 637dba06bcd94d5f
+72 df778b58ba0c569c
+73 c178983838e25f39
+74 72b4544a9c3a498e
+75 fdb6f1ae16a02e13
+76 c98ebf10b39a6410
+77 e43195bf7cc42f9d
+78 41382630e7fdb3f2
+79 0fe394f195a84bb7
+80 63c1d8445f21e594
diff --git a/goldens/router_ceiling.t1 b/goldens/router_ceiling.t1
diff --git a/goldens/router_ceiling.t1 b/goldens/router_ceiling.t1
index f7fde0c..0ef3085 100644
--- a/goldens/router_ceiling.t1
+++ b/goldens/router_ceiling.t1
@@ -3,85 +3,85 @@ t1 1
 demo router_ceiling
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 250679b1940fb87b
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
+1 0209b0bbef37a6eb
+2 25529d83db923e28
+3 aa7691d1d8258529
+4 99dd851f0c5dea96
+5 8d336d993bb1eb07
+6 4b7c00e504a593d4
+7 08b3facf8655bf75
+8 5b990f1d39119dd2
+9 06cf7f974afce7fe
+10 2147903373948097
+11 56edcb9b6d26d24d
+12 e8381528a91866a6
+13 f8af8a3c9f113a57
+14 4e687a766ccfe860
+15 dbbd087dca5cedf1
+16 8e8b7a69c90044b2
+17 b12c60a00328ddd3
+18 ef1b2c499804380c
+19 92f5bfc0f924e6dd
+20 7a3a510711eff28e
+21 f5d6a8299094b23f
+22 68ddee9f83e38dd8
+23 3d6a6bc33b7a7db9
+24 6e2c27f6c953803a
+25 0a3288f07bfe2c9b
+26 b68bfb044bd27d34
+27 a94b8429032436a5
+28 d7468471d597bff6
+29 3a11a41749ea5707
+30 1f4282f2c96b6a00
+31 40fcdca6a1bc9321
+32 c87610e80c312762
+33 aaf32e85a0682f83
+34 bcfc5869ac62827c
+35 1e27265cd2c3304d
+36 861b6c1ef78599fe
+37 0c936d8c56e0a16f
+38 70944613b214ea88
+39 b956f713b9099ca9
+40 08540e5d38eb27ea
+41 f04a7b6377a9cb0b
+42 417c9f78e0408e64
+43 65befbe50ece8815
+44 c7b4eec8ab130f26
+45 72f8ee7ffbeaa337
+46 e7889cf5c063ca30
+47 16209e65499ce251
+48 616a4ca7489a3d92
+49 edbc5b0a317f11b3
+50 d552826baa40396c
+51 7d9b6e0603561c3d
+52 87e0fd3fa704a16e
+53 d9411c9cb3d38f1f
+54 3797a4415dab5838
+55 ba7e0c7af8929b99
+56 33929fb355e4689a
+57 f1c6bfabad65497b
+58 b74ef2e6a4460314
+59 9b21c2946217ee05
+60 7857cc707bd70bd6
+61 f99c027a12d67ee7
+62 1541ce971195e4e0
+63 316434e69bf47681
+64 b4f2efb38c9e93c2
+65 694039d56fccbfe3
+66 00ee4ce5b0aa61dc
+67 59e2e421ac0a8b2d
+68 a6dcc92ee56ac45e
+69 1d61123c95253e4f
+70 49952f6453a75ee8
+71 16f679f32255db89
+72 e2478b413eb6774a
+73 4c4852d8368a8e6b
+74 60425de76094a544
+75 b2284a149e5d8275
+76 8af3c61f9a19cf06
+77 4de128e8b1e4de97
+78 57affc4032639390
+79 29d213b53aeb3931
+80 c15ccb77bbb17cf2
diff --git a/goldens/place.t1 b/goldens/place.t1
diff --git a/goldens/place.t1 b/goldens/place.t1
index 65fc213..ee64622 100644
--- a/goldens/place.t1
+++ b/goldens/place.t1
@@ -3,85 +3,85 @@ t1 1
 demo place
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 250679b1940fb87b
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
+1 f69d36eda7ade0df
+2 d8a6d0303112cc4c
+3 5d83511c187a64c9
+4 79fad4f90bd1f326
+5 d57814644e2c4503
+6 8294892039913060
+7 e5ec895319bbd4cd
+8 c2122320b1d18e1a
+9 15899633100b9797
+10 f43a40ae030b2204
+11 71ccf2146ad2dc85
+12 309250189ba5a698
+13 8d04621110852f6b
+14 05ecfe326448735e
+15 4e52f47079792cb1
+16 cfdb5b30708b77e4
+17 bd576e4af00bb4a7
+18 1ed4d39cef1f8afa
+19 b37ded98c2e1824d
+20 64375cd8f541f7a0
+21 e97c91be0029ebd3
+22 165974ab9888e1c6
+23 4d2cfb53b487bff9
+24 736995efb47aacec
+25 111181c821890e8f
+26 a9f6634f6480d982
+27 2b50f33add4c1795
+28 27810203a545d628
+29 a05b2f2c2494b9bb
+30 6b7408c32038126e
+31 8d4af3ff7960df15
+32 2cb42be2e5cf2fde
+33 eb45abdf67bf0a0f
+34 12e107982d4a19d0
+35 2eadac724e9bc4b9
+36 b1253abdc75a10e2
+37 4b243236fa8c6163
+38 1a70e5fa53e07494
+39 8ce7bc7899e6d79d
+40 a89f137158eed9e6
+41 060e1e8ab86514b7
+42 520f1c6a171bf2b8
+43 fecf2d51f4496861
+44 c152bc842e20ab4a
+45 5d2125336b51d4eb
+46 84252649a46facdc
+47 aecea837dd441685
+48 40e09964ecbada8e
+49 7919152f8440513f
+50 6d804cfcc5a59040
+51 53d944aebb038629
+52 15df41d88a8a5d12
+53 22b788e8eaeb6093
+54 ee76c3eb9a6c6f04
+55 6b4cd2634a1d868d
+56 837e8858a6fc7996
+57 36ef8b7719e0c267
+58 197ed45359c4eb28
+59 0c3200ac80326911
+60 b2ff2463bdbe9cfa
+61 8a126b61d285ff5b
+62 63e0a41109590c0c
+63 127cc7e7ad996df5
+64 081b39bf3747b6be
+65 fc4f1ffbceaf54ef
+66 ad346ee3612b4bb0
+67 379f1e4d2d8f1719
+68 94bbbd5a44786242
+69 37e73bbbf456e943
+70 586b14485938fc74
+71 9b5dbfd44a07d17d
+72 cdd3cc41f5ecb4c6
+73 df1ed76df775ca97
+74 9787d366bd42a818
+75 a437dba5cee3e641
+76 61659c0c3b930e2a
+77 3c704e8e4f00c2cb
+78 e904ee505228d8bc
+79 0e3f13b560fce865
+80 1c90018da01a6c6e
diff --git a/goldens/ecmp.t1 b/goldens/ecmp.t1
diff --git a/goldens/ecmp.t1 b/goldens/ecmp.t1
index 1c5e6d3..5288b37 100644
--- a/goldens/ecmp.t1
+++ b/goldens/ecmp.t1
@@ -3,85 +3,85 @@ t1 1
 demo ecmp
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 250679b1940fb87b
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
+1 09aa41949d307700
+2 50832aa4627f74b1
+3 44d52dcc5c6b071e
+4 1df96b9c67fd0a6f
+5 5578ef76febab164
+6 4b90444b554527c5
+7 7d57b88b508ee812
+8 8b78015160417d33
+9 fd082ffd36122b08
+10 bfbcc23338d7cb59
+11 be08755fa559d268
+12 4ba9439fa7610f95
+13 fd12040fc18fca5e
+14 849a7899d54115eb
+15 7d031c3c07c2ef4c
+16 9b3c009e61c3d409
+17 1cf5afb7bea4eab2
+18 8f4c601f7340018f
+19 7bc9c32caeb480b0
+20 78f7656294f6cbe3
+21 996726ff0ebc1fc1
+22 2a973e63493e2ed4
+23 34c27707deb70f6e
+24 2cb3cecd99d2bdf8
+25 38ba201e40b3735f
+26 33f53b090fff2080
+27 a2753b009af6d20e
+28 524f0731b092312e
+29 c7acfd98178c9f19
+30 fae75354d0cfee52
+31 27218de679698641
+32 09fa1acd2fb4b331
+33 1fe637ba43e29f0e
+34 b053ddbb2cf5a823
+35 f07adb2aac7a90f8
+36 a20c356ce65a10d5
+37 ea617f5a4951d152
+38 1d11639e49294187
+39 25401e4ea12d712c
+40 a67d1b492d4ba529
+41 306a7dadd73c5bc6
+42 5894d8bb3a427e7b
+43 c1f0383b5bd5e070
+44 bbbc0c780ed31ded
+45 abd14fe3f4b6a9ca
+46 3d57cb6cefc4d53f
+47 a7739fa4da9d3744
+48 971a654acc4860a1
+49 553967c1dc5e307e
+50 ae3aa527b4cf00d3
+51 9492a9d65beb79a8
+52 690b0b6bbe4887c5
+53 f96ff590d2707d02
+54 d2e4c240c9c59337
+55 f035084e22d3045c
+56 2140de8035974e99
+57 69748cb01c4d14b6
+58 873c02be7dc8fd2b
+59 d647b2c14519ede0
+60 590be84f9a5b8f9d
+61 bffe3e77af15b7ba
+62 815cab528a8f036f
+63 82f6db8e43c60d34
+64 703955b19740da91
+65 d1803087a302fcee
+66 b2bf4f1c72634a83
+67 0c1b63a92c44c7d8
+68 5236d2963cda3cb5
+69 cfa27323da8825b2
+70 d38c0d2f0d9cb3e7
+71 8bc3bd9543af898c
+72 b2b8fcaf90318689
+73 bdcd6fd98cbf8826
+74 f8401229d7485edb
+75 173a80cb011f3c50
+76 90d97bcad5b250cd
+77 65f4d395204fe6aa
+78 02063ee212a7139f
+79 d031107be72d97a4
+80 67c4e9a004e5cb81
diff --git a/goldens/ecmp_cost.t1 b/goldens/ecmp_cost.t1
diff --git a/goldens/ecmp_cost.t1 b/goldens/ecmp_cost.t1
index 7e3d6f6..deec2d9 100644
--- a/goldens/ecmp_cost.t1
+++ b/goldens/ecmp_cost.t1
@@ -3,45 +3,45 @@ t1 1
 demo ecmp_cost
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 250679b1940fb87b
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
+1 b98cde937cf7f9ec
+2 054135d5b0908e19
+3 cc021435a98aa4de
+4 4d486348194744c3
+5 cc7d50e3da81bd48
+6 7265fe8082ce8f75
+7 53edba0c1037390a
+8 289b75dd8b65829f
+9 a99e854cd8126354
+10 6fb8d6107f962cc1
+11 c89e78f285f5e78c
+12 1b81cc63d27c5311
+13 75fe9395737f884e
+14 4927bd2162e7d373
+15 36c7412ee3038d68
+16 d66306ab3c8a533d
+17 9819ad04c165f19a
+18 14bf5f4ce8357f1f
+19 d05e7d7ae051ab74
+20 5602db78828a544d
+21 cc2b745003f00f8e
+22 3a4518b6ef3157f3
+23 ebab31f536678f3d
+24 826dfee9ee55c4e9
+25 c40eb9ab49eb4504
+26 d4357184a05962b9
+27 e3d6cc875f766518
+28 c62c3cba1eec6c9b
+29 c7980fc4e5a02f9e
+30 02880f33a7a87526
+31 543dbac912420b01
+32 55ccd2cf62a3e780
+33 2261b77d220fa8f3
+34 097994b21fb5fee2
+35 dd6f6c0ce6ef8c1d
+36 0d8b65bf6541f42c
+37 a63dabe7268efb7f
+38 0cb8ecdc6c01141e
+39 a1fd72b8720d9619
+40 39bac1e4c064b918
diff --git a/goldens/demolish.t1 b/goldens/demolish.t1
diff --git a/goldens/demolish.t1 b/goldens/demolish.t1
index 1c64a02..26dd135 100644
--- a/goldens/demolish.t1
+++ b/goldens/demolish.t1
@@ -3,85 +3,85 @@ t1 1
 demo demolish
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 250679b1940fb87b
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
+1 e6dbd8643784dbe4
+2 ff4623d51cbeaabf
+3 0312855b77c8f1de
+4 d49a014ff124e1a9
+5 d7b68187b0c01c18
+6 1de4007dd0bd3d43
+7 ccc23c68dfbb2832
+8 a4a7ae839850e39d
+9 2a60ea8e10d853dc
+10 385b509faaa6a4b7
+11 9ed4b8cef3b38e06
+12 f44ab94422e47a83
+13 6739ee6c236acaa8
+14 e9c1018d7dbe0cd5
+15 e892158c3ff3030a
+16 4706da81dc215827
+17 29b12680c3007b9c
+18 d91871203335e5e9
+19 37b8136bea917cbe
+20 771a6d671cdbe83a
+21 3810c40bb8865150
+22 afc4fd51fba130c6
+23 2d6f7a35f0673586
+24 03736a8442a5c223
+25 1d24c3507d3e349c
+26 9ab4a9096e80e96c
+27 4b4556524bf75aec
+28 6ff639de0e884e06
+29 f81e2278b0f1078d
+30 3642f883849d6f94
+31 513aaaeb48c264db
+32 d8b228178bcc92c2
+33 1cb1756d02724f59
+34 9070a5e240f333d0
+35 d771031c46ff1177
+36 5a22a131521a6b8e
+37 b29881fc71777995
+38 227c3f1ba5f97c9c
+39 55ff074a7a475e03
+40 ab933a05f13d806a
+41 df8c4af5854a2701
+42 0b445a909669f1f8
+43 6de21599935ea27f
+44 dee6b839d2647f16
+45 8f6bab7799d4471d
+46 7864881036e49b24
+47 53e80ab2e3789bab
+48 e3d0ad6173b98852
+49 056beb36f4738aa9
+50 2cc0778f79f06ba0
+51 060f3856106d02c7
+52 8883c087bce2bfde
+53 0bf1af2f4e4561e5
+54 f001f85715fef1ac
+55 3a4bcfdaeb4a5453
+56 7ae2c90c40abe13a
+57 0c696c84275ba0d1
+58 ccc518d85c808348
+59 6f806fae68ed6e0f
+60 b982d91abe3c37a6
+61 38b301e2ebb57a2d
+62 00df23ab884e7eb4
+63 135d5bc24a708e7b
+64 b1567d7e0a5cb862
+65 1726428a73d1e0f9
+66 3a6897c9db9e3270
+67 22930b8a7db6c097
+68 1ee7b4c729a4cb2e
+69 68736e3564518fb5
+70 0f7573695bf99dbc
+71 823219bd4857b923
+72 a65a3a5a8d264d0a
+73 e9827fff50fb3721
+74 1f00ea82ed23bc98
+75 ba41890eb1fb559f
+76 b3f0bc8407bb9ab6
+77 6e5155c3e16c59bd
+78 7eb1d9754ad9bd44
+79 a70d9bc47168dfcb
+80 726905c4eab40c72
diff --git a/goldens/demolish_bundle.t1 b/goldens/demolish_bundle.t1
diff --git a/goldens/demolish_bundle.t1 b/goldens/demolish_bundle.t1
index c990178..4643cbe 100644
--- a/goldens/demolish_bundle.t1
+++ b/goldens/demolish_bundle.t1
@@ -3,85 +3,85 @@ t1 1
 demo demolish_bundle
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 250679b1940fb87b
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
+1 ab231c4a5e36778a
+2 c89c829c4e4a9b2d
+3 e00409c10ba58c14
+4 2d4a65e251237e7f
+5 25f81cc2a0ed990e
+6 94425e9a2e943411
+7 acd31b4064bc13a8
+8 5bb26ec3240560a3
+9 2b66e7feda9592f2
+10 3fdf915d49978a75
+11 efc4911362c85efa
+12 dda2c76a15d130af
+13 c59288fc5a95b364
+14 2034066495f35cb9
+15 9b365aba45522a4e
+16 0a6e1bc5aad11343
+17 fe736599517e0a18
+18 0176b101e6b424cd
+19 58fdc68796d115a2
+20 17c212811c484836
+21 40ce8006717daa54
+22 d27edb21e832b3d2
+23 da702ea848e26692
+24 76ff363e973ffde9
+25 e352c1f022336a77
+26 78e5e7afecdf2524
+27 4cde2715af723286
+28 8d9682c41fdb4c7c
+29 e278ead0d332dff8
+30 fd26c9df16aafe74
+31 6607b8722bc46eb0
+32 74596e68c32e8502
+33 d0c4a2c347693509
+34 20ecce5bf66f280c
+35 f4d381c9279bd1bb
+36 ab6ade5050883fde
+37 2b3606be7bd3c785
+38 3f920cf049ced268
+39 b74158e53836e187
+40 87f12dc5e586ac8a
+41 a2bf27307a0df5d1
+42 5d9dab8931d5d1f4
+43 92605540c5bf5243
+44 6a3da374b8a8e866
+45 02917425ae898d0d
+46 e75e4abd8fc80b10
+47 da1f41ac9d4a3e2f
+48 d6ec84125c8898f2
+49 2ef10cbb316541b9
+50 4474a2292623927c
+51 a0b418fd4c2238ab
+52 9e28b83bff7e80ce
+53 299ea92538ff09b5
+54 e5c74ff8a9994198
+55 dced21c2bc429bf7
+56 18a2d12f375d10fa
+57 1ee1059a54b83ac1
+58 dfff84741a9410e4
+59 ab3cdcc6ad119bb3
+60 5d055d7729699556
+61 da896c700dd3dffd
+62 d78564a9f4d09080
+63 faa5dd6861e599df
+64 cb9ade1b43243062
+65 5e3eed82799cc6e9
+66 adf09167dc336eec
+67 1f095db968355c1b
+68 492f76f74210c73e
+69 86482df290601065
+70 128d1607cb420ec8
+71 be9375bd82bbe5e7
+72 d693bc370c31476a
+73 b872affcd6a8c8b1
+74 f1ffb2a152821a54
+75 a2d402476735d623
+76 9528cce2c64fb5c6
+77 efe53ceb7cef07ed
+78 adc080dfcd99a570
+79 76f9784ba3c6ca8f
+80 65294bf2be5711d2
diff --git a/goldens/audio_throttle.t1 b/goldens/audio_throttle.t1
diff --git a/goldens/audio_throttle.t1 b/goldens/audio_throttle.t1
index 629bd63..3aa410e 100644
--- a/goldens/audio_throttle.t1
+++ b/goldens/audio_throttle.t1
@@ -3,85 +3,85 @@ t1 1
 demo audio_throttle
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 250679b1940fb87b
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
+1 844bc7b248e52d71
+2 e17cf230f56df5c0
+3 50ca08be265d1b02
+4 e80d237adf50925e
+5 04f85bdfd18fac2a
+6 9e085ba0788a7d5c
+7 08d543b58c0ead71
+8 f9d29a498fb74e68
+9 09c513f46305794b
+10 e9694cccef203f25
+11 2066036c139e52d8
+12 c7a12152efb51c35
+13 844461b0be7848fc
+14 0badc601588ef89f
+15 93f3a03f0f117930
+16 2108240ad38ff38c
+17 1af95cb3f2ecc8ab
+18 22f07c7b7a466dda
+19 ab81215a9779956e
+20 99f435a52654f1ae
+21 52484b143e32f271
+22 72e81569e53c0ca4
+23 cc40b1d78f6a0409
+24 bd80b6f8e825fcc1
+25 ebdc42524c8510fb
+26 581eec4714955577
+27 de6d5247a49cc72c
+28 1b311176b5768990
+29 b6511584d5648450
+30 75d1c67e127dcbb4
+31 086e74d5ed8b9e78
+32 b6b69e253488dbcd
+33 4d7175d81e1ef58f
+34 6e942cf8aaa6eda9
+35 759fd5eb3753c3ab
+36 de8ff46eab323a03
+37 e91490fac04a5e68
+38 733bfc4f576c1535
+39 2b40242a0e4c12b5
+40 9f8aa089501c1c34
+41 706ec9f0b3068e57
+42 73c44d4c6fce3c97
+43 c413e2004e698c97
+44 1f805a2b349d8964
+45 d4ccd08c5b83152c
+46 df783034829f2b9b
+47 3aee4238c35eaa32
+48 e986711dd41dee20
+49 ba923aea029a8780
+50 6db8dca10752e2bb
+51 c18927282c809dd0
+52 71b6f639374ee233
+53 592699874f0cd156
+54 46452fc1f1d3fbf7
+55 807484a8a5a18487
+56 b24dc176ee6f71de
+57 5c365d2478b4ca8b
+58 c6bdeb5e7d6dfef5
+59 d0b68160987025f2
+60 05822bcfd8490cae
+61 7a892ab17a13b95f
+62 9af2b7292c928847
+63 a4c0016faecd17c3
+64 f08714973402b14f
+65 29838c7c2c478b59
+66 1cb715fb278694d7
+67 6786a074d8a81210
+68 766dbcde87274f3e
+69 2e2e99893df6536f
+70 0a83f5dfbbb4b228
+71 e99af05e81df228a
+72 c16c7462598c1173
+73 34eb862e20c8c47a
+74 b19fd69ea21de9e3
+75 465a1b738969eedb
+76 fc88d6603f490f36
+77 49581a74f270df1d
+78 4a5869f4356d04c5
+79 a7ae3cb41af525e5
+80 4ebad5370120db7b
diff --git a/goldens/bundle.t1 b/goldens/bundle.t1
diff --git a/goldens/bundle.t1 b/goldens/bundle.t1
index 339c632..418b28e 100644
--- a/goldens/bundle.t1
+++ b/goldens/bundle.t1
@@ -3,75 +3,75 @@ t1 1
 demo bundle
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 250679b1940fb87b
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
+1 f37f3bb293cec206
+2 615e1fe93867328b
+3 4d15ab7e1e1bde08
+4 f550080b52a0bf7d
+5 7f624bc0b35570c2
+6 dbccbb0390f96cc7
+7 497fbd1927e073c4
+8 7ab79faad4e7ffe9
+9 cc2edb1b313dd6ee
+10 ab33ac6cd9bc1213
+11 85dea11334ee8b0d
+12 503f09f1d5446942
+13 b3fefac3f80c1b8b
+14 eb6ee34527d81f68
+15 8653f9ce86782e89
+16 ef3ce13b197af1be
+17 35a799d4c2dc9f37
+18 ba52f5865e689bb4
+19 6aca2066e83f5075
+20 397f76a4ed3fd7ea
+21 66d90d35c6a1c833
+22 985900552cb6c570
+23 398def85b588d8d1
+24 0e74aef5029c8ce6
+25 e3a3392d6a25245f
+26 e345c595e393ffdc
+27 a919ede4afad657d
+28 c4b87417b89a2732
+29 1d35d7dd45a35ffb
+30 7dbbda4c65d53058
+31 73b2e3d84fd8aa3b
+32 f1e4ead4c98cd53a
+33 3dc5e8a884746a69
+34 f8e94bbd5cfc46f8
+35 0b8fc93670df51b7
+36 01ff3f3f8cab9bc6
+37 c9c77c7324b0cfe5
+38 80f0ce1abee3daf4
+39 936beb938df14d23
+40 450db50c0ec6fca2
+41 201f00bab6403131
+42 6827cc889e893040
+43 16cda03c1461fa7f
+44 6a3ec121a61251ce
+45 22a1c6b1137087cd
+46 21ee14c6b7ee17bc
+47 9db4127763270a0b
+48 204e9ee5cefeca0a
+49 af905af5b821e439
+50 a5f6bbfab2fdeb48
+51 b1e2fa02b34b65a0
+52 7b120b33f879f893
+53 9141722fee893382
+54 aaf0948a98c56f88
+55 7dc50e17cc6dbcce
+56 6dbe6562b110371c
+57 818fa75e807f0c58
+58 e4e0689d99ea5ad8
+59 bb36d967d35e1b97
+60 041778f89141348c
+61 cfeb7f772d8c1c39
+62 750fdc566039c2fe
+63 830f9a408b94fac3
+64 e3fd7fb9204d78a8
+65 ed0f787328870fc5
+66 5ca58898c11320da
+67 5ddaaeeac4a3d8af
+68 aa46064a0e8117e4
+69 1a578e5f07046c91
+70 f1b5f3163a7f29d6
diff --git a/goldens/demolish_node.t1 b/goldens/demolish_node.t1
diff --git a/goldens/demolish_node.t1 b/goldens/demolish_node.t1
index cd06da2..b873a63 100644
--- a/goldens/demolish_node.t1
+++ b/goldens/demolish_node.t1
@@ -3,105 +3,105 @@ t1 1
 demo demolish_node
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 250679b1940fb87b
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
+1 2bca3a352981c5b1
+2 fb5fa5adaead2b66
+3 639533b4307bf577
+4 30052cfb8e61caa4
+5 7cc674ad9218f3d5
+6 7e488260e7b28efa
+7 0312ff10e12fab2b
+8 56cd6cc8e32e1538
+9 8718b1fcdad93674
+10 9899be444189da6d
+11 f01805ca2c690b0f
+12 ef9fc627b8260b3a
+13 b06d0964bc3ce301
+14 9336a200110a175c
+15 1c92936ed0f4c923
+16 124fcedac588850e
+17 f1c03ca359617aa5
+18 f40d21ccb02f95c0
+19 6f1dcc52f9c9d5e7
+20 62f18b64e8fb94b3
+21 8dbf985484e59d29
+22 787a6cb82b42b3cf
+23 76455f55eddadcac
+24 755265b726dd2392
+25 622212c84c5b3581
+26 06a426b84c7b7731
+27 753aa58750095fb4
+28 f554d06b1073f9ee
+29 601e2c9afa62547d
+30 ebd1c4b79ae905d4
+31 386ea7a8126b2c13
+32 3add99eb8a68875a
+33 e9a60a3fcdb9d0b9
+34 6429844535080540
+35 c195ef07308b06df
+36 e542cbfd66ac6756
+37 6cb3e96e3f9ce445
+38 2c712b287ba41c7c
+39 f94938b7eb4c679b
+40 8912fc3025a2fcc2
+41 3217b47b464b19bf
+42 1831702dffd8d2e2
+43 114cd2fd2657ba7d
+44 acb230d2cfa4d280
+45 f98197cbc13822cb
+46 905184487471753e
+47 756ed0ef38fcead9
+48 8359acf865c1c84c
+49 a1bc7c19e6c4db67
+50 bf2656ff3ce1154a
+51 30766b8bd7b24cc5
+52 d644f633e6f7ba88
+53 6097fb1400245ad3
+54 f2164191cd6d4386
+55 4cde80effd864ae1
+56 2fe98095bba24c74
+57 6e15df0b130d262f
+58 bfdc9194482c1292
+59 9a70145c9f116dad
+60 68bfe31a647901b0
+61 a3c37ea7199df87b
+62 d835bca3b38145ae
+63 b19cd217843bc809
+64 68001f9615a8cdbc
+65 acd3d860421e4f97
+66 2eabadace73401ba
+67 9ea0e6a5fc18d1b5
+68 1ff04bc78ca279f8
+69 f7cceb4a19b976c3
+70 ef19cf8dbeae2636
+71 2fed55e65a2f7091
+72 3444ef8efa2a15a4
+73 0fcb32b7bc8cce9f
+74 2ea90ad0ef6b3642
+75 fe85959278ec015d
+76 94677dafebae4ee0
+77 e4d3242601a77fab
+78 a10fb73a12e2631e
+79 891c9cb5d8c08ab9
+80 e0a16b09d59419ac
+81 ffc2204bb9127ac7
+82 f2aba9de01c66caa
+83 23779742cf7707a5
+84 c6a1ec40c097d668
+85 c3f20f46fcbae933
+86 f992c7b93c28de66
+87 de50e703dcfabbc1
+88 f6bcfcecbe847ed4
+89 937edba9b915530f
+90 5ac2f719a9420772
+91 cc413263df24488d
+92 83273167d706b990
+93 e03f43420915e7db
+94 e0dfba4289d2f80e
+95 1e27309bf4030b69
+96 2194ddc5f7bed09c
+97 71f138e96b72a877
+98 720f5994f303739a
+99 ab1ffb414591e015
+100 9f5d5b5a8195c258
diff --git a/goldens/boot.t1 b/goldens/boot.t1
diff --git a/goldens/boot.t1 b/goldens/boot.t1
index cac995a..75b602b 100644
--- a/goldens/boot.t1
+++ b/goldens/boot.t1
@@ -3,105 +3,105 @@ t1 1
 demo boot
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 250679b1940fb87b
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
+1 ab1fb0d04a90026c
+2 6b789c57b8ebef47
+3 e7232713a305f3e2
+4 0516a4761944febd
+5 c07dcb64e748ad70
+6 7f8c7df00273987b
+7 23137022083c13a6
+8 c9d5a45442a4dcf1
+9 c610208f0a4d5aa4
+10 d00849a03164fcdf
+11 5c743e8384e1815a
+12 12166608a5b272b5
+13 b86c509a50971688
+14 522e71bb2fe18353
+15 b4ee4a483c9a19fe
+16 603e3afc6a6abfe9
+17 757fd5dce3810a7c
+18 b1f5655d61fc1897
+19 0b1fc00561c52a32
+20 4900c0b92a2f508d
+21 e939fcb8060d2fc0
+22 1ece77566dfe400b
+23 15021cbde00f56f6
+24 5bab4c3ef5ae33c1
+25 6c60b134b9a5d974
+26 6d52dd1536551cef
+27 65c2c50f8e64e12a
+28 583bfae3231bd405
+29 d79b945f7d3cf698
+30 1d8774ee756b5423
+31 669c6500121d0a8e
+32 707ac03f040db239
+33 3cfa4208c6fbc44c
+34 ef3aabf94945e127
+35 c87bdd8f4661ab42
+36 05948fbcc52bc49d
+37 e269f5e4fd6802d0
+38 473ed5682aa3f55b
+39 3ff62abf39d1b606
+40 62e8bcaf61986251
+41 ceebd637cc946e84
+42 06502e865848933f
+43 485e495276c00f3a
+44 c6b78d951a641215
+45 e36073056e2ceae8
+46 a1c3c78dc37f2833
+47 ab6341529a1011de
+48 af26bd15e1e904c9
+49 d35138f8c32e6a5c
+50 3cbf023f22f83d77
+51 2afaaeae2afd7b92
+52 c78a36b4faf483ed
+53 0c819a83f4255120
+54 36dce4d08c3dcdeb
+55 073b23ddded66856
+56 c57f216a3f941821
+57 9edb3095a88fc254
+58 098cf90b68a70ecf
+59 a4ff629f4804f48a
+60 e795458f73514be5
+61 260f85fcbac0ca78
+62 a62b837356ddd383
+63 860a6c596154c9ee
+64 3616209381cc2219
+65 fe0a5204d08e50ac
+66 de8e8e7ffa631c87
+67 d9de5cf9e2be9222
+68 a8dbd2d978a32afd
+69 e77053d86a9f6bb0
+70 618c0f622ffae5bb
+71 bf5523aa1c2a00e6
+72 ff8390de39bd8631
+73 36bc9fbb52c10de4
+74 477a476950ffb61f
+75 bbf5a9cea023459a
+76 d541252c04917df5
+77 678423875d0f89c8
+78 83452484016a8d93
+79 adb31bbc1fa7ed3e
+80 161f91738d31a029
+81 2b5f18bf5c8408bc
+82 f41339210ecc0ad7
+83 828c0311e85a2972
+84 29b9b921b661cccd
+85 6d22ff5085011b00
+86 11a9071074eb2a4b
+87 5b37aaa356a77536
+88 061e431797a37101
+89 8e5d0904e9f3dfb4
+90 5384b60e592be72f
+91 34e85512334ead6a
+92 29ae0c5590969a45
+93 19b092778349add8
+94 d3e42e5af00a9763
+95 e87efce2860b77ce
+96 1b8ad81d0b7b6879
+97 56143723ada3408c
+98 d8636daa3c745567
+99 181fb85bc77b2282
+100 3f99458390d702dd
diff --git a/goldens/forecast_shift.t1 b/goldens/forecast_shift.t1
diff --git a/goldens/forecast_shift.t1 b/goldens/forecast_shift.t1
index 263f19e..1166abb 100644
--- a/goldens/forecast_shift.t1
+++ b/goldens/forecast_shift.t1
@@ -3,63 +3,63 @@ t1 1
 demo forecast_shift
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 250679b1940fb87b
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
+1 07187ee271787b2a
+2 9770cb9afc0b89f7
+3 6e81dace061d2b2c
+4 0782c6053a60a5e1
+5 a3f573f350cb43f6
+6 75ca4566d4a8ce43
+7 93270b0f601fac48
+8 3b048737900871ed
+9 ec9a98a54c24bc82
+10 73043db802506aaf
+11 c14fa4233a2726f4
+12 195fc9d1bcf1ce21
+13 d2c6cca71d1355d6
+14 bf7a7ca64fafcf7b
+15 70a7aa797c6ba360
+16 a8dc410e607e6c0d
+17 b158ec6c6cf9ec22
+18 eb713cc048a87c17
+19 deee3e2be175e30c
+20 2bd54cc583186cbd
+21 344973fd69a1390f
+22 ac868ac11beffc87
+23 f9b3e97d601b07d5
+24 7e48bc7b1d265b9c
+25 1691aca333aa3cd7
+26 37577da1d2140a31
+27 a5f94fcbd9c2fef6
+28 c21bf23e947ad0d7
+29 153583e830fd61de
+30 873dbb2545039e95
+31 11df58bd838e69f2
+32 568b35a9f4bc9e9e
+33 af9709bcccba0769
+34 94502c9d42b7c4c0
+35 bcc480fe6beb89d3
+36 74771cccbe417aa8
+37 86ea85e54654f0b6
+38 46387c64befc2344
+39 654c2edee1787a47
+40 60758b49b1647b79
+41 5795516dacc0bc08
+42 31127e3b61a84094
+43 d9a003580f15c919
+44 83eb048fa533bb0d
+45 15b9a2c25926c967
+46 994dde5663615793
+47 d11a1c85115884c3
+48 6bed8cf2c01f959a
+49 31b4420cd7042011
+50 3af28f40b4954216
+51 e560eecac5db00ea
+52 13cf3af02766bc31
+53 9ea2591b584edc4a
+54 00b1e3b5ce91ff23
+55 ed053021666fac72
+56 55be22166541135c
+57 a912dc1bdd99e183
+58 531a1de9460e7c3e

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
2. **`role_from_name`** (`core/catalog.odin`) — resolves `"small_biz"` / `"campus"` at catalog load.
3. **`collect_terminals` role selector** (`core/flow.odin`) — role-generic by construction; the same scan now resolves the new roles (commented + pinned by `test_terminal_class_profiles`'s selector assertions).
4. **The growth type-pick** (`core/growth.odin`) — `growth_terminal_roster` consumes the new types via the existing era-gated, TERMINAL-only, demand_weight-weighted draw (routers remain player-placed; every spawn E31-valid + 5.6-separated).
5. **The #65 sprite wiring** (`app/render/sprites.odin`, `app/render/view.odin`) — role → sprite index + footprint: residential → house, small_biz → the small_biz sprite, campus → the campus sprite; the pre-sprite fallback also draws distinct primitive shapes (E9.1 even without the sheet).

### The catalog roster (`data/node_types.json` `[ODN-5]` — appended at the END so existing type indices stay stable)

Per-type profile = `throughput_units` (the cap input) + `demand_weight` (the volume attractor); the per-terminal cap is computed **uniformly** by the 5.9 accumulator: `cap = cap_fraction_permille × throughput ÷ packet_bandwidth` (500 permille, bandwidth 30).

| type | era | throughput | accrue (milli/tick) | cap (pkts/tick) | burst ceiling | demand_weight |
|---|---|---|---|---|---|---|
| residential | 1 | 5 u/s | 83 | 0.083 | 1 (none) | 1 |
| small_biz | 2 | 20 u/s | 333 | 0.333 (4× a home) | 1 (none) | 2 |
| content_host | 3 | 80 u/s | 1333 | 1.333 | 2 | 1 |
| **campus** | 3 | 150 u/s | 2500 | **2.5 (30× a home)** | 3 | 4 |

Era gating: small_biz unlocks at era 2, campus at era 3 — `growth_terminal_roster` spawns the era-unlocked subset (era 3 = the full spectrum), pinned by `test_growth_era_gating`.

### Bounded, distinct demand (`data/demand.json` — era 3 entries, `[ODN-7]`)

- `email` from **small_biz** → residential, volume 1 (offices email; bounded by their 0.333 cap)
- `streaming` from **campus** → residential, volume 1 (campuses flood; bounded by their 2.5 cap — the ×10 surge lands on campuses too, the honest aggregation event)
- Entries whose role has **no live terminal spawn nothing and draw no rng** — every pre-5.11 fixture is untouched by construction (verified: all 32 existing `.log.bin` files differ from HEAD **only** in the 8-byte catalog_hash header field).
- `test_terminal_class_profiles` pins the spectrum: campus fully served (≈window), campus > 10× home in volume, every terminal inside `cap×W + burst`, credit ≤ MAX, and the typed selectors never pick outside their role.

### Readable without color `[E9.1]` — the all-three-types T2 golden

New `demos/terminal_types.dem` (era 3, growth on, fixture + one small_biz + one campus): captures at 5000 ms and 30000 ms show the three classes as **distinct sprites** (house / office / campus — the #65 canon set, never re-rendered). Growth-born small_biz/campus join organically, each spawn E31-valid + min-separated (`test_growth_e31_validity` extended: 20 windows, both new types present + valid).

### The deliberate re-bless (the slice's cause chain — 4.3 discipline)

The catalog fold (`node_types.json` + `demand.json` change the folded bytes):

- **Fold:** `66c4324a06058860 → 250679b1940fb87b`.
- **Fold-only proof (boot):** the new tick-1 state dump under the new code, with the OLD hash spliced at the fold position (bytes 33..40), FNV-hashes to the OLD golden tick-1 **exactly** (`6c24e9cec592aece`); the un-spliced dump hashes to the blessed tick-1 (`ab1fb0d04a90026c`). The era-0/no-demand shift is the fold alone.
- **Logs:** all **32 existing `.log.bin`** byte-verified — they differ from HEAD ONLY in the 8-byte catalog_hash header field (bytes 17-24). (The new `terminal_types.log.bin` joins the set.)
- **T2 partition:** pixels moved **only** in `node_health` (10000 ms / 20000 ms) — the era-3 growth now spawns the new terminal classes + the era-3 demand sources from them (behavioral, cause-documented); the 50 ms frame (pre-growth) and **every other demo's frames are byte-identical** (the fold does not shift pixels).
- **W9 re-pin** (`test_w9_surge_lands_under_caps`): the 5.9 surge-lands pin now counts the **streaming-capable crowd** (content_hosts + campuses, the 5.11 roster's honest evolution) with **per-type** burst ceilings + envelopes (the crowd floor 8, MIN_LAND, credit/rate bounds all re-verified from the sim). Input-parity manifests re-saved (the same fold).

### Verification

- `tools/ci-local.sh --mac`: **10/10 gates green** (lint, 193 core tests, app build, golden harness ×33 demos + replay gate, palcheck, W1 drift-rejection 233/233 mutations, preview cross-check, PP_DEBUG builds, stats replay-identity, input parity 24/24).
- Story card status line updated in `stories-v2.md` (the established pattern).

### Decisions & rationale

- **Role/type index stability:** both the enum and the `node_types.json` array **append** the new entries. An earlier mid-list JSON insert shifted `content_host`/`router_basic`'s serialized type indices (T1-visible bytes) — caught by the fold-only proof and fixed; the final fold is pure.
- **Profiles:** small_biz 20 u/s (4× a home, cap 0.333 — a middle rung with no burst, same latency discipline as homes), campus 150 u/s (the spec's cited example: cap 2.5 pkts/tick, ceiling 3 — the flood site).
- **Era picks:** small_biz at era 2 (the office class arrives mid-progression), campus at era 3 (the streaming era). Eras 1/2 demand is deliberately UNCHANGED (dormant in the MVP — the era-FSM story owns their re-tune).
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
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.11-terminal-types/r1/lens-out/edge-g6.json
using your file-writing tool, then stop. (Your source value is: edge)
