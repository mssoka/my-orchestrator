# righttenantry-mobile-form-hunt — field notes

- The status-stepper "escapes card" bug needed BOTH `min-w-0` on the rail AND `w-full` on its `flex flex-wrap` wrapper — the wrapper is a flex item of a `flex-col items-center` column where align-items:center sizes items by CONTENT (cross-axis), so flex-shrink/min-width never apply; verify flex geometry by walking the ancestor chain in the DOM, not by reading classes.
- `dot_env.load_default()` overrides process env — to point the dev server at a local Docker DB, copy `server/.env` (rm symlink + cp) and patch it; a fresh `server/.env` symlink must be created in new worktrees (only root `.env` is bootstrapped) or the server panics "DATABASE_URL not set".
- agent-browser `eval` returns `["<json-string>"]` (array-wrapped double-encoded) — parse with a loop, not a single json.loads; the default session is shared machine-wide, always `--session <job-id>`; `set viewport W H 3` gives DPR3.
