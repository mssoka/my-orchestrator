# Briefing: perkins-form-stepper-f1-r3 (Perkins automated review, round 3 — FINAL, re-review)

- **Job under review:** righttenantry-form-stepper-f1
- **PR:** https://github.com/solarity-services/RightTenantry/pull/561 (#561)
- **Reviewed sha:** 8f2faf09ea84151d516fc44a2dea9686305627c6 (the r2-rework push — the merge candidate)
- **repo_root:** /Users/moses/code/RightTenantry
- **Round:** 3 of 3 — FINAL automated round. After your verdict the human takes over; there is no round 4.
- **Original job briefing (your spec):** /Users/moses/code/_bmad-output/briefings/righttenantry-form-stepper-f1.md — spec of record: `_bmad-output/planning-artifacts/problem-solving-application-form-completion-2026-07-31.md` (F1/F4/F5 rows + Solution Analysis + Recommended Solution + Risk Mitigation).
- **GitHub issue:** none for this job — the original briefing + spec of record are the spec.
- **prior_findings (RE-REVIEW — fix audit first, carry-forward markers):** /Users/moses/code/_bmad-output/perkins/righttenantry-form-stepper-f1/r2/consolidated.json — round 2 found 2B/5W/14N (both blockers in the reworked E2E suite: the {MOVE_IN_DATE}-neutralized boundary scenario; the listing_source tamper assertion) plus carried N5 (bare `new Event(`). The minion claims all fixed at this sha (new {MOVE_IN_DATE_TOO_FAR} template; post-F4 error-summary-row assertion; root.Event). Verify each fix first, then hunt anew. NOTE: r2 was reviewed at 7ac11fe pre-rebase; the current diff includes the post-#562 rebase + RC1.2 attestation gating wiring (data-gating-message pattern) — that wiring IS in scope this round.
- **Your cwd:** /Users/moses/.herdr/worktrees/RightTenantry/perkins-form-stepper-f1-r3 (detached at exactly the reviewed sha)
- **Ledger round id:** righttenantry-form-stepper-f1-perkins-r3

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

## Round-3 specifics

- `<job-id>` = righttenantry-form-stepper-f1, `<N>` = 3, `<pr>` = 561,
  `<owner>` = solarity-services, `<round-id>` = righttenantry-form-stepper-f1-perkins-r3.
- No GitHub issue — skip the `gh issue view` dump; `spec_files` = original
  briefing + the spec of record it names.
- This is the LAST automated round: be exact about blocker-vs-warning;
  the human merges on your verdict.
