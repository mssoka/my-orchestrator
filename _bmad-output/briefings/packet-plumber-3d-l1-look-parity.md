# Briefing — packet-plumber-3d-l1-look-parity (v2 — AMENDED per user steering)

## Amendment (2026-09-06, user)

User ruling, completed: "have L1 **use the planet we want. then we can
refine. once I see that.**" — Do NOT rework the wedge branch's look. L1
switches to the flagship CONTINENTS planet (the one from the look-pass
captures, all assets already in place). This job is the SWAP; refinement is
a LATER round driven by the user's reaction after they see it.

## Task (lean swap — nothing rebuilt)

1. **Switch L1's map kind to the continents branch.** L1 renders the same
   seeded continents world the flagship captures showed. The wedge map kind
   stays in the codebase untouched (other authored levels may use it).
2. **Authored campus placement on the new world.** The four ARPANET sites
   (UCLA / SRI / UCSB / Utah) get deterministic authored positions on the
   continents world (fixed seed; sites on land, sensible spread). Their IMP
   nodes, labels, and the intro card ("1969 · ARPANET") unchanged.
3. **Igloos: free, not rebuilt.** The continents branch already stages the
   snow-band igloos (r6-verified: 3 staged, in-band). L1 inherits them.
   (The fold's wedge-branch igloo fix remains valuable for the wedge kind —
   it is NOT this job's concern.)
4. **Determinism contract.** L1 replay/capture baselines change — re-bless
   per the local-goldens canon; byte-identity replay re-proven; inventory
   note in the PR body.
5. **GDD rider (short paragraph):** "All planets rich and colourful — every
   level's planet wears the flagship look language. L1 renders the flagship
   continents world." (user rulings 2026-09-06)
6. **Clouds/palette: NO tuning this round.** The continents planet already
   looked right in captures. Refinements (cloud spread, composition,
   palette) wait for the user's eyes on the real thing.

## Refine-later doctrine (load-bearing)

This PR is "make L1 use the right planet." It is NOT a polish pass. Keep the
diff lean; expect a user-driven refinement round after they play it. Do not
gold-plate.

## Serialization — unchanged

Held behind the fold (pHC) merge close-out: same files
(level_manifest.gd / world_seed.gd / l1_arpanet.gd — collision guaranteed
pre-merge). Release = resolve fresh main head, then dispatch.

## Acceptance

- Multi-angle orbit captures: L1 gameplay (intro card, 4 IMP campuses,
  cable verb) ON the continents planet with its oceans/green/igloos.
- Determinism replay byte-identity at the new world; baselines re-blessed.
- GDD rider paragraph in the PR.
- Lean diff — swap, not rebuild.
- pr_review=1 (canon surface: level worldgen + baselines).

## Skills policy

- Workflow skill: bmad-quick-dev.

## Model policy

- Unset (Silas pins at dispatch; ops default).

## Dispatch parameters

- repo: Packet-Plumber-3D
- repo_root: /Users/moses/code/Packet-Plumber-3D
- slug: packet-plumber-3d-l1-look-parity
- base: main (post fold-merge)
- pr_review: 1
- serialize: behind packet-plumber-3d-alive-planet-fold merge close-out
