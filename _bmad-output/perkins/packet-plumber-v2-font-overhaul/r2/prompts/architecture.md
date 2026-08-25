SHARED BLOCK (given to every lens EXCEPT blind — blind gets its own file)

You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- INPUTS (absolute paths) ---
- DIFF: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-font-overhaul/r2/diff.patch
  (the canonical diff under review — 153 files, 144 KB; read it with offset/limit in chunks; every hunk matters but the 111 goldens/*.png + 13 docs/captures/*.png + 8 assets/fonts/*.ttf entries are binary one-liners)
- WORKTREE (the checkout at exactly the reviewed sha 0166c3f — every verification read happens here; trust it, not origin/v2): /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-font-overhaul-r2
- PROJECT CONVENTIONS: /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-font-overhaul-r2/project-context.md
- SPEC / CONTEXT (review_mode = full):
  1. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-font-overhaul/r2/spec/job-briefing.md (the job briefing — the spec)
  2. /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-font-overhaul/r2/spec/perkins-briefing-r2.md (the round briefing — its 'Lens-guards' section is part of the spec: what NOT to re-litigate + the round-2 fix-audit focus)

--- ROUND 2 (fix-audit re-review) CONTEXT ---
This is round 2 of a Perkins loop. Round 1 (review of sha 47ebd0f) returned CHANGES_REQUESTED
with 2 blockers (B1 fail-loud guard dead code, B2 wrong PR body) + 5 warnings + 15 notes. The
implementing minion claims ALL were folded in commit 0166c3f ("fix: Perkins r1 — ..."), which
also absorbed a rebase onto the settled head (PR #86's audio work landed; the PP_SW_AUDIO usage
was refactored to a single seam — "17 wrappers, one when-block").

Your job as a lens:
1. VERIFY the folds that touch your lens's domain — do the fixes actually hold, or are they
   skin-deep/wrong? A half-folded or wrongly-folded finding is a NEW blocker.
2. Hunt for issues INTRODUCED by the fix commit / the rebase (delta-introduced findings are the
   norm this round). The r1->r2 changed-file surface is: _pr_body_font_overhaul.md,
   app/audio/audio.odin, app/gallery.odin, app/main.odin, app/render/{crisis,font_test,noc_overlay,
   palette,settings_panel,view}.odin, harness/{font_check,goldens,overlay,palcheck}.odin.
3. Do NOT re-litigate (user-ruled, twice-gated — findings here are auto-discarded):
   - The IBM Plex Sans family pick, the header hierarchy, and the contrast fold (incl. the
     disclosed ink_soft recolor of non-text surfaces).
   - The T2 golden storm (every text-bearing golden re-blessed) — expected, cause-documented.
   - The audio seam REFACTOR'S DESIGN (17 wrappers, one when-block). VERIFY it preserves
     behavior; do not re-argue that wrappers should not exist.

Prior round findings for reference (do not re-file what is verifiably fixed; DO file
still-present ones — they carry forward as blockers if they were blockers):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-font-overhaul/r1/consolidated.json

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this path (create parent dirs if needed; write the file, do not print the JSON into chat):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-font-overhaul/r2/architecture.json

Each element must match this schema exactly:
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
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

Round-2 spotlight (in addition to the above): the fix commit refactored font loading into font_atlas_build (pure-CPU data stage) + load_fonts reporting ok=false — check the layering (does app/render/view.odin own what it should, is the pure stage genuinely testable headless, is the ok-propagation consistent across the three call sites app/harness/palcheck). The #86-rebase PP_SW_AUDIO seam (17 wrappers, one when-block in app/audio/audio.odin): DO NOT re-argue the wrapper design (user-ruled conflict-class fix) — but DO verify it is a faithful behavior-preserving regrouping of the previous gating and that no call site lost its gating.
