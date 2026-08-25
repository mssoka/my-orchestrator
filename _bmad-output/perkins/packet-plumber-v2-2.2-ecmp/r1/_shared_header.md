You are ONE lens of an automated code review (Perkins round 1) of PR #26 in solarity-services/Packet-Plumber: **v2 Story 2.2 — ECMP across equal-cost next hops.** You review; you NEVER edit, push, or merge.

**Read these (your inputs):**
- DIFF (the canonical bytes under review): `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.2-ecmp/r1/diff.patch`
- WORKTREE = your cwd (detached at sha a1c6e64): `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-2.2-ecmp-r1` — verify claims by reading files here.
- SPECS: Story 2.2 card `/Users/moses/code/packet-plumber/_bmad-output/planning-artifacts/sprints/stories-v2.md` (search "Story 2.2"); architecture `/Users/moses/code/packet-plumber/_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` (4-rule spine, ODN-9/10, E10).

**What the PR does:** among N equal-cost next hops the pick is a PURE hash `splitmix64(src,dst,class,pkt_id) mod N`. Changes: `core/routing.odin` (table restructured single-next-hop → equal-cost-set: `Hop{node,pipe}`, `hop_offset/hop_count/hops` arrays, BFS-per-destination collecting neighbors one hop closer; new `ecmp_hash`/`ecmp_pick`), `core/flow.odin` (hot path: `routing_equal_cost_hops` + `ecmp_pick`), `core/ecmp_test.odin` (new, 7 tests).

**🚨 LENS-GUARDS — load-bearing invariants (already verified GREEN by Perkins; do NOT re-flag as defects, but DO flag any REAL violation):**
1. PURE HASH / NO SIM-RNG (4-rule spine rule 2): pick = `splitmix64(src,dst,class,pkt_id) mod N`, a pure function of identity. A sim-rng draw (`rng_next`/`rng_range`/`state.rng`) in the routing path = real blocker. (Verified: `ecmp_hash` calls `splitmix64` on a LOCAL u64; `splitmix64` in rng.odin is pure.)
2. NO MAP ITERATION in the hot path — equal-cost set is array-indexed (`hops[offset+hash%count]`). Map iteration = real blocker. (Verified clean.)
3. FLOW AFFINITY — same `(src,dst,class,pkt_id)` → same path every replay. (Verified: `ecmp_pick` pure; test passes.)
4. DETERMINISM (E10/ODN-9/10) — per-packet paths ride the T1 hash; replay byte-identical; routing table is DERIVED (not serialized). A serialized routing state or replay divergence = real blocker. (Verified.)
5. CORE ENGINE-FREE (ODN-1) — these files are `package core`; an engine type leaking in = real blocker. (Verified clean.)
6. BACKWARD-COMPAT (count==1 reproduces slice-1/2.1 single-hop) is a FEATURE — do NOT flag "missing re-blessed goldens." (43/43 tests pass.)
7. T2 PIXEL HARNESS GAP is a DOCUMENTED CARRY-FORWARD (a mini-story recommendation), NOT a defect — do NOT flag as a blocker.
8. Em-dashes are FINE in Packet-Plumber copy. Base is `v2`. The prototype is reference-only. Do NOT re-open merged 1.1–2.1 findings.
9. The implementing minion hit/recovered a bmad-tooling quirk (edits briefly mis-resolved to the main checkout, caught + corrected) — review the PR content AS-IS at the sha; do not flag the recovery.

**Legitimate findings here would be:** a sim-rng draw in routing; map-iter in the hot path; flow affinity broken; a determinism break; an engine type in `package core`; an `odin test`/`odin build` failure; a real bug or unhandled path the tests miss; an AC not actually met.

**OUTPUT CONTRACT — write ONE valid JSON array to the exact path named in your lens file.** Per-element schema:
`{source, severity (blocker|warning|note), category, title, location (file:line|hunk|N/A), evidence (the EXACT lines you READ, verbatim — 'N/A' only when no code reference is possible), detail (≤40 words), recommended_fix (≤40 words)}`
- ONLY the JSON array in the file. No prose, no markdown fencing, no preamble. Empty `[]` is valid + expected when clean.
- **ACCURACY MANDATE:** Perkins re-verifies every finding against the code; unverifiable findings are DISCARDED silently. Open the file, read the lines, quote them verbatim in `evidence` or drop the finding. Hedging ("might/could/possibly") = not verified = drop it. Accuracy > volume.
- After writing the file, stop. Do nothing else.
