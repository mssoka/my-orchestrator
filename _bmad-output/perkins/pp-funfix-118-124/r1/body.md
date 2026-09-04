## 🤖 Perkins automated review — round 1

**Job:** pp-funfix-118-124 · **Reviewed sha:** 7b109d3 · **Reviewers:** 6/7 completed (blind failed: output-length cap, then a provider error on its one retry — degraded, disclosed below)
**Verification:** 19/19 findings confirmed against the code — 0 discarded as false-positive

**MEGA-DIFF shape (disclosed):** 93,959 lines (61ea014..7b109d3); `gh pr diff` is API-capped, so the canonical diff was generated locally and chunked per the two-class protocol — full 7-lens attention on the CODE chunk (737 lines, 13 files: the health/catalog/sources, both new goldens' .dem scripts, tuning JSON, tests, PR body); the golden bulk (120 .t1/.log.bin + 14 PNG) got mechanical verification only.

**Mandate legs (independently verified, mutation-tested):**
- **#118 real and load-bearing** — grace 400→900 revert verified by experiment: `health_lose` death moves 51.65 s → 26.65 s; `health_recover` fight-back becomes impossible (dead @ 26.65 s). The tuning table's unprepared-repro row rebuilt and confirmed EXACT on both sides (dip 77.5 s / dead 82.0 s after; dip 52.5 s / dead 57.0 s before).
- **#124 real and pinned** — killing the refill branch in code fails exactly `test_health_meter_refill_streak_in_grace` (RED-then-GREEN verified). `health_recover` demonstrates a real recovery loop end-to-end: meter 100 → trough 40 @ 50.65 s → 100 @ 53.65 s (stats-stream verified; pre-fix the same run dies at 26.65 s).
- **#115 tension preserved** — the unprepared build still dies (meter 0 @ tick 1033); the lose state is reachable; the drain/E16/E17 bytes are untouched.
- **Suites** — `odin test core` 300/300; `harness run` 52/52 (replay gate: every blessed log re-sims bit-for-bit); `input-parity` 27 green; `tools/ci-local.sh --mac` 13/13 gates; drift-check 375/375 mutations rejected. CI billing-block signature noted, not gated (local gates are the merge ground truth).
- **Re-bless census** — one raster convention (14/14 PNGs 1280×720 8-bit RGBA); all .t1 shifts are the disclosed catalog-hash fold + the intentional grace-timing beats; replay gate green proves behavior preserved where it should be.

### Blockers (0)

### Warnings (4)
1. **#124's new refill arm is never exercised by any golden** — `health_recover`'s heal rides the pre-existing all-clear recharge (breach exits at ~1013 before healing starts), and the PR tuning table cites that demo as `meter_refill_per_tick`'s measured effect. Proven by mutation: `meter_refill_streak_ticks 200→1000000` leaves the golden behaviorally identical (min 40 → 100, score 49). The mechanic is real (unit-pinned, mutation-verified) but ships unit-test-only; the acceptance criterion's "demonstrated in a golden" is met for the recovery loop, not for the new arm. [architecture + acceptance + tests + codebase + Perkins mutation] — *Fix: extend the golden (or a sibling) so a class stays breach-latched-in-grace with meter <100 while the +1/tick refill visibly heals; re-cite the table row.*
2. **Shipped grace 900 has no unit-level pin; the determinism fixture keeps 400** under a "mirror the data file" comment this same diff invalidates (while adding a "MUST carry the real values" comment for the meter_refill pair). [architecture + tests + codebase] — *Fix: mirror 900 + re-derive pins, or document the deliberate divergence.*
3. **`health_recover.dem` misdescribes its own timeline** — the fix lands at 40.0 s, the drain starts at 49.2 s (measured): the fight-back happens inside the grace, not "mid-drain" as the header and PR body say; the frozen spec committed in this PR (spec line 51) prescribes the mid-drain-fix order. [acceptance + Perkins stats] — *Fix: re-time the fix past 49.2 s (which would also let the trough demonstrate the W1 refill arm) or correct spec/header/PR wording.*
4. **`era3_surge_survivable.dem` header claim "Pre-fix (grace 400) this exact mesh DIED at ~57 s" is false** — under reverted grace 400 the same demo wins identically (score 213, meter 100): the cold 13-leg mesh never breaches, so the golden is insensitive to the knob its header credits (the knob's load-bearing proofs are `health_lose`/`health_recover`). [Perkins mutation] — *Fix: correct the header's provenance line, or re-shape the demo to a hotter mesh.*

### Notes (6)
- New balance keys parse via lenient `jint` (float truncation, i32 wrap) where `jint_strict` exists — consistent with all sibling health keys; doctrine hygiene. [security]
- balance.json comment "4× slower than the drain cap" is 2× under shipped values (1 vs 2), clause garbled. [architecture + codebase]
- Test-comment arithmetic drift: "~330" vs "~400" expiry; `blocked_by_drain` docstring ~5/~105 vs inline ~85/~185. [acceptance + codebase]
- `health_lose.dem` header keeps stale "(0.25 s)" beside breach ~tick 84 (= 4.2 s). [acceptance + codebase]
- #115 citation points at the HUD-signifiers issue; the lose-state evidence lives in the neweyes playtest doc ("#115 adjacent") — shorthand inherited from the job briefing. [acceptance]
- Advisory test gate: PASS (P0 100%, P1 100%, overall ~90%). [tests]

### Reviewer agreement
- **W1** is a 4-lens convergence (architecture, acceptance, tests, codebase) with independent mutation proof — the round's headline finding.
- **W2** converged across 3 lenses. N2/N3/N4 each converged across 2.

**Degraded disclosure:** the blind lens output-capped (the flash truncation-canary class) and its one retry died on a provider error; the verdict stands 6/7 with compensating verification — Perkins performed line-by-line hunk verification of the full 737-line code chunk plus the four mutation legs above; no diff-only finding class remained unexamined.

**Verdict:** READY TO MERGE

_0 blockers; the 4 warnings are documentation/coverage-honesty fixes, all foldable without touching sim behavior (the harness is green and the re-bless is sound). Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
