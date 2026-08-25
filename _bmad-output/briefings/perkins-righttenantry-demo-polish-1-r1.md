# Perkins briefing — righttenantry-demo-polish-1 r1

- **Job:** righttenantry-demo-polish-1 · **Round:** 1 (loop-until-APPROVED budget)
- **PR:** https://github.com/solarity-services/RightTenantry/pull/630 (demo-mode polish round 1 — real-app parity gaps)
- **Reviewed sha:** `34a2f3b5aa8f5367efb02955d2a71312eb1eeb5d` (head of `demo-polish-1`, base `develop`)
- **repo_root:** `/Users/moses/code/RightTenantry` · **Your cwd:** detached worktree at exactly the reviewed sha — trust it, not `origin/develop`
- **Spec pointers:** original job briefing `/Users/moses/code/_bmad-output/briefings/righttenantry-demo-polish-1.md` (5+1 fixes) + the PR body's Decisions & rationale + the demo-mode canon (the #629 5-round gauntlet: no-network pillar, exit leak, deep-link boot, session stash/restore).
- **Model:** kimi-coding/k3 (reasoning tier — user-confirmed back from the billing-cycle cap; probed OK at dispatch). Lens mega-minions: name the model explicitly at every spawn (`kimi-coding/k3`) — and PIN `--cwd <this worktree>` on every lens tab.

## Lens-guards

- **ONE hard blocker class — the no-network pillar (carried from #629):** demo issues ZERO real API calls; the no-network lint + its bite-tests must hold after the polish. Also no regression on the r1–r5 gauntlet classes (exit leak — demo state never bleeds into a real session; deep-link boot; session stash/restore).
- **Fix audit (each of the 6 must bite or be verified-parity):**
  1. Toast placement — the minion verified it's ALREADY the real-app twin (shared `components/toast.gleam`, fixed top-20 right-4; changing it would regress the #615 consent-banner guarantee) and pinned it with a test. Verify the pin + that the #615 guarantee is intact.
  2. Remind + Follow-up state mutation — must mutate the demo row state (→ reminded/followed-up visual state), not just toast.
  3. Compare Top 3 — verified-parity (flows the shared handler + demo-branched /compare fetch, renders for v-maples) + pinned. Verify the pins.
  4. Report detail — the downloaded demo report must match the real report's structure (sections, figures, breakdowns) with demo data.
  5. Logo/wordmark → landing navigation.
  6. a-grace purge — zero `grace` grep hits in demo code (9 renames → a-grainne, PDF re-baked to report-a-grainne.pdf, URL shows the new id).
- **What NOT to re-litigate:** the #629 gauntlet findings (applied); the user's parity-fix rulings (the 5+1 fixes are the spec); the toast/compare verified-parity decisions (unless the pins are broken).
- **What to flag for verification:** the 5 new demo pins (client 626); the no-network lint still bites (poison-style check); the demo fixtures navigate for the new paths.
- **CI note:** GitHub Actions is billing-blocked today (runners never start). Local suite is ground truth: shared 119 / client 626 / server 1527 per the badge-out — re-run the client suite + the no-network lint at minimum.

## Perkins standing orders (verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 630` → `/Users/moses/code/_bmad-output/perkins/righttenantry-demo-polish-1/r1/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the original job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-demo-polish-1/r1`, no `prior_findings` (r1). Headless mode owns pane mechanics, the `<lens>.json` output contract, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and `consolidated.json`. Visual checks: verify MECHANICALLY first (byte/hash/capture-diff); when a visual judgment is unavoidable, run the `vision-read` skill on `lmstudio/qwen/qwen3.8-27b` — never trust a text-only model's eye. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 blockers → `--request-changes`; 4+ → `--request-changes`, body leads with "MAJOR REWORK". **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — STDOUT ONLY, never `2>&1` (stderr cache warnings corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → mint failed; fall back to `gh pr comment 630 --body-file <body.md>`, note `fallback-comment` in your ledger note, call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 630 --<event> --body-file <body.md>`
- Body format: `## 🤖 Perkins automated review — round 1 of 3` header (loop-until-APPROVED), Job, Reviewed sha, Reviewers x/7, Verification counts, Blockers/Warnings/Notes sections, Reviewer agreement, Verdict line, "_Address findings and push — I re-review automatically on the new sha._"
- Before posting, re-fetch `headRefOid` (gh pr view 630 --json headRefOid). If it moved mid-review, post anyway but note "reviewed <old>, head now <new> — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-demo-polish-1-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Skip the code-review skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
