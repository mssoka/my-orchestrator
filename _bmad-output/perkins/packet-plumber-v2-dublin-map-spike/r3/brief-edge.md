# Lens brief — EDGE CASE (r3)

You are reviewing a code diff. You have read-only access to the repository (your cwd IS the reviewed worktree) and may verify the diff's claims against the actual codebase using your available tools. Do not modify any file.

--- PROJECT CONVENTIONS ---
Read project-context.md in the repo root (governs code conduct). tools/ scripts are offline dev tooling, not game runtime code.

--- DIFF ---
The canonical diff file (905 lines; ONE line inside it — L52 — is a single ~3.9 MB JSON asset line; NEVER cat that line raw, slice it with sed/python3):

/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-map-spike/r3/diff.patch

Diff map: L1-15 .gitignore (rebase-resolved: two blank separator lines removed, .osm-cache/ added, ambience-WAV and python-cache blocks both kept); L17-25 .memlog.md (append-only log); L27-44 new field-notes md; L46-53 new data/maps/dublin.json (entire asset = ONE line, L52, valid JSON — analyze via python3 reading the diff file, extracting L52, stripping the leading '+', json.loads); L54-88 nine new binary PNG stubs; L90-687 new tools/osm_extract.py (593 lines); L689-905 new tools/render_dublin_preview.py (211 lines).

--- SPEC / CONTEXT ---
The job briefing (the spec for this diff):
/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-dublin-map-spike.md

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

Context for relevance: osm_extract.py is run manually by a developer (fetch from Overpass mirrors → cache → bake → verify). render_dublin_preview.py renders preview PNGs from the baked asset. Neither runs in the game. Data-shape edge cases in the bake pipeline (empty/missing cache, malformed Overpass responses, degenerate geometry, empty element lists) and in the renderer (missing palette keys, empty districts, crop views near board edges) are in scope.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "edge",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. boundary, error-path>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

--- FILE OUTPUT (mandatory) ---
Write your JSON array — and NOTHING else — to this exact absolute path (do not derive or guess any other path):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-map-spike/r3/edge.json
Use your file-writing tool to create that file containing exactly the JSON array. After the file is written, stop. Do not do anything else.
