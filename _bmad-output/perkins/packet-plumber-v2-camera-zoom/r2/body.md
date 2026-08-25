## 🤖 Perkins automated review — round 2
**Job:** packet-plumber-v2-camera-zoom · **Reviewed sha:** bd3b142 · **Reviewers:** 7/7 completed
**Verification:** 33/33 findings confirmed against the code — 0 discarded as false-positive

**Mechanical round evidence (run on the reviewed sha, detached worktree):** local CI 11/11 gates PASS (native) — including the golden harness **48/48 demos green** (T1 hashes + T2 pixels + replay byte-identical, no re-bless — the zero-drift hard bar holds) and input-parity 27/27. The hard bars (a) sim-untouched (ODN-1: `core/` unchanged, SEED family derived view-side), (b) zero golden drift, (c) single wheel consumer (`effect_zoom`), (d) HUD screen-space all verified in code. The blockers below are contract/coverage issues, not hard-bar breaks.

### Blockers (3)

**B1 — Pullback fit-floor never re-pins the camera center** · `app/main.odin pullback_feed` + `app/render/camera.odin camera_pullback_target` · [acceptance, edge]
Real map is 40×30 tiles = 1040×780 px, height-bound fit (`fit = 720/780`): at zoom 1.0 the visible height is *exactly* the world height, so only `cy = 390` shows the whole map. A camera panned to the bottom clamp at high zoom (e.g. `cy = 585`, valid at 2×) that floor-clamps to 1.0 keeps its off-center center — `camera_update` never clamps and `pullback_feed` assigns `cx_to/cy_to` without calling `camera_clamp_center` — so after the ~2 s ease, world y ∈ [0, 195) is still cut off and **the new district can remain off-screen at the converged "fit"**. Breaks the ruled contract ("ease out … or to the fit-view floor if beyond") and the PR body's own claim ("a floor-clamped target always includes the district" — only true if the center pins). The existing floor test passes only because its fixture camera happens to sit where the district stays visible.
**Fix:** run the returned `(cx_to, cy_to)` through `rnd.camera_clamp_center(..., z_to, ...)` before assigning the targets (it pins the center to the world center at the fit); add a floor test with an off-center camera asserting district inclusion at convergence.

**B2 — NOC wheel-ownership + modal-block policy has zero automated coverage** · `app/main.odin effect_zoom/effect_pan`, `noc_panel_hit` · [tests]
Acceptance item "NOC wheel-ownership respected" is *implemented* correctly (verified in code: one consumer, panel-hit → scroll, modal blocks, else zoom — and the old render-block read is gone), but no test pins any of it: `noc_panel_hit`, the scroll-vs-zoom branch, the modal block, and release-build always-zooms have no unit pin; the only evidence is the manual one-shot `PP_CAM_E2E` captures.
**Fix:** fixture-App unit pins (the `pullback_test` precedent): wheel over the panel scrolls-not-zooms (PP_DEBUG), the modal blocks zoom+pan, elsewhere zooms; pin `noc_panel_hit` inside/boundary/outside.

**B3 — Advisory test gate: FAIL (P1 ≈ 0%)** · [tests]
P0 is 100% — camera math, intent wiring, conflict gates, pullback feed/ease/toggle, settings v2/v1 are all pinned and green. But every composition-level behavior is untested: the five pullback-yield clears (W8), the NOC ownership branches (B2), a positive touch-pan pin (W9), and the latch lifecycle transitions (W10) — deleting any single one keeps all 11 gates green. Gate arithmetic: P0 100%, P1 < 80% → FAIL.

### Warnings (10)

