# Briefing: perkins-form-save-resume-f3-r4 (Perkins automated review, round 4 — USER-OVERRIDDEN CAP, re-review)

- **Job under review:** righttenantry-form-save-resume-f3
- **PR:** https://github.com/solarity-services/RightTenantry/pull/563 (#563)
- **Reviewed sha:** d3f7700c6b62c0bfbbf1fac3024ad9ad9df3e930
- **repo_root:** /Users/moses/code/RightTenantry
- **Round:** 4 of 3 — explicitly USER-OVERRIDDEN cap (verbatim: "one more perkins round on #563", 2026-08-02). This sets no precedent; the cap stays 3 elsewhere. Your verdict is still advisory — the human merges.
- **Original job briefing (your spec):** /Users/moses/code/_bmad-output/briefings/righttenantry-form-save-resume-f3.md — spec of record: `_bmad-output/planning-artifacts/problem-solving-application-form-completion-2026-07-31.md` (F3 row + Solution Analysis + Recommended Solution + Risk Mitigation incl. the draft data-protection row + E2 reminder row).
- **GitHub issue:** none for this job — the original briefing + spec of record are the spec.
- **prior_findings (RE-REVIEW — fix audit first, carry-forward markers):** /Users/moses/code/_bmad-output/perkins/righttenantry-form-save-resume-f3/r3/consolidated.json — round 3 found 1B (PostHog autocapture leaking the raw data-resume-token off <body> past the URL scrub) + 1W (413 envelope lacks ok:false) + carried notes. The minion claims: token moved off the DOM entirely (CSP-nonced inline-script global), recursive key-scrub in sanitize_properties, 413 gate fixed, clearTimeout seam pinned. Fix-audit FIRST on the r3 blocker — verify the token cannot reach the analytics store through any capture path (attributes, $elements_chain, custom events) — then hunt anew.
- **Your cwd:** /Users/moses/.herdr/worktrees/RightTenantry/perkins-form-save-resume-f3-r4 (detached at exactly the reviewed sha)
- **Ledger round id:** righttenantry-form-save-resume-f3-perkins-r4

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

## Round-4 specifics

- `<job-id>` = righttenantry-form-save-resume-f3, `<N>` = 3, `<pr>` = 563,
  `<owner>` = solarity-services, `<round-id>` = righttenantry-form-save-resume-f3-perkins-r4.
- No GitHub issue — skip the `gh issue view` dump; `spec_files` = original
  briefing + the spec of record it names.

