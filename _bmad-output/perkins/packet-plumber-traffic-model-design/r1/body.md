## 🤖 Perkins automated review — round 1 of 3
**Job:** packet-plumber-traffic-model-design · **Reviewed sha:** 7214204 · **Reviewers:** 7/7 completed
**Verification:** 25/29 findings confirmed against the code — 4 discarded as false-positive

Docs/canon-only diff (spec + GDD M6 + decision log + sprint-plan row + story cards 5.9–5.12) verified against the worktree at the reviewed sha. Scope guard holds: no code, no balance.json changes; GDD edit is section-additive (no terminology rewrites). The four threads, determinism spine, E31 conflict resolution, and sequencing rationale are sound in shape — the blockers below are numeric/mechanism defects inside that shape, all fixable in the docs.

### Blockers (2)

1. **Fractional cap unenforceable as specified** — card 5.9's When ("volume would assign more spawns to one terminal than its cap this tick") cannot enforce a 0.2 pkts/tick cap: spawns are integer per tick (`core/flow.odin:645` `for k in 0..<vol`), so a per-tick compare against 0.2 rejects **every** residential spawn — email never lands. No accumulator/token-bucket semantics (or its run-state home + T1/determinism implications) are specified anywhere; the spec's own `(20 ÷ cap)` formula only coheres with rate semantics. *Fix: specify the enforcement mechanism (per-terminal spawn accumulator, credit = cap/tick, spawn costs 1; state home + hash surface named) or an integer form (1 spawn per N ticks) in Thread 2 + card 5.9.*

2. **Proposed cap value violates the load-bearing invariant at its own starting numbers** — 0.2 pkts/tick ≈ 6 u/s exceeds the residential node's throughput (5 u/s = 0.167 pkts/tick, `data/node_types.json`) and the pre-5.10 narrow service rate. 5.9 lands **before** 5.10's resize, so at 5.9's own launchable increment ("no residential is ever the drop site") the capped 0.2 arrival against a 5 u/tick access link backlogs and E9 sheds at the endpoint's own access lane — the exact self-congestion noise M6 exists to kill. Also inconsistent with the spec's own per-type rule (content_host caps **at** its throughput 2.67; residential would cap 1.2× **above** its). *Fix: cap ≤ node throughput with headroom computed from that, or land 5.9+5.10 as one unit; apply caps-against-throughput uniformly.*

### Warnings (9)

3. **Dead provenance link (4 reviewers agree)** — three canon docs cite `_bmad-output/implementation-artifacts/surge-explainer/surge-explainer.html` as the ruling's primary source; it is not in the repo and never was (`git log --all` empty). Commit the artifact (or a §B excerpt) or repoint the citations.
4. **GDD tier numbers unreconciled in the GDD** — M1/Numerical-Design tables (10/25/50/120) vs new M6 (shipped 5/15/40, narrow → 8–10); the reconciliation flag lives only in spec §1. Add one additive sentence (M6 block or decision log) marking the M1 row aspirational, catalog ground truth.
5. **Group radius collides with GROWTH_MIN_SEP_TILES=3** — a 2-tile-radius biased candidate is always E31-invalid (min-sep covers nodes AND pipe segments, `core/growth.odin:76`), so the bias silently no-ops; the conflict-resolution section addresses ordering, not this constant. Radius ≥4 or document the packing consequence.
6. **Sink-side concentration unbounded** — caps bind source spawning only; the ×10 surge onto few residential sinks still drops at the endpoint's own access pipe (inbound), falsifying the absolute claim. Bound dst picks or scope the invariant to source-side explicitly.
7. **"A data change, not a code change" is false** — `Terminal_Role` is a closed enum (`core/catalog.odin:22`); new roles fail catalog load and cap/profile fields are inert until loader code reads them. Qualify in GDD M6/spec/card 5.11 and name the touch points.
8. **"The six GDD mechanics" count collision** — slice-8+ row now vs a GDD with literally six M-blocks, M6 pre-gate. Addive rename/clarification needed in the sprint plan or decision log.
9. **5.9's "surge still lands" acceptance unpinned** — its own named failure mode (silent non-landing) is undetectable via re-bless; canon says acceptance criteria become durable tests. Pin a post-cap surge-volume assertion.
10. **5.10's headroom invariant unpinned** — 5.11/5.12 each name a pinning golden; 5.10 uniquely has re-bless only. Add a one-subscriber-at-cap zero-drop scenario.
11. **Advisory test gate: CONCERNS** — P0 seams 100% pinned; P1 pin coverage ≈83% (4/6 FULL, 2 PARTIAL — the two warnings above).

### Notes (9)

12. Residential-share derivation misattributes streaming volume (streaming sources from content_host; residential's era-3 share is the email 4/tick ≈ 0.13).
13. Access-tier headroom assumes exactly one access pipe — state the invariant's unit (per-bundle) and the dual-homed case.
14. "One re-bless at the slice boundary" vs each card's own mandated re-bless — reword to one cause-family, four bless events.
15. Card 5.9's Systems line names demand.odin; the spawn pass lives in flow.odin §1b (demand.odin is structurally topology-blind).
16. Card 5.10's `[E3]` tag is wrong (E3 = self-loop rejection; span rules carry no E-tag).
17. Group-membership derivation owner unpinned for its two consumers — pin one shared derived view (the lane_caps pattern).
18. SLA identity miscited as (E24) — E24 is zero-demand-neutral; the pin is `core/sla_test.odin` `sla_check_invariant`.
19. Hard-wrapped code-span path in stories-v2 5B intro (renders with a space mid-path).
20. Sprint plan gains the 5B row but no §3 section (every other MVP slice has one).

### Reviewer agreement
- Dead provenance link: **4 independent lenses** (edge, acceptance, architecture, codebase) — highest confidence in the report.
- GDD tier-table contradiction: architecture + acceptance.
- Wrapped path: blind + codebase.

**Verdict:** NEEDS CHANGES

_The design's shape — four threads, Given/When/Then, E31 conflict resolution, determinism spine, sequencing — is approved direction; the two blockers are spec-internal numeric/mechanism defects (cap enforceability + cap-vs-throughput) that must be fixed in the docs before the story cards dispatch. Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
