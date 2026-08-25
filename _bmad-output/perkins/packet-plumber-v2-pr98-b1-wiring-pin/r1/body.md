## 🤖 Perkins automated review — round 1
**Job:** packet-plumber-v2-pr98-b1-wiring-pin · **Reviewed sha:** 1bec4e3 · **Reviewers:** 7/7 completed
**Verification:** 8/10 findings confirmed against the code — 2 discarded as false-positive

**The core hard gate PASSES, verified by live mutation legs at the sha:**
- Deleting the `:972` routing call → exactly `start_run_wiring_homes_on_the_source_cluster` fails (both asserts: DEFAULT_ZOOM + home anchor). 1 failure, isolated.
- Deleting `:1135` → exactly `effect_cancel_wiring_homes_on_the_source_cluster` fails (all 3 asserts incl. pullback-clear).
- Deleting `:1800` → exactly `deselect_wiring_homes_on_the_source_cluster` fails.
- All three removed → exactly 3 failures. Legacy `camera_set_default_homes_on_the_source_cluster` green throughout.
- Completeness: exactly three `camera_set_default` routing calls exist (`:972/:1135/:1800`); boot (`main` :454) and run-reset (`restart_run` :991) route through `start_run`, ESC/right-click/pad-B through `on_cancel = effect_cancel` (:493), deselect through `camera_set_selection`'s else-branch. No fourth mutation-invisible site.
- Suites: app 46 (43+3), core 261, app/render 81 — all green, counts match the PR body. Test-only confirmed: the diff touches only `app/pullback_test.odin`. Em-dash convention held in test names/strings (comments exempt).

### Blockers (0)

None. All three pins drive real routing entry points and are mutation-visible; the B1 fix as prescribed (#97: "tests driving the real entry points, asserting `cam_zoom_to == DEFAULT_ZOOM` / home anchor") is delivered in full.

### Warnings (2)

**W1 — False comment rationale: start_run's pullback-clear is NOT independent of the camera routing, and that half is unpinned** *(edge+acceptance+codebase+tests — 4-lens agreement; Perkins mutation-verified)*. `pullback_test.odin:513-516` claims start_run clears pullback "via its destroy-then-reinit run-init independent of the camera routing". That is false: `run_init`/`run_destroy` take `^Run_State` (`core/types.odin:561/:582`), `pullback` is an App field (`main.odin:263`) — the only clear on the path is `camera_set_default`'s `app.pullback = false` (`main.odin:1763`) via the `:972` routing call. Proven by mutation: an armed pullback survives `start_run` with `:972` removed (scratch-leg verified both directions). The sibling tests arm and pin their clears; start_run's clear is skipped on a false premise — a maintainer re-routing the camera call would silently lose restart's clear, the exact mutation-blind class this PR pins. Fix: arm `app.pullback = true` before `start_run(&app, 42)`, assert `false` after (verified: passes pristine, red under mutation), and rewrite the NOTE.

**W2 — Advisory test gate: CONCERNS** *(tests lens)*. P0 100% — all three wiring pins mutation-visible (re-proven above). P1 ≈83% — the wiring-level contract is 5/6 pins: start_run's pullback-clear half is unpinned (W1). Overall ≥80% → CONCERNS. W1's one assert lifts it to 6/6 → PASS. (#97's W1/W4 remain unaddressed by design — out of this PR's scope, not counted here.)

### Notes (3)

- **N1** — The frame-loop selection-diff guard upstream of the deselect pin is unpinned (`main.odin:697-699`): production reaches `:1800` only via that guard; the test calls `camera_set_selection` directly, so deleting the guard breaks deselect-homing with the suite green. Beyond B1's named scope (the `:1800` call site IS pinned); future hardening.
- **N2** — `seed_fixture`'s `content_host` lookup silently misses on the fixture's 2-type catalog (`main.odin:2438` discards ok; miss returns index 0 → residential-typed host). Fidelity only: node position, not type, feeds the centroid, and the asserts are self-consistent.
- **N3** — The 8-line camera-away arming block now exists in three verbatim copies (fixture + the two new tests). Optional `arm_camera_away(app)` helper beside the fixture.

### Reviewer agreement
W1 was independently found by 4 of 7 lenses (edge, acceptance, codebase, tests) and empirically confirmed by a fresh mutation leg. 2 blind-lens findings were rejected as false-positives after verification (one refuted by the mutation legs, one a non-defect provenance question).

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha.
The loop runs until an APPROVED verdict._
