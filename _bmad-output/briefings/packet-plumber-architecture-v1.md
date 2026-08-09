# Briefing: packet-plumber-architecture-v1

- **Repo:** Packet-Plumber (`/Users/moses/code/packet-plumber`, remote: `solarity-services/Packet-Plumber`)
- **Worktree:** work directly in the repo root (local repo, no worktree — this IS the repo; PR targets main)
- **Workflow:** **gds-game-architecture** — read the skill's step file at `/Users/moses/code/.agents/skills/gds-game-architecture/SKILL.md` and follow it. The architecture is the technical design that makes the GDD BUILDABLE — engine systems, scene structure, core systems, data model, backend. **Do NOT re-decide anything the GDD locked** — translate design into technical architecture. Orchestration overrides per standing orders (genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Self-review before PR: bmad-review-adversarial-general / bmad-review-edge-case-hunter, max 10 panes, badge out all.
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** OFF (docs deliverable).

## Mission

Produce the official BMGD technical architecture for Packet Plumber — Step 6 of the setup flow. This is the bridge between the GDD (what the game IS) and the sprint plan + prototype build (how it's BUILT). Every later agent (sprint planning, story implementation) reads this.

## Source material (read ALL in full before writing)

1. **`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md`** — the GDD (4 pillars, 6 eras, 9 packet types, open-ended run + Network Health, link-level QoS, leaderboards, monetization). **PRIMARY INPUT.**
2. **`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/epics.md`** — the 11 epics derived from the GDD.
3. **`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/decision-log.md`** — the 15+ review-evolution decisions (provenance for every design choice).
4. **`project-context.md`** (repo root) — technical ground truth: Godot 4.7.1, GDScript, gl_compatibility renderer, landscape 1280×720, stretch mode canvas_items / aspect expand, cross-platform (Steam + mobile), 60fps budget, custom-audio-only rule.
5. **`_bmad-output/planning-artifacts/briefs/brief-Packet-Plumber-2026-08-05/brief.md`** — the game brief.
6. **`_bmad-output/planning-artifacts/forge-packet-plumber-2026-08-05/forged-idea.md`** — the forge output (locked decisions + the 4 surviving weak points).
7. **`/Users/moses/code/docs/game-design-references.md`** — Tyroller + Brush references (the pillars' provenance).

## Architecture scope — what to design

Translate every GDD system into a buildable technical design. Cover:

### Engine + project structure
- Godot 4.7.1 project layout (autoloads/singletons, scene hierarchy, the `scenes/` `scripts/` `assets/` `data/` dirs from the setup).
- The node/scene architecture: how the game world, the topology (nodes + pipes), the UI, and the meta-layer compose.

### Core systems (each needs a clear boundary + interface)
- **Pipe-drawing system** — input model (touch/mouse/controller → snap-to-node → pipe creation/validation), the routing/graph data structure (how nodes + pipes are represented, adjacency, pathfinding if any).
- **Packet-flow simulation** — how packets spawn, travel along pipes, respect QoS priority lanes, consume bandwidth, arrive/fail. The simulation tick / update loop.
- **QoS / priority lanes** — link-level priority (from the GDD): how a pipe's bandwidth is allocated across packet types, the trade-off mechanics.
- **Era progression** — the state machine (6 eras: what unlocks, what obsoletes, transition triggers, the infrastructure-lifecycle/upgrade model — the differentiator).
- **Crisis model** — the predictable/fair disaster system: warning signs (node strain states), escalation curves, failure modes, how crises are DESIGN CONSEQUENCES not random.
- **Network Health** — the loss condition: how it's calculated, what drains it, the threshold.
- **Economy / score** — currency, contracts, score, the run loop.
- **Meta-layer** — global leaderboards (this implies a BACKEND — design the service boundary: what's client vs server, the API, the auth, where it hosts). Note: this is the most architecturally significant new system.

### Data model
- How game data is structured: node types, pipe types, packet types (the 9 from the GDD), eras, crises — as data files (JSON/Resource) vs code. The data-driven design (new content = data, not code).

### Cross-cutting concerns
- **Save / run system** — open-ended runs, save state, resume.
- **Cross-platform input** — the input abstraction layer (touch + mouse + controller → unified actions), proven by the setup's stretch/aspect config.
- **Audio** — the custom-audio pipeline (no stock licenses), the reactive SFX system per the Thomas Brush juice lens.
- **Performance** — 60fps budget, the simulation cost (packet-flow at scale), mobile constraints.

### MVP vs full-game architecture
- Carve out the **prototype architecture** (the email→streaming MVP slice: 1 era transition, 2 packet types, draw+upgrade+prioritize, survive the surge). The full architecture must make clear what the prototype needs vs what's full-game. The prototype tests the CORE loop; the architecture should let the prototype be built without the meta-layer (leaderboards) or the full era tree.

### The 4 surviving weak points (address each architecturally)
1. **Fun unproven** → architecture enables a fast prototype loop (data-driven, hot-reloadable, minimal setup to test the core loop).
2. **Plumbing metaphor limits at VPN/VLAN/SDN** → how late-era tech maps to the pipe/valve visual vocabulary (or where the metaphor extends vs breaks).
3. **Engineer/non-engineer audience balance** → difficulty/accessibility systems (scaling, assists, the QoS abstraction depth).
4. **V2 AI stress-test system** → where it plugs in architecturally (an interface the AI disaster director can satisfy later, without building it now).

## Constraints (do not violate — GDD/forge-locked)

- Godot 4.7.1, GDScript, gl_compatibility, landscape 1280×720, canvas_items/expand stretch.
- Cross-platform same-game (Steam controller+mouse + mobile touch) — one project, input-abstracted.
- Experience-first; mechanics serve the experience (Tyroller).
- Crises are FAIR and PREDICTABLE — design consequences, never random.
- Two differentiators: (1) packet types + QoS lanes, (2) era progression + infrastructure lifecycle.
- Visual: Mini Motorways style (2D/isometric, clean, readable).
- Audio: custom/original exclusively.
- Go-to-market: free prototype → playtest → Steam page → full launch. NO early access.
- Satirical brand names (YouTune, Amazoom) — never real trademarks.
- The leaderboard/meta backend is the biggest architectural decision — propose a pragmatic approach (don't over-engineer for a prototype that hasn't proven fun yet; the backend can be a thin stub for the MVP).

## Review loop (lavish — BEFORE the PR opens)

DOCS deliverable: when drafted + self-reviewed, render via the **lavish** skill and post the review URL. Do NOT open the PR until the user's verdict. The architecture is visual (system diagrams, scene tree, data flow) — a rich lavish render with diagrams is expected.

## Acceptance

- Architecture doc at `_bmad-output/planning-artifacts/architecture/architecture-v1.md` following the gds-game-architecture skill structure.
- Every GDD system translated into a buildable technical design (clear boundaries + interfaces).
- Scene tree / autoload structure defined.
- Data model specified (data-driven design for content).
- Leaderboard/meta backend approach proposed (pragmatic, MVP-stubbable).
- MVP prototype architecture carved out.
- The 4 surviving weak points addressed architecturally.
- After user approval: commit, push, open PR targeting main. **Never merge.**

## Env/bootstrap

This IS the repo — no worktree, no bootstrap copy. BMad + GDS module installed in `_bmad/`. Godot 4.7.1 at `/opt/homebrew/bin/godot`. GDD + brief + project-context all on main.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set packet-plumber-architecture-v1 working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger note packet-plumber-architecture-v1 "lavish review posted: <url>"` when the review goes up
- `/Users/moses/code/bin/ledger set packet-plumber-architecture-v1 in-review "PR <url>"` when the PR opens (after approval)
- `herdr notification show "packet-plumber-architecture-v1" --body "<one-line>"` on finish
- Final message: summary, architecture path, lavish URL, the system count, the leaderboard/backend approach, open questions.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-architecture-v1
- base: main
