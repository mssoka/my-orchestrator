You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Your cwd IS the reviewed worktree — verify everything here, never elsewhere.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-blender-silhouettes-r2/project-context.md (the in-repo conventions doc) first.

--- DIFF ---
Read the canonical diff (these exact bytes): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-blender-silhouettes/r2/diff.patch
(936 lines; the _pr_body.md hunks are PR-description prose — reviewable for claims-vs-code consistency but not code.)

--- SPEC / CONTEXT ---
Read BOTH spec docs:
1. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-blender-silhouettes/r2/spec-briefing.md — the job briefing (THE spec for this PR)
2. /Users/moses/code/_bmad-output/implementation-artifacts/packet-plumber-v2-design-audit/kyle-design-directions.md — design source of truth (§3 Node Identifiability, §1 Scale)

Round-2 context (do not let it bias you, just scope): this is a fix-audit round after r1 (2 blockers + 6 warnings, all claimed folded). STAGE-1 intent: spec + pipeline only — PNGs intentionally unchanged (re-render + T2 re-bless land later with the user's Blender pass); the branch merges LAST. Fresh findings on the fix delta are expected and welcome.

--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in location.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in location.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

Use source "codebase" in every element.

--- OUTPUT ---
Write ONLY your JSON array (no prose, no markdown fencing) to this exact absolute path with your file tools:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-blender-silhouettes/r2/codebase.json
Then stop. Do not derive or substitute the path — use it verbatim.

Each element must match this schema exactly:
{
  "source": "<assigned>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use N/A ONLY for findings that have no possible code reference. Do not paraphrase. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, less than 40 words>",
  "recommended_fix": "<the change to apply, less than 40 words>"
}

Output contract:
- ONLY the JSON array in that file, valid JSON, parseable by json.load.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. An empty array is a fine and honest answer when nothing is wrong.
