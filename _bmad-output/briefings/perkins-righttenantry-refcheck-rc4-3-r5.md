# Perkins briefing — round 5: righttenantry-refcheck-rc4-3 (USER-APPROVED CAP OVERRIDE, r5)

- **PR:** https://github.com/solarity-services/RightTenantry/pull/606 (targets `develop`)
- **Reviewed sha:** `ccc0ff68bee390dd94e024b4efb7482503127479` (short `ccc0ff6`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 5 (cap overridden by the user — "We need Perkins to be happy", Gru ruling 2026-08-13)
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-3-r5` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc4-3.md` + Story RC4.3 in `_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md` + the UX spec (§7.4/§7.7/§8.2/§8.3 copy) + the architecture (`A7` take-over, `AD-7`/`A1` correct, `AD-16` substitute audit, `§8.6` cadence, `AR-RC13` one-stable-contract). GitHub issue: none (parent story in the epic doc).
- **prior_findings:** r4 `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r4/consolidated.json` (VERIFY-DON'T-REOPEN round).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## Round-5 mandate: verify the r4-rework claims at ccc0ff6 (fix-audit)

The r4 round (4925103981, @ df0ea22) came back CHANGES_REQUESTED: B1 TOCTOU not
closed + W1/W2 + N1-N19. The minion's rework (ccc0ff6) claims ALL of it closed.
**Verify each claim against the code — the rework summary is leads, NOT proof.**

(a) **B1 (THE r4 blocker) — verify the wiring is REAL:**
- `mark_awaiting_correction_wrong_person` is WIRED into `apply_wrong_person`
  (form_handler.gleam) and the unguarded `update_reference_call_status` call is
  GONE (no residual caller on the wrong-person path).
- The guarded SQL carries BOTH backstops: `taken_over_at IS NULL` AND
  `correction_cycles = 0`.
- The new race pin `wrong_person_taken_over_race_stands_down_test` drives the
  wrong-person **POST route** on a taken-over row (303, status untouched, no
  audit) AND pins the SQL mechanism directly — neutralizing either guard turns
  it red. A vacuous or route-bypassing pin = a blocker.
- B1 closed ONLY if all three hold. The r2/r3/r4 dead-end scenario (take-over
  racing the UPDATE yanks a landlord-handled row into awaiting_correction) must
  be structurally impossible at ccc0ff6.

(b) **W1 — legacy co-nudge exclusion:** the find's EXISTS leg excludes BOTH
kind-tagged AND legacy untagged co-nudge entries (batch-shape predicate:
single-email batch with no sms sibling at the same `at`); both timestamp
subqueries carry the exclusion. A legacy entry's bounce must NOT exhaust the
corrected row or fabricate `referee_contact_invalid`.

(c) **W2 — the pin bites:** the co-nudge fixture is legacy-shaped with a
POST-correction timestamp (deleting the exclusion turns it red) and the
producer side is pinned (the sweep suite asserts the `"kind": "co_nudge"` tag
lands in the attempts log).

(d) **N1-N19:** each either fixed as claimed or carried with justification.
N4 + N9 were carried with documented justifications (N4: substitution response
id informational — refetch authoritative; N9: pre-correction-only fallback is a
deliberate trade-off). Verify the justifications are REAL (the code matches the
claim), do not auto-flag carried-with-reason items, do not demand rework of a
documented trade-off.

(e) **DO NOT re-litigate:** r1 B1/B2/B3, r2 blocker, r3 blocker, r4's
verified-fixed list (W6, N4-fixed, N8-client, N11-resend, W2-partial, W4, N13,
N15, N16, N21), and r4's 7 rejected false-positives (unused import / doc-vs-SQL
/ `?slot=` degradation / sweep-exclusion clock / detail-payload sentinel /
stand-down silence / schema-migration checks). The gender-neutral pronouns stay
FLAGGED FOR THE HUMAN — not a finding. FLAG NEW findings ONLY.

## What the PR does (review scope — carried from r4)

**Epic RC4 Story 3 — the landlord's per-row control surface:** the panel's ⋯
menu becomes ACTION (RC4.2 deliberately left it unwired — THIS PR wires it):
Take over (A7), Correct (AD-7/A1), Substitute (idempotent), with exhaustion
going LIVE (rc3-7's mechanism). Server-side actions_handler + 8 SQL + trigger/
webhooks/form_handler/router/audit/detail-handler changes; one expand-only
migration; client menu/confirms/toasts/refetch. The r4 rework adds: wrong-
person guarded SQL wiring, legacy co-nudge exclusion, per-row edit dict,
malformed-at consistency, vacancy-check 500s, exhaust-row Sentry capture,
Objected menu arm, client pins.

## ⚠️ CRITICAL lens-guards (carried from r4 — prevents false positives)

- **🚨 TAKE-OVER [A7] — load-bearing.** Guarded on queued/contact_initiated/
  unreachable ONLY; writes `taken_over_at` + clears the cadence clock; status
  stickiness untouched — a late form completion still transitions (§8.6). A
  guard hole, a broken late-completion transition, or a missing sweep exclusion
  = a blocker.
- **🚨 CORRECT [AD-7/A1] — THE ONE-CYCLE RULE.** The awaiting-guard IS the
  one-cycle rule: awaiting_correction → queued with the corrected trio
  (snapshot immutable), correction_cycles = 1, re-arm, audit. A second
  correction allowed (cycle > 1), a mutated snapshot, or a missing audit = a
  real defect.
- **🚨 SUBSTITUTE IDEMPOTENCE [AD-16].** A new reference_call row via an
  idempotent CTE — DOUBLE-SUBMIT must return the existing successor (200, no
  duplicate audit); audit carries old + new ids. A duplicate row or a double
  audit on double-submit = a blocker.
- **EXHAUSTION LIVE (rc3-7's mechanism).** Second failure → unreachable +
  `referee_contact_invalid` stamp, at BOTH the delivery webhooks AND the
  wrong-person route, with audit + in-app notification.
- **EXPAND-ONLY MIGRATION (corrected_name).** One additive migration;
  back-compat decoders; RC4.1 strip assertions untouched.
- **AR-RC13 — one stable contract.** The client refetches after every action
  and renders server-computed hooks/status; NO client-side re-derivation of
  action legality/status.
- **⋯ MENU NOW WIRED (guard flip from RC4.2).** Verify the actions actually
  dispatch (take-over/correct/substitute/sub-nudges); do NOT flag "menu
  unwired" (prior story's design).
- **INLINE CONFIRMS, NEVER MODALS.** A modal confirm = a defect.
- **COPY VERBATIM + RT em-dash ban.** §7.4/§7.7/§8.2/§8.3 copy verbatim; NO
  em-dashes in implementer-authored user-facing strings — check new strings
  AND the timeline composition sites. (N14 was flagged in r4: refcheck_action_
  strings() omitted refcheck_action_correct_details — verify it now carries
  the pin.)
- **TIMELINE SORT (carried warning).** If the PR touches the timeline/attempt-
  log, the RFC3339-vs-`::text` format-mix = a finding.
- **a11y + AC testids** on the menu/confirms/rows; keyboard operable.
- **base = `develop`** (RC4.1 + RC4.2 merged — carry-forward only).
- **bmad-quirk heads-up (context, not a finding):** the create-story/dev-story
  tooling historically mis-resolved edits to the main checkout; Silas syncs it.
  Review the PR content as-is at the sha.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = the original job briefing + the GitHub issue (dump it with `gh issue view <n> --json title,body,comments` into the round dir first), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5`, and `prior_findings` = the previous round's `consolidated.json` when N > 1 (re-review: fix audit first, carry-forward markers). The headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r<N>` labels), the `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and writing `consolidated.json`. Its verdict thresholds are yours below. You MUST close every lens pane before finishing.
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
  (Round-5 note: the human already overrode the cap for this round; if your
  verdict is NEEDS CHANGES, the relay will surface it to the user directly.)
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc4-3-perkins-r5 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
