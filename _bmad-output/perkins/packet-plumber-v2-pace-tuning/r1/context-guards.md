# Round context for reviewers (from the orchestrator's lens-guards — user rulings)

You are reviewing ONE chunk of a chunked review: the CODE chunk
(core/, app/, data/, repo root). The goldens/ chunk (179 files, 77k
diff lines — the deliberately re-blessed golden corpus) is verified
MECHANICALLY by the repo's replay gate (CI gate 4: every blessed log
re-sims its manifest bit-for-bit), not by lens review.

## User rulings already made — do NOT re-litigate (findings contradicting these are invalid)

- The 4x packet pace (packet_bandwidth 30 -> 120) and the 2x spawn
  reduction (interval 40 -> 80) ARE the user's direction (play session
  2026-08-21). Do not argue the magnitude.
- The golden re-bless (45 demos + input-parity) is DELIBERATE and
  cause-documented (catalog_hash fold + genuine behavioral shift); the
  replay gate (bit-for-bit T1+T2) is the honest proof, not a defect.
- The fun-test gate is user-held (merge != done) — "no user playtest
  yet" is EXPECTED, not a blocker.

## The one hard blocker bar

The time-axis stretch must NOT leak into routing semantics,
serialization, packet contracts, or LOG_VERSION. The diff should touch
only: the pace knob (packet_bandwidth) + dependent constants scaled in
lockstep to preserve breach semantics (SLA latency tolerances 4x, E30
exit margin 4x) + the spawn-cadence constants migrated from core consts
to balance.json (terminal_spawn_interval_ticks, terminal_min_sep_tiles).

## What to VERIFY (not assume)

- The documented consequence: the x10 surge's packet multiplicativity
  dims to ~2.6x in units at 4x — verify this is the units-anchored
  design working as described, not a hidden demand-contract regression.
- Demand contracts (W9/W10/director) re-derived units-anchored —
  spot-check the re-derivation is honest.
- 46 pace-related test pins re-pinned across 17 files — sampled sanity
  only; the CI 10/10 + harness goldens are the bulk evidence.

## Vision caveat (non-k3 round)

Pixel verification MECHANICAL only (byte/hash/capture-diff); aesthetic
verdicts deferred; never faked.
