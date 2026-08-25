# Briefing: Packet-Plumber-UE — bootstrap (engine-comparison track)

**Job id:** packet-plumber-ue-bootstrap
**Repo:** packet-plumber-ue (NEW — created by this job)

## Mission

The user wants a SECOND Packet Plumber implementation on **Unreal Engine**,
to compare against the Odin v2 build and decide by evidence. Requirements
(user, 2026-08-20): UE **5.9**-targeted, **MCP set up**, **optimized for
AI-agent workflow**. Reality check: 5.9 is confirmed-in-development (Unreal
Fest Seoul 2026; AI workflows are the headline — expanded official MCP
plugin, Epic Developer Assistant w/ project context + screenshots, semantic
search) but NOT yet released (~Nov/Dec 2026). **Therefore: scaffold on UE
5.8.x now (official MCP plugin v1 lives there), pin the 5.9 upgrade path.**

## Deliverables

1. **Repo + project scaffold.** New repo `packet-plumber-ue`
   (solarity-services/Packet-Plumber-UE), git init, .gitignore tuned for UE
   (uasset filtering rules — decide the LFS/binary strategy explicitly),
   README stating the comparison mission. C++ project (agents can't diff
   Blueprints — C++-first is an AI-workflow requirement; Blueprints only
   where unavoidable, documented). UE 5.8.x installed via Epic Launcher CLI
   if scriptable, else document the manual step.
2. **MCP integration.** Enable Epic's official MCP plugin (5.8) in the
   project; evaluate the community `UE-MCP` (github.com/db-lyon/ue-mcp,
   783+ actions) for gap-filling. Wire ONE of them into the orchestrator's
   MCP config (.pi MCP setup — coordinator task with Silas if needed).
   Document what the agent can drive: editor, assets, builds, screenshots.
3. **AI-workflow optimization (the core ask).** Port the PP-Odin agent
   discipline to UE:
   - **AGENTS.md + project-context** for the repo (bmad-project-context
     skill) — agent rules, build commands, conventions.
   - **Headless-first**: Unreal AutomationTests + a commandlet entry
     (determinism spine port: seeded RNG, state hash, replay equality —
     the v2 slice-1 equivalent) runnable WITHOUT the editor GUI.
   - **Local CI script** (the local-ci-suite replica pattern): format
     (clang-format), build, test, goldens — with timing expectations
     documented (UE builds are heavy; first build 30-60min+).
   - Screenshot loop: MCP-driven editor screenshots for vision-read
     verification (the harness T2-pixel-golden equivalent).
4. **Technical research report (LAVISH — reviewed by the user before any
   architecture work):** UE 5.9 timeline + AI features; MCP landscape
   (official vs community, what agents can/can't drive today); determinism
   in UE (fixed tick, seeded streams — what's possible vs Odin's spine);
   comparison CRITERIA for the two engines (agent drivability, iteration
   speed, headless testability, build times, binary size, platform reach);
   recommended slice-1 scope for the comparison build; the 5.8→5.9 upgrade
   path. Cite sources.

## Canon

The game design is the existing PP GDD (packet-plumber repo,
`_bmad-output/planning-artifacts/gdds/`) — same game, second engine. Do NOT
re-decide design; port the spine. Routing canon [RR] (per-hop forwarding,
ECMP, bundles) and determinism rules [ODN-*] carry over as requirements.

## Acceptance

- Repo exists, C++ builds headlessly, automation test skeleton runs green.
- MCP wired: an agent command can drive the editor (screenshot or asset
  query proven in the PR body).
- Local CI script runs the full loop once, timings recorded.
- Lavish report delivered + user-reviewed (the gate before architecture).
- managed-repos.txt updated (packet-plumber-ue) — do via Silas/Gru, not
  the repo itself.

## Skills policy

- **bmad-build** (implementation), **bmad-deep-recon** (the research
  report), **bmad-project-context** (AGENTS.md), **lavish** (report
  review artifact).

## Model policy

- Minion: pi default (ops tier — deepseek/deepseek-v4-flash) + thinking max.
- Perkins round on the PR head (reasoning tier, glm/k3 per regime).

## Review

- `pr_review: true` — the determinism-spine scaffold is canon-surface.

## Dispatch parameters

- repo: packet-plumber-ue (NEW — Silas: create repo + GitHub, then normal
  worktree flow)
- repo_root: /Users/moses/code/packet-plumber-ue
- slug: bootstrap
- base: main (initial)
- pr_review: 1
