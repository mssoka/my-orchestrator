You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any repository files — the only file you may write is your output file, named at the end.

--- PROJECT CONVENTIONS ---
The project conventions live in AGENTS.md at the root of the worktree:
/Users/moses/.herdr/worktrees/RightTenantry/perkins-self-employed-sweep-r1/AGENTS.md
Read it first and treat it as the binding conventions.

--- DIFF ---
The canonical diff under review is at exactly this path:
/Users/moses/code/_bmad-output/perkins/righttenantry-self-employed-sweep/r1/diff.patch
Read it in full. Review exactly these bytes — never re-fetch or regenerate the diff.

--- WORKTREE ---
/Users/moses/.herdr/worktrees/RightTenantry/perkins-self-employed-sweep-r1
A detached checkout at exactly the reviewed sha. Every verification read happens here.

--- SPEC / CONTEXT ---
- /Users/moses/code/_bmad-output/briefings/righttenantry-self-employed-sweep.md — the original job briefing (the spec). Its Mission items 1-4 and Acceptance section are the contract; the PR also folds in the "W1 error-path" item from PR #573's review (user ruled 'reword + fold'), which is why the employer-trio validation messages changed too.
- /Users/moses/code/_bmad-output/briefings/righttenantry-self-employed-copy-fix.md — the #573 briefing this PR amends (named context: the scoped invite sentence deliberately amends #573's sentence).

ROUND CONTEXT (binding):
- ALL copy in this PR is verbatim user ruling — the slot label "Employer / business reference", the helper amendment, the scoped invite sentence "A written reference from your employer, if you're working — or from a client, accountant, or business contact if you're self-employed.", and the error-path reword ("Your employer or business name, please." etc.). Do NOT flag any of these strings as wording/copy bugs; the exact wording is the spec.
- The scoped sentence intentionally amends the #573 form (user-approved amendment). Test pins asserting #573's old text (e.g. that "employer, if you" is absent) were updated deliberately — the substring is present in the scoped form.
- The refcheck referee QUESTION SETS (the employer-ref slot's structured questions) are fenced off as refcheck v1 design — do not report anything about them.
- The PR body's "Left untouched deliberately" FYI flags are disclosed for later user rulings, NOT missed instances — do not report them: the Section-4 contact-trio surfaces (references.gleam "Employer" group heading, situation.gleam "Employer contact name", and their error_summary "Employer contact — name/phone/email" labels), the audit PDF's guarantor_employer "Employer" line, the AI source tags "Stated employer" / "Employer letter", and the employment_requires_employer predicate name.
- The scorer field NAME (employer_name) is intentionally unchanged — this is a label-only change; the #573 briefing required verifying the scorer keys on the field id, not the label.
- Stored analyses keep the old "Employer name:" label on re-render — the PR body discloses this as cosmetic, historical-only, self-healing. Accepted trade-off, not a finding.

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

This diff is copy-only relabeling plus one display-label mapping function (display_label_for_key). Behavior changes are: validation message text, upload-slot labels, helper text, email/form/PDF copy, and the employer_name -> "Employer / business name" humanized label. Judge coverage against THAT risk profile — copy assertions exist for most surfaces; check which changed surfaces lack any assertion (e.g. the two .typ Typst templates, upload_required_message, co-applicant slot labels).

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

--- FILE OUTPUT CONTRACT ---
When done, write ONLY your JSON array (no prose, no markdown fencing) to exactly this path using the Write tool:
{out}/tests.json
Then stop. Do not do anything else.
