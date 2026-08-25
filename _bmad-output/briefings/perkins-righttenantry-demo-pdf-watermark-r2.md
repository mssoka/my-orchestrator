# Perkins round r2 — righttenantry-demo-pdf-watermark (FIX-AUDIT)

**You are Perkins.** You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane (minion at w1T:p34S, worktree `righttenantry-demo-pdf-watermark` — hands off).

## Context

- **PR:** https://github.com/solarity-services/RightTenantry/pull/637 (OPEN, head `e9537cd2ed6783d40f517e2f37091fef9aacf7fd`) — "feat(demo): watermark every demo PDF with diagonal DEMO" + r1-fix commit
- **Reviewed sha:** `e9537cd` (detached — trust your cwd, not `origin/develop`)
- **Round id:** `righttenantry-demo-pdf-watermark-perkins-r2` (self-report `bin/ledger set righttenantry-demo-pdf-watermark-perkins-r2 working` at start)
- **Repo root:** /Users/moses/code/RightTenantry · **cwd = your worktree** (the detached round worktree at exactly the reviewed sha)
- **This is r2 — a FIX-AUDIT round.** `prior_findings` = `r2/prior_findings.json` (r1's consolidated). Fix-audit first: verify EVERY r1 finding against the new code, then hunt DELTA-introduced issues on e9537cd (the r1-fix commit). DELTA blockers are the norm, not a failure.

## r1 findings to verify (from prior_findings.json — read it fully)

- **B1 (r1): handler watermark:False flag UNASSERTED** — claimed fix: pin the handler's real-mode PDF body (watermark:False propagates / served bytes == real-mode golden). Verify the pin BITES (flip watermark:True → test fails).
- **B2 (r1): advisory test gate FAIL** — aggregate of B1 + unpinned served demo bytes. Verify the gate now passes with real pins.
- **W1 (r1): cover renders TWO stacked watermark layers (~44% vs 25%)** — claimed fix: dropped the cover double layer ("drop cover double layer" in the commit). Verify mechanically (cover-only render variant + pixel/byte diff — ONE layer, ~25%).
- **W2 (r1): no test reads committed priv/static/demo/*.pdf** — claimed fix: pinned committed bytes == fresh re-bake. Verify the pin bites (corrupt a committed PDF → test fails).
- r1 notes (7): carry-forward check — each either fixed or explicitly carried as a note.

## Round mechanics

1. **Canonical diff first:** `/Users/moses/code/_bmad-output/perkins/righttenantry-demo-pdf-watermark/r2/diff.patch` (740 lines — r1-fix delta + the cumulative PR). Every lens reviews these identical bytes.
2. **Run the lenses** per the `code-review` skill's **Headless / Automated Mode**:
   - `diff_file` = the diff above · `worktree` = your cwd · `spec_files` = `r2/job-briefing.md` · `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-demo-pdf-watermark/r2` · `prior_findings` = `r2/prior_findings.json` (r1)
   - Headless mode owns pane mechanics (`mm-<lens>-r2` labels), the `<lens>.json` contract + existence check, one retry per failed lens, verification pass, consolidation, `consolidated.json`.
   - **Lens-spawn rooting:** every lens tab pins `--cwd <your worktree>` — mis-rooted = close + relaunch with `--cwd`.
   - **Empty-lens doctrine:** acceptance/architecture 3-byte-EMPTY a third straight generation → sweep + regenerate; subset-valid verdict counts.
3. **VISION CAVEAT (you are glm-5.3 — no native vision; k3 is down on its billing-cycle cap, probe-verified):** pixel/visual verification MECHANICAL ONLY (byte/hash/capture-diff, cover-layer via cover-only variant renders). Aesthetic adjudication DEFERRED for the k3 re-check, NEVER faked. The job's KYLE evidence rides the PR body — cross-check as evidence, don't re-adjudicate aesthetics.
4. **Verdict → review event:** 0 blockers → `--approve` · 1–3 → `--request-changes` · 4+ → `--request-changes` + "MAJOR REWORK". Degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
5. **Post as the app:**
   ```
   TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)
   ```
   STDOUT only — NEVER `2>&1`. Check EMPTY token, not `$?`; empty → `gh pr comment 637 --body-file <body.md>` + note `fallback-comment`. Non-empty → `GH_TOKEN=$TOKEN gh pr review 637 --<event> --body-file <body.md>`.
6. **Body format:** per the annex (🤖 header, Job/Reviewed sha/Reviewers/Verification, Blockers/Warnings/Notes, Reviewer agreement, **Verdict:**, loop-until-APPROVED footer).
7. **Before posting:** re-fetch `headRefOid`; if moved, post anyway + note.
8. **Close-out hygiene:** close every lens pane before finishing. Final message = verdict + review URL + findings counts.
9. Skip `code-review` Step 5 — fixing is the implementing minion's job.

## Model

zai-coding-cn/glm-5.3 (probe OK 14:33Z; k3 capped — the k3→glm-5.3 chain). `--thinking max`.
