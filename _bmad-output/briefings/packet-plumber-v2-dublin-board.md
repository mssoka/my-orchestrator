# packet-plumber-v2-dublin-board

## Task

Stage 1 of the real-maps arc: wire the baked Dublin cross-section
(data/maps/dublin.json, merged in #90) INTO the game as the board.
User: "when do we get the dublin map? not in local v2." The spike
shipped look-only; this ships the city. Per user rulings (2026-08-23):
curated Dublin cross-section + streets-constrain-pipes — THIS job is
the board + spawns; streets-constrain-pipes is stage 2 (separate).

## Scope

1. **Board underlay**: render dublin.json — water (Liffey, bay,
   canals), parks (Phoenix Park), coastline, street skeleton — in the
   game's paper-map aesthetic (match the #90 gallery the user blessed;
   palette tokens, IBM Plex labels for districts). The board REPLACES
   the procedural terrain when the map source = dublin.
2. **Map source = first-class determinism input**: named tunable
   (map: dublin | procedural). Demos/replays PIN the map id — the map
   is part of the run state, hashed like a seed (LOG_VERSION-safe:
   old replays on procedural still run; new runs default dublin).
3. **Spawn anchoring**: growth SEED/ATTACH draws from dublin.json's
   street-adjacent spawn candidates at the 1-in-6 density (user's
   blessed level). Districts become the estate anchors
   (growth_groups interplay: cluster radius/caps apply WITHIN
   districts; document the exact interplay).
4. **Camera fit**: the map.* design-grid world sizes to the Dublin
   board; zoom/pullback (#89) works over it; minimap stays.
5. **KYLE visual gate**: the board must match the blessed #90 gallery
   (KYLE grades a live capture vs the gallery previews — side-by-side
   in the PR body).

## Rules (hard)

1. Streets do NOT yet constrain pipes — existing placement rules
   unchanged (stage 2). Free drawing over the real map.
2. Full golden re-bless EXPECTED (the board legitimately changed) —
   cause-documented; determinism suite green on both map sources
   (dual-run: procedural pins old goldens, dublin re-blesses).
3. E31 packing floors + placement rules still apply (spawn candidates
   respect terminal_min_sep_tiles; document conflicts if a candidate
   violates — filter at bake-load, never place illegally).
4. The extract pipeline is untouched (tools/osm_extract.py stable).
5. IP/ODbL attribution renders in-game (about/credits line or map
   corner — "© OpenStreetMap contributors").

## Acceptance

- `odin run app` boots Dublin: terrain, districts labeled, spawns on
  real streets at 1-in-6, estates clustering per district.
- Procedural map still runs (tunable flip); old demos/replays pin and
  replay byte-identical on procedural.
- KYLE gate: live board vs blessed gallery — side-by-side PR body.
- Determinism: T1/T2/replay green on BOTH map sources; dublin goldens
  re-blessed cause-documented.
- pr_review: 1.

## Skills policy

bmad-quick-dev; KYLE for the visual gate.

## Model policy

deepseek-v4-flash, --thinking max. KYLE: glm-4.6v (remote; local
fallback lmstudio/zai-org/glm-4.6v-flash).

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-dublin-board
- base: v2 (fresh head — post-#92 if merged, else current)
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- stage 2 (streets-constrain-pipes) NOT in scope — follow-up job
