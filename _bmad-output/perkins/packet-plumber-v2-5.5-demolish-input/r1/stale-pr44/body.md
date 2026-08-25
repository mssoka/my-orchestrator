## 🤖 Perkins automated review — round 1 of 3

**Job:** packet-plumber-v2-5.5-demolish-input · **Reviewed sha:** 23e1704 · **Reviewers:** 7/7 completed
**Verification:** 8/8 surviving findings re-verified against the code at the reviewed sha — 2 lens claims discarded as false-positive; 4 app-layer coverage blockers consolidated into one warning per repo precedent (3.2 r1 warning / 3.5 r1 note — both shipped READY TO MERGE).
**Local suite (CI is account-billing-blocked — ground truth):** `odin test core` 153/153 · `tools/lint.sh` all gates green · `odin build app` clean · harness `run` **22/22 PASS** (20 pre-existing goldens byte-identical — zero shift; both new demos green through T1 + T2 pixels + replay gate). New T2s pixel-verified: pooled link slims in the bundle band (1335/1324 → 1049/1038 orange/green px); junction batch drops pipe/node pixels ~63% with the fixture leg intact. New `.t1` catalog_hash `1106c1cc8652a91f` matches all 20 existing. LOG_VERSION stays 3. Core + catalogs untouched.

### Blockers (0)

None. The LOAD-BEARING guard holds: click-select + popover + X/DEL dispatch the real `Cmd_Demolish_Pipe` / `Cmd_Demolish_Node` through the existing validate→apply→action-log fast-path (byte-identical to draw/place), E2 terminal-reject and E27 junction-batch are reachable through the UI, and X/DEL are inert while placing / mid-drag / in Game_Over.

### Warnings (3)

1. **ESC mid-click re-selects — the drag-release click-select never checks `press_swallowed`** *(5 lenses: blind, security, architecture, codebase, edge)* — `app/main.odin:332-337` vs `488-494` vs the gated `524`. ESC deselect sets the latch ("an in-flight click's release must not re-select after ESC") but leaves `drag.active` set; press-on-node → ESC → release-without-move takes the drag branch and re-selects the node, contradicting the code's own comment and the PR interaction map. *Fix: gate the drag-branch click-select on `!app.press_swallowed`, or clear `app.drag.active` in the non-placing ESC branch.*

2. **Placement commit lacks the `release_ui_hit` guard — a 6px chip-boundary release places a router under the tray** *(edge)* — `app/main.odin:510-516`. Click-select releases gate on `release_ui_hit` (the 6px boundary gap), the placement commit checks only `press_swallowed`. With the camera-fit (off_y=0) the tray band (y 684..710) overlays real map rows, so press 1–5px outside a chip edge, release onto the chip → a router is placed on the tile under the tray where the player aimed at the chip (cancel intent). *Fix: add a tray-chip hit check to the placement commit condition.*

3. **App-layer input glue has zero automated coverage** *(tests — regraded from the lens's blocker per repo precedent)* — no test references `click_select`/`popover_click`/`release_ui_hit`/`press_swallowed`/`demolish_pipe`; the harness links only `../core` + `../app/render`, so the demos pin the command stream the surface submits (same kinds, validate→apply→log, replay byte-identity) but not the selection/hit-test glue. 3.2 r1 rated the identical class a warning, 3.5 r1 a note — both merged. *Fix: extract the input logic and add headless tests (selection priority, latch lifecycle, dispatch, toasts) when convenient.*

### Notes (5)

1. **PR interaction map vs chord code** *(acceptance, blind, codebase)* — `_pr_body.md:74-75` says the right+left chord "swallow[s] that gesture's release so it cannot re-select"; `app/main.odin:342-346` deliberately re-anchors the press (`press_swallowed = false`) so its release click-selects. Docs-only — fix the sentence.
2. **Node-demolish reject toast has no render path** *(codebase)* — the toast draws only inside the `sel_pipe >= 0` block (`app/main.odin:1022`, `1062-1063`); a `.Missing_Node`/`.Terminal_Demolish` rejection keeps `sel_node >= 0` so the belt-and-braces toast never renders. Unreachable through the UI today, but the spec's error-handling row has no visible surface.
3. **`popover_rect` small-window clamps can go negative** *(blind, codebase)* — `app/render/popover.odin:48-56`: with `win_w < 226` or `win_h < h+TRAY_CLEAR` the final `min()` yields negative x/y, contradicting the "never overflow a small window" comment.
4. **Pipe popover anchor midpoint computed twice** *(architecture)* — `app/main.odin:671` (`pipe_anchor`) vs inline at `app/render/popover.odin:91`, against the file's "layout is owned HERE" single-source contract. Export the anchor like `node_screen`.
5. **Popover can draw under the top-left HUD block** *(blind)* — the popover draws before `draw_hud` and clamps to y=8; an entity near the top-left anchors it under the title/instructions/score/legend/QoS readout (y 10..150), leaving the button invisible-but-clickable. Draw after `draw_hud` or clamp below the HUD band.

### Reviewer agreement

- **ESC mid-click re-select** — 5 independent lenses (blind, security, architecture, codebase, edge) on one code-anchored finding: the highest-confidence item in this report.
- Chord release vs PR interaction map — 3 lenses (acceptance, blind, codebase).
- `popover_rect` small-window clamp — 2 lenses (blind, codebase).

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
