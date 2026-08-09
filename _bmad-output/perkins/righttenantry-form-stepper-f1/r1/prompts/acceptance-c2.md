You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PATHS ---
- DIFF CHUNK (review EXACTLY these bytes — read the whole file): /Users/moses/code/_bmad-output/perkins/righttenantry-form-stepper-f1/r1/chunk-c2.patch
- WORKTREE (a checkout at exactly the reviewed sha — do ALL verification reads here, never in any other checkout or repo): /Users/moses/.herdr/worktrees/RightTenantry/perkins-form-stepper-f1-r1
- PROJECT CONVENTIONS: read /Users/moses/.herdr/worktrees/RightTenantry/perkins-form-stepper-f1-r1/AGENTS.md first.

--- SPEC / CONTEXT ---
- Original job briefing (the spec for this work): /Users/moses/code/_bmad-output/briefings/righttenantry-form-stepper-f1.md
- Spec of record it names: /Users/moses/.herdr/worktrees/RightTenantry/perkins-form-stepper-f1-r1/_bmad-output/planning-artifacts/problem-solving-application-form-completion-2026-07-31.md — the requirements are the Generated Solutions table (F1, F4, F5 rows), Solution Analysis, Recommended Solution (Wave 1 build pack), and Risk Mitigation sections.
Read both before reviewing.

--- CHUNK SCOPE ---
This chunk covers only the `server/` production code: `server/priv/static/form_stepper.js` (new static JS stepper), `server/priv/static/form.css` additions, the Gleam SSR changes (`form_view.gleam`, `form_pages.gleam`, `form_sections/{documents,situation,work_income}.gleam`, `copy.gleam`), and the Gleam test changes. The `_bmad-output/` artifacts, `scripts/js-tests/`, and `.gitignore` are a separate chunk reviewed by other reviewers — do NOT file findings about those files. Key context files for verification in the worktree: `server/priv/static/form.js` (condition engine, preflight), `server/priv/static/apply_analytics.js` (W0 funnel contract — must stay untouched and keep firing), `server/src/application/error_summary.gleam` (anchor contract), `server/src/application/form_fields.gleam` (field id conventions).

--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

Reminder of the acceptance criteria from the briefing (verify each against this chunk):
- Stepper works end-to-end on mobile + desktop; no-JS fallback still submits the full form; `application_form_section_*` events still fire with unchanged section ids; scoring inputs unchanged (diff-verifiable); F4/F5 copy in place.
- Named progress ("Step 3 of 8 — Work & Income"), sticky progress on mobile, built on the existing data-condition engine, SINGLE POST at the end (no per-section round-trips).
- F4: defer non-scoring optional fields (listing_source → post-submit or drop); collapse the optional address cluster. ALL scoring inputs untouched — do not remove, rename, or re-require any field the scorer reads. Check what the scorer actually reads (search the worktree, e.g. server/src/ai, for eircode/current_address/listing_source usage) before judging.
- F5: camera-roll-friendly copy at the document slots; per-slot "what counts as this letter" helper text.
- Seams: stable data-section-ids kept intact; the F3-SEAM comment and the one-visit line in form_view.view_prep_block left untouched; apply_analytics.js untouched (W0 funnel contract).
- Follow-up C (save-resume) must NOT be built here — flag any scope drift into draft persistence; seams for it (e.g. the step-changed event) should exist.
- SSR no-JS fallback remains the current single long form (hard risk-mitigation requirement — verify it).
- In-app copy voice (AGENTS.md): no raw error strings, contractions, calm confidence — judge the new copy.gleam strings against it.

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
/Users/moses/code/_bmad-output/perkins/righttenantry-form-stepper-f1/r1/acceptance-c2.json
Do not derive a different path. The file must contain ONLY the JSON array (valid JSON, parseable). After writing the file, stop.
