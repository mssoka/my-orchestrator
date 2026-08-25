# Perkins briefing — righttenantry-mobile-layout-1 r1

- **Job:** righttenantry-mobile-layout-1 · **Round:** 4 (loop-until-APPROVED budget)
- **PR:** https://github.com/solarity-services/RightTenantry/pull/631 (real-path mobile UX fixes + application-notification deep-link)
- **Reviewed sha:** `98601499c26627490a630bf06591c0978cbcc6ad` (head of `mobile-layout-1`, base `develop`)
- **repo_root:** `/Users/moses/code/RightTenantry` · **Your cwd:** detached worktree at exactly the reviewed sha — trust it, not `origin/develop`
- **Spec pointers:** original job briefing `/Users/moses/code/_bmad-output/briefings/righttenantry-mobile-layout-1.md` (5 fixes) + the PR body's Decisions & rationale.
- **Model:** kimi-coding/k3 (reasoning tier — user-confirmed back; probed OK at dispatch). Lens mega-minions: name the model explicitly at every spawn (`kimi-coding/k3`) — and PIN `--cwd <this worktree>` on every lens tab.

## Lens-guards (fix-audit round — r4)

- **Verify the r3 blocker fix BITES — the cold-boot leaderboard drop:**
  the fix must set `leaderboard_vacancy_id: Some(id)` AND
  `leaderboard: Loading` in BOTH cold-boot model updates alongside the
  fetch — the session-restore path (client.gleam:1046-1090) and the
  enter_demo / demo_entry_effects path (5839-5934). Verify the exact r3
  repro: refresh the browser on /vacancies/<id> (and deep-link a demo
  vacancy) -> the leaderboard must load (not stuck NotAsked). Also verify
  the Error arm now respects the guard (the r3 W1).
- **Carried (verified-fixed r1/r2/r3, spot-verify they hold):** the
  stale-leaderboard fabrication guard (regression test), the
  notification_target_path neutral-module routing (both arms, both
  entity types, no-op cases), the demo arm through the shared helper.
- **ONE hard blocker class (carried): the notification deep-link
  contract** — both entity types navigate + mark read; no fabricated
  vacancy ids; vacancy behavior unchanged; no live-product regression
  (the r3 miss was exactly that).
- **What NOT to re-litigate:** the r3 blocker fix (audit it LANDED); the
  user-approved client-side resolution choice; the fix list.
- **What to flag for verification:** client suite green (640+); the
  cold-boot set-sites are complete (grep all fetch_leaderboard call sites
  — none missing the tag); the Error arm guard.
- **CI note:** GitHub Actions is billing-blocked. Local suite is ground
  truth — re-run the client suite at minimum.

## Perkins standing orders (verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 631` → `/Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r4/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the original job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r4`, `prior_findings` = the r3 `consolidated.json` (fix audit first, carry-forward markers). Headless mode owns pane mechanics, the `<lens>.json` output contract, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and `consolidated.json`. Visual checks: verify MECHANICALLY first (byte/hash/capture-diff); when a visual judgment is unavoidable, run the `vision-read` skill on `lmstudio/qwen/qwen3.8-27b` — never trust a text-only model's eye. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 blockers → `--request-changes`; 4+ → `--request-changes`, body leads with "MAJOR REWORK". **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — STDOUT ONLY, never `2>&1` (stderr cache warnings corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → mint failed; fall back to `gh pr comment 631 --body-file <body.md>`, note `fallback-comment` in your ledger note, call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 631 --<event> --body-file <body.md>`
- Body format: `## 🤖 Perkins automated review — round 4 of 3` header (loop-until-APPROVED), Job, Reviewed sha, Reviewers x/7, Verification counts, Blockers/Warnings/Notes sections, Reviewer agreement, Verdict line, "_Address findings and push — I re-review automatically on the new sha._"
- Before posting, re-fetch `headRefOid` (gh pr view 631 --json headRefOid). If it moved mid-review, post anyway but note "reviewed <old>, head now <new> — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-mobile-layout-1-perkins-r4 working` at start; final message = verdict + review URL + findings counts.
- Skip the code-review skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
