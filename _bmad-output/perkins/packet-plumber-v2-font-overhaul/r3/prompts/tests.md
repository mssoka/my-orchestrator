You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- INPUTS (absolute paths) ---
- DIFF: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-font-overhaul/r3/diff.patch
  (the canonical diff under review — 153 files, 2892 lines; read it with offset/limit in chunks; every hunk matters but the 111 goldens/*.png + 13 docs/captures/*.png + 8 assets/fonts/*.ttf entries are binary one-liners)
- WORKTREE (the checkout at exactly the reviewed sha abec50b — every verification read happens here; trust it, not origin/v2): /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-font-overhaul-r3
- PROJECT CONVENTIONS: /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-font-overhaul-r3/project-context.md
- SPEC / CONTEXT (review_mode = full):
  1. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-font-overhaul/r3/spec/job-briefing.md (the job briefing — the spec)
  2. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-font-overhaul/r3/spec/perkins-briefing-r3.md (the round briefing — its 'Lens-guards' section is part of the spec: what NOT to re-litigate + the round-3 fix-audit focus)

--- ROUND 3 (fix-audit re-review) CONTEXT ---
This is round 3 of a Perkins loop. Round 1 (review of sha 47ebd0f) returned CHANGES_REQUESTED
with 2 blockers (B1 fail-loud guard dead code — every font-load failure was coerced to
rl.GetFontDefault() before the guards, so the os.exit(2) refusals were unreachable and palcheck
had no guard at all; B2 the PR body carried the WRONG job's content) + 5 warnings (W1 screenshot
order, W2 glyph_probe over-read, W3 deleted-asset baseline, W4 duplicated replay loop, W5 zero
pixel coverage for the NOC mono surface) + 15 notes (N1-N15: stale specimen ladder, stale
comments, fg block leak, missing[8] cap, palette fallback drift, score/settings/NOC size
mismatches, gallery global, PP_SW_AUDIO build irreproducibility, gallery retry budget, ink_soft
wording, title-clearance watch, palcheck guard, debug-tooling smoke gap).

A round 2 ran but was SWEPT (the PR was rebased mid-review; its review never counted). Treat
round 1 as the only prior round.

The implementing minion claims ALL r1 findings folded in commit b4154c3 ("fix: Perkins r1 —
B1 fail-loud loader (report, never coerce), B2 PR body rewrite, + W1-W5, N1-N15"), which also
absorbed a rebase onto the settled head (PR #86's audio work; the PP_SW_AUDIO usage refactored
to a single seam — "17 wrappers, one when-block"). A further 3rd rebase (abec50b) absorbed
PR #88 (blender-sculpt): its sprite goldens taken --theirs + a combined-tree golden re-bless
in one pass; harness/palcheck.odin re-pinned for the sculpted sprites (re-measured tones,
floors re-pinned, the deleted play-marking canary succeeded by a HOST_WALL bottom-content
canary); the audio-seam refactor survived with ZERO audio conflicts.

Your job as a lens:
1. VERIFY the folds that touch your lens's domain — do the fixes actually hold, or are they
   skin-deep/wrong? A half-folded or wrongly-folded finding is a NEW blocker. (Fix-audit
   first: B1 — the loader now REPORTS failure and never coerces to rl.GetFontDefault, and
   app + harness + palcheck all refuse; the missing-asset-exits test actually bites. B2 —
   the PR body on GitHub is now the FONT job's content: hash-equal T1/replay proof + re-bless
   cause + before/after header pointers ON the body.)
2. Hunt for issues INTRODUCED by the fix commit / the rebases (delta-introduced findings are
   the norm this round). Two deltas to hunt in: (a) the audio-gating seam refactor (17
   wrappers, one when-block — the PP_SW_AUDIO single seam) must NOT change behavior (#86's
   teardown idioms preserved, no call site lost its gating); (b) the r2-sha->abec50b sculpt
   rebase (within the PR surface: harness/palcheck.odin's re-pin + the combined golden
   re-bless — verify the re-pinned floors/canaries are coherent, not self-fulfilling).
3. Do NOT re-litigate (user-ruled, twice-gated — findings here are auto-discarded):
   - The IBM Plex Sans family pick, the header hierarchy, and the contrast fold (incl. the
     disclosed ink_soft recolor of non-text surfaces and the disclosed Open Sans fallback catch).
   - The T2 golden storm (152,844 px text bands; every text-bearing golden re-blessed) —
     expected, cause-documented.
   - The audio seam REFACTOR'S DESIGN (17 wrappers, one when-block). VERIFY it preserves
     behavior; do not re-argue that wrappers should not exist.

Prior round findings for reference (do not re-file what is verifiably fixed; DO file
still-present ones — they carry forward as blockers if they were blockers):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-font-overhaul/r1/consolidated.json

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this path (create parent dirs if needed; write the file, do not print the JSON into chat):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-font-overhaul/r3/<LENS>.json

Each element must match this schema exactly:
{
  "source": "<LENS>",
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

Round-3 spotlight (in addition to the above): the fix commit added font_guard_reports_missing_asset (claimed to pin: missing file fails, garbage file fails, committed family loads). Verify it actually BITES: read the test, trace what it executes — does it exercise the real loader end-to-end (not a mock), does it assert on the ok=false propagation (not just a helper), and would it fail if someone re-introduced the GetFontDefault coercion? Same rigor for the new font_mono_tabular_digits pin (W5): does it actually pin tabular advance equality on font_mono? Check whether the harness tests, render tests, and core tests cover the fail-loud paths across ALL three call sites (app main, harness render_setup, palcheck). Also trace the combined re-bless: does any automated check tie the re-blessed goldens to the sculpt+font combined baseline (i.e. would a stale golden from EITHER source slip through)?

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
