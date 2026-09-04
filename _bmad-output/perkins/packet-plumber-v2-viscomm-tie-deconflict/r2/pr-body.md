## What

Finding A of the vis-comm audit (2026-08-25): the equal-cost tie mark and the
congestion-warning telegraph are gestalt twins. `route_tie` {242,181,68,235}
was RGB-identical to `state_congested` {242,181,68,255} (alpha 20/255 apart),
and both drew solid node-centered rings — two UNRELATED meanings ("routing
info, nothing is wrong" vs "this node is strained — act") sharing hue AND
shape. A player who learns "amber ring = congestion" misreads the tie mark as
a warning, or worse, learns to ignore amber rings outright.

This PR de-conflicts on BOTH levers (never color alone, both directions).

## Hue: info violet `#965EE8` = {150, 94, 232, 235}

- **Hue 264°** — a clear family exit, not a nudge: **225°** from
  `state_congested` (39°, warm-danger family).
- **Pipe-tier safety**: >= **62°** from every tier (copper 28°, gold 51°,
  steel-cyan 202°) — well past the 15° canon minimum, so the ring can never
  read as a pipe tier. (Deep teal was rejected: only ~25° from the
  steel-cyan tier.)
- **Canvas contrast**: on the warm-cream `#EDE2C8` paper the violet reads at
  rec.601 luminance ~126 vs the canvas ~226 — a dark-on-light pop in the
  cool register the board otherwise reserves for nothing node-shaped, so it
  reads "annotation/overlay", not "danger" (warm) or "infrastructure"
  (copper/gold). Violet is the classic informational/selected-state family.

Applied in the three canonical places, one value each: `data/palette.json`,
`palette_load`'s inline fallback, and `fallback_palette` (ODN-5: palette is
data; the fallbacks mirror it).

## Shape: dashed ring

`draw_tie_mark` now draws **6 dashes of 30°** (3-on / 3-off around the pinned
36-segment `SPAWN_RING_TABLE` fan — the `draw_ring_annulus` quad precedent:
two CCW triangles per segment, alpha-safe in rlsw, no transcendentals in the
draw path). The warning telegraph stays a SOLID ring. Even a fully colorblind
read cannot confuse dashed-info with solid-warning. Caption
("equal cost - split by hash", ASCII) unchanged. The modulated predicate is a
pure proc (`tie_dash_on`) so the test pins draw behavior, not just constants.

## a11y mode tables (derived, not hand-waved)

The old mode tables remapped `route_tie` to pale amber `[242,213,120]` —
**RGB-identical to `state_congested`'s deutan/protan remap** — i.e. the CVD
modes reintroduced the exact collision this PR removes. The base violet
clears every oracle pair under all three Machado-2009 severity-1.0
simulations, so the remap is retired:

| mode | worst pair (route-marks, vs `route_glow` teal) | threshold |
|---|---|---|
| deutan | 109.8 | 48 |
| protan | 148.5 | 48 |
| tritan | 136.2 | 48 |
| deutan/protan, tie vs congested remap | **241.2 / 275.7** | 48 |

`tools/derive_a11y_palettes.py`'s amber anchor for `route_tie` is removed
(partial tables: absent tokens keep base values); the three `route_tie` lines
are deleted from `data/palette.json` "modes". `tools/harness.sh palcheck`
green on the shipped tables. (Side note: the derive script chokes on the
`//` comments now present in palette.json — I ran it on a comment-stripped
copy; pre-existing, out of scope.)

## Mutation leg (vacuous-pin doctrine)

`app/render/palette_polish_test.odin` gains two tests:
`route_tie_is_hue_distinct_from_warning_and_pipe_tiers` (exact bytes on both
load + fallback paths, warm-family exit classifier, >= 15° from every pipe
tier via `hue_degrees`) and `route_tie_mark_is_a_dashed_ring_not_a_solid_warning_shape`
(duty cycle must be exactly 1/2, run-boundary spot checks, dash count >= 4).

**Proven by mutation, both levers:**
1. Hue revert (`route_tie` back to `{242,181,68,235}` in palette.json):
   `odin test app/render` FAILS — byte pin, warm-family check, and two
   tier-separation asserts (copper 11.5°, fiber 11.6° < 15) all fire.
2. Shape revert (`tie_dash_on` -> `return true`, i.e. solid ring):
   FAILS — "dash duty cycle must be 1/2 (on=36 of 36)".

## Verify (all green, from the worktree root)

| command | result |
|---|---|
| `odin test core` | 261 tests OK |
| `odin test app` | 46 tests OK |
| `odin test app/render` | 83 tests OK |
| `tools/lint.sh` | all gates green |
| `tools/harness.sh palcheck` | all green |
| `tools/harness.sh run` | **49/49 demos green, ZERO golden diffs** (golden-safety premise held: the harness never invokes the assist draws) |

Out of scope (noted in the audit findings file): `sel_halo` and
`lane_express` also sit in the amber family but draw on pipes/bands, not
node rings.

