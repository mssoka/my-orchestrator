# The district spawn-director — Dublin stage 2, job 1

The mock gate's rulings are now the spawn policy on the real board. The
growth director's SEED/ATTACH families are weighted by district (real
neighborhoods as estate anchors), the district caps encode the density
ruling as a hard bound, and the zoom-band model (dense-core rich, backbone
sparse) lives in balance.json as named tunables the user fun-tests.

## The canon this implements (read from the approved artifacts, never assumed)

| Ruling (approved mock, Round 7) | Implementation |
|---|---|
| Density: **1-in-6** calm default (the data's own `rulings.density_default`, user-approved at the #90 spike gate) | The stride-6 pool is the draw domain (unchanged); the NEW `growth_districts.district_cap_permille` (default 1000) caps each district's live terminals at its own pool share — never more houses than the blessed fabric; ~667 ≈ the 1-in-9 fabric is the user's density iteration surface |
| Zoom model: zoomed-out backbone / zoomed-in dense play; core richest, periphery sparser (the approved gallery) | `growth_districts.seed_weight_<kind>` — the district KIND tier IS the band: city/town/quarter = dense-core (rich), village/suburb/neighbourhood = backbone (sparse). Weights bias the SEED-family's district pick AND the ATTACH family's cluster pick |
| Cluster shapes: estates anchored in real neighborhoods (the 08-21 strict doctrine — ATTACH within radius / SEED at a fresh area, cap 5) | Unchanged doctrine; the estate now LABELS by its seed district (the load-time nearest-anchor assignment) and the cluster pick extends core estates eagerly |
| Building conformity: street-aligned blocks | Unchanged — the pool is street-adjacent by construction; spawns stay on it (pinned) |
| The stage-1 warning (map.odin header): a district-SCOPED attach ring starves ~63% of pool tiles (Voronoi cells < estate radius) | The ATTACH ring stays GLOBAL (the streets rule); the district weighting lives in the CLUSTER PICK — the estate forms on the streets the grid gives it, weighted by its seed district |

## The district director (all data + derived state)

1. **Load-time assignment** (map.odin): every pool tile partitions to its
   nearest district anchor (scaled-integer Euclidean² — ODN-10, tie-break =
   lower index, deterministic; `map_district_assign` is the ONE definition
   the partition, the seed labels, and the attach cluster labels all use).
   This is the stage-1 note's "future district-scoped policy re-adds the
   assignment + ranges as data".
2. **SEED family** (board branch): ONE weighted district pick (kind weight;
   eligibility = has tiles AND under its cap) then ONE uniform tile pick in
   the district. Zero-weight band = excluded (a lone zero-weight district is
   never picked by the single-eligible shortcut — pinned).
3. **ATTACH family** (board branch): the eligible-cluster scan adds the
   district-cap predicate (a capped district's estates stop extending) and
   the cluster pick becomes ONE weighted draw over the clusters' seed-
   district weights (same draw count as the uniform pick it replaces).
4. **District caps**: `cap(d) = max(1, floor(pool_tiles(d) × permille /
   1000))`, gating BOTH families; demolished terminals free the budget
   (live counts derive from the topology).

## Determinism (rule 1 — no LOG_VERSION impact, documented)

- The director state is a PURE FUNCTION of (board bytes, catalog, topology,
  seed): assignment derived at load from the same bytes (the fixture
  precedent — replay re-derives identically), weights/caps ride
  catalog_hash, live counts derive from the topology. **Nothing new
  serializes; LOG_VERSION untouched** — the map_source byte already pins the
  map input (absent-when-procedural) and the spawned terminals ride the
  topology section of the T1 hash.
- **Dual-run:** procedural runs never enter the board branch — zero rng-draw
  change. Proven: 117/119 T2 PNGs **pixel-identical** before/after the
  re-bless; all 49 `.log.bin` differ ONLY in the 8 catalog-hash header bytes
  (@ 18..25 — the documented header-field pattern), dublin_board included
  (growth stays derive-don't-record).
- **Re-bless (cause-documented):** `balance.json` gained `growth_districts`
  (catalog_hash folds every byte → every `.t1` + log header shifts — the
  deliberate, legitimate re-bless) and the dublin board branch's SEED draw
  went 1 → ≤2 draws + the cluster pick became weighted (values differ;
  counts identical) — the deliberate dublin behavioral shift: the 2
  `dublin_board` T2 captures re-blessed, everything else pixel-pinned.

## KYLE mock-match gate (rule 2) — PASS

Live captures of the grown board (the new `harness dublin-grown` verb —
plays `dublin_board.dem` through the real core, captures the gallery's two
framings with the full topology) graded against the approved mock
(`docs/captures/dublin-map-mock/`), side-by-side composites:

- **baywide: MATCH** — sea east, core center-west, parks, dotted fabric read
  identically; terminals sit along streets; density calm (the 1-in-6 read).
- **templebar: MATCH** — street-aligned blocks in the mock's building
  language; compact estate clusters; no off-street strays.

The estate lens (the derived cluster view): 15 grown terminals = **3 full
5-member estates**, seed-anchored in real neighborhoods (Rialto,
Clonskeagh, Artane — per the district audit). The per-district counts read
1–2 because estates straddle Voronoi boundaries by design (the streets
rule: a street crossing a district boundary keeps its houses together).

## Verification

- 256 core tests green — 8 new pins: the assignment partition (one
  definition, tie-break), the weighted SEED draw (4:1 majority +
  determinism), zero-weight band exclusion (draw + step level, both
  families), the district-cap contract (both families + exhaustion =
  ok=false + the 1-tile district), the attach cluster-pick band exclusion
  (+ positive control), and a board replay byte-identity pin. **Every new
  pin mutation-verified** (uniform-pick mutation fails the majority pin;
  exclusion-off mutations fail the band pins; cap-off fails the cap pin).
- 13/13 local CI gates native (macOS) + 13/13 linux container.
- `cmp -l` evidence: 49/49 `.log.bin` = 8 header bytes only; 51 `.t1`
  re-blessed with the cause above.

## Decisions & rationale

1. **District weighting by KIND tier, not per-district rows.** The mock's
   band model maps to the data's own district classes (city/town/quarter =
   dense-core; village/suburb/neighbourhood = backbone). Per-district
   weights would need a dublin.json re-bake (osm_extract changes — out of
   scope) for no expressive gain; the kind table is the user's tunable
   surface. Rejected: per-district `band` fields in the asset.
2. **The cap is a permille of the district's own pool share, not a global
   count.** The density ruling is per-fabric (1-in-6 of the street points);
   a global cap would misallocate (the city's 5-tile district vs Raheny's
   67). The floor-1 keeps a tiny district one estate slot. The knob is the
   user's density iteration (667 ≈ the 1-in-9 fabric the briefing named).
3. **The ATTACH ring stays global; the cluster PICK carries the district
   weight.** The stage-1 header documents the starvation math (Voronoi
   cells smaller than the estate radius → a district-scoped ring starves
   63% of pool tiles). Weighting the pick delivers the band model on the
   SEED side of every estate while the streets rule binds the geometry.
4. **Zero weight = band excluded (0..1000), not a load error.** The
   fail-fast siblings (growth_groups) ban 0 because 0 breaks their
   contract; a 0 weight here is a deliberate tunable ("make the suburbs
   dormant") — the exclusion lives in the eligibility predicate so the
   single-eligible shortcut can never pick a dormant band.
5. **No serialization, no LOG_VERSION bump.** The director is
   seed-derived + caller-owned-board data — the derive-don't-record spine
   holds; the T1 map_source byte + topology section already pin everything.
   The re-bless is the catalog-hash fold + the deliberate dublin draw
   shift, both cause-documented above.
6. **bmad-build waiver (canon note):** the PP repo has no
   `_bmad/scripts/render_skill.py` (the documented Silas ruling 08-21 /
   08-23 waiver) — this job followed the self-contained briefing (spec at
   `_bmad-output/implementation-artifacts/spec-v2-dublin-spawn-director.md`).
7. **The demo golden's mesh bounds growth** (2 routers → ~15 terminals in
   90 s — E31 connectability, unchanged from stage 1). The player extends
   the mesh in real play; the gate captures use the golden's own run.

## Out of scope (named)

Streets-constrain-pipes (stage-2 job 2), last-mile draw (stage-2 job 3),
zoom-LOD render bands, dublin.json re-bake, procedural terrain.

