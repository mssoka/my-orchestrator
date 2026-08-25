# Lens: Acceptance Auditor (Perkins r1 — packet-plumber-v2-2.1-bundles)

Audit the diff against the spec. Identify: violations of specific acceptance criteria, deviations from spec intent, missing implementation of specified behavior, contradictions between spec constraints and actual code, scope drift (changes not asked for by the spec).

## Inputs
- **Diff:** `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.1-bundles/r1/diff.patch`
- **Worktree (verify here):** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-2.1-bundles-r1`
- **Spec (read all):**
  - `/Users/moses/code/_bmad-output/briefings/perkins-packet-plumber-v2-2.1-bundles-r1.md` (this round's spec + lens-guards)
  - `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-2.1-bundles.md` (the job briefing — full AC)
  - Worktree `project-context.md` (ODN rules)
  - Worktree `_bmad-output/planning-artifacts/sprints/stories-v2.md` → **Story 2.1** (the Given/When/Then + edge-case contracts)
  - Worktree `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` → **ODN-9/10/11** and the **4-rule spine** (lines ~643–690; rule 3 = "bundled capacity is a static sum at table-build time")

## The acceptance criteria (from Story 2.1)
- Parallel pipes between a node pair **bundle into one pooled-capacity link (cap = sum of members)**.
- Capacity is a **static sum at table-build time** (4-rule spine rule 3) — computed once, not per-packet, not mid-flow.
- Drawing a second parallel pipe → the two bundle, with a **merge "pop" animation**.
- Routing sees **one fat edge per pair**; **NO load balancing** (round-robin/weighted LB deleted, grep-gated absent) `[RR]`.
- **bundle-capacity-equals-sum unit test passes.**
- **Golden: T1 (bundle state in the hash) + T2 (the merge-pop frame).**
- **Carry-forwards W1/W2 from 1.4:** a headless app-layer restart test (restart → fresh seed, full FSM cycle, no state leakage) AND a LOSE-loop replay test (losing run replays byte-identical).
- `odin test` + `odin run harness` green; core still engine-free (ODN-1).

## ⚠️ Lens-guards (DO NOT flag these as defects — they are the spec)
- **NO LB is the requirement.** Pooling (cap = sum, served whole) is the locked model. Absence of round-robin/weighted LB is CORRECT. (A stray LB pattern sneaking in, or the grep-gate failing to catch one, WOULD be a real blocker.)
- **Bundle state is DERIVED, not serialized** — "bundle state in the hash" (T1 golden) is satisfied by the composing pipes being serialized; the Bundles struct re-derives on replay. This is the architecture's stated design (same as the routing table). Do not flag it as missing.
- **`Packet.edge` = a representative pipe id** is by design.
- **ECMP (next story 2.2) is OUT of scope** — this story has NO per-pipe pick at all (single-path representative). Do not flag "no ECMP."
- **The 2.3 severance concern** (rep pipe demolished, bundle survives, Packet.edge stale) is a documented carry-forward NOTE for story 2.3 — NOT a 2.1 defect.
- Do not re-open 1.1–1.4 (merged, Perkins-verified). Do not flag em-dashes, the `v2` base, or "should port the prototype."

## OUTPUT
Write ONLY a valid JSON array to: `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.1-bundles/r1/acceptance.json`
Schema per finding:
```
{ "source":"acceptance", "severity":"blocker"|"warning"|"note", "category":"<tag>",
  "title":"<one-line>", "location":"<file:line|hunk|N/A>",
  "evidence":"<exact lines READ from worktree/diff, verbatim; quote the violated AC phrase where possible>", 
  "detail":"<≤40 words, reference the violated AC>", "recommended_fix":"<≤40 words>" }
```
ONLY the JSON array in the file. `[]` is valid. Accuracy > volume — verify each claim against the actual code before emitting it. When done: "acceptance lens done — N findings".
