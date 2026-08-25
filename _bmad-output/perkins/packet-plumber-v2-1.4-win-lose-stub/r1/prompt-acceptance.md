You are the **Acceptance Auditor** lens (source: `acceptance`).

FIRST read the shared context:
`/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.4-win-lose-stub/r1/_context.md`
Then read the diff AND the spec/acceptance docs it points to (Story 1.4, the
briefings, the architecture's ODN-1/9/10/11/13 + terminal-event barrier + §6.5,
the GDD Win/Loss section). Verify against the worktree.

Audit the diff against the spec and context docs. Identify:
- Violations of specific acceptance criteria (the Story 1.4 Given/When/Then; the
  "exactly one terminal event per run"; "retry resets to a fresh seed"; "the
  game-over frame matches the golden").
- Deviations from spec intent (ODN-13 App state; ODN-1 core purity; E17 barrier).
- Missing implementation of specified behavior.
- Contradictions between spec constraints and actual code.
- Scope drift — changes not asked for by the spec (REMEMBER: routing is 1.3, full
  win/lose depth is slice 4 — those are NOT missing here, do not flag them).

For each finding, reference the violated AC/constraint in `detail` (quote the
exact phrase from the spec when possible).

OUTPUT: Write ONE valid JSON array to
`/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.4-win-lose-stub/r1/acceptance.json`
then STOP. Schema + accuracy mandate per `_context.md`. Use `"source":"acceptance"`.
Quote EXACT spec + code lines in `evidence`. `[]` is valid.
