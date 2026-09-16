# packet-plumber-3d-l1-topology-font — field notes

- 2026-09-05: Godot 4.7 `FontVariation.variation_opentype` SILENTLY IGNORES
  string axis keys (`{"wght": 700}` renders regular) — only integer fourcc
  tags work (`{("w"<<"24")|...: 700}`); a bold-vs-regular advance-width pin
  is the cheap guard. Also: `#` comment lines poison project.godot sections
  (keys read back empty) — use `;`.
- 2026-09-05: macOS occlusion throttling freezes windowed captures (the
  freshness gate caught identical frames); fullscreen puts the window on an
  active Space and `CONTENT_SCALE_MODE_CANVAS_ITEMS`+`EXPAND` keeps UI at
  true game proportions on the big canvas (downscale to 1600 wide after).
- 2026-09-05: the godot MCP LSP serves the MAIN checkout root — worktree
  files analyze as outsiders (phantom "hides a global script class" +
  "not declared" for NEW global classes). Prove health via on-disk
  `.godot/global_script_class_cache.cfg` + `--check-only --script` per file.
