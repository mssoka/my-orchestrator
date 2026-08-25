You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- INPUTS (absolute paths) ---
- DIFF: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/diff.patch
  (the canonical diff under review — 18 files, 2435 lines; the docs/captures/*.png entries are binary one-liners; read it whole)
- WORKTREE (the checkout at exactly the reviewed sha 9094f45 — every verification read happens here): /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-camera-zoom-r3
- PROJECT CONVENTIONS: /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-camera-zoom-r3/project-context.md
- SPEC / CONTEXT (review_mode = full):
  1. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/spec/job-briefing.md (the job briefing — the spec; there is NO GitHub issue for this job)
  2. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/spec/perkins-briefing-r3.md (the round briefing — its 'Lens-guards' section is part of the spec: the fix-audit targets + the user rulings on what NOT to re-litigate)

--- YOUR LENS (source tag: tests) ---

Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- New/modified API endpoints without matching coverage
- Happy-path-only coverage where error handling is implied
- New state transitions without boundary tests

Test level mix (unit/integration/E2E): flag mismatches as findings.

Round context (round 3, fix commit 9094f45). The r2 review's B2/B3 claimed the composition layer was unpinned; this diff adds: camera_test.odin (9 pins — spawn/seed classification, pullback target, off-center floor, noc_panel_hit, wheel policy, zoom step, anchor, pan center, clamp), camera_input_test.odin (7 pins — wheel chain, empty-ground pan, plain-click, draw-no-pan, two-finger deltas, wheel accumulator, latch lifecycle), pullback_test.odin (7 pins — seed trigger, router-skipped walk, 7 yield clears, wheel-policy composition, attach ignore, toggle/in-view, ease/convergence), settings_test.odin (v2 byte round-trip + the mixed-corruption fallbacks). Audit those pins' SUBSTANCE:

- NON-VACUOUS: would each pin FAIL if the pinned behavior regressed? (r2's N3 found a vacuous assertion — check the new pins for the same disease: assertions that can't fail, wrong fixture numbers, comments contradicting the math.)
- The off-center floor pin (B1's fold): check its fixture against the real clamp math — cy=585 at zoom 2.0 with fit=720/780, world 780 high: is 585 truly the bottom clamp ([195,585])? Does the test assert the B1 failure mode (district inclusion at convergence) or just the center pin?
- UNTESTED REGRESSION SURFACE of the fix itself: poll_mouse's wheel accumulation is driven through wheel_accumulate pure pins only — the poll path itself (the `w != 0` gate, residue persistence in Input) is untested (raylib state — acceptable? classify honestly); the cam-e2e block in main.odin is manual-only; effect_pan's live-zoom clamp vs target-zoom convergence (W5 fold) has no mid-ease test; camera_newest_terminals has NO direct unit pin (only the feed-level walk test with ONE interleaved router — what about 0 found, >8 spawns, dead terminals?); the settings v1→v2 migration path (a real v1 6-byte file loading with pullback ON) — is there a v1-format test?
- The PR body's test-count table vs the actual files — count the @(test) procs in the four test files in the worktree and reconcile with the claimed counts.

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
Write ONE valid JSON array to EXACTLY this path (create parent dirs if needed; write the file, do not print the JSON into chat):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom/r3/tests.json

Each element must match this schema exactly:
{
  "source": "tests",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
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
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is an fine and honest answer when nothing is wrong.
