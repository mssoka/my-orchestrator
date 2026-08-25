# Lens: edge (Edge Case Hunter) — Perkins r1

**OUTPUT FILE:** `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.3-packet-flow/r1/edge.json`

First read the common context:
`/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.3-packet-flow/r1/_lens_common.md`

## Your lens
You are a pure path tracer. Do NOT comment on whether the code is good or bad —
list ONLY unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly
reachable from the diff hunks. Derive edge classes from the changed code itself
— no fixed checklist. Examples relevant here: boundary conditions (empty
`packets`/`demand`, zero `bandwidth`, zero `capacity`, `n==0` in the routing
table, a packet spawned at its own dst, a `dst` removed mid-traversal),
off-by-one in the +1/-1 id scheme, the `gen` bump missing on some mutation,
integer overflow in `progress_units`/`need = n*n`, state the new code doesn't
account for (e.g. a topology change that does NOT bump `gen`), input the new
code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled
paths that lack an explicit guard; discard handled ones silently. No
editorializing.

Remember the lens-guards (common context): per-hop is required (absence of route
cache is correct); 1.3 is single-path (no ECMP/bundles); the `on_edge` flag and
+1 id scheme are the CORRECT id-0 fix, not a smell.

## Output
Write ONE valid JSON array to your OUTPUT FILE (source = `"edge"`). `[]` is
valid. Accuracy > volume. Then print `LENS DONE: edge` and stop.
