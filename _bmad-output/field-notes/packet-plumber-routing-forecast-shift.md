# Field notes — packet-plumber-routing-forecast-shift (Job C, R4)

- The 3.3 lane queues are STRICTLY FIFO at full pipe capacity per packet
  (serve_bundle_lane walks the array; windows repeat until capacity consumed)
  — a packet behind N queued packets waits N x edge-transit, so demo transit
  comments must count queue position, not lone-packet transit; verify capture
  narratives with a packet-state dump test, not arithmetic.
- The app's step passes `{}` (edits land via fast-path + are logged for
  replay) — tests exercising "the real edit path" should use the harness
  flavor (log-only + step_n) to stay aligned with the replay gate; the pixel
  capture narrative (which leg carries packets) is verifiable headlessly with
  a PIL blob-scan of email-color pixels vs screen-space segments (camera:
  scale min(1280/1040, 720/780), off_x 160).
- draw_forecast_panel's nil-preview default keeps harness T2 byte-identical,
  but a preview-non-nil + empty-forecast path still must NOT draw the weather
  card (the zero-pixels-when-empty contract is per-card, not per-call) — a
  self-review catch.
- r2 addendum: Odin `defer` is BLOCK-scoped — a `defer delete(sh)` inside a
  loop's if-block frees the buffer before the code after the block reads it
  (the preview golden rendered magnet=0 from freed-but-intact memory), and a
  block-local struct whose address escapes dangles past the block; hoist both
  to the loop body. Also: `var x T` is NOT Odin (use `x: T`), and a
  `odin build | head && echo OK` pipeline lies about the rc — check rc
  explicitly or the STALE binary silently re-blesses goldens (hit twice in
  one round).
