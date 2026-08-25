## 🤖 Perkins automated review — round 1
**Job:** packet-plumber-v2-blender-sculpt · **Reviewed sha:** 0137f92 · **Reviewers:** 7/7 completed
**Verification:** 30/31 findings confirmed against the code — 1 discarded as false-positive

**Blocker-bar audit (independently re-run, not taken from the PR body):**
- **Sim untouched ✓** — golden diff is PNG-only (111 files, zero `.t1`/`.log.bin`); full harness at this sha: **48/48 green** (T1 + T2 + replay).
- **Determinism ✓** — re-ran the pipeline twice from the committed `.blend` sources: run A **byte-identical to the committed** PNGs + `sprites.json` (sha256), run B byte-identical to run A.
- **IP ✓** — `.blend`s verified: sculpted geometry only, no embedded image bytes, no text blocks/scripts; sprites read as original low-poly masses.
- **W5 ✓** — guard + 8 bite-legs + CI gate 7b green; the real clip (puck pad 0.95→1.15, ≥13px margins) checks out against committed bboxes. **W4 partial** — see Warning 1 (doc-only; renders unaffected).
- Gates 7/7b run in `tools/lint.sh`, which CI runs (`ci.yml`); both green here.

### Blockers (0)

None.

### Warnings (8)

1. **W4 tilt labels stale after the W5 pad bump** [blind, edge, acceptance, architecture, codebase, tests] — `tools/gen_sprites.py:190-192`, `assets/blender/README.md:46`, `docs/silhouette-spec.md:40`, `_pr_body.md` — every doc says "pucks ≈65° STEEPEST, range 47–65°", but at the committed pad 1.15 pucks render **60.8°** and **house (61.4°) is actually steepest**; committed range is 47.3–61.4°. 65.0° is the pre-bump pad-0.95 number. Re-measure and relabel (doc-only — camera is computed from pad in code; re-render proven byte-identical).
2. **Gate-7 negative self-test is vacuous** [blind, acceptance, architecture, tests] — `tools/test_sprite_order.py:62-70` — `mutated` never passes through the so/of/jo comparator and `mutated == of` can never be true, so the claimed "comparator must BITE" fold is decorative; a comparator regression still passes CI. Feed the mutated list through a real comparison helper.
3. **House recolor silently skips missing material slots** [edge, architecture] — `tools/gen_sprites.py:249-252` — `if m is not None` (needed for house's absent-by-design `fill_hip`) also hides missing-by-accident slots: stale coral face ships with every gate green (bbox guard is alpha-only). Assert the family's full contract slot list when a colorway is set. Committed `.blend` verified correct today — latent drift risk.
4. **Puck tier solo walks only direct collection children** [edge, architecture] — `tools/gen_sprites.py:242-245` — root-level or nested objects escape the hide loop and render into every tier, passing the W5 guard. Committed `puck.blend` verified clean (tiers are the only children) — latent. Walk recursively + scene-root objects, or assert the root shape.
5. **`.blend`s embed `/Users/moses/...` paths** [security] — all 6 binaries carry wip-render filepaths + browser recents (zstd-decompressed) — the exact leak class the N3 fold scrubbed from docs. Clear render filepath + recents, resave, re-verify determinism.
6. **Auto-run defense is policy, not enforcement** [security] — README notes auto-exec "must stay OFF", but the documented invocation is bare `blender -b -P` and nothing pins `use_scripts_auto_execute` before `open_mainfile` — protection depends on each runner's preference state while the pipeline reads committed opaque binaries (current files verified script-free). Pin `--disable-autoexec` + set the pref in-script.
7. **`strip_png_metadata` has zero automated coverage** [tests] — `tools/gen_sprites.py:205-230` — the determinism-critical chunk stripper is proven only by one-off manual double-runs; extract to `sprite_guard.py` + a gate-7b leg (synthetic PNG → tEXt/iTXt/zTXt stripped, IDAT intact).
8. **Advisory test gate: CONCERNS** [tests] — P0 100%, P1 ≈86% (order pin partial via W2, byte-determinism manual-only), overall ≥80%. Warnings 2+7 lift P1 ≥90%.

### Notes (10)

1. Hash-named external JPG residue (8 refs/blend, no bytes ship, not a live datablock) — purge + document provenance [security]
2. `eval` with full builtins on the SPEC AST in `test_sprite_foldin.py:50` [security]
3. Puck tier solo map unpinned — assert the 132/150/168 bbox ladder in gate 7b [tests]
4. Unused `import math` at `gen_sprites.py:70` [blind, codebase]
5. README Materials row has 3 cells in a 2-column table [blind]
6. Docstrings say "lint gate 7" where lint.sh wires gate 7b [blind, codebase]
7. Shadow offset documented "∝ footprint" but floored at 2.5/3px (houses sit at the floor) [blind]
8. "round 1" = both a rejected and a user-approved round in `silhouette-spec.md` [blind]
9. Solo blanket-unhides the kept tier (ignores sculptor hide state) [edge]
10. README references `wb_camera(pad)` which exists nowhere (0 cameras in all 6 .blends) [codebase]

### Reviewer agreement
- W4 label staleness: **6/7 lenses** independently (top-confidence finding of the round)
- Vacuous negative self-test: 4/7 lenses
- Recolor silent-skip: 2/7 · Solo-walk hole: 2/7 · dead `import math`: 2/7 · gate 7/7b label: 2/7

**Verdict:** READY TO MERGE

Round notes: lens wave launched on `kimi-coding/k3` → 403 billing-cycle cap; relaunched on the briefing-chain fallback `zai-coding-cn/glm-5.3` (pin verified), with a 429 recovery continue on 3 panes. All 7 lenses delivered; no degraded verdict.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
