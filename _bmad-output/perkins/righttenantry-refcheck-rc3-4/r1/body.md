## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantry-refcheck-rc3-4
**Reviewed sha:** `13ae750b4a75a9c06c6c4670c334bc5fbc415889` (head unchanged mid-review)
**Reviewers:** 7/7 completed (blind · edge · acceptance · security · architecture · codebase · tests) — 0 failed
**Verification:** 25/25 reviewer findings survived code re-verification — 0 discarded as false-positive, 0 unverifiable. Dedup → **21 unique** (1 blocker / 6 warnings / 14 notes). Single-wave (diff 3310 lines; lens-guards need holistic cross-file verification, so directory-chunking would fragment it).
**Model:** `zai-coding-cn/glm-5.2` (kimi quota down — sanctioned fallback).

### Lens-guards (verified, not re-litigated)
- ✅ **Registry prefix-match** — `is_public_path` / `csrf.should_skip` / `redact_token_route` each have exactly ONE `["reference", ..]` prefix arm, none shadowed; all 7 router arms live under `/reference/`. Per-route registry entries would be dead code. No false positive filed.
- ✅ **Objection stickiness** — guarded `WHERE status='contact_initiated'`; late submit/stop on an `objected` row is a 0-row no-op. AC5 test asserts status+outcome+result-outcome+result-verification+evidence-count unchanged (real, not tautological).
- ✅ **Evidence-log single writer** — `apply_objection` is the sole writer; INSERT fires only when the guarded UPDATE returns a row (at most once); `channel:'web'`; migration widens the CHECK.
- ✅ **Deterministic result** — `result.gleam` is pure, no LLM; `ai_summary` templated; `confidence` from completeness.
- ✅ **One submission** — second POST on a terminal token → redirect to the branded GET page.
- ✅ **Carry-forward folded** — N3 (`get_value` deleted; 5 sites via `application_handler.get_form_value`) + N6 (`view_post_form` at `form_pages.gleam:292`, used by resend + all 4 exit forms).
- ✅ **Em-dash ban** — zero em-dashes in user-facing string literals (grep hits are code comments only).

---

### Blockers (1)

**B1 — Reference notifications pass a scheme-full origin → double-scheme `https://https://…` dead CTA in every reference email** `acceptance`
`server/src/reference_checks/form_handler.gleam:1309` (+ `notification_dispatch.gleam:478`, `email_client.gleam:891`)
```gleam
let origin = domain_helpers.origin_from_domain(row.origin_domain)  // → "https://righttenantry.ie"
…
origin_domain: origin,   // fed to notify_reference_* → build_entity_url
```
`build_entity_url` always prepends `https://` (`"https://" <> domain <> path`), so every reference notification's "View application" CTA becomes `https://https://righttenantry.ie/vacancies/<id>/applications/<id>` — a dead link. The precedent `notify_application_scored` (`ai_client.gleam:1927`) correctly passes the **raw** `vacancy_row.origin_domain`. **Fix:** pass `row.origin_domain` raw to the three `notify_reference_*` calls (reserve `origin_from_domain` for the invite base_url).

### Warnings (6)

**W1 — `focus_seconds_reported` is always 0 in production** `blind`
`form_pages.gleam:211-234` (`view_review`) + `form_handler.gleam:1262`. The review submit form renders honeypot + timing + button but **no `_focus_seconds`** (only `form_question_pages.gleam:84` renders it, on the per-question form). `reference_form.js:157` fills `[data-focus-seconds]` only if present. So the submit POST never carries `_focus_seconds` → `parse_focus_seconds` → 0, contradicting the dev record ("rc3-4 captures focus_seconds_reported") and starving rc3-7's focus-time signal. The integration test masks it by injecting `#("_focus_seconds","240")`. **Fix:** add the hidden field to the review submit form; stop injecting it in the test.

**W2 — `decline_reason` has no server-side bound** `edge` `security`
`form_handler.gleam:926-930`. `apply_decline` stores the reason verbatim into the result JSONB; the only cap is client-side `maxlength="200"`. The `/apply` precedent truncates identical free text to 2000 graphemes (`application_handler.gleam:1772/1788/1802`); decline does not. **Fix:** pipe through `truncate(200)` (or 2000) server-side.

**W3 — AC7 abuse posture has ZERO coverage on the four new exit-route POSTs (incl. the stop-must-not-object branch)** `tests` `codebase`
Every exit-route integration test sends a clean honeypot (`timing_fields()`). No test fills the honeypot or trips timing on submit/decline/stop/wrong-person. `handle_stop_post`'s fake-success-without-objecting branch — the "critical" AC7 case (a fake object on a leaked token would silently opt out real referees) — is unpinned. The guard is correct; the coverage is absent. **Fix:** add tests: honeypot-filled POST to `/stop` → 200 stop-confirmed, row stays `contact_initiated`, `objection_log` count 0; likewise for the other routes.

