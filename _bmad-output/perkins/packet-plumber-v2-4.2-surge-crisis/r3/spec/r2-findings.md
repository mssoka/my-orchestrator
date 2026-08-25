# r2 findings — the rework this round audits (prior findings, fix-audit input)

Round 2 verdict: NEEDS CHANGES at f906725. The commit 121d8a0 claims to fix the blocker + 3 warnings and address the notes. The round orchestrator (Perkins) runs the authoritative fix audit. YOUR job: find NEW findings — regressions the rework introduced, new bugs, new coverage gaps, claims visibly false in your chunk. Rules:
- Do NOT re-file an r2 finding as a new finding unless the code in YOUR chunk proves a claimed fix is absent — then file it with title prefix "STILL-PRESENT: " and category "fix-audit".
- Do NOT re-raise the rejected false-positives listed at the bottom.
- New findings go through the normal verify + consolidate pass.

## r2 BLOCKER (the one the rework must close)

**B1** (tests + audit): the pair-keyed identity mechanism (bundle_lo/bundle_hi + per-tick bundles_slot_for_pair re-resolution + !ok-resolve + pair-keyed cooldowns) was verified correct by inspection, but NO test exercised the renumber scenario — every fixture preserved slot order at every transition (demolish the crisis's OWN bundle → redraw mints the same pairs in the same order). Mandate close-condition: a demolish-and-renumber test that BITES — crisis active on pair P (slot 1), demolish a FULL bundle at slot 0, rebuild renumbers P to slot 0, assert crisis STAYS active, names P, no spurious Crisis_Resolved, no same-tick re-trigger, banner/outline correct. Neutralizing the renumber-proof identity (or the test's demolish) must turn it red.

## r2 WARNINGS (the rework claims to fix)

**W-qos** (golden-discipline): qos.t1 re-bless documented only the @1200 element change (b0 vs blessed b1) — but the blessed stream pins trigger b0 @1200 → SAME-TICK resolve b0 + re-trigger b1 @1201 churn (probe-verified), contradicting "a persistent flaw emits ONE trigger per activation"; 'T1/log/T2 re-blessed' was false for log/T2 (byte-identical). Fix = disclose the churn accurately + correct the re-bless scope, OR root-fix (trigger confirmation delay) removing the churn.

**W-pool** (contract-deviation): Pool_Exhaustion triggered on an EVAL-TIME pool check (`len(state.flow.packets) >= pool_max_packets && drop_of_reason_this_tick`) — but the E22 shed happens at SPAWN (admission) and phase-5 CULL removes deliveries in the same flow_step before crisis_evaluate runs, so in delivering networks the pool drains post-shed and the trigger under-fires (map-wide flaw sheds every other tick, never named). Fix = trigger on the drop evidence (drop_of_reason_this_tick(.Pool_Exhaustion)) with the eval-time pool check as the anti-flap guard; plus a routed-network pool fixture (pipes delivering, pool shedding) pinning the map-wide naming.

**W3-carry** (doc-contract-drift): types.odin:293 still claimed "pre-3.3/3.4/4.1/4.2 event streams stay byte-identical" while serialize.odin + change-log admit the +4B drop-payload fold. Fix = amend types.odin to the serialize wording; mark the frozen spec Events bullet superseded.

**W-render** (render-defect): the crisis banner titles use a non-ASCII em-dash fed to draw_text_c (which truncates runes to bytes) — mojibake glyph blessed into the T2 captures. Fix = ASCII in both title format strings.

## r2 NOTES (each must be fixed or explicitly carried with a real reason)

- **B2-3 pin depth**: drop-payload + tags-8/9 payloads size-pinned only (byte-value asserts wanted) and the failure message says 'want 30' while the expression evaluates to 38. → byte-level pins or corrected message.
- **W5 branches**: absent-key (-1 pure-demand) + wrong-typed (named load error) archetype_id catalog paths untested (only the unknown-id row pinned). → new test rows.
- **Pool marginal regime**: the pinned pool fixture has no pipes (zero deliveries) — the routed-network case + the ANY-class discriminator unpinned. → routed fixture (also the W-pool close-condition).
- **surge.dem T2 bracket**: the 2381/2401 resolve + re-fire cycle was T1-pinned only (captures at 30s/65s/170s) — no T2 brackets the resolved frame or the re-fired banner. → capture(s) at ~119500ms etc.
- **N4 carry claim inaccurate**: the change-log claimed "a blocked cause no longer suppresses a DIFFERENT cause's trigger that tick" but the per-path `continue` still skipped the alternative causes on a cooldown block. → either fall through to the remaining paths on a cooldown block (verify the `continue` is actually gone / restructured so a cooldown-blocked cause no longer skips alternative causes past the pool backstop), or reword the carry note to what actually changed (the pair key).
- **N2 silent omission**: dedup key still (archetype, set_piece) vs arch §6.4's per-root-cause wording; no carry note. → carry line or align.
- **N7 silent omission**: multi-bundle same-tick shed attribution order still unpinned; no carry note. → carry line or pin.
- **Frozen-text residues**: the frozen Dedup bullet (resolve on "the first tick the condition is absent" — omits the 3-condition hysteresis) and the trigger bullet's (b) element ("first any-lane-at-bound fallback" vs the code's drop's-own-site selection) unamended — frozen, needs human renegotiation; mark superseded-by-change-log.

## r2 REJECTED FALSE-POSITIVES — DO NOT RE-RAISE (24)

qos T2 not re-blessed / engine renders bundle 0 at 65s (refuted by harness + probe + PNG decode) · cause-doc is false, element did NOT change (incomplete, not false) · surge.t1 tick-1 divergence unexplained (action-log hash fold — demo-content change covers it) · wide pipes drawn twice at same timestamp (by design) · draw/flow/win log.bin byte-identical (false — they changed, catalog_hash fold) · full-stream re-bless complaints qos/contention/emphasis/sla/warn (cause-documented; 'binary goldens unauditable' re-raises the held pixel-compare design) · catalog_hash changed with no version bump (the header IS the version record) · consecutive hashes share a 16-bit prefix (noise) · manifest declares 4000 ticks but diff ends at 1992 / hunk length mismatch / scale relationship unverifiable (chunking artifacts) · FNV-1a golden opaque and brittle (re-litigates settled T1 design) · manifest tick-index/demo header never validated (pre-existing harness design, out of 4.2 scope) · crises.json strings unbounded and rendered unclipped (developer-authored catalog data, uniform pattern, no security boundary) · crisis_evaluate walks the full packet array per bundle per lane every tick (bounded by pool cap 512 × bundles × 3 lanes at 20Hz, negligible).

Plus 2 r1 false-positives (see r1 consolidated) — also do not re-raise.
