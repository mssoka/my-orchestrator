# packet-plumber-v2-look-polish

## Task

Raise the v2 game's visual quality to the Mini Motorways look bar that
UE slice-1 established — the user played the UE slice-1 build and was
underwhelmed ("doesn't look as good as expected out of the box");
direction is now ODIN FOCUS. This job is the answer: make the Odin
build look genuinely good.

Look target (the bar, from UE slice-1 + established canon):
- Warm palette: warm-cream background, amber accents, gray-blue system
  tones (NOT PBR, NOT realistic — UAD-22 anti-PBR doctrine, see
  ../packet-plumber-ue/docs + its UAD-22 references)
- Ribbon-style roads (thick, rounded, layered under nodes)
- Soft shadows / gentle depth separation between layers
- Clean node/building shapes; readable packet dots with satisfying
  motion (the 7.1 easing work is the base — do not regress it)

Base your pass on: current v2 view layer (post 7.1 visual-juice,
wire-aesthetics r1, background-maps). Reference frames: UE slice-1
golden screens live in ../packet-plumber-ue/docs/goldens/screens/ (read
only — match the FEEL, don't pixel-copy a different renderer).

## Hard constraints

1. PRESENTATION-ONLY. The sim spine, serialization, LOG_VERSION, packet
   contracts, routing semantics: UNTOUCHED. If a change needs sim
   behavior to change, it's out of scope — note it in the PR instead.
2. The user is ACTIVELY PLAYING this build (`odin run app`). Every push
   to the branch must leave the build compiling and runnable. No
   "broken intermediate" pushes.
3. All existing tests/gates stay green. If look changes break a golden
   capture test, re-bless deliberately with the same honest process
   used before (tick_nonce etc.) and say so in the PR.
4. Performance: the game runs at 60fps on a laptop — keep it there
   (state your measured before/after in the PR).

## Deliverables

- PR to v2 with the polish pass, broken into reviewable commits
  (palette / roads / shadows-depth / node+packet polish suggested)
- BEFORE/AFTER golden frames embedded in the PR body (same scenario
  seed both sides), plus one side-by-side vs a UE slice-1 reference
  frame
- PR body includes the lavish artifact (use the lavish skill: rich HTML
  with the before/after gallery) — the user judges looks with eyes
  before merge; the bake-off criterion is looks, and the human is the
  judge

## Skills policy

bmad-quick-dev (workflow), lavish (the before/after gallery in the PR
body).

## Model policy

deepseek-v4-flash, --thinking max.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: v2-look-polish
- base: v2
- model: deepseek-v4-flash
- pr_review: 1 (visual/canon surface)
- note: UE slice-2 dispatch is PARKED (user ruling 08-21 — Odin focus);
  this job rides instead
