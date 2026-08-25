# Lens brief — ARCHITECTURE (source: `architecture`) — Perkins round 1, packet-plumber-v2-spawn-feel

You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-spawn-feel-r1/project-context.md first — the project's rules for agents (Odin + raylib; pure core ODN-1; arena discipline ODN-18 — three arenas, core never allocates without an explicit allocator; no globals ODN-13; events not callbacks ODN-14; render determinism §10.4 — no transcendentals in the raster path; layering: core ← app/render ← app).

--- DIFF ---
Read the canonical diff (the exact change under review):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-spawn-feel/r1/diff.patch
The repo at /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-spawn-feel-r1 is checked out at exactly the reviewed state — verify against it.

--- SPEC / CONTEXT ---
Read /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-spawn-feel.md (the job briefing — this IS the spec: view-layer-only spawn telegraph/reveal; the shadow-sim prediction approach is the documented design decision, justified in the PR body `_pr_body_spawn_feel.md` inside the diff).

--- YOUR LENS ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

Specific architectural questions worth checking against the real code (verify, don't assume):
- The render package now contains a shadow-sim predictor (`shadow_clone` deep-copies `Run_State` field-by-field). What happens to this clone when `core.Run_State` gains a new `[dynamic]` field in a future change — is there a guard (test or otherwise) that catches a missed field, and is that guard durable?
- `spawn_fx_predict` runs a ≤10-step sim replay per frame-window in the APP render loop (and per capture in the harness). Is the cost bounded and does it respect the app's frame budget discipline (compare how other view-layer systems guard cost)?
- The app (main.odin) now calls `rnd.spawn_fx_predict(&app.view, &app.state, ...)` — passing the live `Run_State` by pointer into the render package. Does the render package mutate it anywhere (ODN-1 purity), or is the read-only discipline only enforced by convention?
- Default-parameter threading (`sprite_blit`/`draw_family_wash`/`draw_type_chip` gained optional params) — consistent with how the codebase evolves shared draw procs, or a smell?
- Is the new state (`Spawn_FX` on `View`) reset at every boundary that matters (start_run, harness per-demo)?

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "architecture",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. coupling, layering, maintainability>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract: write ONLY the JSON array (no prose, no markdown fencing, no preamble) to this EXACT absolute path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-spawn-feel/r1/architecture.json
An empty array `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota. Then stop — do not wait for input.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
