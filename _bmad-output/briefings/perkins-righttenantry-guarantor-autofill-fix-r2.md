# Briefing: perkins-guarantor-autofill-fix-r2 (Perkins automated review, round 1)

- **Job under review:** righttenantry-guarantor-autofill-fix
- **PR:** https://github.com/solarity-services/RightTenantry/pull/581 (#581)
- **Reviewed sha:** 83be09972cd9fd98a010e8cc75e5be8f4726c7b6
- **repo_root:** /Users/moses/code/RightTenantry
- **Round:** 2 of 3
- **Original job briefing (your spec):** /Users/moses/code/_bmad-output/briefings/righttenantry-guarantor-autofill-fix.md — verbatim 6-item checklist + trigger notes + GLOBAL em-dash ban.
- **GitHub issue:** none.
- **prior_findings (RE-REVIEW — fix audit first, carry-forward markers):** /Users/moses/code/_bmad-output/perkins/righttenantry-guarantor-autofill-fix/r1/consolidated.json — round 1 found 1 blocker (B1: Chrome 9-per-type cap suppresses guarantor name/email; the AC over-promised). USER RULED [A]: accept the partial fix — the spec AC is now AMENDED to carve out Chrome-capped name/email explicitly (browser limitation, not a form defect). The minion also pushed mechanical-notes fixes (spec partition + tel-national pin). Fix-audit FIRST: verify B1 is resolved by the AC amendment (the blocker was an acceptance-contract issue, not a code defect — the amendment IS the fix), then hunt anew.
- **Your cwd:** /Users/moses/.herdr/worktrees/RightTenantry/perkins-guarantor-autofill-fix-r2 (detached at exactly the reviewed sha)
- **Ledger round id:** righttenantry-guarantor-autofill-fix-perkins-r2

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

## Round-2 specifics

- `<job-id>` = righttenantry-guarantor-autofill-fix, `<N>` = 2, `<pr>` = 581,
  `<owner>` = solarity-services, `<round-id>` = righttenantry-guarantor-autofill-fix-perkins-r2.
- No GitHub issue — `spec_files` = the original briefing.
- **Diff scope:** ~4 files (form_fields.gleam rewrite + 2 test files + spec) — small diff, single wave, no chunking needed. chunking is likely needed. The diff spans the
  entire user-facing copy surface (apply funnel, emails, auth/account/
  payment/consent, legal, content, AI report, landlord dashboard, static
  JS, llms.txt) — most changes are em-dash → comma/colon/paren replacements
  + the 6 verbatim checklist items + trigger notes. Expect many files with
  1-2 line changes each.
- Context for the lenses: this PR fixes browser autofill — do not flag
  the wording itself as a bug. The em-dash ban is absolute and user-ordered;
  `rg "\u2014|&mdash;"` returning 0 user-facing hits is the acceptance, not
  a gap. The `no_em_dash_test` CI guard is a regression guard (prevents
  re-introduction), not overkill. The en-dash in "Equal Status Acts
  2000–2018" is a date range (NOT an em-dash) — correctly kept. The no-JS
  item-6 trade-off (save-resume copy is JS-enhanced) is user-accepted and
  disclosed in the PR body — not a finding. Code comments retaining dashes
  are fine (the ban is user-facing only).
