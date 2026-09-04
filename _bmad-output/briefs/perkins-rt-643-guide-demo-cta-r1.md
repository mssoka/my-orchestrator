# Perkins round: rt-643-guide-demo-cta-perkins-r1

**PR:** https://github.com/solarity-services/RightTenantry/pull/644 (number 644)
**Reviewed sha:** a014a43d97f030a556c8daaaf18d12ef3e40e40c (re-fetch headRefOid before posting; if moved, post anyway + note)
**Repo root:** /Users/moses/code/RightTenantry · **Your cwd:** your detached round worktree at exactly the reviewed sha
**Spec:** the original job briefing /Users/moses/code/_bmad-output/briefs/rt-643-guide-demo-cta.md + gh issue view 643 (solarity-services/RightTenantry)
**Round dir:** /Users/moses/code/_bmad-output/perkins/rt-643-guide-demo-cta/r1/
**prior_findings:** none (round 1)
**Model:** zai-coding-cn/glm-5.3-flash (natively multimodal; pixel measurements decide). Bash 3.2 — NO arrays in wave scripts.

## What this PR claims (verify INDEPENDENTLY)

Adds a SECONDARY "Try the demo" CTA to the SSR guide template so every `/guides/*` page links to `/demo` (issue 643). Requirements (from the issue — each is a mandate): plain anchor to `/demo` on every guide page; `data-testid="guide-demo-cta"`; SECONDARY visual weight vs the signup CTA (one primary per view); brand copy EXACTLY: heading "See it work before you sign up", button "Try the demo", subline "A live sandbox with a mock vacancy and ranked applications. No signup." — no exclamation marks, no em dashes, outcome-led; no new analytics instrumentation (demo_entry already fires on /demo); client untouched.

## Your r1 mandates (verify INDEPENDENTLY)

- Every `/guides/*` render path carries the CTA — find the guide template(s) and confirm the anchor is in the shared/looped path, not one guide's hand-patch.
- The anchor attributes: href `/demo`, `data-testid="guide-demo-cta"`.
- Visual weight: secondary vs the signup CTA — check the classes/markup mirror `demo_cta_button` in client/src/pages/landing.gleam (~line 83) at secondary weight, and the primary signup CTA is untouched (still primary, still one per view).
- Brand copy: the three strings EXACT (typo-hunt: em dashes, exclamation marks, wording drift).
- Client untouched: `git diff 61586bb..a014a43 --stat` shows no client/ changes.
- Build + tests: `cd server && gleam build` (and `gleam test` if a suite exists) at this sha — green.
- If a rendered-guide check is cheap (the PR body may show rendered HTML), verify the anchor renders where claimed.

CI context: billing-block signature (0 steps) — note-only, NOT a gate; local gates are the merge ground truth.

Self-report: `/Users/moses/code/bin/ledger set rt-643-guide-demo-cta-perkins-r1 working` at start; final message = verdict + review URL + findings counts. Round row already exists — work it, do not create one.

---

## Standing orders (paste verbatim)

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
  briefing + the GitHub issue (dump it with `gh issue view 643 --json
  title,body,comments` into the round dir first), `out_dir` =
  `/Users/moses/code/_bmad-output/perkins/<job-id>/r<N>`, and
  `prior_findings` = the previous round's `consolidated.json` when N > 1
  (re-review: fix audit first, carry-forward markers). The headless mode
  owns: pane mechanics (dedicated tab, `mm-<lens>-r<N>` labels), the
  `<lens>.json` output contract + existence check, one retry per failed
  lens, big-diff chunking, the mandatory verification pass, consolidation,
  and writing `consolidated.json`. Its verdict thresholds are yours
  below.
  **Lens-spawn rooting (user-approved 2026-08-18):** the headless spawn
  template pins `--cwd <worktree>` on every lens tab FOREVER — a lens
  pane whose cwd is not the round worktree is mis-rooted: close +
  relaunch with `--cwd`.
  **Empty-lens doctrine (2026-08-18/19):** acceptance/architecture
  lenses back 3-byte-EMPTY a THIRD straight generation → sweep those
  lens panes + regenerate (intervene — an empty-lens verdict never
  ships); a g-wave COMPENSATION verdict (a subset of lenses delivering a
  valid verdict) counts as valid.
  Visual checks (goldens, sprites): verify MECHANICALLY first
  (byte/hash/capture-diff); your model is natively multimodal — vision
  is INLINE for screening, but pixel measurements decide, never a bare
  visual impression. Never fake a measurement.
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
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner <owner>)` —
     capture STDOUT ONLY. NEVER append `2>&1`: the script writes cache
     warnings to stderr, which would corrupt the token and make a good
     mint look like a failure.
  2. Check for an EMPTY token, NOT `$?` (an intervening command can
     clobber `$?`, and a `2>&1` capture makes it lie — the 2026-08-09
     rc3-2 round posted a fallback-comment instead of a formal approve
     on exactly this):
     `if [ -z "$TOKEN" ]` -> the mint failed; fall back to `gh pr comment
     <pr> --body-file <body.md>`, note `fallback-comment` in your ledger
     note, and call it out in your final message.
  3. Otherwise (token non-empty): `GH_TOKEN=$TOKEN gh pr review <pr>
     --<event> --body-file <body.md>`
- Body format:
  ```
  ## 🤖 Perkins automated review — round <N>
  **Job:** <job-id> · **Reviewed sha:** <short> · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed against the code — <rejected> discarded as false-positive[, <u> kept as [unverified]]

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Address findings and push — I re-review automatically on the new sha.
  The loop runs until an APPROVED verdict._
  ```
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post
  anyway but note "reviewed `<old>`, head now `<new>` — a fresh round
  will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set <round-id> working` at
  start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely —
  fixing is the implementing minion's job, triggered by the review relay.
