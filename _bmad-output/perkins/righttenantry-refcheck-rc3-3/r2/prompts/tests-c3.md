You are reviewing a code diff. You have read-only access to the repository checkout at:
/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-3-r2
You may (and MUST) verify the diff's claims against the actual codebase using your tools. Read files under that path only. Do not modify anything.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-3-r2/AGENTS.md for the project standards (no let assert, explicit httpc timeouts, Squirrel SQL, copy voice, etc.).

--- DIFF (review exactly these bytes; the full PR diff was chunked by file group - this is chunk c3 of 4) ---
Read the diff file: /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-3/r2/diff-c3.patch
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
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing in the worktree). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80-89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- New/modified API endpoints without matching coverage
- Auth/authz paths missing negative tests
- Happy-path-only coverage where error handling is implied
- New DB operations without integration coverage
- New state transitions without boundary tests
- TAUTOLOGICAL tests: tests that cannot fail, assert on their own fixtures, or duplicate the implementation rather than pin behavior (critical in a fix-rework where new tests were added to close coverage findings)

Test level mix (unit/integration/E2E): flag mismatches as findings.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS -> note, CONCERNS -> warning, FAIL -> blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds:
- PASS: P0 100%, P1 >=90%, overall >=80%
- CONCERNS: P0 100%, P1 80-89%, overall >=80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "tests",
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
/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-3/r2/tests-c3.json
Then stop. Do not write anywhere else.