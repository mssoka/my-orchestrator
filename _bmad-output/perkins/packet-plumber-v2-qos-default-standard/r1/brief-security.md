You are reviewing a code diff. You have read-only access to the repository (your cwd is the repo root at exactly the reviewed state) and may verify the diff's claims against the actual codebase using your available tools. Review READ-ONLY: do not modify, create, or delete any repository file (your ONLY write is the output JSON file named below, outside the repo).

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


--- DIFF (the review target) ---
diff --git a/_bmad-output/implementation-artifacts/spec-v2-qos-default-standard.md b/_bmad-output/implementation-artifacts/spec-v2-qos-default-standard.md
new file mode 100644
index 0000000..ad6a57a
--- /dev/null
+++ b/_bmad-output/implementation-artifacts/spec-v2-qos-default-standard.md
@@ -0,0 +1,90 @@
+---
+title: 'QoS unconfigured default — 100% Standard lane'
+type: 'bugfix'
+created: '2026-08-19'
+status: 'done'
+review_loop_iteration: 0
+baseline_commit: 'f162ba6c3ed9a31be02623e084393d16e846a25b'
+context: []
+---
+
+## Intent
+
+**Problem:** A pipe with NO player QoS configuration splits bandwidth across all 3 lanes (the `balanced` preset `[1,1,1]` ≈ 33/33/33) instead of carrying everything on Standard at 100%. This drifts from canon (user ruling 2026-08-19: "when no queue is configured, all traffic should be on the standard queue and would take 100% of the capacity. And that should be the auto. Everything on standard and 100% until we start implementing QoS") — GDD M2 "all traffic starts on Standard; QoS is player-engineered, never auto."
+
+**Approach:** Make the unconfigured state the ladder's 1-lane row (`lane_auto_reserve_ladder[0] = [100]` → Standard 100%, data-driven, no hardcoded splits) at every site that currently applies the `balanced` preset as the pipe default: pipe creation, the resting-weight fallback, serialization's absent-when-empty default, and `qos_auto_weights`' untouched-pipe branch. The auto-ladder then engages only via the player's first type→lane assignment.
+
+## Boundaries & Constraints
+
+**Always:**
+- Unconfigured pipe = Standard 100% at every read site (allocator caps, serialize, panel, auto-ladder), sourced from `balance.lane_auto_reserve_ladder[0]` — never a hardcoded `[100,0,0]` literal (ODN-5).
+- Ladder rows keyed by in-play count = player-assigned distinct lanes + Standard (always in-play, per the 08-14 ruling — Standard is every un-categorized type's home). Row values hand out in lane-priority order E→S→B. Never-drop fold applies only once the pipe HAS an assignment (untouched pipe = exactly {Standard} → 100%, per the 08-19 ruling; the E6 flow floor remains the backstop).
+- `balanced` preset stays as the app-side manual quick-set; it is no longer any pipe's resting default.
+- Sparse serialization preserved: default pipes (weights == new default) serialize ZERO QoS bytes.
+- Determinism/replay: all changes are pure state reads; the app's auto-follow write-through path is unchanged.
+
+**Ask First:** none anticipated.
+
+**Never:** no hardcoded split values; no change to the app's auto-follow write mechanism (`qos_apply_auto` / `Cmd_Set_Weights`); no touching `qos_allocate`'s largest-remainder math or the E6 floor; no silent golden mutation — every re-bless is deliberate + cause-documented.
+
+## I/O & Edge-Case Matrix
+
+| Scenario | Input / State | Expected Output / Behavior | Error Handling |
+|----------|--------------|---------------------------|----------------|
+| Fresh pipe, zero assignments | draw; no Set_Lane / Set_Weights | `qos_pipe_weights` / `qos_auto_weights` = `{0,100,0}`; caps on cap-15 standard tier = `[15,0,0]` (nothing held for E/B) | n/a |
+| Oversubscribed Standard demand | Standard lane saturated | Standard packets use FULL capacity (`qos_serialize` with ready={false,true,false} → budget `{0,15,0}`); lone packet still crosses in 2 on-edge ticks | n/a |
+| First assignment | Set_Lane streaming→Express | auto = `{70,30,0}` (in-play {E,S} = 2 → ladder row 2) | never-drop bus guard unchanged |
+| Remove all assignments | Set_Lane back to Standard | auto returns to `{0,100,0}` | n/a |
+| 2 assignments | Set_Lane streaming→Express + email→Best-effort | auto = `{50,30,20}` (in-play 3 → row 3) | n/a |
+| Unassigned never-drop default lane (future content) | banking default Express, NO assignments | untouched pipe = exactly `{0,100,0}` (fold gated on assigned); E6 flow floor backstops banking | n/a |
+| Save/load, era advance, tier change | default pipe, no QoS edits | weights stay `{0,100,0}`; serialize emits zero QoS bytes; tier change reallocates 100% to Standard at the new capacity | n/a |
+
+## Code Map
+
+- `core/qos.odin` -- `qos_auto_weights` (untouched branch + never-drop fold gating), `qos_pipe_weights` (resting fallback), `qos_pipe_caps` (E5 default_w), new `qos_unconfigured_weights` helper
+- `core/topology.odin` -- `apply_draw` appends the pipe's initial weights (line ~196)
+- `core/serialize.odin` -- `def_w` (absent-when-empty default, line ~343)
+- `core/catalog.odin` -- `Balance` struct comment (default_preset_idx semantics)
+- `data/balance.json` -- `lane_auto_reserve_ladder` comment (the 5.8 "untouched pipes keep the default preset" clause is the documented bug — rewrite)
+- `core/qos_test.odin` -- pin updates + new AC tests
+- `app/input/exec.odin`, `app/qos_panel.odin` -- comment touch-ups (AUTO derivation still holds)
+- `demos/qos_auto.dem`, `demos/qos_emphasis.dem`, `demos/qos_manual.dem`, `demos/qos_contention.dem`, `demos/sla.dem`, `demos/audio_throttle.dem` -- lane-only demos get the auto weights the app writes (intent preservation); "default balanced" capture comments update
+
+## Tasks & Acceptance
+
+**Execution:**
+- [x] `core/qos.odin` -- add `qos_unconfigured_weights(cat)` (ladder row 1 → Standard 100%); make `qos_auto_weights` drop the `!assigned` balanced early-return and gate the never-drop fold on `assigned`; `qos_pipe_weights` fallback + `qos_pipe_caps` default_w → the helper; update doc comments
+- [x] `core/topology.odin` -- `apply_draw` appends `qos_unconfigured_weights(cat)`
+- [x] `core/serialize.odin` -- `def_w` = `qos_unconfigured_weights(cat)`
+- [x] `data/balance.json` -- rewrite the ladder comment (untouched = 100% Standard ladder row, the 08-19 ruling; note the catalog_hash re-bless)
+- [x] `core/catalog.odin` -- `Balance` struct comment update (pipes no longer start on balanced)
+- [x] `core/qos_test.odin` -- update pinned untouched values (`{1,1,1}` → `{0,100,0}`); add AC tests: unconfigured 100% caps + full-capacity Standard; first-assignment engages ladder + removal returns; unassigned-never-drop untouched = exactly {0,100,0}; tier-change keeps 100% Standard
+- [x] `app/input/exec.odin`, `app/qos_panel.odin` -- comment accuracy (untouched auto == the 100% Standard default)
+- [x] `demos/*.dem` -- add the app-mirroring auto weights to lane-only demos; update "default balanced" comments
+- [x] goldens -- deliberate re-bless (tools/harness.sh save) + cause-document every shift in the PR body
+
+**Acceptance Criteria:**
+- Given a fresh pipe with zero assignments, when caps are computed, then Standard carries the pipe's FULL capacity and Express/Best-effort carry 0 (headless).
+- Given an oversubscribed Standard lane on an unconfigured pipe, when the flow runs, then Standard-lane packets use the full capacity (no reservation held for unused lanes; lone packet crosses in 2 on-edge ticks).
+- Given a pipe's first type→lane assignment, when the assignment lands, then the auto weights flip to the ladder rung for its in-play count (1 assign = 70/30, 2 = 50/30/20 from balance.json).
+- Given all assignments removed from a pipe, when the last override reverts to Standard, then the auto weights return to {0,100,0}.
+- Given a default pipe, when the run is serialized/replayed, era advances, or its tier changes, then weights stay {0,100,0} and no QoS bytes serialize (sparse contract holds).
+- Given the full local suite, when run, then `tools/ci-local.sh --fast` (lint + unit) and the full suite pass; goldens re-blessed only where behavior legitimately changed, each shift cause-documented.
+- PR body names the divergence root cause (the balanced preset applied as the pipe default at `apply_draw` + the resting/auto fallbacks, documented in the 5.8 ladder comment).
+
+## Spec Change Log
+
+## Design Notes
+
+**Why the untouched branch changes:** the ladder's row 1 IS `[100]` — Standard 100%. The 5.8 code explicitly avoided it for untouched pipes ("byte-stable no-QoS runs") in favor of the balanced preset; the 08-19 ruling overturns that: the unconfigured state IS the ladder's rung 1. Removing the `!assigned` early-return makes untouched pipes flow through the same in-play/ladder path, so the resting state is data-driven by construction.
+
+**Never-drop fold gating:** the fold keeps every never-drop class's lane in-play (so auto never zeroes it). Gating it on `assigned` makes an untouched pipe EXACTLY {Standard} → 100% (the ruling's "until we start implementing QoS"). MVP data is unaffected (all defaults pinned to Standard); the E6 flow floor stays as the backstop for hypothetical future never-drop non-Standard defaults.
+
+**Golden impact:** `lane_caps` is derived + never serialized, so T1 dumps for no-QoS runs shift only via the catalog_hash fold (balance.json comment). Behavior shifts where lanes are ready on formerly-balanced pipes: lane-only demos (sla, audio_throttle, qos_contention) get the app-mirroring auto weights to preserve intent; T2 captures pinning "default balanced" (qos_auto/qos_emphasis/qos_manual at 1000ms) legitimately re-render as 100% Standard.
+
+## Verification
+
+**Commands:**
+- `tools/ci-local.sh --fast` -- gates 1-2 green (lint + `odin test core`)
+- `tools/ci-local.sh --mac` -- full 10-gate suite green, goldens re-blessed where documented
+- `tools/harness.sh run qos_auto qos_contention qos_emphasis qos_manual sla audio_throttle` -- targeted re-bless verification before the full run
diff --git a/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/decision-log.md b/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/decision-log.md
index 7cc47a4..b0a9b60 100644
--- a/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/decision-log.md
+++ b/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/decision-log.md
@@ -1013,3 +1013,37 @@ the r1/r2 notes below), never by editing this exhibit.)*
   legacy-byte-identical draw branches. **NO T2 re-bless** (verdict C: shipped flags off →
   the blessed frames are untouched; the harness run proves zero golden shift). A future
   aesthetic ruling flips the flags; terrain-aware routing (rivers) stays a named follow-up.
