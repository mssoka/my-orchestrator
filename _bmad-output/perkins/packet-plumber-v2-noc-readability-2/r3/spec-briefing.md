# packet-plumber-v2-noc-readability-2

## Task

The NOC dashboard is still illegible in play (user verdict 2026-08-23,
third strike: "still so hard to read — bigger fonts please"). KYLE's
assessment of the live screenshot: 1.5–2× needed. Current ladder:
body 14px, labels 12px — labels sit BELOW the game's own 14px minimum
(the 2026-08-15 font-resize floor). Fix properly this time.

## Scope

1. **New ladder**: header/title 20px · body/counters 18px · labels 15px
   (all at-or-above the 14px floor; KYLE's recommendation band).
2. **DOCK RIGHT — full-height rail (user ruling, same message)**: the panel
   docks at the FAR RIGHT of the screen, covering top-to-bottom (a
   full-height right rail, NOC-wall style). The playfield's usable
   width shrinks while D is on (the camera fit math respects the rail
   — or the rail overlays; minion resolves which, documents — but the
   rail NEVER covers the HUD chips' top band mid-ridge: place
   carefully vs the top-band cards; the fit-to-rail approach is
   preferred if the camera math is clean). More vertical space = more
   visible rows at the bigger sizes — the two rulings help each other.
3. **Panel scales with it**: width +~40% (tabular columns need room at
   18px numerals — recompute the column math; keep right-aligned
   tabular figures, zebra rows, dark plate).
3. **Row density**: fewer visible rows at bigger text is CORRECT —
   keep the ring buffer 256, reduce visible rows as fits; the wheel
   scroll handles the rest. (Renumbered: was 3, now after the dock
   rule.)
4. **Verify with KYLE** (remote glm-4.6v; local fallback): capture the
   new panel ON in a real run — KYLE grades legibility (labels
   readable, numbers steady, hierarchy clear, docked right full-height
   per ruling). Include in PR body.
5. Zero golden drift must hold (no pixels until D) — 48/48 proof.

## Rules (hard)

1. View-layer only; hash-equal streams; no pixels without D pressed.
2. Named size constants (not magic numbers) — the ladder is a tunable
   triplet + panel-width scale.
3. Tests updated (panel rect expectations, visible-row math).

## Acceptance

- New ladder in; KYLE legibility verdict on a live capture (PASS).
- 48/48 + full suites; T1/T2/replay hash-equal.
- PR body: before/after captures + the size table.
- pr_review: 1.

## Skills policy

bmad-quick-dev.

## Model policy

deepseek-v4-flash, --thinking max. KYLE: glm-4.6v.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-noc-readability-2
- base: v2 (fresh head — post-#87 b40fe84)
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
