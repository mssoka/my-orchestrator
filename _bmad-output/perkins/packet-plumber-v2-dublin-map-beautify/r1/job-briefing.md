# packet-plumber-v2-dublin-map-beautify

## Task

Style the Dublin board to the Mini Motorways grammar. User verdict on
#93's first look (2026-08-24, with five MM reference screenshots: Rio
night/day, Zürich, İstanbul, LA): "ugly with all the red dots, and the
names of the locations — we just want the map... can we get something
like that? also there is no irish sea in what was delivered." The
current render is a faithful GIS export; it must become a GAME map.

## The MM grammar (from the user's reference screenshots — ground truth)

1. **KILL the red/salmon urban speckle** — the `landuse=residential`
   polygons rasterizing as thousands of red dots. Either drop the
   urban landuse layer entirely or collapse it into ONE soft muted
   tint at very low contrast (no texture). MM shows no urban shading
   at all — clean base only.
2. **KILL the district-name labels** — no location text on the board.
   (The end-screen city caption pattern is fine; live-board labels are
   not.) Keep ODbL attribution (tiny, in a corner/credits).
3. **FIX THE IRISH SEA** — the eastern board must be WATER (currently
   beige). Root-cause the gap (coastline polygon not rendering? bbox
   clipped the sea? water-vs-coastline tag coverage in the extract?)
   and render the sea as the big flat body it is. Verify the Liffey,
   the bay, and the canals also read.
4. **Water = big flat bodies** (MM's navy/soft-blue), land = clean
   paper base, parks = soft green patches — match the game's paper
   palette tokens; no texture noise anywhere.
5. **Streets = thin clean lines** (the arterials we have), kept subtle
   under the nodes/pipes — MM's roads are quiet; ours must not fight
   the game elements.
6. Spawn candidates/district data unchanged (gameplay semantics pin) —
   this is a RENDER/DATA-STYLING change, not a sim change.

## Rules (hard)

1. Sim untouched: T1/T2/replay hash-equal; goldens re-bless ONLY the
   board-underlay class (cause-documented: map restyle).
2. The fix must be in the RENDER + bake styling (tools/osm_extract.py
   layer selection may change; if the SEA requires a re-extract, run
   it — dublin.json versioned, determinism preserved).
3. KYLE gate: side-by-side the new board vs the user's MM references —
   the verdict must be "reads as a game map, not a GIS export" and
   the sea visibly present. PR body carries the comparison.
4. District labels gone EXCEPT the attribution line (ODbL) — tiny.
5. Deliverables run at BOTH the current default zoom and a zoomed-in
   crop (the style must hold at zoom levels, per #89).

## Acceptance

- No urban speckle; no district labels (attribution excepted); the
  IRISH SEA renders as water; water/parks/streets read clean at all
  zooms.
- KYLE side-by-side vs MM refs — PASS.
- T1/T2/replay hash-equal; underlay goldens re-blessed with cause.
- pr_review: 1.

## Skills policy

bmad-quick-dev; KYLE for the visual gate.

## Model policy

deepseek-v4-flash, --thinking max. KYLE: glm-4.6v (remote; local
fallback lmstudio/zai-org/glm-4.6v-flash).

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-dublin-map-beautify
- base: v2 (fresh head)
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- references: the user's 5 MM screenshots live on the Desktop
  (Screenshot 2026-08-24 at 01.25.56 / 01.25.38 / 01.25.06 / 01.24.17
  / 01.22.39.png) + the delivered-ugly screenshot (01.19.18.png);
  copy them into _local-refs/mm/ for KYLE if easier (IP guardrail:
  reference only, never into the repo)
