## 🤖 Perkins automated review — round 1 of 3
**Job:** packet-plumber-v2-5.4-input-parity · **Reviewed sha:** `2f5027a` · **Reviewers:** 14/14 lens-runs completed (7 lenses × 2 chunks — 3,816-line diff split at the ~3,000-line policy: `app/` vs harness+goldens+ci)
**Verification:** 27/28 unique findings confirmed against the code (44 raw lens reports deduped) — 1 discarded as false-positive, 0 kept as [unverified]

The intent layer is a faithful, well-documented transcription and the guard checks pass: every command-producing input path funnels through the intent layer (the one remaining direct `rl.GetMouseX/Y` is the pre-existing view-only hover card), validation lives at the Command stage with rejections surfaced (not silently dropped), no `LOG_VERSION` bump and no serialization change, landscape is camera-fit flag-only (Pan is an explicit, flagged no-op), and the T1 across-inputs pins are real — live command+hash stream equality per scenario, 2 blessed manifests, CI step wired. The FORGE #6/ODN-12 design, the 5.2/5.8 serialization discipline, and the #55 rebase hunks were not re-litigated.

Two mouse-path parity deltas survived verification — the round's ONE hard blocker class.

### Blockers (2)

**B1 — Phase-2 keys act on frames the old `handle_input` early-returned from** [acceptance] · `app/input/mouse.odin:217-236` + `exec.odin:134-149`
The old code `return`ed inside the right-press branch (and on popover/QoS/tray-swallowed left-presses), so X/DEL/U/1/2/E/S/B were **ignored** on those frames. The new mapping emits phase-2 key intents unconditionally, and the executor's Demolish re-checks only placing/drag — which Right_Click has already cleared. **Same-frame right-click+X: old = select the pipe; new = select + DEMOLISH it.** Same for a popover-swallowed left-press+X. Deterministic, scriptable mouse-path delta.
*Fix direction:* suppress phase-2 key intents on frames with a right-press or a UI/tray-swallowed left-press (mirror the old early returns); add a same-frame right-press+X T1 case.

**B2 — Same-frame ESC + left-press while placing diverges (no drag starts; the release is swallowed)** [codebase, edge] · `app/input/mouse.odin:63-76,148-181` + `exec.odin:45-58`
Old order: cancel block ran FIRST (`placing=-1`, swallow set), then the press block re-anchored, **reset** the swallow, ran the popover/QoS checks and started a drag — the release committed or click-selected. New: the mapping evaluates the press branch on pre-execution `placing` (still ≥0 → no `Begin_Draw`, no UI checks), then the executor's Cancel re-latches `press_swallowed=true`, killing the later release. The whole gesture dies where the old code drew a pipe. `input_parity_cancel` scripts ESC alone, so the corner is unpinned.
*Fix direction:* when `esc_cancelled`, decide the left-press branch on the post-cancel state and re-clear the swallow after Cancel executes; add the same-frame ESC+press scenario.

### Warnings (11)

