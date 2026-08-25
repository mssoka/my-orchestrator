# Story 5.12 — Aggregation groups (congestion lives at the shared uplink)

The payoff of slice 5B: terminals cluster into groups (neighborhood analogues — **estates**, per the
user ruling 2026-08-17 night) whose flows share one player-built uplink — the honest choke. The
demand director weights group-scoped demand; the ×10 surge is an **aggregation event** at the group
uplink. And per the ruling: **NOT 100% clustered** — estates + the occasional isolated home.

## What shipped

- **The group-bias growth draw** (`core/growth.odin`, story 5.1's branch): each rejection-sampling
  attempt first draws a bias **coin**; a biased draw (coin < `bias_prob_permille` AND an eligible
  cluster exists — size < `max_members`) picks a cluster, a member anchor, a compass direction, and
  a distance in `[GROWTH_MIN_SEP_TILES, radius_tiles]` — the candidate lands within the group radius
  of a member and JOINS the estate in the derived view. Every other attempt is the pre-5.12
  outward-from-mesh draw — the **isolated home in the middle of nowhere**. Either family's candidate
  still faces the full **E31** test (`growth_pos_valid` + `growth_connectable`) — the bias is a
  soft preference inside the E31 validity envelope, never a bend; rejection-sampling is unchanged
  (a failed biased candidate is replaced by a fresh draw that can land outside the group). The
  uplink is never forced — the player wires it.
- **The derived estate view** (`group_cluster_view_build`): live terminals partitioned under radius
  adjacency (union-find, slot order). Pure function of (topology, catalog) — seed-derived, never
  serialized (the lane_caps precedent); replay recomputes it identically.
- **The group-scoped demand weight** (`core/flow.odin` §1b, director `[ODN-7]`): a source terminal
  that is a member of an estate (cluster size ≥ `min_members`) picks at
  `group_pick_scale/1000` of its demand_weight — `1000 + (size-1) × member_weight_permille`.
  Aggregate group demand rises as members join, and the ×10 surge lands concentrated on the
  estate's shared uplink. (Scale applied by **multiplication** — a `/1000` would truncate a
  weight-1 terminal and silently neutralize the concentration.)
- **The surge naming** (`data/crises.json`): the surge archetype's `preventive_redesign` now reads
  *"Add a parallel pipe or a higher tier on the group uplink's path."* — the crisis engine names the group uplink (display-only; no sim change).
