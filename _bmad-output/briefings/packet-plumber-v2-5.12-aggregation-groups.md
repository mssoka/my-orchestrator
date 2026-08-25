# Briefing — packet-plumber-v2-5.12-aggregation-groups (story 5.12 + the estates ruling)

- **Job id:** `packet-plumber-v2-5.12-aggregation-groups`
- **Repo:** packet-plumber · **Base:** `v2` @ post-5.11-types merge head (HELD —
  Silas resolves the exact sha at release; see the hold note below) ·
  **Slug:** `v2-5.12-aggregation-groups`
- **HOLD (Silas):** do NOT dispatch on receipt. Release trigger = the
  `packet-plumber-v2-5.11-terminal-types` merge close-out (5B sequence:
  5.11 → 5.12). Record the hold on the row.
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any
  mega-minion you spawn launches with the same model — name it explicitly at
  every spawn.
- **Skills policy:** `gds-dev-story` (story execution) — the story card below IS
  the spec; `project-context.md` for code conduct. Your own adversarial pass
  uses `gds-code-review` layers (blind hunter + edge-case hunter).
- **Perkins:** `pr_review: 1` (growth + director + surge — canon surface).
  **Loop ruling (user, 2026-08-17):** rounds run UNTIL APPROVED.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start;
  badge-out your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-v2-5.12-aggregation-groups <url>` yourself.
- **Story card:** `_bmad-output/planning-artifacts/sprints/stories-v2.md` §Story
  5.12 (relative to `/Users/moses/code/packet-plumber`). Read it + the design
  spec `_bmad-output/implementation-artifacts/spec-traffic-model.md` BEFORE
  designing.
- **USER RULING (2026-08-17 night) — the ESTATES pattern, canon for this
  card:** "we usually have homes grouped together in say estates, with the
  occasional residentials in the middle of nowhere isolated... having clusters
  of end points, but NOT 100% of the time. Nodes should be placed to also aid
  good-looking topologies in a bird's-eye view." Translation: the group bias is
  PROBABILISTIC — a majority of growth draws bias toward existing clusters
  (estates), a minority stay uniform (isolated homes in the middle of
  nowhere). Propose `group_bias_prob ≈ 0.7–0.8` in `balance.json`
  (playtest-tunable data, NOT a code constant); assert BOTH patterns in
  tests: multi-member estates AND isolated spawns on the same seed. Placement
  aesthetics: within the E31 envelope, prefer compact, legible cluster shapes
  (the bird's-eye read) — name the heuristic, keep it seed-derived.
- **CI:** billing-blocked GH Actions — the LOCAL suite is ground truth;
  `tools/ci-local.sh` (10 gates) must pass.

## Mission — implement story 5.12 (aggregation groups: congestion lives at the shared uplink)

**The goal:** the payoff of 5B — terminals cluster into groups (neighborhood
analogues, estates per the ruling) whose flows share one player-built uplink:
the honest choke. The demand director weights group-scoped demand; the ×10
surge is an aggregation event at the group uplink. And per the ruling: NOT
100% clustered — estates + the occasional isolated home.

**Hard requirements (all pinned by the card + the ruling):**

1. **Group-bias growth draw** (soft preference INSIDE the E31 validity
   envelope — bias draw first, E31 validity on the biased candidate,
   rejection-sampling unchanged; the uplink is never forced — the player wires
   it; E31 stays the hard contract). Group size 3–8 members, radius ~4–6 tiles
   (MUST exceed `GROWTH_MIN_SEP_TILES = 3`, the E31 packing floor);
   `group_bias_prob` per the ruling (data-driven).
2. **Group-scoped demand weight** (director `[ODN-7]`): aggregate group demand
   rises as members join; the ×10 surge stresses the GROUP UPLINK — the crisis
   engine's `preventive_redesign` names the group uplink ("add a parallel pipe
   or a higher tier on the spike's path").
3. **Determinism.** Growth stays fully seed-derived (no log entries,
   derive-don't-record); replay byte-identical `[E10]`; deliberate re-bless at
   the slice boundary (cause-documented).
4. **The estates pattern pinned.** Tests assert: (a) estates form (multi-member
   groups, compact); (b) isolated terminals still appear on the same seed (the
   bias-prob minority); (c) every spawned terminal satisfies E31
   (connectable-within-span, min-separated, in-grid).
5. **Slice-5B exit note:** this card closes 5B — update the slice exit line if
   the story-card fold requires it (the established pattern).

**Acceptance:**

1. Card's Given/When/Then verified; the ruling's estates+isolated mix pinned;
   the surge reads as an aggregation event at the shared uplink.
2. Full local suite green (`tools/ci-local.sh` 10/10); determinism pinned.
3. PR body: the bias mechanics (prob, radius, sizes — all data-driven), the
   group-demand weighting, the surge-naming change, the re-bless cause chain,
   citations `[ODN-7]` `[E10]` `[E31]` + the ruling (estates, not 100%).
4. Story card status line updated in the same PR (the established pattern).

**Scope guard:** aggregation groups ONLY. No terrain-aware placement (follow-up),
 no new terminal types (5.11), no QoS/balance changes beyond the group data, no
 UI beyond the crisis naming. E31 is never bent.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-5.12-aggregation-groups
base: v2
model: deepseek/deepseek-v4-flash
pr_review: 1
```
