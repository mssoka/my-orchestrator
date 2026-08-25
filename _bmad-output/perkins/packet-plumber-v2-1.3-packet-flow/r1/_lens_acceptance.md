# Lens: acceptance (Acceptance Auditor) — Perkins r1

**OUTPUT FILE:** `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.3-packet-flow/r1/acceptance.json`

First read the common context:
`/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.3-packet-flow/r1/_lens_common.md`

## Your lens
Audit the diff against the spec (Story 1.3 + the architecture §6.2 / 4-rule
spine / ODN-9/10/11). Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

Story 1.3 acceptance (from the story card + architecture):
1. Packet spawns from trivial hardcoded demand, travels source→router→sink,
   forwarded **per-hop** via a forwarding table — single-path (no ECMP/bundles,
   no spawn-cached BFS route, no LB).
2. Forwarding table **rebuilt only on a topology-changing Command, synchronously
   inside the tick** (4-rule spine rule 1) `[ODN-10]`.
3. Packet path captured in the state hash → replay-equality holds `[E10]`.
4. On a demolish that severs the path, packet re-forwards at the next junction
   (no stale spawn-time route) `[E29]` — **NOTE: demolish is Story 2.3; 1.3
   delivers the MODEL that makes E29 automatic (no cached route). Do NOT flag
   "E29 not implemented" — flag only if the per-hop MODEL is broken.**
5. Golden: T1 (packet path in hash) + T2 (mid-traversal frame) + a
   forwarding-table-rebuild-on-topology-change unit test.

For each finding, reference the violated AC or constraint in `detail` (quote the
exact spec phrase when possible). Respect the lens-guards in the common context.

## Output
Write ONE valid JSON array to your OUTPUT FILE (source = `"acceptance"`). `[]`
is valid. Accuracy > volume. Then print `LENS DONE: acceptance` and stop.
