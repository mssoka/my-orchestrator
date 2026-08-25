## r1 guards (round-specific — fresh PR, the aggregation-groups canon)

**The ONE hard blocker class — the estates ruling is honored WITHOUT
breaking the determinism spine:**

- **The estates ruling (user 2026-08-17 night — canon):** terminals
  cluster into estates — majority clustered, minority isolated, NOT 100%.
  The bias is a SOFT preference: `bias_prob_permille 750` in
  balance.json (data-driven, fail-fast validated at load), a bias coin per
  rejection-sampling attempt, and the biased candidate still faces the
  FULL E31 test; rejection-sampling unchanged; the uplink is never forced.
  VERIFY: (a) the bias is genuinely inside the E31 envelope (a biased
  draw can fail E31 and fall back); (b) it is NOT a hard 100% cluster
  (the ruling's "NOT 100%" is load-bearing — check the measured majority
  vs the isolated minority on the pinned seed); (c) the draw counts are
  pure functions of state — replay byte-identical [E10].
- **The derived estate view is PURE and NEVER serialized:** union-find
  under radius adjacency, seed-derived, no LOG_VERSION bump. Verify the
  view isn't persisted and doesn't touch the serialization/replay path
  (the 5.4/5.8 derive-don't-record discipline).
- **Group-scoped demand weight [ODN-7]:** an estate member's source-pick
  weight scales as `1000 + (size-1) * member_weight_permille` (250) —
  aggregate group demand rises as members join. Verify the math + the
  concentration pin (estate >= 750 per-mille vs the no-bonus control —
  non-vacuous; the r3/N5 lesson: a literal that silently stops biting on
  re-tune is a defect).
- **The surge is an aggregation event at the group uplink:** crisis
  naming updated ("Add a parallel pipe or a higher tier on the group
  uplink's path"), the shed happens at the shared uplink — never on the
  estate's own access. Verify the crisis test pins the uplink bundle.
- **The deliberate re-bless is cause-partitioned:** fold-check PASS
  (17d3baf8 → febe2afc, era-0 tick-1 shift = the catalog fold alone), all
  33 pre-existing .log.bin fold-only (bytes 17–24), T2 shifts partitioned
  (6 banner-copy + 7 growth-map frames + 1 new estate_surge.dem;
  everything else byte-identical). Verify the partition mechanically
  (byte-compare the .log.bin set vs v2; PNG diff on the non-partition
  frames) and that the new T2 golden was vision-verified (estate cluster
  + red-outlined uplink + banner naming the group uplink — the 7.1
  golden discipline).
- **The adversarial catches landed:** the Odin block-scoped defer
  use-after-free on the view and the /1000 truncation that silently
  neutralized the weight for weight-1 terminals — verify BOTH fixes are
  in the tree (the use-after-free class is the r3 double-free's sibling:
  check it isn't masked by the tracking allocator).
- **5 new pins non-vacuous:** estates + isolated spawns on seed 9
  (radius-connected compactness + E31 audit) · pure view/scale units ·
  weight concentration · surge sheds at the shared uplink · E10 replay
  spine with both live. Mutation-check at least the weight and the
  surge-shed pins.

**What NOT to re-litigate:** the 5.11 roster + era gates + W9 honest pin
(4-round approved); the #65 sprite canon (lavish-APPROVED); the 5.9/5.10
accumulator contracts; the fair-crisis grown-mesh start map; the estates
ruling itself (a user decision — the question is whether the CODE honors
it, not whether it's right); the fold-check harness (N11 of 5.11 — done);
the fallback-model caveat.

**Verdict severity:** cap lifted — if the bias is soft + E31-respecting,
the view is pure, the weight math + pins bite, the surge names the
uplink, and the re-bless partition is exact, APPROVE. Warnings ≠
blockers.

**CI note:** GitHub Actions on Packet-Plumber is org-billing-blocked
(runners never start — the retired-caveat class) — NOT a signal; the
local suite is ground truth (minion reports 10/10 gates, 199 tests,
34-demo harness + replay, drift 240/240, input parity 24/24).
