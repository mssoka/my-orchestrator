# Perkins round 3 — packet-plumber-ue-slice-1

- **PR:** https://github.com/solarity-services/Packet-Plumber-UE/pull/3 (PR #3, `slice-1` → `main`)
- **Reviewed sha:** `1c00b5155a67875c353e472f372589a8530a7f25`
- **Repo root:** /Users/moses/code/packet-plumber-ue
- **Round:** 3 (FIX-AUDIT — prior findings from round 2)
- **Original job briefing:** /Users/moses/code/_bmad-output/briefings/packet-plumber-ue-slice-1.md
- **GitHub issue:** none
- **Model:** `zai-coding-cn/glm-5.3` + `--thinking max` (probe OK 14:34Z)
- **Out dir:** /Users/moses/code/_bmad-output/perkins/packet-plumber-ue-slice-1/r3
- **Prior findings:** /Users/moses/code/_bmad-output/perkins/packet-plumber-ue-slice-1/r2/consolidated.json
- **Target stability:** head @1c00b51 verified on origin/slice-1; PR OPEN, MERGEABLE, 2 reviews (r1 CHANGES_REQUESTED 09:09:47Z, r2 CHANGES_REQUESTED 14:15:03Z)

## Perkins standing orders

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff 3` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-ue-slice-1/r3/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = the original job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-ue-slice-1/r3`, `prior_findings` = the r2 `consolidated.json` (re-review: fix audit FIRST, carry-forward markers). The headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r3` labels), the `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and writing `consolidated.json`. Its verdict thresholds are yours below. Visual checks (goldens, sprites): verify MECHANICALLY first (byte/hash/capture-diff); when a visual judgment is unavoidable, run the `vision-read` skill on `lmstudio/qwen/qwen3.8-27b` — the describe_image auto-delegation is retired (user ruling 2026-08-18), never trust a text-only model's eye.
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

  _Address findings and push — I re-review automatically on the new sha._
  ```
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-ue-slice-1-perkins-r3 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.

## Lens guards (this round)

- **Round shape:** r3 FIX-AUDIT of the slice-1 vertical slice. Audit order: (1) fix audit — verify EACH r2 finding (1 blocker + 10 warnings + 16 notes from r2's consolidated.json) against the delta 0256d8a→1c00b51: addressed properly, or addressed-but-broken (worse than before = a NEW blocker), or skipped with no rationale (a blocker); (2) delta review — new surface introduced by the fix (road-anchor Center−(L/2,H/2) with casing, `scripts/verify-capture-geometry.py` committed geometry gate incl. the 37px negative-control claim, PPViewGeometry.h extraction + 3 automation tests, dot +0.5 exactly-once, always-latch same-tick re-step, E4 snap radius scaling with fit, same-tick draws keying TopologyGen, driver terminal guard, spawned formula unification + SCHEMA, bUseFixedFrameRate=False render-clock decision + static check); (3) carry-forward check — anything in r2 NOT part of the delta but still open (e.g. MCP-bridge accepted-risk carry, U-E2 gitignored-ini gap, deserializer, `algorithm`).
- **The ONE hard blocker bar:** the slice's core contract — the **determinism spine is UNTOUCHED** (zero sim-state changes; the r2-approved spine contract holds): spine-check 111 checks green, the engine-golden 3-way (engine PPProbe == standalone spine-check == committed golden) still passes at this sha, PPProbe routing dump consistent, fast 3/3 + full 7/7 gates runnable (the engine IS installed — run them first-hand).
- **Verify specifically (flag, don't assume):** (1) the road-anchor fix is REAL and COMPLETE — roads emerge from node discs in the re-captured frames, `verify-capture-geometry.py` actually bites (run it on BOTH the old 0256d8a-era frame — expect the ~37px failure — and the new frames — expect pass; a gate that passes the bad frame is a blocker); (2) the dot rides the road row in the re-captured frames (pixel-verify y≈road band, not just the minion's claim; the +0.5 offset is applied exactly once); (3) the 8 warning fixes — each guard real and holding (always-latch same-tick re-step, snap radius scaling, same-tick TopologyGen keying, terminal guard, spawned single formula both writers + SCHEMA, FixedFrameRate=False + the static-check, view-geometry tests actually fail on the old bugs); (4) golden discipline held — 111 spine checks, hash unchanged, tick_nonce proof intact, no re-bless in the delta.
- **Do NOT re-litigate:** the user rulings (LOOKS = the primary UE-vs-Odin bake-off criterion; UAD-22 unlit/stylized flat-vector steering vs PBR defaults; UE-MCP approved; LFS strategy; the spine contract verbatim), the r2-APPROVED bootstrap surface, the engine choice, or r2 findings the delta addresses as claimed (verify, then close). The ACTUAL Mini Motorways reference frame is USER-PROVIDED (not on this machine — the PR flags it; IP guardrail: it never enters the repo): the committed surface = the UE frame + the checklist score; the absent literal side-by-side is NOT a defect.
- **Flag for verification (not blockers):** CI red on this PR = GitHub Actions BILLING block (runners never start, ~5s runs, no logs; standing user ruling — local gates are the ground truth).
- **VISION CAVEAT (non-k3 round — verbatim):** pixel verification MECHANICAL only (byte/hash/capture-diff), aesthetic verdicts deferred for the k3 re-check, never faked.
