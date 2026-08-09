# orchestrator-docs-ua1-ua2 — field notes

- 2026-08-07 (orchestrator-docs-ua1-ua2): briefing said "work directly in
  the orchestrator root (no worktree)" but the dispatch actually created a
  STANDARD worktree — pane cwd was `~/.herdr/worktrees/code/orchestrator-docs-ua1-ua2`
  with the `<slug>` branch already checked out. Ground truth = pane cwd; work
  there on the slug branch (the PR→main outcome is identical either way). Adds
  a "worktree/no-worktree decision in the briefing disagrees with the actual
  dispatch" flavor to the existing stale-briefing lesson.
- 2026-08-07 (orchestrator-docs-ua1-ua2): for a pure structural doc reorg
  (zero-content-loss constraint), the reliable PROOF is a sorted multiset of
  non-header lines old-vs-new (`grep -vE '^(##|###|\s*$)' | sort | diff`) →
  byte-identical = nothing changed/lost. Don't eyeball `git diff` — reordering
  shows as noisy add+remove pairs that look like content change.
- 2026-08-07 (orchestrator-docs-ua1-ua2): `gh pr create --body "$(cat <<'EOF'
  ... EOF)"` BREAKS when the body contains backticks — bash command-
  substitution executes them (got `node_modules: command not found`). Use
  `--body-file <file>` for any PR body with backticks/code spans.
