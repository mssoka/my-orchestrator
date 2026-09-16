# packet-plumber-3d-scene-refactor — field notes

- 2026-09-05: Godot placeholder-instance trap bites @tool generation:
  `PackedScene.instantiate()` of a scene whose root script is NOT @tool
  yields a placeholder under the editor — script methods (setup()) are
  uncallable and staging silently aborts at child 1. Editor-hint paths must
  construct via .new(); runtime can instantiate. Caught ONLY by pixel
  forensics (suite is runtime-only).
- 2026-09-05: editor-viewport PNG md5 is NOT a valid determinism gate:
  same-code re-renders gave 3 different md5s pre-refactor; the audit pinned
  the mechanism (editor viewport height drifts ±1 px with window/dock
  layout). Gate instead on structural pixel diff (12× downscale + blur,
  grayscale): noise floor max≈1; real composition change reads max 110+.
- 2026-09-05: the godot MCP's LSP is a long-lived `godot --headless --editor
  --lsp --path .` process that holds the PRE-MOVE class cache after refactors
  (140 phantom diagnostics citing old paths; res:// resource-existence checks
  also lag new files). `pkill -f "godot.*--lsp"` → MCP respawns fresh → 0
  real diagnostics. Check disk `.godot/global_script_class_cache.cfg` first
  to prove the cache is fine.
