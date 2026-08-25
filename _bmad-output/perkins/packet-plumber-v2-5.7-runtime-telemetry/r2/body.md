## 🤖 Perkins automated review — round 2 of 3 (fix audit)

**Job:** packet-plumber-v2-5.7-runtime-telemetry · **Reviewed sha:** `86ef8f8` · **Reviewers:** 7/7 completed
**Verification:** 22/24 findings confirmed against the code — 2 discarded as false-positive (both blind: the "unused `g` won't compile" claim is r1's exact falsified false-positive — `odin test core` is 164/164 green at this sha; the "CI stats-check fails because harness.sh wasn't updated" claim is premise-false — the wrapper is a pass-through `exec ./bin/harness "$@"` and CI ran the step green)

**Local ground truth (re-ran everything):** `odin test core` 164/164 · lint all gates green · `harness run` 25/25 demos, goldens byte-identical, worktree clean after · `stats-check` byte-identical on pause (369,452 B), qos_contention (65,626 B), surge (933,876 B), health_lose (87,978 B) · both app builds compile · CI 4/4 green on this sha. **The determinism contract holds everywhere I probed it.** Two instrumented-copy probes verified pin non/vacuousness mechanically (details below).

### Fix audit of round 1 (the delta this push claims)

**FIXED and verified (17):** **B1** — the class-row pins are real and bite (probe: tick-12 fixture carries loss 50%/90%, avg 250/400 ms, real latch splits; the pins recompute from `flow.sla` independently, so a wrong formula fails) · **W1** dangling flag → exit 2 (run live; duplicate flag too) · **W2** unwritable path → exit 1 · **W3** the PR-body excerpt is now **byte-identical to the real tick-21 stream** (mechanically diffed, sim_hash `3065d3ada10b1ef9` included) · **W4** seed-column claim corrected · **W5** AC5 ticked · **W6** D rows aggregate in code (map-free find-or-append, exercised with count=2) · **W7** D-row accounting pinned non-vacuously (pipe 1 dropped=2 with `offered == carried + 2×bw` on real drops) · **W9** `stats_emit` is the one emission proc, called by all three drivers and pinned · **N1 N2 N4 N5 N6 N7 N9** verified in code · **N10** (spec code map now lists both harness files — unclaimed but fixed).

**PARTIAL (3) → this round's findings:** **B2** gate raised but still FAIL on narrower grounds (R2-B1/R2-B2) · **W8** test exists but load-column pins are vacuous (R2-W1) · **W10** app gate only (R2-W2).

**Still present (carried, non-blocking):** N3, N8, N11 (folded into R2-N8/N10 below).

### Blockers (2)

**R2-B1 — the W6 aggregation shape has no discriminating pin** `[tests]` · `core/stats_test.odin:206-229`
The D-row assertions (E9-only reason, count≥1, live-pipe, per-pipe `sum(count) == dropped`) all pass equally on the r1 per-event shape (two `count=1` rows) and the r2 aggregated shape (one `count=2` row) — and both byte-compares compare the build against itself. Probe: the congested fixture's tick-12 record really emits `D pipe=1 class=1 count=2`, so the shape is *exercised* but not *pinned*. This is exactly r1-B1's class ("byte-identity passes on identically-wrong shapes") on the semantic the W6 fix introduced ("the count column is meaningful").
*Fix:* assert no two `rec.drops` rows share `(pipe,class,reason)`, and/or pin the known tick-12 shape (one row: pipe 1, class 1, reason 0, count 2).

**R2-B2 — Advisory test gate: FAIL** `[tests]` (aggregate of R2-B1 + R2-W1 + R2-W2)
P0: byte-identity 100% (unit + stats-check + CI) · shared-emission 100% · golden-safety 100% (25/25 + PP_DEBUG app build in CI) · record math **partial** — class/pipe/D-row-accounting pins verified non-vacuous, but the aggregation shape (R2-B1) and the bundle load-columns (R2-W1) are pins that don't bite. P1: harness PP_DEBUG compile gate 0%, CLI error paths untested. Gate requires P0 100%.
*Fix:* two one-line test changes (R2-B1, R2-W1) + one CI line (R2-W2) — the gate then passes.

### Warnings (4)

- **R2-W1** `[tests]` *still present since r1 (W8)* `core/stats_test.odin:257,288-301` — the bundle-replication pin is **vacuous for load columns**: the record is computed at tick 20 where both members are all-zero (probe: ticks 2–8 carry offered=30/carried=30/util=100/q=[0,1,0]; tick 12+ all zeros), so offered/carried/dropped/util/q equalities compare 0==0. Only `cap_units==30` bites. The runtime behavior itself is *correct* (mid-flight loads replicate identically — verified) — it's the pin that doesn't bite. *Fix:* compute the record mid-flight (tick ≤ 8) and assert identical AND non-zero member loads.
- **R2-W2** `[architecture,codebase,blind]` *still present since r1 (W10)* `.github/workflows/ci.yml:99-104` — the CI PP_DEBUG gate compiles **the app only**; `harness/overlay.odin` (a whole gated file) and the overlay-check dispatch in `harness/main.odin` compile in no CI step. The step's own comment says "two whole files rot silently otherwise" — it covers one of the two. *Fix:* one CI line: `odin build harness -define:PP_DEBUG=true` (compiles green locally today).
- **R2-W3** `[edge,security,acceptance]` — `--stats-out ""` (empty token, e.g. an unset shell variable) **silently disables telemetry in both CLIs**: exit 0, no stream, no diagnostic (reproduced live) — and it bypasses the harness one-demo guard too. Defeats the W1 fix's stated contract ("never silently run telemetry-off"). *Fix:* track flag-seen separately from the value; empty token → usage error, exit 2.
- **R2-W4** `[edge]` `app/main.odin:246-260` — the app never calls `free_all(context.temp_allocator)` (zero occurrences in `app/`; the harness drivers free per tick), and the new per-step `state_hash` serializes the **full state into that arena at 20 Hz** whenever `--stats-out` or the overlay is on. Odin's runtime documents the default temp arena as needing a per-frame-loop `free_all` "to prevent it from leaking". Unbounded session-long growth on the telemetry path. *Fix:* one `free_all(context.temp_allocator)` per frame in the app loop.

### Notes (10)

- **R2-N1** `[codebase,acceptance]` `_pr_body.md:93` — stale r1-era "555KB" pause-stream size; the stream at this sha is 369,452 B (the W6 aggregation changed the byte count silently). Update or drop the figure.
- **R2-N2** `[security]` `harness/main.odin:117-123` — the harness accepts a flag-shaped path token (`--stats-out --stats-out` writes a literal file named `--stats-out` in cwd — reproduced); the app exits 2 on the same argv. Divergent validation at the shared flag; reject `-`-prefixed tokens in the harness too.
- **R2-N3** `[security]` `.gitignore:24-25` — CI's `app-debug.bin` isn't covered by the never-commit-binaries rule (`git check-ignore` → no match). Extend to `app*.bin`.
- **R2-N4** `[codebase,blind]` `core/stats_test.odin:124-132,258-266` — dead `before := len(state.events)` / `_ = before` pairs left in both test loops. Delete.
- **R2-N5** `[codebase]` `app/render/debug_overlay.odin:283-287` — fmt_tmp's comment claims "the render package has no fmt strings"; four sibling render modules call `fmt.aprintf` directly. Fix the comment or drop the shim.
- **R2-N6** `[architecture,blind]` `app/main.odin:169-178` — the always-init builder+header comment says the overlay "appends via stats_emit even without `--stats-out`", but the loop passes a nil sb in exactly that case (compute-only). Comment is false; the never-flushed header alloc is conditional-free. Fix one or the other.
- **R2-N7** `[blind]` `app/render/debug_overlay.odin:79-81` — `draw_heat_tints` discards `node_slot`'s ok and indexes `node_pos` unvalidated while `pipe_slot`'s ok is guarded two lines above. Handle both failures the same way.
- **R2-N8** `[tests]` *still present since r1 (N11)* — the W1/W2 error paths (exit 2 dangling/duplicate, exit 1 unwritable, one-demo guard) have no automated coverage; this review ran them by hand.
- **R2-N9** `[tests]` — no literal pin of the CSV row format; the G-row passthroughs (gen/score/meter) are never value-asserted. A column swap drifts live and replay identically. Pin one literal row of each kind (the verified tick-21 excerpt).
- **R2-N10** *carried from r1* — N3 (session stream buffered in memory until exit; compounded by R2-W4) and N8 (overlay_check re-implements the stepping/composition loop) — both unclaimed and unchanged.

### Reviewer agreement

Three-lens agreements: the CI PP_DEBUG gate covering the app only (architecture/codebase/blind — R2-W2) and the empty-token silent telemetry-off (edge/security/acceptance — R2-W3). Two-lens: stale 555KB (R2-N1), dead captures (R2-N4), builder-comment contradiction (R2-N6).

**Verdict:** NEEDS CHANGES

The r1 blockers are genuinely fixed and the determinism contract is intact — this round's two blockers are the remaining pins that don't bite (aggregation shape, bundle load columns) plus the gate they fail. All fixes are small: two one-line test changes, one CI line, one parser guard, one `free_all`.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
