# Briefing: kids-finlit-game-brainstorm

Standing orders: read `/Users/moses/code/docs/orchestration-playbook.md`
section "Minion standing orders" — with the overrides noted in this briefing.

## Task

Resume and facilitate the BMad brainstorming session already in progress for
Moses' kids' financial-literacy game. You are the facilitator — the session
was started by Gru and is handed to you mid-stream.

- **Resume state:** `_bmad-output/brainstorming/brainstorm-kids-financial-literacy-game-2026-07-27/.memlog.md`
  under your cwd (the worktree). Follow the bmad-brainstorming resume flow
  (`references/resume.md` in the skill).
- **Mode:** Creative Partner (user's choice). They generate the majority; you
  spark. Attribution (`--by user` / `--by coach`) is mandatory.
- **Batch already selected** (logged in the memlog): Job to Be Done →
  Persona Journey → Assumption Reversal → Trait Transfer →
  Kill the Crown Jewel. Technique 1 (JTBD) was posed but NOT answered —
  the pending question is in the memlog; re-ask it after resuming.
- **The user (Moses) talks to you DIRECTLY in your pane.** There is no Gru
  relay for this job — the quick-dev clarify-halt override does not apply;
  all questions go straight to him, conversationally.

## Acceptance

- Session resumed as Carson; the batch runs to completion (or the user
  steers elsewhere — his call, always).
- Memlog kept faithfully updated throughout.
- Wrap-up per bmad-brainstorming's finalize flow (synthesis artifact) when
  the user is spent.
- All artifacts committed on branch `brainstorm`.

## Repo map

- Brand-new project created for this idea.
  repo_root: `/Users/moses/code/kids-finlit-game` (git init'd, **no remote**
  — leave branches local, per standing orders).
- Your cwd: `/Users/moses/.herdr/worktrees/kids-finlit-game/brainstorm`
  on branch `brainstorm`.
- `_bmad` config is committed in the repo. `_bmad-output` is **tracked in
  this repo deliberately** — the brainstorm output IS the deliverable.
  Commit it.

## Env/bootstrap

None. No env files, no dependencies.

## Verify

- Memlog exists and grows; final synthesis file lands in the brainstorm
  workspace; `git log` on `brainstorm` shows the artifacts committed.

## Model policy

You: pi default. Mega-minions (if any): pi default.

## Skills policy

- **Your workflow:** adopt `bmad-cis-agent-brainstorming-coach` (Carson
  persona), running `bmad-brainstorming` for the session itself (resume
  flow). Greet Moses as Carson and pick up exactly where the memlog leaves
  off.
- **Likely follow-ups when the user asks** (name them before using):
  `bmad-technical-research` (stack/platform/engine options),
  `bmad-market-research` (competitors: Prodigy, Roblox, Greenlight, etc.),
  `bmad-product-brief` (once the idea firms up).
- Mega-minions: not expected; if you spawn any for research, max 10
  concurrent, and close every one before finishing.

## Completion

When the user declares the session done (or you wrap it): commit everything
on `brainstorm`, run
`herdr notification show "kids-finlit-game-brainstorm" --body "<one-line status>"`,
and report transitions to the ledger as they happen:
`/Users/moses/code/bin/ledger set kids-finlit-game-brainstorm <status> "<note>"`
(set `working` when you resume; leave `done` to Gru). End your final message
with: summary, artifacts produced, confirmation everything is committed.
