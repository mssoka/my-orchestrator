# Spec + context for Perkins lenses — packet-plumber-v2-5.5-demolish-input (PR #44)

You are reviewing PR #44 (reviewed sha 23e1704eae1abed8cdcdb635d85dd4ec30d8aca2) on repo Packet-Plumber, base v2. Story 5.5 — the demolish INPUT SURFACE (app layer only): release-based click-select (junction/pipe), a demolish popover + X/DEL keys. The demolish MECHANIC (2.3, merged #27) is settled core — this PR wires the player surface. Repo root for verification reads: /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.5-demolish-input-r1 (detached at the reviewed sha — trust it, not origin/v2).

## 1. Job briefing (condensed acceptance)

1. **Select a pipe → demolish** → pipe gone, bundle shrinks gracefully (traffic continues, only full-bundle-loss drops the route `[E1]`), live playable.
2. **Select a junction → demolish** → atomic batch: incident pipes removed in edge-id order, then the vertex (core `[E27]`) — verify live.
3. **Terminal click → NO demolish affordance** (never `.Terminal_Demolish` shown). Mirrors core E2.
4. **Replay equality:** a run with demolishes replays byte-identical `[E10]`.
5. **Full local suite green; existing goldens MUST NOT shift** (app-layer only — no demolish in any existing log; any T1/T2 shift = STOP). New goldens: T2 of pipe-demolish under a bundle + T2 of junction-demolish batch.
6. **PR body** carries an interaction map (what each input does, conflicts resolved) + story card 5.5 in stories-v2.md under slice 5.

**Design pins (latitude within them):**
- Left-click on a pipe selects it (exists — moved from press to RELEASE); left-click on a junction selects it (new). Selection runs on EVERY left release, never only after drags.
- Selected entity shows a demolish affordance — popover button near the entity AND/OR a key (X or DEL). Empty-click / ESC deselects.
- Demolish submits the EXISTING `Cmd_Demolish_Pipe` / `Cmd_Demolish_Node` through the existing command path (action-logged → replay equality `[E10]`). **No new command kinds → NO `LOG_VERSION` bump.**
- Rejects surface the existing error strings (`reject_copy` pattern): terminals show no demolish affordance at all.
- The demolish affordance must never collide with the 1/2 lane keys, right-click dial, or placement mode (demolish disabled while placing).
- No economy: no refund, no inventory — documented `[ASSUMPTION]`.

## 2. Story 5.5 card (stories-v2.md, verbatim)

