## 🤖 Perkins automated review — round 2 (FIX-AUDIT)

**Job:** packet-plumber-3d-e2-flow-qos · **Reviewed sha:** 94c6fa5 · **Reviewers:** 14/14 lens runs completed (7 lenses × 2 diff chunks — 4014-line diff chunked per big-diff policy: c1 = runtime `scripts/`+`scenes/` 1863L, c2 = tests/tools/captures/docs 2151L)
**Verification:** 68/71 lens findings confirmed against the code — 3 discarded as false-positive (1 chunking artifact, 1 documented deferral, 1 verified-false capture claim), 0 unverified

### Fix audit (round 1 → this sha)

**r1 BLOCKER (pipe-select grammar zero coverage): FIXED ✅** — `tests/test_view_interaction.gd` pins the REAL gesture path (`Input.parse_input_event` → `InputRouter` → `FlowView.pick_pipe` → `pipe_selected` → QosPanel). Suite grew 142 → **170 printed oks (+28: 20 view_interaction + 4 sim_flow + 3 sla + 1 view_purity — all substantive, no padding)**. Five mutation legs, each turned the suite RED then restored clean:
- M1 kill SELECT decision → 2 fails · M2 kill drag-to-orbit conversion → 1 fail · M4 kill pick occlusion guard → 1 fail · M5 kill dot material rebind → 1 fail · M6 kill panel rung fallback → 1 fail

**r1 warnings: 9/11 verified FIXED** (dot-material rebind, QoS-panel logic pins, invalid-command no-ops, pick-pipe occlusion, latency event attribution `pipe/node`, merge-path pop restored, EditorInterface export-safety via singleton indirection, autoload pin de-vacuated, plus the gate re-emitted below). **2 folds are broken — they are this round's blockers.** Notes: 13 verified folded (fixture dedupe, spec ticks, dead consts, @tool structural pin, capture-06 ladder-first, loss-latch stickiness, view-purity negative control, …); the rest carried forward and marked below.

### Blockers (2)

**1. `SimCore._pick_next_pipe` crashes on empty routes — the folded no_route/isolation test aborts and 3 of its 5 checks never execute** — `scripts/sim/sim_core.gd:295`
`setup()` clears `routes` and never rebuilds (only `_cmd_add_pipe` does), so on a zero-pipe sim `routes == {}`; `var r: Dictionary = routes.get(dst)` is a typed assignment of **Nil → SCRIPT ERROR** (observed this round: *"Trying to assign value of type 'Nil' to a variable of type 'Dictionary'"* cascading to an out-of-bounds at `_enqueue_at_node:274`). The `if r == null: return -1` guard beneath it is dead code. The new isolation test's `_spawn_packet(1, 20, …)` hits exactly this — its checks *"no_route: unroutable packet drops with an attributable record"*, *"counts against the class"*, *"single no_route does not latch"* are **phantom** (23 `check()` calls in the file, only 20 printed). Gameplay never reaches it (`_spawn_demand` is `_reachable`-guarded), but the harness door is the documented staging door and the r1-W5 contract remains unpinned. Fix: untype the local (`var r = routes.get(dst)`, matching `_reachable`) or `routes.get(dst, {})`; guard `drops.is_empty()`; re-run and confirm the 3 phantom checks now execute.

