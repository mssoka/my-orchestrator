## 🤖 Perkins automated review — round 1 of 3
**Job:** righttenantry-refcheck-rc3-3 · **Reviewed sha:** a0b6910 · **Reviewers:** 7/7 completed
**Verification:** 42/46 findings confirmed against the code — 4 discarded as false-positive

### Blockers (1)

1. **`/reference/*` POST/PUT routes missing from `csrf.should_skip`** — `server/src/auth/csrf.gleam:79-101` + `server/src/router.gleam:80, 968-973` · [tests, edge, architecture]
   Every sibling public POST family (`/apply`, `/dsar`, `/erase`) is CSRF-skipped; `/reference` is not. The router runs `csrf.validate` unconditionally, and `validate_token` enforces whenever the request carries a valid `rt_session` cookie — the SSR form and `reference_form.js` never send `x-csrf-token`. A referee whose browser holds a session (landlord testing their own invite link, a shared device, a referee who is also a landlord) gets **403 CsrfInvalid on every answer POST/PUT and the resend**, with the answer lost and the JS falling back into the same 403. Same registry-omission class as the rc3-2 redact gap this round was mandated to fix — the AD-3 "three places" checklist has a fourth registry.
   **Fix:** add `["reference", ..] -> True` to `csrf.should_skip` (the apply/dsar/erase pattern) + a pin in `server/test/auth/csrf_test.gleam` + a router-stack integration test with a session cookie.

### Warnings (11)

1. **Desktop JS path never navigates to the review screen after the final answer saves** — `server/priv/static/reference_form.js` (navigation only under `shouldStep(isMobile)`) · [blind, edge, architecture] · No-JS POST (303 to bare URL) and mobile JS both reach the review; desktop+JS leaves the referee stranded with no in-page path to the review/submit screen (the URL carries `?q=` so even a reload re-renders the form).
2. **Validation-error re-render discards the submitted answer** — `form_handler.gleam` (error branch re-renders from the DB draft only) · [acceptance, codebase, edge] · The cited `/apply` precedent (`view_form_with_errors`) preserves submitted values; the referee's just-typed answer vanishes while the inline error says "Check it and try again".
3. **Autosave DOM choreography has zero automated coverage; the JS comment claims bug-hunt E2E scenarios that do not exist** — `scripts/js-tests/reference_form.test.js` + `.pi/skills/bug-hunt/scenarios/` · [tests] · The `form_draft_wiring` precedent was not followed; the fetch/PUT/409-reload/POST-fallback wiring is unpinned.
4. **PUT `/answer` error contract untested (400/404/409/bot-200)** — integration pins only the 200 happy path · [tests] · The JS keys its closed/unknown reload behavior off 409/404; a regression would silently misbehave.
5. **No fetch/FormData capability gate: a fetch-less environment swallows the submit with no native-POST fallback** — `reference_form.js` `onSubmit` (`preventDefault()` first) · [acceptance, edge] · Marginal in practice (fetch is universal), one line to guard.
6. **Answer-timing stale cap (7 days) is shorter than the link TTL (10 days): a legitimate slow referee's answers are silently dropped with fake success** — `form_handler.gleam:is_answer_timing_suspicious` vs `remint_form_token.sql` · [security] · Decision 12 adapted the fast floor but carried the stale cap over unexamined from the /apply one-sitting posture; the JS even shows "Saved".
7. **Resend delivered-path effects unpinned** (remint persisting, old token dying, the `reference_call_link_resent` audit row, the resent page) — integration pins only the all-failed rollback branch · [tests] · The compliance-relevant audit write is never executed by any test.
8. **`questions.gleam` read-side (`decode_draft`, `prefill_for`, `answer_summary`) has zero direct tests** — the resume/review half of the A2 contract is pinned write-side only · [tests].
9. **Employer/character slot renderers never executed by any test** — `form_pages_test` builds `LandlordRef` views only; the as-stated + short-text-pair controls of 2 of 3 slots are unpinned · [tests].
10. **`form_pages` re-implements the pub brand header** — private copy is byte-identical to `application/form_view.view_brand_header` (already imported) · [codebase] · Third copy of the wordmark markup.
11. **`month_year` accepts non-canonical months ("2023-6", "2023-006")**, bypassing the zero-padded ordering assumption and letting a crafted from>to pair store · [edge, blind, codebase] · Crafted-input only (browsers always zero-pad).

