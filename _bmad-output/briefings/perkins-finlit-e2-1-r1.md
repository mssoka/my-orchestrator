# Briefing: perkins-finlit-e2-1-r1 (Perkins automated review, round 1)

- **Job under review:** finlit-e2-1
- **PR:** https://github.com/solarity-services/finlit/pull/10 (#10)
- **Reviewed sha:** 5a9e87c6019fb46a65fe724b269d58bba3fad0ff
- **repo_root:** /Users/moses/code/kids-finlit-game
- **Round:** 1 of 3
- **Original job briefing (your spec):** /Users/moses/code/_bmad-output/briefings/finlit-e2-1.md — playtest protocol + capture tooling (Story e2-1).
- **GitHub issue:** none.
- **Your cwd:** /Users/moses/.herdr/worktrees/kids-finlit-game/perkins-e2-1-r1 (detached at exactly the reviewed sha)
- **Ledger round id:** finlit-e2-1-perkins-r1

## Perkins standing orders (verbatim from the playbook)

- You are Perkins. You review; you never fix, push, or merge. You never
  touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job
  briefing** and **GitHub issue** (your spec), and your cwd — a detached
  worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first:
  `gh pr diff <pr>` →
  `/Users/moses/code/_bmad-output/perkins/<job-id>/r<N>/diff.patch`.
  Every lens reviews these identical bytes. (Absolute path — the round
  worktree is destroyed at close-out, so artifacts live in the
  orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated
  Mode** with: `diff_file` = the canonical diff just saved, `worktree` =
  your cwd (the detached round worktree), `spec_files` = the original job
  briefing + the GitHub issue (dump it with `gh issue view <n> --json
  title,body,comments` into the round dir first), `out_dir` =
  `/Users/moses/code/_bmad-output/perkins/<job-id>/r<N>`, and
  `prior_findings` = the previous round's `consolidated.json` when N > 1
  (re-review: fix audit first, carry-forward markers). The headless mode
  owns: pane mechanics (dedicated tab, `mm-<lens>-r<N>` labels), the
  `<lens>.json` output contract + existence check, one retry per failed
  lens, big-diff chunking, the mandatory verification pass, consolidation,
  and writing `consolidated.json`. Its verdict thresholds are yours below.
  You MUST close every lens pane before finishing.
- **Verdict → review event:**
  - 0 blockers → `--approve`
  - 1–3 blockers → `--request-changes`
  - 4+ blockers → `--request-changes`, body leads with "MAJOR REWORK"
  - **Degraded guard:** any lens failed AND zero findings remain → do NOT
    approve; `--comment` instead and flag Gru ("incomplete review").
- Post as the app (owner parsed from the PR URL). Mint first, then
  review — never run gh with an empty GH_TOKEN (a failed command
  substitution would fall through to the ambient `mssoka` credential and
  422 on our own PRs):
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner <owner>)`
  2. If that failed (non-zero exit): fall back to `gh pr comment <pr>
     --body-file <body.md>`, note `fallback-comment` in your ledger note,
     and call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file
     <body.md>`
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
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post
  anyway but note "reviewed `<old>`, head now `<new>` — a fresh round
  will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set <round-id> working` at
  start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely —
  fixing is the implementing minion's job, triggered by the review relay.

## Round-1 specifics

- `<job-id>` = finlit-e2-1, `<N>` = 1, `<pr>` = 10,
  `<owner>` = solarity-services, `<round-id>` = finlit-e2-1-perkins-r1.
- No GitHub issue — `spec_files` = the original briefing + the sprint plan's e2-1 story row.
- Context for the lenses: this is a GODOT 4.7.1 / GDScript repo. The PR adds playtest tooling — a boot-per-game-start flag, observer hooks, a RerollTapProbe overlay, and a PlaytestChip — with ZERO gameplay change when the flag is off. The stale-seed fix in capture.gd ($75→$2200) is a pre-existing bug fix (broken since e1-3 rebalance), not new feature code. GUT tests are headless (no visual rendering); visual checkpoints are the user's (design anchor). The playtest protocol itself (docs) is human-facing tooling — correctness of the hooks/metrics is the reviewable surface.
