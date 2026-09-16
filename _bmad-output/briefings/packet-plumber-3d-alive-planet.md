# Briefing: packet-plumber-3d-alive-planet

Read the standing orders first: `/Users/moses/code/docs/orchestration-playbook.md`
section 'Minion standing orders'. This briefing is your task spec.

## Task

**THE ALIVE PLANET — the flagship look pass** (user, 2026-09-05): "I'm
looking for something that makes the planet alive rather than just houses
that need to be connected. it should be alive, it should look beautiful."

**The look canon:** `/Users/moses/code/_local-refs/little-planet-ref/frames/`
(77 frames, `frame-tNN.jpg` = second NN; browsable grid:
`../frame-atlas.html`). Cite specific frames for every design decision.

## The three layers

1. **Terrain with intent** (procedural, Godot):
   - **Snow caps at the poles**; **mountain ridges** between biomes;
     **rivers running to a colorful ocean**; ocean islets. Placement by
     design — the planet reads as a place, not a scatter.
   - User: "The planet should have intent where the snow caps are, the
     mountains, the water." Displacement/biome logic with purposeful
     placement (pole-banded snow, ridge-following mountains, carved
     river paths downhill to sea level).
2. **Life props via the Blender MCP** (user confirmed: "we can get assets
   via blender"):
   - Hunt + modify: **trees** (temperate wedges), a **lighthouse** (on an
     ocean islet — the reference has one), **igloos** (cold areas), plus
     whatever the atlas reveals that says "someone lives here" (rocks,
     bushes, boats…). CC0/CC-BY ONLY; tri-light; attribution registry.
   - **SHARED-BLENDER GUARDRAILS (standing):** the running Blender is the
     user's — NEVER open_mainfile, NEVER save, NEVER touch existing
     objects; imports → modify → glTF export → DELETE; zero residue.
     Craft gotchas: sanitize ID names `[A-Za-z0-9_]`, measure bbox after
     import, origin-normalize, downscale review renders.
   - Props are AMBIENT (not connectable nodes) — they dress the world;
     staging is seeded-deterministic per level.
3. **Palette + first impression**:
   - Palette drawn from the atlas (bright, saturated, alive — colorful
     ocean, distinct biomes). The player's FIRST sight of a planet must
     be beautiful — the world before the wires.
   - Water/ocean shader-feel: colorful, inviting (reference frames), not
     default-blue.

## Acceptance

1. Terrain intent demonstrable: pole snow caps, ridge mountains, ≥2
   rivers to the ocean, an islet with the lighthouse — visible in one
   orbit.
2. Props staged: trees in temperate wedges, igloos in snow, lighthouse
   lit on its islet — seeded-deterministic; sim/view purity (replay
   byte-identity per level; suite green).
3. **Look-parity evidence**: side-by-side captures vs cited atlas frames
   (≥4 comparisons); you are natively multimodal — verify the look
   YOURSELF before claiming it; `LOOK-PARITY.md` updated.
4. Fresh-clone import clean; LSP clean; `captures/` committed.
5. PR body: run command, capture walkthrough, frame citations, Decisions.

## Model policy / Skills / Perkins

Minion: `zai-coding-cn/glm-5.3-flash`. Workflow: `gds-quick-dev`.
`pr_review=1` (the game's face). No lavish — the L1 play gate iterates on
the result.

## Dispatch parameters

```
job_id:    packet-plumber-3d-alive-planet
repo:      packet-plumber-3d
slug:      alive-planet
base:      main
model:     zai-coding-cn/glm-5.3-flash
pr_review: 1
notes:     Worktree from origin/main (5a5d5d0). _bmad bootstrap. PARALLEL
           LANES: gdd-amend-alive-planet (docs) + l1-topology-font (code)
           — disjoint files (yours: terrain/world gen + props staging +
           palette; NOT the connect grammar or UI theme).
```
