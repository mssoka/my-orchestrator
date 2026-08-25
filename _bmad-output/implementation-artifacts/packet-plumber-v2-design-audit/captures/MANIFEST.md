# Capture manifest — packet-plumber-v2-design-audit

All captures rendered from the worktree at **sha `8639d5f`** (base v2 @ head,
post look-polish PR #75) via the golden-image harness (rlsw software renderer —
bit-exact, no GPU/display; the same capture approach the look-polish job used).
Baseline verified: `harness run juice terminal_types router_tiers growth
estate_surge qos_contention` — 6/6 PASS at this sha.

- stills/*.png — blessed T2 golden frames (committed at this sha, byte-identical
  re-render proven by the PASS run above) + copies
- motion/motion-*.png — 11 consecutive frames, 100 ms apart (2 sim ticks @ 20 Hz),
  juice scene (seed 7, era 3, calm moment): packets in flight
- spawn/spawn-*.png — 12 frames across the first growth terminal pop:
  1500/1900/1950 (pre) → 2000 (pop, diff-bbox verified 859,246–905,282) →
  2050/2100/2150 (settle) → 2500–4500 (later windows)
- crops/*.png — close-up crops of individual nodes (router tiers, every terminal
  type), pipe corridors with packets, composite strips, 4× spawn zooms

| Set | Files | What it covers | Kyle questions |
|---|---|---|---|
| stills/ | juice-30000/65000, terminal_types-05000/30000, router_tiers-02500/03500, growth-01500/88000, estate_surge-75000, qos_contention-01000/03000 | routers + terminals, every node type, dense/surge states | Q1, Q2 |
| crops/ | router_*, rt_*, tt_*, house_*, host_*, core_motion_*, corridor_motion_*, *_strip, spawn_*_zoom | node close-ups, packet corridors, spawn pop | Q1–Q4 |
| motion/ | motion-29800…30800ms | packet motion sequence | Q3 |
| spawn/ | spawn-01500…04500ms | terminal spawn cadence sequence | Q4 |
| blurtest/ | *_blur3/6/12 + *_blur8 crops | Brush blur-test set (DIRECTION.md fold): full frames at σ3/σ6/σ12 + per-type crops at σ8 | blur test |

## Design-direction fold (DIRECTION.md, 2026-08-22)

- blur set: captures/blurtest/ (Gaussian σ3/σ6/σ12 full frames + σ8 per-type crops)
- Kyle's blur-test verdict: kyle-blurtest.md (PASS visually at σ3/σ6 by sat/lightness; hue deltas 3–13° fail the ≥15° hue-separation standard; saturation band 0.50 wide = the direction's anti-pattern)
- palette-harmony + depth columns added to the report's decision table (measured hue-family share + center→corner haze drift)
- sound recommendations (DIRECTION.md §3) folded into the report's job list — out of visual scope, user-directed
- source: /Users/moses/code/_local-refs/design-videos/DIRECTION.md (Brush 5-steps + Hokkori; thumbnails brush-thumb.jpg / hokkori-thumb.jpg, local only)
