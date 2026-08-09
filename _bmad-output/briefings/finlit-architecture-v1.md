# Briefing: finlit-architecture-v1

- **Repo:** kids-finlit-game (`/Users/moses/code/kids-finlit-game`, remote: solarity-services/finlit)
- **Worktree:** this pane's cwd (`finlit-architecture-v1` worktree, branch `finlit-architecture-v1`, base `origin/main`)
- **Skills policy:** workflow = **gds-generate-project-context** (deliverable 1) then **gds-game-architecture** (deliverable 2) — follow their step files; orchestration overrides per standing orders (genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Self-review before lavish: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter** (docs lens: GDD-consistency, contradictions, buildability), max 10 panes, badge out all.
- **Model policy:** unset — pi default (you and any mega-minions).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** off (docs deliverable).

## Mission

Two sequential deliverables, GREENFIELD doctrine per user ruling 2026-08-03: **the Godot slice in `game/` was "just a prototype" — a spike. It is evidence, never a constraint.** The GDD + brief govern; you design fresh.

**Deliverable 1 — `project-context.md`** (repo root, per the BMGD Godot setup guide: the single source of truth all later agents read): project name/description, target platforms (portrait 720×1280 mobile-first, desktop resizable), engine (Godot 4.7, GDScript — confirm from `game/project.godot`), renderer choice, performance budgets (60fps), critical technical decisions.

**Deliverable 2 — `_bmad-output/planning-artifacts/architecture-finlit-street-v1-<date>.md`** via gds-game-architecture's full structure: project structure (scenes/scripts/resources per the BMGD Godot layout), autoload singletons (game state, save — minimal per doctrine), scene composition + signal patterns, **the economy engine** (tick model, 60s cadence, seeded provably-fair event decks — the GDD's ranked-play requirement), **`ISaveBackend` interface** (local-first; thin Go/Postgres server drops in later as a one-class swap — locked in the prototype spec), data model for assets/trust/seasons/legacy, age-bracket adaptation plumbing, COPPA-compliant architecture constraints (no social surface; server-mediated anonymous market as the ONLY networked play; age-signal API integration points), export configurations, and testing strategy (GUT per BMGD recommendation — the prototype's `game/tests/` is spike evidence for what worked).

**Sources (in order):** `_bmad-output/planning-artifacts/gdd-finlit-street-v1-2026-08-01.md` (GOVERNS — incl. the approved N27 + your 13 baked rulings), `_bmad-output/planning-artifacts/briefs/brief-FinLit-2026-07-31/` (brief + addendum, locked MoSCoW), `_bmad-output/implementation-artifacts/spec-quick-prototype-finlit-street.md` (spike spec — mining for proven decisions only), `game/` (spike code — what worked: two-door doctrine, economy rebalance; what to redesign freely).

Every element traceable: GDD-locked vs NEW architecture proposal (mark NEW clearly — the user reviews those hardest). Flag anything where the GDD is silent and you're inventing (candidate ruling questions).

## Review loop (lavish — BEFORE the PR opens)

DOCS deliverables: when both docs are drafted + self-reviewed, render via the **lavish** skill (`lavish-axi`, one session covering both — context first, architecture second) and post the review URL in your final message. Do NOT open the PR until the user's verdict comes back through Gru/Silas. Clarify questions go through lavish too when practical.

## Acceptance

- `project-context.md` at repo root + architecture doc in planning-artifacts; GDD-traceable throughout; NEW proposals indexed; lavish URL delivered; zero unresolved self-review findings (or each explicitly deferred with reason).
- After user approval: commit on `finlit-architecture-v1`, push, `gh pr create --base main` titled "docs: FinLit Street project-context + game architecture v1" with NEW-vs-locked summary. **Never merge.**

## Env/bootstrap

Standard bootstrap applied (`_bmad` copied — gds module config is in this repo's `_bmad/gds`). The Godot project in `game/` needs no running; read it as evidence.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set finlit-architecture-v1 working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger note finlit-architecture-v1 "lavish review posted: <url>"` when the review goes up
- `/Users/moses/code/bin/ledger set finlit-architecture-v1 in-review "PR <url>"` when the PR opens (after approval), and `/Users/moses/code/bin/ledger pr finlit-architecture-v1 <url>`
- On blocked/finished: `herdr notification show "finlit-architecture-v1" --body "<one-line>"`
- Final message: summary, both doc paths, lavish URL, NEW-proposals list, candidate ruling questions, open questions.

## Dispatch parameters

- repo: kids-finlit-game
- repo_root: /Users/moses/code/kids-finlit-game
- slug: finlit-architecture-v1
- base: main
