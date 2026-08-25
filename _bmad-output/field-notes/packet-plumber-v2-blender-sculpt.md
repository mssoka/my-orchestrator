# Field-notes shard: packet-plumber-v2-blender-sculpt

- (2026-08-23) **Never trust a piped Blender run**: `blender -b -P … | grep`
  masks the exit code AND the traceback — two "determinism-proof" runs had
  crashed on a bad API call (`RenderSettings.use_metadata` is GONE in 5.2)
  while `cmp` compared stale files. Capture `rc` first, then sanity-check
  output FRESHNESS (mtimes / expected new values) before believing a
  byte-compare. PNG byte-determinism fix that works on 5.2: strip
  tEXt/iTXt/zTXt chunks post-render (the wall-clock `Date` tEXt is the only
  mover; IDAT is stable run-to-run).
- (2026-08-23) Blender-MCP exec chunks run in a FRESH globals namespace per
  call — imports don't persist; park helpers in `bpy.app.driver_namespace`
  and re-import `bpy/os/Vector` at the top of every chunk (and if a helper
  needs a module, inject it into `helper.__globals__`). Keep chunks small
  (~<100 lines — a big one died mid-write with a broken pipe, and a partial
  exec leaves partial scene state; clear and rebuild, don't patch).
- (2026-08-23) Look-gate lesson: at the MM top-down tilt (~60° elevation),
  sub-mass stacking (setback blocks) reads as MUDDY STRIPES, and wall-band
  shading alone stays subtle — the depth that actually reads is (a) the
  two-tone ROOF (gable barns / hip caps, per the user's top-down refs) and
  (b) the engine-drawn CAST SHADOW (12-18% ink @ fixed 2px offset is an
  invisible sliver; 25-33% ink @ proportional offset 0.08w/0.10h down-right
  reads). Coplanar plate overlaps z-fight — butt-joint instead.
