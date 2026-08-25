# SHARED CONTEXT — Perkins r2 lenses (righttenantry-refcheck-rc4-3)

You are one lens in a parallel code-review wave (round 2). Read-only access to the repository. Verify every claim against the actual codebase — no claim is taken at face value. Every finding you emit is independently re-verified by the round conductor (Perkins) against the worktree; findings that fail verification are DISCARDED silently.

## Round & scope

- **Round 2 of 3.** PR #606 → `develop`. Reviewed sha `0fdbf93cb56c010bcbee3dfe3c7268225d70e5eb` (short `0fdbf93`).
- **Scope:** Epic RC4 Story 3 — the landlord's per-row control surface. The panel's `⋯` menu becomes ACTION (RC4.2 deliberately left it unwired — THIS PR wires it): **Take over** (A7), **Correct** (AD-7/A1), **Substitute** (idempotent, AD-16), with exhaustion going LIVE (rc3-7's mechanism). Server-side `actions_handler` + 16 SQL + trigger/webhooks/form_handler/router/audit/detail-handler changes; one expand-only migration (`corrected_name` + `corrected_at`); client menu/confirms/toasts/refetch.
- 47 files, 8493 diff lines, chunked c1–c4. Review EXACTLY the bytes of your assigned chunk; the worktree is at the same sha for verification.
- base = `develop` (RC4.1 + RC4.2 merged — do NOT re-open their findings; carry-forward only).
- **Round context (from the briefing):** this is the r1 REWORK head. r1 review (4919278443) was NEEDS CHANGES @ `ace27b1`: 3 blockers + 12 warnings + notes. The implementing minion claims ALL addressed in the rework (head `0fdbf93`, MERGEABLE badge-out; suites green locally: shared 110 / client 544 / server unit 1477 / integration 521; migration gained `corrected_at`, expand-only, still unmerged; CI: code jobs green, Terraform fmt+validate job was failing on a PROVIDER DOWNLOAD TIMEOUT infra flake, not code). Those claims are leads, NOT a substitute for your own verification.

## Inputs (absolute paths)

- `diff_file` chunk 1 (server/src code — actions_handler, sql.gleam, trigger, webhooks, sweep, form_handler, router, audit/event_type, notification_dispatch, retention/audit_log_schema, application_detail_handler, application/sql.gleam): `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r2/diff.c1.patch`
- `diff_file` chunk 2 (server SQL — 16 files under reference_checks/sql/ + application/sql/list_reference_calls_for_detail.sql — plus server tests — actions integration + detail payload + schema migration + audit schema): `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r2/diff.c2.patch`
- `diff_file` chunk 3 (client — reference_panel, api/reference_checks_api, client, model, msg, copy, pages/application_detail, + client tests): `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r2/diff.c3.patch`
- `diff_file` chunk 4 (shared types/decoders + shared tests + the expand-only migration + the PR's own spec artifacts): `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r2/diff.c4.patch`
- `worktree`: `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-3-r2` (detached at `0fdbf93`; verification reads happen HERE)
- Round briefing (lens-guards + standing orders): `/Users/moses/code/_bmad-output/briefings/perkins-righttenantry-refcheck-rc4-3-r2.md`
- Job briefing: `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc4-3.md`
- Prior findings (r1 review — the FIX AUDIT list): `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r2/lens-briefs/prior-findings.md`
- Story RC4.3 AC (epics file, Story RC4.3 at line ~659): `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-3-r2/_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md`
- UX spec (authoritative copy — §7.4 state-by-state ~385, §7.7 warm handoff ~492, §8.3 correction ~541, §8.6 late completion ~579, §8.2 substitution ~538, §7.6 attempt log ~477, §12 a11y ~677): `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-3-r2/_bmad-output/planning-artifacts/ux-reference-checking-v1-2026-07-29.md`
- Architecture (A7 amendment ~line 61 epics, AD-7 one-cycle ~342, AD-14 mutation ownership ~508, AD-16 audit ~553, §8.2 state rules the API computes ~996, §4.1 table shape ~592): `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-3-r2/_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md`
- PR's own implementation spec (in the diff, chunk c4): `_bmad-output/implementation-artifacts/spec-rc4-3-row-actions.md` and `epic-RC4-context.md` in the worktree

## FIX AUDIT — read prior-findings.md FIRST

Round 2 is a re-review. Every r1 finding (3 blockers + 12 warnings + 18 notes) is listed in `prior-findings.md` with its r1 location. For each prior finding **in your lens's area**, re-read the cited code in the CURRENT worktree and classify:
- **FIXED** → say nothing (no finding).
- **STILL PRESENT or WRONG FIX** → emit a finding with the ORIGINAL severity, title prefixed `STILL PRESENT (r1): `, location = current file:line, evidence = the current code that shows the gap.

Do NOT re-open fixed findings as new. A missing or wrong fix is a finding. Note: r1 findings were reported against the PRE-rework diff; the rework may have moved code (e.g. helpers extracted, files added like `verify_application_in_vacancy.sql`, `update_application_referee_trio_*.sql`, `sweep_claim_t0.sql`, `find_reference_call_by_send_ref.sql`) — find the current home of each concern before classifying.

The implementing minion's own fix map (leads, verify yourself):
- **B1** correct SQL resets `attempt_count=0` + fresh `form_token` (sweep re-runs the T0 claim to the corrected contact; pinned 2 ways incl. the negative control `corrected_row_without_attempt_reset_dead_ends_test`).
- **B2** action buttons omit the `disabled` attribute when enabled (serialized adjacency test).
- **B3** substitute gated on `hooks.can_substitute_referee` everywhere + take-over gained a server hook `can_take_over` (no action legality re-derived client-side).
- Warnings: stale-bounce exhaustion gate (new `corrected_at` column — a redelivered pre-correction failure stands down instead of fabricating `referee_contact_invalid`), corrected-replaces-snapshot effective-contact rule, app↔vacancy precheck, route-change PII leak, late-response guard, em-dash scan gap.
- Notes N1–N18 mostly folded incl. creation-fraud stamping on substituted rows.

## 🚨 Lens-guards — the load-bearing checks of THIS round (verify, don't assume)

1. **🚨 TAKE-OVER [A7] — load-bearing.** Guarded on queued/contact_initiated/unreachable ONLY; writes `taken_over_at` + clears the cadence clock; **status stickiness untouched — a late form completion still transitions (§8.6)**. Sweep exclusion pinned by test. A guard hole (take-over from a wrong state), a broken late-completion transition, or a missing sweep exclusion = a blocker.
2. **🚨 CORRECT [AD-7/A1] — THE ONE-CYCLE RULE.** The awaiting-guard IS the one-cycle rule: `awaiting_correction` → `queued` with the corrected trio (snapshot immutable), `correction_cycles = 1`, re-arm, audit. A second correction allowed (cycle > 1), a mutated snapshot, or a missing audit = a real defect.
3. **🚨 SUBSTITUTE IDEMPOTENCE [AD-16].** A new `reference_call` row via an idempotent CTE — DOUBLE-SUBMIT must return the existing successor (200, no duplicate audit); audit carries old + new ids. A duplicate row or a double audit on double-submit = a blocker.
4. **EXHAUSTION LIVE (rc3-7's mechanism).** Second failure → `unreachable` + `referee_contact_invalid` stamp, at BOTH the delivery webhooks AND the wrong-person route, with audit + in-app notification. A miss on either route = a real defect.
5. **EXPAND-ONLY MIGRATION (corrected_name + corrected_at).** One additive migration; back-compat decoders; RC4.1 strip assertions untouched. A breaking migration, a dropped back-compat path, or the strip weakened = a blocker.
6. **AR-RC13 — one stable contract.** The client refetches the detail after every action and renders the server-computed hooks/status; it does NOT re-derive state rules client-side (the RC4.2 r1 blocker pattern — `is_terminal` re-derivation — must NOT recur; the r1 B3 blocker was exactly this for substitute). A client-side re-derivation of action legality/status = a blocker.
7. **⋯ MENU NOW WIRED (guard flip from RC4.2).** RC4.2's overflow button was DELIBERATELY unwired — THIS PR wires it. Verify the actions actually dispatch (take-over/correct/substitute/sub-nudges); a menu that renders but doesn't dispatch = a real defect. Do NOT flag "menu unwired" (that was the prior story's design).
8. **INLINE CONFIRMS, NEVER MODALS** (established pattern) — a modal confirm = a defect.
9. **COPY VERBATIM + RT em-dash ban.** §7.4/§7.7/§8.2/§8.3 copy verbatim; **NO em-dashes in implementer-authored user-facing strings** — check the new strings by hand AND the timeline composition sites for ` — ` joins. An em-dash in user-facing copy = a real defect. (The UX spec's own strings contain em-dashes — where the spec itself ships one, verbatim wins; an em-dash ADDED by the implementer where the spec has none, or in implementer-authored strings, is a defect.)
10. **TIMELINE SORT (carried warning — check if touched).** RC4.2's r2 warned the timeline sort mixes RFC3339 vs Postgres `::text` (same-day inversion). If this PR touches the timeline/attempt-log, the same format-mix = a finding.
11. **a11y + AC testids** on the new menu/confirms/rows; keyboard operable.
12. **The verification claims:** 521 integration / 544 client / 110 shared / 1477 server unit green at `0fdbf93` — claimed by the implementer, verify what you can from the diff (test files exist, tests assert the guards).
13. **bmad-quirk heads-up (context, not a finding):** the create-story/dev-story tooling historically mis-resolved edits to the main checkout; Silas syncs it. Review the PR content as-is at the sha.
14. Em-dashes in code/commits are fine; in USER-FACING COPY they are banned (RT CI).

## OUTPUT CONTRACT (mandatory)

Write ONLY a single valid JSON array to your assigned output file (path given in your lens brief). Each element matches this schema exactly:
`{"source": "<your source tag>", "severity": "blocker"|"warning"|"note", "category": "<short tag>", "title": "<one-line>", "location": "<file:line | file:hunk | N/A>", "evidence": "<EXACT lines you read from the file/diff — verbatim, no paraphrase>", "detail": "<≤40 words>", "recommended_fix": "<≤40 words>"}`

No prose, no markdown fencing, no preamble. `[]` is valid and expected when you find nothing real. Do not invent findings to fill a quota. Then stop.
