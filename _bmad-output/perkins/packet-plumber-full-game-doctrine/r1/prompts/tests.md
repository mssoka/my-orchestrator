You are reviewing a DOCS-ONLY diff (no code). You have read-only access to the repository and may verify the diff's claims against the actual files using your available tools. Do NOT modify any file in the repository.

--- PROJECT CONVENTIONS ---
This is a game project (Packet Plumber, Odin + raylib) whose canon lives in planning docs under `_bmad-output/planning-artifacts/`. The established canon-amendment pattern: the decision log is APPEND-ONLY; superseded lines carry dated supersede notes citing the decision-log entry. For a docs-only canon amendment, "coverage" means: every required edit in the spec traced to an actual change in the docs, and every claim in the PR body traced to reality.

--- DIFF ---
Read the canonical diff FIRST and IN FULL: /Users/moses/code/_bmad-output/perkins/packet-plumber-full-game-doctrine/r1/diff.patch (427 lines, unified format, PR #61 of solarity-services/Packet-Plumber, base branch v2). These exact bytes are the review target — never re-fetch or regenerate the diff.

--- WORKTREE (your verification source) ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-full-game-doctrine-r1 — a checkout at exactly the reviewed sha (ddf8f2800ac6e7d6fa6331c044aa73447d90a513). Every verification read happens here. Trust this checkout, not origin/v2. The five docs under review:
- _bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/decision-log.md
- _bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/epics.md
- _bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md
- _bmad-output/planning-artifacts/sprints/sprint-plan-v2.md
- _bmad-output/planning-artifacts/sprints/stories-v2.md

--- SPEC / CONTEXT ---
- Job briefing (the spec): /Users/moses/code/_bmad-output/perkins/packet-plumber-full-game-doctrine/r1/spec/job-briefing.md — the six Mission items are the required behaviors.
- Round briefing (review rulings): /Users/moses/code/_bmad-output/perkins/packet-plumber-full-game-doctrine/r1/spec/round-briefing.md — the r1 guards section is binding on your judgments.
- No GitHub issue exists for this job — the files above are the complete spec.

--- LENS-GUARDS (round-specific rulings — prevents false positives; honor them) ---
THE ONE HARD BLOCKER CLASS — canon consistency + provenance discipline (grep bar; decision-log entry complete + cited; no scope creep; traceability intact).
WHAT NOT TO RE-LITIGATE (false-positive guards — do NOT file these):
- The user ruling itself; the lavish-approved amendment set; the 5.5/7.2 stories; the fun-test gate's existence; the pre-existing "PR open, in review" 5.5 status line in stories-v2.md (note-only).
- "MVP" retained as a redefined term; E11 kept as a SUPERSEDED section; E11 features folded as a paragraph not new stories; the declared-kept historical references.
- There is NO automated test suite for docs (the 9-gate local CI has no doc checks — the PR body says so). Do NOT file "no tests for this change" — for this PR, traceability coverage IS the test analog.
- GitHub Actions being org-billing-blocked on #61 is NOT a signal (docs-only PR).

--- YOUR LENS ---
Traceability coverage analysis. For each required edit in the job briefing's Mission items 1–6, trace it to an actual change in the worktree docs (visible in the diff AND present in the file). Classify each as FULL / PARTIAL / NONE coverage and emit one finding per gap:
- Mission 1 (decision-log entry: date, verbatim anchors, rationale, consequences)
- Mission 2 (epics.md: E11 rewrite as SUPERSEDED with features as backlog; header scope line reframe; build-staging "rebuild from scratch"/"prototype = reference" removed; "MVP = juiced GRAYBOX" → production quality; MVP-build-order closing line amended)
- Mission 3 (gdd.md: Development Epics summary + prototype/rebuild staging refs aligned; traceability chain intact)
- Mission 4 (sprint-plan-v2.md: slice map MVP? column meaning; executive summary; slice 8+ "(post-fun-gate)" framing; slice N "(E10) + production polish (E11)" framing → full-game-on-v2 language; fun-test gate stays at slice-7 exit as content greenlight)
- Mission 5 (stories-v2.md: slice-7 exit line "MVP COMPLETE (E1–E9)" → "fun-test gate"; slice 8+/N coarse framing lines aligned; story cards NOT touched)
- Mission 6 (provenance discipline: every superseded line carries a dated supersede note citing the decision-log entry; no silent strikes — spot-check by comparing removed lines in the diff against the worktree for their supersede-note cover)

Severity mapping: a NONE gap on a required Mission edit = blocker; PARTIAL = warning; wording-level shortfall = note.

Blind-spot heuristics: required edits claimed in the PR body's per-doc summary but missing from the diff; a Mission item covered in one of two parallel locations (e.g., epics traceability matrix updated but gdd's epics summary row not, or vice versa).

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory coverage gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale — how many of the ~20 required edits traced FULL vs PARTIAL vs NONE
- recommended_fix: what would raise the gate

Gate thresholds: PASS = every Mission item FULL; CONCERNS = all covered but ≥1 PARTIAL; FAIL = any NONE.

Your `source` value is "tests".

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "tests",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. coverage-gap, coverage-gate>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:
NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual files before it reaches the report. Findings that fail verification are DISCARDED SILENTLY. Open the file. Read the relevant lines. The `evidence` field must contain the EXACT lines you read. Hedging language ("might", "could", "possibly") is a signal that you have not verified — either verify and report crisply, or do not report. Prefer fewer, well-grounded findings. An empty array is a fine and honest answer.

FILE-OUTPUT CONTRACT (headless mode): using your file-write tool, write ONLY your JSON array (valid JSON, no prose, no markdown fencing, no preamble) to exactly this absolute path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-full-game-doctrine/r1/tests.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens tests complete — N findings written".
