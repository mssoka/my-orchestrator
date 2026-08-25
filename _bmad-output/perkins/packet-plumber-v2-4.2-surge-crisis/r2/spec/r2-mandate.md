# Perkins round-2 mandate — packet-plumber-v2-4.2-surge-crisis (FIX-AUDIT)

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/36 (targets `v2`)
- **Reviewed sha:** `f906725c1f2be8911903ecb951c6ad0a44859e22` (short `f906725`)
- **Round:** 2 of 3 (r1 = CHANGES_REQUESTED @ b94d54f)
- **Commit:** "perkins r1: stable crisis identity, frozen attribution restore, drop-site input, test-gate pins (B1/B2, W1-W7)"

## Round-2 mandate: verify the r1-rework claims at f906725

The commit message is a CLAIM, not proof. Verify EACH r1 finding against the code.

### (a) B1 — Active_Crisis identity is now STABLE (verify the mechanism)
- `Active_Crisis.bundle` no longer stores the compaction-prone slot index — keyed on the canonical `(bundle_lo, bundle_hi)` node pair or the E11-stable member pipe id, with the bundle slot resolved at eval time (`bundles_slot_for_pair` / `bundle_of_pipe`).
- A mid-crisis topology edit (demolish a FULL bundle whose slot precedes the crisis's bundle) must NOT: spuriously `Crisis_Resolved` while the flaw is still saturated, re-trigger same-tick (E13 chatter), mislabel the banner/bottleneck outline.
- The resolve test must exercise the demolish-and-renumber scenario (not pass by fixture symmetry). B1 closed ONLY if the renumber-proof identity is real and pinned by a test that bites.

### (b) B2 — test gate now PASSES (verify each pin)
- Settled-scan POSITIVE test: queue at bound, no same-tick drop → `crisis_find_saturated_bundle` ok=true branch executes.
- Backward-tick latch test (`tick < state.tick` rejected; `tick == state.tick` behavior asserted — r1 N1).
- Byte-layout pins extended: drop-payload target byte + tags 8/9 + the crises section (not just tags 1–7).

### (c) W1-W7 (verify each; fixed-or-carried-with-reason, no auto-flag)
- W1 pool backstop class-filter vs frozen "ANY Pool_Exhaustion" (filter dropped OR frozen text amended)
- W2 surge.dem now includes the mid-run capacity fix + `Crisis_Resolved` pin in the launchable golden
- W3 byte-identity promise amended (spec-4-2:30 + types.odin:279 + serialize.odin:358 — drop payload is +4B, change-log admits)
- W4 trigger attribution matches the pinned slot-order definition (or the frozen block amended)
- W5 wrong-typed `archetype_id` type-asserted (`json.String`; key present but non-string → named load error, ODN-5)
- W6 drop-site input moved off the ODN-14 event buffer (per-tick drop-site field on `Flow_State` or equivalent)
- W7 replay-test leak fixed (no leaks under the tracking allocator)

### (d) N1-N13 — each either fixed or explicitly carried with a reason. Verify the carries are REAL (code matches the claim). FLAG NEW FINDINGS ONLY.

### (e) DO NOT re-litigate
- The r1 lens-guards that HELD: crisis engine read-only on topology (ODN-4), Director never reads crisis state (ODN-7/M1 structural signature), LOG_VERSION stays 3, determinism spine, 4.1 wiring (shared set-piece schedule).
- The 9 r1 false-positives (see r1 consolidated.json rejected_false_positives) — do not re-raise.
- **Golden discipline:** r1 verified the golden shifts clean (catalog_hash fold + drop-payload byte; warn/qos @65s T2s cause-documented; zero-traffic T2s untouched). Any NEW golden shift in this rework MUST have cause-documented proof — a re-bless without proof = a finding.

## ⚠️ CRITICAL lens-guards (carried from r1 — prevents false positives)

- 🚨 ODN-4 LOAD-BEARING — crisis engine READ-ONLY on topology. A topology write from the crisis path = a blocker.
- 🚨 ODN-7 / REVIEW M1 — Director never reads crisis state (structural). A director→crisis read = a blocker.
- 🚨 E13 DEDUP — one crisis per root cause per activation. Re-trigger only after `Crisis_Resolved`; duplicate `Crisis_Triggered` without a resolve = a blocker (the B1 contract — verify the identity mechanism holds it under topology edits).
- 🚨 AC-E13 FAIRNESS — no crisis on a healthy within-capacity topology; no crisis without a resolvable root cause + `preventive_redesign`.
- E10 DETERMINISM — same seed → same crisis timeline (no new draw, no map-iter in the hot path).
- 4.1 WIRING — forecast panel names the surge with a countdown; the engine fires it on cue.
- GOLDEN DISCIPLINE — existing goldens must NOT shift without cause documentation — an undocumented shift = a REAL finding.
- SCOPE GUARD — Surge archetype + engine + root-cause ONLY. NOT 4.3, NOT the other four archetypes, NO new player commands (LOG_VERSION stays 3 — a bump without a flag = flag it).
- BASE = `v2`. Do NOT re-open settled prior-story findings (carry-forward only).
- Em-dashes are OK in PP (the RT ban does not apply).
