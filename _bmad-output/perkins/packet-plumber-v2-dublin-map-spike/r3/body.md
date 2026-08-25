## 🤖 Perkins automated review — round 3
**Job:** packet-plumber-v2-dublin-map-spike · **Reviewed sha:** 6be06dc · **Reviewers:** 7/7 completed
**Verification:** 39/39 findings confirmed against the code — 0 discarded as false-positive

Round history: r1 @28c6d5a and r2 @bd394fc were both swept mid-flight (base moved twice). This round audits the true head. The three findings visible in r2's partials (grid-alpha cite, unclipped remark guard, cache atomicity) are all still present — carried here, not double-counted.

**Guard bars (the spike's hard contract) — all PASS, verified mechanically:**
- **New files only:** 13 new files; only `.gitignore`/`.memlog.md` modified; zero sim/render/golden paths; both `.gitignore` trailing blocks survived the rebase (ambience WAV + `.osm-cache`/`__pycache__`).
- **Deterministic bake:** `--verify` re-baked from the pinned cache (`889f0aab9df546cc`): byte-identical, 3,889,867 bytes.
- **ODbL:** `attribution` + `license` fields inside the asset + credits note.
- **No runtime network:** zero references to the asset/OSM in `app/`/`core/`; the asset declares snapshot semantics.

### Blockers (0)
None.

### Warnings (12)
1. **Overpass error guard checks XML `<remark>` only** — queries pin `[out:json]`, where errors are a top-level `"remark"` key; such responses pass, get cached, and the cache-first fetch never retries (a silently partial asset can commit). `tools/osm_extract.py:250` [security, edge]
2. **Relation members flattened into one LineString** — multipolygon waters fail `polygonize()` and drop silently. Root cause of #3. `tools/osm_extract.py:283` [blind, edge]
3. **Spec-named waters missing: Liffey quays (~4 km gap) + Royal Canal** — verified by point-in-polygon at O'Connell Bridge / Ha'penny / Chapelizod / Phibsborough / Cross Guns: all miss; the Royal Canal relation IS in the raw cache; only way-mapped docks survive. *The look was user-approved at the lavish gate with this asset — fix at the wiring job or record supersession; the gate is not reopened.* `data/maps/dublin.json` [acceptance]
4. **Dublin Bay renders canvas paper (no water polygon); Phoenix Park absent from the park layer** (no polygon covers its center — only "Phoenix Park Avenue" streets in cache). Same supersession note as #3. `tools/osm_extract.py:99` [acceptance]
5. **`GRID_ALPHA=46` (18%) cites "map.odin grid blend"; live canon is 9% in view.odin's LEFOU pass** — preview grid is 2× the game's. `tools/render_dublin_preview.py:33` [codebase]
6. **Preview base fills `palette.canvas`; map.odin's canon land layer is `palette.land`** (warm tint) — the "canon order" comment omits it. `tools/render_dublin_preview.py:91` [codebase]
7. **Board dims (40/30/26) hardcoded in both tools** instead of reading `data/balance.json map.*` — match today, silent-drift risk for the wiring surgery. [architecture, acceptance, tests]
8. **Asset lacks the fit origin (ox0/utm_top)** — every consumer re-implements the centered-fit math (renderer already does). `tools/osm_extract.py:352` [architecture, codebase]
9. **Non-atomic cache write + existence-only cache-hit check** — an interrupted fetch leaves a truncated permanent "cache hit". `tools/osm_extract.py:217` [blind, edge]
10. **Determinism contract has only the manual `--verify` self-check** — nothing wires it into CI/gates. [tests]
11. **Projection math has zero automated cross-check** (only the spawn bounds filter; today's manual cross-check passed). [tests]
12. **Advisory test gate: CONCERNS** — P0 (determinism self-check) present but unwired; P1 gaps at ~80%. [tests]

### Notes (18)
MIN_AREA comments 3–9× overstated (72 m actual vs ~220 m claimed) [blind, edge] · docstring omits `village` (13 in asset) [blind] · unused imports `io`/`shape` [blind, codebase] · dead `--bake` flag (`if args.bake or True:`) [blind, codebase] · `DP_TOL["coast"]` unused; coast layer is beaches [blind] · certifi CA failure swallowed by `except: pass` [blind] · missing palette key renders opaque black [blind] · determinism contract vs unpinned shapely/pyproj [blind] · `.osm-cache/` under the "# Python cache" heading [blind] · shapely/pyproj/certifi/Pillow undeclared (no manifest predated the diff either) [codebase] · fetch failover except-tuple misses gzip/decode errors [edge] · `--verify` without cache dies as raw FileNotFoundError (reproduced) [edge] · `fetched_utc` from cache mtimes — byte-identity is mtime-dependent [edge] · osmnx deviation documented in docstring [acceptance] · local street layer kept beyond arterials-only letter (visible in approved previews) [acceptance] · float→int tile seam undocumented for the future consumer [architecture] · 3.9 MB asset is a ~363× outlier vs `data/*.json` [architecture] · preview re-render stability untested [tests]

### Reviewer agreement
Eight multi-lens findings (highest confidence): the remark-guard, relation-flattening, cache-atomicity, MIN_AREA-comments, board-dims, fit-origin, unused-imports, and dead-flag findings were each independently reported by 2–3 lenses and all survived verification.

**Verdict:** READY TO MERGE

The spike's hard contract holds (new-files-only, byte-identical re-bake, ODbL, offline runtime). The warnings are follow-up-grade: the water/park gaps and preview palette drifts bind to the wiring job (or supersession), the robustness/coverage items are cheap hardening — none block this look-only spike the user already gated.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
