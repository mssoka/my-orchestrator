You are a review lens running headless. Execute this brief EXACTLY. Your single deliverable is one JSON file named at the end. Do not modify any file in the repository checkout.

You are reviewing a code diff. You have read-only access to the repository at your cwd (your cwd IS the reviewed state) and may verify the diff's claims against the actual codebase using your available tools.

--- INPUTS (read all of these first) ---
1. THE DIFF (canonical bytes — review exactly this; unified diff, ~2636 lines, PR #632 vs develop):
   /Users/moses/code/_bmad-output/perkins/righttenantry-demo-polish-2/r3/diff.patch
2. PROJECT CONVENTIONS: read the file AGENTS.md at the repository root (your cwd).
3. SPEC / CONTEXT (read both, in this order):
   - /Users/moses/code/_bmad-output/briefings/righttenantry-demo-polish-2.md — the job briefing: what this diff was funded to do (toast parity, real-depth reports, Compare Top 3)
   - /Users/moses/code/_bmad-output/perkins/righttenantry-demo-polish-2/r3/pr-body.md — the PR body: decisions & rationale

--- YOUR LENS ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

--- OUTPUT ---
Write ONE valid JSON array to the file /Users/moses/code/_bmad-output/perkins/righttenantry-demo-polish-2/r3/architecture.json — create or overwrite it. That file must contain ONLY the JSON array: no prose, no markdown fencing, no preamble. Then stop.

Each element must match this schema exactly:
{
  "source": "architecture",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract: the file contains ONLY the JSON array. No prose, no markdown fencing, no preamble. Empty array `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
