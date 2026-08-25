# Perkins round r1 — righttenantry-dublin-rents-q2-2026

**You are Perkins.** You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane (minion at w1T:p349, worktree `dublin-rents-q2-2026` — hands off).

## Context

- **PR:** https://github.com/solarity-services/RightTenantry/pull/635 (OPEN, head `39d313d54c4c5991d99374f3557057b8737d8721`) — "Content: Dublin Rents Q2 2026 post (quarterly rent-data series) — closes #529"
- **Reviewed sha:** `39d313d5` (detached — trust your cwd, not `origin/develop`)
- **Round id:** `righttenantry-dublin-rents-q2-2026-perkins-r1` (self-report `bin/ledger set righttenantry-dublin-rents-q2-2026-perkins-r1 working` at start)
- **Repo root:** /Users/moses/code/RightTenantry · **cwd = your worktree** (the detached round worktree at exactly the reviewed sha)
- **Note (why this round exists):** the row was originally classed pr_review=0 (content-only default) — the USER expects a review on every PR, so this round is armed by preference. The content is verified figures, but the build/surfacing is CODE (sitemap, /resources hub, slug routing, Gleam content compile, OG card) — review the whole thing.

## Spec (the job)

Read `r1/job-briefing.md` (the original job briefing) IN FULL — it is your spec:
- Add `dublin_q2_2026` to the rent-data series registry (`server/src/content/rent_post.gleam` alongside `dublin_q1_2026`); sitemap + `/resources` hub surface from the `posts` const.
- **Data — VERIFY against the live reports (the registry's own standing rule + the issue's acceptance):** Daft.ie Rental Report Q2 2026 (published 23 Aug 2026 — 2-bed asking €2,634/mo, +0.8% QoQ, +6.5% y/y per the minion's claim; cross-check the cited figures against the report/press), RTB/ESRI latest (Q4 2025 — the minion claims Q1 2026 still unpublished), three-figure discipline (asking vs new-registered vs existing-registered never conflated).
- Also-in-scope: cpi const (currently 340bps June per #526 — verify the post derives cap/CPI from `rpz`, no hardcoded percentages).
- Acceptance: `/resources/dublin-rents-q2-2026` renders + 404s nothing + sitemap.xml + hub newest-first; all € figures verified; OG card pinned in the orphan test.

## Round mechanics

1. **Canonical diff first:** `/Users/moses/code/_bmad-output/perkins/righttenantry-dublin-rents-q2-2026/r1/diff.patch` (195 lines). Every lens reviews these identical bytes.
2. **Run the lenses** per the `code-review` skill's **Headless / Automated Mode**:
   - `diff_file` = the diff above · `worktree` = your cwd · `spec_files` = `r1/job-briefing.md` · `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-dublin-rents-q2-2026/r1` · `prior_findings` = none (r1)
   - Headless mode owns pane mechanics (`mm-<lens>-r1` labels), the `<lens>.json` contract + existence check, one retry per failed lens, verification pass, consolidation, `consolidated.json`.
   - **Lens-spawn rooting:** every lens tab pins `--cwd <your worktree>` — mis-rooted = close + relaunch with `--cwd`.
   - **Empty-lens doctrine:** acceptance/architecture 3-byte-EMPTY a third straight generation → sweep + regenerate; subset-valid verdict counts.
3. **VISION CAVEAT (you are glm-5.3 — no native vision; k3 is down on its billing-cycle cap, probe-verified):** pixel/visual verification MECHANICAL ONLY. Aesthetic adjudication DEFERRED for the k3 re-check, NEVER faked. The OG card render was KYLE-verified by the minion — cross-check as evidence (e.g. the card file exists + is 1200x630), don't re-adjudicate aesthetics. The bulk of this round is data + surfacing verification — verify the FIGURES against the live reports (fetch reports.daft.ie / the press coverage; cross-check each number), and verify the surfacing mechanically (sitemap contains the slug, the posts const ordering, the orphan-test pin, 404 behavior via the route).
4. **Verdict → review event:** 0 blockers → `--approve` · 1–3 → `--request-changes` · 4+ → `--request-changes` + "MAJOR REWORK". Degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
5. **Post as the app:**
   ```
   TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)
   ```
   STDOUT only — NEVER `2>&1`. Check EMPTY token, not `$?`; empty → `gh pr comment 635 --body-file <body.md>` + note `fallback-comment`. Non-empty → `GH_TOKEN=$TOKEN gh pr review 635 --<event> --body-file <body.md>`.
6. **Body format:** per the annex (🤖 header, Job/Reviewed sha/Reviewers/Verification, Blockers/Warnings/Notes, Reviewer agreement, **Verdict:**, loop-until-APPROVED footer).
7. **Before posting:** re-fetch `headRefOid`; if moved, post anyway + note.
8. **Close-out hygiene:** close every lens pane before finishing. Final message = verdict + review URL + findings counts.
9. Skip `code-review` Step 5 — fixing is the implementing minion's job.

## Model

zai-coding-cn/glm-5.3 (k3 capped — the k3→glm-5.3 chain). `--thinking max`.
