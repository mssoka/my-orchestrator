You are the SECURITY reviewer ("mega-minion") for a pull request review team (Perkins round 1, job righttenantry-form-save-resume-f3, PR #563, "feat: application save-and-resume (F3) + reminder continue-link"). You have READ-ONLY access to the repository checkout at /Users/moses/.herdr/worktrees/RightTenantry/perkins-form-save-resume-f3-r1 (a detached worktree at exactly the reviewed sha d99a67374f29e2857b36be4caf05b16ecbf8df0e). Use it to verify claims against the actual code. Do not modify any repo file.

--- THE DIFF (your chunk) ---
Read the full diff chunk first: /Users/moses/code/_bmad-output/perkins/righttenantry-form-save-resume-f3/r1/chunk3.patch (1026 lines, 8 files — read ALL of it, in chunks if needed). Review these exact bytes. The full PR diff (4359 lines, 42 files) exceeded the big-diff threshold and was split into 3 chunks by directory; you are reviewing chunk 3 of 3, which covers `server/test/` — unit and integration tests (draft integration suite, middleware, csrf, email client, form pages/view tests). Files outside your chunk exist in the worktree — read them freely for context, but anchor findings in your chunk where possible.

--- PROJECT CONVENTIONS ---
Read AGENTS.md at the worktree root — its rules are binding review criteria (Gleam/Lustre monorepo; Squirrel-generated SQL only; no JavaScript FFI; no `let assert` outside tests; explicit HTTP timeouts on outbound calls; brand-voice copy in form_copy.gleam/copy.gleam; expand-only migrations; audit-on-state-change and /apply consent capture are defended invariants).

--- SPEC / CONTEXT (read ALL of these) ---
1. Original job briefing: /Users/moses/code/_bmad-output/briefings/righttenantry-form-save-resume-f3.md — the mission contract. Requirements 1–5 (draft persistence, magic continue link, expiry + erasure, no documents in drafts, E2 reminder seam), the Seams list, and the Acceptance block are the heart.
2. Spec of record: _bmad-output/planning-artifacts/problem-solving-application-form-completion-2026-07-31.md in the worktree — the Generated Solutions table (F3 row), Solution Analysis, Recommended Solution (Wave 1 build pack), Risk Mitigation (especially the draft data-protection row), and the E2 reminder row.
3. The implementing minion's own spec, committed in this PR: _bmad-output/implementation-artifacts/spec-form-save-resume-f3.md (readable in the worktree). Secondary context — docs 1 and 2 are the contract.

--- ROUND-1 CONTEXT (established — do NOT report these as findings) ---
- Drafts carry FIELD VALUES ONLY by design — "no documents in drafts" is spec requirement 4, not a gap.
- The migration having been applied only to a local Docker test DB is per project policy (the deploy chain applies migrations on merge to staging/prod) — not a finding.
- The stepper seam (the `rt:form-step-changed` custom event) is the sanctioned save trigger documented by the merged F1 stepper PR — not an undocumented coupling.

--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

This diff adds a tokenized magic continue-link (draft resume) and a draft persistence table — token entropy, token storage (hashed vs plaintext), link single-use/expiry semantics, cross-account draft access, and PII handling in drafts are first-class concerns here.

--- OUTPUT ---
When your review is complete:
1. Use the Write tool to write ONE valid JSON array to EXACTLY this absolute path:
   /Users/moses/code/_bmad-output/perkins/righttenantry-form-save-resume-f3/r1/security-c3.json
   Each element must match this schema exactly:
   {
     "source": "security",
     "severity": "blocker" | "warning" | "note",
     "category": "<short tag>",
     "title": "<one-line summary>",
     "location": "<file:line | file:hunk | N/A>",
     "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
     "detail": "<why this is a problem, ≤40 words>",
     "recommended_fix": "<the change to apply, ≤40 words>"
   }
   - Write ONLY the JSON array to the file. No prose, no markdown fencing, no preamble.
   - Empty array `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota.
2. Then reply with one short line ("done — N findings written") and STOP. No further work.

ACCURACY MANDATE — this is the most important instruction in this brief:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
