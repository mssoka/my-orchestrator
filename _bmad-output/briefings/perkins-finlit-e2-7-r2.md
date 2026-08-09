# Briefing: perkins-finlit-e2-7-r2 (Perkins automated review, round 2)

- **Job under review:** finlit-e2-7
- **PR:** https://github.com/solarity-services/finlit/pull/11 (#11)
- **Reviewed sha:** 64cc48793eb5ba977ba6a17f296e6d2b895933e1
- **repo_root:** /Users/moses/code/kids-finlit-game
- **Round:** 2 of 3
- **Original job briefing (your spec):** /Users/moses/code/_bmad-output/briefings/finlit-e2-7.md — A29 touch-target rules (≥160px primary / ≥120px secondary floors, FIND WORK > FIX oldest-damaged-first > BUY/UPGRADE > WORK SHIFT priority, modal-card interplay, touch-proxy rect math) for the finlit Godot street scene.
- **GitHub issue:** none.
- **Your cwd:** /Users/moses/.herdr/worktrees/kids-finlit-game/perkins-e2-7-r2 (at exactly the reviewed sha)
- **Ledger round id:** finlit-e2-7-perkins-r2
- **prior_findings (round 1):** /Users/moses/code/_bmad-output/perkins/finlit-e2-7/r1/consolidated.json

## Perkins standing orders (verbatim from the playbook)

- You are Perkins. You review; you never fix, push, or merge. You never
  touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job
  briefing** and **GitHub issue** (your spec), and your cwd — a worktree
  at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first:
  `gh pr diff 11` →
  `/Users/moses/code/_bmad-output/perkins/finlit-e2-7/r2/diff.patch`.
  Every lens reviews these identical bytes. (Absolute path — the round
  worktree is destroyed at close-out, so artifacts live in the
  orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated
  Mode** with: `diff_file` = the canonical diff just saved, `worktree` =
  your cwd, `spec_files` = the original job briefing + the GitHub issue
  (none here), `out_dir` =
  `/Users/moses/code/_bmad-output/perkins/finlit-e2-7/r2`, and
  `prior_findings` = `/Users/moses/code/_bmad-output/perkins/finlit-e2-7/r1/consolidated.json`
  (re-review: **fix audit first**, carry-forward markers). The headless mode
  owns: pane mechanics (dedicated tab, `mm-<lens>-r2` labels), the
  `<lens>.json` output contract + existence check, one retry per failed
  lens, big-diff chunking, the mandatory verification pass, consolidation,
  and writing `consolidated.json`. Its verdict thresholds are yours below.
  You MUST close every lens pane before finishing.
- **Verdict → review event:**
  - 0 blockers → `--approve`
  - 1–3 blockers → `--request-changes`
  - 4+ blockers → `--request-changes`, body leads with "MAJOR REWORK"
  - **Degraded guard:** any lens failed AND zero findings remain → do NOT
    approve; `--comment` instead and flag Gru ("incomplete review").
- Post as the app (owner parsed from the PR URL). Mint first, then
  review — never run gh with an empty GH_TOKEN (a failed command
  substitution would fall through to the ambient `mssoka` credential and
  422 on our own PRs):
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner <owner>)`
  2. If that failed (non-zero exit): fall back to `gh pr comment <pr>
     --body-file <body.md>`, note `fallback-comment` in your ledger note,
     and call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file
     <body.md>`
