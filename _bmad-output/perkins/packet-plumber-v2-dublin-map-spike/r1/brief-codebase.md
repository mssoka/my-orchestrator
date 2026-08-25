You are reviewing a code diff. You have read-only access to the repository worktree below and may verify the diff's claims against the actual codebase using your tools. STRICTLY READ-ONLY on the worktree: modify nothing; the only file you may write is your one output file named at the end.

--- CANONICAL DIFF (the exact bytes under review) ---
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-map-spike/r1/diff.patch (899 lines). Map:
- L1-9: .gitignore modification · L11-19: .memlog.md modification · L21-38: new _bmad-output/field-notes/packet-plumber-v2-dublin-map-spike.md
- L40-47: new data/maps/dublin.json — the ENTIRE asset is ONE ~3.9 MB line at L46. NEVER cat/print that line raw; analyze with python3 (read diff, take line 46, strip leading '+', json.loads). Note L47: "\ No newline at end of file".
- L48-82: nine new PNGs under docs/captures/dublin-map-spike/ ("Binary files differ" stubs; real files exist in the worktree)
- L84-681: new tools/osm_extract.py (593 lines) · L683-899: new tools/render_dublin_preview.py (216 lines)
The worktree is a checkout at exactly the reviewed commit: new-file diff content == the file on disk.

--- WORKTREE (your cwd; read-only) ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-dublin-map-spike-r1

--- SPEC / CONTEXT (the job briefing IS the spec) ---
Read: /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-dublin-map-spike.md

--- PROJECT CONVENTIONS ---
Read: project-context.md in the worktree root.

--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?
Specific claims in this diff to reality-check against the codebase: render_dublin_preview.py claims to use "the game's OWN tokens: data/palette.json" (keys canvas, water, coast, park, grid, ink, ink_soft, ink_faint, house_bodies) and the font assets/fonts/open_sans_regular.ttf as "the HUD font the render layer loads", and claims its draw order "mirrors map.odin canon" with an "18% grid blend" and TILE_PX=26 / 40x30 board from data/balance.json map.*. Verify each claim against the actual game files. Also check the existing tools/ Python scripts for prior conventions the new tools should match, and whether .gitignore/.memlog.md changes match repo convention.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "codebase",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
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
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-map-spike/r1/codebase.json
Use your file-writing tool to create that file containing exactly the JSON array. After the file is written, stop. Do not do anything else.
