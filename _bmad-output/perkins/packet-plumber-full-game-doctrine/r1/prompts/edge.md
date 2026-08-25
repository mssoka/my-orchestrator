You are reviewing a DOCS-ONLY diff (no code). You have read-only access to the repository and may verify the diff's claims against the actual files using your available tools. Do NOT modify any file in the repository.

--- PROJECT CONVENTIONS ---
This is a game project (Packet Plumber, Odin + raylib) whose canon lives in planning docs under `_bmad-output/planning-artifacts/`. The established canon-amendment pattern: the decision log is APPEND-ONLY; superseded lines are never struck silently — each carries a dated supersede note citing the decision-log entry that supersedes it (banner + pointer, never silent removal). Doctrine-level amendments cascade through five docs with the decision-log entry recorded FIRST and every other amendment citing it.

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
- Job briefing (the spec): /Users/moses/code/_bmad-output/perkins/packet-plumber-full-game-doctrine/r1/spec/job-briefing.md — the user ruling (verbatim anchors), the Doctrine, the six Mission items (the required per-doc edits), the five Acceptance criteria, and the Scope guard.
- Round briefing (review rulings): /Users/moses/code/_bmad-output/perkins/packet-plumber-full-game-doctrine/r1/spec/round-briefing.md — the r1 guards section is binding on your judgments.
- No GitHub issue exists for this job — the two files above are the complete spec.

--- LENS-GUARDS (round-specific rulings — prevents false positives; honor them) ---
The user ruling (2026-08-17) IS the spec — quote-level checks against it matter.

THE ONE HARD BLOCKER CLASS — canon consistency + provenance discipline:
- Acceptance bar (grep-verify across the FIVE docs): zero remaining "rebuild the full game fresh" / "prototype is reference, not codebase" framings; any intentional historical reference MUST carry a dated supersede note citing the 2026-08-17 decision-log entry — nothing struck silently.
- The 2026-08-17 decision-log entry must be complete + cited by every amended section: date, verbatim anchors, rationale (v2 production discipline: deterministic core, command bus, golden harness, local CI; the pre-v2 prototype fulfilled the prototype role), consequences (E11 SUPERSEDED — features live on as full-game backlog; no rebuild; fun-test gate REFRAMED as the content-scaling greenlight, never removed).
- No scope creep: no slice resequencing, no new stories, no story-card (Given/When/Then) edits, no GDD mechanic changes, no code/catalog changes in the diff.
- Traceability chain intact: gdd.md's Development Epics summary + any prototype/rebuild staging refs align with epics.md; the sprint plan's slice-8+/N framing and the stories-v2 slice-7 exit line read as "fun-test gate" on the full-game-on-v2 language.

WHAT NOT TO RE-LITIGATE (false-positive guards — do NOT file these):
- The user ruling itself (verbatim anchors — it IS the spec).
- The lavish-approved amendment set (the user reviewed + approved this content in-browser before the PR opened).
- The 5.5/7.2 stories (approved + in flight).
- The fun-test gate's EXISTENCE (reframed, never removed — its continued presence is CORRECT, not a defect).
- The pre-existing "PR open, in review" 5.5 status line in stories-v2.md — a sibling-stale artifact; note-only if you see it, NOT a blocker.
- "MVP" retained as a term, redefined (the full game's core up to the fun-test gate) — a documented PR decision; both traceability matrices carry footnotes pinning the new meaning.
- Intentional historical references the PR body declares as kept: sprint-plan-v2 title + §1 mission "from scratch"; §5 harness "mined from the prototype reference" + frontmatter `prototype_reference`; gdd risk-5 title "Prototype methodology"; `[ASSUMPTION: prototype tuning]` tags + Assumptions Index; decision-log history (append-only); epics.md E1.4 `[PROTO (PR #17)]` routing note. These are declared provenance — flag one ONLY if it lacks the stated supersede note/rationale where the PR claims one exists.
- GitHub Actions being org-billing-blocked on #61 is NOT a signal (docs-only PR).

--- YOUR LENS ---
You are a pure path tracer — for documentation. Do not comment on whether the docs are good or bad — list only unhandled cross-reference paths reachable from the changed lines.

Method: mechanically walk every reference, citation, and claim touched by the diff hunks, and trace each one to its target in the worktree. Derive edge classes from the changed text itself — no fixed checklist. Edge classes for a canon cascade include: a supersede note citing a decision-log entry that does not exist or lacks the cited content; a footnote pinning a term's new meaning whose matrix row was NOT updated; a section reference (§x.y, decision N, OQ N, "Development Epics", "traceability matrix") that no longer resolves to matching text; a doc-to-doc claim (epics says X about E11; gdd's epics summary says Y) that diverges; a renamed label ("MVP done" → "fun-test gate") updated in a row but not in the row's sibling cells; a declared-kept historical reference whose claimed adjacent supersede note is absent; boundary cases like the ONE remaining "E10–E11" citation label (sprint-plan §6.4) and the ONE remaining "juiced GRAYBOX" (inside the dated supersede note) — verify each is exactly where the PR body says it is and carries the claimed cover.

For each path, determine whether the worktree handles it. Report ONLY unhandled paths that lack the required cover; discard handled ones silently. No editorializing.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "edge",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. citation, cross-ref, supersede-note>",
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
/Users/moses/code/_bmad-output/perkins/packet-plumber-full-game-doctrine/r1/edge.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens edge complete — N findings written".
