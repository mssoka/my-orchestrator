--- SPEC: PR #98 body (the user-authored PR under review — this IS the spec) ---
## What
Makes the camera RESTING-HOME wiring mutation-visible. Three new tests drive the REAL routing paths — start_run, effect_cancel, and the deselect else-branch of camera_set_selection — NOT a bare camera_set_default(&app) call. Removing any of the three camera_set_default(app) routing calls (main.odin:972/:1135/:1800) now turns the suite RED.

## Why
PR #97 established camera_set_default as the resting home, but the existing resting-home test calls camera_set_default directly (self-referential), so the wiring was mutation-invisible. Confirmed by deep-dive before this change.

## Verify
- odin test app: 46 green (43 baseline +3).
- odin test core: 261 green (unchanged). odin test app/render: 81 green (unchanged).
- Mutation-visibility proven: removing the routing call at start_run/:972, effect_cancel/:1135, and deselect/:1800 each fails the corresponding new test; all three removed = 3 failures. Legacy camera_set_default_homes_on_the_source_cluster stays green throughout.

Test-only change; camera logic, goldens, tools/ untouched. INTENDED for review; human merges.

--- SPEC: the PR #97 r1 B1 finding this PR fixes (review 5012533699) ---
B1 — Resting-home wiring unpinned (mutation-invisible call sites). app/main.odin:972,1135,1800. The headline behavior (resting home on boot/run-reset/deselect/ESC) is pinned only at the callee — pullback_test.odin:393 calls camera_set_default directly. Zero tests drive effect_cancel, start_run, or the selection-diff deselect (grep: comments only). Reverting any call site to camera_set_fit passes the entire suite (385 tests + 49 demos — the harness never runs app camera wiring). Fix: app-package tests driving the real entry points, asserting cam_zoom_to == DEFAULT_ZOOM / home anchor.

--- SCOPE NOTE (round scoping — do not violate) ---
This PR is a fix-forward for B1 ONLY. PR #97's B2/W1-W5 findings were that round's scope and are deliberately NOT addressed here; do not report them as blockers of THIS PR. The PR is TEST-ONLY: the diff must touch ONLY test files.
