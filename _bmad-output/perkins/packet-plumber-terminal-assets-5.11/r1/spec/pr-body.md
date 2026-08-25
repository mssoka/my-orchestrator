## Story 5.11 — new terminal shapes: small-biz (office) + campus (ART + pipeline only)

The 5.11 terminal roster gains its class analogues — **small-biz (office)** and
**campus** — as canon sprites in the 7.1 top-down two-tone-roof language:
capacity-scaled (campus footprint > small-biz > residential), distinct
silhouettes, readable without color `[E9.1]`. **This PR is art + sprite-pipeline
data only** — the `Terminal_Role` enum, role→sprite draw wiring, caps, and
growth integration belong to story 5.11 and are deliberately NOT touched here
(see the consumer note below).

### Lavish gate verdict (recorded verbatim)

The lavish gate session
(`.lavish/terminal-assets-5.11.html`, opened 2026-08-18) delivered, via the
verdict form's Queue control, session ended by the user:

> **"APPROVE — ship these two shapes as shown"**

The approved set is what shipped in this PR: `small_biz` (warm-stone flat
parapet office) + `campus` (brick multi-wing complex).

### Shape rationale (silhouette → role readability, E9.1)

| Type | Silhouette language | Footprint (bbox) | Reads as |
|---|---|---|---|
| Residential (canon) | two-tone gable roof + chimney, 4 colorways | 88×89 px | the small home |
| **Small-biz (office)** | flat parapet roof (two-tone rim + darker inner panel), rooftop AC unit, cream storefront sign band | 120×87 px | a low-rise office — no gable, no chimney, no play-button; the rectilinear flat block between the gabled home and the campus |
| **Campus** | multi-wing complex: main hall + two side wings + center pavilion around a shallow quad, clock-tower marking | 154×103 px | the school/campus — the only multi-wing silhouette in the roster; the biggest terminal footprint |

Each type is identifiable by silhouette alone (no color dependency): the gable
ridge distinguishes residential; the flat parapet + storefront band the office;
the multi-wing U-plan the campus. The warm-stone / brick tones are a secondary
register (distinct from the four cheerful house colorways, the brand-blue host,
and the teal data center) — never the sole encoder.

### Pipeline commands used

```bash
# regenerate the sheet + manifest (adds small_biz + campus)
/Applications/Blender.app/Contents/MacOS/Blender --background --python tools/gen_sprites.py

# the 9 canon PNGs were restored byte-identical after the regen (Blender's
# PNG encoding is non-deterministic run-to-run; pixels + bboxes are stable —
# committed canon bytes kept, only the two new files + manifest extension land)

# full local suite (the GH CI is billing-blocked; local is ground truth)
tools/ci-local.sh --mac
```

Result: **10/10 gates green, incl. the palcheck oracle (gate 5)**. Goldens
byte-identical — no re-bless (the new sprites are loaded by the sheet but not
yet drawn by any role, so no golden shifts; verified gate 4 T1/T2 stable).

### Canonical citations

- Look-book v1 §2 (palette tokens) — new tones extend the building register
  in the same flat-MM register (warm stone `#9C8C6C`-family office, brick
  `#A8503C`-family campus, quad `#A8C878`, cream marking `#FFF6E6`).
- Look-book v1 §6 (the 7.1 amendment) — "Buildings are a SPRITE pipeline…
  true top-down… the ROOF carries the read" — both new shapes follow this.
- The 7.1 gate verdict (lavish r4, 2026-08-17): *"APPROVE — ship the
  top-down sprite direction as shown"* — the two-tone roof + painted-shading
  language this PR extends. Contact shadows are NOT baked (Blender's hashed
  alpha dithers at sprite size) — the game draws the flat ink ellipse, as the
  7.1 pipeline requires.
- Story 5.11 card (`stories-v2.md` §Story 5.11): "Distinct shape/icon per
  type (never color alone `[E9.1]`)"; capacity spectrum campus >> home.

### Provenance

- `tools/gen_sprites.py` gains `build_small_biz` + `build_campus`
  (reproducible — the blend source for the sprites).
- `art-renders/blend-sources/pp_lib.py` + `pp-scene-light-vista.blend` gain
  `make_small_biz` + `make_campus` with clean naming (the canon blend now
  carries the new models; re-saved via headless Blender).
- `assets/sprites/sprites.json`: `order` + `content_bbox` extended to 11
  entries — the existing 9 entries are byte-stable (verified).
- `app/render/sprites.odin`: **sheet loader mirror only** — `SPRITE_COUNT`
  9→11 and the files list, which IS the loader's contract with the manifest
  (`sprites_parse_boxes` rejects a length mismatch and the whole sheet falls
  back to primitives). No role→index wiring changed.

### Decisions & rationale

- **D1 — Two sprites, not colorways:** small-biz + campus each ship as ONE
  sprite (like host/dc), not 4 colorways like residential — they are
  institutional types; the shape is the identity. 5.11 can add colorways
  later if the roster needs variety.
- **D2 — Warm stone + brick register:** distinct from the four house
  colorways / host blue / dc teal so the new types don't get mistaken for an
  existing family even at a glance; both are flat-MM register, canon-token
  consistent.
- **D3 — Capacity ladder in the sprite geometry:** bbox widths 88 (house) →
  120 (small-biz) → 154 (campus) encode the capacity scaling at the data
  level, so 5.11's draw wiring only needs per-type target widths (proposed
  ~2.0 / ~2.6 tiles) to complete the read.
- **D4 — Multi-wing campus (U-plan + quad + tower):** chosen over a
  single-block "big building" because multi-wing is the one silhouette
  nothing else in the roster owns — the strongest E9.1 signal for "campus".
- **Rejected — a flat-roof "host-lookalike" office:** too close to the
  content host; the parapet + storefront band + rooftop AC keeps the office
  in its own silhouette family.

### 5.11 consumer note (what the code story must wire)

- `core/catalog.odin:22` — `Terminal_Role` gains variants (e.g. `Small_Biz`,
  `Campus`) + `role_from_name` (`core/catalog.odin:1011`).
- `app/render/sprites.odin` — `sprite_index_building` maps the new roles to
  sprite indices **9 (small_biz)** and **10 (campus)**; per-type target
  widths (proposed ~2.0 / ~2.6 tiles) in `sprite_*_target`.
- `data/node_types.json` — new roster entries with per-type caps
  (`cap_fraction_permille × throughput ÷ packet_bandwidth`) and
  `demand_weight`; campus throughput >> residential.
- `core/flow.odin` `collect_terminals` role selector + `core/growth.odin`
  type-pick (era-gated, E31 validity, 5.6 separation).
- A T2 frame with all three types visible (story card golden requirement).

