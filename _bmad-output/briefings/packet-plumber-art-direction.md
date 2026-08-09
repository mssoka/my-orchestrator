# Briefing: packet-plumber-art-direction

- **Repo:** Packet-Plumber (`/Users/moses/code/packet-plumber`, remote: `solarity-services/Packet-Plumber`)
- **Worktree:** work directly in the repo root on a feature branch off `main` (PR targets main)
- **Workflow:** **gds-agent-game-designer** (Samus Shepard — creative vision) + **gds-ux** for UI/HUD specifics. This is an ART-DIRECTION deliverable — propose the visual identity; the user reacts via lavish. Orchestration overrides per standing orders (genuine blockers: numbered questions then HALT; internal checkpoints pre-approved). Self-review before PR: bmad-review-edge-case-hunter.
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** OFF (creative/docs deliverable).

## Mission

Produce the **art-direction spec** for Packet Plumber — the visual identity that makes the "save the internet" fantasy *felt* and distinguishes Packet Plumber from its Mini Motorways baseline. This runs IN PARALLEL with the prototype fun-test (it doesn't block it) and feeds both the prototype's presentation polish AND the full game's identity.

## Source material (read ALL)

1. **`_bmad-output/planning-artifacts/forge-packet-plumber-2026-08-05/forged-idea.md`** — visual locked: **Mini Motorways style** (clean, minimalist, top-down, 2D/isometric, readable at a glance on phone + monitor). The forge's experience-first thesis.
2. **`_bmad-output/planning-artifacts/gdds/.../gdd.md`** — the visual-direction section + the 9 packet types (each needs distinct visual identity), the 6 eras (visual evolution), the node health states (🟢🟡🔴), the crisis/juice moments.
3. **`_bmad-output/planning-artifacts/architecture/architecture-v1.md`** — the rendering constraints (gl_compatibility, landscape 1280×720, canvas_items/expand).
4. **`project-context.md`** — Godot 4.7.1, cross-platform same-game, 60fps, custom-audio-only.
5. **`/Users/moses/code/docs/game-design-references.md`** — the Thomas Brush juice lenses (color theory, reactive particles) + Tyroller (appeal/capsule design).

## What to design (the art-direction spec)

### 1. Color palette + system
- A **core palette** (the base canvas, the pipes, the nodes, the UI chrome) — colorblind-SAFE (avoid red/green-only encoding; use shape/value/hue triads).
- **Per-packet-type color identity** — the 9 packet types (email, streaming, gaming, banking, voice/video, multicast, IoT, AI...) each need a distinct, learnable color + visual treatment (the player reads "that's a streaming packet" instantly).
- **State colors** — node health (🟢🟡🔴), crisis escalation, era-transition cues.

### 2. Visual language
- **Pipes** — how they render (the "draw" feel — snap, glow, the flow pulse). Tier differentiation (copper → fiber, narrow → wide). Legacy/wear visual cues.
- **Packets** — the dots/units flowing (distinct per type, readable at speed, the "personality" the forge locked).
- **Nodes** — terminals (Residential, Content host, etc.) vs junctions (routers) — visually distinct, health-state legible.
- **The map** — the canvas, the topology, how it grows.

### 3. UI / HUD chrome
- The dashboard the player reads: Network Health meter, SLA gauges, the demand forecast ("weather report"), era indicator, crisis alerts. Minimalist, glanceable, cross-platform (touch + mouse + controller).

### 4. Era-visual-evolution
- The 6 eras should FEEL different visually (ARPANET's spareness → the streaming surge's density → the cloud era's scale → the SDN/edge abstraction). The visual evolves WITH the internet — a progression cue, not just content gating.

### 5. Juice / feedback visuals (per Thomas Brush)
- The reactive moments: packet-arrival bounce, leak spray, router blink, crisis-alert flash, the "surge survived" celebration. Every pixel reacts.

### 6. Accessibility
- Colorblind-safe palette (test with simulators), sufficient contrast, scalable UI, the visual encoding not relying on color alone.

## Deliverable + placement
- Art-direction spec at `_bmad-output/planning-artifacts/art-direction/art-direction-v1.md` (or per the skill's structure).
- Include **concrete color values** (hex), visual mockups described precisely (or ASCII/diagrams), and a **mood-board rationale** (why this palette/feel serves the "save the internet" fantasy).

## Constraints (do not violate — forge/GDD-locked)
- **Mini Motorways style**: clean, minimalist, top-down, readable. (Don't propose a cluttered/realistic aesthetic — the forge rejected heavy visuals.)
- **Colorblind-safe** (non-negotiable — broad audience + accessibility).
- **Cross-platform readable** (mobile screen + desktop monitor, same game).
- **Experience-first**: the visual serves the "save the internet" fantasy, not the other way around.
- No em-dashes in any copy (global ban).
- Satirical brand names only (YouTune, Amazoon, Glitch...) — never real trademarks.

## Review loop (lavish — BEFORE the PR)
Creative deliverable: render via **lavish** with the palette visualized (color swatches, the visual language, era-evolution) + post the review URL. The user reacts to the proposed identity. Do NOT open the PR until the verdict.

## Acceptance
- Art-direction spec with concrete palette (hex), per-packet-type visual identity, UI/HUD design, era-evolution, juice moments, accessibility.
- Colorblind-safe + cross-platform readable.
- After user approval: commit, push, open PR targeting main. **Never merge.**

## Self-report (do not skip)
- `/Users/moses/code/bin/ledger set packet-plumber-art-direction working` at start
- `/Users/moses/code/bin/ledger note packet-plumber-art-direction "lavish review posted: <url>"` when up
- `/Users/moses/code/bin/ledger set packet-plumber-art-direction in-review "PR <url>"` when PR opens
- `herdr notification show "pp-art-direction" --body "<one-line>"` on finish
- Final message: the palette + visual-language summary, lavish URL, open questions.

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: packet-plumber-art-direction · base: main
