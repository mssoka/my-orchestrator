You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- INPUTS (read these exact files) ---
- DIFF (chunk c2 of 2 — the canonical diff was chunked per the big-diff policy; review exactly these bytes; read the file in full, paging with offset/limit): /Users/moses/code/_bmad-output/perkins/packet-plumber-3d-e2-flow-qos/r1/diff-c2.patch
  Chunk c2 = tests + artifacts: tests/, captures/, _bmad-output/, README.md. The other chunk exists but is out of scope for this lens run; the worktree below contains the full merged state if you need to cross-reference.
- WORKTREE (checkout at exactly the reviewed state; every verification read happens here): /Users/moses/.herdr/worktrees/packet-plumber-3d/perkins-e2-r1
- SPEC 1 (original job briefing — task spec): /Users/moses/code/_bmad-output/perkins/packet-plumber-3d-e2-flow-qos/r1/spec-job-briefing.md
- SPEC 2 (merged epic section "E2 — Flow Simulation, Packet Types & QoS" — stories E2.1–E2.5 + test contracts ARE the acceptance criteria, plus the folded editor-preview QoL story): /Users/moses/code/_bmad-output/perkins/packet-plumber-3d-e2-flow-qos/r1/spec-epic-e2.md

--- PROJECT CONVENTIONS ---
none

Read the DIFF chunk file first in full, then the spec files, then verify claims against the WORKTREE as your lens requires.

--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "acceptance",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

FILE-OUTPUT CONTRACT (headless): write ONLY your final JSON array to this exact path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-3d-e2-flow-qos/r1/acceptance-c2.json
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