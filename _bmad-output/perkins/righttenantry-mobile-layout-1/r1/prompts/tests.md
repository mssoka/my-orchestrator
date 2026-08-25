You are reviewing a code diff in the RightTenantry repo. You have read-only access to the repository worktree and may verify the diff's claims against the actual codebase using your tools. Do NOT modify, build, or write any repo file.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/RightTenantry/perkins-mobile-layout-1-r1/AGENTS.md for project conventions.

--- DIFF ---
The canonical diff is at /Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r1/diff.patch - read it fully with the read tool. Review exactly these bytes; do not re-generate or re-fetch the diff.

--- WORKTREE (verification) ---
/Users/moses/.herdr/worktrees/RightTenantry/perkins-mobile-layout-1-r1 is a checkout at exactly the reviewed state. Every verification read happens here.

--- SPEC / CONTEXT ---
Read both:
- /Users/moses/code/_bmad-output/briefings/righttenantry-mobile-layout-1.md (original job spec: 5 mobile UX fixes + acceptance criteria)
- /Users/moses/code/_bmad-output/briefings/perkins-righttenantry-mobile-layout-1-r1.md (reviewer briefing; the "Lens-guards" section names what each fix must satisfy)

--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80-89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- New/modified behaviour without matching coverage
- Happy-path-only coverage where error handling is implied
- New state transitions without boundary tests

Per the reviewer briefing, the 8 test pins to verify exist and actually exercise the claim: navigation/resolver for both entity types (vacancy + application), stepper layout, compare padding, demo touch target. The notification deep-link contract REQUIRES a navigation test (click -> route) for BOTH entity types - absence of either is a blocker.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS -> note, CONCERNS -> warning, FAIL -> blocker
- detail: rationale with coverage observations
- recommended_fix: what would raise the gate

--- OUTPUT ---
Write ONE valid JSON array (nothing else in the file) to this EXACT path: /Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r1/tests.json
Each element must match this schema exactly:
{
  "source": ""tests"",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract:
- The file must contain ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, STOP. Reply with one line: "wrote tests.json".

ACCURACY MANDATE - this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY - they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination - drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume - an empty array is a fine and honest answer when nothing is wrong.