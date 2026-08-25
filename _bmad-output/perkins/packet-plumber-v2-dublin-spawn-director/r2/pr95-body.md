# The Dublin board restyle — the Blender low-poly underlay (mock-gate approved)

## What

The Dublin board reads as a Mini Motorways-style game map instead of a GIS export. The board background is now a **Blender-baked low-poly base map** (`assets/maps/dublin_underlay.png`, committed), and the game's terminals render as **street-aligned blocks**. Every styling decision was ruled by the user in a 7-round lavish mock gate (`.lavish/dublin-mock-gate.html`, APPROVED + three final rulings).

## The user's rulings this PR implements

| Ruling | Implementation |
|---|---|
| "ugly with all the red dots + the names… we just want the map" | Red spawn-dot speckle gone; district labels gone (the tiny ODbL attribution stays, rule 4) |
| "there is no irish sea in what was delivered" | `build_sea` constructs the sea at bake time — OSM never maps the open sea as a polygon (root cause); sea = the coastline ∪ bbox partition face, clipped to a coastal strip |
| The sea "taking half the map… maybe just 10%" → final: **~15%** | `SEA_STRIP_M = 1300` (pixel-verified 15.8% incl. the Liffey/bay/moats) |
| The tight city-core bbox is the approved path | `BBOX = (53.30, -6.32, 53.385, -6.08)` — the docklands/Temple Bar → Ballsbridge corridor, Phoenix Park west, the bay east |
| The Blender pivot: "generate an asset in blender… tailor it to suit the game" | `tools/blender_board/` bakes the underlay: flat emission layers in the game's paper palette, top-down ortho, 4160×3120 (4× world px) |
| "roads look jagged… match the rough shape, aesthetics first" | Chaikin corner-cut smoothing + DP 12m on the arterial skeleton |
| "roads look disjointed… they should link to each other" | `connect_roads` endpoint stitching — every dangling end within 0.55 tiles of another road links in |
| "just want to see land, sea, river and major road — buildings come from the game" | The underlay carries NO building fabric; the game's own nodes are the buildings |
| Amendment #2 (REQUIRED): terminals as street-aligned blocks | `dublin_node_block_draw`: the nearest street segment orients the block; type chip rides it; no street within 3 tiles → logged axis-aligned fallback (never a silent float) |
| Grid on the Dublin board: **drop** | `dublin_map_draw` draws no grid (the procedural map keeps its own) |

## The mock gate (the process)

Seven rounds in one lavish session, KYLE (glm-4.6v) judging every render: PIL fabric-block mock → Blender low-poly base → buildings clustered Rio-style → the access/distribution/core topology drawn on the map → the zoom model (zoomed IN = houses + last-mile web; zoomed OUT = neighborhoods as blobs + only the backbone; rich mesh + circle-marker endpoints). The user APPROVED from the gallery. Evidence: `docs/captures/dublin-map-mock/` (the Blender LOD renders + the live game captures).

**Flagged follow-ups (out of scope here):** the spawn-director "method to the chaos" (cluster-aware placement), the zoom-LOD render bands (buildings fade → blobs), the last-mile link draw.

## Architecture

- The game keeps the deterministic data pipeline: `tools/osm_extract.py` (cache-first Overpass → `data/maps/dublin.json`, byte-identical `--verify`) → the sim's spawn pool / districts / street segments. The render reads the **committed underlay texture** instead of rasterizing vectors per-pixel.
- Sim untouched: T1/replay hashes for every procedural demo are unchanged (49/49 green); `dublin_board` re-blessed with cause — the core-bbox re-extract changes the spawn pool by design (the user-approved path).
- The harness **refuses to capture** if the underlay fails to load (`Dublin_Underlay_Ready` — the fonts/sprites precedent; a golden must never bless the degraded street-only fallback). The app itself fails soft (street skeleton on canvas, playable).

## Decisions & rationale

1. **Baked texture vs. live vector render.** The vector rasterizer (even-odd per-pixel fill) is what read "GIS" — real geometry at game resolution looks like a map export. A baked Blender render gives the hand-crafted low-poly look the user approved, deterministically (the PNG is byte-stable: Blender's wall-clock tEXt chunks stripped post-render). Rejected: restyling the vector path (3 KYLE rounds proved the look couldn't get there); generating the texture at runtime (no benefit, adds Blender to the build).
2. **The sea as a coastal strip, not the full face.** The full partition face (to the bbox east edge) read as "half the map." The strip (`coast_union.buffer(SEA_STRIP_M) ∩ sea_face`) hugs the shore and keeps Bull Island's moat. Deterministic shapely ops on the pinned raw cache.
3. **`street_blocks` stays in dublin.json even though the game render doesn't consume it yet.** It's the bake-time record of every candidate's street frontage (nearest segment via STRtree, deterministic tie-break by input order) — the follow-up LOD/fabric passes read it. The loader ignores unknown keys (no core change).
4. **The street-segment grid lives in the view layer** (`dublin_seg_grid_build`, 1-tile cells over arterial+local segments): pure data prep from the already-parsed board, rebuilt on board change. Node orientation lookup is a 3×3 cell scan — no locks, no sim state, deterministic f32 math.
5. **Em-dash ban in string literals** — the lint gate caught one in a log line (mojibake risk). All new render strings are ASCII.
6. **Blender flat-color gotcha (for future bakers):** Principled BSDF "Emission" still receives world ambient on its diffuse term — flat colors blow out. Pure `ShaderNodeEmission` nodes + explicit sRGB→linear + `view_transform='Standard'` give hex-exact PNGs (probe-verified ±2).

## Verification

- `tools/osm_extract.py --verify`: byte-identical re-bake from cache (after every code change).
- 49/49 demos green post re-bless; input-parity 27 scenarios green; **all 13 local CI gates green** (`tools/ci-local.sh --mac`).
- KYLE gate (live captures vs the approved mock): **PASS** — baywide ("reads as the approved game map, sea present") + templebar zoom ("street-aligned blocks grounded, underlay crisp, game elements read").
- Pixel evidence: sea 15.8% of the zoom-out frame; zero dark text pixels on the board face (no labels).

ODbL: the attribution line renders bottom-left (rule 4); the asset's `attribution`/`license` fields unchanged.

