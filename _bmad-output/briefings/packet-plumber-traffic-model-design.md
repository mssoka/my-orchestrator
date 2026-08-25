# Briefing — packet-plumber-traffic-model-design (canon: the Section B design thread becomes story cards)

- **Job id:** `packet-plumber-traffic-model-design`
- **Repo:** packet-plumber · **Base:** `v2` @ latest · **Slug:** `pp-traffic-model-design`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Mega-minions same —
  name explicitly at every spawn.
- **Skills policy:** `gds-agent-game-designer` (story-card + canon authorship) +
  `lavish` (the user reviews the design in-browser BEFORE the PR — docs loop).
- **Perkins:** `pr_review: 1` (canon-surface PR).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out
  your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-traffic-model-design <url>` yourself.
- **Source material (the thread is already decision-ready — read first):**
  `_bmad-output/implementation-artifacts/surge-explainer/surge-explainer.html`
  §Section B design notes + the real-world-scale math (1G/40G/100G → u/tick).
- **Coordination:** the terminology audit (p1P8) may amend GDD wording and its
  phase-2 rename PR serializes behind 5.2's merge — your GDD edits must be
  SECTION-additive (mechanics/decision-log entries), not terminology rewrites, so
  the diffs don't collide. Silas serializes the PRs.

## Mission — turn the explainer's Section B design thread into canon + story cards

**User ruling (2026-08-15):** the Section B design notes are TASKS to be done:
the traffic model gains realism so congestion lives where it does in real networks.

**The four design threads (from the explainer, user-endorsed):**

1. **Narrow as residential access** — narrow pipes are the access tier (the
   last-mile); congestion is an AGGREGATION event (at routers/cores), endpoints
   never self-congest.
2. **Per-terminal demand caps** — terminals emit bounded, realistic demand; no
   single endpoint saturates a network alone.
3. **Aggregation groups** — the demand director spawns/weights terminals in
   clusters so surge stress lands on aggregation points (where the player's
   router/tier/bundle decisions matter).
4. **Diverse terminal types** — terminal variety (residential/small-biz/campus
   class analogues) with different demand profiles per type.

**Deliverables:**

1. **Design spec (lavish-reviewed):** for each thread — the mechanic in Given/When/
   Then shape, the real-world rationale (cite the explainer's 1G/40G/100G math),
   the balance levers (catalog/balance.json placement — data-driven per canon),
   determinism constraints (all seed-derived; no wall-clock; replay byte-identical
   or deliberate LOG_VERSION), and interaction with existing canon (E22 pool, E9
   bounds, 4.1 strain, 5.1 growth spawning, 5.8 QoS). Resolve conflicts EXPLICITLY
   (e.g. growth-spawn validity vs aggregation groups).
2. **Story cards** appended to stories-v2 (the existing card format): where they
   slot in the slice line (post-5.4? fold into slice 6?) — propose the sequencing
   with rationale.
3. **GDD decision-log amendment**: the traffic-realism ruling + the four mechanics,
   section-additive.
4. The lavish artifact presents ALL of it for the user's verdict; the PR opens only
   after approval.

**Scope guard:** design docs + story cards ONLY. No code, no balance.json changes,
no implementation — those are the story cards' jobs.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: pp-traffic-model-design
base: v2
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1
```
