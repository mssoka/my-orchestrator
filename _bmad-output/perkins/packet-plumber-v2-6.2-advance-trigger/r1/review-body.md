## 🤖 Perkins automated review — round 1 of 3

- **Job:** packet-plumber-v2-6.2-advance-trigger · **Reviewed sha:** `58dc3bc9fee9642d14ce16332f64d7703732377f`
- **Reviewers:** 7/7 lenses completed (blind, edge, acceptance, security, architecture, codebase, tests — kimi k3, worktree-rooted)
- **Verification:** 24/26 findings confirmed on re-verification against the worktree (1 rejected as false-positive, 1 demoted). Goldens chunk verified mechanically (byte-level), not by lens.
- **Local CI (run independently by Perkins this round):** `tools/ci-local.sh --mac` **10/10 PASS** (215 core tests, golden harness + replay gate, drift-check, stats replay-identity, input-parity 24/24). Note gate 4/6 pass *hollow* for the gate demos — see the blockers.

**Diff note:** the PR diff exceeds GitHub's 20k-line API limit, so the canonical diff was built locally from the reviewed worktree (base `192468d`, exactly the 2 PR commits) and chunked: code+demos+harness+data+docs (2,871 lines → full lens wave) and goldens (~53k lines → mechanical fold verification).

### Golden fold discipline (the sanctioned re-bless) — mechanically verified, 0 breaks

- 35 re-blessed `.log.bin`: **header-only** — only the 8-byte catalog_hash field (bytes 17–24) changed; commands/seed/version byte-identical; each new field matches its `.t1` header hash.
- 37 re-blessed `.t1`: only the `catalog_hash` line + per-tick hashes changed (the catalog fold rides every tick hash via `state.catalog_hash` in the T1 input); structure + tick counts identical.
- 0 `.png` churn on re-blessed demos; `balance.json` parsed-JSON walk confirms the semantic diff is **exactly** the added `advance` key. The fold discipline held. The 3 new gate demos are another matter — below.

### BLOCKERS (2)

**B1 — The 3 gate goldens were blessed with the advance gate DISABLED** `[edge + acceptance]` · `harness/run.odin:269`
`run_demo`'s `Demo_Replay` literal omits `advance_gate_on` (only `load_demo_replay:688` sets it), and `demo_apply_setup:635` applies the zero value — so the live/bless path runs gate-off. Reproduced directly: `harness replay advance_fire goldens/advance_fire.log.bin` → **`FIRST DIVERGENCE at tick 600`** (exactly the gate-fire tick); a gate-off replay of `advance_block_legacy` matches its manifest **bit-for-bit**. Consequences:
- All 3 manifests pin gate-off runs: era stays 2 for all 1400 ticks — **no `Era_Advanced`, no `Era_Advance_Blocked`**. The demos' header comments, the stories-v2 status fold ("goldens `advance_fire.dem` (conditions met → fires)… each block branch T1-pinned"), and this PR's body are false in the blessed artifacts.
- Deliverable/acceptance **"Golden: T1 of the advance (conditions met → fires); T1 of each block branch" is not met**; the story's GWT "meet the gate → the era advances" has no golden demonstration.
- The standalone ODN-11 replay gate is **red on all 3 demos as shipped**; `harness run`'s `verify_replay` uses the same gate-off cfg for both halves, so CI gate 4 passes hollow. The new demos' T2 pixels (60000 ms captures) are gate-off renders too.
- *Fix:* add `advance_gate_on = demo.advance_gate_on` to `run_demo`'s cfg literal and re-bless the 3 goldens (the acceptance lens verified the one-line fix produces the tick-600 fire + bit-for-bit replay).

**B2 — The drift-check flip classes are vacuous (the shipped guard never bites)** `[perkins + acceptance]` · `harness/drift.odin:113`
`lpath := log_path(name)` is a temp-allocated string held across the mutation loop; `replay_hashes`' per-tick `free_all(context.temp_allocator)` recycles its memory, and the last mutation's `tmp` tprintf overwrites it. The flip then reads `/tmp/pp-drift-<name>-.` (lpath's original 30-char length over the tmp path's memory) → `accepted=false` → `ok := !accepted || …` → vacuous **"rejected (OK)"**. Confirmed by instrumented probe (independently reproduced by two reviewers): the flip never re-sims anything. The `advance_gate_flip` class — new in this PR, the guard this review was explicitly asked to verify — passes vacuously on all 3 gate demos; an honest flip on the actual gate-off manifests would have **failed** and caught B1 before merge. The pre-existing `growth_flip` (5.1) has the identical defect; leftover `/tmp/pp-drift-*-bad_era.bin` files corroborate the clobbering (`os.remove(tmp)` also operates on a clobbered path).
- *Fix:* re-call `log_path(name)` at the flip sites (or clone `lpath` with a stable allocator at loop top); audit `growth_flip` for the same lifetime bug.

