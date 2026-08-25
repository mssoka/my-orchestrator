You are reviewing a DOCS-ONLY diff (no code). You have read-only access to the repository and may verify the diff's claims against the actual files using your available tools. Do NOT modify any file in the repository.

--- PROJECT CONVENTIONS ---
This is a game project (Packet Plumber, Odin + raylib) whose canon lives in planning docs under `_bmad-output/planning-artifacts/`. The established canon-amendment pattern: the decision log is APPEND-ONLY; superseded lines are never struck silently — each carries a dated supersede note citing the decision-log entry that supersedes it. Terminology, epic ids (E1–E11), story ids (X.Y), and slice numbers are canonical identifiers other docs cite.

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
- Job briefing (the spec): /Users/moses/code/_bmad-output/perkins/packet-plumber-full-game-doctrine/r1/spec/job-briefing.md
- Round briefing (review rulings): /Users/moses/code/_bmad-output/perkins/packet-plumber-full-game-doctrine/r1/spec/round-briefing.md — the r1 guards section is binding on your judgments.
- PR body (its claims are checkable facts): /Users/moses/code/_bmad-output/perkins/packet-plumber-full-game-doctrine/r1/spec/pr-body.md
- No GitHub issue exists for this job — the files above are the complete spec.

--- LENS-GUARDS (round-specific rulings — prevents false positives; honor them) ---
THE ONE HARD BLOCKER CLASS — canon consistency + provenance discipline (grep bar; decision-log entry complete + cited; no scope creep; traceability intact).
WHAT NOT TO RE-LITIGATE (false-positive guards — do NOT file these):
- The user ruling itself; the lavish-approved amendment set; the 5.5/7.2 stories; the fun-test gate's existence; the pre-existing "PR open, in review" 5.5 status line in stories-v2.md (note-only).
- "MVP" retained as a redefined term; E11 kept as a SUPERSEDED section quoting the original framing; E11 features folded as a paragraph not new stories.
- The declared-kept historical references (sprint-plan title + §1 mission "from scratch"; §5 harness "mined from the prototype reference" + frontmatter `prototype_reference`; gdd risk-5 title "Prototype methodology"; `[ASSUMPTION: prototype tuning]` tags; decision-log history; epics.md E1.4 `[PROTO (PR #17)]` note) — flag one ONLY if the cover the PR claims for it is absent.
- Docs OUTSIDE the five in scope (e.g., other planning-artifacts, READMEs) are NOT in this PR's scope — do not demand they be amended here.
- GitHub Actions being org-billing-blocked on #61 is NOT a signal (docs-only PR).

--- YOUR LENS ---
Reality check against the actual files. Verify by reading files, not by assuming:
- Do the section references cited in the diff and the PR body actually exist and match? Check each: sprint-plan-v2.md "§6.4", "decision 6", "OQ 3", "§1 mission", "§5 harness", the slice-map table rows 7 and N, the "MVP?" column footnote; gdd.md "Development Epics" summary, the win/loss table row, the forge-risk rows 1 & 5, the traceability matrix + "MVP?" footnote; epics.md header scope line, traceability-matrix E11 row + footnote, build-staging bullets, E10 fold-line, E11 section, MVP-build-order closing line; stories-v2.md notation line, slice-7 header + exit line, slice-N header + E11 bullet. Any cited anchor that does not exist or says something different = finding.
- Are the diff's claims about untouched content true? Spot-check: no story-card (Given/When/Then) text appears in the diff's removed/added lines; no slice numbers resequenced; no GDD mechanic numbers altered (compare removed vs added lines in gdd hunks — only labels/staging/epics-summary wording should differ).
- Orphan references: grep the five docs for live references to "E11" that still treat it as a future rebuild (not citing the SUPERSEDED section) — excluding declared-kept historical refs.
- Terminology consistency: the new labels introduced ("fun-test gate", "MVP core (fun-test gate)", "SUPERSEDED", the footnote wording) — spelled/capitalized consistently across all five docs?
- Does the PR body's "Grep proof" table match reality (run the greps yourself in the worktree)?
- Are there other files in the repo whose text the diff claims to align with, that actually contradict (verify before filing)?

Your `source` value is "codebase".

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "codebase",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. dangling-ref, terminology, stale-claim>",
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
/Users/moses/code/_bmad-output/perkins/packet-plumber-full-game-doctrine/r1/codebase.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens codebase complete — N findings written".