### Notes (33)

Key ones: AC6's 2s floor vs the documented 500ms answer adaptation (spec decision 12, disclosed); `_focus_seconds` documented as visibility-gated but implemented as wall-clock; `restore_form_token` lacks the remint's `taken_over_at` guard (harmless — restored token is always expired); `stamp_form_opened` SQL guard weaker than its docstring; `get_form_context_by_form_token` selects an unused `rc.form_token` with a false justification comment; mobile-stepper `focus()` targets the hidden `_question` input (no-op); matchMedia gate evaluated once; `shouldStep` tests tautological; `SAVED_TEXT` sync comment-only; spec structure notes omit `restore_form_token.sql`; JS test count "118+6" overstated (118 total, verified by running); router wiring + the AC7 catch-all arm untested (integration bypasses the route table — the exact gap that let the CSRF omission slip); `clamp_current` untested; escape-route/review-submit forward links render live but unregistered (rc3-4 contract — unreachable pre-rc3-5, but rc3-4 must land before rc3-5 mints tokens, and the interim 404 copy reads misleadingly); desktop "Save" chrome not rendered (`save_label` dead); `other_option_label` dead; hard-coded `reference-input-dont_remember` testid; `thousands_separated` duplicates an existing helper; resend double-submit lands on the truthful unknown page (handled by design); `form_handler` ~835 lines vs the 200 target; `is_answer_timing_suspicious` copies `is_timing_suspicious`; public-path pins omit `/wrong-person`/`/decline`; `test-token-48-chars` fixture is 19 chars; `open_vars` fixture drift; banned-vocab test is case-sensitive; `euro_amount` accepts leading zeros; em-dash enumeration is hand-maintained; CopyVars fixtures triplicated; bot fake-advance 303s to the bare URL (distinguishable shape from the legit `?q=` advance, minor); landlord compound-control fields never asserted; resume pre-fill wiring never asserted; Start/Back navigation pins missing; **Advisory test gate: CONCERNS** (per-chunk c1 FAIL, c2 FAIL, c3 PASS, c4 CONCERNS, c5 CONCERNS — the P0 first-class no-JS path is well pinned; the JS-enhancement path and the middleware chain are the drag).

### Reviewer agreement

- **CSRF skip-list omission** — 3 lenses (tests, edge, architecture), verified by direct code trace. The highest-confidence finding in this round.
- **Desktop JS review-screen gap** — 3 lenses (blind, edge, architecture).
- **Validation-error re-render discards input** — 3 lenses (acceptance, codebase, edge).
- **`_focus_seconds` docs mismatch / timing-floor deviation / unused `rc.form_token` / matchMedia one-shot / `shouldStep` tautology** — 2 lenses each.

### Discarded as false-positive (4)

- Character `would_stand_again` "no" option — spec-pinned UX table (§6.5: Yes / Unsure / Prefer not to say).
- Wrong-person URL swallowed by the catch-all — rc3-4 forward contract, spec-explicit, unreachable pre-rc3-5.
- `q_salary` empty-datum fallback — `monthly_income_cents` is `NOT NULL` in the schema; salary is always present.
- Amount field-name derivation asymmetry — internally consistent per control.

### Verification

- **The mandated redact fix is DONE and complete**: `redact_token_route` gained `["reference", ..] -> Ok("/reference/<redacted>")` (prefix covers `/answer` + `/resend`), `is_public_path` gained the `/reference` arm, the router has all five arms before the SPA catch-all, and the regression pins cover `sentry_safe_path` (token + sub-paths), `access_log_line`, CSP `redact_token_url`, and `is_public_path`. The CI-guarded em-dash ban holds across the entire diff (zero U+2014). CI is green on this sha (format/lint/unit/build, integration, migration-safety, terraform).
- 35/35 lens runs completed (5 chunks x 7 lenses, big-diff chunking); no degraded lenses.
- Full `consolidated.json` at `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-3/r1/consolidated.json`.

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
