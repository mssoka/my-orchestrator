# Perkins round: pp-funfix-118-124-perkins-r1

**PR:** https://github.com/solarity-services/Packet-Plumber/pull/125 (number 125)
**Reviewed sha:** 7b109d3a6db66743c6524f89a98ccd2aac9855e2 (re-fetch headRefOid before posting; if moved, post anyway + note)
**Repo root:** /Users/moses/code/packet-plumber · **Your cwd:** your detached round worktree at exactly the reviewed sha
**Spec:** the original job briefing /Users/moses/code/_bmad-output/briefs/pp-funfix-118-124.md + the evidence base: gh issue view 118 and 124 (solarity-services/Packet-Plumber), docs/playtests/2026-08-31-{fun,stress,neweyes}.md
**Round dir:** /Users/moses/code/_bmad-output/perkins/pp-funfix-118-124/r1/
**prior_findings:** none (round 1)
**Model:** zai-coding-cn/glm-5.3-flash (natively multimodal; pixel measurements decide). Bash 3.2 — NO arrays in wave scripts.

## What this PR claims (verify INDEPENDENTLY)

Fixes the two playtest fun-killers: **#118** (era-3 arrival was an ~17s unwinnable death clock — the surge unreachable) via an era-3 retune, and **#124** (one-way health drain, no recovery) via a new recovery mechanic. Acceptance per the brief: era-3 surge **survivable-by-good-play** (new golden), a real recovery path demonstrated, `odin test core` green, rlsw re-bless where behavior intentionally changed, tuning table before/after in the PR, and **#115 not regressed** (the lose state must stay reachable — tension preserved on both sides).

