# orchestrator-playbook-diet — field notes

- 2026-08-21: bmad-quick-dev → bmad-build render HALTs on this install
  (`ambiguous config value implementation_artifacts`) — waiver carried as
  a canon note in the PR body; the briefing was self-contained.
- 2026-08-21: full-file rewrites from memory re-inflate to ~950+ lines —
  the reliable diet is SEGMENTED line surgery (measure per section →
  exact-string replace → re-measure), not whole-file rewrites.
- 2026-08-21: heredoc + triple-quote Python strings with embedded quotes
  self-terminate (SyntaxError) — write replacement scripts to files or use
  the edit tool for exact-match replacements instead.
- 2026-08-21: the 650-line core target has a doctrine floor ~700: the
  keep-list sections (Model policy vision block, Minion standing orders
  paste-block, Dispatch commands, six-sensor table) are irreducible without
  cutting doctrine — report the honest number (713) and flag it in the PR.
- 2026-08-21: a `tr '\n' ' '` command inside a rewritten heredoc got
  corrupted into a literal newline — byte-check commands after any
  scripted rewrite (grep for the exact token).
- 2026-08-21: lavish session "ended by user" with the verdict in the
  session chat (`~/.lavish-axi/state.json` → sessions.<id>.chat) even when
  prompts shows 0 — check chat when the poll returns a dom_snapshot.
