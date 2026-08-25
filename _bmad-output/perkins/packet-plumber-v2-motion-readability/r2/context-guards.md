# Round context + user rulings — packet-plumber-v2-motion-readability r2 (fix-audit)

Reviewed sha: 3635de08a7f1067006af9861e00d53aea6611c41 (base v2, PR #82).
This is ROUND 2: a fix-audit of r1's CHANGES_REQUESTED (review 5000626898).
Repo: Packet Plumber v2 — Odin + raylib deterministic sim (20 Hz fixed tick),
60 Hz render app, T1 (state-hash) + T2 (pixel golden) + replay gates.

## The change (what the PR claims)

View-layer motion readability for packets: (1) sub-tick interpolation —
the render lerps each packet's drawn position between the last two 20 Hz
snapshots using the render frame's fractional progress within the tick;
(2) a 3-echo fading trail ring per packet; (3) PACKET_R_FACTOR 1.15; (4)
harness `motion-strip` evidence verb + tools/measure_packet_motion.py;
(5) T2 golden re-bless (38 demos) + new T1-only motion golden.

The fix commit 3635de0 (this round's delta vs r1's a57b68c) claims:
- B1/B2 closed: NEW app/render/motion_test.odin — 13 tests pinning
  interp_continuous's four continuous kinds + every teleport snap,
  row-roll alpha endpoints, prune/reset, and a trails_active predicate
  (W6). Claimed to run in "the gate-2 render test run".
- draw_packet_shape extracted (N14): ONE geometry definition for live
  packet + echo ring; goldens claimed byte-identical (46/46).
- motion-strip verb hardened (W5 ExportImage checked, N10 arg validation,
  N11 dead cat param, N16 UnloadImage).
- measure_packet_motion.py hardened (W3 both means guarded, W4 frame-name
  mismatch exit 2, W7 lost-track != hold, N12 missing dir/non-PNG).
- N8 motion.dem comment corrected; N13 PR body documents the 100ms→60Hz
  acceptance substitution; N15 (third orchestration copy in
  run_motion_strip) DEFERRED with documented rationale.

## Hard blocker bar (unchanged from r1)

View-layer only (ODN-1: the view never writes back to sim state), sim
truth untouched: NO sim-semantics/routing/serialization/LOG_VERSION
changes. Identity-guarded interpolation (snap on spawn/sever/reroute
teleports — no ghost packets). Reduced-motion canon (7.3) respected —
echoes off, live packet + glide stay.

## What NOT to re-litigate (user rulings + r1 verdicts — do NOT file these)

- The MM "consistent speed" motion read IS the direction; the sub-tick
  interpolation + trails mechanism is the chosen implementation — don't
  re-argue the approach.
- Zero-golden-impact by construction for the INTERPOLATION (harness
  interp_alpha defaults 1.0 → snapshot-exact) + the 38-demo T2 size
  re-bless (cause-documented) = honest, not a defect.
- The 20 Hz snapshot tick + 60 Hz render interpolation is the sim's
  design; packet SPEED is out of scope.
- r1's verified-clean bar: view-layer only, identity guards cover every
  teleport class, measurement honest — verified green in r1, do not
  re-file unless the FIX COMMIT regressed them.
- r1 finding N13 (100 ms literal AC vs 60 Hz evidence substitution): the
  fix documents it in the PR body — accepted, do not re-file.

## What to flag for verification (not assumed)

- Do the new motion tests ACTUALLY run in a real gate (not dead files)?
  Check which gate runs `odin test app/render`: tools/ci-local.sh gate 2
  AND .github/workflows/ci.yml — are they in parity? Where does the
  motion test actually execute?
- Did draw_packet_shape extraction keep goldens byte-identical?
- Does motion_test.odin genuinely cover the four continuous kinds + every
  teleport class + row-roll endpoints, or is it a vacuous test?
- The N15 deferral rationale (third demo-setup copy in run_motion_strip)
  — is it documented and sound?
- Any regression the fix commit introduced (delta-introduced findings
  are the norm in fix-audit rounds).

## Vision caveat (non-k3 round)

Pixel verification is MECHANICAL only (byte/hash/capture-diff);
aesthetic verdicts are deferred for the k3 re-check; never faked.
