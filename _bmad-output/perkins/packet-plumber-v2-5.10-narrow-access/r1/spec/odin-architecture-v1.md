---
title: 'Packet Plumber — Odin Architecture (the Odin pivot)'
project: 'packet-plumber'
game: 'Packet Plumber'
date: '2026-08-08'
author: 'Moses'
version: 'v1'
status: 'lavish-reviewed 2026-08-08 — rulings applied (§18); ready for PR'
language: 'Odin dev-2026-08'
renderer: 'raylib 6.0 (via vendor:raylib)'
platform: 'Desktop-first launch (Steam PC/Mac) — ruled 2026-08-08; mobile follows when the toolchain matures (FORGE #6 amended)'
supersedes_engine_of: '_bmad-output/planning-artifacts/architecture/architecture-v1.md (GL5.2 — the reviewed DESIGN this doc evolves, prototype-validated at the surge slice; not re-decided, re-targeted)'

# Source documents (this architecture translates them; it does not re-decide them)
gdd: '_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md'
epics: '_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/epics.md'
gdd_decision_log: '_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/decision-log.md'
forge: '_bmad-output/planning-artifacts/forge-packet-plumber-2026-08-05/forged-idea.md'
art_direction: '_bmad-output/planning-artifacts/art-direction/art-direction-v1.md + art-direction-v1-amendments.md'
look_book: '_bmad-output/planning-artifacts/art-renders/look-book-v1.md'
project_context: 'project-context.md (redone for Odin+Raylib in this branch)'
gl52_architecture: '_bmad-output/planning-artifacts/architecture/architecture-v1.md'
gl52_reviews: '_bmad-output/planning-artifacts/architecture/review/{adversarial-general,edge-case-hunter}.md'
prototype_reference: 'game/ (the proven-fun Godot prototype, PR #11/#12 — reference, not codebase)'
golden_harness_reference: 'ThePrimeagen golden-image testing (scripted test frames + render-to-texture + golden compare + agent-readable diffs)'

stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8, 9]
workflow: 'gds-game-architecture (headless, adapted to the packet-plumber-odin-architecture briefing)'
---

# Packet Plumber — Odin Architecture

