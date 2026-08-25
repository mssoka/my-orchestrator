# Perkins briefing — righttenantry-mobile-layout-1 r1

- **Job:** righttenantry-mobile-layout-1 · **Round:** 1 (loop-until-APPROVED budget)
- **PR:** https://github.com/solarity-services/RightTenantry/pull/631 (real-path mobile UX fixes + application-notification deep-link)
- **Reviewed sha:** `2879deefdfe2d26e95f59ba788a3a2e4ae1d94e7` (head of `mobile-layout-1`, base `develop`)
- **repo_root:** `/Users/moses/code/RightTenantry` · **Your cwd:** detached worktree at exactly the reviewed sha — trust it, not `origin/develop`
- **Spec pointers:** original job briefing `/Users/moses/code/_bmad-output/briefings/righttenantry-mobile-layout-1.md` (5 fixes) + the PR body's Decisions & rationale.
- **Model:** kimi-coding/k3 (reasoning tier — user-confirmed back; probed OK at dispatch). Lens mega-minions: name the model explicitly at every spawn (`kimi-coding/k3`) — and PIN `--cwd <this worktree>` on every lens tab.

## Lens-guards

- **ONE hard blocker class — the notification deep-link contract (fix 5):** `entity_type == "application"` must navigate to `/vacancies/<vid>/applications/<aid>` with the owning vacancy resolved client-side (demo authoritative in-memory; live from the loaded leaderboard, else graceful no-op); vacancy behavior UNCHANGED; both entity types mark-read; a navigation test (click → route) must exist for BOTH. The server payload carries only the application id — verify the resolution is sound (no fabricated/nonexistent vacancy ids, no crash on missing data) and the demo fixtures navigate.
- **Fix audit (each of the 5 must bite):**
  1. Compare-bar bottom padding — pb-28 reserved behind the fixed bar on BOTH application_detail AND vacancy_detail (the minion's honest stale-premise correction — the briefing claimed vacancy-detail handled it; grep showed neither did). Verify the Documents toggle clears the bar on app-detail.
  2. Status stepper mobile — horizontal scroll rail (flex + overflow-x-auto, shrink-0 stops) keeping left-to-right step semantics; desktop still wraps; applied to live, rejected, auto-closed steppers.
  3. Filter chip truncation — shrink-0 on the pills so the rail scrolls instead of ever clipping a label (root-cause; an ellipsis alone would keep the label permanently clipped).
  4. Demo CTA/Reset tap targets — min-h-[44px] + centering, no layout shift.
  5. (deep-link — see the hard-blocker class.)
- **What NOT to re-litigate:** the user-approved fix list (the spec); the client-side vacancy resolution choice (the user approved "either include the vacancy id at notification creation or resolve client-side"); the demo-surfaces coordination with demo-polish-1 (no cross-edit — flag any collision).
- **What to flag for verification:** the 8 test pins (navigation/resolver both entity types, stepper layout, compare padding, demo touch target); the new Tailwind classes present in the built CSS; no regression on the demo r1–r5 gauntlet classes (the demo inherits the deep-link fix).
- **CI note:** GitHub Actions is billing-blocked today (runners never start). Local suite is ground truth: shared 119 / client 632 / server 1527 per the badge-out — re-run the client suite at minimum.

## Perkins standing orders (verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 631` → `/Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r1/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the original job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r1`, no `prior_findings` (r1). Headless mode owns pane mechanics, the `<lens>.json` output contract, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and `consolidated.json`. Visual checks: verify MECHANICALLY first (byte/hash/capture-diff); when a visual judgment is unavoidable, run the `vision-read` skill on `lmstudio/qwen/qwen3.8-27b` — never trust a text-only model's eye. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 blockers → `--request-changes`; 4+ → `--request-changes`, body leads with "MAJOR REWORK". **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — STDOUT ONLY, never `2>&1` (stderr cache warnings corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → mint failed; fall back to `gh pr comment 631 --body-file <body.md>`, note `fallback-comment` in your ledger note, call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 631 --<event> --body-file <body.md>`
- Body format: `## 🤖 Perkins automated review — round 1 of 3` header (loop-until-APPROVED), Job, Reviewed sha, Reviewers x/7, Verification counts, Blockers/Warnings/Notes sections, Reviewer agreement, Verdict line, "_Address findings and push — I re-review automatically on the new sha._"
- Before posting, re-fetch `headRefOid` (gh pr view 631 --json headRefOid). If it moved mid-review, post anyway but note "reviewed <old>, head now <new> — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-mobile-layout-1-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Skip the code-review skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
