# packet-plumber-v2-scale-depth

## Task

The user's final in-review feedback (2026-08-22, after the POP fix):
"the houses are smaller in MM vs PP. We need that as well. They used
shadows to create depth. Houses have smaller shadows and the buildings
have larger shadows. Also while we're at it, compare the background
maps as well. And also the art."

Three measured gaps against the MM bar:

1. **Node scale** (measured): at 1280×720 fit our house = 36 px (3.2×
   the 11.2 px standard pipe band), campus = 53 px (4.7×). MM houses ≈
   0.5–1.0× road width (image_01: houses ~105 px vs road 228 px;
   image_07: 65 px vs 68 px). Our nodes are TOO BIG relative to the
   network. Shrink footprints toward MM's ratio:
   - house: 1.50 → ~0.8–1.0 tiles
   - small_biz/host: 1.60/1.75 → ~1.0–1.2 tiles
   - campus: 2.20 → ~1.4 tiles
   - standard pipe band: 11.2 → ~15 px (slightly thicker ribbon so the
     network reads against smaller nodes — MM's road is ~2 px at board
     scale, keep ours legible but rebalanced)
2. **Shadow depth** (measured): ours = uniform 0.64w×0.36w ellipse at
   16% ink under EVERY node. MM = soft drop shadows offset down-right,
   SCALING with building size — small houses get small tight shadows,
   big buildings get larger shadows (image_07). Implement per-footprint
   shadow scale: house ~0.5w×0.3h, campus ~0.7w×0.4h, ink 12–18% by
   size; offset down-right ~2 px.
3. **Background map** (measured): ours = 34% canvas / 49% water / 9%
   park (juice capture). MM = 51% plain paper / 26% water / 11% warm
   land tint (image_01). Rebalance toward paper-dominant board + warm
   land tint; water retreats to edges; park reads as accent, not
   carpet. (Depth/haze from DIRECTION.md §5 is the separate N2/N3
   harmony job — only map share + warm tint here.)

"Also the art" = the silhouette question: verify after scaling whether
the shrunk sprites still read (silhouette minimalism is the separate
Blender job — this job only scales what exists).

## Rules (hard)

1. View-layer constants + palette tokens only (sprite targets in
   app/render/sprites.odin / view.odin draw_building, sprite_shadow,
   tier widths). No geometry, no sim, no LOG_VERSION.
2. Golden re-bless: this is a DELIBERATE, cause-documented visual
   change (node size + shadows + map share) — re-bless affected
   goldens with the change documented per capture.
3. Thumbnail gate: after scaling, re-check the 427×240 read — smaller
   nodes must NOT lose the network hero read (coordinate with
   v2-network-pop if needed).
4. MM refs are reference-only (audit ref set); measure with Python,
   never copy MM bytes into the repo.

## Acceptance

- Node:pipe ratio moved toward MM (house ≈ 1–2× band, down from 3.2×);
  before/after numbers in PR body.
- Shadows scale per footprint with down-right offset; before/after
  crops.
- Map share shifted toward paper-dominant + warm land tint; numbers in
  PR body.
- Goldens re-blessed (documented); local suite green.
- pr_review: 1 (Perkins before merge).

## Skills policy

bmad-quick-dev.

## Model policy

deepseek-v4-flash, --thinking max.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-scale-depth
- base: v2
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- parallel-safe with the whole v2 visual wave; coordinates with
  v2-network-pop (thumbnail gate) + v2-node-clarity (sprite reads);
  merge near the END of the wave so the final re-bless is one pass
- source of truth: kyle-design-directions.md §1 + §6 + design-audit
  (Scale/Shadow/Map measurements in the report)
