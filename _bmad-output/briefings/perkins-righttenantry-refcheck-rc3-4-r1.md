# Perkins briefing — round 1: righttenantry-refcheck-rc3-4

- **PR:** https://github.com/solarity-services/RightTenantry/pull/599 (targets `develop`)
- **Reviewed sha:** `13ae750b4a75a9c06c6c4670c334bc5fbc415889` (short `13ae750`; commit "feat(refcheck): RC3.4 form completion + exit routes (submit/decline/stop/wrong-person)")
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-4-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc3-4.md` + the story spec at `_bmad-output/implementation-artifacts/spec-rc3-4-form-completion-exit-routes-submit-decline-objection-wrong-person.md` + the architecture (AD-3/AD-6/AD-7/AD-9/AD-14, A8, A9, §4.6) + UX (§6.5/§7.9/§8.6/§10.2). No GitHub issue.
- **prior_findings:** none (round 1 for this PR). CONTEXT: the rc3-3 r2 review (APPROVED, `_bmad-output/perkins/righttenantry-refcheck-rc3-3/r2/consolidated.json`) had advisory notes on files rc3-4 extends — N3 (get_value dedup) + N6 (resend-form extract) were the ones flagged for rc3-4; the minion claims they're folded. Verify they're actually folded.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**RC3.4: Form Completion & Exit Routes** — everything that happens when the referee finishes or bails on the rc3-3 form session:
- **Submit:** guarded `contact_initiated → form_completed` transition (AD-14), deterministic `ReferenceCallResult v1` (AD-9 — schema_version "refcall-v1", verification block with per-slot variants, free_text_signals verbatim, ai_summary with completeness-derived confidence, compliance block), one-submission-only (AD-3), `purge_after` from retention, audit terminal entry, thank-you identical across paths (§8.6 — referee never told of takeover).
- **Decline:** → `refused` (A8), optional one-line reason (never required), null verification, `reference_declined` notification, messages stop.
- **Stop-link objection:** → sticky `objected` (AD-6/AD-14 — a late bounce/sweep/submission CANNOT move it), `next_attempt_at` NULL, all future sends blocked, `reference_objection_log` row written AT OBJECTION TIME by the objection handler ALONE (single writer, channel 'web' — note: a migration adds the 'web' CHECK value the AD-6 amendment needed).
- **Wrong-person:** → `awaiting_correction`, never a re-send to the same details (AD-7), `next_attempt_at` NULL.
- **Notifications** per UX §7.9 verbatim + a late-completion copy branch on `taken_over_at`.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

Production server code (Gleam SSR) on the referee-facing path.

- **THE REGISTRY LENS-GUARD — verify the minion's prefix-match finding, don't re-litigate it.** The 3 security registries (`is_public_path`, the CSRF allowlist, `redact_token_route`) are **prefix-matched** — a single `["reference", ..]` arm covers ANY depth (the `..` is a list-tail wildcard; the docstrings say so). Per-route registry entries would be DEAD CODE (Gleam `case` arms match in order — the prefix shadows them). The ROUTER is the only per-arm registry (7 new arms for submit/decline/stop/wrong-person). So the real verification: **(a)** every new route has its ROUTER arm, **(b)** the end-to-end coverage tests hit each route through the full middleware stack (no 403-CSRF, redacted paths in logs), **(c)** the prefix arms genuinely cover the new paths (a route OUTSIDE the prefix pattern would be a blocker). The minion also surfaced + fixed two real gaps: the `objection_log.channel` CHECK lagged the AD-6 amendment (added 'web') + `update_reference_call_status` needed `awaiting_correction` in its no-send CASE — verify both are actually in.
- **THE LOAD-BEARING EDGE CASE: objection stickiness (AD-6/AD-14).** A late event (bounce, sweep tick, second submission) MUST NOT un-object or move an objected row. The integration suite claims objection-stickiness-vs-late-submit + evidence-written-once — verify the tests are real (not tautological) + the guarded `UPDATE ... WHERE` actually prevents movement.
- **`reference_objection_log` single writer** — only the objection handler writes it, AT OBJECTION TIME (Art 21 evidence, survives parent deletions). Verify no other writer + the row is written at objection, not later.
- **Deterministic result (AD-9)** — the result must be deterministic (no LLM in the result path per the briefing: "deterministic ReferenceCallResult v1 (new result.gleam, AD-9 — no LLM)"). Verify the result is fully deterministic + the guarded transitions are real.
- **One submission only (AD-3)** — a second POST to the same token → branded "already completed" page, no duplicate result/audit.
- **The rc3-3 r2 carry-forward** (N3 get_value dedup + N6 resend-form extract) — verify folded into the files rc3-4 extends.
- **Do NOT flag "missing per-route registry entries"** — per the lens-guard above, that would be dead code + a false positive (the prefix arms cover all `/reference/*`).
- **Do NOT flag the truthful/decline/escape-route copy** as "missing features" — honest-first design is the spec (the referee is doing the applicant a favour).
- **SSR never requires JS** — the exit routes work as plain POSTs (decline/object/wrong-person reachable without JS). Do NOT flag "the JS path should be primary."
- **No em-dashes in user-facing copy** (RT CI ban) — notification copy, thank-you, confirmation pages. The minion claims the em-dash→period fix + a migration bite-test ('web' ✓ / 'telegram' ✗).
- **JSONB test gotchas (from the minion's field-note — check the tests aren't broken by these):** Postgres JSONB re-serialises with a space after colons (`"key": value`) + may reorder keys — substring assertions on `result::text` FAIL; correct assertions use `result->>'field'` extraction. Squirrel generates its OWN `ReferenceCallStatus` type inside `reference_checks/sql.gleam` (separate from `shared.reference_call.ReferenceCallStatus`) — status args must be `sql.Refused`/`sql.Objected`/etc. `decode.null` does NOT exist in this Gleam version.

### Legitimate findings here would be
- **Objection stickiness broken** — a late event moves/un-objects an objected row (the guarded transition is wrong or a path bypasses it).
- **The evidence log is wrong** — written by another writer, or not at objection time, or missing the 'web' channel handling.
- **A double-submit leaks** — a second POST creates a duplicate result/audit/notification instead of the branded page.
- **A new route missing its router arm** or OUTSIDE the prefix coverage (a genuinely uncovered path = blocker).
- **A deterministic-result violation** — nondeterminism in the result construction, or the guarded transition not actually guarding.
- **The carry-forward (N3/N6) not folded.**
- **A Gleam compile/test failure** (minion reports shared 101 / client 471 / server 1418 / integration 448 — verify real).

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 599 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the job briefing + the story spec + the architecture (AD-3/AD-6/AD-7/AD-9/AD-14, A8, A9, §4.6) + the UX (§6.5/§7.9/§8.6/§10.2), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r1`, `prior_findings` = none (round 1). Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (cache warnings on stderr corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 599 --repo solarity-services/RightTenantry --body-file <body.md>`, note `fallback-comment` in your ledger note + final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 599 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** righttenantry-refcheck-rc3-4 / **Reviewed sha:** 13ae750 / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc3-4-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: zai-coding-cn/glm-5.2** — kimi quota down; glm-5.2 is the sanctioned fallback.
