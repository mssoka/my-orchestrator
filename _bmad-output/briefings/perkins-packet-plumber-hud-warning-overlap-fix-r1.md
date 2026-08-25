# Perkins briefing — round 1: packet-plumber-hud-warning-overlap-fix

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/42 (targets `v2`)
- **Reviewed sha:** `b3b8ded6d2351c620e54b23ee2b2e7f0c7b69a5f` (short `b3b8ded`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-hud-warning-overlap-fix-r1` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-hud-warning-overlap-fix.md` (the user-reported bug + the option-C fix the user verified). GitHub issue: none.
- **Model:** `deepseek/deepseek-v4-pro` (Perkins reasoning tier). Launch EVERY lens pane with `pi --model deepseek/deepseek-v4-pro`. NEVER glm-5.2.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **CI note:** GitHub CI is account-billing-blocked — YOUR local verification at the sha is the ground truth.

## What the PR does (review scope)

**TINY diff (+9/−6, app/main.odin, ONE block):** the drag-rejection warning no longer draws at the fixed `12, 76` (colliding with the 4.1 strain legend) — it anchors at the drag cursor, following the cost readout's established pattern (option C, user-verified 2026-08-14).

## ⚠️ CRITICAL lens-guards (this is a surgical-fix review)

- **Verify the collision is actually gone:** the strain-legend draw (`"node strain ~30s to critical / …"` at `12, 76, 14, p.ink_soft`) and the drag-warning draw must no longer share a position. The warning renders at the cursor (the reject_label text at the drag point). A residual overlap or a warning that renders off-screen/at a nonsense position = a finding.
- **Verify the pattern matches the established cost readout** (the anchor style the briefing names) — consistent placement, readable, not clipped at screen edges.
- **Verify the diff is surgical:** ONE block in app/main.odin, no unrelated changes, no core/ touches, LOG_VERSION 3, no new commands. Anything beyond the drag-rejection draw = a finding.
- **BASE = `v2`** (Job A/B/C + 4.1/4.2 + pin merged — carry-forward only). NOTE: in-flight 4.3 (win/lose toast) will touch app/main.odin separately — not in this PR; do not flag missing win/lose UI.
- **Em-dashes OK in PP.** Golden discipline: this diff cannot shift goldens (render-path only — verify none shifted).
- **User-verified approach:** the option-C cursor-anchor was explicitly confirmed by the user — review whether it's IMPLEMENTED correctly, do not re-litigate the choice of approach.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-hud-warning-overlap-fix/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = the job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-hud-warning-overlap-fix/r1`, `prior_findings` = N/A. Headless mode owns pane mechanics, lens JSONs, one retry per failed lens, chunking, verification pass, consolidation. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK"; degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` (STDOUT ONLY, never 2>&1); `if [ -z "$TOKEN" ]` → fallback `gh pr comment` + note fallback-comment; else `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`.
- Body format per the playbook (round N of 3, findings counts, verdict line).
- Before posting, re-fetch `headRefOid`. Self-report: `/Users/moses/code/bin/ledger set packet-plumber-hud-warning-overlap-fix-perkins-r1 working` at start; final message = verdict + review URL + counts. Skip Step 5 (no fixing).
