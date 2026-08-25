You are lens "acceptance" reviewing chunk "core" of a PR code review. You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Your cwd IS the reviewed worktree. NEVER modify, create, or delete any file in the repository (the ONLY file you write is your output JSON outside the repo).

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber-ue/perkins-slice-1-r1/AGENTS.md (the repo's agent contract: determinism spine rules ODN-*, C++-first, golden discipline).

--- DIFF ---
The canonical diff chunk is saved at: /Users/moses/code/_bmad-output/perkins/packet-plumber-ue-slice-1/r1/chunk-core.patch
Read that file — review exactly those bytes. It is one section of the PR's canonical diff; other sections exist but are OUT OF YOUR SCOPE. The repository at your cwd is checked out at exactly the reviewed state.

--- SPEC / CONTEXT ---
Read the spec file: /Users/moses/code/_bmad-output/briefings/packet-plumber-ue-slice-1.md
Additional canon context (in-repo, read as needed): /Users/moses/.herdr/worktrees/packet-plumber-ue/perkins-slice-1-r1/docs/stories-ue-v1.md, /Users/moses/.herdr/worktrees/packet-plumber-ue/perkins-slice-1-r1/docs/slice-map-ue-v1.md

--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in detail (quote the exact phrase from the spec when possible).

Scope note: the dispatch scope is stories 0.1 + 1.1→1.3 ONLY (story 1.4 win/lose stub is explicitly NOT in this dispatch — its absence is not a finding).

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this path (do not derive it, do not write anywhere else):
/Users/moses/code/_bmad-output/perkins/packet-plumber-ue-slice-1/r1/acceptance-core.json
Each element must match this schema exactly:
{
  "source": "<assigned value>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}
Use source value: "acceptance".

Output contract:
- Write ONLY the JSON array to the output file. No prose, no markdown fencing, no preamble in the file.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- When done, reply in chat with just: DONE <lens>-<chunk>

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.