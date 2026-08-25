# LENS: Acceptance Auditor (source = `acceptance`)

First load the shared context: read `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.2-window-draw-pipe/r1/prompts/_shared.md` (lens-guards, output schema + contract, empirical gate status, canonical input paths). Follow it exactly.

## YOUR LENS — diff vs spec/context
Audit the diff against the spec and context docs (briefing + Story 1.2 card + architecture + GDD). Identify:
- Violations of specific acceptance criteria.
- Deviations from spec intent.
- Missing implementation of specified behavior.
- Contradictions between spec constraints and actual code.
- Scope drift — changes not asked for by the spec.

The Story 1.2 acceptance criteria you must check (from the card + briefing):
- A 1280×720 window renders the hardcoded static fixture (1 source, 1 router, 1 sink).
- Mouse drag-draw with snap-to-node creates a pipe via the validated Command_Bus + edit fast-path; pipes appear same-frame.
- `.Self_Loop` (E3), `.Terminal_To_Terminal` (E26), span-exceeding draws are rejected.
- Replay applies all log entries for tick N before stepping N → live and replay see identical state at every step boundary (E10/ODN-2).
- Pipe/node ids monotonic, never recycled (E11).
- Snap inclusive at radius (E4).
- T1 golden: the drawn topology is IN the hash → replay-equality is real (not vacuous).
- T2 golden: the re-rendered drawn-pipe frame matches byte-exact.
- W1: the drift-rejection negative test is exercised in CI.

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible). Pay special attention to the load-bearing lens-guard #1 (replay-equality over draw) — is the replay test actually covering a draw sequence and non-vacuous? And lens-guard #5 (W1 in CI) — is the negative test actually a CI step, not local-only?

## OUTPUT
Write ONE valid JSON array (schema + contract in `_shared.md`) to:
`/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.2-window-draw-pipe/r1/acceptance.json`

`source` = `"acceptance"`. Only the JSON array in the file. `[]` is valid. Verify every claim against the actual code; quote exact lines in `evidence`. When done, stop.
