# Lens brief — CODEBASE FIT (source: `codebase`) — Perkins round 4, packet-plumber-v2-spawn-feel

You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-spawn-feel-r4/project-context.md first — the project's rules for agents.

--- DIFF ---
Read the canonical diff (the exact change under review):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-spawn-feel/r4/diff.patch
The repo at /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-spawn-feel-r4 is checked out at exactly the reviewed state — verify against it.

--- SPEC / CONTEXT ---
Read /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-spawn-feel.md (the job briefing — this IS the spec).

--- ROUND CONTEXT (r4) ---
Round 4 after B1/B2 fixes and two rebases (#82, #83). The last rebase merged #83's Shadow_Spec with this PR's tint: sprite_blit takes BOTH spec and tint now. r1 flagged: spawn_fx_init/spawn_fx_destroy dead code (no call sites; reveals latches the ambient allocator); sfx_fixture positions not matching the harness's actual demo fixture; sfx_load_cat's unused allocator parameter. Audit the CURRENT state of each of those against the file as it exists now (grep for call sites — do not trust the r1 wording), plus anything the rebases introduced.

--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

Specific reality checks wanted this round:
- ALL sprite_blit / sprite_shadow / draw_building / draw_family_wash / draw_type_chip call sites after the #83 merge — did every caller get the new params coherently (defaults vs explicit)? Any caller left passing the OLD signature semantics (e.g. a spec where a tint belongs)?
- The harness demo fixture positions (find where demos build their seed topology in harness/) vs sfx_fixture's claimed "growth.dem recipe" comment — do the positions match?
- spawn_fx_init / spawn_fx_destroy / spawn_fx_reset call sites across app/ and harness/.
- The goldens tree: goldens/spawn_feel/*.png + spawn_feel.t1 + spawn_feel.log.bin vs demos/spawn_feel.dem's capture list (9 captures) — do the manifests, the demo, and the committed files agree?

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "codebase",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. orphan-code, fixture-drift, signature-mismatch>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract: write ONLY the JSON array (no prose, no markdown fencing, no preamble) to this EXACT absolute path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-spawn-feel/r4/codebase.json
An empty array `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota. Then stop — do not wait for input.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
