# Spec + context for Perkins lenses — packet-plumber-v2-5.5-demolish-input (PR #59, round 1)

You are reviewing PR #59 (reviewed sha `55d1b66366a05c685f938797a2ed92ea7f1132d4`, short `55d1b66`) on repo Packet-Plumber, base `v2` (base sha `e07265b`). Story 5.5 — the demolish INPUT SURFACE on the 5.4 intent layer: the demolish MECHANIC (core 2.3, merged #27 — `Cmd_Demolish_Pipe` / `Cmd_Demolish_Node`) reachable from mouse, touch, AND controller through the SAME validated intent path.

Verification reads happen in the detached worktree at exactly the reviewed sha:
`/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.5-demolish-input-r1` (trust it, not `origin/v2`).

Project conventions (read before judging style/patterns): `<worktree>/project-context.md` — Odin + raylib, pure core (ODN-1), integer-only sim, no globals, arena discipline, errors are values.

The diff under review: `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.5-demolish-input/r1/diff.patch` (418 lines, 11 files). Verified byte-identical to `git diff e07265b..55d1b66`; `core/`, `data/`, `goldens/`, `demos/` are untouched by it.

## 1. The ONE hard blocker class — demolish input surface parity [FORGE #6]

The story's whole point: the demolish mechanic is reachable from mouse, touch, AND controller through the SAME validated intent path — no per-device command production. Verify:

- **Controller leg:** pad X (`RIGHT_FACE_LEFT` — the keyboard X/DEL twin) maps to the shared `Demolish` intent; `Node_Select` mirrors the dpad cursor onto the selection (junction → select, terminal → clear — `click_select`'s rule, `[E2]` mirrored). "Select → confirm" rides the same executor as the mouse.
- **The W1-r4 fold (4-lens agreement from 5.4):** the shared `popover_demolish_hit`'s POSITIVE path — previously wired only to the negative esc_ui scenario — now executes in scripted scenarios: `input_parity_demolish_btn_node` (mouse == touch == pad → `Cmd_Demolish_Node`) and `input_parity_demolish_btn_pipe` (mouse == touch → `Cmd_Demolish_Pipe`). The minion claims both are mutation-verified (deadening the hit-test / dropping the pad X mapping fails the suite). Confirm the pins actually bite (the scenarios would genuinely fail if the wiring were dead — e.g. check the ui_hook is wired for these scenarios and the expected-command assertion covers the pad leg).
- **The r3-N7 fold:** gate 9 (ci-local + GH workflow mirror) runs a negative-control leg — bogus arg rejected (exit 2), with an `[ -x ]` guard against the 127→!→0 false-green.

## 2. Acceptance criteria (from the original job briefing + story card)

1. **Select → demolish affordance.** On every left release the click-select surface resolves node → pipe → clear; a selected pipe/junction shows the demolish popover and X/DEL is live. Demolish is DISABLED while placing (no collision with the 1/2 lane keys, the right-click dial, or placement mode).
2. **Existing commands only.** Popover button / X/DEL submits the EXISTING `Cmd_Demolish_Pipe` / `Cmd_Demolish_Node` through the validated edit fast-path + action log. **No new command kinds, no `LOG_VERSION` bump**; replay byte-identical `[E10]`.
3. **Topology response.** Pipe demolish shrinks its bundle gracefully — traffic continues, only full-bundle-loss drops the route `[E1]`. Junction demolish runs the atomic batch: incident pipes in edge-id order, then the vertex `[E27]`. Terminals NEVER show a demolish affordance (`.Terminal_Demolish` mirrored in the UI) `[E2]`. Rejects surface the existing error strings `[E29]`.
4. **Goldens.** New T1+T2 of pipe-demolish under a bundle and junction-demolish batch were pinned by the 2.3 demos (`demolish_bundle`, `demolish_node`). Existing goldens MUST NOT shift — app-layer-only change.
5. **No economy.** No refund, no inventory, no refund copy anywhere.

The story card §5.5 (verbatim) is at `./story-card-5.5.md` next to this file. The full original job briefing is at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-5.5-demolish-input.md`. No GitHub issue exists for this story (checked — issues #48/#34/#6 are unrelated); the briefing + card ARE the spec.

## 3. What NOT to re-litigate (out of scope for findings)

- The 2.3 demolish CORE mechanic (merged #27, already reviewed — verify the WIRING, not the mechanic).
- The 5.4 intent-layer architecture (4 approved rounds — its decisions stand).
- The superseded 08-14 #44 implementation (pre-intent-layer code, replaced).
- The carried 10W/11N warnings/notes from 5.4 r1–r4 (fold ONLY where they touch the demolish surface — never as new scope).

## 4. Claims made by the PR body (verify, don't trust)

- Pad X = `RIGHT_FACE_LEFT` → `Demolish` intent; `Node_Select` mirrors cursor → selection (junction → select, terminal → clear).
- Executor re-checks `placing < 0 && !drag.active` for Demolish (inert while placing/mid-drag, same as keyboard X).
- 2 new parity scenarios (24 total), both mutation-verified; gate 9 negative-control leg mutation-verified.
- `pipe_anchor` single-sourced in `app/render/popover.odin`; `pipe_popover_anchor` in exec.odin delegates (N2-r4 fold).
- Zero changes in `core/`, `data/`, `goldens/`, `demos/` (CONFIRMED by the reviewer orchestrator: the diff touches none of those trees).
- Full local suite green: `tools/ci-local.sh --mac` 9/9, 184 core tests, 29 demos byte-identical, 24 parity scenarios.

## 5. CI note

GitHub Actions on #59 is org-billing-blocked (runners never start) — NOT a signal; the local suite is ground truth.
