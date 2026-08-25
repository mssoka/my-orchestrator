### Story 5.12 — Aggregation groups (congestion lives at the shared uplink)

- **Slice:** 5B · **Epic(s):** E3.2, E4.2 · **Systems:** growth (5.1 group-bias draw), director
  `[ODN-7]` (group-scoped demand weight), crisis Surge (S4).
- **Goal.** The payoff: terminals cluster into groups (neighborhood analogues) whose flows share one
  player-built uplink — the honest choke. The demand director weights group-scoped demand; the ×10
  surge is an **aggregation event** at the group uplink. **Explicit conflict resolution:** the group
  bias is a **soft preference inside the E31 validity envelope** (bias draw first, E31 validity on
  the biased candidate, rejection-sampling unchanged); the uplink is never forced — the player wires
  it. E31 stays the hard contract.

**Given/When/Then:**
- **Given** a group-bias growth draw (spawn near an existing cluster member within a group radius;
  proposed 3–8 members, radius **~4–6 tiles** — Perkins r1 W5: the radius must exceed
  `GROWTH_MIN_SEP_TILES = 3` (`core/growth.odin:76`), the E31 packing floor — playtest-tunable) and
  a group-scoped demand weight;
- **When** aggregate demand from a cluster rises (base or the ×10 surge);
- **Then** the shared uplink — not any member terminal, not any access drop — is where congestion
  appears; every spawned terminal still satisfies E31 (connectable-within-span, min-separated,
  in-grid) and growth stays fully seed-derived (no log entries, derive-don't-record); the surge
  stresses the group uplink (the crisis engine's `preventive_redesign` — "add a parallel pipe or a
  higher tier on the spike's path" — now names the group uplink); replay is byte-identical `[E10]`;
  deliberate re-bless at the slice boundary.

- **Edge-case contracts:** `[E10]` replay, `[E31]` hard floor preserved (group bias never violates
  it), `[E9]`/`[E22]` unchanged. **Golden:** T1/T2 re-bless + a T2 frame of a clustered topology
  under surge (drops at the uplink).
- **Launchable increment:** run the app — a handful of homes share one uplink; the surge saturates
  the shared link, and the player's router/tier/bundle/QoS call on it decides who lives.

**→ Slice 5B exit:** the traffic model is honest — endpoints never self-congest (5.9), access is
real last-mile (5.10), terminals read as a spectrum (5.11), and congestion lives where it does in
real networks — at the shared uplink the player builds (5.12). The slice-6 era transition and the
slice-7 playtest gate exercise the honest aggregation model from the start. **(One deliberate,
cause-documented golden re-bless lands at this slice's boundary — the traffic-model change is
precisely the "legitimate re-bless" event the 4.3 discipline reserves for.)**
- **Status:** implemented 2026-08-18 — PR open (the estates ruling wired: `balance.json`
  `growth_groups` — bias_prob_permille 750 (the 0.7–0.8 majority-clustered, minority-isolated mix),
  3–8 members, radius 5 (> the E31 packing floor), member_weight_permille 250 — the group-bias
  growth draw (a SOFT PREFERENCE inside the E31 envelope: bias draw first, E31 on the biased
  candidate, rejection-sampling unchanged; the uplink is never forced) + the director's group-scoped
  demand weight (`[ODN-7]`: a source terminal in an estate picks at group_pick_scale/1000 of its
  demand_weight — aggregate group demand rises as members join) + the surge naming in `crises.json`
  (the preventive redesign now names the group uplink: "Add a parallel pipe or a higher tier on the
  group uplink's path."); the estates+isolated mix, the
  radius-connected compactness heuristic, the E31 floor, the surge-at-the-uplink aggregation, and
  the `[E10]` replay spine all pinned as durable tests; the slice's deliberate T1/T2 re-bless,
  fold-checked + byte-verified + cause-documented).

---

## Slice 6 — One era transition: Email → Streaming (modernization)

