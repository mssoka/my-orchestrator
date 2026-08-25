# Lens brief — EDGE CASE (source: `edge`) — Perkins round 4, packet-plumber-v2-spawn-feel

You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-spawn-feel-r4/project-context.md first — the project's rules for agents (Odin + raylib; pure core ODN-1; integer-only sim paths ODN-10; arena discipline ODN-18; owned RNG ODN-9; events not callbacks ODN-14; render determinism §10.4: no transcendentals in the raster path, tick-anchored animations).

--- DIFF ---
Read the canonical diff (the exact change under review):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-spawn-feel/r4/diff.patch
The repo at /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-spawn-feel-r4 is checked out at exactly the reviewed state — verify against it.

--- SPEC / CONTEXT ---
Read /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-spawn-feel.md (the job briefing — this IS the spec: view-layer-only spawn telegraph/reveal, tick-anchored T2 stability, sim-validity timing unchanged).

--- ROUND CONTEXT (r4) ---
Round 1 blockers were fixed: B1 (spawn_fx_draw_highlight radius now compares TILE units both sides — verify the fix is actually in the file) and B2 (spawn_fx_test pending-commands pin reworked to a legal ROUTER PLACE with anti-vacuity + negative legs). The PR then rebased twice onto v2 (#82 trail rings, #83 scale/shadows — sprite_blit now takes BOTH a Shadow_Spec and a tint). Delta-introduced findings are expected and wanted.

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

Pay particular mechanical attention (derived from the changed code, not assumed): the u64 tick arithmetic (`tick % interval`, window/lead computation, `T - SPAWN_LEAD_TICKS` underflow at tiny intervals), the reveal-buffer bounds (`len > 4` trim, `ordered_remove`), the walk-back id math (`topo.next_node_id - remaining`), the B1 radius fix's f32 tile-unit comparison (dx*dx+dy*dy > rad*rad at exactly 8.0 tiles — boundary pipes), the shadow-clone completeness (which [dynamic] fields does `core.step` touch that `shadow_clone` might miss — read core/sim step paths to check), temp-allocator lifetime of the shadow + per-tick batches, the B2 reworked pending test's own paths (can the anti-vacuity assert fire spuriously?), the #83 sprite_shadow alpha merge (`u8(f32(spec.ink) * f32(alpha) / 255)` truncation at low alphas, tint.a=0 callers), the i32→i64 casts in the diameter guard ((w-1)²+(h-1)² at w or h = 1), and integer/float coercions in the draw math (`u8(alpha*255)` truncation, `f32` precision).

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "edge",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. boundary, underflow, allocator>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract: write ONLY the JSON array (no prose, no markdown fencing, no preamble) to this EXACT absolute path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-spawn-feel/r4/edge.json
An empty array `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota. Then stop — do not wait for input.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
