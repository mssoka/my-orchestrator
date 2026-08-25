# Perkins round r1 — righttenantry-demo-bulk-invite-guard

**You are Perkins.** You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane (the implementing minion is at w1T:p34A, its worktree is `righttenantry-demo-bulk-invite-guard` — hands off).

## Context

- **PR:** https://github.com/solarity-services/RightTenantry/pull/636 (OPEN, head `599a6569bf1758f3c3ecf92d9397927b4e1c8b52`) — "fix(demo): bulk invite shows demo notice instead of simulated send"
- **Reviewed sha:** `599a6569` (detached — trust your cwd, not `origin/develop`)
- **Round id:** `righttenantry-demo-bulk-invite-guard-perkins-r1` (self-report `bin/ledger set righttenantry-demo-bulk-invite-guard-perkins-r1 working` at start)
- **Repo root:** /Users/moses/code/RightTenantry · **cwd = your worktree** (the detached round worktree at exactly the reviewed sha)

## Spec (the job)

Read `r1/job-briefing.md` (the original job briefing) IN FULL — it is your spec:
- User ruling verbatim: "it should just say this is demo, not sent."
- Demo bulk-invite must show a demo notice at the SEND path — zero sends, zero send-shaped validation errors; real mode byte-identical/untouched.
- Canonical demo detection, not a second detector. Rule 3: the real-mode validation-error path (toast lacks WHICH email failed though the API returns invalid_emails) was FLAGGED not fixed — verify it's flagged in the PR, don't hold the round on it.

## Round mechanics

1. **Canonical diff first:** `gh pr diff 636` → already saved at `/Users/moses/code/_bmad-output/perkins/righttenantry-demo-bulk-invite-guard/r1/diff.patch` (200 lines). Every lens reviews these identical bytes.
2. **Run the lenses** per the `code-review` skill's **Headless / Automated Mode**:
   - `diff_file` = `/Users/moses/code/_bmad-output/perkins/righttenantry-demo-bulk-invite-guard/r1/diff.patch`
   - `worktree` = your cwd (the detached round worktree)
   - `spec_files` = `/Users/moses/code/_bmad-output/perkins/righttenantry-demo-bulk-invite-guard/r1/job-briefing.md`
   - `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-demo-bulk-invite-guard/r1`
   - `prior_findings` = none (r1)
   - Headless mode owns pane mechanics (dedicated tab, `mm-<lens>-r1` labels), the `<lens>.json` output contract + existence check, one retry per failed lens, the mandatory verification pass, consolidation, and writing `consolidated.json`.
   - **Lens-spawn rooting:** every lens tab pins `--cwd <your worktree>` — a lens pane whose cwd is not the round worktree is mis-rooted: close + relaunch with `--cwd`.
   - **Empty-lens doctrine:** acceptance/architecture lenses back 3-byte-EMPTY a third straight generation → sweep those lens panes + regenerate; a subset-valid verdict counts as valid.
   - **Vision:** you are on k3 (sees images natively) — vision is INLINE, no caveat. This round is code+test (client demo flow) — visual judgment should be minimal; verify mechanically where possible.
3. **Verdict → review event:** 0 blockers → `--approve` · 1–3 → `--request-changes` · 4+ → `--request-changes` + "MAJOR REWORK" lead. Degraded guard: any lens failed AND zero findings → `--comment` + flag Gru, never approve.
4. **Post as the app:**
   ```
   TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)
   ```
   STDOUT only — NEVER `2>&1`. Check EMPTY token, not `$?`; empty → `gh pr comment <636> --body-file <body.md>` + note `fallback-comment`.
   Non-empty → `GH_TOKEN=$TOKEN gh pr review 636 --<event> --body-file <body.md>`.
5. **Body format:** per the playbook annex 'Perkins — the lens run' (🤖 header, Job/Reviewed sha/Reviewers/Verification, Blockers/Warnings/Notes sections, Reviewer agreement, **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED, loop-until-APPROVED footer).
6. **Before posting:** re-fetch `headRefOid`; if it moved, post anyway + note "reviewed `599a6569`, head now <new> — a fresh round will follow".
7. **Close-out hygiene:** you MUST close every lens pane before finishing. Final message = verdict + review URL + findings counts.
8. Skip `code-review` Step 5 (interactive fix flow) — fixing is the implementing minion's job, triggered by the review relay.

## Model

kimi-coding/k3 (probe-verified OK 13:13Z) — reasoning tier, vision inline. `--thinking max`.
