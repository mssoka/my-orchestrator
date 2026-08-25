# packet-plumber-v2-dublin-map-spike

## Task

Prove the real-city board: extract a Dublin cross-section from
OpenStreetMap, bake it as a game asset, and render it as the board
underlay for a lavish user review. User rulings (2026-08-23): (a)
CURATED Dublin cross-section (not a general importer) + (a) streets
will constrain pipes (MM-soul) — but THIS spike touches NO gameplay.
Deliverable = the look, judged by the user before any game surgery.

## The pipeline (user-approved shape)

1. **Extract**: query OSM for the cross-section bbox — Dublin, roughly
   lat 53.28–53.44, lon -6.45 to -6.03 (Dublin Airport N, Dún
   Laoghaire S, Blanchardstown W, Howth E — the user's reference
   screenshot area). Sources: Overpass API or a Geofabrik Ireland
   extract filtered down. Tool: **osmnx** (Python) for the street
   graph + layers.
2. **Layers**: terrain (the Liffey, Dublin Bay/coastline, Royal Canal,
   Phoenix Park + major parks), street graph SIMPLIFIED (arterials:
   motorway/primary/secondary/tertiary — merge tiny residential
   streets), building/spawn candidates (building centroids), district
   names (place=suburb: Rathmines, Ballsbridge, Finglas, Cabra…).
3. **Project**: lat/lon → UTM 29N meters → game tile units, fitted to
   the board size (map.* in balance.json).
4. **Bake**: `tools/osm_extract.py` (committed, deterministic,
   offline-rerunnable) → `data/maps/dublin.json` (terrain polygons,
   street edges, spawn points, districts). The game never touches the
   network at runtime. Include ODbL attribution in the asset
   ("© OpenStreetMap contributors").
5. **Render the look**: produce board-underlay previews in the game's
   paper-map aesthetic (palette from the settled look — paper-dominant,
   warm tint). A standalone preview render is acceptable for the spike
   (in-game wiring is the follow-up IF approved) — but the preview
   must use the game's palette/typography (IBM Plex) so the review is
   honest.

## Density knob (the user's anti-noise ask)

Render the spawn-candidate overlay at **3 density levels** (e.g. every
building, ~1 in 3, ~1 in 6) — the user picks the calm level at the
gallery. Districts labeled.

## Rules (hard)

1. NO gameplay/sim changes; NO golden changes; new files only
   (tools/osm_extract.py, data/maps/dublin.json, preview renders).
2. Deterministic bake: same query/bbox → same dublin.json (pin the
   extract inputs; note OSM drift — the asset is the snapshot).
3. ODbL attribution inside the asset + a credits note.
4. KYLE grades the previews (remote glm-4.6v; local fallback): does
   the cross-section read like the game? Districts legible? Street
   density right for pipe-drawing?
5. **Lavish gallery to the user BEFORE any follow-up is even
   proposed** — underlay at a few zoom crops (bay-wide, Temple Bar
   close-up, a residential district), 3 density levels, KYLE's grades.
   The user's eye is the gate for the whole arc.

## Acceptance

- `tools/osm_extract.py` + `data/maps/dublin.json` committed; bake is
  deterministic.
- Preview renders (bay-wide + 2 close-ups × 3 densities) in the lavish
  gallery with KYLE verdicts.
- Zero diff to existing sim/render/goldens.
- pr_review: 1 (Perkins on the pipeline + asset).

## Skills policy

bmad-quick-dev; lavish for the gallery; KYLE for visual grades.

## Model policy

deepseek-v4-flash, --thinking max. KYLE: glm-4.6v (remote; local
fallback lmstudio/zai-org/glm-4.6v-flash).

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-dublin-map-spike
- base: v2 (fresh head)
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- parallel-safe: new files only; merge anytime after Perkins
