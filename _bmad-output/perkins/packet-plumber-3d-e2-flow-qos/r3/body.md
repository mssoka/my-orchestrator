## 🤖 Perkins automated review — round 3 (fix audit)

**Job:** packet-plumber-3d-e2-flow-qos · **Reviewed sha:** e224804 · **Reviewers:** 14/14 completed (7 lenses × 2 chunks; 1 retry)
**Verification:** 31/33 findings confirmed against the code — 2 discarded as false-positive
**Chunking:** 4240-line diff split c1 (runtime, 1938L) / c2 (tests+evidence, 2302L); one full wave per chunk, merged before verification.

### Fix audit — round 2 verdict items

**B1 `_pick_next_pipe` Nil-crash — FIXED (mutation-proven).** The local is now untyped with a real null guard. Reverting the fix (re-typed local) reproduces the exact r2 crash and eats 3 checks — and the new gate turns it into **`ran 23, expected 26` → SUITE FAIL, exit 1** where r2 printed PASS. Green leg: the isolation test's **5/5 checks execute and pass** — the r2 phantoms are gone. (The fix deviates from the recommended `drops.is_empty()` branch-guard: the EXPECTED_CHECKS gate catches the same abort class structurally instead.) Disclosed: the 5th isolation check flipped from "a single no_route does not latch" (never executed in r2) to "injected lost traffic latches the loss SLA (honest accounting)" — verified coherent: every drop counts against its class, 1/1 = 100% > 30%; the "must not poison" clause covers unreachable *natural* demand (never spawns — pinned by checks 1–2).

**B2 vacuous exit-0 gate — FIXED (mutation-proven, three independent legs).** `run_tests.gd` now has two independent trips: the `completed` flag (set by `run_all`'s last statement) and the pinned **EXPECTED_CHECKS** count — 12/12 runnable files pinned, shortfalls (and overruns) FAIL with `ran N, expected M`. Mutation proofs at this sha: **M-A** abort-with-resume (the exact r2 false-green class) → check-count FAIL; **M-B** a silently disabled check → `ran 24, expected 25` FAIL; **M-C** flag removal → `ABORTED before its completion flag` FAIL. The gate is not faked — and notably the M-A abort class slips past the flag trip (Godot resumes the caller) while the count trip catches it, so the two trips are genuinely independent. Your commit's claim that the gate caught 4 unpinned files mid-fold is consistent with this behavior.

**7/7 warnings folded:** layout computed once ✓ · REPLAY_INJECT_TICK hoisted (tool re-run reproduces captures/05 **byte-identical** — committed evidence current) ✓ · lane-speed exact pins (2000/1000/600 milli per 10 ticks) ✓ · HUD chip + both-latches elif pin ✓ · egress pulse + cooldown pin ✓ · streaming 1200 ms latch pin ✓ · capture harness drives the panel's public surface (`open` + `apply_requested` signal) ✓.

**Suite:** `godot --headless -s res://tests/run_tests.gd` → **PASS, exit 0, 185/185 oks, 12/12 exact pins.**

**Captures (mechanical only — round model is text-only):** 7 real PNGs (6 in-game 1600×900 + editor viewport 2964×2253), each with 1600–3400 unique colors per downscaled frame — real rendered scenes, correct filenames/sizes. Determinism log: all-MATCH, PASS. **Aesthetic parity deferred (k3 re-check).**

### Blockers (0)

None.

### Warnings (2)

1. **QosPanel.open's null guard is dead-on-arrival** — `var p: Dictionary = sim.pipes.get(pipe_id)` throws before `if p == null` can fire (the r2-B1 construct, proven to throw by this round's mutation leg). `open()` on an unknown pipe crashes instead of auto-closing. [blind] — `scripts/qos_panel.gd:115`
2. **"Strands re-thicken on QoS apply" is unpinned** — the alloc→view rebuild (`flow_view.gd:51`) has no test; a constant thickness passes the suite. Spec names the clause; captures 06/07 are one-time static evidence only. [tests ×2 chunks]

### Notes (22)

Gate is opt-in for future files (−1 fallback skips unpinned scripts) [blind+architecture+tests] · `_sync_dots` repeats the dead-guard pattern · class-cycle button no-ops on rung 1 · long-arc geometry guarantees email latency latch with zero congestion (balance observation) · capture harness triple-fetch (carry-forward) · `set_lanes` accepts totals < 100 · rung fallback hardcodes lane 0 (carry-forward r2) · ConnectController parent reach · pulse positional mapping (carry-forward N32) · editor capture harness in main (carry-forward N34) · dot-pool cap/ghost-hide/reverse-render unpinned · QosPanel guard paths untested · editor one-shot path untestable headless · same-class tie-break unpinned · CMDS_CAP=512 windowing unexercised · **advisory test gate: PASS** (upgraded from r2 CONCERNS — P0 100%, P1 ≥90%) · spec code map predates r1 folds (test_view_interaction unlisted) · noop test hardcodes pipe id 1 · test rename discarded its .uid · determinism_log hardcodes the seed 4× · gesture helpers duplicated (carry-forward) · REPLAY_CMDS spine duplicated in capture_runner (carry-forward).

### Reviewer agreement

- Check-count gate opt-in fallback — 3 independent lenses (blind, architecture, tests)
- Strand-thickness gap — tests lens, both chunks independently

**Verdict: READY TO MERGE**

Both r2 blockers are fixed and mutation-proven, the harness can no longer false-green, all seven warnings folded, and no new blockers surfaced in the delta. The two warnings are a dead defensive guard and a P2 coverage gap — fold them post-merge or in the E3 lane at your discretion.

_Address findings and push — I re-review automatically on the new sha.
The loop runs until an APPROVED verdict._
