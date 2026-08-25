# packet-plumber-v2-flow-focus

## Task

Source-focus broadcast visualization. User directive (2026-08-23):
"if we have source/destination it doesnt have to be pairs, could be a
broadcast — how do we make that work?" Click a node → see every
destination it feeds and every pipe its traffic rides, in one glance.

## Scope

1. **Focus mode**: click a node = focused SOURCE (click empty/ESC =
   clear). Hover-focus is explicitly NOT the default (too fleeting) —
   click only.
2. **The fan**: destinations the source feeds PULSE (reuse the
   telegraph-ring token from spawn_fx); pipes carrying its traffic get
   a translucent glow band whose alpha/intensity scales with that
   pipe's SHARE of the source's flow (the spawn_fx band math — quad
   pair + round caps, the rlsw line-alpha trap is documented there).
3. **Data**: derive from live packets + a rolling window (last N
   ticks) of per-(source → dst, edge) counts — read-only aggregation,
   the NOC overlay's scan pattern. No sim writes. N is a named
   tunable.
4. **Reduced motion**: pins steady states (no pulse; static fan) per
   the existing reduced-motion gate.
5. **Readability**: the fan must not fight the crisis glow or the
   spawn band — distinct hue (route-adjacent but distinguishable) or
   distinct token; document the choice.
6. **Future-proof (do NOT build)**: class-focus (SLA-row click) and
   pair-focus (source then dst) reuse this machinery — leave the
   focus-state design open to extension.

## Rules (hard)

1. View-layer only; zero sim writes; T1/T2/replay hash-equal.
2. Captures never click → zero golden drift (48/48 must hold); add a
   pin test for the focused state rendering.
3. Follow existing conventions: spawn_fx band math, telegraph ring
   token, palette tokens (no new colors without palette-odin review).
4. Interaction must not conflict with existing gestures (selection,
   placement, drag-pan, zoom) — focus on click of a node that is NOT
   mid-placement; document the resolution vs selection (focus could
   BE selection's new visual layer — minion resolves, documents).

## Acceptance

- Click node → fan (destinations pulsing, pipes banded by share);
  ESC/empty-click clears; reduced-motion steady variant works.
- Rolling-window tunable; stable fan (no flicker at 20 Hz).
- T1/T2/replay hash-equal; 48/48 + full suites; new pin test green.
- PR body: capture of the fan on a live board + the gesture-conflict
  resolution documented.
- pr_review: 1.

## Skills policy

bmad-quick-dev.

## Model policy

deepseek-v4-flash, --thinking max.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-flow-focus
- base: v2 (fresh head at dispatch)
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- parallel-safe: view-layer; coordinate merge order (several PRs in
  flight — Silas coordinates)
