# Briefing: righttenantryagents-bmad-post-strip-hardening

- **Repo:** /Users/moses/code/RightTenantryAgents
- **Worktree (your cwd):** /Users/moses/.herdr/worktrees/RightTenantryAgents/bmad-post-strip-hardening
- **Branch:** `bmad-post-strip-hardening` → PR targets **`develop`**
- **Base:** `develop`

## Standing orders

Read `/Users/moses/code/docs/orchestration-playbook.md` section **"Minion standing orders"** and follow it exactly. Use the **bmad-quick-dev** skill; step-01 clarify = HALT and wait for relayed answers; internal approval checkpoints are pre-approved. Self-report every status transition: `/Users/moses/code/bin/ledger set righttenantryagents-bmad-post-strip-hardening <status> "<note>"`. When blocked or finished: `herdr notification show "righttenantryagents-bmad-post-strip-hardening" --body "<one-line status>"`. Never merge the PR.

## Context (why — user decisions 2026-07-21)

Follow-up to strip PR #162 (`.agents/skills/bmad-*` removal, pending merge — your branch is disjoint from it: you touch `.claude/skills`, not `.agents/skills`). User decisions:

1. **pi is the primary agent harness going forward** — Claude Code is retired for this repo; its per-repo bmad skill copies get removed. **Note:** a **kimi** harness is still in use in this repo — kimi-related config stays (see part 2).
2. **The bmad loop is retired** ("we don't need the loop now that Gru orchestrates") — `bmad-loop-*` skills are NOT preserved anywhere. (This repo's `.claude/skills/` is known to contain `bmad-loop-setup`.)
3. **The strip must stick** — the BMAD installer manifest must no longer reinstall per-repo skill copies for pi or claude-code.

Canonical skill home (pi-global): `/Users/moses/code/.agents/skills/` (symlinked into `~/.pi/agent/skills/`). `_bmad/` stays per-repo forever.

## Task part 1 — PR in this repo (tracked changes)

1. **Rescue unique skills before deleting anything.** For each directory under `.claude/skills/` matching `bmad-*`: if its name is **absent** from `/Users/moses/code/.agents/skills/` AND does **not** match `bmad-loop-*`, copy it to the canonical dir (`cp -R <dir> /Users/moses/code/.agents/skills/`; skip if it appears there mid-task — a sibling job may have rescued it already). Record the rescued list for the PR + final report.
2. `git rm -rq .claude/skills/bmad-*` — remove ALL of them. **Keep** all non-`bmad-*` entries under `.claude/skills/` (e.g. `arize-instrumentation`). Do not touch any other part of `.claude/`, the repo-root `skills/` dir, or `.pi/`.
3. **AGENTS.md:** add a short "Skill locations" section: bmad skills are pi-global (canonical `/Users/moses/code/.agents/skills`, symlinked into `~/.pi/agent/skills`); do not reinstall them per-repo; the `.claude/skills/bmad-*` copies were removed; `_bmad/` config remains per-repo. If a `CLAUDE.md` exists and references the removed paths, make the minimal edit pointing it at AGENTS.md.
4. Commit on `bmad-post-strip-hardening`, push, `gh pr create --base develop`. PR description needs **"Decisions & rationale"**: pi-primary decision, loop retirement, rescued-skills list, and an explicit note that the installer manifest fix is a **local, gitignored change in the main checkout** (part 2) because `_bmad/` is not tracked.

## Task part 2 — local main-checkout changes (no commit, `_bmad` is gitignored)

In `/Users/moses/code/RightTenantryAgents` (NOT the worktree):

1. Edit `_bmad/_config/manifest.yaml`: remove `pi` **and** `claude-code` from `ides`. **Keep `kimi-code`** — the kimi harness is still in use. **However:** investigate what install target `kimi-code` maps to (installer docs/config under `_bmad/`). If keeping `kimi-code` would reinstall bmad skills into this repo's `.agents/skills/` (resurrecting the strip), do NOT guess — HALT with a numbered clarify question and Gru will relay the user's decision. If it installs elsewhere, proceed and cite your evidence in the final report.
2. `_bmad/_config/bmad-help.csv`: it catalogs skills at now-deleted per-repo paths. Regenerate it if a generator exists (check `_bmad/scripts/`); otherwise remove the stale per-repo `.agents/skills` rows by hand; if neither is safely possible, note it.
3. `.bmad-loop/` at the repo root (loop retired): verify untracked (`git ls-files .bmad-loop` empty), then `rm -rf .bmad-loop`. If tracked, do NOT delete — note it instead.
4. **Guard:** after these steps, `git -C /Users/moses/code/RightTenantryAgents status --porcelain` must show no tracked modifications caused by you.

## Env / bootstrap

- No `.env` files in the main checkout — nothing symlinked.
- `_bmad` project config was copied into the worktree.

## Verify

No build/test needed — deletions + docs only. Final message must include: rescued-skills list (with canonical paths), count of `.claude/skills/bmad-*` dirs removed, manifest before/after `ides` (plus the kimi-code evidence), bmad-help.csv outcome, .bmad-loop outcome, guard-check result, PR URL.

## Model policy

Unset — pi default model resolution. Applies to any mega-minions you spawn (close them when done).
