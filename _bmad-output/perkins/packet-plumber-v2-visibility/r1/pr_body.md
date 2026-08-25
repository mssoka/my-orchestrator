## v2-visibility: make invisible chokepoints visible in-game

The user-ordered visibility job (ruling 2026-08-14: *"if players need a manual to play, that's a design failure"*). The surge-explainer's Section C named five invisible design gaps, each confirmed in code; this PR spends that debt — telegraph **in-game**, not docs out-of-game.

### Gaps shipped (all five)

| # | Gap | Surface | Code |
|---|---|---|---|
| 1 | **Pool exhaustion** (E22) — pool cap + map-wide shedding had no HUD surface | **Pool-pressure gauge** (bottom-left, above the SLA block): `POOL <in-flight>/<cap>` + fill bar colored by the shared `warnings` thresholds (green < 70 / amber < 90 / red ≥ — the same ladder the rings use), + a `SHEDDING +N` tag when E22 drops land in the ~2 s window | `app/render/visibility.odin:72` |
| 2 | **Drop sites** — drops recorded per tick but never rendered | **Drop-site markers**: a fading cross + aggregated count at the shed bundle's midpoint (E9), anchored via the canonical `bundle_lo/hi` node pair with an identity guard against slot renumbering; E22 sites are map-wide by construction and ride the gauge's SHEDDING tag | `app/render/visibility.odin:118` |
| 3 | **Queue depth** — the 6-packet lane bound had no depth readout | **Queue-depth row** on the 5.8 QoS panel (selected pipe's bundle): per-lane depth vs `lane_queue_packets`, at-bound lanes turn critical | `app/qos_panel.odin:446` |
| 4 | **Why-dropped** — SLA gauges showed loss% but never the cause | **Reason split on the SLA gauges**: `(pool N / queue M / severed K)` per class — the severed residual names the 2.3 silent-cull drops, so the split always sums to the gauge's own `drop N` | `app/main.odin:1416` |
| 5 | **Node strain cause** — rings show THAT a node is stuck, not WHAT | **Stuck-by-class line** on the 5.2 node-health hover card: `stuck: Email 3 - Streaming 2` (capped at 2 classes + `+N more`, screen-clamped), only when a node actually has stuck packets | `app/render/node_health.odin:48` + `core/node_health.odin:101` |

### Determinism — no LOG_VERSION bump, T1 byte-identical

Everything is **presentation-side**: the app copies the per-tick `Drop_Site` scratch (`state.flow.drop_sites` — the same data the crisis engine reads) into an app-owned ~2 s ring after each step; nothing is re-derived or re-recorded, no serialization change, no new core state (the one core addition, `node_stuck_by_class`, is a pure read over the same pile `node_health_measure` sums). **Proof: `tools/harness.sh run` → 29/29 demos green, byte-identical** (T1 state hashes + T2 pixels unchanged).

**Why no T2 fold:** every surface is drawn from `draw_hud`, which the harness T2 capture path (`harness/goldens.odin:capture_frame`) never calls — the same app-layer construction as the 5.2 node-health card. Zero golden shift by construction, verified by the green harness run.

### The Section B numbers they validate against

- The pool gauge reads the sim's own truth: in-flight = `len(flow.packets)` at the step boundary — exactly the count the E22 guard (`flow_try_spawn`) compares against `pool_max_packets` (512). Section B: the cap is **fixed** (a protection, not a lever) — the gauge is diagnostic; capacity levers show their effect as the bar recedes and SHEDDING stops.
- The why-dropped split satisfies the pinned invariant (every drop is pool OR queue OR the severed cull; `demand_seen == delivered + dropped + live`).
- The queue-depth row cites `lane_queue_packets` (6) — the exact bound the E9 ladder sheds from.
- All new strings honor quiet-at-green: markers only while shedding, split only when dropped > 0, stuck line only when stuck.

### Terminology citations (in-flight audit canon)

New HUD strings use the renamed networking terms per the 2026-08-15 audit verdicts (merged into `v2` as PR #55 mid-flight; this branch **rebased onto it**): **drop precedence** (never "drop ladder" — the markers/tag describe sheds without naming the ladder), **congestion/utilization** vocabulary, and **lane stays "lane"** on the player HUD (the QoS queue-depth row reads per-lane depth; the sim-side "class queue" rename is the audit's, not this PR's).

### GDD canon amendment (hard req 4)

- `decision-log.md` — dated entry: legibility in-game is a design requirement; invisible chokepoints are defects, not mysteries; every loss state must be readable without a manual. Proves the ruling source + the shipped surfaces.
- `gdd.md` — one additive row in the M5 warning-sign table + the canon sentence (the one section that needed it).

### Review

Blind + edge-case hunter round before the PR; both MEDIUM findings fixed (severed residual in the split; bundle-slot identity guard on markers) plus five LOW hardenings; two findings rejected with disk evidence (min-window clamp makes one overlap impossible; the card-vs-ring "disagreement" is the traceability surface's purpose).

### Decisions & rationale

- **App-layer over world-layer**: surfaces live in `draw_hud` so T2 goldens cannot shift — a deliberate trade of "not in the harness capture" for "zero golden churn" (the 5.2 card precedent).
- **App-owned ring over core state**: the ~2 s marker window + per-class reason counters are app presentation state, fed from the existing per-tick scratch — keeps core serialization surface untouched (no LOG_VERSION bump) at the cost of a small app-side accumulator.
- **Queue depth on the QoS panel (inspect) rather than always-on tags**: the panel is the pipe's inspect surface; always-on depth numbers on every pipe would violate quiet-at-green and force a T2 fold. The drop marker tells you WHICH bundle to select; the panel shows the depth.
- **E22 rides the gauge, not the map**: map-wide sheds have no per-link home by construction; a gauge tag is the honest marker (the explainer's own framing).
- **No balance/mechanic changes**: the pool cap, lane bound, ladders, and strain formulas are untouched — this job is visibility only; the 5.9–5.12 traffic-model threads remain on their own slots.

### Verification

- `tools/harness.sh run` — 29/29 green (T1/T2 byte-identical)
- `odin test core` — 184 pass (incl. the new `test_node_stuck_by_class_breakdown` pin)
- `tools/lint.sh` — all gates green
- `odin build app` — clean
- Scratch pixel-scan (rlsw shadow + LoadImageFromScreen): pool bar fill, SHEDDING tag, and drop-marker positions verified programmatically; QoS depth row layout measured against the rendered label


