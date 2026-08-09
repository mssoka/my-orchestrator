You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS (condensed from the repo AGENTS.md) ---
- Gleam monorepo: shared/ (types+codecs), client/ (Lustre SPA), server/ (Wisp/Mist SSR API). This diff is server-side SSR application-form rendering.
- No JavaScript FFI. No `let assert` in production code (use `case`). All fallible ops return Result. Prefer pipelines and `use`.
- No technical debt: no placeholders, TODOs, or "cleanup later" comments. Implement completely or defer entirely.
- No hardcoded data: all UI data from DB via API endpoints (exceptions: labels, route paths, CSS, defaults).
- Module organization: public view first, helpers last; target <200 lines logic modules.
- Tests: gleeunit/unitest; integration tests tagged "integration"; every interactive element gets data-testid.
- New feature workflow: SQL file -> run_squirrel.sh -> API endpoint -> client fetch. This diff touches NO SQL (no squirrel run needed).
- Defended invariants: audit-log on state change, CSRF, free-tier counter, session forgery resistance, Stripe webhook validity, /apply consent capture.
- Before merging: make format && make test && make build; CI also runs integration tests with a Postgres 16 container.
- In-app copy voice: never expose raw error strings; "Couldn't" not "Failed".

--- DIFF ---
The canonical diff to review is at:
/Users/moses/code/_bmad-output/perkins/righttenantry-guarantor-autofill-fix/r1/diff.patch
Read it in full. Review exactly these bytes. Do not re-fetch or regenerate the diff.

--- SPEC / CONTEXT ---
Your spec for the acceptance audit and the original mission context:
1. Original job briefing: /Users/moses/code/_bmad-output/briefings/righttenantry-guarantor-autofill-fix.md (the user-reported bug + requirements + acceptance criteria)
2. PR body (root cause, decisions, verification table): /Users/moses/code/_bmad-output/perkins/righttenantry-guarantor-autofill-fix/r1/pr-body.json
3. The spec artifact added by the diff itself: _bmad-output/implementation-artifacts/spec-guarantor-autofill-fix.md (inside the diff)
The worktree checkout at exactly the reviewed state is:
/Users/moses/.herdr/worktrees/RightTenantry/perkins-guarantor-autofill-fix-r1
Verify claims by reading files there (the diff may be verified against these files).

Context you may rely on (already verified by the orchestrator, do not re-litigate):
- This PR fixes a browser-autofill bug on the public application form: fields now carry WHATWG autocomplete tokens. Do not flag the *choice of wording/copy* as a bug.
- The Chromium 9-fields-per-type fill cap (kTypeValueFormFillingLimit) is a real browser limit; tel and tel-national resolve to different FieldTypes in Chromium (PHONE_HOME_WHOLE_NUMBER vs PHONE_HOME_NATIONAL_NUMBER), so they count as separate buckets. The PR's cap math is not itself a defect.
- The PR discloses that guarantor name/email remain subject to the Chromium cap in Chrome (10th NAME_FULL / 11th EMAIL instance) — that disclosure exists in the PR body; whether it conflicts with the spec's acceptance criteria is a legitimate thing to check.

--- OUTPUT ---
Write ONE valid JSON array to this exact absolute path, then stop:
/Users/moses/code/_bmad-output/perkins/righttenantry-guarantor-autofill-fix/r1/tests.json
- The file must contain ONLY the JSON array. No prose, no markdown fencing, no preamble, no trailing explanation.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- If you emit findings, the file must be valid JSON — validate it yourself before finishing (e.g. python3 -m json.tool or a JSON parse).

ACCURACY MANDATE — the most important instruction in this prompt:
NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.
Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read (verbatim). If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

--- YOUR LENS: TEST COVERAGE ---
Test coverage analysis via traceability.
For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap
Blind-spot heuristics to check:
- New/modified API endpoints without matching coverage
- Auth/authz paths missing negative tests
- Happy-path-only coverage where error handling is implied
- New DB operations without integration coverage
- New state transitions without boundary tests
Test level mix (unit/integration/E2E): flag mismatches as findings.
Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate
Gate thresholds:
- PASS: P0 100%, P1 ≥90%, overall ≥80%
- CONCERNS: P0 100%, P1 80–89%, overall ≥80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%
For this diff: the changed behaviour is the autocomplete_for mapping (exact table, suffix rules, bracket normalization, tel-national split) and the rendered attribute. Check whether every mapping branch and every field name used by the real form sections is pinned by a test, and whether the conditional show/hide regression is covered (guarantor hidden/visible).
