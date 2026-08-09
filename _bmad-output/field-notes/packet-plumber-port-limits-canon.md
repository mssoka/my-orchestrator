# Field notes: packet-plumber-port-limits-canon (2026-08-08)

- The atomic-multi-edit trap bit me live: one `oldText` aimed at the wrong
  file (decision-log text fired at gdd.md) rejected BOTH edits silently —
  check each oldText's target file before batching, re-issue survivors
  per-file.
- Packet-Plumber GDD canon amendments: provenance is MANDATORY in
  `decision-log.md` (the doc's own rule) — dated entry + inline tag in
  gdd.md matching house style `(*...addition...*)` / `[RULING — user, DATE]`.
- Ground-truth-first paid off: `game/data/node_types.json` +
  `topology_graph.gd` confirmed basic 4 / mid 8 / high 16, "parallel pipes
  each count", and BOTH-ENDS port consumption before canonizing — the
  per-end ambiguity was the only edge-hunter finding (fixed pre-commit).
