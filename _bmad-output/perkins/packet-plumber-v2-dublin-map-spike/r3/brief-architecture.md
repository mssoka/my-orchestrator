# Lens brief — ARCHITECTURE (r3)

You are reviewing a code diff. You have read-only access to the repository (your cwd IS the reviewed worktree) and may verify the diff's claims against the actual codebase using your available tools. Do not modify any file.

--- PROJECT CONVENTIONS ---
Read project-context.md in the repo root (governs code conduct). Existing tools/ scripts are the convention reference for how this repo does offline tooling (look at a couple, e.g. tools/blur_gate.py or the harness runner, for style). The game itself is Odin (core/ + app/); tools/ is Python.

--- DIFF ---
The canonical diff file (905 lines; ONE line inside it — L52 — is a single ~3.9 MB JSON asset line; NEVER cat that line raw, slice it with sed/python3):

/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-map-spike/r3/diff.patch

Diff map: L1-15 .gitignore (rebase-resolved: two blank separator lines removed, .osm-cache/ added, ambience-WAV and python-cache blocks both kept); L17-25 .memlog.md (append-only log); L27-44 new field-notes md; L46-53 new data/maps/dublin.json (entire asset = ONE line, L52, valid JSON — analyze via python3 reading the diff file, extracting L52, stripping the leading '+', json.loads); L54-88 nine new binary PNG stubs; L90-687 new tools/osm_extract.py (593 lines); L689-905 new tools/render_dublin_preview.py (211 lines).

--- SPEC / CONTEXT ---
The job briefing (the spec — this is a look-only spike: bake a Dublin map asset + render previews; explicitly NO gameplay/sim changes; the follow-up, if approved, wires the asset into the game):
/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-dublin-map-spike.md

--- YOUR LENS ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

Considerations in scope: the asset schema (data/maps/dublin.json top-level shape: _comment/attribution/license/extract/board/rulings/terrain/streets/spawn_candidates/districts) as a contract for the future in-game consumer; projection constants duplicated between osm_extract.py (BBOX/BOARD_W_TILES/scale math) and render_dublin_preview.py (recomputes ox0/utm_top from the asset's extract+board blocks — is the single-source-of-truth story sound?); the decision to pin Overpass QL by hand instead of osmnx (documented in the docstring — judge whether the stated reasoning holds); where a 3.9 MB single-line JSON asset fits the repo's data-loading story (other data/*.json catalogs, how the game loads data today); tools/ placement and naming.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "architecture",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. coupling, contract, duplication>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. If you cannot quote the lines, you have not done the work to file the finding.>",
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
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones — an empty array is a fine and honest answer when nothing is wrong.

--- FILE OUTPUT (mandatory) ---
Write your JSON array — and NOTHING else — to this exact absolute path (do not derive or guess any other path):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-map-spike/r3/architecture.json
Use your file-writing tool to create that file containing exactly the JSON array. After the file is written, stop. Do not do anything else.
