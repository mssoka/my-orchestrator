# Perkins round r1 — Packet-Plumber PR #97 (camera zoom tiers)

**Role: Perkins.** You review; you never fix, push, or merge. You never touch the implementing worktree or pane (there is no minion here — see Context).

## Context

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/97
- **Reviewed sha:** `9bf97978adfce9d8dc1df28724fc9f3ecd3c2f71` (headRefOid, verified at dispatch)
- **Repo root:** `/Users/moses/code/packet-plumber` (main checkout, branch `v2`)
- **Your cwd:** `/Users/moses/code/.herdr/worktrees/pp-camera-zoom-tiers-r1` — a DETACHED worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- **This is a USER-INITIATED PR** (user wrote the code and opened it 2026-08-24 20:31Z). There is NO minion job row and NO minion pane. Your verdict routes to Gru (the user interface); findings become follow-up jobs. Do not expect a relay back to an implementer.
- The user already posted an informal "Orchestrator review — approve with notes" (COMMENTED, as mssoka) at 20:32Z. That is NOT a Perkins verdict and NOT a formal approve — your independent review is what counts.

## Your spec

The PR body IS the spec (user directive 2026-08-23: "default should be zoomed in… extra zoom in for node/link click, zoom out is just to see all the links"). Key claims to verify:

- **A. Three-tier zoom:** `DEFAULT_ZOOM=2.0` resting home at the source-cluster centroid; boot/run-reset/deselect home via `camera_set_default`; `camera_set_fit` demoted to manual wheel-out floor (1.0); focus 2.3/2.6 unchanged; pullback floor now 2.0 (documented tradeoff: distant seed may sit at viewport edge rather than forcing full-out).
- **B. Terminal blocks:** `DUBLIN_NODE_BLOCK_L/W` 0.40/0.22 → 0.55/0.30 (street-aligned; sized against a street lane).
- **C. Pucks:** base 1.15→1.05, `PUCK_GROWTH_MAX=1.30` cap (tier ratios ≤1.27 inside the cap — cap is future-proofing; visible change ~9% shrink; palcheck passed, no re-pin).
- **D. Tests/goldens:** new pins for DEFAULT_ZOOM / cluster home / 2.0 floor; 113 T2 re-blessed with proven cause; T1 untouched (sim spine intact).
- **ESC homes via `camera_set_default`** — a flagged extension beyond the brief's enumeration; the user's review agrees it's justified.

## Lens-run mechanics

Per the `code-review` skill's **Headless / Automated Mode**:
- `diff_file` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom-tiers/r1/diff.patch` (975 lines — single chunk, no chunking needed)
- `worktree` = your cwd (the detached round worktree)
- `spec_files` = this briefing (no GitHub issue exists — user PR, no issue)
- `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-camera-zoom-tiers/r1`
- `prior_findings` = none (fresh r1)

**Lens-spawn rooting:** every lens pane MUST pin `--cwd <worktree>` at spawn — a lens pane whose cwd is not the round worktree is mis-rooted (close + relaunch).

**VISION CAVEAT (this is a NON-k3 round — glm-5.3):** pixel verification MECHANICAL only (byte/hash/capture-diff); aesthetic verdicts deferred for the k3 re-check, never faked. The PR's goldens/re-bless claims must be verified mechanically (golden bytes, camera math, tier table), not by eye.

You MUST close every lens pane before finishing.

## Verdict → review event

- 0 blockers → `--approve`
- 1–3 blockers → `--request-changes`
- 4+ blockers → `--request-changes`, body leads with "MAJOR REWORK"
- Degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.

Post as the app (owner `solarity-services`):
1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — capture STDOUT ONLY (never `2>&1`). Empty token → `gh pr comment` fallback + note.
2. Re-fetch `headRefOid` before posting; if moved, post anyway + note it.
3. `GH_TOKEN=$TOKEN gh pr review 97 --<event> --body-file <body.md>` (write `body.md` in `out_dir` first).

## Close-out (you self-report; Silas sweeps)

- `bin/ledger set packet-plumber-v2-camera-zoom-tiers-perkins-r1 working` at start.
- Final message = verdict + review URL + findings counts.
- Ledger row: `packet-plumber-v2-camera-zoom-tiers-perkins-r1` (pr_review=1, model glm-5.3).
