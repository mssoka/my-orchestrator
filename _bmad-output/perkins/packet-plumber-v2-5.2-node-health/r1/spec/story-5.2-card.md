### Story 5.2 — Node health states

- **Slice:** 5 · **Epic(s):** E3.3, E3.4 · **Systems:** Topology (S1), Crisis (S4).
- **Goal.** Node health states (🟢 healthy → 🟡 strained → 🔴 critical) driven by utilization
  vs throughput; readable at a glance (icon + outline, never color alone).

**Given/When/Then:**
- **Given** the health-state model + the readability canon;
- **When** utilization crosses thresholds;
- **Then** health transitions fire on defined thresholds; a 🔴 node is always traceable to a
  measurable strain; state is readable without color (icon + outline + pulse).

- **Edge-case contracts:** health-on-thresholds, 🔴 traceable. **Golden:** T2 of health
  states.
- **Launchable increment:** watch nodes telegraph trouble (🟡→🔴) under load.
- **Status:** implemented 2026-08-16 — PR open (the per-node health layer `core/node_health.odin`
  beside the 4.3 health module: the never-serialized tri-state `crisis.node_health` derived
  per tick from the un-forwardable pile vs the node's throughput ceiling — the balance
  `warnings` 70/90 thresholds shared with the 4.1 strain, coherence by construction; a
