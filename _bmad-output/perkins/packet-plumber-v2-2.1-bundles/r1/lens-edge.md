# Lens: Edge Case (Perkins r1 — packet-plumber-v2-2.1-bundles)

You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines. No editorializing.

## Inputs (read them; verify against the worktree)
- **Diff:** `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.1-bundles/r1/diff.patch`
- **Worktree (verify claims here — this is the reviewed state):** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-2.1-bundles-r1`
- **Spec/context (read for framing only):** `/Users/moses/code/_bmad-output/briefings/perkins-packet-plumber-v2-2.1-bundles-r1.md` (the lens-guards section), and `project-context.md` in the worktree root (ODN-1/9/10/11 conventions).

## Method
Mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples for THIS change: empty pipe arrays (np == 0), a topology with zero live pipes, `resize`/`clear` on dynamic arrays across rebuilds, a bundle whose member count hits a capacity bound, `NO_BUNDLE` sentinel handling, `pipe_bundle[pipe_slot]` indexing when `pipe_slot >= len(pipe_bundle)`, mixed live/dead pipe slots in the rebuild scan, `bundle_capacity_for_pipe` returning 0 and the flow's fallback, the `count-1` width calc when count could be 0, `cat.pipe_tiers[tier]` indexing, a pair where lo==hi (self-loop pipe).

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently.

## ⚠️ Lens-guards (prevent false positives — read the briefing's guard section)
- **NO LOAD BALANCING is the requirement**, not a gap. A bundle is ONE pooled edge (cap = sum). Do NOT flag "no per-pipe distribution / no round-robin" — pooling is the spec. (A round-robin/weighted-LB pattern *sneaking in* would be a real blocker, but its absence is correct.)
- **Static sum at table-build** is correct; capacity is intentionally NOT computed per-packet.
- **Bundle state is intentionally DERIVED (rebuilt from topology), not serialized** — do not flag "bundles not in save/log" as a gap; that is by design (ODN-10/11). The composing pipes ARE serialized.
- **`Packet.edge` stays a pipe id (a representative member)** — by design, not a bug.
- **The 2.3 "severance" concern** (a representative pipe demolished but bundle survives) is a FUTURE-story note, NOT a 2.1 defect — do not flag it.
- Do not flag em-dashes in copy, the `v2` base, or re-open 1.1–1.4.

## OUTPUT
Write ONLY a valid JSON array to: `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.1-bundles/r1/edge.json`
Schema:
```
{
  "source": "edge",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. boundary, indexing, sentinel>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<exact lines you READ from the worktree file/diff, verbatim. 'N/A' only when no code anchor is possible.>",
  "detail": "<≤40 words>",
  "recommended_fix": "<≤40 words>"
}
```
ONLY the JSON array in the file. `[]` is valid. Accuracy > volume. When done: "edge lens done — N findings".
