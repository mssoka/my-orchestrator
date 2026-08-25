# v2-node-clarity — node types identifiable at a glance (Q2a/Q2b)

The audit's complaint #2 ("it's not clear which node is what") was measured
true: small_biz / campus / content_host shared the wide-block aspect and
small_biz / campus shared the warm-brown family. The σ6 blur test failed the
DIRECTION.md §1 bar — residential↔small_biz **4°**, residential↔campus
**13°**, router_mid↔content_host **9.7°**, saturation band **0.40** wide.

This PR is the in-engine fix (palette tokens + draw layer only — no
geometry, no sim bytes touched): **distinct hue families per terminal class,
type icon chips, router tier markers**.

## The blur-test gate — every pair hue-separated ≥15°, sat band ≤0.30

Measured by the committed gate tool `tools/blur_gate.py` (σ6 Gaussian blur on
the terminal-types capture at 5000 ms; per-type mean-RGB signature at each
node's screen position — the same lens the audit used, baseline-calibrated
against its numbers before the fix).

| Type | Hue (baseline → this PR) | Sat (baseline → this PR) |
|---|---|---|
| residential | ~13° (mixed) → **0.6°** terracotta | 0.20 → 0.395 |
| small_biz | 40.6° warm tan → **109.4°** cool stone | 0.175 → 0.138 |
| campus | 22.8° brick → **23.3°** dusty brick | 0.337 → 0.354 |
| content_host | 217.8° → **210.3°** deep blue | 0.414 → 0.427 |
| router_mid | 208.1° gray-blue → **181.6°** teal tier wash | 0.172 → 0.378 |

| Pair | Baseline | This PR |
|---|---|---|
| residential ↔ small_biz | 3–4° ❌ | **108.8°** ✅ |
| residential ↔ campus | 13–13.8° ❌ | **22.6°** ✅ |
| router_mid ↔ content_host | 9.7–9.9° ❌ | **28.7°** ✅ |
| all 10 pairs | 4 pairs < 15° | **min 22.6° — all ≥ 15°** ✅ |
| saturation band | 0.403 ❌ | **0.289** ✅ (≤ 0.30) |

Evidence frames (before/after, full + σ6 blur + node close-ups):
`_bmad-output/pr-bodies/v2-node-clarity/` — `full-before-after.png`,
`blur6-before-after.png`, `node-closeups-after.png`.

## What changed

