You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- INPUTS (read these exact files) ---
- DIFF (chunk c1 of 2 — the canonical diff was chunked per the big-diff policy; review exactly these bytes; read the file in full, paging with offset/limit): /Users/moses/code/_bmad-output/perkins/packet-plumber-3d-e2-flow-qos/r1/diff-c1.patch
  Chunk c1 = implementation core: scripts/, scenes/, tools/. The other chunk exists but is out of scope for this lens run; the worktree below contains the full merged state if you need to cross-reference.
- WORKTREE (checkout at exactly the reviewed state; every verification read happens here): /Users/moses/.herdr/worktrees/packet-plumber-3d/perkins-e2-r1
- SPEC 1 (original job briefing — task spec): /Users/moses/code/_bmad-output/perkins/packet-plumber-3d-e2-flow-qos/r1/spec-job-briefing.md
- SPEC 2 (merged epic section "E2 — Flow Simulation, Packet Types & QoS" — stories E2.1–E2.5 + test contracts ARE the acceptance criteria, plus the folded editor-preview QoL story): /Users/moses/code/_bmad-output/perkins/packet-plumber-3d-e2-flow-qos/r1/spec-epic-e2.md

--- PROJECT CONVENTIONS ---
none

Read the DIFF chunk file first in full, then the spec files, then verify claims against the WORKTREE as your lens requires.

--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "codebase",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

FILE-OUTPUT CONTRACT (headless): write ONLY your final JSON array to this exact path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-3d-e2-flow-qos/r1/codebase-c1.json
Then stop. Do not print the JSON to chat; the file is the deliverable.

Output contract:
- Return ONLY the JSON array in the file. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.