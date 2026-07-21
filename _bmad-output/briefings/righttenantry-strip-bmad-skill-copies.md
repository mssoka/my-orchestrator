# Briefing: righttenantry-strip-bmad-skill-copies

- **Repo:** /Users/moses/code/RightTenantry
- **Worktree (your cwd):** /Users/moses/.herdr/worktrees/RightTenantry/strip-bmad-skill-copies
- **Branch:** `strip-bmad-skill-copies` → PR targets **`develop`**
- **Base:** `develop`

## Standing orders

Read `/Users/moses/code/docs/orchestration-playbook.md` section **"Minion standing orders"** and follow it exactly. Use the **bmad-quick-dev** skill; step-01 clarify = HALT and wait for relayed answers (this task is fully specified — halt only on genuine blockers); internal approval checkpoints are pre-approved. Self-report every status transition: `/Users/moses/code/bin/ledger set righttenantry-strip-bmad-skill-copies <status> "<note>"`. When blocked or finished: `herdr notification show "righttenantry-strip-bmad-skill-copies" --body "<one-line status>"`. Never merge the PR.

## Context (why)

BMAD skills are now installed once, canonically, at `/Users/moses/code/.agents/skills/bmad-*` and symlinked into `~/.pi/agent/skills/` — every pi agent (including worktree minions like you) sees them globally. The per-repo copies under `.agents/skills/bmad-*` are redundant. This job strips them across the workspace. `_bmad/` project config stays per-repo — Gru's dispatch bootstrap copies it into worktrees.

**Self-preservation note:** your own running session may have loaded bmad skills from this repo's copy. Before deleting anything, run `cp -R .agents/skills/bmad-quick-dev /tmp/bmad-quick-dev-ref` and read step files from there if the worktree copies disappear mid-task. Delete `bmad-quick-dev`'s directory last.

## Task part 1 — PR in this repo (RightTenantry)

1. Enumerate: `ls .agents/skills/`. Delete **only directories matching `bmad-*`**:
   `git rm -rq .agents/skills/bmad-*` (expand the glob; verify each path is under `.agents/skills/` and starts with `bmad-`).
2. **Keep** all non-bmad skills (arize-*, wds-*, anything not `bmad-*`).
3. Check `skills-lock.json` at the repo root: if it lists `bmad-*` entries, remove them. If the file is tool-generated and the format is unclear, leave it and flag it in the PR description.
4. Do **not** touch: `_bmad/`, `_bmad-output/`, `.claude/`, `.bmad-loop/`, `.env*`, `.agents/skills/` non-bmad entries, `/Users/moses/code/.agents/skills` (canonical copy), `~/.pi/agent/skills` (symlinks). Do **not** run any bmad "uninstaller" — surgical deletion only.
5. Verify: `ls .agents/skills | grep -c '^bmad-'` → 0; non-bmad skills still present; `git status` shows only deletions of `.agents/skills/bmad-*` (plus possibly `skills-lock.json`).
6. Commit on `strip-bmad-skill-copies`, push, open PR targeting `develop` (`gh pr create --base develop`). PR description must include a **"Decisions & rationale"** section: why the copies are redundant (global symlink), that `_bmad` intentionally stays, and the post-merge note that future worktrees get skills from the global install.

## Task part 2 — untracked sweep in other main checkouts (no PR, no worktree)

These repos hold bmad skill copies that are **not git-tracked** (gitignored or never committed). Delete them directly in the main checkouts — this is local hygiene, no branch, no commit:

- `/Users/moses/code/form11tax/.agents/skills/bmad-*` (gitignored)
- `/Users/moses/code/ideas/.agents/skills/bmad-*` (gitignored; `ideas` may not be its own git repo — that's fine, the files are untracked regardless)
- `/Users/moses/code/RTBComplianceCopilot/.agents/skills/bmad-*` (believed untracked — **verify first**)

For each of the three:
1. **Verify untracked before deleting:** `git -C <repo> ls-files .agents/skills | grep bmad` must output nothing. If it outputs anything (tracked files), **do not delete there** — note it and move on.
2. `rm -rf <repo>/.agents/skills/bmad-*` (only `bmad-*`, nothing else).
3. **Verify after:** `git -C <repo> status --porcelain` must be clean (no accidental tracked deletions).

LarOS-Lustre and LarOSAgents were checked and have no bmad skills on disk — no action.

## Env / bootstrap

- `.env` / `.env.test` (whichever were gitignored) are symlinked from the main checkout — treat as read-only.
- `_bmad` project config was copied into the worktree.

## Verify

No build/test needed — deletions only. Final message: summary, files/dirs removed per location (counts), part-2 verification results, PR URL.

## Model policy

Unset — pi default model resolution. Applies to any mega-minions you spawn (close them when done).
