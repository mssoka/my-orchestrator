# Perkins briefing — round 1: righttenantry-refcheck-rc4-4

- **PR:** https://github.com/solarity-services/RightTenantry/pull/609 (targets `develop`)
- **Reviewed sha:** `1a3839ce73a8d619d873855f27f3ff74689a5ec3` (short `1a3839c`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-4-r1` — detached at exactly the reviewed sha. Trust it, not `origin/develop`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc4-4.md` + Story RC4.4 in `_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md` (~line 692) + the UX spec §7.6 (attempt log) / §7.9 (notification copy) / OQ-5 (verbatim toast) + the architecture (`AR-RC13` one-stable-contract). GitHub issue: none (parent story in the epic doc).
- **Model:** `deepseek/deepseek-v4-pro` (Perkins reasoning tier). Launch EVERY lens pane with `pi --model deepseek/deepseek-v4-pro` — bare `pi` falls to the pi default provider. NEVER glm-5.2 (retired).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**Epic RC4 Story 4 — attempt-log timeline, export & notification completeness:** the
deferred RC2.1 codec lands (reference_* NotificationType variants + codec arms — the
minion shipped FIVE variants incl. reference_awaiting_correction, where the briefing
said four; completeness demanded five, decision documented in the PR); §7.6 attempt-log
timeline as a server-built payload key (typed, server-ordered, RFC3339-normalized, cadence
restart after corrections); Export (plain-text clipboard + verbatim OQ-5 toast); notification
completeness (§7.9 bodies verbatim as pure builders + preference-matrix + no-duplicate-
terminals pins); expand-only migration (substituted_at + terminalized_at).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 AR-RC13 LOAD-BEARING — server-built timeline, NO client re-derivation.** The
  attempt-log timeline is a server-typed payload; the client renders it. A client-side
  re-derivation/re-sort of event state (the RC4.2-r1 / RC4.3-r1 blocker pattern) = a
  blocker. The RFC3339 normalization + server-side ordering is the fix for the latent
  same-day mis-order — verify it actually normalizes PG `::text` → RFC3339 before sorting.
- **🚨 CODEC COMPLETENESS — every emitted reference_* notification decodes.** Five
  variants shipped (send/opened/correction/takeover/substitution/awaiting_correction/
  terminal — count them against what the server emits). An emitted variant without a
  decode arm = the bell-breaks-for-every-landlord blocker class. Verify the client
  notification-list decode + dropdown icon match are exhaustive.
- **🚨 EXPAND-ONLY MIGRATION.** One additive migration (substituted_at + terminalized_at
  stamped by the five terminal writers + substitute path). A breaking migration, a dropped
  back-compat decode (old server payload WITHOUT the new keys must still decode — the
  RC4.2/RC4.3 back-compat test family), or a terminal event without its stamp = a blocker.
- **🚨 NOTIFICATION COMPLETENESS — §7.9 copy verbatim + the pins.** The five §7.9 bodies
  as pure builders pinned; preference-matrix proven (realtime/daily/off per landlord
  notification_preference — unit + integration); no-duplicate-terminals proven (exactly
  one reference_unreachable across the full walk, none at T+144 — the late-completion-
  after-handoff variant reuses reference_completed). A missing pin or a duplicated
  terminal notification = a blocker.
- **VERBATIM TOAST (OQ-5).** "Attempt log copied — paste it into your records or a
  message." — spec copy verbatim; the em-dash scan exemption for this string is BY
  CONSTRUCTION (it contains no em-dash) — do not flag the string itself; verify the
  toast fires with the exact copy.
- **RT em-dash ban APPLIES** to all other implementer-authored user-facing strings
  (check the new timeline copy + export text + any new UI strings by hand AND the
  composition sites for ` — ` joins).
- **Timeline correctness:** every send, form-opened, correction, takeover, substitution,
  and terminal event appears; the cadence restarts after corrections (the warm-handoff
  window re-arms). A missing event class or a broken cadence restart = a real defect.
- **Export completeness:** reference + timeline + outcome + signals all present in the
  plain text; clipboard copy works for any started row.
- **base = `develop`** (RC4.1 + RC4.2 + RC4.3 merged — carry-forward only; the RC4.3
  r1-r5 saga findings are settled — do NOT re-open the TOCTOU/correct/substitute
  mechanisms; verify only that THIS story's dispatch wiring doesn't break them).
- **a11y + AC testids** on the new timeline/export UI; keyboard operable.
- **bmad-quirk heads-up (context, not a finding):** the create-story/dev-story tooling
  historically mis-resolved edits to the main checkout; Silas syncs it. Review the PR
  content as-is at the sha.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-4/r1/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = the original job briefing + the GitHub issue (dump it with `gh issue view <n> --json title,body,comments` into the round dir first), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-4/r1`, and `prior_findings` = the previous round's `consolidated.json` when N > 1 (re-review: fix audit first, carry-forward markers). The headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r<N>` labels), the `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and writing `consolidated.json`. Its verdict thresholds are yours below. You MUST close every lens pane before finishing.
- **Verdict → review event:**
  - 0 blockers → `--approve`
  - 1–3 blockers → `--request-changes`
  - 4+ blockers → `--request-changes`, body leads with "MAJOR REWORK"
  - **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru ("incomplete review").
- Post as the app (owner parsed from the PR URL). Mint first, then review — never run gh with an empty GH_TOKEN (a failed command substitution would fall through to the ambient `mssoka` credential and 422 on our own PRs):
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — capture STDOUT ONLY. NEVER append `2>&1`: the script writes cache warnings to stderr, which would corrupt the token and make a good mint look like a failure.
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` -> the mint failed; fall back to `gh pr comment <pr> --body-file <body.md>`, note `fallback-comment` in your ledger note, and call it out in your final message.
  3. Otherwise (token non-empty): `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`
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
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc4-4-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
