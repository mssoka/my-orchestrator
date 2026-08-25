# Round context + user rulings — packet-plumber-v2-motion-readability r1

Reviewed sha: a57b68c043b5c1d4e69f240d2fb2524c9af67de1 (base v2, PR #82).
Repo: Packet Plumber v2 — Odin + raylib deterministic sim (20 Hz fixed tick),
60 Hz render app, T1 (state-hash) + T2 (pixel golden) + replay gates.

## The change (what the PR claims)

View-layer motion readability for packets: (1) sub-tick interpolation —
the render lerps each packet's drawn position between the last two 20 Hz
snapshots using the render frame's fractional progress within the tick
(interp_alpha = accum/tick_seconds); (2) a 3-echo fading trail ring per
packet (world-space drawn positions, packet body color at low alpha);
(3) PACKET_R_FACTOR 1.15 (+15% packet radius); (4) harness `motion-strip`
evidence verb + tools/measure_packet_motion.py measurement; (5) T2 golden
re-bless (packet pixels legitimately moved) + new T1-only motion golden.

## Hard blocker bar (the ONE bar this round)

View-layer only (ODN-1: the view never writes back to sim state), sim
truth untouched: NO sim-semantics/routing/serialization/LOG_VERSION
changes. Identity-guarded interpolation (snap on spawn/sever/reroute
teleports — no ghost packets). Reduced-motion canon (7.3) respected —
echoes off, live packet + glide stay.

## What NOT to re-litigate (user rulings already made — do NOT file these)

- The MM "consistent speed" motion read IS the direction (user play
  session); the sub-tick interpolation + trails mechanism is the chosen
  implementation — don't re-argue the approach.
- Zero-golden-impact by construction for the INTERPOLATION (harness
  interp_alpha defaults 1.0 → snapshot-exact) + the 38-demo T2 size
  re-bless (cause-documented: all 76 T1 manifests + .log.bin
  byte-identical, diff bundles show only packet colors) = honest, not a
  defect.
- The 20 Hz snapshot tick + 60 Hz render interpolation is the sim's
  design; pacing (4x) already merged — packet SPEED is out of scope.

## What to flag for verification (not assumed)

- Interpolation identity guards: does the snap-on-teleport logic cover
  ALL teleport sources (spawn, sever, reroute) — no residual ghost.
- The before/after measurement (21/24 holds → ~10px glide; 30.6px jumps
  → continuous) — spot-check tools/measure_packet_motion.py + the
  motion-strip verb are honest.
- Trail alpha/echo-count under the reduced-motion toggle.

## Vision caveat (non-k3 round)

Pixel verification is MECHANICAL only (byte/hash/capture-diff);
aesthetic verdicts are deferred for a later k3 re-check; never faked.
