## 🤖 Perkins automated review — round 4 of 3
**Job:** packet-plumber-v2-4.2-surge-crisis · **Reviewed sha:** f9184fa · **Reviewers:** 7/7 completed
**Verification:** 38/56 findings confirmed against the code — 18 discarded as false-positive

_User-approved cap override (rc4-3 r5 precedent): verify-don't-reopen on the r3 rework. Head unchanged during review._

### Fix-audit — the round-4 mandate (verify, don't re-litigate)

- ✅ **B3 (the r3 blocker) — CLOSED.** The trigger pass restores the post-trigger gate: a successful (a)/(b) `crisis_trigger` sets `triggered`; the (c) pool backstop is gated on `!triggered`; a cooldown-BLOCKED (a) still falls through to (c) (N4's intent survives — verified, not over-restricted); (b) is back on the settled-scan-MISSING path (frozen order). Exactly three mutually-exclusive `crisis_trigger` callers. Regression-pinned by `test_crisis_no_same_tick_double_trigger` (the exact probe shape), and my probe swept pool caps 11–13: **one event + one active row at every cap**.
- ✅ **W-1 — fixed.** The scope line names warn.t1 (300 shifted hashes @1201–1500, margin-fix cause) and drops the unchanged qos.log.bin; "everything else byte-identical" is now TRUE against the f906725..121d8a0 delta (13 files; logs + surge.t1 byte-identical — harness-verified).
- ⚠️ **W-2 — STILL-PRESENT (narrowed + probe-extended).** See warning below.
- ✅ **W-3 — fixed.** types.odin's self-contradictory trailing claim rewrote; serialize/flow comments aligned.
- ✅ **Notes:** N-1 (HUD ASCII), N-2 (dead `cat` param), N-3 (stale comments), N-6/N-7/N-8 (new pins, all green), N-10/N-11 (surge.dem comment + 149000ms capture — pixel-verified a real banner frame) fixed. N-4/N-5 partial (title fits now; pins remain weak — notes below). N-9, N-13 carried with real reasons. N-12 fixed: lint GATE 6 exists, passes, and **bites** (standalone scanner test: flags em-dash + middot literals, skips comments).
- ✅ **Golden discipline:** only `goldens/surge/149000ms.png` re-blessed at this sha; harness 15/15 demos + 104/104 drift mutations + 122/122 core tests green; app builds. Held guards (ODN-4, ODN-7, LOG_VERSION 3, determinism) re-checked — all hold.

### Blockers (0)

None. The r3 blocker is closed.

### Warnings (1)

**W2-STILL-PRESENT — legal pool caps 1–2 still produce a Pool_Exhaustion crisis that can never resolve** (since r3; narrowed + probe-extended) — `core/crisis.odin:406-412`
The resolve clamp guards `pool_max_packets > 1`, so cap 1 keeps margin 2 and `len + 2 < 1` can never hold — permanent by arithmetic. For caps 2–4 the clamped band is unreachable in practice: under the era-3 baseline (6 spawns/tick) a drop-free eval below `cap − margin` never occurs. Probe: cap 1 — trigger @1200, **zero resolves through tick 4300**; caps 2/3/4 — zero resolves through tick 3600 (min depths 0/1/2). The commit's "authoring-time caps covered" is false; no test pins the clamp. Shipped balance.json=512 is unaffected (authoring-time only — hence warning, not blocker).
_Fix:_ clamp with `max(1, cap) − 1` for cap 1 and validate `pool_max_packets` against a sane floor (probes show 4 is still permanent under continuous demand — consider keying the small-cap resolve on drop-absence rather than depth), plus a pin.

### Notes (12)

1. **N-W2-coverage** — the clamp branches have zero test coverage (the 3 new pins cover B3/(b)/lane-threshold only).
2. **N5-pin** — the "ANY-class discriminator pinned" assertion checks aggregate email loss, not an E22 shed (the discriminator itself is class-free by inspection).
3. **N4-coverage** — the pool banner branch (now shortened, ≈390px < 440px card) still has zero blessed pixel coverage.
4. **N12-data** — gate 6 scans only .odin literals; catalog-JSON display strings feeding the banner bypass it (shipped data is ASCII).
5. **N-tripwire** — app/main.odin:120-126 misdescribes the engine's input (drop scans read `flow.drop_sites`, not the event buffer).
6. **N-email22** — dead `email_e22` accumulator in the pool test (computed, never asserted).
7. **N-deadparam2** — `bundle_class_queue`'s `cat` parameter is unused.
8. **N-resolvecomment** — `crisis_resolve_row` comment claims a return value the proc doesn't have.
9. **N-banner-overlap** — the crisis card (x 410–870) paints over the HUD title's tail whenever a crisis is active (pre-existing; visible in banner captures).
10. **N-B3fallthrough** — the cooldown-blocked-(a) → (c) fall-through is code-verified but unpinned.
11. **N-poolgolden** — the golden tier never exercises the (c) pool backstop (the B3 class is only catchable by unit pins).
12. **N-W1sub** — the warn 65s PNG is still credited to "the mojibake" alone; its element 3→1 rename (margin-fix) stays unnamed in the scope line.

### Reviewer agreement
W2-STILL-PRESENT was independently filed by **7/7 lenses** plus the probe sweep — the round's highest-confidence signal. The gate-6 data bypass (4 sources) and the N-5/N-4 pin weaknesses (2 sources each) follow.

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
