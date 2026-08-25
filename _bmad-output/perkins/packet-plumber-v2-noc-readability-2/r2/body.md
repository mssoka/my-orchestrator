## 🤖 Perkins automated review — round 2

**Job:** packet-plumber-v2-noc-readability-2 · **Reviewed sha:** 729ef0d · **Reviewers:** 7/7 completed
**Verification:** 17/21 findings confirmed against the code — 4 discarded as false-positive

### Fix-audit on the r1 fold (all r1 findings re-read against 729ef0d)

**Every r1 finding is fixed or addressed.** B1 (the blocker) is properly closed: `view_set_rail(&app.view, false)` on the settings-dismissal path (main.odin:1152) + the resize re-apply (main.odin:633), pinned by the dismissal leg asserting play_w 756→1280 on a real 1280×720 fixture. W1 is resolved by the documented alternative (bottom band stays at win_w over the plate's empty bottom; content ends at 668 < tray top 684, test-pinned). W2's preview card re-anchors into the playfield (746 < rail edge 756). W3's `NOC_PANEL_W` now genuinely derives from `NOC_PANEL_W_SCALE` (integer-percent 140, test-pinned). W4/N3's harness refit landed (`view_set_rail` + `view_refit`, app draw order) — I re-ran it locally: the overlay .t1 sidecar is hash-byte-identical to the blessed golden (1200/1200 ticks). W5/W6/W7/N9's pins are in (W7's pin duplicates the 84/196 literals instead of referencing production locals — soft, carried as a note). N1/N4/N8 carry forward as notes.

The hard bars were **re-proven locally on the reviewed bytes**, not carried: `odin test` 73/73 render + 40/40 app + 236/236 core; **golden harness 48/48 green**; overlay-pixels smoke 94,161 changed px inside the rail rect (gate bites). k3 vision was inline this round — I inspected all four shipped captures plus a fresh capture generated from the reviewed sha. The docking, full-height rail, top-band-over-plate, and overall legibility claims all hold up. KYLE's PASS rides as the job's vision-gate evidence, un-re-litigated.

### Blockers (1)

- **B1′ — The recomputed per-class column math ships a colliding `loss`/`SLA` header and a window-clipped `/3s`** (acceptance + my inline vision pass; `noc_overlay.odin:686-698`). Headers are drawn **left-aligned at the data columns' right-edge anchors**: `loss` occupies [1134, 1170] at 15px but `SLA` starts at `sla_x = loss_r + 16` = 1150 → a 20px glyph overlap rendering "loS&A"; `/3s` starts at `rate_r = px + NOC_PANEL_W − 6` = 1262 and runs to ~1289 — **past the 1280 window edge**, the final glyph clips. Pixel-verified in *both* shipped after-captures and in my fresh capture from the reviewed bytes. The data rows are clean (right-aligned, 84px pitch seats 7-digit counters); only the header row breaks. On a third-strike legibility job, the PR's own evidence images show a merged header. Fix: right-align the del/drop/loss//3s headers at their column anchors (`noc_col`) and give SLA real clearance; re-capture + re-grade.

### Warnings (6)

- **W1′ — Demolish popover clamps to `win_w`, draws before the rail — can hide under the plate with its demolish button still clickable** (architecture + edge; popover.odin:40-58, main.odin:699-719, exec.odin:517). East-edge entity + D on: the popover crosses the 756 rail edge (the flip only triggers past 1280), the plate covers it, and the *invisible* demolish button still takes clicks — an unseen destructive action. Clamp `popover_rect` to `play_w` when the rail is on (the `settings_panel_rect` pattern) or draw it after the rail.
- **W2′ — The W2 fix's new branch (`view_rail_on` preview re-anchor) has no test** (tests; forecast.odin:110-121). A deleted `if view_rail_on` stays green.
- **W3′ — Resize re-apply (transition 2 of 3) + `view_compute`'s `play_w` reset unpinned** (tests; main.odin:633, view.odin:435). B1's whole class was a missed rail-state transition; one transition still has no pin.
- **W4′ — Rail-on app camera threading untested** (tests; main.odin:1732/1865/1893/1804). The render-layer fit is pinned; the four app call-sites that moved from `win_w` to `play_w` aren't, at rail-on geometry.
- **W5′ — The rail plate owns the wheel but not clicks** (edge; mouse.odin:356). Press/release over the plate starts a pan and clears the selection via the empty-ground path. (Trimmed sub-claim: a hidden-node `Begin_Draw` is *not* reachable — the camera clamp keeps the world's east edge at exactly `play_w` at every zoom; verified.) Swallow presses inside `noc_panel_rect` when the overlay is on.
- **W6′ — Advisory test gate: CONCERNS** (tests). P0 pinned (48/48 + suites + wiring legs); the fix's own new branches are the remaining gaps. W2′+W3′+W4′ lift it to PASS.

### Notes (7)

- **N1′** Duplicated DOCK-RIGHT comment sentence, three lines apart, in `overlay_check` (blind; harness/overlay.odin:72-79).
- **N2′** New tests re-implement production formulas/literals — the visible-rows formula and the 84/196 column-math copies drift silently if production changes (blind; r1 W7/N9 residual softness).
- **N3′** The D-toggle re-fit snaps the world ~21% in one frame — `cam_zoom` eases, `fit` steps (blind). Polish; the panel itself appears instantly.
- **N4′** Camera helper params still named `win_w` / documented "the window dims" while every call site passes `play_w` (architecture; camera.odin:71-72,188,226).
- **N5′** `noc_panel_rect`'s comment claims "hit-test + the draw share it (single source)" but `draw_noc_panel` re-derives the plate as `px − NOC_PLATE_PAD` (architecture; numerically equal, win_w−524 — carried from r1 N5).
- **N6′** **The live GitHub PR body was never updated for the fix commit** — it's still the r1 text: "24 visible rows" vs the pinned 23, "plate at x=757" vs 756, "play_w == win_w in the harness", and none of the W1/W2/W3 resolutions the shipped `_pr_body_noc_readability_2.md` documents (acceptance + codebase; diffed live vs repo copy). One `gh pr edit` fixes it.
- **N7′** `draw_noc_panel`'s doc comment still says "Open Sans digits" — the top-of-file occurrence was fixed to Plex Mono, this one missed (codebase; noc_overlay.odin:617).

Still present since round 1 (carried, not double-counted): r1-N1 (draw order never asserted), r1-N4 (View binds NOC_RAIL_W), r1-N8 (pre-first-tick transient — harmless).

### Reviewer agreement

- **W1′** popover occlusion + clickable-while-invisible button — architecture × edge
- **N6′** stale live PR body — acceptance × codebase
- **B1′** header collision — acceptance × Perkins' inline k3 vision pass (independent; pixel-verified)

**Verdict:** NEEDS CHANGES

The fix commit does exactly what it claimed — the r1 fold is clean, and the zero-drift/stream-neutrality bars re-proven locally. But the column-math recompute left the ledger's header row colliding (`loS&A`) and clipped (`/3s`) in the very captures offered as legibility evidence — on a third-strike readability job, that ships the failure class under review. One-line-class fix (right-align the headers at the column anchors), then re-capture.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
