# Briefing: packet-plumber-3d-router-family

Read the standing orders first: `/Users/moses/code/docs/orchestration-playbook.md`
section 'Minion standing orders'. This briefing is your task spec.

## Task

**The router family**: replace/augment the junction visuals (currently the
rounded-window pick) with a **family of fun, cool router looks** built from
Blender-MCP-hunted assets **modified in Blender**. User's words (verbatim):
"right now we are using a rounded window as a router. can you find
something via blender mcp that we then modify in blender? should look fun
and cool esp for the different routers types we might have."

## What to build

1. **Hunt** via the Blender MCP (`blender_search_sketchfab_models`,
   `blender_get_sketchfab_model_preview`). Gru's probe already found stock:
   Server Rack and Console v3 (639 tris, CC-BY, UID 24ebe6f197c44e0a93f4010045c4a997),
   Network Server Rack (1.1k, CC-BY, UID 3b15fb8779274844b54e63a40194d450),
   Server V2 +console (1.1k, CC-BY, UID f24594ece9634cec9c1210c041838371),
   satellite dishes (e.g. 3.1k tris, CC-BY, UID 929f056abe02416da19d7b1aa805d235).
   Hunt MORE (antenna towers, utility cabinets, stylized computers) — CC0/CC-BY
   ONLY, NC banned.
2. **Modify in Blender** (the shared-session craft): strip, retint, recompose
   into **one round-shape-language family** (the user's pick language is
   canon: round devices). Produce **3 variants** reading as tiers for the
   router TYPES the game will grow (e.g. edge junction → hub → core) — fun,
   chunky, bright, little-planet toy vibe. Reference frames:
   `/Users/moses/code/_local-refs/little-planet-ref/` (cite only).
3. **Integrate**: junction staging uses the family (deterministic per-site
   selection from the seed — same seed, same world); cable/link visuals
   unchanged; the rounded-window pick stays available but is no longer the
   default junction look.
4. **Fold U4 (user ruled YES tonight)**: `.gitignore` the Godot side-file
   churn in this same PR — ignore `*.import` rewrites churn per policy:
   ignore `.godot/` (already), and untrack/ignore the `*.uid` + asset
   `*.import` side-files that play sessions rewrite (design the ignore set
   so tracked game assets still import cleanly on fresh clones — Godot
   regenerates side-files on import; if any side-file MUST be tracked for
   that, say so in the PR with evidence). State the policy in the PR body.

## Blender session guardrails (STANDING — the running Blender is the user's)

- NEVER `open_mainfile`, NEVER save/write any .blend, NEVER touch existing
  objects/scenes. Imports + edits + glTF export + DELETE imported objects —
  zero residue, zero saves.
- Craft gotchas (burned-in lessons): sanitize ID names to `[A-Za-z0-9_]`
  (Blender 5.2 stoi crash on `-`/`.`); measure world bbox after import and
  scale by measurement (imports lie); origin-normalize before export
  (bbox center 0, base z 0 — instances draw at library transforms
  otherwise); downscale review renders before reading them into context.

## Acceptance

1. 3 router-family variants in `assets/junctions/` (glTF + attribution
   entries in `ATTRIBUTION.md` — original authors credited even after
   modification, CC-BY).
2. Deterministic staging (replay byte-identity contract holds; 195+ checks
   green; view purity — art swap never shifts sim state).
3. Look evidence: captures per variant (editor preview + runtime) vs the
   reference frames; you are natively multimodal — verify the LOOK yourself
   before claiming it. `LOOK-PARITY.md` updated.
4. U4 policy landed (gitignore + PR-body rationale).
5. `godot --headless --import` clean; LSP diagnostics clean; suite green.

## Model policy

Minion: **`zai-coding-cn/glm-5.3-flash`**. Mega-minions: same, skills named.

## Skills policy

Workflow: **`gds-quick-dev`**. No lavish (code/assets deliverable —
captures carry the look; the user rules at their next editor look).

## Perkins

`pr_review=1` — canon-surface visual + staging code. Loop-until-APPROVED.

## Dispatch parameters

```
job_id:    packet-plumber-3d-router-family
repo:      packet-plumber-3d
repo_root: /Users/moses/code/packet-plumber-3d
slug:      router-family
base:      main
model:     zai-coding-cn/glm-5.3-flash
pr_review: 1
notes:     Worktree from origin/main. _bmad symlink bootstrap. PARALLEL
           LANES: gdd-amend-levels (docs) — disjoint files.
```
