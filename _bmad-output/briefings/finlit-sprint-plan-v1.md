# Briefing: finlit-sprint-plan-v1

- **Repo:** kids-finlit-game (`/Users/moses/code/kids-finlit-game`, remote: solarity-services/finlit)
- **Worktree:** this pane's cwd (`finlit-sprint-plan-v1` worktree, branch `finlit-sprint-plan-v1`, base `origin/main`)
- **Skills policy:** workflow = **gds-sprint-planning** (follow its step files; orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Self-review before lavish: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter** (docs lens: GDD/arch traceability, story sizing, dependency sanity), max 10 panes, badge out all.
- **Model policy:** unset — pi default (you and any mega-minions).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** off (docs deliverable).

## Mission

Generate the **sprint plan for FinLit Street v1** — `sprint-status.yaml` + the epics/stories breakdown, per the BMGD Godot setup flow's Step 7 (Game Scrum Master): stories from the GDD + architecture, sprint goals, definition of done, dependency-ordered.

**Sources (in order):**

1. `project-context.md` (repo root — governs technical ground truth)
2. `_bmad-output/planning-artifacts/architecture-finlit-street-v1-*.md` (system design; NEW-vs-locked register incl. the A29 minute-one cluster tagged pending-confirmation — stories touching A29 must note it)
3. `_bmad-output/planning-artifacts/gdd-finlit-street-v1-2026-08-01.md` (design; locked MoSCoW Must-board = the v1 scope)
4. `_bmad-output/planning-artifacts/juice-checklist-game-feel-2026-08-03.md` (the art/audio pass lens — juice/audio stories should exist, not be implied)
5. GREENFIELD doctrine (user ruling): the `game/` slice is spike evidence; stories build fresh per the architecture, mining the spike only for proven decisions (two-door doctrine, economy tuning baseline)

**Requirements:**

- `sprint-status.yaml` at `_bmad-output/implementation-artifacts/sprint-status-finlit-v1.yaml` — statuses, dependency notes, dispatch order (mirror the refcheck tracker's format: it works; see RightTenantry's `sprint-status-refcheck-v1.yaml` if accessible, else the gds template).
- Epic/story list in the plan doc (`_bmad-output/planning-artifacts/sprint-plan-finlit-v1-<date>.md`): each story = title, intent, acceptance criteria sketch, dependency, rough size — enough for later `gds-create-story` runs.
- Sequencing must respect the architecture's phases and flag any external gates early (e.g. age-signal store APIs, server provisioning — the Rust/Axum path is ruled but phases it per the arch doc).
- Scope honesty: v1 = the MoSCoW Must board + the architecture's v1 scope line (supply chains IN, insurance/farm-weather v1.1, parent-goals droppable stretch). Deferred items go to a backlog section, not stories.

## Review loop (lavish — BEFORE the PR opens)

DOCS deliverable: when drafted + self-reviewed, render via the **lavish** skill and post the review URL in your final message. Do NOT open the PR until the user's verdict comes back through Gru/Silas. Clarify questions go through lavish too when practical.

## Acceptance

- sprint-status.yaml + sprint-plan doc complete; every story traceable to GDD/arch sections; dependency order coherent; lavish URL delivered.
- After user approval: commit on `finlit-sprint-plan-v1`, push, `gh pr create --base main` titled "docs: FinLit Street sprint plan v1 (epics + stories + tracker)" — **never merge**.

## Env/bootstrap

Standard bootstrap applied (`_bmad` copied — gds module config in-repo). Godot project in `game/` needs no running.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set finlit-sprint-plan-v1 working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger note finlit-sprint-plan-v1 "lavish review posted: <url>"` when the review goes up
- `/Users/moses/code/bin/ledger set finlit-sprint-plan-v1 in-review "PR <url>"` when the PR opens (after approval), and `/Users/moses/code/bin/ledger pr finlit-sprint-plan-v1 <url>`
- On blocked/finished: `herdr notification show "finlit-sprint-plan-v1" --body "<one-line>"`
- Final message: summary, both doc paths, lavish URL, epic/story counts, external gates flagged, open questions.

## Dispatch parameters

- repo: kids-finlit-game
- repo_root: /Users/moses/code/kids-finlit-game
- slug: finlit-sprint-plan-v1
- base: main
