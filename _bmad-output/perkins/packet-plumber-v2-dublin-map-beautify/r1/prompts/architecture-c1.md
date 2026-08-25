You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. You are a review LENS in a parallel team — find what your lens finds; stay in your lane.

--- INPUTS (absolute paths) ---
- DIFF (chunk 1 of 2 — the code files; 11 files, 2522 lines): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-map-beautify/r1/diff-c1.patch
  Files: .gitignore (+1: .scratch/), app/render/dublin.odin (rewritten, 639 diff lines), app/render/view.odin (21),
  data/maps/dublin.json (8 — re-extracted spawn pool), harness/dublin_shot.odin (16), harness/run.odin (17),
  tools/blender_board/blender_board_build.py (NEW, 505), tools/blender_board/prep_board_geometry.py (NEW, 272),
  tools/blender_board/render_dublin_preview.py (NEW, 330), tools/osm_extract.py (479), tools/render_dublin_preview.py (216).
  Read it with offset/limit in chunks; every hunk matters. (Chunk 2 — goldens/assets/docs — is a SEPARATE wave;
  you may verify those files EXIST in the worktree, but your findings must be anchored in chunk-1 files.)
- WORKTREE (the checkout at exactly the reviewed sha 6f23b31a — every verification read happens here; trust it, not origin/v2): /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-dublin-map-beautify-r1
- PROJECT CONVENTIONS: /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-dublin-map-beautify-r1/project-context.md (read it — core purity ODN-1, integer sim ODN-10, determinism, arena discipline, golden harness rules)
- SPEC / CONTEXT (review_mode = full): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-map-beautify/r1/job-briefing.md (the job briefing — the spec; read it IN FULL)

--- ROUND CONTEXT (round 1 — no prior findings; nothing is pre-ruled) ---
Job: restyle the Dublin game board to the Mini Motorways grammar. User verdict on the previous look:
"ugly with all the red dots, and the names of the locations — we just want the map ... also there is no
irish sea in what was delivered." Spec rules (hard): sim untouched (T1/T2/replay hash-equal; goldens re-bless
ONLY the board-underlay class, cause-documented); fix lives in render + bake styling (osm_extract layer
selection may change; sea fix may re-extract — dublin.json versioned, determinism preserved); district labels
gone EXCEPT the tiny ODbL attribution; deliverables hold at default zoom AND a zoomed crop.
The implementing minion's claims (from PR #95 body — verify against the code, do not trust):
- Sea root cause: OSM never maps the open sea as a polygon; build_sea constructs the sea from the coastline
  union + bbox partition face, clipped to a coastal strip (SEA_STRIP_M = 1300, ~15% of the frame incl. Liffey/bay).
- The board background is now a committed Blender-baked texture assets/maps/dublin_underlay.png (4160x3120,
  hex-exact paper palette, Blender timestamp chunks stripped for byte-stability); the bake pipeline lives in
  tools/blender_board/ and is deterministic from the pinned raw cache.
- dublin.odin rewritten: texture underlay draw, no grid/labels/dots; terminals = street-aligned blocks
  (nearest street segment orients the block; no street within 3 tiles -> logged axis-aligned fallback).
- The harness REFUSES to capture if the underlay fails to load (Dublin_Underlay_Ready; fonts/sprites precedent);
  the app fails soft (street skeleton on canvas).
- 49/49 demos green post re-bless; input-parity 27/27; 13/13 local CI gates; sim hashes unchanged for every
  PROCEDURAL demo (dublin_board re-blessed with cause: the bbox re-extract changes the spawn pool by design).
PR: https://github.com/solarity-services/Packet-Plumber/pull/95 (head 6f23b31a).

--- YOUR LENS (architecture) ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?
Project invariants that govern: core purity (ODN-1 — core/ never imports vendor/os/time), integer sim (ODN-10), view-layer floats never flow back into state, determinism everywhere (T2 byte-identical pixels), arena discipline (ODN-18).

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this path (create parent dirs if needed; write the file, do not print the JSON into chat):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-map-beautify/r1/architecture-c1.json

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