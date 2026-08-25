# The Dublin board (stage 1 of the real-maps arc)

The baked Dublin cross-section (`data/maps/dublin.json`, merged in #90) is
now the game board. The user asked "when do we get the dublin map? not in
local v2" — this ships the city: the board underlay, the map source as a
first-class determinism input, and growth spawns anchored to real streets.
Streets do NOT constrain pipes yet (stage 2, follow-up).

## The KYLE gate (the #90 ruling's visual bar)

The live board vs the blessed gallery — graded side-by-side by KYLE
(glm-4.6v), verdict quoted from the gate run:

> **PASS** — "The live game frame accurately matches the reference Dublin
> board layout with consistent streets, waterways, parks, and urban density.
> The ~18 growth-spawned terminal buildings are properly positioned on city
> streets rather than floating in empty areas. No visual artifacts are
> present."

![Live game frame vs the blessed gallery](docs/captures/dublin-board/game_vs_gallery.png)

![Live underlay vs the blessed gallery](docs/captures/dublin-board/underlay_vs_gallery.png)

![The ODbL attribution renders in the map corner](docs/captures/dublin-board/attribution.png)

## What shipped

**1. The board underlay** (`app/render/dublin.odin`) — replaces the
procedural noise map when the map source = dublin. The gallery's exact
draw order + tokens: canvas → terrain (water/coast/park) → grid (18%) →
streets (arterial heavier, local faint) → the 1-in-6 candidate dots →
district labels (IBM Plex, kind-priority + collision-avoided like the
gallery) → the ODbL credit (rule 5, bottom-left of the board).

The terrain is rasterized once per board into a per-world-px cell grid with
the **even-odd point-in-polygon rule — the SAME fill rule the gallery's
renderer (PIL) uses**. This matters: the OSM rings contain pinch/retrace
artifacts that make them self-intersecting (80/80 water rings fail the
simple-polygon test) — ear clipping silently drops them, even-odd fills
them exactly like the blessed previews. The © glyph renders from a
dedicated one-glyph font so the shared HUD atlas never changes.

**2. Map source = a named determinism input** (`core/map.odin`) —
`map: dublin | procedural` is run setup like the seed:
- serialized into the T1 hash **absent-when-procedural** (the zero value),
  so every legacy demo/replay stays byte-identical — LOG_VERSION-safe, the
  log format never changes;
- demos pin it: `map dublin` / `map procedural` in the `.dem` header
  (absent = procedural — every pre-board demo is unchanged);
- the app boots **dublin by default** ("new runs default dublin");
  `PP_MAP=procedural` flips the named tunable back.

**3. Spawn anchoring on real streets** (`core/growth.odin`) — growth
SEED/ATTACH draw from the board's street-adjacent tile pool at the 1-in-6
density (the user's blessed calm default): the stride-6 subsample, snapped
to the integer tile grid, deduped + grid-filtered **at bake-load** (rule 3
— the pool only ever contains legal tiles). The ATTACH family draws the
anchor's **street ring** (pool tiles within `[terminal_min_sep_tiles,
radius_tiles]` of a member — the exact ring the procedural compass draw
targets, expressed over the real streets; the strict-radius closure is
preserved: no strays). An estate is eligible only while its streets hold a
legally-placeable tile (E31 + connect span checked ahead) — a saturated
estate yields to the SEED family instead of stalling the window budget.
The E31 predicates themselves are unchanged — a pool tile is a candidate,
never a guaranteed placement; every spawn is rejection-sampled through the
same `growth_pos_valid` / `growth_connectable` gates.

**The exact growth_groups interplay (documented per the briefing):** the
estate (the derived cluster) forms on the streets the grid gives it —
cluster radius/caps apply within the estate, and the estate's seed district
labels it. The district assignment is label-anchored (nearest anchor); a
street crossing a district's Voronoi boundary keeps its houses together —
the streets are the geometry that binds an estate. Measured: every pool
tile has ≥1 attach-ring neighbor globally (0% stall); district-scoped pools
would starve 63% of tiles (the district Voronoi cells are smaller than the
estate radius at the 1-in-6 snap) — hence the global ring.

**4. Camera fit** — the board is 40×30 tiles == the balance design grid,
so the fit + zoom/pullback (#89) and the NOC rail (#92) work over it
untouched.

## Determinism (the dual-run)

| Source | Proof |
|---|---|
| procedural | **all 48 pre-board demos byte-identical on their old goldens** (T1 manifests + T2 pixels + replay gates) — the absent-when-0 map byte + the untouched procedural draw path |
| dublin | `demos/dublin_board.dem` — the new named golden: `map dublin`, era 3, growth on, 2 routers on core street tiles + a wide fiber; T1 manifest + T2 captures + replay gate blessed + green |

**Re-bless cause-documented:** only the NEW demo's goldens were blessed
(`goldens/dublin_board.*`). Zero existing goldens changed — the board is
presentation + the map byte is absent-when-0; the procedural path draws
zero rng differently. The dublin demo's 90s run grows 18 terminals on pool
tiles, with estates of 5 forming along streets (the derived cluster view
unions them at the radius).

## Verification

- `tools/ci-local.sh --mac` — **13/13 gates green** (lint, 240 core unit
  tests incl. the new board/loader/growth pins, builds, the full golden
  harness, palcheck, drift, preview, motion, PP_DEBUG, stats, input parity).
- The app boots: `app: map = dublin (data/maps/dublin.json, 720 spawn
  tiles at 1-in-6)`; `PP_MAP=procedural` → `app: map = procedural`.
- New unit pins: the 1-in-6 snap/dedupe/grid-filter contract, the dims
  fail-loud contract, dublin growth lands on the pool + stays within the
  estate radius + E31-valid.

## Decisions & rationale

- **Even-odd cell rasterization over vector triangulation** — the OSM
  rings are self-intersecting (pinch/retrace); ear clipping produced
  overlapping/wrong fills (triangulated area exceeded the polygon area 1.5–
  3.6×) and dropped rings outright. The cell grid is deterministic,
  immune, and pixel-exact at fit zoom (1 cell = 1 world px). Rejected
  alternatives: fan+centroid (boundary straddle errors at coarse rings),
  ring repair (general ring-splitting, high complexity).
- **Global street ring over district-scoped pools** — measured geometry:
  63% of pool tiles have zero same-district attach-ring neighbors (the
  Voronoi cells are smaller than the estate radius at the 1-in-6 snap), so
  a district-scoped draw stalls estates across most of the city. The
  global ring preserves the strict-radius closure while keeping estates
  where the streets allow. The district pools (per-district candidate
  ranges) remain in the board + pinned by tests — the data is there for a
  future district-scoped policy.
- **The board is NOT part of the log format** — the map id rides the T1
  state hash (absent-when-0) and the demo/run setup (the fixture
  precedent), not the action-log header: adding it to the header would
  either break old-log parsing or need a LOG_VERSION bump that rejects
  them. "Old replays on procedural still run" is satisfied by construction.
- **The app default is dublin, the demo default is procedural** — the
  user's ruling ("new runs default dublin") applies to interactive runs;
  the demo default must stay procedural or every legacy golden shifts.
- **One-glyph © font** — adding U+00A9 to the shared codepoint set moved
  the ⚠ AA pixels (2–9 px/frame) across 18 demos' goldens; the dedicated
  font is additive and zero-impact.
- **`dublin-shot` harness verb** — the KYLE-gate capture tool (fit +
  zoomed underlay frames); kept as a permanent verb (the PP_DEBUG verbs'
  pattern) so the gate is re-runnable.
- **bmad-build waiver (canon note):** per the standing ruling, the
  quick-dev flow ran self-contained (the bmad-build render fails on this
  install with `ambiguous config token implementation_artifacts`; the
  waiver is documented in the field notes).

## Out of scope (stage 2, follow-up)

- Streets do NOT constrain pipe placement yet — free drawing over the
  real map (existing placement rules unchanged).
- The extract pipeline (`tools/osm_extract.py`) is untouched.

