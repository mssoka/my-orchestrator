You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. The repository checkout at the reviewed state is at:
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.11-terminal-types-r4
(all verification reads happen there; treat it as the source of truth).

Chunk orientation: This chunk contains the fold-critical and NEW goldens: boot.t1 (the canonical fold-proof demo), node_health.t1 + terminal_types.t1 (the demos that spawn the new terminal classes), the input-parity t1s, and every binary golden stub (.log.bin/.png — 'Binary files differ' lines).

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
diff --git a/goldens/audio.log.bin b/goldens/audio.log.bin
index fb01682..22c8783 100644
Binary files a/goldens/audio.log.bin and b/goldens/audio.log.bin differ
diff --git a/goldens/audio_throttle.log.bin b/goldens/audio_throttle.log.bin
index 148c0ab..e9ceb15 100644
Binary files a/goldens/audio_throttle.log.bin and b/goldens/audio_throttle.log.bin differ
diff --git a/goldens/boot.log.bin b/goldens/boot.log.bin
index c6d8597..2bf73a6 100644
Binary files a/goldens/boot.log.bin and b/goldens/boot.log.bin differ
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
diff --git a/goldens/bundle.log.bin b/goldens/bundle.log.bin
index 3407de0..410b7d5 100644
Binary files a/goldens/bundle.log.bin and b/goldens/bundle.log.bin differ
diff --git a/goldens/demolish.log.bin b/goldens/demolish.log.bin
index f100eee..1314554 100644
Binary files a/goldens/demolish.log.bin and b/goldens/demolish.log.bin differ
diff --git a/goldens/demolish_bundle.log.bin b/goldens/demolish_bundle.log.bin
index abc2e1c..815e96f 100644
Binary files a/goldens/demolish_bundle.log.bin and b/goldens/demolish_bundle.log.bin differ
diff --git a/goldens/demolish_node.log.bin b/goldens/demolish_node.log.bin
index 2980a50..2566981 100644
Binary files a/goldens/demolish_node.log.bin and b/goldens/demolish_node.log.bin differ
diff --git a/goldens/draw.log.bin b/goldens/draw.log.bin
index 3d95e02..cf3b36a 100644
Binary files a/goldens/draw.log.bin and b/goldens/draw.log.bin differ
diff --git a/goldens/ecmp.log.bin b/goldens/ecmp.log.bin
index d8ce2eb..a8467d3 100644
Binary files a/goldens/ecmp.log.bin and b/goldens/ecmp.log.bin differ
diff --git a/goldens/ecmp_cost.log.bin b/goldens/ecmp_cost.log.bin
index 0409c04..5af0b4b 100644
Binary files a/goldens/ecmp_cost.log.bin and b/goldens/ecmp_cost.log.bin differ
diff --git a/goldens/flow.log.bin b/goldens/flow.log.bin
index 3d95e02..cf3b36a 100644
Binary files a/goldens/flow.log.bin and b/goldens/flow.log.bin differ
diff --git a/goldens/forecast_preview.log.bin b/goldens/forecast_preview.log.bin
index 51297b4..6efbc6f 100644
Binary files a/goldens/forecast_preview.log.bin and b/goldens/forecast_preview.log.bin differ
diff --git a/goldens/forecast_shift.log.bin b/goldens/forecast_shift.log.bin
index f0ef496..79d125d 100644
Binary files a/goldens/forecast_shift.log.bin and b/goldens/forecast_shift.log.bin differ
diff --git a/goldens/growth.log.bin b/goldens/growth.log.bin
index 7585193..7901ed9 100644
Binary files a/goldens/growth.log.bin and b/goldens/growth.log.bin differ
diff --git a/goldens/health_lose.log.bin b/goldens/health_lose.log.bin
index fb01682..22c8783 100644
Binary files a/goldens/health_lose.log.bin and b/goldens/health_lose.log.bin differ
diff --git a/goldens/health_win.log.bin b/goldens/health_win.log.bin
index 96307fb..3b2f3d8 100644
Binary files a/goldens/health_win.log.bin and b/goldens/health_win.log.bin differ
diff --git a/goldens/input_parity_draw.t1 b/goldens/input_parity_draw.t1
index 5724349..d834f0d 100644
--- a/goldens/input_parity_draw.t1
+++ b/goldens/input_parity_draw.t1
@@ -3,17 +3,17 @@ t1 1
 demo input_parity_draw
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 12
-1 485414581be6a892
-2 4032cea4b72de819
-3 7d59ff0782386364
-4 ad9b5271276b00e3
-5 aed68eaa9c0fd54e
-6 b8c8c7264d760e15
-7 fca1e7c57945b780
-8 28b1c62bd725bbcf
-9 91df56a669cf7d1a
-10 2970575cd55c6e21
-11 6826ff85b5aeac4c
-12 60e4fbb740869acb
+1 763eb2a9e0d0a992
+2 c3013be5f28a1ead
+3 c323f7dc716e98d4
+4 6796427039eaac37
+5 4c24a52e203041be
+6 090ff9ce170e58b9
+7 ad371847898ffd40
+8 5a7bd6273f0651d3
+9 b3594847bc483fba
+10 7177c1affcdf5ab5
+11 ad153a0f9be4015c
+12 6ced3e0c02345e7f
diff --git a/goldens/input_parity_draw_wide.t1 b/goldens/input_parity_draw_wide.t1
index 5234f41..54c56b6 100644
--- a/goldens/input_parity_draw_wide.t1
+++ b/goldens/input_parity_draw_wide.t1
@@ -3,17 +3,17 @@ t1 1
 demo input_parity_draw_wide
 seed 42
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
 ticks 12
