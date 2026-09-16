# Briefing: packet-plumber-3d-gdd-amend-alive-planet

Read the standing orders first: `/Users/moses/code/docs/orchestration-playbook.md`
section 'Minion standing orders'. This briefing is your task spec.

## Task

**Canon amendment carrying three user rulings (2026-09-05, post-L1
feedback).** Direct PR (the rulings are the user's own words; lavish not
needed). Amend gdd.md + epics.md + decision-log.md.

## Ruling 1 — router-mediated topology (M1/M3)

User verbatim: "buildings should never connect to each other. should be
via routers."

- **Terminals never peer.** Every link is terminal↔router or
  router↔router. The connect verb rejects building→building (with a
  readable affordance steering to the router).
- **L1 adapts historically:** each ARPANET site = **host + IMP** (the IMP
  IS the router — historically true: hosts talked to IMPs, IMPs to each
  other). The four-site mesh becomes IMP-to-IMP; the LOGIN rides
  host→IMP→IMP→host. L1's beat is unchanged in spirit; its grammar gains
  the router from the first minute. Update the L1 spec + the tech ladder
  (junctions "arrive" at L2 as *placed/player-built* — but the
  router-mediated rule is law from L1 via the site IMPs; word this
  carefully so both hold).

## Ruling 2 — the alive planet (Art Direction rewrite)

User verbatim (anchors): "the planet should be beautiful… beautiful colour
palette. colourful ocean/rivers, trees, even a light house in the ocean.
mountains, igloos in the cold areas… something that makes the planet
alive… it should be alive, it should look beautiful. The planet should
have intent where the snow caps are, the mountains, the water."

- **Terrain has intent**: snow caps at the poles, mountain ridges between
  biomes, rivers running to a colorful ocean — placement by design, not
  scatter. The reference frame atlas is the canon:
  `/Users/moses/code/_local-refs/little-planet-ref/frames/`
  (frame-tNN.jpg, 1 fps; browsable via frame-atlas.html).
- **Life props**: trees in temperate wedges, a lighthouse on an ocean
  islet, igloos in the snow — props say "someone lives here."
- **Palette**: drawn from the reference frames; bright, saturated, alive.
- First impression is the requirement: the player's FIRST sight of a
  planet must be beautiful — the world before the wires.

## Ruling 3 — font (readability + theme)

User verbatim: "the font is hard to read so we need to use a font that
actually fits the game world theme. You can also look at the reference."
Current HUD/UI font fails readability. Canon: a themed, readable font
(the reference video's UI typography is the vibe — rounded, friendly,
legible at distance). Licensing discipline (open license; PP-Odin's
font-overhaul era has precedent lore in
`packet-plumber/_pr_body_font_overhaul.md`).

## Acceptance

1. All three rulings in canon with verbatim anchors + decision-log
   entries (dated, supersede notes where they reshape prior spec — the
   L1 "no junctions" flag reworded per Ruling 1's careful wording).
2. Art Direction section cites the frame atlas as the look canon.
3. No implementation — docs only. Suite untouched (docs-pinning tests
   updated if they reference amended lines).

## Model policy / Skills / Perkins

Minion: `zai-coding-cn/glm-5.3-flash`. Workflow: `gds-gdd` (update).
`pr_review=0` (docs, direct PR).

## Dispatch parameters

```
job_id:    packet-plumber-3d-gdd-amend-alive-planet
repo:      packet-plumber-3d
slug:      gdd-amend-alive-planet
base:      main
model:     zai-coding-cn/glm-5.3-flash
pr_review: 0
notes:     Worktree from origin/main (5a5d5d0). _bmad bootstrap. Parallel
           lanes: topology+font (code) + alive-planet (code) — disjoint.
```
