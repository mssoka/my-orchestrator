You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Work in /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-613-615-r1 (a checkout at exactly the reviewed state).

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-613-615-r1/AGENTS.md (repo project instructions: brand voice, no-em-dash ruling, code style, invariants).

--- DIFF ---
The exact diff under review is saved at /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-613-615/r1/diff.patch (unified diff, 763 lines). Read it FIRST. Every reviewer reviews these identical bytes; never regenerate or re-derive the diff.

--- SPEC / CONTEXT ---
- /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-613-615/r1/issue-613.json — GitHub issue #613 (stepper label ambiguity; the issues ARE the spec)
- /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-613-615/r1/issue-615.json — GitHub issue #615 (toasts hidden behind consent banner)
- /Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-613-615.md — original job briefing
- The worktree also contains the implementing spec: _bmad-output/implementation-artifacts/spec-613-615-bug-hunt-ux-fallout.md

--- REVIEW GUARDS (from the Perkins briefing; treat as binding spec) ---
- #613 scope is LABEL AND USER-FACING COPY ONLY: DB enum stays `viewed`; refcheck trigger logic untouched; `vacancy.viewed_at` untouched; internal/log/migration identifiers keep `viewed`. A stray USER-FACING "Viewed" status label surviving anywhere = a blocker.
- ONE user-facing term everywhere: "Viewing held" (stepper stop, backward-confirm modal, audit trail, shared pill, detail-page pill).
- #615: the consent banner must remain visible AND clickable at all times; `consent.js` untouched. Toast visibility DURING the consent window must be proven by the in-repo evidence artifact (DOM geometry + screenshots + clickability, desktop/mobile/degenerate).
- The degenerate-corner trade-off (320x480 + expanded customize panel: toast chosen over never-covering-banner THERE ONLY) is a documented, user-flagged decision — verify documentation accuracy, do NOT re-litigate the trade-off.
- No em dashes in any user-facing copy.
- Scope: the two fixes only. BASE = develop (includes merged #607/#610/#612/#616); carry-forward only.

--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

--- OUTPUT ---
Write ONE valid JSON array to this EXACT absolute path (do not derive or guess any other path):
/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-613-615/r1/acceptance.json

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

Output contract: the file must contain ONLY the JSON array — no prose, no markdown fencing, no preamble. Empty array `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota. After writing the file, print "LENS COMPLETE: acceptance" and stop.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
