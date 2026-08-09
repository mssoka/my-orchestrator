You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PATHS ---
- DIFF CHUNK (review EXACTLY these bytes — read the whole file): /Users/moses/code/_bmad-output/perkins/righttenantry-form-copy-revision/r1/chunk-c3.patch
- WORKTREE (a checkout at exactly the reviewed sha — do ALL verification reads here, never in any other checkout or repo): /Users/moses/.herdr/worktrees/RightTenantry/perkins-form-copy-revision-r1
- PROJECT CONVENTIONS: read /Users/moses/.herdr/worktrees/RightTenantry/perkins-form-copy-revision-r1/AGENTS.md first.

--- SPEC / CONTEXT ---
- Original job briefing (the spec for this work): /Users/moses/code/_bmad-output/briefings/righttenantry-form-copy-revision.md
Read it before reviewing.

--- REVIEW CONTEXT (read carefully — false-positive guardrails) ---
This PR is a user-ruled COPY REVISION, not a feature change. The user supplied the new wording VERBATIM and ordered a GLOBAL ban on em-dashes in user-facing copy. Concretely:
- ALL user-facing copy in this diff is VERBATIM USER RULING — do NOT flag the wording, tone, phrasing, or style of the copy itself as a bug. The mission was "replace with EXACT copy".
- The em-dash ban is absolute and user-ordered. ZERO `\u2014`/`&mdash;` hits in user-facing copy IS the acceptance criterion — its absence is not a gap. The `no_em_dash_test` CI guard is a regression guard, not overkill.
- The en-dash in "Equal Status Acts 2000\u20132018" is a date range (NOT an em-dash) and is correctly kept — not a finding.
- The no-JS trade-off (checklist item 6's save-resume copy is JS-enhanced and hidden without JS) is user-accepted and disclosed in the PR body — not a finding.
- Code comments and non-user-facing strings retaining dashes are fine — the ban covers user-facing copy only.
What IS in scope: copy inconsistencies (one surface updated, another missed), broken code/references introduced by the edits, missed acceptance items, test breakage, em-dashes remaining in user-facing strings, or regressions the copy edits could introduce (e.g. string-splitting bugs in JS, Gleam compile issues, punctuation breaking HTML/URLs).

--- CHUNK SCOPE ---
This chunk covers only these files:
.pi/skills/form-bug-hunt/scenarios/stepper/stepper-happy-path.yaml
.pi/skills/form-bug-hunt/scenarios/validation/has-pets-missing-answer.yaml
.pi/skills/form-bug-hunt/scenarios/validation/listing-source-tamper.yaml
.pi/skills/form-bug-hunt/scenarios/validation/missing-guarantor-when-first-time-renter.yaml
.pi/skills/form-bug-hunt/scenarios/validation/missing-guarantor-when-student.yaml
.pi/skills/form-bug-hunt/scenarios/validation/missing-guarantor-when-unemployed.yaml
.pi/skills/form-bug-hunt/scenarios/validation/unticked-consent.yaml
_bmad-output/implementation-artifacts/spec-form-copy-revision.md
scripts/js-tests/form_draft.test.js
scripts/js-tests/form_draft_wiring.test.js
server/priv/static/form_draft.js
server/priv/static/form_stepper.js
server/priv/static/llms.txt
server/test/ai/audit_report_test.gleam
server/test/ai/contract_v4_test.gleam
server/test/ai/evidence_humanize_test.gleam
server/test/application/error_summary_test.gleam
server/test/application/form_pages_test.gleam
server/test/application/form_view_test.gleam
server/test/application/reference_attestation_test.gleam
server/test/copy_test.gleam
server/test/legal/legal_test.gleam
server/test/notification/email_client_test.gleam
server/test/response_helpers_test.gleam

The rest of the diff is split across other chunks reviewed by other reviewers — do NOT file findings about files outside this list (but you may read anything in the worktree for verification and context).

--- YOUR LENS ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "architecture",
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
/Users/moses/code/_bmad-output/perkins/righttenantry-form-copy-revision/r1/architecture-c3.json
Do not derive a different path. The file must contain ONLY the JSON array (valid JSON, parseable). After writing the file, stop.