# Briefing: finlit-e2-7-touch-target-rules

- **Repo:** kids-finlit-game (`/Users/moses/code/kids-finlit-game`, remote: solarity-services/finlit)
- **Worktree:** this pane's cwd (`finlit-e2-7` worktree, branch `finlit-e2-7`, base `origin/main`)
- **Skills policy:** workflow = **gds-create-story** then **gds-dev-story** (create the story file from the sprint plan, then implement it; orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Review pass before PR: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** `glm-5.2` (kimi walled until 08-08T21:57Z; vision not required for this story — sizing rules are programmatic assertions, not visual evaluation).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** `pr_review: true`.

## Mission

Ship **Story e2-7: Touch-Target Rules (A29 minute-one working rules)** (Epic E2, first-to-dispatch per the sprint plan).

**Sources (in order):**
1. `_bmad-output/implementation-artifacts/sprint-status-finlit-v1.yaml` — the tracker; find story e2-7's spec row.
2. `_bmad-output/planning-artifacts/sprint-plan-finlit-v1-*.md` — the full story breakdown; read e2-7's section.
3. `_bmad-output/planning-artifacts/gdd-finlit-street-v1-2026-08-01.md` — the GDD's §Minute-one + the A29 proposals (FIND WORK collision prefix, oldest-damaged-first FIX tie-break, modal-card button interplay, ≥160px/120px touch proxy — these are the A29 rules tagged pending-confirmation; the user hasn't explicitly ruled on A29 yet, so IMPLEMENT them as proposed and flag in the PR for the user's ack).
4. `_bmad-output/planning-artifacts/architecture-finlit-street-v1-*.md` — the architecture's input/touch section (touch + mouse parity; portrait-locked handheld).
5. `project-context.md` — Godot 4.7.1, 720×1280 portrait, gl_compatibility.

**What this story produces:** the touch-target system — the rules that govern how the game's dominant bottom-center action button, modal cards, and step-progress UI behave on touch: minimum sizes (≥160px primary / ≥120px secondary per A29), the FIND WORK prefix collision rule, the FIX tie-break (oldest-damaged-first), modal-card button interplay, and the touch-proxy (invisible enlarged hit areas around small targets). Implemented as GDScript (a touch-target manager/autoload or a theme/constants file) + GUT tests asserting the sizing rules programmatically.

**A29 note:** these rules were tagged `pending-confirmation` in the architecture. Implement as proposed; the PR body must explicitly ask the user to confirm A29 — if any rule is wrong, it's a one-line constant change.

## Vision note

This story does NOT require visual evaluation — the touch-target rules are sizing constants and programmatic assertions (`assert button.size >= Vector2(160, 160)`). A blind model can fully implement and test this. The user does the visual checkpoint ("does 160px feel right on a phone?") — which is the design-anchor's job anyway.

## Acceptance

- Story file created at `_bmad-output/implementation-artifacts/stories/e2-7-<slug>.md` per the `gds-create-story` format.
- Implementation complete: touch-target constants/manager + GUT tests asserting every A29 rule; `make test` / Godot test run clean.
- Commit on `finlit-e2-7`, push, `gh pr create --base main` titled "feat: e2-7 touch-target rules (A29 minute-one working rules)" with **Decisions & rationale** + the A29 confirmation ask. **Never merge.**

## Env/bootstrap

Standard bootstrap applied (`_bmad` copied — gds module config in-repo). Godot 4.7.1 at `/opt/homebrew/bin/godot`.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set finlit-e2-7 working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set finlit-e2-7 in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr finlit-e2-7 <url>`
- On blocked/finished: `herdr notification show "finlit-e2-7" --body "<one-line>"`
- Final message: summary, files changed, PR URL, story path, A29 confirmation ask, open questions.

## Dispatch parameters

- repo: kids-finlit-game
- repo_root: /Users/moses/code/kids-finlit-game
- slug: finlit-e2-7
- base: main
- pr_review: true
