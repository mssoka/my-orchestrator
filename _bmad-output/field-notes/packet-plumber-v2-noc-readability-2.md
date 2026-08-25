# packet-plumber-v2-noc-readability-2 — field notes

- The DOCK-RIGHT ruling's geometry is IMPOSSIBLE to satisfy by re-anchoring
  the top band into the shrunken playfield (title 180 + health 460 + forecast
  250 = ~890px > play_w 756 at 1280) — the sanctioned resolution is: fit-to-
  rail camera (View.play_w, one derivation) + top band cards KEEP win_w
  anchors and draw OVER the rail (world -> rail -> HUD order); the rail
  content starts below the top band (NOC_CONTENT_Y 116). Document in the PR.
- Odin const arithmetic: `NOC_PANEL_W :: i32(360 * 1.4)` TRUNCATES to 503
  (float const 503.999...) — use int math `360 * 14 / 10` for the 504 rail.
- The PP_DEBUG harness verbs need the rlsw software build (bin/harness-debug
  is GPU and renders a SOLID BLACK frame headless — the 08-11 trap, still
  live); the overlay-check verb takes the `12000ms` suffix form; both
  overlay verbs must view_set_rail(true) so the capture matches the app.
