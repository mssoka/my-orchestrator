## 🤖 Perkins automated review — round 3 of 3
**Job:** packet-plumber-traffic-model-design · **Reviewed sha:** `42e4eb6` · **Reviewers:** 7/7 completed
**Verification:** 34/36 findings confirmed against the code — 2 discarded as false-positive (one a re-litigation of the endorsed unit convention, one a misread of the pre-PR review process)

### Fix audit (round 2 → round 3) — FINAL automated round

**7/7 r2 blockers+warnings verified FIXED against the worktree bytes** (re-read, not trusted). This was the round that mattered: the B1 re-spec had to be genuinely integer and loadable, and it is.

| r2 | Verdict |
|---|---|
| **B1** fractional state vs ODN-10 | **Fixed** — integer milli-packet credit on all four surfaces (`spawn_credit_milli`, spawn costs 1000, gate ≥ 1000; `cap_fraction_permille` int 500 — loadable); accrual/cost/ceiling all integer-only; no residual float state. ⚠️ The fix's *justification* carries one false claim about the loader (warning 1). |
| **W2** impossible demand.odin state home | **Fixed** — `Flow_State` beside `lane_caps` (verified `flow.odin:96`), updated in place by §1b; "rebuilt each tick" removed; card 5.9 Systems → `flow [ODN-3]`. |
| **W3** decision-log "data change" falsehood | **Fixed** — item 4 now states a new role is a CODE change (closed enum + touch points). |
| **W4** MAX_CREDIT clamps campus | **Fixed** — `MAX_CREDIT_MILLI(type) = 1000 × max(1, ceil(cap))`; campus 150 u/s → accrue 2500, ceiling 3, cap achievable long-run (math re-derived and correct). |
| **W5** burst-2 self-breaches email latency | **Fixed** — residential ceiling 1 = no burst by construction; 600 ms > 500 ms math carried; W10 pin asserts transit ≤ tolerance (advisory residual: note 10). |
| **W6** pins not quantitative | **Fixed** — rate envelopes on a known seed (≥ 0.95 × expected surge volume; ≤ cap × window + burst; credit ≤ MAX_CREDIT) (advisory residual: note 12). |
| **W7** unit-test re-pin surface unnamed | **Fixed in substance** — demand_test / determinism_test named with positive+negative assertions, but one member is misattributed (warning 3). |
| Notes N1/N5/N8/N9/N11 | **Fixed** — pin cited `sla_test.odin:88`; [E3] tag dropped; `growth.odin:76`; director-spawned scope; provenance disclaimer. Residuals: notes 1, 9. |
| Notes N2/N3/N4/N6/N7/N10/N12 | Not claimed — verified still present, carried below at note severity. |

### Blockers (0)

None. The canon is coherent across all four surfaces, ODN-10-compliant, loadable in its specified int form, derive-don't-record-clean (never serialized, T1 surface stated), and quantitatively pinned.

### Warnings (3)

