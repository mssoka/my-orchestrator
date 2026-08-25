# packet-plumber-v2-dublin-map-beautify (2026-08-24)

- The IRISH SEA root cause: OSM never maps the open sea as a polygon in the
  Dublin area — the coastline ways are OPEN lines (they can't close_ring),
  and no natural=water sea relation exists in the extract. The fix is
  bake-time construction: clip the coastline to the bbox (it crosses the
  bbox's N/S edges — Dún Laoghaire south, Howth north), unary_union (noding)
  with the bbox boundary, polygonize, take the face containing a pinned sea
  seed. NAMING TRAP: a module-level `def polygonize()` SHADOWS the shapely
  import of the same name — build_sea silently called the ring helper and
  returned nothing for a full round (the bake's --verify PASSED because it
  compared the same buggy output twice!). Also: a seed ON the bbox edge is
  `touches`, never `contains` — keep the seed inside the bbox.
- The user's red speckle was NOT landuse=residential — it was the 224k
  building-centroid spawn candidates rendered as house_bodies[0] (red) dots.
  The fix (mock-gate amendments): street-aligned BLOCKS baked per candidate
  (nearest street segment via shapely STRtree — deterministic, ties break by
  input order; the asset's --verify proves byte-identical re-bakes).
- PIL does NOT alpha-blend on draw — RGBA pixels are stored raw; composite
  manually before pixel-scanning mock renders (a scan that skips this reads
  raw-alpha garbage and lies).
- KYLE mock-gate iterations: (1) saturated 4-color blocks + the residential
  street web + the 18% grid = "GIS export"; (2) muted 2-tone blocks + locals
  faded to alpha 40 + no grid + arterials up = crop PASS "game map", overview
  near-pass ("more abstraction"). The overview/crop LOD (block alpha 40 vs
  120) was needed — same data, zoom-aware wash.
- Lavish asset paths: the HTML at .lavish/<name>.html must reference images
  as <dir>/img/... — the session serves /artifact/<id>/<rel>; a bare img/…
  path fails as 8 fatal artifact-asset-unavailable failures (the poll returns
  them, not user feedback — repair + re-poll).
- Blender (5.2) flat-color render trap: Principled BSDF "Emission" still
  receives the WORLD's ambient light on its diffuse term — a flat paper color
  renders blown-out white. Use a pure ShaderNodeEmission node (no diffuse
  term at all) for unlit map layers; convert palette hex sRGB->linear
  explicitly and keep view_transform='Standard' for hex-exact PNGs. Also:
  bpy materials assigned sRGB values directly render +50% brighter — the
  double conversion bites silently.
- Odin nested procs do NOT capture the enclosing scope — pass the struct
  pointer as an explicit parameter (the seg-grid builder bit once).
- The mock gate evolved the design 7 rounds in one lavish session (fabric
  blocks -> Blender low-poly base -> topology-on-the-map -> zoom LOD model);
  the user APPROVED from the gallery with three final rulings (sea ~15%, no
  grid, roads must connect). The committed look = the Blender-baked underlay
  texture (assets/maps/dublin_underlay.png, 4160x3120, timestamp chunks
  stripped for byte-stability) + the game's own nodes as street-aligned
  blocks (dublin_node_block_draw). The LOD zoom bands + cluster spawn
  director are flagged follow-ups.
