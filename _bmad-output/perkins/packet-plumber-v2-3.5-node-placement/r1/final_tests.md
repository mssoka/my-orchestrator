You are reviewing a code diff as a specialist reviewer. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Packet-Plumber is an Odin game (raylib). Core package is deterministic pure sim (arrays-only + seeded rng, no maps — lint-gated). Command_Bus = topology_apply_edit validate→apply single authority (ODN-2 edit fast-path). All edits are logged Commands replayed byte-identically (E10, ODN-11). Catalogs are JSON single source (ODN-5); cat.hash folds catalog bytes — ANY catalog change shifts every golden. LOG_VERSION gates old logs (reject cleanly).

--- DIFF ---
Read the canonical diff at: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.5-node-placement/r1/diff.patch
Review EXACTLY those bytes. Do not re-fetch or regenerate the diff.

--- SPEC / CONTEXT ---
- /Users/moses/code/_bmad-output/briefings/perkins-packet-plumber-v2-3.5-node-placement-r1.md (the briefing incl. lens-guards)
- /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-3.5-node-placement.md (job briefing)
- /Users/moses/code/packet-plumber/_bmad-output/planning-artifacts/sprints/stories-v2.md (stories 3.5 + 5.1)
- /Users/moses/code/packet-plumber/_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md ([E10], [ODN-2], [ODN-5], §11.7)

--- VERIFICATION WORKTREE ---
Read files at: /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-3.5-node-placement-r1 (a checkout at exactly the reviewed sha 666b082). All verification reads happen here.

--- YOUR LENS ---
see LENS BRIEF section below

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "tests",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

FILE-OUTPUT CONTRACT: write ONLY your JSON array to exactly this path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.5-node-placement/r1/tests.json
Use the write tool. Then stop. Do not write anything else to that path.

Output contract:
- The file contains ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — the most important instruction:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. Accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

--- LENS BRIEF ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- New command kind Cmd_Place_Router: validation paths (terminal reject, unknown type, off-map, min-sep, boundary AT the radius), apply path (gen bump, id monotonic, live junction), serialization round-trip, version-2 log rejection, replay byte-identical — which are covered by core/placement_test.odin and which are not?
- Port limits: 5th pipe on basic (4 ports), demolish frees port, terminals never limited, mid (8) / high (16) capacities — covered? What about a draw where BOTH endpoints are junctions (both port-checked)? What about the app-layer paths: tray arm/cancel/ESC/right-click, press-move guard, chip swallow — are any of these tested (or is that acceptable for a game app layer)?
- Negative controls: does a neutralized validation actually make tests go red (the min-sep radius test pins boundary semantics)?
- The demo place.dem + goldens/place.t1 + place T2 PNGs: does the T2 golden actually pin the placed router + new pipe?

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
