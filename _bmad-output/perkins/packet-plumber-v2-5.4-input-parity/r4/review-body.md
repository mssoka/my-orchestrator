## 🤖 Perkins automated review — round 4 (cap lifted — loop until approved)
**Job:** packet-plumber-v2-5.4-input-parity · **Reviewed sha:** 606bfcd · **Reviewers:** 6/7 completed (blind failed twice on malformed JSON output — findings dropped; degraded-review guard satisfied: findings remain)
**Verification:** 5/5 findings confirmed against the code — 0 discarded as false-positive

### Fix audit (r3 findings — verified FIRST, with live mutation testing)
- **r3-B1 (the chord-gate blocker) — FIXED + pins bite.** `press_anchor := has_left && (esc_cancelled || esc_deselect || placing_eff >= 0)` now fires on ESC frames, ordered BEFORE Right_Click in both right-branch legs (the old last-write latch order survives a drag-interrupting right-click). MUTATION: reverting the gate to the r3 condition fails BOTH new chord scenarios with the exact r3 probe signature (`sel_node -1, want 1`). The r3 probe [Esc+Right@n1+Left@n1, release@n1] → sel_node=1 is now pinned for BOTH chord shapes (±placing) by `input_parity_esc_deselect_chord` / `input_parity_esc_cancel_chord` (22/22 green).
- **r3-W1 (ci-local gate unreachable) — FIXED.** Both `run_gates` calls derive from `${#GATES[@]}`; a full `ci-local.sh --mac` run at this sha executed **9/9 gates, all green**, incl. gate 9 input-parity.
- **r3-W2 (esc_release_place moved-release shape) — FIXED.** The board-press-while-placing frame makes anchor == release point; MUTATION (`drag_eff := inp.drag.active`, the r2-B2 bug shape) now FAILS the scenario — the drag_eff leg is pinned.
- **r3-W3 advisory gate — both prescribed raises landed; the tests lens files the gate PASS this round.**
- **r3 fold set all confirmed:** esc_pressed dead state removed; ESC-branch indent; mouse_map header names the map-time deselect exception; `parity_ui_press_effect` delegates to the shared `input.popover_demolish_hit` (read-verified byte-equivalent to the removed app-side code — junction gate, demolish-on-button + swallow, panel-body rect, midpoint math; `app.input.topo/view` alias `&app.state.topology/&app.view`); sel_pipe comment corrected; .memlog updated.
- **Delta verified fix-shaped:** 7 files, the r3 fix + fold set only — no new scope, no core changes, no LOG_VERSION bump, no serialization change.

### Blockers (0)
None. The round's ONE hard blocker class (mouse-path parity vs the pre-change `handle_input`) comes back clean under probe + mutation.

### Warnings (1)
- **W1-r4 — the shared `popover_demolish_hit`'s positive demolish path never executes in any scripted scenario** [edge, acceptance, architecture, tests — 4-lens agreement] (`harness/parity.odin:813-816` + `app/input/exec.odin:437-475`). The ui hook is wired only for `input_parity_esc_ui`, whose map-time deselect clears the selection before the press branch, so the shared helper always early-returns; the NEW pipe leg is unreachable. App-side mouse behavior is byte-equivalent (read-verified) — this is pin fidelity on the round's new shared code, not a behavior defect. Fix: positive-pin scenarios (junction demolish-button press → Cmd_Demolish_Node; the pipe twin → Cmd_Demolish_Pipe).

### Notes (4)
- **N1-r4** `esc_deselect_chord`'s placing==-1 assert is vacuous on leg 1 (placement never armed in scenario 21; only the sel_node==1 probe pins it) [edge]
- **N2-r4** `pipe_popover_anchor` duplicates the pipe-midpoint math render computes inline in `draw_demolish_popover` — render owns layout, so the anchor remains a drift surface (pre-existing in kind, relocated not introduced) [codebase]
- **N3-r4** `pipe_popover_anchor` discards `node_slot`'s ok — safe via the caller's `pipe_slot` guard; verbatim move of the old `pipe_anchor` [security]
- **N4-r4** Advisory test gate: PASS (P0 100% mutation-pinned, P1 100%, overall ~90%) [tests]

Carried forward (still open, tracked from r1–r3 — do not block): 10 warnings + 11 notes (+2 accepted-standing), incl. r3-N7 (input-parity CLI arg-validation leg untested). Full ledger in `consolidated.json`.

### Reviewer agreement
W1-r4 is the round's agreement finding (4 independent lenses). Everything else is single-source and note-grade.

**Verdict:** READY TO MERGE

The r3 blocker is dead (mutation-proven), every fold item verified, the delta is exactly the fix set, and the full local suite runs 9/9 green at this sha (GH CI remains billing-blocked — not a signal; the local suite is ground truth). Approving. The carried warnings/notes and W1-r4's positive demolish pins are good follow-up candidates but are not merge gates.

_No push needed — this round approves. The carried findings stay on the ledger for the next slice._
