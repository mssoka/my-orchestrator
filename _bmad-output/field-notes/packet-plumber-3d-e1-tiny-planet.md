# Field notes — packet-plumber-3d-e1-tiny-planet

- 2026-09-04: Godot camera gotchas that renders catch and unit tests miss: `look_at_from_position`
  takes GLOBAL coords (pinned our camera to world +Z — rig spanned, camera didn't); and
  `frame_point`-style "aim at X" must place the camera on X's SIDE, not the antipode (we
  photographed the wrong hemisphere). Always verify pose changes with a SCREENSHOT, not just
  transform asserts.
- 2026-09-04: Icosphere face winding: the classic Kahler table is CW = back-facing in Godot
  (CCW = front). Symptom: land invisible from outside, visible from inside. Swap two leaf verts
  and rely on SurfaceTool.generate_normals following winding.
- 2026-09-04: `-s` SceneTree scripts: nodes added during `_initialize` aren't inside the tree yet
  (global_transform errors) — run the suite on the first `process_frame`, and never `.free()`
  RefCounted test instances (drop the ref). Any pre-quit crash = engine hangs forever: null-guard
  every `load()` in the runner. Also GDScript has no `%e` format and INFERENCE_ON_VARIANT
  (`var x := get_setting()`) is an ERROR by default.
