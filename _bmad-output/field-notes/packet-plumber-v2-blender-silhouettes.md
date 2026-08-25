# Field-notes shard: packet-plumber-v2-blender-silhouettes

- (2026-08-22) gen_sprites.py re-render on Blender 5.2 is PIXEL-DETERMINISTIC
  (decoded RGBA identical; md5 diffs are PNG-encoder metadata only) — a no-op
  re-render is golden-safe, so pipeline validation = render + pixel-compare,
  no re-bless. T2 compares decoded pixels, never file bytes.
- (2026-08-22) the pipeline's camera tilt VARIES with the per-sprite pad
  (direction vector includes the camera Y position: `(0, 0.35, 0.10) -
  (0, -4.5*pad, 10.0)`), so bbox aspects differ from world aspects — the
  renderer consumes the bbox aspect, so the READ is the bbox; don't "fix"
  the tilt without re-blessing (it's a pre-existing quirk, spec-documented).
- (2026-08-22) port-ring dots need an explicit cx/cy in add_flat_disc — the
  first cut stacked all dots at the disc center (PUCK_PORT_R was defined but
  never used in placement); KYLE caught nothing at contact-sheet scale — the
  bbox geometry table + a zoomed per-sprite check caught it.
