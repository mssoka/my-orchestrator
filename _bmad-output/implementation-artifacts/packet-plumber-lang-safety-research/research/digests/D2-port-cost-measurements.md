# D2 — Port-cost + hardening surface, MEASURED on this repo @ v2 3960644 (2026-08-28)

All numbers measured this run (wc/grep on the checkout). Non-test LOC.

## Size & shape

| Module | LOC (non-test) | Notes |
|---|---|---|
| core (sim) | 11,230 | deterministic spine; serialize+hash = 1,250 |
| app (game) | 15,571 | main 2,614; input 2,192; audio 874 |
| app/render | 8,850 | CUSTOM renderer on raylib (view 2,409; wire_path 744; NOC 1,078) |
| harness | 8,816 | golden-image CI: palcheck 1,618, parity 1,400, run 1,011, demo 763 |
| tests | 22,665 | more test code than sim code |
| **TOTAL Odin** | **~58,000** | + 50 demos, 148 golden files (16 MB), data catalogs (JSON) |

## The memory-discipline surface (what "harden Odin" must cover)

- `delete(...)` sites: **232** (non-test) — every one a manual lifetime decision
- raw `free(...)`: **0** — the codebase is 100% Odin dynamic arrays/maps, zero
  raw pointer frees (discipline: no raw pointers at all in sim/app)
- `make([dynamic]...)`: 158; `resize(...)`: 35; `free_all(temp_allocator)`: 10
  (per-frame temp arena discipline in app; harness per-tick)
- custom allocator use: essentially NONE beyond `context.temp_allocator`
  (no tracking_allocator, no arenas for the sim, no checked allocators in CI)
- Run_State's dynamic-field tree: **~57 fields** across 9 structs;
  `shadow_clone` clones **55** — the 2 missing (Box.pieces/.spools) are
  tonight's crash. Prior misses: tx ring (network-units), residency (egress S5)
  — the recurring class has no structural guard.

## FFI / engine coupling (port cost driver)

- raylib (`vendor:raylib`) is the only foreign dep: **92 distinct rl.* procs**
  across app/input/render/audio. Custom renderer means a Rust port re-choices
  the whole draw stack (wgpu/bevy), not a binding swap.
- The sim (core) is raylib-FREE (pure Odin) — the determinism spine
  (serialize/hash/step) ports mechanically IF the port keeps integer-only
  discipline; the golden corpus is the re-verification vehicle.
- Audio: raylib audio + synthesized stings (874 LOC) — smallest surface.

## Harness coverage of the app layer (the hidden-bug exposure)

- The harness links core + render headless and replays 50 demos against 148
  goldens + T1 hash + drift gate — but NEVER calls `spawn_fx_predict`
  (grep: 0 refs in harness/) and never drives the app input/effect layer.
  The app-only surface (input executor effects, telegraph predictor, HUD
  string paths, audio feed, camera effects) is exercised ONLY by playtest.
- App-layer LOC (input+main+audio minus render) ≈ 5,700; render 8,850 —
  i.e. roughly 40% of the game's LOC run only under the user's cursor.
