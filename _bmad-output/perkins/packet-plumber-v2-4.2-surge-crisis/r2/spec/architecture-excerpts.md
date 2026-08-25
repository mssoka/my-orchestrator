## [ODN-4]
#### ODN-4 — Crisis Engine: root-cause-driven (carried, Surge only for PROTO)

Unchanged design `[FORGE #3]`: strain metrics from Topology + Flow each tick →
warning signs (🟡/🔴, pressure, forecast, wear) → crisis fires only on
measurable visible strain; every archetype carries a structured `root_cause`
+ a preventive redesign; the 4 fairness rules are executable test contracts
(§11.3). **PROTO ships the Surge archetype only**; the archetype table is
data (`crises.json`), so the remaining four are content + evaluation procs,
not re-architecture. The Director owns the demand timeline **upstream** of the
flow; the Crisis Engine evaluates **downstream**; the Director must never read
crisis state to force a crisis (`[REVIEW M1]` carried as an explicit rule).

## [ODN-7]
#### ODN-7 — CrisisDirector seam as a proc field (carried, de-boilerplated)

All crisis *pressure* (demand timeline + surge scheduling + map growth) flows
through one proc pointer on the run config:

```odin
Run_Config :: struct {
    seed:          u64,
    modifiers:     []Modifier_Id,          // daily/weekly twists; [] for standard
    plan_pressure: proc(topology: Topology_Snapshot, era: Era_State,
                        tick: u64, rng: ^Rng) -> Pressure_Plan,
    // ^ read-only view in, plan out; pure w.r.t. sim state — the M1 rule
    // ("the Director must never read crisis state") is structural, not discipline.
    leaderboard:   Leaderboard_Service,    // ODN-6
}
```

PROTO binds `scripted_plan_pressure` (data-driven demand timeline — for PROTO
the surge curve lives in `crises.json` + `balance.json`; `eras.json` takes
over when the Era layer lands — seeded). V2 binds the AI auditor `[FORGE weak #4]`
behind the same field. GL5.2 needed an abstract-base-class convention +
`assert(false, "override me")` to fake this (`[REVIEW M4]`); Odin's proc
pointers make it one line, type-checked, zero ceremony. (GL5.2's own m12
observation — the seam earns its place in the architecture while the prototype
impl stays trivial — carries over exactly.)

#### ODN-8 — Packet storage: SOA pools, no view-side objects


## [S6.4 Crisis Engine]
### 6.4 S4 — Crisis Engine **[PROTO: Surge only]**

- **Responsibility.** `[GDD § M5]`: strain metrics from Topology + Flow →
  warning signs (node 🟡/🔴, pipe pressure, forecast, wear) → archetypes.
  PROTO ships **Surge** (forecast demand spike, cascade saturation if
  unprepared); Saturation/SPOF/Degradation/Severance are [LATER] content +
  evaluation procs on the same frame.
- **Boundary.** **Downstream of flow** — reads Topology + Flow state, emits
  `Warning_Sign` + `Crisis_Event`. Never owns the demand timeline (that's the
  Director, upstream — ODN-7); a crisis is a consequence, never its own cause
  (`[REVIEW M1]` rule carried — and here it is *structural*: the ODN-7
  signature hands the Director a read-only view, not `^Run_State`). Does not resolve crises (the player does).
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


## [S11.3 fairness]
### 11.3 Novel pattern: fair-crisis root-cause contract (carried as executable tests)

Every `Crisis_Event` carries `root_cause` (structured ref to the topology
flaw) + `preventive_redesign`. The `@(test)` suite pins: no crisis without a
root cause; every root cause has a preventing edit; no crisis fires on a
healthy within-capacity topology; warnings always precede failures by ≥ the
reaction window `[FORGE #3]`.

### 11.4 Novel pattern: action-log replay = save = validation = demo (evolved)


## [E10/E13 rows]
| E8 | Largest-remainder integer distribution | E→S→B tie order, pinned test |
| E9 | Drop ladder BE → Standard → Express | full ladder, every emptiness combo |
| E10 | Iteration/tie-break determinism | arrays-only + seeded rng + replay test (ODN-10) |
| E11 | Monotonic ids, never recycled | `{slot, gen}` ids (ODN-8) |
| E12 | Timers pure functions of (seed, log) | load→re-step→assert-match test |
| E13 | One crisis per root-cause per tick | dedup by cause ref |
| E14 | Era advance preserves active crises; no mid-crisis demand spawn | [LATER] layer contract, decided now |
