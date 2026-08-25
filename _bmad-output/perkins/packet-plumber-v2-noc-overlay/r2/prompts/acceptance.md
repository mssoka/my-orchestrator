You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Your cwd is the exact reviewed state of the repository — trust it, not any branch or remote.

--- PROJECT CONVENTIONS ---
Read project-context.md in your cwd first (the repo's agent conventions: pure core/ODN rules, PP_DEBUG compile gates, view-layer patterns, testing rules, anti-patterns).

--- DIFF ---
The canonical unified diff under review (2082 lines, PR #85, base branch v2) is saved at:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-noc-overlay/r2/diff.patch
Read exactly those bytes; never re-derive the diff from git. The binary .png hunks are committed capture artifacts — judge the code.

--- SPEC / CONTEXT ---
Read /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-noc-overlay.md — the job briefing; it IS the spec for this PR (there is no GitHub issue).

--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

--- OUTPUT ---
Write ONE valid JSON array — the file must contain ONLY the JSON array, no prose, no markdown fencing, no preamble — to exactly this absolute path (do not derive, rename, or relocate it):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-noc-overlay/r2/acceptance.json
Each element must match this schema exactly:
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
After writing the file, reply with a one-line confirmation and stop.

Output contract:
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
