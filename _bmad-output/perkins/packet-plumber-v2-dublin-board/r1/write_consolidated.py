import json

consolidated = {
  "job": "packet-plumber-v2-dublin-board",
  "round": 1,
  "pr": 93,
  "reviewed_sha": "2f17837a79f339cac5470944b204bebb31b592bd",
  "chunking": "diff 3926 lines > 3000 — chunk A (code, 2101) + chunk B (goldens, 1825), one lens wave each, findings merged",
  "mechanical_verification": {
    "core_tests": "240/240 PASS",
    "golden_harness": "49/49 demos green (T1 + T2 + replay), exit 0",
    "t2_mutation_kill": "byte-flip in dublin 90000ms.png golden -> FAIL caught -> restored -> green (the T2 compare is real)",
    "ci_local_mac": "13/13 gates PASS, exit 0",
    "district_ranges": "district_start prefix-sum misgroups 709/719 (98.6%) pool tiles on the real asset (latent — zero sim consumers)",
    "router_tiles_on_pool": "(20,15) and (16,12) are pool tiles: True",
    "delete_literal_probe": "delete on string literal: abort under default allocator (odin run, trap 6); tolerated as '+++ bad free' diagnostics under the test tracking allocator (odin test passes)",
    "attribution_bytes": "asset attribution = c-a9 'OpenStreetMap contributors', UTF-8 lead 0xC2 0xA9 matches the renderer's check"
  },
  "failed_layers": [],
  "lens_waves": {"A": "7/7 (edge 429-rate-limited once, one retry succeeded)", "B": "7/7 (5 honest empties on blessed-data chunk + tests gate PASS)"},
  "raw_findings": 52,
  "verification": {
    "confirmed": 51,
    "rejected": 1,
    "rejected_detail": "tests 'attach test cannot distinguish ATTACH from SEED' — central mechanism refuted: with bias=1000 and both seed anchors on the pool, no pool tile passes the SEED fresh-area floor (>=10 tiles from EVERY terminal; the pool spans 26 tiles wide), so a dead ATTACH path yields zero spawns and the test's expect(>0) fails. Residue (E31 pairwise unasserted) merged into W2.",
    "demotions": [
      "blind blocker 'test_board deletes string literals' -> warning: the test-regime tracking allocator tolerates the invalid frees (suite green); abort occurs only under the default allocator; production loader clones names correctly",
      "blind blocker 'district scoping contradiction' -> warning: behavior correct + accurately documented in growth.odin and the PR body; the defect is the contradictory committed docs"
    ]
  },
  "blockers": [
    {
      "id": "B1",
      "sources": ["tests"],
      "category": "coverage-gate",
      "title": "Advisory test gate: FAIL — P1 coverage ~60-70% despite 'pinned by tests' claims",
      "location": "core/map_test.odin",
      "evidence": "map_test fixture: 6 spawn_candidates with MAP_SPAWN_STRIDE 6 -> only index 0 sampled (stride+snap only; grid-filter + dedupe branches never execute). Header pin (b) (district assignment + ranges) has no assertions — only fixture construction. E31 pairwise separation asserted nowhere. PP_MAP parsing + read/load fallbacks untested in app. map_board_load fail-loud pinned on 1 of ~15 error paths.",
      "detail": "P0 100% — dual-run determinism mechanically proven (48 procedural goldens byte-identical + dublin_board T1/T2/replay green, mutation-killed T2 compare). P1 gaps real and verified; two header pins are partly/entirely false. Chunk-B gate: PASS (goldens data verified by harness).",
      "recommended_fix": "Extend the loader fixture so stride-6 samples an out-of-grid point and a snapping duplicate; assert candidate_district + district_start; assert pairwise E31 separation of grown terminals; extract + test app map-source resolution; table-test load error strings.",
      "verification": "confirmed"
    }
  ],
  "warnings": [
    {
      "id": "W1",
      "sources": ["blind", "architecture", "tests", "acceptance", "codebase", "edge"],
      "category": "doc-consistency",
      "title": "District-scoped ATTACH documented in three committed artifacts; implementation is a GLOBAL street ring — and the district pool machinery is dead + 98.6% misgrouped",
      "location": "core/map.odin:33-36; demos/dublin_board.dem:5-7; core/map_test.odin:13",
      "evidence": "map.odin: 'the ATTACH family draws from the anchor's OWN district's pool (an estate never crosses a district boundary)' vs growth.odin:532: 'The ring is GLOBAL (not district-scoped)' (implementation matches growth.odin). dublin_board.dem header repeats the false claim. Mechanically: district_start prefix-sum assumes district-grouped candidates but candidates stay in file order -> 709/719 tiles in the wrong district's range on the real asset; zero sim consumers (map_board_pool_lo/hi, candidate_district, board_district_at all production-dead).",
      "detail": "The global-ring choice itself is right (PR documents 63% starvation under district scoping) — but stage-2 work following map.odin or the blessed .dem header would change replay-relevant spawn behavior, and the latent district data is wrong-if-ever-used.",
      "recommended_fix": "Rewrite the map.odin paragraph, .dem header, and test header to the global-ring contract; either fix district_start grouping (sort candidates by district at load) or trim the dead district machinery until a district-scoped policy lands.",
      "verification": "confirmed"
    },
    {
      "id": "W2",
      "sources": ["tests", "architecture", "blind", "codebase", "acceptance"],
      "category": "coverage-gap",
      "title": "map_test header pins overstated: (a) only stride+snap executes; (b) district pins asserted nowhere; (d) E31 pairwise never asserted",
      "location": "core/map_test.odin:7-13",
      "evidence": "Header claims '(a) stride -> snap -> grid filter -> dedupe', '(b) the district assignment ... + the flat per-district ranges', '(d) ... E31-valid'. Fixture: 6 candidates / stride 6 = 1 sampled in-grid point; district code is fixture CONSTRUCTION only; no pairwise separation assertion in any dublin test. PR body: 'New unit pins: the 1-in-6 snap/dedupe/grid-filter contract' — the dedupe/grid-filter half never runs.",
      "detail": "The suite passes with the filter/dedupe branches and district logic deleted; the PR's 'pinned by tests' claim is materially overstated.",
      "recommended_fix": "Assert what the headers claim (see B1 fix) or correct the headers + PR claims.",
      "verification": "confirmed"
    },
    {
      "id": "W3",
      "sources": ["blind", "edge"],
      "category": "invalid-free",
      "title": "test_board deletes string-literal district names — invalid frees (bad-free diagnostics today, abort under a default allocator)",
      "location": "core/map_test.odin:64",
      "evidence": "test_board appends Map_District{name=\"A\"/\"B\"} (literals); test_board_destroy: for d in districts { delete(d.name) }. odin test core output: '+++ bad free @ ... [map_test.odin:64:test_board_destroy()]' on both dublin growth tests (tolerated, suite green). Probe: same pattern aborts (trap 6) under odin run's default allocator. Pre-existing sibling: health_test.odin:877.",
      "detail": "Test-only defect (production loader clones names — map_board_destroy deletes heap clones correctly); one allocator-regime change away from crashing the suite.",
      "recommended_fix": "Clone the fixture names (make+copy, like strings_clone) or skip delete for literals in test_board_destroy.",
      "verification": "confirmed (demoted from blocker)"
    },
    {
      "id": "W4",
      "sources": ["tests", "edge", "codebase", "blind", "architecture"],
      "category": "leak-on-error",
      "title": "map_board_load error paths after partial allocation leak the partially-built board",
      "location": "core/map.odin:319-422",
      "evidence": "After districts/candidates/render_dots are allocated, later failures (empty pool, malformed terrain/streets) 'return {}, err' with no map_board_destroy(&b); only snapped/counts are deferred. App falls back to procedural on these errors — the partial board leaks per failed boot.",
      "detail": "ODN-18 arena discipline; tracking-allocator CI would flag it if the paths were exercised (they aren't — see B1).",
      "recommended_fix": "defer-if-err map_board_destroy(&b) or destroy before each error return after allocations begin.",
      "verification": "confirmed"
    },
    {
      "id": "W5",
      "sources": ["tests"],
      "category": "coverage-gap",
      "title": "PP_MAP tunable parsing + corrupt-asset fallbacks have zero app coverage",
      "location": "app/main.odin:409-435",
      "evidence": "PP_MAP branches (invalid value -> dublin default; read failure -> procedural; load failure -> procedural) untested; CI gate 2 runs app unit tests and the app test convention exists (settings/noc_toggle/pullback).",
      "detail": "Acceptance-relevant ('tunable flip', graceful fallback) yet unpinned.",
      "recommended_fix": "Extract map-source resolution into a pure proc (env string + loader outcome -> source/board_ok) and unit-test all four paths.",
      "verification": "confirmed"
    },
    {
      "id": "W6",
      "sources": ["edge", "architecture", "blind"],
      "category": "api-hygiene",
      "title": "growth_board_ring_scan declares unused t: ^Topology and alloc params; ring scratch uses the implicit context allocator",
      "location": "core/growth.odin:537-550",
      "evidence": "Signature: proc(board, t: ^Topology, anchor, sep, radius, ring, alloc := context.temp_allocator) — body references neither t nor alloc (appends via ring's implicit allocator); ring_scratch in growth_plan_demand is a bare dynamic with no explicit allocator (ODN-18 explicit-allocator discipline in core).",
      "detail": "Dead params imply a topology dependence the scan doesn't have; allocator intent bypassed.",
      "recommended_fix": "Drop t and alloc (or thread alloc into the appends); give ring_scratch an explicit allocator.",
      "verification": "confirmed"
    }
  ],
  "notes": [
    {"id": "N1", "sources": ["security"], "title": "map_board_load traps (runtime panic) on missing/mistyped terrain or streets keys — bypasses the fail-loud error + app fallback", "location": "core/map.odin:409-421", "severity": "note", "verification": "confirmed (lens verified empirically: 'Invalid type assertion from Value to Object' abort)"},
    {"id": "N2", "sources": ["blind", "codebase", "acceptance", "edge"], "title": "Teardown comments promise frees that never happen: map_board_destroy has zero production callers; dublin_render_destroy zero callers anywhere", "location": "app/main.odin comment + app/render/dublin.odin:75", "severity": "note", "verification": "confirmed by grep"},
    {"id": "N3", "sources": ["blind", "edge"], "title": "map_board_destroy frees via the destroy-time context allocator, not the loader's allocator param (latent mismatch)", "location": "core/map.odin:167-186", "severity": "note", "verification": "confirmed by inspection"},
    {"id": "N4", "sources": ["architecture"], "title": "board_cache/board_cache_loaded introduce the first file-scope mutable state in the harness", "location": "harness/catalogs.odin:85-106", "severity": "note", "verification": "confirmed by grep (no other package-level mutable state in harness)"},
    {"id": "N5", "sources": ["architecture", "codebase"], "title": "dublin label cstring built twice per label per frame + hand-rolled copy vs the package's strings.clone_to_cstring helper", "location": "app/render/dublin.odin:385-415 vs noc_overlay.odin:514-519", "severity": "note", "verification": "confirmed by read"},
    {"id": "N6", "sources": ["blind"], "title": "DUBLIN_LABEL_GAP documented as world px but anchor distances compared in screen space (equal only at fit zoom)", "location": "app/render/dublin.odin:63-65 + dublin_draw_labels", "severity": "note", "verification": "confirmed by read"},
    {"id": "N7", "sources": ["blind"], "title": "view.odin calls the dublin cache a 'triangulation cache' — the renderer rasterizes even-odd; no triangulator exists", "location": "app/render/view.odin:87-89", "severity": "note", "verification": "confirmed in diff"},
    {"id": "N8", "sources": ["blind"], "title": "district_start zero-fill loop is a no-op (make() already zeroes)", "location": "core/map.odin:392-394", "severity": "note", "verification": "confirmed by read"},
    {"id": "N9", "sources": ["codebase", "blind", "architecture"], "title": "json_get_int re-implements catalog's jint; pool accessor comment names nonexistent proc 'map_board_candidate_pool'; lo/hi accessors orphaned", "location": "core/map.odin:426-450 vs core/catalog.odin:484", "severity": "note", "verification": "confirmed by grep"},
    {"id": "N10", "sources": ["codebase"], "title": "map_ring_clean/map_line_clean silently drop malformed points — contradicts the loader's documented fail-loud contract", "location": "core/map.odin:196-260", "severity": "note", "verification": "confirmed by read"},
    {"id": "N11", "sources": ["acceptance"], "title": "T1 hash carries only the 1-byte map id — the dublin.json bytes driving every spawn carry no content hash (replay gate catches divergence downstream; catalog_hash precedent)", "location": "core/serialize.odin:121-128", "severity": "note", "verification": "confirmed by read"},
    {"id": "N12", "sources": ["blind", "edge"], "title": "dublin-shot: usage() printed but execution continues on bad args; verb exits 0 when PNG export fails", "location": "harness/main.odin:97-101 + harness/dublin_shot.odin:45-48", "severity": "note", "verification": "confirmed in diff"}
  ],
  "reviewer_agreement": ["W1 (6 sources)", "W4 (5 sources)", "W2 (5 sources)", "N2 (4 sources)", "W6 (3 sources)", "W3 / N5 / N9 / N12 (2 sources each)"],
  "verdict": "NEEDS CHANGES",
  "verdict_rule": "1 blocker (1-3 band) -> --request-changes"
}

with open('/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-board/r1/consolidated.json', 'w') as f:
    json.dump(consolidated, f, indent=1)
print("consolidated.json written")
print("blockers=%d warnings=%d notes=%d" % (len(consolidated['blockers']), len(consolidated['warnings']), len(consolidated['notes'])))
