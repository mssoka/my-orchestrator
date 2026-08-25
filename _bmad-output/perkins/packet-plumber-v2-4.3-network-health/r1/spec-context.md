# Spec + context for Perkins lenses — packet-plumber-v2-4.3-network-health (PR #43)

You are reviewing PR #43 (reviewed sha 8659070ed0a5ec176dc15eece6e807432c9a2a34) on repo Packet-Plumber, base v2. Story 4.3 — Network Health meter + win/lose/retry (closes Slice 4, the fun-test loop). Repo root for verification reads: /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-4.3-network-health-r1 (detached at the reviewed sha).

## 1. Job briefing (condensed acceptance)

1. **Network Health meter** — drains on sustained SLA breach: grace countdown starts on breach; drain = **max(severity) + per-tick cap** (never instant) `[E16]`; SLA hysteresis (enter/exit thresholds); re-breach during active grace = no-op `[E30]`; recharges when healthy; **empty → `Run_Lost` (Error 404)**.
2. **Terminal-event barrier** — after `Run_Lost`, the rest of the tick is skipped; **one terminal event per run** `[E17]`.
3. **Win condition** — uptime ≥ 90% through the surge → `Run_Won`.
4. **Retry** — creates a fresh run context (fresh arena, no leakage — the ODN-13 pattern); no-soft-lock property test passes `[FORGE #3]`.
5. **Goldens** — T1 + T2 of win AND lose frames; the no-soft-lock property test.
6. **Launchable increment** — the full surge-survival loop: predict → survive or drain → win/lose → retry.
7. **Scope guard:** the meter + win/lose/retry ONLY. NOT 4.4+ (no such story), NOT the remaining four crisis archetypes, NOT era content. LOG_VERSION stays unless the new terminal events truly require it — flag first (the implementer flagged: LOG_VERSION stays 3).

## 2. Story 4.3 spec (stories-v2.md, verbatim)

- **Slice:** 4 · **Epic(s):** E6.1, E6.2, E6.3, E6.4 · **Systems:** Network Health (S5), win/lose/retry flow.
- **Goal.** The aggregate loss condition: a Network Health meter drains on SLA breach (grace countdown), recharges when healthy, empties → Error 404 → run over. Win = uptime ≥ 90% through the surge. Retry restores a clean state. No-soft-lock guaranteed.

**Given/When/Then:**
- **Given** the Network Health meter (drain/grace/recharge) + the win/lose thresholds;
- **When** an active class's SLA breaches (sustained);
- **Then** a grace countdown starts; drain = **max(severity) + per-tick cap** (never instant) `[E16]`; SLA hysteresis (enter/exit thresholds), re-breach during active grace = no-op `[E30]`; the meter recharges when healthy; empty meter → `Run_Lost` (Error 404); the terminal-event barrier skips the rest of the tick after `Run_Lost` — **one terminal event per run** `[E17]`; **win fires at uptime ≥ 90%** through the surge; retry creates a fresh run context (no leakage); the **no-soft-lock property test passes** `[FORGE #3]`.

- **Edge-case contracts:** `[E16]` drain, `[E17]` terminal barrier, `[E30]` hysteresis, no-soft-lock. **Golden:** T1 + T2 of win + lose frames; no-soft-lock property test.
- **Launchable increment:** play the full surge-survival loop — predict, survive or drain, win/lose, retry.

## 3. Architecture pins (verbatim)

From architecture-v1.md edge-case table:
- **E16** | All classes breach simultaneously | Drain = `max(severity)` (not sum) + a per-tick drain cap → meter always recoverable, never instant. No-soft-lock test.
- **E17** | Grace expires same tick meter empties | Signal precedence: `run_lost` supersedes `grace_expired` (one terminal event).
- **E30** | SLA hysteresis (enter/exit thresholds); re-breach during an active grace is a no-op | §6.5.

