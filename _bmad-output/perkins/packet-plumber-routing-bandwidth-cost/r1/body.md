## 🤖 Perkins automated review — round 1 of 3
**Job:** packet-plumber-routing-bandwidth-cost · **Reviewed sha:** 32a1b65 · **Reviewers:** 7/7 completed
**Verification:** 25/27 findings confirmed against the code — 2 discarded as false-positive

### Blockers (0)

### Warnings (2)

**1. Mixed-tier bundle min-cost pricing branch has no dedicated pin — the re-pricing path (a cheaper later member) never executes in any test or demo** *(tests)*
`core/routing.odin:221-225` · vs `demos/bundle.dem` (parallel pipes, both standard)

The four contract pins cover mixed-tier PATHS but never a mixed-tier BUNDLE: the `else if c < min_cost[ns]` re-pricing branch (a fatter later member re-pricing a bundle edge) runs in no test and no demo — bundle.dem's parallel pipes are standard+standard, so min == representative cost everywhere. **I independently fuzz-verified the branch's correctness**: 400 random graphs (2–6 nodes, random tiers, including parallel mixed-tier bundles), 5,482 (u,d) pairs against a reference Bellman-Ford with min-edge-cost semantics — 0 mismatches. The code is right; the regression pin is missing.
**Fix:** one pin: parallel narrow(20)+wide(5) pipes between a pair, assert the edge prices at min member (5), the ECMP/next-hop reflects it, and the representative `Hop.pipe` stays the lowest-slot member.

**2. Advisory test gate: CONCERNS** *(tests)*
P0 100%: all four contracts (fat-path unique hop, TRUE different-tier equal-sum tie → ECMP 2, re-step byte-identity, ladder-read-from-data) + the ODN-5 reject rows (cost 0/negative/missing/decimal) are pinned and green (`odin test core` 126/126). P1 ~90%: the single gap is the mixed-tier bundle pin above; overall ≥90%. (The lens filed FAIL counting the bundle branch as P0; I re-gated after the fuzz verification.)

### Notes (4)

1. **Frozen spec §Changes-2 prices the bundle edge at the representative (lowest-slot) pipe's tier cost; the implemented Dijkstra (and decision-log + arch §6.2) price it at the MIN member cost** *(acceptance, architecture, blind, codebase, edge, tests — 6-lens agreement)* — `spec-routing-bandwidth-cost.md:29-31` vs `core/routing.odin:215-238`. For a narrow-then-wide bundle the spec prices the edge at 20, the code at 5; the code matches the canon docs. Reword the spec line: edge cost = the MINIMUM tier cost among live pipes toward the neighbor (fattest member); the lowest-slot representative only records `Hop.pipe`.
2. **No upper bound on the tier `cost`** *(security, blind, edge, acceptance, architecture, tests — 6-lens agreement)* — `core/catalog.odin:343` + `core/routing.odin:178`. `jint_strict` admits cost = i32::MAX; two such hops wrap `nd` negative and a wrapped −1 collides with the UNREACHABLE sentinel, silently erasing routes. Reachable only with absurd catalog data (the shipped 20/10/5 ladder is safe) and explicitly deferred in this PR's `deferred-work.md` — add the ≤1e6 cap at the balance gate.
3. **Tie pin dereferences `hops[off+1]` after a non-fatal count check** *(blind)* — `core/routing_cost_test.odin:105-108`. A regression that breaks the ECMP count still fails the run, but via an out-of-bounds panic (or a mis-read of the adjacent row) instead of the pinned message. Guard the node asserts with the count condition.
4. **ecmp_cost.dem diamond B's sink (host2 at grid x=48) is outside the 40-tile map** *(edge)* — `demos/ecmp_cost.dem:47`. `topology_spawn_node` has no map-bounds check (only player placement does), so host2 screens at x≈1312 > the 1280 window and both captures crop the sink + the second-hop leg tips. The t23 sim state does carry a packet on each second-hop leg (my flow dump: pkt 2 on r1→host2, pkt 4 on r2→host2 — the tie split is real), but both sit at progress 0/30, which the lerped render draws at the departure nodes — "mid-edge" is generous for that frame. Shift diamond B inside the map and soften the comment wording.

### Reviewer agreement
- **Spec-wording drift (representative vs min-member)** — acceptance + architecture + blind + codebase + edge + tests
- **Missing cost upper bound (i32 overflow)** — security + blind + edge + acceptance + architecture + tests

### Golden discipline (verified clean, independently)
- **Splice proof REPRODUCED**: all 16 demos — the new goldens are reproducible tick-for-tick at this sha, and folding the OLD catalog_hash (`8da858ab04b113db`) into the new dump's fixed byte slot 33 reproduces the OLD golden's hash EXACTLY on all 15 re-blessed demos (every tick, including qos/surge's thousands). Zero non-catalog-hash byte delta = zero behavior shift.
- All 15 `.log.bin` diffs = exactly 8 bytes at offset 18 (the catalog_hash header field). No seed/ticks/hash-count drift; all 16 manifests carry one consistent new hash `0a6324230ab9dcba`. No existing T2 PNG changed; `harness run` green = T2 byte-identical for the existing demos; `ecmp_cost`'s goldens are new files.
- **Gates**: `odin test core` 126/126 (4 new pins) · `tools/lint.sh` 6/6 · `tools/harness.sh run` 16/16 (T1+T2+replay) · `drift-check` 111/111 rejected · `odin build app` green. LOG_VERSION stays 3; no new commands; `flow.odin` forward pass untouched; the table stays derived-not-serialized; `ecmp_pick`/`ecmp_hash` byte-identical.
- 2 lens findings rejected as false-positives: (a) "OQ-5 register note missing" — the arch register entry #5 (routing-model ruling) IS amended in this PR's diff; (b) "t23 capture shows no packet on r2→host2" — the flow dump disproves it (both second-hop legs carry a packet at t23).

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
