You are reviewing a code diff. You have read-only access to the repository (your cwd is the reviewed worktree) and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
<!-- AGENTS.md — Packet-Plumber-UE agent instructions.
     Provenance: bootstrap job packet-plumber-ue-bootstrap, 2026-08-20.
     This block is the repo's agent contract; read it before any work. -->

# Packet-Plumber-UE — agent instructions

## Mission

Second Packet Plumber implementation on UE 5.8.x, built to compare against
the Odin v2 build (packet-plumber repo) and decide by evidence. Same game,
second engine: the GDD is canon, routing canon [RR] and determinism rules
[ODN-*] carry over. Do NOT re-decide design; port the spine.

## Running and verifying

- **Pre-engine loop (always works):**
  - `scripts/local-ci.sh --fast` — format, spine, static gates.
  - `tests/build/spine-check` — the determinism conformance runner (compiles
    the same headers the engine module uses; exit 0 = the ODN-9/11 contract
    holds). Rebuild it after ANY spine change:
    `mkdir -p tests/build && g++ -std=c++17 -O2 -I Source/PacketPlumberCore/Public tests/spine_check.cpp -o tests/build/spine-check`
- **Engine-gated (UE 5.8 installed):**
  - `scripts/local-ci.sh` — full suite incl. UBT build + headless automation
    tests + PPProbe + golden compare.
  - `scripts/run-tests-headless.sh --tests|--probe|--build-only`.
  - First build 30-60+ min; incremental 5-15 min. Plan gate runs around it.
- **MCP / editor driving:** see `docs/agent-playbook.md` — the UE-MCP server
  (`.mcp.json`, stdio) plus the official Unreal MCP plugin; screenshots go
  through `bin/vision-read` (fails loudly without a vision backend — never
  guess image content; flash/glm have no native vision).
- **Engine install/upgrade:** `scripts/install-engine.sh` (manual step,
  documented) — and the 5.8→5.9 path in `docs/research-report.md`.

## Conventions

- **C++-first.** Blueprints only where unavoidable, and documented in the
  PR. A change that adds Blueprint-authored logic without a doc note will
  be sent back.
- **Determinism spine discipline (the ODN port — non-negotiable):**
  - All state-affecting sim math is **integer** (ODN-10). Floats never flow
    back into state.
  - The sim owns its PRNG (`PP::FRng`, ODN-9) — never `FMath::Rand`,
    `FRandomStream`, or any engine/global RNG inside sim state paths.
  - No `TMap`/`TSet` iteration in sim state paths (iteration order is
    unspecified) — arrays + insertion order, lookups may use maps (ODN-10).
  - Serialization is **explicit little-endian field-by-field** (ODN-11) —
    never raw `memcpy` of structs (padding is not portable).
  - Every spine change re-runs `tests/build/spine-check` AND the UE-side
    `PacketPlumber.*` automation tests; pinned vectors are the
    cross-runner contract (same seed → same numbers everywhere).
  - Replay-equality: same (seed, action log) → byte-identical state hash.
  - Forwarding table rebuilt only on topology change, inside the tick;
    ECMP next-hop = pure splitmix64 hash of packet identity; bundle capacity
    = static sum at table-build time (routing 4-rule, lavish 2026-08-10).
- **Fixed tick:** the sim steps at 20 Hz (ODN-2; `bUseFixedFrameRate` is
  pinned in `Config/DefaultEngine.ini`). `PP::Step` is the only sim advance.
- **Golden discipline:** a golden change is deliberate + proven (see
  `docs/goldens/` + `scripts/compare-golden.sh`). Never re-bless to dodge a
  mismatch — explain the state change first. Two surfaces pin the golden
  numbers: the committed `docs/goldens/probe-seed42-ticks100.json` AND the
  inline CHECKs in `tests/spine_check.cpp` — re-blessing means updating
  BOTH (compare-golden.sh also checks the engine probe
  `docs/goldens/.engine-probe.json`, written by gate 6, when present).
- **Env/config files are read-only** unless the task says otherwise; never
  commit secrets. `Config/*.ini` changes are code review surface.
- **MCP server state** (`.mcp.json` and the UE-MCP flows it drives) is
  committed project config — changes ship in the PR, not in `Saved/`.

## Where things are

- Sim spine: `Source/PacketPlumberCore/Public/PacketPlumberCore/`
  (`PP_Rng.h`, `PP_Hash.h`, `PP_SimState.h`, `PP_Sim.h` — UE-header-free,
  dual-runner).
- UE automation tests: `Source/PacketPlumberCoreTests/`.
- Headless probe: `Source/PacketPlumberEditor/PPProbeCommandlet.*`
  (`-run=PPProbe -seed=42 -ticks=100`).
- CI + scripts: `scripts/`.
- Research/design docs: `docs/` (`research-report.md` is the reviewed gate;
  `architecture-ue-v1.md` + `slice-map-ue-v1.md` + `stories-ue-v1.md` are the
  UE-native build plan — lavishly reviewed 2026-08-20, the gate before any
  build; `agent-playbook.md` is the MCP/vision recipe).
