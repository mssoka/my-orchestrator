## What & why

The user's mid-review correction (2026-08-22): *"networking is boring… has to make good attention-grabbing thumbnails."* The v2-look-polish LEFOU system-tone pass muted the pipe tiers to gray-blue, killing the saturation ceiling — top-2% HSL saturation 0.51–0.57 (calm frames) vs Mini Motorways 0.91–1.00. This PR reverses the mute **in the network layer only**, per the design-audit direction §2 (kyle-design-directions.md). Palette-token changes only: `data/palette.json` + the `palette.odin` mirrors + the casing-blend test pins. No geometry, no sim, no LOG_VERSION.

## The change

| Token | Before (muted) | After | Role |
|---|---|---|---|
| pipe_copper | #968E84 warm gray | **#F06E00** copper-orange | narrow access tier |
| pipe_steel | #7E8692 neutral | **#0096F0** cyan | standard line tier |
| pipe_fiber | #586E8E slate | **#FFD700** gold | wide fiber — the hero (the direction's warm-gold anchor) |
| lane_standard / lane_best_effort | muted | steel-blue / green | the QoS stripes |
| router_led | #2E8B57 | **#00CD5A** | node accent token |
| packet_dot / packet_dark | muted blue | saturated blue | fallback path |

- **Tier hues pairwise-separated 23°/152°/175°** (≥ the audit's 15° blur-test standard); each tier a distinct saturated hue — the MM "bright ribbons" model.
- **Network 70/30 by real geometry**: band-area warm-gold share = 74% (3.5² + 8.5² of 3.5² + 5.5² + 8.5²) vs the direction's "network 70% warm-gold / 30% cool-cyan".
- **Calm board stays calm**: canvas/water/coast/park/grid **byte-identical** (canon D9 + palcheck pins untouched). Board 70% = the quiet paper, network 30% = the pop.
- **Packets at catalog maxima**: the catalog is untouched (cat.hash is golden-poison) — streaming #1E4A98 is already the saturated core; email #5A6270 is look-book canon grey (D4). Verified the draw path reads the catalog color directly.
- **a11y mode tables untouched** → deutan/protan/tritan goldens are **byte-identical** (the modes override every changed token).

## Verification

- **Re-measure** (audit method reproduced to ±0.004; same demos, same sha base):

| Frame | Before | After |
|---|---|---|
| juice-30000ms (thumbnail hero) | 0.570 | **0.886** ✓ |
| juice-65000ms (surge) | 0.825 | **0.879** ✓ |
| estate_surge-25000 / -75000 | 0.532 / 0.833 | **0.913 / 0.899** ✓ |
| growth-88000ms | 0.687 | 0.826 |
| terminal_types-05000ms | 0.572 | 0.715 |
| router_tiers-02500ms | 0.513 | 0.698 |

  The audit's own pop-mock measured 0.685; the shipped build **exceeds the mock on every network-bearing frame**.
- **427×240 streamer-card test** (vision-verified, glm-4.6v): the network reads as the hero on every thumbnail; board stays calm; no garish colors. Strips + evidence: `_bmad-output/design-analysis/pop/`.
- **70/30 split verified**: board tokens untouched by construction; vivid share rose 0.346→0.369 on juice-30000 (MM 0.585) — the network carries the saturation, the board still doesn't.
- **palcheck 38/38 with NO constant re-pins** (sprite/map/LANE_AMBER pins untouched); local CI **10/10**; T1 + .log.bin byte-identical (deliberate 45-demo T2 re-bless).

## Decisions & rationale

1. **Tier-hue assignment** (narrow=orange, standard=cyan, wide=gold): the wide fiber is the largest band surface (63% of pipe area) — gold makes the network warm-gold dominant (74/26 by area ≈ the direction's 70/30) while the thin copper-orange preserves the access-tier warmth canon and cyan keeps a cool "utility line" read. Alternative (wide=cyan, gold=standard) inverts the ratio (63% cool) — rejected.
2. **Sparse frames can't reach 0.85 — structural, documented**: the ceiling is the mean of the top 2% of pixels (18,432 @ 1280×720). router_tiers-02500 has 8,329 saturated px after this change (terminal_types-05000: 7,816) — below the population even at sat 1.0; the boundary falls into the canvas mass (HSL 0.51). The only token lever is saturating the board — **forbidden by the briefing's own rule 3** (70/30; "a fully-saturated board fails the direction's own standard") and canon D9. Closing the gap needs more saturated network surface (art/geometry — out of the token-only scope). The dense frames — the ones a thumbnail actually shows — all cross 0.85.
3. **router_led token raised but sprite pucks keep baked LEDs**: the puck/tier-ring accents are baked into the committed sprite art (Blender pipeline via `tools/gen_sprites.py`) — the sprite path never reads palette tokens. The token now matches the intended vivid LED (primitive fallback + future sprite regen), and the limitation is flagged rather than silently regenerating art outside the token-only scope.
4. **lane_express kept** (#E08A2E): palcheck's LANE_AMBER pin + the crisis-amber canon; the express stripe already blends vivid onto the new gold bands.
5. **Casing blend test re-pinned** (the `palette_polish_test` exacts) — same deliberate re-pin pattern as the look-polish water/park hexes.
6. **Saturation metric is HSL** (not HSV): reproduces the audit's numbers exactly (0.571/0.825/0.574); documented in the evidence artifact.

## Evidence

- `_bmad-output/design-analysis/pop/saturation-evidence.md` — method, full table, sparse-frame physics, vision quotes.
- `_bmad-output/design-analysis/pop/*-thumb.png` — before/after 427×240 strips.
- `_bmad-output/design-analysis/pop/juice-calm-surge.png` — full-res calm + surge.

