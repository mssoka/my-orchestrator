# Briefing: righttenantryagents-strip-bmad-skill-copies

- **Repo:** /Users/moses/code/RightTenantryAgents
- **Worktree (your cwd):** /Users/moses/.herdr/worktrees/RightTenantryAgents/strip-bmad-skill-copies
- **Branch:** `strip-bmad-skill-copies` → PR targets **`develop`**
- **Base:** `develop`

## Standing orders

Read `/Users/moses/code/docs/orchestration-playbook.md` section **"Minion standing orders"** and follow it exactly. Use the **bmad-quick-dev** skill; step-01 clarify = HALT and wait for relayed answers (this task is fully specified — halt only on genuine blockers); internal approval checkpoints are pre-approved. Self-report every status transition: `/Users/moses/code/bin/ledger set righttenantryagents-strip-bmad-skill-copies <status> "<note>"`. When blocked or finished: `herdr notification show "righttenantryagents-strip-bmad-skill-copies" --body "<one-line status>"`. Never merge the PR.

## Context (why)

BMAD skills are now installed once, canonically, at `/Users/moses/code/.agents/skills/bmad-*` and symlinked into `~/.pi/agent/skills/` — every pi agent (including worktree minions like you) sees them globally. The per-repo copies under `.agents/skills/bmad-*` are redundant. This job strips them from this repo. `_bmad/` project config stays per-repo — Gru's dispatch bootstrap copies it into worktrees.

**Self-preservation note:** your own running session may have loaded bmad skills from this repo's copy. Before deleting anything, run `cp -R .agents/skills/bmad-quick-dev /tmp/bmad-quick-dev-ref-rtagents` and read step files from there if the worktree copies disappear mid-task. Delete `bmad-quick-dev`'s directory last.

## Task — PR in this repo (RightTenantryAgents)

1. Enumerate: `ls .agents/skills/`. Delete **only directories matching `bmad-*`**:
   `git rm -rq .agents/skills/bmad-*` (expand the glob; verify each path is under `.agents/skills/` and starts with `bmad-`).
2. **Keep** all non-bmad skills (anything not `bmad-*`). Also leave the repo-root `skills/` directory and `.pi/` alone — out of scope.
3. Check `skills-lock.json` at the repo root: if it lists `bmad-*` entries, remove them. If the file is tool-generated and the format is unclear, leave it and flag it in the PR description.
4. Do **not** touch: `_bmad/`, `_bmad-output/`, `.claude/`, `.bmad-loop/`, `.env*`, `.agents/skills/` non-bmad entries, `/Users/moses/code/.agents/skills` (canonical copy), `~/.pi/agent/skills` (symlinks). Do **not** run any bmad "uninstaller" — surgical deletion only.
5. Verify: `ls .agents/skills | grep -c '^bmad-'` → 0; non-bmad skills still present; `git status` shows only deletions of `.agents/skills/bmad-*` (plus possibly `skills-lock.json`).
6. Commit on `strip-bmad-skill-copies`, push, open PR targeting `develop` (`gh pr create --base develop`). PR description must include a **"Decisions & rationale"** section: why the copies are redundant (global symlink), that `_bmad` intentionally stays, and the post-merge note that future worktrees get skills from the global install.

## Env / bootstrap

- No `.env` files found in the main checkout at dispatch time — nothing symlinked.
- `_bmad` project config was copied into the worktree.

## Verify

No build/test needed — deletions only. Final message: summary, count of skill dirs removed, confirmation non-bmad skills remain, PR URL.

## Model policy

Unset — pi default model resolution. Applies to any mega-minions you spawn (close them when done).
