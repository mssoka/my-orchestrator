# Perkins briefing — round 1: righttenantry-refcheck-followup-607

- **PR:** https://github.com/solarity-services/RightTenantry/pull/610 (targets `develop`)
- **Reviewed sha:** `955284755d1c64e8884d557a2999fadc2a287db2` (short `9552847`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-followup-607-r1` — detached at exactly the reviewed sha. Trust it, not `origin/develop`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-followup-607.md` + GitHub issue #607 (the canonical spec — dump it with `gh issue view 607 --json title,body,comments` into the round dir) + the architecture canon (`AR-RC13`). GitHub issue: **607**.
- **Model:** `deepseek/deepseek-v4-pro` (Perkins reasoning tier). Launch EVERY lens pane with `pi --model deepseek/deepseek-v4-pro`. NEVER glm-5.2 (retired).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**The five #607 carried advisories** (each non-blocking at its source verdict; hardening):
1. **Escaped-form markers** — the §4.2 payload-strip marker set extended to cover `form_token` + `payload_ref` (every payload field covered; the strip holds AND the markers now catch what they missed).
2. **Unknown-outcome fallback** — a NAMED contract rule: unrecognised outcome → `null` on the wire, NEVER `OutcomeUnreachable`; shared `outcome_from_string_optional` + shared & server encode pins.
3. **Format-mix sort** — the RC4.4 timeline normalize covers both datetime sides; the one missing fixture (space-form alongside T-form) added + pinned.
4. **Em-dash pin** — `scripts/lint_em_dash.py` + CI step FAILS on em-dash; two real shipping em-dashes removed (batch line + nudge-skipped join) into dash-free fn-built labels in copy.gleam, scanned by the ban test.
5. **AR-RC13 systemic guard** — `shared is_terminal_status` = single terminality truth (server hooks + client fixture consume it; the drifting test-side list deleted); truth-table + lockstep pins; `scripts/lint_refcheck_hooks.py` + CI step; proof walk: restoring the RC4.2-r1 status list fails the Completed-terminal test, restoring the RC4.3-r1 menu shape fails the lint; AR-RC13 lesson entry + AD-11 cross-ref in the architecture doc.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 ITEM 5 LOAD-BEARING — the AR-RC13 guard is the point of this PR.** The systemic guard must make server hooks the single source of terminality truth. Verify: (a) `is_terminal_status` is genuinely SHARED (server hooks + client both consume it — no client-side re-derivation list remains anywhere); (b) the truth-table + lockstep pins exist and bite; (c) the lints run in CI and FAIL on the historical shapes (the proof walk — spot-check the lint actually detects the RC4.2-r1-style list and the RC4.3-r1-style menu re-derivation; a lint that can't fail is decorative); (d) the test-side drifting list is really deleted, not duplicated. A client-side terminality re-derivation surviving anywhere = a blocker (the RC4.2-r1/RC4.3-r1 blocker class).
- **🚨 ITEM 1 — the strip still holds.** The marker extension is defense-in-depth ON TOP of the §4.2 strip: verify the strip itself is unchanged in behavior AND the markers now cover form_token + payload_ref (a test proves both). A weakened strip or a still-uncovered payload field = a real defect.
- **🚨 ITEM 2 — the fallback contract is NAMED and pinned.** Unrecognised outcome → null on the wire, never OutcomeUnreachable; the encode pins cover shared + server. An implicit/undocumented fallback or an OutcomeUnreachable on unknown = a real defect.
- **ITEM 3 — the pin bites.** The mixed-format fixture (space-form alongside T-form) sorts correctly and is pinned; the RC4.4 normalize is the mechanism (verify both sides normalise before compare).
- **ITEM 4 — the lint FAILS on em-dash.** `scripts/lint_em_dash.py` fails on an em-dash in the scanned surface; wired into CI (the workflow diff); negative controls exist. RT em-dash ban applies to implementer-authored user-facing strings — the two removed em-dashes are gone from the shipped copy.
- **Scope guard:** the five #607 items ONLY — flag anything beyond (no design changes, no unrelated refactors).
- **base = `develop`** (RC4.1–4.4 merged — carry-forward only; do NOT re-open RC4-series findings; item 3's RC4.4 origin is expected, not a defect).
- **a11y + AC testids** untouched by this PR (verify no regression).
- **bmad-quirk heads-up (context, not a finding):** review the PR content as-is at the sha.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-followup-607/r1/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = the original job briefing + the GitHub issue (dump it with `gh issue view 607 --json title,body,comments` into the round dir first), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-followup-607/r1`, and `prior_findings` = the previous round's `consolidated.json` when N > 1 (re-review: fix audit first, carry-forward markers). The headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r<N>` labels), the `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and writing `consolidated.json`. Its verdict thresholds are yours below. You MUST close every lens pane before finishing.
- **Verdict → review event:**
  - 0 blockers → `--approve`
  - 1–3 blockers → `--request-changes`
  - 4+ blockers → `--request-changes`, body leads with "MAJOR REWORK"
  - **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru ("incomplete review").
- Post as the app (owner parsed from the PR URL). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — capture STDOUT ONLY. NEVER append `2>&1`.
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` -> the mint failed; fall back to `gh pr comment <pr> --body-file <body.md>`, note `fallback-comment` in your ledger note, and call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`
- Body format:
  ```
  ## 🤖 Perkins automated review — round <N> of 3
  **Job:** <job-id> · **Reviewed sha:** <short> · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed against the code — <rejected> discarded as false-positive[, <u> kept as [unverified]]

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Address findings and push — I re-review automatically on the new sha.
  After round 3, the human takes over._
  ```
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-followup-607-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
