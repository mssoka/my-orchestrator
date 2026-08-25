# packet-plumber-v2-blender-silhouettes

## Task

OPTIONAL-but-dispatched: the MM-minimal silhouette re-render. User
decision 2026-08-22: run this IN PARALLEL with the in-engine wave
rather than holding it. Only a re-render if the in-engine pass
under-delivers — but the worktree is opened now so the pipeline is
ready and the user can launch the Blender pass on their own schedule.

Target: true MM-minimal silhouettes per node type (flat single-fill
rects/discs, thin dark outline, no gable step, no wash, no 3D fake)
via the existing sprite pipeline `tools/gen_sprites.py` (Blender 5.2).

Per-type silhouette specs (from kyle-design-directions.md + the audit's
silhouette direction):
- residential: simple house (gable rect) — keep the house read, drop
  the roof-step detail that reads "game asset"
- small_biz: flat shop block (wide rect, no awning detail)
- campus: flat wide block (brick color family, no facade lines)
- content_host: flat tower-ish block (deep blue, taller aspect)
- routers: flat discs with port ring only (no two-tone weight)

## Rules (hard)

1. The user LAUNCHES the Blender session themselves — this job
   preps/validates the pipeline (tools/gen_sprites.py input formats,
   silhouette specs, render settings) so the Blender pass is a
   fill-in-the-blanks re-render. If the user launches it, do the
   re-render; if not, deliver the pipeline + spec ready for them.
2. T2 re-bless required on any sprite asset change (goldens compare
   against rendered sprites) — cause-documented.
3. MM refs are reference-only; never copy MM bytes into the repo.
4. Coordinate with the in-engine wave: silhouettes land AFTER the
   scale/shadows pass reads (merge near the end; final wave re-bless
   is one pass).

## Acceptance

- Pipeline + per-type silhouette spec ready for the user's Blender
  launch; if launched, re-rendered sprites with T2 re-bless.
- No sprite change without documented golden impact.
- pr_review: 1 (Perkins before merge).

## Skills policy

bmad-quick-dev; the repo's tools/gen_sprites.py + docs/Blender notes.

## Model policy

deepseek-v4-flash, --thinking max.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-blender-silhouettes
- base: v2
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- parallel-safe with the whole v2 visual wave; merges LAST (sprite
  assets are the wave's final re-bless)
- source of truth: kyle-design-directions.md §3 silhouettes + design-
  audit.html Q1 ranked fix "Silhouette minimalism" + tools/gen_sprites.py
