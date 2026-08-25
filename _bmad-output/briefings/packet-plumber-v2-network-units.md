# packet-plumber-v2-network-units

## Task

Speak network-engineer natively (user ruling 2026-08-23: "rather than
units, use proper networking terms — Mbps/Kbps/Gbps capacity, bytes
for packet sizes; would help me understand as a network engineer") AND
fix the utilization bug the NOC exposed (queue-occupancy masquerading
as utilization). One coherent job: honest counters + real units.

## The bug being fixed (ground truth, core/stats.odin)

util_pct = (queued_packets × packet_bandwidth) × 100 / cap_units —
the BACKLOG SNAPSHOT divided by ONE TICK of capacity. One queued
packet on a standard pipe: 120/15 = 800% → clamped 100%. Honest
utilization = octets TRANSMITTED per window ÷ (rate × window) — the
ifHCOutOctets/ifSpeed pattern. Queue depth becomes its OWN display
signal (it is one). Warnings (amber 70 / red 90) ride the honest
metric.

## The unit model (data-layer rescale, isomorphic math)

1. **Link tiers → real rates**: narrow = **10 Mbps** (residential
   access) · standard = **100 Mbps** (distribution) · wide = **1 Gbps**
   (core) — the access/dist/core hierarchy the user already builds.
2. **Packets → bytes**: uniform frame first (1500 B standard MTU);
   per-class sizes (email 512 B, streaming ~9 KB jumbo) as a FOLLOW-UP
   knob, not this job's scope creep — note the extension point.
3. **Serialization delay is the transit formula**: transit =
   frame_bits ÷ rate — the game's ceil(packet_bandwidth/cap) IS this
   in disguise. Introduce a named SIM_TIME_SCALE (the game clock runs
   slowed for readability — MM's readable-time): real units, readable
   pace. CONSTRAINT: standard-link 1500B transit stays ~8 ticks (the
   MM-pace ruling must NOT drift — retune the scale so the feel is
   byte-identical to today).
4. **Every display goes native**: NOC rail + HUD + warnings in
   Mbps/Kbps/Gbps (auto-scaled), packet sizes in bytes/KiB, drops in
   packets, queue depth in packets, utilization % from the new octet
   counters. D-key rail relabels accordingly.

## Rules (hard)

1. Sim math stays isomorphic — this is units + counters + displays,
   NOT a gameplay rebalance. The pace feel must be unchanged
   (byte-identical golden timing on the procedural map).
2. LOG_VERSION-safe: old replays pin old units (map/units as
   determinism inputs); document the serialization impact (if any) —
   if replay bytes change, that's a finding, not a re-bless.
3. E9/E22 bounds unchanged (6 packets / 512 pool — packets stay
   packets).
4. Full golden re-bless expected where DISPLAYED numbers change
   (NOC/HUD pixels) — cause-documented; sim-truth goldens must NOT
   move (T1/T2/replay hash-equal).
5. KYLE verifies: the rail reads network-native and the utilization
   numbers are HONEST under a known synthetic load (e.g. a single
   stream on one link reads well under 100%).

## Acceptance

- Utilization from octet counters (windowed); queue depth its own
  row; amber/red on honest numbers; single-stream link reads < 100%.
- All displays in real units (KYLE-verified legibility + correctness).
- Pace feel unchanged (golden timing on procedural pins).
- T1/T2/replay hash-equal (sim truth); display goldens re-blessed
  cause-documented.
- pr_review: 1.

## Skills policy

bmad-quick-dev; KYLE for the rail verification.

## Model policy

deepseek-v4-flash, --thinking max. KYLE: glm-4.6v.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-network-units
- base: v2 (fresh head; coordinate vs dublin-board — no file overlap
  expected: stats/display vs map/growth; Silas coordinates merge order)
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
