# Perkins briefing — packet-plumber-v2-6.2-advance-trigger r1

- **Job:** packet-plumber-v2-6.2-advance-trigger · **Round:** 3 (loop-until-APPROVED budget)
- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/71 (story 6.2: the era advance trigger — the modernization gate)
- **Reviewed sha:** `464db76a23603e835aa0602a9492dac6ed0b73a7` (head of `v2-6.2-advance-trigger`, base `v2`)
- **repo_root:** `/Users/moses/code/packet-plumber` · **Your cwd:** detached worktree at exactly the reviewed sha — trust it, not `origin/v2`
- **Spec pointers:** the original job briefing `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-6.2-advance-trigger.md` (if present) + the parent 6.1 row's fold-forward (below) + `stories-v2.md` §Story 6.2 (implemented) + the GitHub issue if any (`gh issue view` — the 6.2 spec lives in the briefing/stories). No GitHub issue exists for this job.
- **Model:** kimi k3 (reasoning tier; probed OK 08:14Z/09:10Z — regime file OK). Lens mega-minions: name the model explicitly at every spawn per the code-review skill's headless template — and PIN `--cwd <this worktree>` on every lens tab (the 08-18 mis-rooted-lens class).

## Lens-guards (fix-audit round — r3)

- **Verify the r2 blocker fix BITES — the scripted-advance gate test must
  no longer be vacuous:** the fix must assert the `Era_Advanced` event tick
  >= 600 (or step 500 ticks and expect era == 2 with the latch held). A
  scripted `Cmd_Era_Advance` that ignores the gate must now FAIL the test
  (the r2 finding: an ungated fire at tick 100 also landed era 3, and the
  collected-but-unasserted tick was the only differentiator). Verify by
  reverting the gate in a scratch check — the pin must bite.
- **Carried (verified r2 — spot-verify they hold):** B1 gate-goldens
  gate-ON + bit-for-bit replays (tick-600 divergence gone), the drift flips
  re-simming (instrumented probe), 10/10 ci-local. The carried r3 items the
  minion folded (block-event count pins, scripted-while-blocked, E15
  fire_tick, ODN-16 citation, the r2 trio) — check the high-value ones
  landed, warning-tier.
- **ONE hard blocker class (carried): the determinism/replay spine.**
- **What NOT to re-litigate:** the r2 blocker fix (audit it LANDED); 6.1
  era infra; the gate's request->latch->fire mechanics.
- **CI note:** GitHub Actions is billing-blocked. Local suite is ground
  truth — re-run ci-local + the gate demos + drift-check at minimum.

## Perkins standing orders (verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 71` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-6.2-advance-trigger/r3/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the original job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-6.2-advance-trigger/r3`, `prior_findings` = the r2 `consolidated.json` (fix audit first, carry-forward markers). Headless mode owns pane mechanics, the `<lens>.json` output contract, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and `consolidated.json`. Visual checks: verify MECHANICALLY first (byte/hash/capture-diff); when a visual judgment is unavoidable, run the `vision-read` skill on `lmstudio/qwen/qwen3.8-27b` — never trust a text-only model's eye. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 blockers → `--request-changes`; 4+ → `--request-changes`, body leads with "MAJOR REWORK". **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — STDOUT ONLY, never `2>&1` (stderr cache warnings corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → mint failed; fall back to `gh pr comment 71 --body-file <body.md>`, note `fallback-comment` in your ledger note, call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 71 --<event> --body-file <body.md>`
- Body format: `## 🤖 Perkins automated review — round 3 of 3` header (loop-until-APPROVED), Job, Reviewed sha, Reviewers x/7, Verification counts, Blockers/Warnings/Notes sections, Reviewer agreement, Verdict line, "_Address findings and push — I re-review automatically on the new sha._"
- Before posting, re-fetch `headRefOid` (gh pr view 71 --json headRefOid). If it moved mid-review, post anyway but note "reviewed <old>, head now <new> — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-6.2-advance-trigger-perkins-r3 working` at start; final message = verdict + review URL + findings counts.
- Skip the code-review skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
