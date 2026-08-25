# Lens: architecture (Architecture) — Perkins r1

**OUTPUT FILE:** `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.3-packet-flow/r1/architecture.json`

First read the common context:
`/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.3-packet-flow/r1/_lens_common.md`

## Your lens
Architectural fit review. Given the diff and the surrounding codebase (read the
existing `core/*.odin` to judge fit):
- Does it follow existing patterns and conventions (ODN-1 core purity, ODN-10
  array-only/no-map, ODN-13 no globals, integer-only sim, owned-RNG,
  events-not-callbacks, arena discipline)?
- Does it introduce unnecessary coupling between modules (e.g. flow reaching
  into rendering, or the routing table being serialized when it's derived
  state)?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries (core vs app vs harness)?
- Will it create technical debt or make future slices (ECMP/bundles/QoS) harder?
- Does complexity match the problem (1.3 is trivial single-path)? Any premature
  abstraction?

Key architectural facts to verify AGAINST (flag if violated, do NOT flag the
facts themselves): the routing table is DERIVED from topology and correctly NOT
serialized; the flow demand is run-setup re-created in both live+replay paths;
`step` is the ONLY entry point; the forwarding rebuild is gated on
`topology.gen != routing_gen` (rule 1, synchronous in-tick).

## Output
Write ONE valid JSON array to your OUTPUT FILE (source = `"architecture"`).
`[]` is valid. Accuracy > volume. Then print `LENS DONE: architecture` and stop.
