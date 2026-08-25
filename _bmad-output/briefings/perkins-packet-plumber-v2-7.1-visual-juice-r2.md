# Perkins round 2 — packet-plumber-v2-7.1-visual-juice

**PR:** https://github.com/solarity-services/Packet-Plumber/pull/64 (PR #64)
**Reviewed sha:** `cb3bf2de25aaf7076652a41edccfdc7c116235c4`
**repo_root:** /Users/moses/code/packet-plumber (repo `packet-plumber`, base `v2`)
**Round:** 2 (fix-audit after r1 CHANGES_REQUESTED) · **CAP LIFTED (user ruling 2026-08-17): rounds run until APPROVED** · **Model:** `zai-coding-cn/glm-5.3` — **FALLBACK (kimi k3 cycle quota exhausted; probed OK 20:18Z). VISION CAVEAT (as r1): pixel claims verified MECHANICALLY (byte/pixel/hash comparisons) — never eyeballed; aesthetic verdicts deferred for the k3 re-check, never faked.**
**STATUS: LIVE — r2 fix-audit on the fresh sha.**
**prior_findings:** `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r1/consolidated.json` (r1: NEEDS CHANGES 2B/7W/9N, review 4954131568 @ dbed6a3)
**Spec files:**
- Original job briefing: /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-7.1-visual-juice.md
- CANON: `_bmad-output/planning-artifacts/art-renders/look-book-v1.md` (+ `renders/`, `art-direction-v1.md` + amendments)
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
  start (round id: `packet-plumber-v2-7.1-visual-juice-perkins-r2`); final
  message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely —
  fixing is the implementing minion's job, triggered by the review relay.

---

## r2 guards (round-specific — fix-audit, loop until APPROVED)

**Fix audit FIRST (r1 findings — verify each bites, mechanically where
pixel-adjacent), carry-forward markers second.**

**r1-B1 — sprite bbox y flip:** the minion claims `content_bbox` now emits
top-down y (+ sprites.json regenerated). Verify MECHANICALLY with the r1
probe method: the PIL alpha-bbox of the committed PNGs must now match the
sidecar values WITHOUT the flip formula; `sprite_blit` renders house BODIES
(alpha fill in the correct window — the r1 cross-check: as-drawn window
24–38% alpha was the broken signature, 77–96% correct); the juice golden
(`goldens/juice/30000ms.png`) must now CONTAIN house-body hex pixels.

**r1-B2 — cold-boot camera-fit:** the minion claims the boot order now
computes the view before `start_run` (or re-fits once world dims are
valid). Verify: a cold-start capture (fresh boot, no selection change)
renders the map centered — not displaced half a screen; resize still
heals; selecting/deselecting no longer needed.

**r1 W-fold spot-checks (claimed folded):**
- W1 ×2.2 tier-band formula — ONE shared helper (view.odin + crisis.odin
  call it).
- W2 NEW palette-presence scan GATE — ci-local now 10/10 (the new gate
  runs the §2-palette oracle over the juiced frames). Verify the gate is
  real and pins the sprite/palette output (this is the "objective oracle"
  r1 asked for — it should catch a B1-class crop).
- W3 alerts-as-nav zoom exit — ESC/pad-B homes the camera with nothing
  selected.
- W4 doorstep fan — 5×5 = 25 slots (no 15-wrap).
- W5 SLA focused-row chip — single-source `sla_row_rect` + the 5.5
  translucent fill + hairline idiom; hit rect matches the drawn chip.
- W6 popover-first order — banner/SLA hit-tests AFTER `popover_click`.

**r1 notes folded (claimed):** sprites_load unloads partials on failure +
value-range checks; the harness refuses to capture without the sheet (no
silent primitive bless); app logs the fallback.

**The 76-golden re-bless (the B1 consequence):** ALL 76 goldens changed
again — the cause chain must be documented (bbox flip + regenerated
sprites.json + the juiced frames). Verify: T1/replay byte-identical
(only PNGs + the juice manifest changed — the minion claims this);
existing .t1/.log.bin untouched; per-demo re-bless counts match the
claim.

**Lane awareness:** this branch sits on v2 with #62 + #63 merged — the
rebases were handled via relays; verify the history is clean and no
sibling golden collision.

**What NOT to re-litigate:** the user-approved style-gate verdicts (the
roof-only depth read is the approved design — the minion's honest note
confirms the two-tone roof + contact shadow IS the gate design, not a
defect); r1's held-clean ground (canon application, ODN-1 view purity,
chrome idiom, never-color-alone, golden discipline — all verified
mechanically in r1); the fallback-model caveat (operational, not canon).

**Verdict severity:** cap lifted — if B1/B2 are verified fixed (mechanical
proof), the folds land, and the re-bless chain is sound, APPROVE.
Warnings ≠ blockers. If blockers remain, CHANGES_REQUESTED precisely; the
minion fixes and r3 follows.

**CI note:** GitHub Actions on #64 is org-billing-blocked + today's
GitHub incident — NOT a signal; the local suite is ground truth (the
minion reports 10/10 with the new gate, 32/32 demos).
