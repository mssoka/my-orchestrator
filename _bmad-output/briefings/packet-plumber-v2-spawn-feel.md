# packet-plumber-v2-spawn-feel

## Task

Terminal spawn FEELS frantic (user complaint #3). Two sides: the RATE
(owned by the parallel pace-tuning job) and the VISUAL FEEL (this job).
Code-verified: a terminal spawn is an INSTANT POP with zero telegraph —
no spawn animation exists anywhere in the view layer (growth adds the
node inside core/growth.odin GROWTH_INTERVAL_TICKS=40, and draw_building
just draws whatever exists).

Give spawn a readable reveal so the board "announces" new nodes instead
of popping them:

1. **Spawn telegraph**: soft expanding ring + brief "new connection"
   ping ~0.5 s BEFORE the node lands (cause→effect: player sees where
   the next terminal will appear).
2. **Reveal animation**: scale 0.4→1.0 + fade over ~0.4 s on the sprite
   (pure view-layer; tick-anchored so captures stay T2-stable).
3. **Placement feedback**: brief highlight on the connecting pipe
   ("this node just joined the network").
4. **Cadence pacing signal** (if the 2 s cadence stays after
   pace-tuning): vary the telegraph feel so steady streams don't
   fatigue.

## Rules (hard)

1. View-layer ONLY — the reveal must not write to sim state and must
   not change WHEN the node becomes gameplay-valid (no gameplay
   semantics change; the pop is cosmetic timing).
2. Tick-anchored for T2 stability: the animation is driven by render
   time relative to the growth tick, so golden captures at the same
   ticks stay reproducible.
3. The RATE is out of scope (pace-tuning owns it); if the rate job
   lands first, verify the reveal reads at the new cadence.
4. MM model: spawn telegraph + reveal (image_01/03/05/07); keep it
   brief — MM's reveal is a moment, not a cutscene.

## Acceptance

- Spawn capture sequence (pre→pop) shows: telegraph ring → reveal
  scale/fade → pipe highlight; no instant pops.
- Sim-validity timing unchanged (node becomes valid at the same tick);
  goldens re-blessed cause-documented if capture ticks shift.
- Local suite green.
- pr_review: 1 (Perkins before merge).

## Skills policy

bmad-quick-dev.

## Model policy

deepseek-v4-flash, --thinking max.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-spawn-feel
- base: v2
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- parallel-safe with the whole v2 visual wave (view-layer; coordinate
  reveal timing with v2-motion-readability if trails land in the same
  render pass)
- source of truth: kyle-design-directions.md §5 + design-audit.html Q4
  + captures/spawn/
