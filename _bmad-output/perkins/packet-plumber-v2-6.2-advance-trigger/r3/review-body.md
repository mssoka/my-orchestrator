## 🤖 Perkins automated review — round 3 of 3

**Job:** packet-plumber-v2-6.2-advance-trigger · **Reviewed sha:** `464db76a23603e835aa0602a9492dac6ed0b73a7` (head of `v2-6.2-advance-trigger`, base `v2` @ `4521cf7`) · **Reviewers:** 7/7 completed (blind needed its one retry) · **Verification:** 14/15 lens findings survived code re-verification — 1 discarded as false-positive; every carried item re-audited by direct read.

---

### Fix audit (round 2 → 3)

**R2-B1 (blocker — vacuous scripted-gate test): FIXED + BITES.** The test now pins `fires == 1` **and** `fire_tick >= 600` on the `Era_Advanced` event (advance_gate_test.odin:445–459). Empirical bite check: with the gate reverted in a scratch clone (a scripted advance firing ungated at tick 100), exactly the `fire_tick` pin fails; restored, 219/219 core tests pass. The r2 vacuity is closed — the shipped guard now guards.

**R2-W1 (overlay `advance_gate_on`): FIXED.** overlay.odin:50 threads the flag; all three `Demo_Replay` cfg sites now mirror the demo directive.

**Determinism/replay spine (the hard blocker class): HELD.** Re-verified this round on a pristine copy of the reviewed worktree: `tools/ci-local.sh --mac` **10/10** (incl. drift-check 306/306 bites), the 3 gate demos replay **bit-for-bit (ODN-11)** at 1400 ticks, and the goldens chunk is byte-identical (`cmp`) to the r2-verified state — r2's mechanical goldens verification folds forward unchanged.

**Carried items NOT folded (warning-tier per the r3 lens guards):** r1-W1 (block-event count pins), r1-W2 (scripted-while-blocked test), r1-W4 (E15 `fire_tick` dead), r1-W8 (ODN-16 citation absent — re-verified against the live PR body), R2-W2/W3/W4, and the note set (R2-N1..N8, r1-N1..N6). All re-confirmed still-present by direct read.

### BLOCKERS (0)

None.

### WARNINGS (3 new + 7 carried)

- **[R3-W1 · 5-lens agreement]** `overlay_check`'s `Demo_Replay` literal still omits `growth_on` — the fold closed the `advance_gate_on` half of the cfg-mirror parity gap but left the growth half; `overlay-check` on the 3 growth demos re-sims growth-OFF (wrong verification frame). Pre-existing from 5.1, surfaced by touching the literal. Fix: one line, `growth_on = d.growth_on,` mirroring run.odin:280.
- **[R3-W2]** Scripted+gate-on has no demo/golden/replay coverage — the just-pinned contract is unit-only (no `.dem` combines `advance gate on` with a scripted `advance`; era_advance.dem is gate-off). Fix: bless a scripted+gate demo with T1 + replay.
- **[R3-GATE]** Advisory test gate: **CONCERNS** — P0 100% (219/219 unit + goldens + CI), P1 ~85% (the two gaps above + r1-W1/R2-W4).
- Carried: r1-W1, r1-W2, r1-W4, r1-W8, R2-W2, R2-W3, R2-W4 (unchanged from r2; details in the r2 review).

### NOTES (2 new + 14 carried)

- **[R3-N1]** The overlay fold comment says "6.2 r2 W2" but the r2 report numbers the overlay finding **R2-W1** (R2-W2 is the demand_era split-brain) — wrong cross-reference id, right substance.
- **[R3-N2]** The fire-tick pin hardcodes `600` instead of `cat.balance.advance.milestone_window_ticks` — hidden fixture coupling (determinism_test.odin:120 sets 600).
- Carried: R2-N1..N8, r1-N1..N6 (unchanged; includes the documented 6.3 seams).

### Reviewer agreement

Five independent lenses (edge, acceptance, architecture, codebase, tests) converged on R3-W1 — the round's highest-confidence signal.

### Verification notes

One lens finding rejected: "tag-14 payload written but never read" — no event-payload reader exists anywhere (events are hash-only inputs to the T1 state hash; replay re-sims, never deserializes); refuted by the bit-for-bit replays of streams containing tag-14 events, and by the approved 6.1 tag-13 precedent.

Model note: the briefing-pinned kimi k3 was 403 at dispatch; the glm-5.3 fallback hit a 5-hour cap mid-wave and the wave was re-dispatched on deepseek-v4-pro (probed OK) — all 7 lenses completed on it with `--thinking max`, rooted `--cwd` at the reviewed worktree.

### Verdict

**APPROVED — 0 blockers.** The r2 blocker is fixed and demonstrably bites; the determinism/replay spine holds under full re-verification; the round's new findings are warning/note-tier (one pre-existing, surfaced by the fold). The loop closes here.

_Address findings and push — I re-review automatically on the new sha._
