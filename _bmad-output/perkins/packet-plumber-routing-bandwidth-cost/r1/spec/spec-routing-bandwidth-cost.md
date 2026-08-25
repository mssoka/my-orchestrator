---
status: done
job: packet-plumber-routing-bandwidth-cost
slug: routing-bandwidth-cost
base: v2
baseline_commit: 094bc8a46cd044f574c49ff143d0af2de9a482d6
canon: _bmad-output/problem-solution-2026-08-13.md (problem-solution-2026-08-13)
---

# Spec — Job A: capacity-cost routing (the canon amendment)

## Goal

Wire STATIC pipe-tier cost into the locked routing model (canon #18 / routing
ruling lavish 2026-08-10; `core/routing.odin`, arch §6.2): path cost = tier
`cost` (fixed at draw time — never dynamic utilization), intent = "flows
prefer fat pipes"; equal END-TO-END cost → ECMP (pure hash, unchanged). One
player line: "packets take the fattest route; equal cost splits by hash".
Jobs B (assist/glow/tie-cue) and C (forecast flow-shift) are OUT of scope.

## Changes

1. **Data (ODN-5)** — `data/pipe_tiers.json`: add `cost` per tier
   (narrow 20, standard 10, wide 5), integer, `cost >= 1` validated at
   catalog load (zero-cost edges break the per-hop progress guarantee —
   reject at load: `core/catalog.odin` `Pipe_Tier.cost` field + the
   pipe_tiers validation block).
2. **Core** — `core/routing.odin` `routing_rebuild`: unit-weight BFS →
   Dijkstra over integer pipe costs (edge cost = representative pipe's tier
   `cost` via `Topology.pipe_tier` → catalog; the representative is the
   lowest-slot live pipe toward the neighbor — matches `Hop.pipe`). Array-
   backed cheapest-first min-scan with insertion-order (slot-order)
   tie-breaks; NO map iteration, NO floats, NO rng draws. Equal-cost
   condition becomes `dist[v] + cost(pipe) == dist[u]`; the ECMP set is the
   neighbors satisfying it. `routing_equal_cost_hops` (offset, count) shape
   unchanged. Signature gains `cat: ^Catalogs` (caller: `core/step.odin`
   rebuild site, which already holds `cat`).
3. **KEEP LOCKED** — `ecmp_pick`/`ecmp_hash` untouched; rebuild-only-on-
   topology-change (static weights ⇒ automatic, pure function of Topology);
   table stays DERIVED (not serialized into T1); `flow.odin` forward pass
   untouched (same `(offset, count)` lookup + `ecmp_pick`).
4. **Core tests** — new `core/routing_cost_test.odin`:
   (a) mixed-tier diamond picks the fat path as a UNIQUE next hop (no ECMP
   when costs differ); (b) different-tier equal-sum tie → ECMP set of 2
   (standard(10)+wide(5) vs wide(5)+standard(10)); (c) re-step determinism
   byte-identical (record_run ×2 over a mixed-tier topology); (d) ladder
   read from data: mutate `cat.pipe_tiers[].cost` in a test catalog →
   routing behavior moves (proves ODN-5 wiring). Update
   `core/determinism_test.odin::test_catalog` Pipe_Tier literals with
   costs 20/10/5; update `core/catalog_test.odin` TIER_VALID fixture +
   a reject pin for `cost < 1`.
5. **Demo + goldens** — new `demos/ecmp_cost.dem` (mixed-tier diamond):
   captures pin the fat-path UNIQUE hop mid-flight AND a true different-tier
   tie split; `expect hash stable`. NEW golden files only
   (`goldens/ecmp_cost.*`). Existing demos: all standard-tier or single-path
   ⇒ routing behavior byte-identical. T1 `.t1`/`.log.bin` re-bless is the
   MECHANICAL catalog_hash fold (adding `cost` changes `cat.hash`, which
   rides every per-tick state hash + the log header) — same defined
   re-bless class as 3.2/4.1/4.2, cause-documented in the PR body; T2
   pixels must stay byte-identical (negative proof).

## Acceptance

- `odin test core` green (incl. the 4 new pins + catalog reject pin).
- `tools/lint.sh` 6/6 green.
- `tools/harness.sh run` — 15 existing + ecmp_cost green; T2s byte-identical
  except ecmp_cost's new ones; drift-check green.
- Determinism: re-step byte-identical (test (c) + harness replay gate).
- New pins pass on CI matrix (linux/macos).
- Docs in the SAME PR: arch `odin-architecture-v1.md` §6.2 routing model +
  ODN-10 routing-spine wording + OQ-5 register note; GDD routing section
  one-line rule + assist-features note; decision-log 2026-08-13 entry.
- No new commands (LOG_VERSION stays 3), no per-class routing, no dynamic
  cost, no `ecmp_*` changes.

## Verify

Baseline (pre-change): odin test 122 green · lint 6/6 · harness 15/15 +
drift green. Post-change: diff-bundle first if ANY existing golden shifts
beyond the catalog_hash fold; prove T2 byte-identity; PR body carries the
launchable increment (mixed-tier map story) + Decisions & rationale.

## Suggested Review Order

**The cost model (design intent)**

- Dijkstra replaces BFS: array min-scan, insertion ties, min-cost bundles
  [routing.odin:98](../../core/routing.odin#L98)

- Header comment: the capacity-cost model + spine restated
  [routing.odin:13](../../core/routing.odin#L13)

**Data + validation (ODN-5)**

- Ladder 20/10/5 in the catalog (the player-summable near-inverse)
  [pipe_tiers.json:8](../../data/pipe_tiers.json#L8)

- jint_strict: decimals/wrong types reject, missing -> 0 -> >= 1 rejects
  [catalog.odin:334](../../core/catalog.odin#L334)

- New field on the tier struct
  [catalog.odin:41](../../core/catalog.odin#L41)

**Core tests (the 4 pins)**

- Fat-path unique hop (no ECMP when costs differ)
  [routing_cost_test.odin:51](../../core/routing_cost_test.odin#L51)

- TRUE different-tier tie -> ECMP set of 2
  [routing_cost_test.odin:85](../../core/routing_cost_test.odin#L85)

- Re-step determinism byte-identical over the cost model
  [routing_cost_test.odin:113](../../core/routing_cost_test.odin#L113)

- Ladder read from data: a catalog mutation moves routing
  [routing_cost_test.odin:168](../../core/routing_cost_test.odin#L168)

- Catalog reject pins (cost 0/negative/missing/decimal)
  [catalog_test.odin:258](../../core/catalog_test.odin#L258)

**Demo + golden discipline**

- Mixed-tier diamond: fat-path + tie captures, expect hash stable
  [ecmp_cost.dem:1](../../demos/ecmp_cost.dem#L1)

- Canon docs: arch §6.2 cost model + GDD player rule + decision-log entry
  [odin-architecture-v1.md:964](../../_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md#L964)

- GDD: the one-line player rule + assist-features note
  [gdd.md:231](../../_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md#L231)