- Golden probes: `docs/goldens/probe-seed42-ticks100.json`.
- Odin reference (read-only canon): `/Users/moses/code/packet-plumber`
  (GDD + `odin-architecture-v1.md` ODN spine + `core/` ports).

## Pitfalls (from the bootstrap + sibling-repo field notes)

- The briefing's `repo_root` names the MAIN checkout
  (`/Users/moses/code/packet-plumber-ue`) — work happens in YOUR worktree;
  pin the worktree path first (`pwd` + `git branch --show-current`) and use
  it for every file/git command.
- Gate scripts must not false-green: missing binaries fail loudly, gate
  counts derive from the gate list, success is asserted on artifacts (logs,
  JSON), not just exit codes. See `scripts/run-tests-headless.sh` for the
  log-grep truth checks.
- `npx -y lavish-axi` builds: write HTML via file (never a pipe —
  ~85KB truncation); `end` your own session, never `stop` (shared server).
- UE module boilerplate is engine-API surface: if the engine version
  changes (5.8 → 5.9), re-verify `BuildSettingsVersion`, plugin ids, and
  `EAutomationTestFlags` names against the installed engine before
  trusting a green build.


--- DIFF ---
The canonical diff chunk for this review wave is saved at:
  /Users/moses/code/_bmad-output/perkins/packet-plumber-ue-slice-1/r3/chunk-view.patch
Read that file FIRST and review exactly those bytes. (The canonical PR diff was split by file group into chunks; chunks other than yours are out of scope for this run. Plugins/ is reviewed under a separate provenance verdict and is out of scope.)

--- SPEC / CONTEXT ---
# Briefing: packet-plumber-ue-slice-1

## Mission

Execute SLICE 1 of the UE port — the first vertical slice, whose job is to
answer THE question: can UE render Packet Plumber in the Mini Motorways
look? The plan docs are canon and freshly merged to main (PR #2 @
`978ee8d`): `docs/slice-map-ue-v1.md` + `docs/stories-ue-v1.md`.

Scope = the stories the slice-map assigns to slice 1, in order:
- **Story 0.1** — MCP screenshot proof (the W3 fold): the ue-mcp loop
  (.mcp.json bridge + editor `-ModelContextProtocolStartServer`) drives a
  headless/editor capture of a rendered frame. This screenshot loop IS the
  look-parity delivery vehicle.
- **Story 1.1 → 1.2 → 1.3** per stories-ue-v1.md — static fixture render in
  the MM look (warm-cream palette, ribbon roads with rounded casing, soft
  blob shadows, clean AA per **UAD-22**), then MM-style motion easing
  (presentation-only, NEVER sim state — 20 Hz snapshots, eased in the view
  layer).

## Acceptance

- Every story's exit criteria from stories-ue-v1.md, checked off.
- Engine gates stay green (the 7/7 suite incl. engine-golden 3-way);
  determinism spine UNTOUCHED — zero sim-state changes in this slice.
- Fast gates 3/3 green in the PR.
- **PR body carries the look-parity evidence**: side-by-side UE frame vs
  the actual Mini Motorways + the checklist score from the slice-map.
  IP GUARDRAIL: the MM reference frame stays LOCAL (never committed) —
  the committed surface is the UE frame + the checklist score.
- IP note: engine-first build is 30-60 min; plan gates around it
  (scaffold work while the first build runs).

## Skills policy

- Workflow: `gds-dev-story` — the stories exist (stories-ue-v1.md); execute
  them, do not re-plan. GDD/architecture are the canon under
  `docs/canon/` + `docs/architecture-ue-v1.md`.
- Screenshots/image reads: `bin/vision-read` (the local vision model) —
  never guess image content.

## Model policy

- `deepseek/deepseek-v4-flash` + `--thinking max` (launch pin).
  Perkins round (pr_review=1): glm-5.3 (k3 capped; probe first per
  standing doctrine).

## Dispatch parameters

- repo: packet-plumber-ue
- repo_root: /Users/moses/code/packet-plumber-ue
- slug: slice-1
- base: main (resolve FRESH head at dispatch — post-#2-merge)
- model: deepseek/deepseek-v4-flash + thinking max
- pr_review: 1


--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80-89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- New/modified API endpoints without matching coverage
- Auth/authz paths missing negative tests
- Happy-path-only coverage where error handling is implied
- New DB operations without integration coverage
- New state transitions without boundary tests

Test level mix (unit/integration/E2E): flag mismatches as findings.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds:
- PASS: P0 100%, P1 ≥90%, overall ≥80%
- CONCERNS: P0 100%, P1 80-89%, overall ≥80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Write ONLY the JSON array to the output file named below, then stop. No prose anywhere else.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

OUTPUT FILE (write your JSON array here — exact absolute path, do not derive it):
  /Users/moses/code/_bmad-output/perkins/packet-plumber-ue-slice-1/r3/tests-chunk-view.json
Write the file, verify it parses as a JSON array, then stop.