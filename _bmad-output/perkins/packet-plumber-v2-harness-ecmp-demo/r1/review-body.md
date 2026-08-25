## 🤖 Perkins automated review — round 1 of 3

**Job:** packet-plumber-v2-harness-ecmp-demo
**Reviewed sha:** f90351da
**Reviewers:** 7/7 (blind, edge, acceptance, security, architecture, codebase, tests)
**Verification:** 7/7 surviving findings confirmed against the worktree — 18 raw lens findings, 11 rejected as duplicates, 0 rejected as false-positives

**Diff:** 663 lines — `demos/demolish.dem` (captures added), `demos/ecmp.dem` (NEW), `goldens/{demolish,ecmp}/*.png` + `goldens/ecmp.t1` + `goldens/ecmp.log.bin` (NEW, first-bless), `harness/{demo,drift,goldens,run}.odin`. Core untouched. Single wave, no chunking.

### Blockers (0)

### Warnings (3)

1. **spawn_node coordinates silently truncate i64 to i32 — negatives and out-of-range values accepted, no fail-loud range check** — `harness/demo.odin:119-121` — 7-lens agreement (blind/edge/acceptance/security/architecture/codebase/tests). `strconv.parse_int` returns i64; the unchecked `i32(x)` cast wraps values outside i32 range (e.g. `3000000000` → bogus position) and negatives parse fine. Contradicts the PR's own fail-loud stance ("The type name resolves against the catalog at lower time (fail loud…)"); a wrapped position is deterministic, so the golden gate cannot catch it — a nonsense topology would be first-blessed silently. Fix: range-check both coords before the cast; add one bad-coord test.
2. **T2 mismatch/corrupt/no-golden branches + save_diff_bundle (the PR's own allocator + JSON fixes) have zero automated exercise** — `harness/goldens.odin:97-190` — tests lens. The minion's own comment admits this path "was latent until the first real T2 miss" — the exact bug class this PR fixed has no regression pin. Perkins live-probe confirmed the no-golden branch fails loudly at f90351da (never a silent accept); the pixel-mismatch branch is untested. Fix: a golden-tamper negative test (corrupt / flip pixels / delete → run must FAIL).
3. **Advisory test gate: CONCERNS** — P0 (golden-blessing discipline) is exercised and green (8/8 demos, drift 47/47, live negative probe); P1 error-path coverage sits ~80-89% (the two tests-lens gaps above).

### Notes (4)

1. `parse_demo` error returns leak cloned `spawn_node` type_name strings + dynamic backings (6-lens agreement) — `harness/demo.odin:114` — bounded CLI fatal path; free clones before error returns.
2. `fixture off` + spawn referencing ids outside the spawn_node set: packets silently inert, demo still blesses green — `core/flow.odin:76-78` — pre-existing core behavior newly exposed by `fixture off`; validate spawn src/dst at lower time.
3. New directive error paths (bad spawn_node/fixture lines, unknown node type, run-setup-failed) exercised by nothing.
4. Fixture-on + spawn_node combined numbering (fixture ids 0..2, entries follow at 3..) unexercised — deterministic by construction (E11), optional pin.

### Verification (independently re-run at f90351da in the round worktree)

- `odin test core`: **54/54 green** · `tools/lint.sh`: **5/5 gates green**
- **rlsw fresh from-scratch build works** (`tools/build_raylib_sw.sh` → shadow root → harness links; PLATFORM_MEMORY + `-ffp-contract=off`)
- `harness run` (all 8 demos, T1 hashes + T2 pixels + replay gate): **8/8 PASS** — bundle/flow/draw/win/lose matched bit-for-bit (**NO drift**); ecmp + demolish first-blessed goldens reproduce
- `harness drift-check`: **47/47 mutations rejected** (ODN-11 gate bites)
- **T2 comparison path live-verified**: missing golden → FAIL with explicit message (restored after; worktree left pristine)
- **First-bless pixel content verified**: ecmp 1250/1350ms frames show the ECMP split on both equal-cost legs (2 packets in flight, mirrored); 3000ms settled (0 packets); demolish frames show the leg vanish at the demolish (1804px band), re-forward on the survivor pipe, settled. Genuine captures, not blanks or noise.
- **spawn_node determinism [E10/E11]**: ids = monotonic `next_node_id` spawn order (core/topology.odin:128-131), array-indexed file order, no RNG, no map-iter
- **`{{}}` diff.json fix verified CORRECT** for this Odin nightly's fmt (braces are special; the old single-brace string emitted `%!(MISSING CLOSE BRACE)` garbage — the PR fixes it, does not introduce it)
- **Demo_Replay single-struct threading correct**: run_demo's cfg shares type_name strings with the live Demo and correctly skips `demo_replay_destroy` (no double-free); standalone paths own their clones; replay-side run-setup failure is a defined rejection
- **ecmp.t1 header consistent**: seed 42, 80 ticks = 4000ms @ 20Hz, catalog_hash 99a32393078e0cca matches all 8 goldens
- **Core untouched [ODN-1]** — diff touches demos/goldens/harness only; no engine types leak

### Reviewer Agreement

Cluster A (spawn_node coordinate bounds) reported by all 7 lenses; Cluster B (parse-error string leak) by 6 — both confirmed, both non-blocking dev-tool robustness gaps.

**Verdict:** READY TO MERGE

The harness mini-story delivers what it claims: the T2 pixel debt (deferred since 2.2) is closed with a working, deterministic, bit-exact rlsw pipeline, first-blessed goldens are genuine, no legacy golden drifted, and every load-bearing invariant (determinism, blessing discipline, ODN-11 replay, ODN-1 core separation) verified green at the reviewed sha. The 3 warnings are coverage/robustness hardening for future rounds — worth addressing in a follow-up, none blocking.

---

_Address findings and push a fix commit to `v2-harness-ecmp-demo` (or a follow-up branch) — a fresh Perkins round will re-verify. Reviewing minion: Perkins (automated, headless mode, round 1 of 3)._