-1 88bbf1972c0dd40c
-2 0e6d66a8ba912ddf
-3 6cddb5144cd927fe
-4 5d6e68746cbd45a9
-5 9d37ad3ccfb47b68
-6 87035f2a50d953db
-7 3e2c5c7f2069017a
-8 d884dc2f1c780095
-9 804075389d742334
-10 49b1ae0db5423947
-11 a9b1743f5cd1f646
-12 62bed067625b64f1
+1 b6a68fe8f0f7d50c
+2 e3429296d26fe9d3
+3 b2a7ade93c0f5d6e
+4 697017205bbf765d
+5 3a85c3c053d4e7d8
+6 d74a91d21a719e7f
+7 eec18d0130b3473a
+8 0a4eec2a84589699
+9 a1ba66d9efece5d4
+10 3fb259b40042a07b
+11 ee9faec943074b56
+12 1cc0540f4786a345
diff --git a/goldens/juice.log.bin b/goldens/juice.log.bin
index 695e566..ebbbda8 100644
Binary files a/goldens/juice.log.bin and b/goldens/juice.log.bin differ
diff --git a/goldens/lose.log.bin b/goldens/lose.log.bin
index e3dc727..287d9c8 100644
Binary files a/goldens/lose.log.bin and b/goldens/lose.log.bin differ
diff --git a/goldens/node_health.log.bin b/goldens/node_health.log.bin
index c4cf698..54d4eb8 100644
Binary files a/goldens/node_health.log.bin and b/goldens/node_health.log.bin differ
diff --git a/goldens/node_health.t1 b/goldens/node_health.t1
index 51d203d..7ec805b 100644
--- a/goldens/node_health.t1
+++ b/goldens/node_health.t1
@@ -3,425 +3,425 @@ t1 1
 demo node_health
 seed 4243
 logic_hz 20
