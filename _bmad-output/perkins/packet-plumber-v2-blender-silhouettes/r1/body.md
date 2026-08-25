## 🤖 Perkins automated review — round 1

**Job:** packet-plumber-v2-blender-silhouettes · **Reviewed sha:** `2c84b85` · **Reviewers:** 7/7 completed
**Verification:** 26/28 findings confirmed against the code — 2 discarded as false-positive

**Stage-1 verification (mechanical, Blender 5.2.0 LTS sandbox at the reviewed sha):**
- ✅ **Determinism proven**: two runs of the new script → decoded RGBA identical for all 11 sprites. The old-script no-op claim **holds exactly**: base-v2 script re-render == committed PNGs (decoded), regenerated `sprites.json` == committed sidecar; raw bytes differ only in encoder metadata, as the PR body states.
- ✅ **PR-body bbox table accurate**: host 104×116 (0.90 portrait ✓), campus 134×74 (1.81 ✓), pucks 158/180/202 wide — all 11 values reproduce.
- ✅ **No runtime drift**: `app/`, `assets/sprites/`, `goldens/` untouched vs base; PNGs-unchanged is honored (stage-1 intent respected — not a missing deliverable).
- ❌ **Order check FAILS** → blocker 1.

### Blockers (2)

**1. Regenerated `sprites.json` order mismatches `sprites.odin`'s positional texture↔bbox binding — silent corruption at the first follow-up re-render.** `[blind, edge, acceptance, architecture, codebase, tests]`
`tools/gen_sprites.py` `main()` emits `order` as `…, dc, small_biz, campus, puck_1..3`, but the renderer loads textures by its pinned `files[]` (`puck_1..3` at indices 6–8, `small_biz` 9, `campus` 10) and binds `bboxes[i]` from `order[i]` **positionally**. Verified by sandbox render: indices 6–10 cross-bind five sprites; every value still passes the value-range checks; palcheck pins palette (flat fills keep their colors under a wrong crop window), so nothing fails until the T2 re-bless **blesses the corrupted crops as the new goldens**. Fix: append `small_biz`/`campus` after the pucks (emit the pinned order), and pin script-emitted order == `sprites.odin` `files[]`.

**2. Advisory test gate: FAIL.** `[tests]` — the P0 pipeline contract (sidecar order ↔ renderer pin) has zero coverage; the "validated" evidence exists only as PR-body prose. Same root as B1; one fix commit closes both (order + a pin).

### Warnings (6)

1. **Determinism claim mis-worded in committed docs** `[blind, acceptance]` — docstring + spec §preamble say the *current* script re-renders "byte-identical to the committed sprites"; true only of the OLD script (the new geometry differs: house 84×79 vs committed 92×90…). As worded it could bait a no-re-bless commit of new PNGs. Attribute the pixel-identity proof to unchanged SPEC values / the pre-rework geometry.
2. **Outline ring width stated two incompatible ways** `[blind, codebase, acceptance, architecture, tests]` — README "footprint + ~0.03" vs spec §0 "footprint + ~0.06" vs code `fw + 2×0.03` (+0.06 total). The user is sculpting against these tables live; pick one convention in both docs.
3. **Ridge axis spec-vs-code** `[blind, architecture]` — spec §1: "ridge along the long axis"; the gable default runs it along Y = the **short** axis (0.62×0.56). A Blender sculpt to §1 lands 90° off the KYLE default.
4. **"ORTHO ~66°" contract vs 48.7–66.9° reality** `[codebase, acceptance]` — elevation = atan(10/(4.5·pad)): campus renders at **48.7°**, dc at 54.2°. Pre-existing quirk, ruled left-as-is — but "varies slightly" is a 17° spread and both contract tables state ~66° flat. State the real range.
5. **"Sculpted" fold-in path unsupported by the tool** `[edge]` — spec §2 way-2 promises "export PNGs yourself; the minion folds them in (bbox regen…)", but `main()` always re-renders and overwrites the exports, and the README forbids hand-editing `sprites.json`. Needs a bbox-only mode or a reworded promise.
6. **No durable in-repo validation artifact** `[tests]` — SPEC-table drift fails nothing until the wave-end re-bless. A harness pin on order/bbox plausibility would close the class.

### Notes (6)

1. `PUCK_TIER[ports]` KeyError trap + `{4:1,8:2,16:3}` literal duplicated at the call site `[edge]`
2. `mat_hex` silently mis-parses wrong-length SPEC hexes (slices, no length check) `[edge]`
3. Committed docs embed `/Users/moses/…` absolute paths `[security]`
4. `.blend` policy lacks the embedded-scripts auto-run caveat `[security]`
5. README export-name list cites the `sprites.odin` pin but lists a third order variant `[tests]`
6. Camera pads live outside the SPEC table; oversized footprints clip at the 256px frame edge silently (no bbox-touching-edge check) `[architecture]`

### Reviewer agreement

- Order-mismatch blocker: **6/7 lenses** (independently, before consolidation)
- Outline-ring doc conflict: **5/7** · determinism wording: 2 · ridge axis: 2 · tilt claim: 2

**Verdict:** NEEDS CHANGES

Stage-1 rulings stand (PNGs unchanged intentional; merge order LAST unchanged — an APPROVED verdict here does not unlock the merge). The blockers are one small fix commit: emit the pinned order + add the pin. A glm 429 wave hit three lenses mid-round; all recovered with one continue each — no lens ran degraded.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