> **What this document is.** The technical architecture for the **Odin + Raylib
> pivot** — the full re-plan the user committed to ("let's move to Odin, let's
> own it end to end"). It **evolves** the reviewed GL5.2 (Godot) architecture's
> *design* into Odin — every system boundary, every fairness contract, every
> edge-case ruling that GL5.2 + its review swarm produced is carried forward and
> re-expressed natively. It does **not** re-brainstorm the game: the GDD, forge
> locks, art canon, and narrative are engine-agnostic and survive untouched.
> It also does what the user explicitly asked for: **highlight the GL5.2
> architecture's misses honestly** (§14) — the pivot fixes some of them for free,
> and pretending otherwise would corrupt the re-plan.
>
> **Buildable-core-first.** This doc is optimized so the **early Odin prototype
> (Heist 2)** can be implemented from it immediately. Systems are tagged
> **[PROTO]** (the buildable core — Simulation Core, Raylib rendering, the
> golden-image harness, the fun-test systems) or **[LATER]** (spec'd but
> post-prototype: Era machine, Economy/Score, Leaderboard). When a conflict
> arises between "exhaustive" and "buildable tomorrow," buildable wins.
>
> Citation tags trace choices to source: `[FORGE #n]` (forge locks), `[GDD §]`,
> `[GL5.2 §]` (the prior architecture), `[LOOK §]` (look-book v1 canon),
> `[REVIEW m#]` (the GL5.2 review findings). Provenance for decisions lives in
> the ODN-ADRs (§5) and the disposition table (§17).

---

## 1. Executive Summary

**Packet Plumber** is rebuilt in **Odin (dev-2026-08) + raylib 6.0** —
a data-oriented language with no runtime engine between us and the machine —
targeting Steam PC/Mac first, landscape 1280×720 design grid, one input-agnostic
game `[FORGE #6]`.

The architecture keeps GL5.2's load-bearing invariant — **the simulation is
deterministic from a seed** — and makes it *native* instead of aspirational:

- **The Simulation Core is pure Odin.** Zero vendor imports, zero OS calls,
  zero floats on state-affecting paths. Determinism stops being a discipline
  enforced by grep gates (GL5.2's approach) and becomes a *structural property*:
  the core is a package of pure procedures over plain data that cannot touch a
  renderer, a clock, or a global even by accident. The same source compiles
  into the game, the test harness, and (later) the server-side leaderboard
  validator — GL5.2's "door left open" becomes a doorway (`[REVIEW m6]`
  resolved, §14.1).
- **Data-oriented by construction.** Packets, pipes, and flows live in Odin's
  native `#soa` (struct-of-arrays) containers with fixed-capacity pools and
  free lists. "Play the internet" is a data-heavy simulation; Odin's hot
  integer loops over contiguous buffers are exactly the shape of the problem.
  No node tree, no scene graph, no per-entity heap objects.
- **Rendering is raylib, and nothing else touches raylib.** The light-canvas
  Mini Motorways canon (look-book v1: literal buildings, round capacity-scaled
  router pucks, bezier pipes, blue/grey packets, procedural land/ocean map)
  maps directly onto raylib's immediate-mode 2D drawing. The presentation layer
  reads per-tick snapshots and interpolates to 60 fps.
- **The golden-image test harness is a first-class system, built before feature
  stories** (§10). Scripted demos + test frames (time + mouse) + render-to-
  texture + golden compare + agent-readable pixel diffs — the LLM-verification
  loop that makes LLM-driven Odin development safe. Raylib 6.0's new **software
  renderer (`rlsw`) + headless `PLATFORM_MEMORY` backend** make pixel goldens
  bit-identical across machines with no GPU and no display — a material upgrade
  over what GL5.2 could have done in CI.
- **The fun-test loop is the prototype scope:** Topology, PacketFlow, QoS,
  Crisis (Surge), NetworkHealth — the systems the surge-survival fun gate
  exercises. Era progression, Economy/Score, and the Leaderboard seam are
  spec'd here but marked **[LATER]** (§13).

**Decisions made:** 18 (§5; GL5.2 disposition map in §17). **GL5.2 misses
surfaced + resolved:** 6 (§14) — plus the pivot's costs, carried honestly.
**Systems:** 8 core (5 PROTO + 3 LATER) + 5 supporting + the harness.

---

## 2. Project Context

### 2.1 Game Overview

**Packet Plumber** — a network engineer keeps the internet alive by drawing
pipes between nodes, routing colored packets by type through class queues,
predicting fair crises from warning signs, and upgrading infrastructure as the
internet evolves across six eras within a single open-ended run `[GDD § Vision]`.
The game design is **locked and unchanged** — this doc re-targets the
*implementation*.

### 2.2 Technical Scope

| Attribute | Value | Source |
|---|---|---|
| Genre | Top-down 2D routing puzzle (hybrid: +sim/crisis-mgmt) | `[GDD]` |
| Language | **Odin `dev-2026-08`** (pin; recheck at phase boundaries) | verified 2026-08-08 (odin-lang/Odin releases) |
| Renderer / platform lib | **raylib 6.0**, via Odin's `vendor:raylib` bindings (bindings fixed for 6.0 in Odin dev-2026-07a) | verified 2026-08-08 |
| Base viewport | 1280×720 landscape design grid; the window is resizable and reveals more map (the GL5.2 `aspect=expand` doctrine, re-implemented as a camera-fit calculation, §9.1) | `[RULING — user]` |
| Platforms | **Desktop-first launch** (Steam PC/Mac; Linux is the dev/CI platform) — **ruled 2026-08-08** (§18, lavish): mobile follows when the Odin+raylib toolchain matures; `[FORGE #6]` amended accordingly | `[RULING — user, lavish 2026-08-08]` |
| Framerate | **60 fps sustained**; optional unlocked toggle on capable displays | `[GDD § Performance]` |
| Networking (gameplay) | None — single-player v1.0 | `[GDD OQ-2]` |
| Networking (service) | Leaderboard backend — v1.0 dependency, **[LATER]** layer, prototype stubs it | `[GDD § Online Services]` |
| Tests | `odin test` for the core (pure, no engine); the golden-image harness for visual regression; CI build matrix | §10, §16 |

### 2.3 Core Systems Requiring Architecture

| # | System | Complexity | GDD ref | Layer |
|---|---|---|---|---|
| S1 | **Topology Graph** (nodes + pipes, adjacency, span) | Medium | M1, M3 | **[PROTO]** |
| S2 | **Packet-Flow Simulation** (routing, bandwidth, contention, SLA) — QoS class queues + SLA accumulators live *inside* it (§14.2) | **High** | M2, Core Loop | **[PROTO]** |
| S3 | **QoS class queue model** (per-pipe 3-class-queue WFQ allocation + node serialization) — a pure-proc collaborator of S2, not a peer system | **High** | M2 | **[PROTO]** (inside S2) |
| S4 | **Crisis Engine** (warnings, Surge archetype, fairness contract) | Medium-High | M5 | **[PROTO]** (Surge only) |
| S5 | **Network Health** (loss meter, drain/recharge/grace) | Medium | Win/Loss | **[PROTO]** |
| S6 | **Era State Machine** (unlocks, legacy, transition) | Medium | M4 | **[LATER]** |
| S7 | **Economy / Score** (run scoring, budget) | Low-Medium | Economy | **[LATER]** (prototype uses a hardcoded draw budget constant) |
| S8 | **Meta / Leaderboard** (client seam + future service) | Medium (service) | Replayability | **[LATER]** (no-op stub in prototype) |
| — | **Golden-Image Test Harness** (§10) | Medium | (the LLM-verification foundation) | **[PROTO]** — built *first* |
| — | Draw Interaction (input → topology edit) | Medium | M1, Controls | **[PROTO]** (mouse; touch/controller follow) |
| — | View / Render Layer (snapshot → light-canvas scene) | Medium | Art canon | **[PROTO]** |
| — | Input Abstraction (mouse/touch/controller → intent) | Medium | Controls | **[PROTO]** (mouse first) |
| — | Audio Manager (Suno music + reactive SFX) | Low | Audio | **[LATER]** (prototype: silent or 3 stings, §13) |
| — | Save / Run (seed + action log) | Medium | Run § | **[LATER]** for players; the **replay mechanism itself is [PROTO]** — the harness consumes it (§10) |

### 2.4 Complexity Drivers

1. **Determinism (HIGH).** Same driver as GL5.2 — seeded runs must replay
   bit-for-bit for fairness + leaderboard validation. In Odin this becomes a
   structural property of the core package, not a discipline (§5 ODN-1/9/10).
2. **Packet-flow at scale (HIGH).** Late-era maps (~20–30 nodes, hundreds of
   in-flight packets) at 60 fps. The SOA + fixed-pool design makes the sim
   cheap; the renderer is a handful of batched draw calls per frame (§12).
3. **Fair-crisis traceability (MEDIUM-HIGH).** Unchanged contract `[FORGE #3]`;
   carried as executable test contracts (§11.3).
4. **The QoS decision surface (HIGH, novel).** GL5.2's custom queueing model
   carries over unchanged in *design*; in Odin it becomes pure integer procs
   over SOA lanes (§6.3, §11.2).
5. **The verification loop (HIGH, new).** In Godot, an LLM agent could lean on
   the editor + MCP scene inspection. In Odin there is no editor — **the golden
   harness is how the agent sees.** It is therefore a core system, not a test
   afterthought (§10).
6. **No engine safety nets (MEDIUM, new).** No scene tree, no autoloads, no
   GC, no inspector. Memory, lifetime, and wiring are explicit. Mitigated by
   arenas + explicit context passing (ODN-13/18) and the harness.
7. **Cross-platform input parity (MEDIUM).** Same-game doctrine `[FORGE #6]`;
   mouse first for the prototype, touch/controller behind the same intent layer.
8. **Mobile timing (MEDIUM, new — the pivot's honest cost, now ruled).**
   `[FORGE #6]` locked Steam + mobile same-game; Odin+raylib mobile is
   emerging, not turnkey. **Ruled 2026-08-08 (lavish): desktop-first launch;
   mobile follows when the toolchain matures** — the same-game doctrine is
   amended to a *sequencing*, not abandoned: the intent-layer input model
   (ODN-12) and camera-fit framing (§9.1) keep mobile addable without
   re-architecture, and a maturity spike is re-evaluated at the production
   gate.

### 2.5 Technical Risks (carried; mitigations)

| Risk | Mitigation |
|---|---|
| Fun must survive re-implementation (the Godot prototype proved it; the Odin build must reproduce it) | The golden harness replays the *same* scripted scenarios on the new core; the surge-survival loop is rebuilt first; the Godot prototype stays reachable as the behavioral reference via the `prototype-fun-gate` tag (§13.3) |
| Mobile timing under the pivot | Ruled: desktop-first launch, mobile follows at toolchain maturity (§18); the intent layer + camera-fit keep mobile additive, not a re-architecture; maturity spike re-evaluated at the production gate |
| No editor → slower iteration on layout/feel | Golden harness + data-driven catalogs + fast Odin compile; debug overlay with live balance sliders (§7.6) |
| Determinism regressions (the silent killer) | State-hash goldens run in every CI job; the replay-equality contract is a unit test (ODN-10) |
| Ecosystem/documentation thinner than Godot's | Context7 Odin docs pinned as agent tooling; `vendor:raylib` is shipped with the compiler (no dependency drift); versions pinned (§16) |
| Manual memory bugs (no GC) | Arena discipline (ODN-18): sim state in a run arena, per-frame temp in a frame arena; `core:mem` tracking allocator in dev builds to catch leaks |

---

## 3. Language & Framework

### 3.1 Selected stack (the pivot — locked by the user, not re-decided here)

- **Odin `dev-2026-08`** (released 2026-08-06; verified 2026-08-08). Pin exact;
  recheck at phase boundaries. Odin releases monthly; the pin moves only
  deliberately (a `.odin-version` file + CI enforce it).
- **raylib 6.0** (released 2026-04-23; verified 2026-08-08) via Odin's
  **shipped `vendor:raylib`** bindings (6.0-binding fixes landed in Odin
  dev-2026-07a). No third-party package manager, no dependency drift — the
  bindings ship with the pinned compiler.

**Why this pivot serves the design (honest accounting, both directions):**

*What Odin+Raylib gives the game that Godot could not:*
- **Determinism native** — no engine types in the core; integer-only sim paths;
  an owned PRNG (ODN-9); SOA memory layout. The leaderboard re-sim story stops
  being aspirational (`[REVIEW m6]`, §14.1).
- **Data-oriented performance for free** — `#soa` containers are a language
  feature; the packet sim is exactly the workload Odin is designed around.
- **No engine trap surface** — the entire `[FinLT]` trap class (deferred frame
  semantics, theme propagation, JSON int-float churn, headless-no-renderer,
  silent GDScript int truncation, reserved words) **evaporates**. GL5.2 spent
  real architecture on surviving its engine; this doc spends it on the game.
- **True headless verification** — `odin test` needs no engine; pixel goldens
  run on raylib 6.0's software renderer with no GPU/display (§10).
- **One compiled artifact per platform** — trivial distribution, tiny binaries,
  no export-preset labyrinth.

*What it costs (stated, not hidden):*
- No visual editor / scene tree / inspector — layout and level tooling are
  code + data (mitigated: procedural maps, JSON catalogs, debug overlay).
- No engine-provided UI, animation, or tweening — a minimal immediate-mode
  widget set is built once (§9.2) — and interpolation is ~20 lines (§9.1).
- Manual memory (no GC) — mitigated by arena discipline (ODN-18).
- Mobile export is no longer one click — ruled desktop-first (§18 OQ-1).
- A smaller community/thinner StackOverflow corpus — mitigated by the golden
  harness (the agent verifies empirically instead of pattern-matching) and
  pinned Context7 docs.

### 3.2 What the stack provides

| Concern | Provided by | Notes |
|---|---|---|
| Window/input/2D drawing/audio | raylib 6.0 (`vendor:raylib`) | Immediate-mode; we build the camera-fit + widget layer (§9) |
| Render-to-texture | `rl.RenderTexture` | The golden-harness capture path (§10) |
| Headless pixels | raylib 6.0 `rlsw` software renderer + `PLATFORM_MEMORY` backend | Built from source for the harness only (§10.4) |
| Unit testing | `odin test` + `core:testing` (`@(test)`, `testing.T`) | Core tests need no window, no GPU |
| Data-oriented containers | `#soa[N]T`, `#soa[dynamic]T`, `soa_zip` | Native language feature (verified, odin-lang docs) |
| Memory | `core:mem` arenas, tracking allocator, explicit `context.allocator` | ODN-18 |
| Serialization | `core:encoding/json` for catalogs; hand-rolled little-endian writer for the action log (ODN-11) | No Godot `Resource` dual-format (§14.4) |
| Desktop builds | `odin build -target:{windows_amd64, darwin_arm64, linux_amd64, ...}` | Native CI runners per OS (§16) |
| Audio | `raudio` (in vendor:raylib) | Suno-owned tracks doctrine unchanged (§9.6) |
| **Nothing** for the sim core | — | The core imports only `core:*` — and for PROTO, not even `core:os` (§4) |

### 3.3 Remaining architectural decisions (made explicitly in §5)

Language choice does not decide: the sim/presentation separation, the tick
model, the PRNG, the data model, the save/log format, the harness design, the
QoS queueing model, the event mechanism, memory arenas, or the input
abstraction. Those are §5 + §11.

### 3.4 AI Tooling

| Tool | Purpose | Status |
|---|---|---|
| **Context7** (`upstash/context7`) | Live Odin + raylib doc lookup (training data lags both) | **Adopted** (used in writing this doc) |
| **The golden harness** (§10) | The agent's eyes — screenshots, replays, pixel diffs | **First-class system** |
| GoPeak Godot MCP | — | **Obsolete** (Godot-only); the prototype remains runnable from the `prototype-fun-gate` tag for behavioral comparison |

> There is no editor MCP for Odin/Raylib and none is needed: the agent edits
> plain source and verifies through the harness. This is the LLM-coding reframe
> the pivot is predicated on — the harness *is* the tooling.

---

## 4. System Architecture (the layering)

```
┌──────────────────────────────────────────────────────────────────────┐
│  EXECUTABLES (three build targets, one shared core)                  │
│   app/      — the game (raylib window, input, render, audio)         │
│   harness/  — the golden-image test runner (§10)                     │
│   (`odin test core` runs the co-located @(test) unit tests)          │
├──────────────────────────────────────────────────────────────────────┤
│  PRESENTATION LAYER  (package render + package ui — raylib allowed)  │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│   │ Input Layer  │→ │  View Layer  │← │ Audio Layer  │  [PROTO:     │
│   │ raw raylib   │  │ snapshot →   │  │ raudio;      │   input+view;│
│   │ events →     │  │ light-canvas │  │ LATER]       │              │
│   │ intents      │  │ scene, 60fps │  │              │              │
│   └──────┬───────┘  └──────▲───────┘  └──────▲───────┘              │
│          │ intents         │ snapshot(s)     │ events                │
├──────────▼─────────────────┼─────────────────┼──────────────────────┤
│  ORCHESTRATION LAYER  (package run — still no raylib)                │
│   ┌──────────────────────────────────────────────────────────┐      │
│   │ App struct   (mode FSM: menu/run/pause/gameover)         │      │
│   │ Sim_Driver   (fixed-timestep accumulator → core.step)    │      │
│   │ Command_Bus  (validate intents → commands → apply)       │      │
│   │ Save_System  (seed + action log ↔ file)        [LATER]   │      │
│   └──────────────────────────┬───────────────────────────────┘      │
│                              │ step(tick, commands)                 │
├──────────────────────────────▼──────────────────────────────────────┤
│  SIMULATION CORE  (package core — pure Odin, deterministic,          │
│                    headless, portable; zero vendor/os imports)       │
│   ┌─────────────┐ ┌─────────────────────────┐ ┌───────────────────┐ │
│   │ Topology    │ │ Packet_Flow             │ │ Crisis_Engine     │ │
│   │ (nodes+     │ │ (routing, bandwidth,    │ │ (congestion metrics,  │ │
│   │  pipes,     │ │  contention, drops)     │ │  warnings, Surge; │ │
│   │  adjacency, │ │   └── QoS class queue procs    │ │  root-cause       │ │
│   │  span,bndl) │ │   └── SLA accumulators  │ │  contract)        │ │
│   └─────────────┘ └─────────────────────────┘ └───────────────────┘ │
│   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────────┐ │
│   │ Network_    │ │ Era_FSM     │ │ Economy/    │ │ Rng (owned    │ │
│   │ Health      │ │ [LATER]     │ │ Score       │ │ PRNG, seeded) │ │
│   │             │ │             │ │ [LATER]     │ │               │ │
│   └─────────────┘ └─────────────┘ └─────────────┘ └───────────────┘ │
│         reads catalogs (data-driven, loaded once, read-only)        │
├──────────────────────────────────────────────────────────────────────┤
│  DATA LAYER  (data//*.json — single source, §8)                  │
│   packet_types · pipe_tiers · node_types · eras · crises · balance   │
├──────────────────────────────────────────────────────────────────────┤
│  META SEAM  [LATER]                                                  │
│   Leaderboard_Service (proc-table interface — no-op stub | HTTP)     │
└──────────────────────────────────────────────────────────────────────┘
```

**The import rule (the spine, made structural).** `package core` imports only
whitelisted `core:*` packages (`core:mem`, `core:slice`... — and **not**
`core:os`, `core:time`, `core:fmt`-for-side-effects). It never imports
`vendor:*`. CI enforces this with a one-line check (§16.3): the package must
compile to an object file with no OS/renderer symbols. In GL5.2 this rule was
a grep gate on `scripts/core/`; here the package system makes it a compile
fact.

**Data flow (one logic tick)** — unchanged in shape from GL5.2 §4 (the design
survived review); re-expressed in Odin:

```
 raw input ──▶ Input Layer ──▶ intents ──▶ Command_Bus.validate
                                              │
                                              ▼
   EDIT FAST-PATH (ODN-2): validated commands apply to Topology IMMEDIATELY
   (same frame, even paused) and are logged with apply_tick = next tick.
                                              │
 Sim_Driver.step(tick):  live play passes no pending commands (they already
   landed); REPLAY feeds the tick's log entries into step, which applies
   them first — the same topology_apply_all authority, so live and replay
   see identical state at every step boundary:
        │
        ▼
   director.demand_plan(topology, era, tick, rng) ──▶ Demand_Plan
        │                                               (map growth + demand)
        ▼
   Packet_Flow.step(tick, rng, topology_snapshot, demand)
        │   ├─ forward (per-hop + ECMP; junction = repeater, span resets)
        │   ├─ qos_allocate(pipe)      ← QoS procs, INSIDE the flow step
        │   ├─ qos_serialize(node)     ← work-conserving gap-fill + WRR floor
        │   ├─ advance packets (bandwidth units/tick, integer)
        │   ├─ contend/drop by class queue (BE → Standard → Express)
        │   └─ sla_accumulate(class)   ← SLA accumulators, INSIDE the flow
        ▼
   Crisis_Engine.evaluate(tick, topology, flow, era)   (downstream of flow)
        ▼
   Network_Health.update(tick, sla_state)              (downstream)
        ▼
   Era.step(...)  [LATER]  ·  Economy.score(...)  [LATER]
   (terminal-event barrier: nothing after Run_Lost — one terminal event/run)
        │
        ▼
   snapshot_write(state) ──▶ immutable Snapshot (SOA memcpy into a
        │                      per-tick snapshot slot — double-buffered)
        ▼
   events buffer (every event tick-tagged) ──▶ Presentation drains once per
                                                frame, in append order

 View Layer ◀── reads snapshots[t-1], snapshots[t] (lerp between them)
```

The **snapshot** remains the sole contract between Core and Presentation: the
View reads only immutable snapshots; it can never perturb the sim. In Odin the
snapshot is no longer a bespoke projection object — the core state *is* plain
SOA data, so a snapshot is a memcpy into a double-buffered arena slot (ODN-1).
"Full snapshot vs diff" (`[REVIEW m8]`) is settled for good: full snapshot
always; at hundreds of packets the copy is microseconds.

---

## 5. Architectural Decisions

GL5.2 ADR-1..16 are **dispositioned** in §17 (kept / evolved / obsolete). The
decisions below are the Odin architecture's own — numbered ODN-1..18.

### 5.1 Decision Summary

| # | Decision | Choice | Layer | Rationale (short) |
|---|---|---|---|---|
| ODN-1 | Sim/Presentation separation | Pure `package core`; presentation separate; snapshot = SOA memcpy | PROTO | Determinism structural, not disciplined; §14.1 |
| ODN-2 | Logic tick | Fixed 20 Hz accumulator; latency in integer ms (sub-tick) | PROTO | `[GL5.2 ADR-2]` + `[REVIEW m16]` carried |
| ODN-3 | QoS model | 3 DiffServ lanes, integer WFQ weights, work-conserving + WRR floor — pure procs **inside** Packet_Flow | PROTO | `[FORGE #4]`; §14.2 ownership resolution |
| ODN-4 | Crisis model | Root-cause-driven, warning-first, fairness-as-test-contract | PROTO | `[FORGE #3]` carried |
| ODN-5 | Content catalogs | **JSON single source** (no dual .tres/JSON); validated at load; `#load`-embedded in release | PROTO | §14.4; hot-iterate stays |
| ODN-6 | Leaderboard seam | Proc-table interface; PROTO = no-op; production = HTTP client + **the same compiled core** as validator | LATER | §14.1 — re-sim becomes real |
| ODN-7 | CrisisDirector seam | A proc field on Run_Config (`demand_plan`); PROTO impl = scripted; V2 = AI auditor | PROTO seam | `[FORGE weak #4]`; zero-boilerplate in Odin |
| ODN-8 | Packet storage | SOA pools + free lists; **no view-side per-packet objects at all** (dots are draw calls from snapshot arrays) | PROTO | Perf; the Godot node-pool concept evaporates |
| ODN-9 | RNG | **Owned PRNG in the core** (splitmix64-seeded PCG32 XSH-RR, ~40 lines, reference-pinned test vectors); not `core:math/rand`; **ECMP next-hop = pure splitmix64 hash** (not an rng draw) | PROTO | Toolchain-independent determinism |
| ODN-10 | Math + iteration discipline | Integer-only state paths; **no `map` iteration in core** (arrays/slices only); ties → seeded rng (ECMP = pure hash); **forwarding table rebuilt on topology-change only; bundled cap = static sum** | PROTO | `[REVIEW M5]` carried + made native; routing 4-rule (lavish 2026-08-10) |
| ODN-11 | Save format | Seed + era + modifiers + action log; **little-endian binary**, versioned header; no JSON for logs | LATER (mechanism PROTO) | Kills the JSON int-float trap at the root |
| ODN-12 | Input model | Raw raylib input → `Intent` → validated `Command`; snap-to-node in the bus; mouse first | PROTO | `[FORGE #6]` parity preserved |
| ODN-13 | App state | Explicit `App` struct + mode enum; **no globals/singletons anywhere**; context passed by pointer | PROTO | §14.5 — autoloads evaporate |
| ODN-14 | Communication | **Tick-tagged event buffer** (tagged union array), drained per frame in append order; replaces signals | PROTO | §14.6 — ordering is program order |
| ODN-15 | Audio | Suno-owned doctrine; raudio; **dedicated cosmetic PRNG stream** (not a global-RNG exception) | LATER | `[BRIEF]`; keeps ODN-9 absolute |
| ODN-16 | Prototype scope gate | Sim Core + Raylib view + harness + fun-test systems first; Era/Economy/Leaderboard later | PROTO | The briefing's buildable-core-first mandate |
| ODN-17 | Golden-image harness | First-class system, built **before** feature stories; rlsw + PLATFORM_MEMORY for bit-exact CI pixels | PROTO | §10 — the LLM-verification foundation |
| ODN-18 | Memory model | Three arenas: run (sim state), snapshot (double-buffered), frame (temp, reset per frame); tracking allocator in dev | PROTO | No GC; lifetimes structural |

### 5.2 Decision Detail

#### ODN-1 — Simulation Core / Presentation separation (the spine, native)

**Context.** GL5.2's ADR-1 proved the *design*: a pure core, stepped by tick,
never reading the clock, emitting immutable snapshots. Its weakness was
*enforcement* — GDScript can't stop a contributor from touching a node; the
gate was a grep rule and a parse test.

**Decision.** The core is Odin `package core` (`core//`): plain structs,
SOA containers, and pure procedures. It imports only whitelisted `core:*`
packages (never `vendor:*`, never `core:os`/`core:time`), holds **all**
authoritative state in one `Run_State` struct tree, and steps only via:

```odin
// core/ — the ONLY entry point that advances the simulation
step :: proc(state: ^Run_State, tick: u64, commands: []Command) {
    topology_apply_all(&state.topology, commands)              // atomic batch (E23);
    // replay/tooling entries — live edits already landed via the fast-path
    plan := state.config.demand_plan(state.topology.snapshot(), state.era,
                                       tick, &state.rng) // ODN-7: read-only view
    flow_step(state, tick, plan)                                // QoS + SLA inside (ODN-3)
    crisis_evaluate(state, tick)
    health_update(state, tick)
    // era_step / economy_score — [LATER] layers, called here when present
    // Terminal-event barrier (E17, §6.5): once Run_Lost is appended, the
    // remaining systems in the tick are skipped — one terminal event per run.
}
```

The **Presentation layer** (`app/`: `package render`, `package ui`) is the
only code allowed to import `vendor:raylib`. It receives `Snapshot` pointers
(read-only) and the drained event buffer.

**Snapshot = memcpy.** `Run_State` is SOA containers + value structs. A
snapshot is a copy of the live arrays into one of two pre-allocated snapshot
slots (ping-pong). The view lerps between `snap[t-1]` and `snap[t]` for 60 fps
motion from a 20 Hz sim (ODN-2). No bespoke projection types, no diff format,
no per-node diffing — the GL5.2 `(or a diff)` hedge (`[REVIEW m8]`) is gone.

**Consequences.** + determinism is a compile-time fact; + `odin test` exercises
the entire game headlessly; + the identical source compiles into the server
validator (ODN-6); + the harness drives the core with zero stubs. − the
discipline cost moves to memory management (ODN-18) and the import whitelist
(§16.3).

#### ODN-2 — Fixed-timestep logic tick (carried, unchanged design)

`LOGIC_HZ = 20` (50 ms/tick, tunable in `balance.json`). The app accumulates
clamped wall-clock (`dt = min(dt, 0.25)` — the `[FinLT]` clamp carried as a
rule, now trivially typed since Odin won't silently truncate) and steps the
core N times to catch up, capped against the spiral-of-death. **Sim slower
than real-time → slow-mo, never tick-skipping** (E21, carried). Latency SLAs are tracked in **integer milliseconds** (sub-tick resolution —
the Gaming class's < 80 ms SLA needs it; `[REVIEW m16]` carried).

**The edit fast-path (premium feel, made mechanical).** Player edits are *not*
tick-gated: a validated Command applies to the Topology **immediately on
arrival**, between steps — the same frame, and even while paused (the GDD's
pause-and-plan doctrine requires paused redesign to work). Determinism is
preserved by the action log: the edit is recorded with `apply_tick` = the next
tick the sim will execute, and replay applies all log entries for tick N
**before** stepping N. Live play and replay therefore see identical state at
every step boundary, while the player sees their edit land the instant they
make it (the view re-snapshots topology-only on edit). This is the GL5.2
Open-Q1 ruling carried — this time with the mechanism written down (§11.1).

#### ODN-3 — QoS: 3 DiffServ lanes, integer WFQ, inside the flow (the ownership fork, decided once)

**Decision (design unchanged from GL5.2 ADR-3 + the review's M3 fix — now
structural).** Each pipe carries 3 class queues (Express/Standard/Best-effort);
bandwidth partitions by integer WFQ weights (`weights: [3]i32`); node
serialization is work-conserving with gap-fill plus a weighted-round-robin
floor (≥1 slot per class queue per window — no starvation, E7); contention drops by
drop precedence, BE → Standard → Express (E9); allocation uses the
largest-remainder rule with Express→Standard→Best tie order (E8).

**Player surface (user ruling 2026-08-14, story 5.8).** A per-pipe QoS panel
replaces the invisible emphasis dial: the weight set auto-follows the player's
type→class-queue assignments from a data-driven ladder (`lane_auto_reserve_ladder` in
`balance.json`: 1 class queue = 100 · 2 = 70/30 · 3 = 50/30/20 — playtest-tunable)
unless the player sets manual weights. The type→lane call stays player-owned;
only the split auto-follows.

**The ownership resolution (§14.2).** GL5.2's pre-review canonical tick code
referenced phantom peers (`state.sla.accumulate`, `state.qos.apply`) that
contradicted its own data model. Decided once, here and forever:

- **QoS is not a system.** It is a set of pure procs (`qos_allocate`,
  `qos_serialize`) in `package core`'s flow files, called by `flow_step`.
  Lane weights/policies live on pipes/nodes (Topology owns the *data*).
- **SLA accumulators are fields of the flow state** (`Flow_State.sla`), fed
  inside `flow_step`, read downstream by Crisis/Health. There is no `state.sla`
  peer because there is no SLA system — there is a struct of counters.

```odin
Sla_Accumulator :: struct {
    delivered, dropped:      u64,
    total_latency_ms:        u64,
    breach_window_ticks:     u32,
    // zero-demand tick = neutral (E24): callers check demand before reading ratios
}
Flow_State :: struct {
    packets: #soa[dynamic]Packet,          // ODN-8 pool
    free:    [dynamic]u32,                 // free-list of packet slots
    sla:     [dynamic]Sla_Accumulator,     // indexed by class id
    // ...
}
```

#### ODN-4 — Crisis Engine: root-cause-driven (carried, Surge only for PROTO)

Unchanged design `[FORGE #3]`: congestion metrics from Topology + Flow each tick →
warning signs (🟡/🔴, congestion, forecast, wear) → crisis fires only on
measurable visible congestion; every archetype carries a structured `root_cause`
+ a preventive redesign; the 4 fairness rules are executable test contracts
(§11.3). **PROTO ships the Surge archetype only**; the archetype table is
data (`crises.json`), so the remaining four are content + evaluation procs,
not re-architecture. The Director owns the demand timeline **upstream** of the
flow; the Crisis Engine evaluates **downstream**; the Director must never read
crisis state to force a crisis (`[REVIEW M1]` carried as an explicit rule).

#### ODN-5 — Data-driven catalogs: JSON single source

**Decision.** All balance/content lives in `data//*.json`:
`packet_types`, `pipe_tiers`, `node_types`, `eras` [LATER], `crises`,
`balance`. **One format, one source** — GL5.2's `.tres` + JSON mirror was two
sources of truth kept in sync by discipline (§14.4). Odin has no Inspector, so
the dual format loses its only justification.

- Dev builds read the JSON at startup (edit → restart → test; Odin compiles
  fast enough that even recompile-in-the-loop is quick).
- Release builds embed the same JSON via `#load()` — byte-identical content,
  no runtime file dependency.
- **Load-time validation is fail-fast:** unknown fields, out-of-range values,
  cross-reference errors (a packet type naming a lane that doesn't exist)
  abort startup with a named error. Catalogs are read-only after load.
- Determinism note: catalogs contain **integers only** for sim-relevant values
  (capacities, weights, thresholds, ms latencies). Cosmetic floats (colors as
  0–255 RGBA quads, pulse rates) are labeled cosmetic and never read by core.

#### ODN-6 — Leaderboard service seam (the m6 payoff, upgraded honestly)

**Decision.** `Leaderboard_Service` is a struct of proc pointers (Odin's
native interface idiom — §11.5): `submit`, `fetch_board`, `poll`. PROTO binds
a no-op local impl. Production binds an HTTP client (`core:net` or a vendored
HTTP lib — a production decision, not this doc's).

**The upgrade the pivot buys:** GL5.2's validation strategy was *lean* because
full re-sim needed a portable core it didn't have (`[REVIEW m6]`). Here the
core is portable by construction — the server validator can **compile the same
`package core`** into the backend (any language hosting it via C-ABI, or a
small Odin validator service). Full per-submission re-sim becomes cheap and
bit-exact; the lean-vs-full validation decision moves from "constrained by
portability" to a pure cost/ops choice at production time. The submission
payload carries `(seed, era_progress, modifiers, action_log_summary, score)`
— `modifiers` included from day one (`[REVIEW m14]` carried).

#### ODN-7 — CrisisDirector seam as a proc field (carried, de-boilerplated)

All crisis *congestion* (demand timeline + surge scheduling + map growth) flows
through one proc pointer on the run config:

```odin
Run_Config :: struct {
    seed:          u64,
    modifiers:     []Modifier_Id,          // daily/weekly twists; [] for standard
    demand_plan: proc(topology: Topology_Snapshot, era: Era_State,
                        tick: u64, rng: ^Rng) -> Demand_Plan,
    // ^ read-only view in, plan out; pure w.r.t. sim state — the M1 rule
    // ("the Director must never read crisis state") is structural, not discipline.
    leaderboard:   Leaderboard_Service,    // ODN-6
}
```

PROTO binds `scripted_plan_demand` (data-driven demand timeline — for PROTO
the surge curve lives in `crises.json` + `balance.json`; `eras.json` takes
over when the Era layer lands — seeded). V2 binds the AI auditor `[FORGE weak #4]`
behind the same field. GL5.2 needed an abstract-base-class convention +
`assert(false, "override me")` to fake this (`[REVIEW M4]`); Odin's proc
pointers make it one line, type-checked, zero ceremony. (GL5.2's own m12
observation — the seam earns its place in the architecture while the prototype
impl stays trivial — carries over exactly.)

#### ODN-8 — Packet storage: SOA pools, no view-side objects

**Decision.** Packets live in a fixed-capacity `#soa` pool with a free list
(ODN-18 arena). Slot indices are stable; **ids are monotonic per run** (E11 —
never recycled) by carrying a generation counter: `Packet_Id = {slot: u32,
gen: u32}` so a reused slot never aliases a stale id (replay-safe, E10/E11).

**The view owns nothing per-packet.** GL5.2 pooled `PacketDot` *nodes*; in
raylib there are no nodes. Each frame the view iterates the snapshot's packet
arrays and issues draw calls (circle/triangle/diamond per type — §9.1) at
lerped positions. "Pool exhaustion → drop lowest-priority class queue first" (E22)
becomes "sim-side pool is sized to the era ceiling; on exhaustion, spawn
fails as a BE-first drop" — the policy is identical, the mechanism is an
integer check, not a node allocation failure. PROTO pool size: the surge-slice
worst case (a few dozen); the constant lives in `balance.json` and the
late-era ceiling is an E10-scale tuning value, not a pre-allocation
(`[REVIEW m13]` carried).

#### ODN-9 — RNG: an owned PRNG with published test vectors

**Decision.** The core contains its own PRNG — **PCG32 XSH-RR** (64-bit state,
32-bit output — ample state for this sim) with seed expansion via
**splitmix64** — ~40 lines of explicit integer code with the algorithm's
constants written in the source (the canonical pcg-random.org PCG32 XSH-RR;
the pinned test vectors are generated once from that reference implementation).
**Not `core:math/rand`**: the stdlib's implementation may change between Odin
releases; our determinism guarantee must not depend on the toolchain's
internals.

```odin
Rng :: struct { state: u64, inc: u64 }   // PCG32 XSH-RR (64-bit state); seeded via splitmix64(seed)
rng_next :: proc(r: ^Rng) -> u32 { ... } // exact constants + shifts pinned in source
rng_range :: proc(r: ^Rng, lo, hi: u32) -> u32 { ... } // bounded; bias-avoidance note in code
```

- One `Rng` instance **held by `Run_State`** (it is core state; it serializes
  into the save, riding the action-log form as pure function of seed+log).
  Passed explicitly; there is no global RNG to forbid (§14.5).
- **Cosmetic randomness** (SFX variant, particle jitter) uses a **second,
  separately-seeded `Rng` owned by the app layer** (ODN-15) — never the sim's,
  never a library global. GL5.2's "global RNG exception" becomes "a second
  owned stream."
- **Fresh-run seeds** (GDD: each main run rolls a fresh seed) are drawn by the
  **app layer** from OS entropy (`core:crypto`) at run creation and logged in
  the save header (E32) — never from the sim rng (sequential runs must not
  correlate), never left unstated.
- **Test vectors are pinned:** seed 0's first 8 outputs are a unit test. Any
  future port (server validator, wasm build) must reproduce them — this *is*
  the cross-language determinism conformance test `[REVIEW m6]` asked for.
- Most equal-candidate tie-breaks draw from this rng (ODN-10 corollary,
  `[REVIEW M5]` carried). **The ECMP next-hop pick is the exception**
  (routing ruling, lavish 2026-08-10): among N equal-cost next hops it is a
  **pure hash** `splitmix64(src, dst, class, pkt_id) mod N` — reusing this
  decision's splitmix64 as a *deterministic finalizer*, **not** a draw from
  the sim rng. Same packet → same next hop on every replay (flow affinity, no
  intra-flow reordering), with zero dependence on sim-rng state or processing
  order. A pure hash (not an rng draw) is what makes per-packet forwarding
  byte-replay-identical without consuming rng state in the hot path.

#### ODN-10 — Integer math + array-only iteration (the determinism core)

**Decision.** All state-affecting computation is integer (`i32`/`u32`/`u64`) or
explicit fixed-point. Floats appear only in the view (lerp factors, pulse
phases) and never flow back. Odin integer semantics are bit-identical across
every target — the ARM-vs-x86 re-sim concern that forced GL5.2's discipline is
simply gone.

**Iteration determinism, made native.** Odin `map` iteration order is
unspecified — so the core **does not iterate maps at all**: topology adjacency,
packet pools, and spawn queues are arrays/slices; lookups may use maps but
*iteration* is always over the array (insertion-ordered, stable). Equal-
  candidate choices resolve via the seeded rng (ODN-9) — **except the ECMP
  next-hop pick**, which is a pure splitmix64 hash of the packet, not an rng
  draw (routing ruling, lavish 2026-08-10; see ODN-9). **Pinned test:** re-step
the same `(seed, action_log)` twice, assert byte-identical snapshot hashes —
  a unit test *and* the harness's tier-1 golden (§10.2).

**Routing determinism — per-hop forwarding + ECMP + bundles, kept
byte-replay-identical (routing ruling, lavish 2026-08-10).** The locked
full-game routing model is **as deterministic as the BFS it replaces** —
replays stay bit-identical — provided these four rules hold (the ODN-9/10
spine, restated for routing):

1. **Forwarding table rebuilt only on topology change, inside the tick**
   (synchronous — no async convergence). Each junction's `(junction, dst) →
   next hop` table is computed by a deterministic Dijkstra/SPF over INTEGER
   PIPE COSTS (insertion-order tie-breaks) and rebuilt only when a Command
   changes the topology — never per-packet, never per-tick.
2. **ECMP tie-break = a pure hash of packet identity** —
   `splitmix64(src, dst, class, pkt_id) mod N`, integer-only, pinned
   finalizer. **No sim-rng draw, no map iteration in the hot path** (tables
   are arrays indexed by slot, insertion-ordered).
3. **Bundled capacity is a static sum at table-build time** — the pooled
   capacity of a bundle is computed once when the table is built, not
   per-packet.
4. **Pinned by the existing replay test** (tier-1 golden, above): same seed
   + same commands → byte-identical snapshot, per-packet paths included.

Satisfy those four and per-hop + ECMP + bundles is as deterministic as
BFS-by-insertion-order. The spine holds. (And none of it is player-facing —
players draw pipes; the forwarding table + ECMP hash are implementation
details, not a UI surface.)

#### ODN-11 — Save = seed + action log, little-endian binary

**Decision (carried from GL5.2 ADR-11, mechanism upgraded).** A run is
`(seed, era_progress, modifiers, action_log[])`; replay reproduces the run
bit-for-bit; the same artifact is the leaderboard validation input (ODN-6) and
the debug-replay input (§7.6). The log is a **hand-rolled little-endian binary
format** with a versioned header — not JSON. This deletes the `[FinLT]`
JSON-int-to-float trap at the root instead of mitigating it per-load (§14.3),
and makes "byte-identical replay" a `mem.compare`.

**Replay-contract completeness (the fine print):**

- The versioned header also carries `catalog_hash` (FNV-1a-64 over the exact
  catalog bytes in force) **and `logic_hz`** — replay or leaderboard
  validation against different balance data is a **defined rejection**, never
  silent divergence. The same pair rides in the submission payload (ODN-6) and
  every golden manifest (§10.3).
- Log records store **post-validation, post-snap commands** (resolved node
  ids, not raw pointer positions): core-side validation is the single
  authority (the Command_Bus merely previews it for UX), and a command that
  fails validation during replay is a **critical error** (§7.1) — play and
  replay can never drift apart on legality.
- **Fast resume** (GL5.2's ruling carried): a full-state snapshot may be
  cached alongside the log as a *derived* artifact (regenerable by replay,
  never the source of truth). Native re-sim of even a long run is cheap, so
  the cache is a convenience, not a crutch — measure at production.

**PROTO note:** the log
writer/reader ships in PROTO *because the harness consumes it* (demos are
action logs; §10), even though player-facing save slots are [LATER]. All
timers (grace, meter) are pure functions of `(seed, log)` (E12 — load →
re-step → assert-match test).

#### ODN-12 — Input: raw events → Intent → Command (mouse first)

**Decision.** Three-stage: raylib raw input (mouse pos/buttons; later touch
gestures + gamepad) → semantic `Intent`s (`Begin_Draw{node}`, `Extend_Draw{pos}`,
`Commit_Draw{node}`, `Select{target}`, `Cycle_Tier`, `Set_Emphasis`,
`Pan_Zoom{delta}`, `Pause`) → validated `Command`s (`Draw_Pipe_Cmd`,
`Upgrade_Pipe_Cmd`, `Set_Lane_Weights_Cmd`, `Set_Junction_Policy_Cmd`) applied
through the Command_Bus (snap-to-node **inclusive** at radius (E4), span ≤ tier
max, budget, era unlock, no self-loop (E3), terminal demolish forbidden (E2)).
No input path mutates the core directly. **PROTO implements mouse** (the dev
platform); touch/controller are new mappings onto the *same intents* — parity
by construction `[FORGE #6]`, not a redesign. The harness scripts input at the
**Intent level over time** (§10.3), so a recorded demo exercises the exact
player path.

#### ODN-13 — App state: explicit context, no globals

**Decision.** One `App` struct (mode enum `Boot/Menu/Run/Paused/Game_Over`,
window state, settings, the `Run` context) created in `main` and passed by
pointer everywhere. **No globals, no singletons, no autoloads, no
`@(thread_local)` shared state.** GL5.2's autoloads (ADR-13) were global
mutable services with init-order and reset-per-run hazards; here the Run
context is a value owned by `App`, created/destroyed per run — reset is
"make a new one," which is *why* per-run reset can't leak state (§14.5).

#### ODN-14 — Communication: the per-tick event buffer

**Decision.** Cross-layer communication is an **event buffer**: during
`core.step`, systems append `Event` values (a tagged union —
`Packet_Arrived`, `Packet_Dropped`, `Sla_Threshold_Crossed`, `Warning_Raised`,
`Crisis_Triggered{archetype, root_cause}`, `Grace_Started`, `Meter_Changed`,
`Run_Lost`, `Era_Advanced` [LATER]…) to `Run_State.events`. **Every event
carries its `tick: u64`** — the demo assertion language (`expect event …
within 12000ms..16000ms`, §10.3) and event-stream goldens depend on tick
attribution. The app drains the buffer **once per frame, after the step
loop**, preserving append order (catch-up frames deliver their ticks' cues in
tick order, never interleaved). Signal precedence rules become **sim-side
suppression** (E17: `health_update` never emits `Grace_Expired` once the meter
is empty, and the terminal-event barrier (§4) skips the rest of the tick after
`Run_Lost` — one terminal event per run by construction, not "handled first
of two").

This replaces Godot signals wholesale (§14.6): ordering is program order
(inspectable in a replay), no deferred-vs-immediate subtlety, no stringly
names, no connection bookkeeping, and the event buffer is itself a golden-able
artifact (the harness can assert event sequences — cheaper than pixels for
logic regressions).

#### ODN-15 — Audio: Suno doctrine, dedicated cosmetic PRNG

**Decision (carried).** Suno-owned music + reactive SFX, paid-tier tracks
(Content-ID-free) `[BRIEF]`. Implementation is `raudio` (bundled in
vendor:raylib): `Music` streams for beds/stings, a small pool of `Sound`
aliases for concurrent SFX with 3–4 variants per recurring sound. Variant
selection draws from the **app-owned cosmetic `Rng`** (ODN-9) — determinism-
neutral by construction. Every audio alert is captioned on-screen (GDD
Accessibility). **[LATER] layer for the prototype** (§13): the fun test
proved out in graybox with minimal audio; PROTO carries at most the crisis
sting + arrival clicks if cheap.

#### ODN-16 — Prototype scope gate (the briefing's priority, made a decision)

**Decision.** The build order is **harness-first, then the fun-test core**,
then juice. Era/Economy/Leaderboard are spec'd (§6.6–6.8) but excluded from the
prototype branch — imported as `[LATER]` layer packages when Heist 3+ arrives.
This inverts GL5.2's "core full, content subset" (ADR-16): here the *prototype
itself* is a subset of systems, because the pivot's first question is "does
the Odin build reproduce the proven fun," not "is the full core ported." The
surge-slice needs: Topology, Packet_Flow (+QoS/SLA), Crisis (Surge),
Network_Health, the win/lose gate, draw interaction, the view, and the
harness. Full list + rationale in §13.

#### ODN-17 — The golden-image harness is a first-class system

**Decision.** The harness (§10) is built **before feature stories** and is a
release-gated CI citizen: scripted demos (seeded scenarios) + test frames
(time + mouse intents) + render-to-texture + golden compare + agent-readable
diffs + `save` to re-bless. Two verification tiers: **state-hash goldens**
(pure core, every platform, zero graphics) and **pixel goldens** (raylib 6.0
software renderer + memory platform — bit-identical across machines, no GPU,
no display). This is the system that makes LLM-driven Odin development
verifiable, and it is the prototype's regression net while the fun is being
matched against the Godot reference.

#### ODN-18 — Memory model: three arenas, no GC

**Decision.** All allocations route through explicit arenas:

| Arena | Lifetime | Holds |
|---|---|---|
| (app-owned, program lifetime) | process | the loaded catalogs (ODN-5); `Run_State` holds refs into them |
| `run_arena` | one run (created/reset per run) | `Run_State`, SOA pools, the route slab |
| `snapshot_arena` | ping-pong slots, overwritten per tick | snapshot copies (ODN-1) |
| `tick_arena` | reset at the top of every `core.step` | core scratch (serialization orderings, route recompute) |
| `frame_arena` | reset every frame | view scratch (lerp buffers, draw batches), event drain copies |

Dev builds run `core:mem`'s tracking allocator to report leaks; there is no
per-frame heap churn by construction (the frame arena makes "allocate per
frame" free and leak-proof). Packet slots recycle within the fixed pool
(ODN-8). The rule for agents: **core code never calls `new`/`make` without an
explicit allocator argument** — enforced by review + a CI lint (§16.3).

---

## 6. Core Systems (boundary + interface + data)

> Each system: responsibility, boundary, interface (the contract other code
> relies on), data, GDD trace. **[PROTO]** systems carry enough detail to
> implement tomorrow; **[LATER]** systems are spec'd to boundary + seam level.

### 6.1 S1 — Topology Graph **[PROTO]**

- **Responsibility.** The authoritative network model: terminal nodes
  (Residential, Content host — PROTO roster; Gaming/Financial/DC/CDN [LATER])
  and junction nodes (routers: merge/split/repeater), and pipes (tier/capacity/
  span/lane-weights/legacy). Owns adjacency, span budget, parallel-pipe
  bundles (groups derived from adjacency — all pipes between a node pair)
  `[GDD § M1, M3]`.
- **Boundary.** Owns graph structure + edit application. Does not route
  (Packet_Flow), render (View), or read input (Command_Bus).
- **Interface.**
  - `topology_apply_edit(t: ^Topology, cmd: Edit_Command) -> (Edit_Result, Edit_Error)`
    — validate-all-then-apply for batches (E23); rejections are typed enums
    (`self_loop`, `span_exceeds_tier`, `over_budget`, `terminal_demolish`,
    `era_locked`), never strings (§7.1).
  - `neighbors(t, node) -> []Node_Id` (slice into adjacency arrays),
    `pipe_between(t, a, b) -> Maybe(Pipe_Id)`, `topology_snapshot(t) -> Topology_Snapshot`.
- **Data (SOA).**
  ```odin
  Node_Kind :: enum u8 { Terminal, Junction }
  Topology :: struct {
      // nodes (parallel arrays; index = slot)
      node_kind:  [dynamic]Node_Kind,
      node_type:  [dynamic]u16,        // index into node_types catalog
      node_pos:   [dynamic][2]i32,     // integer grid — ADR-10 carried
      node_gen:   [dynamic]u32,        // generation for monotonic ids (E11)
      // pipes
      pipe_a, pipe_b:   [dynamic]u32,
      pipe_tier:        [dynamic]u16,  // index into pipe_tiers catalog
      pipe_weights:     [dynamic][3]i32, // lane WFQ weights (integer — ODN-3)
      pipe_lb_mode:     [dynamic]Lb_Mode,  // [PROTO] round-robin/weighted per-pipe LB; [FULL] deleted — parallel pipes BUNDLE (derived from adjacency at table-build)
      pipe_legacy:      [dynamic]bool,
      adjacency:        [dynamic][dynamic]u32, // node slot -> incident pipe slots
  }
  ```
  Positions are `[2]i32` grid coords (integer → determinism). Ids are
  `{slot, gen}` — monotonic, never recycled (E11). Adjacency is array-based;
  **no maps are iterated anywhere in core** (ODN-10).
- **Topology canon from the art pivot (now load-bearing data, not just pixels):**
  **terminals connect via routers only — never terminal-to-terminal** (look-book
  D11 / amendment A6). The Command_Bus rejects terminal↔terminal draws
  (`Edit_Error.terminal_to_terminal`); terminals are leaves, routers are the
  interconnect. This was locked *after* GL5.2 was written — the Odin build
  inherits it as a first-class edit rule.
- **Span (modernization constraint).** Tier max-span enforced at edit;
  junctions are repeaters (routing through one resets the span budget)
  `[GDD § M3]`; clean-span degradation is the `wear` curve ([LATER] depth;
  PROTO enforces the hard max). **Parallel pipes bundle** into one
  pooled-capacity link (cap = sum of members) `[GDD § M1, M3]` — there is
  **no LB mode in the full game**. `[PROTO: PR #17 still uses round-robin /
  capacity-weighted LB per pipe; the full-game port replaces it with bundles
  + per-hop forwarding — routing ruling, lavish 2026-08-10.]`
- **Deterministic map growth + spawn validity.** New nodes appear over time
  (Mini Motorways model); spawn timing + placement come from `demand_plan`
  (ODN-7) drawing the seeded rng, applied by Topology — reproducible from the
  seed. Growth proceeds **outward from the router mesh** (routers co-spawn
  with/alongside terminals — the lesson the Godot prototype paid for: its
  director once spawned a house 20+ tiles from every router, unwinnable
  demand). **Spawn-validity contract (E31 — pinned test, tied to the
  no-soft-lock rule):** every spawned terminal must be connectable — within
  some available tier's span of an existing or co-spawned router — else the
  director re-places it by rejection sampling from the *same* rng stream
  (deterministic). Placement also enforces a minimum node separation and
  never overlaps (snap disambiguation, E4, depends on it). Whether routers are
  additionally *player-placeable* (a Command with cost) is a [LATER] tool
  decision; PROTO's routers are director-spawned.
- **Distance metric (pinned).** All span/cost/snap math uses **integer
  Euclidean²** — `dx*dx + dy*dy <= span*span`; no `sqrt` anywhere in core
  (exact, cheap, identical on every target). One metric serves span
  validation, draw cost (length × tier), and the snap radius (E4).
- **Junction demolish (E27).** Demolishing a junction is an **atomic batch**:
  its incident pipes are demolished first (in edge-id order — deterministic),
  each per E1 (reroute-or-drop), then the vertex is removed — one `apply_all`
  transaction, so replay cannot diverge on ordering.

### 6.2 S2 — Packet-Flow Simulation **[PROTO]** (QoS + SLA inside)

- **Responsibility.** The deterministic tick loop: spawn per the demand plan,
  **forward along the graph** (per-hop at each junction; ECMP across equal-cost
  next hops), allocate bandwidth across lanes, serialize at nodes,
  drop/buffer on contention, terminate at sinks, accumulate per-class SLA
  (latency ms / loss) `[GDD § M2]`.
  `[PROTO (PR #17): routes are a one-shot BFS cached on the packet at spawn,
  with parallel-pipe LB (round-robin / greedy-capacity). FULL: per-hop
  forwarding + ECMP + bundles — routing ruling, lavish 2026-08-10; see the
  modeling note below.]`
- **Boundary.** Owns packet slots + routing + bandwidth accounting + SLA
  accumulators. Reads the Topology snapshot; does not own the graph, crises
  (downstream), or rendering. **QoS procs and SLA accumulators live here**
  (ODN-3, §14.2) — invoked by `flow_step`, never peers.
- **Interface.**
  - `flow_step(state: ^Run_State, tick: u64, demand: Demand_Plan)` — the only
    entry; internally: route → `qos_allocate` → `qos_serialize` → advance →
    contend/drop → `sla_accumulate`.
  - Events appended: `Packet_Arrived{class}`, `Packet_Dropped{class, reason}`,
    `Sla_Threshold_Crossed{class, metric, direction}` (ODN-14).
- **Data.**
  ```odin
  Packet :: struct {
      src, dst:          Node_Id,
      route:             Route_Handle,  // [PROTO] precomputed BFS route cached at spawn; [FULL] per-hop forwarding — no cached route, next hop decided at each junction
      edge_idx:          u16,
      class_id:          u16,           // index into packet_types catalog
      lane:              Lane,
      progress_units:    u32,           // bandwidth-units along current edge
      spawn_tick:        u64,
      accrued_latency_ms:u32,           // integer ms — sub-tick SLA resolution (m16)
  }
  ```
  SLA accumulators per class (§5.2 ODN-3 struct). Zero-demand tick = neutral
  (E24). **CDN reservoir nodes (Era 5) are a buffering mode of this system**
  (store-and-smooth, data-flagged on the node type — no new system;
  `[REVIEW m15]` carried).
- **Modeling note (carried + routing ruling, lavish 2026-08-10).** Packets
  progress by **bandwidth units per tick** — a discrete flow/queueing sim,
  integer-cheap, deterministic.
  **[PROTO] routing** (PR #17): a one-shot **BFS by hop count**
  (`compute_route`, insertion-order tie-break — no RNG in routing), cached on
  the packet at spawn and held until a pipe is demolished under it; parallel
  pipes between a node pair are served by a per-pipe pick (`pick_pipe`: basic
  junction round-robins, smart junction picks highest capacity with RR among
  ties). This is the playability-gate model, not the target.
  **[FULL] routing** (the locked model): **per-hop forwarding + ECMP +
  bundles.** Each junction holds a **forwarding table** `(junction, dst) → next
  hop`, computed by a deterministic **Dijkstra/SPF over integer pipe costs**
  (the capacity-cost model, user ruling 2026-08-13 — see below) and
  **rebuilt only on a topology-changing Command, synchronously inside the
  tick** — never per-packet, never async. Among **N equal-cost next hops** the
  pick is a **pure hash** `splitmix64(src, dst, class, pkt_id) mod N` (reuses
  ODN-9's splitmix64 as a *finalizer*, NOT a draw from the sim rng — same packet
  always takes the same path, with flow affinity). **Parallel pipes between a
  node pair bundle into one pooled-capacity link** (cap = sum of members);
  routing sees one fat edge per pair, so there is **no LB** in the full game.
  Determinism is preserved — the 4-rule spine is pinned in ODN-9/ODN-10.
- **The capacity-cost model (user ruling 2026-08-13, the canon amendment).**
  Path cost = STATIC pipe capacity — each pipe's routing cost is its tier's
  integer `cost` from `data/pipe_tiers.json` (the data-driven ladder
  20/10/5 for narrow/standard/wide), NEVER dynamic utilization: congestion
  avoidance is the player's job (QoS + engineering), and the static ladder
  keeps the table a pure function of the Topology (spine rule 1 holds by
  construction). **Equal cost is an END-TO-END sum property** — the
  equal-cost next-hop condition is `dist[v] + cost(pipe) == dist[u]` (the
  textbook SPF condition over cost units), so the ECMP set is the neighbors
  whose *total* path cost ties, even across different tiers (e.g.
  standard(10)+wide(5) == wide(5)+standard(10) = 15 both ways → ECMP set of
  2). When costs differ the fatter (lower-cost) path wins as a UNIQUE next
  hop — the player rule is one line: **"packets take the fattest route;
  equal cost splits by hash."** A mixed-tier bundle prices at its fattest
  member (min member cost — the same member the bundle renders at its
  highest tier), so an upgrade to a bundle visibly attracts flow. Ladder
  values are balance data (ODN-5), not code — retuning is a data change.
  (Player-assist features — draw-time flow preview, post-draw route glow,
  forecast flow-shift prediction — are follow-up jobs B/C, NOT this ruling.)
- **Per-link buffering is bounded.** Each pipe-lane output queue has a catalog
  bound (`balance.json: lane_queue_packets`); when full, the E9 drop precedence
  engages **at that link**. The global packet pool (ODN-8) remains the E22
  backstop — one saturated link can never absorb the whole pool and starve the
  map.
- **Unroutable demand (E28).** If a source has demand but no path to any sink
  (disconnected graph), the packet is **not spawned**; the undelivered demand
  accrues to the class's SLA as undelivered — it feeds congestion → warnings →
  crises exactly like a loss, but no phantom packets park at sources.
- **Route migration (E29).** Under per-hop forwarding, route migration is
  **automatic**: there are no stale spawn-time routes to migrate — a topology
  change propagates via a forwarding-table rebuild at the next sync, and
  in-flight packets **re-forward at the next junction** they reach (never
  mid-edge). `[PROTO (PR #17): routes are cached at spawn; only a demolished
  edge forces a re-BFS (E1) — the gap the per-hop model closes.]` E1's
  demolish rule is the (now-only) exception that forces an immediate
  reroute-or-drop at the current node.

### 6.3 S3 — QoS class queue model **[PROTO]** (pure procs inside S2)

- **Responsibility.** `[GDD § M2]` link-level QoS: per-pipe 3-class-queue bandwidth
  partition (WFQ weights), per-node serialization order, work-conserving
  gap-fill + WRR floor, contention drop precedence.
- **Boundary.** Stateless pure procs over pipe/node data; weights/policies are
  Topology-owned data; called only by `flow_step`. **Not a system** (§14.2).
- **Interface.**
  ```odin
  qos_allocate :: proc(capacity: u32, w: [3]i32) -> (caps: [3]u32)
  // weight-only partition (demand is NOT an input — gap-fill is a
  // serialization-time concern); all-zero weights → catalog default preset (E5);
  // largest-remainder distribution, Express→Standard→Best tie order (E8).
  // Weight domain: 0 ≤ w_i ≤ MAX_WEIGHT, bounded at the Command_Bus
  // (Edit_Error.Invalid_Weights); sums/remainders computed in i64.

  qos_serialize :: proc(ready: [3][]Packet_Slot) -> (order: []Packet_Slot)
  // Express → Standard → Best-Effort, work-conserving gap-fill, with a
  // weighted-round-robin floor: ≥1 slot per non-empty lane per window (E7).
  ```
- **The never-drop floor lives in `flow_step`, not the allocator (E6).**
  `qos_allocate` is pure weight-only — it cannot know which lane carries a
  never-drop class; `flow_step` knows the class→lane bindings, so it floors
  that lane at a **quantum of 1 bandwidth-unit** after allocation. If floors
  exceed pipe capacity (tiny pipes), floors are satisfied in lane order
  (Express → Standard → Best) and capacity exhaustion is the defined
  truncation. The Command_Bus still rejects the edit that would zero such a
  lane (the primary guard). Pinned as a min-capacity test.
- **Depth dial (audience bridge, `[FORGE weak #3]`).** PROTO: a single
  "priority emphasis" dial per pipe mapping to integer weight presets from
  `balance.json`. Full game: raw `[3]i32` weights. Same core, two control
  surfaces. Dedicated-pipe-per-class = 100% one lane (the premium reservation).
- **Orthogonal to routing (routing ruling, lavish 2026-08-10).** QoS is
  **unchanged** by the per-hop-forwarding + ECMP + bundle ruling: QoS is
  bandwidth-on-a-pipe (lane scheduling inside a link); routing is next-hop
  selection across links. The two axes never share state — a bundled link
  carries the pooled capacity with the same 3 lanes; ECMP decides *which*
  equal-cost link, the class-queue weights decide *what rides first* on it. Stated
  explicitly so the two are never conflated.

### 6.4 S4 — Crisis Engine **[PROTO: Surge only]**

- **Responsibility.** `[GDD § M5]`: congestion metrics from Topology + Flow →
  warning signs (node 🟡/🔴, pipe congestion, forecast, wear) → archetypes.
  PROTO ships **Surge** (forecast demand spike, cascade saturation if
  unprepared); Saturation/SPOF/Degradation/Severance are [LATER] content +
  evaluation procs on the same frame.
- **Boundary.** **Downstream of flow** — reads Topology + Flow state, emits
  `Warning_Sign` + `Crisis_Event`. Never owns the demand timeline (that's the
  Director, upstream — ODN-7); a crisis is a consequence, never its own cause
  (`[REVIEW M1]` rule carried — and here it is *structural*: the ODN-7
  signature hands the Director a read-only view, not `^Run_State`). Does not resolve crises (the player does).
- **Interface.** `crisis_evaluate(state: ^Run_State, tick: u64)`; events
  `Warning_Raised{sign}`, `Crisis_Triggered{archetype, root_cause}`,
  `Crisis_Resolved{archetype}`.
- **Fairness enforcement.** `root_cause` is a structured ref to the specific
  topology flaw + a `preventive_redesign` description; test-pinned (§11.3):
  no crisis without a resolvable root cause; every root cause has a preventing
  edit; no crisis on a healthy within-capacity topology. Dedup by root-cause **across the whole
  activation** (E13): one *active* crisis per root-cause, period — a persistent
  flaw does not re-fire `Crisis_Triggered` every tick; re-trigger only after
  `Crisis_Resolved` (an optional cooldown in `crises.json` governs re-fire if
  design wants it). Era-advance interplay rules (E14/E15) ready for the [LATER]
  Era layer.

### 6.5 S5 — Network Health **[PROTO]**

- **Responsibility.** The aggregate loss condition `[GDD § Win/Loss]`: meter
  drains while any active class's SLA is breached (rate ∝ severity; **drain =
  max(severity), not sum, plus a per-tick cap** — E16, "never instant"), recharges
  when healthy; breach starts a grace countdown; expiry hits the meter; empty
  meter → **Error 404**, run over.
- **Boundary.** Reads SLA state from Flow (via the step's results); owns grace
  windows + meter. **Terminal suppression is sim-side (E17):** `health_update`
  never emits `Grace_Expired` once the meter is empty, and the terminal-event
  barrier (§4) skips the remaining systems in the tick after `Run_Lost` — one
  terminal event per run, by construction. **Hysteresis (E30):** SLA threshold
  crossings use enter/exit thresholds per class (catalog values) so an
  oscillating class doesn't emit crossings every tick; a re-breach during an
  active grace window is a no-op (one countdown per episode).
- **Interface.** `health_update(state: ^Run_State, tick: u64)`; events
  `Grace_Started{class}`, `Grace_Expired{class}`, `Meter_Changed{pct}`,
  `Run_Lost{}`.
- **No-soft-lock guarantee.** Recoverable until empty — test contract carried.

### 6.6 S6 — Era State Machine **[LATER]**

- **Spec (boundary + seam level).** The 6-era in-run arc `[GDD § M4]`: advance
  trigger (sustain SLA ≥ 95% across active classes for the milestone window
  AND modernize all in-service legacy pipes AND no active crisis — E15),
  unlock sets, legacy/degradation lifecycle. Data-driven from `eras.json`.
  Step ordering already reserved in `core.step` (§4); the advance-vs-crisis
  contracts (E14/E15) are decided here so the layer drops in without
  re-litigation. **Metaphor boundary (Era 6)** mechanics — VPN overlay = a pipe
  attribute; SDN = a `Junction_Policy` variant; AI traffic = an adaptive
  `Demand_Profile` — are data + small procs on existing seams; no new core
  system (GL5.2 §13.2 carried). **PROTO stubs it with a no-op `era_step`.**

### 6.7 S7 — Economy / Score **[LATER]**

- **Spec.** Full game: score (survival + era + uptime % + crises survived) and
  the draw/upgrade budget (cost = length × tier; tier-delta upgrades)
  `[FORGE MVP scope]`. The Command_Bus already consults `can_afford` — PROTO
  binds a constant budget from `balance.json` so the fun-slice can't
  over-draw; the real economy replaces the constant behind the same two procs
  (`can_afford`, `spend`) + `score() -> u64` / `score_breakdown()`.
  **PROTO budget semantics (pinned):** a fixed depleting pool from
  `balance.json`; demolish **refunds** cost (redesign is the game — GDD Player
  Assistance), so exhaustion blocks only *new* spend and a reroute-out always
  exists (no soft-block); exhaustion surfaces as typed rejection copy only.

### 6.8 S8 — Meta / Leaderboard **[LATER]** (no-op stub in PROTO)

- **Client seam (PROTO-present, [LATER] to implement for real).**
  ```odin
  Leaderboard_Service :: struct {
      submit:      proc(entry: Score_Entry),
      fetch_board: proc(board_id: Board_Id),
      poll:        proc() -> Maybe(Submission_Result), // drained by the app loop
  }
  ```
  PROTO binds `noop_leaderboard`. Production binds an HTTP impl with an
  offline outbox (queue + flush on reconnect — E19) and non-blocking rejection
  toasts (E20). Submission payload includes `modifiers` (E25/m14).
- **Backend (production scope).** I/O-bound CRUD + validation. **The pivot
  changes the validation economics** (ODN-6): the server can compile *this*
  `package core` and re-sim submissions bit-for-bit. Lean-vs-full validation
  becomes a pure ops-cost decision at production time (`[GDD OQ-7]` evolved).

---

## 7. Cross-cutting Concerns

> Mandatory for every implementation — the constitution that keeps agents
> consistent. GL5.2 §7 carried and re-idiomed.

### 7.1 Error handling

**Strategy:** Odin-native multiple returns — `(T, Error)` with typed error
enums — plus the event buffer for systemic/async surfacing. **Never
catch-and-ignore** (carried; easier to keep in Odin: there are no exceptions
to swallow, and an ignored `ok: bool` is visible at the call site).

```odin
Edit_Error :: enum u8 { None, Self_Loop, Span_Exceeds_Tier, Over_Budget,
                        Terminal_Demolish, Terminal_To_Terminal, Era_Locked }
Edit_Result :: struct { applied: bool, pipe: Pipe_Id } // meaningful on applied=true

topology_apply_edit :: proc(t: ^Topology, cmd: Edit_Command) -> (Edit_Result, Edit_Error) {
    if cmd.a == cmd.b            { return {}, .Self_Loop }
    if is_terminal_pair(t, cmd.a, cmd.b) { return {}, .Terminal_To_Terminal } // art-canon rule
    if !within_span(t, cmd)      { return {}, .Span_Exceeds_Tier }
    if !can_afford(cmd)          { return {}, .Over_Budget }
    return mutate(t, cmd), .None
}
```

- **Critical errors** (save corruption, invariant violation, catalog load
  failure) → `ERROR` log + the sim pauses; never continue on corrupt state.
- **Recoverable errors** (invalid draw, over budget) → typed error → the
  Command_Bus turns it into a UI hint (satirical-brand rejection copy) — no
  interruption.
- No bare `_ = fallible_call(...)` in committed code — a CI lint greps for
  dropped second returns in `core/` (§16.3).

### 7.2 Logging

Levels `ERROR/WARN/INFO/DEBUG/TRACE`; structured one-line
(`[LVL] tick=N system=X msg`); console in dev, rolling file always (crash
forensics). Core logging is **sink-injected**: the core receives a
`Logger_Proc` at init (PROTO: stderr; harness: memory buffer that becomes part
of the golden report). The core never touches `core:fmt` stdout directly —
keeps the import rule (§4) intact and makes CI logs diffable.

### 7.3 Configuration

Four tiers (carried): **game constants** + **balance values** in
`data//*.json` (ODN-5 single source) · **player settings** (audio,
accessibility, unlocked-fps toggle) in a small binary/JSON user file ·
**platform overrides** as compile-time `-define:` flags where needed. Never
hardcoded balance literals in code — the grep gate for this is §16.3.

### 7.4 Event system

ODN-14 is the whole story: a `[dynamic]Event` buffer on `Run_State` (every
event tick-tagged), tagged-union payload, drained by the app once per frame
after the step loop, in append order. Sync by construction.
Debug replay can diff event streams — a logic-level golden cheaper than pixels.

### 7.5 Save / run system

ODN-11. `save_write(path, run) -> Save_Error`, `save_load(path) -> (Run_Descriptor, Save_Error)`.
Versioned header (`magic, format_version, seed, era_progress, modifiers[],
catalog_hash, logic_hz` — ODN-11), then length-prefixed little-endian command
records `{apply_tick: u64, tag: u8, payload: [...]}` (post-validation,
post-snap — ODN-11). `format_version` bumps are a deliberate, reviewed event —
the replay contract depends on it.

### 7.6 Debug / dev tools

Compile-gated with `-define:PP_DEBUG=true` (real conditional compilation —
GL5.2 had to settle for a runtime `OS.is_debug_build()` check whose code still
shipped (`[REVIEW m11]`); Odin removes the trap class): debug overlay (tick,
fps, active packets, SLA per class), cheat commands (set era [LATER], force
crisis archetype, inject surge, give budget), visualization toggles (lane
allocation bars, congestion heatmap, slow-mo), and **replay-from-log** (feed a
seed + action log — the same path the harness uses, §10). Live balance
sliders edit the in-memory catalog copy for tuning, with a "write back to
JSON" button — the no-editor iteration loop. *(Realized in story 5.7: debug
overlay (`D` key) + `--stats-out` deterministic per-tick stats stream,
replay-pinned.)*

---

## 8. Data Architecture

### 8.1 Catalogs (`data//*.json` — single source, ODN-5)

| Catalog | Key fields | Source values |
|---|---|---|
| `packet_types.json` | `id, color_rgba, shape, icon, latency_tol_ms, loss_tol, bandwidth_demand, default_lane, era_introduced, sla_fail_effect` | `[GDD § M2 roster]` (9 types; PROTO: email + streaming) |
| `pipe_tiers.json` | `id, capacity, clean_span, max_span, era_introduced, cost_per_tile` | `[GDD § M1]` (Narrow/Standard/Wide/Backbone) |
| `node_types.json` | `id, kind(terminal/junction), throughput, lb_mode_capable, era_introduced, sprite_id` (`lb_mode_capable` is `[PROTO]`-only — full-game junctions forward, no LB mode) | `[GDD § M3]` |
| `eras.json` **[LATER]** | `id, name, packet_types[], node_types[], pipe_tiers[], demand_signature, milestone_window_ticks, sla_threshold, metaphor_mode` | `[GDD § M4]` (6 eras) |
| `crises.json` | `archetype, root_cause_pattern, warning_curve, lead_time_ticks, failure_effect` | `[GDD § M5]` (5; PROTO: Surge) |
| `balance.json` | `health_drain_rates, grace_windows, snap_radius, score_weights, logic_hz, packet_pool_sizes, default_lane_weights, emphasis_presets, placement_min_sep_router, placement_min_sep_terminal, lane_auto_reserve_ladder` | `[GDD § Numerical Design]` |
| `palette.json` | the look-book hexes (canvas, grid, ink, buildings, routers, pipes, packets, state triad) | `[LOOK §2]` — rendering reads this too, so art tuning is data |

**Rules:** integer-only for sim-relevant values (ODN-10); cosmetic values
(colors, pulse rates) labeled and never read by core; absent = omitted field
with an explicit default at load (no sentinel values); fail-fast validation at
load (ODN-5); release builds embed via `#load()`.

### 8.2 Core data model (relationships)

```
Run_State ──owns──▶ Topology (SOA node/pipe arrays + adjacency)
        │            └── Node {slot,gen} ──via──▶ Pipe {slots, tier, weights, legacy}  (parallel pipes bundle at table-build — [FULL])
        ├──owns──▶ Flow_State ──has──▶ Packet pool (#soa + free list)
        │            │                  Route slab (routes as edge-id spans) — [PROTO] only; [FULL] per-hop forwarding has no cached route
        │            ├──has──▶ Sla_Accumulator[]  (per class)
        │            └──uses──▶ qos_allocate / qos_serialize (pure procs)
        ├──owns──▶ Crisis_State (warnings[], active[], forecast[])
        ├──owns──▶ Health_State (meter, grace windows)
        ├──owns──▶ Era_State / Economy_State            [LATER]
        ├──holds──▶ rng: Rng (seeded; ODN-9)
        ├──holds──▶ config: Run_Config (seed, modifiers, demand_plan, leaderboard)
        ├──holds──▶ events: [dynamic]Event (per-tick buffer; ODN-14)
        └──refs───▶ Catalogs (loaded once, read-only)

App ──owns──▶ Run_State (created per run; ODN-13)
   ──owns──▶ Cosmetic_Rng (ODN-15), settings, window/render state
   ──uses──▶ Save_System [LATER], Leaderboard_Service (ODN-6)
```

No `Node`, no `RefCounted`, no `Resource` — plain data end to end.

---

## 9. Presentation (raylib) **[PROTO]**

### 9.1 View / Render Layer — the light-canvas canon, in raylib idioms

The locked visual canon is look-book v1 `[LOOK]`: **light Mini-Motorways
daytime canvas** (amendment A1), **literal buildings** for the 6 terminal types
(A2), **round capacity-scaled router pucks** (A3), **smooth bezier pipes with
glowing cores** on fiber/backbone (A4), **procedural land/ocean/parks map** (A5),
**terminals-via-routers topology** (A6 — also a data rule, §6.1), blue/grey
packet personalities + the 9-type colorblind-safe shape system (A7). Exact
hexes live in `palette.json` (§8.1); the reference renders in
`_bmad-output/planning-artifacts/art-renders/` are the north star — and the
golden harness (§10) compares against frames rendered from this layer.

**Render pass per frame (all immediate-mode raylib):**

```
1. Camera-fit: compute world→screen transform so the 1280×720 design grid
   letterboxes/expands like GL5.2's aspect=expand — wider/taller windows
   reveal more map (a routing-game advantage, carried ruling).
2. Map: procedural landmasses (seeded value-noise → coastline polylines),
   ocean fill, park blobs — generated once per run at run creation by the app
   from a **dedicated derived stream** (`splitmix64(run_seed ^ MAP_TAG)` —
   never `state.rng`, which would perturb the sim; never the cosmetic stream,
   ODN-15). **Geography is cosmetic-only:** it never constrains topology, and
   node placement ignores land/water (the canon is an abstract map; keeping
   map-gen out of the core keeps the re-sim story clean). Cached in a
   RenderTexture (static layer, redrawn only on pan/zoom/**resize**).
3. Pipes: per pipe, a quadratic bezier between endpoints (deterministic
   control point from endpoint geometry), drawn as layered thick lines:
   tier color outer (width by tier) + lighter inner core on fiber/backbone.
   Rounded caps. `DrawLineBezier`-family calls; batching via one pass.
4. Nodes: buildings as small sprite/polygon compositions per type
   (placeholder shapes in PROTO per the no-purchased-assets rule; the
   Blender→PNG sprite pipeline slots in later unchanged); routers as disc +
   LED ring + core (tier-scaled). Health state = ring color (state triad) +
   pulse rate + icon — never color alone `[GDD § Accessibility]`.
5. Packets: iterate snapshot arrays; per packet a shape draw call
   (circle/triangle/diamond/… per type, size = bandwidth) at the lerped
   position between snapshots[t-1] and snapshots[t]. Within a pipe, dot
   color *proportion* reflects class-queue allocation; at nodes, exit order shows
   serialization (the QoS-made-visible canon, `[GDD § M2]`).
6. UI/HUD (screen space): Network Health meter, demand forecast, alert
   toasts (satirical brand copy), contextual popover on selection.
```

**PROTO placeholder discipline carries** (`project-context.md`): colored
rects + emoji + system shapes until the playtest gate; the art pipeline
(Blender → orthographic PNG sprites → `LoadTexture`) is a content swap, not a
render-layer change.

### 9.2 UI layer (minimal immediate-mode widgets)

No retained UI framework exists here — by design. A tiny immediate-mode
widget set (~button, slider, popover, toast; one file) drawn with raylib
primitives, styled from `palette.json`. Progressive disclosure (default view
clean; select → popover), filter/focus modes, alerts-as-navigation, minimap —
all carried from `[GDD § UI & Navigation]`. These are view-layer concerns and
none of them touch the core.

### 9.3 Input layer

ODN-12. Mouse first (PROTO): `GetMousePosition/IsMouseButtonDown` → drag-draw
with generous snap radius; `GetMouseWheelMove` → zoom; edge-scroll/drag → pan.
Touch (raylib gestures) and gamepad (`GetGamepadAxisMovement` + buttons) map
to the same intents — [LATER] for PROTO, same-game parity by construction
`[FORGE #6]`. Pause-anywhere: crises tick only unpaused (fairness +
accessibility, carried). Landscape-only framing is a camera-fit decision
(§9.1), not an engine lock.

### 9.4 Save / run system

ODN-11 / §7.5. [LATER] player-facing; the log mechanism is PROTO (harness).

### 9.5 App / mode state

ODN-13: `Boot → Menu → Run ↔ Paused → Game_Over`. The `Run` context composes
core + view + audio per run and is destroyed/rebuilt per run (a fresh arena —
reset is structural).

### 9.6 Audio layer

ODN-15. [LATER] for PROTO beyond a sting or two; the reactive wiring consumes
the event buffer (ODN-14) — `Crisis_Triggered` → alert sting,
`Packet_Arrived` → per-class click variants, etc.

---

## 10. The Golden-Image Test Harness **[PROTO — built first]** (ODN-17)

> **Why this is a core system, not a test utility.** In Godot the agent had an
> editor, a scene tree, and MCP inspection to see its work. In Odin there is
> nothing between the agent and the machine — so the harness is how the agent
> *sees*. It is the verification foundation for the entire pivot: it proves the
> Odin core reproduces the Godot prototype's proven behavior, it catches
> determinism regressions before they compound, and it gives the LLM a
> readable diff when pixels move. Pattern per the ThePrimeagen reference
> (scripted test frames + render-to-texture + deterministic replays + golden
> compare + agent-readable diffs), upgraded for raylib 6.0 (§10.4).

### 10.1 What it is

A second executable (`harness/`) that links the **same `package core`**
and the **same render package** as the game, but:

- takes its input from **scripted demos** (files) instead of a live mouse,
- renders to a **RenderTexture** instead of (or in addition to) the screen,
- compares every captured frame against a **golden** on disk,
- emits **agent-readable diffs** (PNG + JSON + event-log) on mismatch,
- and can **re-bless** goldens on command when a change is intentional.

### 10.2 Two verification tiers

| Tier | What it compares | Needs GPU? | Where it runs | Catches |
|---|---|---|---|---|
| **T1 — State-hash goldens** | Per-tick **FNV-1a-64** hash of the snapshot's **canonical serialized form** (the ODN-11 writer: field-wise, lengths-not-capacities, no padding — **including rng state + the event stream**); never raw in-memory bytes (pointers/padding/arena slack) | No | `odin test`-style native run, every CI job, every platform/arch | Logic/determinism regressions (the spine, ODN-10) |
| **T2 — Pixel goldens** | Rendered frames (keyed at scripted times) vs reference PNGs | **No** — software renderer (§10.4) | Harness in CI (Linux/Windows/macOS × amd64/arm64) | Visual regressions — moved dots, wrong colors, broken canon |

T1 is the workhorse: it runs everywhere, is bit-exact by construction, and
fails fast with the tick number + system that diverged. T2 exists because the
fun-test is *visual* — "does the surge read like the surge" is a pixel
question.

### 10.3 Scripted demos + test frames (time + input)

A **demo** is a file (`demos//*.dem`) describing a scenario:

```
# surge_basics.dem — the fun-test slice, scripted
seed 42
map   demo_six_nodes          # a named map fixture (or `gen` for procedural)
at 0ms      intent Pan_Zoom{...}                    # optional setup
at 100ms    intent Begin_Draw{node: house_a}
at 600ms    intent Commit_Draw{node: router_1}      # "move over 500ms": the harness
                                                    # interpolates pointer positions
                                                    # across frames between intents
at 900ms    intent Set_Emphasis{pipe: p0, preset: express_heavy}
run 18000ms                                         # 18s of sim = 360 ticks
capture at 1000ms, 9000ms, 17000ms                  # T2 pixel goldens
expect event Crisis_Triggered{archetype: Surge} within 12000ms..16000ms   # T1 event assertion
expect hash stable                                   # T1: every tick hashed + compared
```

Key properties:

- **Test frames are (time, input) pairs.** The harness replays wall-clock-
  independent *frames*: at each simulated frame it injects the scripted
  intents (pointer motion is interpolated between waypoints — "move mouse to
  X over 500ms" is literal), steps the fixed accumulator deterministically
  (the harness drives a **virtual clock** — no real time is ever sampled in a
  test), and the game behaves exactly as if a human played.
- **Demos double as design documents.** `surge_basics.dem`, `qos_dial.dem`,
  `draw_and_upgrade.dem`, `severance_reroute.dem` [LATER]… the scenario list
  is the fun-test checklist made executable.
- **Time quantization (pinned).** The harness drives a virtual clock at
  **exactly 1/60 s per frame** (a rational — no float drift); demo times in ms
  convert by **floor-to-frame** (`frame = floor(ms × 60 / 1000)`), so intent
  and capture times land on unambiguous frames regardless of author
  arithmetic. Every golden manifest records `logic_hz` + `catalog_hash`
  (ODN-11): retuning either forces a deliberate re-bless, never a silent
  shift.
- **Demos lower to action logs.** A demo is a header (seed, map fixture,
  modifiers) + an intent script; the harness plays intents through the **real
  Input Layer → Command_Bus → core** path (the same path a mouse drives), and
  the resulting validated command stream *is* the action log (ODN-11) that
  T1/replay/validation consume. `harness --record` captures a live session as
  both the intent script and the compiled log. One determinism surface, not
  two.

### 10.4 Bit-exact pixels with no GPU (the raylib 6.0 upgrade)

GL-based screenshots differ across GPUs/drivers (AA, blending rounding) — the
classic reason pixel tests rot. Raylib 6.0 (verified 2026-08-08) ships:

- **`rlsw`** — a software renderer backend (CPU, no GPU), and
- **`PLATFORM_MEMORY`** — a platform backend rendering to a memory
  framebuffer, headless, frames exportable directly to images.

**Decision:** the harness builds its own raylib from source with the software
renderer + memory platform (a small pinned build script; the game binary keeps
the stock `vendor:raylib` GPU build). Consequences: golden pixels are produced
by **the same CPU code path on every machine** → zero-tolerance compare is
sound → CI needs no display, no Xvfb, no GPU runner. This is strictly stronger
than anything available to the Godot stack (whose headless mode has no
renderer at all — the `[FinLT]` capture trap).

**T2 mechanics:** render the frame → read the memory framebuffer →
`ExportImage` → compare against the golden PNG (zero-tolerance byte compare on
the decoded pixels). On mismatch, emit the **diff bundle** (§10.5).

**Render-path determinism rule:** harness-rendered code paths use basic IEEE
float ops only — no `@(fast_math)`, no fast-math build flags, no libm
transcendentals in rendered geometry (pulse phases derive from virtual time;
any `sin`-class need lives behind one pinned shared proc). Harness builds run
`PP_DEBUG=false`, and HUD/debug overlays, wall-clock text, or any
non-virtual-time content are excluded from captured frames (the harness
renders the world pass only). Anti-aliasing is fixed-off in the harness
config. With the rasterizer, the float discipline, and the virtual clock all
pinned, the zero-tolerance compare is sound.

### 10.5 Agent-readable diffs (the LLM's verification loop)

On any mismatch the harness writes a report directory:

```
goldens//_reports/surge_basics/2026-08-08T230000/
  expected_09000ms.png          # the golden
  actual_09000ms.png            # what we rendered
  diff_09000ms.png              # per-pixel delta, amplified, red overlay
  diff.json                     # {frame, mismatched_pixels, total_pixels,
                                #  bounding_box_of_change, first_divergent_tick (T1),
                                #  event_stream_delta: [...]}
  replay.dem                    # the exact demo to re-run locally
```

`diff.json` is the agent's entry point: it says *what* moved, *where* on
screen, *when* the sim first diverged, and how the event streams differ —
usually enough to diagnose without opening an image. The bounding box +
first-divergent-tick pair localizes "the streaming dots stopped taking the
left pipe after tick 212" class of bugs immediately.

### 10.6 Commands (the developer/agent loop)

```bash
odin run harness -- run            # replay all demos; T1+T2 compare; exit non-zero on mismatch
odin run harness -- run surge_basics   # one demo
odin run harness -- save           # re-bless ALL goldens (intentional change)
odin run harness -- save surge_basics  # re-bless one
odin run harness -- record         # play live (GPU window); save the session as a demo
odin test core                     # pure core unit tests (T1 logic contracts, §11)
```

`save` is deliberately explicit (never automatic) and its output diffs are
reviewed in the PR like any other change — a re-blessed golden with no code
change is a red flag.

### 10.7 Harness build & CI matrix (ODN-17 carried into §16)

- **Build matrix (CI):** Windows / macOS / Linux × amd64 / arm64 (native
  runners; Odin cross-compiles but native runners keep the harness honest on
  the real targets). Every job runs `odin test` (T1 contracts) and the
  harness (T1 hashes + T2 pixels via software renderer).
- **Goldens are platform-independent** because T2 is software-rendered; one
  set of goldens lives in the repo, valid on every runner.
- **Flake policy:** a T2 mismatch is never retried-and-forgotten; the diff
  bundle is uploaded as a CI artifact on failure.

### 10.8 What the harness proves during the pivot (acceptance use)

1. **Determinism:** T1 hash-stable across runs, platforms, and replays
   (the `(seed, action_log)` → identical snapshots contract).
2. **Parity evidence (not proof):** the scripted surge scenario on the Odin
   core produces the same qualitative outcome as the Godot prototype — the
   harness supplies the *evidence* (event streams + key frames); the *verdict*
   on fun is a human gate, side-by-side against the `prototype-fun-gate` tag checkout. CI-green never means
   fun-proven.
3. **Regression net:** every feature story after the harness lands runs
   `harness run` green before PR.

---

## 11. Implementation Patterns

### 11.1 Novel pattern: the deterministic core, native (GL5.2 §10.1.1 evolved)

Same data flow as §4; the Odin difference is that the pattern needs no
defensive scaffolding. `Sim_Driver` in the app owns the accumulator; `core.step`
is pure; the snapshot is a memcpy; the event buffer is the only output channel.

```odin
// app/ — Sim_Driver (the ONLY code that knows about real time)
Sim_Driver :: struct { accumulator: f64, tick: u64 }
sim_driver_update :: proc(d: ^Sim_Driver, state: ^Run_State, frame_dt: f64) {
    dt := min(frame_dt, 0.25)             // clamp stalls — carried rule
    d.accumulator += dt
    steps := 0
    for d.accumulator >= TICK_SECONDS && steps < MAX_STEPS_PER_FRAME {
        core.step(state, d.tick, {})      // player commands arrive via the edit
        d.tick += 1                       // fast-path (ODN-2), not the step loop
        d.accumulator -= TICK_SECONDS
        steps += 1
    }
    d.accumulator = min(d.accumulator, TICK_SECONDS) // bounded catch-up debt
    // steps == MAX_STEPS_PER_FRAME ⇒ slow-mo (E21) — never skip ticks.
    // View lerp alpha = clamp(d.accumulator / TICK_SECONDS, 0, 1) — never
    // extrapolates, even during slow-mo.
}

// The edit fast-path (ODN-2) — player edits apply THIS frame, even paused:
on_command :: proc(app: ^App, cmd: Command) {
    if res, err := core.topology_apply_edit(&app.run.state.topology, cmd);
       err == .None {
        log_append(&app.run.log, {apply_tick = app.driver.tick + 1, cmd})
        // replay applies all entries with apply_tick == N before stepping N →
        // live play and replay see identical state at every step boundary.
        view_resnapshot_topology(&app.view)   // the player sees it instantly
    } else {
        ui_hint(err) // typed rejection → satirical copy; no interruption
    }
}
```

### 11.2 Novel pattern: link-level QoS allocation + work-conserving serialization (evolved)

Design carried verbatim from GL5.2 §10.1.2 (the review-fixed version:
weight-only allocation; gap-fill at serialization; WRR floor; largest-remainder
integers). The Odin form is pure integer procs over `[3]i32` weights and SOA
lane queues (§6.3) — no `Allocation` heap objects, no `Vector3i`, and the
allocation result is a `[3]u32` on the stack.

### 11.3 Novel pattern: fair-crisis root-cause contract (carried as executable tests)

Every `Crisis_Event` carries `root_cause` (structured ref to the topology
flaw) + `preventive_redesign`. The `@(test)` suite pins: no crisis without a
root cause; every root cause has a preventing edit; no crisis fires on a
healthy within-capacity topology; warnings always precede failures by ≥ the
reaction window `[FORGE #3]`.

### 11.4 Novel pattern: action-log replay = save = validation = demo (evolved)

One mechanism, now four uses: save/resume, leaderboard validation, debug
replay, and **harness demos**. `(seed, modifiers, action_log)` through a fresh
`Run_State` reproduces the run bit-for-bit; the binary format makes "identical"
a `mem.compare` (ODN-11).

### 11.5 Standard patterns (Odin idioms, mandatory)

| Concern | Pattern | Example |
|---|---|---|
| Interfaces / seams | **Proc-pointer table structs** (ODN-6/7) or tagged unions — never inheritance | `Leaderboard_Service{submit: ...}` |
| Sum types / events | Tagged unions + exhaustive `switch` | `Event :: union { Packet_Arrived, Crisis_Triggered, ... }` |
| Error returns | `(T, Error)` multiple returns; typed enums | §7.1 |
| Entity creation | Fixed pools + free lists (core); factories read catalogs | ODN-8 |
| State machines | `enum` + `switch` (game modes, node health) | ODN-13 |
| Collections in core | Arrays/slices/`#soa` only; maps allowed for lookup, **never iterated** | ODN-10 |
| Memory | Arena discipline; explicit allocator args | ODN-18 |
| Data access | Catalogs loaded once, read-only | ODN-5 |
| Time | Integer ticks in core; the accumulator only in `Sim_Driver` | ODN-2 |
| Compile-time config | `-define:PP_DEBUG=true` for debug tools; `#load()` for embedded data | §7.6, ODN-5 |

### 11.6 Consistency rules (mandatory; CI-enforced where possible)

| Rule | Convention | Enforcement |
|---|---|---|
| Naming | Odin stdlib style: types/consts `Ada_Case`, procs/vars `snake_case`, files `snake_case.odin` | review + CI lint |
| Core purity | `core/` imports whitelisted `core:*` only; no `vendor:*`, no `core:os`, no `core:time` | **CI compile check** (§16.3) |
| No globals | everything reachable from `App`/`Run_State`, passed by pointer | review + grep for `var` at file scope |
| Integer sim | no float fields on core state; floats labeled cosmetic in catalogs | review + schema lint |
| No map iteration in core | arrays only | review + grep gate |
| RNG | sim draws from `state.rng` only; cosmetics from `app.cosmetic_rng` only | grep gate |
| Allocators | no `new`/`make` without explicit allocator in core | grep gate |
| Balance numbers | in `data//`, never literals | review + grep gate |
| Errors | no dropped error returns | CI lint |

### 11.7 Edge-case & degenerate-input contracts (carried from GL5.2 §10.5 — re-verified for Odin)

The GL5.2 review swarm produced 25 decided behaviors (E1–E25); they are
**design** contracts and carry unchanged. Re-verified against the Odin
mechanisms (what each contract *is* now):

| # | Contract (unchanged design) | Odin mechanism note |
|---|---|---|
| E1 | Demolish pipe w/ packets in transit → reroute or drop w/ `severance` reason. **Under bundles, demolishing one pipe of a bundle shrinks the pool (graceful), not a hard cut — only full-bundle-loss drops** (routing ruling, lavish 2026-08-10) | Atomic per edge inside `apply_all` |
| E2 | Terminal-node demolish forbidden | `Edit_Error.Terminal_Demolish` |
| E3 | Self-loop rejected | `Edit_Error.Self_Loop` |
| E4 | Snap radius inclusive (`<=`) | integer grid distance, one-line test |
| E5 | All-zero class-queue weights → catalog default preset | `qos_allocate` guard |
| E6 | Never-drop class lane floored; zeroing edit rejected | bus validation + quantum floor |
| E7 | No starvation under continuous Express | WRR floor in `qos_serialize` + test |
| E8 | Largest-remainder integer distribution | E→S→B tie order, pinned test |
| E9 | Drop precedence BE → Standard → Express | full drop precedence, every emptiness combo |
| E10 | Iteration/tie-break determinism | arrays-only + seeded rng + replay test (ODN-10) |
| E11 | Monotonic ids, never recycled | `{slot, gen}` ids (ODN-8) |
| E12 | Timers pure functions of (seed, log) | load→re-step→assert-match test |
| E13 | One crisis per root-cause per tick | dedup by cause ref |
| E14 | Era advance preserves active crises; no mid-crisis demand spawn | [LATER] layer contract, decided now |
| E15 | Era advance blocked while crisis active | [LATER] layer contract, decided now |
| E16 | Drain = max(severity) + per-tick cap | health proc constant |
| E17 | `run_lost` supersedes `grace_expired` | sim-side suppression + terminal-event barrier (§4, §6.5) |
| E18 | Demolish cascades to overlay/policy refs; re-draw doesn't inherit | [LATER] (Era-6 overlays) |
| E19 | Offline outbox for HTTP leaderboard | [LATER] seam behavior, decided now |
| E20 | Backend rejection → non-blocking toast, retryable vs terminal | [LATER] seam behavior, decided now |
| E21 | Slow-mo, never skip ticks | `MAX_STEPS_PER_FRAME` (§11.1) |
| E22 | Pool exhaustion → drop lowest-class queue first | sim-side integer check (ODN-8) |
| E23 | Batch validate-all-then-apply | `apply_all` atomicity + test |
| E24 | Zero-demand class = neutral SLA | accumulator guard |
| E25 | Run descriptor carries `modifiers` | in the save header from day one |
| **E26 (new)** | Terminal↔terminal draw rejected (art-canon topology rule) | `Edit_Error.Terminal_To_Terminal` (§6.1) |
| **E27 (new)** | Junction demolish = atomic batch: incident pipes first (edge-id order, each per E1), then the vertex | §6.1 |
| **E28 (new)** | Unroutable demand is not spawned; accrues as SLA-undelivered | §6.2 |
| **E29 (new)** | **Automatic under per-hop forwarding** — no stale spawn-time routes; topology changes propagate via table rebuild at next sync; in-flight packets re-forward at the next junction. E1 demolish is the (now-only) forced-reroute exception (routing ruling, lavish 2026-08-10) | §6.2 |
| **E30 (new)** | SLA hysteresis (enter/exit thresholds); re-breach during an active grace is a no-op | §6.5 |
| **E31 (new)** | Spawn validity: connectable-within-span + min separation, rejection-sampled from the same rng stream | §6.1 |
| **E32 (new)** | Fresh-run seeds from app-layer OS entropy, logged in the save header | ODN-9 |

---

## 12. Performance

| Concern | Strategy |
|---|---|
| Sim cost | Fixed 20 Hz tick; integer math; SOA hot loops (cache-friendly by layout); packets advance by bandwidth-units/tick. Late-era worst case (hundreds of packets, ~30 nodes) is comfortably inside budget for a native build — well under the GDScript cost of the prototype slice (desktop-observed). The phone budget itself is unmeasured (GDD OQ-3 + §18 OQ-1) — no mobile perf claim is made |
| Render cost | Immediate-mode batched draw calls; static map cached in a RenderTexture (redrawn on pan/zoom only); packet dots are shape calls from arrays (no per-entity objects); ~O(pipes + packets) draw calls per frame |
| Frame budget | Accumulator caps catch-up steps; slow-mo degradation (E21); render interpolates → 60 fps motion from 20 Hz sim |
| Memory | Arenas (ODN-18); fixed pools; zero per-frame heap churn; catalogs loaded once |
| Load time | Native binary + embedded catalogs (`#load`) → cold start is OS-bound, well under the 3 s phone target |
| Mobile thermal | Unlocked-fps toggle off by default (carried); sim cost bounded |
| CI | `odin test` + harness on every job (§10.7); the pure core tests are milliseconds-scale |

---

## 13. Prototype Scope — Buildable-Core-First (the Heist 2 target)

The user wants to **see the early Odin prototype soon** to compare against the
Godot one. This section is the prototype's build manifest — everything else in
this doc exists so these layers land without re-architecture.

### 13.1 The prototype builds (in this order)

| Step | Deliverable | Systems | Exit signal |
|---|---|---|---|
| 1 | **Harness skeleton** | `harness/` + `core.step` no-op + one trivial demo + one golden | `harness run` green in CI (all platforms) |
| 2 | **Topology + draw** | S1, Command_Bus, input (mouse), view pass 1–4 | Demo: draw pipes between buildings via routers; pixel golden of a small map |
| 3 | **Packet flow** | S2 (+S3 procs), demand plan (scripted director), view pass 5 | Demo: dots flow source→sink; T1 hash golden |
| 4 | **QoS dial** | S3 emphasis presets, popover widget (view pass 6) | Demo: `qos_dial.dem` — lane proportions visibly change |
| 5 | **Surge + health + win/lose** | S4 (Surge), S5, forecast UI, game-over flow | `surge_basics.dem` — the fun-test slice, golden'd end to end |
| 6 | **Juice pass** | map polish, pulse/packet feel, 1–2 stings | Compare feel against the Godot prototype (tag checkout) side by side |

After step 5 the prototype is **the fun-test loop** (Topology, PacketFlow, QoS,
Crisis, NetworkHealth) — comparable to the Godot prototype, which is the
briefing's priority. Step 6 is deliberately small: just-enough juice
`[BRIEF risk #5]`, not polish.

### 13.2 Explicitly [LATER] (spec'd above; not in the prototype)

- **S6 Era State Machine** (§6.6) — the step-order slot and contracts (E14/E15)
  are reserved; the layer drops in as data + procs.
- **S7 Economy/Score** (§6.7) — PROTO uses a constant budget; the seam exists.
- **S8 Leaderboard** (§6.8) — no-op stub bound; the portable core makes the
  backend validation story stronger whenever it lands (§14.1).
- Touch + controller input mappings (the intent layer is PROTO; new device
  mappings are additive).
- Full audio (Suno beds + SFX library).
- The remaining crisis archetypes (data + evaluation procs on the S4 frame).

**Scope flag (surfaced, not silent):** the forge MVP scope includes *one* era
transition (email → streaming) and the epics place E5 inside the MVP (E1–E9).
This prototype defers the **entire** Era layer — the fun gate per GDD Win/Loss
is surge survival, which does not exercise the transition. If the side-by-side
comparison against the Godot tag checkout needs the transition to be fair, pulling a minimal
single-transition Era stub forward is a small additive change on the reserved
seam (§6.6) — a review decision, not a hidden cut.

### 13.3 Relationship to the Godot prototype — RULED (lavish 2026-08-08)

**Ruled: Odin-native root layout; `game/` leaves the main branch.** Odin's
convention is one directory per package at the repo root (`odin build <dir>`),
so the Odin build lives at the root — `core/`, `app/`, `harness/`, `demos/`,
`data/`, `goldens/`, `tools/`. The Godot prototype (PR #11/#12 — the proven-fun
reference) is removed from main on the first Odin code PR, after tagging the
fun-gate state **`prototype-fun-gate`**: the prototype stays runnable from the
tag forever (the step-6 side-by-side comparison runs from a tag checkout), and
the GL5.2-era "new repo at the fun gate" doctrine (GL5.2 §12.1) is fully
superseded — the pivot *is* the fresh codebase, in this repo, at its root.

---

## 14. GL5.2 Critical Review — the misses, honestly

The user asked for this explicitly: evolve the design, but surface the misses.
The GL5.2 review swarm's findings (M1–M5, m6–m16) were mostly **fixed in the
v1 text** before merge; what follows are the weaknesses that survived those
fixes — the ones that were *structural to the Godot stack* — plus what the
pivot itself costs. Each item: the miss, why it mattered, how this
architecture resolves it (or carries it honestly).

### 14.1 m6 — the portability narrative was aspirational (the big one)

**The miss.** GL5.2 sold "the server *could* re-sim an action log" (Exec
Summary, ADR-1) while ADR-6 quietly hedged: the GDScript core still depended
on Godot types (`RefCounted`, `Resource`, `Vector2i`) and Godot's PCG
implementation, so a server re-sim meant *re-implementing the sim in another
language and bit-matching Godot's RNG* — nobody costed that, and the
cheat-resistance story leaned on it.

**The resolution (native).** ODN-1/9/10: the core is pure Odin (no engine
types exist to leak in), the PRNG is ~40 lines of owned integer code with
pinned test vectors, and integer math is bit-exact across every Odin target.
The server validator **compiles the same `package core`** (ODN-6). Full
re-sim validation moves from "aspirational, un-costed" to "an ops-cost
choice." This is the pivot's single biggest architecture payoff.

### 14.2 The `state.sla` / `state.qos` ownership fork (M3)

**The miss.** GL5.2's canonical tick code (the most-copied block in the doc)
invoked `state.sla.accumulate(...)` and `state.qos.apply(...)` as RunState
peers while its prose said PacketFlow owns SLA and QoS is a collaborator. Two
agents reading different sections would build different sims. The merged text
patched the code block, but the *shape* that caused the fork — "systems as
peers on a state bag" — remained.

**The resolution (structural).** ODN-3 decides it once and removes the
conditions for the fork: **QoS is a set of pure procs** (not a system, so it
can't be a peer), and **SLA accumulators are fields of `Flow_State`** (so
there is no `state.sla` to phantom-reference). `flow_step` is the only caller.
The §4 tick flow and §6 system boundaries cannot contradict each other because
there is only one place the work happens.

### 14.3 The `[FinLT]` tax — an entire defensive layer, evaporated

**The miss.** GL5.2 carried a standing tax of Godot traps: JSON int→float
re-casting, float accumulators silently truncating, deferred-frame sizing,
theme propagation across CanvasLayers, headless-has-no-renderer capture rules,
`trait` reserved, no conditional compilation (debug code ships), silent
GDScript failures. Each was individually handled; collectively they were a
permanent complexity lien on every future change (and they kept recurring in
the sibling project's reviews).

**The resolution.** The trap class does not transfer: Odin is statically typed
with explicit casts (no silent int truncation), the save format is binary
(ODN-11 — no JSON for state), there is no scene tree (no deferred frames, no
themes), `-define:` is real conditional compilation (§7.6), and the harness's
headless pixels come from the software renderer (§10.4 — no "headless has no
renderer" gotcha). New costs replace them (manual memory, no editor) — stated
in §3.1, not hidden.

### 14.4 Dual catalog formats — two sources of truth by design (ADR-5)

**The miss.** `.tres` for the Inspector + "a JSON mirror for tooling" meant
the same balance numbers existed in two serializations kept in sync by
discipline — exactly the class of thing that drifts at 2am and passes review.

**The resolution.** ODN-5: JSON single source, validated fail-fast at load,
`#load`-embedded for release. The Inspector was the dual format's only
justification; the debug overlay's live sliders + write-back (§7.6) replace
the *workflow* without the dual source.

### 14.5 Autoload singletons — global mutable state as architecture (ADR-13)

**The miss.** AudioManager/SaveSystem/Settings/EventBus as autoloads made
cross-run reset a *discipline* ("destroyed/rebuilt per run") rather than a
fact, and gave every system a hidden global reach (the EventBus especially —
ADR-14 said "sibling systems never reach into each other" while providing a
global bus they all could).

**The resolution.** ODN-13: no globals exist; `App` owns the `Run` context;
per-run reset is "make a new arena," which cannot leak. ODN-14: no global bus;
the per-tick event buffer is drained by the one owner of the presentation
layer.

### 14.6 Signals as the primary communication mechanism (ADR-14)

**The miss.** Typed signals were the right Godot choice, but they baked in
ordering subtlety (sync-by-default with deferred escapes), invisible wiring
(connect sites scattered across systems), and untestable-by-diff
communication (you can't `diff` a signal storm). The GL5.2 reviews kept
finding *ordering* bugs (signal precedence, same-tick interactions) — a
symptom of the mechanism, not the design.

**The resolution.** ODN-14's event buffer: ordering is program order (visible
in a replay), wiring is one append site + one drain site, and the event stream
is a first-class golden artifact (the harness can assert
`Crisis_Triggered within 12000..16000ms` — §10.3 — without a single pixel).

### 14.7 What the pivot *costs* (the honest other column)

- **Mobile (FORGE #6) was the real risk — now ruled.** Godot's mobile export
  was solved; Odin+raylib's is emerging (`-subtarget:android` exists upstream
  with rough edges; raylib has Android/iOS backends). **The user's ruling
  (lavish 2026-08-08): desktop-first launch; mobile follows when the toolchain
  matures.** This was the one place the pivot moved backward — it is now a
  sequenced launch decision, not an open architecture risk.
- **No editor.** Map/level iteration is code + data + the debug overlay; the
  harness replaces "press play and look." Acceptable because maps are
  procedural and the design grid is simple — but it is a real workflow loss.
- **Ecosystem.** No Godot-sized tutorial corpus; mitigated by pinned Context7
  docs, the tiny API surface we use, and the harness as empirical ground truth.
- **UI/animation tooling.** The widget set (§9.2) and interpolation (§9.1) are
  built once and owned; no tween engine, no theme system. The light-canvas
  aesthetic is flat-color vector drawing — raylib's home turf — so the cost is
  low *for this game*.

### 14.8 What was *not* a miss (for the record)

GL5.2's system boundaries, the QoS queueing model, the fairness contracts, the
edge-case table (E1–E25), the MVP/full-game carve-out doctrine, and the
determinism-first *invariant* all survived review and port intact — the pivot
changes the substrate, not the design. This doc deliberately re-derives
nothing the forge/GDD/GL5.2 already locked.

---

## 15. Validation

| Check | Result | Notes |
|---|---|---|
| Decision compatibility | ✅ | Determinism (ODN-1/9/10) coherent across sim/save/validation/harness; QoS inside flow (ODN-3) has no peer to fork; seams (ODN-6/7) don't touch core |
| GDD system coverage | ✅ §15.1 | All GDD systems mapped; [LATER] layers spec'd to seam level per the buildable-core-first mandate |
| Forge locks | ✅ | No `[FORGE #n]` re-decided by this doc; A1–A7 art amendments incorporated (A6 became a data rule); FORGE #6's same-game doctrine was amended *by the user* to desktop-first sequencing (§18 OQ-1, lavish 2026-08-08); the forge MVP's single era transition is deliberately deferred past the parity prototype (§13.2) |
| Pattern completeness | ✅ | Communication, entity, state, data-access, error, event, time, memory all defined (§11) |
| Prototype buildability | ✅ §13 | Six-step manifest; each step demo-verifiable via the harness |
| GL5.2 misses | ✅ §14 | 6 surfaced with resolutions + the pivot's costs carried honestly |
| Version specificity | ✅ | Odin dev-2026-08, raylib 6.0 — both verified against upstream releases 2026-08-08 |

### 15.1 GDD coverage

| GDD system | Architecture support | Layer |
|---|---|---|
| M1 Draw/tiers/span | Command_Bus + Topology (§6.1); tiers/span in `pipe_tiers.json` | PROTO |
| M2 Packet types & QoS class queues | Flow + QoS procs (§6.2/6.3); `packet_types.json` | PROTO |
| M3 Topology & nodes / bundles | Topology (§6.1); terminals-via-routers rule (E26); pipe bundles + per-hop forwarding (routing ruling) | PROTO |
| M4 Era progression / lifecycle | Era FSM (§6.6); `eras.json`; contracts E14/E15 decided | LATER |
| M5 Crisis model (fair) | Crisis Engine (§6.4) + §11.3 contracts; `crises.json` | PROTO (Surge) |
| Win/Loss + Network Health | Network Health (§6.5) | PROTO |
| Controls (cross-platform) | Input layer (§9.3) + ODN-12 | PROTO (mouse) |
| Art & audio juice | View (§9.1, light-canvas canon) + Audio (§9.6) | PROTO view / LATER audio |
| Accessibility | View-layer (never-color-alone, reduced-motion, captions) carried | PROTO core set |
| Online services | Leaderboard seam (§6.8) + ODN-6 (portable-core validation) | LATER |
| Save / run | ODN-11 (mechanism PROTO via harness; player-facing LATER) | mixed |
| Performance/determinism | ODN-1/2/8/9/10/18 + §12 | PROTO |
| **Verification (new)** | The golden harness (§10) | PROTO — first |

---

## 16. Development Environment

### 16.1 Prerequisites

- **Odin `dev-2026-08`** — pinned; install per odin-lang.org; the pin lives in
  `.odin-version` and CI checks `odin version` against it.
- **raylib 6.0** — via `vendor:raylib` (ships with the pinned Odin). The
  harness additionally builds raylib-from-source (software renderer + memory
  platform) via a pinned script (`tools//build_raylib_sw.sh`), cached in CI.
- **Git + gh** (remote: `solarity-services/Packet-Plumber`).
- **Blender + Suno** — full-game art/audio pipelines, post-prototype (unchanged
  doctrines: owned assets only, paid-tier tracks).
- No Godot requirement for the Odin build; Godot 4.7.1 remains installed only
  to run the reference prototype from the `prototype-fun-gate` tag.

### 16.2 Repo layout (target)

```
packet-plumber/
  core/                 # package core — the simulation (pure; §4 import rule)
  app/                  # package main — the game executable (raylib allowed)
    render/             # package render — the light-canvas view
    ui/                 # package ui — immediate-mode widgets
  harness/              # package main — the golden-image runner (§10)
  demos/                # scripted scenarios (*.dem)
  data/                 # JSON catalogs (§8.1)
  goldens/              # golden PNGs + T1 hash manifests (+ _reports/ on failure)
  tools/                # build scripts (software-raylib, CI helpers)
  _bmad-output/         # planning artifacts (unchanged)
  project-context.md    # redone for Odin+Raylib (this branch)
  # game/ — REMOVED per the 2026-08-08 ruling; the `prototype-fun-gate` tag preserves it
```

(Packages at the repo root — the Odin-native convention; ruled 2026-08-08.)

### 16.3 Commands + CI gates

```bash
odin run app                 # play (dev)
odin build app -define:PP_DEBUG=true   # debug tools build
odin test core               # core unit tests (fairness contracts, determinism, QoS)
odin run harness -- run      # T1 hashes + T2 pixels vs goldens
odin run harness -- save     # re-bless goldens (deliberate, PR-reviewed)
```

CI gates per job (matrix §10.7): (1) **purity check** — `odin build core
-build-mode:obj` (a package with no `main` builds as an object file)
plus the import whitelist lint (no `vendor:*`/`core:os`/`core:time`); (2)
grep gates from §11.6 (no file-scope `var`, no dropped errors, no map
iteration in core); (3) `odin test`; (4) `harness run`; (5) on T2 failure,
upload the diff bundle artifact.

### 16.4 First steps (handoff to Heist 2)

1. **Migration step (first Odin code PR):** tag `prototype-fun-gate` on main,
   remove `game/`, scaffold the root packages (core/app/harness + CI matrix) —
   **harness skeleton first** (§13.1 step 1).
2. Port the catalogs (the tagged prototype's `game/data/` values → `data/*.json`, integers only).
3. Steps 2–6 of §13.1, each with its demo + goldens.
4. Pin the design invariants as `@(test)` contracts at the lowest layer
  (snap precision, fair-crisis, drop precedence, no-soft-lock, replay equality).
5. Side-by-side fun comparison against the `prototype-fun-gate` checkout at
  §13.1 step 6 — the pivot's gate.

---

## 17. GL5.2 ADR Disposition (traceability)

| GL5.2 ADR | Disposition | As |
|---|---|---|
| ADR-1 Sim/View separation | **Evolved — now structural** | ODN-1 |
| ADR-2 Fixed 20 Hz tick | **Kept** | ODN-2 |
| ADR-3 QoS 3-class-queue WFQ | **Kept (design); ownership fixed** | ODN-3 |
| ADR-4 Fair-crisis model | **Kept** | ODN-4 |
| ADR-5 Data-driven catalogs | **Evolved — single source** | ODN-5 (§14.4) |
| ADR-6 Leaderboard seam | **Evolved — portable core upgrades validation** | ODN-6 (§14.1) |
| ADR-7 CrisisDirector seam | **Kept — proc field, zero boilerplate** | ODN-7 |
| ADR-8 Packet-dot pooling | **Evolved — no view objects at all** | ODN-8 |
| ADR-9 Single seeded RNG | **Evolved — owned PRNG + cosmetic stream** | ODN-9/ODN-15 |
| ADR-10 Integer-tick math | **Kept + array-iteration corollary native** | ODN-10 |
| ADR-11 Save = seed + action log | **Kept — binary format** | ODN-11 (§14.3) |
| ADR-12 Unified input → Command | **Kept — mouse first** | ODN-12 |
| ADR-13 Scene/FSM + autoloads | **Evolved — explicit context, no globals** | ODN-13 (§14.5) |
| ADR-14 Typed signals | **Replaced — event buffer** | ODN-14 (§14.6) |
| ADR-15 Audio doctrine | **Kept** | ODN-15 |
| ADR-16 MVP scope gate | **Revised — buildable-core-first** | ODN-16 |
| (new) Golden harness | **New** | ODN-17 |
| (new) Memory model | **New** | ODN-18 |

---

## 18. Review Rulings (lavish, 2026-08-08)

1. **OQ-1 — Mobile under the pivot → RULED: desktop-first launch.** `[FORGE #6]`
   (Steam + mobile same-game) is amended by the user to a *sequencing*: ship
   Steam PC/Mac first; **mobile follows when the Odin+raylib toolchain
   matures** (upstream state at ruling time: Odin has `-subtarget:android`
   with rough edges — e.g. odin-lang/Odin#6759; raylib ships Android/iOS
   backends). The same-game doctrine is deferred, not abandoned — the intent
   layer (ODN-12) and camera-fit framing (§9.1) keep mobile additive rather
   than a re-architecture, and a toolchain-maturity spike is re-evaluated at
   the production gate. (Cascade flagged for Gru: the forge doc's #6 wording
   needs the amendment recorded there.)
2. **OQ-2 — Repo layout → RULED: Odin-native root layout; `game/` removed from
   main.** Packages at the repo root (`core/`, `app/`, `harness/`, … — the
   `odin build <dir>` convention); the Godot prototype is preserved via a
   `prototype-fun-gate` tag before removal (the step-6 side-by-side comparison
   runs from a tag checkout). Applied in §13.3/§16.2/§16.4.
3. **OQ-3 — Touch/controller timing → RULED: mouse-only prototype.** The intent
   layer is PROTO; touch/controller mappings are additive later layers.
4. **OQ-4 — Audio in the Odin prototype → RULED: 1–2 stings at step 6.** The
   full reactive SFX pool stays [LATER].
5. **Routing model → RULED: per-hop forwarding + ECMP + bundled parallel
   pipes (lavish 2026-08-10).** The merged prototype (PR #17) routes with a
   one-shot BFS cached at spawn + parallel-pipe LB (round-robin /
   capacity-weighted) + severance-only reroute. The locked full-game model
   replaces all three: each junction **forwards per-packet** (internal — no
   router-config UI; players draw pipes), choosing among equal-cost next hops
   via a **deterministic ECMP hash** `splitmix64(src, dst, class, pkt_id) mod
   N`; **parallel pipes bundle into one pooled-capacity link** (cap = sum),
   deleting the LB mechanic (round-robin and weighted LB are gone; redundancy
   becomes active capacity). Determinism holds via the 4-rule spine pinned in
   ODN-9/ODN-10 (forwarding table rebuilt on topology-change only; ECMP = pure
   hash, no rng draw; bundled cap = static sum; replay-test pinned). QoS (§6.3)
   is orthogonal and unchanged. Captured in GDD §M1/§M3/§M5 + arch §6.1/§6.2;
   E1 softens under bundles, E29 is now automatic.
   **Amended 2026-08-13 (user ruling, capacity-cost routing):** path cost is
   now the STATIC per-tier integer `cost` ladder (data/pipe_tiers.json
   20/10/5, ODN-5) — the routing table is a Dijkstra over pipe costs, "flows
   prefer fat pipes", equal END-TO-END cost still ECMPs (pure hash). The
   SPF/ECMP determinism spine is untouched; congestion avoidance stays the
   player's job (QoS + engineering). Implemented in this PR; the assist
   features (flow preview, glow, forecast) are follow-up jobs. Clean-span
   degradation remains deferred. Source artifact preserved at
   `docs/routing-explorer.html`.

---

_Generated by the `gds-game-architecture` workflow (headless), adapted to the
`packet-plumber-odin-architecture` briefing. Evolves `architecture-v1.md`
(GL5.2) onto Odin + Raylib per the user's engine pivot. Source of truth for
locked design = the forge; for the game = the GDD + decision-log; for the
visual canon = art-direction v1 + amendments + look-book v1; for code conduct
= `project-context.md` (redone for Odin in this branch); for the prior
technical design = GL5.2. Human review of this document runs via **lavish**
before the PR opens._
