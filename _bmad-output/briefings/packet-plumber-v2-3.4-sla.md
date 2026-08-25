# Briefing — packet-plumber-v2-3.4-sla (per-class SLA)

- **Job id:** `packet-plumber-v2-3.4-sla`
- **Repo:** packet-plumber · **Base:** `v2` · **Slug:** `v2-3.4-sla`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — minions. NOT kimi, NOT glm).
  Any mega-minion you spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow).
- **Perkins:** `pr_review: 1` (the v2 line's standing bar).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `v2` (current: 3.3 merged — qos_serialize cyclic-WRR + E9/E22 + Packet_Dropped
  events; LOG_VERSION 3; spatial-lane canon live). Rebase onto origin/v2 if it moves
  mid-work; clean-rebase hygiene (no leftover conflict markers — verify with
  `git diff --check` before force-with-lease).

## Mission (story 3.4 — closing the QoS differentiator)

Implement **Story 3.4: Per-class SLA** from
`_bmad-output/planning-artifacts/sprints/stories-v2.md` (line ~295) — full spec there.
Read the architecture `[ODN-3]` (QoS/SLA inside Flow — no `state.sla` peer), `[ODN-2, m16]`
(integer-ms latency), `[E24]` zero-demand-neutral. Builds on 3.2 (weights) + 3.3 (serialize,
drops).

**Acceptance (condensed — stories-v2 is canonical):**

1. **SLA accumulators as fields of `Flow_State`** — `delivered`, `dropped`,
   `total_latency_ms`, `demand_seen` — per class, fed inside `flow_step` `[ODN-3]`. NO
   `state.sla` peer system.
2. **Latency tracked in integer ms** (sub-tick resolution preserved) `[ODN-2, m16]` —
   no floats in the sim.
3. **Zero-demand tick is neutral** `[E24]` — a tick with no demand must not move any
   accumulator in a way that fabricates breach/latency signal.
4. **Breach crossing** — detectable and **attributable to a class** (which class crossed,
   at which tick) — the attribution feeds the future crisis/surge system; keep the API
   minimal but clean (a breach event record, not UI).
5. **Launchable increment:** per-class SLA gauges update as traffic flows (the demo shows
   delivered/dropped/latency per class live; the 3.2/3.3 lane visuals are the stage).
6. **Golden:** T1 — SLA state in the hash (determinism: same seed + same commands →
   identical accumulator values) `[E10]`. Bless deliberately with proof; existing goldens
   must not shift (if one does, STOP and flag).
7. **Scope guard:** accumulators + breach detection ONLY. No new player commands, no UI
   beyond the gauge readout for the launchable demo, no crisis/surge logic (slice 4).

**Verify:** `odin test` suites green (core/demos/drift/lint), `[E24]` + integer-ms + breach-
attribution tests green, golden blessed with proof, launchable increment in the PR body.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-3.4-sla
base: v2
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1
```
