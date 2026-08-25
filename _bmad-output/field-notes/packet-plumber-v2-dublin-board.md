# packet-plumber-v2-dublin-board (2026-08-23)

- The dublin.json OSM rings are SELF-INTERSECTING (pinch/retrace — all 358
  rings fail the simple-polygon test): ear clipping silently drops them;
  the even-odd point-in-polygon cell raster (1 cell/world px, span-filled
  like map_draw) is the ONLY fill that matches PIL's blessed gallery.
- `make([dynamic]T, n, cap)` makes LENGTH n (zeros) — the index-ring bug
  that silently zeroed an entire triangulation; 0-length+cap is the append
  pattern. The temp-arena free_all also ate a test board mid-run (default
  allocator for anything a record_run outlives).
- Board geometry reality: 719 snapped street tiles at 1-in-6 (sub-tile
  raw dots kept for the render); district Voronoi cells are smaller than
  the estate radius — 63% of tiles have zero SAME-DISTRICT attach-ring
  neighbors, so district-scoped attaches stall; the global street ring +
  ring-has-room eligibility is the working interplay (documented in
  growth.odin).
