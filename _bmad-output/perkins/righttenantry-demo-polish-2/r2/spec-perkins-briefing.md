# Perkins briefing — righttenantry-demo-polish-2 r1

- **Job:** righttenantry-demo-polish-2 · **Round:** 2 (loop-until-APPROVED budget)
- **PR:** https://github.com/solarity-services/RightTenantry/pull/632 (demo-mode polish round 1 — real-app parity gaps)
- **Reviewed sha:** `1efcf2708c0a9dc43cc13fec5372e135f03bbca3` (head of `demo-polish-1`, base `develop`)
- **repo_root:** `/Users/moses/code/RightTenantry` · **Your cwd:** detached worktree at exactly the reviewed sha — trust it, not `origin/develop`
- **Spec pointers:** original job briefing `/Users/moses/code/_bmad-output/briefings/righttenantry-demo-polish-2.md` (5+1 fixes) + the PR body's Decisions & rationale + the demo-mode canon (the #629 5-round gauntlet: no-network pillar, exit leak, deep-link boot, session stash/restore).
- **Model:** kimi-coding/k3 (reasoning tier — user-confirmed back from the billing-cycle cap; probed OK at dispatch). Lens mega-minions: name the model explicitly at every spawn (`kimi-coding/k3`) — and PIN `--cwd <this worktree>` on every lens tab.

## Lens-guards (fix-audit round — r2)

- **Verify the r1 blocker fix BITES — the PDF personal-statement parity:**
  the fix must thread the five fixture statements through `simple_row`
  (server/src/demo/pdf_prebake.gleam) and re-bake. Verify by pdftotext on
  report-a-{conor,marta,sara,tom,liam}.pdf: NONE may say 'did not provide
  a personal statement'; each must carry its applicant's statement (match
  the client fixture text); Sara's Recommended Next Steps must not ask to
  request a statement she gave; the quoted-evidence Category Notes (Tom/
  Marta/Liam) must stay consistent with the section.
- **Carried (verified r1 — spot-verify they hold at this sha):** toast
  position + #615 pin (z-2147483001 vs banner 2147483000), the 13-15pp
  report skeleton + substance pin (brief >1,200 chars etc.), Compare Top 3
  real gate (leaderboard_view.gleam:140-141), the no-network pillar + the
  r1-r5 gauntlet classes.
- **What NOT to re-litigate:** the r1 blocker fix (audit it LANDED); the
  user's fix list; the #615 guarantee; the accepted stale-prod analysis.
- **CI note:** GitHub Actions is billing-blocked. Local suite is ground
  truth — re-run the client suite + pdftotext spot-checks at minimum.

## Perkins standing orders (verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 632` → `/Users/moses/code/_bmad-output/perkins/righttenantry-demo-polish-2/r2/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the original job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-demo-polish-2/r2`, `prior_findings` = the r1 `consolidated.json` (fix audit first, carry-forward markers). Headless mode owns pane mechanics, the `<lens>.json` output contract, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and `consolidated.json`. Visual checks: verify MECHANICALLY first (byte/hash/capture-diff); when a visual judgment is unavoidable, run the `vision-read` skill on `lmstudio/qwen/qwen3.8-27b` — never trust a text-only model's eye. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 blockers → `--request-changes`; 4+ → `--request-changes`, body leads with "MAJOR REWORK". **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — STDOUT ONLY, never `2>&1` (stderr cache warnings corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → mint failed; fall back to `gh pr comment 632 --body-file <body.md>`, note `fallback-comment` in your ledger note, call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 632 --<event> --body-file <body.md>`
- Body format: `## 🤖 Perkins automated review — round 2 of 3` header (loop-until-APPROVED), Job, Reviewed sha, Reviewers x/7, Verification counts, Blockers/Warnings/Notes sections, Reviewer agreement, Verdict line, "_Address findings and push — I re-review automatically on the new sha._"
- Before posting, re-fetch `headRefOid` (gh pr view 630 --json headRefOid). If it moved mid-review, post anyway but note "reviewed <old>, head now <new> — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-demo-polish-2-perkins-r2 working` at start; final message = verdict + review URL + findings counts.
- Skip the code-review skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
