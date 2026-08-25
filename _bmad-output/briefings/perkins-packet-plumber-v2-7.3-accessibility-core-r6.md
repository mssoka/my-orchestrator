# Perkins briefing — packet-plumber-v2-7.3-accessibility-core r4

- **Job:** packet-plumber-v2-7.3-accessibility-core · **Round:** 6 (loop-until-APPROVED budget)
- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/72 (Story 7.3: accessibility core)
- **Reviewed sha:** `fe233c075599c55841e7040a4a5ea7ee5dbba0f0` (head of `v2-7.3-accessibility-core`, base `v2`)
- **repo_root:** `/Users/moses/code/packet-plumber` · **Your cwd:** detached worktree at exactly the reviewed sha — trust it, not `origin/v2`
- **Spec pointers:** original job briefing `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-7.3-accessibility-core.md` + the r3 verdict (`prior_findings` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r5/consolidated.json` — 4 blockers @70e3e91) + the PR body's r3→r4 section.
- **Model:** zai-coding-cn/glm-5.3 (STANDING reasoning primary — user ruling 08-19 night; probed OK at dispatch). Lens mega-minions: name the model explicitly at every spawn (`zai-coding-cn/glm-5.3`) — and PIN `--cwd <this worktree>` on every lens tab.

## Lens-guards (fix-audit round — r6)

- **Verify the r5 blocker fix BITES — the effect_settings WIRING must be
  pinned (the r5 miss: the pin guarded settings_pause_effect, the pure
  proc, while deleting the flip in effect_settings itself still passed
  CI 16/16 — the r4 failure mode persisted CI-silent):** the fix must add
  the exec/effect-level leg (the a11y_apply precedent): construct
  App+Input, call effect_settings, assert open flips Run->Paused and close
  leaves it Paused. **Verify by the revert-style check: deleting the flip
  in effect_settings must now FAIL CI.** If the pin still only covers the
  helper, that's the blocker again.
- **Carried (verified-fixed r3/r4/r5, spot-verify they hold at this sha):
  the settings-test race** (nanosecond-unique paths + gate-2 repeat leg —
  repeated full `odin test app` runs must stay green), **the ui-swallow
  gate** (base-v2 shape), **SLA/pool hud scaling**, **linear_to_srgb**
  (both copies, min dists 51.3/54.7/43.0, poison bites).
- **ONE hard blocker class (carried): the never-color-alone invariant
  (ODN-1)** + palcheck oracle in the corrected sRGB space.
- **Presentation-only discipline (carried):** no core/, no LOG_VERSION, no
  catalog edits; goldens pure-presentation; x1.00 identity.
- **What NOT to re-litigate:** the r5 blocker fix (audit it LANDED); user
  rulings; applied canon.
- **CI note:** GitHub Actions is billing-blocked today. Local suite is
  ground truth — `tools/ci-local.sh --mac` incl. repeated `odin test app`
  + the four test binaries + palcheck + 27/27 parity.

## Perkins standing orders (verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 72` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r4/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the original job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r4`, `prior_findings` = the r4 `consolidated.json` (fix audit first, carry-forward markers). Headless mode owns pane mechanics, the `<lens>.json` output contract, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and `consolidated.json`. Visual checks: verify MECHANICALLY first (byte/hash/capture-diff); when a visual judgment is unavoidable, run the `vision-read` skill on `lmstudio/qwen/qwen3.8-27b` — never trust a text-only model's eye. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 blockers → `--request-changes`; 4+ → `--request-changes`, body leads with "MAJOR REWORK". **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — STDOUT ONLY, never `2>&1` (stderr cache warnings corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → mint failed; fall back to `gh pr comment 72 --body-file <body.md>`, note `fallback-comment` in your ledger note, call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 72 --<event> --body-file <body.md>`
- Body format: `## 🤖 Perkins automated review — round 6 of 3` header (loop-until-APPROVED), Job, Reviewed sha, Reviewers x/7, Verification counts, Blockers/Warnings/Notes sections, Reviewer agreement, Verdict line, "_Address findings and push — I re-review automatically on the new sha._"
- Before posting, re-fetch `headRefOid` (gh pr view 72 --json headRefOid). If it moved mid-review, post anyway but note "reviewed <old>, head now <new> — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-7.3-accessibility-core-perkins-r4 working` at start; final message = verdict + review URL + findings counts.
- Skip the code-review skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
