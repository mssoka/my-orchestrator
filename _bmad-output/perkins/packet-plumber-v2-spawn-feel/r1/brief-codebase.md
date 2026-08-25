# Lens brief — CODEBASE FIT (source: `codebase`) — Perkins round 1, packet-plumber-v2-spawn-feel

You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-spawn-feel-r1/project-context.md first — the project's rules for agents (Odin + raylib; pure core ODN-1; arenas ODN-18; the rlsw software-renderer golden harness; naming/style conventions of the codebase).

--- DIFF ---
Read the canonical diff (the exact change under review):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-spawn-feel/r1/diff.patch
The repo at /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-spawn-feel-r1 is checked out at exactly the reviewed state — verify against it.

--- SPEC / CONTEXT ---
Read /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-spawn-feel.md (the job briefing — this IS the spec).

--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

Specific reality checks worth doing (verify, don't assume):
- `shadow_clone` claims to copy "everything step() touches" — diff the field list in `shadow_clone` against `core.Run_State`'s actual field list (read the struct definition) AND against every `[dynamic]`/pointer field `core.step` and its callees (flow/growth/crisis/health/era) actually read or write. A missed field is a real bug class here.
- `clone_dyn` duplicates an existing helper? Search the codebase for existing deep-copy utilities (snapshot/clone paths in core or app) that already do this.
- `pp.run_destroy` on a clone whose `action_log`/`events` were set to `{}` — read `run_destroy` and confirm zero-length dynamic delete is safe/correct in Odin for that type.
- `node_screen`, `smoothstep01`, `clamp01` — does `smoothstep01`/`clamp01` already exist elsewhere in app/render (duplication)? Check the existing pulse/easing helpers.
- `EVENT_TAG_NODE_SPAWNED`, `topology_spawn_node`, `topology_apply_edit`, `node_slot`, `topology.next_node_id`, `topology.gen`, `cat.balance.terminal_spawn_interval_ticks`, `cat.balance.logic_hz`, `state_hash` — confirm each exists with the signature the diff uses.
- The goldens set: does `harness/run.odin` integration match how other per-demo view state is reset (a11y_reset precedent)?
- The test file's `sfx_load_cat` mirrors the app's load path — is there an existing shared/catalog test helper it duplicates (check how other render/core tests load catalogs)?
- Orphans: did `sprite_shadow`/`sprite_blit`/`draw_family_wash`/`draw_type_chip` signature changes leave any call site un-updated (compile break) — enumerate every caller in the repo.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "codebase",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. missing-symbol, duplication, orphan>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract: write ONLY the JSON array (no prose, no markdown fencing, no preamble) to this EXACT absolute path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-spawn-feel/r1/codebase.json
An empty array `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota. Then stop — do not wait for input.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
