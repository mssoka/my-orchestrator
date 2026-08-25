# Briefing — packet-plumber-v2-5.2-node-health (story 5.2 — node health states)

- **Job id:** `packet-plumber-v2-5.2-node-health`
- **Repo:** packet-plumber · **Base:** `v2` @ post-#51 merge head (Silas resolves the
  exact sha at dispatch) · **Slug:** `v2-5.2-node-health`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model — name it explicitly at every spawn.
- **Skills policy:** `gds-dev-story` (story execution) — the story card below IS the
  spec; `project-context.md` for code conduct. Your own adversarial pass uses
  `gds-code-review` layers (blind hunter + edge-case hunter).
- **Perkins:** `pr_review: 1` (gameplay + canon surface).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out
  your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-v2-5.2-node-health <url>` yourself.
- **Story card:** `_bmad-output/planning-artifacts/sprints/stories-v2.md` §Story 5.2.
  Read it + sprint-plan-v2 §5.2 row BEFORE designing.
- **CI:** green. Full local suite must pass.

## Mission — implement story 5.2 (nodes telegraph their trouble)

**The goal:** per-node health states 🟢 healthy → 🟡 strained → 🔴 critical, driven
by utilization vs throughput, readable at a glance. After 5.1, the map GROWS — now
each node must telegraph when it's drowning, before the aggregate meter (4.3) starts
draining. This is the player's early-warning surface.

**Existing seams to build on (investigate first, don't duplicate):**

- `core/health.odin` (4.3) — the AGGREGATE Network Health meter: windowed per-class
  measurement (the E30 seam). 5.2 adds the PER-NODE layer; the aggregate meter
  stays the loss condition, unchanged.
- `core/stats.odin` (5.7 telemetry) — the per-tick stats stream (+ PP_DEBUG
  overlay). Per-node utilization data may already flow here or one seam away; ride
  it rather than inventing a parallel measurement path.
- 4.1 warning signs + forecast — node strain may already be partially modeled;
  5.2's states are the per-node SURFACE, coherent with (not contradicting) the
  forecast's idea of strain.

**Hard requirements (all pinned by the card):**

1. **Thresholds are defined + deterministic.** Health transitions fire on defined
   utilization-vs-throughput thresholds — data-driven (catalog/config), same inputs
   → same states; no wall-clock, no randomness. Threshold values documented in the
   story/PR rationale.
2. **🔴 traceability:** a critical node is ALWAYS traceable to a measurable strain
   — an inspect/tooltip surface (or equivalent) showing the numbers that put it
   red. Never an unexplained red.
3. **Readability canon — never color alone:** icon + outline (+ pulse for 🔴).
   A colorblind player reads states at a glance. This is canon (a11y core, 7.3,
   builds on this).
4. **Derived state — derive, don't record:** health states are a pure function of
   per-tick measurements. They must NOT enter the replay log / save format (no
   LOG_VERSION bump) — same reasoning as 5.1's decision, state it + prove it in
   the PR body (a replayed run shows identical health timelines implicitly via
   identical measurements).
5. **Goldens:** add T2 golden(s) of health states (data-level). Existing goldens
   unshifted — visual styling is presentation; if any golden captures
   health-affected state deliberately, update deliberately + list.
6. **Rendering:** 🟢🟡🔴 icon + outline on nodes (growth-born nodes included);
   pulse on 🔴. Keep it quiet at 🟢 (the map shouldn't scream when healthy).

**Acceptance:**

1. Card's Given/When/Then verified: threshold transitions (pinned by test), 🔴
   traceable (pinned), no-color-alone readability (pinned by test/evidence).
2. New health T2 golden(s); existing suite unshifted; full local suite green.
3. PR body carries: threshold values + rationale, the derive-don't-record proof,
   the seam chosen (stats vs health.odin extension) + why.
4. Story card status line updated in the same PR (the 5.3 pattern).

**Scope guard:** per-node health surface ONLY. No aggregate-meter changes, no
crisis-engine changes, no a11y overhaul beyond the no-color-alone canon on this
surface, no input work (5.4 next).

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-5.2-node-health
base: v2
model: deepseek/deepseek-v4-flash
pr_review: 1
```
