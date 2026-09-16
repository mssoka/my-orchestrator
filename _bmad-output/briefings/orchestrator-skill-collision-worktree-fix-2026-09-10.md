# Worktree skill-collision fix — untrack .agents/skills, bootstrap-symlink it

## Problem (diagnosed by Gru, verified on disk 2026-09-10)

- `~/.pi/agent/skills/gds-*` (and bmad-*) are SYMLINKS to canonical `/Users/moses/code/.agents/skills/*` — all 33 gds skills byte-identical.
- pi dedupes by realpath: at the orchestrator ROOT, symlink target == project path → silent. In WORKTREES (e.g. perkins-gemini-storyboard-skill-r1), the git-tracked `.agents/skills/gds-*` copy sits at a different realpath → pi reports collision, project copy auto-wins, global skipped.
- Cosmetic-but-recurring noise on every orchestrator worktree session; contents identical so correctness is unaffected today, but future drift would silently shadow canonical in worktrees.
- Side finding: `~/.pi/agent/skills/bmad-build` symlink is MISSING (bmad-build exists only as canonical project path). Check history for intentional removal; if none, Silas adds the symlink directly (no PR needed).

## Fix (durable, matches _bmad worktree-bootstrap doctrine)

1. In mssoka/my-orchestrator: untrack `.agents/skills` (`git rm -r --cached .agents/skills` — files REMAIN in the root working tree as canonical content) + add `.agents/skills/` to `.gitignore`. The global symlinks keep resolving to the root's working tree — zero functional change at the root.
2. Update the worktree bootstrap doctrine so new orchestrator worktrees symlink `.agents/skills` from the repo root (same shape as the existing `_bmad` bootstrap): docs/playbook-annex.md 'Dispatch — worktree bootstrap' section + any bootstrap helper scripts. Search the repo for `.agents/skills` references in bootstrap/dispatch docs and update them all.
3. Do NOT force-touch existing in-flight worktrees (perkins-gemini-storyboard-skill-r1 keeps its tracked copies; future worktrees get the clean shape).

## Verification

- Fresh throwaway worktree from the branch + a `pi --no-session` launch inside it shows NO gds-*/bmad-* collision warnings (the project copy is absent; global symlinks serve canonical).
- Root behavior unchanged: `pi` at /Users/moses/code still resolves all skills from canonical (project scope = same files).
- Sweep-check other managed repos (packet-plumber-3d, youtube-channel) for tracked `.agents/skills` — if any carry tracked copies, note them in the PR as the same class (fix only if trivially identical; otherwise report).
- bmad-build global symlink gap reported in PR body (Silas fixes the symlink itself).

## Dispatch parameters

- job_id: orchestrator-skill-collision-worktree-fix
- repo: orchestrator · repo_root: /Users/moses/code · github_repo: mssoka/my-orchestrator
- slug: skill-collision-worktree-fix · base: main
- worktree: new, from origin/main (fresh origin/main is ahead of dirty live root — that is fine, this is a fresh-branch change)
- model: zai-coding-cn/glm-5.3 · thinking: max (code-only lane, quota-hold interim routing)
- pr_review: 1 (structural tooling change; glm-5.3 Perkins round sanctioned under hold)
- Skills policy: bmad-build (mandatory render gate; if the same ambiguous-short-config halt recurs, apply the documented job-local qualified-token binding from gemini-storyboard-internal-unblock-2026-09-10.md — BMM module) — focused PR, no merge, no live-root mutation beyond the git rm --cached (Silas stages/commits on the worktree branch only; the live root keeps its files).
