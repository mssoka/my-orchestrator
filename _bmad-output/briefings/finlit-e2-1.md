# Briefing: finlit-e2-1-playtest-protocol

- **Repo:** kids-finlit-game (`/Users/moses/code/kids-finlit-game`, remote: solarity-services/finlit)
- **Worktree:** this pane's cwd (`finlit-e2-1` worktree, branch `finlit-e2-1`, base `origin/main`)
- **Skills policy:** workflow = **gds-create-story** then **gds-dev-story** (create the story file from the sprint plan, then implement it; orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Review pass before PR: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** `glm-5.2` (kimi walled until 08-08T21:57Z; vision not required for this story — it's protocol/doc + tooling).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** `pr_review: true`.

## Mission

Ship **Story e2-1: Playtest Protocol** (Epic E2, first-to-dispatch per the sprint plan).

**Sources (in order):**
1. `_bmad-output/implementation-artifacts/sprint-status-finlit-v1.yaml` — the tracker; find story e2-1's spec row (acceptance criteria, dependencies, sizing).
2. `_bmad-output/planning-artifacts/sprint-plan-finlit-v1-*.md` — the full story breakdown; read e2-1's section in detail.
3. `_bmad-output/planning-artifacts/gdd-finlit-street-v1-2026-08-01.md` — design context (the playtest doctrine: design anchor is Moses's 9-year-old; sessions of 5–10 min; "every pixel must react").
4. `project-context.md` — technical ground truth (Godot 4.7.1, GDScript, 720×1280 portrait).
5. `docs/playtest-script.md` — if a playtest script already exists in the repo, mine it; don't duplicate.

**What this story produces:** the playtest protocol — how to run a structured playtest session with the target audience (kids 8+). Likely deliverables: a playtest script/checklist (what to observe, what to ask, what metrics to capture), a capture setup (the existing `tools/capture.gd` rig for screenshots/recording), and any Godot tooling that supports playtesting (a debug overlay, a playtest-mode flag, a feedback-capture mechanism).

**GREENFIELD doctrine:** the `game/` slice is spike evidence — mine it for proven tooling (the capture rig) but design the protocol fresh per the GDD's playtest doctrine.

## Vision note

This story does NOT require visual evaluation — it's protocol + tooling + docs. Write the code, run the tests (GUT headless), assert behavior programmatically. Visual checkpoints are the user's (design anchor).

## Acceptance

- Story file created at `_bmad-output/implementation-artifacts/stories/e2-1-<slug>.md` per the `gds-create-story` format.
- Implementation complete: playtest script + capture tooling + any debug/playtest-mode code; GUT tests green; `make test` / Godot test run clean.
- Commit on `finlit-e2-1`, push, `gh pr create --base main` titled "feat: e2-1 playtest protocol + capture tooling" with **Decisions & rationale**. **Never merge.**

## Env/bootstrap

Standard bootstrap applied (`_bmad` copied — gds module config in-repo). Godot 4.7.1 installed at `/opt/homebrew/bin/godot`.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set finlit-e2-1 working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set finlit-e2-1 in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr finlit-e2-1 <url>`
- On blocked/finished: `herdr notification show "finlit-e2-1" --body "<one-line>"`
- Final message: summary, files changed, PR URL, story path, open questions.

## Dispatch parameters

- repo: kids-finlit-game
- repo_root: /Users/moses/code/kids-finlit-game
- slug: finlit-e2-1
- base: main
- pr_review: true
