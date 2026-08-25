## M5 Crisis model
#### M5 — Crisis model: fair and predictable (P3) `[FORGE #3]`

Crises are the **consequence** of a topology flaw the player should have designed around — never random. Every crisis is foreshadowed by readable warning signs with a lead time, and every crisis has a topology-flaw root cause the player could have prevented.

**Warning-sign system (the fairness contract):**

| Indicator | Meaning | Lead time to failure |
|---|---|---|
| Node 🟡 strained | Approaching capacity | ~30 s `[ASSUMPTION: prototype tuning]` |
| Node 🔴 critical | Imminent overload/fire | ~10 s |
| Pipe pressure climbing | Saturation incoming | ~20 s |
| Demand forecast ("weather report") | A surge/failure is N seconds out | 15–60 s |
| Legacy pipe wear indicator | Degradation incoming | long (era-scale) |

**Five crisis archetypes** (each a design consequence, each preventable):

| Archetype | Root cause (preventable) | Warning | Failure |
|---|---|---|---|
| **Saturation** | Built too little capacity / no bundled redundancy for demand | Pressure climbing, nodes 🟡 | Mass packet drops; SLA collapse |
| **Single-point-of-failure** | One junction carries critical load with no alternate route around it | Junction 🔴 | Junction overload/fire → all routes through it fail |
| **Degradation** | Left legacy pipes in service under new-era load | Wear indicator, falling throughput | Pipe burst / throughput collapse |
| **Surge** *(MVP)* | No spare capacity / redundancy for a forecast demand spike | Demand forecast (viral event, 10× spike) | Cascade saturation across the map |
| **Severance** | A whole link-bundle lost (no alternate route) | Link marked vulnerable / timed event | Cut one pipe of a bundle → pool capacity shrinks (graceful); only **full-bundle-loss** drops the route |

**Fairness rules (pinned as test contracts):**

1. Every crisis has a warning sign with lead time ≥ the player's reaction window.
2. Every crisis has at least one topology redesign that would have prevented it.
3. No crisis is RNG-spawned onto a healthy topology — a crisis always traces to a measurable strain that was visible.
4. The player can always recover (no soft-locks) — reroute, upgrade, or reprioritize out.

The V2 **AI stress-test system** (deferred — full-game replayability, forge weak point #4) is an *auditor* that analyzes the player's topology, finds the exploitable weakness, and pressures *that* — fairly, because it attacks a real flaw, never a random one.

**Demand director — bespoke per-era crisis rhythm (P3, *user-ratified addition, lavish review 2026-08-10*).** Crisis pacing is **hand-tuned per era**, not a flat difficulty curve: a demand director scripts each era's surges to an authored rhythm — a tension peak climbing through staged thresholds (the Hades 2 wave-gate principle: 50 / 70 / 90%), broken by an *earned* breath where gauges recover and the player banks the era's reward. The rhythm kills dead time (a lull is always about to break) and makes the breath *relieving* rather than empty. Each era's signature demand (M4) gets its own cadence — the streaming surge is a single 10× wall, the real-time era is rapid multi-class triage, the cloud era is long sustained pressure. This is the *pacing* layer of the crisis model: crises stay *fair* (every spike forecast, every flaw preventable, per the fairness rules) while their *timing* is authored for feel. `[ASSUMPTION: prototype tuning — per-era threshold curves and breath windows are authored at balance time.]` *(Full-game `[FULL]`; the MVP ships one fixed surge set-piece.)*
