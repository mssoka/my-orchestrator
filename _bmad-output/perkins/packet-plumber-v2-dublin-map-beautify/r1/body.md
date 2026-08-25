## 🤖 Perkins automated review — round 1

**Job:** packet-plumber-v2-dublin-map-beautify · **Reviewed sha:** `6f23b31a` · **Reviewers:** 14/14 completed (7 lenses × 2 chunks; big-diff split: code / goldens+assets)
**Verification:** 28 distinct findings confirmed against the code — 9 raw findings discarded as false-positive, 19 merged as cross-lens duplicates. No lens failed (two 429 storms recovered with one continue per pane).

**Independent mechanical verification this round** (the aesthetic gate rode the mock gate + KYLE evidence on the PR; everything below re-ran in a detached worktree at the reviewed sha):
- `tools/harness.sh run` → **49/49 demos green** (T1 + T2 software pixels + replay) — sim-untouched + re-bless coherent, confirmed end-to-end.
- Parent-commit (`2809eea`) harness run of `dublin_board` → **PASS** — the old golden was NOT stale; the `catalog_hash` fold is wholly this PR's sanctioned re-extract (a lens cluster claiming a missed #93 re-bless was rejected on this evidence).
- `osm_extract.py --verify` → **byte-identical** re-bake from the mtime-preserved cache (6,030,218 bytes).
- Underlay re-bake (fresh `prep_board_geometry` → headless Blender 5.2.0/EEVEE → chunk strip, sandboxed via `PP_WT`) → **SHA-256 identical** to the committed `dublin_underlay.png` (`b6755232…`); PNG carries zero tEXt/iTXt/zTXt/tIME chunks.
- Harness refusal gate correctly scoped to Dublin demos only (`run.odin:303-311`, `dublin_shot.odin:68-73`).
- Street-window probe over all 125,860 spawn candidates: 277 have an in-range (≤3.0-tile) street the 3×3 lookup cannot see; 72 orient by a non-nearest segment; 12 have no street at all.

### Blockers (0)

None.

### Warnings (9)

- **W1 · Per-frame fallback log spam** [`blind,edge,acceptance,architecture,codebase`] — `app/render/dublin.odin:336`. The "one log line" is unguarded `fmt.printfln` inside `dublin_node_block_draw` — fires every frame per street-less node. Fix: one-shot latch.
- **W2 · Street lookup window ≠ documented radius** [`blind,edge,architecture,codebase`] — `dublin.odin:57,145-160`. 3×3 1-tile-cell scan accepts up to `DUBLIN_SEG_MAX_DIST=3.0` but can only see ~1-2 tiles; 277 pool candidates would render axis-aligned (+ trip W1) despite an in-range street; 72 orient by a farther segment. Fix: widen the ring or lower MAX_DIST to the true window reach.
- **W3 · Silent app-side underlay failure** [`architecture`] — `dublin.odin:95-101`. The header claims "loud in the log"; the `else` branch sets `underlay_ok=false` with no log anywhere in the app path. Fix: one `fmt.eprintfln` on load failure.
- **W4 · Machine-specific default path in a committed tool** [`edge,acceptance,security,architecture,codebase`] — `blender_board_build.py:15`. Default `WT` is this round's disposable worktree; a bare run writes the 9MB asset into a soon-deleted path. Fix: default to repo-root-relative.
- **W5 · `build_sea` can silently return empty** [`edge`] — `osm_extract.py:441-515`. Five unguarded `return []` paths; the exact failure mode this PR exists to fix (no sea) could regress silently on an input change. Fix: assert non-empty sea when coastline inputs exist.
- **W6 · Missing-underlay negative path untested** [`tests`] — the refusal gate is new load-bearing behavior; the fonts/sprites precedent (missing-asset-exits test) isn't met.
- **W7 · Seg-grid/block geometry has zero unit tests** [`tests`] — `dublin_node_street`, grid build, axis fallback covered only at golden level.
- **W8 · Determinism-critical bake geometry has no logic tests** [`tests`] — `--verify` proves determinism, not correctness; wrong-but-stable `build_sea`/`connect_roads` output would pass.
- **W9 · Advisory test gate: CONCERNS** [`tests`] — P0 100% (49/49 goldens) but P1 gaps on negative paths + new geometry.

### Notes (19)

N1 Dublin block path drops `reveal_fade` (pops while the chip fades) · N2 `core` `render_dots` orphaned (parse+alloc alive; only its own test reads it) · N3 dual nearest-street implementations (baked `street_blocks` unused at runtime — disclosed PR decision #3) · N4 Blender engine/version unpinned (same-machine byte-stability proven this round; cross-machine unproven) · N5 `query_nearest` tie relies on internal index order · N6 `.scratch/blender_board.png` clobbered (top-down then zoom-out) · N7 `prep_board_geometry` re-implements `layout_clusters` seed math (~30 lines) · N8 `build_boxes` `fam_idx` unused · N9 unused `Point` import · N10 mock-gate scaffolding (~half the bake file) rides the committed tool · N11 PIL preview lives under `tools/blender_board/` without using Blender · N12 block draw inverse-transforms screen→tile instead of receiving tiles · N13 `dublin_shot.odin` docstring still describes candidates/labels · N14 "no libm" comment vs `math.sqrt` · N15 no automated re-bake check for the committed asset · N16 no automated zoom-crop golden (`dublin-shot` captures both zooms ungated) · N17 re-bless cause durable only in commit/PR body · N18 8.8MB asset = 7× outlier, no LFS policy · N19 12.6MB design captures referenced only by the PR body.

### Reviewer agreement

W1 (5 lenses) · W4 (5 lenses) · W2 (4 lenses) · W7/W8 confirmed by direct test-surface grep · the sea-strip aesthetic and the spawn-pool re-extract were challenged and **rejected as false-positives** (user gate rulings + parent-commit harness PASS).

**Verdict:** READY TO MERGE

The spec's hard rules all verify mechanically: 49/49 goldens green with sim hashes untouched for procedural demos, the re-bless is scoped to the dublin_board class with cause, the bake is deterministic (JSON + underlay both re-baked byte-identical this round), labels/speckle are gone from the render path, and the sea is constructed at bake time. The 9 warnings are real but none is merge-blocking — fold W1-W5 with the test debt (W6-W8) as follow-ups or in a fix commit.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
