# field notes — packet-plumber-3d-e2-flow-qos

- 2026-09-04: Per-tick admission allowances can NEVER admit a packet larger
  than one tick's reserve — lanes need persistent deficit CREDIT (banked
  reserve, spendable in bursts) or a 1000-milli packet starves forever on a
  416-milli/tick budget. Caught by white-box probe before first suite run.
- 2026-09-04: Godot 4.7.1 runtime reload honors @warning_ignore at
  STATEMENT level only — func-level annotations pass the LSP but still warn
  in editor-run debug output. Also: non-tool scripts attached to scene nodes
  are PLACEHOLDER instances in the editor (@tool callers can't invoke their
  methods — Planet needed @tool for the editor-preview button path).
- 2026-09-04: Godot EDITOR windows at macOS off-screen positions (-3000)
  freeze to a 2x2 viewport texture (game windows render fine there) —
  capture EditorInterface.get_editor_viewport_3d(0) instead, and reposition
  the editor camera: its default pose sits INSIDE a radius-8 planet
  (front faces culled = "world missing" in the shot).
