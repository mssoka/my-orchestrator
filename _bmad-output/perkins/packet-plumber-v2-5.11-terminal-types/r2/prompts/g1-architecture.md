You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. The repository checkout at the reviewed state is at:
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.11-terminal-types-r2
(all verification reads happen there; treat it as the source of truth).

Chunk orientation: This chunk contains the 5.11-relevant goldens in FULL (the NEW terminal_types.* golden set, the re-blessed node_health.* golden set), every binary golden stub (one-line 'Binary files differ' entries for .log.bin/.png files), plus head+tail EXCERPTS of the six largest re-blessed .t1 tick-hash dumps (elision marked inline). Other .t1 goldens are reviewed in other chunks of the same canonical diff (big-diff chunking).

NOTE — round context: this is round 2 of review on the SAME PR after it was rebased onto the post-#67 base (procedural land/ocean/park background maps merged into the base). Consequences you should treat as EXPECTED, not findings: every re-blessed golden .png now renders the #67 background tiles; the .t1/.log.bin re-bless is the documented deliberate catalog-fold re-bless (the 5.11 catalog change alters the catalog_hash field at fixed offsets in otherwise-identical dumps — cause-documented in the PR body); node_health goldens changed because the demo spawns the new terminal types. Audit the re-bless CAUSE documentation and consistency, not its existence.

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
diff --git a/goldens/terminal_types.t1 b/goldens/terminal_types.t1
new file mode 100644
index 0000000..81737f1
--- /dev/null
+++ b/goldens/terminal_types.t1
@@ -0,0 +1,647 @@
+# t1 manifest — per-tick FNV-1a-64 state hashes (full sim state)
+t1 1
+demo terminal_types
+seed 42
+logic_hz 20
+catalog_hash 250679b1940fb87b
+ticks 640
+1 51345e6acfcc29a5
+2 2ed7ca6909b19cfa
+3 a03035f367f93a5a
+4 b635082eb4f0c640
+5 a89a92448af7ea74
+6 2bd47bbcddf5812a
+7 4520ff54b85fc578
+8 178de7b7a880d209
+9 c0e6bfcbcc67c934
+10 5f886911bb1aa14f
+11 89ef99c3211fad4d
+12 54a312d8e27a508d
+13 7a1b8dbef0a556f3
+14 0605570b2e22afa2
+15 7be8043eb321ced5
+16 1feb151adb7941b7
+17 b63f2731f807d112
+18 46610a527d6020aa
+19 96afd41bdcf72cf2
+20 5c77964628ca25c8
+21 e75a9b512d4c008f
+22 bbacf4f327479db5
+23 747872d7d37ae814
+24 419c5175db724577
+25 5a6df5fd1ce4c8b1
+26 d5c4dbbacacafe60
+27 7da07411cd0a4f22
+28 ddfccfd9e813a025
+29 c9b22e4cab3932b2
+30 50e0dde745687630
+31 5fbd37c41bb36b9b
+32 a997778dedfb91f7
+33 0c3b7b9508c55f08
+34 2657e070464cfa26
+35 bb97e15740e24af4
+36 05cc9a590721898d
+37 eedab780b4981ace
+38 e6e65eead90871b5
+39 90d7007738664151
+40 a7d7d3be8df4dc33
+41 f64b171a49dc7f7d
+42 58d516c9c4963d16
+43 2e1dc40822a5d88d
+44 6af0e51ff96171d4
+45 be41c14005a0fa5c
+46 c1f6bd3d45b034bc
+47 258cd72f543b6361
+48 fa6e35ae41ba1d29
+49 f76eeec2ae587184
+50 84321c2e67c4b99c
+51 523ab1268475a7b9
+52 e8de02d708f0c574
+53 3227865a93e58cc7
+54 a16d6002f56c24f4
+55 71da68afb6747c25
+56 ac293b83fd64dbd7
+57 8177308fe18e00ce
+58 d3dd0bf0921887b0
+59 f2d23c4819d6371c
+60 a7e1291a68f22ca6
+61 0fa11c81374e3f47
+62 296718c1529e4814
+63 6ed37fc192218fa5
+64 5cf3166b9f6c2da1
+65 20067517c3794d16
+66 594e99f2e8f9b7c3
+67 d3194ceb9851f6c3
+68 c76e3001f7a5f3a6
+69 ee137e92f55b93e5
+70 baebc940a5a7a6d4
+71 6af81cd971d622e5
+72 984e92f66b2196a2
+73 3a339269397a53f2
+74 ff14c436b1047016
+75 aaceab4e7e81432a
+76 c9b18a476fa6cddc
+77 904765037fefeddd
+78 0969aeaa943b452d
+79 c63be709af67cedf
+80 69b312bfe395830a
+81 c68ef08ea2137241
+82 f32dec5d727003d2
+83 0f6c3ca1d2cef852
+84 36229a838c71a492
+85 093314be100042d3
+86 64183d5c974231fc
+87 cd2a9afdd072bf4a
+88 e2828e97781692c5
+89 75ae5bf8b3b1ddcc
+90 8830c79b3277bf47
+91 9339f1faff2371ad
+92 8a57a86d88056258
+93 0470c113c1f6149f
+94 a3d7b0dfc3ab657d
+95 31fd18996b87027a
+96 915a6cab07d17504
+97 bafab22f2a78eb43
+98 c408d63771c2a133
+99 c8318e713eff2e40
+100 5a0f957bd62bbbc4
+101 b8ec44b6258e0d97
+102 5441134936017daa
+103 b371f970d3b8bed0
+104 1b50fccb0402280e
+105 577a28f88f3c5216
+106 a69bde2711821de6
+107 07386c7add66bd24
+108 f7be08f71cf6e9e4
+109 7563f4afa40482ba
+110 1f30cf036c12af18
+111 334ca773bf413523
+112 df6e3286ad5930f7
+113 865221ca8a1d4e60
+114 476cf7e2af84dad9
+115 1d0666b123e2f126
+116 3472c1481be18704
+117 b79073e27178bb7e
+118 0033a32fcd7a2949
+119 f6290bad06ff01d2
+120 f3abbe9b05ea75cd
+121 027c2c44477ccd34
+122 659d65aed47f7a6a
+123 546c1716b77b36d7
+124 d4c0532ac633b169
+125 d8458b1b277d86dd
+126 72b2d1573bd5869e
+127 6870617f4d99335a
+128 1aa3d67f735ec6d9
+129 8e8789b5da4c7cf8
+130 6f43ef01abdf2212
+131 cae1ec1fa8125b4b
+132 22bb117edf2ca619
+133 2f90c75b4f3d37b3
+134 00de72e2f2d2c47c
+135 215a90d070cfe422
+136 a7a0d28589fb7f41
+137 f80b41a65abcfdcd
+138 7fbd3677e0d85ffa
+139 8fa96e1754b13e84
+140 4ad4d329d453af54
+141 c5b4b941f64bddd0
+142 a532525cbc754bde
+143 2c911f09ba8006f7
+144 badad8b426ae82fe
+145 e34ece8e5b1c9d05
+146 69488625bb9bbe06
+147 7f6cc8d095b07445
+148 9346d4fd5c4fd85b
+149 80a2b76f693c9a32
+150 b3d041f2f00593db
+151 a035b1e1727f9757
+152 deb1ec8181be1001
+153 76a951f7e9308093
+154 386e214628207431
+155 d87b45176b5a6bb2
+156 e578d477a32530f8
+157 01636a3cd31e790f
+158 040a3ee3e762d3bd
+159 a195dd51575ee6b8
+160 21dbbcee4d2f9fda
+161 101269d6cd2f9e20
+162 9f87f3b581f1f94d
+163 b6e0e60fe1ac9b04
+164 8e162005fef4e9b3
+165 ba8e46082440956d
+166 c9adba622a7100a6
+167 73c16edcd3e65d90
+168 9f225cfdd7e91db1
+169 366336a56e68462e
+170 7ec36b3b5e9564c9
+171 2e343922709a8f11
+172 9f7ddd5a242ceeb1
+173 451f9b7536f9444d
+174 589da4c23f1b632e
+175 6eeb02b56d9fd7e5
+176 1152252ccab68fbc
+177 b2ecf4b798ee2daa
+178 0fd3f331c3f55fb4
+179 d0839a46439af530
+180 ee4bae0ed3c8404e
+181 c1e01fdb54f8079a
+182 d905012b4f6ff6b4
+183 8564fbe8b88fb5b5
+184 5ac650ec94d9e9f8
+185 23258329f59c3296
+186 b212b62983cf4037
+187 86fa2b2a0e41860e
+188 f142d25a91eb0b7e
+189 1616e4196940dc34
+190 7877695d89fcc7f1
+191 876de0e044f2a41d
+192 e7a6da52b036c933
+193 ecf00f283b63784c
+194 acd6c2d9d08a5a46
+195 1e495afb5632d6ca
+196 e8df04f235ff38c8
+197 11aa610a15a7b2f4
+198 b8d830c68a488b30
+199 4aa8c852921a8195
+200 ecd7d99a96679b57
+201 4a01e321e9f432f9
+202 af83f135f51bd4f9
+203 09d620ce3870755d
+204 cf89b6c58e9ed33c
+205 368ebf9c852c7775
+206 327561fc799d86a9
+207 8768dff3953209cb
+208 308c0c7a776ce034
+209 8aa71a4006841d8a
+210 a950ff11c6f36f1e
+211 015a6c8fffd1d40b
+212 9ded3786d857690e
+213 2ffd75216a5f048d
+214 80fbc5f9a2cc7334
+215 526422c795646b7e
+216 18d64966f99d79ff
+217 7048b4908ec95543
+218 9441ac47b6800a4b
+219 ea37bec682fc42b9
+220 13108745705eb830
+221 1c8633d52b2988b7
+222 67fb51088495f167
+223 1613580e5ff0cfc0
+224 2d1e7ac38732422e
+225 1bc322bd3eece7be
+226 6150309a7fcc6350
+227 b2f181b225ded0c8
+228 a10508b11d6afb07
+229 cadb97c7a8fbd69a
+230 49af623235a7a09b
+231 9a0d5008e1eb97bc
+232 8582220dd341d855
+233 616f0775b31fb5ee
+234 56db63581e7d6e41
+235 dd274206a672bc22
+236 a2e71c99932127aa
+237 1e067a136e8aea6a
+238 15c4bb83e69e9491
+239 8279ed60e6b0d2d3
+240 4dbfe8f65ff5e883
+241 42c89e30d83437de
+242 286effc24ebfa1a2
+243 8a9d798a1d55fa60
+244 178669b56824dcd2
+245 09b73658c2e62571
+246 6a6598ddb00ea1a6
+247 7707be9a8a708f8b
+248 bb31c5cb10d29501
+249 facdb3cf973ba057
+250 f1659f0f6dd7b0fd
+251 8ee26dd94dca72c1
+252 111896e67646a502
+253 7d593260d70cdddf
+254 1c19a952e4b639bc
+255 6398abf7e9725fd8
+256 644f8df0f579438a
+257 01aab1ca50fb005b
+258 cc9e87ed6a36eba0
+259 fa8133768ab95f8c
+260 a807e9831684610c
+261 96a186420b7e5e5d
+262 b217b58d2ec47826
+263 83e319ad369488e3
+264 753ef2fee6642923
+265 e171e1fa93237fba
+266 793d87d61989122c
+267 905786d8abf14c54
+268 905bed7425c53fc3
+269 aad24e7cf7b4d506
+270 8e4f1160ef5b7e8d
+271 ef1c3d396b593a95
+272 ca03240719de34b2
+273 5ba0cf9157c2be9f
+274 a4b626a9aa4f4dca
+275 c90aa7d3da1da34f
+276 5c7865c3ed5d4d19
+277 a812e5cff4ce32b9
+278 39916e6a32e70a0f
+279 ac2be0798c9c5367
+280 522d2e7dffbdc8dc
+281 06aa41c8b752d4dd
+282 314c3ff1c77022db
+283 ee68bb432ff9e909
+284 d1e750c3e5360774
+285 dd0092f064a04fb9
+286 1f8cee7af618efd6
+287 3b40c251e9e89435
+288 3fa39e70d23c15b2
+289 11094a41fad6be2f
+290 edf7105f2ef9836f
+291 6cc7ee0c6c35f0a1
+292 7e960516eccd4357
+293 af66c3413468162e
+294 460e18b70bebf811
+295 bdc02043f5cf630f
+296 12ac22c06b804344
+297 703d19e402f25136
+298 62398defe5dd5df5
+299 b17376d3949f0fd2
+300 e13fe2c01dad59eb
+301 7c42e7498c5ecf18
+302 444431b49cb3448f
+303 7ff9a0d7221ba09c
+304 a87620e006fa77cd
+305 8560b62b2be092bd
+306 c4f85a80b3ffc6e2
+307 02eaa130169ad9ad
+308 b16c0ab4092b0c5c
+309 6878d06389126d08
+310 632f2ac42bf8c824
+311 d27badfcb22e981b
+312 dcda8cd17fd3558e
+313 72677bc7986a1c97
+314 1e7da2e919656cd4
+315 d517789aec3a50bb
+316 ac0b4490c9c4df31
+317 c08c56fbd275a516
+318 88b7b2259f7c127a
+319 f50c6bfb9adae257
+320 9f0db23f46516b76
+321 818e330e2a28641d
+322 49df3a3e57edb5d6
+323 a840d1d639341711
+324 16e08652cafa971f
+325 e3fab4a221914da2
+326 f9481e48255c38bc
+327 619ac79fb13871b9
+328 e8f039b5d3f54088
+329 bbdca40325ede228
+330 a84cb5a42a3d526a
+331 698b744501b2e38e
+332 142e5f2f19ea604a
+333 52386492aca6c533
+334 12ab55ee004f09bf
+335 1cb6e233d89b366b
+336 132dad84d9636d2b
+337 c340cbc4e2de09a0
+338 fd7c902a6f24960a
+339 1f5437773181c210
+340 eaaf25d982164947
+341 9ca0837fa55b8e83
+342 14851a336fa038eb
+343 3e5faa0e40f3a933
+344 42ad0282faa7bba9
+345 459171ec37a7b4d4
+346 209ef2aa428eed70
+347 b643ea41743639e8
+348 817f1fd9b278fa76
+349 44174aee4e080c7b
+350 7320965f10df7240
+351 79013e139f0eefdb
+352 07a64773e2909ac4
+353 8f2eeeab34fd0ec7
+354 8232e03b28be6e3d
+355 5c5df62100fb03bf
+356 feb0e9bd46841880
+357 97cda716e212e9ed
+358 6f430aa1f1dc5c21
+359 1467d1b429420bd0
+360 b9ed6a3ef44205c2
+361 074aef369175446e
+362 b8386c4127be7839
+363 5b125b99fca84dd5
+364 b368ef437815519c
+365 5ddad872441086f5
+366 71b2e66cedf2c1f5
+367 5ac793092dec02d0
+368 339f9cac14a724d3
+369 6acc740bffae7679
+370 4f6bab200e3b7d5b
+371 d11e377d1f83a678
+372 42c08aeca0312ed7
+373 333b55b4609930cf
+374 fde2a5cc91115faa
+375 70b60941473fe651
+376 b69a5dc21998dbbb
+377 5eec01572563f87c
+378 9e0b493ee741a2f9
+379 31b11719b91d2dba
+380 c1c4da99bbf23ec3
+381 18f997d1b4c6d9d1
+382 f1797a718b7e2ef5
+383 8745ef5ca28a4402
+384 21268a17bc71f6aa
+385 4dd8b82f2b32edad
+386 ca5cbd1373074707
+387 4b7ae8580dd77d9a
+388 cb5ce3225a928554
+389 56f1901675974f08
+390 651d841d704806e9
+391 41b85e03597b5e51
+392 2a7c7d6bbe3da43a
+393 edb99234868e1572
+394 43b03b6ff1a7b20c
+395 cb16d40d47ad6b22
+396 3f765b12eeec9f48
+397 cc5f867e7c906187
+398 dd9d52900ab2caeb
+399 ddf54aa4e13f9be8
+400 7c4c2d4f453536cd
+401 706f430746d98aeb
+402 12928d1b790577eb
+403 7d8d27d1b2219a46
+404 ee596d4e24949340
+405 06ed48a32275a3d5
+406 1ea034a606e71a67
+407 6cc4922837392f4d
+408 aee82493081df008
+409 df8f2163f845f629
+410 7e426a5faadc0a97
+411 9f8a2d12c3bb3459
+412 e478d30f08d2e59a
+413 4107d791881f1352
+414 260211a53b676d88
+415 a7675f713bc7f4ed
+416 287ed4f2d6de3a42
+417 701c713cc7bb947c
+418 117fa35ea2606dd5
+419 fc62d62823633342
+420 81c27ef49fe88f65
+421 04b588f758f4a51e
+422 5da56f7f67589983
+423 24f9445aa02f2fe0
+424 d84b5f4b6d9025de
+425 6d61480531e0bab6
+426 a3a21434d18c7900
+427 778df6364b38c46b
+428 a6a48038c38ed22a
+429 221af4c0df6f31f6
+430 81a444061ce23a08
+431 0b637af9a3685b04
+432 133b84e5b64b0f59
+433 75ce43f9ba6694b1
+434 09f3d1d772ec53a8
+435 7438e3b930a6d48c
+436 aaf8ea788d3a182f
+437 a39d205b6f4066be
+438 f843e567a82b409f
+439 8e1b551332b9d455
+440 71d86665048c3c64
+441 07294c57197dca95
+442 e9f059f05c99271d
+443 14713ec4e6a25479
+444 ccc049cf128977e5
+445 39947f45f875b72d
+446 1643df25cf574899
+447 cb35c045c0c4bcd6
+448 ff29a59a4d4cc1a4
+449 44ec02744495423a
+450 f1c6606ea1f96816
+451 598a13351fb6ded1
+452 b7971a178ecf0a98
+453 52b01d4d3a844e66
+454 629f1d861ad8494d
+455 4b1c1bc3dd843bff
+456 aeb44ed473dea3b9
+457 d94fc33a023544cb
+458 3056a15e9f92bff6
+459 2f3b8c912ba95a4c
+460 cdc049a5ad1eb76a
+461 f3fd1c3b916697bb
+462 edd43581eba05f7a
+463 65f2c692a99ad4f3
+464 dee427c6f1a0f5be
+465 947f67d20e12f683
+466 5e76ef6b0d1910e0
+467 e1f9596fcaa11b74
+468 3671233a030f4ce1
+469 c8b98706bec7bb2c
+470 40195b8603e07bff
+471 5e3dbf369665e30b
+472 d016104e962c4387
+473 3b3c35fb5e08798b
+474 4ef83dacb0e2abbd
+475 5ecc78c1a2491e10
+476 4d57636916569350
+477 cfd46896c062c456
+478 8d3107e7aa40c747
+479 dd60f236455c247e
+480 8a66efd420dfd830
+481 4895ae141f03908e
+482 b57ecaf3886128a3
+483 8142ad34b34d3c2e
+484 8d848cfe22b2be0a
+485 fa6b3324f61a4caf
+486 025336dd40b5aad6
+487 a030c29f31df99ca
+488 ba29f303c8b38db2
+489 17af5b83a8693ef6
+490 04ba3578d9e4716e
+491 34a3b774562b3190
+492 0fc9284b4fa84acc
+493 eae12dee8896eddf
+494 2ceaab289e8282af
+495 b568fb30f8d483fb
+496 3b8368a858f1b648
+497 1179dffe1c58414b
+498 5bd532c8d14a123a
+499 ae5941fa04f6f82c
+500 a674acf1dfa4bfad
+501 7cdd0823a0b1bb7a
+502 d1ef5ce5b64f5c57
+503 d1f45bd3baf4d0fc
+504 2f0ad5d8e4d70acf
+505 137407b1debfce70
+506 78eacab75597695a
+507 e49c04a9af726392
+508 910c9fed929f411c
+509 8eeeb8bd79b26e0b
+510 b85ead8710a7cceb
+511 96a42ea5277f2456
+512 29a6ad8fd56c6dd5
+513 eaaa82263616f492
+514 c559133e6d3e6862
+515 8f422ec7721458ed
+516 977be7cc6bfaa2bd
+517 25afc4c032a05a9c
+518 a28ff416798d2497
+519 88043c5429f17e53
+520 1a6acb73c275531b
+521 5da2ee3b9379780d
+522 9acb10d96d17dab4
+523 ac75214a057745fb
+524 027029fda2c3eb1b
+525 64ad7023a2884fe8
+526 bf5718b86e183fee
+527 bea1e141c6e39f1e
+528 b16943b994ab779f
+529 e3a9f60718c7764b
+530 6e6e6260cd97859c
+531 86222afe325f60d9
+532 13becb5dc742a0db
+533 b59d2b076c2cae8a
+534 c0518f22a132da44
+535 04917a58930222a9
+536 87c53c3d0accfabc
+537 045b681edc9e3244
+538 7bebc04fa345fcb1
+539 0ef0d6ab49f850bd
+540 75a2f5c28b5608bc
+541 2f184d803cb2c33f
+542 edff66f809cc68f3
+543 af589c572c845487
+544 ac04489ecce935db
+545 bed6be284bf94dac
+546 ff93bcdd2a22bd25
+547 c97a8ac13a351163
+548 5eec65bf36a3a6bd
+549 007d8329763c62dc
+550 254432ec23c21344
+551 0e70a87011a5aaea
+552 155f2d43ff2a6e55
+553 3eb215cacaee4baf
+554 eefc4fb5b698daf9
+555 393c2ba67eb0292d
+556 125816d07994fb02
+557 8a1fa03932c13b77
+558 bde4e97fc2589cef
+559 3871b515f45b66db
+560 303b4f2badf9420f
+561 3635a7ecbb164a25
+562 5b98ae54d1c859af
+563 e9acf4db0d2c41b6
+564 599c0ed7a02ae1e7
+565 af015ae244e9a985
+566 a33399f7b7d78a33
+567 8493804781d0d44a
+568 847dacb0bb8143af
+569 ed35a9a30d21f73f
+570 13a36438ed8cbc58
+571 d0aafcceb8716668
+572 0ad84a5b8b1a6325
+573 db3b8c9c91461c02
+574 188292b23fcb64d4
+575 7637c4d153b38661
+576 fc598c07fb16bccc
+577 d9b35a2c126fe8ea
+578 973bbd3a68a8c1bf
+579 e6f30a5cdc511d1a
+580 c428bfde64f21590
+581 186e3cf25e254eea
+582 9fd156275f5f7756
+583 a7e3b3cee5711e4d
+584 5e571e6aaa07b1e6
+585 efd44430f97e061f
+586 7b5ad105c5a66e53
+587 f445bbb37bfeaf4a
+588 b6c71fa9c96b1b17
+589 3d21171eac4d066a
+590 a21a35eae52d65fc
+591 509dfcb1fef49767
+592 04cb7ba5c75af529
+593 a89e5533d0113735
+594 bbd15a0ebd070053
+595 5105ef776fa16946
+596 677e34e9c63d9c3b
+597 525977f4b76e7ea6
+598 a0b7fb2bc5107d7f
+599 96ca1a1c9799d888
+600 dc93da8bbf9037bb
+601 b607721405a4a551
+602 5cedce6efbc7d906
+603 52ebe2be047fb2f3
+604 6705b0ba3b383598
+605 1bd9f3f573935de0
+606 ea20be9f7a792f7c
+607 f7fc50f8a7595d51
+608 24f1368481927a31
+609 11096b45d91dadd0
+610 487d5e81547ad8b0
+611 6376b654605a1eb8
+612 6aaf984cd14bf9ba
+613 054742e6a270fd63
+614 1158523fc578f08d
+615 a1b70e6256abbfa0
+616 d4e236c9cb1bbf69
+617 ed8321420c1db723
+618 f6cc3bcabef2c624
+619 a6fd698faa459b3c
+620 7b7c7577c4381539
+621 fab03445c1685c20
+622 e3ed98b5d7d87296
+623 1d41422f9964bbdd
+624 8de74b219ec9f061
+625 8eea48365951136b
+626 c00d26f97622e629
+627 795e166a861660d5
+628 02e7ca571b2a60a3
+629 e9e3c255d249697d
+630 e402f701b54def24
+631 c0fc9b521c89b198
+632 aa540952ceabb6a0
+633 70bfded8bc500dcf
+634 0c0079da923c882f
+635 6439bf85c7013fde
+636 d5bf510e04bf813e
+637 ce424a7a3eb632bd
+638 175dc3ef78d98f77
+639 e0a8d19406fd36cc
+640 93d35c5cc0c4db4e
diff --git a/goldens/node_health.t1 b/goldens/node_health.t1
index 51d203d..caec11a 100644
--- a/goldens/node_health.t1
+++ b/goldens/node_health.t1
@@ -3,425 +3,425 @@ t1 1
 demo node_health
 seed 4243
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 250679b1940fb87b
 ticks 420
