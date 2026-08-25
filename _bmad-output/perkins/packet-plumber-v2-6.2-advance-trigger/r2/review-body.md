## 🤖 Perkins automated review — round 2 of 3

**Job:** packet-plumber-v2-6.2-advance-trigger · **Reviewed sha:** `5cc561942cb44ded620bace196005dbbc4302f42` (head of `v2-6.2-advance-trigger`, base `v2` @ `4521cf7`)
**Reviewers:** 7/7 completed (blind, edge, acceptance, security, architecture, codebase, tests) — 0 failed. ⚠️ Model note: the briefing-pinned `kimi-coding/k3` went quota-dead mid-dispatch (403 billing-cycle, 7/7 first-wave panes; fresh probe recorded in `quota-regime.json`); the wave was relaunched on `zai-coding-cn/glm-5.3` (probed OK — the sanctioned reasoning fallback per regime policy).
**Verification:** 22/22 lens findings re-verified against the round worktree — 21 confirmed, 1 discarded (tag-14 byte-layout: rejected on the r1 precedent — the layout-test convention covers tags 1..7; 6.1's tag-13 shipped identically and was approved; no production payload reader exists). Plus Perkins-originated checks: full `tools/ci-local.sh --mac` **10/10 PASS**, 3 gate-demo replays bit-for-bit, an instrumented drift-check probe (inserted + reverted), and byte/pixel-level fold verification of the goldens chunk.

### Fix audit (round 1 blockers + folds)

**B1 — FIXED AND BITES.** `run_demo`'s cfg literal carries `advance_gate_on` (`harness/run.odin:281`); all 3 gate goldens re-blessed gate-ON. Empirical: `harness replay` on all 3 = 1400 ticks **bit-for-bit (ODN-11)** — r1's divergence at exactly tick 600 is gone — and a gate-off re-sim of any of the 3 manifests diverges at tick 600 (probe: `accepted=true n=1400 first_div=599`), proving the blessings are genuinely gate-ON.

**B2 — FIXED AND BITES.** Both drift-check flip sites re-call `log_path(name)`; `growth_flip` audited as demanded. Probe: honest re-sims, not vacuous rejections (`growth_flip accepted=true n=640/1800/420 first_div=39`; `advance_gate_flip accepted=true n=1400 first_div=599`); clean-build drift-check: **306/306 mutations across 43 demos all rejected**.

**Folds:** W3 ✅ (cap 20000 + tests) · W5 ✅ (formatting restored; parsed-JSON semantic diff vs base = exactly `ADDED .advance`) · W6 ✅-with-new-gap (routing landed — see W2/W4 below) · W7 ✅ (dense-table rejection + test row). **Still present (carried):** W1, W2, W4, W8 + notes N1–N6. The rebase folds held mechanically: 40 pre-existing `.log.bin` header-only, 0 non-a11y PNG churn, input-parity T1s re-blessed, and the 5 a11y PNG re-blesses reproduce the claimed latent-v2-defect signature pixel-level (warm-cream → cool-blue-grey, ~5k px, single region).

### BLOCKERS (1)

**1. `test_advance_gate_scripted_request_still_gated` is vacuous — it cannot fail if a scripted advance ignores the gate** [tests] · `core/advance_gate_test.odin:438-441`
The test scripts `Cmd_Era_Advance{to_era=3}` at tick 100, runs 700 ticks, asserts only `era == 3`. Traced: an **ungated** scripted fire at tick 100 also lands era 3 (era 3's standard pipes are legacy in the test table, blocking 3→4 forever) — era==3 at tick 700 either way. The `Era_Advanced` tick (600 gated vs 100 ungated) is collected but never asserted, and no golden covers scripted+gate-on (`era_advance.dem` is gate-off). This is the **only pin** for the story contract "a scripted advance still works, gated the same way" — on a win-condition canon surface — and it cannot catch its own regression class. Same vacuity genus as r1's B2: a shipped guard that never guards.
**Fix:** assert the `Era_Advanced` event tick ≥ 600, or step only 500 ticks and expect `era == 2` with the latch held. (Three lines.)

### WARNINGS (new: 4 + gate)

**2. `overlay_check`'s `Demo_Replay` literal omits `advance_gate_on` — the B1 flag-threading missed the third cfg site** [edge + acceptance] · `harness/overlay.odin:46-52`
The PP_DEBUG overlay verb re-sims the 3 gate demos **gate-off** — its exported verification frame silently shows the wrong sim. No golden/CI/app impact (gate 8 is compile-only): the r1-B1 defect class caught at its one residual site. One-line fix mirroring `run.odin:281`.

**3. The W6 fold routed only the director — crisis/health(surge)/warnings still key demand rows by direct `era-1` index** [architecture] · `core/crisis.odin:337`, `core/health.odin:117`, `core/warnings.odin:239` vs `core/demand.odin:59`
On any legal-but-divergent era table (`demand_era != era`), the director reads row `demand_era` while the other three read row `era` — split-brain demand views in one run. Real catalog is identity (unaffected today). Route the three readers through the binding, or enforce identity at load.

**4. The new `advance` block parses via lenient `jint` — a decimal silently truncates instead of failing fast** [edge + security] · `core/catalog.odin:939-940`
`600.5` loads as `600` and passes validation; `jint_strict` exists precisely because decimals are fail-fast rejections for new content (28 uses elsewhere; ODN-5). Mitigation: consistent with balance.json's legacy loader convention. Switch the two reads to `jint_strict`.

**5. The W6 binding has no distinguishing test — only identity rows (`demand_era == era`) are ever exercised** [tests] · `core/demand.odin:55-59`
The fold can silently regress to direct indexing with nothing failing; the divergent era-4 row is reached but never asserted. Add a unit test pinning era 4's plan == the demand_era-3 row.

**Advisory test gate: CONCERNS** [tests] — the apparatus is honest and biting post-rework (empirically re-verified), but blocker 1 + warning 5 leave the scripted-gated contract and the W6 divergence point unpinned. Fix those and the gate returns to PASS.

### NOTES (new: 8)

6. Redundant era-table test scaffolding: `era_test_catalog_3` rebuilds a table `test_catalog` already carries (equivalent fixture, display strings aside); `era_test_catalog` overwrites (and leaks) the prior array [blind + architecture + codebase] · `advance_gate_test.odin:27-31`, `era_test.odin:32`
7. `gate_record_run` duplicates same-package `era_record_run` verbatim [architecture] · `advance_gate_test.odin:51-73`
8. The B2 re-call pattern leans on a documented-but-implicit ordering (path read before any `free_all`); a stable clone would be invariant-independent [architecture] · `harness/drift.odin`
9. `advance gate on` lacks the `era >= 1` parse-time cross-check `growth on` has — an era-0 gate demo would bless a silently-inert gate golden [codebase] · `harness/demo.odin:590` vs `:616`
10. Duplicate era rows pass the density check (silent last-wins overwrite) [blind] · `core/catalog.odin:1286-1295`
11. Window-elapsed precondition duplicated with two tick sources (`tick` param vs `state.tick` — equal today) [blind] · `core/era.odin`
12. `era_gate_update` lacks growth's once-per-tick re-step guard (no reachable re-step path found — consistency only) [blind] · `core/era.odin`
13. Boundary values (window 20000, bar 1, bar 100) lack clean-load rows [tests] · `core/catalog_test.odin:510-514`

### Carried from round 1 (still present, not re-counted)

Warnings: **W1** (block-event count pins), **W2** (scripted-while-blocked untested), **W4** (`fire_tick` dead), **W8** ([ODN-16, §6.6] citation still absent from the PR body). Notes: N1 (window/ring never re-anchored on fire — the documented 6.3 seam; re-flagged by two lenses this round), N2, N3 (6.3 seams), N4, N5, N6.

### Reviewer agreement

R2-W1/edge+acceptance · R2-W3/edge+security · note 6/blind+architecture+codebase — all three survived verification.

### Verdict

**NEEDS CHANGES** — 1 blocker (a vacuous pin on a headline contract; the implementation itself traces correct — the fix is three assertion lines, not a rework). The r1 blockers are genuinely fixed and empirically biting; this round's remaining new items are warning-tier hygiene.

_Address findings and push — I re-review automatically on the new sha._
