# Briefing: packet-plumber-3d-art-integration

Read the standing orders first: `/Users/moses/code/docs/orchestration-playbook.md`
section 'Minion standing orders'. This briefing is your task spec.

## Task

**Wear the wardrobe**: replace the placeholder primitive buildings/pipes
with the user-picked assets in `assets/` (PR #3, merged). The user opened
the editor and saw boxes — the picked art must be what the world stages,
in RUNTIME and in the EDITOR PREVIEW (the "Regenerate Preview" inspector
path builds the same world).

## What exists

- `assets/houses|dcs|schools|junctions|cables/` (+ `ATTRIBUTION.md`) —
  the 10 user picks (glTF, bbox-normalized, import-clean). The user's pick
  language is canon: junctions = **round devices / Round-Window shape
  language**; links = **frosted-glass conduit** + **lane-colored packet
  beads** (beads already exist in E2's FlowView — keep them).
- `scripts/node_site.gd` — currently BoxMesh/CylinderMesh primitives,
  surface-normal staging logic (KEEP the placement/orientation math).
- `scripts/main.gd` `@tool` + "Regenerate Preview" — the editor path.

## Acceptance

1. **NodeSite stages real assets per node type** — house→`assets/houses/`,
   DC→`assets/dcs/`, school→`assets/schools/`, junction→`assets/junctions/`.
   Deterministic per-site variety selected FROM THE SEED (same seed → same
   world, byte-identical replays — the determinism contract is absolute).
2. **Pipe arcs wear the cable visual** — the picked conduit/cable assets
   (or their materials) on the arc rendering; frosted-glass look per the
   user's pick; parallel bundles still read "fatter".
3. **View-layer purity**: sim replay state unchanged by the art swap
   (the E2 test contracts re-run green — 185 checks).
4. **Editor preview shows the real look** — "Regenerate Preview" builds
   the world with assets; verified by capture.
5. **Look parity evidence**: captures committed (`captures/`) — editor
   preview + runtime, side-by-side with the reference frames
   (`/Users/moses/code/_local-refs/little-planet-ref/` f0/f2/f4 — cite
   only, copy nothing).
6. **Tri discipline**: total staged scene stays light for the tiny planet;
   note per-asset tri counts in the PR body.
7. `godot --headless --import` clean; LSP diagnostics clean; suite green.

## Environment

- Godot 4.7.1 (`/opt/homebrew/bin/godot`); **Godot MCP** in your pane
  (scene-*, editor-run, debug-output, lsp-diagnostics) as the build/verify
  surface. You are natively multimodal — attach the captures and the
  reference frames; verify the LOOK yourself before claiming parity.

## Model policy

Minion: **`zai-coding-cn/glm-5.3-flash`**. Mega-minions: same, skills named.

## Skills policy

Workflow: **`gds-quick-dev`**. No lavish (code deliverable).

## Perkins

`pr_review=1` — canon-surface visual code. Loop-until-APPROVED.

## Dispatch parameters

```
job_id:    packet-plumber-3d-art-integration
repo:      packet-plumber-3d
repo_root: /Users/moses/code/packet-plumber-3d
slug:      art-integration
base:      main
model:     zai-coding-cn/glm-5.3-flash
pr_review: 1
notes:     Worktree from origin/main. _bmad symlink bootstrap. PARALLEL
           LANE: gdd-amend-levels (docs-only worktree) — files disjoint.
```
