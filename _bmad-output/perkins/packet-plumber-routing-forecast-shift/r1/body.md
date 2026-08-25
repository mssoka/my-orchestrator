## 🤖 Perkins automated review — round 1 of 3
**Job:** packet-plumber-routing-forecast-shift · **Reviewed sha:** da825d8 · **Reviewers:** 7/7 completed
**Verification:** 16/17 findings confirmed against the code — 1 discarded as false-positive

### Blockers (1)

**B1 — Advisory test gate: FAIL — the acceptance-2 panel path (U → update_preview → preview card) has zero automated coverage** [tests, edge] — `app/main.odin:551`, `harness/goldens.odin:53`, `.github/workflows/ci.yml:70`

The P0 core is fully pinned (helper purity + determinism + honest-prediction pin: 132 core tests green, 17/17 demos green, drift-check 118/118 rejected — all independently re-verified). But the player-facing payoff — the upgrade-preview card — is exercised by nothing automated: `capture_frame` always passes a nil preview, CI runs only `odin test core` + harness, `app/` has no `@(test)`, and the demo language has no key verb. The card is testable headless (rlsw + `capture_frame`), and project doctrine is "Everything testable headless, is." A regression in the card's aggregation/render would merge silently.

**Fix (cheap, either or both):** add a harness capture that renders a non-nil `Upgrade_Preview` (NEW golden file — allowed by the golden discipline), and/or extract `update_preview`'s decision + `Preview_Row` aggregation into pure procs with `@(test)` pins in core.

### Warnings (4)

**W1 — `attract` magnet telegraph misses upgrades of non-representative parallel-bundle pipes** [codebase, edge] — `core/forecast_shift.odin:171-177`. `Hop.pipe` is the bundle's lowest-slot representative; upgrading a parallel pipe that isn't the rep genuinely re-prices the edge (min semantics) yet `attract` stays false — the telegraph under-reports. Fix: set attract when any live pipe sharing the hop's (from, neighbor) pair is the upgraded pipe.

**W2 — "N flows" labels pair counts** [blind, architecture] — `app/render/forecast.odin:141`. One `Route_Shift` entry is one (from, dst) node pair; the card aggregates pair counts and prints "N flows". The demo spawns four packets per pair — the number understates real flow movement. Fix: relabel ("affects N routes") or count actual demand flows per pair.

**W3 — `tiers` scratch sized by `len(pipe_alive)` but filled by `len(pipe_tier)` — latent OOB** [security, blind] — `core/forecast_shift.odin:115-119`. Safe today (both arrays appended in lockstep, `topology.odin:187,191`, never shrink); a future divergence would panic. Fix: size by `len(t.pipe_tier)` (the loop's bound) and assert the two lengths match.

**W4 — Preview-card render branches (overflow tail, zero-shift line, magnet, pluralization) untested** [tests, edge] — `app/render/forecast.odin:122-237`. The >12-bucket overflow, "no reroute predicted", magnet line, and conjugation produce the exact text players read — no pin. Fix: pure-proc extraction with `@(test)` pins; dense + empty preview-card golden captures.

### Notes (6)

**N1** — `routing_rebuild_with_tiers` indexes the caller-supplied `tiers` slice without length validation [security, edge] — `core/routing.odin:116`. Latent hardening; both current callers pass matching lengths. Guard the seam.
**N2** — Preview card duplicates the weather card's chrome/layout math instead of a shared `draw_card` [architecture] — `app/render/forecast.odin:70-73`.
**N3** — The commit leg is unwalkable in the live app: demolish input was never wired into `app/main.odin` (pre-existing — 2.3 shipped without it), so "demolish+redraw → watch the prediction come true" is walkable in the demo only [edge]. Adding a demolish key would violate the no-new-player-commands scope guard — descope explicitly or note the demo is the walkable surface.
**N4** — Disarm paths (pipe gone / widest tier / deselect) leave `preview_shifts` allocated until re-arm or run end [blind] — `app/main.odin:553`. Bounded; free on every disarm path.
**N5** — `Route_Shift` display fields (attract-on-split, `old_pipe`) and the same-cost-different-tier path unasserted [tests] — `core/forecast_shift_test.odin:70-90`.
**N6** — Preview card height is one line (20px) too tall whenever shifts exist (`lines := 2 + nrows` vs 1+nrows drawn) [perkins] — `app/render/forecast.odin:150-156`. Cosmetic, app-only.

### Reviewer agreement
Five findings independently confirmed by two lenses: W1 [codebase, edge], W2 [blind, architecture], W3 [security, blind], W4 [tests, edge], N1 [security, edge], plus the coverage gate [tests, edge].

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
