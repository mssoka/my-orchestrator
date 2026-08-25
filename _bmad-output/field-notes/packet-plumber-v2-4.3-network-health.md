# packet-plumber-v2-4.3-network-health — field notes

- The E9 lane bound (not the pool) dominates saturation timing: a narrow path
  breaches the WINDOWED SLA at ~tick 5 (2 arrivals/tick vs 0.083 service), so
  grace+death land at ~405/~455 — measure with a probe, don't model the pool.
- The windowed-exit latency: the E30 exit needs a FULL window slide after the
  drops stop (~200 ticks) — the grace must exceed window+drain or the recovery
  is unwinnable; the prototype's grace 200 @10Hz = 20 s (400 @ 20 Hz), not 10 s.
- The 4-port router cap + the real base demand (120 u/tick) force 2+-router
  recovery/win fixtures (ECMP); a single router physically cannot serve it.
- A demolish-only "fix" clears the windowed breach (no pipes = no drops = 0%
  loss) — re-saturate by re-drawing, and remember Cmd_Place_Router enforces
  PLACEMENT_MIN_SEP_TILES (7): a 6-tile-away spot silently rejects the fan.
- The `.log.bin` re-bless for a catalog-hash fold is EXACTLY the 8 header
  bytes (cmp-proven); zero old T2 PNGs change when the new HUD draws
  zero-pixels-when-disabled — that is the negative proof.
