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
/Users/moses/code/_bmad-output/perkins/righttenantry-guarantor-autofill-fix/r1/edge.json
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

--- YOUR LENS: EDGE CASE HUNTER ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.
Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.
For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.
Focus extra scrutiny on: the bracket-name normalization (`inner_field_name`, `string.split(name, "][")` with `string.drop_end`), the suffix-rule ordering in `autocomplete_for_suffix`, the `co_applicant[` + `_phone]` guard, and any field name in the actual form sections that produces a wrong token (check server/src/application/form_sections/*.gleam and form_fields.gleam callers).
