## 🤖 Perkins automated review — round 2 of 3
**Job:** packet-plumber-traffic-model-design · **Reviewed sha:** `da3a50e` · **Reviewers:** 7/7 completed
**Verification:** 44/47 findings confirmed against the code — 3 discarded as false-positive

### Fix audit (round 1 → round 2)

10 of 11 r1 blockers+warnings verified **fixed** against the worktree bytes; every claimed fix was re-read in the code, not trusted:

| r1 | Verdict |
|---|---|
| **B1** fractional cap unenforceable | **Fixed in mechanism** — rate accumulator (accrue/spend/eligible-set) is integer-spawn-coherent, one-draw-per-pick preserved, SLA seam verified against `flow.odin:476-513`. ⚠️ But the fix's *preferred form* carries a new **blocker** (below) + 3 warnings. |
| **B2** cap > throughput | **Fixed clean** — uniform `CAP_FRACTION × throughput ÷ packet_bandwidth`; invariant holds by construction; all numbers re-derived and correct (0.083 = 2.5 u/s, ~2× headroom pre-5.10; content_host 1.33 = 40 u/s). |
| W3 dead artifact link | **Fixed** — artifact committed, citations resolve, §B content verified present. |
| W4 GDD tier reconciliation | **Fixed** (M6 closing note). |
| W5 radius vs min-sep | **Fixed** (~4–6 tiles > 3). |
| W6 sink-side scope | **Fixed** on all surfaces. |
| W7 Terminal_Role code-change | **PARTIAL** — spec/GDD/card 5.11 fixed; the **decision-log's item 4 still says "a data change, not a code change"**, self-contradicting the same entry's W7 foot (warning 2). |
| W8 M6 vs six post-gate | **Fixed** (GDD M6 + spec §4). |
| W9 surge-lands pin | **Fixed** (pin named; quantization gap → warning 5). |
| W10 at-cap zero-drop pin | **Fixed** (homed in 5.9; decoupling rationale coherent). |
| W11 test gate CONCERNS | **Resolved — gate PASS** (P1 6/6 FULL). |

### Blockers (1)

