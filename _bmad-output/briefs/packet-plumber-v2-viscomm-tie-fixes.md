# Briefing — packet-plumber-v2-viscomm-tie-fixes (Perkins r1 rework on PR #99)

Skill to execute: **bmad-quick-dev** (small targeted fix; briefing is
self-contained if the skill is absent).

## Repo / workspace facts

- Repo: `/Users/moses/code/packet-plumber` (Odin `dev-2026-08` + raylib 6.0).
- Workspace: WORKTREE at branch `packet-plumber-v2-viscomm-tie-deconflict`
  @ `4b3a887` (the PR #99 head — Silas creates it; work ONLY there; NEVER
  touch the main checkout, it sits on a user branch).
- PR target branch: **v2**. Push fix commit(s) to the same branch — NO new PR.
- Read `/Users/moses/code/packet-plumber/project-context.md` first — ODN
  rules and [LOOK] canon govern.

## Task: fold the Perkins r1 verdict (CHANGES_REQUESTED) into PR #99

r1 verdict (review `PRR_kwDOTvPMrs8AAAABK0lovw`, sha 4b3a887): 1 blocker,
6 warnings, 10 notes, 7/7 lenses. Fix these, in priority order:

### B1 (BLOCKER — the vacuous mutation leg)

The r1 shape gate passes even when the feature is reverted: Silas
reproduced live — deleting the `tie_dash_on` guard in `draw_tie_mark`
(reverting to a solid ring) leaves `odin test app/render` **83/83 GREEN**.
The test does not guard the actual draw path.

Fix standard = the MUTATION LEG: deleting the dash/shape differentiation
in `draw_tie_mark` MUST fail a test. Build a capture- or geometry-level
assert (e.g. render the tie mark via `capture_frame`-style construction and
assert dash-arc geometry / segment count, so a solid ring fails). Prove it:
run the mutation (delete the guard) → tests RED; restore → GREEN. Put both
runs in your report.

### W1 — hue canon separation

`route_tie` violet (hue 264.35°) sits 14.03° from `router_tier_high`
(250.32°); canon minimum is 15°. Nudge route_tie to clear 15°+ and ADD the
router tiers to the hue test so the pair is guarded from now on.

### W2 — missing CVD oracle pair

`palcheck`/`derive` oracle lacks the `route_tie` vs `state_congested` pair
(the exact confusion this PR exists to kill). Add the pair to the oracle.

### W3 — palette.json strict-parse

`palette.json` fails a strict parse (Silas reproduced). Fix the schema
violation.

### W4 — PR body hue claim

PR body claims 225° — that is an UNWRAPPED mean; the real circular mean is
134.62°. Correct the PR body text (edit via `gh pr edit 99`).

## Acceptance

- All mutation-leg proofs (B1) shown RED-then-GREEN in the report.
- Full local suite green (app/render 83+, palcheck, hue test).
- Pushed to `packet-plumber-v2-viscomm-tie-deconflict`; CI green.
- `ledger set packet-plumber-v2-viscomm-tie-deconflect in-review "<PR url>"`
  (the sensor arms Perkins r2 at the fresh sha — do NOT dispatch r2
  yourself unless Silas orders it).

## Model policy

- Minion: `deepseek/deepseek-v4-flash`, `--thinking max`.
- Any mega-minion: pin model explicitly in the spawn prompt.

## Dispatch parameters

- repo: Packet-Plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: viscomm-tie-fixes
- base: v2
- branch: packet-plumber-v2-viscomm-tie-deconflict (existing PR #99)
- model: deepseek/deepseek-v4-flash
- pr_review: 1 (row already carries it; r2 rides the sensor)
