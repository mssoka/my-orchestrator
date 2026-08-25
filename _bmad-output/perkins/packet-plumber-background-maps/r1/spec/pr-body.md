## Story 7.4 — Background maps (canon D9): the world under the network

The play surface stops being a flat cream void and becomes a procedural **land/ocean/parks map** — noise-driven landmasses with coastlines + green park blobs over soft-blue water, MM-style, in the light-canvas palette (look-book D9, user verdict 2026-08-08: "a map background, just like Mini Motorways").

**LAVISH GATE VERDICT (verbatim, 2026-08-18):**

> "Map style verdict: pick B (seed 1234)"

Three candidate map seeds were rendered on the same gameplay moment (the story-7.1 juice scene) side by side against the vista reference (`renders/01b-vista-light.png`); the land-heavy balance (~52% land / ~28% water / ~8% parks — the largest continuous landmass) was approved. The approved style — soft water, sand coast band, sage park blobs, subtle grid over land and water — is applied to **every** run seed (the map is seed-derived by design; B's balance is the selected tuning).

### The generator (`app/render/map.odin` — presentation-only)

- **Seed derivation:** the map is a pure function of the **run seed** + the world dims — same seed → **byte-identical map** (pinned by a new palcheck identity gate). No snapshot fields, no LOG_VERSION bump, no sim fields: **T1 hashes + the replay gate are byte-identical** (proven below).
- **Noise:** deterministic integer-hash **value noise** (splitmix64-style mixing + smoothstep interpolation) — no transcendentals anywhere in the rasterized path (the §10.4 rule). Land = land-noise above a threshold (~50% land); coast = a dilated-water sand band (2px); parks = a second, coarser noise domain on interior land (~10%).
- **Render:** the sea base fills the window (world + camera-fit margins); land/coast/park cells span-fill the world rect as integer-screen rects (exact shared boundaries — no hairline gaps). The snap lattice stays at the 7.1 canon 18% blend, over land AND water.
- **Cache:** per-seed per-pixel classification cached in the View, regenerated on seed/world change; zero per-frame heap churn.
- **Determinism proof:** new palcheck section 3 — the seed-7 cells FNV pin + same-seed-stability + seed-sensitivity legs (this gate caught a real stale-cache bug during development: prior-seed park/coast cells survived a regen in the multi-demo harness process — fixed by making the generator total).

### Palette extension (data/palette.json + the look-book §2 oracle)

| token | hex | use |
|---|---|---|
| `water` | `#A4C7D8` | soft sea base (world + margins) |
| `coast` | `#D5C5A3` | sand edge band |
| `park` | `#A0C294` | sage green blobs |
| land | `#E8DDC2` | = the canon `canvas` (unchanged) |

The palcheck gate (gate 5) now scans the blessed juice goldens for water/land/park/coast presence (floor counts with margin — a removed/broken map collapses all four at once). All tokens are cosmetic — `palette.json` is deliberately NOT hashed (it cannot bind replay).

### Goldens — deliberate re-bless, cause-documented

- **Cause:** the map changes EVERY frame (every T2 capture now renders the seeded map under the world). 76 T2 frames re-blessed — deliberate, reviewed like code.
- **T1 + replay: byte-identical, proven.** The sim layer is untouched (map is view-only). The full harness run passes every demo's T1 manifest hashes + the replay gate; `git status` shows **zero** `.t1`/`.log.bin` diffs (PNGs only).
- `tools/ci-local.sh --mac`: **10/10 gates green** (lint, core tests, app build, golden harness, palcheck incl. the new map gates, drift-rejection, preview cross-check, PP_DEBUG builds, stats replay-identity, input parity).

### Canon fold (same PR)

- `stories-v2.md` — new **Story 7.4** card (slice 7 view lane, Given/When/Then + status).
- `decision-log.md` — the **D9 scheduled + shipped** entry (2026-08-18).
- `look-book-v1.md` — the §2 palette table gains the map tokens (the palcheck oracle) + a §7 amendment documenting the D9 shipment + the gate verdict.

### Decisions & rationale

- **"Pick B" means the style, not a fixed map.** The map is seed-derived by design (hard requirement 1 — same seed → identical map); the gate approved B's balance/palette, which every seed then produces (a similar-feeling land-heavy map).
- **Real geography flagged at the gate (not silently dropped).** The user asked whether the map could represent real cities/states/countries; the honest feasibility read was given in-browser (needs a coastline dataset, projects to ~20-30px at our 40×30-tile world, amends D9's "noise-driven" canon, drops seeded variety). The user's pick of B = proceed with the abstract seeded map; **real geography is a named follow-up story** with its own gate.
- **The stale-cache determinism bug** (above) was caught by the very pin this PR adds — the generator is now total (every cell written per generation).
- **Dev tool added:** `harness map-preview <seed>` renders the juice scene on any seed's map (the gate's candidate renderer; also handy for future art iteration). Not a CI gate.
- **Out of scope (named follow-ups):** terrain-aware placement (terrain does NOT gate gameplay in v1 — grid rules unchanged), minimap, camera changes, real geography.

### Verification

- Lavish verdict recorded verbatim above (gate page + candidate PNGs archived at `.lavish/d9-map-gate/` in the working tree — local, not committed).
- Same-seed map identity pinned (palcheck section 3: `MAP_IDENTITY_PIN` = the seed-7 cells FNV-1a-64, re-blessed deliberately).
- Replay byte-identical + T1 unshifted (proven: zero `.t1`/`.log.bin` diffs; full harness green).
- `tools/ci-local.sh --mac` 10/10.
- Citations: look-book-v1.md §2 "Canvas / map" + decision D9; GDD decision-log 2026-08-18; stories-v2.md Story 7.4.

**Files changed:** `app/render/map.odin` (new — the generator), `app/render/view.odin` (map pass + seed threading), `app/render/palette.odin` + `data/palette.json` (tokens), `app/main.odin` (seed), `harness/palcheck.odin` (map presence + identity gates), `harness/goldens.odin` + `run.odin` + `overlay.odin` (seed threading), `harness/map_preview.odin` + `main.odin` (new preview tool), `goldens/**` (76 re-blessed T2 frames), `_bmad-output/.../stories-v2.md`, `decision-log.md`, `look-book-v1.md` (canon fold).

