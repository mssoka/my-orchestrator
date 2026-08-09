# Briefing: perkins-guarantor-checkbox-desync-r3 (Perkins automated review, round 1)

- **Job under review:** righttenantry-guarantor-checkbox-desync
- **PR:** https://github.com/solarity-services/RightTenantry/pull/577 (#577)
- **Reviewed sha:** 117ac6ee969b3be8e34a1c77a6d469a4967bd516
- **repo_root:** /Users/moses/code/RightTenantry
- **Round:** 3 of 3 — FINAL automated round; the human takes over after your verdict
- **Original job briefing (your spec):** /Users/moses/code/_bmad-output/briefings/righttenantry-guarantor-checkbox-desync.md — BUT SUPERSEDED by the in-flight user rulings (the "desync" framing was DEAD; the policy is force_required = never_rented OR {student, unemployed}, SERVER-enforced; declared-required treatment per cohort; both silent ticks killed; step-level gating; definition-based copy). Read the job's ledger notes for the final policy in full.
- **GitHub issue:** none.
- **prior_findings (RE-REVIEW — fix audit first, carry-forward markers):** /Users/moses/code/_bmad-output/perkins/righttenantry-guarantor-checkbox-desync/r2/consolidated.json — round 2 found 0 blockers / 0 warnings (the W1 fix verified empirically via mutation check) (the student fixture missed-retired-migration, dead-copy-string false-pass) + 5 notes. The r2 APPROVED 0B/0W on 279a661; the head has since moved to 117ac6e (a rebase onto post-#574 develop — commit oids changed but content is the same W1 fix). Verify the rebase didn't alter semantics, then hunt anew. Note r2 flagged N1: a misnamed test (optional_path_posted_uncheck_roundtrips_test fixtures a student — a required cohort — contradicting its name; the pin is live, the true case covered elsewhere).
- **Your cwd:** /Users/moses/.herdr/worktrees/RightTenantry/perkins-guarantor-checkbox-desync-r3 (detached at exactly the reviewed sha)
- **Ledger round id:** righttenantry-guarantor-checkbox-desync-perkins-r3

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

- `<job-id>` = righttenantry-guarantor-checkbox-desync, `<N>` = 3, `<pr>` = 577,
  `<owner>` = solarity-services, `<round-id>` = righttenantry-guarantor-checkbox-desync-perkins-r3.
- No GitHub issue — `spec_files` = original briefing + the job's ledger notes (carry the final policy).
- Context for the lenses: the "desync" framing in the briefing's title is SUPERSEDED — the real fix is a deliberate SERVER-ENFORCED required-cohort policy (force_required = never_rented OR {student, unemployed}); the previously-suspected "self-marking bug" was the deliberate force_required path. Do NOT flag the required-cohort behavior as a desync bug; it's the spec. The killed silent ticks (JS autoTickGuarantor + view has_guarantor_default_check) are the deliberate removal. Definition-based copy (no "usually a parent"), step-level gating, and the counsel flag (student tracks age — equality-law note in PR) are user-ruled, not findings. The PR's parked questions (Ireland-vs-foreign acceptance) are disclosed, not missed.
