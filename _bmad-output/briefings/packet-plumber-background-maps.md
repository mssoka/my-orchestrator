# Briefing — packet-plumber-background-maps (canon D9: procedural land/ocean/parks)

- **Job id:** `packet-plumber-background-maps`
- **Repo:** packet-plumber · **Base:** `v2` @ af05b1a (post-#65 head; Silas resolves
  the exact sha at dispatch) · **Slug:** `background-maps`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — mechanical
  render work; the aesthetic verdict is the USER's at the lavish gate, no
  native-vision dependency). Any mega-minion you spawn launches with the same
  model — name it explicitly at every spawn.
- **Skills policy:** `gds-quick-dev` (view + procedural-gen work);
  **`lavish` is MANDATORY — present the map style for the user's in-browser
  verdict BEFORE the PR** (2–3 candidate map seeds; iterate on annotations).
  `project-context.md` for code conduct.
- **Perkins:** `pr_review: 1` (canon art surface + every-frame T2 churn).
  **Loop ruling (user, 2026-08-17):** rounds run UNTIL APPROVED.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start;
  badge-out your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-background-maps <url>` yourself.
- **CANON (this is D9, not new design):** look-book-v1.md §"Canvas / map" +
  decision D9 — "a procedural land/ocean map (noise-driven landmasses with
  coastlines + green park blobs over soft-blue water), MM-style — not a flat
  void", user verdict 2026-08-08 ("a map background, just like Mini Motorways").
  The vista render `renders/01b-vista-light.png` is the reference. Palette per
  the look-book tokens (cream land `#E8DDC2` family, muted water, soft parks) —
  MM daytime, flat-2D minimalism (no textures, no gradients on terrain edges
  beyond soft two-tone).
- **Lane note (sibling in flight):** 5.11-types (core lane, p21R) carries its
  own T2 golden additions; your map changes EVERY T2 frame → full deliberate
  re-bless. First-lander documents impact; if 5.11 lands first, your re-bless
  lands on its merged tree (4.3 discipline both ways).
- **CI:** billing-blocked GH Actions — the LOCAL suite is ground truth;
  `tools/ci-local.sh` (10 gates incl. palcheck) must pass.

## Mission — implement canon D9 (the world under the network)

**The goal:** the play surface stops being a flat void and becomes a procedural
**land/ocean/parks map** — noise-driven landmasses with coastlines, green park
blobs, soft-blue water — MM-style, in OUR light-canvas palette. Terminals,
pipes, and packets read ON the world, not floating in cream.

**Hard requirements:**

1. **Deterministic, seeded, presentation-only.** The map generates from the
   run seed (same seed → identical map, byte-stable); it lives in the View
   layer, perturbs NOTHING in the sim; **no snapshot fields, no LOG_VERSION
   bump, replay byte-identical `[E10]`**; T1 goldens unshifted (state-hash
   ignores the map — it is derived presentation).
2. **The generator.** Noise-driven landmasses + coastlines + park blobs over
   water, tuned for the game's grid scale (the map must not fight readability:
   terrain stays LOW-contrast under pipes/nodes; water/parks are soft, never
   saturated). Terrain does NOT gate gameplay in v1 — placement stays on the
   existing grid rules (terrain-aware growth is a named follow-up, out of
   scope).
3. **Render order + tokens.** Map under everything; the snap grid stays subtle
   per canon; palette from the look-book tokens (extend the palette table with
   water/park hexes — palcheck gate must cover them).
4. **LAVISH GATE (before the PR):** present 2–3 candidate map seeds (same
   gameplay moment rendered on each) side-by-side against the vista reference —
   coastline style, water/park density + color balance, grid interaction. The
   user picks/annotates; iterate until an explicit approve. HARD GATE.
5. **Goldens.** Full T2 re-bless — deliberate, cause-documented (the map
   changes every frame); T1 + replay byte-identical (prove it in the PR).
6. **Canon fold:** add the story card (§Story 7.4 — background maps, slice 7
   view lane) + the decision-log note (D9 scheduled + shipped) in the same PR.

**Acceptance:**

1. Lavish verdict recorded verbatim in the PR body (the approved map style is
   what shipped).
2. Same-seed map identity pinned (a determinism test); replay byte-identical;
   T1 unshifted; `tools/ci-local.sh` 10/10.
3. PR body: the generator design (noise, seed derivation), the palette
   extension, the re-bless cause chain, citations (look-book D9 + §palette).

**Scope guard:** the background map ONLY. No terrain-aware placement (follow-up),
no new terminals/routers, no gameplay effect, no minimap, no camera changes. If
a canon gap appears, FLAG it — never redesign canon.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: background-maps
base: v2
model: deepseek/deepseek-v4-flash
pr_review: 1
```
