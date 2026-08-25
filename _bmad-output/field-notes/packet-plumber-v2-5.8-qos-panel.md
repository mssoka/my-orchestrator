# packet-plumber-v2-5.8-qos-panel — field notes

- 2026-08-15 (packet-plumber-v2-5.8-qos-panel): a gitignore trailing-slash
  pattern (`tools/raylib-sw/`) does NOT ignore a SYMLINK FILE at that path —
  my local rlsw shadow symlink got `git add -A`'d and committed (machine-
  absolute, broken elsewhere). Ignore the bare path (`tools/raylib-sw`), and
  after any `ln -s` in a worktree, `git status` + `git ls-files` to confirm
  it stayed untracked.
- 2026-08-15 (packet-plumber-v2-5.8-qos-panel): Odin `strconv.parse_int`
  returns `(int, bool)` — NOT `(i64, bool)` — so an i64 range-check against
  `i64(min(i32))` mismatches types in a `package main`/harness context (the
  catalog's identical-looking line compiles because it casts from
  `json.Integer` first). Compare as `int` or cast the parse result first.
- 2026-08-15 (packet-plumber-v2-5.8-qos-panel): review swarms earn their cost
  on canon-surface gameplay code — the 2-hunter pass caught a committed
  build-artifact symlink (BLOCKER), a silent manual-tune clobber on the
  panel's primary affordance, and a future-era never-drop default-lane hole in
  auto-reservation's E6-safety claim, all before Perkins sees the PR.
