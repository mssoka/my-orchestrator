You are reviewing a code diff — ONE specialist lens (security) in a multi-lens headless review. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.5-demolish-input-r1/project-context.md (the project's AI-agent rules) before judging conventions.

--- DIFF ---
Read exactly this file: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.5-demolish-input/r1/diff.patch (unified diff of PR #59, reviewed sha 55d1b66, repo Packet-Plumber base v2 — an Odin/raylib game; story 5.5, the demolish input surface on the intent layer).

Verification reads happen in the detached worktree at exactly the reviewed sha: /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.5-demolish-input-r1 (trust it, not origin/v2).

--- SPEC / CONTEXT ---
Read: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.5-demolish-input/r1/spec-context.md (the spec + this round's guards) and /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.5-demolish-input/r1/story-card-5.5.md (the story 5.5 card, verbatim). The full original job briefing is at /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-5.5-demolish-input.md if you need it.

--- YOUR LENS ---
OWASP-oriented security review of the diff, proportionate to context (a local single-player Odin/raylib game + its shell-script CI gates and GitHub workflow — no network service, no user data, no secrets). Identify:
- Unsafe shell construction in the CI gate changes (ci-local.sh / ci.yml): quoting, injection via arguments, negation pitfalls (the 127->!->0 false-green class), PATH/permission assumptions
- Unsafe handling of the new input paths (out-of-bounds indexing from input state, unvalidated indices into topology arrays reachable from the new code)
- Anything logged/serialized that shouldn't be (replay log purity — inputs must never be serialized)
- Insecure defaults introduced by the diff
Do not manufacture web-security findings that have no anchor in this diff; an empty array is an honest answer.

--- OUTPUT ---
When your analysis is complete, write your final answer as ONE valid JSON array to this EXACT absolute path using the Write tool:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.5-demolish-input/r1/security.json
The file must contain ONLY the JSON array — no prose, no markdown fencing, no preamble. Each element must match this schema exactly:
{
  "source": "security",
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
