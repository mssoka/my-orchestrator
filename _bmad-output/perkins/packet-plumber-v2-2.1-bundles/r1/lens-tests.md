# Lens: Test Coverage (Perkins r1 — packet-plumber-v2-2.1-bundles)

Test coverage analysis via traceability. For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap. Also run the advisory gate.

## Inputs
- **Diff:** `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.1-bundles/r1/diff.patch`
- **Worktree (verify here — read `core/bundles_test.odin`, `core/win_lose_test.odin`, and the existing test files to judge coverage):** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-2.1-bundles-r1`
- **Spec/context:** `/Users/moses/code/_bmad-output/briefings/perkins-packet-plumber-v2-2.1-bundles-r1.md` (lens-guards) and worktree `project-context.md`. The story requires T1+T2 goldens and the W1/W2 carry-forward tests.

## Behaviours to trace (the diff's behaviour changes)
1. **cap = static sum** (2 std=30, 3 std=45, mixed std+wide=55) → trace to a unit test.
2. **A lone pipe is a 1-member bundle** (cap = own tier) → trace.
3. **The routing representative pipe resolves to the bundle's pooled cap** ("one fat edge per pair") → trace.
4. **Rebuild on topology change** (adding a parallel pipe grows the bundle mid-run) → trace.
5. **No-LB behavioral pin** (a 2-pipe bundle serves the FULL pool — transit in 1 tick vs 2 for a lone pipe) → trace.
6. **T1 determinism** (parallel-pipe draw replays byte-identical) → trace (unit test + the `goldens/bundle.t1` manifest).
7. **W1 carry-forward:** headless app-layer restart test (restart → fresh seed, no state leakage) → trace.
8. **W2 carry-forward:** LOSE-loop replay test (losing run replays byte-identical) → trace.
9. **Render:** the merge-pop frame + single-pipe stays byte-identical to slice-1 (T2 golden) → trace to `demos/bundle.dem` + `goldens/bundle/*.png`.
10. **The flow's bundle-capacity lookup + defensive fallback** (`bundle_capacity_for_pipe` → 0 fallback) → trace.

## ⚠️ Lens-guards (prevent false positives)
- The grep-gate form of the no-LB pin lives in `tools/lint.sh` gate 5; the BEHAVIORAL pin is `test_bundle_serves_full_capacity_no_split`. Both count as coverage for behaviour #5 — do not double-flag.
- "Bundle state in the hash" (T1) is satisfied via the composing pipes being serialized — the determinism unit test (`test_parallel_pipe_draw_replays_byte_identical`) covers it. Do not flag "bundles not serialized = no determinism test."
- The **T2 pixel golden** (`goldens/bundle/*.png`) requires the software-raylib harness to re-verify; its presence in the diff + the demo + the `goldens/bundle.t1` manifest is the traceable artifact. If you can confirm the harness wiring is correct, that's FULL; if you can only confirm the manifest exists, mark the PIXEL match as unverified (a `note`, not a blocker — the determinism property is unit-tested).
- Don't flag em-dashes / the `v2` base / re-open 1.1–1.4.

## OUTPUT
Write ONLY a valid JSON array to: `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.1-bundles/r1/tests.json`
Schema:
```
{ "source":"tests", "severity":"blocker"|"warning"|"note", "category":"<tag, e.g. coverage-gap>",
  "title":"<one-line>", "location":"<file:line|hunk|N/A>",
  "evidence":"<exact lines READ from worktree/diff, verbatim>",
  "detail":"<≤40 words>", "recommended_fix":"<≤40 words>" }
```
ALSO emit exactly ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate", severity: PASS→note / CONCERNS→warning / FAIL→blocker
- detail: rationale with coverage %, recommended_fix: what would raise the gate
Gate thresholds: PASS = P0 100%, P1 ≥90%, overall ≥80%; CONCERNS = P0 100%, P1 80–89%, overall ≥80%; FAIL = P0 <100% or P1 <80% or overall <80%.

ONLY the JSON array in the file (it will have your gap findings + the one gate finding). `[]` is NOT expected here (the gate finding is always present). Accuracy > volume. When done: "tests lens done — N findings + gate: <PASS|CONCERNS|FAIL>".
