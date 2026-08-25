# Round context + guards — packet-plumber-v2-blender-silhouettes r1

PR: https://github.com/solarity-services/Packet-Plumber/pull/79 (base `v2`)
Reviewed sha: 2c84b85be7d44de6b7087baf1de070fbe692fce6
Diff: 4 files — `_pr_body.md` (rewritten PR body), `assets/blender/README.md`
(new), `docs/silhouette-spec.md` (new), `tools/gen_sprites.py` (reworked).
No PNGs, no `goldens/`, no `app/` code in the diff.

## Stage-1 intent (do NOT flag as missing deliverables)

This PR is a **work-start release**: pipeline + per-type silhouette spec so
the USER can launch the Blender pass themselves. **PNGs intentionally
unchanged** (the validation render was `git checkout`-reverted): committing
them now would force the T2 re-bless twice; the ruling is the wave's final
re-bless is ONE pass. The re-render + T2 re-bless land as the follow-up pass.

## What NOT to re-litigate (user rulings already made)

- The silhouette direction IS the KYLE + audit verdict (MM-minimal flat
  fills, thin dark outline, no gable step, no wash, no 3D fake) — the user
  is LIVE in Blender sculpting against this spec.
- PNGs unchanged in this PR is INTENTIONAL (stage-1).
- Merge order LAST is the standing wave ruling (scale-depth gates it) —
  APPROVED does not unlock the merge.
- KYLE §3 hue targets NOT applied (canon hexes stay; documented one-line
  swaps) — deliberate, documented in the PR body.

## The hard blocker bar (pipeline-correctness + no-runtime-drift)

`tools/gen_sprites.py` is the reviewed surface. Verify:
(a) the SILHOUETTE SPEC table drives the generic shapes deterministically
    (same input = same PNG — the golden-safe no-op claim);
(b) no app/render code touched (`app/render/sprites.odin` untouched —
    bboxes flow via `sprites.json`);
(c) the render contract (256px ortho ~66°, flat emissive sRGB→linear,
    Standard CM, no baked shadows) is implementable as specced.

## What to flag for verification (not assumed)

- The proposed asset path (`assets/blender/` + README render contract, final
  exports → `assets/sprites/` 11 pinned names) — coherent with the existing
  sprite pipeline + gitignore?
- **Order-coupling:** `app/render/sprites.odin` loads textures by its pinned
  `files[]` array (indices 6–8 = puck_1..3, 9 = small_biz, 10 = campus) but
  binds `bboxes[i]` from `sprites.json`'s `order[i]` POSITIONALLY
  (`sprites_parse_boxes`). Check what order the new `main()` emits
  (`names.append` sequence) and whether a regenerated sidecar still
  positionally matches the renderer's pinned order.
- bbox verification claims (host 0.90 portrait, campus 1.81 wide, puck
  ladder intact in the PR body's table) — these describe the UNCOMMITTED
  validation render; the committed `sprites.json` still holds the OLD
  bboxes (consistent with unchanged PNGs). Claims are checked mechanically
  by the orchestrator (Blender re-render in a sandbox), not assumed.
- `sprite_index_building` has no case for `dc` (claim in PR body + spec §1).

## Vision caveat (non-k3 round, verbatim)

Pixel verification MECHANICAL only (byte/hash/capture-diff); aesthetic
verdicts deferred for the k3 re-check; never faked. KYLE vision-verified
contact sheet = mechanical evidence; aesthetic calls belong to the
design-audit + k3 re-check.

## Repo test machinery (for the tests lens)

`tools/ci-local.sh` runs the gates (incl. T2 golden compare vs rendered
sprites + input parity). The golden corpus lives in `goldens/`; demos in
`demos/`. A tools-only diff that changes NO committed sprite byte should
leave every gate green at this sha.
