# Briefing: packet-plumber-odin-architecture

- **Repo:** Packet-Plumber (`/Users/moses/code/packet-plumber`, remote: `solarity-services/Packet-Plumber`)
- **Worktree:** WORKTREE off `main` (isolate). The Odin architecture is a full re-plan deliverable; lavish review before PR.
- **Workflow:** **gds-game-architecture** (or bmad-architecture) + a critical-review pass. Perkins: OFF (docs). Self-review before PR: bmad-review-adversarial-general + bmad-review-edge-case-hunter (this architecture must be RIGHT — it's the foundation of the full re-plan).
- **Model policy:** **kimi-coding (k3)** — the user switched to kimi for game work. If the bare label fails to route, use the full provider path for kimi.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** OFF (docs deliverable).

## Mission — THE ODIN PIVOT ARCHITECTURE (Heist 1 of the engine pivot)

The user committed to a **full engine pivot: Godot → Odin + Raylib** ("let's move to Odin, let's own it end to end," with the LLM-coding reframe: LLMs code, so building infrastructure isn't a cost). This is the **new technical architecture** for Packet Plumber in Odin. It **evolves** the proven GL5.2 (Godot) architecture's DESIGN into Odin — it does NOT re-brainstorm the game. AND it must **highlight any design misses** in the GL5.2 architecture (a critical review, not just a port).

### ⚡ PRIORITY: buildable-core-first (the user wants to SEE the early prototype soon)
The user re-writing everything in Odin BUT wants to **see the early Odin prototype soon** (to compare to the Godot prototype). So this architecture must be **buildable-oriented, not exhaustive-first**: spec the **BUILDABLE CORE** clearly enough that the EARLY PROTOTYPE (Heist 2, immediately after) can implement it fast. Prioritize:
- **The Simulation Core** (Odin, determinism native) — the foundation.
- **The Raylib rendering** (the light-canvas aesthetic).
- **The golden-image harness** (verification).
- **The fun-test systems** (Topology, PacketFlow, QoS, Crisis, NetworkHealth — the fun-test loop).
The **full systems** (Era, Economy, Leaderboard) are **later layers** — spec them, but mark them clearly as post-prototype. Optimize for "the early prototype can build from this tomorrow," not "every system exhaustively spec'd first."

## Inputs (read ALL)

1. **`_bmad-output/planning-artifacts/architecture/architecture-v1.md`** (GL5.2 Godot architecture, 64 Godot-specific mentions) — the proven DESIGN to evolve. **Also critically review it for misses** (the adversarial review in `architecture/review/` already flagged some — e.g. m6: the GDScript core isn't truly portable, the `state.sla`/`state.qos` ownership fork, the `maybe_send_shortlist_notification` vs ADR ownership).
2. **`_bmad-output/planning-artifacts/gdds/.../gdd.md` + `epics.md` + `decision-log.md`** — the engine-agnostic game design (survives; the architecture implements it in Odin).
3. **`project-context.md`** — the Godot-locked engine pin (redo for Odin+Raylib).
4. **`_bmad-output/planning-artifacts/forge-packet-plumber-2026-08-05/forged-idea.md`** — the locked decisions (Mini Motorways style, determinism spine, etc.).
5. **The golden-image test harness reference:** ThePrimeagen's approach ([video](https://www.youtube.com/watch?v=G8vdu30EEfw)) — golden-image regression testing with scripted test frames + render-to-texture + deterministic replays + agent-readable pixel diffs. **This is a first-class system, built early.**
6. **The Godot prototype** (`game/` on main, #11/#12) — the proven-fun REFERENCE implementation (the Odin build re-implements the proven-fun DESIGN, not the code).

## The Odin architecture — what to design

### 1. The Simulation Core (Odin — the crown jewel, ADR-10 reborn NATIVELY)
- **Determinism is native:** Odin's own deterministic RNG (no Godot types — fixes the m6 portability flag). Integer-tick math for state-affecting paths. A single seeded RNG the whole run replays from.
- **Data-oriented:** packets + topology + flows as **SOA arrays** (structs of arrays), hot integer loops, contiguous buffers — Odin's strength for a network simulation ("play the internet" is data-heavy). NOT Godot's node-tree/scene-graph.
- **Headless-safe:** the core runs without any rendering (pure functions over state) — the golden-harness + server re-sim depend on this.
- **Portable:** the SAME compiled core runs client + server (leaderboard anti-cheat re-sim becomes trivial — the architecture's aspirational Godot problem becomes free in Odin).

### 2. The Rendering layer (Raylib)
- Top-down 2D, the locked **light-canvas Mini Motorways aesthetic** (literal buildings, round capacity-scaled routers, bezier pipes, blue/grey packets, procedural map — art-direction v1.2 canon).
- Raylib idioms for the render loop, input (mouse draw, snap-to-node, router select), the packet-flow visualization.
- **Render-to-texture** (for the golden-image harness).

### 3. The Golden-Image Test Harness (FIRST-CLASS — the verification foundation)
This is the ENABLER of LLM-driven Odin dev — spec it as a core system, **built early (before feature stories)**. Per ThePrimeagen's reference:
- **Demo runner:** plays scripted demos (seeded routing scenarios: draw pipes, spawn packets, run the surge).
- **Test frames** (time + mouse): script input over time ("move mouse to X over 500ms") → the game acts as if real input → deterministic capture.
- **Render-to-texture:** render to a texture (not screen) → save to file (golden) or paint to screen.
- **Golden compare:** on every run, replay all demos + compare to reference goldens — automated visual regression.
- **Agent-readable diffs:** on mismatch, log the pixel diff so the LLM can diagnose what changed. The LLM's verification loop.
- **Update goldens:** `test save` re-saves when intentional.
- **Build matrix:** Windows/Mac/Linux amd64/arm64 in CI.

### 4. The core systems (evolve the GL5.2 boundaries into Odin)
The GL5.2 system boundaries survive (they're engine-agnostic-good): Topology, PacketFlow, QoS, Crisis, NetworkHealth, Era, Economy, Leaderboard. Re-implement each in Odin (data-oriented, the core separated from rendering). Keep the data model (`Packet {src, dst, route}`, the PressurePlan, WEIGHTED_RANDOM dst-selection).

### 5. The surviving-docs touch-up (folded in)
Note in the architecture + a light touch-up that **GDD/art-direction/narrative are engine-agnostic** (survive) + **project-context is now Odin+Raylib** (redo the engine pin).

## ⚠️ CRITICAL REVIEW — highlight GL5.2 architecture misses
Don't just port. The GL5.2 architecture had known weaknesses (see `architecture/review/adversarial-general.md` + `edge-case-hunter.md`):
- **m6**: the GDScript core isn't truly portable (Godot types + PCG) — the architecture's re-sim narrative was aspirational. **How does Odin fix this natively?** (Answer: no Godot types, own RNG, same compiled core.)
- **The `state.sla`/`state.qos` ownership fork** (the canonical tick code contradicts the data model + system boundaries). **Resolve it cleanly in the Odin architecture** (decide once: SLA accumulators + QoS live INSIDE PacketFlow, invoked by `flow.step` — not as phantom peers).
- **Any other misses you find** — surface them honestly (the user explicitly asked: "evolve, but highlight misses if any").

## Constraints
- **Evolve, don't re-brainstorm** — the game design (GDD) is locked; this re-targets the technical implementation to Odin.
- **Determinism native** (own RNG, integer-tick, SOA, headless-safe, portable) — the #1 requirement (it fixes the Godot weak points).
- **Golden-harness is first-class + early** (ThePrimeagen reference) — the LLM-verification foundation.
- **Light canvas + the locked visual canon** (art-direction v1.2) — Raylib renders it.
- **Highlight misses honestly** (the critical review is a deliverable).
- Em-dashes fine (PP copy, not RT).

## Review loop (lavish — BEFORE the PR)
Big architecture deliverable: render via **lavish** (the Odin architecture: the core/rendering/harness/systems, the determinism-native design, the GL5.2 misses highlighted + resolved). The user reviews the re-plan before it drives the sprint + stories.

## Acceptance
- Odin architecture at `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md`.
- Simulation Core (Odin, determinism native, SOA, headless-safe, portable) spec'd.
- Rendering (Raylib, the locked visual canon) spec'd.
- Golden-image test harness (first-class, ThePrimeagen reference, built early) spec'd.
- Core systems evolved (GL5.2 boundaries → Odin).
- **The GL5.2 misses highlighted + resolved** (the critical review).
- The surviving-docs touch-up (project-context → Odin+Raylib).
- After user review: commit, push, open PR targeting main. **Never merge.**

## Self-report (do not skip)
- `/Users/moses/code/bin/ledger set packet-plumber-odin-architecture working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger note packet-plumber-odin-architecture "lavish review posted: <url>"` when up
- `/Users/moses/code/bin/ledger set packet-plumber-odin-architecture in-review "PR <url>"` when PR opens (after approval)
- `herdr notification show "odin-architecture" --body "<one-line>"` on finish
- Final message: the architecture path, the determinism-native design, the GL5.2 misses highlighted, the harness spec, lavish URL, open questions.

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: packet-plumber-odin-architecture · base: main
