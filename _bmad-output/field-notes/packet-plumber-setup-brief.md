# Field notes: packet-plumber-setup-brief

- 2026-08-05: the briefing listed source-material paths under the
  orchestrator-root `_bmad-output/planning-artifacts/`, but the concept +
  forge files actually lived in the REPO's own
  `_bmad-output/planning-artifacts/` (same relative path, different root).
  For a repo-local job (cwd = the repo), `find` the planning artifacts
  *inside the repo* before declaring ENOENT against the orchestrator root.
- 2026-08-05: Godot `aspect=expand` + "both orientations" needs a SQUARE base
  (720×720) per the multiple-resolutions doc's explicit tip — a rectangular
  base yields a different scale factor per orientation. The user then ruled
  landscape-only, so 1280×720 + `orientation=0` (SCREEN_LANDSCAPE) won.
  Verify viewport/orientation semantics against the Godot
  multiple-resolutions doc before committing display settings; the
  `--headless --check-only` gate is invalid (hangs) — use `--import` then
  `--quit-after 600`.
- 2026-08-05: `gh pr create --body "$(cat <<'EOF' … EOF)"` choked on the
  body's embedded quotes/backticks even with a single-quoted heredoc — use
  `--body-file <file>` for any non-trivial PR body. (General shell lesson,
  reusable across jobs.)
