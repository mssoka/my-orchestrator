# Field notes — packet-plumber-architecture-v1 (architecture minion)

- The `gds-game-architecture` skill's per-step A/P/C "Ready to begin? [Y/N]"
  checkpoints are **pre-approved** per the orchestration standing orders; the
  briefing's detailed scope overrides the skill's generic GDD discovery — proceed
  headless (read ALL source in full first), halt only on genuine blockers. None
  arose; the lavish review was the human gate.
- A **2-hunter review swarm** (adversarial-general + edge-case-hunter mega-minions)
  caught real contradictions the author was blind to on a high-stakes doc every
  downstream agent reads (CrisisEngine↔Director data-flow *direction*, `Vector3`
  vs `Vector3i` on the determinism spine, sim-tick SLA/QoS ownership, GDScript-has-
  no-interfaces). Worth the ~2-pane cost; verify every finding against disk
  (ground-truth-first) before applying — all 40 findings here were legit.
- lavish markdown→HTML via `marked --gfm -o` (file write, **no pipe**) handled a
  78KB doc cleanly (98KB HTML, verified tail); one `poll` return can deliver a
  **batch** of 7 feedback items at once — handle them together, re-render, reply
  once. Batch the doc edits in one `edit` call (disjoint oldTexts), re-render,
  reply — faster than per-item round-trips.
