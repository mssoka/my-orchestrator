#!/usr/bin/env python3
"""Consolidated findings for packet-plumber-routing-bandwidth-cost r1 (post-verification)."""
import json

OUT = "/Users/moses/code/_bmad-output/perkins/packet-plumber-routing-bandwidth-cost/r1"

def f(sources, severity, category, title, location, evidence, detail, fix, verification):
    return {"sources": sources, "severity": severity, "category": category, "title": title,
            "location": location, "evidence": evidence, "detail": detail,
            "recommended_fix": fix, "verification": verification}

warnings = [
    f(["tests"], "warning", "coverage-gap",
      "Mixed-tier bundle min-cost pricing branch has no dedicated pin — the re-pricing path (a cheaper later member) never executes in any test or demo",
      "core/routing.odin:221-225 (pass 1 re-pricing) — vs demos/bundle.dem (parallel pipes both standard)",
      "core/routing.odin:222-225: `if !seen[ns] { seen[ns] = true // first (lowest-slot) pipe to this neighbor wins the representative slot / min_cost[ns] = c } else if c < min_cost[ns] { min_cost[ns] = c // a fatter (cheaper) member re-prices the edge }`; demos/bundle.dem:13-14: `at 500ms draw 0 1 standard` / `at 2500ms draw 1 2 standard` — the only parallel-pipe demo, both members standard (min == representative cost, the else-branch never runs).",
      "The four contract pins cover mixed-tier PATHS but never a mixed-tier BUNDLE (parallel pipes of different tiers between one pair); the re-pricing branch is unexercised by every test and demo. Perkins' independent fuzz (400 random graphs, 5,482 (u,d) pairs, incl. parallel mixed-tier bundles, vs a reference Bellman-Ford) matched the table exactly — the code is correct; only the regression pin is missing.",
      "Add one pin: parallel narrow(20)+wide(5) pipes between a pair, assert the edge prices at min member (5), the ECMP/next-hop reflects it, and the representative Hop.pipe stays the lowest-slot member.",
      "confirmed"),
    f(["tests"], "warning", "coverage-gate",
      "Advisory test gate: CONCERNS",
      "N/A",
      "N/A",
      "P0 100%: the four contracts (fat-path unique hop, TRUE different-tier equal-sum tie -> ECMP 2, re-step byte-identity, ladder-read-from-data) + the ODN-5 reject rows (cost 0/negative/missing/decimal) are all pinned and green (odin test core 126/126). P1 ~90%: the single gap is the mixed-tier bundle min-cost pin (see the warning above); overall >= 90%. Perkins re-gated from the lens's FAIL (which counted the bundle branch as P0) after independently fuzz-verifying the branch's correctness.",
      "Add the mixed-tier bundle pin to reach PASS.",
      "confirmed"),
]

