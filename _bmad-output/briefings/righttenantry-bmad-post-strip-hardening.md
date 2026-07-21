# Briefing: righttenantry-bmad-post-strip-hardening

- **Repo:** /Users/moses/code/RightTenantry
- **Worktree (your cwd):** /Users/moses/.herdr/worktrees/RightTenantry/bmad-post-strip-hardening
- **Branch:** `bmad-post-strip-hardening` → PR targets **`develop`**
- **Base:** `develop`

## Standing orders

Read `/Users/moses/code/docs/orchestration-playbook.md` section **"Minion standing orders"** and follow it exactly. Use the **bmad-quick-dev** skill; step-01 clarify = HALT and wait for relayed answers; internal approval checkpoints are pre-approved. Self-report every status transition: `/Users/moses/code/bin/ledger set righttenantry-bmad-post-strip-hardening <status> "<note>"`. When blocked or finished: `herdr notification show "righttenantry-bmad-post-strip-hardening" --body "<one-line status>"`. Never merge the PR.

## Context (why — user decisions 2026-07-21)

Follow-up to strip PR #541 (`.agents/skills/bmad-*` removal, pending merge — your branch is disjoint from it: you touch `.claude/skills`, not `.agents/skills`). User decisions:

1. **pi is the only agent harness going forward** — Claude Code is retired for this repo; its per-repo bmad skill copies get removed too.
2. **The bmad loop is retired** ("we don't need the loop now that Gru orchestrates") — `bmad-loop-*` skills are NOT preserved anywhere.
3. **The strip must stick** — the BMAD installer manifest must no longer reinstall per-repo skill copies.

Canonical skill home (pi-global): `/Users/moses/code/.agents/skills/` (symlinked into `~/.pi/agent/skills/`). `_bmad/` stays per-repo forever.

## Task part 1 — PR in this repo (tracked changes)

1. **Rescue unique skills before deleting anything.** For each directory under `.claude/skills/` matching `bmad-*`: if its name is **absent** from `/Users/moses/code/.agents/skills/` AND does **not** match `bmad-loop-*`, copy it to the canonical dir (`cp -R <dir> /Users/moses/code/.agents/skills/`; skip if it appears there mid-task). Expected: `bmad-review-verification-gap`; enumerate for others. Record the rescued list for the PR + final report.
2. `git rm -rq .claude/skills/bmad-*` — remove ALL of them (duplicates, loop skills, rescued ones now safe in canonical). **Keep** all non-`bmad-*` entries under `.claude/skills/`. Do not touch any other part of `.claude/`.
3. **AGENTS.md:** add a short "Skill locations" section: bmad skills are pi-global (canonical `/Users/moses/code/.agents/skills`, symlinked into `~/.pi/agent/skills`); do not reinstall them per-repo; the `.claude/skills/bmad-*` copies were removed (pi-only going forward); `_bmad/` config remains per-repo. If a `CLAUDE.md` exists and references the removed paths, make the minimal edit pointing it at AGENTS.md.
4. Commit on `bmad-post-strip-hardening`, push, `gh pr create --base develop`. PR description needs **"Decisions & rationale"**: pi-only decision, loop retirement, rescued-skills list (now pi-global), and an explicit note that the installer manifest fix is a **local, gitignored change in the main checkout** (part 2) because `_bmad/` is not tracked.

## Task part 2 — local main-checkout changes (no commit, `_bmad` is gitignored)

In `/Users/moses/code/RightTenantry` (NOT the worktree):

1. Edit `_bmad/_config/manifest.yaml`: remove `pi` **and** `claude-code` from `ides` (if the schema requires the key, use `ides: []`). If you find evidence `ides` drives more than skill-install targets, make the minimal safe change and explain in the final report.
2. `_bmad/_config/bmad-help.csv`: it catalogs skills at now-deleted per-repo paths. Regenerate it if a generator exists (check `_bmad/scripts/`); otherwise remove the stale per-repo `.agents/skills` rows by hand; if neither is safely possible, note it.
3. `.bmad-loop/` at the repo root (loop retired): verify untracked (`git ls-files .bmad-loop` empty), then `rm -rf .bmad-loop`. If tracked, do NOT delete — note it instead.
4. **Guard:** after these steps, `git -C /Users/moses/code/RightTenantry status --porcelain` must show no tracked modifications caused by you.

## Env / bootstrap

- `.env` is symlinked from the main checkout — read-only.
- `_bmad` project config was copied into the worktree.

## Verify

No build/test needed — deletions + docs only. Final message must include: rescued-skills list (with canonical paths), count of `.claude/skills/bmad-*` dirs removed, manifest before/after `ides`, bmad-help.csv outcome, .bmad-loop outcome, guard-check result, PR URL.

## Model policy

Unset — pi default model resolution. Applies to any mega-minions you spawn (close them when done).