**1. The B1 fix's ODN-10 justification is false as written: `balance.json`'s top-level loader uses `jint`, not `jint_strict` — a fractional cap value would silently truncate, not fail-fast** — `spec-traffic-model.md:130-131` (+ card 5.9, GDD M6, decision-log ×2) `[codebase]`
The canon says "`balance.json` loads with `parse_integers = true` + `jint_strict` (`core/catalog.odin:675`) — a fractional cap would fail-fast at catalog load". Verified: the top-level balance keys all load via `jint` (`catalog.odin:680`…), whose `case json.Float: return i32(x)` silently truncates — `jint_strict` is used only in the newer sub-catalogs and the placement block (its own comment: "the old loaders keep jint"). A minion copying the neighboring `jint` pattern gets `0.5 → 0`: accrue 0, eligible set permanently empty, all director spawns silently dead — the exact silent failure the canon claims is impossible. (The specified int value 500 is compliant and safe either way; this is the justification, not the design, that's wrong.)
**Fix:** pin the accessor in card 5.9 — load `cap_fraction_permille` with `jint_strict` (the `catalog.odin:794` placement precedent) + a 1..1000 range check; correct the five "loads with jint_strict" claims.

**2. The accumulator's initial value and newly-live-terminal lifecycle are unspecified — new-slot init (0 vs MAX) and growth-resize-vs-gen-rebuild are left to the implementing minion and shift T1 golden bytes either way** — `spec:133-148`, card 5.9 `[edge, architecture]`
No canon surface states the initial credit. Growth adds terminals mid-run (every 120 ticks), and the cited `lane_caps` precedent IS gen-rebuilt (`flow.odin:598-613`) — the credit buffer must grow without rebuilding (a gen-rebuild re-commits the r2-W2 failure). 0-init adds a ~12-tick dead window per grown terminal; MAX-init grants an immediate burst; the choice changes the golden spawn stream.
**Fix:** one sentence in Thread 2 / card 5.9: buffer grows on topology gen, existing slots untouched; a newly-grown terminal starts at 0 (or MAX — pick one and pin it).

**3. W7's re-pin surface misattributes "per-spec spawn counts" to `core/flow_test.odin` — that file carries only cap-exempt legacy §1a fixtures; the real pins live in `demand_test.odin:193`** — `stories-v2.md:690-691` `[tests, codebase]`
All six flow_test tests spawn via `flow_seed_demand` (§1a — exempt per the card's own N9 scope line), so "re-pin flow_test per-spec spawn counts" is a no-op instruction. The actual pin is `test_director_spawns_by_spec` in demand_test (already correctly named beside it).
**Fix:** re-word W7: re-pin demand_test (volume + histogram + per-spec counts) and determinism_test; note flow_test's legacy fixtures are exempt and expected unshifted.

### Notes (16)

1. The `demand_seen` identity keeps its `(E24)` tag beside the (correct) `sla_test.odin:88` pin — §11.7's E24 is the zero-demand guard (`spec:213`, 3 surfaces; N1 residual) `[architecture, codebase]`
2. "One deliberate re-bless at the slice boundary" still contradicts the four per-card re-blesses *(still present since round 2)* (`spec:324` + 3 surfaces) `[architecture, acceptance]`
3. Slice 5B row still has no §3 sprint-sequence section *(still present since round 2)* (`sprint-plan-v2.md:77` vs §3) `[architecture, acceptance]`
4. Hard-wrapped code-span path still breaks the spec cross-reference in the slice-5B intro *(still present since round 2)* (`stories-v2.md:641-642`) `[architecture, acceptance, codebase, blind]`
5. Access-tier headroom invariant still assumes exactly one access pipe — dual-homed/bundled unit unstated *(still present since round 2)* (`spec:79`) `[acceptance, tests]`
6. Aggregation-group derivation owner still unpinned for growth + director *(still present since round 2)* (`spec:259`) `[acceptance, tests]`
7. Group-bias draw's degenerate branches (first spawn, full cluster) still unspecified *(still present since round 2)* (`spec:234-235`) `[edge, acceptance]`
8. Artifact's sole innerHTML sink still interpolates runtime state (numeric-by-construction, no untrusted source) *(still present since round 2)* (`surge-explainer.html:846-847`) `[security, acceptance]`
9. Provenance disclaimer added, but the exhibit's specific stale items stay unnamed (§B ECMP slip "2/tick — under the 1.33 service"; "data change, not code change" claim refuted by item 4; A4/A5 anchor mislabels) — one dated line would finish N11 `[blind]`
10. W5's burst-latency guard is stated residential-only; ceiling>1 types unanalyzed — content_host burst-2 breaches streaming's 300 ms only on a grossly under-sized narrow (8× below its cap; standard access passes at 200 ms, wide at 100 ms; no fixture wires a host to a narrow) — advisory `[edge]`
11. "(or waits)" names no mechanism — an empty-eligible-set tick's volume silently vanishes (not a demand event, unobservable by any pin) (`spec:117-118`) `[edge]`
12. "Burst allowance" in the quantitative pins is unvalued — bind it to the derivable tight bound: spawns over W ≤ floor((MAX_CREDIT_MILLI + W × accrue_milli) ÷ 1000) (`spec:192-194`) `[edge]`
13. "~1,000×" compression is precise only for narrow (833×); standard ≈ 11,111×, wide ≈ 10,417× at the table's own values (`spec:55-57`) `[blind]`
14. Card 5.9's "accrue 1000-free integer" is undefined jargon — use the spec's formula wording (`stories-v2.md:665`) `[blind]`
15. Card 5.11 leaves growth_test's era-roster count pins (`len(r1)==1`, `len(r3)==2`) unnamed as a re-pin surface (`growth_test.odin:268,278`) `[tests]`
16. Advisory test gate: PASS — P0 4/4 (quantitative W9/W10, SLA seam at `sla_test.odin:88`, E10 replay), P1 5/5 FULL at the design level `[tests]

### Reviewer agreement
Warnings 2 (edge+architecture) and 3 (tests+codebase) were independently confirmed by two lenses each — the highest-confidence signals in this round.

**Verdict:** READY TO MERGE

The r2 blocker and all six warnings genuinely bit: the accumulator is now integer end-to-end and loadable, correctly homed in Flow_State, type-relative ceilings cover the campus class, and the pins are quantitative. The three remaining warnings are one-clause canon fixes (a loader-accessor pin, an init sentence, a re-worded re-pin member) — none breaks the design's contracts, and all fold cleanly into the implementing cards. After this round the automated budget is spent; the three warnings + notes above are the human's fold-in list.

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
