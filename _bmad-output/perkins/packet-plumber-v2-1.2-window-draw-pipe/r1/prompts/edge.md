# LENS: Edge Case (source = `edge`)

First load the shared context: read `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.2-window-draw-pipe/r1/prompts/_shared.md` (it has the lens-guards, the output schema + contract, the empirical gate status, and the canonical input paths). Follow it exactly.

## YOUR LENS — pure path tracer
You are a pure path tracer. Do NOT comment on whether the code is good or bad — list ONLY unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples relevant to THIS diff: empty arrays / zero counts / max sizes (Topology node/pipe arrays, the snap loop over `node_alive`), null/missing-node lookups (`node_slot` returns false), integer overflow in `dist2`/`isqrt`/`span_between` (i64 math on grid coords), the `isqrt` loop termination + the `d2 - r*r > r` round-half-up branch, off-by-one in the snap-radius inclusive boundary (E4: `d2 <= r2` vs `d2 <= best_d2` with the tie-break `continue`), the fixed-timestep accumulator clamp (`accum = min(accum, tick_seconds)` + `max_steps=5`), JSON parse failures / wrong types / missing fields in `catalogs_load`, the `jint` float→i32 cast path, the `node_slot_raw` "unreachable when called post-validate" fallback (returns slot 0 — what if it's hit?), the demo parser (`parse_ms`, `parse_uint`, forward-compat `case:`), the drift mutation byte offsets (catalog_hash@17, logic_hz@25, tag@41 — what if the log is shorter than assumed? the `if len(src) > N` guards), `replay_hashes` reading a log whose header `ticks` exceeds the manifest, the T2 capture-tick floor quantization (`cap_tick == tick` exact-equality), `compare_images` dimension mismatch + the `bbox` init sentinel `{1<<30,...}`.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard; discard handled ones silently. No editorializing.

## OUTPUT
Write ONE valid JSON array (schema + contract in `_shared.md`) to:
`/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.2-window-draw-pipe/r1/edge.json`

`source` = `"edge"`. Only the JSON array in the file. `[]` is valid. Verify every claim by reading the actual code in the worktree; quote the exact lines in `evidence`. When done, stop.
