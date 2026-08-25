You are reviewing a code diff. You have read-only access to the repository checkout at:
/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-3-r2
You may (and MUST) verify the diff's claims against the actual codebase using your tools. Read files under that path only. Do not modify anything.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-3-r2/AGENTS.md for the project standards (no let assert, explicit httpc timeouts, Squirrel SQL, copy voice, etc.).

--- DIFF (review exactly these bytes; the full PR diff was chunked by file group - this is chunk c4 of 4) ---
Read the diff file: /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-3/r2/diff-c4.patch
Read it fully before reviewing.

--- SPEC / CONTEXT ---
Read these spec/context files (they define what this diff is meant to do):
1. /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-3/r2/briefing.md  (round-2 fix-audit briefing; the prior-round findings it lists are CLAIMED fixed - your job is NEW issues, not re-confirming fixes)
2. /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-3-r2/_bmad-output/implementation-artifacts/spec-rc3-3-referee-form-session-open-answer-autosave.md  (story spec)
3. /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-3-r2/_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md  (architecture: AD-3 route registration + capability token + resumable, AD-10 form_opened_at, AD-15 abuse, A2 draft_answers, A3 TTL)
4. /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-3-r2/_bmad-output/planning-artifacts/ux-reference-checking-v1-2026-07-29.md  (UX: section 6.5 landing + question tables, section 8.5 token-state pages)

--- CRITICAL LENS-GUARD (read before reviewing - prevents false positives) ---

This is server-side Gleam SSR code for a referee reference-check form - production code with paying users, NOT a prototype. RT-specific constraints:

- The security spine = registry completeness. The /reference/:token route is open/unauthenticated (capability-token auth, AD-3) handling referee PII. Any middleware registry that omits /reference/* (csrf validate/skip, redact_token_route, is_public_path, rate-limit, CSP) is a security hole. A missing /reference arm in such a registry is a BLOCKER, never a note.
- This is a FIX-AUDIT round: this diff is the rework that claims to fix a previous review round's findings. Scan it for NEW defects and regressions the rework introduced. Do NOT re-litigate design decisions the previous round accepted: capability-token-is-auth (no login is the design), the truthful-copy escape routes, the honeypot/timing silent-drop-with-fake-success abuse posture (AD-15, same as /apply).
- No em-dashes in user-facing copy (CI-guarded ban) - form copy, question text, token-state pages. A single em-dash in copy is a legitimate finding.
- SSR never requires JS - the per-question POST (PRG) is the first-class path; PUT (JS) is the enhancement. Do NOT flag "the JS path should be primary" - the no-JS PRG path is the spec. DO flag it if the no-JS POST path is broken.
- Do NOT flag the form as "no authentication" - the capability token IS the auth (AD-3).
- Do NOT flag the silent-drop-with-fake-success on honeypot/timing as deception - it is the documented abuse posture (AD-15).
- Do NOT flag the truthful/decline/escape-route copy as "missing features" - honest-first design is the spec.

--- YOUR LENS ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?
This is a fix-rework: also check the fixes did not introduce duplication or break module boundaries the original respected.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "architecture",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract:
- Write ONLY the JSON array to the output file named below. No prose, no markdown fencing, no preamble in the file.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE - this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY - they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination - drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. An empty array is a fine and honest answer when nothing is wrong.

--- OUTPUT FILE ---
Write ONLY the JSON array (no fencing, no prose) to this exact absolute path:
/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-3/r2/architecture-c4.json
Then stop. Do not write anywhere else.