- Body format:
  ```
  ## 🤖 Perkins automated review — round 2 of 3
  **Job:** finlit-e2-7 · **Reviewed sha:** `64cc487` · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed against the code — <rejected> discarded as false-positive[, <u> kept as [unverified]]

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Address findings and push — I re-review automatically on the new sha.
  After round 3, the human takes over._
  ```
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post
  anyway but note "reviewed `64cc487`, head now `<new>` — a fresh round
  will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set finlit-e2-7-perkins-r2 working` at
  start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely —
  fixing is the implementing minion's job, triggered by the review relay.

## Round-2 specifics — REBASE RE-REVIEW (this is the load-bearing focus)

- `<job-id>` = finlit-e2-7, `<N>` = 2, `<pr>` = 11,
  `<owner>` = solarity-services, `<round-id>` = finlit-e2-7-perkins-r2.
- **Why r2 exists:** round 1 reviewed + APPROVED sha `4cd9aa7` (0 blockers, 3 warnings, 6 notes — all advisory). The branch then **rebased onto a moved main**: `finlit#10` (e2-1 playtest protocol + capture tooling) and `finlit#12` (GDD amendments) merged to main AFTER e2-7 diverged. The rebase conflict-resolved `game/scripts/street.gd` (e2-1 added ~83 lines there too) and `game/scenes/street.tscn` (+12). New head: `64cc487`, now CLEAN/MERGEABLE. **r2 is a rebase re-review**, not a cold review.
- **The three things r2 must establish (in priority order):**
  1. **Rebase content-preservation audit (highest priority).** Verify e2-7's touch-target code survived the rebase **intact and semantically identical** to the r1-APPROVED `4cd9aa7` content. Concretely confirm present and unaltered in `street.gd`/`touch_targets.gd`/`touch_proxy.gd`: the ≥160px primary / ≥120px secondary floors, the dominant-action priority `FIND WORK > FIX oldest-damaged-first > BUY/UPGRADE > WORK SHIFT`, `_on_dominant_pressed` dispatch wired to `dominant_action()`, `_shift_ready()` cooldown gate, the bounded 300-frame `process_frame` proxy-wrap poll (NOT the unbounded `await reset.resized` the old docs cited), viewport-clamped `touch_proxy_rect`. Run the 295-check GUT suite (`gdut` / bare runner) — must stay 295/0. **Any drift in e2-7 logic from the conflict resolution = a blocker**, not a warning — the rebase must be content-preserving for the r1 approval to carry.
  2. **e2-1 interaction hunt.** e2-1's playtest capture tooling (`playtest_session.gd`, `game/tools/capture.gd`, +83 lines in `street.gd`) now coexists with e2-7's touch-target/dominant-button code in the same files. Hunt for **semantic conflicts the textual 3-way merge resolved cleanly but that break at runtime**: does playtest input capture route correctly through the touch proxies? Does the dominant button behave during a playtest capture session? Does e2-1's street.gd additions touch the same functions/regions e2-7 modified (e.g. `_open_popup`, the reset button, `_on_dominant_pressed`)? A clean textual merge ≠ a correct runtime merge.
  3. **Fix-audit r1's findings (carry-forward).** From `prior_findings` (r1/consolidated.json): r1's 3 warnings — (W1) transient sub-120px NEW GAME hit window during pop-in before the proxy wraps (`street.gd:756-778`); (W2) `_on_dominant_pressed` press dispatch never exercised by any test (`street.gd:388`); (W3) advisory test gate CONCERNS — plus 6 notes (theme `min_touch_size` unconsumed; `_shift_ready` untested; defensive `id<0` skip unreachable; committed review artifact describes pre-fix commit; docs cite unbounded `await` vs shipped bounded poll; `first_upgradeable` missing id guard). Mark each carry-forward / addressed / worsened-by-rebase. These were advisory at r1; they stay advisory UNLESS the rebase re-introduced or worsened them.
- **Not findings (disclosed, do not flag):** the A29 confirmation ask — four touch-target rules implemented as proposed, awaiting user ack in the PR body (each is a one-line constant change if ruled differently). That is the PR's open question, not a defect. The theme `min_touch_size` "design surface, not enforcement" disclosure stands.
- The minion's own pre-PR review swarm (adversarial 13 + edge 6 findings, all fixed) ran before r1; Perkins is the independent gate. Godot 4.7.1 / GDScript; GUT headless is the test runner.
