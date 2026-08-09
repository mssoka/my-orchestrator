You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any repository files — the only file you may write is your output file, named at the end.

--- PROJECT CONVENTIONS ---
The project conventions live in AGENTS.md at the root of the worktree:
/Users/moses/.herdr/worktrees/RightTenantry/perkins-self-employed-sweep-r2/AGENTS.md
Read it first and treat it as the binding conventions.

--- DIFF ---
The canonical diff under review is at exactly this path:
/Users/moses/code/_bmad-output/perkins/righttenantry-self-employed-sweep/r2/diff.patch
Read it in full. Review exactly these bytes — never re-fetch or regenerate the diff.

--- WORKTREE ---
/Users/moses/.herdr/worktrees/RightTenantry/perkins-self-employed-sweep-r2
A detached checkout at exactly the reviewed sha. Every verification read happens here.

--- SPEC / CONTEXT ---
- /Users/moses/code/_bmad-output/briefings/righttenantry-self-employed-sweep.md — the original job briefing (the spec). Its Mission items 1-4 and Acceptance section are the contract; the PR also folds in the "W1 error-path" item from PR #573's review (user ruled 'reword + fold'), which is why the employer-trio validation messages changed too.
- /Users/moses/code/_bmad-output/briefings/righttenantry-self-employed-copy-fix.md — the #573 briefing this PR amends (named context: the scoped invite sentence deliberately amends #573's sentence).

ROUND-2 BINDING CONTEXT (round 1 of 3 done; this is the re-review round after the r1 fix commit 55ee07f, which is IN this diff):
- ALL copy in this PR is verbatim user ruling (slot label 'Employer / business reference', helper amendment, scoped invite sentence, error-path reword, count-cap message) — do NOT flag wording as bugs.
- The 'Employer / business name' label is a LABEL-ONLY change by design: the scorer keys on the field NAME (unchanged). A scorer-visible label change WOULD be a finding.
- The referee-slot question-set path incoherence was deliberately EXCLUDED by the briefing (separate track, ruling pending) — do not report it.
- The audit-PDF label split and the landlord .typ checklist are disclosed in the PR's open questions.
- Commit 55ee07f regenerated the committed tenant-vetting-checklist.pdf (binary hunk) and swept the count-cap rejection message.

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
  "category": "<short tag>",
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
/Users/moses/code/_bmad-output/perkins/righttenantry-self-employed-sweep/r2/codebase.json
Then stop. Do not do anything else.
