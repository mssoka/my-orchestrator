## 🤖 Perkins automated review — round 1 of 3

**Job:** packet-plumber-prototype-build · **Reviewed sha:** `4677f83` · **Reviewers:** 7/7 completed
**Verification:** 62/63 raw lens findings re-verified against the worktree at the reviewed sha — 1 discarded as false-positive; merged/deduped to **46 findings (3 blockers / 14 warnings / 29 notes)**. Every finding was confirmed by direct file reads; two were additionally reproduced headless (ghost-pipe demolish bug, ADR-11 replay divergence).

> **Note:** this PR was merged while the review was in flight (head sha unchanged — these are the exact merged bytes). The verdict stands as the correctness record; the findings feed the foundation-audit job. Full detail (evidence quotes per finding): `/Users/moses/code/_bmad-output/perkins/packet-plumber-prototype-build/r1/consolidated.json` + `diff.patch`.

### Blockers (3) — all verification gaps, no demonstrated gameplay defect

1. **NetworkHealth win/lose/drain has ZERO test coverage** — the loss meter (Error 404) and the surge win condition (FR12) are the fun-test gate's terminal states; no suite in `run_tests.gd` exercises drain/grace/recharge/win/lose. Perkins scratch-verified the behavior *works* headless (no-build → `lost` at tick 250; demo network → `won` at surge end, 92.7% uptime), but nothing in CI pins it. `game/scripts/core/network_health.gd` + `game/tests/run_tests.gd`
2. **QoS priority behavior untested at flow level** — the differentiator (FORGE #4): a prioritized pipe's promote/demote lane behavior, the E9 drop ladder, and E7 no-starvation have zero tests; `test_qos.gd` covers only the static WFQ partition helper. `game/scripts/core/packet_flow.gd:151-224` + `game/tests/core/test_qos.gd`
3. **Advisory test gate: FAIL** — P0 coverage <100% (the two gaps above) per the test-coverage gate thresholds.

### Warnings (14) — correctness/contract nits

- **Upgrade validation charges full new-tier cost; apply spends only the tier-delta** (topology_graph.gd:169,246) — affordable delta upgrades rejected unless the player holds full cost (architecture §6.7).
- **Upgrade validation skips the span ≤ tier.max_span check** that draw enforces (topology_graph.gd `_validate_upgrade`) — an over-span pipe is legal via upgrade.
- **Junction demolish with parallel pipes leaves a ghost pipe referencing the removed node** (topology_graph.gd `_apply_demolish`) — repro'd headless: 2 parallel pipes content↔router, demolish router → 1 ghost pipe survives. The cascade removes one pipe per neighbor.
- **balance.json `logic_hz=10` contradicts ADR-2's 20 Hz, the file's own comment, and CoreConst default** — surge runs ~2× the documented 90 s; demand.json's timing comments assume 20 Hz. (3 lenses agreed.)
- **RunState.bootstrap never passes balance to PacketFlow** — `ms_per_tick` stays 50 (should be 100 at 10 Hz): latency accrual 2× off; balance lane weights never consulted. `run_state.gd:bootstrap`
- **Determinism fingerprint omits in-flight packet state and latency** — `sla_summary` has no latency, `utilization_units` is always 0; AC-E10 replay-equality can pass while packet internals diverge. (architecture + blind agreed.)
- **Replay-equality keystone runs on a no-pipes topology** — commands/routing/traversal/QoS determinism never re-stepped. (3 lenses agreed.)
- **`submit_command` applies edits immediately vs SimDriver's tick-start batches — ADR-11 replay needs an undocumented +1 convention** — repro'd headless: naive replay diverges at the command's tick; the matching convention (log entry tagged T applied at start of T+1) reproduces byte-identically. Nowhere documented or tested.
- **AC-E21 slow-mo contract violated** — the accumulator cap *discards* backlog (skips ticks) and emits no "can't keep up" telemetry, contradicting the pinned contract and its own comment.
- **Onboarding-dismiss input is never consumed** — the same click starts a phantom drag (can draw an unintended pipe); SPACE dismiss unpauses then re-pauses. (blind + edge agreed.)
- **AC-E1 demolish-in-transit reroute/severance untested** (behavior scratch-verified working in the basic path).
- **SLA uptime aggregation (overall/recent/class) untested** — feeds the untested health breach input; E24 zero-demand neutrality unasserted.
- **`node_health_states` (🟡/🔴 warning surface) untested** — the never-phantom fairness guarantee unasserted.
- **RunController fixed-timestep accumulator (AC-E21 clamp/catch-up) untested.**

### Notes (29) — debt for the foundation-audit, none blocking the fun-test

Stubbed/deferred systems: CrisisEngine archetype firing (E4.1–E4.3 — surge IS live via scripted set-piece + forecast + node-health surface), AC-E22 pool-exhaustion drop (`IN_FLIGHT_CAP` unused), strain/critical lead-time tunables loaded but unapplied. Determinism hygiene: `span_between` float-sqrt letter deviation (mitigated, documented in-code), ADR-7 concrete-`ScriptedDirector` typing (spec-sanctioned by architecture §10.4), `_snapshot_now` passing the live rng on the display path (latent ADR-9). Single-source violations: QoS emphasis preset `Vector3i(4,1,1)` hardcoded, content-host throughput 40 in bootstrap vs 80 in catalog. Doc-vs-code: latency-tol drops claimed in `packet_flow.gd` header but never implemented (`latency_tol_ms`/`max_loss_pct` have zero consumers — latency data also 2× off per warning above), QUEUE_DROP_DEPTH "oldest drops" comment vs tail-drop behavior. Config: MCPRuntime autoload unconditional (unauthenticated TCP server on 7777 — dev convenience, exclude from release exports), `orientation=0` landscape pin missing from project.godot, `logic_hz` comment cascade (see warning). Latent core issues: budget-negative multi-cmd batches, batch-apply KeyError on conflicting commands, `clean_span` fallback ordering, E6 never-drop guard documented-not-implemented, surge-window accumulators never reset. Coverage nits: catalog error paths, `_pick_dst` dead param, dead code (`_draw_ellipse`, `play_w/play_h`, `queue_command`, orphan `main.tscn`), cosmetic draw-order (bundle capsule over priority marker), stale comments, demo-mode gaps (ignored `apply_edit` results, `--capture` without `--demo`).

### Reviewer agreement (multi-lens, highest confidence)

- `logic_hz` config contradiction — codebase + blind + architecture
- Onboarding input double-handling — blind + edge
- Replay keystone on no-pipes topology — tests + architecture + acceptance
- Fingerprint omits packet state — architecture + blind
- ScriptedDirector concrete coupling — architecture + blind
- `IN_FLIGHT_CAP` unused — blind + codebase + acceptance
- Missing landscape pin — architecture + edge

**Verdict:** NEEDS CHANGES

_The prototype's determinism spine is intact (pure RefCounted core, seeded single RNG, integer math — parse gate + 62/62 tests green, both verified by Perkins directly) and the fun-test loop demonstrably works: loss reachable, surge survivable, win achievable, command replay reproducible with the +1 convention. The 3 blockers are the missing regression suites for the win/lose meter and the QoS priority flow — the two behaviors the fun-test gate hinges on. Add those before treating the prototype as verified; warnings are correctness nits to fix or consciously defer; notes feed the foundation-audit._

_Full findings with verbatim evidence: `/Users/moses/code/_bmad-output/perkins/packet-plumber-prototype-build/r1/consolidated.json`_
