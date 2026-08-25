## 🤖 Perkins automated review — round 2 (fix-audit)
**Job:** packet-plumber-v2-dublin-board · **Reviewed sha:** 330b952 · **Reviewers:** 14/14 completed (2 chunk waves × 7 lenses)
**Verification:** 38/45 findings confirmed against the code — 6 discarded as false-positive, 0 kept as [unverified]

### Fix audit (r1 → r2)

| r1 finding | verdict |
|---|---|
| **B1** (blocker — advisory gate FAIL, load stages unpinned) | ✅ **FIXED** — the fixture's stride now samples an out-of-grid point AND a snapping duplicate (filter + dedupe branches actually run); districts-parse test; 14-case fail-loud table + dims contract (15 paths pinned); E31 **pairwise** separation asserted; PP_MAP resolution extracted to pure procs with all four branches unit-pinned |
| **W1** (docs-vs-global-ring) | ⚠️ **PARTIAL** — map.odin + map_test.odin rewritten, dead district machinery trimmed (`candidate_district`, `district_start`, `board_district_at`, pool lo/hi). **Still present:** `demos/dublin_board.dem:5-7` (→ r2-W3) |
| **W2** (overstated header pins) | ✅ **FIXED** — headers now match the assertions |
| **W3** (fixture deletes literals) | ✅ **FIXED** — zero map_test bad-free diagnostics |
| **W4** (loader leak on error) | ✅ **FIXED** — `map_board_load_fail` destroys the partial board on every post-allocation error path |
| **W5** (PP_MAP + fallbacks untested) | ✅ **FIXED** — `map_source_from_env`/`map_source_after_load` pure procs, unit-pinned |
| **W6** (dead params/allocator hygiene) | ⚠️ **REGRESSED** — params dropped, but the `defer delete` was removed under a false temp-arena comment: now a real per-window heap leak (→ r2-W1) |
| **N1** (loader traps on mistyped blocks) | ✅ **FIXED** — two-value assertions, fail-loud, table-pinned |
| **N3** (destroy allocator mismatch) | ⚠️ **ELEVATED** — the new load_fail path + new loader tests exercise it: 10 bad-free diagnostics per suite (→ r2-W2) |
| N2, N4–N7, N9–N12 | carried as still-present notes (N8 moot after the trim) |

### Mechanical verification (this head)
- `odin test core` **242/242** · `odin test app` **42/42** · golden harness **49/49** (T1+T2+replay) · `tools/ci-local.sh --mac` **13/13 gates**
- **Dual-run holds:** `git diff v2...330b952 goldens/` = only `dublin_board.*` added — the 48 pre-board goldens are byte-untouched; the fix commit touched zero goldens/demos. T2 mutation-kill re-run: byte-flip → FAIL → restore → green.
- **Map id LOG_VERSION-safe:** T1 map byte absent-when-procedural; demo `map` directive absent=procedural, fail-loud on bad values.
- **KYLE gate rides:** the 3 side-by-side captures verified inline (k3 vision round — live vs blessed gallery matches; the ODbL credit renders bottom-left; asset attribution bytes `c2a9 OpenStreetMap contributors`).
- **Probes:** ring_scratch leak reproduced (5×32B @ growth.odin:526); destroy bad-frees reproduced (10× @ map.odin:136); saturated-yield probe fired **72×** (refuting a lens claim it never runs).

### Blockers (0)

None.

### Warnings (7)
1. **r2-W1 — ring_scratch leaks one heap array per board-run growth window** (5 lenses). The r2 fix removed `defer delete(ring_scratch)` under a false "rides the caller's TEMP arena" comment — bare appends bind the implicit heap allocator; `free_all(temp)` never reclaims it. Empirically leaking @ `core/growth.odin:526`. One-line fix (explicit temp allocator or restore the defer) + comment.
2. **r2-W2 — map_board_destroy bad-frees names/attribution when the loader's allocator param ≠ the destroy-time context.allocator** (2 lenses; carried+elevated r1 N3). Safe today (both production callers pass `context.allocator`), but the r2 `load_fail` path bakes the trap into the loader's error exit; the new fail-loud tests themselves print 10 bad-free diagnostics per run. Thread the allocator into destroy.
3. **r2-W3 — the blessed `dublin_board.dem` header still documents the REJECTED district-scoped ATTACH draw** (3 lenses; r1 W1 residual — the one artifact the fix missed). Contradicts growth.odin, the new map.odin header, and the PR body's own 63%-starvation rationale; stage-2 work reading it inherits a false replay-relevant contract. Comment-only edit, golden bytes unaffected.
4. **r2-W4 — the fail-loud loader silently accepts a missing ODbL attribution** (2 lenses). Hard rule 5 has no loader teeth: absent credit loads clean and renders nothing. Fail loud on a missing/empty `attribution`.
5. **r2-W5 — docs claim the seed's district "labels" the estate; zero labeling code exists** (1 lens). The trim deleted `board_district_at` (the only nearest-anchor proc) while the new headers + PR body claim nearest-anchor labeling. Implement the label or reword the three doc sites.
6. **r2-W6 — `map_ring_clean`/`map_line_clean` content branches have zero unit coverage** (1 lens). Every loader fixture passes empty terrain/streets; the real-asset cleaning path rides goldens only.
7. **r2-GATE-A — advisory test gate (code chunk): CONCERNS** (P0 100%, P1 ~85% — hugely improved by the B1 pins; the gaps above are the remainder). Goldens chunk gate: **PASS**.

### Notes (25)
Carried still-present: teardown-comment frees (N2), label-gap units (N6), triangulation comment (N7), json_get_int dup (N9, lo/hi half fixed), harness board_cache globals (N4), label cstring 2×/frame (N5), ring/line silent-drop (N10), T1 map-id-only hash (N11), dublin-shot arg/exit hygiene (N12).
New: mutable label tables (`:=` vs `::`), label-size derivation comment, pool-vs-dots boundary filter divergence, PR body 15-vs-14 fail-loud count, 719-vs-720 pool comment (actual 720), "defensive" continue mislabels routine flow, ±80px label cull at deep zoom, map_source proc placement, Map_Source enum unused as a type, strings_clone dup, nonexistent `map.odin's GRID_ALPHA` citation, vacuous `if step > 0`, empty-pool guard unexercised, dublin.odin zero unit pins (T2+KYLE are the sanctioned tiers), demo `map` parse errors unpinned.

### Reviewer agreement
r2-W1 ring_scratch leak (5 sources) · r2-W3 .dem header (3) · teardown comments (4 raw) · r2-W2 destroy bad-free (2) · r2-W4 attribution (2) · 719-vs-720 (2).

### Verdict
**READY TO MERGE** — r1's blocker B1 is verifiably fixed with real pins; all r1 warnings addressed or accounted for; 13/13 gates, 242+42 tests, 49/49 goldens, and the KYLE gate green on this head. The 7 warnings are advisory — none blocks the board; r2-W1/W2/W3 are the stage-2 follow-up's first candidates.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
