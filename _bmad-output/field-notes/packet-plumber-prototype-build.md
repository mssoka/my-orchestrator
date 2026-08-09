# Field notes: packet-plumber-prototype-build

- 2026-08-08: the GoPeak Godot MCP install has NO `capture_screenshot` tool
  (briefing said it did — verify against disk). Visual verification path =
  in-game viewport capture: `get_viewport().get_texture().get_image()` run
  WINDOWED offscreen `--position -3000,-3000` (NOT -32000 — outside the
  renderable desktop → the viewport never clears → ghosted/overlapping text).
  The agent can't view images; `describe_image` (vision) is the only "eyes" and
  is flaky (returns empty / aborts) — retry, and it often only parses 1 image per
  call even when you pass several.
- 2026-08-08: SLA/loss uptime must be a ROLLING recent window (~last 10s), NOT
  cumulative-from-tick-0. Cumulative permanently tanks the average during the
  build phase (player reading onboarding + drawing first pipes) → pre-surge loss
  even with good pipes. Rolling forgives setup; the meter recharges once built.
- 2026-08-08: latency is an SLA METRIC, not a drop trigger (real packets don't
  drop when late). Drops = contention/queue-overflow/unreachable only. Also:
  decouple a cosmetic `vis_dist` (flows along the route) from bandwidth progress,
  and advance it ONLY when a packet is served — congestion then piles ALONG a
  clogged pipe (the readable panic) instead of vanishing. Cosmetic, excluded from
  the replay fingerprint; determinism holds.
