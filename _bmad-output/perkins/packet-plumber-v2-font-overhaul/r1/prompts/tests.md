SHARED BLOCK (given to every lens EXCEPT blind — blind gets its own file)

You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- INPUTS (absolute paths) ---
- DIFF: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-font-overhaul/r1/diff.patch
  (the canonical diff under review — 152 files, 129 KB; read it with offset/limit in chunks; every hunk matters but the 111 goldens/*.png + 13 docs/captures/*.png + 4 assets/fonts/*.ttf entries are binary one-liners)
- WORKTREE (the checkout at exactly the reviewed sha — every verification read happens here): /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-font-overhaul-r1
- PROJECT CONVENTIONS: /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-font-overhaul-r1/project-context.md
- SPEC / CONTEXT (review_mode = full):
  1. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-font-overhaul/r1/spec/job-briefing.md (the job briefing — the spec)
  2. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-font-overhaul/r1/spec/perkins-briefing-r1.md (the round briefing — its 'Lens-guards' section is part of the spec: the hard blocker bar + the user rulings on what NOT to re-litigate)

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this path (create parent dirs if needed; write the file, do not print the JSON into chat):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-font-overhaul/r1/tests.json

Each element must match this schema exactly:
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
- The file contains ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, STOP. Do not fix anything. Do not push. You are a reviewer.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

--- YOUR LENS (tests) ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing in the worktree). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- The new merged-atlas font loader (font_merge_fallback / font_from_glyphs / load_fonts) — what pins it?
- The fail-loudly guards in app/main.odin + harness/goldens.odin — is the refusal path itself tested/reachable?
- The PP_DEBUG tooling (gallery mode, font-check verb) — compile gate only, or behavioural pins?
- Happy-path-only coverage where error handling is implied
- Test level mix (unit/integration/E2E): flag mismatches as findings.

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
