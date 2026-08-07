# Briefing: packet-plumber-sprint-plan-v1

- **Repo:** Packet-Plumber (`/Users/moses/code/packet-plumber`, remote: `solarity-services/Packet-Plumber`)
- **Worktree:** work directly in the repo root (local repo, no worktree — this IS the repo; PR targets main)
- **Workflow:** **gds-create-epics-and-stories** — read the skill's step file at `/Users/moses/code/.agents/skills/gds-create-epics-and-stories/SKILL.md` and follow it. The GDD already produced 11 epics; this phase breaks them into **buildable stories** and **sequences them for the MVP-first prototype**. Orchestration overrides per standing orders (genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Self-review before PR: bmad-review-adversarial-general / bmad-review-edge-case-hunter, max 10 panes, badge out all.
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** OFF (docs deliverable).

## Mission

Produce the Packet Plumber sprint plan — Step 7 of the setup flow, the last doc gate before the prototype build. Break the 11 GDD epics into buildable user stories, sequence them **MVP-first** (the email→streaming prototype that tests fun comes FIRST), and **define the demand-pairing data** that the architecture left as a flagged follow-up.

## Source material (read ALL in full)

1. **`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md`** — the GDD (4 pillars, 6 eras, 9 packet types, M1–M5 mechanics, win/loss).
2. **`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/epics.md`** — the 11 epics derived from the GDD.
3. **`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/decision-log.md`** — the 15+ review-evolution decisions.
4. **`_bmad-output/planning-artifacts/architecture/architecture-v1.md`** — the architecture (8 core systems, 16 ADRs, the Packet data model with src/dst/route, the PressurePlan mechanism). **PRIMARY technical input** — stories must map to the architecture's systems (Topology, PacketFlow, QoS, Crisis, NetworkHealth, Era, Economy, Leaderboard seam).
5. **`_bmad-output/planning-artifacts/sprint-plan-inputs.md`** ⬅️ **FLAGGED DELIVERABLE** — the demand-pairing data-design task from the architecture review. **You MUST define this** (see below).
6. **`project-context.md`** + the brief + forge output (context).

## Scope — what to produce

### 1. Story breakdown (MVP-first sequencing)
Break the 11 epics into buildable stories. **Sequence them so the MVP prototype (email→streaming slice) is the first sprint(s)** — the goal is to test FUN as cheaply as possible before building the full game. The MVP slice (from the forge):
- ONE era transition: Email → Streaming
- TWO packet types (email + streaming)
- 4–6 nodes on one map
- Core actions: draw pipes, upgrade pipes, designate priority lanes
- Predictable crises (node 🟡→🔴), survive the streaming surge
- The simulation core (determinism, headless-safe per architecture ADR-10)

The full-game stories (later eras, AI disasters, leaderboards, all 9 packet types) come AFTER the MVP stories in the sequence — they're the post-fun-validation work.

### 2. Demand-pairing data definition (FLAGGED — from sprint-plan-inputs.md)
The architecture models `Packet {src, dst, route}` and the `PressurePlan` mechanism, but left the demand-pairing DATA undefined. **This sprint plan must define:**
- **`PressurePlan` structure** — enumerate the fields (explicit src→dst pairs? per-source volume + dst-selection rule?)
- **Typed source→sink mapping per era** — which packet types originate at which source terminals and terminate at which sink terminals (the proposed baseline table is in sprint-plan-inputs.md — confirm/adjust)
- **Destination-selection rule** — when a source spawns a packet, how is `dst` chosen? (random matching sink? nearest? load-balanced?) Pin as a decided behavior with a headless test.
- **Player visibility** — how the player SEES source→destination demands (color-coding, demand lines, forecast markers)

This is the routing-puzzle legibility the player needs (P1). It's DATA/CONTENT design (the pairings are tunable per-era), driven through the architecture's PressurePlan mechanism.

### 3. MVP testability
Every MVP story should be **testable headless** (per architecture determinism/ADR-10) — the prototype must prove fun via a seeded, reproducible run, not just "looks right in the editor."

## Constraints (do not violate — GDD/architecture/forge-locked)

- Experience-first; mechanics serve the experience (Tyroller).
- Core mechanic = Draw (A) + React (C). Crises are FAIR and PREDICTABLE.
- Two differentiators: (1) packet types + QoS lanes, (2) era progression + infrastructure lifecycle.
- Godot 4.7.1, GDScript, gl_compatibility, landscape 1280×720, canvas_items/expand.
- Cross-platform same-game (Steam + mobile), input-abstracted.
- Audio: custom/original exclusively.
- Go-to-market: free prototype → playtest → Steam page → full launch. NO early access.
- The architecture's determinism spine (pure integer-tick headless-safe Simulation Core separated from Godot rendering) is foundational — MVP stories build on it.

## Review loop (lavish — BEFORE the PR opens)

DOCS deliverable: when drafted + self-reviewed, render via the **lavish** skill and post the review URL. Do NOT open the PR until the user's verdict. The sprint plan is a natural fit for a rich lavish render (story map, MVP-slice visualization, sequencing).

## Acceptance

- Sprint plan at `_bmad-output/planning-artifacts/sprints/sprint-plan-v1.md` (+ epics/stories files per the skill's structure).
- The 11 GDD epics broken into buildable stories, **MVP-first sequenced** (email→streaming prototype stories first).
- Every MVP story maps to an architecture system + is headless-testable.
- The **demand-pairing data fully defined** (PressurePlan fields + typed source→sink mapping + destination-selection rule + player visibility).
- The MVP slice is clearly carved (the fun-test gate).
- After user approval: commit, push, open PR targeting main. **Never merge.**

## Env/bootstrap

This IS the repo — no worktree, no bootstrap copy. BMad + GDS module installed in `_bmad/`. GDD + architecture + sprint-plan-inputs all on main.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set packet-plumber-sprint-plan-v1 working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger note packet-plumber-sprint-plan-v1 "lavish review posted: <url>"` when the review goes up
- `/Users/moses/code/bin/ledger set packet-plumber-sprint-plan-v1 in-review "PR <url>"` when the PR opens (after approval)
- `herdr notification show "packet-plumber-sprint-plan-v1" --body "<one-line>"` on finish
- Final message: summary, sprint-plan path, lavish URL, story count (MVP vs full-game), confirmation the demand-pairing data is defined, open questions.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-sprint-plan-v1
- base: main
