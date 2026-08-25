## 🤖 Perkins automated review — round 3 of 3
**Job:** packet-plumber-ue-slice-1 · **Reviewed sha:** `1c00b51` · **Reviewers:** 21/21 completed
**Verification:** 61/67 findings confirmed against the code — 6 discarded as false-positive

**Mechanical gates (first-hand this round):** fast 3/3 · full 7/7 (fresh build, **22/22** automation incl. the 3 new `PacketPlumber.View.*` tests) · spine-check **111 checks** · 3-way golden byte-identical (`state_hash=5e440f9c5a28892a`, `tick_nonce=2381141952` — unchanged from r2, **no re-bless**) · PPProbe routing dump consistent. The determinism spine is untouched — the hard blocker bar holds.

### Fix audit (r2 → r3)
- **Blocker (road anchor): FIXED FOR REAL.** `RoadSlotTopLeft` anchors Center−(L/2,H/2); the two cited frames pass `verify-capture-geometry.py` AND an independent pixel scan (roads x[230–395] bridging discs at 214/408; dot 37 px at (357–363, 57–63) ON road row y[56–65] — exactly the PR body's claim; +0.5 applied exactly once). **Negative control: the actual r2-era frame (`git show 0256d8a`) fails the gate by 37 px** — it bites.
- **Warnings: 7/10 properly fixed** (dot offset · same-tick re-step now latches, contract symmetric + pinned · snap radius scales with fit · Gen-keyed same-tick rebuild · driver terminal loop-guard · spawned formula unified on both writers + SCHEMA · render clock unpinned with the static check flipped). **2 partial** (evidence frames re-captured only for the 2 cited → W1/W3; view coverage: geometry math pinned, widget internals remain → W7/W8). **1 carried** (MCP bridge, accepted risk).
- **Notes:** ~8 closed (bHasLastEditError removed honestly, shadow header 14%, GetMousePosition checked, dead accessors removed, node-id dump labels, save_version constant…), the rest carried.

### Blockers (0)
None.

### Warnings (10)
1. **ApplyEdit bypasses the E17 terminal barrier** `Step` enforces — post-terminal live edits mutate a "frozen" run (topology + action log). Unreachable until 1.4; guard it. [blind+architecture]
2. **FPPSimDriver::Advance clamps only the upper bound** — a negative delta is UB (float→uint64) + runaway stepping. One-line `FMath::Clamp`. [edge]
3. **The fix commit corrupted `scripts/static-check.py`** — shebang mangled to `#!/ usr / bin / env python3`, exec bit dropped 755→644, comments whitespace-damaged. Gate 3 still passes (invoked via `python3`), but the file is visibly damaged. Restore.
4. **`verify-capture-geometry.py` is wired into nothing** — 0 in-repo references; committed non-executable. It bites (verified), but no gate runs it. Wire it into local-ci over the committed frames + the negative control.
5. **2 committed evidence frames still carry the r2 blocker geometry** — `slice1-3-packet-alternate.png` + `slice1-3-packet-route2.png` FAIL the committed gate (37 px road offset, dot 16 px off-road). Uncited by the PR body, but committed; the checklist also retains pre-fix coordinates (x=223/272/320-326/369-375). Re-capture or delete; fix the checklist. *(partially addressed since r2)*
6. **Checklist scores Shadows ✅ against its own rubric** — the note admits "true radial-gradient softness is a slice-2 refinement" = 🟡 by the file's own scale. Score it honestly. [acceptance]
7. **View colors terminals via `Id == SCENARIO_SOURCE`** — palette keyed to the golden fixture's node id; every non-zero terminal renders sink-blue. Correct today, breaks with any second source. [architecture+edge]
8. **The production input path is never executed by any test** — OnDrawStart/OnDrawEnd, SetupInputComponent wiring, the new GetMousePosition guard. The r1 blocker class lives exactly here. *(partially addressed since r2)*
9. **The r3 fix logic itself ships unverified** — Gen-keyed same-tick rebuild, dot-pool lifecycle, fit re-fit, BuildSnapshot mapping, and the driver's terminal-barrier loop-guard have no tests (the geometry *math* is pinned; the orchestration is not). *(partially addressed since r2)*
10. **Advisory test gate: CONCERNS** — P0 spine coverage 100%; gaps are the view/widget orchestration + tooling wiring above (W4/W7/W8/W9).

### Notes (27)
Carry-forward set from r1/r2 (bundled: `<algorithm>` include, "Windows repeat" comment, no deserializer, EqualCostHops same-count staleness, ApplyEdit+StepScenario double-apply, U-E2 gitignored-ini, …) plus new: FlowSeedDemand unvalidated ids (latent), multi-tick Step skips demand (latent), tick-0 demand can't fire, self-route lookup, Dist2 overflow at extremes, FCommandKind ignored in dispatch (inert, single-kind), EcmpHash tautology still x==x, engine mirror omits the new same-tick pin, ZeroVector sentinel collision in PacketGridPos, EndGrid dead local (sibling removed, this one remains), StartRun doesn't reset drag state, RoadFillHeight orphan + MakeRoad hardcodes `Width+4` vs the helper, PPViewGeometry comment names a nonexistent test, AGENTS.md fixed-tick prose now contradicts the deliberate False, FPPScreenFit layering, MakeRoad degenerate guard, CoreTests module scope + hardcoded input coords, self-test corrupts 2/18 keys + label remap unasserted, driver-test identical deltas, raw `SKIPABLE:` prefix, save_magic literal remains, null-Commands contract, resolve_key hardening, granular spine coverage set, populated-form byte-pin. Full detail: `consolidated.json` (out dir below).

### Reviewer agreement
- ApplyEdit/E17: 2 lenses + Perkins (verified in code).
- Geometry-gate-unwired: 3 lenses + Perkins (grep-verified 0 refs).
- static-check corruption: 3 lenses + Perkins (mode+shebang verified).
- ZeroVector sentinel: 3 lenses (verified).
- Node-id coloring: 2 lenses (verified).

**Verdict:** READY TO MERGE

The slice's core contract holds first-hand (spine untouched, 7/7 gates, golden 3-way, no re-bless); the r2 blocker is fixed for real with a biting negative control. The 10 warnings are real but none touch sim semantics — W3/W4/W5 (the corrupted script, the unwired geometry gate, the stale frames) are the ones worth fixing before slice 2 builds on this surface.

_Address findings and push — I re-review automatically on the new sha._
