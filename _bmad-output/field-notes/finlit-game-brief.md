# Field notes — finlit-game-brief (2026-07-31)

- `herdr wait agent-status --status done` can time out even when the mega-minion finished — panes in a watched tab complete as `idle`, not `done`; poll `herdr pane get` and accept either.
- Mega-minions re-reviewing a file the parent just edited can report STALE findings from session context (2 this run) — verify every finding against disk before applying.
- gds-create-game-brief's `.decision-log.md` is a dotfile inside the run folder — `git add` the folder path normally picks it up, but confirm with `git status` before committing (the verify bar is "only the new artifact").
