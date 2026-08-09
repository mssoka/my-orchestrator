# Briefing: packet-plumber-gdd-v1

- **Repo:** Packet-Plumber (`/Users/moses/code/packet-plumber`, remote: `solarity-services/Packet-Plumber`)
- **Worktree:** work directly in the repo root (local repo, no worktree needed — this IS the repo; PR targets main)
- **Workflow:** **gds-gdd** — read the skill's step file at `/Users/moses/code/.agents/skills/gds-gdd/SKILL.md` and follow it. The GDD is the design bible; the brief + forge output are the input. **Do NOT re-decide anything the forge locked** — expand the locked decisions into full design detail. Orchestration overrides per standing orders (genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Self-review before PR: bmad-review-adversarial-general / bmad-review-edge-case-hunter, max 10 panes, badge out all.
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** OFF (docs deliverable).

## Mission

Produce the official BMGD Game Design Document for Packet Plumber — the canonical design reference every later agent (architecture, sprint plan, prototype build) reads. This is Step 5 of the BMGD Godot setup flow.

## Source material (read ALL in full before writing)

1. **`project-context.md`** (repo root) — technical ground truth (Godot 4.7.1, landscape 1280×720, gl_compatibility, cross-platform doctrine)
2. **`_bmad-output/planning-artifacts/briefs/brief-Packet-Plumber-2026-08-05/brief.md`** — the official game brief (executive summary, vision, core loop, pillars, MoSCoW, differentiators, go-to-market). THIS IS YOUR PRIMARY INPUT.
3. **`_bmad-output/planning-artifacts/forge-packet-plumber-2026-08-05/forged-idea.md`** — the forge output (8 locked decisions, 6 rejections, 4 surviving weak points, MVP scope). The full provenance behind every brief decision.
4. **`/Users/moses/code/docs/game-design-references.md`** — the Tyroller + Brush design references that shaped the pillars (experience-first, juice lenses, custom audio).

## GDD scope — what to design in detail

The forge locked the high-level decisions. The GDD's job is to make them BUILDABLE. Expand each into full design specification:

### Core systems to design
- **🎮 Core loop** — the moment-to-moment cycle (assess topology → draw/upgrade pipes → designate priority → packets flow → predict crisis → react). Specify the player's decision space at each step.
- **📦 Packet types + QoS** — the full roster across eras (email, web, streaming, gaming, banking, multicast, AI...). For each: latency tolerance, loss tolerance, bandwidth demand. How does the player designate priority lanes? What's the trade-off (a high-priority lane steals bandwidth from others)?
- **🕰️ Era progression** — the full historical arc. Specify each era: what packet types appear, what infrastructure is available, what becomes obsolete, what the era-transition trigger is. The forge locked "era progression + infrastructure lifecycle" as a differentiator — design the UPGRADE lifecycle (old pipes degrade, must be modernized, can't just be ignored).
- **🚨 Crisis model** — the predictable/fair disaster system. Specify the warning signs (node 🟡 strained → 🔴 critical), escalation curves, the failure modes (pipe burst, node overload, bandwidth saturation). The forge locked "I should have seen this coming" — every crisis must be a DESIGN CONSEQUENCE the player could have prevented, never random. Specify 3-5 concrete crisis archetypes.
- **📈 Progression + economy** — what unlocks when (eras, packet types, map expansion, tools). Is there currency? Contracts? Score? What's the win/lose condition per level and per era?

### Content to specify
- **🗺️ Maps/topology** — how nodes are laid out, how maps grow, how the player expands (Mini Motorways-style: city grows over time).
- **🔢 Numerical design** — rough tuning targets (pipe capacities, packet spawn rates, crisis thresholds, era duration). Ballpark figures the prototype can start from; precise balance is a later iteration.
- **🎨 Visual direction** — the Mini Motorways aesthetic spec (palette, pipe rendering, packet visualization, node states, UI chrome). Landscape 1280×720.
- **🔊 Audio direction** — custom/original exclusively (no stock licenses — streamer monetization rule from project-context). Ambient + reactive SFX per the Thomas Brush juice lens.
- **♿ Accessibility** — colorblind-safe palette, scaling, input alternatives (the forge locked Steam + mobile + controller).

### Must include
- **🧪 MVP prototype scope** — carve out the email→streaming prototype slice as a dedicated section (the forge scoped it: one era transition, two packet types, 4-6 nodes, draw+upgrade+prioritize, survive the surge). The GDD must make clear what the prototype tests vs what's full-game.
- **⚠️ The 4 surviving weak points** from the forge — address each in the GDD: (1) the fun question is unproven (prototype answers it), (2) the plumbing metaphor's limits at VPN/VLAN/SDN layers, (3) the engineer/non-engineer audience balance, (4) the V2 AI stress-test system scope.

### Document placement
- GDD at `_bmad-output/planning-artifacts/gdd/gdd-v1.md` (follow the gds-gdd skill's structure — typically: game overview, pillars, core loop, mechanics, content/progression, visual/audio, accessibility, MVP scope, risks/open questions).

## Constraints (do not violate — forge-locked)

- Experience-first: "save the internet" is the pitch. Mechanics serve the experience.
- Core mechanic = Draw (A) + React (C). NOT Factorio construction (B was rejected).
- Crises are FAIR and PREDICTABLE — design consequences, never random.
- Two differentiators: (1) packet types + QoS lanes, (2) era progression + infrastructure lifecycle.
- Visual: Mini Motorways style (2D/isometric, clean, readable).
- Cross-platform: same game on Steam (controller + mouse) + mobile (touch).
- Go-to-market: free prototype → playtest → Steam page → full launch. NO early access.
- Audio: custom/original exclusively.
- Landscape 1280×720 (user ruling from setup phase).
- Satirical brand names (YouTune, Amazoom) — never real trademarks.

## Review loop (lavish — BEFORE the PR opens)

DOCS deliverable: when drafted + self-reviewed, render via the **lavish** skill and post the review URL. Do NOT open the PR until the user's verdict. The GDD is large and visual (eras, packet types, crisis model) — a rich lavish render is expected.

## Acceptance

- GDD at `_bmad-output/planning-artifacts/gdd/gdd-v1.md` following the gds-gdd skill structure.
- Every forge-locked decision expanded into buildable detail (no contradictions).
- MVP prototype scope clearly carved out.
- The 4 surviving weak points addressed.
- Numerical ballpark tuning targets included (prototype-starting values).
- After user approval: commit, push, open PR targeting main. **Never merge.**

## Env/bootstrap

This IS the repo — no worktree, no bootstrap copy. BMad + GDS module installed in `_bmad/`. Godot 4.7.1 at `/opt/homebrew/bin/godot`.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set packet-plumber-gdd-v1 working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger note packet-plumber-gdd-v1 "lavish review posted: <url>"` when the review goes up
- `/Users/moses/code/bin/ledger set packet-plumber-gdd-v1 in-review "PR <url>"` when the PR opens (after approval)
- `herdr notification show "packet-plumber-gdd-v1" --body "<one-line>"` on finish
- Final message: summary, GDD path, lavish URL, open questions, the era/packet-type count.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-gdd-v1
- base: main
