You are reviewing a code diff — ONE specialist lens (acceptance) in a multi-lens headless review. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.5-demolish-input-r1/project-context.md (the project's AI-agent rules) before judging conventions.

--- DIFF ---
Read exactly this file: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.5-demolish-input/r1/diff.patch (unified diff of PR #59, reviewed sha 55d1b66, repo Packet-Plumber base v2 — an Odin/raylib game; story 5.5, the demolish input surface on the intent layer).

Verification reads happen in the detached worktree at exactly the reviewed sha: /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.5-demolish-input-r1 (trust it, not origin/v2).

--- SPEC / CONTEXT ---
Read: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.5-demolish-input/r1/spec-context.md (the spec + this round's guards) and /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.5-demolish-input/r1/story-card-5.5.md (the story 5.5 card, verbatim). The full original job briefing is at /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-5.5-demolish-input.md if you need it.

--- YOUR LENS ---
Audit the diff against the spec and context docs above (spec-context.md sections 1-2 are the acceptance criteria; section 3 lists what is OUT of scope — do not file findings on out-of-scope items). Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

The ONE hard blocker class is demolish input surface PARITY (FORGE #6): demolish reachable from mouse, touch, AND controller through the SAME validated intent path — no per-device command production. Verify the controller leg (pad X = RIGHT_FACE_LEFT -> the shared Demolish intent; Node_Select mirrors the dpad cursor onto the selection: junction -> select, terminal -> clear), the W1-r4 positive pins (input_parity_demolish_btn_node / _btn_pipe actually execute popover_demolish_hit's positive path and would fail if the wiring died), and the r3-N7 gate-9 negative-control leg (bogus arg rejected, [ -x ] guard against the 127->!->0 false-green). Verify the PR-body claims listed in spec-context.md section 4 against the actual code.

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

--- OUTPUT ---
When your analysis is complete, write your final answer as ONE valid JSON array to this EXACT absolute path using the Write tool:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.5-demolish-input/r1/acceptance.json
The file must contain ONLY the JSON array — no prose, no markdown fencing, no preamble. Each element must match this schema exactly:
{
  "source": "acceptance",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}
Then reply with exactly one word: done. Do not create or modify any other files. Do not fix anything. Empty array `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. Accuracy > volume — an empty array is a fine and honest answer when nothing is wrong.
