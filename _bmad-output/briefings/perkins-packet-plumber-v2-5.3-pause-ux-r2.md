# Perkins briefing — round 2: packet-plumber-v2-5.3-pause-ux

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/49 (targets `v2`)
- **Reviewed sha:** `bfdd7c500862b3bd0764bd861d88cabe4bcd81fc` (short `bfdd7c5`) — r1 (57eeda7) + a BASE MERGE of origin/v2 (the 5.7 telemetry merge 4a94fcb landed in v2)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 2 of 3 — **DELTA/fix-audit on the base-merge** (`prior_findings` = r1)
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.3-pause-ux-r2` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** GitHub issue **#48** + the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-5.3-pause-ux.md` + **r1's `consolidated.json`** at `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.3-pause-ux/r1/consolidated.json` + the r1 review body (4941491462).
- **Model:** `zai-coding-cn/glm-5.3` (Perkins reasoning tier — live). Launch EVERY lens pane with `pi --model zai-coding-cn/glm-5.3`. Interim fallback: `deepseek/deepseek-v4-pro`.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **CI note:** CI billing FIXED (checks green); local verification at the sha remains ground truth.

## What changed since r1 (the delta to audit)

r1 = APPROVED (0 blockers; 3 advisory warnings — W1: pause chip overlaps the
forecast panel below window width 1220px; W2/W3 styling/typo-level). The head then
moved 57eeda7 → bfdd7c5 via **`Merge branch 'v2' into v2-5.3-pause-ux`** — the v2
base absorbed the **5.7 runtime-telemetry merge (4a94fcb)**, and BOTH 5.7 and
5.3-pause-ux touched `app/main.odin` (5.7 added the per-step stats emission +
debug overlay plumbing; 5.3-pause-ux changed the pause overlay presentation). This
round audits THAT merge.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 LOAD-BEARING — the merge must not have lost/overwritten a hunk.** r1 verified the
  pause-ux change (no dim veil, edge chip @ win_w/2+240, presentation-only scope,
  canon lines, goldens byte-identical). Verify at bfdd7c5 that: the edge-chip pause
  indicator is still present + correct, the dim veil + center text are still gone,
  the 5.7 stats emission/overlay plumbing is present and intact, and NO hunk from
  either side was silently dropped by the merge (diff r1's 57eeda7 state vs bfdd7c5
  for the pause-ux files). A dropped/regressed hunk = a blocker.
- **🚨 Determinism + golden-safety (carried):** 25/25 demos goldens byte-identical at
  bfdd7c5 (both the pause-ux presentation and 5.7's telemetry must not shift them);
  the determinism contract (paused window one repeated T1 hash, exact-tick resume,
  replay [E10]) holds. `odin test core` 158+ green.
- **r1's advisory W1 stands (not re-litigated):** the sub-1220px chip/forecast
  overlap was documented + user-flagged as optional fold-in — the minion chose NOT
  to fold it in with this merge (the delta is a base-merge only). Do NOT convert it
  into a blocker; it remains advisory unless the merge made it worse.
- **Base = `v2`** — now includes 5.7 telemetry (4a94fcb). Carry-forward only; do NOT
  re-open settled findings.
- **Scope guard:** presentation + canon only, as r1 verified.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.3-pause-ux/r2/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = the issue dump + job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.3-pause-ux/r2`, `prior_findings` = the r1 `consolidated.json`. Headless mode owns pane mechanics, lens JSONs, one retry per failed lens, chunking, verification pass, consolidation. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK"; degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` (STDOUT ONLY, never 2>&1); `if [ -z "$TOKEN" ]` → fallback `gh pr comment` + note fallback-comment; else `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`.
- Body format per the playbook (round N of 3, findings counts, verdict line).
- Before posting, re-fetch `headRefOid`. Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-5.3-pause-ux-perkins-r2 working` at start; final message = verdict + review URL + counts. Skip Step 5 (no fixing).