- **W1 — Pan latch strands across the settings modal; stale-anchor lurch on close** · [blind, edge] — S / pad-Y mid-pan opens the modal without clearing `panning`; the panel-suppress branch drops the release (and the poll guard then synthesizes one every frame, also swallowed); on close the accumulated release fires `Pan{cursor − stale press anchor}` — a full-displacement camera jump. Clear the latch when the panel opens (or in the suppressed branch).
- **W2 — No cross-frame wheel accumulator; slow trackpad scrolling never zooms** · [acceptance, blind, codebase, edge — 4-lens agreement] — raylib delivers fractional per-frame deltas on smooth trackpads; `i32(delta)` truncates |δ|<1 to zero every frame. Zoom is now a primary input on laptops; accumulate the residue in `Input` and fire whole notches.
- **W3 — Pipe selection and `camera_focus_pair` never clear `app.pullback`** · [codebase, edge] — the node leg and `camera_set_fit` clear it; the pipe leg (QoS click-select) and crisis-banner focus set 2.6× targets without clearing — the focus eases at the pullback rate (~1.5-2 s instead of ~0.5 s) and a later SEED can steal the camera from the user's selection. Contradicts the function's own comment ("Any selection change ends an in-flight pullback").
- **W4 — Router placement skews the spawn-id walk-back; the SEED pullback is silently skipped** · [acceptance] — `apply_place` consumes a node id *without* emitting `NODE_SPAWNED`; if a placement shares the frame with a growth spawn, the count-based walk-back (`next_node_id − remaining`) points at the router (not a Terminal → skipped) and the real seed is never classified. Track the previous frame's `next_node_id` and classify the whole window.
- **W5 — `effect_pan` scales by the eased zoom *target*, not the live scale its comment promises** · [blind] — mid-wheel-ease drags mis-track the cursor by the target/live ratio; `effect_zoom` anchors against the live transform. Pick one (live matches the comment) and align code+comment.
- **W6 — v2 settings fallback ≠ `DEFAULT_A11Y` under mixed corruption** · [blind] — `s.auto_pullback` is applied before the shared palette/motion/scale range checks; a pullback=0 file with any other corrupt byte returns defaults-*except*-pullback. The existing out-of-range tests all use byte 1, masking it. Apply payload only after all checks pass; add a pullback=0 mixed-corruption test.
- **W7 — `camera_spawn_is_seed` "exact mirror" diverges on same-window siblings** · [blind] — the core classifies at spawn time; the view classifies after — a younger same-window attach within 10 tiles flips a genuine seed to attach (pullback missed). Narrow (needs a multi-tick catch-up window) but the "exact mirror" comment overclaims. Exclude same-window ids from the sibling set.
- **W8 — The five pullback-yield clears are untested** · [tests] — "any user camera input yields the pullback instantly" is 5 distinct clear sites, none exercised. Arm + clear through each path in `pullback_test`.
- **W9 — Two-finger touch pan has no positive pin** · [tests] — deleting `touch.odin:94-95`'s `Pan` emission keeps every gate green. One dispatch test with `Two_Finger_Pan` asserting the exact `on_pan` deltas.
- **W10 — Pan-latch lifecycle edges untested** · [tests] — the missed-release guard, `begin_draw` clear, and `start_run` reset have zero coverage (W1 proves the strand class is real). Factor the poll-guard condition into a testable predicate and pin the three transitions.

### Notes (11)

- **N1** — Fit derivation triplicated despite `camera_fit`'s "ONE source" comment (`camera_fit`, `camera_update` inline, `view_compute`) · [blind, codebase, architecture] — have `camera_update` call `camera_fit(v)`.
- **N2** — Test-count claims misaligned: PR says 4 camera-math tests (actual 6), 14 new (actual 16); briefing says 18 pins · [blind, tests] — fix the PR body / reconcile "pins" vs "tests".
- **N3** — The "panned release never click-selects" assertion can't fail (nothing selected beforehand) · [blind] — select first, then assert it stays unselected.
- **N4** — Clamp-test comment ("x is free", "960px viewport") contradicts its own correct both-axes-pin assertion · [blind] — rewrite the comment math.
- **N5** — `pullback_feed` re-implements `spawn_fx_feed`'s id walk-back · [codebase] — extract a shared helper.
- **N6** — New tests skip the `catalogs_destroy` cleanup their own fixture precedent uses · [codebase] — add the defers (ODN-18).
- **N7** — `harness/parity.odin:521` still documents Pan as "a no-op today" · [codebase] — stale comment, reword.
- **N8** — SEED during a held stationary drag: zero-delta `Pan` clears the flag but the zoom-out target survives → a fast zoom-out mid-drag, neither yield nor pullback · [edge] — define the intended behavior.
- **N9** — `PP_CAM_E2E` is manual-only evidence (no gate/helper wiring, like the pre-existing NOC_E2E pattern) · [tests] — a `run-dev.sh` subcommand + optional capture regen/diff.
- **N10** — Settings `.tmp` write lacks `O_EXCL` (symlink-follow; negligible single-user desktop) · [security].
- **N11** — `App.auto_pullback` mirrors `App.a11y.auto_pullback`, synced by hand at two sites · [architecture] — keep one source of truth.

### Reviewer agreement
6 multi-lens findings (highest confidence): **B1** fit-floor center [acceptance+edge] · **W1** modal pan-strand [blind+edge] · **W2** wheel accumulator [acceptance+blind+codebase+edge] · **W3** pipe/focus pullback clear [codebase+edge] · **N1** fit triplication [blind+codebase+architecture] · **N2** test counts [blind+tests].

**Verdict:** NEEDS CHANGES

The view-layer architecture, the input chain, and the golden immunity are solid — 11/11 gates, 48/48 byte-identical demos, and the conflict gates genuinely bite. But B1 breaks the pullback ruling's core guarantee in a reachable path (pan to the edge + a far district seed), and the composition layer (ownership policy, yield clears, touch pan, latch edges) ships with no automated pin — B2/B3. The fixes are small and local; with B1-B3 addressed this should converge quickly.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
