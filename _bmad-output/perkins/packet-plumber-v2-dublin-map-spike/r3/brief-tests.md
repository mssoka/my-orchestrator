# Lens brief — TEST COVERAGE (r3)

You are reviewing a code diff. You have read-only access to the repository (your cwd IS the reviewed worktree) and may verify the diff's claims against the actual codebase using your available tools. Do not modify any file.

--- PROJECT CONVENTIONS ---
Read project-context.md in the repo root (governs code conduct). Note how this repo tests: core/ has Odin unit tests + golden-image harness (harness/, goldens/); tools/ scripts historically ship with lint/verify gates but NOT unit tests — check what convention actually exists in tools/ before demanding test scaffolding the project would never build. This diff is an explicitly look-only spike (user-gated; NO gameplay/sim changes allowed; the follow-up wiring, if approved, is a separate job).

--- DIFF ---
The canonical diff file (905 lines; ONE line inside it — L52 — is a single ~3.9 MB JSON asset line; NEVER cat that line raw, slice it with sed/python3):

/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-map-spike/r3/diff.patch

Diff map: L1-15 .gitignore (rebase-resolved: two blank separator lines removed, .osm-cache/ added, ambience-WAV and python-cache blocks both kept); L17-25 .memlog.md (append-only log); L27-44 new field-notes md; L46-53 new data/maps/dublin.json (entire asset = ONE line, L52, valid JSON — analyze via python3 reading the diff file, extracting L52, stripping the leading '+', json.loads); L54-88 nine new binary PNG stubs; L90-687 new tools/osm_extract.py (593 lines); L689-905 new tools/render_dublin_preview.py (211 lines).

--- SPEC / CONTEXT ---
The job briefing (the spec):
/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-dublin-map-spike.md
Its acceptance section is the coverage target: committed deterministic bake; preview renders; zero diff to existing sim/render/goldens; pr_review.

--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check (adapted to this diff's reality — offline tools, not a web app): new/modified API endpoints (none); the determinism contract (does anything TEST it, or only the --verify self-check?); projection math correctness (any cross-check that tile coords land in-bounds?); renderer output stability (re-render hash compare?); asset schema validity. Judge against what the project's testing conventions would actually demand for a look-only spike — do not import web-app coverage quotas that do not fit.

Test level mix (unit/integration/E2E): flag mismatches as findings.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds:
- PASS: P0 100%, P1 ≥90%, overall ≥80%
- CONCERNS: P0 100%, P1 80–89%, overall ≥80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "tests",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing (except: always emit the advisory-gate finding).
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
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-map-spike/r3/tests.json
Use your file-writing tool to create that file containing exactly the JSON array. After the file is written, stop. Do not do anything else.
