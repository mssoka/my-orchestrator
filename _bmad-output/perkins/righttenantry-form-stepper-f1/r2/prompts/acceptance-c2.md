You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PATHS ---
- DIFF CHUNK (review EXACTLY these bytes — read the whole file): /Users/moses/code/_bmad-output/perkins/righttenantry-form-stepper-f1/r2/chunk-c2.patch
- WORKTREE (a checkout at exactly the reviewed sha — do ALL verification reads here, never in any other checkout or repo): /Users/moses/.herdr/worktrees/RightTenantry/perkins-form-stepper-f1-r2
- PROJECT CONVENTIONS: read /Users/moses/.herdr/worktrees/RightTenantry/perkins-form-stepper-f1-r2/AGENTS.md first.

--- SPEC / CONTEXT ---
- Original job briefing (the spec for this work): /Users/moses/code/_bmad-output/briefings/righttenantry-form-stepper-f1.md
- Spec of record it names: /Users/moses/.herdr/worktrees/RightTenantry/perkins-form-stepper-f1-r2/_bmad-output/planning-artifacts/problem-solving-application-form-completion-2026-07-31.md — the requirements are the Generated Solutions table (F1, F4, F5 rows), Solution Analysis, Recommended Solution (Wave 1 build pack), and Risk Mitigation sections.
Read both before reviewing.

--- ROUND 2 CONTEXT ---
This is round 2 of an automated review. Round 1's findings (2 blockers, 4 warnings, 6 notes) were claimed fixed by this push; a separate fix audit covers that — your job is to hunt ANEW for problems in the current diff. Sequencing note: this PR is deliberately HELD from merging until PR #562 lands (a rebase will then wire `reference_attestation.validate_choice` into the References-step gating). That wiring is NOT in this diff by design — do NOT flag its absence.

--- CHUNK SCOPE ---
This chunk covers only: the `server/` production code (`server/priv/static/form_stepper.js` static JS stepper, `form.js` preflight changes, `form.css` additions, the Gleam SSR changes under `server/src/application/`, and the Gleam tests) AND the `.claude/skills/{form-bug-hunt,bug-hunt}/` E2E skill + scenario changes (the round-1 rework that taught the harness `?stepper=off`, the `stepper: true` scenario key, `tamper_hidden_inputs`, and refreshed stale scenario content). The `_bmad-output/` artifacts, `scripts/js-tests/`, and `.gitignore` are a separate chunk reviewed by other reviewers — do NOT file findings about those files. Key context files for verification in the worktree: `server/priv/static/form.js` (condition engine, preflight), `server/priv/static/apply_analytics.js` (W0 funnel contract — must stay untouched and keep firing), `server/src/application/error_summary.gleam` (anchor contract), `server/src/application/form_fields.gleam` (field id conventions), `server/src/application/application_handler.gleam` (server-side validation the scenarios target).

--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).
Reminder of the acceptance criteria from the briefing (verify each against this chunk):
- `application_form_section_*` events still fire with unchanged section ids; scoring inputs unchanged (diff-verifiable); F4/F5 copy in place.
- `make test` green; new behavior covered (step navigation, validation gating per step, fallback path).
- Progressive enhancement: the form must still work end-to-end with JS disabled (SSR + server validation is the fallback).
- The `.claude/` scenario rework in this chunk is the round-1 fix for the broken E2E suite — audit whether the harness changes + scenario content now correctly exercise the form as it exists at this sha (stepper on and off).

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
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
/Users/moses/code/_bmad-output/perkins/righttenantry-form-stepper-f1/r2/acceptance-c2.json
Do not derive a different path. The file must contain ONLY the JSON array (valid JSON, parseable). After writing the file, stop.