- **Slice:** 5 · **Epic(s):** E7.2, E7.4 · **Systems:** Input surface `[ODN-12]` (mechanic: 2.3).
- **Goal.** The demolish MECHANIC (2.3 — `Cmd_Demolish_Pipe`/`Cmd_Demolish_Node`, merged #27) finally reachable from the input surface: click-select a pipe or junction on every left release, see a demolish popover + the X/DEL key, and watch the topology respond (bundle shrink, atomic junction batch). The missing third step of 3.5's launchable ("place routers, connect them, demolish and redesign").

**Given/When/Then:**
- **Given** the release-based click-select surface (prototype Perkins r2 B2 pattern: node → pipe → clear, on EVERY left release);
- **When** the player selects a pipe or junction and demolishes it (popover button or X/DEL);
- **Then** the EXISTING `Cmd_Demolish_Pipe` / `Cmd_Demolish_Node` submits through the validated edit fast-path + action log (replay byte-identical `[E10]`; **no new command kinds, no `LOG_VERSION` bump**); a pipe demolish shrinks its bundle gracefully (traffic continues — only full-bundle-loss drops the route `[E1]`); a junction demolish runs the atomic batch (incident pipes in edge-id order, then the vertex `[E27]`); terminals never show a demolish affordance (`.Terminal_Demolish` mirrored in the UI `[E2]`); demolish is disabled while placing (no collision with the 1/2 lane keys, the right-click dial, or placement mode).

- **Edge-case contracts:** `[E1]` `[E2]` `[E10]` `[E27]` `[E29]`. **Golden:** T1 + T2 of pipe-demolish under a bundle (capacity shrink) + T1 + T2 of the junction-demolish batch (the E27 batch ORDER is pinned by the core's 2.3 tests — the golden pins the batch's end state); existing goldens MUST NOT shift (app-layer-only change).
- **Launchable increment:** build a net, demolish a pipe of a bundle (watch the capacity shrink), demolish a whole junction (atomic batch).
- **Assumption:** no economy — no refund, no inventory (the prototype's "refund banked" copy does NOT apply; refunds land with the economy story).

## 3. Architecture pins (verbatim, odin-architecture-v1.md)

- **E1** | Demolish pipe w/ packets in transit → reroute or drop w/ `severance` reason. **Under bundles, demolishing one pipe of a bundle shrinks the pool (graceful), not a hard cut — only full-bundle-loss drops** (routing ruling, lavish 2026-08-10) | Atomic per edge inside `apply_all`
- **E2** | Terminal-node demolish forbidden | `Edit_Error.Terminal_Demolish`
- **E10** | Iteration/tie-break determinism | arrays-only + seeded rng + replay test (ODN-10)
- **E27 (new)** | Junction demolish = atomic batch: incident pipes first (edge-id order, each per E1), then the vertex | §6.1
- **E29 (new)** | **Automatic under per-hop forwarding** — no stale spawn-time routes; topology changes propagate via table rebuild at next sync; in-flight packets re-forward at the next junction. E1 demolish is the (now-only) forced-reroute exception.

## 4. Lens-guards — LOCKED items (do NOT file findings on these)

- **The core demolish mechanic** (2.3 — settled; E1/E2/E27/E29 semantics in core/topology.odin). This PR must NOT change core/.
- **The routing/crisis models** (any file outside the diff).
- **LOG_VERSION 3** — a bump would BE a finding; the absence of a bump is correct. Do not file "LOG_VERSION unchanged" as a finding — flag only if the PR DID bump it.
- **The demolish-input gap being "pre-existing"** — this story IS the fix.
- **Missing router-tier UI (5.6)** — sibling story, held behind this merge. NOT in scope.
- **No-economy** — no refund/inventory is the ASSUMPTION, not a defect.
- **Em-dashes in PP docs** are OK (the codebase uses them; the "no em-dash" rule belongs to another repo).

**The lens-guards that ARE in scope (real findings if violated):**
- 🚨 **LOAD-BEARING — the surface drives the REAL commands.** Click-select + popover + X/DEL must dispatch Cmd_Demolish_Pipe / Cmd_Demolish_Node through the validate→apply path — a surface that renders but never dispatches (or dispatches a wrong command kind) = a blocker. The terminal reject [E2] + junction batch [E27] behaviors must be reachable through the UI (a UI that silently ignores illegal targets = a real defect).
- **Release-based click-select:** select fires on RELEASE (not press); a press-fires select (or a drag that demolishes accidentally) = a finding.
- **Key handling:** X/DEL dispatch only when a demolishable target is selected; no accidental demolition during normal play (a stray key = a finding).
- **Golden discipline:** 2 NEW goldens claimed — verify they're new files + blessed with proof; existing goldens MUST NOT shift (any shift = a finding).
- **Scope guard:** input surface ONLY — app/main.odin + app/render/popover.odin + demos/goldens/docs. NO unrelated refactors, NO core changes, NO catalog changes (catalog edits are golden-poisoned — `cat.hash` folds catalog bytes).

## 5. Implementer claims (PR body — claims to verify, not truth)

1. Selection moved from press to release; click-select runs on every left release (junction → pipe → clear priority; terminal click clears; empty ground clears).
2. Popover press swallows (button = demolish NOW; panel = keep selection, no drag, no re-select on release); `press_swallowed` latch also gates the placement commit (tray-chip release can't place a router).
3. X/DEL demolish the selected entity, disabled while placing AND mid-drag.
4. Demolish fast-path: `pp.topology_apply_edit` → `append(&app.state.action_log, ...)` at apply_tick = tick+1 — byte-identical to draw/place; rejections → `last_reject` toast.
5. Popover draws ONLY from the app render loop (never `draw_world`) — harness T2 capture path untouched.
6. 22/22 demos green (20 pre-existing goldens byte-identical + 2 new); `odin test core` 153/153; lint green; app builds.
7. New goldens deliberately blessed via `harness save`; T2 frames verified visually (fat→slim bundle; junction + incident pipes gone post-batch).
8. CI is account-billing-blocked — red CI is NOT a code failure; local suite is ground truth.

## 6. Where things live (verification map)

- `app/main.odin` — handle_input restructure, click_select, popover_click, release_ui_hit, pipe_anchor, demolish_pipe/demolish_node, ESC/X/DEL keys, reject_label.
- `app/render/popover.odin` — NEW: popover_rect, demolish_button_rect, draw_demolish_popover, draw_popover_panel, draw_demolish_button, POPOVER_W/H_NODE/H_PIPE/TRAY_CLEAR.
- `core/topology.odin` (~209–310) — the settled demolish mechanic (validate_demolish_pipe/node, apply_demolish_pipe/node, E27 batch). UNTOUCHED by this PR.
- `core/serialize.odin` — LOG_VERSION 3; CMD_TAG_DEMOLISH_* command tags. UNTOUCHED.
- `demos/demolish_bundle.dem`, `demos/demolish_node.dem` — the two new demos (T1 + T2 + replay gate).
- `goldens/demolish_bundle.*`, `goldens/demolish_node.*` — the two new golden sets (t1 + log.bin + T2 PNGs).
- `harness/` — capture path (`draw_world` with default sel), replay gate (`expect hash stable`).
- Existing pipe selection machinery: `pipe_hit`, `snap_node`, readout + lane keys 1/2 + right-click dial in app/main.odin.
