# Briefing: packet-plumber-3d-e1-tiny-planet

Read the standing orders first: `/Users/moses/code/docs/orchestration-playbook.md`
section 'Minion standing orders'. This briefing is your task spec.

## Task

Build **E1 — Tiny Planet & Connect Verb**: the first playable vertical slice
of Packet Plumber 3D (Godot 4). Your spec of record is the merged epic:
`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-3d-2026-09-04/epics.md`
section **E1** (+ the GDD's art-direction and camera sections). The epic's
stories E1.1–E1.5 and its test contracts ARE your acceptance criteria —
this briefing restates the load-bearing points, it does not replace them.

## Scope (from the epic — slice 1 = NO sim, NO character)

1. **E1.1 Planet world** — unit planet, 3 MVP biome wedges from seed;
   geodesic surface math (arc length, surface projection, geodesic paths).
2. **E1.2 Orbit camera** — drag-orbit (free azimuth, latitude clamped
   ±85°, up-vector stable, never rolls), scroll/pinch zoom through the
   ladder (globe / district / street), damped easing. View-layer only.
3. **E1.3 Connect verb** — drag building→building: ray-cast surface
   projection, live preview arc (slight elevation), generous snap radius,
   release-to-connect / cancel-elsewhere. Disambiguation: node-drag = draw,
   space-drag = orbit.
4. **E1.4 Pipe arcs + bundle rendering** — cables hug the surface on
   trestles (valid geodesics, NO tunneling through the planet); parallel
   pipes merge fatter.
5. **E1.5 Node staging** — chunky primitive buildings on the wedges
   (placeholder art per doctrine; look-parity tokens only).

## Acceptance

- **A1 (canon):** every E1 test contract from the epic passes and is
  demonstrable: snap honors intent not path · arcs are valid geodesics ·
  draw-vs-orbit never misfires · camera never rolls · no sim state exists.
- **A2 (runs):** the project boots to the planet scene with Godot 4.7.1;
  the PR body carries the exact run command for the user
  (`godot --path <worktree>` or equivalent). README updated.
- **A3 (verified, not claimed):** use the **Godot MCP** (user-globally
  configured, available in your pane: scene-*, editor-run, debug-output,
  lsp-diagnostics, …) to drive the project — build scenes, run, read
  errors, iterate. `lsp_get_diagnostics` clean on your GDScript.
- **A4 (captures):** commit in-game captures (`captures/` in the repo —
  viewport saves, not the reference material) proving: full globe with
  biome wedges · a zoom-ladder tier · a completed arc between two
  buildings · a parallel-pipe bundle. Reference these in the PR body.
- **A5 (look):** the look target is the little-planet reference at
  `/Users/moses/code/_local-refs/little-planet-ref/` (frames f0/f2/f4 —
  chunky flat-shaded low-poly, bright palette, soft light). **IP guardrail:
  cite for look only; copy NOTHING into the tree.** You are natively
  multimodal — attach the frames and compare directly.
- **A6 (gate):** this slice's exit is **user-played**: the PR opens,
  Perkins loops to APPROVED, the user plays and rules. Your final message
  + self-notify name the run command for the user.

## Environment / tooling

- Godot **4.7.1** at `/opt/homebrew/bin/godot`.
- **Godot MCP in your pane** (gopeak, user-global) — your build/verify
  surface; prefer it over blind file writes for scene work.
- Worktree note: `_bmad` is gitignored; Silas symlinks it during bootstrap
  — your `_bmad-output` planning paths resolve through it.

## Model policy

Minion: **`zai-coding-cn/glm-5.3-flash`** (ops tier; natively multimodal —
read the reference frames inline). Mega-minions (max 10, close before
finish): same model, skills named explicitly.

## Skills policy

- Workflow: **`gds-quick-dev`** (implementation). Step-01 clarifies: HALT
  with numbered questions if genuinely blocked — the epic is the spec, so
  expect few; internal checkpoints are pre-approved.
- **`lavish`** is NOT required (code deliverable — regular PR pattern).

## Perkins

`pr_review=1` — gameplay/canon-surface code (connect verb, camera grammar,
geodesic math). Loop-until-APPROVED; you fold fix rounds locally and hold
the push until each verdict posts.

## Dispatch parameters

```
job_id:    packet-plumber-3d-e1-tiny-planet
repo:      packet-plumber-3d
repo_root: /Users/moses/code/packet-plumber-3d
slug:      e1-tiny-planet
base:      main
model:     zai-coding-cn/glm-5.3-flash
pr_review: 1
notes:     Standard worktree dispatch from origin/main (repo is live).
           Bootstrap: symlink _bmad into the worktree (gitignored — the
           PP-pattern gotcha; worktrees get no _bmad otherwise).
```