1. **`input_parity_right_click` asserts nothing about the right-click SELECT** [blind, edge, acceptance, architecture] — the scenario comment promises `sel_pipe == 0`, but `check_states` has no case for it; a broken right-click select passes green on the hard-blocker surface.
2. **Same-frame duplicate phase-1 keys break the old `||` semantics** [blind, edge] — P+Space double-flips pause (net no-op), R+Enter double-restarts. Coalesce to one intent per frame.
3. **Touch presses bypass the app-UI swallow** [blind] — `touch_map` never calls `on_ui_press`: draws start/commit through the demolish popover + QoS panel, and the popover buttons are touch-dead.
4. **One shared drag slot, no gesture ownership** [architecture] — a touch press or pad A mid-mouse-drag hijacks/commits it (`begin_draw` overwrites unconditionally).
5. **Per-frame heap churn** [architecture] — `mouse_map`'s `moves` dynamic allocates+frees every frame (poll emits `Mouse_Move` per frame); violates the zero-per-frame-heap-churn rule (`project-context.md:63`).
6. **Pad B (Cancel/Cancel_Drag) + Start have zero coverage** [tests] — `Cancel_Drag` is brand-new executor code; only `.A/.Dpad_Down/bumpers` are scripted.
7. **No negative/validation-rejection scenario** [tests] — the 'rejections are surfaced, not silently dropped' guard is code-read-only; `last_reject/reject_tick` never execute under test.
8. **Game_Over retry + pause toggle never driven** [tests] — R/Enter, pad A at Game_Over, P/Space/Start produce no intent in any scenario.
9. **Mouse transcription branches unpinned** [tests] — pause/assist/overlay/preview keys, ESC-deselect, right-while-placing (W3), drag-interrupt swallow — the same corner class as B1/B2.
10. **`pad_step` boundaries untested** [tests] — Dpad_Up first-placement, wrap, dead-node skip never run despite an edge-hunter fix living in that arithmetic.
11. **Advisory test gate: FAIL** [tests ×2, calibrated warning per round guards] — the across-inputs pin is real, but P1 breadth (rejections, pad B, same-frame gates, right-click edges) is untested — and B1/B2 were found in exactly those corners. Land the blocker fixes *with* their pinning scenarios, then re-bless.

### Notes (14)

- `key_map` in poll.odin is dead code (zero callers, grep-verified) [blind, codebase]
- Pad cursor can point at a demolished node; Confirm aims from a dead id resolved via `node_pos[0]` (validation rejects — no corruption, silent no-op until dpad step) [blind, edge]
- A touch press clears the mouse press's swallow latch mid-frame → later mouse release re-selects [blind]
- Pad aim-commit never invokes `on_drag_update` → the R3 glow never lights for pad draws (the app's effect doc claims it does) [edge]
- Pad B while placement is armed routes to `Cancel_Drag`: ghost hides, `placing` stays armed, next release places [edge]
- Four unused imports in `app/input` (exec:fmt, touch:rl, controller:rl+pp) — compile-clean on the pinned nightly, dead baggage [codebase]
- Demolish node flavor / Delete key / same-frame X-suppression gate unpinned [tests]
- T1 goldens are first-blessed here; 'mouse preserved exactly' has no pre-change baseline (rests on transcription review — which caught B1/B2 — plus the explicit expected streams) [tests]
- `parity_right_click_effect` hand-duplicates the app's `effect_right_click` (identical today; drift silently decays the pin) — move the body into `app/input` and delegate [tests, architecture, codebase]
- Mixed-device frames never scripted — the fixed mouse→touch→controller dispatch order is unexercised [tests]
- Effect hooks pass an untyped `rawptr user` — a documented departure from the events-not-callbacks convention (ODN-14) [architecture]
- The input package now hosts QoS business rules (lane auto-follow moved from `qos_panel`) — structurally motivated, watch the cohesion [architecture]
- `class_cycle` mouse leg is vacuous (preset 0 + `.One` SETs 0 — a dropped key passes) [edge, acceptance]
- Scenario frame scripts leak their `[dynamic][]Device_Event` backings (trivial, one-shot CLI) [edge]

**Discarded as false-positive (1):** "cmd_equal compares only apply_tick + kind — wrong payloads pass" [blind] — Odin union `==` compares tag **and** payload; all `Command_Kind` variants are plain comparable structs (`core/types.odin:58-64`). The expected-stream check is payload-aware.

### Reviewer agreement

Highest-confidence signals (multi-source, code-verified): **B2** [codebase+edge]; the unpinned right-click select [blind+edge+acceptance+architecture]; duplicate phase-1 keys [blind+edge]; the right-click effect duplication [tests+architecture+codebase]; `key_map` dead code and the stale pad cursor [blind+edge / blind+edge].

**Verdict:** NEEDS CHANGES

Two confirmed mouse-path parity deltas (B1/B2) against the round's hard blocker — mouse behavior preserved EXACTLY. Both are deterministic, scriptable same-frame corners with clear fix directions; the warnings are dominated by the coverage gaps that let them through.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
