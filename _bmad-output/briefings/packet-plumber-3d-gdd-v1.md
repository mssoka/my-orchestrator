# Briefing: packet-plumber-3d-gdd-v1

Read the standing orders first: `/Users/moses/code/docs/orchestration-playbook.md`
section 'Minion standing orders'. This briefing is your task spec.

## Task

Birth the **packet-plumber-3d** repo and author its planning spine: **GDD +
development epics + decision log**, following the same build structure as
PP-Odin (packet-plumber), adapted to the new tiny-planet full-3D vision.

## The vision (user rulings, 2026-09-04 — verbatim)

- "The world would be like a tiny planet with houses etc and we rotate the
  planet and connect the network — and routers — rather than it being 2D.
  Should be full 3D."
- "The game would still be called Packet Plumber."
- "Let's do Godot then." (engine ruling: **Godot 4**, over Unreal — Gru's
  comparison accepted; UE lost the 08-20 slice audition on out-of-box look,
  and text `.tscn` scenes keep the world agent-reviewable.)
- "We follow the same build and epics as PP-odin, with vertical slicing so
  we can test. You can use that as reference."

## What this job is / is not

- **IS:** repo birth + docs spine (GDD, epics, decision log) — a DOCS
  deliverable. Lavish review BEFORE the PR opens (standing policy).
- **IS NOT:** implementation. No game code in this job beyond the repo
  scaffold. Slice 1 (tiny planet + orbit camera + connect verb) is the next
  dispatch, briefed from YOUR epics.md.

## Acceptance

1. **Repo born:** git repo at `/Users/moses/code/packet-plumber-3d` (Silas
   pre-created the dir + `git init -b main`; you take it from there).
   Initial scaffold commit to `main`: README.md (game name: Packet Plumber;
   Godot 4 project; link to the GDD), `.gitignore` matching PP's pattern
   (Godot ignores + `.lavish/` + `_bmad/` ignored, `_bmad-output` TRACKED).
   Private GitHub remote under the `solarity-services` org
   (`gh repo create solarity-services/Packet-Plumber-3D --private`); if org
   perms block, create under the authed user and flag it in the PR.
2. **`_bmad` scaffold:** copy `_bmad/` from
   `/Users/moses/code/packet-plumber/_bmad/` (it is gitignored there — copy,
   don't link) and update `config.toml` `project_name = "packet-plumber-3d"`.
3. **GDD** at `_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-3d-<yyyy-mm-dd>/gdd.md`:
   adapt PP's GDD to the tiny-planet 3D vision — pillars; the connect verb
   (drag building→building on a curved surface); the rotate-the-planet
   camera grammar (drag-orbit + scroll zoom, from the reference video);
   routers/nodes in 3D; art direction (chunky flat-shaded low-poly, bright
   palette — the little-planet look); carried-over doctrines from PP where
   they survive the dimension change (pause-and-plan, QoS/priority as a
   design pillar, fair-failure/crisis telegraphing, accessibility,
   determinism where it applies).
4. **Epics** at `.../epics.md` — same shape as PP's: traceability matrix +
   per-epic stories + build staging. **Vertical slices, playable from E1.**
   E1 = the slice-1 prototype: tiny planet world + orbit camera + connect
   verb (no sim, no character). Sequence toward an earliest fun-test gate,
   carried over from PP's doctrine (MVP = the core epics to the gate;
   production quality from the start; no-rebuild doctrine — this repo IS
   the full-game build, there is no later rewrite).
5. **Decision log** at `.../decision-log.md` — record: Godot-over-UE ruling
   (with the evidence above), new-repo ruling (PP-Odin 2D canon untouched),
   brand ruling (the game is Packet Plumber), look-reference IP guardrail
   (little-planet video = inspiration for the LOOK; we do not clone its
   assets, code, or layout), and anything you decide load-bearing.
6. **Lavish review loop BEFORE the PR** (standing DOCS policy): build the
   GDD as a lavish session, foreground-poll for the user's in-page
   annotations, apply them, THEN open the PR.
7. **PR** to `main` with a "Decisions & rationale" section; self-report
   ledger transitions; self-notify checklist gate with pasted `shown:true`.

## Reference pack (READ-ONLY)

- **PP GDD + epics (structural + doctrine reference):**
  `/Users/moses/code/packet-plumber/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/`
  (`gdd.md`, `epics.md`, `decision-log.md`) — mirror the shape; adapt, don't
  copy wholesale. The 2D game's mechanics are your inheritance list: decide
  per mechanic whether it survives the dimension change and say so.
- **Look reference (IP-sensitive — cite, never copy into any tree):**
  `/Users/moses/code/_local-refs/little-planet-ref/` — the user's reference
  video (`3d little planet - HD 720p.mov`, "Little Planet — A Pocket
  Adventure" dev demo) + 6 extracted frames (`f0` globe with biomes +
  dotted path, `f2` farm scene camera grammar, `f4` ocean/swim). These are
  the LOOK target for the GDD's art direction section. You may attach the
  PNGs directly (your model is natively multimodal).

## Environment / tooling

- Godot **4.7.1** at `/opt/homebrew/bin/godot` (informational for this docs
  job; implementation slices start next dispatch).
- **Godot MCP is configured user-globally** (`~/.config/mcp/mcp.json`,
  `npx -y gopeak`, 34 tools: scene-create, node-add, script-create,
  editor-run, lsp-diagnostics, …) — every pi pane in any cwd has it. Note
  it in the GDD's tooling section as the build/verification surface for the
  implementation belt.

## Model policy

Minion: **`zai-coding-cn/glm-5.3-flash`** (ops tier; natively multimodal —
read the reference frames inline, no vision detour). Mega-minions, if you
spawn any: same model, name their skills explicitly.

## Skills policy

- Workflow: **`gds-gdd`** (primary — GDD create flow) +
  **`gds-create-epics-and-stories`** (epics.md + story breakdown).
- **`lavish`** for the pre-PR review loop (Acceptance 6).

## Perkins

`pr_review=0` — docs/lavish deliverable; the lavish loop is the review.

## Dispatch parameters

```
job_id:    packet-plumber-3d-gdd-v1
repo:      packet-plumber-3d
repo_root: /Users/moses/code/packet-plumber-3d   (NEW — does not exist yet)
slug:      gdd-v1
base:      main
model:     zai-coding-cn/glm-5.3-flash
pr_review: 0
new_repo:  true — Silas: mkdir -p + git init -b main (mechanical birth, NO
           content), then IN-REPO dispatch (no worktree, no origin fetch):
           tab create --cwd <repo_root>, label packet-plumber-3d-gdd-v1,
           launch `pi --model zai-coding-cn/glm-5.3-flash --thinking max`,
           standard handover + delivery verification.
```
