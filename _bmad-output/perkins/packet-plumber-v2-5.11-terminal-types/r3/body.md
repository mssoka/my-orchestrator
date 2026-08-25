## 🤖 Perkins automated review — round 3 (cap lifted — loop until approved)
**Job:** packet-plumber-v2-5.11-terminal-types · **Reviewed sha:** `d0c2c38` · **Reviewers:** 7/7 completed
**Verification:** 51/71 findings confirmed against the code — 20 discarded as false-positive (44 substantive → 16 distinct after dedupe; 7 advisory-gate statements)

### Fix audit of round 2 (the round's contract) — CLEAN

- **B1 — W9 honest re-pin: FIXED and BITES.** EXPECTED is the doubled ask (20×WINDOW), counting is window-gated, campus-must-exist + campus-must-source, honest message, grown-mesh start map. Verified by mutation on the fresh tree: floor raised to 100% still passes (actual ≥ 36000 — your 36000/36000 claim is true; campuses alone landed exactly 18000 = their full half); surge multiplier 10→1 **fails** (3600 < 34200 — the floor is coupled to the gate); campus entry removed **fails at both gates** (got 0 / 18000 < 34200). Seeded-campus removal still passes — doctrine-consistent (growth builds the crowd; the pin is the landable ceiling).
- **W1 palcheck: FIXED and BITES.** Canon hexes scanned over the terminal_types frame (176px / 1100px — your exact numbers); wiping the small_biz tone fails the gate (0px).
- **W2 ratio windows: FIXED and CALIBRATED.** Base ≥4x / surge ≥10x asserted separately; measured 6.51x / 16.42x — mutation to 7x/17x fails both. No knife-edge.
- **W3 citations: FIXED.** [ODN-5] [ODN-7] [E10] [E31] [E9.1] all present.
- **W4 inertness pin: FIXED and BITES** (spawn stream + rng state compared, vacuity guards, equality fails on a live-role trim) — but the new test introduces the blocker below.
- **Both r2 header notes fixed**; 13/20 carried notes fixed (N8 resolved-by-design); 7 carried (see notes).
- **Fold integrity: MECHANICALLY VERIFIED vs v2.** All 31 pre-existing `.log.bin` differ in exactly 8 bytes (the catalog hash, `17d3baf8c6e1df7f` confirmed in-tree); `terminal_types` the only new log; ALL 72 pre-existing PNGs byte-identical except the two node_health frames (the T2 partition, exactly as claimed). 194 core tests + 10/10 gates green on my run; a lens independently re-ran the harness (33 demos, drift-check 233/233 rejected) and reproduced your PR-body splice values (`d1d2e53b…` / `ab1fb0d0…`) from the committed tree.

The delta hunt (the fold commit itself) found two new issues — one of them blocks:

### Blockers (1)

1. **NEW — `test_role_absent_demand_inert` double-frees the trimmed entries array** — `core/demand_test.odin:530` + `core/catalog.odin:982`. `defer delete(trimmed)` runs LIFO before `defer catalogs_destroy(cat2)`, which frees the aliased `eras[2].entries` again. Flagged by the runtime on **every** suite run: `+++ bad free @ [catalog.odin:982:catalogs_destroy()]`; a standalone double-delete repro under the default allocator **aborts** (Abort trap: 6). The suite stays green only because odin-test's tracking allocator masks it — "10/10 gates green" is carrying a live UB warning. *Fix:* delete the `defer delete(trimmed)` line (ownership passes to cat2; one line). [10 reviewers]

### Warnings (1)

2. **NEW — W9's `hosts >= 8` clause is vacuous and mislabeled** — `core/demand_test.odin:726`. The fixture pre-seeds 14 streaming-capable terminals (≥8 at tick 0; seeded capacity 25.7/tick alone satisfies MIN_LAND), so the test passes with growth completely dead — while the message says "growth must place" and the header claims the trio is "re-validated together". The honest teeth (95% floor + campus-source, both mutation-proven) are intact; the seeded grown-mesh design is sanctioned — the dead clause is the defect. *Fix:* count growth-born terminals separately or reword. [9 reviewers]

### Notes (14)

3. Campus-half landing floor is existence-only — the "campus half must land fully" claim is measured, not pinned (share could fall to ~50–84% unnoticed); assert `campus_window_spawns >= 10*WINDOW*95/100`. [6]
4. `test_terminal_class_profiles` hardcodes `SURGE_AT=1200` (no end bound) while W9 derives the window from the set-piece — a timing re-tune silently mis-windows the split. Derive it like W9. [6]
5. W9's `EXPECTED := 20 * WINDOW` is a literal — no guard that multiplier==10 or the streaming-entry count is 2; retune-up weakens the floor silently. Compute from the entries or assert both. [1]
6. `run_inert` discards `record_run`'s returned array — 2×4.69KiB leak (tracker-logged). Capture + `defer delete`. [2]
7. palcheck 5.11 scan is presence-only with loose floors: a 9↔10 sprite swap passes (both tones present) and partial crops (57%/9% of tone) pass. Raise floors + unit-pin `sprite_index_building`. [2]
8. W9 header's "(era-3 demand 1+1…)" parenthetical is stale post-5.11. [1]
9. palcheck's new block is numbered 1e above 1d. [1]
10. E9.1 primitive-fallback claim has zero coverage (no render tests; palcheck aborts without the sheet) *[carried since r1]*. [1]
11. Fold-splice proof remains prose-only and cites the intermediate golden's tick-1 (`ab1fb0d0…` — the 11c6cf6-era value, matching nothing committed); reproducible with effort but not anchored in-repo. Commit the splice verifier as a harness subcommand *[carried since r1, sharpened]*. [4]
12. Catalog hash folds raw JSON bytes including comments — docs-only edits re-bless every golden (this fold's own trigger) — accept or hash canonical JSON. [1]
13. Health-ring radius sits inside the campus half-footprint for most of the pulse *[still present since r1]*.
14. `expect hash stable` parsed but never enforced *[still present since r1]*.
15. Growth type-draw composition (campus 4/8) unpinned *[still present since r1]*.
16. `test_catalog` hand-mirror not tied to `data/*.json` — profile numbers restated in three places; data mutations invisible to the suite *[still present since r1]*.

### Reviewer agreement
The blocker was found independently by **10/7 lens-wave instances** (all six code-wave lenses + three g-wave re-sightings); the warning by 9; note 3 by 6; note 4 by 6. Rejected as false-positives: 20 (the 5×-rejected wholesale-re-bless class ×10, identical-log-blob class ×2, chunking artifacts ×2, a "flaky suite" claim traced to my own mutation-probe window contaminating one lens run — 28 clean suite runs since, and misc).

**Verdict:** NEEDS CHANGES

The fix-audit contract is fully satisfied — B1 bites honestly, W1–W4 landed, header notes fixed, fold partition exact. One new delta-introduced blocker (the double free) is all that stands between this and approval: drop the `defer delete(trimmed)` line, push, and r4 should be fast.

_Address findings and push — I re-review automatically on the new sha._
