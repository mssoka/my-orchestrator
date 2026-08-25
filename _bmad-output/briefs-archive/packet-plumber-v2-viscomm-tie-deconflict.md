# Briefing — packet-plumber-v2-viscomm-tie-deconflict

Skill to execute: **bmad-quick-dev** (small targeted code fix; if the skill is
absent from your catalog, follow this briefing directly — it is self-contained).

Model note: this dispatch runs on the DSH session default. If you spawn any
mega-minion, pin its model explicitly in the spawn prompt and record it in
your final ledger note.

## Repo / workspace facts

- Repo: `/Users/moses/code/packet-plumber` (Odin `dev-2026-08` + raylib 6.0).
- Your workspace is the WORKTREE `/Users/moses/code/packet-plumber-wt-viscomm-tie`
  (already created, branched `packet-plumber-v2-viscomm-tie-deconflict` off
  `origin/v2` @ 9622ef5). Work ONLY there. NEVER touch the main checkout
  (it sits on another branch) or any sibling worktree.
- PR target branch: **v2** (NOT main).
- Read `/Users/moses/code/packet-plumber/project-context.md` (repo root of the
  main checkout, same content in your worktree) before coding — the ODN rules
  and [LOOK] canon govern.

## Problem (finding A of the vis-comm audit, 2026-08-25)

Gestalt similarity: things that look alike read as related. Two UNRELATED
meanings currently share shape AND hue:

- `state_congested` = `{242,181,68,255}` — the node-warning telegraph ring
  (app/render/node_health.odin). Meaning: "this node is strained — act."
- `route_tie` = `{242,181,68,235}` — RGB-IDENTICAL (alpha differs 20/255) —
  the equal-cost split mark (app/render/assist.odin `draw_tie_mark`, a
  `DrawCircleLinesV` ring centered on the split node + the caption
  "equal cost - split by hash"). Meaning: "routing info, nothing is wrong."

A player who learns "amber ring on a node = congestion warning" will misread
the tie mark as a warning, or worse, learn to ignore amber rings outright.
(`sel_halo` {232,181,68,90} and `lane_express` {224,138,46,255} share the
amber family too but draw on pipes/bands, not node rings — OUT OF SCOPE here;
noted in the findings file.)

Source analysis (context, not required reading):
`/Users/moses/code/dsh-orchestrator-setup/_bmad-output/viscomm/findings.md`.

## Task

De-conflict the tie mark from the warning telegraph, BOTH levers:

1. **Hue**: move `route_tie` out of the amber warning family in
   `data/palette.json` (+ the inline fallbacks in `app/render/palette.odin`
   `palette_load` AND `fallback_palette` — three places, one value each).
   Pick a hue that reads "informational/neutral-explanatory", NOT in the
   warm-danger family, and that keeps >=15 deg hue separation from the pipe
   tier family (copper-orange/steel-cyan/gold) so the ring never reads as a
   pipe tier. A cool violet or deep teal family is the natural candidate;
   you decide, and justify the pick in the PR body against the canvas
   (#EDE2C8) contrast.
2. **Shape**: make the tie mark's geometry distinct from the warning ring —
   e.g. a DASHED ring (arc segments) or a double concentric ring — so even
   an 8-bit colorblind read cannot confuse the two. Keep the existing
   caption text (ASCII, lint gate 6). Keep it deterministic (integer/lookup
   math only — see PULSE16 precedent; no transcendendentals in draw paths).

## Constraints (hard)

- **Never color alone** stays: the tie mark keeps ring + caption; the
  warning telegraph keeps ring + glyph + pulse.
- **Golden safety is a claim you must PROVE**: `draw_route_glow`/`draw_tie_mark`
  are called ONLY by the app (harness `capture_frame` invokes `draw_world`
  with no assist args — see assist.odin's own header comment). Therefore a
  full `tools/harness.sh run` must pass with ZERO re-blessed goldens. If ANY
  golden shifts, STOP — that means the golden-safety premise is wrong; report
  it in the PR instead of re-blessing.
- **palcheck separation**: `tools/harness.sh palcheck` must pass. The a11y
  mode tables (palette.json "modes") override Route_Tie under CVD; if the new
  base color breaks pairwise separation under any deficiency, re-derive the
  tables with `tools/derive_a11y_palettes.py` (that script owns the modes
  output) and state it in the PR.
- Palette is DATA (ODN-5): art tuning lives in `data/palette.json`; the Odin
  fallbacks mirror it. The packet-types CATALOG is golden-poison — do not
  touch it.
- ASCII-only string literals (lint gate 6).

## Acceptance criteria

1. `route_tie` no longer shares its hue family with `state_congested`
   (target: clear hue-family exit, not a nudge — justify in PR body).
2. The tie mark is shape-distinct from the warning ring (dashed or double
   ring implemented; caption unchanged).
3. **Mutation leg (vacuous-pin doctrine)**: a test that FAILS when `route_tie`
   reverts to the amber value or when the shape distinctness is deleted.
   Extend `app/render/palette_polish_test.odin` (existing precedent) to pin
   the hue separation between `route_tie` and `state_congested`, and add a
   guard for the new mark geometry (e.g. the dash/segment count or the
   double-ring radii constant — whatever you implement, pin it). Prove the
   leg by actually flipping the value locally and watching the test fail;
   report that you did.
4. `odin test core` green; app render tests green (`odin test app` — the
   `*_test.odin` files in app/render); `tools/lint.sh` clean;
   `tools/harness.sh palcheck` green; `tools/harness.sh run` green with
   zero golden diffs.
5. PR opened against **v2** with a body covering: the gestalt rationale, the
   hue pick justification, the mutation-leg proof, and the verify-command
   outputs. PR body file convention: `_pr_body_*.md` at repo root (see
   existing examples).
6. Perkins round: after the PR is open, STOP and report — Gru runs the
   Perkins review round. Human merges, always.

## Verify commands (run from the worktree root, in this order)

```bash
odin test core
odin test app
tools/lint.sh
tools/harness.sh palcheck
tools/harness.sh run
```

## Ledger self-report (mandatory)

Ledger CLI: `/Users/moses/code/dsh-orchestrator-setup/bin/ledger`.
Your row id: `packet-plumber-v2-viscomm-tie-deconflict` (already dispatched).
- On first output: `ledger set <id> working "worktree up, reading canon"`
- When the PR opens: `ledger set <id> in-review "<PR URL>"` THEN
  `ledger pr <id> <PR URL>` (set does NOT populate the pr field) — verify
  with `ledger show <id>`.
- Same-status updates: `ledger note <id> "<text>"` (set refuses same-status).
- On finish: final note with the PR number, the hue you picked, the
  mutation-leg proof statement, and verify results.
- Do NOT mark done — the human merge closes the row (Gru handles it).

## Memory

Append <=3 one-liner lessons to `_bmad-output/field-notes/<job-id>.md` in the
ORCHESTRATOR root (`/Users/moses/code/dsh-orchestrator-setup/_bmad-output/
field-notes/`), not the repo.
