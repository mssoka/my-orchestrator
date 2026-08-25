# packet-plumber-v2-camera-zoom

## Task

Zoom in/out + pan for the game camera. User directive (2026-08-23):
"zoom in and out enabled — to see areas and out for the overall bird
view of the city." This is the prerequisite for the real-city-maps arc
(a Dublin cross-section board is coming — design questions pending
with the user) and a standalone UX win.

## Scope

1. **Wheel zoom** around the cursor position (zoom-to-point, not
   zoom-to-center), clamped to sane min/max (min = the current
   fit-to-window view; max = enough to read individual nodes/links
   clearly).
2. **Drag pan** (mouse drag on empty map space — must not conflict
   with pipe drawing / node placement gestures; gate pan-drag so it
   never eats a draw gesture; middle-drag or space-drag are acceptable
   fallbacks if left-drag conflicts — minion resolves, documents).
3. **Wheel ownership vs the NOC panel**: wheel = map zoom; the NOC
   drop log scrolls ONLY when the pointer is over the log region
   (the r1 scroll-clamp work already localizes the log — build on it).
4. **HUD + overlays stay screen-space** (HUD, NOC panel, chips,
   banners do NOT zoom — anchored to the window); world elements
   (nodes, wires, packets, terrain) zoom with the camera.
5. **Deterministic captures**: the harness capture path pins the
   default camera (fit-to-window) so existing goldens/captures are
   UNAFFECTED — no re-bless from this job unless a golden genuinely
   changes (report any).
6. Font readability at zoom: the #87 font-overhaul approach (IBM Plex
   + AA) must hold at zoom extremes — world-space text either scales
   cleanly or snaps to screen-space; pick and document (no blurry
   bitmap scaling).

## Rules (hard)

1. View-layer only — sim/determinism untouched; T1/T2/replay
   hash-equal.
2. Raylib Camera2D (the established camera fit already exists —
   map.* in balance.json); follow existing input conventions.
3. No new dependencies; no gameplay-semantics change.
4. Golden safety per rule 5 — report any capture that moves and why.

## Acceptance

- Wheel zoom-to-point, clamped; drag pan without gesture conflicts;
  HUD screen-space at all zooms; NOC wheel-ownership respected.
- Mechanical capture: same tick at default zoom byte-matches the old
  capture (no golden drift); a zoomed capture in the PR body shows the
  feature.
- T1/T2/replay hash-equal; 11/11 + full suites green.
- pr_review: 1.

## Skills policy

bmad-quick-dev.

## Model policy

deepseek-v4-flash, --thinking max.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-camera-zoom
- base: v2 (fresh head at dispatch)
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- parallel-safe with font-overhaul (#87) + blender-sculpt + ambience
  (#86): camera/input surface — coordinate merge order with Silas
  (font is merge-last of the old wave; camera has no golden storm)
