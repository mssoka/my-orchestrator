# packet-plumber-v2-pace-tuning (2026-08-21/22)

- The 5.9 spawn-credit clamp makes the effective per-terminal pick rate
  `1 / ceil(1000/accrue)` per tick (campus 625 milli → 0.5/tick; host 333 →
  0.25/tick) — the raw accrue/1000 formula OVERSTATES the rate whenever
  accrue > 500 milli; demand tests must derive from the clamp, and W9-class
  "ask lands" contracts re-derive units-anchored at any pace scale (the ×10
  surge multiplicativity dims to ~2.6× at 4× — the packet ask can't express
  above the units-anchored pool; the saturation trigger still fires).
- The crisis (b)-drop-fallback regime is phase-dependent at the 4× pace:
  the director's bursty credit arrivals make the post-flow eval lane land on
  the bound every other tick (a) — the deterministic construction is ODD
  arrivals/tick (5/tick: 5→6→shed→5, post-flow below the bound) or a
  pre-window backlog at the bound at the window's first tick.
- A 4× pace re-tune ripples into EVERY exact-tick/unit test pin (17 files,
  46 pins) AND the health stagings: the post-fix breach exit lands ~fix+179
  (the latency window slides faster with sparser deliveries) vs the grace
  expiry ~428 — the "exit just after the expiry" staging needs the fix ≥300
  (at 241 the exit beats the expiry and the meter never drains).
