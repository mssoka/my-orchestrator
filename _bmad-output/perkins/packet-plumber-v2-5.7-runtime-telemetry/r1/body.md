## 🤖 Perkins automated review — round 1 of 3

**Job:** packet-plumber-v2-5.7-runtime-telemetry · **Reviewed sha:** `6b09497` · **Reviewers:** 7/7 completed
**Verification:** 36/38 findings confirmed against the code — 2 discarded as false-positive (one falsified by direct run: the claimed compile error does not exist, `odin test core` is 162/162 green at this sha; one premise-false: `bundle_cap` is capacity-units, same dimension as `carried`)

**Local ground truth (this review re-ran everything):** `odin test core` 162/162 · `tools/harness.sh run` 25/25 demos green, goldens byte-identical, worktree clean after · `stats-check` qos_contention 65,626 B and pause 555,483 B live==replay byte-identical · two live `--stats-out` runs `cmp`-identical · `odin build app` and `odin build app -define:PP_DEBUG=true` both compile · the real tick-21 stream was extracted and diffed against the PR body excerpt. **The determinism contract holds everywhere I probed it.** The findings below are coverage and documentation gaps, not determinism breaks.

### Blockers (2)

**B1 — P0 record math unasserted** `[tests]` · `core/stats_test.odin:96-116`
The derivation test pins the pipe formulas (`carried == queued*30`, util clamp, cap) but asserts **nothing** about the class rows: `loss_pct`, `avg_latency_ms`, the `demand/delivered/dropped` accumulator mapping, and the `sla_lat/sla_loss` latch copies have no value-level pin. C rows are half the stream artifact; byte-identity passes on identically-wrong values (both live and replay would carry the same wrong formula), and the copy is a separate proc from `sla_evaluate`. A C-row regression ships undetected.
*Fix:* extend `test_stats_derivation_congested` — per class row assert `loss_pct == dropped*100/(delivered+dropped)`, `avg_latency_ms == total_latency_ms/delivered`, the accumulator mapping from `flow.sla`, and the latches against `flow.sla_breach`.

**B2 — Advisory test gate: FAIL** `[tests]` (aggregate of B1 + the warnings below)
P0 ≈ 82% (record math half-pinned), P1 ≈ 15% (app emission loop 0%, PP_DEBUG compile gate 0%, stats-check manual-only, bundle replication 0%), overall ≈ 65%. Gate requires P0 100%, P1 ≥ 80%.
*Fix:* pin C-row/D-row/bundle-replication values in `stats_test`; wire `stats-check` and a `PP_DEBUG` build into the suite/CI.

### Warnings (10)

- **W1** `[edge,acceptance,security,architecture]` `app/main.odin:142-147` — the app silently ignores a dangling `--stats-out` (missing path token) while the harness rejects the same input with a usage error; a typo'd launch runs with telemetry silently off. Mirror the harness parse error.
- **W2** `[edge,codebase,blind]` `app/main.odin:170-176` — on an unwritable stats path the app `eprintln`s but exits 0; the committed spec's I/O matrix (line 72) mandates `eprintln + exit 1`. Surface the failure so main returns non-zero.
- **W3** `[codebase,blind]` `_pr_body.md:49-64` — **the sample excerpt misrepresents the real stream**: the real tick-21 output contains exactly one D row (`D,21,0,0,0,1`); the PR body shows a second (`D,21,1,1,0,1`) that the stream never emits, and the prose "pipe 1 … shed 1 (streaming)" contradicts the real `P,21,1` row (`dropped=0`). AC6's excerpt must be the verbatim artifact. *Verified mechanically by this review.*
- **W4** `[codebase,blind]` `_pr_body.md:135` — the PR claims "the sim_hash + seed column disambiguates runs"; the serializer writes no seed column. Fix the claim or add the column.
- **W5** `[acceptance,tests,blind]` `spec-5-7 …:109` — the committed spec leaves the AC5 full-suite checkbox unchecked while the PR body claims the suite green (the suite IS green — this review verified it locally). Tick the box.
- **W6** `[edge,architecture]` `core/stats.odin:205-224` — D rows emit per drop event, never aggregated per `(pipe,class,reason)`; the `count` column is always 1 despite the legend implying aggregation. Aggregate into `count` or document it as reserved.
- **W7** `[tests]` `core/stats_test.odin` — D-row accounting (member replication, class/reason, E22 exclusion) and the `offered == carried + drops*bw` equality are never asserted.
- **W8** `[tests]` `core/stats.odin:201` — bundle-member replication (pooled bundle, shared load columns) is untested: no test constructs a parallel-pipe bundle.
- **W9** `[tests]` `app/main.odin:234` — the app-side emission loop has zero automated coverage; the unit mirror mirrors the harness loop, not the app's. Factor a shared per-step emission proc both drivers call and pin it.
- **W10** `[tests]` `.github/workflows/ci.yml:75` — no CI step builds with `-define:PP_DEBUG=true`, so the overlay code (two whole files) can rot between reviews. Both builds compile at this sha (verified); add the gate so it stays true.

### Notes (11)

- **N1** `[acceptance,tests]` `stats-check` is a manual verb — nothing wires it into `harness run` or CI. Run it for a demo subset (pause + qos_contention) automatically.
- **N2** `[security,architecture]` `harness/stats.odin:27-28` — predictable `/tmp` paths (symlink/collision; not portable to the Windows target). Write under gitignored `bin/` like overlay-check.
- **N3** `[security]` `app/main.odin:166-176` — the app buffers the whole session's stream in memory, flushed only at exit (documented decision; crash loses it, growth is unbounded). Consider incremental flush.
- **N4** `[edge]` `harness/overlay.odin:79-131` — `overlay-check` with zero stepped ticks (e.g. `cap_ms=0`) exits 0 with an overlay-free PNG. Fail or warn when `stats_valid` is false.
- **N5** `[codebase]` `harness/overlay.odin:38-45` — demo teardown block inlined a third time; extract `demo_destroy`.
- **N6** `[codebase]` `harness/main.odin:192` — `overlay-check` missing from the usage string.
- **N7** `[architecture,blind]` `app/main.odin:127` — `overlay_on` field is not compile-gated though comments claim "field + toggle are compile-excluded". Gate it or fix the comment.
- **N8** `[architecture]` `harness/overlay.odin:82-113` — overlay_check re-implements the stepping loop + frame composition; drift risk vs the capture path.
- **N9** `[blind]` `harness/overlay.odin:1-4` — header comment says the PNG lands in `_bmad-output/`, the code writes `bin/`.
- **N10** `[blind]` — the spec's Code Map/Tasks omit the two new harness files (`harness/stats.odin`, `harness/overlay.odin`).
- **N11** `[tests]` — `--stats-out` CLI error paths (duplicate flag, missing token, ≠1 demo, unwritable path) untested.

### Reviewer agreement

Four findings independently confirmed by 3–4 lenses each (highest confidence): the dangling `--stats-out` token (W1), the exit-0-vs-spec-exit-1 error contract (W2), the fabricated excerpt D row (W3, mechanically re-verified), the AC5 checkbox contradiction (W5). Four more by 2 lenses: seed column (W4), D-row count (W6), stats-check wiring (N1), /tmp paths (N2).

**Verdict:** NEEDS CHANGES

The determinism spine, golden safety, and the shared-serializer byte-identity contract all hold under direct verification — the code is sound where it was pinned. What's missing is pins: the class-row math (B1) is the one true coverage hole; the rest of the blockers/warnings are the gate that hole trips plus documentation-integrity fixes (W3–W5) on the artifact the user will actually read.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
