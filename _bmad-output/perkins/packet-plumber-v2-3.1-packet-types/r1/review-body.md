## 🤖 Perkins automated review — round 1 of 3

**Job:** packet-plumber-v2-3.1-packet-types · **Reviewed sha:** `37f5581` · **Reviewers:** 14/14 completed (7 lenses × 2 chunks — diff 4013 lines exceeded the big-diff threshold: chunk 1 code+catalogs 1387 lines/16 files, chunk 2 goldens 2626 lines/23 files; findings merged before verification)
**Verification:** 13/17 unique findings confirmed against the code (35 raw lens reports deduped) — 4 discarded as false-positive, 0 kept as [unverified]

**Ground truth at `37f5581` (verified independently this round):** `odin test core/` **59/59 green** · `harness run` **8/8 green** — incl. the NEW `qos` era-3 golden, 1500 ticks, replayed bit-for-bit through the ODN-11 gate · `tools/lint.sh` **5/5 gates green** (core import purity, no file-scope vars, no map-iter, no bare discards, no LB mechanic). The load-bearing invariants hold: **distinct shapes** (email=circle / streaming=triangle — never color alone ✓), **spawn determinism [E10]** (one seeded Lemire draw per pick inside the deterministic stream; arrays-only; era-0 legacy runs draw zero rng ✓), **director read-only [ODN-7]** (`scripted_plan_pressure` sees only the catalog; no topology/Run_State handle ✓), **core engine-free [ODN-1]** ✓, **§3.3 dst-distribution pin real** (uniform-weight sink pin + [1,2,3] unit pin + same-seed byte-identical histograms ✓), era rides the log header and is applied on replay ✓.

### Blockers (1)

1. **P0 coverage gap: zero error-path tests for the new ODN-5 fail-fast catalog loaders** (advisory test gate: **FAIL**, P0 5/6) — `tests` · `core/catalog.odin:272-390`. The story's own AC demands "catalogs are integer-only for sim values + **fail-fast validated at load** [ODN-5]". The two dozen new fail-fast rules (bad JSON, unknown shape/class_id/role/selection, latency/loss/bandwidth/lane/era bounds, set-piece multiplier/duration, required email/streaming) are exercised only happy-path — no core test calls `catalogs_load` with malformed input at all. The gap already hides one live silent-default (warning #1). *Fix:* table-driven negative tests feeding malformed `packet_types.json`/`demand.json` bytes to `catalogs_load`, one per fail-fast rule, asserting the named `Catalog_Error`.

### Warnings (6)

1. **`color_rgba` element type guard is dead code (`!ok` tests the outer object assert, not `!okc`)** — malformed element silently becomes 0 instead of fail-fast · 7-lens agreement (acceptance, architecture, blind, codebase, edge, security, tests) · `core/catalog.odin:295`. A string/float element fails the `json.Integer` cast, yields `n=0`, passes the 0..255 check — a live silent default on malformed JSON, contra ODN-5 (cosmetic field, hence warning). *Fix:* `if !okc || n < 0 || n > 255`.
2. **Set-piece tick fields u64-wrap negative JSON values with no sign check** — `start_tick: -5` loads as ~2^64 and the surge silently never fires; negative `duration_ticks` passes the `==0` check and wraps the window · 5-lens agreement · `core/catalog.odin:373-375`. *Fix:* reject negative i32 ticks (duration < 1) before the u64 casts.
3. **`default_lane` truncated to u8 BEFORE the `>2` range check (both new loaders)** — JSON 256/257/258 wrap to 0/1/2 and silently pass · 4-lens agreement · `core/catalog.odin:306` and `:356`. *Fix:* range-check the i32 before narrowing, both sites.
4. **`Packet_Type.demand_weight` has no range validation** — negative weight loads silently while `Node_Type.demand_weight` (≥0) and `Demand_Entry.demand_weight` (≥1) are both validated · codebase · `core/catalog.odin:307-309`. *Fix:* add the bound to the packet_types validation chain.
5. **`weighted_pick_excluding` untested** — the §3.3 flow-level pin uses all-equal sink weights, so a weights-ignoring dst pick would still pass it; the exclusion variant's weighting and the all-excluded ⇒ skip path (lone-sink topology silently spawns nothing) are uncovered · tests · `core/flow.odin:125`. *Fix:* non-uniform-weight distribution pin, excluded-slot-never-picked, all-excluded ⇒ `ok=false`, plus a single-sink flow test.
6. **Drift-check mutation matrix has no era-byte tamper class** — the era byte became load-bearing this story (first era-3 golden); era-tampered logs are *accepted* by `replay_hashes` (era is applied, not a rejection class) and caught only by hash divergence at the compare stage — which `drift_check` never runs. The end-to-end gate DOES hold (verified: 8/8 replay green), so this is matrix completeness, not a silent acceptance · tests · `harness/drift.odin:100-125`. *Fix:* add an era-flip mutation (byte 16) + a divergence assertion.

### Notes (6)

1. **Duplicate demand era rows silently last-wins** and leak the shadowed era's arrays — no duplicate-key fail-fast · 3-lens agreement · `core/catalog.odin:384`.
2. **`weighted_pick` doc comment contradicts the code** — claims a zero/negative weight "still counts toward the total"; the code excludes it (code correct, comment misleading on the [E10] pick math) · 2-lens agreement · `core/flow.odin:103-104`.
3. **`load_demo_qos_fixture` frees draws/spawns/captures but not `demolishes`** — leak per call on demos with demolish intents (mirrors a pre-existing omission in the sibling loaders) · blind · `harness/run.odin:253-258`.
4. **`jint` silently truncates `json.Float`** on the new 3.1 sim fields (`"volume": 2.9` → 2) — weakens the integer-only bar for the new catalogs · codebase · `core/catalog.odin:507-513`.
5. **T2 failure messages are temp-allocated inside the tick loop and freed by the per-tick `free_all` before the post-loop FAIL print** — failure detail (mismatch count, diff-bundle path) reads as garbage exactly when T2 fails; PASS/FAIL gating unaffected · codebase · `harness/run.odin:128-132,165-167`.
6. **`qos.dem` is the only demo missing `expect hash stable`** — the directive is parsed but never read (dead field), so zero behavioral effect; convention drift · acceptance · `demos/qos.dem`.

### Reviewer agreement

The 7-lens convergence on the `color_rgba !ok/!okc` typo (every non-blind lens plus blind caught it from the diff alone) and the 5/4-lens convergence on the two cast-before-validate gaps give high confidence the ODN-5 validation family is the real work item this round — all four warnings (#1–#4) plus notes #1/#4 are one coherent fix-and-test pass over the new loaders. Rejected as false-positive after code verification: a blind "era never written to the log header" blocker (the plumbing pre-exists at `core/serialize.odin:78/:266`; empirically falsified by the green era-3 replay), an `or_continue` style note (house pattern since 1.2), and two goldens observations fully explained by the class-0 render change + run-setup-vs-action-log design (PNG re-blesses match exactly the demos with a visible in-flight packet; draw/flow/win share one log by design and replay to divergent manifests green).

**Verdict:** NEEDS CHANGES

The QoS data foundation itself is solid — determinism, shapes, read-only director, golden replay all verified — but a named AC (ODN-5 fail-fast) ships with zero negative tests and four live validation gaps that those tests would catch. One focused pass on the new loaders + the negative-test suite closes everything above.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