**W4 — `notify_reference_completed/declined/objected` + the `late_after_handoff` branch have no test pins** `tests`
AC1/AC3/AC4 "dispatches" clauses unpinned (no notification-row, no preference-gate, no late-completion-copy assertion). Because `notify_reference_event` discards the dispatch `Result`, a broken dispatch passes CI silently. **Fix:** assert the notification row + late-completion copy.

**W5 — The four new audit terminal events are written but never asserted** `tests`
The audit-on-status-change defended invariant (AGENTS.md) is unpinned for the `form_completed`/`refused`/`objected`/`awaiting_correction` transitions rc3-4 introduces. **Fix:** query `audit_log` for the expected `event_type` + `entity_id` in the per-path tests.

**W6 — Advisory test gate: FAIL** `tests`
Per-AC: AC1 55%, AC2 80%, AC3 57%, AC4 63%, AC5 100%, AC6 90%, **AC7 0%**, AC8 100%, AC9 100% → overall ≈72% (<80%). AC5 (objection stickiness) + AC8 (registry coverage) tests are genuinely biting; the unit suite is green (server 1418, integration 448). Largely a coverage signal — fixing W3/W4/W5 lifts it above threshold.

### Notes (14)

- **N1** `blind` `acceptance` — `character_ref` verification block omits the spec-pinned `free_text_signals[]` (`result.gleam:164-173`); nil impact today (no character free-text question) but the AD-9 shape is incomplete for RC4.
- **N2** `blind` — `headline()` LandlordRef has two identical arms (`result.gleam:222-223`); the `_, ""` arm is shadowed by `_, _`. Dead code.
- **N3** `blind` — an objector re-visiting the token sees "This reference was declined." (`classify` collapses `Refused|Objected → Declined`). Honest-first copy mismatch; a distinct `view_objected` or truthful shared copy resolves it.
- **N4** `acceptance` — `form_session.completion_seconds` is null at submit; spec Dev Notes pin it as rc3-4's job, Completion Notes defer to rc3-7 (internal spec contradiction; implementation follows the Completion Notes).
- **N5** `acceptance` — AC8 CSRF-stack test asserts only `not_equal(403)`, weaker than the spec-pinned 2xx/3xx reachability assertion; a 404/500 would pass. Tighten to `{200,303}`.
- **N6** `codebase` — the claimed `'telegram' ✗` negative-control bite-test for the widened channel CHECK does not exist (the `'web' ✓` half does). Overclaim in the dev record.
- **N7** `security` — `parse_focus_seconds` accepts negative/unbounded values (no clamp); moot in prod today (W1) but reachable via crafted POST.
- **N8** `architecture` — `purge_after` is stamped only by `complete_reference_call`; refused/objected keep it NULL despite the column's "stamped at terminal" comment. Deferred impact (no purge sweep yet).
- **N9** `architecture` — exit handlers omit `handle_resend`'s injectable seam; `notify_reference_event` discards the dispatch `Result` (ties to W4).
- **N10** `architecture` — `ObjectionChannel` shared enum lacks the `'web'` variant the new migration adds (documented drift; inert today).
- **N11** `edge` `security` — objection evidence INSERT is not atomic with the guarded terminal UPDATE; a crash in the window leaves an objected row with no Art 21 evidence (documented best-effort; a transaction or retry closes it).
- **N12** `tests` — `purge_after` / `submitted_at` / denormalised `fraud_signals` are never asserted at submit.
- **N13** `tests` — AC2 one-submission pin asserts only the 303, not that nothing re-persisted (low risk — handler redirects before any write).
- **N14** `tests` — the three GET confirm pages are untested, incl. AC4's pre-fetch-safe stop GET (mutates nothing).

### Reviewer Agreement (multi-source — higher confidence)
- **W2** decline-reason bound — `edge` + `security`
- **W3** AC7 abuse coverage — `tests` + `codebase`
- **N1** character `free_text_signals` — `blind` + `acceptance`
- **N11** non-atomic evidence — `edge` + `security`

---

**Verdict: NEEDS CHANGES**

One verified production defect (B1 — dead email CTA on every reference event, one-line fix) plus a coverage gate that fails primarily on the unpinned AC7 abuse branch (correct code, missing tests). The load-bearing lens-guards all hold: objection stickiness, single-writer evidence, deterministic result, prefix-match registries, and the N3/N6 carry-forward are genuinely in place.

Address findings and push — Perkins round 2 will re-verify the fixes against this round's `consolidated.json` (`_bmad-output/perkins/righttenantry-refcheck-rc3-4/r1/consolidated.json`).

— *Perkins (automated). 7-lens headless wave on `zai-coding-cn/glm-5.2`.*