-catalog_hash 66c4324a06058860
+catalog_hash 17d3baf8c6e1df7f
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
+1 eaed7b4553ac1940
+2 dc1e3a5e566b96f4
+3 178f2a139baa37e4
+4 b7b7b656a6a9dac2
+5 4947e09ecf76b2f0
+6 433f16ccb13a2a39
+7 403ccd79d0a802f4
+8 81d76c48e92c3982
+9 f06005968260518f
+10 b19809b944f1965d
+11 60ab6bf41cf5b508
+12 b1dbfdb3c7077f50
+13 dc49c59cfe4e7dcd
+14 9572fe2dd863026c
+15 5d538658d314b20d
+16 9fbd867ca8d06f8b
+17 b4bebe3134419608
+18 b8292e420467e49d
+19 61fefb77eee818e2
+20 6cb0db9b4c3bbd27
+21 7ffe567c3b2d51d8
+22 3dcc95b8c8fad14e
+23 1f70e3aef6833861
+24 22bda8fad751df5a
+25 b04db644e63ee941
+26 22c83e53ca0c1032
+27 fcef5c210635d779
+28 10a2b14c39a27638
+29 24a28b0166a28fce
+30 ba1b9f7875a4e8ee
+31 a2bb8e579398e5c8
+32 de9f9caf38020923
+33 37f431bd0df7eadb
+34 b9de7f9205a734eb
+35 03173a3dcebf0a64
+36 d3ec3c072d41659d
+37 24340afde3fa2219
+38 cbdb7744053de942
+39 47aac94ed2007a2f
+40 bb241abd8930235a
+41 f1579b7491f38e79
+42 bcf55732587bc34a
+43 df7723a3a35b8835
+44 110687cfa3a0ce87
+45 e0d2f09015fcf3b8
+46 d94c6d0042d57c26
+47 193fb5f9f0a2c13a
+48 3faa629b54b06470
+49 470464b924a2afbd
+50 0dc46baef5a2e81e
+51 53943acaa1401a93
+52 bdde3b2ae1686682
+53 131019d652a15400
+54 f5200e2d5b838e9f
+55 982bd3ad0ffd2385
+56 96efec4cd12c76f5
+57 36ac1b4200e31e92
+58 64cfc0b593047ae6
+59 a62a7e07c4ab993a
+60 d56c5c903f46c3e7
+61 02f8e22870c64c38
+62 04a88a08daf88cd4
+63 971f432999ca6813
+64 c0a5660242a63b08
+65 2a738f87259d0dd5
+66 1323f12c423f85d6
+67 c59d00947f3fff2c
+68 f0c72903748c0a7c
+69 726f7f04fd4dc1a0
+70 69ddc547d0a98fb2
+71 f8759839a7b469f5
+72 5832bb0cd1004f85
+73 ae92ca9aba852199
+74 73622ec756aabd82
+75 b625013dc10d13b5
+76 97c2451821bc708e
+77 9f2e81236bd38e7d
+78 cafa3ba38e6ee762
+79 d1bed8d196f90e17
+80 f00280e7148bd059
+81 27ba10c171b221d2
+82 aa33991d45de990e
+83 79aabd79b5797289
+84 d4f7ecc180429cd0
+85 7a27b67ba973c6e4
+86 e33b522684947128
+87 c1776b0fdf0385ad
+88 4a04246a73d198fe
+89 b0b053e58e8e12ed
+90 09a6632bcc043deb
+91 6a05b40901431324
+92 9718564546edd01e
+93 0df621e3299baf2b
+94 c5769b998c4ccdcf
+95 1822c0a4a6385a99
+96 8c5fe51c0055cf48
+97 dd5742ef90060a4f
+98 290a828f74157ea1
+99 6d4232c78a485c4e
+100 964b6de9c4decf67
+101 b5f9c8dd3af169da
+102 8e99b0183abc3016
+103 2af60f0eb4deda7d
+104 e1fa6624a4e56837
+105 3322c23a590496af
+106 3bdb510afc972194
+107 2e6e507d5a2aba6b
+108 559596cfe68f87dc
+109 7abb76c77c8de550
+110 d2c938a58b8b0677
+111 8d41c06910d69d5e
+112 5a4286cc78b6950d
+113 e049bdb9bfa9c1c7
+114 3cf6e4c26488686b
+115 6a5ec00f0fb972b8
+116 06de27b98b1851aa
+117 dc551033a32a1bd5
+118 06ff9e8b97b581c4
+119 a4c445e9622183a2
+120 6e49fbbd10cd64d5
+121 853aa6359e661d78
+122 3277c76b23b437e1
+123 bc82824e616baa4d
+124 5dc4267d375a27c0
+125 e244a690a29ad503
+126 d7c44e9604d16650
+127 7f3ada31c692b6f6
+128 2c78e2490e910227
+129 72698a0224071d82
+130 f359b78f181de2c0
+131 d73dccd8b33ca2ac
+132 0cd6e24e48039556
+133 876a03c096c549eb
+134 2eb40ef3fd76d42d
+135 640a911344ca13fd
+136 5c7d17c03f0aafb4
+137 119514d90362b60f
+138 4b999254fa398ee6
+139 8c0743ded353eb1a
+140 05c85b1494c24f37
+141 825b8106e2a83c5a
+142 1386f872bed51be5
+143 136b6b0a35206387
+144 e600466989cbb11a
+145 0d696ef677e4bc96
+146 7bd7914fdb3dc999
+147 c06d7710136e3ffd
+148 b8e9147865407e9d
+149 0770f9f10e3b60dd
+150 30dff2f3264e3cbd
+151 d0ef5129a814ad5c
+152 f49f20e5b08b450b
+153 98d2efc28fbe58fb
+154 557ef4c0a3989418
+155 ac8e29dea8e96e5a
+156 e18739eacdf41eef
+157 d230941f03a1d11c
+158 0ff9674bdf3a1974
+159 9b0840b4a0b1c189
+160 e6596cfc3ea22e8f
+161 d3c5bcf5d342b975
+162 5562670ab7d51a63
+163 18c7557d9658c135
+164 86baebafeb5a0733
+165 e79c46f0070649c9
+166 e8655df40c426e9d
+167 e707a108f90b96cf
+168 7d3ffc9121e692b0
+169 96168daab633d315
+170 72f89b18c5fa4099
+171 0f5d672c8dbbdaa3
+172 d42db0da9ad631d7
+173 df4ea539d90d6690
+174 7e59d2ecd721c877
+175 345f6973280c37e9
+176 4782202e5ad40050
+177 fe720d112823ffbf
+178 d6d054b0528d5877
+179 54b5df439f5751a3
+180 c9ab26ccac99f1c7
+181 ef8581fe510e7f01
+182 2915bbee2a2b5e71
+183 0ff0e4f773f1b951
+184 858ac2672078c6d3
+185 e92469c35b28f75d
+186 f6d43e15b35a699f
+187 0cf8562b8dc6eeb5
+188 02a1992390d87811
+189 026960892d87be0e
+190 ca659582b51cefda
+191 14f786a86a12ce2a
+192 43636688085af3e9
+193 c6f203bf8ccd9db5
+194 52c229be868e26d5
+195 1996cdbf42e2b820
+196 e44f98208e0cd629
+197 6beb80197cc9290d
+198 acccdecabcfc65be
+199 5875e57674a23b0f
+200 7642a362769e081f
+201 17f2e733535b201e
+202 e0c055ab6c8464c2
+203 a6be2caecf20908a
+204 c5bd7b86913aff2b
+205 d2da1cc06390a9e0
+206 4ab419bb1e158349
+207 d9617350ae453810
+208 5e5e38e7ac37f46d
+209 3152126ee6b9a2a1
+210 2797d5ef70ff8bfd
+211 c6561d637a6abff6
+212 fd391018e3803a79
+213 6a3597c0aaf98a46
+214 5dd11b657843d65c
+215 afe967d1efe15a94
+216 b52bf80f94251162
+217 af477cbf7dbafa86
+218 4d1e4853117bc03d
+219 0dd496a850818313
+220 dbf0abecd52172d8
+221 507b947f7f676bac
+222 44f95badc4169602
+223 78315ad08f4c8413
+224 31adf5520a7e5fa0
+225 a2d01ca0f2d93540
+226 3868ff82dfbcd383
+227 2923d601c5d7f789
+228 4f9b875c02b9bab2
+229 66cb44a22e2af352
+230 caa728f46b9e431e
+231 01d2c473c3b28eb0
+232 d97470c0487ad3d7
+233 a38948c258c4f3a6
+234 68a3d17647d80131
+235 99d98ea6dbb599e2
+236 7cb3c171f81b42b6
+237 f211eb85a67d694d
+238 09189147a4c2bd95
+239 acd7f8aeda2853b2
+240 dc16a7e11eb523c5
+241 dcc403ef97122c03
+242 c8bfe3d378402bfa
+243 5ff9c615f3998495
+244 c0ed2bb9ae06d588
+245 c939dbf6fbeb6283
+246 4eb603fbb61ace1f
+247 4983117b9e8bd2ba
+248 e21a9ca24712b4b2
+249 195bec97a4ad73d6
+250 cfd319f4b208297e
+251 2c51603d9ec968c1
+252 a0193ee1d33414e9
+253 019e6feae35dfa2d
+254 b6a24fe80aac73bb
+255 3b9f0ddfe30efee0
+256 769e8259afd6d6b6
+257 defe4e54db85d0aa
+258 ebd131a19b9917ff
+259 d6778b6a60efbe14
+260 e2fe89ceb6a07e98
+261 336693b79b75adb2
+262 22e5f0a439408303
+263 d21f2b8a166bd6ed
+264 5186789c67ea9442
+265 18b4327768d5ef3e
+266 2a42367c72c3894c
+267 0790edd1037e7157
+268 50af3a9a10f521df
+269 c6bc5f80d1e48cf8
+270 0769347badd64f3e
+271 3943e5d986a9a58f
+272 a577313e84f3fff9
+273 317aa69f88b31f5f
+274 d85b26310ee52556
+275 26ee4cedafb70b1d
+276 c3965e65105d548b
+277 e18f9dd3d3b228a2
+278 3d8f8a3f59e56e53
+279 1af64fdb3b85ddff
+280 748063ea467580e8
+281 306e84890c0ce30a
+282 df71f438f355cbea
+283 5215058cb02b87c9
+284 37f7a5898811ab89
+285 32adf495609feb3d
+286 c8485641ee38c762
+287 22fd41199421e97f
+288 dc13858bdc3d2ad5
+289 994c0276f092c532
+290 c16d1411032bd49a
+291 663c3b123357419b
+292 45e21f37154f2a56
+293 c65cc35768510cce
+294 550cc667ea43174a
+295 109cf23d8c623515
+296 01c1567202a3ba27
+297 06dc7d264dbc5b22
+298 3bf43ee5b4f286c0
+299 9ef55e32ac1818ab
+300 840981c1c5d253ac
+301 8f113f01ab89185c
+302 18ae268cff0d745a
+303 9dda59e0991fa4f9
+304 007906de60bb6256
+305 0814f41f67b74de9
+306 57e62cdfa3684101
+307 c1bcec8ff53e9776
+308 73f24a871fd303da
+309 1092418f04b7f2a2
+310 9b7368fed0bb7135
+311 3b48b977f7f7ec14
+312 9ef54325e834540c
+313 bb0d08087dd341b2
+314 64bf7224c3da931b
+315 ff8906887585d0cc
+316 0d22f797ee3cc753
+317 5693043af8bf434d
+318 5db57645cbf16cf1
+319 9ecc72fdd44c9587
+320 9fedc7b80656db96
+321 3ae57d915dd94e0f
+322 5dc5b475a11195c3
+323 a6efe9d19b8f544c
+324 377a2206d74de1e6
+325 dc44bc2bd9eb5eb2
+326 20e8244ab9982245
+327 6f931dfb9b18d4b0
+328 1e4769403c0e8e1a
+329 31bb5f60e9f1c196
+330 4bc3bdc9b688e22d
+331 9c49a37f27cd1c8a
+332 25d7909dd80b8dd7
+333 aa7aaae871096bcf
+334 979bb09df6f4abc4
+335 742e384fe9649ff2
+336 6116d47a6234a97f
+337 0b0d01e89d450b8b
+338 7222075a1d1be165
+339 799722af9a42e9f2
+340 f2c41ddb3526fc5b
+341 ad6b5469d705ff2f
+342 93edd8e0f119e9ac
+343 37c0216f9a5f7dbd
+344 6e270a4f19b9d773
+345 e1aa9b01a632fc19
+346 3385b54d1e0ccd61
+347 df0a0bc8292f081e
+348 32d099217e2fa161
+349 1fc9123b4fac3e97
+350 c7a25e97194e04a0
+351 62170fac63a987ed
+352 672120547eb44d61
+353 c1f3bcada588d9ef
+354 ad4b215a2b2f5c92
+355 9d69c9bd56f91df0
+356 c6d9ae492121bef3
+357 f642d637332a242a
+358 2dfbd9e65d3d2d66
+359 1dc0911b143421cd
+360 ebb299822decbe3e
+361 9c79f0fd7a2d565f
+362 8e1d8c4fe0caaf6d
+363 d47c953e1dbc9908
+364 9354da2466ff5835
+365 f1ee079427ffc52c
+366 8acca88ce6c35e4c
+367 2ad2d5cbdaa7322b
+368 10c12c1695a73fa8
+369 8e89a29e6419b9c7
+370 b4d4f6c7219ebe1f
+371 e75cdcdf2706fbcf
+372 75a5a9ff23f1b2cd
+373 69bb63178fb4afbf
+374 8e99118d444dc1c2
+375 3f9c5e3f515b0fdf
+376 7fac3c2339d5ed84
+377 cc1d567cb71793c5
+378 95e5f3308e3c66a0
+379 c3d8763cd54d9ab8
+380 852850b7e6144413
+381 40a988b0dd2a2889
+382 e91a30dcacd6b58f
+383 688e5190b40ac340
+384 c1846be43460c849
+385 d340a76b3b681010
+386 4509ff83f7c63327
+387 97d0855e78d7c224
+388 afbb30b20fba7cfb
+389 1538343a954a9189
+390 bc75b02ad2792c01
+391 eccb52bb85b167b3
+392 2795caafb62a6512
+393 d4e505ac6e37aa0c
+394 1b115ce6d7fd20a8
+395 f37aebe161c370b2
+396 f458f7ae79993073
+397 aff80011e4995740
+398 21557053bb8c74c4
+399 7f97e354ae504776
+400 2303e048cc9f3113
+401 780e1511ff984f2d
+402 e63f14bcbfaff6f0
+403 0c24b1439eaae83f
+404 7da0e3c7e3dc6a9a
+405 bd1d1e4a204607c4
+406 35bf94581557129e
+407 056addf950525669
+408 70c1bccf9f684512
+409 1e388c790a70da4a
+410 c634ecc5b2ad6f02
+411 20e01482e29a6c58
+412 34a9675c68f07318
+413 295e0e9c598c5187
+414 073142144aa4c517
+415 acb83b0cd89f9747
+416 3bddfc12b420bbcd
+417 8fbe9e80a39789ab
+418 bbb8bb71a89963a7
+419 5018511e33614b57
+420 505e1e5c1fbcf36f
diff --git a/goldens/node_health/10000ms.png b/goldens/node_health/10000ms.png
index 4ae3211..c49b4a6 100644
Binary files a/goldens/node_health/10000ms.png and b/goldens/node_health/10000ms.png differ
diff --git a/goldens/node_health/20000ms.png b/goldens/node_health/20000ms.png
index ab27915..3dd0de3 100644
Binary files a/goldens/node_health/20000ms.png and b/goldens/node_health/20000ms.png differ
diff --git a/goldens/pause.log.bin b/goldens/pause.log.bin
index c7196dc..44095ac 100644
Binary files a/goldens/pause.log.bin and b/goldens/pause.log.bin differ
diff --git a/goldens/place.log.bin b/goldens/place.log.bin
index d8a920c..d875e43 100644
Binary files a/goldens/place.log.bin and b/goldens/place.log.bin differ
diff --git a/goldens/qos.log.bin b/goldens/qos.log.bin
index 6179869..557cc6d 100644
Binary files a/goldens/qos.log.bin and b/goldens/qos.log.bin differ
diff --git a/goldens/qos_auto.log.bin b/goldens/qos_auto.log.bin
index 2321b95..53d8964 100644
Binary files a/goldens/qos_auto.log.bin and b/goldens/qos_auto.log.bin differ
diff --git a/goldens/qos_contention.log.bin b/goldens/qos_contention.log.bin
index f28a323..365d3f8 100644
Binary files a/goldens/qos_contention.log.bin and b/goldens/qos_contention.log.bin differ
diff --git a/goldens/qos_emphasis.log.bin b/goldens/qos_emphasis.log.bin
index df61696..8b55734 100644
Binary files a/goldens/qos_emphasis.log.bin and b/goldens/qos_emphasis.log.bin differ
diff --git a/goldens/qos_manual.log.bin b/goldens/qos_manual.log.bin
index 0b3edb3..b87ec94 100644
Binary files a/goldens/qos_manual.log.bin and b/goldens/qos_manual.log.bin differ
diff --git a/goldens/router_ceiling.log.bin b/goldens/router_ceiling.log.bin
index 18555f4..47bbcc6 100644
Binary files a/goldens/router_ceiling.log.bin and b/goldens/router_ceiling.log.bin differ
diff --git a/goldens/router_tiers.log.bin b/goldens/router_tiers.log.bin
index de4b035..b7a042f 100644
Binary files a/goldens/router_tiers.log.bin and b/goldens/router_tiers.log.bin differ
diff --git a/goldens/sla.log.bin b/goldens/sla.log.bin
index 8917231..a6cfb93 100644
Binary files a/goldens/sla.log.bin and b/goldens/sla.log.bin differ
diff --git a/goldens/surge.log.bin b/goldens/surge.log.bin
index 2bdfb81..c47f7a3 100644
Binary files a/goldens/surge.log.bin and b/goldens/surge.log.bin differ
diff --git a/goldens/terminal_types.log.bin b/goldens/terminal_types.log.bin
new file mode 100644
index 0000000..d639a72
Binary files /dev/null and b/goldens/terminal_types.log.bin differ
diff --git a/goldens/terminal_types.t1 b/goldens/terminal_types.t1
new file mode 100644
index 0000000..f2ad9cd
--- /dev/null
+++ b/goldens/terminal_types.t1
@@ -0,0 +1,647 @@
+# t1 manifest — per-tick FNV-1a-64 state hashes (full sim state)
+t1 1
+demo terminal_types
+seed 42
+logic_hz 20
+catalog_hash 17d3baf8c6e1df7f
+ticks 640
+1 0c123ba45ed3a973
+2 67880ca65b639944
+3 7322669417b86758
+4 2e202c7852fd1956
+5 325e85e721139a76
+6 9071af2556a00348
+7 df0b2aa6bd2746de
+8 7e1c40d425d8698b
+9 e677dfe3c334e1c6
+10 0e126945f91f8d55
+11 231632816943394f
+12 91ecc83b7d1272db
+13 315f185699af5269
+14 3847fa074bd85110
+15 6b410c551e9ace4f
+16 4a32ccdfb704e665
+17 d3024ffec87049ec
+18 f7d980ce4dda30bc
+19 36f9bd98d9795528
+20 e0fafc5427d52ff2
+21 950de7ee5c441479
+22 177a3e052d725ce7
+23 8dd1a7e4b88b61b6
+24 a9bc86de52bb10cd
+25 59fd67513471782f
+26 eba8f9ccc97d65fa
+27 c2b2038838e53254
+28 5903bc84b701d64f
+29 3b82dd76c84c86f8
+30 c1460b1654e12752
+31 7729cb10db193591
+32 6a1631a439876a09
+33 6cf7a13c6018c4d2
+34 1640b51521f14178
+35 600560656e85ae9a
+36 d7787dd01b64ab07
+37 f865b47b77b55b6c
+38 53301de1a562ea2b
+39 cc8229b73f8fa513
+40 f46df796e4f4271d
+41 5e5460feff310cc7
+42 f0b6ce598d981bb4
+43 95042fc742ef199b
+44 0a744deebd7a8a5e
+45 32cabb8cd7d0f9e2
+46 d903ebd2c12bfeee
+47 18a44d6efdd95123
+48 8644d5a52fd635f3
+49 06c9dc5201cc1efa
+50 c4fe408e57cdadf6
+51 a1f7476ca010435b
+52 1e7cc7945e0c217a
+53 2999896689428d45
+54 20bed7c16d590d7a
+55 2a8d04fe8e42f717
+56 94ec57138befa3e1
+57 123a54f59d1790d8
+58 fb73c6306ff2926e
+59 1c460f5064ba15c2
+60 76736f53c507b898
+61 9445f22ec964becd
+62 0b9db722d8c057aa
+63 2615a34417a8e4bb
+64 dcbc53aa1655561b
+65 6680efeb9b3c5d40
+66 4999267789e58019
+67 0f409cef198985f9
+68 c1cfe03169fe4f78
+69 7480004f3ec47437
+70 fadfffaa1e845d3e
+71 5c1b84771fa1ecb3
+72 77f965d0586911a4
+73 3ae42cac7dee0e78
+74 05114af8ee80b554
+75 235e52aeaf0eeb78
+76 db842d0ea115766e
+77 9799e4fee5e0ba73
+78 fe753cf9a172244f
+79 03e1b7f5b22b9651
+80 d442669bb136bf10
+81 eccdbd89b09b94af
+82 144f3f9049b22f28
+83 ff3df59db167068c
+84 3d77658c8baf9318
+85 6391550f14d5d209
+86 ba54708a64f68aaa
+87 85a72a3fa9eb2d40
+88 74fdd6ee938951c7
+89 b824f201e025a92e
+90 b9776860daa3c969
+91 b30f5e41c298227f
+92 768ab3deaff9ea72
+93 e913ed7aaa899eb5
+94 72bed867adcbd243
+95 1d38e44bf4b3efb4
+96 ba2179425ed533fe
+97 2c6fe8d5a0c2fc25
+98 df22d5feb0ca8a3d
+99 ca1b0bb7553a610a
+100 c5b8c271420bc316
+101 6f63599e408d546d
+102 c970aff78a8769d4
+103 e19803a8350c3df2
+104 faf964142d7807f0
+105 2b160246054517c0
+106 8fb7f79b3b0ba030
+107 68f4b4d5bd98e766
+108 f06173c6922852ea
+109 62925a1aa18b56c8
+110 47a7cb8876ab324e
+111 3199a785f4ead4c9
+112 00830abe4e8bae29
+113 e0476aaebf21cfce
+114 a6ab5cec87f72aa3
+115 08f36ed16bfac9cc
+116 355cd9961392a4da
+117 eeb74247897a2e9c
+118 bb825ba2171465bf
+119 1c54df4d757a5554
+120 f40982e390cae3a3
+121 7e98a40c108986ea
+122 aca03e714188bc3c
+123 e38ddf34e5f61e79
+124 8914d032abadfa1b
+125 4eb3e5ba57e6bb0f
+126 0fabf1f96880c4ac
+127 0779d8eac54cedcc
+128 e3e73a182111ff93
+129 d67ee0854ed12f76
+130 4474dc245af63e98
+131 4225e622a42ce521
+132 6450374fff9ac6a7
+133 e8123194836269c1
+134 4c063afe2683f25e
+135 12d224a84a0c7908
+136 90838e6e6aeb6dff
+137 317ada105f03b9cb
+138 41b815ce317d5fac
+139 5f43e6a49ba14c4a
+140 9e1aabc7d1f8b65a
+141 7ff12fd86a69ae5e
+142 271d8f7b87b9fd3c
+143 de02d8bd28e7c335
+144 4cada97979328e9c
+145 7ac994a520f5adb7
+146 008ab060aeb78e80
+147 cc9f03b404ffbda7
+148 cd55a94eae4d2335
+149 8bd601195e548294
+150 09b79a8803456735
+151 ce56e81f4ad1cee9
+152 3c31ae46ee63f493
+153 f053aefde79be39d
+154 184094aa70906717
+155 dc0e5194336dfd9c
+156 ddda64b10f39c58e
+157 ee62f8f6aae2a2e5
+158 f0d5c8a404c665bf
+159 f4794f58bb7aa45a
+160 3773b88a06b87f2c
+161 46659621b4dc1d36
+162 4af2cb781d337087
+163 ba9a097147210c6a
+164 743fd4a77c3eff79
+165 ce4063e4e25c0517
+166 789c45f57fea49bc
+167 48f5acae5aa2e062
+168 b93c386a59dd80af
+169 23f3c08bb499ed8c
+170 7022e95358563ed7
+171 0c1438127424594b
+172 0642bf0f5fa05033
+173 4679544df6d90c6f
+174 2ccb45e294791fdc
+175 225c43e3ffc9cb9f
+176 af7b0cdbcc2c83d2
+177 9e47b8cc6a27da34
+178 2b51594d3eddf88e
+179 b7e73ad4524f63ea
+180 01f52d2bab62efc4
+181 5a680b3381dd5b10
+182 a6788db5a6eb4296
+183 b8c1a4f814205e03
+184 b2e05e1ee90c5d16
+185 1faac48018655534
+186 57292b052030a609
+187 0c75d20eb85d6acc
+188 db06955e621b8650
+189 ba912854513b33fa
+190 807fb7af3b47fb93
+191 98869d1dd50edb5b
+192 7e154eae64244e75
+193 84111cf4c870dff2
+194 32c04cee5ab5c8f4
+195 898732bcddad05b0
+196 1f0c0de2479d86b6
+197 187f2373402ed78a
+198 474f189950ef4776
+199 0ed16fa7cfc5eadb
+200 b87ef4b12a06c991
+201 81d11ee9970113d7
+202 16d422392d9cd25b
+203 9ed4d4ea14e994af
+204 453c17142f7abb9a
+205 e2b346e8b3a941ff
+206 3548c74d97cd121b
+207 938d5ccbf13352dd
+208 f84899524e0a60d6
+209 e16b58cda066efd4
+210 0e066c2612c70828
+211 b659e6796cfd4c25
+212 14325f6b07942430
+213 035ba91719a1f823
+214 1021a13ccd16bc7a
+215 ce5d99467eb65b88
+216 da2a4663fbfac4b1
+217 5e6177fd3bba8fa9
+218 a740cf8394123805
+219 1c9270a2ae6d307b
+220 2bd59163f304d576
+221 6a9268f9ee1dd715
+222 abef874c0f20a1c5
+223 91a3fee3caab3a2a
+224 fabef68f22045e28
+225 0fbcba8f30b7f41c
+226 976e4d000f442af6
+227 8e53885614bf3c5a
+228 6a4ba78e4c9404e9
+229 f73b34369a1aa314
+230 46d8f15c19ecffcd
+231 d20f4fa24a9fc21a
+232 8d540e48debcab4b
+233 cf6e960fd96b06ac
+234 a768159526ab5ae3
+235 d91e9b310db26124
+236 74c487f00479a1ac
+237 1073e649af78efcc
+238 f2ab3150fbda0067
+239 a7aa9aafbf408245
+240 dffd935a7693ec15
+241 87dfac99a01583f8
+242 27e17c6c4b5fe6d8
+243 52cd6afb76ba874e
+244 8f95109f185521d4
+245 ac8ad32aae3c6797
+246 9d22fc459c521c54
+247 5f3165070341b0dd
+248 81c35deb3343b82b
+249 828a27946ceb4365
+250 beef870984a14143
+251 9c56164a74ccd36f
+252 f84b6ccc53416478
+253 fce98d7ed7d7570d
+254 8c120b54db903c76
+255 061265d534122a26
+256 1bf490e6ba423704
+257 3309e620c251c5b1
+258 c60d4c3ec544a85e
+259 b0ac76378228048a
+260 3400daf70a6a2916
+261 aa944f259e48e82f
+262 4ce654ccd7b0c16c
+263 078bc4c87e1939b5
+264 07b13ba475a17f09
+265 c579bf14bb5150c4
+266 7184b584b4298bf6
+267 bf038d668a085162
+268 24e72ff409d6cdd1
+269 76e8d8dd3ab298e0
+270 6124f608cabfbc2f
+271 32bb61f79ecb494f
+272 223296c875a509e0
+273 437234c57bc541c9
+274 cc8390d0b9a7922c
+275 c1fb9a3ba4afa9fd
+276 17b21bd6aa3da82b
+277 82ce9a40e120b667
+278 ea622b61cfd85ce1
+279 4b6cd8373ebd1b19
+280 072f8db9fbca0fc2
+281 0f44f91c43eec3eb
+282 c26435fdb55bf531
+283 ab930851270f053b
+284 9fafde89e58cdc9a
+285 3dab2030223e209f
+286 94c7204bfe8fc588
+287 9a5baf08fd09e1a3
+288 eb01f3eb270e0524
+289 d03d466682f07ed1
+290 0f0145709f6e8ddd
+291 e264b34a096ddbcb
+292 c39503e0746a7efd
+293 a5fb5d45c7eda904
+294 f729ee5809e6f76b
+295 37f275193b7f5f6d
+296 ba1c79d37839b592
+297 c46038bd592de724
+298 317fc021fea0720b
+299 665730e59eca85dc
+300 3dfe3b607f21635d
+301 9d2df4f3a69704da
+302 d216dac103497be5
+303 d99727c5d3b226aa
+304 fece0fa71c22577f
+305 bc8ae2fd636e188b
+306 3d3c4d9efcc89658
+307 d3a717146686c497
+308 f15bb5e5b074a132
+309 35b66e5f30c4c31e
+310 0f5593be9b3bb14e
+311 9a9fc88822d8a149
+312 8327258491480918
+313 f1b98d5db8d4721d
+314 5f95f6ae106b949a
+315 9f87edbfc7d3847d
+316 9149309eaeafe8ff
+317 8610c88935709f5c
+318 f1d37f3e8c81f304
+319 17f2f6eb9ba5d471
+320 421f8f45bc8c3404
+321 00f0475daddf3b13
+322 0b81c320291bf9b0
+323 524efee88072fedb
+324 534eea4a9f1acf89
+325 7207d4252e2e0f40
+326 9f2375aa3b238cfe
+327 53154b175a931e83
+328 c864f9dd2a0c62d6
+329 01444f287040ed76
+330 9e7f3c241447f82c
+331 7df11b8b5d9e9a60
+332 bedbab551e06c044
+333 1e0d358876c21061
+334 dffe01bdd79fd6c9
+335 0841e0e6e5de56a5
+336 5a0bfa9d2ede39c1
+337 7a74ec88db3102a6
+338 1aacd771e759ee98
+339 1444bde4773a141a
+340 df5951884336c87d
+341 60cdd103a9b24a85
+342 0f79eac3238051b9
+343 938424f4aea2fee9
+344 594db5500ce4ce3b
+345 8077d949998db8be
+346 29bf73b7bb9e86ca
+347 90ce227d798232b2
+348 38048ab2e3fed490
+349 c7a9cae890e73c39
+350 e90f9c3c7d2234b2
+351 78e3a2184d2d0001
+352 935bb6cfc09fef22
+353 7e6cd0bd6f1b1955
+354 544f766ce8a593f7
+355 9b094eaba7d3ab05
+356 2c5837eeeb40a56a
+357 9df8779caab88e77
+358 74f4784bcf9ab4c7
+359 4dfb6a35e1e78bfa
+360 2897d75611814508
+361 465573edc19f3b30
+362 4539d3d9c6978c3f
+363 8036a5138df9b68f
+364 be1e03f5a8394776
+365 a9ce17c06f5b69c7
+366 d1e2eb71d6c2f6bf
+367 26313f839f7561be
+368 262baf01e6442971
+369 d8e1d97b48065417
+370 bce6f77133e4d015
+371 fbaa88c30fac9f22
+372 82c347c40fafd415
+373 7783a1ed2b7b5679
+374 f23813a19514ae44
+375 ec5009209c783507
+376 8aa8a36f23d08265
+377 5d4e72682a532cc2
+378 33913e0d127c6d3b
+379 1ff6199e02f4c2c8
+380 2abfadaff3f787f5
+381 4d045e2ecebf9297
+382 a90ca9d41a8c7cdf
+383 affcf5f21159fee4
+384 33846201b1bb2ec8
+385 85d7a2c2114dbfdf
+386 bf241d2768912c6d
+387 0a1eb08257631190
+388 51c82a520c5a7b9e
+389 80c001b18ce031d6
+390 1ebbef0edcc81763
+391 826984977f2933fb
+392 3741635a501396e8
+393 f3c923040bbc10d0
+394 3d779727b2ba4cea
+395 3cd7acb7781626f8
+396 542cf7a74b0ed3fa
+397 e951a6c551320629
+398 72a0223368b664e1
+399 5e7af63763f540b6
+400 be2a1507f4c6cdfb
+401 6593d468a2358679
+402 12b1e742ce0d0269
+403 9e79973b9263f3a8
+404 f5671b0a7abb44de
+405 51775a2a169a10c7
+406 c5018bf6b5e9cf5d
+407 840b3dfeb8580d83
+408 03b589001ed59c3e
+409 93beb69c73ff4dbb
+410 2d39c2d5e40e5955
+411 dcc06d5a46841c27
+412 d6e888ee5d3086fc
+413 9e3716b86cdfa19c
+414 8a208980b55fe06a
+415 9ac35b566c9c7473
+416 225bc07ee18c616c
+417 317682976457d936
+418 dc996e71de53524f
+419 a72fbc9ed4491b30
+420 6c1a9de04caecddf
+421 0b55a2516e676834
+422 5d87be1da84c7f61
+423 6392513810e176ea
+424 b1fa6d194d85417c
+425 2479328b7008845c
+426 7e04f9211ee3ac2a
+427 1728026f0e4acb81
+428 fb09f31232321710
+429 73684caf6c1440dc
+430 e0c6d996c11f5332
+431 81cb7f712e8df076
+432 09df6be94a650823
+433 e94d6a156fab0bd3
+434 940d05778335372a
+435 4e0992f21a7cdf16
+436 539e88c1ee98877d
+437 fc9b28f39d061cac
+438 5770e12244368e8d
+439 31caf23638ecda17
+440 010b7a2d05d591ae
+441 047b92f5fa79d2df
+442 44c019526108641f
+443 b66f6a93d4f2fcbb
+444 b11c4372d5d811ef
+445 a4ab1d0cdf2c17a7
+446 e2d17daf0c4e6b8b
+447 f36f572b07f6197c
+448 27e3984b2598a3ee
+449 40b6bfda2876c318
+450 e045488d068470c4
+451 e2e5b738cef24a1b
+452 b0d0949f9da2f5b6
+453 0b98187801e1a758
+454 f1e28d91c81b3d13
+455 f8c8c4d96c79f609
+456 e7396782a00daca7
+457 6191aaae37268bd5
+458 e097f789d6fe7600
+459 e2b027db347ccb4a
+460 6706e963084c53d4
+461 dd301c20f70dded5
+462 c784661fb875383c
+463 78681585e5a86f9d
+464 da2b43f4c4541500
+465 3adffffa78e94da5
+466 dfe437beef8e2a56
+467 c4873640587eae6a
+468 2c78ded7ae9afab7
+469 3890d313cf7eae62
+470 434d018b7b9daf49
+471 69aae0ac5b43facd
+472 d716f8f87d78a5e1
+473 945f2925d9d04b1d
+474 17ff8c2f2c17c253
+475 80290d538ebc7fd6
+476 5618358d0edf9ed6
+477 00e4fd226332cff8
+478 30668e82059951d9
+479 c8320c71c50db528
+480 c0f078b480c8c42e
+481 fcfcbab4b1150120
+482 96871ccf7e3b9e15
+483 465ed84bb0ba7b88
+484 d88fd233b5cdeaac
+485 7537fbb44dea35a9
+486 dafc925aa6bdaa20
+487 f9a5b8aa196e275c
+488 45cc34f9c340ba24
+489 a746d608f8a182f0
+490 4f99bae8234067c8
+491 d98fcab2a29a3816
+492 6b546c4e0b1ff372
+493 3f9a5e69cf60df59
+494 11da3f712dab74c1
+495 7dfc22ef3e13db4d
+496 2cdadb071a43af3e
+497 2ce8b64841c8b60d
+498 42ad4bc8f97826dc
+499 a40e598559723572
+500 7edc645b922b9cd3
+501 e27ad2919f819444
+502 bc6bf196aa81a8a9
+503 d3f88f4d743f092a
+504 914bc88b85f7e119
+505 ecf738dadfdcb0c6
+506 8791cb6dbc0677dc
+507 7bbf44f27cae547c
+508 d7b7d8437c5900fa
+509 8a3593da0637b60d
+510 f048a13cd16338ad
+511 4f6003cf644e0718
+512 3e39c56599271843
+513 c09ab63ffadeb988
+514 085d5e56e18b6d48
+515 0fcbdd6f4e73d267
+516 ffd93fff106492bb
+517 bfa1f9b898c5709e
+518 7502d121c757ae05
+519 35d1c328d371b09d
+520 6c532ee8d263c111
+521 bbabcc9be8170cc3
+522 e3173cfbd366eb3a
+523 341af0f056dc8f39
+524 cbc9421219079fa9
+525 eb2d2e54a7f3fd02
+526 63f3de6b9bb7143c
+527 ba8e50950b6c6f58
+528 fbb4784e63538e2d
+529 f6b247cb8c64b069
+530 1a37c41ea9f7fc36
+531 f233720f3f513557
+532 5208dffdda72871d
+533 5ab2472c8dbd5e4c
+534 4cbbd8a4f273eaba
+535 b431ed343e15738b
+536 fd68d77dac41730e
+537 caa32cf8d9ee9ee2
+538 f2ea17b1ffc3de0b
+539 5c2740e4e438c103
+540 cb1fd45909a3f50a
+541 3c5ab3cbf0516ac1
+542 c73de99d31ae3cd1
+543 678cdd55fa2235a9
+544 002b0bec6526c64d
+545 c0035a696371a9b6
+546 c833b1ed0a9a3343
+547 95ec47f4c8d0a0f1
+548 7018f83ef5e78487
+549 f15d0ea054cf5ec2
+550 4ec713ccf7b3f9fa
+551 2a42cd8696489794
+552 7c93111f021a0eeb
+553 c7f8c421284ded1d
+554 3a44ec0b200c85bf
+555 16f9f842bb685863
+556 69fd1263a3ec8cd4
+557 ebd1327cc51a8265
+558 f7db51253d07ecdd
+559 6f7599505a5b9e21
+560 a819a63958cc9bed
+561 979fe01274991be3
+562 83f396177cc4d169
+563 9db3b8ef9168183c
+564 63a7fecbf3b39271
+565 04a914bae15cb367
+566 13b1edbbe4c2a551
+567 040d741314127a90
+568 2e9b4ddd12d2b621
+569 2f8df86271d4a8e5
+570 88a0cae4d43578ca
+571 317ae639b01c10f6
+572 881588ac76bc9347
+573 ceda860224190204
+574 0fb6080114eb4bda
+575 db2ccc9f17fedffb
+576 fd060288e356b8f6
+577 49b82812ee243eb8
+578 e83b6008fdc1f93d
+579 b89899eff0eddf3c
+580 fbc765c33b9d2d4e
+581 cad62b7f8b487c84
+582 7b252158c67e5298
+583 927713c78f097697
+584 416aebcbae47e3d4
+585 8d5c20c3a972d57d
+586 8e3a56c1347ba9a9
+587 1715b0353164a664
+588 ddc6e608b8cdde41
+589 3a50981ffdd205d0
+590 56f353ee14807752
+591 927c480548344015
+592 45d52242d3ea2533
+593 d61a50a790bc91b7
+594 a7a3db7b27589acd
+595 b5b69e2a141fdb9c
+596 03c4ec8aa1b62f09
+597 af3bb543b8b87fd8
+598 f9d26b7021309b5d
+599 0921c2753525ec06
+600 86e608bfae80f3f1
+601 c404af94b56dc0e7
+602 79c40c1a9afc045c
+603 6d07b904de2bbf4d
+604 37a2b27378c1d3b2
+605 ee52ad18b6d5824a
+606 e0c9ebba15e97e16
+607 e5487c7e8ea98f2f
+608 c90049891335f22f
+609 811a2d4fbf81c9f2
+610 77eb36dc39c40aae
+611 7885ccd38be84eea
+612 17593c5b9ba115a4
+613 3c935051f299ed35
+614 5949f5ed74566913
+615 f58386364141b002
+616 b0ca96dc1431ea17
+617 c4858754efb485c5
+618 7108cb5938c1b30a
+619 84576faa04f09aa6
+620 7201a70a2a29076f
+621 3a07c2b24645e4a2
+622 911b2364b64be150
+623 4939aee621135743
+624 ab9b8f44afc836eb
+625 5fa496e8e6a2eb45
+626 a480024c9fd36cb7
+627 e51ef700d69e6513
+628 c20a9683e60c3d19
+629 a9192e0a7597a0f3
+630 3cf115992c96d36a
+631 ad06b715a3b36e2a
+632 2d3e52581d27f236
+633 8ea158232372ff09
+634 41a8355078242235
+635 195a40915503eddc
+636 05fe8d0849940b8c
+637 4fe8e574dc2d306b
+638 60b702d5d6fe08d1
+639 0dc156d14850fbb6
+640 9abe5d62fcc600b0
diff --git a/goldens/terminal_types/05000ms.png b/goldens/terminal_types/05000ms.png
new file mode 100644
index 0000000..311c087
Binary files /dev/null and b/goldens/terminal_types/05000ms.png differ
diff --git a/goldens/terminal_types/30000ms.png b/goldens/terminal_types/30000ms.png
new file mode 100644
index 0000000..380b821
Binary files /dev/null and b/goldens/terminal_types/30000ms.png differ
diff --git a/goldens/warn.log.bin b/goldens/warn.log.bin
index a296010..e6df4c7 100644
Binary files a/goldens/warn.log.bin and b/goldens/warn.log.bin differ
diff --git a/goldens/win.log.bin b/goldens/win.log.bin
index 3d95e02..cf3b36a 100644
Binary files a/goldens/win.log.bin and b/goldens/win.log.bin differ

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
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "acceptance",
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
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.11-terminal-types/r4/lens-out/acceptance-g1.json
using your file-writing tool, then stop. (Your source value is: acceptance)