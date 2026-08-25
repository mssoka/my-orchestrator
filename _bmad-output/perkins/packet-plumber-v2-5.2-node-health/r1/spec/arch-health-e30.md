- **Interface.** `crisis_evaluate(state: ^Run_State, tick: u64)`; events
  `Warning_Raised{sign}`, `Crisis_Triggered{archetype, root_cause}`,
  `Crisis_Resolved{archetype}`.
- **Fairness enforcement.** `root_cause` is a structured ref to the specific
  topology flaw + a `preventive_redesign` description; test-pinned (§11.3):
  no crisis without a resolvable root cause; every root cause has a preventing
  edit; no crisis on a healthy within-capacity topology. Dedup by root-cause **across the whole
  activation** (E13): one *active* crisis per root-cause, period — a persistent
  flaw does not re-fire `Crisis_Triggered` every tick; re-trigger only after
  `Crisis_Resolved` (an optional cooldown in `crises.json` governs re-fire if
  design wants it). Era-advance interplay rules (E14/E15) ready for the [LATER]
  Era layer.

### 6.5 S5 — Network Health **[PROTO]**

- **Responsibility.** The aggregate loss condition `[GDD § Win/Loss]`: meter
  drains while any active class's SLA is breached (rate ∝ severity; **drain =
  max(severity), not sum, plus a per-tick cap** — E16, "never instant"), recharges
  when healthy; breach starts a grace countdown; expiry hits the meter; empty
  meter → **Error 404**, run over.
- **Boundary.** Reads SLA state from Flow (via the step's results); owns grace
  windows + meter. **Terminal suppression is sim-side (E17):** `health_update`
  never emits `Grace_Expired` once the meter is empty, and the terminal-event
  barrier (§4) skips the remaining systems in the tick after `Run_Lost` — one
  terminal event per run, by construction. **Hysteresis (E30):** SLA threshold
  crossings use enter/exit thresholds per class (catalog values) so an
  oscillating class doesn't emit crossings every tick; a re-breach during an
  active grace window is a no-op (one countdown per episode).
- **Interface.** `health_update(state: ^Run_State, tick: u64)`; events
  `Grace_Started{class}`, `Grace_Expired{class}`, `Meter_Changed{pct}`,
  `Run_Lost{}`.
- **No-soft-lock guarantee.** Recoverable until empty — test contract carried.

### 6.6 S6 — Era State Machine **[LATER]**

- **Spec (boundary + seam level).** The 6-era in-run arc `[GDD § M4]`: advance
  trigger (sustain SLA ≥ 95% across active classes for the milestone window
  AND modernize all in-service legacy pipes AND no active crisis — E15),
  unlock sets, legacy/degradation lifecycle. Data-driven from `eras.json`.
  Step ordering already reserved in `core.step` (§4); the advance-vs-crisis
  contracts (E14/E15) are decided here so the layer drops in without

| E12 | Timers pure functions of (seed, log) | load→re-step→assert-match test |
| E13 | One crisis per root-cause per tick | dedup by cause ref |
| E14 | Era advance preserves active crises; no mid-crisis demand spawn | [LATER] layer contract, decided now |
| E15 | Era advance blocked while crisis active | [LATER] layer contract, decided now |
| E16 | Drain = max(severity) + per-tick cap | health proc constant |
| E17 | `run_lost` supersedes `grace_expired` | sim-side suppression + terminal-event barrier (§4, §6.5) |
| E18 | Demolish cascades to overlay/policy refs; re-draw doesn't inherit | [LATER] (Era-6 overlays) |
| E19 | Offline outbox for HTTP leaderboard | [LATER] seam behavior, decided now |
| E20 | Backend rejection → non-blocking toast, retryable vs terminal | [LATER] seam behavior, decided now |
| E21 | Slow-mo, never skip ticks | `MAX_STEPS_PER_FRAME` (§11.1) |
| E22 | Pool exhaustion → drop lowest-priority lane first | sim-side integer check (ODN-8) |
| E23 | Batch validate-all-then-apply | `apply_all` atomicity + test |
| E24 | Zero-demand class = neutral SLA | accumulator guard |
| E25 | Run descriptor carries `modifiers` | in the save header from day one |
| **E26 (new)** | Terminal↔terminal draw rejected (art-canon topology rule) | `Edit_Error.Terminal_To_Terminal` (§6.1) |
| **E27 (new)** | Junction demolish = atomic batch: incident pipes first (edge-id order, each per E1), then the vertex | §6.1 |
| **E28 (new)** | Unroutable demand is not spawned; accrues as SLA-undelivered | §6.2 |
| **E29 (new)** | **Automatic under per-hop forwarding** — no stale spawn-time routes; topology changes propagate via table rebuild at next sync; in-flight packets re-forward at the next junction. E1 demolish is the (now-only) forced-reroute exception (routing ruling, lavish 2026-08-10) | §6.2 |
| **E30 (new)** | SLA hysteresis (enter/exit thresholds); re-breach during an active grace is a no-op | §6.5 |
| **E31 (new)** | Spawn validity: connectable-within-span + min separation, rejection-sampled from the same rng stream | §6.1 |
| **E32 (new)** | Fresh-run seeds from app-layer OS entropy, logged in the save header | ODN-9 |

---

## 12. Performance

| Concern | Strategy |
|---|---|
| Sim cost | Fixed 20 Hz tick; integer math; SOA hot loops (cache-friendly by layout); packets advance by bandwidth-units/tick. Late-era worst case (hundreds of packets, ~30 nodes) is comfortably inside budget for a native build — well under the GDScript cost of the prototype slice (desktop-observed). The phone budget itself is unmeasured (GDD OQ-3 + §18 OQ-1) — no mobile perf claim is made |
| Render cost | Immediate-mode batched draw calls; static map cached in a RenderTexture (redrawn on pan/zoom only); packet dots are shape calls from arrays (no per-entity objects); ~O(pipes + packets) draw calls per frame |
| Frame budget | Accumulator caps catch-up steps; slow-mo degradation (E21); render interpolates → 60 fps motion from 20 Hz sim |
