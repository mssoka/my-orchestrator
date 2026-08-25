## 🤖 Perkins automated review — round 2 of 3

**Job:** packet-plumber-v2-3.1-packet-types · **Reviewed sha:** `abe578b` · **Reviewers:** 14/14 completed (7 lenses × 2 chunks — diff 4620 lines exceeded the big-diff threshold: chunk 1 code+catalogs 1805 lines/18 files, chunk 2 goldens 2815 lines/30 files; findings merged before verification)
**Verification:** 11/12 unique findings confirmed against the code (27 raw lens reports deduped) — 1 discarded as carry-forward false-positive, 0 kept as [unverified]

**r1 fix audit (13/13 findings):** 12 fixed correctly + verified this round (table-driven fail-fast suite `test_catalogs_load_failfast` — 43 rows incl. the color-rgba element, lane-256-wrap, negative-tick, duplicate-era, decimal-sim-field rows; `!okc` color guard; pre-cast lane/weight range checks at both sites; i32 tick validation before the u64 casts; `demand_weight` bounds in both loaders; `weighted_pick_excluding` suite — determinism + all-excluded ⇒ ok=false + zero-weight; `bad_era` drift mutation with the divergence assertion — drift-check 62/62 rejected; duplicate-era fail-fast (`seen: [64]bool`); `fmt.aprintf` T2 fail strings; corrected `weighted_pick` comment; `expect hash stable` in `qos.dem`). **One fix landed WRONG** (warning #3 below) and **one is incomplete** (warning #1 below).

**Ground truth at `abe578b` (re-verified independently this round):** `odin test core` **61/61 green** · `harness run` **9/9 green** — incl. the `qos` era-3 golden, 1500 ticks, replayed bit-for-bit through the ODN-11 gate · `drift-check` **62/62 mutations rejected** across 9 demos (incl. the new `bad_era` divergence class) · `tools/lint.sh` **5/5 gates green**. Load-bearing invariants hold: **distinct shapes** (email=circle / streaming=triangle — never color alone ✓), **spawn determinism [E10]** (one seeded Lemire draw per pick inside the deterministic stream; era-0 legacy runs draw zero rng ✓), **director read-only [ODN-7]** (`scripted_plan_pressure` receives only cat/era/tick — no topology handle at all ✓), **core engine-free [ODN-1]** ✓, **§3.3 dst-distribution pin real** ✓, era rides the log header and is applied on replay ✓.

### Blockers (0)

None.

### Warnings (5)

1. **`jint_strict` still silently defaults non-numeric JSON — the r1 Float fix is incomplete** · 4-lens agreement (acceptance, architecture, blind, edge) · `core/catalog.odin:564-571`. The `#partial switch` rejects only `json.Float`; **String/Boolean/Null fall through to `return def, true`** — empirically verified: `"volume": "high"` → `(0, true)`, `"multiplier": true` → `(1, true)`. A live silent-default catalog path [ODN-5] in the exact helper the r1 fix introduced. *Fix:* add a default case returning `(0, false)`; add string/bool rows to the fail-fast table.
2. **`jint_strict` narrows i64→i32 BEFORE any range check — 2³²-scale values wrap into valid small values** · codebase + security · `core/catalog.odin:564-568`. Empirically verified: `"era": 4294967297` → `(1, true)` passes the era 1..64 check. Same wrap family as the r1 default_lane finding, now inside the shared helper so **every** new 3.1 field is wrappable. *Fix:* range-check x before the cast in the Integer branch; add 2³²-era test rows.
3. **`load_demo_replay` leak REGRESSION — the r1 demolish fix REPLACED the pre-existing `demo.nodes/draws/spawns` deletes instead of adding to them** · 5-lens agreement · `harness/run.odin:305-309`. Base `7931aa5` deleted `nodes/draws/spawns/captures`; the diff hunk `@@ -298,9 +305,7 @@` shows all three pre-existing deletes replaced by `delete(demo.demolishes)`. drift-check (9 demos) + run_replay now leak three dynamic arrays per call. *Fix:* restore the three deletes alongside the demolishes one.
4. **`node_types` `demand_weight` fail-fast rules (integer-only + ≥ 0) have NO negative rows** · tests · `core/catalog.odin:231-239`. Every packet_types/demand rule has negative coverage; the two new node_types rules are the only fail-fast rules in the diff untested — the round-2 audit bar ("a rule with no negative row = a gap"). *Fix:* add `demand_weight: 1.5` → "must be an integer" and `demand_weight: -1` → "must be >= 0" rows.
5. **Advisory test gate: CONCERNS** · tests (both chunks). P0 fail-fast ~94% (only via warning #4), P1 ~90%, overall ~95%; goldens 100% (9/9 `.t1` headers consistent, line counts == ticks, r1→r2 goldens byte-identical + the expected ecmp/demolish re-bless for the catalog-hash fold). Gate passes once warning #4 closes.

### Notes (6)

1. **Wrong-typed per-era `entries`/`set_pieces` keys silently accepted as "no entries"** — soft-check inconsistent with the hard `eras`/packet_types checks · acceptance + blind · `core/catalog.odin:368-370, 397-399`. (`"entries": {}` loads an era with zero demand.) The `or_continue` row-skip variant is NOT re-opened — r1-ruled house pattern.
2. **`catalogs_load` never `json.destroy`s its parse trees** — the new 43-row fail-fast suite surfaces ~5,000 leaked allocations in `odin test core` (verified: 5028 leak lines, `parser.odin:299` + `catalog.odin:211/251/278/344`) · 5-lens agreement. Bounded one-shot, no sim impact; gate noise.
3. **`effective_volume` i32 multiply can wrap for accepted large multipliers** — set-piece `multiplier` has no upper bound (`v *= sp.multiplier`, lower-bound-only check) · edge + security · `core/demand.odin:72-80`. Absurd-but-accepted data only; ODN-5 upper-bound gap.
4. **ODN-7 `plan_pressure` proc-field seam deferred to [LATER]** — flow_step hardcodes `scripted_plan_pressure`; documented in-code with the PROTO note carried · architecture · `core/demand.odin:22-24`. Read-only discipline fully intact; flag so the seam isn't forgotten before the V2 auditor.
5. **Flow-level §3.3 pin exercises only UNIFORM sink weights** — the node `demand_weight` → `weighted_pick` wiring is never flow-tested non-uniform (a weights-ignoring wiring bug would pass every flow-level test) · tests · `core/demand_test.odin:22-25, 216-228`.
6. **`catalogs_hash_sources` fold has no unit pin** — a dropped source in the fold would pass every gate silently (bless+replay stay internally consistent) · tests · `core/catalog.odin:502-506`.

### Reviewer agreement

The 5-lens convergence on the `load_demo_replay` leak regression (every lens that read the base-vs-current hunk caught the swap) and the 4-lens convergence on the `jint_strict` string/bool fall-through give high confidence these two are the real residual work items — both are the r1 fixes landing **incompletely** (fix #11 wrong, fix #9 partial), exactly what this round was chartered to catch. The i64→i32 narrowing (2 lenses, empirically verified) is the same wrap family as the r1 lane finding, now at the shared-helper level. Rejected as carry-forward after code verification: the edge lens's re-file of the `or_continue` row-skip (r1-ruled house pattern — not re-opened).

**Verdict:** READY TO MERGE

The QoS data foundation is solid and every r1 blocker/warning family is either fixed-and-verified or reduced to two residual hardening items in the new `jint_strict` helper + one harness leak swap — none merge-blocking, all cheap follow-ups. Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over.
