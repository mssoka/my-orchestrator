# Perkins round 2 — packet-plumber-v2-7.2-audio-juice

**PR:** https://github.com/solarity-services/Packet-Plumber/pull/60 (PR #60)
**Reviewed sha:** `1b96bea688e44db021eca8a98b9fc9cded27daff`
**repo_root:** /Users/moses/code/packet-plumber (repo `packet-plumber`, base `v2`)
**Round:** 2 (fix-audit after r1 CHANGES_REQUESTED) · **CAP LIFTED (user ruling 2026-08-17): rounds run until APPROVED** · **Model:** kimi-coding/k3
**STATUS: LIVE — r2 fix-audit on the fresh sha.**
**prior_findings:** `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.2-audio-juice/r1/consolidated.json` (r1: NEEDS CHANGES 1B/6W/7N, review 4950182382 @ 84b46cc)
**Spec files:**
- Original job briefing: /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-7.2-audio-juice.md
- r1 artifacts: `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.2-audio-juice/r1/`
- Story card: `_bmad-output/planning-artifacts/sprints/stories-v2.md` §Story 7.2 (in-repo)

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
  start (round id: `packet-plumber-v2-7.2-audio-juice-perkins-r2`); final
  message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely —
  fixing is the implementing minion's job, triggered by the review relay.

---

## r2 guards (round-specific — fix-audit, loop until APPROVED)

**Fix audit FIRST (r1 findings — verify each bites, mutation-test where
practical), carry-forward markers second.**

**r1-B1 — M-key mute chain dead:** the r1 blocker (6-lens) was that
`Key_Press{.M}` was never translated to `Intent(Toggle_Mute)` — the mute
path was dead end-to-end. The minion claims `app/input/mouse.odin`
phase-1 now collects `.M` and emits `Toggle_Mute` (Perkins' prescribed
shape: collect like `.T`, `case .M: append(out, Intent(Toggle_Mute{}))`).
Confirm the chain is ALIVE: poll → mouse.odin phase-1 → intent → exec
`on_mute` → `effect_mute` → the audio module's mute flag; M press actually
mutes (and captions stay live while muted).

**r1 W-fold spot-checks (claimed folded):**
- W1 caption crisis-priority (arrival set_caption skipped while a crisis
  caption is in dwell — or a small queue).
- W2 terms trail: the README now carries the supplier story (SFX =
  ElevenLabs; music = Suno Premier) matching the PR body — verify the
  README/body contradiction is actually resolved (the r1 review predated
  the doc trail).
- W3 per-kind draw minimums (crisis ≥ 1, arrival ≥ 1) asserted for the
  audio demo; W4 arrival-throttle assertion (new audio_throttle.dem —
  dense tick, suppressed ≥ 1); W5/W6 the 7 new unit tests
  (odin test app/audio: draws/throttle/caption priority-expiry-reset,
  wav_pack/synth forms, variant bounds) + failed-asset UnloadSound
  hygiene.

**r1 notes folded (claimed):** `pending.*_plays` → u16; dead
`SYNTH_RAMP_S` removed; demo header comment corrected (director demand);
flush cycles variants; Game_Over frozen-caption documented harmless.

**Rebase-aware review:** 1b96bea sits on v2 @ 388e316 (the #59 merge —
5.5's pad-X controller leg + popover refactor landed in v2). The minion
claims zero-conflict rebase (disjoint hunks). Verify: the PR diff =
r1-fix + folds ONLY, cleanly rebased; #59's intent-layer additions are
present and untouched; no #59 features regressed by the rebase.

**What NOT to re-litigate:** r1's PROVEN-clean ground (ODN-15 determinism
neutrality — probe-proven non-vacuous: draws 228/crisis 1/arrival 227,
replay gate real, consumer structurally pure; asset contract sound;
existing suite unshifted); the #59 demolish surface (already approved +
merged); the 5.4 intent-layer architecture; the asset-contract source
rulings (SFX=ElevenLabs, music=Suno Premier — user-owned). r1's discarded
FPs stay discarded.

**Verdict severity:** cap lifted — if the delta is clean (B1 chain alive
+ pins bite + folds verified + no new deltas), APPROVE. Warnings ≠
blockers. If blockers remain, CHANGES_REQUESTED precisely; the minion
fixes and r3 follows.

**CI note:** GitHub Actions on #60 is org-billing-blocked (runners never
start) — NOT a signal; the local suite is ground truth (the minion
reports 9/9 native + 9/9 container on the final head).
