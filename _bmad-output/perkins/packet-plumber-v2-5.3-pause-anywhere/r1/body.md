## 🤖 Perkins automated review — round 1 of 3
**Job:** packet-plumber-v2-5.3-pause-anywhere · **Reviewed sha:** 9ae8612 · **Reviewers:** 7/7 completed
**Verification:** 19/19 findings confirmed against the code at the reviewed sha — 0 discarded as false-positive, 0 kept as [unverified] (1 downgraded on reachability: the Boot-toggle ternary is latent-only — start_run clears Boot before input can fire)

**Local suite (CI is account-billing-blocked — ground truth):** `odin test core` **158/158** · harness `run` **25/25 PASS** (24 pre-existing goldens byte-identical — zero shift; the new `pause` demo green through T1 + T2 + replay gate) · `drift-check` **174/174 mutations rejected** · `preview-check` 7/7 · `tools/lint.sh` all gates · `odin build app` clean. **Perkins data audit of the new golden:** `pause.t1` window 1211–1400 is one repeated hash (`0xd3600eef9503b6d9`), the hash moves exactly at 1401 (first post-resume step), and `pause.log.bin` decodes to the mid-pause draw at `apply_tick=1211` (paused tick 1210 + 1) with no-pause draws at the back-compat floor+1 (=3). The determinism spine — freeze, exact-tick resume, mid-pause edit landing, byte-identical replay — **holds and is pinned**.

### Blockers (0)

None. The load-bearing spine is intact: no path drifts the paused window, resume lands on the exact tick, mid-pause edits log at paused tick + 1 and land on the first resumed step, and the old goldens are untouched.

### Warnings (7)

1. **Pause-schedule parsing checks file-order alternation but not chronological `at_ms` order** *(5 lenses: blind, edge, security, architecture, codebase — the highest-confidence item in this report)* — `harness/demo.odin:389-410` + `harness/run.odin:127-145`. `at 70000ms pause` then `at 60500ms resume` passes arity+alternation; `paused_at`'s last-wins loop never pauses (the pause silently vanishes), and `ticks_stepped_by`'s `n -= hi - pe + 1` underflows u64 when the resume effect precedes the pause effect — commands fired at/after the pause ms get garbage `apply_tick`s silently written into a blessed log. The PR's own hardening standard is "fail loud, like an unknown tier"; chronological order is the one authoring error class it misses. *Fix: reject a pause/resume whose `at_ms` ≤ the previous pause event's `at_ms` (track `last_pause_ms`); optionally saturate the subtraction.*
2. **`harness save` blesses through a stability violation** *(acceptance)* — `harness/run.odin:333-339` vs `420-425`. The STABLE-violation check appends to `fails` in both modes, but the save branch returns true without inspecting (or printing) it — a drifting paused window gets blessed, contradicting the code's own "fail loud, never bless a broken pause" comment. Run-mode catches drift; the deliberate re-bless path doesn't. *Fix: fail the save when `len(fails) > 0`, mirroring the `replay_error` check that already gates save.*
3. **`core/pause_test` clause (a) pins boundary hash-equality the harness contract disavows** *(blind + tests)* — `core/pause_test.odin:80-84`. `state_hash` folds the tick's events, so wall-11 == wall-10 holds only because this fixture emits zero events at tick 10 — the golden's own boundary differs (`df84…` → `d360…`, crisis events at 1210). A legit fixture change would falsely fail the test, and the pin misdocuments the contract as boundary-equality rather than window-internal stability. *Fix: baseline the window on its own first hash (wall-11), not the last stepped tick's.*
4. **The new parse-rejection paths have zero automated coverage** *(tests)* — `harness/demo.odin:380-410`. Bad arity / double-pause / resume-without-pause are claimed fail-loud but never proven to fire; by the repo's own drift.odin standard ("must be PROVEN, not just asserted locally"). *Fix: a small parse-rejection test set — include the W1 ordering case.*
5. **`apply_tick_at`'s trailing-pause and multi-window branches never exercised** *(tests)* — `harness/run.odin:127-146`. Both the golden and the core test use one non-trailing window; the `re = max(u64)` trailing branch and multi-window accumulation (where W1's underflow lives) run untested. *Fix: a trailing-pause + two-window case in `core/pause_test` or a second demo.*
6. **The paused-STABLE checks are never proven to bite** *(tests)* — `harness/run.odin:332-339, 666-678`. No drift class touches `apply_tick` bytes or the pause schedule; if the stability condition were inverted or dropped, every existing gate would still pass. *Fix: a drift mutation that shifts the mid-pause edit into the window and asserts the violation fires in both paths.*
7. **Advisory test gate: CONCERNS** — P0 (the determinism spine) is fully pinned (golden + replay gate + core test + drift-check); P1 (the new hardening branches, W4–W6) sits at ~80–85%. Closing W4–W6 lifts the gate to PASS.

### Notes (5)

1. **Pause toggle's else-branch maps any non-Run mode to Run** *(blind, downgraded — unreachable today)* — `app/main.odin:344-345`. Only Run/Paused are reachable at that line (start_run clears Boot; Game_Over returns early). Optional explicitness: gate on `(Run || Paused)`.
2. **Veil uses live window size, PAUSED label uses WIN_W/WIN_H constants** *(blind)* — `app/main.odin:246-249`. Off-center label after a resize (first centered element in the app; corner HUD text shares the fixed-coord convention).
3. **pause.dem comment + PR body claim a banner "countdown" that doesn't render** *(acceptance)* — `demos/pause.dem:29-32`. The banner shows title + static redesign hint only; reword to "same crisis still active, banner pixel-identical; window advanced only post-resume".
4. **Virtual-clock loop triplicated** *(blind + architecture)* — `run_demo`, `replay_hashes`, and the core test's `record_paused_run` carry three hand-kept copies of the determinism-critical loop (the replay copy's allocator discipline already differs, deliberately). A shared driver or a documented independence rationale would keep them from drifting.
5. **`pause_effect_tick`'s i64 multiply wraps for absurd `at_ms`** *(security)* — `harness/run.odin:153-155`. Identical arithmetic to the pre-5.3 command lowering — convention extended, not a new hazard; bound `at_ms` at parse if ever hardened.

### Reviewer agreement
- **Out-of-order pause-schedule validation gap** — 5 independent lenses (blind, edge, security, architecture, codebase) on one code-anchored finding: the highest-confidence item in this report.
- Boundary-equality pin vacuous/brittle — 2 lenses (blind, tests).
- Virtual-clock duplication — 2 lenses (blind, architecture).

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
