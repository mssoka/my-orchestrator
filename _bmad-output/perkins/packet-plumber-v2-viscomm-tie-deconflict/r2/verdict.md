# Perkins round 2 — packet-plumber-v2-viscomm-tie-deconflict (fix-audit)

**PR:** https://github.com/solarity-services/Packet-Plumber/pull/99 (base v2)
**Reviewed sha:** `0c024aef0806b202263dce4c024e9248a48d7322` (detached worktree; head re-verified at post time)
**Diff source:** saved diff.patch — 8 files, +331/−30 of r2 fixes (652 lines total)
**Spec:** PR #99 body + the r2 fix obligations brief (acceptance contract)
**Reviewers:** 7/7 completed (blind, edge, acceptance, security, architecture, codebase, tests) — no failed layers, no retries
**Verification:** 16/18 lens findings survived independent re-verification — 2 rejected as false-positive (both blind: `pale` is consumed at derive:205, same r1 precedent; tracked `_pr_body` files are repo convention, 12 siblings); 0 unverifiable-speculative
**Model:** glm-5.3 (all 7 lens sessions modelId-verified); vision caveat honored — all color/pixel verification mechanical (computed from shipped palette bytes), aesthetic judgment deferred to k3 re-check per doctrine

## Fix audit (round 1 → 17/17 FIXED, 0 still-present)

| r1 | Finding | Status | Evidence |
|----|---------|--------|----------|
| B1 | Shape gate vacuous vs draw path | ✅ fixed | `tie_dash_segments()` consumed by `draw_tie_mark`; palcheck §5 pixel-scans the real draw path (drawn 18/36, mismatches 0). **Mutation-verified by Perkins**: enumeration bypassed to a solid ring → palcheck **FAIL** "drawn 36 of 36, mismatches 18"; restored → green; porcelain empty |
| W1 | Verified on stripped copy | ✅ fixed | `strip_jsonc_comments`/`load_jsonc` shipped; script runs on **shipped bytes**: ALL PAIRS CLEAR ×3; numbers reproduce exactly (worst route_tie pair 102.8; tie-vs-congested 202.1/236.5/105.0) |
| W2 | 14.03° from router_tier_high | ✅ fixed | Hue 280.0° → 29.68° from router_tier_high, 118.97° circular from state_congested (independently computed from shipped bytes); tiers array now 6 (3 pipe + 3 router) |
| W3/W5 | tie-vs-congested pair missing from oracles | ✅ fixed | Pair present in `a11y_separation_check` AND the derive script's `pair_list` |
| W4 | Predicate-only pin | ✅ fixed | Same as B1 |
| adv | Gate CONCERNS | ✅ fixed | This round's tests-lens gate: **PASS** |
| N1/N5 | derive can't regenerate modes | ✅ fixed | Same as W1; emits zero route_tie remaps |
| N2/N6 | geometry duplicated | ✅ fixed | `draw_ring_segments` single-sources the quad fan; `draw_ring_annulus` delegates via identity enumeration |
| N3 | "6 dashes" comment rot | ✅ fixed | `TIE_DASH_COUNT` derived + compile-time `when` trip |
| N4 | PR 225° impossible | ✅ fixed | Correction comment verified on PR #99 (134.6° circular then; 119.0° now — matches recomputation) |
| N7 | missing degenerate guard | ✅ fixed | Guard present (see new note 3: it also suppresses the caption — minor) |
| N8 | classifier-only pin | ✅ fixed | Numeric `dc >= 90` circular pin |
| N9 | modes absence untested | ✅ fixed | palcheck asserts `eff.route_tie == base.route_tie` per mode |
| N10 | no render-level test | ✅ fixed | §5 renders the real `draw_route_glow → draw_tie_mark` path on rlsw |

**Verify suite independently reproduced:** lint.sh all green · `odin test core` 261 OK · `app` 46 OK · `app/render` 83 OK · palcheck all green.

## BLOCKERS (0)

None.

## WARNINGS (3)

1. **Committed PR body documents r1 values contradicting the shipped r2 bytes** [blind] — `_pr_body_viscomm_tie.md:13` (and the live PR #99 body): `#965EE8`/hue 264°/"≥62° from every tier"/r1 a11y table vs shipped `[186,94,232]` @ 280°, 29.7° from router_tier_high. *Cluster: acceptance/codebase/architecture mirror-notes below.* → `gh pr edit` + refresh the tracked mirror.
2. **PR body side note calls the derive-script bug "pre-existing, out of scope" while this diff fixes it** [blind] — `_pr_body_viscomm_tie.md:55-57` vs `strip_jsonc_comments` in the same diff. Same refresh.
3. **palette_load's inline jcol default for route_tie (3rd ODN-5 mirror site) has zero coverage** [tests] — **empirically proven by Perkins mutation probe**: reverting only the jcol default to amber → 83/83 tests PASS (vacuous). → add a stripped-JSON `expect_color` leg.

## NOTES (13)

1. [blind] `draw_ring_segments` never uses its `v: ^View` param — dead weight.
2. [edge] `draw_ring_segments` doesn't validate `segs` bounds (callers by-construction in-range; Odin bounds-check is loud — prefer that to a silent skip).
3. [blind] new degenerate guard also suppresses the rule caption (old code always drew it; degenerate-config-only divergence).
4. [edge] palcheck §5 discards lookup/edit errors — file-wide harness convention (§2 does the same); fix belongs file-wide, not on this diff.
5. [acceptance/architecture/codebase] stale-PR-body cluster mirrors (in-tree copy keeps r1 numbers).
6. [architecture] palcheck §5 mirrors the 0.62/2.5 ring-geometry constants textually — export a `tie_ring_geometry` proc to bind them.
7. [architecture] 35-line JSONC stripper for exactly one `//` line — strict-JSON normalization (fold line 11 into `_comment`) was the simpler path; pick one deliberately.
8. [codebase] palette.json `_comment` rotates the tie-vs-congested triple (actual deutan=202.1/protan=236.5/tritan=105.0) — independently reproduced before reading the finding.
9. [tests] degenerate guard happy-path-only (no negative leg).
10. [tests] W1 fix has no automated gate — add a lint.sh run of the derive script.
11. [tests] Advisory test gate: **PASS** (P0 100%, P1 ~100%, overall ~82%).

*(Full detail with verbatim evidence in `consolidated.json`.)*

### Reviewer Agreement

Empty (all titles distinct under the mechanical dedupe key). Semantic clusters disclosed above.

### Verdict

**READY TO MERGE** — all 17 round-1 findings fixed (blocker mutation-proven to bite, twice), 0 new blockers; 3 warnings are doc-staleness plus one follow-up pin, none blocking.

*Deferred per doctrine: aesthetic read of the violet (k3 re-check when kimi returns). All numeric hue/CVD claims verified by computation from shipped bytes.*
