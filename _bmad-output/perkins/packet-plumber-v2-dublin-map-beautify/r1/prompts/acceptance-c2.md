You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. You are a review LENS in a parallel team — find what your lens finds; stay in your lane.

--- INPUTS (absolute paths) ---
- DIFF (chunk 2 of 2 — goldens/assets/docs; 11 files, 3648 lines): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-map-beautify/r1/diff-c2.patch
  Files: assets/maps/dublin_underlay.png (binary, committed 9MB), docs/captures/dublin-map-mock/*.png (6 binary),
  goldens/dublin_board.log.bin (binary), goldens/dublin_board.t1 (3610 lines — the per-tick hash transcript: EVERY line changed),
  goldens/dublin_board/30000ms.png + 90000ms.png (binary re-bless).
  The .t1 is a text manifest: header (demo/seed/logic_hz/catalog_hash/ticks) + one "<tick> <fnv1a64-hash>" line per tick.
  Binary entries are one-liners in the diff — verify their PRESENCE, and verify the actual files in the worktree mechanically
  (dimensions, byte size, PNG structure) with python if useful.
- WORKTREE (checkout at exactly the reviewed sha 6f23b31a): /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-dublin-map-beautify-r1
- SPEC: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-map-beautify/r1/job-briefing.md (read IN FULL — the acceptance rules govern this chunk: goldens re-blessed ONLY for the
  board-underlay class, cause-documented; sim untouched otherwise)
- PROJECT CONVENTIONS: /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-dublin-map-beautify-r1/project-context.md

--- ROUND CONTEXT ---
Chunk 1 (code) is reviewed by a separate wave — anchor findings to chunk-2 files (the worktree is available for
cross-verification: goldens/README or lack of it, how .t1 manifests are structured, what log.bin carries, which demos
exist under goldens/). Key spec rule: "goldens re-bless ONLY the board-underlay class (cause-documented: map restyle)"
and "sim untouched: T1/T2/replay hash-equal". The dublin_board demo's T1 transcript changing is EXPECTED (the spec
allows the re-extract to change the spawn pool); any OTHER demo's goldens changing would be a violation. The PR body
claims: re-bless cause documented (core-bbox re-extract changes the spawn pool by design); 49/49 demos green post
re-bless; input-parity 27/27; KYLE live-capture PASS at both zooms (evidence = docs/captures/dublin-map-mock/*.png).


--- YOUR LENS (acceptance) ---
Audit chunk 2 against the spec. Check specifically:
- Re-bless SCOPE: only the dublin_board golden class changed (verify against the diff's file list AND the worktree's goldens/ — e.g. compare git-free: the diff itself is the scope record; also confirm no other *.t1/*.png golden appears in it).
- Cause documentation: is the re-bless cause recorded anywhere durable (PR body, goldens doc, .t1 header)? The .t1 header lines are in the diff — quote what is/isn't there.
- The .t1 transcript's internal consistency: catalog_hash changed (spawn-pool re-extract), ticks count matches header, hash lines well-formed, no duplicate ticks, no gaps in the tick sequence.
- The committed underlay asset exists at the claimed size/dimensions (4160x3120) — verify mechanically in the worktree.
- The KYLE evidence captures exist (docs/captures/dublin-map-mock/).
For each finding, quote the violated spec phrase in `detail`.

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this path (create parent dirs if needed; write the file, do not print the JSON into chat):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-map-beautify/r1/acceptance-c2.json

Each element must match this schema exactly:
{
  "source": "acceptance",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings with no possible code reference. Do not paraphrase. Do not reconstruct from memory.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- ONLY the JSON array in the file. No prose, no fencing, no preamble.
- Empty array `[]` is valid and expected.
- No quota-filling.
- After writing the file, STOP. Do not fix anything. Do not push.


ACCURACY MANDATE — NO claim will be taken at face value. Every finding will be independently re-verified against the actual codebase/worktree before it reaches the report; failures are DISCARDED SILENTLY. Paste EXACT lines as evidence — if you cannot quote them, drop the finding. Hedging = not verified. Fewer, well-grounded findings > volume; [] is honest.