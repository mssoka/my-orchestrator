# Perkins round 1 — packet-plumber-v2-7.1-visual-juice

**PR:** https://github.com/solarity-services/Packet-Plumber/pull/64 (PR #64)
**Reviewed sha:** `dbed6a3a38385bde63eef0e34cbf7f997b519ed1`
**repo_root:** /Users/moses/code/packet-plumber (repo `packet-plumber`, base `v2`)
**Round:** 1 (fresh PR) · **CAP LIFTED (user ruling 2026-08-17): rounds run until APPROVED** · **Model:** `zai-coding-cn/glm-5.3` — **FALLBACK (kimi k3 cycle quota exhausted — probe 403 @ 18:49Z, re-confirmed; glm-5.3 probed OK 19:24Z). VISION CAVEAT: the job's native-vision ruling (k3) cannot be honored this cycle — verify PIXELS MECHANICALLY (byte/hash comparisons, capture-frame analysis, pixel-diff tooling), never by eyeballing screenshots.**
**STATUS: LIVE — r1 on the fresh sha.**
**prior_findings:** none (fresh PR).
**Spec files:**
- Original job briefing: /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-7.1-visual-juice.md
- CANON: `_bmad-output/planning-artifacts/art-renders/look-book-v1.md` (+ `renders/`, `art-direction-v1.md` + amendments) — the user-approved style gate
- Story card: `_bmad-output/planning-artifacts/sprints/stories-v2.md` §Story 7.1 (in-repo)

---

## Perkins standing orders

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
  orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated
  Mode** with: `diff_file` = the canonical diff just saved, `worktree` =
  your cwd (the detached round worktree), `spec_files` = the original job
  briefing + the GitHub issue (dump it with `gh issue view <n> --json
  title,body,comments` into the round dir first), `out_dir` =
  `/Users/moses/code/_bmad-output/perkins/<job-id>/r<N>`, and
  `prior_findings` = the previous round's `consolidated.json` when N > 1
  (re-review: fix audit first, carry-forward markers). The headless mode
  owns: pane mechanics (dedicated tab, `mm-<lens>-r<N>` labels), the
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
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` —
     capture STDOUT ONLY. NEVER append `2>&1`: the script writes cache
     warnings to stderr, which would corrupt the token and make a good
     mint look like a failure.
  2. Check for an EMPTY token, NOT `$?` (an intervening command can clobber
     `$?`, and a `2>&1` capture makes it lie — the 2026-08-09 rc3-2 round
     posted a fallback-comment instead of a formal approve on exactly this):
     `if [ -z "$TOKEN" ]` -> the mint failed; fall back to `gh pr comment <pr>
     --body-file <body.md>`, note `fallback-comment` in your ledger note,
     and call it out in your final message.
  3. Otherwise (token non-empty): `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file
     <body.md>`
- Body format:
  ```
  ## 🤖 Perkins automated review — round <N> (cap lifted — loop until approved)
  **Job:** <job-id> · **Reviewed sha:** <short> · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed against the code — <rejected> discarded as false-positive[, <u> kept as [unverified]]

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Address findings and push — I re-review automatically on the new sha._
  ```
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post
  anyway but note "reviewed `<old>`, head now `<new>` — a fresh round
  will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set <round-id> working` at
  start (round id: `packet-plumber-v2-7.1-visual-juice-perkins-r1`); final
  message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely —
  fixing is the implementing minion's job, triggered by the review relay.

---

## r1 guards (round-specific — fresh PR, loop until APPROVED)

**This is a VISION job — with the vision model unavailable this cycle.
Pixel claims are verified MECHANICALLY (byte/hash comparisons, capture
diff tooling, golden byte-identity), never by eyeball. Where a judgment
needs native vision (aesthetic verdicts), record it as an explicit
deferred item for the kimi-backed re-check — do NOT block on it and do
NOT fake it.**

**The ONE hard blocker class — canon application + view purity:**
- **Canon application, not redesign:** the look-book palette + glow
  treatment applied per `look-book-v1.md`; node health states 🟢🟡🔴
  readable per canon; leak-spray per canon. Where a canon render and the
  code disagree, canon wins — each adoption named in the PR body. The
  user-approved style-gate verdicts (TRUE TOP-DOWN buildings — roof
  carries the read; flat solid colors, no gradients/bevels/bloom) are
  canon: verify the implementation matches, mechanically where possible
  (color constants vs the look-book palette).
- **View purity `[ODN-1]`:** the View reads ONLY snapshots — polish never
  perturbs the sim; no new snapshot fields without a documented reason;
  replay byte-identical `[E10]`.
- **Chrome idiom:** gauges / forecast / alerts filter/focus +
  alerts-as-nav consistent with the 5.5 demolish popover's chrome
  (match, not a second language).
- **Never-color-alone:** packet type + node state readable without color
  (icon/shape/outline companions).
- **Camera-fit:** the viewport scales so wider/taller screens reveal more
  map.
- **Goldens + re-bless discipline:** the new T2 juiced-frame golden;
  existing goldens re-blessed ONLY where juice provably changes pixels —
  EACH re-bless listed in the PR with before/after (the 4.3 discipline).
  This branch's re-bless sits ON TOP of #62's deliberate 29-frame fold
  (the cross-lane contract) — verify no golden collision and that the
  re-bless cause chain is documented.
- **No scope creep:** no a11y MODES (7.3), no audio (7.2), no mechanics,
  no core/snapshot changes, no asset regeneration (the look-book is
  final — the sprite pipeline (Blender/headless CLI gen_sprites.py) must
  match the canon).

**Lane awareness:** #63 (5.10) also carries a slice-boundary re-bless —
verify this branch's rebase history is clean (it sits on v2 with #62 +
#63 merged; the conflict sensor + rebase relays handled the moves).

**What NOT to re-litigate:** the user-approved style-gate verdicts
(Phase A — lavish-approved); the 5.5 popover chrome (approved + merged);
#62's golden fold (approved); the 5.9/5.10 catalog work; the look-book
canon itself (final — apply, don't judge); the kimi vision ruling (the
fallback is operational, not a canon decision).

**Verdict severity:** cap lifted — if the contracts hold (canon
applied, view purity intact, chrome idiom matched, never-color-alone,
camera-fit, goldens disciplined, mechanical pixel verification clean),
APPROVE. Warnings ≠ blockers. If blockers remain, CHANGES_REQUESTED
precisely; the minion fixes and r2 follows.

**CI note:** GitHub Actions on #64 is org-billing-blocked + today's
GitHub incident — NOT a signal; the local suite is ground truth (the
minion reports 9/9).
