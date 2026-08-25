Read `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.2-ecmp/r1/_shared_header.md` first — it has your inputs, lens-guards, output contract, and accuracy mandate. This file adds only your lens brief + output path.

LENS — EDGE CASE (pure path tracer): mechanically walk every branching path + boundary condition reachable from the diff hunks. Derive edge classes from the changed code itself (empty lists, zero counts, N==0, N==1, max sizes, off-by-one, integer overflow, stale table shape, count==0 vs ok==false, unreachable nodes, the `int(offset)+int(pick)` index bounds, the `seen[]` per-(u,d) reset, the `dist[u]-1` when dist[u]==0, self-loops, dead pipes, node id 0). For each path determine whether the diff handles it; report ONLY unhandled paths lacking an explicit guard. No editorializing; no style comments.

Write your JSON array to `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.2-ecmp/r1/edge.json` (source:"edge"). Stop after writing.