notes = [
    f(["acceptance", "architecture", "blind", "codebase", "edge", "tests"], "note", "doc-accuracy",
      "Frozen spec §Changes-2 prices the bundle edge at the representative (lowest-slot) pipe's tier cost; the implemented Dijkstra (and decision-log + arch §6.2) price it at the MIN member cost",
      "_bmad-output/implementation-artifacts/spec-routing-bandwidth-cost.md:29-31 vs core/routing.odin:215-238",
      "spec-routing-bandwidth-cost.md:29-31: `edge cost = representative pipe's tier `cost` via `Topology.pipe_tier` → catalog; the representative is the lowest-slot live pipe toward the neighbor — matches `Hop.pipe``; core/routing.odin:222-225: `else if c < min_cost[ns] { min_cost[ns] = c // a fatter (cheaper) member re-prices the edge }`; arch §6.2: `A mixed-tier bundle prices at its fattest member (min member cost — the same member the bundle renders at its highest tier)`; decision-log 2026-08-13: `A mixed-tier bundle prices at its fattest member (min member cost ...)`.",
      "6-lens agreement. For a narrow-then-wide bundle the spec prices the edge at 20, the code at 5; the code matches the canon docs (decision-log + arch §6.2 + the routing.odin header comment). The frozen spec line is the outlier — a pure doc-accuracy fix, no behavior change.",
      "Reword spec Changes §2: edge cost = the MINIMUM tier cost among live pipes toward the neighbor (fattest member); the lowest-slot representative pipe only records Hop.pipe.",
      "confirmed"),
    f(["security", "blind", "edge", "acceptance", "architecture", "tests"], "note", "validation-gap",
      "No upper bound on the tier `cost` — a pathological ladder value passes load and can overflow the i32 dist accumulation in routing_rebuild (documented + deferred)",
      "core/catalog.odin:343 + core/routing.odin:178 (tracked in _bmad-output/implementation-artifacts/deferred-work.md)",
      "core/catalog.odin:343: `if t.id == \"\" || t.capacity_units <= 0 || t.max_span <= 0 || t.cost_per_tile < 0 || t.cost < 1 {`; core/catalog.odin:869: `if i < i64(min(i32)) || i > i64(max(i32)) {`; core/routing.odin:178: `nd := dist[cur] + cat.pipe_tiers[t.pipe_tier[pi]].cost`; deferred-work.md: `summary: Add an upper-bound validation for pipe_tiers cost (e.g. <= 1e6) to make dist-accumulation overflow impossible in routing_rebuild.`",
      "6-lens agreement. jint_strict admits cost = i32::MAX; two such hops wrap nd negative and a wrapped -1 collides with the UNREACHABLE sentinel, silently erasing routes. Reachable only with absurd catalog data (the shipped 20/10/5 ladder is safe), and the minion documented the deferral explicitly in this PR — honor it at the playtest/balance gate, not this job.",
      "Add the deferred upper-bound validation (cost <= 1e6) at catalog load with a reject row, when the balance gate lands.",
      "confirmed"),
    f(["blind"], "note", "test-hygiene",
      "The tie pin dereferences hops[off+1] after a non-fatal count check — a routing regression panics (or mis-reads the adjacent row) instead of a clean pin failure",
      "core/routing_cost_test.odin:105-108",
      "core/routing_cost_test.odin:105-108: `testing.expectf(t, count == 2, \"different-tier equal-sum tie must ECMP (count 2), got %d\", count)` then `testing.expectf(t, s.routing.hops[int(off)].node == m1 && s.routing.hops[int(off + 1)].node == m2, ...)` — expectf records and CONTINUES; the next assertion indexes hops[off+1] unconditionally.",
      "A regression that makes count != 2 still fails the run, but via an out-of-bounds panic (or a misleading read of the next row's Hop) instead of the pinned message; the unique-hop pin has the same shape on hops[off]. Test-hygiene only — the pins do catch the regressions.",
      "Guard the node asserts with the count condition (if count == 2 / count == 1) so the expectf message is the failure.",
      "confirmed"),
    f(["edge"], "note", "demo-authoring",
      "ecmp_cost.dem diamond B's sink (host2 at grid x=48) is outside the 40-tile map — cropped from both T2 captures; and the t23 capture's 'mid-edge' wording overstates the frame (packets are on-edge at progress 0, rendered at their departure nodes)",
      "demos/ecmp_cost.dem:47 + app/render/view.odin:50-56 (camera-fit)",
      "demos/ecmp_cost.dem:47: `spawn_node content_host 48 15`; app/render/view.odin:50-52: `v.tile_px = f32(bal.tile_px) / v.world_w = f32(bal.map_w_tiles) * v.tile_px` (40 tiles) — host2 screens at x = off_x + 48*26*scale ≈ 1312 > the 1280 window; core/topology.odin topology_spawn_node has no map-bounds check (only player placement does).",
      "Diamond B's sink and the tips of its second-hop legs are invisible in both captures, so the 'settled delivery on both diamonds' visual evidence is partial. The t23 sim state DOES have a packet on each second-hop leg (Perkins' flow dump: pkt 2 on pipe 6 = r1->host2, pkt 4 on pipe 7 = r2->host2 — the tie split is real), but both sit at progress 0/30, which the lerped render draws at the departure nodes — 'mid-edge' is generous for this frame. T1 + the core pins carry the behavior; this is capture polish.",
      "Shift diamond B left (or shrink the grid spread) so host2 and both second-hop legs fall inside the 40-tile map; reword the t23 comment to 'on-edge, departing' if the capture tick stays.",
      "confirmed"),
]

