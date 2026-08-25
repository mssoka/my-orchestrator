## 🤖 Perkins automated review — round 1 (cap lifted — loop until approved)

**Job:** packet-plumber-v2-5.9-demand-caps · **Reviewed sha:** `2314a22` · **Reviewers:** 7/7 completed
**Verification:** 29/29 findings confirmed against the code — 0 discarded as false-positive

**The contracts — verified directly (the card's pinned acceptances as acceptance audit):**

- **Accumulator contracts ✅** — `spawn_credit_milli[terminal_slot]` in `Flow_State` beside `lane_caps` (flow.odin:98-110), updated IN PLACE by the §1b spawn pass; **derived + NEVER serialized** (zero references in serialize.odin; the only T1 surface is the gated spawn stream); integer-only with `jint_strict` fail-fast (1..1000, decimal/missing/out-of-range all rejected — 5 negative rows in catalog_test); accrue = `cap_fraction_permille × throughput ÷ packet_bandwidth` milli/tick (83 res / 1333 host ✓); cost 1000, pickable ≥ 1000, `MAX_CREDIT_MILLI = 1000 × max(1, ceil(cap))` type-relative (1000/2000 ✓); `500` in balance.json.
- **Credit-gated eligibility ✅** — the eligible set is rebuilt LIVE per pick (consumption moves terminals out mid-tick), the gating filters BEFORE the draw so **ONE rng draw per pick [ODN-10]** holds; the §1a `flow_seed_demand` path is untouched (N9); era-0 accrual is gated off (empty plan → no credit state, no rng — `test_era0_legacy_no_rng_draws` intact).
- **E24 ✅ real, not vacuous** — the pin at `sla_test.odin:88` (`sla_check_invariant`, called per tick by `sla_record_run`) is exercised by the new `test_sla_credit_gated_skip_not_demand_e24` under BOTH paths in one run: skip path (demand_seen < 500 of ~1200 attempted), pool-drop path (`flow_try_spawn` flow.odin:522 counts demand+drop), and the final identity on both classes.
- **W10 ✅ non-vacuous** — the fixture fix is real: `sla_draw` wires existing node ids (r0=0, router=1, r2=2), `!s.replay_error` guards every new fixture test, `delivered > 0` + avg ≤ 500 ms + `per_term[r0] >= 40` liveness all asserted.
- **Re-pins ✅ structural** — exact seed-pinned volumes + POSITIVE (per-terminal bounds) + NEGATIVE (max ≤ 2/tick burst) in demand_test/flow_test/determinism_test; collateral re-pins (crisis/health/node_health/stats) are cause-commented and preserve intent.
- **Surge re-validation ✅ together** — `test_w9_surge_lands_under_caps` drives era-3 + growth (40) + ×10 in ONE run with ≥ 8 growth-born hosts required.
- **Re-bless (4.3) ✅ byte-verified by me** — all 31 `.log.bin` differ from base ONLY at bytes 17..24 (the 8-byte catalog_hash field; byte 22 coincidentally equal); the PNG set is exactly the 29 documented frames incl. the `growth/05500ms.png → 01500ms.png` rename; `catalog_hash` rides inside every per-tick state hash (serialize.odin:111) so the all-lines .t1 shift is the mechanical fold; era-0 demos are sim-inert by construction.
- **Local suite ✅ independently re-run at the reviewed sha: 9/9 gates green** (GitHub Actions billing-block is not a signal, per dispatch).
- **7.1 lane ✅** — no finding requires further T2 churn; all fixes are comments/tests, no golden impact.

### Blockers (0)

None. The accumulator honors its invariants; E24 is real; W9/W10 bite; the re-bless cause chain is sound.

### Warnings (7)

1. **W9 pin scope dilution** [tests, edge, acceptance, architecture, codebase] — `core/demand_test.odin:426-470`: `stream_spawned`/`per_host_spawns` accumulate over ticks 1..3000 while `MIN_LAND` (17,100) and the per-host bound are window-sized — the pinned ×0.95 is effectively ×0.88 in-window. Still decisively non-vacuous (a silent non-landing lands ~3–5k total), but the card says 0.95. Fix: gate the counters on `tick >= SURGE_START`.
2. **growth.dem:7 stale `GROWTH_INTERVAL_TICKS = 120`** [blind, architecture, codebase] — two lines below the re-tune note. (Same miss at `core/node_health_test.odin:286` — "3 growth windows (120 ticks each)".)
3. **warn.dem "golden-verified stream" narrative still pins the pre-5.9 numbers** [blind, codebase] — Node_Congested @1 / Node_Critical @2 is now @2 / @4 at the re-tuned 1/tick (your own node_health_test re-pin documents the new numbers).
4. **crisis re-pin comment self-contradicts** [blind] — `core/crisis_test.odin:328`: "arrival 2.67/tick < the post-fix service 2.67/tick" — the service is 2.83/tick (two wides, per the helper comment). Events are exact; the cause-chain number is a typo.
5. **`cap_fraction_permille` ∈ [1,5] truncates residential accrual to 0** [edge] — `f×5÷30 = 0` → the type is permanently spawn-ineligible INSIDE the validated 1..1000 range, silently. Consider a load fail-fast when any type's accrual truncates to 0 with fraction > 0.
6. **health_test latency-enter check is guarded by `win_delivered > 0`** [tests] — can silently skip; mitigated by the unconditional `breach[0]` assertion above it. Add an explicit `win_delivered > 0` expect (the W10 pattern).
7. **`throughput_units` unvalidated, now feeds wrap-prone u32 credit math** [security] — pre-existing load (`jint`, default 0, no bounds) with a NEW state-math consumer; negative/huge values wrap. Low practical risk (shipped catalogs + T1 coverage); ODN-5 would bound it.

### Notes (11)

1. **W10 header says "the sink (id 3)" — actual sink is id 2** [blind, acceptance, architecture, codebase] — the fixture fix corrected the draw, not the prose (`demand_test.odin:495`).
2. **Seed attribution inconsistency** [blind, codebase] — the constants block says seed 7; the surge test's inline comment says "seed 42 exact count below" but runs seed 7 (`demand_test.odin:307`).
3. **health_lose.dem / health_win.dem narratives still cite pre-5.9 volumes** [codebase] — "2 streaming/tick", "20 streaming/tick x 60 u".
4. **surge.dem credits the capped 1.33/tick arrival with "overwhelms the wides' service"** [blind] — the re-fire @2401 is real (golden + capture) but the mechanism is the drained-backlog flood (as crisis_test documents); wording only.
5. **health hysteresis band comment still cites the loss band (27, 30]** [blind] — after the latency re-pin (500/460 ms).
6. **The `!okd` dst-fail path burns 1000 credit with no spawn** [blind] — consistent with the documented ask-semantics; name the sub-case in one comment line.
7. **§1b scratch arrays never deleted** [architecture] — `e_ids/e_w/e_slots` skip the file's temp-scratch delete discipline (harmless at free_all-per-tick).
8. **`crisis_catalog_mult2`'s `volume = 1` is now a no-op** [blind] — the test catalog already mirrors the re-tune.
9. **node_health_test.odin:286 "120 ticks each"** [architecture] — folds into warning 2.
10. **growth-born cause-chain pin skips `waiting_ticks == 0` same-tick arrivals** [tests] — one-tick hole in the replacement pin.
11. **Advisory test gate: PASS** [tests] — P0 behaviors all carry direct pins incl. non-vacuity guards.

### Reviewer agreement

The W9 scope dilution (warning 1) was found independently by **5 of 7 lenses** — highest-confidence signal; the one-line fix tightens the pin to the card's exact 0.95. The growth.dem staleness drew 3 lenses; the W10 "(id 3)" prose drew 4.

**Verdict:** READY TO MERGE

The contracts hold — warnings are polish (test-pin precision + doc-narrative sweep), none block. The warnings above are carried for the minion's next card or a follow-up commit at your discretion; they do not require another round.

_Address findings and push — I re-review automatically on the new sha._
