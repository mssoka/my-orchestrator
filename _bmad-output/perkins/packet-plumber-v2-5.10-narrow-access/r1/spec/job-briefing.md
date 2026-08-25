# Briefing — packet-plumber-v2-5.10-narrow-access (story 5.10 — narrow as residential access)

- **Job id:** `packet-plumber-v2-5.10-narrow-access`
- **Repo:** packet-plumber · **Base:** `v2` @ 1d7f442 (post-#62 head; Silas resolves
  the exact sha at dispatch) · **Slug:** `v2-5.10-narrow-access`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion
  you spawn launches with the same model — name it explicitly at every spawn.
- **Skills policy:** `gds-dev-story` (story execution) — the story card below IS the
  spec; `project-context.md` for code conduct. Your own adversarial pass uses
  `gds-code-review` layers (blind hunter + edge-case hunter).
- **Perkins:** `pr_review: 1` (catalog/balance canon surface). **Loop ruling (user,
  2026-08-17, "keep going"):** rounds run UNTIL APPROVED.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start;
  badge-out your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-v2-5.10-narrow-access <url>` yourself.
- **Story card:** `_bmad-output/planning-artifacts/sprints/stories-v2.md` §Story
  5.10 (relative to `/Users/moses/code/packet-plumber`). Read it + the design spec
  `_bmad-output/implementation-artifacts/spec-traffic-model.md` BEFORE designing.
- **Lane note (sibling in flight):** 7.1-visual-juice runs concurrently in the VIEW
  lane (k3, lavish-gated). Your files (catalogs + tests/goldens) are disjoint from
  its view code, but you BOTH carry golden re-blesses: yours is the slice
  boundary's deliberate T1/T2 re-bless (cause-documented, `cat.hash` fold proven);
  7.1's is the juice re-bless. First-lander documents the impact in the PR body
  for the other's rebase (the 4.3 discipline).
- **CI:** GitHub Actions is org-billing-blocked (+ today's GitHub incident — git
  ops fine); the LOCAL suite is ground truth. `tools/ci-local.sh` (9 gates) must
  pass; keep it green.

## Mission — implement story 5.10 (narrow as the residential access tier)

**The goal:** narrow's canon role is the **last-mile access drop**, sized so ONE
subscriber's traffic never congests it: narrow `capacity_units` 5 → **~8–10**
(proposed start; playtest-tunable, data-driven) with the routing-cost ladder (20)
UNTOUCHED — cost is moot on a single-path access link, and the 2026-08-13
capacity-cost ruling is unchanged between routers (flows still prefer fat pipes).
With 5.9's per-terminal caps landed (cap ≈ 2.5 u/s vs the node's own throughput),
this rebalance adds access-layer headroom ON TOP: ~2× headroom pre-5.10 → ~3–4×
post-5.10.

**Hard requirements (all pinned by the card):**

1. **The tier change, data-driven.** narrow `capacity_units` 5 → ~8–10 in
   `pipe_tiers` (catalogs `[ODN-5]`) — pick the value per the card's headroom
   math (cap ≈ 2.5 u/s → 3–4× headroom ⇒ 8–10; document the pick + the math in
   the PR). Playtest-tunable stays true: it is DATA, not code.
2. **Untouched:** the routing-cost ladder (20); span rules (`span_exceeds_tier`
   at edit — no contract change); every other tier; the 2026-08-13
   capacity-cost ruling.
3. **The honest signal.** After the change: a single residential on a narrow
   never drops its own traffic (5.9's cap + the new headroom); congestion
   appears only where flows AGGREGATE onto shared standard/wide links — so a
   congested narrow now genuinely signals an undersized access link (the honest
   4.1 reading). Pin it: extend 5.9's at-cap scenario to assert zero own-traffic
   drops WITH headroom, and an aggregation scenario where the shared link (not
   the access drop) congests.
4. **Replay + goldens.** Replay byte-identical `[E10]`; the tier change folds
   `cat.hash` → the slice's DELIBERATE T1/T2 re-bless per the 4.3 discipline
   (cause-documented in the PR; byte-proof of the fold-only diff where
   applicable).

**Acceptance:**

1. Card's Given/When/Then verified; the headroom numbers named (pre vs post).
2. Full local suite green (`tools/ci-local.sh` 9/9); determinism pinned.
3. PR body carries: the picked value + headroom math, the zero-own-drop and
   aggregation-choke pins, the re-bless cause chain, the "ladder/span/ruling
   untouched" statement, citations `[ODN-5]` `[E10]`.
4. Story card status line updated in the same PR (the established pattern).

**Scope guard:** the narrow capacity value ONLY. No cost/span/other-tier changes,
no new terminal types (5.11), no group bias (5.12), no UI. Balance beyond the one
value is out of scope.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-5.10-narrow-access
base: v2
model: deepseek/deepseek-v4-flash
pr_review: 1
```
