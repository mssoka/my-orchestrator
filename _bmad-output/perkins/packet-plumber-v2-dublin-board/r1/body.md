## 🤖 Perkins automated review — round 1
**Job:** packet-plumber-v2-dublin-board · **Reviewed sha:** 2f17837 · **Reviewers:** 7/7 completed (two chunk waves: code + goldens)
**Verification:** 51/52 findings confirmed against the code — 1 discarded as false-positive (the attach-vs-seed indistinguishability claim: with bias=1000 both anchors on the pool, the SEED fresh-area floor rejects every pool tile, so a dead ATTACH path fails the test's `expect(>0)` — its E31-unasserted residue was kept). 2 severity demotions applied (both blocker→warning, details inline).

Mechanical gates re-run on this head: **13/13 CI gates · 240/240 core tests · 49/49 demos (T1+T2+replay)** — the dual-run determinism proof is real, including a mutation kill on the dublin T2 golden (byte-flip → FAIL → restored → green). KYLE's board-vs-gallery PASS is carried as minion-supplied evidence per the round rules.

### Blockers (1)

**B1 — Advisory test gate: FAIL (P1 ~60–70%)** · `core/map_test.odin` · [tests]
The suite passes with entire branches deleted: the loader fixture (6 candidates, stride 6) samples one in-grid point — the **grid-filter and dedupe stages never execute** (briefing hard rule 3's "filter at bake-load" is unpinned); header pin **(b)** (district assignment + flat ranges) has **no assertions** — only fixture construction; **E31 pairwise separation is asserted nowhere**; `PP_MAP` parsing + both fallback paths have zero app coverage; `map_board_load`'s fail-loud is pinned on 1 of ~15 error paths. P0 is 100% (determinism proven) — this is a coverage-quality gate, not a suite failure.
*Fix:* extend the fixture so stride-6 samples an out-of-grid point + a snapping duplicate and assert the pool; assert `candidate_district`/`district_start`; assert pairwise E31 of grown terminals; extract + test the app map-source resolution; table-test the load error strings.

### Warnings (6)

**W1 — District-scoped ATTACH documented in three committed artifacts; the implementation is a GLOBAL street ring — and the district machinery is dead + 98.6% misgrouped** · `core/map.odin:33-36`, `demos/dublin_board.dem:5-7`, `core/map_test.odin:13` · [blind, architecture, tests, acceptance, codebase, edge — 6/7 lenses]
`map.odin` says the ATTACH family "draws from the anchor's OWN district's pool (an estate never crosses a district boundary)"; `growth.odin:532` says and implements the opposite ("The ring is GLOBAL (not district-scoped)") — the .dem header repeats the false claim. Mechanically verified on the real asset: `district_start`'s prefix-sum assumes district-grouped candidates, but candidates stay in file order → **709/719 pool tiles sit in the wrong district's range**. Zero sim consumers today (`candidate_district`, `district_start`, `pool_lo/hi`, `board_district_at` all production-dead) — but stage-2 work following `map.odin` would change replay-relevant spawn behavior, and the latent data is wrong-if-ever-used. The global-ring choice itself is right (the 63%-starvation measurement stands).
*Fix:* rewrite the three headers to the global-ring contract; either sort candidates by district at load or trim the dead machinery until a district policy lands.

**W2 — map_test header pins overstated; "pinned by tests" in the PR body is materially stronger than the assertions** · `core/map_test.odin:7-13` · [tests, architecture, blind, codebase, acceptance]
Pin (a) only exercises stride+snap; pin (b) is asserted nowhere; pin (d)'s "E31-valid" has no pairwise assertion. The PR body's "the 1-in-6 snap/dedupe/grid-filter contract" pin never runs dedupe or the grid filter.

**W3 — test_board deletes string-literal district names — invalid frees** · `core/map_test.odin:64` · [blind (demoted blocker), edge]
`odin test core` emits `+++ bad free [map_test.odin:64:test_board_destroy()]` on both dublin growth tests (tolerated by the test tracking allocator — suite stays green); the identical pattern **aborts (trap 6) under the default allocator** (probe-verified). Production is unaffected (the loader clones names). Pre-existing sibling: `health_test.odin:877`.
*Fix:* clone the fixture names or don't delete literals in the test destroy.

**W4 — map_board_load error paths after partial allocation leak the partially-built board** · `core/map.odin:319-422` · [tests, edge, codebase, blind, architecture]
After districts/candidates/render_dots are built, every later `return {}, err` (empty pool, malformed terrain/streets) discards the allocations — and these are exactly the paths the app's fallback-to-procedural takes. ODN-18.

**W5 — PP_MAP tunable + corrupt-asset fallbacks: zero app coverage** · `app/main.odin:409-435` · [tests]
Invalid-value→dublin, read-failure→procedural, load-failure→procedural — all acceptance-relevant, all untested despite the app test convention (settings/noc_toggle/pullback).

**W6 — growth_board_ring_scan's dead `t: ^Topology` + `alloc` params; ring scratch on the implicit allocator** · `core/growth.odin:537-550` · [edge, architecture, blind]
The scan uses neither param; `ring_scratch` in `growth_plan_demand` has no explicit allocator (ODN-18 discipline in core).

### Notes (12)

- **N1** `map_board_load` traps (runtime panic, not its error return) on missing/mistyped `terrain`/`streets` keys — single-value type assertions bypass both the fail-loud contract and the app's fallback (lens-verified empirically). [security]
- **N2** Teardown comments promise frees that never happen: `map_board_destroy` has zero production callers; `dublin_render_destroy` zero callers anywhere. [blind, codebase, acceptance, edge]
- **N3** `map_board_destroy` frees via the destroy-time context allocator, not the loader's `allocator` param (latent mismatch). [blind, edge]
- **N4** `board_cache`/`board_cache_loaded` are the first file-scope mutable state in the harness. [architecture]
- **N5** Dublin label cstring built twice per label per frame + hand-rolled vs the package's `strings.clone_to_cstring`. [architecture, codebase]
- **N6** `DUBLIN_LABEL_GAP` documented as world px but compared in screen space (equal only at fit zoom). [blind]
- **N7** `view.odin` calls the dublin cache a "triangulation cache" — the renderer rasterizes even-odd; no triangulator exists. [blind]
- **N8** `district_start` zero-fill loop is a no-op (`make` zeroes). [blind]
- **N9** `json_get_int` re-implements catalog's `jint`; the pool comment names nonexistent proc `map_board_candidate_pool`; lo/hi accessors orphaned. [codebase, blind, architecture]
- **N10** `map_ring_clean`/`map_line_clean` silently drop malformed points, contradicting the loader's documented fail-loud contract. [codebase]
- **N11** The T1 hash carries only the 1-byte map id — the dublin.json bytes driving every spawn carry no content hash (the replay gate catches divergence downstream; `catalog_hash` is the precedent). [acceptance]
- **N12** `dublin-shot`: prints usage() but keeps executing on bad args; exits 0 when PNG export fails. [blind, edge]

### Reviewer agreement
W1 (6/7 lenses) · W4 (5) · W2 (5) · N2 (4) · W6 (3) · W3, N5, N9, N12 (2 each)

**Verdict:** NEEDS CHANGES

The determinism spine is airtight — dual-run proven, goldens cause-documented, KYLE gate carried. What blocks is the coverage gate: the new pins claim more than they assert (B1/W2), and three committed documents describe a district-scoped ATTACH that was consciously not shipped (W1) — the exact trap for stage 2.

_Address findings and push — I re-review automatically on the new sha.
The loop runs until an APPROVED verdict._
