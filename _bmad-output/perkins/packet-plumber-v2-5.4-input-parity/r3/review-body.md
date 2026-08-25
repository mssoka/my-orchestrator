## 🤖 Perkins automated review — round 3 of 3 (FINAL automated round)
**Job:** packet-plumber-v2-5.4-input-parity · **Reviewed sha:** b467f9d · **Reviewers:** 7/7 completed
**Verification:** 9/11 lens findings confirmed against the code — 2 discarded as false-positive; the chief's fix-audit re-verified every r2 finding against the worktree, with **5 live mutation tests / probes** run at the reviewed sha (input-parity 20/20 green baseline).

### Fix audit (r2 → r3) — the headline

The r2 blockers are **both fixed**:

- **r2-B1 (map-time ESC deselect) — FIXED, pin verified live.** `esc_deselect` clears the selection at map time before the press branch; `input_parity_esc_ui` pins ESC + demolish-button click (no command, selection cleared). Mutation: deleting the deselect block fails the suite (`expected 0 commands, got 1`). The QoS-row leg is covered by construction (`qos_panel_click` returns false when `sel_pipe < 0` — same gate, same ctx).
- **r2-B2 (`drag_eff`) — FIXED, behavior verified by probe.** The true non-moved shape [board press while placing, then ESC + same-point release] is a total no-op *with* the fix and click-selects *without* it — the fix is load-bearing and correct. (Its shipped pin has a gap — see W2.)

Also confirmed fixed: drive_parity single-apply + re-blessed manifests (W2-r2), the reject/demolish/esc_press vacuous pins (W3–W6 — the latch pin mutation-verified), pad_cursor split (W16), pan re-script (W13), chord Press_Anchor no-ESC leg (W1), R+Enter break (r1-W2-leg), arg validation, zero-device guard, leaks, imports, label/comment fixes. The delta is verified fix-shaped: 7 files, no core changes, no LOG_VERSION bump, no serialization change, no new scope.

**However — the W1-r2 re-gate cut too deep and introduced a new mouse-path delta.** One blocker.

### Blockers (1)

1. **Press_Anchor re-gate drops the chord's swallow reset on ESC frames** [edge + acceptance + codebase — 3-way agreement, chief probe-verified] — `app/input/mouse.odin:188`.
   Same-frame **ESC + right + left chord**, then a non-moved release: the old `handle_input` ran the ESC block (latch=true) *then* the chord re-anchor (latch=**false**) — the release click-selected. The new gate emits Press_Anchor only when `placing_eff >= 0 && !esc_cancelled`, so on ESC frames the queued Cancel's latch=true lands *after* the map-time re-anchor and **sticks** — the executor's Select no-ops. Probe on b467f9d: `[Esc+Right@n1+Left@n1]` then `[release@n1]` leaves `sel_node=-1`; the old code leaves `sel_node=1`. Both ESC-chord shapes (±placing) diverge. Exotic chord, but it is exactly the round's ONE hard-blocker category: a mouse-path behavioral delta vs the pre-change `handle_input`.
   **Fix:** emit Press_Anchor whenever a same-frame Cancel precedes the chord (`has_left && (esc_cancelled || esc_deselect || placing_eff >= 0)`), ordered **before** Right_Click so the old last-write latch order survives a drag-interrupting right-click. Pin both ESC-chord legs with a chord-then-release scenario.

### Warnings (3)

1. **ci-local.sh: the input-parity gate is unreachable — both full-suite `run_gates` calls still cap at 8** [security + architecture] — `tools/ci-local.sh:162,227`. The W15-r2 fix added the 9th GATES entry + "all 9 gates" docs but never bumped the counts — the local mirror silently skips the parity gate in `--mac` and `--in-container` full runs. Still present since round 2 (fix incomplete). Use `${#GATES[@]}` so count and list can't drift again.
2. **`esc_release_place` ships a moved-release shape — the `drag_eff` leg of the B2 fix is unpinned** [chief, mutation-verified] — `harness/parity.odin:697-702`. Anchor at the tray chip, release at n1 = >6px moved, so the moved-check (not `drag_eff`) prevents the select: deleting `&& !esc_cancelled` passes 20/20. The r2-B2 recommended pin was an ESC + **non-moved** release; add the board-press-while-placing frame so anchor == release point (verified: that shape fails without `drag_eff`, passes with it).
3. **Advisory test gate: CONCERNS** [tests] — P0 100% at observable level, P1 ~100%, overall ~83%. Below PASS on the W2 pin gap plus two zero-coverage surfaces (the chord gate — the blocker's hole — and the input-parity arg-validation error leg).

### Notes (7)

- **`esc_pressed` is write-only dead state — and always-true anyway** [blind + security] (`mouse.odin:58,110`; `has_key` scans zero-initialized `[4]Key` slots and `.Esc` is the enum zero). Delete it, or scan `keys[:keys_n]` if a consumer lands.
- **ESC-branch misindent** [blind + architecture + codebase] (`mouse.odin:125` — `esc_cancelled = true` dedented; cosmetic).
- **`!esc_cancelled` redundant in the chord guard** [blind] (`mouse.odin:188` — `placing_eff >= 0` already implies it; fold into the blocker rework).
- **`mouse_map` header contract now false** [acceptance + architecture] (`mouse.odin:27-29` — "mutates only (press, press_swallowed)" vs the map-time deselect; amend the comment to name the exception — the fix approach itself is the r2-recommended one and stands).
- **`parity_ui_press_effect` hand-composes the popover hit-test** [architecture] (junction leg duplicated; rect math shared via `rnd` helpers — watch drift).
- **Chord gate zero coverage** [tests] (the hole the blocker fell through; closed by the blocker's pins).
- **input-parity arg-validation error leg untested** [tests].

### Carried forward (still open — not blocking)

From r1/r2, unchanged by this delta: phase2_blocked disjunct pins (W7-r2), on_ui_release/QoS hook legs (W8-r2 residue), pad Start (W9-r2), pad_alive/dead-skip (W10-r2), placement release gates (W11-r2), click_select branches (W12-r2), S/B/.One keys (W14-r2), one shared drag slot (r1-W4), Game_Over retry surface (r1-W8-leg), right-press-while-placing/mid-drag/U-preview legs (r1-W9-legs), plus 13 notes (incl. `.memlog.md` still saying "11 scenarios / Next: commit + PR", and the `sel_pipe` struct comment still saying "0 = none selected").

### Reviewer agreement

The blocker carries a 3-lens agreement (edge, acceptance, codebase) **and** a chief probe at the reviewed sha — highest confidence. The ci-local cap carries 2-lens agreement (security, architecture).

### Rejected (false positives)

- "esc_ui pin vacuous — router isn't a Junction" [blind] — `router_basic` **is** `kind: "junction"` (node_types.json:29); the mutation test fired the demolish through the wired hook.
- "B2 suppression asymmetric — deselect path still takes the drag branch" [blind] — matches the old deselect block exactly (it never cleared `drag.active` either); byte-parity, not a defect.

**Verdict:** NEEDS CHANGES — one delta-introduced mouse-path parity blocker. Everything else from r2 landed; this is a one-guard rework plus its two pins.

_This was round 3 of 3 — the automated rounds are spent. The human takes over from here: the blocker above is small and precisely specified (one guard + its pins), and the carried warnings/notes are documented for the follow-up._
