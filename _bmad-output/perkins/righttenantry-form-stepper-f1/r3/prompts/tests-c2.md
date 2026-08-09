You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PATHS ---
- DIFF CHUNK (review EXACTLY these bytes — read the whole file): /Users/moses/code/_bmad-output/perkins/righttenantry-form-stepper-f1/r3/chunk-c2.patch
- WORKTREE (a checkout at exactly the reviewed sha 8f2faf09ea84151d516fc44a2dea9686305627c6 — do ALL verification reads here, never in any other checkout or repo): /Users/moses/.herdr/worktrees/RightTenantry/perkins-form-stepper-f1-r3
- PROJECT CONVENTIONS: read /Users/moses/.herdr/worktrees/RightTenantry/perkins-form-stepper-f1-r3/AGENTS.md first.

--- SPEC / CONTEXT ---
- Original job briefing (the spec for this work): /Users/moses/code/_bmad-output/briefings/righttenantry-form-stepper-f1.md
- Spec of record it names: /Users/moses/.herdr/worktrees/RightTenantry/perkins-form-stepper-f1-r3/_bmad-output/planning-artifacts/problem-solving-application-form-completion-2026-07-31.md — the requirements are the Generated Solutions table (F1, F4, F5 rows), Solution Analysis, Recommended Solution (Wave 1 build pack), and Risk Mitigation sections.
Read both before reviewing.

--- ROUND 3 CONTEXT ---
This is round 3 of 3 (FINAL automated round) of an automated review. Round 2's findings (2 blockers, 5 warnings, 14 notes) were claimed fixed by this push; a separate fix audit covers that — your job is to hunt ANEW for problems in the current diff. Sequencing note from round 2 is now STALE: PR #562 has landed, this branch was rebased past it, and the RC1.2 attestation gating wiring (`reference_attestation.validate_choice` + the data-gating-message pattern) IS present in this diff and IS in scope for review.

--- CHUNK SCOPE ---
This chunk covers only: `server/` production code and tests (server/priv/static/form_stepper.js, form.css, form.js; server/src/application/** — situation.gleam, documents.gleam, work_income.gleam, reference_attestation.gleam, form_pages.gleam, form_view.gleam, copy.gleam, form_copy.gleam; server/test/application/**) and `.claude/skills/` E2E scenarios (form-bug-hunt SKILL.md + scenarios, bug-hunt landing scenarios). The `_bmad-output/` artifacts, `scripts/js-tests/`, and `.gitignore` are a separate chunk reviewed by other reviewers — do NOT file findings about those files, but you may read anything in the worktree for verification and context.

--- YOUR LENS ---
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

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "tests",
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
/Users/moses/code/_bmad-output/perkins/righttenantry-form-stepper-f1/r3/tests-c2.json
Do not derive a different path. The file must contain ONLY the JSON array (valid JSON, parseable). After writing the file, stop.