- **The estates ruling, pinned as durable tests** (`core/growth_test.odin`, `core/demand_test.odin`,
  `core/crisis_test.odin` — 5 new tests):
  - estates form (≥ `min_members` members) AND isolated spawns appear on the **same seed** (the
    bias-prob minority) — `test_groups_estates_and_isolated` (seed 9, 28 growth windows);
  - the compactness heuristic (named): every estate member sits within `radius_tiles` of a sibling
    (radius-connected — the bird's-eye read of one neighborhood) — re-audited against raw positions;
  - every spawned terminal satisfies **E31** (the existing `e31_recheck` audit on the biased map);
  - the mechanism's pure pieces (view + pick-scale) — `test_groups_view_and_scale`;
  - the weight concentrates demand (estate share ≥ 750‰ with the shipped weight; the SAME seed with
    the weight zeroed sources strictly less) — `test_groups_demand_concentrates_on_estate`;
  - the **surge is an aggregation event at the shared uplink** — `test_groups_surge_aggregation_*`:
    a 3-campus estate on fat access drops shares one 4-wide uplink; base flows clean, the ×10 surge
    sheds at the uplink (never on the estate's own access drops), and the crisis names the uplink
    bundle; the card's T2 golden `demos/estate_surge.dem` renders it (banner + bottleneck outline);
  - the **E10 replay spine** with both the bias and the weight live — `test_groups_replay_byte_identical`.

## The deliberate re-bless (the slice's cause chain — 4.3 discipline)

The catalog fold (`balance.json` `growth_groups` block + `crises.json` copy — content AND comment
bytes fold the hash) + the growth/director behavioral shifts:

- **Fold chain:** `17d3baf8c6e1df7f` (pre-5.12) → `febe2afcc54f2d96` (5.12 data — final fold; the interim `5eeccdd63bfa9d0c` carried the draft banner copy, folded in the same PR).
- **Fold-only proof (boot):** `harness fold-check 17d3baf8c6e1df7f d1d2e53b7b1037ce` **PASS** — the
  era-0 tick-1 state dump under the final code, with the previous hash spliced at bytes 33..40,
  FNV-hashes to the previous golden tick-1 exactly (`d1d2e53b7b1037ce`); the un-spliced dump hashes
  to the blessed tick-1 (`d0fc99afd015e32c`). The era-0/no-demand shift is the fold alone.
- **Logs:** all 33 pre-existing `.log.bin` **byte-verified fold-only** — they differ from `v2` ONLY
  in the 8-byte catalog_hash header field (bytes 17–24); no command bytes moved (no new commands →
  no LOG_VERSION bump). The new `estate_surge.log.bin` joins the set.
- **T2 partition:** pixels moved **only** where cause-documented — (a) the six 65000/80000ms frames
  of the era-3 demos whose crisis banner is up at the capture (warn/juice/pause/qos/surge: the
  **surge-naming copy** — 899 px in the banner strip only, the map byte-identical); (b) the
  growth-enabled demos (growth, node_health, terminal_types: the **group-bias placements** + the
  era-3 demand, map-region shifts); (c) the new `estate_surge` frames. Every other demo's T2 frames
  are byte-identical (the fold does not shift pixels).
- Input-parity manifests re-saved (the same fold).

## Verification

- `tools/ci-local.sh --mac`: **10/10 gates green** (lint, **199 core tests** incl. the 5 new group
  pins, app build, golden harness ×34 demos + replay gate, palcheck, W1 drift-rejection 240/240,
  assist preview cross-check, PP_DEBUG builds, stats replay-identity, input parity 24/24).
- Replay is byte-identical `[E10]` — the harness replay gate re-sims every blessed log (34 demos) +
  the group-bias replay-identity test (`test_groups_replay_byte_identical`).
- Every spawned terminal satisfies `[E31]` — `test_groups_estates_and_isolated` audits the biased
  map (bounds + min-separation + connectable-within-span).
- The aggregation event is pinned mechanically: the estate_surge scenario fires the crisis at tick
  1202 with root cause = the shared uplink bundle (pipe 9), 2695 drops at the uplink, zero on the
  estate's own access drops.
- Story card status line updated in `stories-v2.md` (the established pattern).

## Decisions & rationale

- **All group tuning is DATA** (`balance.json` `growth_groups`), never code constants — per the
  ruling ("Propose `group_bias_prob ≈ 0.7–0.8` in `balance.json` (playtest-tunable data, NOT a code
  constant)"): `bias_prob_permille` 750 (the 0.7–0.8 majority), `min_members` 3, `max_members` 8,
  `radius_tiles` 5 (MUST exceed `GROWTH_MIN_SEP_TILES = 3`, the E31 packing floor — Perkins r1 W5),
  `member_weight_permille` 250. Fail-fast validated at load like every sibling block (a missing key
  is a load error; bias must be 1..999 — a 0 disables estates, a 1000 breaks the "NOT 100% of the
  time" mix).
- **The bias draw counts are pure functions of deterministic state** (eligible-cluster count +
  cluster sizes + nj + span — all topology/catalog derived): the coin is always drawn, family
  sub-draws skip when degenerate (rng_range draws nothing when hi ≤ lo), so replay is byte-identical
  [E10]. The deliberate re-bless covers the shifted growth/demand rng interleaving.
- **The derived cluster size may exceed `max_members`** when two estates grow near each other and
  bridge (a candidate within radius of both) — the growth CAP applies to the draws (an estate at
  the cap stops extending; new growth starts a fresh estate via the uniform family), never to the
  emergent derived view (real neighborhoods merge too). Documented in the test comment.
- **The weight is structurally neutralized under credit-starvation** (the 5.9 cap regime: every
  terminal is picked at exactly its credit rate, so no weight can move the shares) and bites in the
  credit-rich regime (the grown map's aggregate credit > the ask) — the concentration test uses a
  credit-rich host fixture deliberately, and the shipped value (250 permille/member) is the honest
  estate-differentiation knob.
- **Sink-side concentration is untouched** (W6 scope): deliveries concentrate by the weighted-random
  dst distribution + E9 at the access lane; the estate fixture's sinks are spread thin so the
  aggregation shed stays at the uplink.
- **Scope guard honored:** aggregation groups ONLY — no terrain-aware placement (follow-up), no new
  terminal types (5.11), no QoS/balance changes beyond the group data, no UI beyond the crisis
  naming. E31 is never bent.

## Citations

`[ODN-7]` (director group-scoped demand weight) · `[E10]` (replay byte-identity) · `[E31]` (spawn
validity hard floor preserved) · the **estates ruling** (user 2026-08-17 night: "homes grouped
together in estates ... clusters of end points, but NOT 100% of the time") — bias_prob_permille ≈
0.7–0.8, estates + isolated spawns asserted on the same seed.

