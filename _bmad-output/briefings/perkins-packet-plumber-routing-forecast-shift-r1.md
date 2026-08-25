# Perkins briefing — round 1: packet-plumber-routing-forecast-shift (Job C)

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/39 (targets `v2`)
- **Reviewed sha:** `da825d8be27de5230a7009a53b56c9ca6a70b0a8` (short `da825d8`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-routing-forecast-shift-r1` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-routing-bandwidth-cost.md` + the canon at `/Users/moses/code/_bmad-output/problem-solution-2026-08-13.md` (PROBLEM DEFINITION, SUCCESS CRITERIA, RECOMMENDED SOLUTION — the user ruling drives this job) + the locked routing model (canon #18, `core/routing.odin`, architecture §6.2). GitHub issue: none.
- **Model:** `deepseek/deepseek-v4-pro` (Perkins reasoning tier). Launch EVERY lens pane with `pi --model deepseek/deepseek-v4-pro`. NEVER glm-5.2 (retired).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**Job C — R4 forecast flow-shift prediction:** a PURE predictive helper (given the current Topology + a hypothetical tier change on one pipe, recompute the post-upgrade routing by re-running Job A's Dijkstra against the hypothetical topology + the predicted flow shift — no state mutation, no rng, integer-only, array-only [ODN-9/10]; it is a look, never a write) + the forecast-panel integration (when the player considers upgrading a pipe's tier, the panel shows the predicted reroute: "traffic will reroute to X" / "equal-cost — flow will split"). LOG_VERSION stays 3 (nothing serialized — derived data only). The minion flags app/main.odin as shared-risk with parallel Job B.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 LOAD-BEARING — the helper is PURE + honest.** (a) The predictive helper is a pure function: no state mutation, no rng, integer-only, array-only (ODN-9/10); it RE-RUNS Job A's Dijkstra against the HYPOTHETICAL topology (a tier change on one pipe) — the prediction must match what the sim WILL do (the honest-prediction pin: apply the upgrade FOR REAL in a demo and assert prediction == actual post-upgrade behavior — the determinism twin of `expect hash stable`). A prediction that diverges from actual post-upgrade routing = a blocker. (b) The helper is a look, NEVER a write — no sim-state mutation from the preview path (a write = a blocker).
- **🚨 LOCKED — do not flag as defects:** Job A's Dijkstra model + the splice-proof re-bless (settled); `ecmp_pick`/`ecmp_hash`; the table derived-not-serialized; static costs; capacity effects (bundle speedups) deliberately out of the helper's path-choice scope (the minion flagged this decision); per-class routing preferences (full-game idea, scope-guarded out).
- **PANEL INTEGRATION:** when the player considers upgrading a pipe's tier, the panel shows the predicted reroute BEFORE commitment (with the equal-cost split message). The wiring must actually consume the helper (a panel that renders but never queries = a real defect). The panel shares `app/main.odin` with parallel Job B — review the diff at the sha; B's changes are NOT in this PR.
- **GOLDEN-DISCIPLINE:** NEW golden files only (the property-pin demo); existing goldens MUST NOT shift (any shift = a finding — the "STOP and flag" class).
- **ODN-5 / scope:** no new player commands; LOG_VERSION stays 3 (a bump without a flag = flag it); surge/crisis content is settled (4.2 merged — carry-forward only).
- **BASE = `v2`** (Job A + 4.2 merged). **Em-dashes OK in PP.**
- **BASE = `v2`** (slices 1–3 + harness + 4.1 + 4.2 in — the 4.2 crisis engine is merged; carry-forward only; do NOT re-open 4.2 findings).
- **Em-dashes are OK in PP** (the RT ban does not apply).
- **Determinism spine reminder:** per-hop forwarding, T1 hash rides every serialized state, replay byte-identical.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-routing-forecast-shift/r1/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = the original job briefing + the GitHub issue (dump it with `gh issue view <n> --json title,body,comments` into the round dir first), `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-routing-forecast-shift/r1`, and `prior_findings` = the previous round's `consolidated.json` when N > 1 (re-review: fix audit first, carry-forward markers). The headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r<N>` labels), the `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and writing `consolidated.json`. Its verdict thresholds are yours below. You MUST close every lens pane before finishing.
- **Verdict → review event:**
  - 0 blockers → `--approve`
  - 1–3 blockers → `--request-changes`
  - 4+ blockers → `--request-changes`, body leads with "MAJOR REWORK"
  - **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru ("incomplete review").
- Post as the app (owner parsed from the PR URL). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — capture STDOUT ONLY. NEVER append `2>&1`.
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` -> the mint failed; fall back to `gh pr comment <pr> --body-file <body.md>`, note `fallback-comment` in your ledger note, and call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`
- Body format:
  ```
  ## 🤖 Perkins automated review — round <N> of 3
  **Job:** <job-id> · **Reviewed sha:** <short> · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed against the code — <rejected> discarded as false-positive[, <u> kept as [unverified]]

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Address findings and push — I re-review automatically on the new sha.
  After round 3, the human takes over._
  ```
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-routing-forecast-shift-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
