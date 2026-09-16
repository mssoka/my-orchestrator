# Briefing: packet-plumber-3d-l1-topology-font

Read the standing orders first: `/Users/moses/code/docs/orchestration-playbook.md`
section 'Minion standing orders'. This briefing is your task spec.

## Task

**Two post-L1 feedback fixes** (user, 2026-09-05):

1. **Router-mediated topology** — "buildings should never connect to each
   other. should be via routers."
   - The connect verb **rejects terminal→terminal** with a readable
     affordance (steer to the router — a gentle in-world hint, not an
     error wall).
   - **L1 restaged historically:** each site = **host + IMP** (the IMP is
     the router — the historical truth: hosts talked to IMPs, IMPs to
     each other). Four sites → four IMPs; the mesh is IMP↔IMP; the LOGIN
     rides host→IMP→IMP→host. Use the round router family assets for
     IMPs. The beat (draw UCLA→SRI first, mesh, LOGIN, LO crash, retry)
     is unchanged — only the grammar gains its router.
   - Tests: building→building rejected; host→IMP→IMP→host path delivers;
     determinism per level holds on the restaged seed.
2. **Font overhaul** — "the font is hard to read so we need to use a font
   that actually fits the game world theme."
   - Choose + integrate a themed, readable font (rounded/friendly/legible
     at game distances — the reference video's UI typography is the vibe;
     the frame atlas: `/Users/moses/code/_local-refs/little-planet-ref/frames/`).
   - **Open license only** (OFL-class), license + attribution recorded
     (assets/ATTRIBUTION.md or a FONTS.md). PP-Odin precedent lore:
     `/Users/moses/code/packet-plumber/_pr_body_font_overhaul.md` — read
     it for the pitfalls of that era.
   - Swap ALL UI surfaces (HUD, IMP log, prompts, clear card, QoS panel —
     grep the theme). Readability proof: captures at game resolution.

## Acceptance

1. Topology law enforced + tested (rejection affordance captured); L1
   plays the beat through the IMP grammar; per-level determinism holds.
2. Font live on every UI surface; license recorded; before/after captures
   in the PR; suite green; LSP clean; `godot --headless --import` clean.
3. PR body: run command + captures + Decisions.

## Model policy / Skills / Perkins

Minion: `zai-coding-cn/glm-5.3-flash` (natively multimodal — verify the
font readability yourself on captures). Workflow: `gds-quick-dev`.
`pr_review=1` (canon-surface grammar + UI).

## Dispatch parameters

```
job_id:    packet-plumber-3d-l1-topology-font
repo:      packet-plumber-3d
slug:      l1-topology-font
base:      main
model:     zai-coding-cn/glm-5.3-flash
pr_review: 1
notes:     Worktree from origin/main (5a5d5d0). _bmad bootstrap. PARALLEL
           LANES: gdd-amend-alive-planet (docs) + alive-planet art (code)
           — disjoint files (yours: connect grammar, L1 staging, UI theme).
```
