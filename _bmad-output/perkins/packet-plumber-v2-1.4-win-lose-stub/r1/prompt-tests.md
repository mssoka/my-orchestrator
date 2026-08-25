You are the **Test Coverage** lens (source: `tests`).

FIRST read the shared context:
`/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.4-win-lose-stub/r1/_context.md`
Then read the diff (esp. `core/win_lose_test.odin`) and verify against the worktree.

Test coverage analysis via traceability. For each behaviour change in the diff,
trace to a test (new in the diff, or existing). Classify FULL / PARTIAL / NONE.
The 1.4 contracts are: (a) WIN scores + exactly one Run_Won; (b) LOSE tick-cap +
exactly one Run_Lost; (c) terminal barrier = one event/run + frozen state; (d)
win beats lose on a tie tick; (e) goal==0 disables; (f) byte-identical replay
over the loop incl. the terminal frame; plus independent gating (cap-only lose
with goal==0) + clean restart.

Emit one finding per gap with severity:
- blocker: P0 gap (critical path happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics: is the LOSE path covered? the tie-tick? the barrier over
MANY post-terminal ticks? restart reset (fresh seed, no leaked score/events/
terminal)? cap-only-lose (goal==0)? Is the app Mode FSM (Boot/Run/Game_Over
transitions) tested at all, or only the core? Note honestly if app-layer FSM has
no automated test (that may be acceptable for a stub — calibrate severity).

FINALLY emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"; severity PASS→note, CONCERNS→warning, FAIL→blocker
- detail: rationale with coverage %; recommended_fix: what would raise the gate
Gate thresholds: PASS = P0 100%, P1 ≥90%, overall ≥80%; CONCERNS = P0 100%, P1
80–89%, overall ≥80%; FAIL = P0<100% OR P1<80% OR overall<80%.

OUTPUT: Write ONE valid JSON array to
`/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.4-win-lose-stub/r1/tests.json`
then STOP. Schema + accuracy mandate per `_context.md`. Use `"source":"tests"`.
Quote EXACT test + code lines in `evidence`. Include the advisory-gate finding as
the last element.
