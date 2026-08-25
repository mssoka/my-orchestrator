## 🤖 Perkins automated review — round 1 (cap lifted — loop until approved)
**Job:** packet-plumber-v2-6.1-era-definition · **Reviewed sha:** 39d2a14 · **Reviewers:** 7/7 completed
**Verification:** 25/26 findings confirmed against the code — 1 discarded as false-positive (a claimed Odin compile error contradicted by this worktree's green 10/10 suite)

**Mechanical verification (orchestrator-owned, goldens partition):** all 34 re-blessed `.log.bin` are header-only — version byte 4→5 + `catalog_hash` field only, era byte unchanged, command records byte-identical (byte-compared vs merge-base) · zero existing `.png` churn (only the 2 new era_advance captures) · fold-check PASS (`boot` tick-1 shift is the catalog fold alone, bytes 33..40; new tick-1 `0e1e1afe…` matches the blessed manifest) · `tools/ci-local.sh --mac` **10/10** in this worktree (golden harness incl. `era_advance` PASS + drift rows incl. `bad_era`; replay bit-for-bit). **Mutation checks (non-vacuousness):** removing the E14 gate kills both `test_era_advance_e14_deferred_by_crisis` and `test_era_advance_deferred_replay_identity`; removing the packet missing-roster direction fails `check_reject_eras` — both reverted clean.

### Blockers (0)
None. The hard blocker class is clean: the advance is a logged command (E10 by construction), replay identity is asserted for both the fired AND the E14-deferred path (real engine crisis, not a stub), the seam sits exactly at the reserved [LATER] slot (after `health_update`, before `win_lose_eval`, terminal-barrier-skipped), LOG_VERSION 4→5 is header-confined, the re-bless is partition-exact, and the named follow-ups (6.2 conditions, 6.3 legacy decay, eras 1/2 re-tune + 4–6 content, app-side trigger) are NOT in this diff — scope guard held.

### Warnings (7)
1. **`demand_era` is validated at load but never read at runtime** [acceptance, security, architecture, edge, codebase] — `core/catalog.odin:1232` validates the BOUND row's classes against the roster, but the director spawns `cat.demand.eras[state.era-1]` (`core/demand.odin:52`) — a row with `demand_era != era` passes load while the served row is never roster-checked. No live bug (shipped data has `demand_era == era` everywhere); enforce the equality at load (one fail-fast row) or route the director through the binding.
2. **Sparse `eras.json` pads gap eras to empty `Era_Row{}` that pass `era_row`/`era_advance_validate`** [blind, edge, security, architecture, codebase] — `core/catalog.odin:1243` + `core/era.odin:52`: rows {1,3} load clean and era 2 becomes a valid advance target with an empty roster. Latent (shipped table is contiguous); reject non-contiguous tables at load or treat unpopulated rows as invalid targets.
3. **Load comment claims unique era ids; no id-uniqueness check exists** [blind] — `core/catalog.odin:1077` vs the era-number-only `seen[]` guard. Enforce or stop claiming.
4. **Demo lowering validates each `advance` only against the START era** [blind] — `harness/run.odin`: duplicate/non-forward advance chains pass lowering and bless a `replay_error` log, against the block's own "never bless a poisoned log" comment. Track the running target across sorted advances at lower time.
5. **Pipe-tier exact-equality invariant has no fail-fast row; node premature-listing direction untested** [tests] — `core/catalog_test.odin:741`: packet both directions + node missing only; the pipe-tier loop (`core/catalog.odin:1218-1228`) is unpinned.
6. **PR body omits the required ODN-16 citation (Acceptance #4)** [acceptance] — ODN-5/E14/stories-v2 6.1 all present; the story's own system tag is absent.
7. **Advisory test gate: CONCERNS** [tests] — P0 100% (incl. both replay-identity paths + the real-crisis E14 deferral); P1 gaps per warning 5 + the notes below.

### Notes (10)
`era_step` takes `cat` but never uses it + the seam comment overclaims "loads the unlocks" · demand-switch test hardcodes `e.class == 1` instead of `class_index` · era domain documented as both 1..6 and 1..64 · missing `demand_era` key reports "has no demand.json row" instead of "missing field" · PR body says "20 new fail-fast rows", the test adds 22 (coverage exceeds the claim) · no unit binary roundtrip for `Cmd_Era_Advance` (golden replay covers tag 7 end-to-end) · advance pending on the terminal tick untested · `to_era=0` boundary + last-write-wins double-latch untested · harness `advance` verb fail-loud paths lack negative coverage · `era_record_run` is a fifth near-copy of the step-collect-hash loop (resume delta unexercised).

### Reviewer agreement
Both lead warnings carry 5-source agreement (the strongest signal in this review): the `demand_era` binding/runtime mismatch and the sparse-era gap rows. Both are latent data-contract holes with zero shipped-data impact — none rise to the round's blocker class (the FSM is replay-deterministic on both paths; the invariants bite and are mutation-checked; the re-bless partition is byte-exact).

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha._
