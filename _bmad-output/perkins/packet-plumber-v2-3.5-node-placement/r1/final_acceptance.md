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
  "source": "acceptance",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

FILE-OUTPUT CONTRACT: write ONLY your JSON array to exactly this path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.5-node-placement/r1/acceptance.json
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
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

CRITICAL LENS-GUARDS (from the briefing — treat as canon):
- Terminals are NEVER player-placed (story 5.1): routers are NEVER director-spawned. A path that player-places a terminal, or lets the director spawn a router = blocker.
- Replay determinism [E10] + LOG_VERSION 2→3 re-bless: exactly the version byte changed in old goldens; old v2 logs reject cleanly. A silent re-bless of golden content = blocker.
- ZERO catalog changes claimed (cat.hash fold). Any catalog touch = finding unless deliberate + golden-accounted.
- Validation: span + 7-tile min-separation + no overlap + placement area; rejections use Edit_Error style. A validation hole = blocker.
- Port limits on draws: basic 4 / mid 8 / high 16 from catalog port_capacity; .Router_Ports_Full when exceeded. A draw ignoring port capacity = defect.
- Edit fast-path [ODN-2]: command flows through Command_Bus.validate → apply. A bypass = blocker.
- NO INVENTORY/ECONOMY — do NOT flag "placement is free".
- The prototype is reference-only. Do NOT flag missing prototype commands (draw/upgrade/demolish/lane-weights/pipe-priority/junction-triage) — 3.5 ports ONLY the PLACE command.
- Em-dashes are FINE in Packet-Plumber copy.
- Story 3.5 acceptance: tray renders + arms placement, click drops validated junction, ESC cancels, placed routers accept drag-drawn pipes; Cmd_Place_Router serializes + replays byte-identical; all existing suites green; no code changes outside placement + tests/render; terminals never placable.
