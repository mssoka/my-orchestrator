# Briefing — v2-3.5-node-placement (restore player node placement)

- **Job id:** `packet-plumber-v2-3.5-node-placement`
- **Repo:** packet-plumber · **Base:** `v2` · **Slug:** `v2-3.5-node-placement`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — minions. NOT kimi, NOT glm).
  Any mega-minion you spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow). No review swarm — small,
  well-specified port; rely on quick-dev's built-in review.
- **Perkins:** `pr_review: 0` (off by default — small change).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard at `/Users/moses/code/_bmad-output/field-notes/<job-id>.md` per standing
  orders. On in-review, run `ledger pr <job-id> <url>` (standing orders).

## Mission (user ruling 2026-08-12: "nodes spawn, but I need to be able to place routers")

Restore **player node placement** into v2 — port `Cmd_Place_Router` + the hardware tray +
placement mode from the prototype. The GDD's build/redesign loop presumes a player-designed
network; the prototype proved placement; the v2 vertical-slice fixture dropped it. Canon is
now **story 3.5** in `_bmad-output/planning-artifacts/sprints/stories-v2.md` (amended
2026-08-12, commit `9a5a35b` on v2) — implement that story. Also amended there: story 5.1
(**routers are NEVER director-spawned**; terminals spawn, the player places routers).

## Reference (the prototype code to port — exists in git history)

- `origin/odin-prototype` (same code on `origin/main`):
  - `core/command.odin` — `Cmd_Place_Router` struct (line ~72) + the surrounding command set
    (draw/upgrade/demolish/lane-weights/pipe-priority/junction-triage — port only what 3.5
    needs: the PLACE command; the rest are later stories).
  - `app/main.odin` — `placing` state (line ~36), tray chip handling (lines ~201–250:
    router chips arm placement mode, click the map to drop the router, click again / ESC /
    right-click cancels), `Cmd_Place_Router{...}` construction (~line 249).
  - `app/render/hud.odin` — tray rendering helpers (`tray_router_types`, `tray_chip_count`,
    `tray_chip_rect`).
- v2 today: `core/command.odin` has only 3 kinds (draw-pipe / demolish-pipe /
  demolish-node) — `app/main.odin` has drag-draw but no tray/placing mode.

## Scope (implement story 3.5 exactly)

1. **Command:** add `Cmd_Place_Router` (junction kind — basic/mid/high per the catalogs)
   to the v2 command set, wired through `Command_Bus.validate` → apply (edit fast-path,
   ODN-2) like the existing commands.
2. **Validation:** span + min-separation from existing nodes, no overlap, within the
   placement area; rejections return the existing `Edit_Error` style.
3. **Serialization / replay:** record placement in the action log — `LOG_VERSION` bump per
   the story-1.2 precedent (`core/serialize.odin` command-kind switch, log version 2 →
   3). Same seed + same commands → identical map `[E10]`. Old logs must be rejected cleanly
   like the 1.2→2 transition did.
4. **Tray UI:** port the hardware tray (link chips select draw tier — existing; router
   chips arm placement). Click map to drop; click again / ESC / right-click cancels.
   Placed routers connect via the existing drag-draw.
5. **Port limits:** after placement, junction port limits apply to connections (GDD: basic
   4 / mid 8 / high 16 — check whether the v2 catalogs already carry port counts; if the
   field is absent, wire the const in with the catalog default, do NOT invent a balance).
6. **Terminals:** never player-placed. Tray carries router chips only.
7. **Tests + goldens:** determinism test for placement; a golden of placing a router +
   drawing a pipe to it (T2). Existing goldens (ecmp/demolish/drift) must stay untouched —
   placement is additive; if any existing golden shifts, STOP and flag (do not re-bless
   without checking).

## Acceptance

- Running the app: tray renders, router chips arm placement, click drops a validated
  junction, ESC cancels, placed routers accept drag-drawn pipes.
- `Cmd_Place_Router` serializes + replays byte-identical (LOG_VERSION bump test).
- All existing suites green (core / demos / drift / lint); new placement tests green.
- No code changes outside placement + its tests/render; terminals never placable.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-3.5-node-placement
base: v2
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 0
```
