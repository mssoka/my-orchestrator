# Perkins round 2 — packet-plumber-ue-slice-1

- **PR:** https://github.com/solarity-services/Packet-Plumber-UE/pull/3 (PR #3, `slice-1` → `main`)
- **Reviewed sha:** `0256d8aad43d3029ac88538c1e67c577660d84ae`
- **Repo root:** /Users/moses/code/packet-plumber-ue
- **Round:** 2 (FIX-AUDIT — prior findings from round 1)
- **Original job briefing:** /Users/moses/code/_bmad-output/briefings/packet-plumber-ue-slice-1.md
- **GitHub issue:** none
- **Model:** `zai-coding-cn/glm-5.3` + `--thinking max` (probe OK 11:47Z)
- **Out dir:** /Users/moses/code/_bmad-output/perkins/packet-plumber-ue-slice-1/r2
- **Prior findings:** /Users/moses/code/_bmad-output/perkins/packet-plumber-ue-slice-1/r1/consolidated.json
- **Target stability:** head @0256d8a verified on origin/slice-1; PR OPEN, MERGEABLE, 1 review (r1 CHANGES_REQUESTED 09:09:47Z)

## Perkins standing orders

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff 3` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-ue-slice-1/r2/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = the original job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-ue-slice-1/r2`, `prior_findings` = the r1 `consolidated.json` (re-review: fix audit FIRST, carry-forward markers). The headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r2` labels), the `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and writing `consolidated.json`. Its verdict thresholds are yours below. Visual checks (goldens, sprites): verify MECHANICALLY first (byte/hash/capture-diff); when a visual judgment is unavoidable, run the `vision-read` skill on `lmstudio/qwen/qwen3.8-27b` — the describe_image auto-delegation is retired (user ruling 2026-08-18), never trust a text-only model's eye.
- You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 blockers → `--request-changes`; 4+ blockers → `--request-changes`, body leads with "MAJOR REWORK". **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru ("incomplete review").
- Post as the app (owner parsed from the PR URL). Mint first, then review — never run gh with an empty GH_TOKEN (a failed command substitution would fall through to the ambient `mssoka` credential and 422 on our own PRs):
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — capture STDOUT ONLY. NEVER append `2>&1`.
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → the mint failed; fall back to `gh pr comment 3 --body-file <body.md>`, note `fallback-comment` in your ledger note, and call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 3 --<event> --body-file <body.md>`
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
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-ue-slice-1-perkins-r2 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.

## Lens guards (this round)

- **Round shape:** r2 FIX-AUDIT of the slice-1 vertical slice. Audit order: (1) fix audit — verify EACH r1 finding (2 blockers + 16 warnings from r1's consolidated.json) against the delta 9dabfbe→0256d8a: addressed properly, or addressed-but-broken (worse than before = a NEW blocker), or skipped with no rationale (a blocker); (2) delta review — new surface introduced by the fix (constructor-built UInputActions, CDO-carried bindings, headless drag test, pixel-verified packet-dot capture pipeline, DPI-aware fit, shared PP::SpawnFixture, StateHash growth guard, same-tick re-step latch, E29 recovery path, ApplyEdit live-path); (3) carry-forward check — anything in r1 that is NOT part of the delta but remains open.
- **The ONE hard blocker bar:** the slice's core contract — the **determinism spine is UNTOUCHED** (zero sim-state changes; the r2-approved spine contract holds): spine-check 91 checks green, the engine-golden 3-way (engine PPProbe == standalone spine-check == committed golden) still passes at this sha, PPProbe routing dump consistent, fast 3/3 + full 7/7 gates runnable (the engine IS installed — run them first-hand).
- **Verify specifically (flag, don't assume):** (1) Blocker-1 fix is REAL — UInputActions now exist from the constructor (CDO), SetupInputComponent-order hazard closed (bind no longer captures null), and the headless tests actually bind + Execute + synthesize a drag that creates a pipe (run the tests; don't trust the claim); (2) Blocker-2 fix is HONEST — the re-captured packet-dot evidence is pixel-verified (the minion claims 4 distinct mid-edge positions × 12 frames, x=223/272/320-326/369-375) AND vision-confirmed, the committed PNG contains real #3E7CB1-ish pixels (pixel-scan the committed frame mechanically first), the vacuous-easing + DPI-scale + pool-wipe + zero-ImageSize + NativeTick-paint cascade is genuinely fixed and the dot renders in-session; (3) the 12 warning fixes (StateHash grow w/o fail-open, StepScenario dynamic, EqualCostHops stale-table guard, same-tick re-step latch, ApplyEdit live-path + live-vs-replay convergence, E29 recovery, serve contention, mixed-tier steering, camera fit single-source, road rotation pivot, E4 screen-space snap px-exact, shared PP::SpawnFixture UAD-17) — each one: is the guard real and does it hold; (4) golden discipline held — 111 spine checks, hash unchanged, tick_nonce proof intact, the re-bless is NOT masking a regression.
- **Do NOT re-litigate:** the user rulings (LOOKS = the primary UE-vs-Odin bake-off criterion; UAD-22 unlit/stylized flat-vector steering vs PBR defaults; UE-MCP approved; LFS strategy; the spine contract verbatim), the r2-APPROVED bootstrap surface, the engine choice, or r1 findings that the delta addresses as claimed (verify, then close). The ACTUAL Mini Motorways reference frame is USER-PROVIDED (not on this machine — the PR flags it; IP guardrail: it never enters the repo): the committed surface = the UE frame + the checklist score; the absent literal side-by-side is NOT a defect.
- **Flag for verification (not blockers):** CI red on this PR = GitHub Actions BILLING block (runners never start, ~5s runs, no logs; standing user ruling — local gates are the ground truth).
- **VISION CAVEAT (non-k3 round — verbatim):** pixel verification MECHANICAL only (byte/hash/capture-diff), aesthetic verdicts deferred for the k3 re-check, never faked.
