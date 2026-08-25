## 🤖 Perkins automated review — round 1

**Job:** packet-plumber-v2-dublin-spawn-director · **Reviewed sha:** `93333cd` · **Reviewers:** 7/7 completed (14/14 chunk-verdicts — big-diff split: code + goldens)
**Verification:** 36/41 findings confirmed against the code — 4 discarded as false-positive, 1 kept as [unverified]

**Vision caveat:** glm-5.3 round — pixel/determinism verification was MECHANICAL ONLY (byte/hash/capture-diff: 49/49 `.log.bin` = exactly 8 header bytes @18–25 ✓; exactly 2 of 113 golden T2 PNGs changed ✓; LOG_VERSION untouched ✓; 51 `.t1` re-blesses shape-verified as catalog-hash-fold-only ✓). Aesthetic adjudication of the KYLE mock-match gate rides the PR evidence (MATCH at both framings) and is deferred to the k3 re-check — never faked here.

### Blockers (1)

**1. ATTACH weighted cluster-pick has no semantic bias pin — a uniform-pick regression passes the entire unit suite** [tests, blind, acceptance]
`core/map_test.odin:477-520` vs spec §3 pin 3. The spec pin promised *"two estates in districts of different weights — the rich district's estate extends more"*; the delivered positive control runs at weight **parity** (suburb 4 = city 4), so it proves exclusion-is-the-weight, not bias. Phase 1 pins only zero-weight exclusion. A regression of `weighted_pick` → uniform passes all 8 new unit pins; only a whole-golden re-bless diff would catch it — exactly the failure mode mutation-verified pins exist to prevent. The zoom-band ATTACH side is a headline behavior of this job; the pin gap is un-acknowledged in the PR body.
**Fix:** one fixture test, two eligible estates, unequal weights (city 4 vs suburb 1), assert the rich district's estate extends more over N deterministic windows; mutation-verify by flipping `weighted_pick` to `rng_range`.

### Warnings (5)

**1. ATTACH member tile's own district is never cap-checked — cross-boundary estates can exceed the claimed hard bound** [edge, blind]
`core/growth.odin:850-853` — eligibility checks only the cluster's SEED district; the global-ring ring draw can place a member in a neighboring district already at cap (estates straddle Voronoi cells by design, per the PR's own audit). Contradicts the "hard bound / never more houses than the blessed fabric" claim (PR body + `balance.json` _comment). Bounded in practice (5-member estates, min_sep), reachable at the 667 iteration target. Fix: cap-check the drawn tile's district (reject + redraw), or scope the claim and document the straddle leak as accepted.
**2. Spec pin 4 clause "demolished terminals free the budget" is claimed but untestable** [acceptance, tests]
`core/topology.odin:274` — E2 forbids terminal demolish; the behavior holds by construction (derived live counts) but no test can trigger it. Acknowledge as vacuous-by-design rather than listing it as verified behavior.
**3. `growth_district_live_count`'s Terminal-only filter is unpinned** [tests] — a routers-count-too mutation passes the suite. One pin: routers-only district reads live=0.
**4. Loader pass-3 district partition never asserted** [tests] — every unit test hand-builds the lists; deleting `map.odin:414-425` pass 3 fails no unit test (only integration goldens). One loader-fixture pin closes it.
**5. Advisory test gate: CONCERNS (P1 ≈88%)** [tests] — P0 100% (replay byte-identity, fail-fast rows, procedural inertness via goldens); the ATTACH bias pin is the single P1 gap.

### Notes (17)

- **"117/119 T2 PNGs" miscounts** [6-lens agreement] — the golden tree holds **113** T2 PNGs; the diff touches exactly the 2 `dublin_board` captures. Correct tally: **111/113 pixel-identical + 2 re-blessed**. The 119 denominator is reachable only by adding the 6 static mock-capture PNGs. Substance verified; the published numbers overstate the scope — correct the PR body + memlog.
- **memlog "draw counts unchanged" contradicts spec/PR "SEED 1→≤2 draws"** [blind] — one record is wrong (the SEED draw count DID change); amend the badge-out line.
- **jint lenient parse for the new rows** [edge, security] — decimals silently truncate; consistent with the `growth_groups` sibling convention (advisory: consider `jint_strict` next touch).
- **dublin-grown ms×logic_hz u64 wrap** [edge] — unbounded `parse_u64` product; debug-verb QA only.
- **Usage comment example `240000ms` fails the bare parser** [blind] — `harness/dublin_shot.odin:108` vs the `parse_u64` convention.
- **Partition loop copy-pasted ×4–5** [blind, codebase] — loader + fixtures; a fixture that forgets the copy leaves `district_tiles` empty. Extract one shared build proc.
- **Live counts re-derived O(districts×nodes) per attempt** [architecture] — immaterial at current scale; derive once per window if maps grow.
- **Fractional-anchor quantization unpinned (MAP_ANCHOR_SCALE=10)** [architecture, tests] — every real Dublin anchor is fractional, every test anchor integral; one fractional-anchor fixture would pin the real-board path (also the ODN-10 float gray zone).
- **Statically dead board predicate in the procedural re-walk** [architecture] — `growth.odin:885-897` residue; delete + fix the misleading comment.
- **Spawn-audit header mislabels `node_count` as "live terminals"** [architecture, codebase] — the committed gate artifact reads "17 live terminals" then "15 live terminals" (self-inconsistent: 17 includes the 2 routers).
- **usage() doesn't list dublin-grown** [codebase]; **`dublin_shot_capture` "topology is EMPTY" comment stale for the grown caller** [codebase].
- **Spec pin 1 zero-tile clause untested** (holds by construction) [acceptance]; **permille exercised only at 1000** — floor branch + the 667 iteration target untested [tests].
- **[unverified] Spec's 602/518 pool counts contested (603/517 claimed)** — not mechanically reproducible in review scope; run the loader census once and correct the spec.
- **dublin .t1 re-bless shape cannot distinguish the draw-shift from a pure hash re-salt** [blind] — the cause attribution rests on code reading (verified in this review: SEED 2-draw structure + weighted cluster pick) + the 2 PNGs; transparency note.
- **run_dublin_grown is the 5th hand-rolled `Demo_Replay` construction** [architecture, premise-corrected] — no shared helper exists to fork (the "forks a shared path" framing was rejected on verification); 5 copies invite field drift.

### Reviewer agreement

Six lenses independently converged on the 117/119-vs-113 miscount; three on the ATTACH bias-pin blocker; two each on the cross-boundary cap gap, the jint leniency, the partition copy-paste, the fractional-anchor gap, and the audit-header mislabel. Every finding above was re-verified against the reviewed worktree (4 lens claims discarded as false-positives — including a phantom load-fail leak and an "unpinned hash fold" whose regression would fail all 100 goldens loudly).

**Canon checks (mechanical):** `dublin.json` rulings `density_default: "1in6"` ✓ at source · caps = pool share × permille/1000 ✓ (audit: live 1–2 vs caps 4–67) · 3× size-5 estates seed-anchored Rialto/Clonskeagh/Artane ✓ · LOG_VERSION untouched ✓ · stage-2 scope respected (no streets-constrain-pipes, no last-mile) ✓ · fail-fast rows delivered (cap 1..1000, weights 0..1000, named errors) ✓.

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
