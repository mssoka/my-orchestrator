You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Your cwd IS the reviewed worktree — verify everything here, never elsewhere.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-blender-silhouettes-r2/project-context.md (the in-repo conventions doc) first.

--- DIFF ---
Read the canonical diff (these exact bytes): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-blender-silhouettes/r2/diff.patch
(936 lines; the _pr_body.md hunks are PR-description prose — reviewable for claims-vs-code consistency but not code.)

--- SPEC / CONTEXT ---
Read BOTH spec docs:
1. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-blender-silhouettes/r2/spec-briefing.md — the job briefing (THE spec for this PR)
2. /Users/moses/code/_bmad-output/implementation-artifacts/packet-plumber-v2-design-audit/kyle-design-directions.md — design source of truth (§3 Node Identifiability, §1 Scale)

Round-2 context (do not let it bias you, just scope): this is a fix-audit round after r1 (2 blockers + 6 warnings, all claimed folded). STAGE-1 intent: spec + pipeline only — PNGs intentionally unchanged (re-render + T2 re-bless land later with the user's Blender pass); the branch merges LAST. Fresh findings on the fix delta are expected and welcome.

--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80-89% OR P2 gap
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
- severity: PASS -> note, CONCERNS -> warning, FAIL -> blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds:
- PASS: P0 100%, P1 >=90%, overall >=80%
- CONCERNS: P0 100%, P1 80-89%, overall >=80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%

NOTE for this repo: CI is Blenderless (tools/lint.sh gates + odin test); gen_sprites.py runs only where Blender exists. Coverage claims must respect that constraint. Use source "tests" in every element.

--- OUTPUT ---
Write ONLY your JSON array (no prose, no markdown fencing) to this exact absolute path with your file tools:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-blender-silhouettes/r2/tests.json
Then stop. Do not derive or substitute the path — use it verbatim.

Each element must match this schema exactly:
{
  "source": "<assigned>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use N/A ONLY for findings that have no possible code reference. Do not paraphrase. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, less than 40 words>",
  "recommended_fix": "<the change to apply, less than 40 words>"
}

Output contract:
- ONLY the JSON array in that file, valid JSON, parseable by json.load.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. An empty array is a fine and honest answer when nothing is wrong.
