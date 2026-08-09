# Field notes — orchestrator-perkins-ops-codify (2026-08-07)

What bit me / what future minions must know.

- 2026-08-07 (orchestrator-perkins-ops-codify): the briefing said "work
  directly in the orchestrator root (no worktree)" but the dispatch STILL
  created a worktree — my real cwd was
  `/Users/moses/.herdr/worktrees/code/orchestrator-perkins-ops-codify`,
  and the branch was checked out THERE. I first ran git against
  `/Users/moses/code` (main) and hit `fatal: branch already used by
  worktree`. The worktree-path gotcha applies even on "no worktree"
  orchestrator-root jobs: run git + file edits from your actual cwd, not
  the main checkout. (`pwd`/`git branch --show-current` first.)
- 2026-08-07 (orchestrator-perkins-ops-codify): the briefing's evidence
  citation was inaccurate — it named "RT-agent #169 N3" as a fold-in
  example, but disk check showed `RightTenantryAgents#169` has only r1
  (N3 was advisory, PR merged as-is, no fold-in/r2). Ground-truth-first
  (fresh instance): verify briefing-cited PR numbers + shas against disk
  (`gh pr view`, the perkins `<job>/rN/consolidated.json`) BEFORE writing
  them into a high-stakes doc — don't propagate a briefing's claim into
  the playbook unverified. Dropped #169; kept the verified #585.
- 2026-08-07 (orchestrator-perkins-ops-codify): `gh pr create --body
  "$(cat <<'EOF' … EOF)"` with a trailing `| tail` breaks bash
  (unmatched paren / unexpected EOF) — write the body to a file and use
  `--body-file <file>` instead. Robust for any multi-paragraph PR body.
