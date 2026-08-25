# R1 findings — claimed-fix audit list (Perkins r1, sha b94d54f, CHANGES_REQUESTED)

The r2 commit claims to fix B1/B2 + W1-W7 and carry/fix N1-N13. Verify each against the code at f906725.

## BLOCKERS

- **B1** — `Active_Crisis.bundle` was a compaction-prone slot index (core/types.odin:224; resolve read the stale slot after a mid-crisis demolish renumbers bundle slots — core/bundles.odin rebuilds from scratch). Claimed fix: key on the canonical (bundle_lo, bundle_hi) node pair or E11-stable member pipe id; resolve the bundle slot at eval time (`bundles_slot_for_pair` / `bundle_of_pipe`). MUST include a resolve test that exercises the demolish-and-renumber scenario.
- **B2** — test gate FAIL: (1) settled-scan positive test missing (crisis_find_saturated_bundle ok=true branch never executed), (2) backward-tick latch untested (core/step.odin:35-38), (3) byte-layout pins covered only tags 1–7 — missing drop-payload target byte + tags 8/9 + crises section pins. Claimed fix: all three pins added.

## WARNINGS

- **W1** — Pool_Exhaustion backstop class-filtered (core/crisis.odin:359-361) vs frozen "ANY Pool_Exhaustion drop this tick". Claimed: filter dropped OR frozen text amended.
- **W2** — surge.dem lacked the mid-run capacity fix + Crisis_Resolved pin in the launchable golden. Claimed: fix authored into the demo; resolve tick pinned in captures + comments.
- **W3** — frozen "pre-4.2 streams byte-identical" promise false (drop payload +4B); spec-4-2:30 + types.odin:279 + serialize.odin:358 still claimed byte-identity. Claimed: all three texts amended.
- **W4** — trigger root-cause attribution reversed the pinned slot-order definition (drop-first vs slot-order-first saturated bundle; core/crisis.odin:325-342). Claimed: attribution restored to the pinned slot-order definition OR the frozen block amended.
- **W5** — wrong-typed `archetype_id` silently loads as a pure demand event (core/catalog.odin:550-551, 821-824; `jstr` returns '' for non-strings). Claimed: explicit `json.String` type-assert; key present but non-string → named load error (ODN-5).
- **W6** — crisis engine read the ODN-14 event buffer as sim input (core/crisis.odin:143-175; app never drains). Claimed: per-tick drop-site field on `Flow_State` (or equivalent), cleared each tick.
- **W7** — test_crisis_replay_identity leaked the events array (2x256B; core/crisis_test.odin:53, 366-371). Claimed: leak fixed under the tracking allocator.

## NOTES (N1–N13)

- **N1** — step tick-latch rejects only backward ticks; equal ticks pass (core/step.odin:35-38). Claimed: `tick == state.tick` behavior now asserted/documented.
- **N2** — E13 dedup key (archetype, set_piece) coarser than arch §6.4 per-root-cause text. Claimed: carried or aligned.
- **N3** — set-piece index truncates to u16 in dedup key + serialized row; no set-piece count cap. Claimed: capped at load or carried.
- **N4** — cooldown-blocked drop branch skips settled-scan + pool backstop (core/crisis.odin:331-333). Claimed: falls through or carried.
- **N5** — resolve-margin clamp branch (bound <= margin) never executes in tests. Claimed: tiny-bound catalog case added or carried.
- **N6** — E22 drop events' target=NO_BUNDLE has no unit assertion (core/flow.odin:472,482). Claimed: asserted or carried.
- **N7** — earliest-drop attribution across multiple bundles in one tick untested (core/crisis.odin:164-174). Claimed: two-bundle same-tick fixture added or carried.
- **N8** — pool-exhaustion test comment says fix lands @1501; code draws @1500 (core/crisis_test.odin). Claimed: comment corrected.
- **N9** — Event.target comment omits the Packet_Dropped shed-bundle usage (core/types.odin). Claimed: comment extended.
- **N10** — crises_256_doc builds its 256-row doc on the tracking allocator, never frees (core/catalog_test.odin:84-97). Claimed: temp_allocator + free_all or carried.
- **N11** — harness load_catalogs crises.json read-error path has no negative test (harness/catalogs.odin:28-30). Claimed: negative case added or carried.
- **N12** — qos golden span ends mid-window (tick 1500 < 3000); post-window resolve golden-uncovered there. Claimed: carried (surge.dem covers the full window).
- **N13** — frozen resolution sentence omits the implemented hysteresis (spec-4-2 Dedup bullet + core/crisis.odin header). Claimed: both texts amended.

## DO NOT re-raise (held r1 guards + 9 false-positives)

- Held: ODN-4 read-only, ODN-7/M1 director isolation, LOG_VERSION 3, determinism spine, 4.1 wiring — clean in r1.
- r1 false-positives: cross-chunk surge.t1 artifact; catalog-fold hash rewrites (cause-documented); T2 PNG shifts (era-3 surge-active banner, cause-documented); contention/emphasis/sla re-bless (catalog-fold only, T2s untouched); "displaces t1 1" prose comment (existing pattern); crisis events not visible in T1 text (they ride the per-tick hash; pinned by unit test); catalogs_load construction-site fail-fast (all sites supply crises; suites green).
