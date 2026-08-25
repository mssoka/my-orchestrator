# packet-plumber-v2-network-pop

## Task

Make the network POP — the user's mid-review correction (2026-08-22):
"networking is boring so we need to make it pop… has to make good
attention-grabbing thumbnails." Measured root cause: the v2-look-polish
LEFOU system-tone pass muted the pipe tiers (the network) to gray-blue,
killing the saturation ceiling — our top-2% saturation = 0.51–0.57
(calm frames) vs Mini Motorways 0.91–1.00 (image_01/05).

Reverse the mute **in palette tokens only** — no geometry, no sim change:

1. Pipes back to a vivid tier family (each tier a distinct saturated
   hue; MM's bright ribbons + saturated cores are the model).
2. Packets to catalog maxima (saturated cores, not muted).
3. Node accents up (router LEDs, tier rings).
4. **Calm board stays calm** — the Brush 70/30 done right: board 70%
   cool-cyan (#87CEEB), 30% warm-gold (#FFD700); network layer inverted
   70/30 (warm-gold dominant). MM = white roads + saturated nodes on a
   quiet paper board; our board keeps the paper quiet, the NETWORK pops.

## Rules (hard)

1. Palette-token changes only (data/palette.json + the tier colors the
   renderer reads in app/render/view.odin). No geometry, no sim, no
   LOG_VERSION.
2. **Thumbnail gate**: re-capture the same demos at the pinned sha,
   re-measure top-2% saturation ceiling — target ≥ 0.85 (from 0.51).
   Also render the streamer-card scale test (427×240) and check the
   network reads as the "hero" element.
3. Keep the 70/30 calm/pop split — a fully-saturated board fails the
   direction's own standard (DIRECTION.md §1).
4. Run palcheck (in-repo palette checker) if the repo has one; keep
   canon-adjacent tokens intact.

## Acceptance

- Saturation ceiling ≥ 0.85 on re-measure; network reads as the hero at
  427×240 thumbnail scale.
- 70/30 split verified: board stays calm, network pops.
- Local test suite + goldens green (golden re-bless documented if the
  look shifts — cause-documented).
- pr_review: 1 (Perkins before merge).

## Skills policy

bmad-quick-dev.

## Model policy

deepseek-v4-flash, --thinking max.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-network-pop
- base: v2
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- parallel-safe with the whole v2 visual wave (sibling worktrees; merge
  order = the wave's final re-bless, coordinated by Gru)
- source of truth: kyle-design-directions.md §2 + design-audit.html POP
  section (artifact dir of packet-plumber-v2-design-audit)