-1 bcb304e7ce7471b4
-2 fe037014b64e2a94
-3 09e67dd15696b124
-4 47a1fbce3d7ae4f2
-5 3bdfca3cba8c3304
-6 e1fc1bc4f83cad09
-7 62d0aaf1ca4d2b50
-8 77f0c90b52cfc1ce
-9 58b02465e66acfbf
-10 72239032838320fd
-11 2cbe1174c41f5cb4
-12 8610320df368cfbc
-13 dd849f2008ee79f9
-14 50097b670ef9e66c
-15 3b7e84fced425a2d
-16 e5625e5a6852978b
-17 adf2e7b17b516148
-18 158d7149ee33a56d
-19 8412e997465ad97e
-20 1d062f485ab9ebfb
-21 6a77723e723fa9fc
-22 cf86dac7e094199e
-23 0406b3f0297e5415
-24 e885b754f6125f6a
-25 991e5180f186e50d
-26 a24d991f3e91c24e
-27 d4f19e30a7283e0d
-28 d5a5c4f349885914
-29 215df6020a5256ba
-30 a0ced722d292233e
-31 b61e7400a4901344
-32 9ad3405f00896ab3
-33 979dbe71cee6457b
-34 2a4a072ae81cb5ab
-35 e80e60bc53297358
-36 e62def1846bc39a1
-37 d155dc9327c4dac9
-38 1a129f40b4501f0e
-39 76a44344f348b0ef
-40 1e9e4ca15293d6fe
-41 c846dc19172f4965
-42 b2076347141d2806
-43 6d92da0c52c09135
-44 068de2e28d43d257
-45 293b43a3dd38e708
-46 b0c71f5695872aea
-47 06a61fa3b0e53146
-48 3054f51b049e936c
-49 f070f6c4a5a7cd4d
-50 b3f0973436918582
-51 eded2d9866d3e693
-52 37e2764fd1b8b70e
-53 6a76d584f6968efc
-54 6db1ce826f4c575b
-55 d4f53640a1c994a5
-56 6cd33f552204d151
-57 75e24bc485242ff6
-58 96998f0285560926
-59 8206440ce03b1216
-60 6f88ecf5a3258893
-61 1435a70dc96ded28
-62 c297e879427beee8
-63 e3b0d17e2ea46d9f
-64 7801b49c9c31c008
-65 9cad70dc80a937b1
-66 ebcf7fe765aaaada
-67 1be15babc098acfc
-68 f10b96ed2eaa9758
-69 df94c89504dd5d60
-70 2b48ad4064c12972
-71 cd8a8f1fa0503ee1
-72 230d0c24854ccf01
-73 7cacd7f58f87d695
-74 1f6f6d1b4f54f5f2
-75 8ff20fd072ff25e5
-76 caddc6b0d15019ce
-77 a12d5a89fabffcd1
-78 c678f08179c3d372
-79 42ba9f481d599e13
-80 dffa191920a4d759
-81 bf0f4c0ff42d4366
-82 eb11fef08e80398e
-83 24030de90ca839ad
-84 5df53fbc4ed00404
-85 fe1c9014f7bda534
-86 37bab2e180bf4d5c
-87 e087f63801bc85c1
-88 19dd32c591d4f17e
-89 9e74944a774f3261
-90 d874ce3808fe226b
-91 13543f162da68960
-92 4c01e190c8ce2b1e
-93 694227b615e90587
-94 5d2a6d477a31c5cf
-95 5ad6df52743fdbe9
-96 bc890b98c766ac98
-97 e3e5d0cf178a4513
-98 158fc3f0f22bae75
-99 d03367c2618e9af2
-100 4bc944d2199e0a57
-101 f3d0ac38c9426576
-102 b36e2849a2480916
-103 52cc96b1eb8cf089
-104 d81b9c7bb5636e07
-105 2041e2e330f6ad5f
-106 ab3fcd34d2fdd634
-107 e4d58d18a6394047
-108 ef5444c58852745c
-109 97295839599c5dcc
-110 1b81bf4075995563
-111 53ac4eaf1c33015a
-112 a49785d4972cb171
-113 41f2a270b1e2c7f7
-114 79aa29255755ea2f
-115 6173a4df03c7e1ac
-116 7922d80b6fe24a0a
-117 41b562ce9fea5ea5
-118 ea6ec6357424cea4
-119 a48ec56b43bd7d4e
-120 f06d81cff7708bd3
-121 89aea6bc26f70df1
-122 1752cbc515ca65a6
-123 97363fa80dbd3c68
-124 25f543def519b0d3
-125 cc3e07ddb0b4a328
-126 00eb853ef1bebb27
-127 08fe1fc3586c55fd
-128 ce91c4eb5df3e0d1
-129 cbb1902d8a545137
-130 124790ffd0ba5acf
-131 e365b6efe6f1dc2b
-132 88cb9f112b881f9e
-133 d26695a45095a3b5
-134 eedc5b97ad5db7c0
-135 69e818b0cbdaf5e4
-136 4d7db6b06cddc47f
-137 d5bd0384ea6d83e7
-138 1cedd229fe0b923a
-139 76a207bf43c40c41
-140 b6ab04c27a39948e
-141 b06cbf24b7a4e398
-142 47e8da72f168c015
-143 acee446a11abf7d9
-144 742e3c08b95647de
-145 638b58a70544f41f
-146 92f186fe81bab781
-147 c462375ebfae7dc3
-148 ef1a7f3b16b30348
-149 dd6218ff54114a8c
-150 d33d5160a0b59010
-151 aad129cec12a881c
-152 20eabf79867b1e9a
-153 e804390a8acffe84
-154 e9131a50a4592f6c
-155 1d16aa645133f2a9
-156 1def989ed93602e6
-157 36473ff5456631e9
-158 5eff1d4395c71e0c
-159 a7a16b30201ddd8b
-160 9f5df50b7c10eaca
-161 5b166f3849d40df8
-162 a87d1b91ee9b16ea
-163 c967ca047e6b8b87
-164 bdafb72fe2ab6284
-165 6b26fe2fef452c1b
-166 450c1645045fd990
-167 3b8fe19756255a14
-168 c0b4f1b01057e9b8
-169 ade6488b012dd596
-170 b311fd215b356e24
-171 b0c39b003e9385d4
-172 2de54bbf50b6524a
-173 0da53efc2fb801ea
-174 4f1d1db169177647
-175 6da0be11b5a68ddb
-176 2cf1d304645dd496
-177 65f63ee8ce698c29
-178 a61c800934288d5d
-179 d34f5a20f4497e29
-180 c3afe0640aa5f85b
-181 baeb875ada35cc19
-182 5432982290728f0f
-183 d2cff691c0c22f3d
-184 d9620e6f537b2687
-185 077e36bac9d99b8c
-186 321a1ac565d606de
-187 35f40b8ed278ddb4
-188 c5fb3a25dd64932a
-189 67b6251ac8ab17b7
-190 d71cab82fbe505c5
-191 56db7001710a24bb
-192 6a852e0b72f11bec
-193 6f673e487cac9b34
-194 06e7adb3f9d10f8b
-195 096bd1ac8f70c4f7
-196 8566e08c5ef57fbe
-197 65b5ea36a86533f5
-198 c3cc29f1b677e704
-199 4c9fea8e2f214a10
-200 d2dec6c69a887adf
-201 c8ca5e49d2937a0d
-202 ea1b09086d588479
-203 35acadd7c4b54e50
-204 b906418b80a2ec9f
-205 e034d97eb236b3df
-206 9d673f20e8cdd5c7
-207 0ab13cf602a531be
-208 ef3a8f74beb420fd
-209 3f928be157afd2b9
-210 4a5ca7fef0c33f33
-211 dca965e1d133f944
-212 01ccf86f49060267
-213 2a11e6f28d9bb46e
-214 1a72fcb1b9643fcc
-215 a53c5fe46f7474bb
-216 238643d21b06401c
-217 391825addbff2c2a
-218 49d7ca4a556f4808
-219 833f86e8db70d4bb
-220 d337407a31d53b2b
-221 db446822f67c215d
-222 cdd867b39b1b4c94
-223 853a208b0d54313b
-224 fff1f1c8929dbe71
-225 86b39f0e6636d3c4
-226 abd8bb18a6eb9f08
-227 30dc6b15c2692665
-228 17948fa283bab4ef
-229 c0d72823ba165a6e
-230 b48d38cf6ebf72e4
-231 4e19e9850b2864f1
-232 5c291945c8477fae
-233 515f28498d38e88b
-234 e0ce07da8250c1da
-235 a685f22a98dae9cf
-236 466dced09cf8b846
-237 3cd184c5c12256b0
-238 3d17f2d57511347f
-239 65e55d711749b9f9
-240 280b72de86944cd1
-241 415a757eeed4e2ba
-242 d48e3480ace498d1
-243 9e44aa54264106e7
-244 2336880bb9f671d6
-245 58cc156b00896f1a
-246 b12c2c275b8e4b9a
-247 2d3cb86c61be8afb
-248 9222b19396e1fec1
-249 22d8e1d6b9008b39
-250 c51aacd5032a4971
-251 6cf4ab1ddbf8c7cd
-252 136987d2d87f4e22
-253 2cf7bc094ce30214
-254 b5f663d6483ca710
-255 9213468f508a6763
-256 fe6b28bae72ce29b
-257 65add60818211d58
-258 0216b7026238792b
-259 521cd6231eadd9b6
-260 1b65c172c4c46d34
-261 5652728b354d40c5
-262 ce600c8e338081a2
-263 25319ab799dbc8a7
-264 ff209def8c7d1be6
-265 c79a078770e76d92
-266 7348ca796dba1c3e
-267 fa7000c9c97cfff1
-268 ee573e9aa03c63d0
-269 6f9ca5e2eedceb2f
-270 516bc1d802c36261
-271 cfab1fb040fe1dc1
-272 e76600f7b7aa5ac1
-273 cf3c49f7ee053eee
-274 971c8da4d589e57b
-275 4ef32f30e4bdb3a8
-276 c16c59e3e386971d
-277 857008d2f6051d4d
-278 f86ac66170906b41
-279 72f2af62a800c885
-280 a2f0eae849a15467
-281 910703960ccb0c99
-282 b4cf121b88c95ea6
-283 aa5f539b779cafab
-284 921df0410f6292be
-285 94246f59af8331e3
-286 04080dadc9a9c53f
-287 3483d1f0050353ae
-288 bbe37ac474eb8f80
-289 62bf97913abd0b5c
-290 3d115f1688bc21a8
-291 564ce718015cce59
-292 8c5e2e29571dff27
-293 c8b7f078ed032e36
-294 b0ffd5356a689281
-295 20595a874ece6144
-296 e873769a7067d039
-297 40c234d1033c2474
-298 0546337f6693489c
-299 ef587c671e70bc09
-300 62c7929abd695184
-301 ab1ff76838a42287
-302 b9ca2a7a2d0ecf77
-303 2ac94e5f9dcf36f4
-304 d9acd8665bc7d924
-305 0c692c7e5408963e
-306 9d275c65ca2cb4d7
-307 f91d8390c9c208a7
-308 dbee41707a46e235
-309 fe80dc467e6e52e4
-310 2ab29d5fdc1e88da
-311 22f694fea2ab3293
-312 d3f9bfc8a0acd6a9
-313 3502e9187b5dadb5
-314 2ef65f12cc84ae60
-315 df7a369e372756a6
-316 a2f34926e01e3f6e
-317 b1608c449d33907a
-318 279f074b8a2b73dc
-319 7da790bfc5a978e2
-320 587737ea424a2d5c
-321 8ab49a409cce6821
-322 26514b0bad0fef73
-323 5b6a31f6067fe0c6
-324 27d5e55c9ffbd6a4
-325 a879f7f56019022e
-326 ce971261ba372936
-327 447d9a36af3ffcee
-328 4897ea9eaa833f3a
-329 3fcfced84c6f0a13
-330 faa6953fc1d28256
-331 b62fd9a852ad9518
-332 1db3a0190e41489d
-333 515be4d458fe2dad
-334 867567c15b7c64a5
-335 7aa89c3ae3e0bceb
-336 ddf007738713a045
-337 d925d760244cafe2
-338 a0d905792f5b60a0
-339 458e68b42b5b427d
-340 816d4c02b9a391e7
-341 06042d339d87c2a3
-342 425030284711a333
-343 3136c934d7832b2c
-344 dbebb2f15abb1b24
-345 03afc62a0d16e5e1
-346 84003392e1a35fbe
-347 ba4218e26d6a3e11
-348 4087706ce3122d78
-349 4e764f74064569b1
-350 9e7786211f9775a3
-351 b2c12c4eb808fd89
-352 f6b6f4389374f034
-353 39777da0ff2e015e
-354 8f05d564fa3cc63c
-355 5069ff3221b5973a
-356 54dc928326da6ce7
-357 b611cc4afc18583f
-358 1b00e67260e2c78f
-359 888ac445f2a98cd6
-360 5ca8766c99c98932
-361 88ccddb7b87cdb2b
-362 e1f0d2d4a7ac9150
-363 e6e4aa0360477156
-364 d49a41e0235015c2
-365 9663cb9a784d21b7
-366 3b462f3e042fb121
-367 e2cf0943db8a6508
-368 a03646dfe8a57eaa
-369 5a63f47f78db4b56
-370 abdad2c080366fed
-371 c76dc5ec6fb6224f
-372 bb6dc23e6481c8ed
-373 5fecb56758fd9261
-374 60128cde6a40dd9d
-375 86d7109a013c073f
-376 0a48c88f3d93a792
-377 14bd2767c3d45a37
-378 36e5d4e503382330
-379 c30cc66e3978ea44
-380 7d78b905a9cab1e4
-381 e6575b6307930e9f
-382 7175441d93299f39
-383 dc1accdebe2e01cf
-384 d9c6f57f4eb5ccdd
-385 5ee5a12b63a79ae1
-386 26fbd853facd9321
-387 f64879594214ca16
-388 f87d1ada6a1f34c8
-389 2eac504e2f8c29f8
-390 5f2cab4f9edf355a
-391 a082993e3d456c8e
-392 9ab8a4a34e871c6b
-393 035512a947cb11da
-394 ce602dfa635b5a44
-395 38fa8b157133b4c8
-396 25da5281a0ac1512
-397 77fba4973604a739
-398 7112fc8fef454954
-399 c404747c5493379e
-400 dd16aff2f5eeb428
-401 86670c624856ad3e
-402 302b8e3861b86369
-403 3e4a2534c285be09
-404 be3d7771907a34ca
-405 10302992bbe1e26e
-406 ad93811b7ea2e207
-407 20ac008670ba4ba5
-408 f68ee2b6cfc00732
-409 7e21099993bafedd
-410 06512f3c042f799b
-411 c198854f6162106f
-412 9f729635476f42c1
-413 0518de4cb1b895e0
-414 a412d84d1bf82adb
-415 f88bd247023948db
-416 443a520eb5853811
-417 10016a95393a9925
-418 1a309add05555bc7
-419 a83207e8000e482b
-420 9b7a4740c186c0b4
+1 ff3c236f26a688d2
+2 b380977248e6b016
+3 485ff545b2286e9e
+4 56c25ebb75a776e0
+5 f5ad5447e969894a
+6 44fcec21f40a9dff
+7 673fe6528e322b96
+8 2b93c2dbc42923c0
+9 cd5864c2c718a749
+10 ee8da25b84152843
+11 e1595b7e52ee9322
+12 753b59efc7f256ba
+13 ce3e17c83c5f1c7b
+14 cbc31dd6049132c6
+15 1fe75c70924bcba3
+16 ed2aa1c94c10db11
+17 c0f48f8d79490f0e
+18 b2d433c8e533d7cb
+19 eba53917e56e4ee4
+20 a23c7ae2878a0519
+21 e83c11d39127c47e
+22 616c6afad3470ad0
+23 6c42c8fa373ae103
+24 6dd6bd61dda5cd8c
+25 6eccd7da2dd9b2bb
+26 dc9968a53e32d848
+27 c785baee4c55875b
+28 867aadcd7d7fa172
+29 04d29e0b90a95be0
+30 57f34fdd20b915c0
+31 796ac9828593c686
+32 b1c7519afff31939
+33 ca4b5cca14a4d17d
+34 b1d07094dbcc1831
+35 22da0d9be44ec64e
+36 e99b86f468fec293
+37 e908d53093564567
+38 5b4b553045c14d30
+39 4eb347b990a8e2e9
+40 5e6c64053b9f6074
+41 091385de283729e3
+42 979627f8fa532c5c
+43 101a72ca113f8c0f
+44 95653b3572d37b45
+45 17a11b8af171d0fa
+46 c03aba176f5ce364
+47 3e8e8ffe1f65b190
+48 c7c20a5d93469502
+49 4997003f916b4e47
+50 91f7fab081763494
+51 3dd32e02960caed1
+52 54bb49fba441271c
+53 e7688d44d41c1d02
+54 4b01004ee39341e9
+55 7cdaad060ab457eb
+56 840f63891a698fd7
+57 d3ba0f9e805b7554
+58 83c02f326b03de5c
+59 dc0f7234027fcfec
+60 d577ac007ab36785
+61 27ef217ac19606fe
+62 ae0eab1ba7921352
+63 61d51fb0c37606c9
+64 4d68a4f53232b93e
+65 2ab4a2c379acca97
+66 a6ff6df606d13d04
+67 8448a45a8f1bf9d6
+68 fac392893f32467a
+69 69d833566b5d812a
+70 f5990dbd67fcca68
+71 87094ef5fe0e7d2f
+72 1da5d4119564fa03
+73 28008eb285f38c37
+74 039c161ddff738dc
+75 719c4576c94316f7
+76 c344e87e868d621c
+77 ebdea6085daf1567
+78 16dc793d1658904c
+79 a89ae74a68849d01
+80 0bf3da73e77b4b77
+81 c3d61ce7e7e92a00
+82 82ddc61cdc25693c
+83 669de0a7fffa67e7
+84 1a8ee5f7fe5b40c6
+85 4eb08ea2d6fc504e
+86 9074d6115600653a
+87 fd4d07880464b083
+88 38e5d85e724b5ef8
+89 fa9942c38f88d9eb
+90 bda5629b5083b231
+91 bca99570933b9eda
+92 757870d300d9f0a8
+93 cb1c8768fcab2a2d
+94 d6d779dd1a37eb51
+95 4ec7039afb12a05b
+96 51ffce5b6ed82caa
+97 d752ec35a4dd2019
+98 0fc7c2f21340534f
+99 8042bf5401118f60
+100 04afbec99a926cf5
+101 9a647eb79390b82c
+102 92462299eebf292c
+103 600846bb8d2f043b
+104 d3af25266777a655
+105 3454ed653f21c621
+106 d010b48ebc862caa
+107 478183931dd96715
+108 4b526179a90b863a
+109 1038dbc311135586
+110 f76a66cee9d9005d
+111 f4a2b580e4a9e2bc
+112 219af23bcfc52a67
+113 025e7499ada5f745
+114 082e842094668b1d
+115 bb104804b8d0046a
+116 c6348c32808ab0d4
+117 2ee47e39c5206567
+118 315860cf8162dcb6
+119 6c856aedc5675c1c
+120 c200959d08975e97
+121 7dd35987ffca01a2
+122 341ff932b7d9d50b
+123 a5352a0045b9433f
+124 b41e3fa008517092
+125 edd764b5cdb17649
+126 6978de8c0bb82ee6
+127 1bc76c753574bd9c
+128 b38c68f999a31995
+129 a4c74eea399a3d10
+130 19f850a443892816
+131 e5d39278604b97ca
+132 3bc67d014fe64dec
+133 02e6b56d9e402dc1
+134 8cca714ce9d82c2b
+135 be72270164972e97
+136 0c8c6a5eba2443fe
+137 07acfc4bd14d75fd
+138 f794828cd335373c
+139 ee41e3ea56fa1270
+140 fd04fed742aa25cd
+141 9963c9809fd02bd8
+142 26ccef1fc4f1be9f
+143 f2066c37fb666c0d
+144 334a2bbb13f8a0bc
+145 061a3a6b4ea0d498
+146 994847a68abd3c5b
+147 7ed2d4eac28291f7
+148 29bd2cdab8e07407
+149 293f9f84ae7fac8f
+150 d0d21413c21d9edb
+151 73d9846bc4b4c93e
+152 c656356f774c6ec9
+153 477b0a968bdaa881
+154 fcce9f1a9cf16b42
+155 c8fd252458b178a8
+156 bc5fac9a1f8c9f89
+157 39117768d55300fa
+158 032f5c5049be87fe
+159 968f48369da7661b
+160 2d64a3dbceee6b69
+161 e81d66fee1fb20bb
+162 ee2c2ccbe46c4a5d
+163 fde4b1f67a713df3
+164 60e729ef455a36c1
+165 972cdb747f820c63
+166 29d3cbe039f88763
+167 57afa0e606105985
+168 abf5ed8839e802f2
+169 9167264e5abb57eb
+170 d25b4bb7f9f71737
+171 18ca9bd2f69def21
+172 221f6d420801640d
+173 8559e9bba4e20896
+174 eadeaaf8ff8f3889
+175 e0732f403d9ef843
+176 e55efa6fde401a7a
+177 48852c90fd64d8a9
+178 dea36e77b031f399
+179 1649bdd244537a85
+180 22161997b2fd0539
+181 6607f7eb1d952747
+182 f2bbdbf8056d1ee7
+183 aea7dcce96c475c7
+184 76c934533f0a17dd
+185 810a9c68ff1e7f7b
+186 f39fd9231fd70d79
+187 d619d8c3ad0f4a7b
+188 5ced80284764d21b
+189 d27515edf993570c
+190 c90fc86fa8423658
+191 327c741278538478
+192 1ea647eb66879e97
+193 68a28bdfca0d71a3
+194 953d139ec85e6ef3
+195 ac9136624cdf015e
+196 98d6433636a7c74f
+197 ea68bfc2acc73543
+198 2e797fe79dfc49c8
+199 c68e03cb04d21c35
+200 2ae2cc130a6fc679
+201 9b6ed10fee854b0c
+202 e742eda1df7b3e2c
+203 5ff03eb62f1fe3a8
+204 55a137e231f42565
+205 84e6afd8b172f4b2
+206 aa292eaaac5dc663
+207 4bbf8682069fc5ae
+208 5272350837bca72f
+209 02cf6353f92992a3
+210 930bcb48a9d0181b
+211 02f612535861df0c
+212 6e0f1b5904528483
+213 e5f3543d3adda6fc
+214 52ffdb930e6b971a
+215 c56d55b9fbc49046
+216 629d48d5374b1f68
+217 453a125eb292ed38
+218 cfa8d2528762664f
+219 9f1b170b2fb11b95
+220 ab917f65401f8df2
+221 dcf28ef4096fca8e
+222 077af42b57136f0c
+223 afa1eeda6a495381
+224 1603afbf0b8245f6
+225 d52a94390167e5ae
+226 b50260c6d051a30d
+227 ee270f53ec560833
+228 3d0b72b412917fac
+229 bcb034e18231230c
+230 2a0367eb3de46cf8
+231 a209974e5148a88e
+232 aca54e92e0d4e775
+233 96df6e95f587d448
+234 aaf56293e9d12d07
+235 42835ba72d2a248c
+236 a57657f7addeba74
+237 35d0bc1fc49516ff
+238 78abf509c0f8490b
+239 589e07b8a0050fc4
+240 51a8d01983d36c7f
+241 f33313bbc858eed1
+242 740a6bbc4c49c8ac
+243 204d5cd5838a8b13
+244 3c8b51018dcb2b32
+245 e49a569a34303135
+246 59eace2392a91ac1
+247 e8a1528828326d7c
+248 b3c1318d795d9ad0
+249 9bb6fc08709aa89c
+250 56c8f1e748d754a0
+251 b0244595e8bdd5cf
+252 8362d02d1c880e9f
+253 8a8d374de007c7e7
+254 60b2a9c25263d51d
+255 4a457d7563e02a1a
+256 bf3f31d33d787930
+257 4feedea5f1058b10
+258 5a982caa8921d621
+259 97e5be3027021daa
+260 263aa54bf3e6c67a
+261 8f40647fadce0bc8
+262 40ff4eca1c8a5fed
+263 365ebc4314d7ed47
+264 04a1e2c9a0feb8f0
+265 c1762b0ea0098970
+266 fc6381d231e3f862
+267 a2c277bca1f32075
+268 5b78623916f57639
+269 91134d1431224396
+270 a6470025a0344f40
+271 43aac96263ef4041
+272 e630f3dff8764467
+273 20174c344c5138b9
+274 2954d9018d59d00c
+275 8c71b92986523a67
+276 e642a2f727cd8c05
+277 dcad5b6abbf948e4
+278 b0fa26a9c1cef279
+279 a1e147c149d3fa65
+280 6af4edd79c078af2
+281 f9f83d9df6aee074
+282 641a1ebb3201ce54
+283 5659e295a3a6a613
+284 ac89b3c84e67d953
+285 9303e69e0115ba9b
+286 fb9ec4e7d55b773c
+287 43a95f70e1be88e1
+288 c9a910065c650def
+289 374218bd6b2bf6d8
+290 86309d1715dc5b9c
+291 ab7117a6b706ebad
+292 c2b44a6fc1822ca4
+293 08868b2f8f65d1dc
+294 a335fe65d7728d20
+295 fc2ec7e5f4c84b23
+296 97e8997183ad21b9
+297 19e42b4768236700
+298 43cf76f06a59df3a
+299 cfeab764efe6a58d
+300 a4e2637c3d4f64a2
+301 e28c4b2f82a8d246
+302 de8b175435cb681c
+303 0ccb5156b6733237
+304 cfa78d9c83e6e02c
+305 bbea180358f683a7
+306 2b9626725fd46597
+307 52dd3ebc9f446a04
+308 f96e1ddb88b5e778
+309 5d3cacfaae5f1910
+310 ea74e83a8371ec23
+311 8040d849abdc2706
+312 06df95b30c18cd5a
+313 7b392824b511d570
+314 0856c38b266eac21
+315 5d60a80a31458cae
+316 007cd46305727965
+317 15d9cc22547582d7
+318 0d61e6bf04e40b43
+319 6a98896cd8d0e515
+320 4273713214cfc1e4
+321 cea7dd7e906820c5
+322 ee9dea80fc76fa51
+323 77b0132b639ae806
+324 a9159e0ef307eddc
+325 418f8792c9b31eb0
+326 4c710d36cb3c3177
+327 a0b63e1b6d6cdd0a
+328 e40ceb74c6a0eea0
+329 17c3bdfd20b534dc
+330 bb624db0595a571f
+331 3b26bc613fe5ad00
+332 d525deead3c75b15
+333 770582b6a2c45435
+334 6aee11daecf1690e
+335 cddf52bab29ad7a8
+336 970c3cb9907393ed
+337 4e4a590ea1a81e51
+338 a85dcc5d486e9e77
+339 44a5a59946b6ec90
+340 881a9e71713305e1
+341 8fe4be8f3ae64c3d
+342 0387518a3bf69cce
+343 e045cccbd10f89ef
+344 b6bc1ccc6945fce1
+345 398b2a1da394513b
+346 db692f1481031c53
+347 e6be13e512f2c724
+348 8e698bebfdeacd63
+349 862b5c8f5af102ad
+350 39a2142b9bc96642
+351 761de015b7d12167
+352 fc16d5193869e2bb
+353 467581f0956b553d
+354 d57cc2e78ffb3440
+355 bfba62d14e5c271a
+356 75b4f83706599969
+357 224b0e9840a8d558
+358 92aa53d1293fefbc
+359 7fb44c2ba97805cf
+360 352c4006086677cc
+361 748323d0c802f625
+362 ee6f46e46e5cdb47
+363 89ff190512c42c9a
+364 c70bc393bc44477f
+365 b4ec636d1aefca1e
+366 129bb8f0c9566c56
+367 e32d548b16c232c9
+368 afe153e343cf2e9a
+369 8b13b5abea7b30f5
+370 d4f80d4971c11a35
+371 31b24d3ddeaa83fd
+372 3b06381cfcb192af
+373 6774bc2d35911785
+374 c66e426acbafde60
+375 abf878fa64ab4b85
+376 5c1440b904953566
+377 6f371b43a3e85a3f
+378 e286a7ef5f85f5d2
+379 3898db40f2649f82
+380 602a25c37fb3b601
+381 0f1fb6826bbebf4b
+382 1ee5c76a4891d07d
+383 057b1d16fcde955a
+384 ca4276aa2e2b309b
+385 c2ea9828b99842c2
+386 15171a833c54facd
+387 498fd620b4de3186
+388 ed7aff3b0841e451
+389 70c064d3b79c4413
+390 034e9c614d828f83
+391 fdae137a756264e1
+392 59eff58b199ffd58
+393 9b855fdb519d6516
+394 8460ad66afde0d4a
+395 752257e2ca348678
+396 f28901df9be964b9
+397 cec89818ba833d3a
+398 4601ecd70b57eade
+399 6824dc9d0b13187c
+400 9749dbf5816f173d
+401 23bf836885bc964f
+402 c068cc39c77fa60e
+403 8197c200f1bfa6a5
+404 1eb0b16f5cfd3f74
+405 91156152a5ae18c6
+406 5e8da91dce2d2ed0
+407 239b60b45d4d6c47
+408 bdde5f8fb4f381a0
+409 3e16fa8e7e7d9fc4
+410 7d37e3c174ed23ec
+411 d69d0433662cfc82
+412 118c1b2953255f9e
+413 96ff9696f5e6bbc9
+414 1a46793fdb7d53b5
+415 4d8599ee50b453fd
+416 f17d1a285e3c7ef3
+417 77a0efeca94c7749
+418 e9b9bfdd50b5acb1
+419 0945fe4a9d5d90fd
+420 b64c2ee8adefeb59
diff --git a/goldens/audio_throttle.log.bin b/goldens/audio_throttle.log.bin
index 148c0ab..ef5cbcd 100644
Binary files a/goldens/audio_throttle.log.bin and b/goldens/audio_throttle.log.bin differ
diff --git a/goldens/audio.log.bin b/goldens/audio.log.bin
index fb01682..2f2eca3 100644
Binary files a/goldens/audio.log.bin and b/goldens/audio.log.bin differ
diff --git a/goldens/boot.log.bin b/goldens/boot.log.bin
index c6d8597..31735a9 100644
Binary files a/goldens/boot.log.bin and b/goldens/boot.log.bin differ
diff --git a/goldens/bundle.log.bin b/goldens/bundle.log.bin
index 3407de0..a2baa64 100644
Binary files a/goldens/bundle.log.bin and b/goldens/bundle.log.bin differ
diff --git a/goldens/demolish_bundle.log.bin b/goldens/demolish_bundle.log.bin
index abc2e1c..4b7899f 100644
Binary files a/goldens/demolish_bundle.log.bin and b/goldens/demolish_bundle.log.bin differ
diff --git a/goldens/demolish_node.log.bin b/goldens/demolish_node.log.bin
index 2980a50..1614bae 100644
Binary files a/goldens/demolish_node.log.bin and b/goldens/demolish_node.log.bin differ
diff --git a/goldens/demolish.log.bin b/goldens/demolish.log.bin
index f100eee..101aa8a 100644
Binary files a/goldens/demolish.log.bin and b/goldens/demolish.log.bin differ
diff --git a/goldens/draw.log.bin b/goldens/draw.log.bin
index 3d95e02..95124be 100644
Binary files a/goldens/draw.log.bin and b/goldens/draw.log.bin differ
diff --git a/goldens/ecmp_cost.log.bin b/goldens/ecmp_cost.log.bin
index 0409c04..ba6611d 100644
Binary files a/goldens/ecmp_cost.log.bin and b/goldens/ecmp_cost.log.bin differ
diff --git a/goldens/ecmp.log.bin b/goldens/ecmp.log.bin
index d8ce2eb..5d16406 100644
Binary files a/goldens/ecmp.log.bin and b/goldens/ecmp.log.bin differ
diff --git a/goldens/flow.log.bin b/goldens/flow.log.bin
index 3d95e02..95124be 100644
Binary files a/goldens/flow.log.bin and b/goldens/flow.log.bin differ
diff --git a/goldens/forecast_preview.log.bin b/goldens/forecast_preview.log.bin
index 51297b4..2a0cd8e 100644
Binary files a/goldens/forecast_preview.log.bin and b/goldens/forecast_preview.log.bin differ
diff --git a/goldens/forecast_shift.log.bin b/goldens/forecast_shift.log.bin
index f0ef496..a45bca2 100644
Binary files a/goldens/forecast_shift.log.bin and b/goldens/forecast_shift.log.bin differ
diff --git a/goldens/growth.log.bin b/goldens/growth.log.bin
index 7585193..832d008 100644
Binary files a/goldens/growth.log.bin and b/goldens/growth.log.bin differ
diff --git a/goldens/health_lose.log.bin b/goldens/health_lose.log.bin
index fb01682..2f2eca3 100644
Binary files a/goldens/health_lose.log.bin and b/goldens/health_lose.log.bin differ
diff --git a/goldens/health_win.log.bin b/goldens/health_win.log.bin
index 96307fb..319685b 100644
Binary files a/goldens/health_win.log.bin and b/goldens/health_win.log.bin differ
diff --git a/goldens/juice.log.bin b/goldens/juice.log.bin
index 695e566..a22a4b8 100644
Binary files a/goldens/juice.log.bin and b/goldens/juice.log.bin differ
diff --git a/goldens/lose.log.bin b/goldens/lose.log.bin
index e3dc727..9534249 100644
Binary files a/goldens/lose.log.bin and b/goldens/lose.log.bin differ
diff --git a/goldens/node_health.log.bin b/goldens/node_health.log.bin
index c4cf698..6c51417 100644
Binary files a/goldens/node_health.log.bin and b/goldens/node_health.log.bin differ
diff --git a/goldens/pause.log.bin b/goldens/pause.log.bin
index c7196dc..bd78398 100644
Binary files a/goldens/pause.log.bin and b/goldens/pause.log.bin differ
diff --git a/goldens/place.log.bin b/goldens/place.log.bin
index d8a920c..6aa8877 100644
Binary files a/goldens/place.log.bin and b/goldens/place.log.bin differ
diff --git a/goldens/qos_auto.log.bin b/goldens/qos_auto.log.bin
index 2321b95..478d62f 100644
Binary files a/goldens/qos_auto.log.bin and b/goldens/qos_auto.log.bin differ
diff --git a/goldens/qos_contention.log.bin b/goldens/qos_contention.log.bin
index f28a323..56b01e3 100644
Binary files a/goldens/qos_contention.log.bin and b/goldens/qos_contention.log.bin differ
diff --git a/goldens/qos_emphasis.log.bin b/goldens/qos_emphasis.log.bin
index df61696..e8d5e62 100644
Binary files a/goldens/qos_emphasis.log.bin and b/goldens/qos_emphasis.log.bin differ
diff --git a/goldens/qos_manual.log.bin b/goldens/qos_manual.log.bin
index 0b3edb3..a317027 100644
Binary files a/goldens/qos_manual.log.bin and b/goldens/qos_manual.log.bin differ
diff --git a/goldens/qos.log.bin b/goldens/qos.log.bin
index 6179869..04507a8 100644
Binary files a/goldens/qos.log.bin and b/goldens/qos.log.bin differ
diff --git a/goldens/router_ceiling.log.bin b/goldens/router_ceiling.log.bin
index 18555f4..f055ab3 100644
Binary files a/goldens/router_ceiling.log.bin and b/goldens/router_ceiling.log.bin differ
diff --git a/goldens/router_tiers.log.bin b/goldens/router_tiers.log.bin
index de4b035..2f8df4d 100644
Binary files a/goldens/router_tiers.log.bin and b/goldens/router_tiers.log.bin differ
diff --git a/goldens/sla.log.bin b/goldens/sla.log.bin
index 8917231..e62d2ae 100644
Binary files a/goldens/sla.log.bin and b/goldens/sla.log.bin differ
diff --git a/goldens/surge.log.bin b/goldens/surge.log.bin
index 2bdfb81..2f5f914 100644
Binary files a/goldens/surge.log.bin and b/goldens/surge.log.bin differ
diff --git a/goldens/terminal_types.log.bin b/goldens/terminal_types.log.bin
new file mode 100644
index 0000000..fa47cd9
Binary files /dev/null and b/goldens/terminal_types.log.bin differ
diff --git a/goldens/warn.log.bin b/goldens/warn.log.bin
index a296010..803b636 100644
Binary files a/goldens/warn.log.bin and b/goldens/warn.log.bin differ
diff --git a/goldens/win.log.bin b/goldens/win.log.bin
index 3d95e02..95124be 100644
Binary files a/goldens/win.log.bin and b/goldens/win.log.bin differ
diff --git a/goldens/node_health/10000ms.png b/goldens/node_health/10000ms.png
index 4ae3211..c49b4a6 100644
Binary files a/goldens/node_health/10000ms.png and b/goldens/node_health/10000ms.png differ
diff --git a/goldens/node_health/20000ms.png b/goldens/node_health/20000ms.png
index ab27915..3dd0de3 100644
Binary files a/goldens/node_health/20000ms.png and b/goldens/node_health/20000ms.png differ
diff --git a/goldens/terminal_types/05000ms.png b/goldens/terminal_types/05000ms.png
new file mode 100644
index 0000000..311c087
Binary files /dev/null and b/goldens/terminal_types/05000ms.png differ
diff --git a/goldens/terminal_types/30000ms.png b/goldens/terminal_types/30000ms.png
new file mode 100644
index 0000000..380b821
Binary files /dev/null and b/goldens/terminal_types/30000ms.png differ
diff --git a/goldens/surge.t1 b/goldens/surge.t1
index fc97f52..ea12410 100644
--- a/goldens/surge.t1
+++ b/goldens/surge.t1
@@ -3,4005 +3,4005 @@ t1 1
 demo surge
 seed 4243
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 250679b1940fb87b
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
...[ELIDED: 7861 middle lines of sequential tick-hash entries — head 75 / tail 75 of 8011 shown]...
+3926 bfa64c594f862362
+3927 5767975538f10232
+3928 b4ed7890e394f9b8
+3929 bfc2dabb1878b522
+3930 094a4c183bac3aad
+3931 b24af9ec08889cf0
+3932 e4d4d3d39b5032b5
+3933 f86e2420d1f64dc2
+3934 664e2d7a31474f29
+3935 729b850cddb0ed97
+3936 c67d6dc6a8faac50
+3937 d0d854a37f5140a9
+3938 ddeddd1acfa53562
+3939 04e839c3786fcb14
+3940 3d993fd5d76a52bf
+3941 54fa31fd365ed1dd
+3942 6cd99f9efeb3be92
+3943 92d98ecea8b17224
+3944 21cd4f1aeef9c25f
+3945 f23aa30189e1769a
+3946 43d59b80e23e7c5f
+3947 fa06bf56764adb8b
+3948 b4b4a275f4cb1c3b
+3949 d9b40d61fe0a3745
+3950 066cee9df1fd8da0
+3951 cc740324f3691afa
+3952 539fb7e8f6742f4e
+3953 55e6fecc14dbf219
+3954 3a7b5e37582b61cb
+3955 aa2217d9f30ecc2e
+3956 aec223728dfb2280
+3957 dc4f69e8e14f0fe2
+3958 fea002d5a0c0573a
+3959 61f6c15d00b2d4ef
+3960 b28ab5cb780dd47d
+3961 6aecc0b2887bd102
+3962 73c3a0fd69020eca
+3963 244fddbda2347cba
+3964 708e60a19e56f2f5
+3965 27000f96a765f95f
+3966 01288e103663b392
+3967 7cb415ebd2355eac
+3968 065d87d2cc597423
+3969 35fb5047e213de27
+3970 bd383a70d79ec639
+3971 3cab2c69517910af
+3972 85bb84cf2d5e59ed
+3973 bb4dcb2ef2d235e1
+3974 45b3c9f20c0fb761
+3975 ae83acbf951df8a8
+3976 719a29dfa73964e8
+3977 c77b5a2503ea9ad7
+3978 f216e143896f009d
+3979 0092a5d2695fa1ff
+3980 00c36e1b5976aa56
+3981 8d22c40676f0e133
+3982 4bbf052af750b70e
+3983 f5e8f63d31cbd4e2
+3984 2735964081ee1f8d
+3985 190e91bac5c687ae
+3986 ffb4288cab8847e9
+3987 e6d4fe45755b27fd
+3988 7e2acf60d2bdff84
+3989 0a573adb2bcb81c6
+3990 ac887686c645934c
+3991 3d60b46c62fb41c7
+3992 2d6582966b15b926
+3993 87a5f2173555a9d5
+3994 284a137af289d1bd
+3995 7c949da4f9fb6181
+3996 eec43a2802e35162
+3997 bd6a340b7129c4c0
+3998 18081fccdf9c1d4a
+3999 5b0be3d36b9925a1
+4000 10995501faf46239
diff --git a/goldens/health_win.t1 b/goldens/health_win.t1
index e1ef0a8..4e574b4 100644
--- a/goldens/health_win.t1
+++ b/goldens/health_win.t1
@@ -3,3045 +3,3045 @@ t1 1
 demo health_win
 seed 4243
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 250679b1940fb87b
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
...[ELIDED: 5941 middle lines of sequential tick-hash entries — head 75 / tail 75 of 6091 shown]...
+2966 9aa451dc48e07cf8
+2967 8507e9d7b14d5157
+2968 70d8c1825c97d004
+2969 0e75d6e2132492e3
+2970 fa8e072aa4ba6a34
+2971 50a59bbe5caf6bee
+2972 04d8aece019fce00
+2973 7ceeb033cb609c88
+2974 5b8dbe9321fae309
+2975 3ff01a70c028a146
+2976 001fa5c5a62da80b
+2977 719465a5c3e5bcac
+2978 16c92fef19c43cf8
+2979 6d83dce4e6fbfeb5
+2980 7a2dd4449180d534
+2981 897519850936de45
+2982 ef9dbe40c1917368
+2983 915483b49fcd38ee
+2984 e7815923598fa26d
+2985 4e361e5234021671
+2986 a11efdb7b2ebf622
+2987 f2f6984b52dd8bcd
+2988 ccef83583b47796d
+2989 0784e8b794b1e42d
+2990 1ba269f55ffb02a1
+2991 36dd1ace0ad96ad0
+2992 e1d19ed30cbc9226
+2993 a740ef22af001e18
+2994 eb3be15bd5152094
+2995 e7ab5edb36aa9b91
+2996 a10f41f5ae4877c6
+2997 213aaa828e98dc8c
+2998 086b9323028f39db
+2999 011a0f06274f6938
+3000 cefb20d3095c78f2
+3001 a8dc8aaf6c73bcf9
+3002 a8dc8aaf6c73bcf9
+3003 a8dc8aaf6c73bcf9
+3004 a8dc8aaf6c73bcf9
+3005 a8dc8aaf6c73bcf9
+3006 a8dc8aaf6c73bcf9
+3007 a8dc8aaf6c73bcf9
+3008 a8dc8aaf6c73bcf9
+3009 a8dc8aaf6c73bcf9
+3010 a8dc8aaf6c73bcf9
+3011 a8dc8aaf6c73bcf9
+3012 a8dc8aaf6c73bcf9
+3013 a8dc8aaf6c73bcf9
+3014 a8dc8aaf6c73bcf9
+3015 a8dc8aaf6c73bcf9
+3016 a8dc8aaf6c73bcf9
+3017 a8dc8aaf6c73bcf9
+3018 a8dc8aaf6c73bcf9
+3019 a8dc8aaf6c73bcf9
+3020 a8dc8aaf6c73bcf9
+3021 a8dc8aaf6c73bcf9
+3022 a8dc8aaf6c73bcf9
+3023 a8dc8aaf6c73bcf9
+3024 a8dc8aaf6c73bcf9
+3025 a8dc8aaf6c73bcf9
+3026 a8dc8aaf6c73bcf9
+3027 a8dc8aaf6c73bcf9
+3028 a8dc8aaf6c73bcf9
+3029 a8dc8aaf6c73bcf9
+3030 a8dc8aaf6c73bcf9
+3031 a8dc8aaf6c73bcf9
+3032 a8dc8aaf6c73bcf9
+3033 a8dc8aaf6c73bcf9
+3034 a8dc8aaf6c73bcf9
+3035 a8dc8aaf6c73bcf9
+3036 a8dc8aaf6c73bcf9
+3037 a8dc8aaf6c73bcf9
+3038 a8dc8aaf6c73bcf9
+3039 a8dc8aaf6c73bcf9
+3040 a8dc8aaf6c73bcf9
diff --git a/goldens/pause.t1 b/goldens/pause.t1
index 8767617..7b055a8 100644
--- a/goldens/pause.t1
+++ b/goldens/pause.t1
@@ -3,2005 +3,2005 @@ t1 1
 demo pause
 seed 4243
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 250679b1940fb87b
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
...[ELIDED: 3861 middle lines of sequential tick-hash entries — head 75 / tail 75 of 4011 shown]...
+1926 a6bfe8bdaf548cde
+1927 8629fff86e528e9b
+1928 7849414a78ee1d97
+1929 15473545868ba38b
+1930 40e8655739abc12b
+1931 05cff6a9553b5df7
+1932 3645b5420a7dbafe
+1933 cf0aac85c45d59e5
+1934 120dea0dbf0c0a79
+1935 d202e9d4d1525151
+1936 14e2d538a348af1a
+1937 5d1a0529d6ccf998
+1938 6b345f4ec468cdbb
+1939 ab7272485fd7c6b7
+1940 555d9e3031e88cb9
+1941 48ac9a8d0e37a79a
+1942 cd65b8b409470718
+1943 e004265e97070bc6
+1944 1db5f14215b5e545
+1945 284e7d8df9ae372b
+1946 674b749251a1b08b
+1947 e20ae52084a1ea09
+1948 7ea9867fc1cf4287
+1949 54f86dd8ddc07780
+1950 14bcc35e65e58948
+1951 7196153645a3f695
+1952 998e8873a23cad31
+1953 bf8d20215d33b110
+1954 d5d4f3317d18cba8
+1955 a66f14dd0e17f1f5
+1956 937d4307f2b82e06
+1957 08faee1a3028e409
+1958 91ba0ac3066357b5
+1959 8dd1dbceb1ed7214
+1960 9d1f39b3f4527154
+1961 a02e97af2b539903
+1962 8bfb8759ee345260
+1963 dad4378c64dd7ffa
+1964 6036438a4ae3f77b
+1965 afdfbcf9824630c4
+1966 502564f317fd2c48
+1967 a485a6ac846fbf83
+1968 f4d117eafd5e6ba2
+1969 ba2a55dc926e8923
+1970 06c524f795e8528f
+1971 1c5bbe7b783eb223
+1972 9053cce22b0b297d
+1973 ed3c576078db73c3
+1974 ef66c28e93a73186
+1975 92cd16ed8c6784c1
+1976 eafe42c795476db9
+1977 806fc5eb8cb16906
+1978 75fe533bd92ae17c
+1979 89e0c7987f4bf4f8
+1980 7e3e65aeb37f4397
+1981 c71ff1ff56cbdc49
+1982 73f0741353db0b5a
+1983 85f1efbcfd6e17e2
+1984 7b8c941b42c575ed
+1985 715766091c002e05
+1986 97d2cc2510ce776a
+1987 2f080471fe90db88
+1988 e5d492d7267e3571
+1989 b3b6a8147cae45c1
+1990 d0f8f1d413c9a198
+1991 9a0b195093f7d5c9
+1992 77fc55ebb0778c81
+1993 f93b0c538679ecc1
+1994 b00aa16f885e1e71
+1995 5d72e943e9b8a953
+1996 4fea7c9fe689a6b4
+1997 a3d854b5f768303a
+1998 19223fc5a4bed111
+1999 4ed35e79ba83b516
+2000 706830b71ee1488e
diff --git a/goldens/growth.t1 b/goldens/growth.t1
index 4b258cd..7632e99 100644
--- a/goldens/growth.t1
+++ b/goldens/growth.t1
@@ -3,1805 +3,1805 @@ t1 1
 demo growth
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 250679b1940fb87b
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
...[ELIDED: 3461 middle lines of sequential tick-hash entries — head 75 / tail 75 of 3611 shown]...
+1726 1314cf19a0efd396
+1727 93e7c9ece2715d9a
+1728 8ac9201a96ea1f00
+1729 02f30efdaceab51f
+1730 58b502f651053af9
+1731 14e98d86ff9707a8
+1732 94b1f07f41043cbd
+1733 1c69d1d3d3df18a0
+1734 10f4e860f3f14218
+1735 0a948da8c0431910
+1736 efcfaaad5929b361
+1737 e609faa0c88944dc
+1738 597b153401eebada
+1739 84ebd3cc34869e6b
+1740 93689cae7202d3e5
+1741 dda102b28f1859a5
+1742 e8ab50fef4182d6a
+1743 c1922686d5265e33
+1744 295bc025df0d1319
+1745 5a5940172935baa0
+1746 89e790968cf01765
+1747 d668f7f392f4e95e
+1748 607ef3469184b542
+1749 c587582615fecffc
+1750 5cb71966123bd2b9
+1751 d62768a572f0c77e
+1752 ec4977425d98ae23
+1753 ef395393c227cd81
+1754 9ab882970aa1b54c
+1755 b03e7ff6b4b275a6
+1756 484ef00d34218d57
+1757 490576de1d88e7c0
+1758 98ed49b09f898443
+1759 ed9c6c5f5c33e532
+1760 2a5c1e332a482858
+1761 eb6288234180bee9
+1762 f96939e1d8839087
+1763 eb547c49988152df
+1764 b76af208fd76df99
+1765 02494780bd6bf841
+1766 301f472a2e0ae8cb
+1767 85aa6c4c6b8ce2bb
+1768 6ba4ae68d8c1f07a
+1769 71e575c7174e6fcb
+1770 3bd5f6778f0e6683
+1771 fd13248ad3bc13ca
+1772 3c61f7f560787c14
+1773 3f2c90c652d4b32f
+1774 5a4f605c635d9a95
+1775 8d64a26dacb42293
+1776 43ebbc54392cdba3
+1777 6a7616b86110ec7b
+1778 797cf6f3d6cc2d3c
+1779 dbe0597826d42c97
+1780 a51783a3c215e895
+1781 c6ad6bd5ecba5f15
+1782 881097664ce8e586
+1783 acd02f7ab7ce0172
+1784 802c6531599360a4
+1785 a60c605691297441
+1786 8201240f52288819
+1787 6eb9316949af5cb6
+1788 97a8d80110f03fce
+1789 40d2d73771736ab6
+1790 7a63f23e6593cdcf
+1791 86a85f3d3da4d05e
+1792 49ad2f9e1040c1d8
+1793 58eaa7e5adf0348c
+1794 bfacd1ef85b33ed2
+1795 318ae6d132467c84
+1796 0ec709c649eed68a
+1797 7ae22697406ab01a
+1798 9afd3533176e194b
+1799 eb970b5044dae578
+1800 f6e52e6400bc460b
diff --git a/goldens/warn.t1 b/goldens/warn.t1
index 0042f0c..4091c0a 100644
--- a/goldens/warn.t1
+++ b/goldens/warn.t1
@@ -3,1505 +3,1505 @@ t1 1
 demo warn
 seed 4243
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 250679b1940fb87b
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
...[ELIDED: 2861 middle lines of sequential tick-hash entries — head 75 / tail 75 of 3011 shown]...
+1426 c88b4ce3c71ceda5
+1427 176754e807920b99
+1428 7fdda5e8ae348ed3
+1429 f7636b652b1f0553
+1430 1702e453d278a830
+1431 65fc70765f802971
+1432 79d46c8283b2669e
+1433 f378ba904fb2bb5a
+1434 38e6cb70732e783a
+1435 8e1d5e54768e4d8f
+1436 c4d9c8c4befaf059
+1437 dfb7fcafbd6f76a1
+1438 9d9a24f5b8bc63c3
+1439 1a058ced7e9fe0e7
+1440 05768c2cb273f350
+1441 c822b2e1cb8e0551
+1442 d059917b55d12811
+1443 193b00542852b1ee
+1444 fa36800eed470d28
+1445 933d22f690cbb33e
+1446 a6f776f640ad9295
+1447 f03dfc60c92dc2af
+1448 88640f8eb3420f28
+1449 7623172cdeac79a1
+1450 10b598bff44449db
+1451 4eefe953b2ea1146
+1452 b82f0241abe10912
+1453 47a7cdd12a628780
+1454 436a3908af3aa7f7
+1455 a44913d65176f132
+1456 a013cb875d87076e
+1457 c315872fbadf3623
+1458 82c6b023b25a97cc
+1459 3c329c70661b0548
+1460 d05242d218bb96b5
+1461 20c00d5bf644d404
+1462 da85b91cc52277c4
+1463 54404f50c81081eb
+1464 81d66f5501f6ee10
+1465 16df0351396ca115
+1466 244bdc6d34381adf
+1467 8472e99aae4df2dc
+1468 a423d7ba38d8bda6
+1469 4916902863ebb8b1
+1470 f2d3eb877a9cade9
+1471 6d3032d021303d3f
+1472 a7cbd2e0d9f6b4ca
+1473 c87a3a28b4ceb437
+1474 7c9f67c56f026ef0
+1475 f72785d0bdb431ca
+1476 f0007acd5721cfd6
+1477 c19a8346cfe0c520
+1478 080ab97c6e43dc78
+1479 998d3ef6c6282bb8
+1480 68fc945045de6fc8
+1481 1dc812eb674e78e0
+1482 8e763ba4df2cfd83
+1483 0058f871df364c4a
+1484 3594439c727e5c8a
+1485 e7bd456e53b608e2
+1486 fa962533c6959506
+1487 1389f0b16d5a1568
+1488 aa3862572c96dcc8
+1489 5426fd42ee1b6a05
+1490 93458fbd7683f530
+1491 870d8f774afec737
+1492 c346dd6ca1806276
+1493 4588010625170df8
+1494 bf3f130fc266eb33
+1495 f3c2984765feeee8
+1496 b57d551fb920d282
+1497 9f138cc5ef8472a2
+1498 6ebb215d5427bb15
+1499 fd318d21dfdc3147
+1500 bcd51cbb1c43fc02
diff --git a/goldens/qos.t1 b/goldens/qos.t1
index 35b0efe..c63d2d0 100644
--- a/goldens/qos.t1
+++ b/goldens/qos.t1
@@ -3,1505 +3,1505 @@ t1 1
 demo qos
 seed 3003
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 250679b1940fb87b
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
...[ELIDED: 2861 middle lines of sequential tick-hash entries — head 75 / tail 75 of 3011 shown]...
+1426 d5f94aaf89e9961d
+1427 3b417a145225b93a
+1428 2cc7e4012f935a34
+1429 f8413402fade10f6
+1430 4f2c88f2c5919235
+1431 1ab4a0cab23b5053
+1432 0ccd02ce8b45851d
+1433 57d89859fd853ca4
+1434 172a3ea12011beb8
+1435 8181bc908c6a7e44
+1436 ac77750e2ee0c627
+1437 da3552aa0985c8d3
+1438 c4107bf03e136e29
+1439 a38a50314cc3ea51
+1440 2bd24c41a5fbd213
+1441 48358c9b8de2672c
+1442 dd478b33fca7772d
+1443 639b66b2665c5bc2
+1444 7c6ce6878e971832
+1445 0ee78ccf2ca939f0
+1446 300e0ec1ed7de256
+1447 11580a967b98811f
+1448 7cb45dc9f4326ac4
+1449 68ee43f755891c48
+1450 680ee30efa130c0d
+1451 7708ee86842e65a7
+1452 fea29ecbcf3cdec4
+1453 fced2109a19b7dda
+1454 b315bc516a418e77
+1455 ef273823a9427cf3
+1456 15e2587051b128a7
+1457 d763e34a41af90e4
+1458 3cc83362d17cf54f
+1459 896dae65e202e90e
+1460 a7528df6a65fa280
+1461 34c25358f79ebeba
+1462 b826324548ee876d
+1463 dd65eabf380cd783
+1464 3eb9540442b1f1a7
+1465 e45f11a76c53e39d
+1466 b2c83fc50b1f383e
+1467 048c9ecaa659a5c1
+1468 5d54c6d7caa0c388
+1469 121efe12ac45099d
+1470 54d5a6827e375ceb
+1471 8992a32b521c3089
+1472 29854d6e5830670a
+1473 6dc937d8fd62bf41
+1474 88cb15a6ca737860
+1475 194bfb2e1dcce1b7
+1476 88af0009bc7b4a61
+1477 a513b070289ef311
+1478 cc38e245591a95b9
+1479 81e95f1bf936afeb
+1480 ef9046a6eefa4b76
+1481 544faf51b146c3e3
+1482 29e5e51be51679bb
+1483 3c5ebb72cbb880fa
+1484 e450a450bfb9cc35
+1485 f9a417a0ee48b5c0
+1486 4e9ba75b000f2a21
+1487 1f76e7baf637664c
+1488 c6618797e844dfbc
+1489 b263c522c6b73517
+1490 ad2debbd2bbeaf32
+1491 b92d9114c7550a21
+1492 e0d93a5e838fb7c5
+1493 9054199bebf0a5d1
+1494 b143de52f9468b5e
+1495 28ccbb30d784069e
+1496 125ceb1b36d2d1e6
+1497 ce3d70074a9ad1c2
+1498 c9ecffaaeffbbbdc
+1499 5b89b360677d8f8e
+1500 f782422036104fe9

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
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.11-terminal-types/r2/lens-out/architecture-g1.json
using your file-writing tool, then stop. (Your source value is: architecture)
