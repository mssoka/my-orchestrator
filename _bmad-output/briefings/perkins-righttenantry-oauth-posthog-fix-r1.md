# Briefing: perkins-oauth-posthog-fix-r1 (Perkins automated review, round 1)

- **Job under review:** righttenantry-oauth-posthog-fix
- **PR:** https://github.com/solarity-services/RightTenantry/pull/583 (#583)
- **Reviewed sha:** b9882fa024bcfa6ff230b356eb28fa88479b416f
- **repo_root:** /Users/moses/code/RightTenantry
- **Round:** 1 of 3
- **Original job briefing (your spec):** /Users/moses/code/_bmad-output/briefings/righttenantry-oauth-posthog-fix.md — thread PostHog through the Google OAuth callback chain (router → handle_oauth_callback → process_oauth_callback → complete_oauth_flow) + server-side identify/capture + cookie-lifetime fix.
- **GitHub issue:** none.
- **Your cwd:** /Users/moses/.herdr/worktrees/RightTenantry/perkins-oauth-posthog-fix-r1 (detached at exactly the reviewed sha)
- **Ledger round id:** righttenantry-oauth-posthog-fix-perkins-r1

## Perkins standing orders (verbatim from the playbook)

- You are Perkins. You review; you never fix, push, or merge. You never
  touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job
  briefing** and **GitHub issue** (your spec), and your cwd — a detached
  worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first:
  `gh pr diff <pr>` →
  `/Users/moses/code/_bmad-output/perkins/righttenantry-oauth-posthog-fix/r1/diff.patch`.
  Every lens reviews these identical bytes. (Absolute path — the round
  worktree is destroyed at close-out, so artifacts live in the
  orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated
  Mode** with: `diff_file` = the canonical diff just saved, `worktree` =
  your cwd (the detached round worktree), `spec_files` = the original job
  briefing + the GitHub issue (dump it with `gh issue view <n> --json
  title,body,comments` into the round dir first), `out_dir` =
  `/Users/moses/code/_bmad-output/perkins/righttenantry-oauth-posthog-fix/r1`, and
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

- `<job-id>` = righttenantry-oauth-posthog-fix, `<N>` = 1, `<pr>` = 583,
  `<owner>` = solarity-services, `<round-id>` = righttenantry-oauth-posthog-fix-perkins-r1.
- No GitHub issue — `spec_files` = the original briefing.
- **Context for the lenses:** this is an analytics-tracking (PostHog) PR on the Google OAuth callback path. The minion's claimed fixes:
  1. PostHog threaded through the OAuth chain (router.gleam → handle_oauth_callback → process_oauth_callback → complete_oauth_flow), mirroring how handle_login gets it.
  2. Server-side `identify_with_set_once` (email `$set`) + `capture` of `signup_completed` (first OAuth sign-in) or `login_succeeded` (returning) — first-vs-returning distinguished **atomically** via a new `(xmax = 0) AS is_new` insert-flag in the upsert's RETURNING.
  3. Identify-bridge cookie `rt_landlord_id` lifetime 10s → 60s (sole anonymous→identified merge mechanism; cold JS load can outlive 10s). Sentinels (`rt_landlord_external_id`, `rt_ph_reset`) deliberately stay at 10s.
  4. Review catch: reset-arm now also clears `rt_landlord_id` (with the wider 60s window, a quick logout could otherwise re-identify the previous landlord after `posthog.reset()`).
- **Lens attention (the load-bearing surfaces to verify independently):**
  - **`(xmax = 0) AS is_new` atomicity** — the first-vs-returning distinction rides on this Postgres system column in the upsert's RETURNING. Verify it is genuinely atomic (no TOCTOU vs a pre-check SELECT), codegens to the expected type, and that `signup_completed` vs `login_succeeded` is selected correctly off it. A wrong polarity here = wrong event for every OAuth sign-in.
  - **4-place inline-snippet contract** — the analytics bridge snippets live in BOTH `Makefile` (build-client) and `Dockerfile` perl chains, each with its own substring-pin guard list. Any snippet change must hit all 4 (2 chains + 2 guards). Verify the reset-arm change landed in all 4 and the guard pins are substrings UNIQUE to the changed arm.
  - **Cookie-lifetime contract** — `rt_landlord_id` (identify, 60s) vs the two sentinels (10s) is a cross-cutting contract pinned in test assertions + build guards + doc comments. Verify no sentinel accidentally widened and no narrowing of the identify cookie.
  - **Identify/capture correctness** — confirm identify fires with the landlord `row.id` + email (same shape as email/password path), and the capture uses consent-independent firing matching the email/password path. Verify anonymous→identified merge is still possible (the identify cookie is the only client-side merge link).
  - **Scope discipline** — `login_succeeded` is OAuth-scoped by design (email/password deliberately skips it per the briefing). The minion flags these as disclosed follow-ups, NOT gaps: cross-provider `login_succeeded` on the email path; no first-touch attribution on OAuth (UTM dies in redirect); cross-provider returning = new signup (pre-existing account model). Treat these as notes/acknowledged-limitations, not findings — unless the implementation contradicts the disclosure.
- The minion's own review swarm (adversarial + edge-case hunters) ran 0 blockers; Perkins is the independent gate. The staging real-flow check was NOT possible from the worktree (no OAuth-configured staging) — unit/integration tests are the evidence; flag if the identify path is only asserted via mocks and lacks a real end-to-end capture assertion.