1. **Hue-family separation (palette tokens, additions only)** — every
   pre-existing token keeps its bytes (the parallel v2-network-pop job owns
   the network tokens; the wave-final reconciliation reconciles). New tokens
   in `data/palette.json` (the ALPHA byte is the wash strength):
   - `residential_family` [205,92,92,204] — warm terracotta (anchor #CD5C5C)
   - `small_biz_family` [110,155,116,184] — cool stone
   - `campus_family` [168,114,80,184] — dusty brick (anchor family #8B4513)
   - `host_family` [70,130,180,184] — deep blue (anchor #4682B4)
   - `router_tier_basic/mid/high` — the tier marker colors (steel / teal /
     periwinkle; alpha = puck wash strength)
2. **Draw-layer wash** (`draw_building` / `draw_router`) — the baked sprite
   recolors into its family: the token alpha-blends over the sprite
   footprint (rect for buildings, disc for pucks; 4% inset keeps the
   silhouette edge). Interior detail survives the wash (windows, the host's
   play-marking, puck LEDs all still read at zoom); at fit the blur
   signature lands in the family.
3. **Type icon chip** (`draw_type_chip`) — a tiny paper chip above each
   terminal with the role's silhouette glyph in the family color (the tray
   glyph language: primitives, no font — legible at bird's-eye): house
   triangle / office rect / campus block+tower / host play-mark. Skipped
   while a health ring is up (the state surface owns the node's top then).
4. **Router tier markers** — per-tier puck wash (basic keeps its steel, mid
   teal, high periwinkle — the blur cure for the puck↔host pair) + a thin
   tier-colored ring just outside the puck (the bird's-eye tier read; the
   LED count alone is sub-pixel at fit). Size ladder untouched.
5. **Pins** — `palcheck` 46 checks (washed-tone pins re-measured from the
   re-blessed goldens, chip glyph pins, tier ring pins, family washes
   present on the terminal-types golden); the render test pins the shipped
   tokens + the token-level ≥15° hue separation.

## Honesty notes (the re-bless discipline)

- **T1 byte-identity:** all 45 `.t1`/`.log.bin` re-blessed **byte-identical**
  (`cmp` verified; palette is deliberately unhashed — `core/catalog.odin`
  comment) — the view never perturbs the sim. `fold-check` PASS (the only
  tick-1 shift is the catalog fold itself).
- **T2 re-bless:** deliberate, all 45 demos (the washes/rings/chips change
  every frame that carries nodes), cause-documented in this body; diff
  bundles under `goldens/_reports/` from the first failing run.
- **palcheck:** 46/46 green — the sprite pins were re-pinned to the washed
  composites (measured exact from the goldens; the play-marking canary
  re-pinned washed: the marking now renders under the host wash).
- **a11y caveat (documented, not fixed here):** the campus↔residential pair
  collapses under deutan/protan simulation (warm reds — 12–18 sim-dist vs
  the 48 signal threshold). The family colors are identity, not signals: the
  distinct silhouettes + chip glyphs + tier rings carry the type under CVD
  (E9.1 — never color alone). The a11y mode tables are untouched
  byte-for-byte; the signal-set oracle (states/lanes/pipes/route/map) is
  unchanged.
- **Perf:** the added draws are a handful of primitives per node (wash rect
  + chip 2–4 draws + ring) — no measurable cost (all 10 gates green in the
  container, full demo runs).

## Local suite

`tools/ci-local.sh` (linux container) — **10/10 gates green**:
lint/purity, core+app tests (219+), game build, golden harness (45 demos),
palcheck, drift-rejection, preview cross-check, PP_DEBUG builds, stats
replay-identity, input parity (27 scenarios).

## Decisions & rationale

| # | Decision | Rests on | Rejected alternative |
|---|---|---|---|
| D1 | **Wash the baked sprites at draw time** (token alpha = strength) instead of re-rendering the sprite sheet | The briefing's hard rule 1 (palette tokens + draw layer only — no asset/geometry churn); the blur test needs the RECOLORED signature, and the wash keeps the silhouette + detail | Re-rendering via `tools/gen_sprites.py` (Blender) — outside the allowed surface, non-deterministic-ish re-bless |
| D2 | **Campus anchor tuned to dusty brick** #A87250 (not the literal #8B4513 anchor) | The gate: terracotta↔brick at the briefing's anchors blur to ~13° (both pulled toward the 44° canvas) — 11° short of the ≥15° bar. Same brick family, sat lowered to fit the ≤0.30 band | Keeping #8B4513 exactly (fails the gate) |
| D3 | **Stone anchor tuned cool-green** #6E9B74 (not the literal #A0937D) | #A0937D blurs to ~40° — within 15° of campus's ~28° (and of the canvas itself). The cool-stone FAMILY (the briefing's own name for small_biz) at ~110° is the only slot that clears both warm families and the blue host | Literal anchor (fails the gate) |
| D4 | **Router tiers get a puck wash + ring** (not just a ring) | The ring alone can't move the σ6 blurred signature (the ring is ~1% of the blur weight at the puck center — measured); the wash moves the puck off the host-blue family (the audit's 9.9° failure) while the ring gives the at-a-glance tier read | Ring-only (fails router↔host); port-count text (too small at fit, font-dependent) |
| D5 | **Chips skip congested nodes** (health ring replaces them) | The ring + its glyph own the node's top surface; both would collide at the same screen band | Drawing both (overlap mess) |
| D6 | **Residential houses unify to terracotta** (the 4 colorways still faintly differ through the 0.80 wash) | The blur signature must be ONE family; the briefing explicitly orders the terracotta family while keeping the house silhouette | Keeping the 4 colorways (the audit's mixed-signature failure) |
| D7 | **Additions-only tokens** — zero edits to existing tokens | Parallel-safe with v2-network-pop (both touch data/palette.json — this PR only ADDS keys; a clean merge in either order) | Editing shared tokens (merge conflicts / POP regression) |

## Files

- `data/palette.json` — 7 new tokens (+comment), additions only
- `app/render/palette.odin` — struct fields + load + fallback
- `app/render/view.odin` — `draw_nodes` health threading, `draw_building`
  wash+chip, `draw_router` tier wash+ring, new procs (terminal_family,
  router_tier_family, draw_family_wash, draw_family_wash_disc,
  draw_type_chip, draw_tier_ring)
- `app/render/sprites.odin` — `sprite_blit_dst` extraction (shared dst rect)
- `app/render/palette_polish_test.odin` — shipped-token pins + token-level
  hue separation test
- `harness/palcheck.odin` — washed-tone pins, chip pins, tier ring pins
- `tools/blur_gate.py` — the committed blur-test gate tool (baseline
  calibrated, exit 0 = green)
- `goldens/**` — 45 demos re-blessed (T2 only)

