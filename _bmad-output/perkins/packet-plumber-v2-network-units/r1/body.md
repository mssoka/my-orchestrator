## 🤖 Perkins automated review — round 1
**Job:** packet-plumber-v2-network-units · **Reviewed sha:** 48c0e82 · **Reviewers:** 7/7 completed
**Verification:** 30/34 findings confirmed against the code — 4 discarded as false-positive

Independently verified on this head: **48/48 harness demos green (zero golden movement — T1/T2/replay)**, `odin test core` 239/239, `odin test app/render` 75/75, purity gate green; E9/E22 bounds unchanged; LOG_VERSION untouched (tx ring verified never-serialized, derived-state pattern); amber/red (70/90) verified riding the honest windowed util; the SIM_TIME_SCALE math independently recomputed — the honest util formula, the 16% single-stream reading, and the impossibility of the nominal 10/100/1000 ladder under one scale all check out.

### Blockers (1)

**1. NOC queue rows: the right-aligned util% glyph-collides the Best-effort lane's queue-count digit** — `app/render/noc_overlay.odin:786-800` · [codebase]
Mechanically proven from the shipped font (IBM Plex Mono, 600/1000 em advance) + raylib metrics: lane-3 count digit ink sits at `[px+365.2, px+373.6]`; util% is right-aligned at `px+402`, so **every util ≥ 10% row starts its first glyph inside the digit's ink** ("16%"/"70%"/"99%" first-ink at 368.6–368.8 → 4.8 px overlap; at "100%" the `0` lands 5.0 px on the digit). That's the normal busy case and the saturation showcase row — it mechanically contradicts the KYLE legibility PASS riding the PR (flagged per the vision caveat; no vision used). Fix: re-anchor the right block (≥130 px reserve) and/or narrow the lane pitch/bar so the count clears, then re-capture.

### Warnings (4)

**1. Tier rates ship as 67/100/267 Mbps, not the briefing's 10/100/1000 ladder** — `core/units.odin:24-34` · [acceptance]
Verified deviation **and** verified impossibility: one SIM_TIME_SCALE forces rate ∝ 1/transit (transits 12:8:3 → S would need to be 500/3333/12500 simultaneously); the nominal ladder implies a 3–6.7× pace change = golden movement (forbidden; 48/48 proves the pace held). The derived set is documented in the PR body. This needs your conscious blessing of the derived ladder — if the nominal one is ever wanted, it's its own transit-rebalance + re-bless job.

**2. tx-ring window semantics have zero direct tests** — `core/bundles.odin:184-218` · [tests]
No test references `bundle_tx_record`/`bundle_tx_window`. Indirect coverage exists (units_test formula pins, stats_test measured pins, 48-demo stats-check), so re-triaged P0→P1: unpinned are window-expiry boundary, slot reuse at W, rebuild reset with a populated ring, and the defensive bounds. Fix: a handful of `bundles_test` cases.

**3. `noc_pipe_rows` predicate swap has no discriminating test** — `app/render/noc_overlay.odin:609-620` · [tests]
The row-count pin uses an empty pipes array — it cannot tell the new `util>=red` predicate from the old `carried>=cap` or an inverted one. The measure/draw twins do agree (verified). Fix: hand-built pipes at util 89/90 + cap 0.

**4. Advisory test gate: CONCERNS** — [tests]
Lens said FAIL on a P0 classification; verification re-triage (happy paths pinned end-to-end) lands it at CONCERNS — close W2+W3 to lift it.

### Notes (12)

1. **Zero-capacity link maps to ~800 Mbps, not 0** (`transit_ticks(pb,0)→1`; old `cap>0` display guard dropped) — unreachable with the shipped catalog (decay floor = 5), but the defensive semantics are inverted for a future era with permille < 100. [blind+edge]
2. **Stale "96 px chip" comments** in `main.odin:2235` + `units.odin:148` contradict `TRAY_CHIP_W` 96→112 from this same diff. [blind+architecture+codebase]
3. **node_health comment/PR quote say "util 150%…"** but the format string drops the prefix (fine — see 10). [blind]
4. **NOC headers + default param hardcode 90/6/512** while predicates read catalog tunables — labels go stale if tuned (the new "90" is the tunable itself, unlike the old mathematical 100). [blind+architecture+codebase]
5. **Stats stream stays "v1"** with an appended 18th P field — only consumer is the live==replay byte-compare (unaffected, verified); bump the marker at the next change. [blind]
6. **CSV literal fixture pairs util=100 with tx_octets=0** — impossible under honest semantics; the writer-pin is fine, the fixture misdocuments. [blind]
7. **Sub-Kbps/bps formatter tiers unpinned; compact form is unitless** ("100M") — intentional chip-budget form, network-conventional. [blind]
8. **`line_rate_bytes_per_tick` is production-dead** and its comment overcalls it "the honest utilization reference" (the formula divides by `W×cap` directly). [blind+architecture+codebase]
9. **Same-tick re-step accumulates duplicate served into one slot** — production never re-steps (step-contract: "documented, accepted" for events); the ring joins that class — add the comment. [edge]
10. **Node card pct remains backlog ÷ throughput** — a different, pre-existing quantity (node load, can exceed 100%); load + rate went native this PR and the "util" label was dropped. Re-keying it would move node-health semantics (goldens) — out of scope. [acceptance]
11. **Sim pipe warnings stay queue-pressure-keyed** while the rail tint rides honest util — re-keying would change serialized warning state → golden movement; queue pressure is the queue's own telegraph. Defensible spec reading, documented here. [acceptance]
12. **`Bundles` struct doc still says "pure function of the Topology"** — now false (tx ring = flow history; the field comment in the same PR says so). Also `units.odin:56` points at "balance.json's era" where the documented seam lives in the health section. [architecture]

### Reviewer agreement
Three-way independent agreements: stale 96-px comments (blind+architecture+codebase), hardcoded header constants (blind+architecture+codebase), `line_rate_bytes_per_tick` dead code (blind+architecture+codebase); two-way: zero-cap 800M defensive semantics (blind+edge). The blocker is single-source but mechanically proven by the orchestrator from the shipped TTF.

**Rejected as false-positive (4):** util/rate "outside the gating block" (measure/draw agree exactly — De Morgan of the same predicate); "balance.json documentation does not exist" (it exists — health section, `window_ticks=200`); tick-0 sentinel collision ×2 (both callers increment before stepping — tick 0 never steps).

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha.
The loop runs until an APPROVED verdict._
