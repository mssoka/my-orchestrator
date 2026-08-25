# Perkins round-3 mandate — packet-plumber-v2-4.2-surge-crisis (FINAL automated round, FIX-AUDIT)

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/36 (targets `v2`)
- **Reviewed sha:** `121d8a07420ad9fc8638f33664d631a77fb5b90a` (short `121d8a0`)
- **Round:** 3 of 3 — **FINAL automated round** (after this: the human takes over)
- **Commit:** "perkins r2: renumber-proof test, qos churn root fix, pool under-fire fix, mojibake fix (B1, W-qos/W-pool/W-render)"

## Round-3 mandate: verify the r2-rework claims at 121d8a0

The commit message is a CLAIM, not proof. Verify EACH r2 finding against the code.

### (a) B1 — the demolish-and-renumber pin now EXISTS and bites (the r2 blocker)
- The resolve test: crisis active on pair P at slot 1, demolish a FULL bundle at slot 0 mid-crisis, rebuild renumbers P to slot 0 → assert the crisis STAYS active, still names P, no spurious `Crisis_Resolved`, no same-tick re-trigger, banner/outline still correct.
- Neutralizing the renumber-proof identity (or the test's demolish) turns it red. A vacuous or symmetry-preserving fixture = B1 stays open.
- surge.dem @2381 pair-gone branch: the banner-GONE T2 bracket @119500ms now pins the resolve/re-fire cycle visually (no longer T1-only).

### (b) W-qos — churn disclosed AND/OR root-fixed
- The @1200 trigger → same-tick `Crisis_Resolved` b0 + `Crisis_Triggered` b1 @1201 churn (probe-verified at r2): either the change-log now discloses it accurately AND the re-bless scope is corrected (only qos.t1 moved; log + PNGs byte-identical), OR a trigger confirmation delay / root fix removed the churn. A still-undisclosed churn contradicting "one trigger per activation" = a real defect.

### (c) W-pool — drop-evidence trigger with anti-flap guard + routed fixture
- Pool_Exhaustion triggers on the E22 drop evidence (admission-time) with the eval-time check as the anti-flap guard — NOT the eval-time-only check that under-fired in delivering networks.
- A routed-network pool fixture (pipes delivering, pool shedding) pins the map-wide crisis naming.

### (d) W3-carry + W-render
- types.odin:293 amended to match serialize.odin/change-log (the +4B drop-payload fold); the frozen Events bullet marked superseded (human renegotiation noted).
- Both banner title strings use ASCII (the mojibake em-dash replaced) — verify NO non-ASCII runes in the draw_text_c-fed strings (the file header's own warning class); the re-blessed T2 captures render clean glyphs.

### (e) Notes — each either fixed or explicitly carried with a real reason
B2-3 pin depth (size-only → byte-level or fixed message) · W5 branches (absent-key + wrong-typed pinned) · pool marginal regime · surge.dem T2 bracket (see (a)) · N4 restructured (cooldown-blocked cause no longer skips alternative causes past the pool backstop — verify the per-path `continue` is actually gone) · N2/N7 explicit recorded reasons · frozen-text residues marked superseded. Verify the carries. FLAG NEW FINDINGS ONLY.

### (f) DO NOT re-litigate
- r1/r2 VERIFIED: B2 settled-scan positive + backward-tick latch + equal-tick, W1 class filter dropped, W2 surge.dem demolish/resolve/relief, W4 slot-order + qos.t1 cause, W5 json.String assert, W6 flow.drop_sites (ODN-14 buffer no longer an engine input), W7 replay leak, N1/N3/N5/N6/N8/N9/N10/N11/N12.
- The 24 r2 false-positives + 2 r1 false-positives — do not re-raise.
- Held lens-guards (ODN-4 read-only topology, ODN-7 Director isolation, LOG_VERSION 3, determinism, 4.1 wiring) — the r1/r2 guards that held stay closed.
- **Round 3 of 3: this is the final automated review.** Only REAL defects block. Be exhaustive but fair.

## ⚠️ CRITICAL lens-guards (carried from r1/r2 — prevents false positives)

- 🚨 ODN-4 LOAD-BEARING — crisis engine READ-ONLY on topology. A topology write from the crisis path = a blocker.
- 🚨 ODN-7 / REVIEW M1 — Director never reads crisis state (structural). A director→crisis read = a blocker.
- 🚨 E13 DEDUP — one crisis per root cause per activation. Re-trigger only after `Crisis_Resolved`; duplicate `Crisis_Triggered` without a resolve = a blocker (the B1 contract — the identity mechanism must hold it under topology edits).
- 🚨 AC-E13 FAIRNESS — no crisis on a healthy within-capacity topology; no crisis without a resolvable root cause + `preventive_redesign`.
- E10 DETERMINISM — same seed → same crisis timeline (inside the deterministic RNG stream; no new draw, no map-iter in the hot path).
- 4.1 WIRING — the telegraph becomes true (forecast panel names the surge + countdown; the engine fires it on cue).
- GOLDEN DISCIPLINE — new goldens blessed with proof; existing goldens MUST NOT shift without cause documentation (an undocumented shift = a REAL finding).
- SCOPE GUARD — surge archetype + engine + root-cause ONLY; NOT 4.3; NOT the other four archetypes; NO new player commands (LOG_VERSION stays 3 unless flagged).
- BASE = `v2` — do NOT re-open settled prior-story findings (carry-forward only).
- **Em-dashes are OK in PP code comments but NOT in draw_text_c-fed render strings** (the mojibake class — non-ASCII in byte-truncated render paths; the banner title strings feed draw_text_c which truncates runes to bytes).
- **Determinism spine reminder:** per-hop forwarding, T1 hash rides every serialized state, replay byte-identical.
