## 🤖 Perkins automated review — round 1 of 3
**Job:** packet-plumber-v2-5.1-map-growth · **Reviewed sha:** `ef858e8` · **Reviewers:** 7/7 completed
**Verification:** 18/20 findings confirmed against the code — 2 discarded as false-positive

Independently re-run at the sha (ground truth): **177/177 core tests · 28/28 demos green (T1+T2+replay) · 196/196 drift mutations rejected (incl. `growth_flip`) · growth stats-check live==replay byte-identical · lint 6/6 · app build green · goldens additions-only (catalog_hash unchanged, data/ untouched).**

### Blockers (0)

None. The determinism spine holds (growth derives purely from seed + executed tick; replay byte-identical with zero log bytes, no LOG_VERSION bump), E31 is enforced (in-bounds + integer min-sep nodes/segments + connectable-within-span, bounded rejection from the same stream), routers are never director-spawned, and golden stability is intact.

### Warnings (5)

1. **['E31 by construction' comment is false for diagonal draws](core/growth.odin#L319-L323)** — 4 of 8 compass dirs land up to √2·span from the picked router; E31 actually holds via the `growth_connectable` re-check (verified: all gates green). The comment risks a future "redundant check" deletion breaking E31, and diagonal draws at dist > span/√2 are guaranteed rejects (cardinal bias — growth.dem windows 840+900 exhaust). *Fix the comment; optionally bound diagonal dist.* [blind+acceptance+architecture]

2. **[growth_flip drift class spuriously FAILs a never-spawning growth demo](harness/drift.odin#L88-L94)** — the parser deliberately permits no-junction growth demos ("growth legitimately waits"), and a run capped before tick 120 never opens a window; either way the flipped replay equals the manifest → false "gate ACCEPTED a growth-flipped replay" on a valid demo. Latent (growth.dem doesn't trigger it). *Skip the class when the blessed run spawned zero growth terminals.* [blind+edge]

3. **[Cross-seed divergence assertion is vacuous w.r.t. growth](core/growth_test.odin#L375-L383)** — full-state hashes diverge for any two seeds regardless of growth; seed-99 positions (`nc`) are computed then discarded (`_ = nc`). A growth implementation ignoring the rng stream entirely still passes. *Assert `na` vs `nc` positions differ.* [tests+blind]

4. **[Era-parse fail-loud guard has zero test coverage](harness/demo.odin#L532-L534)** — the `growth on` + era-0 rejection (a claimed swarm fix) has no pin; the harness package has no test files at all. *Add a `parse_demo` unit test for the rejection string.* [tests]

5. **Advisory test gate: CONCERNS** — P0 100% (replay identity, same-seed identity, E31, terminals-only, legacy-inert — all pinned, re-run green); P1 ≈88% (warnings 3+4); overall ≈82%. *Fixing 3+4 lifts the gate to PASS.* [tests]

### Notes (8)

1. [Stale doc comment above `count_terminals`](core/growth_test.odin#L40-L42) names a nonexistent proc (`spawned_terminals`) and wrong return shape. [blind+codebase]
2. [Sibling separation predicates handle `sep < 1` oppositely](core/growth.odin) (clamp-to-1 vs no-constraint) — unreachable today (const 3), asymmetric for future callers. [blind]
3. [Tick 0 aliases `growth_last_tick`'s zero value](core/step.odin) — a tick-0 step would silently skip a spawn window. Verified unreachable: every caller steps from tick 1 (record_run `1..=`, harness/app pre-increment); even if stepped, live+replay skip symmetrically. [blind]
4. [`growth_connectable` ignores junction port capacity](core/growth.odin#L210-L225) — spec-compliant (E31 is span+separation; port limits are 3.5 canon applied at draw; the game-loop answer is player expansion — no hard soft-lock). Design observation. [edge]
5. ['Read-only … structural, same as demand.odin' misstates](core/growth.odin#L15-L17) — demand.odin takes no topology handle (structural); growth takes `^Topology` (discipline, verified read-only). The snapshot seam is [LATER] per 3.1; the comment overclaims. [acceptance]
6. [`e31_recheck` doesn't skip pipes incident to the audited spawn](core/growth_test.odin#L109-L127) — a pipe drawn to a growth spawn has distance 0 → false "violates E31" once any future test/demo connects one. Latent test-helper trap. [acceptance]
7. [growth.dem "after the last spawn at t1680" is wrong](demos/growth.dem#L26) — independently verified via the stats stream: gen 19→20 at tick 1800 (a 15th spawn, T1-pinned only). [codebase]
8. [E31 exhaustion branch not unit-pinned](core/growth.odin#L318) — mitigating: it IS exercised end-to-end by the golden (windows 840+900 deterministically skip — verified). [tests]

### Reviewer agreement

- "E31 by construction" comment false for diagonals — blind + acceptance + architecture (3 lenses)
- growth_flip drift spurious FAIL — blind + edge
- Cross-seed divergence vacuous — blind + tests
- Stale `count_terminals` doc — blind + codebase

**Verdict:** READY TO MERGE

_All blockers none; the 5 warnings are doc-accuracy, latent-test-trap, and coverage-depth items — none touch the determinism spine, E31 enforcement, or golden stability, all of which were independently re-verified green at the sha._

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
