## E2 — Flow Simulation, Packet Types & QoS

**Delivers** the living network: PP-E1's flow simulation (deterministic, tick-driven) + PP-E2's packet types and QoS in full. *Playable value: packets stream across the little world; routing has trade-offs.*

- **E2.1** Flow simulation *(from PP-E1)* — deterministic tick-driven sim core (owned RNG, fixed tick); junctions forward per-packet (ECMP hash across equal-cost paths); parallel pipes bundle into pooled capacity; path cost = static pipe-tier cost ("fattest route; equal cost splits by hash"). *(PP-Odin 2026-08-10/13 rulings, inherited.)*
- **E2.2** Packet-class definition — MVP: email (low/low/low) + streaming (med/med/high). `[FORGE #4]`
- **E2.3** Link-level class queues — 3 lanes per pipe (Express/Standard/Best-effort); all traffic starts Standard at 100%; assignment ladder (100 · 70/30 · 50/30/20) data-driven; per-pipe overrides; QoS panel on pipe select. **Nothing auto-allocates.** *(Inherited.)*
- **E2.4** Serialization at nodes — Express → Standard → Best-effort egress, work-conserving gap-filling; visible in 3D (strand-speed + node egress). *(Inherited.)*
- **E2.5** Per-class SLA tracking — latency/loss accumulate per class; thresholds from Numerical Design.
- **Test contracts:** replay byte-identity on a fixed seed (determinism contract); contention drops by drop precedence (lowest first); a dedicated lane reservation holds its class's capacity; SLA breach is detectable and attributable; view-layer changes never shift sim state.

## E3 — Topology & Nodes
