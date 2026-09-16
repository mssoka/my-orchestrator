# Briefing: packet-plumber-3d-l1-arpanet

Read the standing orders first: `/Users/moses/code/docs/orchestration-playbook.md`
section 'Minion standing orders'. This briefing is your task spec.

## Task

**Build Level 1 — ARPANET (1969), "LO"** — the campaign's first playable
level and its tutorial. Spec of record: GDD v2
`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-3d-2026-09-04/gdd.md`
section **"Level 1 — ARPANET (1969): fully specified"** + the level-manifest
framework + the tech-unlock ladder. The GDD's L1 section IS your acceptance
spec — this briefing restates the load-bearing points only.

**The beat (verbatim):** *draw the first link. Deliver the first message.
Watch history crash — and try again.*

## The level (from canon)

1. **The planet:** a small arpa-blue world, exactly **four nodes — UCLA,
   SRI, UCSB, Utah** (labeled, one per biome wedge), node cap 4.
2. **The task flow:** guided first draw (**UCLA → SRI**, as history did) →
   link all four into one net → **send the first message: the LOGIN**.
3. **The scripted first crisis:** the transmission starts, the far node
   stutters, **dies after "LO"** — an in-period **IMP log alert** walks the
   player through the retry (one retry recovers; zero blame, foreshadowed
   by the beat itself). Retry → LOGIN delivers end-to-end.
4. **Mechanics live (the manifest flags):** draw+snap · Narrow tier only ·
   typeless packets (dots with a destination, NO type UI) · **link
   congestion read 🟢/🔴** (flat-shaded glow along the cable + outline,
   colorblind-safe, readable across the zoom ladder — NO 🟡 yet) · the LO
   scripted beat.
   **OFF (flag out, provably inert — tests pin it):** QoS, class lanes,
   bundles, SLA surfaces, junctions, forecast HUD.
5. **Win:** all four linked + LOGIN delivered → level-clear beat closes,
   **the rocketship waits** (a simple clear-card + rocket tease; the
   campaign map/constellation is E10.7 — OUT of scope).
6. **Per-level determinism:** authored demand script (peak → breath →
   peak) + fixed seed; replay byte-identity **per level**.
7. **Tutorialization:** L1 IS the tutorial — just-in-time diegetic prompts
   for rotate / draw / deliver; no manual, no walls of text.
8. **Boot flow:** the game boots to L1 (a title/intro card → the arpa
   planet). Level select / campaign shell is future content.

## Implementation anchors

- **`scenes/levels/` scaffold + `level_base`** (merged in the refactor) is
  your foundation — L1 lives at `scenes/levels/` per its pattern.
- The **level manifest is data, not code** (the GDD's manifest fields:
  beat / planet / mechanic flag set / demand script / target contract) —
  the E1–E2 engine executes it; gating is config.
- Editor preview must work for the L1 scene (auto-generate path, merged).

## Acceptance

1. The full L1 spec above demonstrable; the beat sequence plays start to
   finish (draw → mesh → LOGIN → LO crash → IMP-log retry → delivered →
   clear card + rocket).
2. **Flag purity pinned by tests:** the OFF list is provably inert in L1
   (no QoS panel reachable, no bundles possible, no SLA surfaces); the
   manifest flags are test-pinned.
3. **Determinism:** per-level replay byte-identity on the authored
   script + seed; suite green with new L1 tests (non-vacuous — mutation
   legs where meaningful).
4. **Congestion read:** visible on pipes across the zoom ladder; captures
   committed proving 🟢 and 🔴 states + the LO moment + the clear card.
5. **Godot MCP** as your build/verify surface (editor-run, debug-output,
   lsp-diagnostics). You are natively multimodal — attach your captures
   and verify the look yourself before claiming.
6. PR body: run command for the user + capture walkthrough + Decisions.

## Model policy

Minion: **`zai-coding-cn/glm-5.3-flash`**. Mega-minions: same, skills named.

## Skills policy

Workflow: **`gds-quick-dev`**. No lavish (code deliverable — the USER-PLAY
gate is the review that matters).

## Perkins

`pr_review=1` — canon-surface (first level, the tutorial, the scripted
crisis). Loop-until-APPROVED.

## Dispatch parameters

```
job_id:    packet-plumber-3d-l1-arpanet
repo:      packet-plumber-3d
repo_root: /Users/moses/code/packet-plumber-3d
slug:      l1-arpanet
base:      main
model:     zai-coding-cn/glm-5.3-flash
pr_review: 1
notes:     Worktree from origin/main (d2e733c, post-refactor). _bmad
           symlink bootstrap. After APPROVED + merge: the L1 play session
           is the gate — it rules the level AND the E2 engine together.
```
