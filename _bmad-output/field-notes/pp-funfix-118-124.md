# pp-funfix-118-124 — field notes

- 2026-09-01 (pp-funfix-118-124): PP worktree bootstrap missed `_bmad` (fully git-ignored) — `ln -s <repo_root>/_bmad _bmad` from the worktree before any bmad-build step; the render_skill.py lives at `/Users/moses/code/_bmad/scripts/` (the MAIN repo's `_bmad/scripts/` does NOT carry it).
- 2026-09-01 (pp-funfix-118-124): PP PRs ALWAYS `gh pr create --base v2` (Silas ops ruling after #125 was opened vs main and retargeted) — the dispatch briefing names no base; don't assume the remote HEAD default.
- 2026-09-01 (pp-funfix-118-124): replay_error latches with NO reason named (#123) — bisect rejections by (a) counting router ports FIRST (4/router; spine links count), (b) computing spans (`span_between` = integer Euclidean; standard 14 / mid 16 / wide 18), (c) `sed`-renumbering spawn ids leaves dangling draw endpoints — rewrite the whole demo instead.
