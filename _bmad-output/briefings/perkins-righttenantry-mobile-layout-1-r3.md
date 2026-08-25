# Perkins briefing — righttenantry-mobile-layout-1 r1

- **Job:** righttenantry-mobile-layout-1 · **Round:** 3 (loop-until-APPROVED budget)
- **PR:** https://github.com/solarity-services/RightTenantry/pull/631 (real-path mobile UX fixes + application-notification deep-link)
- **Reviewed sha:** `0f94e043a50851ecbd9bb82d1ec752f75823338f` (head of `mobile-layout-1`, base `develop`)
- **repo_root:** `/Users/moses/code/RightTenantry` · **Your cwd:** detached worktree at exactly the reviewed sha — trust it, not `origin/develop`
- **Spec pointers:** original job briefing `/Users/moses/code/_bmad-output/briefings/righttenantry-mobile-layout-1.md` (5 fixes) + the PR body's Decisions & rationale.
- **Model:** kimi-coding/k3 (reasoning tier — user-confirmed back; probed OK at dispatch). Lens mega-minions: name the model explicitly at every spawn (`kimi-coding/k3`) — and PIN `--cwd <this worktree>` on every lens tab.

## Lens-guards (fix-audit round — r3)

- **Verify EACH r2 blocker fix BITES:**
  - B1 (r2) — demo click arm bypasses notification_target_path: the fix
    must move the helper (with resolve_application_vacancy) into a neutral
    module both arms import, call it from the demo arm, and pin BOTH arms.
    Verify vacancy-typed demo clicks now NAVIGATE (the r1/r2 miss: demo
    clicks no-op'd) and the real arm still routes through the same helper
    (no contract drift).
  - B2 (r2) — late ApiReturnedLeaderboard response race: the plain
    leaderboard response message (and the page variant) must carry the
    vacancy id and apply only on match (like the refresh handler's
    vacancy_detail_request_id). Verify the exact r2 repro: VacancyDetail(A)
    fetch in flight -> navigate to B -> A's response lands -> A's rows must
    NOT tag as B, and the resolver must not fabricate.
- **ONE hard blocker class (carried): the notification deep-link contract**
  — both entity types navigate + mark read; no fabricated vacancy ids
  (real AI-failure notifications carry only the application id); vacancy
  behavior unchanged.
- **What NOT to re-litigate:** the r2 blocker fixes (audit they LANDED);
  the user-approved client-side resolution choice; the fix list.
- **What to flag for verification:** client suite green (637+ at the last
  round); the neutral-module move didn't break the real arm; the demo
  arm's pins are real; no regression on the demo r1-r5 gauntlet classes.
- **CI note:** GitHub Actions is billing-blocked. Local suite is ground
  truth — re-run the client suite at minimum.

## Perkins standing orders (verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 631` → `/Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r3/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the original job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r3`, `prior_findings` = the r2 `consolidated.json` (fix audit first, carry-forward markers). Headless mode owns pane mechanics, the `<lens>.json` output contract, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and `consolidated.json`. Visual checks: verify MECHANICALLY first (byte/hash/capture-diff); when a visual judgment is unavoidable, run the `vision-read` skill on `lmstudio/qwen/qwen3.8-27b` — never trust a text-only model's eye. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 blockers → `--request-changes`; 4+ → `--request-changes`, body leads with "MAJOR REWORK". **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — STDOUT ONLY, never `2>&1` (stderr cache warnings corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → mint failed; fall back to `gh pr comment 631 --body-file <body.md>`, note `fallback-comment` in your ledger note, call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 631 --<event> --body-file <body.md>`
- Body format: `## 🤖 Perkins automated review — round 3 of 3` header (loop-until-APPROVED), Job, Reviewed sha, Reviewers x/7, Verification counts, Blockers/Warnings/Notes sections, Reviewer agreement, Verdict line, "_Address findings and push — I re-review automatically on the new sha._"
- Before posting, re-fetch `headRefOid` (gh pr view 631 --json headRefOid). If it moved mid-review, post anyway but note "reviewed <old>, head now <new> — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-mobile-layout-1-perkins-r3 working` at start; final message = verdict + review URL + findings counts.
- Skip the code-review skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