From odin-architecture-v1.md §6.5 (S5 — Network Health [PROTO]):
- **Responsibility.** The aggregate loss condition `[GDD § Win/Loss]`: meter drains while any active class's SLA is breached (rate ∝ severity; **drain = max(severity), not sum, plus a per-tick cap** — E16, "never instant"), recharges when healthy; breach starts a grace countdown; expiry hits the meter; empty meter → **Error 404**, run over.
- **Boundary.** Reads SLA state from Flow (via the step's results); owns grace windows + meter. **Terminal suppression is sim-side (E17):** `health_update` never emits `Grace_Expired` once the meter is empty, and the terminal-event barrier (§4) skips the remaining systems in the tick after `Run_Lost` — one terminal event per run, by construction. **Hysteresis (E30):** SLA threshold crossings use enter/exit thresholds per class (catalog values) so an oscillating class doesn't emit crossings every tick; a re-breach during an active grace window is a no-op (one countdown per episode).
- **Interface.** `health_update(state: ^Run_State, tick: u64)`; events `Grace_Started{class}`, `Grace_Expired{class}`, `Meter_Changed{pct}`, `Run_Lost{}`.
- **No-soft-lock guarantee.** Recoverable until empty — test contract carried.

Spine order (odin-arch §4, core/step.odin): topology apply → routing/bundles rebuild → flow_step → warning_evaluate (4.1) → crisis_evaluate (4.2) → **health_update (4.3)** → win_lose_eval (1.4+4.3). Terminal-event barrier at the top of `step`: once terminal, the tick is skipped entirely (state.tick NOT advanced, frozen hashes).

## 4. GDD win/lose rows (verbatim)

- **MVP prototype row (Win):** Survive the streaming-era surge: hold SLA uptime ≥ 90% through the surge window (≈ 90 s) `[ASSUMPTION: prototype tuning]`.
- **MVP prototype row (Lose):** Uptime collapses below the threshold during the surge → fail → retry.
- **The Network Health meter (the loss mechanic).** A single health bar = aggregate internet health (overall SLA uptime across active traffic classes). It **drains** whenever any class's SLA is breached … and **recharges** when uptime is healthy. A breach starts a **grace countdown** … let it expire and the meter takes a hit; if the meter empties, **Error 404**, run over. Hard-SLA classes drain it *fast* (short grace) — but never instant, so it's always telegraphed. Fair (forge #3): the meter drains only on *visible* strain, with a recoverable grace window, no random death.
- **No soft-locks:** there is always a way to reroute or upgrade out of a crisis — the meter is recoverable until it empties. A true dead-end is a design bug, not a difficulty feature.
- **Error 404 post-mortem** is `[FULL]` game content: *(Full-game `[FULL]`; the MVP shows a plain fail → retry.)* — NOT required in the MVP.

## 5. Lens-guards (read before filing — prevents false positives)

- **LOCKED (do NOT flag as defects):** the capacity-cost routing model (A), the readability assist (B), the forecast-shift helper (C), the crisis engine (4.2) — all merged + settled; the W1 pin; the win/lose design per the GDD (the era-3 tuning risk is a DOCUMENTED assumption — playtest's call, not a defect).
- **Golden discipline:** new goldens blessed with proof (see the implementer's re-bless proof claims in _pr_body.md — Perkins has mechanically verified the .log.bin 8-byte-header claim and the .t1 catalog_hash-fold claim; see goldens-digest.md). Existing goldens MUST NOT shift without cause documentation (any undocumented shift = a finding). The HUD fix (#42) touched app/main.odin render — if its golden impact is visible here, verify it traces (cross-PR context, not a defect in THIS diff).
- **Scope guard:** 4.3 content ONLY (meter + win/lose/retry) — NOT 4.4+ content, NOT new player commands (LOG_VERSION stays 3 unless flagged — a bump without a flag = flag it).
- **BASE = v2** (full throttle + 4.1/4.2 + pin + HUD fix merged — carry-forward only). Em-dashes OK in PP.

## 6. Implementer's claims (from _pr_body.md — verify, don't trust)

1. Meter drains on sustained breach, never instant (E16) — windowed per-class SLA measurement; drain = `min(max severity over drained classes, per-tick cap)`; pinned by test_health_drain_max_not_sum_e16, test_health_drain_cap_e16, test_health_grace_lifecycle.
2. SLA hysteresis + re-breach no-op (E30) — enter strictly above tolerance, exit at tolerance − margin; one countdown per episode; gradual refill +5/tick after 50-tick healthy streak. Pinned: test_health_grace_rebreach_noop_e30 + test_health_grace_refill_gradual + test_health_windowed_breach_recovers.
3. Empty → Run_Lost; one terminal event per run (E17) — `run_lost` supersedes `grace_expired`; step barrier skips rest of tick. Pinned: test_health_empty_run_lost_e17.
4. Win at uptime ≥ 90% through the surge — accumulators freeze at deactivation tick; win fires at tick 3000 EXACTLY in health_win.dem (35453 delivered / 489 dropped = 98.6%). Pinned: test_health_surge_win_on_prepared_network (won_tick == 3000) + test_health_win_lose_same_tick_lose_wins.
5. Retry + no-soft-lock — test_health_restart_clean (meter 100, no leakage) + test_health_no_soft_lock_property (adversarial fixtures × seeds reach Run_Lost within a bounded horizon; a mid-grace fix recovers; a healthy run never goes terminal).
6. Goldens — health_win.dem + health_lose.dem (T1 + T2 of win and lose frames). Re-bless: ALL `.t1` (catalog_hash fold — balance.json `health` block + packet_types health fields); `.log.bin` diffs are EXACTLY the 8 catalog_hash header bytes (cmp-proven, same lengths); ZERO old T2 PNGs changed.
7. Launchable — health_win.dem / health_lose.dem play the full loop; the app session is the surge-survival loop (health on + win surge 90, era 3).
8. LOG_VERSION stays 3 (flagged) — no new commands; health section + tags 10–12 are append-only state/events.
9. Verification: `odin test core` 153 tests green; lint 6 gates green; harness 20/20 demos PASS; drift-check 139 mutations rejected; `odin build app` clean.

## 7. Harness/demo conventions (context for the goldens)

- T1 = per-tick FNV-1a-64 state-hash manifest (`goldens/<demo>.t1`); T2 = PNG frame captures (`goldens/<demo>/<ms>.png`); `.log.bin` = the serialized event/action log (8-byte catalog_hash header + events).
- The catalog_hash folds into every tick hash — a catalog data change (balance.json / packet_types.json) shifts ALL .t1 tick hashes mechanically.
- `health on` / `win surge <pct>` are demo setup commands (run setup flags, not player commands — LOG_VERSION unchanged).
- health_lose.dem: era-3 narrow topology → streaming breach at ~tick 5, grace 400 ticks, drain 2/tick → empty ~tick 452 → Run_Lost. health_win.dem: 16-router wide fan → surge passes → Run_Won at deactivation tick 3000.
