## 🤖 Perkins automated review — round 1 of 3

**Job:** packet-plumber-v2-1.4-win-lose-stub · **Reviewed sha:** `0b125e2` · **Reviewers:** 7/7 completed
**Verification:** 8/8 findings confirmed against the code — 0 discarded as false-positive
**Note on model:** kimi quota is down this cycle, so the lenses ran on the sanctioned fallback `zai-coding-cn/glm-5.2`. All 7 lenses produced valid output (security + tests recovered via a re-prompted wave after an initial rate-limit burst). No chunking (diff 1540 < 3000).

### Load-bearing spine — verified sound ✅
- **Terminal-event barrier (E17):** `step` returns at the top *before* `state.tick` mutates → exactly one terminal event per run; post-terminal ticks are frozen no-ops. Pinned by `test_terminal_barrier_one_event_per_run`.
- **Determinism over the full loop incl. the terminal frame:** `score/goal/tick_cap/terminal/outcome` all ride the T1 hash + serialize (`serialize.odin:84-88`). The WIN loop has a byte-identical-replay unit test; the LOSE loop is golden-covered (`lose.t1`, drift-rejected).
- **`package core` is engine-free (ODN-1):** `win_lose/step/flow/types/serialize` have **zero imports**.
- **Win/lose independent gating + win-beats-lose:** `win_lose.odin:43-58`; tested incl. `test_cap_only_lose_with_no_goal` (the goal==0 over-disable regression you self-fixed).
- **Clean restart:** `run_destroy` + `run_init` (zeroes) + fresh crypto seed + reset (`start_run`/`restart_run`/`fresh_seed`).
- **Build/test/harness at `0b125e2`:** `odin test core` = **27/27**; `odin build app` (CI mode) OK; harness drift-check = **29/29 rejected**; harness run = **5/5 green** (boot/flow/**win**/draw/**lose**).

### Blockers (0)
None.

### Warnings (2)
- **W1 — Missing "retry-restores-clean-state test" (spec-named) + app Mode FSM untested** `[acceptance, tests]` (reviewer agreement — two independent lenses). Story 1.4 lists *retry-restores-clean-state test* under its Golden/edge-case contracts; it's absent (no `app/*_test.odin`). The restart **behavior is verified correct** and core-level fresh-context is tested — this is a missing *test artifact*, not a defect. *Fix:* lift the reset into a raylib-free helper; add a headless restart test (assert score=0 / events cleared / terminal=false / fresh seed differs).
- **W2 — Advisory test gate: CONCERNS** `[tests]`. P0 core contracts 100% covered; overall ~85%. CONCERNS because the named clean-restart contract has no automated coverage and the LOSE-loop replay is golden-only. Harness integration (5/5 demos, 29/29 drift) mitigates but isn't unit coverage. Raising to PASS needs: the restart test + a LOSE-loop replay test + a self-delivery test.

### Notes (6)
- **N1 — Redundant terminal guard in `win_lose_eval`** `[blind]` (`core/win_lose.odin:36`). `step`'s barrier already enforces E17, so the inner check is unreachable — but it's documented as intentional defense-in-depth. Optional: reword the comment or drop it.
- **N2 — Demo win-goal ≥ 2³² truncates via `u32(v)`** `[edge]` (`harness/demo.odin:142`). Harness demo-fixture parse path only (not core / not untrusted input); impact nil. Optional range-check.
- **N3 — Sub-tick `cap_ms` floors to `tick_cap 0` (silently disables lose)** `[edge]` (`harness/run.odin:176`). Harness/demo path only — the playable app uses `LOSE_TICK_CAP` ticks directly (`app/main.odin:31,143`), unaffected. Optional floor-to-1.
- **N4 — App Mode FSM transitions (Run↔Game_Over) untested** `[tests]` (`app/main.odin:97-111,172-178`). Related to W1.
- **N5 — LOSE-loop byte-identical replay is golden-only** `[tests]` (`core/win_lose_test.odin:199`). Determinism *is* verified (golden + drift), but no core unit test mirrors the WIN one. Optional `test_lose_loop_replay_byte_identical`.
- **N6 — Degenerate "spawned at own dst" score increment untested** `[tests]` (`core/flow.odin:148-151`). The second `state.score += 1` is a 1.4 behavior with no test. Optional self-dst spawn test.

### Out of scope (carry-forward, not blocking)
- `odin build app -vet` fails on an unused `import "core:strings"` in `app/main.odin` — but it's **pre-existing in base `v2`** (0 usages there too), not introduced by this PR, and CI uses `odin build app` (no `-vet`). Flagged for hygiene only.

### Reviewer agreement
- **W1** (missing restart test) was independently surfaced by the **acceptance** and **tests** lenses — the highest-confidence finding.

**Verdict: READY TO MERGE.** The terminal-event barrier, loop determinism, ODN-1 core purity, win/lose gating, and clean restart are all correct and verified; build/tests/harness are green. The findings are test-coverage completeness + harness-edge notes, not correctness defects. W1/W2/N5 are worth folding in (a restart test + a LOSE-replay test would close the named contract and lift the gate to PASS), but none blocks.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
