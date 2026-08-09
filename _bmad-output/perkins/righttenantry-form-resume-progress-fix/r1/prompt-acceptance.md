You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any repository files — the only file you may write is your output file, named at the end.

--- PROJECT CONVENTIONS ---
The project conventions live in AGENTS.md at the root of the worktree:
/Users/moses/.herdr/worktrees/RightTenantry/perkins-form-resume-progress-fix-r1/AGENTS.md
Read it first and treat it as the binding conventions.

--- DIFF ---
The canonical diff under review is at exactly this path:
/Users/moses/code/_bmad-output/perkins/righttenantry-form-resume-progress-fix/r1/diff.patch
Read it in full. Review exactly these bytes — never re-fetch or regenerate the diff.

--- WORKTREE ---
/Users/moses/.herdr/worktrees/RightTenantry/perkins-form-resume-progress-fix-r1
A detached checkout at exactly the reviewed sha. Every verification read happens here.

--- SPEC / CONTEXT ---
- /Users/moses/code/_bmad-output/briefings/righttenantry-form-resume-progress-fix.md — the original job briefing (the spec; no GitHub issue exists for this job).
- /Users/moses/.herdr/worktrees/RightTenantry/perkins-form-resume-progress-fix-r1/_bmad-output/implementation-artifacts/spec-form-resume-progress-fix.md — the implementer's spec of record, shipped inside the diff (frozen intent section + I/O matrix + acceptance criteria).

ROUND CONTEXT (binding): this PR (#569) fixes the stepper's green progress lying after a save-resume restore (visit-based progress — restored steps rendered white; any visited-then-left step rendered green even when empty). The fix derives per-step progress from ACTUAL FIELD CONTENT. Two sanctioned design decisions you must NOT file as findings:
1. The completeness rule REUSES the stepper's own gating rule (findInvalidControls) rather than duplicating the visible-required logic — "reuse, don't duplicate" is an explicit briefing requirement.
2. Vacuous-complete sections (guarantor step without has_guarantor, all-optional tell_us_more) arriving GREEN on resume is a known, intentionally deferred product question — documented in the spec's "Ask First" boundary and I/O matrix. NOT a finding.

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

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

--- FILE OUTPUT CONTRACT ---
When done, write ONLY your JSON array (no prose, no markdown fencing) to exactly this path using the Write tool:
/Users/moses/code/_bmad-output/perkins/righttenantry-form-resume-progress-fix/r1/acceptance.json
Then stop. Do not do anything else.
