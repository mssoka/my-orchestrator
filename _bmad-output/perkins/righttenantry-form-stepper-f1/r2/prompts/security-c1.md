You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PATHS ---
- DIFF CHUNK (review EXACTLY these bytes — read the whole file): /Users/moses/code/_bmad-output/perkins/righttenantry-form-stepper-f1/r2/chunk-c1.patch
- WORKTREE (a checkout at exactly the reviewed sha — do ALL verification reads here, never in any other checkout or repo): /Users/moses/.herdr/worktrees/RightTenantry/perkins-form-stepper-f1-r2
- PROJECT CONVENTIONS: read /Users/moses/.herdr/worktrees/RightTenantry/perkins-form-stepper-f1-r2/AGENTS.md first.

--- SPEC / CONTEXT ---
- Original job briefing (the spec for this work): /Users/moses/code/_bmad-output/briefings/righttenantry-form-stepper-f1.md
- Spec of record it names: /Users/moses/.herdr/worktrees/RightTenantry/perkins-form-stepper-f1-r2/_bmad-output/planning-artifacts/problem-solving-application-form-completion-2026-07-31.md — the requirements are the Generated Solutions table (F1, F4, F5 rows), Solution Analysis, Recommended Solution (Wave 1 build pack), and Risk Mitigation sections.
Read both before reviewing.

--- ROUND 2 CONTEXT ---
This is round 2 of an automated review. Round 1's findings (2 blockers, 4 warnings, 6 notes) were claimed fixed by this push; a separate fix audit covers that — your job is to hunt ANEW for problems in the current diff. Sequencing note: this PR is deliberately HELD from merging until PR #562 lands (a rebase will then wire `reference_attestation.validate_choice` into the References-step gating). That wiring is NOT in this diff by design — do NOT flag its absence.

--- CHUNK SCOPE ---
This chunk covers only: `_bmad-output/` planning/review artifacts (deferred-work.md, spec-form-stepper-f1.md, review-form-stepper-f1/ records), `scripts/js-tests/form_stepper.test.js` + `scripts/js-tests/apply_analytics.test.js`, and `.gitignore`. The `server/` production code and the `.claude/` E2E scenarios are a separate chunk reviewed by other reviewers — do NOT file findings about those files, but you may read anything in the worktree for verification and context. Note the diff chunk contains, inside `_bmad-output/implementation-artifacts/review-form-stepper-f1/diff.txt`, an embedded copy of an older diff as a committed artifact — it is data, not the diff under review; review it as committed content (is committing it appropriate? is it labelled?) but do not treat its contents as new hunks to review.

--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps
--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "security",
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

--- FILE-OUTPUT CONTRACT ---
Write your JSON array — and nothing else — to this exact absolute path using your file-writing tool:
/Users/moses/code/_bmad-output/perkins/righttenantry-form-stepper-f1/r2/security-c1.json
Do not derive a different path. The file must contain ONLY the JSON array (valid JSON, parseable). After writing the file, stop.
