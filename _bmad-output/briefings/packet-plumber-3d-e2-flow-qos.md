# Briefing: packet-plumber-3d-e2-flow-qos

Read the standing orders first: `/Users/moses/code/docs/orchestration-playbook.md`
section 'Minion standing orders'. This briefing is your task spec.

## Task

Build **E2 — Flow Simulation, Packet Types & QoS** (the living network), plus
one folded QoL story (editor preview). Spec of record:
`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-3d-2026-09-04/epics.md`
section **E2** (+ GDD's sim/QoS sections). The epic's stories E2.1–E2.5 and
test contracts ARE your acceptance criteria.

## Scope (from the epic)

1. **E2.1 Flow simulation** — deterministic tick-driven sim core (owned RNG,
   fixed tick); junctions forward per-packet (ECMP hash across equal-cost
   paths); parallel pipes bundle into pooled capacity; path cost = static
   pipe-tier cost. *(PP-Odin rulings inherited.)*
2. **E2.2 Packet classes** — MVP: email (low/low/low) + streaming (med/med/high).
3. **E2.3 Link-level class queues** — 3 lanes per pipe (Express/Standard/
   Best-effort); all traffic starts Standard 100%; assignment ladder
   (100 · 70/30 · 50/30/20) data-driven; per-pipe overrides; QoS panel on
   pipe select. **Nothing auto-allocates.**
4. **E2.4 Serialization at nodes** — Express → Standard → Best-effort
   egress, work-conserving gap-filling; VISIBLE in 3D (strand speed + node
   egress rate).
5. **E2.5 Per-class SLA tracking** — latency/loss per class; thresholds
   from the GDD's Numerical Design section.

**Folded QoL (user ruling, gate feedback):** `@tool` **editor preview** — an
inspector "Regenerate Preview" on the composition root that runs the SAME
seeded generation inside the editor viewport (canon `_ready()` flow
untouched; no behavior change at runtime). The user should SEE the world in
the editor without pressing play.

**Scale ruling (user):** world stays at slice-1 scale for E2 — NO scale/density
changes. Big world is E3's epic. Do not freelance density.

## Acceptance

- **A1 (canon):** every E2 test contract demonstrable — replay **byte-identity
  on a fixed seed** · contention drops by drop precedence (lowest first) ·
  dedicated lane reservation holds its class's capacity · SLA breach
  detectable + attributable · **view-layer changes never shift sim state**
  (orbit/zoom/QoS panel interactions leave the replay hash unchanged).
- **A2 (visible):** packets visibly stream along arcs at class-dependent
  speed; egress serialization readable at nodes. Captures in `captures/`
  referenced from the PR body (replay determinism capture + a QoS-panel
  interaction capture + editor-preview viewport capture).
- **A3 (verified):** Godot MCP is your build/verify surface — `editor-run`,
  `debug-output`, `lsp_get_diagnostics` clean on all GDScript.
- **A4 (gate):** PR opens, Perkins loops to APPROVED, the user plays and
  rules. PR body carries the run command.

## Model policy

Minion: **`zai-coding-cn/glm-5.3-flash`**. Mega-minions: same, skills named.

## Skills policy

Workflow: **`gds-quick-dev`**. No lavish (code deliverable).

## Perkins

`pr_review=1` — canon-surface sim code. Loop-until-APPROVED; fold fixes
locally, hold the push until each verdict posts.

## Dispatch parameters

```
job_id:    packet-plumber-3d-e2-flow-qos
repo:      packet-plumber-3d
repo_root: /Users/moses/code/packet-plumber-3d
slug:      e2-flow-qos
base:      main
model:     zai-coding-cn/glm-5.3-flash
pr_review: 1
notes:     Worktree from origin/main (c4edcef). _bmad symlink bootstrap.
           PARALLEL LANE: packet-plumber-3d-asset-scout also dispatches —
           create worktrees strictly sequentially (index.lock race).
```
