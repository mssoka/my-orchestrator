# Perkins briefing — righttenantry-demo-mode r5

- **Job:** righttenantry-demo-mode · **Round:** 5 (loop-until-APPROVED budget — round 5 of the arc)
- **PR:** https://github.com/solarity-services/RightTenantry/pull/629 (feat(demo): interactive landing demo — mock-data sandbox)
- **Reviewed sha:** `233018972feea3b40f1d04c6935489859d6179fa` (head of `demo-mode`, base `develop`)
- **repo_root:** `/Users/moses/code/RightTenantry` · **Your cwd:** detached worktree at exactly the reviewed sha — trust it, not `origin/develop`
- **Spec pointers:** original job briefing `/Users/moses/code/_bmad-output/briefings/righttenantry-demo-mode.md` + GitHub issue #628 + the lavish demo-flow verdict (CTA moment B, persistent banner, FFI approved, fixtures 3+9) + the PR body's r4→r5 section.
- **Model:** zai-coding-cn/glm-5.3 (STANDING reasoning primary — user ruling 08-19 night: kimi limit reached, glm-first, no proactive k3 flips; probed OK at dispatch). Lens mega-minions: name the model explicitly at every spawn (`zai-coding-cn/glm-5.3`) — and PIN `--cwd <this worktree>` on every lens tab.

## Lens-guards (fix-audit round — r5)

- **This is a fix-audit: `prior_findings` = `/Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r4/consolidated.json`** (r4 = 2 blockers @4bff855). Verify each r4 blocker fix BITES:
  - B1 (r4) — no-network lint vacuous on the fn-helper path: the r5 fix must (a) match any `*.demo_mode` receiver in `demo_guard_in_same_scope` (so `case saving.demo_mode` guards are seen), (b) delete the DEMO_BRANCHED_HELPERS skip (or verify those fns via the interception manifest — the r4 demo branches in fire_refcheck_*/save_refcheck_edit were DEAD CODE and must be gone), (c) add the helper-scope bite-test. Verify by deleting the skip / poisoning a helper and seeing the lint fail.
  - B2 (r4) — demo ENTRY transition unpinned: two dispatch tests must drive `client.update` on a NON-demo model (landing-CTA `/demo` nav + `is_demo_route` deep-link boot), asserting demo_mode, seeded store, mock-landlord auth swap, dashboard NotAsked → Loading.
- **ONE hard blocker class (carried): the no-network pillar** — demo issues ZERO real API calls; the lint is the mechanism and MUST bite (vacuously-passing lint = blocker, the r3-B3/r4-B1 class). Also verify the W1 session stash/restore pin (nav-exit restores real auth+csrf, logout drops — pinned both ways per the badge-out).
- **What NOT to re-litigate:** the lavish verdict + applied r1-r4 findings (the fix audit covers what's applied); user rulings (demo = real components + mock data, no backend surface, synthetic-footer canon).
- **What to flag for verification:** the W8 post-exit Back re-entry via `is_demo_route` (the r4 W8 — browser-verified claim, code-checkable); W9 ApiReturnedPolicyRefresh demo guard; W10 payment/extended arms batch eff; W11 optimistic unread_count; W12 Grace PDF 98% (was 58%) + re-baked; the 8 lint bite-tests actually fail on synthetic violations.
- **CI note:** GitHub Actions is billing-blocked today. Local suite is ground truth: shared 119 / client 621 / server 1527+549 per the badge-out — re-run the client suite + the no-network lint at minimum.

## Perkins standing orders (verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 629` → `/Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r5/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the original job briefing + the GitHub issue (dump it with `gh issue view 628 --json title,body,comments` into the round dir first), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-demo-mode/r5`, `prior_findings` = the r4 `consolidated.json` (fix audit first, carry-forward markers). Headless mode owns pane mechanics, the `<lens>.json` output contract, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and `consolidated.json`. Visual checks: verify MECHANICALLY first (byte/hash/capture-diff); when a visual judgment is unavoidable, run the `vision-read` skill on `lmstudio/qwen/qwen3.8-27b` — never trust a text-only model's eye. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 blockers → `--request-changes`; 4+ → `--request-changes`, body leads with "MAJOR REWORK". **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — STDOUT ONLY, never `2>&1` (stderr cache warnings corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → mint failed; fall back to `gh pr comment 629 --body-file <body.md>`, note `fallback-comment` in your ledger note, call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 629 --<event> --body-file <body.md>`
- Body format: `## 🤖 Perkins automated review — round 5 of 3` header (loop-until-APPROVED), Job, Reviewed sha, Reviewers x/7, Verification counts, Blockers/Warnings/Notes sections, Reviewer agreement, Verdict line, "_Address findings and push — I re-review automatically on the new sha._"
- Before posting, re-fetch `headRefOid` (gh pr view 629 --json headRefOid). If it moved mid-review, post anyway but note "reviewed <old>, head now <new> — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-demo-mode-perkins-r5 working` at start; final message = verdict + review URL + findings counts.
- Skip the code-review skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
