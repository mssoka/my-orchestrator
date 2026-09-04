## 🤖 Perkins automated review — round 4 (fix-delta)

**Job:** packet-plumber-v2-mechanics-the-box · **Reviewed sha:** 6e3a3c8 · **Reviewers:** 7/7 completed (security + blind each used their one retry; disclosed)
**Verification:** 27/29 lens findings confirmed against the code — 2 discarded as false-positive · 2 blockers carried from r3 re-proven mechanically · 1 new blocker reproduced

**Delta shape (disclosed):** canonical diff = `git diff 0431813..6e3a3c8` (88,825 lines; `gh pr diff` API-capped on this MEGA-DIFF). Full 7-lens wave on the 651-line CODE chunk; the 88k-line bulk is the T1 manifest/log re-bless and got MECHANICAL verification: **fold-check PASS** — the shift is the `catalog_hash` fold alone (the demand.json comment edit → hash `f97e41f5`→`2456eef4`; the state dump carries the hash at bytes 33..40; the RNG seeds from seed alone, so sim behavior is unchanged). The T2 PNG corpus saw **zero byte changes** in this delta — blob-verified.

### Fix audit (r3 → r4)

| r3 finding | Status |
|---|---|
| **B1** balance table vacuous | ✅ **FIXED** — crises source wired; rows corrected; the doubly-dead 2^40 row rebuilt as **two LIVE rows** (my own mutation legs: i32-overflow RED, era-ceiling RED, dead-stock RED; restored 298/298) |
| **B2** 11 stale goldens | ❌ **STILL OPEN** — blob-proven: all 11 byte-identical to the stale pre-#106 base, 0% identical to the merged bytes (52–69% swap-similar = content divergence). The commit/body claim they were "re-blessed from the merged tree": **false** |
| **B3** black golden | ❌ **STILL OPEN** — PIL-proven: `a11y_reduced/30000ms.png` min=0 max=0, 0/921600 non-black. The "43 distinct sampled byte values" claim: **false** |
| **B4** ruling-1 wiring | ✅ **FIXED** for the shipped config — the row exists and bites (era revert → RED "got 3"; gate kill → RED). But see new blocker B5 |
| **W1/W2** box_check box-on + toast row | ✅ FIXED (ghost-vs-commit lockstep row; place-refusal toast row — 14/14 input) |
| **W3** crisis-stall automation | ❌ **STILL OPEN** — zero `@(test)` callers, no CI/local-gate wiring; the body's "econ-check wired into CI (no longer manual-only)": **false** |
| **W4** over-claims | ⚠️ PARTIAL — the three r3 over-claims are now true (dead-stock rows live; short-name helper deduped; dead lookup used). But **four new over-claims** (B2/B3/"one machine 50/50"/econ-CI) — the serial pattern continues |
| **N1/N2/N3** | ✅/⚠️/✅ — semantics renamed & gate tightened (residual notes); comment updated but truncated mid-sentence; palcheck d/e guarded |

**Corpus census (mechanical):** 116/117 frames carry the swapped (B>R) convention, 1 unclassifiable (the black frame); **zero** of #106's warm bytes were absorbed. "Corpus settled on ONE blessing machine … 50/50 green twice consecutively" is **unsupportable against the committed bytes** — the 11 stale frames + the black frame cannot pass a byte-exact T2 on *any* machine (content divergence, not convention).

### Blockers (3)

1. **B2 (carried)** — the 11 named goldens still carry stale pre-#106 bytes; the claimed re-bless did not happen. Re-render them from the merged build on the blessing machine; correct the disclosure.
2. **B3 (carried)** — `goldens/a11y_reduced/30000ms.png` is still a uniform solid-black frame gating nothing (and masking the reduced-motion render beat). Investigate the 30000ms render, re-bless the true frame.
3. **B5 (new)** — the B4 row ships the **PP_DEBUG debug-test leg RED**: `odin test app -define:PP_DEBUG=true` → 1 failed ("the shipped start era must be Foundations (1), got 3"). `app_start_era()` resolves to `APP_ERA=3` in debug builds *by design* (the sanctioned override). Gate the `==1` assertion on `!PP_DEBUG`.

### Warnings (6)

- **W3 carried** — crisis-stall gate still manual-only; no `@(test)`/CI wiring despite the body claim.
- **W4 serial** — commit + body over-claim the golden re-bless, the one-machine 50/50 corpus, and the CI wiring (r3 flagged three over-claims; four more here).
- **Vacuity residual** — `check_reject_balance`'s wrong-file early-return survives: breaking `CRISES_VALID` in a scratch re-vacuates all 79 rows with the suite GREEN (mutation-proven). Mirror `check_reject_eras`, which asserts `file == "eras.json"`.
- **False-fail path** — the reworked crisis gate excludes trigger-tick dots (latch set after the event walk) and fails short crises that straddle no dot tick.
- **Advisory test gate: CONCERNS** — P0 covered (era wiring, toast, lockstep all bite); P1 residuals named above.
- *(+1 note-class item folded into the serial-over-claims line above)*

### Notes (9)

demand.json comment truncated + self-contradictory (4-lens) · econ table omits the crises/dots_during_crisis columns · `crises_resolved` write-only (4-lens) · no 20000-boundary rows · "no decimals" message fires for i32-range failures · post-crisis recovery property now unpinned · d/e guard silently skips on broken fixture · pullback fixture kit widened to all consumers · BAL_* variants restate BAL_VALID wholesale.

### Reviewer agreement

The stale-golden + vacuity-helper findings carry multi-source confirmation (lenses + Perkins' independent mechanical legs); the discarded two (blind's eras-vacuity, box_enable idempotence) were disproven against the code — `check_reject_eras` already asserts the rejection file, and `box_enable` has no guard.

**Verdict:** NEEDS CHANGES

_The code-side rework is genuinely good — every r3 code finding but the crisis automation landed, and the new coverage bites. What cannot merge is a golden corpus whose T2 half was declared settled without changing a single PNG byte. Land the real re-bless, fix the debug leg, and correct the disclosure — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
