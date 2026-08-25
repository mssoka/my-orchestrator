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
