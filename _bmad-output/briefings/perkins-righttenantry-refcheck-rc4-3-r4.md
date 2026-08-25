# Perkins briefing — round 4: righttenantry-refcheck-rc4-3 (USER-APPROVED CAP OVERRIDE)

- **PR:** https://github.com/solarity-services/RightTenantry/pull/606 (targets `develop`)
- **Reviewed sha:** `df0ea22b9317deb20848c6c597333d705a9eb87f` (short `df0ea22`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-3-r4` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc4-3.md` + Story RC4.3 in `_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md` + the UX spec (§7.4/§7.7/§8.2/§8.3 copy) + the architecture (`A7` take-over, `AD-7`/`A1` correct, `AD-16` substitute audit, `§8.6` cadence, `AR-RC13` one-stable-contract). GitHub issue: none (parent story in the epic doc).
- **prior_findings:** r1 (4919278443), r2 (4920836185), r3 (4922512522) — VERIFY-DON'T-REOPEN round (user-approved cap override): (a) CONFIRM the r3 TOCTOU blocker is actually closed at `df0ea22`: the wrong-person awaiting UPDATE must carry the `taken_over_at IS NULL` backstop (dedicated guarded SQL mirroring `mark_awaiting_correction`) AND a take-over-racing-wrong-person-POST integration test must exist and bite (neutralize the backstop -> red). A missing/weak backstop or a vacuous race pin = a blocker. (b) AUDIT the r3 partials (W6, N4, N5, N8-client, N14, N8/N9-spec, N11-resend-pin) — each either fixed or explicitly carried with a reason. (c) DO NOT re-litigate settled findings (r1 B1/B2/B3, r2 blocker, W1-W12, N1-N18 — the ones Perkins verified FIXED in r2/r3 stay closed). N1 pronouns: gender-neutral kept, FLAGGED FOR THE HUMAN — not a finding. FLAG NEW findings ONLY. CONTEXT (r4): the minion's r3-rework badge-out (head df0ea22, CI green incl. terraform, mergeStateStatus CLEAN; suites shared 110 / client 554 / server unit 1482 / integration 533 green; PR comment posted with the full map) — leads, NOT a substitute for your own verification.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**Epic RC4 Story 3 — the landlord's per-row control surface:** the panel's ⋯ menu becomes ACTION (RC4.2 deliberately left it unwired — THIS PR wires it): Take over (A7), Correct (AD-7/A1), Substitute (idempotent), with exhaustion going LIVE (rc3-7's mechanism). Server-side actions_handler + 8 SQL + trigger/webhooks/form_handler/router/audit/detail-handler changes; one expand-only migration; client menu/confirms/toasts/refetch.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 TAKE-OVER [A7] — load-bearing.** Guarded on queued/contact_initiated/unreachable ONLY; writes `taken_over_at` + clears the cadence clock; **status stickiness untouched — a late form completion still transitions (§8.6)**. Sweep exclusion pinned by test. A guard hole (take-over from a wrong state), a broken late-completion transition, or a missing sweep exclusion = a blocker.
- **🚨 CORRECT [AD-7/A1] — THE ONE-CYCLE RULE.** The awaiting-guard IS the one-cycle rule: awaiting_correction → queued with the corrected trio (snapshot immutable), correction_cycles = 1, re-arm, audit. A second correction allowed (cycle > 1), a mutated snapshot, or a missing audit = a real defect.
- **🚨 SUBSTITUTE IDEMPOTENCE [AD-16].** A new reference_call row via an idempotent CTE — DOUBLE-SUBMIT must return the existing successor (200, no duplicate audit); audit carries old + new ids. A duplicate row or a double audit on double-submit = a blocker.
- **EXHAUSTION LIVE (rc3-7's mechanism).** Second failure → unreachable + `referee_contact_invalid` stamp, at BOTH the delivery webhooks AND the wrong-person route, with audit + in-app notification. A miss on either route = a real defect.
- **EXPAND-ONLY MIGRATION (corrected_name).** One additive migration; back-compat decoders; RC4.1 strip assertions untouched. A breaking migration, a dropped back-compat path, or the strip weakened = a blocker.
- **AR-RC13 — one stable contract.** The client refetches the detail after every action and renders the server-computed hooks/status; it does NOT re-derive state rules client-side (the RC4.2 r1 blocker pattern — `is_terminal` re-derivation — must NOT recur). A client-side re-derivation of action legality/status = a blocker.
- **⋯ MENU NOW WIRED (guard flip from RC4.2).** RC4.2's overflow button was DELIBERATELY unwired (RC4.3 owns actions) — THIS PR wires it. Verify the actions actually dispatch (take-over/correct/substitute/sub-nudges); a menu that renders but doesn't dispatch = a real defect. Do NOT flag "menu unwired" (that was the prior story's design).
- **INLINE CONFIRMS, NEVER MODALS** (established pattern) — a modal confirm = a defect.
- **COPY VERBATIM + RT em-dash ban.** §7.4/§7.7/§8.2/§8.3 copy verbatim; **NO em-dashes in implementer-authored user-facing strings** (the RC4.2 r2 warning: `no_em_dash_test` doesn't scan refcheck copy — check the new strings by hand AND the timeline composition sites for ` — ` joins). An em-dash in user-facing copy = a real defect.
- **TIMELINE SORT (carried warning — check if touched).** RC4.2's r2 warned the timeline sort mixes RFC3339 vs Postgres `::text` (same-day inversion). If this PR touches the timeline/attempt-log, the same format-mix = a finding.
- **a11y + AC testids** on the new menu/confirms/rows; keyboard operable.
- **base = `develop`** (RC4.1 + RC4.2 merged — do NOT re-open their findings; carry-forward only).
- **bmad-quirk heads-up (context, not a finding):** the create-story/dev-story tooling historically mis-resolved edits to the main checkout; Silas syncs it. Review the PR content as-is at the sha.
- **Em-dashes in code/commits are fine; in USER-FACING COPY they are banned (RT CI).**

### Legitimate findings here would be
- **A take-over guard hole / broken late-completion transition / missing sweep exclusion** — a blocker [A7/§8.6].
- **A second correction cycle, a mutated snapshot, or a missing correct-audit** — a real defect [AD-7/A1].
- **A duplicate substitute row or double audit on double-submit** — a blocker [AD-16].
- **An exhaustion miss on either route** (webhooks or wrong-person) — a real defect.
- **A breaking migration or weakened strip** — a blocker.
- **A client-side re-derivation of action legality/status** — a blocker [AR-RC13].
- **A wired menu that doesn't dispatch, or a modal confirm** — a real defect.
- **An em-dash in user-facing copy (incl. timeline ` — ` joins)** — a real defect.
- **A `make format` / `make build` / `make test-client` / `make test-shared` / `make test-server` / integration failure at `ace27b1`** (512 int / 540 client / 110 shared / 1476 server).

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 606 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r4/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree at `0fdbf93`), `spec_files` = this briefing + the job briefing + Story RC4.3 + the UX spec (§7.4/§7.7/§8.2/§8.3) + the architecture (A7/AD-7/A1/AD-16/§8.6/AR-RC13), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r4`, `prior_findings` = the r1-r3 review chain — verify the TOCTOU close + r3 partials, don't re-open settled findings, flag NEW only. Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r4` labels), `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (stderr cache warnings would corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 606 --repo solarity-services/RightTenantry --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 606 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `df0ea22`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 4 of 3 (cap overridden by the user)` / **Job:** righttenantry-refcheck-rc4-3 / **Reviewed sha:** ace27b1 / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc4-3-perkins-r4 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: `deepseek/deepseek-v4-flash`** — fleet-wide ruling 2026-08-12 (user override): the ENTIRE fleet rides deepseek on API access, FULL THROTTLE (no glm cap, no serialization — rounds may run parallel with other rounds). Launch every lens mega-minion with `pi --model deepseek/deepseek-v4-flash` — never bare `pi` (resolves to the kimi default) and never glm-5.2. If the round hard-fails, self-report `blocked`.
