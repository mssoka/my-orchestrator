# Briefing: finlit-game-brief

- **Repo:** kids-finlit-game (`/Users/moses/code/kids-finlit-game`, remote: `git@github.com:solarity-services/finlit.git`)
- **Worktree:** this pane's cwd (`game-brief` worktree, branch `game-brief`, base `origin/main`)
- **Skills policy:** workflow = **gds-create-game-brief** (follow its step files; orchestration overrides per standing orders — step-01 clarify: ask numbered questions then HALT for Gru relay; internal approval checkpoints pre-approved). Review pass (optional): **bmad-review-adversarial-general**, max 10 panes, badge out all.
- **Model policy:** unset — pi default (you and any mega-minions).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.

## Mission

Produce the **game brief** for the kids' financial-literacy game (working repo name `finlit`; the game names itself later — do NOT invent a final name), following the gds-create-game-brief skill's output conventions and path.

## Required reading (the brainstorm is COMPLETE and locked — treat it as canon)

All under `_bmad-output/brainstorming/brainstorm-kids-financial-literacy-game-2026-07-27/` in this repo:

1. **`brainstorm-intent.md`** — THE key input: the locked concept, built to feed this brief. Follow it.
2. `.memlog.md` — the sealed 75+ entry session record (decisions, evidence, receipts)
3. `pitch-one-pager.md` — co-founder/publisher framing
4. `build-task-list.md` — phased build plan (prototype → playtest → backend → market → launch)
5. `research-market-kids-money-games-2026-07-27.md`, `research-technical-game-stack-2026-07-27.md`, `synthesis-market-and-stack-2026-07-27.md`
6. `_bmad-output/implementation-artifacts/spec-quick-prototype-finlit-street.md` — the ready-for-dev prototype spec (Quick Flow)

## Canon — locked, do not re-litigate (challenge only via numbered clarify questions)

- Locked concept: *"a life you earn, a street you build, a kid who grows — money learned by living it"*
- Zero-start life sim · life lottery · two doors (wages + OPM) · trust-meter spine · street-as-canvas
- **Four-layer reset model** (2026-07-29 amendment, replaces street-retires): L1 street never resets · L2 race/ladder resets · L3 New Life is a choice (heir inherits) · L4 world events reprice, never wipe
- **Anonymous loan/asset market** (server-mediated order book, NPC liquidity bootstrap, COPPA-safe)
- **Age-adaptive AI tutor** (8–10/11–12/13–15; scripted `tutor.gd` seam now, LLM Ask First) · AI = tutor, never referee
- Honest-brutal (no rubber-banding) · premium + world-DLC model · compliance floor (KWS, neutral age screen, fantasy names, parent dashboard) · Godot 4.7 Stack A
- MoSCoW board confirmed by Moses (see memlog entries ~67–79)

## Constraints

- The brief must be **prototype-anchored**: the Quick Flow prototype slice is the near-term build; the brief's scope section should reflect prototype-first phasing, not the full dream.
- Note open questions explicitly (reroll policy, no-parents tone, LLM tutor integration timing) rather than silently resolving them.
- Audience: Moses (solo founder) — the brief is the alignment doc before GDD (gds-gdd) and the prototype build.

## Acceptance

- Game brief artifact at the skill's conventional path; covers vision/pillars/audience/scope (prototype-first)/compliance posture/business model; canon respected; open questions numbered.
- Commit on `game-brief`, `git push -u origin game-brief`, `gh pr create --base main` titled "docs: game brief — finlit street (from locked brainstorm)" with a **Decisions & rationale** section. **Never merge.**

## Env/bootstrap

Standard bootstrap applied (`_bmad` present incl. gds module; no env files in this repo). Docs task — do NOT run builds or tests.

## Verify

Artifact exists at the skill's path; markdown renders; internal links resolve; `git diff --stat` shows only the new artifact.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set finlit-game-brief working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set finlit-game-brief in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr finlit-game-brief <url>`
- On blocked/finished: `herdr notification show "finlit-game-brief" --body "<one-line>"`
- Final message: summary, files changed, PR URL, open questions.
