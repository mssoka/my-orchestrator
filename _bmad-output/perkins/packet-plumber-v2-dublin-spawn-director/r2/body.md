## 🤖 Perkins automated review — round 2 (FIX-AUDIT)

**Job:** packet-plumber-v2-dublin-spawn-director · **Reviewed sha:** `04ef6a9` · **Reviewers:** 21/21 completed (7 lenses × 3 chunks; one edge-data retry after a 429 burst)
**Verification:** 53/56 lens findings confirmed against the code — 3 discarded as false-positive; merged into 24 consolidated findings. Perkins independently re-ran the full core suite (261/261 green) and **four mutation legs at the reviewed sha** (details below). CI 13/13 is claimed, not re-run.

### Fix audit (r1 → `04ef6a9`)

| r1 finding | Verdict |
|---|---|
| **B1** ATTACH bias pin absent | **FIXED — mutation-verified by Perkins.** `test_growth_dublin_attach_cluster_pick_bias` runs distinct weights (city 4 vs suburb 1, 10 windows × 6 seeds, honest 1.5× bar). Perkins re-applied the uniform-pick mutation at HEAD: fails exactly as claimed (`A=27 B=27` dead-even). |
| **W1** cross-boundary attach leaked the cap | **FIXED — mutation-verified by Perkins.** The attach branch now cap-checks the **drawn tile's own district** (a zero-draw rejection predicate, `growth.odin:959-969`), pinned by `test_growth_dublin_attach_tile_district_cap`. Perkins re-applied the check-removed mutation: a spawn lands at `[15,5]` in capped B and the pin fails. One liveness residue filed as a **new warning** below. |
| **W2** demolish-frees-budget vacuous | **ACKNOWLEDGED honestly** (spec + this PR's r1-fold section) — but the fold is incomplete: canon row 4 below still claims it, and the memlog cites balance.json comments that don't exist. Filed as a warning. |
| **W3** routers-excluded unpinned | **STILL PRESENT.** Perkins re-ran the routers-count-too mutation at HEAD: 261/261 pass. |
| **W4** loader pass-3 unasserted | **STILL PRESENT (narrowed).** The shared `map_board_partition` builder pins the semantics; the loader call site is still unasserted — deleting it passes all 261 core tests. |
| **N-folds** | 111/113 tally corrected; the 603-tile census **independently re-verified by Perkins** (stride-6 + C-round replication yields exactly 603); dead predicate removed; fractional/floor-667/zero-tile pins present; audit header + census line land in `spawn-audit.txt`; dublin-grown bound/usage/comment fixes real. One overstatement: the "loader + 4 fixtures" claim misses `growth_test`'s `one` fixture (note). |

### Blockers (0)

None.

### Warnings (4)

1. **STILL PRESENT since r1 (W3): `growth_district_live_count`'s Terminal-only filter is unpinned** — a routers-count-too mutation passes the entire suite (Perkins re-ran it: 261/261). The district cap's denominator semantics rest on an unpinned predicate. `core/growth.odin:530-541` · *Fix: one pin — a routers-only district reads live=0.* [acceptance, codebase, tests]
2. **STILL PRESENT since r1 (W4, narrowed): the loader's pass-3 partition call is unasserted** — deleting `map_board_load`'s `map_board_partition` call passes all 261 core tests (Perkins re-ran it); only golden replays catch it. The shared builder pins the semantics, not the loader call site. `core/map.odin:417` · *Fix: one assertion in the loader district test — `district_tiles` partitions `spawn_candidates` exactly.* [acceptance, codebase, tests]
3. **DELTA (W1 fold): a cap-locked attach ring starves SEED.** At the default bias (1000‰ = every attempt), an eligible estate whose every placeable ring tile sits in capped districts wins the weighted draw, rejects every candidate at the drawn-tile check, burns the 8-attempt budget, and skips the window — while SEED only fires when **no** eligible cluster exists. Cluster eligibility (`has_room`) checks E31-room but not cap-blockage, so the state is stable: districts **under cap with legal SEED placements receive nothing** — a permanent growth stall reachable at 667‰ long runs as districts fill. No wrong state, no cap leak, determinism intact (the rejection semantics are the spec's design — the eligibility gap is not). `core/growth.odin:800-810, 959-969` · *Fix: mirror the drawn-tile cap into cluster eligibility (cap-locked ring ⇒ ineligible ⇒ SEED takes over), or document the stall as bound-first behavior.* [edge]
4. **W2 fold incomplete (record consistency):** canon row 4 still claims "demolished terminals free the budget" as delivered behavior, contradicting this body's own r1-fold acknowledgment; `growth.odin:530`'s comment still asserts it un-qualified; the memlog cites "balance comments" — `balance.json` carries none. The acknowledgment itself is honest where it lives (spec + fold section). *Fix: amend row 4 ("inherent: counts derive; demolish is E2-forbidden — see r1-fold"), fix the memlog, optionally qualify the comment.* [acceptance, blind, codebase, tests]

### Notes (20)

- **Advisory test gate: PASS** (P0 100%, P1 ≥90% — B1's closure lifted r1's CONCERNS; the P2 residue is W3/W4). [tests ×3 chunks]
- The "shared `map_board_partition` (loader + 4 fixtures)" fold misses the 5th former site — `growth_test.odin:1129`'s `one` fixture still hand-builds `district_tiles`.
- Spec retains stale "48/48 byte-identical, zero re-bless" / "48-golden suite" phrasing (spec:164,226) — the delivered 49/51/111-113 reality is documented elsewhere in the same file.
- PR body presents 4-seed bias measurements (A=25 B=11 / A=16 B=21) unlabeled beside the shipped 6-seed pin (Perkins' 6-seed mutation reproduced 27:27 exactly — the numbers are real, the basis switches silently).
- District anchor x/y load unvalidated → unchecked `i32(round(f64×10))` in `map_district_assign` (corrupt-data hardening; in-repo data today).
- **Carried since r1 (N3):** `growth_districts` rows still parse via lenient `jint` — "4.9"→4 silently (the post-parse 1..1000/0..1000 range checks do reject wraps/negatives — the ≥2³² escalation was discarded on verification).
- `map_board_partition`'s allocator param threads only the outer array (inner lists append on `context.allocator`) — cosmetic.
- `seed_weights: [6]i32` has no load-time coupling to `District_Kind`'s length — a future 7th kind silently weight-0s or traps (`static_assert` is one line).
- `district_kind_name`'s doc claims "the render's label tier" reads the enum — no render code references `District_Kind` (audit-only today).
- dublin-grown's arg-count guard prints usage() but never exits — the standing convention across every harness verb (not a deviation).
- No empty-districts guard in `map_board_partition`/`map_district_assign` (unreachable via the fail-loud loader; defensive only).
- `dublin.json` is a sim input but not byte-bound into any golden header (catalog_hash folds only the 7 catalog sources) — behavior IS bound (per-tick state hashes + replay re-derivation); the residue is byte-binding asymmetry.
- **Delta (fold):** the W1 check calls `map_district_assign` twice for the same `pos` on one line (`growth.odin:966`) — free to halve.
- **Carried since r1 (N7):** district live counts re-derived O(districts × nodes) per eligibility test / now per drawn tile too.
- **Carried since r1 (N17):** `run_dublin_grown` is the 5th hand-rolled `Demo_Replay` construction.
- Loader tests free names + `district_tiles` cross-allocator (`load(temp_allocator)` + `destroy` on `context.allocator`) — pre-existing pattern this PR extends; benign in practice.
- `seed_weight 0` (the deliberate band-exclusion tunable) has no loader-acceptance test.
- The fractional-anchor pin doesn't hit a scale-10 quantization tie (a .5-boundary case).
- The W1 pin would pass vacuously on a zero-spawn path (no `spawns > 0` floor) — the mutation leg keeps the path live today.
- `dublin_board.dem`: router tile (20,15) is claimed a pool tile — it is not ((16,12) is; Perkins' 603-tile replication confirms). Flavor comment, zero behavior impact.

### Reviewer agreement

The two carried warnings (W3/W4) were independently reported by 3 lenses each across all 3 chunks and confirmed by Perkins' own mutation re-runs; the W1 liveness gap by the edge lens across all 3 chunks with consistent code paths. The 429-retry lens (edge-data) delivered a valid verdict on retry — no failed layers.

**Verification detail:** 56 raw findings → 53 confirmed (24 after merge: 4 warnings, 20 notes) → 3 discarded (the jint ≥2³²-wrap escalation — the range checks reject it; the census "should read district_tiles" style preference — same proc, no drift possible; the input_parity log-sibling observation — r1-settled by design).

**Verdict:** READY TO MERGE

Four warnings (two carried P2 coverage gaps, one bounded liveness gap with a one-predicate fix, one record-hygiene residue) — none block the merge; all are one-line-to-one-test fixes if you choose to fold them.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
