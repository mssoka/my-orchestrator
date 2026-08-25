---
title: 'Story 4.1 — Warning signs + forecast'
type: 'feature'
created: '2026-08-13'
status: 'in-progress'
baseline_commit: 9632f83
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md'
  - '{project-root}/_bmad-output/implementation-artifacts/epic-4-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The surge-survival fun loop has no telegraph: nothing warns the player before trouble, so the P3 fairness surface ("I should have seen this coming" `[FORGE #3]`) does not exist yet.

**Approach:** Add the warning surface (story 4.1, slice 4): strain metrics from Topology + Flow feed node 🟡/🔴 states + pipe pressure + a demand forecast — all with lead times — plus a forecast "weather report" panel that names incoming SetPieces with a countdown. Telegraph ONLY: the surge firing (4.2) and the health-meter win/lose (4.3) are out of scope; 4.1 only ever *names* trouble.

## Boundaries & Constraints

**Always:**
- **Core eval** (`core/warnings.odin`, NEW): `warning_evaluate(state, tick, cat)` called inside `core.step` AFTER `flow_step`, BEFORE `win_lose_eval` (arch spine: flow → crisis → win/lose). Pure (ODN-1), integer-only (ODN-10), arrays only (no maps), no new commands (**LOG_VERSION stays 3**).
- **`Crisis_State` on `Run_State`** (types.odin; arch §8.2): `node_strain: [dynamic]Strain_Level` (parallel to node slots), `pipe_strain: [dynamic]Strain_Level` (parallel to pipe slots — a pipe's level is its bundle's pressure; the bundle is the capacity unit), `forecast: [dynamic]Forecast_Entry`. **All DERIVED per tick** (rebuilt identically on replay from serialized state — same status as `lane_caps`/`sla_breach`; never serialized in full). `Strain_Level { None, Amber, Red }`; `Forecast_Entry { sp_index, class, multiplier, start_tick, countdown_ticks, active }`.
- **Strain measure (the pinned contract):** node utilization = Σ `packet_bandwidth` of packets RESIDENT at the node that **FAILED a forward attempt** (`Packet.waiting_ticks >= 1` — incremented in flow.odin's forward pass when no route exists, cleared on every successful forward) × 100 ÷ `node_types[node_type].throughput_units` (integer percent). A packet that forwards next tick — fresh spawn OR fresh transit arrival — has `waiting_ticks` 0 and NEVER strains (the no-flicker contract; the transit case was the reason the spawn-tick exclusion alone was insufficient — see the change log). Pipe pressure = the FULLEST lane queue's depth on the bundle vs its E9 bound (`lane_queue_packets × packet_bandwidth`): a lone packet is 1/6 of a bound (17 %, healthy); a lane at its bound (6 packets) is 100 % — the ladder is dropping. "Pressure climbing toward saturation" (GDD M5), not busy-ness.
- **Thresholds + leads in `balance.json` `warnings` block** (ODN-5; art-direction "Trigger `[balance.json]`"; GDD Numerical Design): `node_amber_pct 70`, `node_red_pct 90`, `pipe_amber_pct 70`, `pipe_red_pct 90`, `node_strained_lead_ticks 600` (30 s), `node_critical_lead_ticks 200` (10 s), `pipe_pressure_lead_ticks 400` (20 s) @20 Hz. Fail-fast validation: amber < red ≤ 100, leads > 0. **Deliberate consequence (documented, 3.2 precedent):** a balance.json content addition folds into `catalog_hash` → ALL `.t1` manifests + `.log.bin` headers re-bless mechanically.
- **Transitions vs the prior tick's levels emit events** (ODN-14): `EVENT_TAG_WARNING_RAISED :: u8(6)` / `EVENT_TAG_WARNING_CLEARED :: u8(7)`, payload = `sign` (Warning_Sign: Node_Strained / Node_Critical / Pipe_Pressure / Pipe_Critical) + `target` (node id / pipe id). None→Amber raises the amber sign; Amber→Red raises the critical sign; any down-step clears the level that ended (one event per transition). `Event` gains `sign: u8` + `target: u32`, serialized **tag-conditionally** (append-only — pre-4.1 event streams byte-identical). **Forecast emits NO events** (a panel read; the serialized rows are the pin).
- **Forecast:** rows = era set-pieces with `start_tick - forecast_lead_ticks ≤ tick < start_tick + duration_ticks`; `countdown_ticks = start_tick - tick` (0 once active; `active` flags the in-window/active span). Reads the catalog schedule only — never fires anything (4.2).
- **Serialization** (serialize.odin): new `warnings` section, **absent-when-empty** (zero traffic → zero bytes, so boot/draw/place shift ONLY via the catalog_hash fold): non-None node strain entries (node id + level, slot order), non-None pipe strain entries (pipe id + level, slot order), forecast rows (sp_index, class, multiplier, start_tick, countdown, active).
- **Render — warning state is never color alone** (art-direction §6.1): Amber node = amber ring + `!` glyph + slow pulse; Red node = red ring + `!!` glyph + fast pulse; rings render ONLY on non-healthy nodes (the canon's healthy ambient ring is slice-7 juice — flagged). Pulse = pinned 16-step table indexed by `(tick, node id)` — deterministic, no transcendentals (§10.4). Pipe pressure = translucent state-colored overlay stroke on member pipes of a pressured bundle. The forecast panel (`app/render/forecast.odin`, NEW — shared by the app HUD + the harness capture) draws **zero pixels when empty**. Text via `rl.DrawText` (rlsw-verified).
- **App session:** `start_run` sets `state.era = 3` + **goal 0 / cap 0** (win/lose disabled — the 4.1 sandbox must outlast the forecast window; the real win/lose is 4.3's health meter) — the launchable needs the surge schedule + director traffic. HUD gains the panel + a strain legend; title → story 4.1.
- **Golden:** NEW `demos/warn.dem` (era 3 + `fixture qos` + draws + lane categorization + burst): T1 pins forecast rows + the warning event stream at exact ticks; T2 captures = forecast countdown frame, amber frame, red/pressure frame (incl. the surge ACTIVE "NOW" frame). Re-bless = ALL `.t1`/`.log.bin` (catalog_hash fold — mechanical, cause-documented) + T2s that shift (a demo that strains at a capture gains rings/halos: sla + qos_contention (the saturated router row), qos_emphasis (era-3 load), qos.dem's 65 s capture (the panel + surge strain), lose.dem (its own stuck packet — the demo's scenario IS the strain: the residential telegraphs 🔴, cause-documented); boot/draw/flow/win/bundle/ecmp/place/demolish T2s stay pixel-identical — the negative proof) + `warn.dem` (new). **STOP + flag any shift beyond the documented set** (e.g. a zero-traffic demo's T2 moving).

**Ask First:** none expected — thresholds/leads are GDD-canon starting points, tunable in balance.json.

**Never:** no crisis firing / root_cause / preventive_redesign (4.2), no Network Health meter or win/lose changes (4.3), no new player commands, no E30 hysteresis/grace machinery (4.3), no windowed strain (the only smoothing is the fresh-spawn exclusion), no new catalogs, no floats in core, no maps in core, no changes to the demand director or the flow's drop ladder.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| HAPPY_PATH | era-3 traffic + the streaming surge scheduled | amber → red node transitions with `Warning_Raised` at exact ticks; pressure mirrors on the bundle's pipes; forecast panel rows with countdowns | n/a |
| Fresh spawn | a packet at its spawn tick | excluded from the node's strain (no flicker); the node reads healthy | n/a |
| Relief | strain drops below amber | one `Warning_Cleared` naming the ended level per transition | n/a |
| E24-like neutrality | zero demand | no strain, no events, warnings section absent from the hash | n/a |
| Forecast boundaries | tick before `start-lead` / in window / active / after end | no row → row with exact countdown → countdown 0 + active → no row | n/a |
| Terminal | run frozen after `Run_Lost` | warning state frozen (barrier — warning_evaluate never runs post-terminal) | n/a |
| Replay | blessed log re-sim | identical strain levels + identical warning event stream (E10) | replay gate rejects divergence |
| Catalog validation | amber ≥ red, or a lead ≤ 0 | load aborts with a named error | fail-fast (ODN-5) |

## Code Map

- `core/types.odin` -- `Strain_Level`, `Warning_Sign`, `Forecast_Entry`, `Crisis_State`, `Run_State.crisis`, `Event.sign`/`target`, tags 6/7, `run_init`/`run_destroy` wiring
- `core/warnings.odin` (NEW) -- `warning_evaluate`: node strain + pipe pressure + forecast rows + transition events
- `core/step.odin` -- the `warning_evaluate` call (after `flow_step`, before `win_lose_eval`)
- `core/serialize.odin` -- the warnings section (absent-when-empty) + tag-conditional 6/7 payloads
- `core/catalog.odin` -- `Balance.warnings` parse + fail-fast rows
- `data/balance.json` -- the `warnings` block (the catalog_hash fold)
- `core/warnings_test.odin` (NEW) -- the contract pins (I/O matrix rows + replay)
- `core/catalog_test.odin` -- the warnings validation rows
- `app/render/view.odin` -- `draw_world`/`draw_nodes` gain `crisis` + `tick`; health rings + `!`/`!!` glyphs + pulse; pressure overlay strokes
- `app/render/forecast.odin` (NEW) -- the weather-report panel (app HUD + harness capture share it)
- `app/main.odin` -- era-3 session, HUD panel call, title
- `harness/goldens.odin` -- `capture_frame` gains `crisis` + `tick` + the panel draw
- `demos/warn.dem` (NEW) -- the launchable golden
- `goldens/*` -- documented re-bless (ALL `.t1`/`.log.bin`; shifted T2s; `warn.dem` new)

## Tasks & Acceptance

**Execution:**
- [x] `core/types.odin` -- the enums + `Crisis_State` + `Run_State.crisis` + Event fields/tags + init/destroy wiring
- [x] `core/warnings.odin` (NEW) -- `warning_evaluate` (strain, pressure, forecast, transitions/events)
- [x] `core/step.odin` -- the eval call in spine order
- [x] `core/serialize.odin` -- the warnings section + tag-conditional payloads
- [x] `core/catalog.odin` + `data/balance.json` -- the warnings block + fail-fast
- [x] `core/warnings_test.odin` (NEW) -- every I/O-matrix row + the replay pin
- [x] `core/catalog_test.odin` -- validation rows
- [x] `app/render/view.odin` + `app/render/forecast.odin` (NEW) -- the warning render + panel
- [x] `app/main.odin` -- era-3 session + HUD panel
- [x] `harness/goldens.odin` -- capture signature + panel draw
- [x] `demos/warn.dem` (NEW) -- author → run → read the actual warning-event stream → pin it in comments + tests
- [x] Golden pass -- re-bless ALL (catalog_hash fold with proof), re-bless only cause-documented T2 shifts, STOP+flag anything else; `drift-check` green

**Acceptance Criteria:**
- Given era-3 traffic with the surge scheduled, when strain crosses the balance thresholds, then nodes/pipes transition amber → red with lead times in the data, `Warning_Raised`/`Cleared` events fire at exact ticks, and a 🔴 node is always traceable to a measured strain (ring + glyph + pulse — never color alone).
- Given the forecast window, when the tick enters `start - lead`, then the forecast state carries the SetPiece with a countdown and the panel names it; the forecast never fires anything.
- Given any run, when it replays from the action log, then identical warning state + identical event stream (E10).
- Given the golden pass, when the harness runs, then every shifted golden has a documented cause (catalog_hash fold; the demo's own strain/panel content); zero-traffic demos' T2s are pixel-identical; any other shift STOPS the line.

## Design Notes

- **Why resident-units-excluding-the-spawn-tick:** "waiting = strain" is the honest telegraph. A packet that spawns at a healthy house and forwards next tick is at the node for one tick — counting it would flicker every house to 600 % (residential throughput 5 vs packet_bandwidth 30). Excluding `spawn_tick == tick` leaves only packets that FAILED to move — a stuck house (queue full / unroutable) or a backed-up junction. Router (40 u/s): amber at 1 waiting packet (75 %), red at 2 (150 %); content_host (80): amber at 2, red at 3; residential: red at any waiting packet (600 %) — honest: a stuck house IS critical.
- **Per-pipe-slot strain mapping:** the render indexes by slot (O(1), no lookup); the pressure value is the BUNDLE's (pooled capacity is the capacity unit — the 2.1 model), replicated to each member pipe.
- **The golden-shift story (the acceptance's "must not shift" clause):** the ONLY universal shift is the deliberate balance.json content fold into `catalog_hash` (the 3.2 precedent — every `.t1` hash + `.log.bin` header changes by construction). Traffic demos additionally shift where the demo itself strains: sla.dem / qos_contention.dem gain rings in strained captures; qos.dem's 65 s capture gains the panel + surge-strain; qos_emphasis.dem gains rings if its captures strain. Every one is cause-documented; boot/draw/place/flow/win/ecmp/bundle/demolish T2s must stay pixel-identical (the negative proof — lose is NOT in the set: its stuck packet telegraphs, review r1 N3). A shift with NO cause = STOP + flag.
- **No forecast events:** the serialized forecast rows ARE the replay-proof pin (like the SLA section); the panel is a read. 4.2's `Crisis_Triggered` lands on the same event seam.
- **The pulse is cosmetic:** a pinned 16-step table (CIRCLE16 precedent), phase from tick + node id, step-size differs by state (slow/fast) — deterministic in goldens, no transcendentals, never feeds back into state.
- **warn.dem authoring:** era 3 director traffic + explicit burst spawns; the seeded sim makes every crossing tick exact. Author → run → READ the real event stream (scratch collection) → pin the ticks in the demo narrative + the test (the 3.4 golden-verified pattern).

## Verification

**Commands:**
- `odin test core` -- all suites green incl. the new warnings_test pins
- `tools/lint.sh` -- all 5 gates green
- `tools/harness.sh run` -- green after the documented re-bless; the negative proof = zero-traffic demos' T2 pixels byte-identical
- `tools/harness.sh save boot draw place flow win ecmp bundle demolish` -- must be T2 no-ops (pixel-identical; `.t1`/`.log.bin` re-bless only — lose is deliberately OUT: its stuck packet telegraphs 🔴, cause-documented)
- `tools/harness.sh save qos qos_emphasis qos_contention sla` -- cause-documented re-bless, then `tools/harness.sh run` -- PASS
- `tools/harness.sh save warn` -- the new golden; `tools/harness.sh drift-check` -- every mutation rejected
- `odin build app` + run -- era-3 session: the panel names the surge ~30 s out; oversubscribe → a node shows 🟡 with lead time, then 🔴; pipes show pressure