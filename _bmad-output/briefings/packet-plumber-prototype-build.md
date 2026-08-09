# Briefing: packet-plumber-prototype-build

- **Repo:** Packet-Plumber (`/Users/moses/code/packet-plumber`, remote: `solarity-services/Packet-Plumber`)
- **Worktree:** work directly in the repo root on a feature branch off `main` (PP's convention; PR targets main)
- **Workflow:** gds-dev-story / gds-quick-dev (implement the sprint-plan stories). Perkins: **ON** (code — prototype-appropriate rigor: correctness + the fun-test loop working, not production-grade). Self-review before PR: bmad-review-edge-case-hunter + bmad-review-verification-gap (the determinism spine + headless testability are load-bearing — verify the sim is actually testable headless).
- **Model policy:** unset — pi default. This is a substantial multi-story build.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** ON (code; one round on the PR — prototype-appropriate).

## Mission — THE FUN-TEST

Build the **MVP prototype** to the **fun-test threshold**: a **PLAYABLE email→streaming slice** of Packet Plumber. The entire forge → GDD → architecture → sprint-plan pipeline existed to answer ONE question: ***is drawing pipes + managing packet types actually fun?*** This build answers it. Everything else (full eras, AI disasters, leaderboards) waits until fun is proven.

**Build through sprint-plan sequence S0→S4** (where the fun-test loop closes). S5→S6 (fuller MVP polish) come AFTER fun is validated — do not build them in this pass.

## Source material (read ALL — these are the complete spec)

1. **`_bmad-output/planning-artifacts/sprints/sprint-plan-v1.md`** + **`stories-v1.md`** — the 35 MVP stories (Given/When/Then), sequenced S0→S6. **Build S0→S4 in order.** This is your task list.
2. **`_bmad-output/planning-artifacts/architecture/architecture-v1.md`** — the buildable design: 8 core systems, 16 ADRs, 25 edge-case contracts. **The determinism spine (ADR-10: pure integer-tick headless-safe Simulation Core separated from Godot rendering) is foundational** — S0 builds it; everything sits on it.
3. **`_bmad-output/planning-artifacts/gdds/.../gdd.md`** — the mechanics (M1–M5: pipes/tiers/span, QoS lanes, topology/nodes, era progression, crises/Network Health).
4. **`_bmad-output/planning-artifacts/sprint-plan-inputs.md`** — the demand-pairing data spec: `PressurePlan` structure + typed source→sink mapping + **WEIGHTED_RANDOM dst-selection** + player visibility. **Implement exactly this.**
5. **`project-context.md`** — Godot 4.7.1, GDScript, gl_compatibility, landscape 1280×720, canvas_items/expand, custom-audio-only.

## The MVP slice (what "playable" means)

- **One era transition:** Email → Streaming (the forge-locked MVP)
- **Two packet types:** email (low priority) + streaming (high bandwidth)
- **4–6 nodes** on one map (terminals: Residential + Content host; junctions/routers)
- **Core actions:** draw pipes (snap-to-node), upgrade pipe tiers, designate priority lanes
- **Predictable crises:** node 🟡 strained → 🔴 critical (the warning surface); survive the streaming surge
- **Network Health meter** (the loss condition) — drains on SLA breach, recharges on health
- **The simulation core:** deterministic, integer-tick, **headless-testable** (per ADR-10 — the sim runs without Godot rendering; this is how fun gets validated reproducibly + how Perkins/you verify it)

## ⚡ USE THE GOPEAK MCP SERVER (it's available — first build with it)

The GoPeak Godot MCP server is configured + the PP project has the addons enabled (`game/addons/godot_mcp_*`, plugins on in `project.godot`). **Use it for visual verification** — the one thing file-editing can't do:

- **Run the game** (`godot --path game` via bash) → the runtime addon opens port 7777.
- **Capture screenshots** via the MCP runtime tools (`capture_screenshot` / `capture_viewport`) to **verify the prototype actually renders + plays right** — packet flow visible, pipes draw correctly, nodes show health states, the Network Health meter reacts. A headless build that never "looks" at the game ships visual bugs.
- **Inspect the live scene tree / runtime state** via MCP when debugging flow issues.
- The LSP (port 6005) + editor bridge (6505) need the editor running — use them if you run the editor, but the **runtime screenshot loop is the primary verification tool**.

Workflow: edit files → run the game → MCP-capture a screenshot → verify it looks/plays right → iterate. **Do NOT ship a prototype you haven't visually verified via screenshots.**

## Constraints (do not violate — GDD/architecture/forge-locked)

- **Determinism spine:** the Simulation Core is pure (integer-tick, headless-safe, seeded) — separated from Godot rendering. S0 nails this; later stories build on it. (ADR-10)
- Core mechanic = Draw (A) + React (C). Crises are FAIR + PREDICTABLE.
- Two differentiators in the MVP: (1) packet types + QoS lanes (the streaming/email priority trade-off), (2) the era-transition modernization pressure.
- Godot 4.7.1, GDScript, gl_compatibility, landscape 1280×720, canvas_items/expand.
- Cross-platform input-abstracted (touch + mouse + controller → unified actions).
- **Audio: custom/original exclusively** (no stock licenses — streamer monetization rule). For the prototype, placeholder/procured-original SFX are fine; flag if you need assets.
- No em-dashes in any user-facing copy (global ban).
- **Do NOT build S5→S6** (fuller MVP) — stop at the S4 fun-test threshold.

## Acceptance — the fun-test gate

- **The prototype is PLAYABLE:** `godot --path game` runs it; the player can draw pipes between nodes, packets flow (email + streaming), priority lanes work, the streaming surge is survivable, Network Health reacts, failure (Error 404) is reachable.
- **Visually verified via MCP screenshots** (packet flow, pipe drawing, node health states, the meter) — include screenshots in the PR/lavish.
- **Headless-testable:** the sim core runs without rendering (a seeded run reproduces; a headless test exercises the fun-test loop). Per ADR-10.
- The S0→S4 sprint-plan stories implemented (Given/When/Then contracts met where pinned).
- After user approval (the fun-test is the user PLAYING it): commit, push, open PR targeting main. **Never merge.**

## Review loop (lavish — the fun-test IS the user playing it)

When the prototype is playable + visually verified: render via **lavash** — screenshots of the running prototype (packet flow, a crisis, a win), the controls, how to run it, + your honest read on whether the core loop *feels* fun. The user's verdict (play it / see it) is the gate — this is the moment the whole pipeline was built for.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set packet-plumber-prototype-build working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger note packet-plumber-prototype-build "lavish fun-test posted: <url>"` when the playable prototype + screenshots are up
- `/Users/moses/code/bin/ledger set packet-plumber-prototype-build in-review "PR <url>"` when the PR opens (after the fun-test verdict)
- `herdr notification show "pp-prototype-build" --body "<one-line>"` on finish
- Final message: summary, is it playable (yes/no + what works), the screenshots, your honest fun-read, the PR URL, what's deferred (S5→S6).

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-prototype-build
- base: main