consolidated = {
    "job": "packet-plumber-routing-bandwidth-cost",
    "round": 1,
    "pr": 37,
    "reviewed_sha": "32a1b653609eb12a478142a902e8bdf262ad9868",
    "reviewers_completed": 7,
    "failed_layers": [],
    "chunking": "10 file-group chunks (spec+docs+core+data+demos; boot/bundle/demolish/draw/ecmp/ecmp_cost goldens; flow/lose/place; qos; contention/emphasis/sla; surge a-d; warn/win) — canonical diff 18,064 lines / 47 files",
    "verification": {
        "raw_findings": 27,
        "confirmed": 25,
        "rejected_false_positive": 2,
        "merged_into_survivors": 25,
        "unverified_kept": 0,
    },
    "blockers": [],
    "warnings": warnings,
    "notes": notes,
    "verdict": "READY TO MERGE",
    "review_event": "--approve",
    "perkins_verification": {
        "splice_proof": "REPRODUCED independently — all 16 demos: new goldens reproducible tick-for-tick at this sha; folding the OLD catalog_hash (8da858ab04b113db) into the new dump's byte slot 33 reproduces the OLD golden exactly on all 15 re-blessed demos (zero non-catalog-hash byte delta, zero behavior shift)",
        "log_bin": "all 15 .log.bin diffs = exactly 8 bytes at offset 18 (the catalog_hash header field)",
        "t1_headers": "no seed/ticks/hash-count drift anywhere; all 16 manifests carry one consistent new catalog_hash 0a6324230ab9dcba",
        "t2_pixels": "no existing PNG changed in the diff; harness run green = T2 byte-identical for the 15 existing demos at this sha; ecmp_cost's 2 PNGs are new files",
        "gates": "odin test core 126/126 (4 new pins) · tools/lint.sh 6/6 · harness run 16/16 (T1+T2+replay) · drift-check 111/111 rejected · odin build app green",
        "dijkstra_fuzz": "400 random graphs (2-6 nodes, random tiers, incl. parallel mixed-tier bundles), 5,482 (u,d) pairs vs an independent Bellman-Ford reference with min-edge-cost semantics — 0 mismatches; extraction/relax/ECMP-set all match",
        "rejected_findings": [
            "blind 'OQ-5 register note missing' — FALSE: the arch open-questions register entry #5 (the routing-model ruling) IS amended in this PR's diff (hunk @@ -1984,9 +2004,16 @@ 'Amended 2026-08-13 (user ruling, capacity-cost routing)'). The lens grepped for the literal 'OQ-5' string; the register entry is titled 'Routing model → RULED'.",
            "edge 't23 capture shows no mid-edge packets / no packet on r2->host2' — FALSE: Perkins' flow dump at tick 23 shows pkt 2 on pipe 6 (r1->host2, wide) and pkt 4 on pipe 7 (r2->host2, standard), exactly as the demo comment claims; both at progress 0/30 (rendered at their departure nodes — see the demo-authoring note).",
        ],
    },
}

with open(f"{OUT}/consolidated.json", "w") as fh:
    json.dump(consolidated, fh, indent=1)
print("consolidated.json written:", len(warnings), "warnings,", len(notes), "notes,", len(consolidated['blockers']), "blockers")
