# Briefing: packet-plumber-setup-brief

- **Repo:** packet-plumber (`/Users/moses/code/packet-plumber`, no remote yet — local repo)
- **Worktree:** this pane's cwd (work directly in the repo root — no worktree needed, this IS the repo)
- **Skills policy:** workflow = **gds-generate-project-context** then **gds-create-game-brief** (follow their step files; orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Self-review before PR: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** off (docs deliverable).

## Mission

Three sequential deliverables — Steps 1, 2, and 4 of the BMGD Godot setup flow. Steps 3 (brainstorm) is ALREADY DONE — the forge output IS the brainstorm.

**Source material (read in full — these contain every design decision, locked by the user through a structured forge session):**
1. `_bmad-output/planning-artifacts/packet-plumber-concept-2026-08-05.md` — the full concept document (experience, mechanics, visual style, market positioning, concerns)
2. `_bmad-output/planning-artifacts/forge-packet-plumber-2026-08-05/forged-idea.md` — the forge output (8 locked decisions, 6 rejections, MVP scope, go-to-market strategy)

### Deliverable 1: Godot project (Step 1)

Create the Godot project at `game/` in the repo root:
- Godot 4.7.1 (standard, non-.NET) — same as FinLit
- **Resolution:** this is a Mini Motorways-style top-down routing game for Steam + mobile. Determine the appropriate viewport/stretch/aspect settings from the concept doc (the forge locked: Mini Motorways visual style, cross-platform, draw-between-nodes input). The game needs to work in both portrait (mobile) and landscape (desktop) — set stretch mode `canvas_items`, aspect `expand`, same pattern as FinLit.
- Renderer: `gl_compatibility` (GLES3 — 2D game, cross-platform, runs on older phones)
- Basic directory structure per BMGD Godot conventions: `scenes/`, `scripts/`, `assets/`, `data/`, `tests/`, `themes/`
- A minimal main scene (just a placeholder — the prototype build comes later)

### Deliverable 2: project-context.md (Step 2)

Run `gds-generate-project-context` — create `project-context.md` at the repo root. This is the single source of truth all later agents read. Include: project name (Packet Plumber), description, target platforms (Steam PC/Mac + mobile iOS/Android), engine (Godot 4.7.1, GDScript), renderer, resolution/stretch settings, performance budgets (60fps), critical technical decisions from the forge (Mini Motorways visual style, draw-between-nodes input model, snap-to-node precision, cross-platform same-game doctrine).

### Deliverable 3: Official game brief (Step 4)

Run `gds-create-game-brief` — create the official BMGD-styled game brief at `_bmad-output/planning-artifacts/briefs/brief-Packet-Plumber-2026-08-05/brief.md`. **Do NOT brainstorm new content — the forge already produced every design decision.** Your job is to FORMAT the forge output into the official brief structure:
- Executive summary (the experience: "Save the internet")
- Vision / elevator pitch
- Target players (network engineers + non-engineers + the Nintendo-model adult audience)
- Market context (Mini Metro / Factorio / Two Point Hospital gap)
- Core loop (draw pipes → packets flow → predict crises → upgrade → survive the surge)
- Pillars (routing puzzle satisfaction, packet-type trade-offs, era-progression modernization pressure)
- Primary mechanics (draw-between-nodes, QoS priority lanes, infrastructure upgrade lifecycle, era progression)
- MoSCoW board (MVP scope from the forge = Must; full-era progression, AI disasters, contracts = Should/Could)
- Differentiators (packet types + QoS, era progression + upgrade lifecycle)
- Go-to-market strategy (free prototype → playtest → Steam page → full launch)

## Review loop (lavish — BEFORE the PR opens)

DOCS deliverables: when drafted + self-reviewed, render via the **lavish** skill and post the review URL. Do NOT open the PR until the user's verdict.

## Acceptance

- Godot project at `game/` with correct settings (parse-tested: `godot --path game --check-only` or equivalent)
- `project-context.md` at repo root
- Official game brief at `_bmad-output/planning-artifacts/briefs/`
- All three consistent with the forge output (no contradictions with locked decisions)
- After user approval: commit, push (create a GitHub remote if none exists — ask Gru), open PR. **Never merge.**

## Env/bootstrap

This IS the repo — no worktree, no bootstrap copy needed. BMad + GDS module already installed in `_bmad/`. Godot 4.7.1 at `/opt/homebrew/bin/godot`.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set packet-plumber-setup-brief working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger note packet-plumber-setup-brief "lavish review posted: <url>"` when the review goes up
- `/Users/moses/code/bin/ledger set packet-plumber-setup-brief in-review "PR <url>"` when the PR opens (after approval)
- `herdr notification show "packet-plumber-setup-brief" --body "<one-line>"` on finish
- Final message: summary, all three deliverable paths, lavish URL, open questions.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-setup-brief
- base: main (local repo — no remote yet)
