# Perkins briefing — round 3 (fix-audit, FINAL): righttenantry-refcheck-rc3-4

- **PR:** https://github.com/solarity-services/RightTenantry/pull/599 (targets `develop`)
- **Reviewed sha:** `9fddf2c6173ef4be73447ee9082a99dd8d75e54d` (short `9fddf2c`; commit "fix(refcheck): Perkins r2 B2 — wire the review-submit _focus_seconds (W1 was inert)"; r2 was `8c9c87e`, r1 was `13ae750`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 3 of 3 — **fix-audit, the FINAL automated round.** If this round does not approve, the human takes over (the 3-round cap).
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-4-r3` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc3-4.md` + the story spec + the architecture (AD-3/AD-6/AD-7/AD-9/AD-14) + UX (§6.5/§7.9/§8.6/§10.2). No GitHub issue.
- **prior_findings:** `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r2/consolidated.json` (r2 = CHANGES_REQUESTED: B2-r2 the only blocker, W4 partial, everything else fixed/holding). **Fix-audit FIRST** (B2-r2 + W4-partial disposition), then scan the delta for new issues.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What changed since r2 (the rework under review)

The impl minion fixed **B2-r2** (the r2 blocker — W1's inert fix) in `9fddf2c`:
- Added an **`initReviewSubmit` seam** to `reference_form.js`: finds `reference-review-form` + its `[data-focus-seconds]` field; on submit, populates `_focus_seconds` from the same page-clock logic (`clampFocusSeconds`) the per-question forms use; does **NOT** preventDefault (the review submit stays a native POST). Called from the top-level init alongside `initBrowser` (both DOMContentLoaded + immediate paths); exported as `_initReviewSubmit` for testing. The form-page gate stays intact (no per-question autosave on the review page — correct).
- **4 Node tests driving the browser path** (not `simulate.form_body`): (1) review submit populates `_focus_seconds` from the page clock (8s → "8"), (2) the native POST is not prevented, (3) the seam no-ops off the review page (form-page path untouched), (4) the value floors to whole seconds (5_999ms → "5").
- Suite: make test-js 136 (+4), make test 1418 unit, build + format clean. Everything else from r1/r2 stays resolved (B1 raw origin, W2 truncate, W3/W5/W6, N1/N2/N3/N5/N6); the r1 `_focus_seconds` integration test stays as the server-side persistence pin, the Node test as the browser-path pin.

## ⚠️ CRITICAL lens-guards (carried — verify, don't re-litigate)

- **B2-r2's fix must be REAL (the r2 lesson: the r1 'fix' was inert).** Verify by CODE TRACE, not claims: `initReviewSubmit` must actually bind to the review form's submit (the same page that renders `[data-focus-seconds]`), populate from the page clock, and NOT preventDefault. The 4 Node tests must drive the browser path (not a server-side `simulate.form_body` mask) — and the negative cases (off-page no-op, native POST preserved, floor-to-whole-seconds) must be real. **This is the load-bearing verification of this round.**
- **W4-partial (r2):** declined/objected notification rows unpinned — verify whether the minion addressed it in this push or it remains (if it remains as a documented low-risk gap, it's a note not a blocker — but check).
- **The load-bearing edge cases must still hold** (verified r1/r2 — confirm the delta didn't disturb them): objection stickiness (AD-6/14), evidence-log single-writer (channel 'web'), deterministic result (AD-9), one-submission (AD-3), registry prefix-match + router arms, B1's raw-origin fix on ALL notification paths, em-dash ban.
- **No new regressions** in the delta (the seam + tests only, ideally).
- **Suite claims** (test-js 136 / unit 1418 / build) — verify real, 0 failures.
- **JSONB test gotchas** from the field-notes (space-after-colon re-serialisation — use `result->>'field'`; Squirrel's own `sql.ReferenceCallStatus`; no `decode.null`).
- **Do NOT re-open r1/r2 findings that are verified fixed** — the fix-audit dispositions them; carry-forward markers only.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 599 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r3/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the job briefing + the story spec + the architecture (AD-3/AD-6/AD-7/AD-9/AD-14) + the UX (§6.5/§7.9/§8.6/§10.2), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r3`, `prior_findings` = r2's consolidated.json (fix-audit FIRST, carry-forward markers). Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r3` labels), `<lens>.json` output contract + existence check, one retry per failed lens, verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- **This is the FINAL automated round (3 of 3).** If the verdict is not READY TO MERGE, state plainly in the body that the human takes over after this round (per the cap), and flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`**.
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 599 --repo solarity-services/RightTenantry --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 599 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 3 of 3 (fix-audit, FINAL)` / **Job:** righttenantry-refcheck-rc3-4 / **Reviewed sha:** 9fddf2c (r2 was 8c9c87e, r1 was 13ae750) / **r2 audit:** B2-r2 <FIXED/NOT>, W4-partial <status> / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers / ### Warnings / ### Notes / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer + the human-takes-over-after-r3 note if not clean.
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc3-4-perkins-r3 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: zai-coding-cn/glm-5.2** — kimi quota down; glm-5.2 is the sanctioned fallback.
