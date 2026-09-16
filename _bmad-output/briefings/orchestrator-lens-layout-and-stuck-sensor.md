# Briefing — orchestrator-lens-layout-and-stuck-sensor

## Context (user ruling re-invoked 2026-09-07)

The lens-tab doctrine (MAX 6 panes/tab, 3 rows × 2 cols, built AT CREATION —
user ruling 2026-08-23) has been violated REPEATEDLY because it lives in the
playbook, not in the spawn code. Tonight's lens-wave-r5: 10 panes in ONE tab
at widths 1/0/1/2/3/7/14/27/55/110 — unreadable, and the user could not see
which lens was frozen. Two deliverables:

## 1. Wave-spawn layout enforcement (code-review skill)

Fix the lens wave-spawn surface (the code-review skill's headless spawn
template/script — `~/.agents/skills/code-review/`, canonical home
`/Users/moses/code/.agents/skills/code-review/`):

- **MAX 6 panes per tab** — waves >6 lenses chunk across additional tabs
  (labels: `lens-wave-<round>b`, `-c`, …). 7 lenses = 6+1 (or 4+3).
- **Build a GRID at creation, never a split ladder**: per tab, 2 columns ×
  3 rows — first split down (2 rows), then each row splits right (or
  equivalent), with explicit `--ratio` floats so panes land ~even with NO
  post-hoc resize surgery needed.
- Keep the existing pins: `--cwd <worktree>` per lens, model pin, thinking
  pin. bash-3.2-safe (NO associative arrays in the wave script — known
  collapse class).
- Acceptance: a dry-run wave (spawn N dummy panes in a scratch tab, then
  close them) produces the grid shape at even sizes for N=6, 7, 10; `herdr
  pane layout` output attached as proof. Zero-pane-collateral: close ONLY
  the dummy panes you created (cwd-exact).

## 2. nefario-watch stuck-pane sensor (new, detection-only)

Add to `.pi/extensions/nefario-watch.ts` (8th sensor; round-debris PR #14 is
the shape precedent — DETECTION-ONLY, one alert until resolved, never
closes/continues/removes; execution stays with Silas):

- **stuck-working**: a tracked pane whose agent_status=working with NO
  session-jsonl growth (size or mtime) for N minutes (configurable;
  default 15).
- **error-never-retried**: a pane whose session tail shows an errored turn
  (`stopReason:"error"` / "Retry failed after N attempts") with no
  subsequent session growth for N minutes (default 10) — the class the user
  keeps finding by hand.
- Alert carries: pane id, tab label, cwd, classification, minutes-stuck.
  cwd-exact matching; dedup (one alert per incident until resolved).
- Sensor-doctrine-sync: grep the new sensor text against retired doctrines;
  config stays in the extension's existing pattern.

Acceptance: a kill-test — pause/simulate a stuck pane (e.g. spawn a pi, kill
its provider turn or leave it idle-on-error), verify the sensor fires ONCE
with the right classification, verify healthy panes stay silent, verify no
auto-action of any kind.

## Mechanics

- Repo: orchestrator root — WORKTREE dispatch (the root is Gru+Silas' live
  home; never branch-switch the main checkout).
- pr_review=0 (ops-tooling class). No lavish. Tests/proofs in the PR body.
- Skills: bmad-quick-dev.

## Dispatch parameters

- repo: orchestrator root (/Users/moses/code — the my-orchestrator remote)
- repo_root: /Users/moses/code
- slug: orchestrator-lens-layout-and-stuck-sensor
- base: main
- pr_review: 0
- worktree: REQUIRED (orchestrator-root doctrine)
