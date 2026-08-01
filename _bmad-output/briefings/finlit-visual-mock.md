# Briefing: finlit-visual-mock

- **Repo:** kids-finlit-game (`/Users/moses/code/kids-finlit-game`, remote: `git@github.com:solarity-services/finlit.git`)
- **Worktree:** this pane's cwd (`visual-mock-street` worktree, branch `visual-mock-street`, base `origin/main`)
- **Skills policy:** workflow = **gds-quick-dev** (follow its step files; orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Review pass before PR: **gds-code-review** or **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default (you and any mega-minions).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start (Godot/headless lessons inside); badge-out shard per standing orders.

## Mission

Produce a **visual mock**: reskin the prototype's street scene with REAL art direction — palette, styled components, motion juice — as a before/after comparison so Moses can judge what Godot can do for this game WITHOUT switching engines. **Presentation layer only: zero game-logic changes.**

## Direction (kids, 8–12; Monopoly GO!-adjacent pop)

- **Palette:** bright, warm, optimistic — define a small named palette (sky/cream/bg, primary amber, street green, money gold, alert red) and apply it as theme resources, not per-node hardcoding where avoidable.
- **Shapes/type:** rounded panels, big readable type, chunky touch targets (the game is kid-mobile-first); keep the emoji vocabulary but make it feel intentional (styled chips/badges, not raw text).
- **Juice (the important part):** tweened motion — wage tick bounce on the money chip, coin particle burst on income, squash-and-stretch on BUY, a subtle idle pulse on available plots, era banner entrance. Cheap Godot tweens/particles; tasteful, not seizure-confetti.
- **Assets:** procedural styling first (StyleBoxFlat, custom draws, emoji badges); Kenney.nl CC0 packs are ALLOWED with attribution if they materially help (kids-friendly) — commit what you use with a note; no other external art.

## Hard constraints (collision discipline)

- **ZERO logic changes**: no edits to tick/event/economy/save/LLM logic. Another minion (`finlit-bugfix-event-messages`, branch `bugfix-event-messages`, IN FLIGHT) owns `street.gd` logic + the top-bar contrast fix — if your styling touches the same label nodes, expect a small merge dance; confine logic-file edits to the minimum (prefer theme/scene/CSS-of-Godot: `.tscn`, `Theme` resources, NEW polish scripts e.g. `scripts/juice.gd` that nodes opt into).
- The bugfix's top-bar contrast fix may land before you — CHECK `git log origin/main` and, if merged, rebase your styling on it rather than redoing it.
- 163-test offline suite must stay green; headless import + run clean.

## Evidence (the seeing loop — mandatory)

- Reuse/build the headless capture rig: boot `scenes/street.tscn`, advance a few ticks, save PNGs. Capture **BEFORE** (current main) and **AFTER** (your reskin) at the same states (fresh start, after first wage, after BUY, event card showing, tutor beat).
- READ your captures yourself and iterate until the after-set is unmistakably more exciting — this is the deliverable's proof.
- Put the before/after pairs in the PR description (commit a small `docs/visual-mock/` set — PNGs under ~300KB each, README.md index) so Moses can judge without running anything. Also include a short "how to run the mock" note.

## Acceptance

- Before/after capture pairs committed to `docs/visual-mock/` + PR description; palette named and themed; at least 4 distinct juice moments; suite green; zero logic diffs (`git diff --stat` shows scenes/themes/new polish scripts only).
- Commit on `visual-mock-street`, push, `gh pr create --base main` titled "feat: visual mock — styled street reskin (palette + juice, no logic changes)" with **Decisions & rationale**. **Never merge.**

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set finlit-visual-mock working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set finlit-visual-mock in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr finlit-visual-mock <url>`
- On blocked/finished: `herdr notification show "finlit-visual-mock" --body "<one-line>"`
- Final message: summary, before/after capture list, PR URL, suite evidence, open questions.
