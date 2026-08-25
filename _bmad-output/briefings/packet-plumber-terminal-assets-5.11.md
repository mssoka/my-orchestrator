# Briefing — packet-plumber-terminal-assets-5.11 (new terminal shapes: small-biz + campus)

- **Job id:** `packet-plumber-terminal-assets-5.11`
- **Repo:** packet-plumber · **Base:** `v2` @ post-#64 merge head (HELD — Silas
  resolves the exact sha at release; see the hold note below) ·
  **Slug:** `terminal-assets-5.11`
- **HOLD (Silas):** do NOT dispatch on receipt. Release trigger = the
  `packet-plumber-v2-7.1-visual-juice` merge close-out (#64) — this job NEEDS
  7.1's sprite pipeline (headless Blender render + sheet + palcheck gate) on v2.
  Record the hold on the row. (5.11 the story is held behind THIS job's lavish
  approval — chain the two.)
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — mechanical
  Blender/render work; aesthetic verdicts are the USER's at the lavish gate, no
  native-vision dependency). Any mega-minion you spawn launches with the same
  model — name it explicitly at every spawn.
- **Skills policy:** `gds-quick-dev` (asset + pipeline extension work);
  **`lavish` is MANDATORY — present the rendered terminal set for the user's
  in-browser verdict BEFORE the PR** (iterate on annotations; PR only after an
  explicit approve). `project-context.md` for code conduct.
- **Perkins:** `pr_review: 1` (canon art surface). **Loop ruling (user,
  2026-08-17):** rounds run UNTIL APPROVED.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start;
  badge-out your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-terminal-assets-5.11 <url>` yourself.
- **Canon + machinery:** the approved top-down sprite language (7.1 lavish gate
  r4: two-tone roofs + contact shadow, literal buildings per the look-book);
  `art-renders/blend-sources/pp-scene-light-vista.blend` + `pp_lib.py`; the
  7.1 sprite pipeline (HEADLESS: `Blender --background --python ...` — the MCP
  addon path is DEAD, do not attempt it; the binary is
  `/Applications/Blender.app/Contents/MacOS/Blender`, not on PATH).
- **CI:** billing-blocked GH Actions — the LOCAL suite is ground truth;
  `tools/ci-local.sh` (10 gates incl. palcheck) must pass with the new sprites.

## Mission — create the 5.11 terminal shapes in the canon Blender file

**The goal:** 5.11 (diverse terminal types) needs **distinct shapes** for its
roster — the analogues of residential: **small-biz (office) and campus** — each
readable WITHOUT color `[E9.1]`, capacity-scaled like the canon shape families
(campus footprint > small-biz > residential; distinct silhouettes, not recolors).
This job produces the ART: blend models + rendered sprites, lavishly approved.

**Hard requirements:**

1. **Re-open the canon blend** (`pp-scene-light-vista.blend` + `pp_lib.py`) and
   model small-biz + campus in the approved top-down two-tone-roof language.
   Respect the existing families: buildings stay literal + geometric
   (look-book §1; MM flat minimalism — no 3D materials/bevels/bloom in the
   sprite output); the shapes must read at gameplay zoom.
2. **Render via the 7.1 pipeline** (headless CLI) into the existing
   sprite-sheet format + manifest; extend the sheet/manifest as DATA. The
   palcheck gate must stay green (sprites use the canon palette tokens).
3. **LAVISH GATE (before the PR):** present the new terminals — ideally in
   context: the trio (residential/small-biz/campus) side by side at gameplay
   zoom + one small composed map moment — via lavish. The user picks/annotates;
   iterate the models until an explicit approve. HARD GATE: no PR before it.
4. **Provenance:** the blend file gains the new models with clean naming; note
   the additions in the PR. NO game-code changes beyond the sheet/manifest data
   (the draw wiring, Terminal_Role enum, caps, and growth integration belong to
   story 5.11 — do NOT do them here).

**Acceptance:**

1. Lavish verdict recorded verbatim in the PR body (the approved set is what
   shipped).
2. Sprites in the sheet, manifest extended, `tools/ci-local.sh` green
   (10/10 incl. palcheck).
3. PR body: the shape rationale per type (silhouette → role readability), the
   pipeline commands used, the canonical citations (look-book sections + the
   7.1 gate verdict).
4. The 5.11 consumer note: what 5.11 must wire (enum, draw, caps).

**Scope guard:** art assets for the 5.11 roster ONLY (small-biz + campus). No
game mechanics, no 5.11 code (enum/caps/growth/draw), no re-render of existing
canon, no other asset types. Modest, precise, done.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: terminal-assets-5.11
base: v2
model: deepseek/deepseek-v4-flash
pr_review: 1
```
