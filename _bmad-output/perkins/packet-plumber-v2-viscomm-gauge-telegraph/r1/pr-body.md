## viscomm(gauge): gauges telegraph, not snap (audit finding B)

Health / pool / SLA gauges snapped value-to-value; when values move fast
(drain, refill, SLA decay) the player reads a strobe, not a level. Each
gauge now carries a **render-owned display value** that eases toward the
raw sim value:

- **EASE16** — a pinned 16-entry ease-out table (the PULSE16 §10.4
  no-transcendentals pattern), indexed by a tick-derived integer phase.
  `[0]=0` pins tween-start continuity (no pop), `[15]=1` pins exact
  arrival (a finished tween reads raw to the byte). Compile-time `when`
  guards pin endpoints/cadence/threshold (the `BROKEN :: 1/0` idiom).
- **Chunk-flash cue** — an instantaneous delta ≥ `CHUNK_PCT` (25 units)
  fires a one-shot ghost of the jumped region (fill geometry, `CHUNK_FLASH`
  table alpha, 3-tick fade), then the ease carries the level across.
- **Reduced motion** (7.3/E9.2) snaps display to raw immediately and
  suppresses the cue (the `pulse_read` pattern).
- Surfaces: health meter bar fill, pool gauge bar fill, SLA avg-ms +
  loss-pct display numbers. Truth channels stay RAW — numbers, counters,
  breach latches, state colors.

### Golden safety (zero churn, by construction)

The harness capture path never feeds gauge targets, so an **unfed gauge
reads raw exactly** — 49 demos green, zero golden bytes changed (the
`pkt_interp` precedent: the app steps presentation, the harness renders
snapshot-exact). Paused frames step nothing, so the ease freezes with the
sim (phase derives from the tick). A fresh run seeds display = raw (no
fill animation at run start).

### Verification

- `odin test app/render` — 91 (83 + 8 new gauge pins: table/tween/chase/
  chunk/reduced-motion/pause/feed/harness-inert)
- `odin test app` — 46; `odin test core` — 261 (untouched)
- `bin/harness run` — 49 demos green, zero golden diffs
- `bin/harness palcheck` — all green incl. **section 6**, the draw-path
  leg: live rlsw render, pixel-scanned mid-ease fill boundary at the
  EASE16-predicted column (~213px vs raw 182), ghost blend present while
  the cue lives / pure track after expiry, reduced-motion snap to raw
- **Mutation legs (RED→GREEN)**: easing bypassed (`gauge_read` := raw)
  → palcheck section 6 FAILS (fill collapses to raw); restored → green.
  Chunk-cue deleted → ghost leg FAILS; restored → green. Deliberate-fail
  probe run on the new test binary.
- `tools/ci-local.sh --mac` — all 13 gates green

### Decisions & rationale

- **Continuous deltas ride the active tween** (target chases raw, phase
  NOT reset); only a chunk crossing re-anchors from the current display.
  Rationale: re-anchoring on every small delta would make a continuous
  drain crawl (the ease would restart at 4% coverage each tick) — the
  chase keeps motion bounded while preserving continuity (pinned: the
  retarget display move ≤ raw move + the tween's own per-tick step).
- **SLA chunk-flash omitted**: the SLA rows are text (no chunk geometry
  to flash); the eased display numbers kill the strobe. The two BARS
  carry the flash cue (health, pool).
- **`draw_health_meter` gained a `tick` param** — the ease phase derives
  from the tick at read time; the harness passes its existing tick with
  the gauge unfed (byte-identical by construction). Same for the five
  other harness call sites.
- **Roster cap 8** on the SLA ease slots (the node_health card's pinned
  catalog cap); classes beyond it simply never feed — an unfed gauge
  reads raw (the zero value IS the fallback).
- **bmad-build skill render waiver** (standing Silas ruling 2026-08-21):
  `_bmad/scripts/render_skill.py` is absent from this BMAD install — the
  pre-rendered project snapshot at
  `_bmad/render/bmad-build/packet-plumber-c02b60b148b2/d1343645b747d61a6ec8/`
  (generated for this exact repo root) was followed instead, and the
  step-04 review layers (blind-hunter / edge-case-hunter /
  verification-gap) ran as mega-minions per the playbook's
  enforced-from-2026-08-23 rule.
- **No golden re-bless** — none needed (the unfed-gauge contract held
  through every health-on capture; a legit golden shift would have been
  a STOP-and-flag canon decision).

### r1 review round (blind-hunter + edge-case-hunter + verification-gap)

Patched: zombie tween (arrived-but-active ate later small retargets — the
strobe would return after the first tween; re-engage + pin), game-over
freeze (terminal snaps gauges — the empty meter is the loss surface), lazy
SLA seed (a hidden "-" readout no longer seeds at 0 — the first VISIBLE
number is raw), terminal-aware feed folding into feed_drop_sites + 2 app
wiring tests (start_run zeroes; the presentation feed lands targets — the
vacuous-wiring class), single-source derivations (pool_fill_pct /
sla_avg_ms / sla_loss_pct shared by feed + draw), SLA slots 8 → 16 (the
planned roster is 9 classes), per-unit chunk thresholds (CHUNK_PCT vs
CHUNK_SLA_MS), flash-flag expiry hygiene, pool-gauge palcheck draw-path
leg + geometry prelude, this _pr_body_ artifact (the repo convention).

Rejected (rationale): eased numbers transiently near tolerance — bounded
by recent RAW values (the telegraph's purpose, ≤0.4 s); pool/SLA
draw-geometry export — pinned via prelude asserts instead.

Deferred (deferred-work.md): the loop→feed_drop_sites call-site pin (the
pre-existing debug_surface_smoke.sh class — needs a headless app-drive
harness); SLA text draw-path pixel pin (app package not harness-
importable; folds into the same story).