+
+## 2026-08-19 — QoS unconfigured default = 100% Standard (the auto state; supersedes the 5.8 balanced-preset resting pipe)
+
+- **Decision (user ruling 2026-08-19, verbatim):** *"in networking when no queue is
+  configured, all traffic should be on the standard queue and would take 100% of the
+  capacity. And that should be the auto. Everything on standard and 100% until we start
+  implementing QoS."* This is CANON restated — GDD M2 already says *"all traffic starts on
+  Standard and the player actively engineers QoS"* + the 08-14 ladder (*"1 class queue
+  used = 100%"*) — NOT a new decision: the 5.8 IMPLEMENTATION drifted by making every pipe
+  start on the `balanced` preset `[1,1,1]` (≈33/33/33) instead of the ladder's 1-lane row.
+- **Divergence root cause:** `apply_draw` appended `lane_presets[default_preset_idx].weights`
+  (balanced) as every new pipe's resting weights, and `qos_pipe_weights`/`qos_auto_weights`
+  returned the same preset for unconfigured pipes — documented as canon in the 5.8
+  `balance.json` comment ("untouched pipes keep the default preset, not the ladder").
+- **Fix (job `packet-plumber-v2-qos-default-standard`):** the unconfigured default is now the
+  ladder's 1-lane row (`lane_auto_reserve_ladder[0] = [100]`) applied to Standard — 100%
+  Standard, data-driven, no hardcoded splits — at every read site: `apply_draw`,
+  `qos_pipe_weights` fallback, `qos_auto_weights` (the `!assigned` balanced early-return is
+  removed; the never-drop fold now engages only once the player HAS an assignment), the
+  serialization absent-when-empty default, and the E5 allocator fallback. The E6 bus guard
+  learns the auto-follow: a never-drop class's FIRST assignment is allowed when the ladder
+  reserves its lane (the settled weights, not the current default, gate the edit).
+  Express/Best-effort carry nothing until the player assigns a type to them; the ladder
+  engages from the first assignment (1 in-play = 100% · 2 = 70/30 · 3 = 50/30/20).
+- **Consequences (applied in this job):** `balance.json` comment corrected (the catalog-hash
+  fold re-blesses every golden — `harness fold-check` proves boot's tick-1 shift is the fold
+  alone; 32 of 35 demo logs are byte-identical except the 8 catalog-hash bytes); three
+  lane-only demos (`sla`, `qos_contention`, `audio_throttle`) gained the app-mirroring
+  auto-follow weights so their scenarios keep their intent; every T2 capture re-renders the
+  default pipe as a single 100% Standard band (the deliberate, cause-documented re-bless);
+  core pins moved from balanced `{1,1,1}` to `{0,100,0}` + new AC tests (unconfigured caps,
+  first-assignment engagement, removal return, never-drop untouched floor, tier-change
+  survival); the `palcheck` lane-stripe oracle sets explicit Express weights (a default pipe
+  no longer shows Express). Full `tools/ci-local.sh --mac` suite green (10/10 gates).
diff --git a/_bmad-output/pr-bodies/v2-qos-default-standard.md b/_bmad-output/pr-bodies/v2-qos-default-standard.md
new file mode 100644
index 0000000..ad08e2c
--- /dev/null
+++ b/_bmad-output/pr-bodies/v2-qos-default-standard.md
@@ -0,0 +1,57 @@
+## Summary
+
+User ruling 2026-08-19 (verbatim): *"in networking when no queue is configured, all traffic should be on the standard queue and would take 100% of the capacity. And that should be the auto. Everything on standard and 100% until we start implementing QoS."*
+
+A pipe with **no player QoS configuration now carries ALL traffic on the Standard lane at 100% of capacity**. Express and Best-effort hold nothing until the player assigns a type to them. The auto-ladder engages only from the player's first type→lane assignment (1 in-play lane = 100% · 2 = 70/30 · 3 = 50/30/20, from `balance.json` `lane_auto_reserve_ladder` — no hardcoded splits).
+
+## Divergence root cause
+
+This is CANON restated (GDD M2: "all traffic starts on Standard and the player actively engineers QoS" + the 08-14 ladder "1 class queue used = 100%"), not a new decision — the **5.8 implementation drifted**:
+
+- `apply_draw` appended `lane_presets[default_preset_idx].weights` — the **balanced `[1,1,1]` preset (≈33/33/33)** — as every new pipe's resting weights.
+- `qos_pipe_weights` and `qos_auto_weights` returned the same balanced preset for unconfigured pipes.
+- The drift was **documented as canon** in the 5.8 `balance.json` comment ("untouched pipes keep the default preset, not the ladder"), which is what made it look intentional.
+
+The fix makes the unconfigured state the **ladder's 1-lane row** (`lane_auto_reserve_ladder[0] = [100]` → Standard 100%) at every read site, data-driven (ODN-5).
+
+## Changes
+
+**Core (`core/`)**
+- `qos.odin` — new `qos_unconfigured_weights(cat)` (single data-driven source for the resting default); `qos_auto_weights` drops the `!assigned` balanced early-return (untouched pipes flow through the ladder path: in-play = exactly `{Standard}` → row `[100]`); the never-drop fold now engages only once the player has ≥1 assignment (an untouched pipe is exactly `{Standard}` = 100% — a never-drop class defaulting off Standard there is backstopped by the E6 flow floor); `qos_pipe_weights` fallback + `qos_pipe_caps` E5 fallback use the helper; new `qos_auto_weights_after` (the ladder result with a candidate override folded in).
+- `topology.odin` — `apply_draw` writes `qos_unconfigured_weights`; `validate_set_lane` E6 guard checks the **settled** weights (the auto-follow result for auto pipes, the manual set otherwise), so a never-drop class's FIRST assignment can engage the ladder (the auto-follow it triggers reserves the lane) while manual zeroing edits are still rejected.
+- `serialize.odin` — the absent-when-empty default (`def_w`) is the unconfigured default; default pipes still serialize ZERO QoS bytes (sparse contract intact).
+- `catalog.odin` / `data/balance.json` — comments corrected (the 5.8 "untouched pipes keep the default preset" clause was the documented bug; the 08-19 ruling supersedes it).
+
+**Tests (`core/*_test.odin`)** — pins moved from balanced `{1,1,1}` to `{0,100,0}`; new AC tests:
+- `test_qos_unconfigured_default_100pct_standard` — fresh pipe, zero assignments → full capacity (15/15) to Standard, nothing held for unused lanes; lone Standard packet crosses in 2 on-edge ticks (full-capacity flow).
+- `test_qos_first_assignment_engages_ladder` — first assignment flips the pipe to the ladder rung (70/30, then 50/30/20); removing all assignments returns to `{0,100,0}`.
+- `test_qos_unconfigured_never_drop_untouched` — an untouched pipe is exactly `{0,100,0}` even with a never-drop class defaulting off Standard; the E6 flow floor backstops it (Express floored to 1).
+- `test_qos_unconfigured_survives_tier_change` — a tier change reallocates the NEW capacity entirely to Standard (no silent re-split).
+- Lane-only fixtures (`lane_pipe_setup`, `test_congested_run`, the crisis construction) now mirror the app's auto-follow weights (the ladder result the app writes after categorizing); `sla_weights` helper added. Stats/crisis shape pins re-pinned to the new allocation (the aggregation mechanism itself is unchanged — one aggregated row, no per-event duplicates).
+
+**App (`app/`)** — comment accuracy only (`qos_mode_manual`'s AUTO derivation still holds: untouched = weights == auto == the 100% Standard default).
+
+**Demos (`demos/`)** — `sla`, `qos_contention`, `audio_throttle` gained the app-mirroring auto-follow weights so their scenarios keep their intent; "default balanced" capture comments updated to "100% Standard".
+
+**Harness** — `palcheck`'s zoomed lane-stripe oracle sets explicit Express weights on the wide pipe (a default pipe no longer shows an Express stripe).
+
+## Golden re-bless — deliberate + cause-documented
+
+The fix legitimately changes pinned behavior (the unconfigured allocation), so goldens were deliberately re-blessed (`harness save`):
+
+- **32 demos fold-only:** the `.log.bin` differs from the pre-bless golden in EXACTLY the 8 `catalog_hash` bytes (byte-verified per file; `balance.json`'s corrected comment folds into the catalog hash). `harness fold-check 5f86ef16ca1c0ece 0e1e1afe9129ff2f` **PASSES** — boot's tick-1 shift is mechanically proven to be the catalog fold alone. Identical commands + unchanged catalog values ⇒ identical sim behavior for these demos.
+- **3 demos behavioral by design:** `audio_throttle`, `sla`, `qos_contention` gained the auto-follow `Cmd_Set_Weights` entries (intent-preserving, see above).
+- **T2 captures re-render** every default pipe as a single 100% Standard band (previously 3 equal bands) — verified the diffs are confined to the lane-band regions of pipes. `input_parity` manifests re-blessed (fold-only).
+
+## Decisions & rationale
+
+- **"1 used = 100%" counts in-play lanes (Standard always in-play).** Standard is the default home of every un-categorized type (08-12 canon) and is always reserved (08-14 ruling) — so the ladder's rung 1 (`[100]`) IS the zero-assignment state. This matches the GDD's own ladder wording ("1 class queue used = 100%").
+- **Never-drop fold gated on `assigned`.** An untouched pipe is exactly `{Standard}` = 100% per the 08-19 ruling ("until we start implementing QoS"). MVP data is unaffected (all defaults pinned to Standard); the E6 flow floor remains the backstop for the hypothetical future never-drop non-Standard default.
+- **E6 guard semantics.** The guard now checks the pipe's SETTLED weights (the auto-follow result for auto pipes). This is what lets the first assignment of a never-drop class engage the ladder — the auto-follow it triggers reserves the lane by construction (every in-play lane gets a positive share), so no never-drop class can ever sit on a zeroed lane via the auto path.
+- **Demos write auto weights.** The harness demos previously categorized lanes without the weights the app auto-writes (a stale lane-only shortcut). With the new default, lane-only categorized pipes would sit at 0% for their assigned lanes (E7 floors only) — so the demos now write the app-mirroring ladder result to preserve their stated intent.
+
+## Verification
+
+- `tools/ci-local.sh --mac` — **10/10 gates green** (lint, unit tests, app build, golden harness + replay, palcheck, drift-rejection, assist preview, PP_DEBUG builds, stats replay-identity, input parity).
+- `harness fold-check` — mechanical fold-only proof for the re-bless.
+- `python3` JSON validation + `odin test core` 209/209 green.
diff --git a/app/input/exec.odin b/app/input/exec.odin
index 13a812b..56014cd 100644
--- a/app/input/exec.odin
+++ b/app/input/exec.odin
@@ -529,8 +529,8 @@ demolish_node :: proc(inp: ^Input, node: u32) {
 
 // qos_mode_manual — the DERIVED mode: manual iff the pipe's current weights
 // differ from the auto-ladder result for its assignments (or the editor is
-// open). Untouched pipes are auto (weights == default preset == auto of the
-// empty assignment set).
+// open). Untouched pipes are auto (weights == the 100% Standard unconfigured
+// default == auto of the empty assignment set — the ladder's 1-lane row).
 qos_mode_manual :: proc(inp: ^Input, ps: u32) -> bool {
 	if inp.qos_editing {
 		return true
diff --git a/app/qos_panel.odin b/app/qos_panel.odin
index e1892e7..eaff00a 100644
--- a/app/qos_panel.odin
+++ b/app/qos_panel.odin
@@ -13,7 +13,9 @@ import rl "vendor:raylib"
 // ladder (balance.json lane_auto_reserve_ladder) — the app writes the
 // computed weight set through the SAME serialized command as the manual
 // editor (Cmd_Set_Weights, weights payload — replay equality by
-// construction, E10). Manual pipes are marked + revertible to auto.
+// construction, E10). An untouched pipe shows the ladder's 1-lane row —
+// 100% Standard (user ruling 2026-08-19: everything on Standard until QoS
+// is engineered). Manual pipes are marked + revertible to auto.
 //
 // The mode is DERIVED, never stored: a pipe is manual iff its current
 // weights differ from qos_auto_weights(its assignments) — so no extra
diff --git a/core/catalog.odin b/core/catalog.odin
index fc3779a..d0c97dc 100644
--- a/core/catalog.odin
+++ b/core/catalog.odin
@@ -225,8 +225,11 @@ Balance :: struct {
 	placement: Placement_Balance,
 	// 3.2: the emphasis-dial presets (GDD M2 lever 2 — "MVP exposes this as a
 	// single 'priority emphasis' dial per pipe"). lane_presets are the dial's
-	// positions; default_preset_idx is the "balanced" resting position every
-	// pipe starts on + the E5 all-zero fallback (ODN-3). 5.8: the dial retires
+	// positions; default_preset_idx is the app-side manual quick-set default
+	// (balanced). The pipe RESTING default is NOT a preset — an unconfigured
+	// pipe is 100% Standard (the ladder's 1-lane row, qos_unconfigured_weights;
+	// user ruling 2026-08-19 — supersedes the 5.8 "every pipe starts on the
+	// balanced preset" resting state; ODN-3). 5.8: the dial retires
 	// into the QoS panel; the presets remain as app-side manual quick-sets (a
 	// preset is a weight set).
 	lane_presets:        [dynamic]Lane_Preset,
diff --git a/core/crisis_test.odin b/core/crisis_test.odin
index 3a7ba16..3067938 100644
--- a/core/crisis_test.odin
+++ b/core/crisis_test.odin
@@ -491,6 +491,12 @@ test_crisis_settled_scan_names_slot_order_bundle :: proc(t: ^testing.T) {
 	sla_draw(&s, cat, 1, 3, "narrow", 1) // bundle 2 — the email sink leg
 	sla_lane(&s, cat, 0, 0, LANE_BEST_EFFORT, 1) // email pays on the bottleneck
 	sla_lane(&s, cat, 2, 0, LANE_BEST_EFFORT, 1)
+	// 5.8 auto-follow (the app writes the ladder result after every
+	// categorization): email→BE on pipes 0+2 → in-play {Standard, Best-effort}
+	// = 2 → 70/30. Pipe 1 (router->host) stays UNTOUCHED — the 08-19 default:
+	// 100% Standard (streaming rides it full-rate).
+	sla_weights(&s, cat, 0, {0, 70, 30}, 1)
+	sla_weights(&s, cat, 2, {0, 70, 30}, 1)
 
 	// step manually to collect the streaming drop sites alongside the crisis
 	// events (crisis_record_run drains the drops)
diff --git a/core/qos.odin b/core/qos.odin
index fe7a91c..950a230 100644
--- a/core/qos.odin
+++ b/core/qos.odin
@@ -7,8 +7,9 @@ package core
 //
 //   qos_allocate :: proc(capacity: u32, w: [3]i32, default_w: [3]i32) -> [3]u32
 //   // weight-only partition (demand is NOT an input — gap-fill is a
-//   // serialization-time concern, story 3.3); all-zero weights → the catalog
-//   // default preset (E5); largest-remainder distribution, Express→Standard→
+//   // serialization-time concern, story 3.3); all-zero weights → the caller's
+//   // default (E5 — qos_pipe_caps passes the unconfigured 100% Standard set,
+//   // qos_unconfigured_weights); largest-remainder distribution, Express→Standard→
 //   // Best tie order (E8). Sums/remainders computed in i64 (ODN-10).
 //
 // The never-drop floor (E6) lives in the flow side (qos_pipe_caps, invoked by
@@ -33,7 +34,9 @@ package core
 // Weight domain: 0 ≤ w_i ≤ MAX_WEIGHT (enforced at the Command_Bus +
 // catalog load; the proc itself is total on i32).
 //
-// E5: all-zero weights → `default_w` (the catalog default preset). A zero
+// E5: all-zero weights → `default_w` (the caller's default — qos_pipe_caps
+// passes the unconfigured 100% Standard set; the balanced preset is only an
+// app-side manual quick-set, never a resting default). A zero
 // weight never contributes to the total and never receives a remainder unit —
 // a zeroed lane's cap is 0 (the player's demote-to-nothing choice; the bus
 // rejects it on never-drop lanes, E6).
@@ -120,21 +123,37 @@ qos_lane_of :: proc(t: ^Topology, cat: ^Catalogs, pipe: u32, class: u16) -> u8 {
 	return LANE_STANDARD
 }
 
+// qos_unconfigured_weights — the resting split of a pipe with NO player QoS
+// configuration (user ruling 2026-08-19): everything rides Standard at 100%
+// of capacity until the player engineers QoS. Data-driven from the ladder's
+// 1-lane row (balance.json lane_auto_reserve_ladder[0] = [100]) — no
+// hardcoded splits (ODN-5). This is exactly qos_auto_weights' zero-assignment
+// state: in-play = {Standard} (every type's default home), 1 in-play lane →
+// row [100] → Standard 100%. Single source for the unconfigured default at
+// every read site (pipe creation, the resting fallback, serialization's
+// absent-when-empty default, and the E5 all-zero allocator fallback).
+qos_unconfigured_weights :: proc(cat: ^Catalogs) -> (w: [3]i32) {
+	w[LANE_STANDARD] = cat.balance.auto_ladder[0][0]
+	return w
+}
+
 // qos_pipe_weights — the active WFQ weights of a pipe: its per-pipe weights if
-// set (Cmd_Set_Weights), else the catalog default preset. All pipes start on
-// the default preset (the "balanced" dial position — GDD: nothing
-// auto-allocates, the dial is the player's lever).
+// set (Cmd_Set_Weights), else the unconfigured default (user ruling
+// 2026-08-19: a pipe with no QoS configuration carries everything on Standard
+// at 100% — the ladder's 1-lane row, qos_unconfigured_weights). All pipes
+// start there; the player engineers QoS (GDD M2: nothing auto-allocates).
 qos_pipe_weights :: proc(t: ^Topology, cat: ^Catalogs, pipe_slot: u32) -> [3]i32 {
 	if int(pipe_slot) < len(t.pipe_weights) {
 		return t.pipe_weights[pipe_slot]
 	}
-	return cat.balance.lane_presets[cat.balance.default_preset_idx].weights
+	return qos_unconfigured_weights(cat)
 }
 
 // qos_auto_weights — the 5.8 assignment-driven auto-reservation split (user
-// ruling 2026-08-14, clarify ruling A): the weight set the pipe SHOULD have
-// given its type→lane assignments. Pure function of the pipe's lane overrides
-// + the catalog ladder (balance.lane_auto_reserve_ladder — data-driven, ODN-5):
+// ruling 2026-08-14, clarify ruling A; the untouched state superseded by the
+// 2026-08-19 ruling): the weight set the pipe SHOULD have given its type→lane
+// assignments. Pure function of the pipe's lane overrides + the catalog
+// ladder (balance.lane_auto_reserve_ladder — data-driven, ODN-5):
 //
 //   in-play lanes = {Standard} ∪ {distinct lanes with ≥1 override on this pipe}
 //
@@ -143,17 +162,23 @@ qos_pipe_weights :: proc(t: ^Topology, cat: ^Catalogs, pipe_slot: u32) -> [3]i32
 // it), so reserving it is the canon-safe floor. The ladder row for the
 // in-play count hands its shares to the in-play lanes in lane-priority order
 // (Express → Standard → Best-effort); non-in-play lanes get 0. A pipe with
-// ZERO overrides keeps the catalog default preset (NOT the ladder's 1-lane row)
-// — an untouched pipe must render byte-identical, so no-QoS-edit goldens shift
-// only by the catalog-hash fold (4.3 discipline).
+// ZERO overrides has exactly {Standard} in play → the ladder's 1-lane row
+// (100% Standard — the 08-19 ruling: "no queue configured = all traffic on
+// the standard queue at 100% of capacity ... until we start implementing
+// QoS"). This SUPERSEDES the 5.8 resting default-preset state (balanced
+// [1,1,1] on every untouched pipe — the divergence this fix retires).
 //
 // The APP writes the result through Cmd_Set_Weights (the serialized command
 // path) whenever assignments change — replay equality holds by construction;
 // core never calls this from a step/replay path. Never-drop safety BY
-// CONSTRUCTION: every lane a never-drop class can ride (assigned, default, or
-// Standard) is folded into the in-play set and every in-play lane gets a
-// positive share — so the auto result can never zero a never-drop lane and E6
-// is only reachable via manual edits.
+// CONSTRUCTION (once the player has ANY assignment on the pipe): every lane a
+// never-drop class can ride (assigned, default, or Standard) is folded into
+// the in-play set and every in-play lane gets a positive share — so the auto
+// result can never zero a never-drop lane and E6 is only reachable via
+// manual edits. An untouched pipe skips the fold (in-play = {Standard} =
+// 100%); a never-drop class defaulting off Standard there is backstopped by
+// the E6 flow floor, not the ladder (future content — the MVP loader pins
+// all defaults to Standard).
 qos_auto_weights :: proc(t: ^Topology, cat: ^Catalogs, pipe_id: u32) -> (w: [3]i32) {
 	in_play := [3]bool{}
 	in_play[LANE_STANDARD] = true
@@ -167,25 +192,72 @@ qos_auto_weights :: proc(t: ^Topology, cat: ^Catalogs, pipe_id: u32) -> (w: [3]i
 			}
 		}
 	}
-	// Every lane a NEVER-DROP class rides (by override OR its catalog default —
-	// the same resolution qos_pipe_never_drop uses) is also in-play, so the
-	// auto result can never zero a never-drop lane: the E6 bus guard can never
-	// reject an auto-follow, even for a never-drop class the player never
-	// assigned (its default lane stays reserved). Without this, a class whose
-	// default lane is not Standard (future content — the MVP loader pins all
-	// defaults to Standard) would break the auto path the moment its lane left
-	// the in-play set.
-	for i in 0..<len(cat.packet_types) {
-		pt := cat.packet_types[i]
-		if pt.max_loss_pct != 0 { continue } // droppable classes reserve nothing
-		lane := qos_lane_of(t, cat, pipe_id, u16(i))
-		if lane < LANE_COUNT {
-			in_play[lane] = true
+	// Once the player has ANY assignment, every lane a NEVER-DROP class rides
+	// (by override OR its catalog default — the same resolution
+	// qos_pipe_never_drop uses) is also in-play, so the auto result can never
+	// zero a never-drop lane: the E6 bus guard can never reject an auto-follow
+	// for a never-drop class the player never assigned (its default lane stays
+	// reserved). An UNTOUCHED pipe skips the fold — its in-play set is exactly
+	// {Standard} (the 08-19 ruling: everything on Standard at 100% until QoS is
+	// engineered); a never-drop class defaulting off Standard on an untouched
+	// pipe is backstopped by the E6 flow floor, not the ladder.
+	if assigned {
+		for i in 0..<len(cat.packet_types) {
+			pt := cat.packet_types[i]
+			if pt.max_loss_pct != 0 { continue } // droppable classes reserve nothing
+			lane := qos_lane_of(t, cat, pipe_id, u16(i))
+			if lane < LANE_COUNT {
+				in_play[lane] = true
+			}
+		}
+	}
+	n := 0
+	for lane in 0..<LANE_COUNT {
+		if in_play[lane] { n += 1 }
+	}
+	row := cat.balance.auto_ladder[n-1] // rows[0] = 1 lane … rows[2] = 3 lanes
+	wi := 0
+	for lane in 0..<LANE_COUNT {
+		if in_play[lane] {
+			w[lane] = row[wi]
+			wi += 1
 		}
 	}
-	if !assigned {
-		// untouched pipe — the resting preset (byte-stable no-QoS runs)
-		return cat.balance.lane_presets[cat.balance.default_preset_idx].weights
+	return w
+}
+
+// qos_auto_weights_after — the auto-ladder result AS IF a (class→lane)
+// override had just landed. Used by the E6 bus guard (validate_set_lane): a
+// never-drop class's first assignment must be allowed when the auto-follow
+// the app runs after Set_Lane reserves the lane — the ladder engages from
+// the player's first assignment (08-19). Mirrors qos_auto_weights with the
+// candidate override folded into the in-play set.
+qos_auto_weights_after :: proc(t: ^Topology, cat: ^Catalogs, pipe_id: u32, class: u16, lane: u8) -> (w: [3]i32) {
+	in_play := [3]bool{}
+	in_play[LANE_STANDARD] = true
+	assigned := false
+	for i in 0..<len(t.pipe_lane_over) {
+		o := t.pipe_lane_over[i]
+		if o.pipe == pipe_id {
+			if o.lane < LANE_COUNT {
+				in_play[o.lane] = true
+				assigned = true
+			}
+		}
+	}
+	if lane < LANE_COUNT {
+		in_play[lane] = true
+		assigned = true
+	}
+	if assigned {
+		for i in 0..<len(cat.packet_types) {
+			pt := cat.packet_types[i]
+			if pt.max_loss_pct != 0 { continue }
+			l := qos_lane_of(t, cat, pipe_id, u16(i))
+			if l < LANE_COUNT {
+				in_play[l] = true
+			}
+		}
 	}
 	n := 0
 	for lane in 0..<LANE_COUNT {
@@ -244,7 +316,7 @@ qos_apply_floor :: proc(caps: [3]u32, never_drop: [LANE_COUNT]bool, capacity: u3
 qos_pipe_caps :: proc(t: ^Topology, cat: ^Catalogs, pipe_slot: u32, pipe_id: u32) -> [3]u32 {
 	cap := u32(cat.pipe_tiers[t.pipe_tier[pipe_slot]].capacity_units)
 	w := qos_pipe_weights(t, cat, pipe_slot)
-	caps := qos_allocate(cap, w, cat.balance.lane_presets[cat.balance.default_preset_idx].weights)
+	caps := qos_allocate(cap, w, qos_unconfigured_weights(cat))
 	nd := qos_pipe_never_drop(t, cat, pipe_id)
 	return qos_apply_floor(caps, nd, cap)
 }
diff --git a/core/qos_test.odin b/core/qos_test.odin
index b733b59..a6a6c82 100644
--- a/core/qos_test.odin
+++ b/core/qos_test.odin
@@ -142,8 +142,9 @@ test_qos_bus_rejections_e6 :: proc(t: ^testing.T) {
 	// E6: a weight set that zeros Express (banking's never-drop lane) is rejected
 	_, e = topology_apply_edit(&s.topology, Command{kind = Cmd_Set_Weights{pipe = pipe, weights = {0, 1, 1}}}, cat)
 	testing.expect(t, e == .Invalid_Weights, "zeroing a never-drop lane must reject with .Invalid_Weights (E6)")
-	// and the pipe is untouched (validate-before-apply)
-	testing.expect_value(t, s.topology.pipe_weights[0], [3]i32{1, 1, 1})
+	// and the pipe is untouched (validate-before-apply) — still the 100%
+	// Standard unconfigured default
+	testing.expect_value(t, s.topology.pipe_weights[0], [3]i32{0, 100, 0})
 
 	// lane override: unknown pipe / class / lane
 	_, e = topology_apply_edit(&s.topology, Command{kind = Cmd_Set_Lane{pipe = 9999, class = 0, lane = LANE_EXPRESS}}, cat)
@@ -170,8 +171,8 @@ test_qos_apply_and_resolve :: proc(t: ^testing.T) {
 	step_n(&s, 1, cat)
 	pipe := s.topology.pipe_id[0]
 
-	// default: balanced weights + Standard lanes for both classes
-	testing.expect_value(t, s.topology.pipe_weights[0], [3]i32{1, 1, 1})
+	// default: 100% Standard weights + Standard lanes for both classes
+	testing.expect_value(t, s.topology.pipe_weights[0], [3]i32{0, 100, 0})
 	testing.expect(t, qos_lane_of(&s.topology, cat, pipe, 0) == LANE_STANDARD, "email rides Standard by default")
 	testing.expect(t, qos_lane_of(&s.topology, cat, pipe, 1) == LANE_STANDARD, "streaming rides Standard by default")
 
@@ -486,6 +487,10 @@ lane_pipe_setup :: proc(s: ^Run_State, cat: ^Catalogs) -> (res, rt, host: u32) {
 	stream_idx, _ := class_index(cat, "streaming")
 	append(&s.action_log, Command{apply_tick = 1, kind = Cmd_Set_Lane{pipe = 0, class = u16(email_idx), lane = LANE_BEST_EFFORT}})
 	append(&s.action_log, Command{apply_tick = 1, kind = Cmd_Set_Lane{pipe = 0, class = u16(stream_idx), lane = LANE_EXPRESS}})
+	// 5.8 auto-follow — the app writes the ladder result after every
+	// categorization (Cmd_Set_Weights, qos_apply_auto): email→BE + streaming→E
+	// → in-play {Express, Standard, Best-effort} = 3 → 50/30/20.
+	append(&s.action_log, Command{apply_tick = 1, kind = Cmd_Set_Weights{pipe = 0, weights = {50, 30, 20}}})
 	// "bulk": a Standard-riding droppable class (max_loss_pct 100) — the S
 	// lane needs a rider distinct from the overridden pair. default_lane must
 	// be Standard (the no-auto canon pin).
@@ -541,9 +546,10 @@ test_qos_lone_packet_full_capacity :: proc(t: ^testing.T) {
 test_qos_no_starvation_under_continuous_express :: proc(t: ^testing.T) {
 	// E7 at the flow level: continuous Express arrivals must not starve the
 	// lower lanes. Streaming (Express on pipe 0) spawns every tick; one email
-	// (Best-effort on pipe 0) sits in the queue. Balanced weights {5,5,5}:
-	// every window serves BE its 5 units, so the email's progress grows 5/tick
-	// (no starvation) while E traffic is continuous.
+	// (Best-effort on pipe 0) sits in the queue. Auto weights {50,30,20} on
+	// cap 15 → caps {8,4,3}: every window serves BE its 3 units, so the
+	// email's progress grows 3/tick (no starvation) while E traffic is
+	// continuous.
 	cat_storage: Catalogs
 	cat := test_catalog(&cat_storage)
 	defer catalogs_destroy(cat)
@@ -557,15 +563,15 @@ test_qos_no_starvation_under_continuous_express :: proc(t: ^testing.T) {
 	for tick in u64(1)..=20 {
 		flow_seed_demand(&s.flow, tick, res, rt, u16(stream_idx)) // continuous E
 	}
-	step_n(&s, 5, cat) // 4 service ticks (the rider joins at tick 1's forward): 5/tick -> 20
+	step_n(&s, 5, cat) // 4 service ticks (the rider joins at tick 1's forward): 3/tick -> 12
 	progress := u32(0)
 	for p in s.flow.packets {
 		if p.class == u16(email_idx) {
 			progress = p.progress_units
 		}
 	}
-	testing.expectf(t, progress == 20,
-		"E7: the Best-effort rider must receive its budget every window under continuous Express (progress 5/tick), got %d", progress)
+	testing.expectf(t, progress == 12,
+		"E7: the Best-effort rider must receive its budget every window under continuous Express (progress 3/tick), got %d", progress)
 }
 
 @(test)
@@ -770,7 +776,8 @@ test_qos_drop_precedence_e9_double_shed :: proc(t: ^testing.T) {
 // the lanes the player assigned + Standard (always reserved — the default
 // home of every un-categorized type, canon-safe). The ladder row for the
 // in-play count distributes shares by lane priority; a pipe with ZERO
-// overrides keeps the catalog default preset (byte-stable no-QoS runs).
+// overrides rides the ladder's 1-lane row — 100% Standard (user ruling
+// 2026-08-19, supersedes the 5.8 balanced-preset resting state).
 
 @(test)
 test_qos_auto_weights_ladder :: proc(t: ^testing.T) {
@@ -788,9 +795,9 @@ test_qos_auto_weights_ladder :: proc(t: ^testing.T) {
 	email_idx, _ := class_index(cat, "email")
 	stream_idx, _ := class_index(cat, "streaming")
 
-	// untouched pipe → the default preset (byte-stable no-QoS runs — NOT the
-	// ladder's 1-lane row, which would change every no-edit run's behavior)
-	testing.expect_value(t, qos_auto_weights(&s.topology, cat, pipe), [3]i32{1, 1, 1})
+	// untouched pipe → the ladder's 1-lane row — 100% Standard (user ruling
+	// 2026-08-19: everything on Standard until QoS is engineered)
+	testing.expect_value(t, qos_auto_weights(&s.topology, cat, pipe), [3]i32{0, 100, 0})
 
 	// streaming→Express (email left on Standard): in-play = {E, S} = 2 → 70/30
 	_, e := topology_apply_edit(&s.topology, Command{kind = Cmd_Set_Lane{pipe = pipe, class = u16(stream_idx), lane = LANE_EXPRESS}}, cat)
@@ -812,8 +819,8 @@ test_qos_auto_weights_ladder :: proc(t: ^testing.T) {
 	testing.expect_value(t, qos_auto_weights(&s.topology, cat, pipe), [3]i32{0, 70, 30})
 
 	// all assignments on Standard: in-play = {S} only = 1 lane → the ladder's
-	// [100] row → Standard 100% (the spec's documented all-on-Standard edge —
-	// the one place the 1-lane row is reachable once an assignment exists)
+	// [100] row → Standard 100% (the same 1-lane row an untouched pipe rides —
+	// the 08-19 ruling)
 	_, e = topology_apply_edit(&s.topology, Command{kind = Cmd_Set_Lane{pipe = pipe, class = u16(email_idx), lane = LANE_STANDARD}}, cat)
 	testing.expect(t, e == .None, "email→Standard must apply")
 	testing.expect_value(t, qos_auto_weights(&s.topology, cat, pipe), [3]i32{0, 100, 0})
@@ -823,10 +830,10 @@ test_qos_auto_weights_ladder :: proc(t: ^testing.T) {
 	testing.expect(t, e == .None, "email→Express must apply")
 	testing.expect_value(t, qos_auto_weights(&s.topology, cat, pipe), [3]i32{70, 30, 0})
 
-	// a second pipe is independent: its untouched state is the default preset
+	// a second pipe is independent: its untouched state is 100% Standard
 	append(&s.action_log, Command{apply_tick = 1, kind = Cmd_Draw_Pipe{a = res, b = rt, tier = std}})
 	step_n(&s, 1, cat) // applies the second draw — pipe id 1
-	testing.expect_value(t, qos_auto_weights(&s.topology, cat, 1), [3]i32{1, 1, 1})
+	testing.expect_value(t, qos_auto_weights(&s.topology, cat, 1), [3]i32{0, 100, 0})
 }
 
 @(test)
@@ -880,3 +887,145 @@ test_qos_auto_weights_never_drop_safe :: proc(t: ^testing.T) {
 	_, e = topology_apply_edit(&s2.topology, Command{kind = Cmd_Set_Weights{pipe = 0, weights = w2}}, cat)
 	testing.expect(t, e == .None, "the unassigned-never-drop auto set must pass the bus guard (E6)")
 }
+
+// --- 08-19: the unconfigured default — 100% Standard -------------------------
+// User ruling 2026-08-19: "in networking when no queue is configured, all
+// traffic should be on the standard queue and would take 100% of the
+// capacity. And that should be the auto. Everything on standard and 100%
+// until we start implementing QoS." These pins cover the briefing's ACs:
+// the unconfigured caps + full-capacity Standard flow, the first-assignment
+// ladder engagement + removal return, the untouched-never-drop floor
+// backstop, and the tier-change survival.
+
+@(test)
+test_qos_unconfigured_default_100pct_standard :: proc(t: ^testing.T) {
+	cat_storage: Catalogs
+	cat := test_catalog(&cat_storage)
+	defer catalogs_destroy(cat)
+	s, _ := qos_setup(cat)
+	defer run_destroy(&s)
+	step_n(&s, 1, cat) // applies the draw — pipe id 0 exists, zero QoS config
+	pipe := s.topology.pipe_id[0]
+
+	// the resting weights, the stored pipe default, and the auto result all
+	// read the ladder's 1-lane row — 100% Standard (data-driven, no hardcode)
+	testing.expect_value(t, qos_pipe_weights(&s.topology, cat, 0), [3]i32{0, 100, 0})
+	testing.expect_value(t, s.topology.pipe_weights[0], [3]i32{0, 100, 0})
+	testing.expect_value(t, qos_auto_weights(&s.topology, cat, pipe), [3]i32{0, 100, 0})
+
+	// caps: the FULL capacity lands on Standard — nothing held for unused lanes
+	caps := qos_pipe_caps(&s.topology, cat, 0, pipe)
+	testing.expectf(t, caps[LANE_STANDARD] == 15 && caps[LANE_EXPRESS] == 0 && caps[LANE_BEST_EFFORT] == 0,
+		"unconfigured pipe must allocate the full capacity (15) to Standard, got %v", caps)
+
+	// flow: an oversubscribed Standard lane uses the full capacity — a lone
+	// Standard packet still crosses a standard pipe in 2 on-edge ticks (the
+	// 3.2 keystone, unshifted by the new default)
+	{
+		cat2_storage: Catalogs
+		cat2 := test_catalog(&cat2_storage)
+		defer catalogs_destroy(cat2)
+		s2: Run_State
+		defer run_destroy(&s2)
+		run_init(&s2, 1, cat2.hash, TEST_LOGIC_HZ)
+		res2, rt2, _ := test_seed_fixture(&s2, cat2)
+		std2, _ := pipe_tier_index(cat2, "standard")
+		append(&s2.action_log, Command{apply_tick = 1, kind = Cmd_Draw_Pipe{a = res2, b = rt2, tier = std2}})
+		queue_packet(&s2, 0, res2, rt2, false, 0, 0) // email — Standard by default
+		step_n(&s2, 2, cat2)
+		testing.expectf(t, s2.score == 0, "unconfigured: not delivered after 2 ticks")
+		step_n(&s2, 1, cat2)
+		testing.expectf(t, s2.score == 1,
+			"unconfigured: lone Standard packet crosses in 2 on-edge ticks — full capacity, no reservation held for unused lanes")
+	}
+}
+
+@(test)
+test_qos_first_assignment_engages_ladder :: proc(t: ^testing.T) {
+	// AC 2: the auto-ladder engages ONLY from the player's first type→lane
+	// assignment; removing all assignments returns the pipe to 100% Standard.
+	// Splits come from balance.json (auto_ladder rows), never hardcoded.
+	cat_storage: Catalogs
+	cat := test_catalog(&cat_storage)
+	defer catalogs_destroy(cat)
+	s, _ := qos_setup(cat)
+	defer run_destroy(&s)
+	step_n(&s, 1, cat)
+	pipe := s.topology.pipe_id[0]
+	email_idx, _ := class_index(cat, "email")
+	stream_idx, _ := class_index(cat, "streaming")
+
+	// untouched → 100% Standard (the 08-19 ruling)
+	testing.expect_value(t, qos_auto_weights(&s.topology, cat, pipe), [3]i32{0, 100, 0})
+
+	// FIRST assignment → the ladder engages: streaming→Express → in-play
+	// {Express, Standard} = 2 → row [70,30]
+	_, e := topology_apply_edit(&s.topology, Command{kind = Cmd_Set_Lane{pipe = pipe, class = u16(stream_idx), lane = LANE_EXPRESS}}, cat)
+	testing.expect(t, e == .None, "streaming→Express must apply")
+	testing.expect_value(t, qos_auto_weights(&s.topology, cat, pipe), [3]i32{70, 30, 0})
+
+	// second assignment → in-play 3 → row [50,30,20]
+	_, e = topology_apply_edit(&s.topology, Command{kind = Cmd_Set_Lane{pipe = pipe, class = u16(email_idx), lane = LANE_BEST_EFFORT}}, cat)
+	testing.expect(t, e == .None, "email→Best-effort must apply")
+	testing.expect_value(t, qos_auto_weights(&s.topology, cat, pipe), [3]i32{50, 30, 20})
+
+	// removing ALL assignments → back to 100% Standard (the 1-lane row)
+	_, e = topology_apply_edit(&s.topology, Command{kind = Cmd_Set_Lane{pipe = pipe, class = u16(stream_idx), lane = LANE_STANDARD}}, cat)
+	testing.expect(t, e == .None, "streaming back to Standard must apply")
+	_, e = topology_apply_edit(&s.topology, Command{kind = Cmd_Set_Lane{pipe = pipe, class = u16(email_idx), lane = LANE_STANDARD}}, cat)
+	testing.expect(t, e == .None, "email back to Standard must apply")
+	testing.expect_value(t, qos_auto_weights(&s.topology, cat, pipe), [3]i32{0, 100, 0})
+}
+
+@(test)
+test_qos_unconfigured_never_drop_untouched :: proc(t: ^testing.T) {
+	// The 08-19 ruling vs the never-drop fold: an UNTOUCHED pipe is exactly
+	// {Standard} = 100% even when a never-drop class defaults off Standard
+	// (banking → Express) — the fold applies only once the player assigns
+	// something. The E6 flow floor is the backstop for the never-drop class.
+	cat_storage: Catalogs
+	cat := never_drop_catalog(&cat_storage)
+	defer catalogs_destroy(cat)
+	s, _ := qos_setup(cat)
+	defer run_destroy(&s)
+	step_n(&s, 1, cat)
+	pipe := s.topology.pipe_id[0]
+	// the AUTO result is untouched-exact — the fold does not engage
+	testing.expect_value(t, qos_auto_weights(&s.topology, cat, pipe), [3]i32{0, 100, 0})
+	// …but the flow floor still protects banking's Express lane (E6) — the
+	// floor ADDS a quantum (sum may oversell by one — defined, absorbed by
+	// 3.3's gap-fill), so Express 1 + Standard's full 15
+	caps := qos_pipe_caps(&s.topology, cat, 0, pipe)
+	testing.expectf(t, caps[LANE_EXPRESS] == 1 && caps[LANE_STANDARD] == 15 && caps[LANE_BEST_EFFORT] == 0,
+		"E6 floor must backstop banking's Express on an untouched pipe (1 unit), Standard keeps its full share, got %v", caps)
+}
+
+@(test)
+test_qos_unconfigured_survives_tier_change :: proc(t: ^testing.T) {
+	// AC 3: the unconfigured 100% Standard default survives pipe upgrade/tier
+	// changes — a tier change reallocates the NEW capacity entirely to
+	// Standard (weights are pipe state; qos_pipe_caps folds the tier each
+	// step). No silent re-split.
+	cat_storage: Catalogs
+	cat := test_catalog(&cat_storage)
+	defer catalogs_destroy(cat)
+	s, _ := qos_setup(cat)
+	defer run_destroy(&s)
+	step_n(&s, 1, cat)
+	pipe := s.topology.pipe_id[0]
+
+	// standard tier → cap 15, all Standard
+	caps := qos_pipe_caps(&s.topology, cat, 0, pipe)
+	testing.expectf(t, caps[LANE_STANDARD] == 15 && caps[LANE_EXPRESS] == 0 && caps[LANE_BEST_EFFORT] == 0,
+		"standard tier: full capacity to Standard, got %v", caps)
+
+	// white-box tier upgrade to wide (cap 40 — no tier command exists yet;
+	// the tier is topology state folded by qos_pipe_caps each step)
+	wide, _ := pipe_tier_index(cat, "wide")
+	s.topology.pipe_tier[0] = u16(wide)
+	caps2 := qos_pipe_caps(&s.topology, cat, 0, pipe)
+	testing.expectf(t, caps2[LANE_STANDARD] == 40 && caps2[LANE_EXPRESS] == 0 && caps2[LANE_BEST_EFFORT] == 0,
+		"wide tier: the NEW capacity reallocates entirely to Standard (no re-split), got %v", caps2)
+	// the stored weights are untouched
+	testing.expect_value(t, s.topology.pipe_weights[0], [3]i32{0, 100, 0})
+}
diff --git a/core/serialize.odin b/core/serialize.odin
index 3cec98f..0f6308e 100644
--- a/core/serialize.odin
+++ b/core/serialize.odin
@@ -340,7 +340,12 @@ state_writer :: proc(state: ^Run_State, tick_events: []Event, cat: ^Catalogs,
 	// replay artifact is the binary action log, never this dump; no reader
 	// parses the dump, so "absent when empty" carries no ambiguity in practice.
 	// A future dump parser must know the sections are omitted when empty.
-	def_w := cat.balance.lane_presets[cat.balance.default_preset_idx].weights
+	// The unconfigured default (user ruling 2026-08-19: 100% Standard — the
+	// ladder's 1-lane row, qos_unconfigured_weights) replaces the balanced
+	// preset here: pipes whose weights equal the resting default serialize
+	// zero bytes either way, so the sparse contract is unchanged for no-QoS
+	// runs (the only shift is the catalog_hash fold from balance.json).
+	def_w := qos_unconfigured_weights(cat)
 	non_default := 0
 	for i in 0..<len(t.pipe_weights) {
 		if t.pipe_alive[i] && t.pipe_weights[i] != def_w {
diff --git a/core/sla_test.odin b/core/sla_test.odin
index 449bc68..86b0929 100644
--- a/core/sla_test.odin
+++ b/core/sla_test.odin
@@ -30,6 +30,14 @@ sla_lane :: proc(s: ^Run_State, cat: ^Catalogs, pipe, class: u32, lane: u8, appl
 	append(&s.action_log, Command{apply_tick = apply_tick, kind = Cmd_Set_Lane{pipe = pipe, class = u16(class), lane = lane}})
 }
 
+// sla_weights — append a logged Cmd_Set_Weights (the 5.8 auto-follow write —
+// the app records the ladder result after every categorization; scenarios that
+// categorize must mirror it, or the pipe sits on the 08-19 unconfigured
+// 100% Standard default).
+sla_weights :: proc(s: ^Run_State, cat: ^Catalogs, pipe: u32, weights: [3]i32, apply_tick: u64) {
+	append(&s.action_log, Command{apply_tick = apply_tick, kind = Cmd_Set_Weights{pipe = pipe, weights = weights}})
+}
+
 // sla_spawn — seed a legacy demand entry (run setup, like the fixture).
 sla_spawn :: proc(s: ^Run_State, tick: u64, class: u16, src, dst: u32) {
 	flow_seed_demand(&s.flow, tick, src, dst, class)
diff --git a/core/stats_test.odin b/core/stats_test.odin
index fa89dd0..d607627 100644
--- a/core/stats_test.odin
+++ b/core/stats_test.odin
@@ -101,6 +101,9 @@ test_congested_run :: proc(state: ^Run_State, cat: ^Catalogs) {
 	// categorize pipe 0 (source->router): email -> BE, streaming -> E
 	append(&state.action_log, Command{apply_tick = 1, kind = Cmd_Set_Lane{pipe = 0, class = 0, lane = LANE_BEST_EFFORT}})
 	append(&state.action_log, Command{apply_tick = 1, kind = Cmd_Set_Lane{pipe = 0, class = 1, lane = LANE_EXPRESS}})
+	// 5.8 auto-follow (the app writes the ladder result after every
+	// categorization): email→BE + streaming→E → in-play 3 → 50/30/20
+	append(&state.action_log, Command{apply_tick = 1, kind = Cmd_Set_Weights{pipe = 0, weights = {50, 30, 20}}})
 	// demand: alternating 0->2 email / 2->0 streaming, 50ms apart
 	for i in 0..<20 {
 		flow_seed_demand(&state.flow, u64(1+i*2), r, h, 0)
@@ -236,10 +239,12 @@ test_stats_derivation_congested :: proc(t: ^testing.T) {
 	// aggregates same-kind sheds into ONE row;
 	// (b) the KNOWN tick-12 shape — the congested fixture's record at tick 12
 	// emits exactly one D row: pipe 1, class 1 (streaming), reason 0
-	// (Queue_Overflow), count 1 (the 5.9 re-tuned era-3 streaming base is
-	// 1/tick — the director's extra arrivals halved the tick-12 shed count
-	// from the pre-5.9 2). Pin the tuple, so a regression back to per-event
-	// rows (or a wrong aggregation key) fails.
+	// (Queue_Overflow), count 2. The 08-19 default-allocation change (untouched
+	// pipe 1 = 100% Standard vs the old balanced [1,1,1]) puts streaming + email
+	// on ONE shared full-capacity Standard lane, so the tick-12 shed count
+	// returns to 2 (the pre-5.9 value; the 5.9 re-tune's 1 assumed the balanced
+	// lane split). Pin the tuple, so a regression back to per-event rows (or a
+	// wrong aggregation key) fails.
 	for a in 0..<len(rec.drops) {
 		for b in a + 1..<len(rec.drops) {
 			d1, d2 := rec.drops[a], rec.drops[b]
@@ -249,11 +254,11 @@ test_stats_derivation_congested :: proc(t: ^testing.T) {
 	}
 	found_agg := false
 	for d in rec.drops {
-		if d.pipe == 1 && d.class == 1 && d.reason == u8(Drop_Reason.Queue_Overflow) && d.count == 1 {
+		if d.pipe == 1 && d.class == 1 && d.reason == u8(Drop_Reason.Queue_Overflow) && d.count == 2 {
 			found_agg = true
 		}
 	}
-	testing.expect(t, found_agg, "tick-12 shape pinned: one aggregated D row (pipe 1, class 1, Queue_Overflow, count 1)")
+	testing.expect(t, found_agg, "tick-12 shape pinned: one aggregated D row (pipe 1, class 1, Queue_Overflow, count 2)")
 }
 
 @(test)
diff --git a/core/topology.odin b/core/topology.odin
index a9fae24..14fe2db 100644
--- a/core/topology.odin
+++ b/core/topology.odin
@@ -190,10 +190,13 @@ apply_draw :: proc(t: ^Topology, c: Cmd_Draw_Pipe, cat: ^Catalogs) -> u32 {
 	append(&t.pipe_b, c.b)
 	append(&t.pipe_tier, c.tier)
 	append(&t.pipe_span, span)
-	// 3.2: a new pipe starts on the catalog default preset (the "balanced"
-	// dial position) — all traffic starts Standard, the player engineers QoS
-	// (GDD M2: nothing auto-allocates).
-	append(&t.pipe_weights, cat.balance.lane_presets[cat.balance.default_preset_idx].weights)
+	// 3.2/08-19: a new pipe starts on the unconfigured default — 100% Standard
+	// (the ladder's 1-lane row, qos_unconfigured_weights — user ruling
+	// 2026-08-19: no queue configured = all traffic on the standard queue at
+	// 100% of capacity until the player engineers QoS; GDD M2: nothing
+	// auto-allocates). This SUPERSEDES the 5.8 balanced [1,1,1] resting
+	// preset every pipe used to start on (the divergence this fix retires).
+	append(&t.pipe_weights, qos_unconfigured_weights(cat))
 	t.gen += 1
 	return id
 }
@@ -422,10 +425,15 @@ apply_set_emphasis :: proc(t: ^Topology, c: Cmd_Set_Weights, cat: ^Catalogs) {
 
 // validate_set_lane — the per-pipe lane override: pipe live (.Missing_Pipe),
 // class in catalog range (.Unknown_Class), lane in 0..2 (.Invalid_Lane), and a
-// never-drop class may not be parked on a lane this pipe's CURRENT weights
-// zero (E6 — parking a never-drop class on a zero-weight lane is the
-// override-shaped zeroing edit; the flow would floor it, but the bus rejects
-// the player's edit as the primary guard).
+// never-drop class may not be parked on a lane this pipe's SETTLED weights
+// zero. The settled set is the AUTO-follow result when the pipe is auto (its
+// current weights match the ladder for its assignments — the app re-writes
+// them after every Set_Lane, qos_apply_auto), else the manual set it already
+// holds. This lets a never-drop class's FIRST assignment engage the ladder
+// (08-19: the ladder starts at the player's first assignment — the auto-follow
+// it triggers reserves the lane) while still rejecting a manual zeroing edit
+// (E6 — the override-shaped zeroing; the flow would floor it, but the bus
+// rejects the player's edit as the primary guard).
 validate_set_lane :: proc(t: ^Topology, c: Cmd_Set_Lane, cat: ^Catalogs) -> Edit_Error {
 	ps, ok := pipe_slot(t, c.pipe)
 	if !ok { return .Missing_Pipe }
@@ -433,6 +441,11 @@ validate_set_lane :: proc(t: ^Topology, c: Cmd_Set_Lane, cat: ^Catalogs) -> Edit
 	if c.lane > LANE_BEST_EFFORT { return .Invalid_Lane }
 	if cat.packet_types[c.class].max_loss_pct == 0 {
 		w := qos_pipe_weights(t, cat, ps)
+		if w == qos_auto_weights(t, cat, c.pipe) {
+			// auto pipe: the assignment triggers the auto-follow, so the lane's
+			// settled weight is the ladder result WITH the override applied
+			w = qos_auto_weights_after(t, cat, c.pipe, c.class, c.lane)
+		}
 		if w[c.lane] == 0 { return .Invalid_Weights } // E6 — never-drop on a zeroed lane
 	}
 	return .None
diff --git a/data/balance.json b/data/balance.json
index bb06658..80ff2b5 100644
--- a/data/balance.json
+++ b/data/balance.json
@@ -1,5 +1,5 @@
 {
-  "_comment": "Balance catalog (GDD § Numerical Design, ODN-5). Single source for every tunable number. All state-affecting values are int (ODN-10). logic_hz=20 is the fixed-timestep tick rate (ODN-2). snap_radius = inclusive node-snap radius in world px (E4). packet_bandwidth = the bandwidth units a packet must accumulate to cross one edge (1.3 flow; transit ticks = ceil(packet_bandwidth / pipe.capacity_units), so a standard pipe (cap 15) takes 2 ticks). lane_presets = the 3.2 emphasis-dial positions (GDD M2 lever 2), per-pipe lane WFQ weights, data-driven — the 5.8 panel keeps them as manual quick-sets; default_lane_preset is the resting position every pipe starts on + the E5 all-zero fallback. lane_auto_reserve_ladder = the 5.8 assignment-driven auto-reservation (user ruling 2026-08-14, GDD M2 / ODN-3): rows[n-1] = the split for n in-play lanes — [100] · [70,30] · [50,30,20], strictly descending (higher-priority lane reserves more). In-play lanes = the lanes the player assigned + Standard (always reserved — the default home of un-categorized types, canon-safe); untouched pipes keep the default preset, not the ladder (no-QoS goldens stay byte-stable). Playtest-tunable; load-fail-fast validated (ODN-5). lane_queue_packets = the 3.3 per-(bundle, lane) queue bound — when a lane queue is full, the E9 drop precedence sheds the lowest-priority non-empty lane. pool_max_packets = the 3.3 global in-flight pool cap — the E22 backstop (pool exhaustion drops the lowest-priority lane first; one saturated link can never absorb the whole pool and starve the map). map.* = the design-grid world the camera fits into the 1280x720 window. placement.* = the 5.6 placement-separation rules (user ruling 2026-08-14, GDD M3): router↔router 4 tiles (playtest-tunable); router↔terminal = the snap-disambiguation floor + a small readability margin (~2 tiles — the floor derives from snap_radius: a terminal 1 tile away sits inside the 36px snap radius, so the smallest unambiguous gap is ceil(36/26) = 2 tiles). Terminals never block router placement the way the old blanket 7-tile rule did. cap_fraction_permille = the 5.9 per-terminal source demand cap (spec-traffic-model Thread 2): accrue = fraction × throughput ÷ packet_bandwidth milli-packets/tick per terminal, uniformly (500 = 50% — endpoints never self-congest). growth_groups = the 5.12 aggregation-group tunables (spec-traffic-model Thread 3 + the estates ruling, user 2026-08-17 night): the group-bias growth draw (a majority of draws bias toward existing clusters, a minority stay uniform — NOT 100% clustered) + the director's group-scoped demand weight. bias_prob_permille = the biased-draw fraction (750 = 0.75, the ruling's 0.7–0.8; a 0 or 1000 would break the estates+isolated mix); min_members/max_members = the estate size band (3–8); radius_tiles = the group radius + the derived-cluster adjacency threshold (5 — MUST exceed GROWTH_MIN_SEP_TILES = 3, the E31 packing floor); member_weight_permille = the per-member source-pick-weight bonus (250 — aggregate group demand rises as members join).",
+  "_comment": "Balance catalog (GDD § Numerical Design, ODN-5). Single source for every tunable number. All state-affecting values are int (ODN-10). logic_hz=20 is the fixed-timestep tick rate (ODN-2). snap_radius = inclusive node-snap radius in world px (E4). packet_bandwidth = the bandwidth units a packet must accumulate to cross one edge (1.3 flow; transit ticks = ceil(packet_bandwidth / pipe.capacity_units), so a standard pipe (cap 15) takes 2 ticks). lane_presets = the 3.2 emphasis-dial positions (GDD M2 lever 2), per-pipe lane WFQ weights, data-driven — the 5.8 panel keeps them as manual quick-sets; default_lane_preset is the resting position every pipe starts on + the E5 all-zero fallback. lane_auto_reserve_ladder = the 5.8 assignment-driven auto-reservation (user ruling 2026-08-14, GDD M2 / ODN-3): rows[n-1] = the split for n in-play lanes — [100] · [70,30] · [50,30,20], strictly descending (higher-priority lane reserves more). In-play lanes = the lanes the player assigned + Standard (always reserved — the default home of un-categorized types, canon-safe); an UNTOUCHED pipe rides the ladder's 1-lane row — 100% Standard (user ruling 2026-08-19: \"no queue configured = all traffic on the standard queue at 100% of capacity\" — supersedes the 5.8 balanced-preset resting state, which was the divergence; the 08-19 default-allocation change re-blesses every golden, this comment folding into catalog_hash). Playtest-tunable; load-fail-fast validated (ODN-5). lane_queue_packets = the 3.3 per-(bundle, lane) queue bound — when a lane queue is full, the E9 drop precedence sheds the lowest-priority non-empty lane. pool_max_packets = the 3.3 global in-flight pool cap — the E22 backstop (pool exhaustion drops the lowest-priority lane first; one saturated link can never absorb the whole pool and starve the map). map.* = the design-grid world the camera fits into the 1280x720 window. placement.* = the 5.6 placement-separation rules (user ruling 2026-08-14, GDD M3): router↔router 4 tiles (playtest-tunable); router↔terminal = the snap-disambiguation floor + a small readability margin (~2 tiles — the floor derives from snap_radius: a terminal 1 tile away sits inside the 36px snap radius, so the smallest unambiguous gap is ceil(36/26) = 2 tiles). Terminals never block router placement the way the old blanket 7-tile rule did. cap_fraction_permille = the 5.9 per-terminal source demand cap (spec-traffic-model Thread 2): accrue = fraction × throughput ÷ packet_bandwidth milli-packets/tick per terminal, uniformly (500 = 50% — endpoints never self-congest). growth_groups = the 5.12 aggregation-group tunables (spec-traffic-model Thread 3 + the estates ruling, user 2026-08-17 night): the group-bias growth draw (a majority of draws bias toward existing clusters, a minority stay uniform — NOT 100% clustered) + the director's group-scoped demand weight. bias_prob_permille = the biased-draw fraction (750 = 0.75, the ruling's 0.7–0.8; a 0 or 1000 would break the estates+isolated mix); min_members/max_members = the estate size band (3–8); radius_tiles = the group radius + the derived-cluster adjacency threshold (5 — MUST exceed GROWTH_MIN_SEP_TILES = 3, the E31 packing floor); member_weight_permille = the per-member source-pick-weight bonus (250 — aggregate group demand rises as members join).",
   "logic_hz": 20,
   "max_ticks": 100000,
   "snap_radius": 36,
diff --git a/demos/audio_throttle.dem b/demos/audio_throttle.dem
index c5607b2..1734f3d 100644
--- a/demos/audio_throttle.dem
+++ b/demos/audio_throttle.dem
@@ -1,11 +1,14 @@
 # audio_throttle.dem — the arrival-throttle golden (r1 W4): a WIDE path with
 # the streaming class split onto its Express lane delivers back-to-back
-# (wide cap 40 -> ceil(30/40) = 1 tick per edge), so a tight spawn burst
+# (wide cap 40, Express 70% of the 08-19 auto-follow write {70,30,0} ->
+# ceil(30/28) = 2 ticks per edge), so a tight spawn burst
 # (500/550/600 ms = ticks 11/12/13) lands arrivals on adjacent ticks — the
 # consumer's throttle (ARRIVAL_MIN_GAP_TICKS = 2) MUST suppress some of them
 # (the golden asserts suppressed >= 1: plays < arrivals on a dense tick).
 # The era-3 director's streaming demand rides the same Express lane, adding
 # more density for free. T1-only (no captures) — the audio golden family.
+# The lane directives carry the app-mirroring auto-follow weights
+# (Cmd_Set_Weights — the ladder result the app writes after categorizing).
 seed 42
 run 4000ms
 era 3
@@ -13,6 +16,8 @@ at 100ms draw 0 1 wide
 at 100ms draw 1 2 wide
 at 200ms lane 0 streaming express
 at 200ms lane 1 streaming express
+at 200ms weights 0 70 30 0
+at 200ms weights 1 70 30 0
 at 500ms spawn 0 2 streaming
 at 550ms spawn 0 2 streaming
 at 600ms spawn 0 2 streaming
diff --git a/demos/qos_auto.dem b/demos/qos_auto.dem
index 62c34e7..fa729ce 100644
--- a/demos/qos_auto.dem
+++ b/demos/qos_auto.dem
@@ -1,5 +1,6 @@
 # qos_auto.dem — Story 5.8 golden: the assignment-driven auto-reservation
-# split (user ruling 2026-08-14). Era-3 demand (email 1/tick res->res +
+# split (user ruling 2026-08-14; the untouched default superseded by the
+# 2026-08-19 ruling). Era-3 demand (email 1/tick res->res +
 # streaming 1/tick host->res — the 5.9 re-tune) over the res->router->host
 # backbone. At 3000ms
 # the player categorizes BOTH classes on pipe 1 (router->host): streaming ->
@@ -9,8 +10,8 @@
 # SERIALIZED outcome; the ladder COMPUTATION itself is core-tested in
 # qos_test.odin). Standard stays reserved even with no Standard-rider (the
 # canon-safe floor — un-categorized types ride it). The T2 captures pin the
-# painted lanes visibly re-splitting: 1000ms = default balanced, 6000ms =
-# 50/30/20.
+# painted lanes visibly re-splitting: 1000ms = 100% Standard (the 08-19
+# unconfigured default), 6000ms = 50/30/20.
 # fixture qos = the 3-node fixture + residentials 3,4. Node ids: 0=res,
 # 1=router, 2=host, 3=res, 4=res. Pipe ids (draw order): 0=res-router,
 # 1=router-host.
diff --git a/demos/qos_contention.dem b/demos/qos_contention.dem
index b547176..af5674c 100644
--- a/demos/qos_contention.dem
+++ b/demos/qos_contention.dem
@@ -1,11 +1,14 @@
 # qos_contention.dem — Story 3.3's launchable: the serialization visual + the
 # contention drop precedence (E7/E9). Pipe 0 (res 0 -> router 1) is oversubscribed
 # ~2.4x with two classes the PLAYER categorized (canon 2026-08-12 — nothing
-# auto-assigns): email -> Best-effort, streaming -> Express. A ~25ms burst
+# auto-assigns): email -> Best-effort, streaming -> Express, plus the
+# app-mirroring auto-follow weights (Cmd_Set_Weights 50/30/20 — the ladder
+# result the app writes after categorizing, in-play {E,S,B} = 3). A ~25ms burst
 # alternating both ways (0->2 email, 2->0 streaming) saturates pipe 0:
 # best-effort drops first (the E9 ladder), the queue exits by lane, packets
 # ride their painted lane end-to-end at lane speed. Pipes 3-1/4-1 stay
-# uncategorized plain routers (all Standard) — the no-auto contrast.
+# uncategorized plain routers — 100% Standard (the 08-19 unconfigured
+# default; everything on Standard until QoS is engineered) — the no-auto contrast.
 seed 4242
 run 12000ms
 fixture qos
@@ -16,6 +19,7 @@ at 100ms draw 3 1 standard
 at 100ms draw 4 1 standard
 at 100ms lane 0 email best_effort
 at 100ms lane 0 streaming express
+at 100ms weights 0 50 30 20
 capture at 1000ms
 capture at 3000ms
 capture at 10000ms
diff --git a/demos/qos_emphasis.dem b/demos/qos_emphasis.dem
index 1993f52..aae784b 100644
--- a/demos/qos_emphasis.dem
+++ b/demos/qos_emphasis.dem
@@ -6,8 +6,8 @@
 # (per-pipe lane override); at 9000ms the dial moves to best_effort_heavy
 # (1:2:4). The T1 manifest pins the whole run; the T2 captures pin the
 # proportions VISIBLY changing (the named golden):
-#   1000ms = default balanced (no lane segments — byte-identical to 3.1's
-#            pipe render), 5000ms = express-heavy segments, 12000ms =
+#   1000ms = 100% Standard (the 08-19 unconfigured default — a single
+#            Standard segment), 5000ms = express-heavy segments, 12000ms =
 #            best-effort-heavy segments.
 # fixture qos = the 3-node fixture + residentials 3,4. Node ids: 0=res,
 # 1=router, 2=host, 3=res, 4=res. Pipe ids (draw order): 0=res-router,
diff --git a/demos/qos_manual.dem b/demos/qos_manual.dem
index ae29179..dd3631f 100644
--- a/demos/qos_manual.dem
+++ b/demos/qos_manual.dem
@@ -5,7 +5,8 @@
 # the `weights` directive is the serialized outcome). The panel marks the
 # pipe MANUAL (derived: current weights != the auto-ladder result) and the
 # split follows the edited weights; lane widths + node serialization follow
-# via the flow's lane_caps. T2 captures: 1000ms = default balanced, 6000ms =
+# via the flow's lane_caps. T2 captures: 1000ms = 100% Standard (the 08-19
+# unconfigured default), 6000ms =
 # the 60/25/15 manual split.
 # fixture qos = the 3-node fixture + residentials 3,4. Node ids: 0=res,
 # 1=router, 2=host, 3=res, 4=res. Pipe ids (draw order): 0=res-router,
diff --git a/demos/sla.dem b/demos/sla.dem
index 94f26c6..b9b08ff 100644
--- a/demos/sla.dem
+++ b/demos/sla.dem
@@ -1,7 +1,9 @@
 # sla.dem — Story 3.4's launchable: per-class SLA accumulators + breach
 # crossings (attributable to a class). Pipe 0 (res 0 -> router 1) is
 # oversubscribed with the 3.3 contention shape (email -> Best-effort,
-# streaming -> Express, the PLAYER's categorization — canon 2026-08-12).
+# streaming -> Express, the PLAYER's categorization — canon 2026-08-12) +
+# the app-mirroring auto-follow weights (Cmd_Set_Weights 50/30/20 — the
+# ladder result the app writes after categorizing, in-play {E,S,B} = 3).
 # Golden-verified crossing stream (T1-pinned): {0,Loss,Enter}@17 (email loss
 # crosses 30%), {1,Loss,Enter}@18 (streaming loss crosses 10% — the E9 ladder
 # sheds Express too once its queue fills), {1,Latency,Enter}@20 (streaming
@@ -20,6 +22,7 @@ at 100ms draw 3 1 standard
 at 100ms draw 4 1 standard
 at 100ms lane 0 email best_effort
 at 100ms lane 0 streaming express
+at 100ms weights 0 50 30 20
 capture at 1000ms
 capture at 4000ms
 capture at 10000ms
diff --git a/harness/palcheck.odin b/harness/palcheck.odin
index 1f4d777..f3eedcd 100644
--- a/harness/palcheck.odin
+++ b/harness/palcheck.odin
@@ -267,8 +267,12 @@ run_palcheck :: proc(cat: ^pp.Catalogs) -> int {
 		narrow, _ := pp.pipe_tier_index(cat, "narrow")
 		wide, _ := pp.pipe_tier_index(cat, "wide")
 		re1, _ := pp.topology_apply_edit(&state.topology, pp.Command{kind = pp.Cmd_Draw_Pipe{a = 0, b = 1, tier = narrow}}, cat)
-		pp.topology_apply_edit(&state.topology, pp.Command{kind = pp.Cmd_Draw_Pipe{a = 1, b = 2, tier = wide}}, cat)
+		re2, _ := pp.topology_apply_edit(&state.topology, pp.Command{kind = pp.Cmd_Draw_Pipe{a = 1, b = 2, tier = wide}}, cat)
 		pp.topology_apply_edit(&state.topology, pp.Command{kind = pp.Cmd_Set_Weights{pipe = re1.id, weights = {4, 2, 1}}}, cat)
+		// 08-19: the DEFAULT pipe is 100% Standard (no Express stripe) — the
+		// oracle's amber presence needs an explicit player-engineered Express
+		// weight on the wide pipe too (express_heavy, a real panel preset).
+		pp.topology_apply_edit(&state.topology, pp.Command{kind = pp.Cmd_Set_Weights{pipe = re2.id, weights = {4, 2, 1}}}, cat)
 		for t in u64(1)..=120 {
 			pp.step(&state, t, {}, cat)
 			clear(&state.events)


--- SPEC / CONTEXT ---
### ORIGINAL JOB BRIEFING (the spec: user report + acceptance criteria)
# Briefing: QoS unconfigured default — 100% Standard lane

**Job id:** packet-plumber-v2-qos-default-standard
**Repo:** packet-plumber

## Task

User report (2026-08-19, verbatim): "in networking when no queue is configured,
all traffic should be on the standard queue and would take 100% of the capacity.
And that should be the auto. Everything on standard and 100% until we start
implementing QoS."

This is CANON, not a new decision — the implementation has drifted from it:

- GDD M2: "all traffic starts on Standard and the player actively engineers QoS
  — the player owns every call."
- Assignment-driven auto-reservation ladder: "1 class queue used = 100% ·
  2 = 70/30 · 3 = 50/30/20" (data-driven in `balance.json`). With ZERO player
  assignments there is exactly one class queue in play (Standard) → 100%.

Find where the unconfigured/default allocation diverges (suspect: a default
weight preset — e.g. the 50/30/20 — being applied to pipes with no player
assignment, or the ladder keyed off available lanes instead of *used* lanes)
and fix it so:

1. A pipe with NO player QoS configuration carries ALL traffic on the
   **Standard** lane at **100%** of capacity. Express and Best-effort carry
   nothing until the player assigns a type to them.
2. The auto-ladder engages ONLY from the player's first type→lane assignment
   (1 used = 100%, 2 used = 70/30, 3 used = 50/30/20 — from `balance.json`,
   no hardcoded splits).
3. Default state survives save/load, era advance, and pipe upgrade/tier
   changes (no silent re-split).

## Acceptance

- Headless test: fresh pipe, zero assignments → 100% Standard allocation;
  oversubscribed demand → Standard-lane packets use the full capacity (no
  reservation held for unused lanes).
- Test: first assignment flips that pipe to the ladder rung; removing all
  assignments returns to 100% Standard.
- Full local suite (`bin/local-ci` or equivalent) green; goldens re-blessed
  ONLY if the fix legitimately changes pinned behavior (fold-only re-bless
  discipline — say so in the PR body if so).
- PR body names the divergence root cause.

## Skills policy

- Workflow: **bmad-quick-dev** (implementation).
- Mega-minions (if spawned): bmad-review-adversarial-general /
  bmad-review-edge-case-hunter for self-review.

## Model policy

- Minion: pi default (ops tier — deepseek/deepseek-v4-flash).
- Mega-minions: same.

## Review

- `pr_review: true` — gameplay/canon-surface code (QoS allocation semantics);
  the 2026-08-12 scope guard applies. Perkins round on the PR head.
- No lavish needed — code fix, PR directly.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: v2-qos-default-standard
- base: v2
- pr_review: 1


### PERKINS ROUND-1 BRIEFING (lens-guards: what is canon, what not to re-litigate)
# Perkins briefing — packet-plumber-v2-qos-default-standard r1

- **Job:** packet-plumber-v2-qos-default-standard · **Round:** 1 (loop-until-APPROVED budget)
- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/73 (QoS unconfigured default — 100% Standard lane)
- **Reviewed sha:** `1a1a175862560110cee8d6ac654ec3e19c879ba3` (head of `v2-qos-default-standard`, base `v2`)
- **repo_root:** `/Users/moses/code/packet-plumber` · **Your cwd:** detached worktree at exactly the reviewed sha — trust it, not `origin/v2`
- **Spec pointers:** original job briefing `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-qos-default-standard.md` (the user report + GDD M2 canon) + the PR body's root-cause + decisions (the drift: balanced [1,1,1] applied at apply_draw + resting/auto fallbacks; the fix: `qos_unconfigured_weights()` single source, ladder 1-lane row `[100]` data-driven from `lane_auto_reserve_ladder[0]`, auto-ladder engages only from the first type→lane assignment) + GDD decision-log entry.
- **Model:** zai-coding-cn/glm-5.3 (reasoning tier FALLBACK — k3 hit its billing-cycle 403 at dispatch; glm probed OK 17:48Z). Lens mega-minions: name the model explicitly at every spawn (`zai-coding-cn/glm-5.3`) — and PIN `--cwd <this worktree>` on every lens tab (the 08-18 mis-rooted-lens class).

## Lens-guards

- **ONE hard blocker class — QoS allocation semantics (the canon):** a pipe with NO player QoS configuration carries ALL traffic on the Standard lane at 100% of capacity (Express/Best-effort carry nothing until the player assigns a type); the auto-ladder engages ONLY from the player's FIRST type→lane assignment (1 used = 100% · 2 = 70/30 · 3 = 50/30/20 — data-driven from `balance.json`, NO hardcoded splits); the default survives save/load, era advance, and pipe upgrade/tier changes (no silent re-split). Any path where an unconfigured pipe holds capacity for unused lanes, or the balanced [1,1,1] preset resurfaces, = real blocker.
- **The deliberate re-bless is SANCTIONED but must be fold-proven:** 32 of 35 demo logs byte-identical except the 8 catalog-hash bytes; 3 demos gained intent-preserving auto weights; harness fold-check PASSES (the boot shift is mechanically the catalog fold alone); T2 diffs confined to the lane-band regions. Flag ONLY if the fold discipline broke (a non-catalog byte moved, a non-lane T2 region changed, fold-check red).
- **What NOT to re-litigate:** GDD M2 canon + the user report (2026-08-19, verbatim in the briefing) — "all traffic on the standard queue at 100% until we start implementing QoS" is CANON, not a decision to revisit; the data-driven ladder from balance.json; the 5.8 QoS architecture (assignment-driven auto-reservation) is settled — this fix corrects its default-weight drift, it doesn't redesign it.
- **What to flag for verification:** `qos_unconfigured_weights()` is the single source at EVERY read site (pipe creation, resting fallback, serialization's absent-when-empty default, E5 allocator fallback) — one missed read site = drift resurface; `validate_set_lane`'s E6 guard now checks settled weights (auto-follow result for auto pipes) so a never-drop class's first assignment engages the ladder; the lane-only demos/tests mirror the app's auto-follow weights; the headless tests (zero-assignment 100%, oversubscribed Standard full-capacity, first-assignment flip, removal returns to 100%, save/load + era + tier survival).
- **CI note:** GitHub Actions is billing-blocked today (runners never start). Local suite is ground truth: `tools/ci-local.sh --mac` 10/10 per the badge-out — re-run at minimum the qos/headless tests + fold-check.

## Perkins standing orders (verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 73` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-qos-default-standard/r1/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the original job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-qos-default-standard/r1`, no `prior_findings` (r1). Headless mode owns pane mechanics, the `<lens>.json` output contract, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and `consolidated.json`. Visual checks: verify MECHANICALLY first (byte/hash/capture-diff); when a visual judgment is unavoidable, run the `vision-read` skill on `lmstudio/qwen/qwen3.8-27b` — never trust a text-only model's eye. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 blockers → `--request-changes`; 4+ → `--request-changes`, body leads with "MAJOR REWORK". **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — STDOUT ONLY, never `2>&1` (stderr cache warnings corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → mint failed; fall back to `gh pr comment 73 --body-file <body.md>`, note `fallback-comment` in your ledger note, call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 73 --<event> --body-file <body.md>`
- Body format: `## 🤖 Perkins automated review — round 1 of 3` header (loop-until-APPROVED), Job, Reviewed sha, Reviewers x/7, Verification counts, Blockers/Warnings/Notes sections, Reviewer agreement, Verdict line, "_Address findings and push — I re-review automatically on the new sha._"
- Before posting, re-fetch `headRefOid` (gh pr view 73 --json headRefOid). If it moved mid-review, post anyway but note "reviewed <old>, head now <new> — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-qos-default-standard-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Skip the code-review skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.


### PR BODY (root cause + decisions, as authored by the implementer)
## Summary

User ruling 2026-08-19 (verbatim): *"in networking when no queue is configured, all traffic should be on the standard queue and would take 100% of the capacity. And that should be the auto. Everything on standard and 100% until we start implementing QoS."*

A pipe with **no player QoS configuration now carries ALL traffic on the Standard lane at 100% of capacity**. Express and Best-effort hold nothing until the player assigns a type to them. The auto-ladder engages only from the player's first type→lane assignment (1 in-play lane = 100% · 2 = 70/30 · 3 = 50/30/20, from `balance.json` `lane_auto_reserve_ladder` — no hardcoded splits).

## Divergence root cause

This is CANON restated (GDD M2: "all traffic starts on Standard and the player actively engineers QoS" + the 08-14 ladder "1 class queue used = 100%"), not a new decision — the **5.8 implementation drifted**:

- `apply_draw` appended `lane_presets[default_preset_idx].weights` — the **balanced `[1,1,1]` preset (≈33/33/33)** — as every new pipe's resting weights.
- `qos_pipe_weights` and `qos_auto_weights` returned the same balanced preset for unconfigured pipes.
- The drift was **documented as canon** in the 5.8 `balance.json` comment ("untouched pipes keep the default preset, not the ladder"), which is what made it look intentional.

The fix makes the unconfigured state the **ladder's 1-lane row** (`lane_auto_reserve_ladder[0] = [100]` → Standard 100%) at every read site, data-driven (ODN-5).

## Changes

**Core (`core/`)**
- `qos.odin` — new `qos_unconfigured_weights(cat)` (single data-driven source for the resting default); `qos_auto_weights` drops the `!assigned` balanced early-return (untouched pipes flow through the ladder path: in-play = exactly `{Standard}` → row `[100]`); the never-drop fold now engages only once the player has ≥1 assignment (an untouched pipe is exactly `{Standard}` = 100% — a never-drop class defaulting off Standard there is backstopped by the E6 flow floor); `qos_pipe_weights` fallback + `qos_pipe_caps` E5 fallback use the helper; new `qos_auto_weights_after` (the ladder result with a candidate override folded in).
- `topology.odin` — `apply_draw` writes `qos_unconfigured_weights`; `validate_set_lane` E6 guard checks the **settled** weights (the auto-follow result for auto pipes, the manual set otherwise), so a never-drop class's FIRST assignment can engage the ladder (the auto-follow it triggers reserves the lane) while manual zeroing edits are still rejected.
- `serialize.odin` — the absent-when-empty default (`def_w`) is the unconfigured default; default pipes still serialize ZERO QoS bytes (sparse contract intact).
- `catalog.odin` / `data/balance.json` — comments corrected (the 5.8 "untouched pipes keep the default preset" clause was the documented bug; the 08-19 ruling supersedes it).

**Tests (`core/*_test.odin`)** — pins moved from balanced `{1,1,1}` to `{0,100,0}`; new AC tests:
- `test_qos_unconfigured_default_100pct_standard` — fresh pipe, zero assignments → full capacity (15/15) to Standard, nothing held for unused lanes; lone Standard packet crosses in 2 on-edge ticks (full-capacity flow).
- `test_qos_first_assignment_engages_ladder` — first assignment flips the pipe to the ladder rung (70/30, then 50/30/20); removing all assignments returns to `{0,100,0}`.
- `test_qos_unconfigured_never_drop_untouched` — an untouched pipe is exactly `{0,100,0}` even with a never-drop class defaulting off Standard; the E6 flow floor backstops it (Express floored to 1).
- `test_qos_unconfigured_survives_tier_change` — a tier change reallocates the NEW capacity entirely to Standard (no silent re-split).
- Lane-only fixtures (`lane_pipe_setup`, `test_congested_run`, the crisis construction) now mirror the app's auto-follow weights (the ladder result the app writes after categorizing); `sla_weights` helper added. Stats/crisis shape pins re-pinned to the new allocation (the aggregation mechanism itself is unchanged — one aggregated row, no per-event duplicates).

**App (`app/`)** — comment accuracy only (`qos_mode_manual`'s AUTO derivation still holds: untouched = weights == auto == the 100% Standard default).

**Demos (`demos/`)** — `sla`, `qos_contention`, `audio_throttle` gained the app-mirroring auto-follow weights so their scenarios keep their intent; "default balanced" capture comments updated to "100% Standard".

**Harness** — `palcheck`'s zoomed lane-stripe oracle sets explicit Express weights on the wide pipe (a default pipe no longer shows an Express stripe).

## Golden re-bless — deliberate + cause-documented

The fix legitimately changes pinned behavior (the unconfigured allocation), so goldens were deliberately re-blessed (`harness save`):

- **32 demos fold-only:** the `.log.bin` differs from the pre-bless golden in EXACTLY the 8 `catalog_hash` bytes (byte-verified per file; `balance.json`'s corrected comment folds into the catalog hash). `harness fold-check 5f86ef16ca1c0ece 0e1e1afe9129ff2f` **PASSES** — boot's tick-1 shift is mechanically proven to be the catalog fold alone. Identical commands + unchanged catalog values ⇒ identical sim behavior for these demos.
- **3 demos behavioral by design:** `audio_throttle`, `sla`, `qos_contention` gained the auto-follow `Cmd_Set_Weights` entries (intent-preserving, see above).
- **T2 captures re-render** every default pipe as a single 100% Standard band (previously 3 equal bands) — verified the diffs are confined to the lane-band regions of pipes. `input_parity` manifests re-blessed (fold-only).

## Decisions & rationale

- **"1 used = 100%" counts in-play lanes (Standard always in-play).** Standard is the default home of every un-categorized type (08-12 canon) and is always reserved (08-14 ruling) — so the ladder's rung 1 (`[100]`) IS the zero-assignment state. This matches the GDD's own ladder wording ("1 class queue used = 100%").
- **Never-drop fold gated on `assigned`.** An untouched pipe is exactly `{Standard}` = 100% per the 08-19 ruling ("until we start implementing QoS"). MVP data is unaffected (all defaults pinned to Standard); the E6 flow floor remains the backstop for the hypothetical future never-drop non-Standard default.
- **E6 guard semantics.** The guard now checks the pipe's SETTLED weights (the auto-follow result for auto pipes). This is what lets the first assignment of a never-drop class engage the ladder — the auto-follow it triggers reserves the lane by construction (every in-play lane gets a positive share), so no never-drop class can ever sit on a zeroed lane via the auto path.
- **Demos write auto weights.** The harness demos previously categorized lanes without the weights the app auto-writes (a stale lane-only shortcut). With the new default, lane-only categorized pipes would sit at 0% for their assigned lanes (E7 floors only) — so the demos now write the app-mirroring ladder result to preserve their stated intent.

## Verification

- `tools/ci-local.sh --mac` — **10/10 gates green** (lint, unit tests, app build, golden harness + replay, palcheck, drift-rejection, assist preview, PP_DEBUG builds, stats replay-identity, input parity).
- `harness fold-check` — mechanical fold-only proof for the re-bless.
- `python3` JSON validation + `odin test core` 209/209 green.



### IMPLEMENTATION SPEC ARTIFACT (committed in this PR)
---
title: 'QoS unconfigured default — 100% Standard lane'
type: 'bugfix'
created: '2026-08-19'
status: 'done'
review_loop_iteration: 0
baseline_commit: 'f162ba6c3ed9a31be02623e084393d16e846a25b'
context: []
---

## Intent

**Problem:** A pipe with NO player QoS configuration splits bandwidth across all 3 lanes (the `balanced` preset `[1,1,1]` ≈ 33/33/33) instead of carrying everything on Standard at 100%. This drifts from canon (user ruling 2026-08-19: "when no queue is configured, all traffic should be on the standard queue and would take 100% of the capacity. And that should be the auto. Everything on standard and 100% until we start implementing QoS") — GDD M2 "all traffic starts on Standard; QoS is player-engineered, never auto."

**Approach:** Make the unconfigured state the ladder's 1-lane row (`lane_auto_reserve_ladder[0] = [100]` → Standard 100%, data-driven, no hardcoded splits) at every site that currently applies the `balanced` preset as the pipe default: pipe creation, the resting-weight fallback, serialization's absent-when-empty default, and `qos_auto_weights`' untouched-pipe branch. The auto-ladder then engages only via the player's first type→lane assignment.

## Boundaries & Constraints

**Always:**
- Unconfigured pipe = Standard 100% at every read site (allocator caps, serialize, panel, auto-ladder), sourced from `balance.lane_auto_reserve_ladder[0]` — never a hardcoded `[100,0,0]` literal (ODN-5).
- Ladder rows keyed by in-play count = player-assigned distinct lanes + Standard (always in-play, per the 08-14 ruling — Standard is every un-categorized type's home). Row values hand out in lane-priority order E→S→B. Never-drop fold applies only once the pipe HAS an assignment (untouched pipe = exactly {Standard} → 100%, per the 08-19 ruling; the E6 flow floor remains the backstop).
- `balanced` preset stays as the app-side manual quick-set; it is no longer any pipe's resting default.
- Sparse serialization preserved: default pipes (weights == new default) serialize ZERO QoS bytes.
- Determinism/replay: all changes are pure state reads; the app's auto-follow write-through path is unchanged.

**Ask First:** none anticipated.

**Never:** no hardcoded split values; no change to the app's auto-follow write mechanism (`qos_apply_auto` / `Cmd_Set_Weights`); no touching `qos_allocate`'s largest-remainder math or the E6 floor; no silent golden mutation — every re-bless is deliberate + cause-documented.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Fresh pipe, zero assignments | draw; no Set_Lane / Set_Weights | `qos_pipe_weights` / `qos_auto_weights` = `{0,100,0}`; caps on cap-15 standard tier = `[15,0,0]` (nothing held for E/B) | n/a |
| Oversubscribed Standard demand | Standard lane saturated | Standard packets use FULL capacity (`qos_serialize` with ready={false,true,false} → budget `{0,15,0}`); lone packet still crosses in 2 on-edge ticks | n/a |
| First assignment | Set_Lane streaming→Express | auto = `{70,30,0}` (in-play {E,S} = 2 → ladder row 2) | never-drop bus guard unchanged |
| Remove all assignments | Set_Lane back to Standard | auto returns to `{0,100,0}` | n/a |
| 2 assignments | Set_Lane streaming→Express + email→Best-effort | auto = `{50,30,20}` (in-play 3 → row 3) | n/a |
| Unassigned never-drop default lane (future content) | banking default Express, NO assignments | untouched pipe = exactly `{0,100,0}` (fold gated on assigned); E6 flow floor backstops banking | n/a |
| Save/load, era advance, tier change | default pipe, no QoS edits | weights stay `{0,100,0}`; serialize emits zero QoS bytes; tier change reallocates 100% to Standard at the new capacity | n/a |

## Code Map

- `core/qos.odin` -- `qos_auto_weights` (untouched branch + never-drop fold gating), `qos_pipe_weights` (resting fallback), `qos_pipe_caps` (E5 default_w), new `qos_unconfigured_weights` helper
- `core/topology.odin` -- `apply_draw` appends the pipe's initial weights (line ~196)
- `core/serialize.odin` -- `def_w` (absent-when-empty default, line ~343)
- `core/catalog.odin` -- `Balance` struct comment (default_preset_idx semantics)
- `data/balance.json` -- `lane_auto_reserve_ladder` comment (the 5.8 "untouched pipes keep the default preset" clause is the documented bug — rewrite)
- `core/qos_test.odin` -- pin updates + new AC tests
- `app/input/exec.odin`, `app/qos_panel.odin` -- comment touch-ups (AUTO derivation still holds)
- `demos/qos_auto.dem`, `demos/qos_emphasis.dem`, `demos/qos_manual.dem`, `demos/qos_contention.dem`, `demos/sla.dem`, `demos/audio_throttle.dem` -- lane-only demos get the auto weights the app writes (intent preservation); "default balanced" capture comments update

## Tasks & Acceptance

**Execution:**
- [x] `core/qos.odin` -- add `qos_unconfigured_weights(cat)` (ladder row 1 → Standard 100%); make `qos_auto_weights` drop the `!assigned` balanced early-return and gate the never-drop fold on `assigned`; `qos_pipe_weights` fallback + `qos_pipe_caps` default_w → the helper; update doc comments
- [x] `core/topology.odin` -- `apply_draw` appends `qos_unconfigured_weights(cat)`
- [x] `core/serialize.odin` -- `def_w` = `qos_unconfigured_weights(cat)`
- [x] `data/balance.json` -- rewrite the ladder comment (untouched = 100% Standard ladder row, the 08-19 ruling; note the catalog_hash re-bless)
- [x] `core/catalog.odin` -- `Balance` struct comment update (pipes no longer start on balanced)
- [x] `core/qos_test.odin` -- update pinned untouched values (`{1,1,1}` → `{0,100,0}`); add AC tests: unconfigured 100% caps + full-capacity Standard; first-assignment engages ladder + removal returns; unassigned-never-drop untouched = exactly {0,100,0}; tier-change keeps 100% Standard
- [x] `app/input/exec.odin`, `app/qos_panel.odin` -- comment accuracy (untouched auto == the 100% Standard default)
- [x] `demos/*.dem` -- add the app-mirroring auto weights to lane-only demos; update "default balanced" comments
- [x] goldens -- deliberate re-bless (tools/harness.sh save) + cause-document every shift in the PR body

**Acceptance Criteria:**
- Given a fresh pipe with zero assignments, when caps are computed, then Standard carries the pipe's FULL capacity and Express/Best-effort carry 0 (headless).
- Given an oversubscribed Standard lane on an unconfigured pipe, when the flow runs, then Standard-lane packets use the full capacity (no reservation held for unused lanes; lone packet crosses in 2 on-edge ticks).
- Given a pipe's first type→lane assignment, when the assignment lands, then the auto weights flip to the ladder rung for its in-play count (1 assign = 70/30, 2 = 50/30/20 from balance.json).
- Given all assignments removed from a pipe, when the last override reverts to Standard, then the auto weights return to {0,100,0}.
- Given a default pipe, when the run is serialized/replayed, era advances, or its tier changes, then weights stay {0,100,0} and no QoS bytes serialize (sparse contract holds).
- Given the full local suite, when run, then `tools/ci-local.sh --fast` (lint + unit) and the full suite pass; goldens re-blessed only where behavior legitimately changed, each shift cause-documented.
- PR body names the divergence root cause (the balanced preset applied as the pipe default at `apply_draw` + the resting/auto fallbacks, documented in the 5.8 ladder comment).

## Spec Change Log

## Design Notes

**Why the untouched branch changes:** the ladder's row 1 IS `[100]` — Standard 100%. The 5.8 code explicitly avoided it for untouched pipes ("byte-stable no-QoS runs") in favor of the balanced preset; the 08-19 ruling overturns that: the unconfigured state IS the ladder's rung 1. Removing the `!assigned` early-return makes untouched pipes flow through the same in-play/ladder path, so the resting state is data-driven by construction.

**Never-drop fold gating:** the fold keeps every never-drop class's lane in-play (so auto never zeroes it). Gating it on `assigned` makes an untouched pipe EXACTLY {Standard} → 100% (the ruling's "until we start implementing QoS"). MVP data is unaffected (all defaults pinned to Standard); the E6 flow floor stays as the backstop for hypothetical future never-drop non-Standard defaults.

**Golden impact:** `lane_caps` is derived + never serialized, so T1 dumps for no-QoS runs shift only via the catalog_hash fold (balance.json comment). Behavior shifts where lanes are ready on formerly-balanced pipes: lane-only demos (sla, audio_throttle, qos_contention) get the app-mirroring auto weights to preserve intent; T2 captures pinning "default balanced" (qos_auto/qos_emphasis/qos_manual at 1000ms) legitimately re-render as 100% Standard.

## Verification

**Commands:**
- `tools/ci-local.sh --fast` -- gates 1-2 green (lint + `odin test core`)
- `tools/ci-local.sh --mac` -- full 10-gate suite green, goldens re-blessed where documented
- `tools/harness.sh run qos_auto qos_contention qos_emphasis qos_manual sla audio_throttle` -- targeted re-bless verification before the full run


--- CHUNK NOTE ---
CHUNK CONTEXT: This diff is the code+script+docs chunk of PR #73 (branch v2-qos-default-standard). The PR also re-blesses 151 golden files (goldens/*.bin, *.png, *.t1) — that golden re-bless chunk is NOT part of this diff and is verified separately by mechanical means (harness fold-check, byte-level log.bin diffs, full local CI suite). Do not file findings about golden files being changed/re-blessed; DO file findings if the code itself is wrong.

--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

Note: this is an offline desktop game (Odin + raylib) — calibrate severity accordingly; a finding that matters only for a web service is a note here, not a blocker. Deserialization (save/load) robustness against corrupted or hostile save files IS in scope.

--- OUTPUT ---
Write ONE valid JSON array — and NOTHING else — to the file:
  /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-qos-default-standard/r1/security.json
using your file-writing tool. Each element must match this schema exactly:
{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- The file contains ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, STOP. Your task is complete.

ACCURACY MANDATE — this is the most important instruction in this brief:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
