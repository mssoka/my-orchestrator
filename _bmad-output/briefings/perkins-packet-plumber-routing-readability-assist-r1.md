# Perkins briefing — round 1: packet-plumber-routing-readability-assist (Job B)

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/40 (targets `v2`)
- **Reviewed sha:** `b0a6defb18fb8672c7f039a0f6c4ffedb76c7cfa` (short `b0a6def`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-routing-readability-assist-r1` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-routing-bandwidth-cost.md` + the canon at `/Users/moses/code/_bmad-output/problem-solution-2026-08-13.md` (PROBLEM DEFINITION, SUCCESS CRITERIA, RECOMMENDED SOLUTION — the user ruling drives this job) + the locked routing model (canon #18, `core/routing.odin`, architecture §6.2). GitHub issue: none.
- **Model:** `deepseek/deepseek-v4-pro` (Perkins reasoning tier). Launch EVERY lens pane with `pi --model deepseek/deepseek-v4-pro`. NEVER glm-5.2 (retired).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**Job B — the readability package (app layer):** R2a live cost-sum flow preview while drawing (the draw ghost shows the path packets WILL take per the cost-aware routing table + the best path's total cost — ONE number or the delta, never a spreadsheet) + assist graduation tiers (full assist sum+glow DEFAULT → partial glow-only → off; settings toggle; graduation nudge after N successful draws, N in balance.json — data-driven ODN-5, opt-in never forced); R3 post-draw route glow (the winning path lights up); T2 equal-cost tie cue (BOTH tied paths marked "equal cost — split by hash"). STRICT view-only (ODN-12): reads the routing table + tier costs, NEVER feeds sim state, NO core changes. New files: app/render/assist.odin + data/assist.json + harness/assist_check.odin; additive palette; app/main.odin wiring.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 LOAD-BEARING — STRICT VIEW-ONLY (ODN-12).** The assist reads the routing table + tier costs and NEVER feeds sim state; NO core changes in this PR (verify: core/ untouched; a core modification = a blocker). The preview must show what the routing table WILL do (the preview path CROSS-CHECKED against actual sim routing — the minion claims a preview-check harness, 7/7 — verify it exists and compares real vs previewed).
- **🚨 LOCKED — do not flag as defects:** Job A's Dijkstra model + the splice-proof re-bless (settled); `ecmp_pick`/`ecmp_hash`; the derived-not-serialized table; static costs; Job C's forecast panel (C owns it — do not demand it here); per-class routing preferences (full-game, out).
- **THE FOUR ACCEPTANCE SURFACES:** (1) R2a live preview: ONE number or the delta (never a candidate spreadsheet) + the draw ghost shows the cost-aware path; (2) assist graduation tiers: full/partial/off toggle + the balance.json-driven nudge (data-driven, opt-in, NEVER forced); (3) R3 post-draw glow: the winning path lights up (the visible payoff of a tier upgrade); (4) T2 tie cue: BOTH tied paths marked on ECMP (a split never looks random). Each surface must actually function (a toggle that doesn't toggle or a glow that never renders = a real defect).
- **GOLDEN-DISCIPLINE:** goldens byte-identical claim (the minion: harness 16/16 + goldens byte-identical) — verify; ANY golden shift = a finding.
- **ODN-5:** assist.json/balance.json additive + validated; a malformed config that breaks the app = a finding.
- **Scope guard:** Job B ONLY (app layer) — NOT C's forecast panel, NOT 4.3, NO new player commands (LOG_VERSION stays 3). app/main.odin is shared-risk with C (already merged? no — C is a SEPARATE open PR; review THIS diff at the sha; C's changes are not here).
- **BASE = `v2`** (Job A + 4.2 merged). **Em-dashes OK in PP.**
- **BASE = `v2`** (slices 1–3 + harness + 4.1 + 4.2 in — the 4.2 crisis engine is merged; carry-forward only; do NOT re-open 4.2 findings).
- **Em-dashes are OK in PP** (the RT ban does not apply).
- **Determinism spine reminder:** per-hop forwarding, T1 hash rides every serialized state, replay byte-identical.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-routing-readability-assist/r1/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = the original job briefing + the GitHub issue (dump it with `gh issue view <n> --json title,body,comments` into the round dir first), `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-routing-readability-assist/r1`, and `prior_findings` = the previous round's `consolidated.json` when N > 1 (re-review: fix audit first, carry-forward markers). The headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r<N>` labels), the `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and writing `consolidated.json`. Its verdict thresholds are yours below. You MUST close every lens pane before finishing.
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
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-routing-readability-assist-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