**THIS IS ALSO A MEGA-DIFF (~93,959 lines: 6e3a3c8-era base 61ea014..7b109d3 — the era-3 retune + recovery mechanic forced a golden-corpus re-bless).** gh pr diff is API-capped. Save the canonical diff LOCALLY: `git diff 61ea014..7b109d3` → round dir `diff.patch`. CHUNK: full 7-lens attention on the CODE chunk (the .odin economy/render sources + the new goldens' .dem scripts + tuning numbers); the PNG bulk gets MECHANICAL verification (re-bless census: one raster convention across the corpus — the 08-28 two-machine split is canon context; blob-vs-#106-warm-bytes where the beats pre-date this PR). Disclose the shape in the verdict.

## Your r1 mandates (verify INDEPENDENTLY)

- **#118**: read the era-3 tuning change (which knob moved: ramp/magnitude/telegraph?). Re-run the era3_surge_survivable .dem yourself — a PREPARED build must ride the arrival (watch for a degenerate giveaway: the demo must show correct play, not a neutered surge). Mutation leg: revert the retune → the demo/sim leg must go RED (era-3 kills prepared builds again).
- **#124**: the recovery mechanic — which knob landed (regen-on-healthy-delivery / repair action / Box-economy cost)? Verify it creates a REAL loop (demonstrated in a golden: health drops, recovers, drops again). Mutation leg: remove the recovery → its leg RED.
- **#115 guard**: with both fixes in, is the LOSE state still reachable? A sim/run showing loss still possible under sustained failure = PASS. If the game now cannot lose, that is a BLOCKER (overcorrected).
- **Tuning table honesty**: PR-body before/after numbers vs the actual code values.
- **Re-bless census**: one raster convention; changed-behavior beats re-blessed, unchanged beats byte-stable (spot-check vs the parent's goldens).
- Suites: core + app + harness + drift + fold-check + stats + econ (the standard sweep); sim/log bytes pristine except where the retune legitimately moves them (disclosed).

CI context: billing-block signature (0 steps) — note-only, NOT a gate; local gates are the merge ground truth. ALSO note: the PR was initially opened against `main` (wrong base, Silas retargeted to v2 — the branch descends cleanly from 61ea014 = origin/v2, no rebase happened; head 7b109d3 is the full fix).

Self-report: `/Users/moses/code/bin/ledger set pp-funfix-118-124-perkins-r1 working` at start; final message = verdict + review URL + findings counts. Round row already exists — work it, do not create one.

---

## Standing orders (paste verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never
  touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job
  briefing** and **GitHub issue** (your spec), and your cwd — a detached
  worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first:
  `gh pr diff <pr>` →
  `/Users/moses/code/_bmad-output/perkins/<job-id>/r<N>/diff.patch`.
  Every lens reviews these identical bytes. (Absolute path — the round
  worktree is destroyed at close-out, so artifacts live in the
  orchestrator's `_bmad-output`.) **[r1 note: gh pr diff is API-capped
  on this MEGA-DIFF. Save the canonical diff LOCALLY as `git diff
  61ea014..7b109d3`. Chunk: code chunk full lens; PNG bulk mechanical.
  Disclose the shape.]**
- Run the lenses per the `code-review` skill's **Headless / Automated
  Mode** with: `diff_file` = the canonical diff just saved, `worktree` =
  your cwd (the detached round worktree), `spec_files` = the original job
  briefing + the GitHub issue (here: use the briefing + issues 118/124 +
  the squad reports), `out_dir` =
  `/Users/moses/code/_bmad-output/perkins/<job-id>/r<N>`, and
  `prior_findings` = the previous round's `consolidated.json` when N > 1
  (re-review: fix audit first, carry-forward markers). The headless mode
  owns: pane mechanics (dedicated tab, `mm-<lens>-r<N>` labels), the
  `<lens>.json` output contract + existence check, one retry per failed
  lens, big-diff chunking, the mandatory verification pass, consolidation,
  and writing `consolidated.json`. Its verdict thresholds are yours
  below.
  **Lens-spawn rooting (user-approved 2026-08-18):** the headless spawn
  template pins `--cwd <worktree>` on every lens tab FOREVER — a lens
  pane whose cwd is not the round worktree is mis-rooted: close +
  relaunch with `--cwd`.
  **Empty-lens doctrine (2026-08-18/19):** acceptance/architecture
  lenses back 3-byte-EMPTY a THIRD straight generation → sweep those
  lens panes + regenerate (intervene — an empty-lens verdict never
  ships); a g-wave COMPENSATION verdict (a subset of lenses delivering a
  valid verdict) counts as valid.
  Visual checks (goldens, sprites): verify MECHANICALLY first
  (byte/hash/capture-diff); your model is natively multimodal — vision
  is INLINE for screening, but pixel measurements decide, never a bare
  visual impression. Never fake a measurement.
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
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner <owner>)` —
     capture STDOUT ONLY. NEVER append `2>&1`: the script writes cache
     warnings to stderr, which would corrupt the token and make a good
     mint look like a failure.
  2. Check for an EMPTY token, NOT `$?` (an intervening command can
     clobber `$?`, and a `2>&1` capture makes it lie — the 2026-08-09
     rc3-2 round posted a fallback-comment instead of a formal approve
     on exactly this):
     `if [ -z "$TOKEN" ]` -> the mint failed; fall back to `gh pr comment
     <pr> --body-file <body.md>`, note `fallback-comment` in your ledger
     note, and call it out in your final message.
  3. Otherwise (token non-empty): `GH_TOKEN=$TOKEN gh pr review <pr>
     --<event> --body-file <body.md>`
- Body format:
  ```
  ## 🤖 Perkins automated review — round <N>
  **Job:** <job-id> · **Reviewed sha:** <short> · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed against the code — <rejected> discarded as false-positive[, <u> kept as [unverified]]

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Address findings and push — I re-review automatically on the new sha.
  The loop runs until an APPROVED verdict._
  ```
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post
  anyway but note "reviewed `<old>`, head now `<new>` — a fresh round
  will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set <round-id> working` at
  start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely —
  fixing is the implementing minion's job, triggered by the review relay.