### WARNINGS (8)

1. **Block-event dedup (anti-chatter) never pinned** `[tests]` — `advance_gate_test.odin:206`: block tests assert boolean `saw_*` only; an emit-every-tick regression passes all unit tests, and reason-transition re-emits (Crisis→Legacy→Sla) are unpinned anywhere. Assert one `Era_Advance_Blocked` per blocked episode + per reason transition.
2. **Scripted `Cmd_Era_Advance` while blocked is untested** `[tests]` — `:436`: only the healthy scripted path exists; the claimed "the latch holds" while blocked is unexercised. Add a scripted-into-blocked-gate test (latch survives, fires after recovery).
3. **Window validator cap (10000) rejects the documented full-game tuning** `[architecture]` — `catalog.odin:937` vs `balance.json`'s own "~8–12 min/era": 12 min @ 20 Hz = 14400 ticks > 10000 → fail-fast load rejection. Raise the cap or reconcile the documented range.
4. **E15 test's `fire_tick` is dead — fire-after-resolve ordering unpinned** `[blind + tests]` — `advance_gate_test.odin:296`: assigned, never asserted. Capture `resolve_tick` and assert `fire_tick > resolve_tick`, or drop the claim.
5. **`balance.json` wholesale reformat around a 4-line addition** `[blind + codebase + architecture + acceptance]` — 1-space indent, `\u`-escaped UTF-8, exploded arrays, dropped trailing newline; semantically verified clean (exactly the `advance` key) but pure churn that buries the change and diverges from every sibling catalog. Re-emit in the original formatting.
6. **6.1 fold (a) not landed: `demand_era` validated-at-load, never read by the sim** `[perkins]` — `demand.odin:52` keys `cat.demand.eras[era-1]` directly; no equality enforcement. Doesn't break the gate; the fold remains open.
7. **6.1 fold (b) not landed: sparse-era gaps not rejected — the gate can now fire INTO a gap era** `[perkins]` — `catalog.odin:1276` pads empty rows; the gate's era+1 latch bypasses validation; a gap era soft-locks the advance arc (`.Sla` forever). Content-armor (real catalog contiguous), but the gate raises the stakes.
8. **6.1 fold (d) not landed: ODN-16 citation absent from the PR body** `[perkins]` — acceptance-required citations (E15, 3.4, 4.2, stories-v2 6.2) are present; the arch citation for the S6 seam was asked to carry forward.

### NOTES (7)

- **N1** `[edge+architecture+acceptance]` Gate ring/window keyed to absolute run tick, never re-anchored on fire — chained advances skip the sustain window (era-1 start fires 1→2 at 600, 2→3 at 601). Documented MVP scope; must be fixed at the 6.3/full-game seam.
- **N2** `[perkins]` Stand-in legacy predicate over-blocks era 1 (narrow is "legacy" in the era that introduces it) — documented 6.3 seam, named for the record.
- **N3** `[perkins]` `advance_block_legacy.dem` draws the narrow *in* era 2 — under 6.3's draw-era model that pipe is not legacy, so 6.3 will need to re-author this golden. Expected churn, named.
- **N4** `[blind]` Zero-demand test builds then destroys a full fixture; claims a `.Sla` block but never asserts the reason.
- **N5** `[blind]` SLA-block test comment claims a 6/tick sustained flood; code seeds 1/tick through tick 400.
- **N6** `[tests]` Per-class SLA term never exercised with multiple active classes (all block tests are era-2, roster {email}).
- **N7** `[tests]` Advisory test gate: **PASS** at unit level (P0 100% — but the golden leg of P0 is hollow per B1).

### Reviewer agreement (highest confidence)

- **B1** — edge + acceptance, both with independent empirical verification (Perkins reproduced it a third way).
- W4 (blind + tests), W5 (blind + codebase + architecture + acceptance), N1 (edge + architecture + acceptance).

### What verified clean

- **The determinism/replay spine itself is sound:** the gate is a pure function of serialized state (flow.sla accumulators + topology pipe_alive/pipe_tier + crisis.active + era + tick + catalogs); the milestone ring is derived, never serialized; enter-edge block dedup via derived `last_block`; replay-identity unit test + honest replay gates (stats-check, standalone replay on non-gate demos) all pass. E15 crisis block, E24 zero-demand neutrality, window precondition, last-era inertness, disabled-gate 6.1 back-compat all unit-pinned. The fold-only re-bless discipline held (0 breaks). The 6.3 seam predicate is a single clean call site. The core design is approvable — the blockers are in the harness/golden layer, not the sim.

### Verdict: **NEEDS CHANGES**

The gate's sim logic is well-built and well-unit-tested, but the story's required golden evidence does not exist: the three gate goldens pin the exact opposite of their claims (B1), and the drift-check guard added to protect the gate is dead on arrival (B2). Both are small fixes with re-bless.

_Address findings and push — I re-review automatically on the new sha._
