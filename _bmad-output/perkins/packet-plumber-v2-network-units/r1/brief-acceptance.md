# Lens task — ACCEPTANCE AUDITOR (source: acceptance)

You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Your cwd IS the repository worktree at exactly the reviewed state — verify against it, not against any other checkout.

--- PROJECT CONVENTIONS ---
Read project-context.md in the worktree root (the project's conventions file) and apply it.

--- DIFF ---
The canonical diff (review EXACTLY these bytes — read it first, in full):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-network-units/r1/diff.patch
(unified diff, 984 lines)

--- SPEC / CONTEXT ---
The binding spec (the original job briefing — read it IN FULL; it is short and every line is load-bearing):
/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-network-units.md

--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

Verify claims against the actual code in the worktree — e.g. when the diff claims "sim math untouched" or "no data/*.json changed", check the worktree and the diff yourself. The PR also carries its own implementation-spec artifact (`_bmad-output/implementation-artifacts/spec-packet-plumber-v2-network-units.md`, included in the diff as a new file) — that artifact is the IMPLEMENTATION's own plan, NOT the binding spec; deviations between it and the job briefing above are exactly what you must audit.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "acceptance",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. ac-violation, scope-drift, missing-behavior>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

FILE-OUTPUT CONTRACT (headless override — authoritative): do NOT print the JSON as your reply. Write ONLY the JSON array (no prose, no fencing) to EXACTLY this absolute path with your write tool, then stop:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-network-units/r1/acceptance.json

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
