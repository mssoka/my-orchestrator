## 🤖 Perkins automated review — round 3 of 3 (final automated round)

**Job:** packet-plumber-v2-5.7-runtime-telemetry · **Reviewed sha:** `4749470` · **Reviewers:** 7/7 completed
**Verification:** 15/18 findings confirmed against the code — 3 discarded as false-positive

### Fix audit (r2 → r3) — every r2 finding re-verified at this sha

| r2 finding | Status | Evidence |
|---|---|---|
| **R2-B1** aggregation-shape pin (blocker) | **FIXED — bites** | Probe (mutated copy): reverting find-or-append to per-event rows fails BOTH the uniqueness walk and the tick-12 tuple; a wrong-count aggregation fails the tuple. Fixture emits the pinned `D pipe=1 class=1 reason=0 count=2` at tick 12. |
| **R2-B2** advisory gate FAIL (blocker) | **FIXED** — gate now **CONCERNS** (warning) | The FAIL drivers (B1 shape, W1 vacuity, W2 CI gap) all closed; residual P1 gaps are advisory (see Warnings). |
| **R2-W1** vacuous bundle pin | **FIXED — bites** | Probe: halving member loads (per-pipe share) fails `carried == 30` + `util == 100`. Mid-flight tick-3 record, identical AND non-zero — the 0==0 vacuity is gone. |
| **R2-W2** CI harness PP_DEBUG gap | **FIXED** | `odin build harness -define:PP_DEBUG=true` is in CI; compiles green locally (as do all four build variants). |
| **R2-W3** empty `--stats-out ""` silent-off | **FIXED** | Live: dangling/duplicate/empty/flag-shaped → **exit 2 in BOTH CLIs** (8/8 probes); valid → exit 0 + 65,626 B stream. Flag-seen is tracked separately from the value. |
| **R2-W4** unbounded temp arena | **FIXED** | `free_all(context.temp_allocator)` per frame; the stream builder, per-tick records, and catalog strings are all general-allocator-owned (json strings are `clone_string`ed into the parser allocator) — structurally verified, and 25/25 goldens + 4/4 byte-identity confirm no determinism effect. |
| R2-N1…N7, N9 (notes) | **FIXED** | 369,452 B matches live; `-`-tokens rejected; `app*.bin` ignored; dead captures gone; `fmt_tmp` gone; comment matches nil-sb code; `node_slot` ok guarded; literal G/C/P/D rows pinned. |
| R2-N8 CLI error paths untested | **still present** (note) | Guards exist and bite live; no automated tests (3 lenses agree — see Notes). |
| R2-N10 documented decisions | still present by design | Stream buffered to exit; overlay_check stepping duplication — documented. |

**Claimed verification reproduced in full:** 165/165 core tests · lint 6/6 · 25/25 demos goldens byte-identical · stats-check byte-identical ×4 (pause 369,452 B / qos_contention 65,626 B / surge 933,876 B / health_lose 87,978 B) · app + harness build plain AND PP_DEBUG · PR-body excerpt verbatim in the live stream (8/8 rows) · worktree clean after.

### Blockers (0)

None.

### Warnings (3)

1. **App silently ignores `--stats-out=<path>` (equals form) and any unrecognized token — telemetry-off with exit 0** *(edge + security)* — `app/main.odin:151`. The parser exact-matches only the two-token form; `app --stats-out=x` runs green with no stream and no diagnostic. Same silent-off family as r2-W3 (which fixed the empty token); the harness fails loud on the same input (treats it as a demo name). Fix: reject any `-`-prefixed argv token that isn't the exact form (exit 2).
2. **Committed spec's AC4 mechanism text contradicts this round's own CI line** *(blind)* — spec says "harness builds never pass `-define:PP_DEBUG`" / "Release + harness builds carry ZERO overlay code"; the new CI gate builds the harness with the define. Golden safety is intact (compile-only; goldens run on the plain build — 25/25 byte-identical), but the contract text is now misleading. One-line spec edit ("the *golden path* never builds with PP_DEBUG; the CI gate builds a separate debug artifact that never runs goldens").
3. **Advisory test gate: CONCERNS (P0 100%, P1 ~85%, overall ~90%)** *(tests)* — P0 fully pinned (byte-identity, shared emission, golden safety, record math incl. the new aggregation + bundle pins). P1 residual: CLI error paths untested (N8), app free_all/stream-lifetime verified by code-reading only. Optional: extract the argv walks into testable procs to lift to PASS.

### Notes (8)

1. **R2-N8 carry-forward:** `--stats-out` CLI error paths remain live-verified only, no automated tests *(tests + security + acceptance)*.
2. PR body Files-changed still says "6 unit pins" — line 96 and the code say 7 *(acceptance + blind)*.
3. R2-W4 residual: app per-frame `free_all` vs stream lifetime is code-verified only; a future allocator-default change in `stats_emit` would silently reintroduce the hazard — worth a one-line allocator-contract comment *(tests)*.
4. R2-N9 residual: the 6 CSV header legend lines are not pinned string-for-string *(tests)*.
5. Paused-wall-ticks-emit-no-rows has no discriminating pin (a symmetric both-driver regression stays byte-identical); enforced by construction today *(tests)*.
6. Spec says "per-frame stats compute when the overlay is on"; code computes per *stepped* tick (the safer, r1-blessed semantics — paused frames never fabricate a record). Spec wording is loose *(blind)*.
7. App stats builder allocated + header-written unconditionally but deleted only when `stats_live` — exit-time, constant-size, cosmetic *(blind)*.
8. Spec frontmatter still says `review_loop_iteration: 1` with no r2/r3 change-log entries *(blind)*.

### Reviewer agreement

- equals-form `--stats-out=x` silent telemetry-off in the app (edge + security)
- R2-N8 CLI error paths untested (tests + security + acceptance)
- stale "6 unit pins" in the PR body (acceptance + blind)

**Verdict: READY TO MERGE**

All r2 blockers and warnings are fixed with bite-probes or live runs; the determinism contract (no wall-clock, one serializer, replay-identity, overlay golden-safety) holds everywhere probed; the three surviving warnings are documentation/CLI-edge polish, none merge-blocking.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