**1. B1's preferred accumulator form is fractional core state with a float tuning value — violates ODN-10 integer-only state paths and is unloadable as written** — `spec-traffic-model.md:127-134` (+ card 5.9 Given, GDD M6 item 1, decision-log item 1) `[architecture]`
The spec prescribes fractional credit accrual ("accrues cap credit (fractional, packets)"; residential ≈ 0.083/tick) and `CAP_FRACTION = 0.5` in balance.json. But ODN-10 is "**Integer-only state paths**" (odin-architecture-v1.md:398, :1236), balance.json's own header says "**All state-affecting values are int (ODN-10)**", core currently has zero float state — and `catalog.odin:675` parses balance with `parse_integers = true` + `jint_strict`, so **0.5 fail-fasts at catalog load**. The integer alternative is demoted ("the accumulator is the smoother preferred form") and only covers MAX_CREDIT 1, not the specified 2. This is the same failure class as r1 B1: a mechanism whose stated form fails at the project's own contracts before gameplay.
**Fix:** re-spec in integer/fixed-point terms — credit in milli-packet units (or rational `cap_num/cap_den`), CAP_FRACTION as int permille or an int pair, covering MAX_CREDIT 2. One coherent edit across spec Thread 2 + card 5.9 + GDD M6 + decision-log (this also resolves warnings 3–4's sizing freedom).

### Warnings (6)

**2.** B1 state home "the director's pressure state (demand.odin)" is architecturally impossible — demand.odin is structurally stateless ("never receives a handle to Run_State"; Pressure_Plan destroyed per tick), the spawn pass and the cited `lane_caps` precedent live in **flow.odin** (Flow_State); "rebuilt by the spawn pass each tick" contradicts cross-tick accrual (a literal rebuild zeroes credit — the eligible set stays permanently empty). Card 5.9's Systems line still points at demand.odin *(still present since round 1)* — `spec:134-135`, `stories-v2.md:647-648` `[architecture, blind, edge, codebase, acceptance]`. **Fix:** home `spawn_credit` in Flow_State beside lane_caps, updated in place by the flow.odin §1b pass.

**3.** Decision-log item 4 still claims new terminal types are "a data change, not a code change" — the exact falsehood W7 flagged (closed `Terminal_Role` enum, `catalog.odin:22`), contradicting the spec/GDD/card corrections and the same entry's own W7 foot — `decision-log.md:775-778` `[acceptance]`.

**4.** `MAX_CREDIT = 2` clamps long-run rate at min(cap, 2)/tick — a token bucket with ceiling 2 and accrual > 2/tick spends at most 2/tick, so any type with throughput > 120 u/s (Thread 4's campus, "campus >> home") is silently capped at 60 u/s. "Long-run rate stays the cap" is false for exactly the high-throughput types 5.11 introduces — `spec:131-133` `[edge]`. **Fix:** type-relative ceiling (≥ ceil(cap)+1, or 2×ceil(cap)) or state the clamp bound and size it for campus.

**5.** Burst-2 on the pre-5.10 access self-breaches email's latency SLA at the spec's own starting values: 2×30 u on a 5 u/s access serializes the second packet in 12 ticks = **600 ms > email's `latency_tol_ms: 500`** (verified in packet_types.json); 5.9 lands before 5.10 per the decoupling, and W10 pins drops only — `spec:131`, card 5.9 `[edge]`. **Fix:** state the burst×latency interaction (MAX_CREDIT 1 pre-5.10, or widen W10's pin to assert burst-transit ≤ tolerance).

**6.** W9/W10 pins are not quantitative — zero-drop is satisfiable by any rate ≤ node throughput (0.167/tick), so a lax cap (e.g. 0.12) or an unbounded-credit bug passes every named pin; goldens bless bytes without asserting bounds — card 5.9 `[tests]`. **Fix:** pin the rate itself (per-terminal spawns ≤ cap×window + burst tolerance on a known seed; credit ≤ MAX_CREDIT).

**7.** Card 5.9 necessarily breaks `core/demand_test.odin`'s exact volume pins (2/tick from ONE host at cap 1.33; 2/tick email over 3 residentials at 0.083 each; the 4×800 + surge-window counts — all arithmetically unreachable) but names only the golden re-bless, not the unit-test re-pin surface — `stories-v2.md:682-684` vs `demand_test.odin:189,218,283-291` `[tests]`.

### Notes (13)

1. SLA identity still miscited as **(E24)** — §11.7's E24 is zero-demand-neutral; the pin is `sla_test.odin:88` *(still present since round 1)*; now on three surfaces. `[5 lenses]`
2. "One deliberate re-bless at the slice boundary" vs the four per-card re-blesses *(still present)*. `[architecture, acceptance]`
3. Slice 5B has no §3 sprint-sequence section *(still present)*. `[architecture, codebase, acceptance]`
4. Hard-wrapped code-span path breaks the 5B intro cross-reference *(still present)*. `[4 lenses]`
5. Card 5.10's `[E3]` tag — E3 is self-loop rejection *(still present)*. `[codebase, acceptance]`
6. Dual-homed/bundled access: invariant unit (per-pipe vs per-bundle) unstated *(still present)*. `[edge, acceptance]`
7. Aggregation-group derivation owner unpinned for its two consumers *(still present)*. `[acceptance]`
8. `GROWTH_MIN_SEP_TILES` cited at growth.odin:72 — the const is at :76. `[architecture]`
9. GDD M6's unqualified "never at endpoints" ignores the uncapped legacy §1a spawn path (flow.odin:629-633) — scope to director-spawned demand. `[edge]`
10. Group-bias degenerate branches unspecified (first spawn founds a group? full-cluster fallback?). `[edge]`
11. Committed provenance artifact carries stale/defective content: the §B ECMP row's "under the 1.33/tick service" is arithmetically false (60 u/s = 2/tick > 1.33; 3 wides can't carry base 180 u/s); D1/D2 font+resize findings superseded by merged #52; reset-button UI desync; A4/A5 anchor mislabels; minor dead JS. **Recommend a one-line provenance disclaimer in the decision log** (historical exhibit, committed verbatim by design) rather than editing the exhibit. `[blind, codebase]`
12. Artifact's sole `innerHTML` sink interpolates runtime counters unescaped — safe by data flow (numeric-only, no untrusted source); textContent would eliminate it. `[security]`
13. **Advisory test gate: PASS** — P0 100%, P1 6/6 FULL (r1's two PARTIALs are now named assertions). `[tests]`

### Reviewer agreement

Findings 2 (state home — 5 lenses), the E24 miscite (5 lenses), the hard-wrapped path (4 lenses), and the 5B §3 gap (3 lenses) were independently confirmed by multiple reviewers — highest-confidence signals.

**Verdict:** NEEDS CHANGES

One blocker: the B1 accumulator's preferred form (fractional state + `CAP_FRACTION 0.5`) violates ODN-10's integer-only-state contract and fail-fasts at catalog load — an integer/fixed-point re-spec (which the spec already half-contains) plus the state-home re-wording clears it. The r1 rework is otherwise substantively landed: B2/W3–W6/W8–W11 all verified fixed in the code.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
