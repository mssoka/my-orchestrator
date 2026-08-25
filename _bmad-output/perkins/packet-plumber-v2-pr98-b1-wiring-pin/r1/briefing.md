# Perkins briefing — round 1: packet-plumber-v2-pr98-b1-wiring-pin

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/98 (targets `v2`)
- **Reviewed sha:** `1bec4e35d43c7ea6fed2741d4351483a34e3ada1` (short `1bec4e3`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 (no prior findings — fresh round)
- **Your cwd:** `/Users/moses/code/packet-plumber/.herdr/worktrees/pp-pr98-b1-wiring-pin-r1` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** this is a **USER-AUTHORED PR** (author mssoka, no implementing minion — there is NO job briefing and NO GitHub issue; the spec IS the PR body + the #97 r1 B1 finding being fixed):
  - PR body: `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-pr98-b1-wiring-pin/r1/pr-body.txt`
  - The B1 finding being fixed: `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-pr98-b1-wiring-pin/r1/pr97-b1-review.txt` (review 5012533699 on PR #97 — read its B1 blocker + verified table; the rest of #97's warnings are OUT OF SCOPE for this round)
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **Canonical diff (already saved):** `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-pr98-b1-wiring-pin/r1/diff.patch` (80 lines). Every lens reviews these identical bytes. The PR is TEST-ONLY — the diff should touch ONLY test files; flag any non-test change.

## The claim under review (verify, don't assume)

PR #97 established `camera_set_default` as the camera's resting home, but its test called `camera_set_default` directly (self-referential → mutation-invisible). **This PR pins the resting-home wiring so it is mutation-VISIBLE: three new tests drive the REAL routing paths — `start_run`, `effect_cancel`, and the deselect else-branch of `camera_set_selection` — NOT a bare `camera_set_default(&app)` call.** Removing any of the three `camera_set_default(app)` routing calls (`main.odin:972/:1135/:1800`) must turn the suite RED.

**Verified claims to check against the worktree (run the suites yourself):**
- `odin test app`: 46 green (43 baseline + 3 new)
- `odin test core`: 261 green (unchanged)
- `odin test app/render`: 81 green (unchanged)
- Mutation-visibility: removing the routing call at start_run (:972), effect_cancel (:1135), and deselect (:1800) each fails the corresponding new test; all three removed = 3 failures
- Legacy test `camera_set_default_homes_on_the_source_cluster` stays green throughout
- Test-only change: camera logic, goldens, tools/ untouched

## ⚠️ Lens guards (read before any lens — the false-positive firewall)

- **This is a fix-forward for ONE blocker (B1).** #97's B2/W1–W5 were scope of THAT round; this PR addresses B1 only. Do NOT re-litigate #97's other findings as blockers here — the user scoped this PR deliberately. (If you judge B2's advisory gate still fails because W1/W4 remain unpinned, that is a NOTE/WARNING carrying context, never a blocker on this PR.)
- **#97 was merged by the human over CHANGES_REQUESTED** — do not question the merge itself, do not demand the unmerged findings be folded into #98. Review #98 on its own scope.
- **The core hard gate: mutation-visibility is REAL, not theater.** A "new test" that merely calls `camera_set_default(&app)` again (replicating the self-referential pattern) is a FAILED fix. Each new test must exercise an actual entry-point routing path (start_run / effect_cancel / camera_set_selection-deselect-else) and the assertion must be capable of failing (e.g. asserts `cam_zoom_to == DEFAULT_ZOOM` / home anchor) when the routing call is removed. **Prove it by mutation: delete each routing call in your worktree copy and run the suite — the corresponding test MUST fail.** If it passes, that pin is vacuous = blocker.
- **Watch for the vacuous-pin class** (the PP v2 wave's dominant blocker class): a test that passes whether or not the thing it guards exists; a test asserting the same constant it reads; a test exercising a path the production code never calls. Mutation is the arbiter.
- **Watch for duplicated/intended-to-fail tests**: three tests that all assert the identical thing through identical paths are one pin wearing three names.
- **Watch for fixture/topology leaks** (N4-class hygiene from #97): bare Topology without teardown — note-level, not blocker.
- **Brittleness counts**: tests that pass by luck of ordering, or that could go green without the routing call because another path also calls `camera_set_default` (over-pinning). Verify each new test isolates its route.
- **CI is GREEN at this sha** (4/4 verify, completed 00:40Z) — your local runs are the ground truth; trust the suite you run, not the PR's reported numbers.
- **No em-dashes** (PP repo convention ban) — test names/strings in the diff.

### Legitimate findings here would be
- A pin that is still self-referential (calls the proc directly instead of the routing entry point).
- A pin that does NOT fail when its routing call is removed (mutation-prove it).
- A routing call left unpinned (the three are pinned — is there a FOURTH `camera_set_default` routing call site, or another resting-home entry point like ESC/boot/reset, that remains mutation-invisible? #97's B1 named :972/:1135/:1800 — verify completeness).
- A test that passes for the wrong reason (over-pinning: another path also sets the home, so deleting the target call doesn't fail).
- Non-test changes smuggled into a "test-only" PR (goldens, tools/, camera logic).
- The legacy test broken/removed.
- Suite-count claims false (run them).

## Vision caveat (NON-k3 round — verbatim)

This round runs on glm-5.3 (k3 403-capped at dispatch). **Pixel verification MECHANICAL only (byte/hash/capture-diff); aesthetic verdicts deferred for the k3 re-check, never faked.** (This PR is test-only — no pixels expected to move; if the diff somehow touches goldens, treat byte-diff mechanically.)

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane (here: no minion exists — the human authored and merges).
- Context: PR URL + number, reviewed sha, repo_root, this briefing + the PR body + the #97 B1 review (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/v2`.
- Canonical diff (already saved): `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-pr98-b1-wiring-pin/r1/diff.patch`.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the PR body + the #97 B1 review, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-pr98-b1-wiring-pin/r1`, and NO `prior_findings` (r1). The headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), the `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and writing `consolidated.json`. **Lens-spawn rooting: the headless spawn template pins `--cwd <worktree>` on every lens tab FOREVER — a lens pane whose cwd is not the round worktree is mis-rooted: close + relaunch with `--cwd`.**
- **Empty-lens doctrine:** acceptance/architecture lenses back 3-byte-EMPTY a THIRD straight generation → sweep those lens panes + regenerate (an empty-lens verdict never ships); a g-wave COMPENSATION verdict (a subset of lenses delivering a valid verdict) counts as valid.
- Visual checks (goldens, sprites): verify MECHANICALLY first (byte/hash/capture-diff); when a visual judgment is unavoidable, run the `vision-read` skill (KYLE) — never trust a text-only model's eye. On this non-k3 round, the vision caveat above applies.
- You MUST close every lens pane before finishing.
- **Verdict → review event:**
  - 0 blockers → `--approve`
  - 1–3 blockers → `--request-changes`
  - 4+ blockers → `--request-changes`, body leads with "MAJOR REWORK"
  - **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru ("incomplete review").
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (the script writes cache warnings to stderr that corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 98 --repo solarity-services/Packet-Plumber --body-file <body.md>`, note `fallback-comment` in your ledger note + final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 98 --repo solarity-services/Packet-Plumber --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow" in the body.
- Body format:
  ```
  ## 🤖 Perkins automated review — round 1
  **Job:** packet-plumber-v2-pr98-b1-wiring-pin · **Reviewed sha:** 1bec4e3 · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed against the code — <rejected> discarded as false-positive[, <u> kept as unverified]

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Address findings and push — I re-review automatically on the new sha.
  The loop runs until an APPROVED verdict._
  ```
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-pr98-b1-wiring-pin-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — there is no implementing minion; the verdict routes to Gru → the user.
