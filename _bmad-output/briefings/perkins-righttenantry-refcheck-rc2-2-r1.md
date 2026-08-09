# Perkins briefing — round 1: righttenantry-refcheck-rc2-2

- **PR:** https://github.com/solarity-services/RightTenantry/pull/590 (targets `develop`)
- **Reviewed sha:** `dc1e08fd25554c8093eac8e8ed2ff52fb5578db7` (head `refcheck-rc2-2`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc2-2-r1` — pinned at exactly the reviewed sha.
- **Spec:** the original job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc2-2.md` + the story spec at `_bmad-output/implementation-artifacts/spec-rc2-2-viewed-application-status-end-to-end.md`. No GitHub issue (the sprint tracker is the spec).
- **prior_findings:** none (round 1).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

Story RC2.2: `viewed` Application Status, end to end (Reference-Checking amendment A5 — moves the reference trigger from shortlist toward viewing). The implementing minion reports (17 files, +377/-25):
- **Migration:** `ALTER TYPE application_status ADD VALUE 'viewed' AFTER 'shortlisted'` (additive, idempotent; viewed at sortorder 3.5, between shortlisted + approved).
- **Shared:** `Viewed` variant + `encode_status`/`status_from_string`/`status_decoder` all carry `"viewed"`.
- **Server:** `parse_status` accepts `"viewed"`; the 400 message lists it; `apply_status_update` + audit unchanged (generic); Squirrel regen added `Viewed`.
- **Client:** stepper is now 5-stop (Submitted → Reviewing → Shortlisted → Viewed → Approved); the shared `status_pill` aligned to the brand-doc house set + gained `Viewed=navy`; detail pill, leaderboard sort rank, comparison CTAs handle viewed.
- **Tests:** shared 101, client 468, server unit 1222, integration 394 (+1 new viewed-PATCH). New: shared 7-variant round-trip, parse_status_viewed, viewed-PATCH integration, stepper direction/focus/clamp pins, viewed-pill-navy render.
- **Key decisions (documented in the PR's Decisions & rationale):** recoloured the drifted shared `status_pill` to match the brand doc + detail-page pill (Approved visually unchanged since score-strong==teal); DELIBERATELY excluded `viewed` from sweep-nudge/bulk-reject (a viewed applicant is engaged, not auto-rejectable); merged `viewed` into the Shortlisted "Contact" CTA.

## ⚠️ CRITICAL lens-guard (read before any lens — prevents false positives)

This is a standard additive-status PR following the established rc1-1/rc1-2/rc2-1 conventions; several decisions are deliberate + user/briefing-driven and must NOT be flagged as defects:

- **Do NOT flag "viewed should be in sweep-nudge/bulk-reject."** Its EXCLUSION is deliberate (a viewed applicant is engaged, not auto-rejectable) — documented in the PR.
- **Do NOT flag "viewed merged into the Shortlisted Contact CTA" as a bug.** Deliberate.
- **Do NOT flag the shared `status_pill` recolour as a regression.** It was DRIFTED vs the brand doc; this realigns it (Approved visually unchanged since score-strong==teal). The recolour is the fix, not the defect.
- **Do NOT flag the migration as risky.** It's additive (`ADD VALUE` AFTER 'shortlisted'), idempotent — the standard pattern. Existing status values must NOT change.

### Legitimate findings here would be
- The `viewed` codec does NOT round-trip cleanly (encode/decode mismatch across shared/server/client), or `parse_status` rejects a valid `"viewed"`.
- A REGRESSION to an existing status (Submitted/Reviewing/Shortlisted/Approved/Reject) — rank logic, pill, filter, or leaderboard breaking for a non-viewed status.
- The 400 message / error path is wrong, or `apply_status_update`/audit behaves incorrectly for viewed.
- The navy pill doesn't render, or the stepper rank/clamp logic is wrong (e.g., viewed reachable from Submitted without passing Shortlisted, or Approved→viewed allowed).
- A migration that's NOT idempotent (fails on re-run) or that reorders existing values.
- **Em-dashes in user-facing copy** (RT global ban, CI-guarded) — the pill labels, stepper, any copy.
- Broken Gleam/JS parse, a `make` target regression, or a test that doesn't actually pin the viewed behavior (tautology).

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge.
- Save the canonical diff first: `gh pr diff 590 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc2-2/r1/diff.patch`.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = this briefing + the job briefing + the story spec (no GitHub issue), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc2-2/r1`, `prior_findings` = none (round 1). Headless mode owns pane mechanics (dedicated tab, `mm-<lens>-r1`), `<lens>.json` + existence check, one retry per failed lens, big-diff chunking, verification pass, consolidation, `consolidated.json`. Close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`): `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)`; on failure fall back to `gh pr comment 590 --repo solarity-services/RightTentry --body-file <body.md>` + note `fallback-comment`; else `GH_TOKEN=$TOKEN gh pr review 590 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Body format:
  ```
  ## 🤖 Perkins automated review — round 1 of 3
  **Job:** righttenantry-refcheck-rc2-2 · **Reviewed sha:** dc1e08f · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed — <rejected> false-positive[, <u> unverified]

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Additive 'viewed' status (RC2.2); sweep-nudge/bulk-reject exclusion + Contact-CTA merge + pill recolour are deliberate decisions._
  ```
- Before posting, re-fetch `headRefOid`. If it moved, post anyway + note "reviewed `dc1e08f`, head now `<new>` — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc2-2-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5.
