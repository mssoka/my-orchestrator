You are reviewing a code diff (a review LENS in a parallel team — stay in your lane). Read-only repository access.

--- INPUTS ---
- DIFF (chunk 2 of 2 — goldens/assets/docs; 11 files, 3648 lines): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-map-beautify/r1/diff-c2.patch
  Dominated by goldens/dublin_board.t1 (3610 lines, EVERY line changed — per-tick hash re-bless) + 10 binary entries
  (assets/maps/dublin_underlay.png committed ~9MB; docs/captures/dublin-map-mock/*.png; goldens/dublin_board.log.bin;
  goldens/dublin_board/{30000ms,90000ms}.png re-blessed).
- WORKTREE (sha 6f23b31a): /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-dublin-map-beautify-r1
- SPEC: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-map-beautify/r1/job-briefing.md — "goldens re-bless ONLY the board-underlay class (cause-documented: map restyle)"; "sim untouched: T1/T2/replay hash-equal"
- PROJECT CONVENTIONS: /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-dublin-map-beautify-r1/project-context.md

--- ROUND CONTEXT ---
Chunk 1 (code: app/, tools/, harness/, data/) is a separate wave — anchor to chunk-2 files but verify against the worktree.
The dublin_board transcript changing is EXPECTED (re-extract changes the spawn pool by design); other demos' goldens must be untouched.
PR claims: 49/49 demos green post re-bless; cause documented; KYLE captures = docs/captures/dublin-map-mock/*.png.

--- YOUR LENS (tests) ---
The .t1 transcript IS the test artifact — audit it as coverage evidence:
- Traceability: does the re-blessed transcript + the 2 re-blessed PNGs + log.bin constitute the FULL golden set the dublin_board demo needs (check the worktree goldens/dublin_board/ for other captures the diff should have re-blessed but didn't — e.g. more timestamps, a11y variants)?
- Which golden classes exist per demo in this repo (inventory goldens/ in the worktree) and does dublin_board have any UNTOUCHED golden file that the restyle should have changed (stale golden = a future harness failure)?
- Emit the advisory coverage-gate finding (PASS/CONCERNS/FAIL) for the re-bless scope.

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-map-beautify/r1/tests-c2.json

Schema:
{
  "source": "tests",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<exact lines pasted verbatim; 'N/A' only when no code reference is possible>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

ONLY the JSON array in the file; [] valid; after writing STOP.

ACCURACY MANDATE — findings are re-verified against the worktree/diff; failures DISCARDED silently. Quote exact lines. [] is honest.