# Perkins briefing — packet-plumber-v2-6.3-upgrade-lifecycle r1

- **Job:** packet-plumber-v2-6.3-upgrade-lifecycle · **Round:** 1 (loop-until-APPROVED budget)
- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/74 (the upgrade lifecycle — legacy decay + modernize; GDD M4, stories-v2 6.3)
- **Reviewed sha:** `9bce5bae53d980157df7ca5e41366caccd9d9795` (head of `v2-6.3-upgrade-lifecycle`, base `v2`)
- **repo_root:** `/Users/moses/code/packet-plumber` · **Your cwd:** detached worktree at exactly the reviewed sha — trust it, not `origin/v2`
- **Spec pointers:** original job briefing `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-6.3-upgrade-lifecycle.md` (canon: GDD E5.3 + §M4 metaphor boundary, ODN-16 era FSM, the 6.1 eras.json infra + 6.2 advance gate + legacy predicate seam, 2.3 demolish, 5.6 router tiers) + the PR body's Decisions & rationale (incl. the draw-era-tracking rejection argument).
- **Model:** zai-coding-cn/glm-5.3 (standing reasoning primary; probed OK at dispatch). Lens mega-minions: name the model explicitly at every spawn (`zai-coding-cn/glm-5.3` — the MODEL PIN: resolve from this briefing, never bare) + `--thinking max` — and PIN `--cwd <this worktree>` on every lens tab.

## Lens-guards

- **ONE hard blocker class — the determinism/replay spine + the decay
  measurability contract:** legacy decay must be DETERMINISTIC and MEASURABLE
  (effective throughput decays by an integer-only, catalog-driven factor —
  the [ODN-5] pattern; the sim's routing/drop behavior reflects reduced
  effective capacity, NEVER a view-only illusion). The golden contrast
  (legacy_decay.dem vs legacy_modernized.dem — identical seed/topology/
  demand, one run modernizing at the fire) is the measurability contract:
  verify the T1 contrast is real and the decay is reflected in behavior.
- **Fix audit (the deliverables):** (1) legacy-decay model — catalog-driven,
  fail-fast validated, integer-only, deterministic; (2) modernize —
  Cmd_Set_Pipe_Tier logged, STRICTLY-upward (LOG_VERSION 5→6, .Not_An_Upgrade
  rejects same/lower), demolish restores by construction; (5) goldens —
  legacy_decay + legacy_modernized, fold-check PASS, 45 .log.bin header-only,
  era-0/1 T2s byte-identical, the 42 changed T2s era-2/3 (traffic-density,
  vision-verified); (6) canon fold.
- **Honest costs to verify (cause-documented, not defects):** era-3
  narrows/standards now decay (the rate-staged test fixtures re-pinned,
  W10/W11 access contracts on WIDE, E16 drain-rate re-tuned, stats pins decay
  at cap 15→7). The draw-era tracking REJECTION (GDD M1 + the blessed 6.2
  goldens pin the tier predicate) — verify the argument holds, don't re-open
  it.
- **What NOT to re-litigate:** the 6.1/6.2 landed infra (eras.json, advance
  gate, legacy predicate seam — APPROVED rounds); the draw-era rejection;
  user rulings (loop-until-APPROVED, canon M4 boundary); the fold-forward
  items already applied from 6.2's rounds (demand_era binding, sparse-era
  gaps — check they held through this rework, warning-tier).
- **What to flag for verification:** the re-pinned fixtures' honesty (the
  era-3 re-stage blast radius — a fixture re-pin can hide a behavior
  regression); the LOG_VERSION 6 header discipline; the 228/228 core tests
  + 9 new contracts bite; no regression on the gate demos (6.2's
  bit-for-bit replays must hold at this sha).
- **CI note:** GitHub Actions is billing-blocked. Local suite is ground
  truth: `tools/ci-local.sh --mac` 10/10 per the badge-out — re-run at
  minimum the core suite + the gate demos + the fold-check.

## Perkins standing orders (verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 74` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-6.3-upgrade-lifecycle/r1/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the original job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-6.3-upgrade-lifecycle/r1`, no `prior_findings` (r1). Headless mode owns pane mechanics, the `<lens>.json` output contract, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and `consolidated.json`. Visual checks: verify MECHANICALLY first (byte/hash/capture-diff); when a visual judgment is unavoidable, run the `vision-read` skill on `lmstudio/qwen/qwen3.8-27b` — never trust a text-only model's eye. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 blockers → `--request-changes`; 4+ → `--request-changes`, body leads with "MAJOR REWORK". **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — STDOUT ONLY, never `2>&1` (stderr cache warnings corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → mint failed; fall back to `gh pr comment 74 --body-file <body.md>`, note `fallback-comment` in your ledger note, call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 74 --<event> --body-file <body.md>`
- Body format: `## 🤖 Perkins automated review — round 1 of 3` header (loop-until-APPROVED), Job, Reviewed sha, Reviewers x/7, Verification counts, Blockers/Warnings/Notes sections, Reviewer agreement, Verdict line, "_Address findings and push — I re-review automatically on the new sha._"
- Before posting, re-fetch `headRefOid` (gh pr view 74 --json headRefOid). If it moved mid-review, post anyway but note "reviewed <old>, head now <new> — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-6.3-upgrade-lifecycle-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Skip the code-review skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
