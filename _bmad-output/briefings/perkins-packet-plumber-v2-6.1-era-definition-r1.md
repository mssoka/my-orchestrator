# Perkins round 1 — packet-plumber-v2-6.1-era-definition

**PR:** https://github.com/solarity-services/Packet-Plumber/pull/69 (PR #69)
**Reviewed sha:** `39d2a14807920276749283c83991ce8f789cdf9c`
**repo_root:** /Users/moses/code/packet-plumber (repo `packet-plumber`, base `v2`)
**Round:** 1 (fresh PR) · **CAP LIFTED (user ruling 2026-08-17): rounds run until APPROVED** · **Model:** `kimi-coding/k3` (HOLD LIFTED 08-18; probed OK 01:20Z) — **FALLBACKS in order: zai-coding-cn/glm-5.3 (down till ~06:48Z 1308 cap) → deepseek/deepseek-v4-pro → deepseek/deepseek-v4-flash.**
**STATUS: LIVE — r1 on the fresh sha.**
**prior_findings:** none (fresh PR).
**Spec files:**
- Original job briefing: /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-6.1-era-definition.md
- Story card: `_bmad-output/planning-artifacts/sprints/stories-v2.md` §Story 6.1 (in-repo)
- PR body: `_bmad-output/pr-bodies/6.1.md`
- Architecture (the [LATER] seam): `_bmad-output/implementation-artifacts/` arch §6.6 (the era_step seam)
- 5.11/5.12 context (the rosters/estates this builds on): r4/r1 briefings under _bmad-output/briefings/

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
  `prior_findings` = the previous round's `consolidated.json` when N > 1.
  The headless mode owns: pane mechanics (dedicated tab,
  `mm-<lens>-r<N>` labels), the `<lens>.json` output contract + existence
  check, one retry per failed lens, big-diff chunking, the mandatory
  verification pass, consolidation, and writing `consolidated.json`. Its
  verdict thresholds are yours below. You MUST close every lens pane
  before finishing.
- **LENS ROOTING (MANDATORY — the 08-18 mis-rooted class):** every lens
  tab MUST be created with `herdr tab create --cwd <this round worktree>`
  — the lens panes root at the round worktree, NEVER at the orchestrator
  root or the repo main checkout. A lens pane whose cwd is not the round
  worktree is mis-rooted: close + relaunch it.
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
     capture STDOUT ONLY. NEVER append `2>&1` (stderr cache warnings would
     corrupt the token).
  2. Check for an EMPTY token, NOT `$?`:
     `if [ -z "$TOKEN" ]` -> the mint failed; fall back to `gh pr comment <pr>
     --body-file <body.md>`, note `fallback-comment` in your ledger note,
     and call it out in your final message.
  3. Otherwise (token non-empty): `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file
     <body.md>`
- Body format:
  ```
  ## 🤖 Perkins automated review — round <N> (cap lifted — loop until approved)
  **Job:** <job-id> · **Reviewed sha:** <short> · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed against the code — <rejected> discarded as false-positive

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Address findings and push — I re-review automatically on the new sha._
  ```
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post
  anyway but note "reviewed `<old>`, head now `<new>` — a fresh round
  will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set <round-id> working` at
  start (round id: `packet-plumber-v2-6.1-era-definition-perkins-r1`); final
  message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely —
  fixing is the implementing minion's job, triggered by the review relay.

---

## r1 guards (round-specific — fresh PR, the era-FSM canon)

**The ONE hard blocker class — the era FSM honors the determinism spine
AND the data contracts:**

- **The FSM advance is replay-deterministic by construction:** Cmd_Era_Advance
  is a LOGGED action-log command (E10 — replay identity for fired AND
  deferred advances must hold); era_step lives at the reserved [LATER]
  seam (arch §6.6); the E14 no-mid-crisis deferral (an active crisis
  holds the advance until it clears) must be deterministic — verify the
  deferral test uses a REAL engine crisis (not a stub) and replay
  identity is asserted for both the fired and the deferred path.
- **eras.json honors the data-driven contract [ODN-5]:** integer-only +
  fail-fast at load; the TWO load-time invariants (the
  roster/unlock tables must exactly equal the era_introduced-derived
  sets; every demand entry class must be in its era's roster) — verify
  the invariants are real (a violating row FAILS load, mutation-checked)
  and non-circular (they can't silently pass with a wrong table).
- **LOG_VERSION 4→5 is honest:** the log header now carries the run-setup
  era; the golden era_advance.dem (era 2→3 flip, streaming spawns) is the
  T1 of the era-advanced state, replay-verified. Verify the version bump
  is confined to the header (byte-compare old-format logs) and the golden
  is byte-stable.
- **The deliberate re-bless (the eras.json catalog fold) is
  cause-partitioned:** fold-check PASS (boot's tick-1 shift is the catalog
  fold alone), T2 pixels byte-identical, log re-bless header-only (version
  byte + catalog_hash — byte-verified). Verify the partition mechanically
  (PNG diff + log byte-compare vs v2).
- **The 6.2 gate surface is present, not built:** era_advance_blocked +
  the unlock queries exist as the seam for 6.2 — verify they're read-only
  surface (no advance logic smuggled in). Follow-ups named in the PR
  (6.2 advance conditions, 6.3 legacy decay, eras 1/2 re-tune + eras
  4-6 content, the app-side trigger) must NOT be in this diff — scope
  creep = blocker-class.
- **The 6 new FSM tests + 20 catalog fail-fast rows are non-vacuous:**
  mutation-check the E14 deferral and at least one invariant.

**What NOT to re-litigate:** the 5.11 roster + era gates + W9 honest pin
(4-round approved); the 5.12 estates ruling + group uplink aggregation
(1-round approved); the #65 sprite canon (lavish-APPROVED); the
5.9/5.10 accumulator contracts; the fold-check harness (N11 of 5.11 —
done); the fallback-model caveat.

**Verdict severity:** cap lifted — if the FSM is replay-deterministic
(both paths), the invariants bite, the version bump + re-bless are
partition-exact, and the scope guard held, APPROVE. Warnings ≠ blockers.

**CI note:** GitHub Actions on Packet-Plumber is org-billing-blocked
(runners never start — the retired-caveat class) — NOT a signal; the
local suite is ground truth (minion reports 10/10 gates, 205 core
tests).
