# packet-plumber-v2-node-clarity

## Task

Node types must be identifiable at a glance (user complaint #2:
"it's not clear which node is what"). Measured: shapes DO differ
(house aspect 1.01 vs small_biz 1.45 / campus 1.48 / host 1.45) but
small_biz / campus / host share wide-block aspect and small_biz/campus
share the warm-brown family — the blur test (DIRECTION.md §1) shows
hue deltas under the ≥15° bar: residential↔small_biz 3°, residential↔
campus 13°, router_mid↔content_host 9–13°.

1. **Hue-family separation** (palette tokens, the blur-test cure):
   give each terminal class a DISTINCT hue family ≥15° apart with a
   saturation band ≤0.3 wide (ours is 0.50):
   - small_biz → cool-stone family (#A0937D anchor)
   - campus → brick family (#8B4513 anchor)
   - residential → warm terracotta (#CD5C5C anchor) — keeps its
     distinct house silhouette (aspect 1.01)
   - content_host → deep blue (#4682B4 anchor) — already unique, keep
     or deepen for contrast
   - router tiers → keep size ladder, add tier color marker
2. **Type icon chip**: tiny glyph above each terminal (the tray icons
   already exist — reuse them) so type reads even at bird's-eye.
3. **Router tier markers**: port count as a small number OR a distinct
   ring color per tier (basic/mid/high) — currently size-only, LED
   count too tiny at fit.

## Rules (hard)

1. Palette tokens + draw-layer only (data/palette.json,
   app/render/view.odin draw_building / draw_router). No geometry/sim.
2. **Blur-test gate**: re-run the σ6 blur on the terminal-types
   capture — every pair must be separable by hue, all deltas ≥15°,
   sat band ≤0.3. Numbers in the PR body.
3. MM model: distinct shapes per type + color families (image_02/04/06/08
   in the audit's MM ref set).
4. Don't regress the calm-board palette (POP job owns the network;
   coordinate token changes).

## Acceptance

- Blur-test σ6: all node-type pairs hue-separated ≥15°, sat band ≤0.3.
- Type icons visible at fit scale; router tiers distinguishable by
  color marker + size.
- Local suite green; palette tokens palcheck-pinned.
- pr_review: 1 (Perkins before merge).

## Skills policy

bmad-quick-dev.

## Model policy

deepseek-v4-flash, --thinking max.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-node-clarity
- base: v2
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- parallel-safe with the whole v2 visual wave; coordinate palette
  tokens with v2-network-pop (both touch data/palette.json — Gru picks
  merge order; final wave re-bless reconciles)
- source of truth: kyle-design-directions.md §3 + design-audit.html Q2
  + captures/blurtest/
