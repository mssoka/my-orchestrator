You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Your current working directory IS the exact reviewed state — trust it.

--- PROJECT CONVENTIONS ---
Read project-context.md at the repo root first (Odin + raylib game: pure integer-only core, view-layer-only floats, arena discipline, golden-image harness with zero-drift doctrine, named-constant rules).

--- DIFF ---
The canonical unified diff — the exact bytes under review (read this file, never regenerate the diff):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-noc-readability-2/r1/diff.patch

--- SPEC / CONTEXT ---
The spec this diff must satisfy:
/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-noc-readability-2.md
The implementation's own claims (PR body — treat as claims to audit, not truth):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-noc-readability-2/r1/pr-body.md

--- YOUR LENS ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

Context you should weigh: this change adds `View.play_w` (a playfield-width field threaded through camera fit / zoom / pan / pullback and several HUD anchors) to implement a docked full-height NOC rail. Judge whether that threading is architecturally sound against how the View/camera/HUD layers already interact in this codebase.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "architecture",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. coupling, layering>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract: write ONLY your JSON array — no prose, no fencing, no preamble — to this exact absolute path using your file-writing tool:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-noc-readability-2/r1/architecture.json
then stop. `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:
NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.
Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