**2. The r1 false-green fold is ineffective — the suite printed `SUITE RESULT: PASS (0 failures)` over the crashed test above** — `tests/run_tests.gd:43-49`
The fold guards `if result is int` → `failures += result`, else count an abort. But on Godot 4.7.1 an aborted awaited coroutine **still yields an int** (r1's own reproduction documented this; the fold checked for null instead). Live proof this round: zero `aborted` FAIL lines in the full output while `test_sim_sla` aborted with 3 checks missing — the A1 exit-0 gate false-greens over exactly the abort class it was folded to catch. Fix: make the guard semantic, not type-based — e.g. run_tests compares a per-script expected-check count (or a shared `check()` invocation counter) against printed oks and FAILs on shortfall; plus branch-guards in tests so aborts convert to counted failures.

### Warnings (8)

1. **`main._ready` still computes `wedge_layout` twice** while `_generate_world`'s new docstring promises "computed ONCE by the caller and threaded through" — the N24 fold overclaims (`sim.setup(SEED, WorldSeed.node_placements(SEED, WorldSeed.wedge_layout(SEED)))` recomputes). [blind+acceptance+architecture]
2. **Determinism capture vs replay test now inject the shared commands at different ticks** (tool: `t == ticks/3` = 300; test: `t == 120`) — the "can never drift apart" pairing no longer exercises the same replay stream (captures/05: 10 delivered vs the test's ≥12). Hoist `REPLAY_INJECT_TICK` into the shared consts; regenerate 05. [blind+acceptance+architecture+codebase+tests]
3. **Lane-dependent traversal speed (Express 200 / Standard 100 / BE 60) has no differential pin** — E2.4's "class-dependent speed" is unpinned; a `LANE_SPEED_MILLI` regression passes the suite. [tests ×2 chunks]
4. **HUD breach chip (`set_breaches`/`_breach_lines`) still untested** — carry-forward N20. [tests ×2]
5. **Node egress pulse (`FlowView.pulse_egress` → `NodeSite.pulse_egress` + cooldown) zero behavioral assertions** — E2.4 visible beat smoke-executed only. [tests ×2]
6. **Streaming-class latency breach (tighter 1200 ms) never tested** — only email latency latches. [tests]
7. **Capture harness still drives main's private handlers — and the fold deepened it** (`main._on_qos_apply` now called twice) — carry-forward N29 escalated. [architecture+codebase]
8. **Advisory test gate: CONCERNS** (both tests lenses voted PASS; amended down by the fix audit: the phantom isolation checks + the false-green harness mean the reported 170-green cannot be trusted until Blocker 2 lands; P1 also holds the lane-speed/streaming-latency/pulse/HUD gaps).

### Notes (36)

Canon/doc: ECMP uses chained 32-bit `hash_i32`, GDD M3 names `splitmix64` (determinism intact — name drift) · spec change-log entry (09-04) predates `created` (09-05) · QosPanel fabricates node names (`n%02d`) instead of seeded `site_name`s [×2] · test_sim_flow "natural demand cannot pollute" header overstates (delivered pins count sim-wide).
Sim hygiene: `_cmd_set_lanes` crashes on type-malformed payloads vs its documented no-op contract [edge+security] · `_spawn_packet` accepts any `cls` string · `bundle_for_pair` sole untyped-return + nullable · TIERS `drawable` flag dead · palette `Color`s live in sim balance data.
Structure (carry-forwards marked): pulse positional child-index mapping (N32) · InputRouter→FlowView coupling (N33, now accurately documented) · editor-capture plumbing in composition root (N34, export-safety fixed) · pooled-capacity formula duplicated panel/sim · REPLAY_CMDS spine re-declared in capture_runner · `_press/_move/_release` helpers duplicated verbatim across two test files [×2] · tools→tests dependency for the fixture consts · capture nullable derefs + double sim fetch + off-by-one step comments · `@tool` inconsistent across the editor-preview path (no mechanical impact — `setup()`-driven visuals; shot-08 aesthetic parity deferred to the k3 re-check).
Tests: null-guard family after non-halting checks (N42 — `drops[0]`, `payload[0]`, `bundle_for_pair().id`; the sla site is Blocker 1's abort) · panel payload cls-loop vacuous on missing class · deactivation "still flows" not cohort-scoped · serialization wave-2 ordering vacuous-ward · set_lanes negative-value branch unpinned · latency event pipe/node attribution implemented but unpinned (W7 residual) · `byte-identical` label vs `is_equal_approx` (N41 carry) · `_regenerate_preview` body replicated, never executed (P3) · house_pair extremes unguarded · detlog unguarded `load()`s · `@onready` fallback `lane = 0` unreachable per LADDER · slop-crossing motion delta swallowed · occlusion pin forges `_pipe_views` privates · `_spawn_packet`/`queues[...]` staging coupling (32 sites).

### Reviewer agreement

Highest-confidence multi-source findings: **the no_route-crash + false-green cluster [acceptance lens + independent fix audit]**; determinism capture/test timing drift [5 lenses]; layout-computed-twice doc overclaim [3 lenses]; lane-speed gap, HUD gap, pulse gap [2 lenses each]; capture private access [2]; set_lanes type-crash [edge+security]; fabricated node names [2]; gesture-helper duplication [2].

**Vision caveat (verbatim for non-k3 rounds):** pixel verification was MECHANICAL only — 8 captures verified as real PNGs of mandated resolutions/filenames (6× in-game 1600×900 incl. re-shot 06/07, editor 2964×2253, all-MATCH determinism log); aesthetic parity deferred for the k3 re-check, never faked.

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha.
The loop runs until an APPROVED verdict._
