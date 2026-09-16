# Briefing: packet-plumber-3d-scene-refactor

Read the standing orders first: `/Users/moses/code/docs/orchestration-playbook.md`
section 'Minion standing orders'. This briefing is your task spec.

## Task

**Multi-scene architecture + GDScript file/folder organization** per Godot
best practice (user ruling, 2026-09-05: "we need to follow best practice of
multiple scenes instead of a single one. and gds file/folder org").
**ZERO behavior change** — this is a pure restructure; the determinism
contract (replays byte-identical), every test, the editor preview, and the
look all stay exactly as they are.

## Current state (the problem)

- ONE scene: `scenes/main.tscn` — everything is child nodes + code-built.
- `scripts/` is flat (14 files, only `sim/` nested).

## Target structure (Godot best practice, campaign-ready)

1. **Component scenes** — each entity a scene, instanced in the composition
   root (keep code-driven GENERATION where it exists; scenes wrap and
   instance it):
   - `scenes/planet.tscn`, `scenes/node_site.tscn`, `scenes/orbit_rig.tscn`,
     `scenes/flow_view.tscn`, `scenes/qos_panel.tscn`, `scenes/hud.tscn`,
     connect layer as fits.
   - `scenes/main.tscn` becomes the thin composition root instancing the
     above.
2. **Campaign scaffold** — `scenes/levels/` + a `level_base.tscn` pattern
     (a documented base the L1 ARPANET scene will build on; do NOT build
     L1 — GDD v2 spec exists, implementation is a separate job).
3. **Script folders by domain**:
   - `scripts/world/` — planet, world_seed, geodesic, node_site, pipe_arc
   - `scripts/sim/` — stays
   - `scripts/input/` — input_router, connect_controller, orbit_camera
   - `scripts/ui/` — hud, qos_panel
   - `scripts/` root — main (composition root) only
   - `tools/` — stays
4. **Path hygiene**: every preload/load/moved reference updated; `.uid`
   files move WITH their scripts (Godot 4 script identity); `project.godot`
   main_scene path updated if main.tscn moves.

## Acceptance

1. **Zero behavior change proven**: determinism replay byte-identical to
   pre-refactor on the fixed seed; full suite green (202+); LSP diagnostics
   clean; `godot --headless --import` clean on a FRESH CLONE.
2. Editor preview ("Regenerate Preview") works — capture committed.
3. The new tree diagram in the PR body (before/after).
4. No orphan files; every moved script's references resolve.
5. Tests that pin file locations (if any) updated with the same
   structural-pinning style they already use.

## Model policy

Minion: **`zai-coding-cn/glm-5.3-flash`**. Mega-minions: same, skills named.

## Skills policy

Workflow: **`gds-quick-dev`**. No lavish (code deliverable).

## Perkins

`pr_review=1` — canon-surface restructure. Loop-until-APPROVED.

## Dispatch parameters

```
job_id:    packet-plumber-3d-scene-refactor
repo:      packet-plumber-3d
repo_root: /Users/moses/code/packet-plumber-3d
slug:      scene-refactor
base:      main
model:     zai-coding-cn/glm-5.3-flash
pr_review: 1
notes:     Worktree from origin/main (post-#6/#7). _bmad symlink bootstrap.
           This is the ONLY in-flight code lane on the repo — GDD v2 is
           merged, L1 implementation WAITS for this refactor (it builds
           the levels/ structure L1 lives in).
```
