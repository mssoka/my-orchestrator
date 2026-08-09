# Briefing: packet-plumber-foundation-audit

- **Repo:** Packet-Plumber (`/Users/moses/code/packet-plumber`, remote: `solarity-services/Packet-Plumber`)
- **Worktree:** WORKTREE off `main` (read-only assessment — isolate from any in-tree state). PR targets main (the report).
- **Workflow:** analysis/audit (read code + architecture, assess, report). Perkins: OFF (analysis deliverable). No code changes — this is a go/no-go assessment.
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** OFF.

## Mission — the gate before full-game dev

The prototype fun-test **PASSED** (the user + kid confirm it's fun). The whole forge → pipeline existed for that verdict. Now we transition to **full game development** — building the real game on top of the prototype's S0–S4 base. But the prototype was built for fun-test *speed*, which may have left debt. **This audit assesses whether the S0–S4 foundation is production-quality enough to build the full game on, or what needs refactoring/firming first.** It's the go/no-go (+ the fix-list) before the full-game sprint starts.

## What to assess (the prototype's S0–S4 code vs the architecture)

Read **`game/`** (the prototype's Godot/GDScript code: the simulation core, the systems, the rendering) + **`_bmad-output/planning-artifacts/architecture/architecture-v1.md`** (the canon design: 8 core systems, 16 ADRs, 25 edge-case contracts) + **`_bmad-output/planning-artifacts/sprints/sprint-plan-v1.md`** (the story sequence S0–S4 built).

Assess each:

### 1. The determinism spine (ADR-10) — the foundation's foundation
- Is the **Simulation Core pure** (integer-tick, headless-safe, seeded)? Is it **separated from Godot rendering** (the sim runs without the renderer)?
- Can a **seeded run reproduce**? Does a **headless test** exercise the fun-test loop?
- This is load-bearing for fair leaderboards + reproducible runs + cheap testing. If it's compromised, the full game can't build on it cleanly.

### 2. System boundaries (the 8 core systems)
- Do **Topology, PacketFlow, QoS, Crisis, NetworkHealth, Era, Economy, Leaderboard** have the clean boundaries + interfaces the architecture specifies? Or are they tangled/coupled?
- Does the data model match: `Packet {src, dst, route}`, the `PressurePlan` demand-pairing (WEIGHTED_RANDOM dst-selection per sprint-plan-inputs)?

### 3. Debt / corners cut for fun-test speed
- What did the fast build skip, hack, or stub? (e.g., the initial comprehensibility layer was missing; color alignment was late; the "looks horrible" iteration.)
- Hardcoded values that should be data? Missing validation? Stubbed systems? TODO/FIXME markers?

### 4. Testability + test coverage
- Do headless tests exist + pass? What's covered vs the architecture's 25 edge-case contracts?
- Can the full-game stories (S5+) be built + tested on this base?

### 5. Production-readiness verdict
- **Per system**: solid (continue) / minor debt (fix-in-flight) / major debt (refactor-before-continuing).
- **Overall**: GO (continue the sprint on this base) / GO-WITH-FIXES (refactor X first) / NO-GO (the foundation's too shaky — rebuild the spine).

## Deliverable

A **foundation-audit report** at `_bmad-output/planning-artifacts/foundation-audit-2026-08-08.md`:
- Per-system assessment (solid/debt/refactor) with evidence (file:line citations).
- The determinism-spine verdict (the critical one).
- A prioritized **debt/fix list** (what to firm before the full build, ranked).
- The **overall GO / GO-WITH-FIXES / NO-GO verdict** + rationale.
- A recommended **first refactor sprint** (if GO-WITH-FIXES) — the stories to firm the base before S5+.

## Constraints
- READ + ASSESS only — no code changes. This is analysis.
- Be honest, not diplomatic — if the spine is shaky, say NO-GO. The full game's success depends on a solid base; sugar-coating debt here costs more later.
- Cite evidence (file:line) for every finding.
- Em-dashes fine in PP copy.

## Review loop (lavish — BEFORE the PR)
Analysis deliverable: render via **lavish** (the per-system scorecard, the verdict, the fix-list) + post the review URL. The user decides GO/GO-WITH-FIXES/NO-GO from your assessment.

## Acceptance
- Foundation-audit report with per-system assessment + determinism-spine verdict + prioritized fix-list + overall GO/GO-WITH-FIXES/NO-GO.
- Evidence-cited (file:line).
- After user review: commit the report, push, open PR. **Never merge** (it's a report; the verdict drives the next step).

## Self-report (do not skip)
- `/Users/moses/code/bin/ledger set packet-plumber-foundation-audit working` at start
- `/Users/moses/code/bin/ledger note packet-plumber-foundation-audit "lavish audit posted: <url>"` when up
- `/Users/moses/code/bin/ledger set packet-plumber-foundation-audit done "audit complete: <verdict>"` when finished
- `herdr notification show "pp-foundation-audit" --body "<one-line>"` on finish
- Final message: the overall verdict (GO/GO-WITH-FIXES/NO-GO), the determinism-spine finding, the top 3 debt items, lavish URL.

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: packet-plumber-foundation-audit · base: main
