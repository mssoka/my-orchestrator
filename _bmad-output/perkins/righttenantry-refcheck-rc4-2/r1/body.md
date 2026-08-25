## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantry-refcheck-rc4-2
**Reviewed sha:** 9d66ce9
**Reviewers:** 7/7 (blind, edge, acceptance, security, architecture, codebase, tests — 2 chunks each: spec+client / server+shared)
**Verification:** 55/57 reviewer findings survived code re-verification at `9d66ce9` — 2 discarded as false positives (what-happens-next trailing period: UX §7.4's quote has no period, the PR's own spec added one, code matches UX; batches `< 3` vs `< 4` dev-note: code is correct — after reminder 1, reminder 2 is still pending so the line must show, the spec's number is the typo)
**Build/test at sha:** `make build` ✅ · `make test-client` 502 passed ✅ · `make test-shared` 108 passed ✅ · `make test-server` pass ✅

### Blockers (1)

1. **Panel re-derives terminality client-side (`is_terminal`) and its set already diverges from the server's (omits `Completed`) — hooks shipped in the same payload are ignored** — `client/src/components/reference_panel.gleam:110-124` · [architecture]
   Server computes `can_record_manual: !terminal` (with `Completed` terminal) and ships it in every `ReferenceCallDetail`; the panel instead re-implements the terminal rule in `is_terminal` and omits `Completed`. That is the exact AR-RC13 re-derivation the one-stable-contract guard forbids — a future voice payload renders the wrong sub-line. Fix: `list.all(calls, fn(c) { not c.hooks.can_record_manual })`.

### Warnings (8)

1. **Em-dashes in implementer-authored user-facing strings** — `client/src/copy.gleam:667,844` · [blind/acceptance/architecture/codebase]
   `"Unmoderated referee text — written by the referee, not reviewed by us."` and `"Applicant nudge — couldn't send"` violate the RT CI em-dash ban. The spec gives no verbatim copy for these two strings, so they're implementer-authored — and `no_em_dash_test` only scans toast/page codes, so the new refcheck consts bypass the pin.
2. **Key-facts word map keys on phantom wire value `their_landlord`; real wire value `landlord` renders raw** — `client/src/copy.gleam:750` vs `server/src/reference_checks/questions.gleam:125` · [acceptance]
   The relationship question stores `"landlord"` (tuple's first element); the word map only maps `"their_landlord"`. A landlord-slot relationship renders raw `landlord` in the key-facts table.
3. **`relationship_other` (referee's verbatim "Other" text) is never rendered** — `client/src/components/reference_panel.gleam:806-843,931-938` · [edge/codebase]
   The server stores the custom text alongside `"other"`; the panel drops it and shows bare "Other". The doc comment claims it renders with its parent row; no code does.
4. **"Form opened" timeline line pinned after the invitation batch — out of chronological order when the form opens after a reminder** — `client/src/components/reference_panel.gleam:537-550` · [edge]
   The link stays live; a referee opening at T+50h (after a T+48h reminder) renders Form-opened before Reminder 1.
5. **Objected-state copy hardcodes "him" while the referee name is interpolated** — `client/src/copy.gleam:616-625` · [blind]
   UX §7.4's example referee is male, so "him" is spec-verbatim — but the implementer interpolates arbitrary names, misgendering female referees ("Sarah … asked us not to contact him.").
6. **PR spec promises a localStorage-persisted explainer dismissed state; code ships a session-scoped toggle reset on every route change** — `client/src/model.gleam:316-321` · [blind/acceptance/architecture]
   UX §7.3's "per-user dismissed state" and the PR's own OWNS #3/Dev Notes are unimplemented; the dismissal is forgotten on every navigation.
7. **Character slot's "answered {m} of {n}" counts `free_text_signals` — a field the character form never asks** — `client/src/components/reference_panel.gleam:838-844` · [acceptance]
   A fully-answered character reference reads "answered 6 of 7" because the client counts a field the server always emits `[]`.
8. **First-view auto-expand + toggle/route-reset logic untested; spec-mandated total-match word-map test absent** — `client/src/client.gleam:2989-3022` · [tests]
   The PR's own Verify standard requires a total-match word-map test; none exists (≈5 of ~30 values asserted), and it would have caught warning #2.

### Notes (13)

1. `status_timestamp` Partial/ManualRecorded arms can never fire — `submitted_at` only stamped on `form_completed` (edge/blind).
2. Form-opened `<time datetime>` carries raw Postgres `::text` (colon-less offset — invalid HTML datetime) (edge).
3. `refcheck_off_contacts_label` is dead code (blind/codebase).
4. `month_abbr` duplicated byte-for-byte with `helpers/format.gleam` (codebase).
5. `reference_panel.gleam` is 1263 lines — 3× the view-module target (architecture).
6. Mini-timeline renders unkeyed while rows use `keyed.ul` (architecture).
7. `field_is_answered` counts content-less objects as answered while the renderer shows "Not answered" (blind).
8. First-view auto-expand is consumed even when nothing was expandable (blind).
9. "Never red" test only pins two class tokens (blind).
10. Object renderer branches (ongoing/dont_remember/differs/stated/dont_know/different_amount_eur) and 6 of 7 signal sentences untested (tests).
11. Server empty→null for the new columns unpinned; no integration wire assertion for them (tests).
12. v2 degradation (Scheduled/Calling/Completed), malformed-result path, aria-expanded="true" untested (tests).
13. Advisory test gate: CONCERNS (demoted from the lens's FAIL per repo convention — coverage ladders are not gates) (tests).

### Lens guards that held
- All 13 §4.2 lifecycle rows render verbatim (Off → Something went wrong) with the A5 viewing wording; no missing state, no reworded copy, no spec-em-dash drift (the em-dashes in §7.4/§7.5/§7.8/§10.3 canon copy are the spec's own).
- Pill colours: teal/slate/navy/amber only — never red (§13); test-pinned.
- No guessed values: "Not answered" for unanswered; Period shows confirmed dates (documented deviation, not flagged).
- "Worth knowing" renders only with payload signals; notable quotes only when present (v1 emits none — by design).
- Overflow button deliberately not click-wired (RC4.3 owns actions) — no dead menu.
- Expand-only contract: `form_opened_at`/`submitted_at` additive, back-compat decoders verified (absent-key → None), RC4.1 strip assertions untouched.
- `display_disclaimer` + confidence line rendered verbatim.
- a11y: `role="region"`, aria-label, row buttons with aria-expanded/aria-controls, status not colour-only; all 5 AC testids present.
- §4.2 strip integrity: SQL guards + escaped-marker assertions intact.

### Verdict
**NEEDS CHANGES**

One AR-RC13 blocker (client-side re-derivation of the server's terminal rule, already diverged) plus eight warnings — mostly copy hygiene, one real word-map bug, one data drop, and a timeline-ordering edge. The contract, colours, copy-verbatim matrix, a11y, and test suites are otherwise green at `9d66ce9`.

Address findings and push — a fresh round will re-review the updated head.
