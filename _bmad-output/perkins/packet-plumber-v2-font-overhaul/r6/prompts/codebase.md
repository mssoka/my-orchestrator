You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read the project conventions at /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-font-overhaul-r6/project-context.md before reviewing. Your cwd IS the reviewed worktree — a detached checkout at exactly the reviewed sha 4688d3df4397dc35bd986c16513475fe197b97df. Every verification read happens there. Do not run builds or the full test suite (the orchestrator owns those); small greps/reads are your tools.

--- DIFF ---
The canonical diff is at /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-font-overhaul/r6/diff.patch (unified format, 3236 lines, 98 files — many are 2-3-line binary markers for re-blessed goldens/fonts/captures). Read it IN FULL first (use offset/limit reads to page through it) and review exactly those bytes. NEVER re-fetch or regenerate the diff (no git diff, no gh pr diff, no fetching origin).

--- SPEC / CONTEXT ---
The spec is the original job briefing: /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-font-overhaul.md — read it. There is no GitHub issue; the briefing IS the spec.

--- ROUND CONTEXT (orchestrator-supplied) ---
This is a RE-REVIEW (round 6) of a REBASED head. Round 5 APPROVED the same branch pre-rebase (@3e62101); the base branch v2 then moved (#89/#90 merged) and this branch was rebased onto it, conflict-only. The diff you review is vs the NEW base. Highest-value findings: DELTA-INTRODUCED regressions from the rebase's conflict resolution — hunt hunks where this branch's changes meet upstream-moved code (prime suspects: app/main.odin main loop, tools/ci-local.sh, harness/overlay.odin). The orchestrator owns the prior-round fix-audit — do not try to classify prior findings; report freshly what THIS diff and code show.

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
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
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

--- FILE-OUTPUT CONTRACT (pane-world) ---
Write your ONE JSON array using the Write tool to EXACTLY this absolute path: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-font-overhaul/r6/codebase.json
Only the JSON array — no prose, no markdown fencing, no preamble. Then STOP (one short chat confirmation line is enough).
