# Perkins briefing — packet-plumber-v2-7.3-accessibility-core r4

- **Job:** packet-plumber-v2-7.3-accessibility-core · **Round:** 4 (loop-until-APPROVED budget)
- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/72 (Story 7.3: accessibility core)
- **Reviewed sha:** `848b481a0106c1d0f82fe8e9f01f270630d5b6e5` (head of `v2-7.3-accessibility-core`, base `v2`)
- **repo_root:** `/Users/moses/code/packet-plumber` · **Your cwd:** detached worktree at exactly the reviewed sha — trust it, not `origin/v2`
- **Spec pointers:** original job briefing `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-7.3-accessibility-core.md` + the r3 verdict (`prior_findings` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r3/consolidated.json` — 4 blockers @70e3e91) + the PR body's r3→r4 section.
- **Model:** zai-coding-cn/glm-5.3 (STANDING reasoning primary — user ruling 08-19 night; probed OK at dispatch). Lens mega-minions: name the model explicitly at every spawn (`zai-coding-cn/glm-5.3`) — and PIN `--cwd <this worktree>` on every lens tab.

## Lens-guards (fix-audit round — r4)

- **Verify EACH r3 blocker fix BITES:**
  - B1 (r3) — settings-test race on the shared temp path: the fix must remove the shared mutable state (unique paths, no non-atomic `settings_test_seq` counter, or single-threaded suite) AND gate 2 must gain a repeat-run leg. **Verify by running `odin test app` multiple times (≥3 full runs — the r3 failure was schedule-dependent: 10/10 full runs failed while isolated tests passed) — it must be green on every full run.** This is the round's sharpest bar: the r3 review's core finding was that the PR's "10/10" claim was false at the reviewed sha.
  - B2 (r3) — UI-swallowed left presses falling through to the world path: the `ui` gate must be restored over the whole world path (base-v2 shape: `if ui {…} else {tray…node…Begin_Draw}`) — a press swallowed by the QoS panel / crisis banner / SLA rows / demolish popover must NOT run tray hit-tests or node snap. Verify by tracing mouse.odin's world-path gate + ideally a test/pin.
  - B3 (r3) — SLA/pool gauge scaling: the pool call site, row pitch, anchors, and `sla_row_rect` must hud()-scale; no ×1.25 SLA-header-on-pool-label collision, no ×1.50 row self-overlap. Verify the geometry at both scales.
  - B4 (r3) — test gate P0: settings_click→adjust must be driven in a test (the exact hole the r2 delta-0 no-op shipped through — deleting the adjust call must now FAIL CI), `odin test app/audio` in gate 2 + the workflow, one startup/pause assert, QoS scaled geometry pinned.
- **ONE hard blocker class (carried): the never-color-alone invariant (ODN-1)** + palcheck oracle in the CORRECTED sRGB space (min dists 51.3/54.7/43.0 hold; poison pair still fails).
- **Presentation-only discipline (carried):** no core/, no LOG_VERSION, no catalog edits; goldens pure-presentation; ×1.00 identity.
- **What NOT to re-litigate:** the r3 4-blocker fixes (audit they LANDED, don't re-argue); user rulings (scaling knob, settings modal, reduced-motion static); applied canon.
- **CI note:** GitHub Actions is billing-blocked today. Local suite is ground truth — the merge ground-truth gate: `tools/ci-local.sh --mac` must pass INCLUDING repeated full `odin test app` runs (the r3 race) + the four test binaries + palcheck + 27/27 parity.

## Perkins standing orders (verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 72` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r4/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the original job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r4`, `prior_findings` = the r3 `consolidated.json` (fix audit first, carry-forward markers). Headless mode owns pane mechanics, the `<lens>.json` output contract, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and `consolidated.json`. Visual checks: verify MECHANICALLY first (byte/hash/capture-diff); when a visual judgment is unavoidable, run the `vision-read` skill on `lmstudio/qwen/qwen3.8-27b` — never trust a text-only model's eye. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 blockers → `--request-changes`; 4+ → `--request-changes`, body leads with "MAJOR REWORK". **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — STDOUT ONLY, never `2>&1` (stderr cache warnings corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → mint failed; fall back to `gh pr comment 72 --body-file <body.md>`, note `fallback-comment` in your ledger note, call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 72 --<event> --body-file <body.md>`
- Body format: `## 🤖 Perkins automated review — round 4 of 3` header (loop-until-APPROVED), Job, Reviewed sha, Reviewers x/7, Verification counts, Blockers/Warnings/Notes sections, Reviewer agreement, Verdict line, "_Address findings and push — I re-review automatically on the new sha._"
- Before posting, re-fetch `headRefOid` (gh pr view 72 --json headRefOid). If it moved mid-review, post anyway but note "reviewed <old>, head now <new> — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-7.3-accessibility-core-perkins-r4 working` at start; final message = verdict + review URL + findings counts.
- Skip the code-review skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
