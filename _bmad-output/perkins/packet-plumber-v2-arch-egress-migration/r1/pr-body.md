## Summary

THE egress QoS model migration — implemented against the ratified spine `architecture-egress-qos-2026-08-26` (AD-1..AD-8; user rulings R1–R4 adopted 4/4). Store-and-forward egress QoS: routers buffer + schedule per `(egress-port, lane)`; links transmit only; endpoints pace. Physical encoding stays derived — no new Packet fields, no queue structs serialized. Five stories, one commit each, suite green between every story; review swarm folded at head (`1e9c783`).

## Story ladder

- **S1 `b2c84aa` — port identity re-key (AD-2/D2, semantics-preserving):** logical queue key = `(router, egress-port, lane)` where egress-port = the directional bundle; direction derived from the retained departure node (`at_node` — canonical; heading derivation coincides, pinned). Directional read twins (`port_lane_count / newest_in_port_lane / port_lane_ready / port_lane_caps`, R2 member-summed caps). All mechanics still read the undirected view — the re-key is invisible until S2/S4. **T1: 49/49 demos byte-identical, ZERO re-bless.**
- **S2 `147f056` — full-duplex direction split (AD-5, ruling R1):** each direction gets its OWN `bundle_cap` serve budget + own tx-utilization ring (a 1 Gbps link is 1 Gbps each way; the pooled 2.1 doctrine is amended). Reverse streams no longer compete for forward budget; same-direction estate contention survives. Stats: `util_pct` = MAX over directions (AV-4), `tx_octets` = Sum. Enumeration order pinned (AV-3).
- **S3 `bad1ceb` — D-2 wired (the user-routed named story):** `bandwidth_demand` (loaded since 3.1, never consumed) now rides the AD-3(c) serialization term: `ceil(demand × 800 / line_rate)`; per-packet need = its own demand total (streaming jumbo 1600); `packet_progress_frac` + `transit_ticks` demand-aware. Count-based health/warnings/stats measures stay packet-count-based by design. Demand load-bounded 1..4096 (u32-wrap class, hunter fold).
- **S4 `6254fb5` — drop/crisis re-key to the port (AD-4/R4):** E9 admission bound + shed ladder per `(port, lane)` bound 6; `Packet_Dropped.target` STAYS the bundle id (AV-1 — never re-keyed); port direction rides the existing tag-conditional `Event.direction` slot (AV-2, no new struct field); crisis measures port-keyed, `root_cause` names (router, port); F1 cooldown key gains direction; the 4.2 crisis hysteresis (`CRISIS_RESOLVE_MARGIN`) survives VERBATIM — margin tests pass unchanged.
- **S5 `4ee2d2b` — latency ledger + reads contract (D3/F2 + AV-5 + AD-7/F3):** per-`(port, lane, class)` residency rings (tx-ring pattern; layout resets on topology gen); F2 term split exact — joiners (a) + unserviced (b) + serviced (c), pinned (b)=7; reads: `router_buffering_packets`, `port_util_pct`, `port_residency_ticks` (the render heists' input contract — consumers are the link-vocab heists, test-pinned here). Stats v3 Q-rows per (router, port); NOC QUEUE DEPTH section re-keys to `R<router>><peer>`; QoS panel depth readout per-direction. Zero golden drift at this story.

## Balance disclosures

- **S2 (full duplex):** bidirectional-shared pairs gain **2× effective serve capacity** — each direction now drains at the full `bundle_cap`. The E9 lane bound was still pooled at this story (deliberate — S4 re-keys it per R4).
- **S3 (D-2 demand wiring):** streaming transit **8 → 16 ticks** at the standard tier (`ceil(1600/100)`); **32 ticks** on era-3-decayed legacy standard (1600/50); 1 tick on mid/wide (unchanged). Streaming SLA math shifts everywhere standard-path streaming contends — 2-hop shorts now 1650 ms > the 1200 ms tolerance (SLA fixtures re-staged on a 1-hop recovery path). Fat-pipe streaming demos are byte-identical (1-tick transit under any demand).
- **S4 (bound re-scope, F4 accepted with R4):** per-pair buffer capacity doubles — **6 → 12 packets per lane per pair**. Runs whose contention lived in the pooled bound shed later or not at all (w11 aggregation re-staged W 600→1200 + host 200 to restore the choke premise).

## T1 re-bless inventory

| Story | Demos re-blessed | Cause |
|---|---|---|
| S1 | **0** | the re-key is invisible by construction (strongest S1 pin) |
| S2 | 16 | contention only: first tick a bundle carries both directions' packets shifts serve interleaving; unidirectional runs byte-identical by construction (33/49 untouched) |
| S3 | 24 | every run where standard-path streaming contends (+1 direction payload byte in S4's fold is separate); fat-pipe streaming demos byte-identical |
| S4 | 23 | every drop/crisis-emitting run (the +1 direction payload byte shifts the T1 event-stream fold) + bound re-scope behavioral shifts |
| S5 | 0 | reads-only + derived state; zero golden drift |

T2 re-blesses: S2 19 pngs, S3 43, S4 6 — the shifted runs' captures only.

## D6 save/replay proof

**LOG_VERSION stays 6.** Every `.log.bin` is byte-identical to origin/v2 across the branch (the action log is commands; replay re-sims the same command stream). The serialized crises section is byte-pinned unchanged (31 bytes). Replay gate: 49/49 demos bit-for-bit, `stats-check` live==replay byte-identical including spawn_feel. Zero golden drift outside the disclosed re-bless inventory.

## Testing (the house bar)

Full suites green at every story gate and at head: `odin test core` 276 (incl. crisis + qos), `odin test app` 48, `odin test app/render` 100, palcheck, lint 8/8 (new gate 8: no link-queue vocabulary on render paths — AD-1's negative space), drift-check 353/353 rejected, 49 demos green ×3. **Mutation leg RED-then-GREEN per story**: S1 direction-filter bypass fails the directional-split pin; S2 shared-budget collapse fails full-duplex independence (6/12 arrived — the pooled math exactly); S3 demand unwired fails the streaming-transit pin (arrives 9, not 17) + 5 staged fixtures; S4 bound pooling fails the R4 admit pin; S5 record-pass deletion fails the (b)=7 pin.

## Review swarm (folded at `1e9c783`)

2 hunters (adversarial-general + edge-case-hunter): F5 lint gate LANDED; residency staleness folds at READ time (idle keys read 0); ledger layout resets on Topology.gen (same-count renumber leak — hunter-probed at 120 phantom ticks pre-fix); `bandwidth_demand` load bound 1..4096; dead code out (`noc_pipe_rate_compact`, `bundle_class_queue`); shadow_clone incident (S5 arrays initially missing from the spawn-feel prediction shadow — cloned like every step()-touched dynamic, pattern-documented in-repo); 3 blockers verified false/by-design and logged (incl. the moving-base "deletes the spine" artifact — merge-base diff has zero deletions). Drive-by: pre-existing v2 lint red (em-dash in a palette test string) ASCII'd, disclosed.

## CI disclosure

Remote CI is billing-blocked (standing ruling: **local suite is ground truth** — disclosed once here). All gates above ran locally.

