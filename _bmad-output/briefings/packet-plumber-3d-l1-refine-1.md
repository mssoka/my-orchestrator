# Briefing — packet-plumber-3d-l1-refine-1 (user-driven refine round)

## Source of truth

The user played the L1 look session (post-#16 lean swap) and ruled. Their
findings + KYLE corroboration are the seed list. The capture-verify loop
below completes it — your eyes on every angle, not theirs.

## User findings (the ruling)

1. **Props FLOAT / wrong orientation.** Igloos not lying down; rocks
   "not lying down, wrong orientation." The user notes the floating-asset
   issue WAS FIXED on the previous (wedge) L1 — port/unify that seating fix
   onto the continents branch staging. KYLE corroboration: SRI slab
   float+tilt, a tipped ring, UCLA-IMP label occluded by a conifer.
2. **Clouds concentrated on one hemisphere.** Confirmed by the user on BOTH
   planets now — systemic placement bias. Rebalance to spread around the
   globe.
3. **Font regression — restore + make GAME-WIDE (canon ruling).** The
   previous L1 had the nice font treatment (see the l1-topology-font lane:
   `_bmad-output/perkins/packet-plumber-3d-l1-topology-font/`); after the
   swap the font is "back to being smaller." Ruling: the font treatment is
   game-wide canon — consistent across ALL planets/levels/labels. Includes
   the small/dim text KYLE flagged (11px caption, 10-11px low-contrast
   mission log).

## KYLE-corroborated extras (secondary; fix if cheap, report if not)

- Prop density: lower hemisphere nearly prop-free; ~60% bare teal ground;
  one tree type only. The "all planets rich and colourful" canon argues for
  density spread + palette variation. Scope: spread + variation, NOT an art
  overhaul.

## Capture-verify loop (load-bearing method)

You are multimodal (glm-5.3-flash) — USE YOUR EYES:
1. Use the existing capture tooling (tools/l1_capture_runner.gd,
   capture_runner.gd) to snapshot L1 across the FULL orbit: >=12 angles,
   2 zoom tiers, day+night if cheap.
2. READ your own captures inline. Enumerate EVERY violation per angle:
   floating prop, misorientation, cloud gap/concentration, label size/occlusion.
3. Fix → re-capture → re-read until the sweep is clean.
4. The PR carries the before/after capture set + the violation checklist
   with per-item resolution.

## Riders (folded from the parked fold — one heist, one round)

- Wedge-branch igloo restore (2→0 regression; snow filter) — count-pin +
  mutation leg per the original fold briefing.
- 11 orphan texture purge (`assets/props/*.png|jpg` + `.import` sidecars
  per repo policy) with the file list in the PR body.
(The parked fold row is FOLDED into this job — Silas notes the rows.)

## Serialization

Behind PR #16's merge (build on merged main; #16 is APPROVED + user-seen).

## Acceptance

- Full-orbit capture sweep: zero floating props, all props flush with the
  surface normal, clouds spread across hemispheres (verified from >=2
  opposing angles), font treatment restored and uniform (labels + captions +
  mission log readable sizes).
- Determinism replay still byte-identical (or honestly re-blessed if the
  seating/placement math changes staged layouts).
- Wedge igloo pin + mutation leg; texture purge list in PR body.
- pr_review=1 (canon surface).

## Skills policy

- Workflow skill: bmad-quick-dev.

## Model policy

- Unset (Silas pins; ops default glm-5.3-flash — multimodal required for
  the capture-verify loop).

## Dispatch parameters

- repo: Packet-Plumber-3D
- repo_root: /Users/moses/code/Packet-Plumber-3D
- slug: packet-plumber-3d-l1-refine-1
- base: main (post #16 merge)
- pr_review: 1
- serialize: behind PR #16 merge close-out
