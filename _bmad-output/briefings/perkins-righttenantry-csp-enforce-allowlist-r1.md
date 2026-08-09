# Briefing: perkins-csp-enforce-allowlist-r1 (Perkins automated review, round 1)

- **Job under review:** righttenantry-csp-enforce-allowlist
- **PR:** https://github.com/solarity-services/RightTenantry/pull/578 (#578)
- **Reviewed sha:** 6b6ba477ae1cab404a0f3a0c366d316dfc05e350
- **repo_root:** /Users/moses/code/RightTenantry
- **Round:** 1 of 3
- **Original job briefing (your spec):** /Users/moses/code/_bmad-output/briefings/righttenantry-csp-enforce-allowlist.md — CSP allowlist additions for enforcement + 3 violation investigations.
- **GitHub issue:** none.
- **Your cwd:** /Users/moses/.herdr/worktrees/RightTenantry/perkins-csp-enforce-allowlist-r1 (detached at exactly the reviewed sha)
- **Ledger round id:** righttenantry-csp-enforce-allowlist-perkins-r1

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

- `<job-id>` = righttenantry-csp-enforce-allowlist, `<N>` = 1, `<pr>` = 578,
  `<owner>` = solarity-services, `<round-id>` = righttenantry-csp-enforce-allowlist-perkins-r1.
- No GitHub issue — `spec_files` = the original briefing.
- Context for the lenses: this is a SECURITY-SENSITIVE CSP allowlist PR. The four directive additions (connect-src sGTM Cloud Run, img-src google.ie+google.com.gh, style-src gstatic, frame-src GA iframe) are from Sentry violation data verified by Gru. The three investigations (AWS ECS hostname, bare "properties", self-origin) were classified as JUNK hitting the public report endpoint — that classification is the minion's finding, verify it. The CSP_ENFORCE flip is DELIBERATELY out-of-PR (deploy-time user action) — its absence is not a gap. The minion's review swarm already ran (adversarial + edge-case); Perkins is the independent gate. Pay special attention to: CSP string well-formedness (no trailing semicolons, quotes balanced), the unit test actually asserts each allowlisted domain, and no overly-broad wildcard slipped in.
