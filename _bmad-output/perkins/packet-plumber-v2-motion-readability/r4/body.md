## 🤖 Perkins automated review — round 4 (fix-audit)
**Job:** packet-plumber-v2-motion-readability · **Reviewed sha:** 8f2ae3b · **Reviewers:** 7/7 completed
**Verification:** 34/35 substantive findings confirmed against the code — 1 discarded as false-positive (0 unverifiable). Perkins executed the gates at the reviewed sha: **11/11 local gates green, 33/33 render tests, `motion-pixel` PASS (alpha05 = 489.0 = the exact midpoint of 476.2→501.8), fix commit touches zero goldens.**

### Fix audit (r3 → this push)

| r3 finding | status |
|---|---|
| **B1** activation unpinned | **FIXED, execution-verified** — `interp_alpha_from_accum` extracted + unit-pinned; the rlsw pixel gate proves the drawn alpha=0.5 packet IS the snapshot midpoint, with the equal-endpoints negative control; wired as local gate 8 + a dedicated remote CI step. A dropped call-site arg no longer compiles (unused local). |
| **B2** advisory gate FAIL (57%) | **FIXED — gate now PASS** (P0 100%, P1 ≈92%, overall ≈86%). |
| **W1** remote CI parity | **FIXED** — the workflow runs all five unit suites + the motion-pixel gate. |
| **W2** trail ring unpinned | **LARGELY FIXED** — 4 new tests pin order/fill, snap-no-push, move gate, fades ladder. Two pin defects below (W3, W4). |
| **W3** delivery pin vacuous | **HALF-FIXED** — the production guard is real (`interp_continuous` reads `p.delivered`), but the pin is still non-decisive: Perkins deleted the guard and **33/33 tests still pass**. The PR-body claim "the pin tests the predicate" is falsified by that mutation. |
| **W4** strip drift net | **FIXED IN SUBSTANCE, delta defect introduced** — the net is wired and bites, but misindexes on paused demos (W1 below, reproduced). |
| Notes N1/N3/N4/N6/N7/N8/N10/N12/N13 | **FIXED.** N9/N11 **half** (PR-body wording / exit-0 vacuity, notes below). N14 partial (selftest exists, no gate runs it). N2/N5 carried (k3-deferred / documented deviation). |

### Blockers (0)

None.

### Warnings (4)

1. **W4's drift net misindexes on paused demos — motion-strip falsely refuses VALID post-pause strips** (`harness/motion_strip.odin:141-153` + `run.odin:402-406`) — [codebase, architecture, edge]. The strip collects one hash per **stepped** tick; the blessed manifest is indexed per **wall window** (paused windows included), so any post-pause window shifts the prefix comparison → false STATE DIVERGENCE → exit 2. **Perkins-reproduced:** `motion-strip pause 71000 72000 100` → exit 2 on a valid timeline (before-pause window and pause-free demos → exit 0). Over-strict only — no false-green path, and a re-bless reproduces the identical manifest, so goldens cannot be corrupted by this. Also: frames export before the refusal (orphan PNGs), and the PR-body "verified" note overstates. *Fix: append the paused-window stable hash (mirror run_demo's convention) or compare by wall-window index; verify with the pause strip + a corrupted-manifest negative.*
2. **[since r3] The delivery-snap pin is still non-decisive** (`motion_test.odin:211-218`) — [codebase, tests, edge]. Mutation-proven: deleting the `p.delivered` guard breaks no test (entry anchors still mismatch, so the guard never decides). *Fix: make the anchor continuous with delivered=true → assert snap; companion delivered=false → assert continuous.*
3. **Drop-oldest shift branch never executes in any test** (`view.odin:374-380`) — [tests]. The fill test drives exactly 3 pushes = full ring; the overflow `else` (the shift loop) has zero executed coverage despite being listed as pinned in the PR body. *Fix: add a 5th move; assert trail[0] advanced and trail_n stays 3.*
4. **trail_ring_stationary_no_push pins a stationary push while asserting the opposite** (`motion_test.odin`) — [blind]. The first call is a snap (no push); the stationary second call pushes via the empty-ring bootstrap (`moved := echo_n == 0`), so trail_n==1 proves a stationary push occurred. The real invariant — stationary frame with a non-empty ring must not push — is untested. *Fix: seed with two moving frames, then assert the stationary frame leaves trail_n unchanged.*

### Notes (11)

1. Echo draw application unasserted anywhere — the fades pin re-derives the ladder math, never the draw code (`view.odin:1615-1623`); goldens render alpha=1.0 and motion-pixel's exact-color scan excludes blended echoes by construction.
2. [N11 half] `measure_packet_motion.py` still exits 0 when zero frames track — vacuous evidence has no failure signal (BODY overridable + selftest did land).
3. [N9 half] PR body still claims snapshot mode is "byte-identically" pre-2.1; the +15% radius applies in both modes (code comment was fixed; the body wasn't).
4. Stale counts: README + the new ci.yml comment say "13" motion pins; the file now has 18 `@(test)`s.
5. `motion_pixel.odin` ships fix-commit scratch: the NEGATIVE CONTROL paragraph duplicated verbatim, a literal "— hmm, no:" mid-comment, dead `_ = bw`, comment band 190..300 vs code 225..255 — the same scratch class r3 N1 flagged, re-introduced in the fix file.
6. `motion_pixel_setup` indexes `flow.packets[0]` before the caller's length check — panics instead of the intended exit-2 if the spawn yields nothing.
7. `check_manifest_prefix` duplicates `check_manifest`'s ~40-line header block (will drift) and silently drops the ticks-vs-hash-lines consistency check.
8. `motion_strip.odin` header still says the T1 manifest is "NOT re-verified here" — contradicting the W4 code it ships — plus an orphaned fragment from the N9 rewording.
9. `interp_alpha_from_accum`'s doc is glued onto `interp_continuous`'s comment block; `interp_continuous` lost its own doc.
10. [r3 N2, carried] Trail echoes multiply RGB by the fade in addition to alpha while the comment says "body color at low alpha" — mechanical mismatch stands; aesthetic verdict deferred to the k3 re-check (vision caveat).
11. [r3 N5, carried] AC's literal "100 ms" strip evidence remains the documented 60 Hz/17 ms substitution — not re-litigated per round orders.

### Reviewer agreement
- W4 misindex: **codebase + architecture + edge** independently, and Perkins reproduced it by execution.
- Delivery-pin vacuity: **codebase + tests + edge**, and Perkins mutation-proved it.
- Stale counts: blind + codebase + acceptance. Hygiene cluster in `motion_pixel.odin`: blind + codebase + acceptance + architecture.

**Verdict:** READY TO MERGE

Both r3 blockers are fixed and execution-verified; the advisory gate passes; remote CI now enforces the pins. The four warnings are harness/test-integrity items with no silent-failure path (the W4 defect is loud-only; the pin gaps have verified-real production guards) — well-scoped for a follow-up, none block the merge.

_Address findings and push — I re-review automatically on the new sha.
The loop runs until an APPROVED verdict._
