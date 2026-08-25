## 🤖 Perkins automated review — round 2 of 3 (fix-audit)

**Job:** righttenantry-refcheck-rc3-4
**Reviewed sha:** 8c9c87e (r1 was 13ae750)
**r1 audit:** **1/1 blockers FIXED** (B1 dead email CTA) — but **W1's fix is INERT** (promoted to r2 blocker below). Warnings: 4/6 fixed (W2/W3/W5/W6), W4 partial, W1 not fixed. Folded notes: 5/5 fixed (N1/N2/N3/N5/N6). Deferred notes: 9 hold (N4/N7-N14, rationales verified).
**Reviewers:** 7/7 (blind, edge, acceptance, security, architecture, codebase, tests — 0 failed, 0 retried)
**Verification:** 8/8 lens findings confirmed against the worktree; 21/21 prior r1 findings dispositioned. Suite verified green: build clean, server unit 1403 / 0 fail, integration 441 / 0 fail / 0 DB-skips. Lens-guards re-confirmed (objection stickiness, single-writer evidence, deterministic result, one-submission, registry prefix-match, B1 completeness on all notification paths, em-dash ban).

---

### ✅ What's genuinely fixed (verified)

- **B1 (r1 blocker): FIXED on every notification path.** `notify_reference_event` now passes the raw `row.origin_domain` to all three of `notify_reference_completed/declined/objected`. `origin_from_domain(...)` is kept only for the invite `base_url` (`form_handler.gleam:694`). `dispatch_reference_notification` → `build_entity_url(origin_domain:, …)` prepends `https://` itself, so the double-scheme `https://https://…` dead CTA is gone. Matches the `notify_application_scored` precedent. Grepped: no scheme-full origin feeds `build_entity_url` on any reference path.
- **W2:** `apply_decline` truncates `decline_reason` via `string.slice(0, 200)` (grapheme-correct; identical to the private `application_handler.truncate`).
- **W3:** AC7 honeypot tests on all 4 exit POSTs. `honeypot_filled_stop_post_does_not_object_test` asserts the **row stays `contact_initiated` AND `objection_log_count == 0`** (the critical "fake success must not object" branch is genuinely pinned).
- **W5:** all 4 audit terminal events pinned (`reference_call_completed/declined/objected/wrong_person`).
- **W6:** advisory gate PASS — every new test asserts real DB row/evidence state.
- **N1/N2/N3/N5/N6:** folded — character `free_text_signals` emitted; `headline` dead arm collapsed; distinct truthful `view_objected()` page (rc3-3 `terminal_rows` test correctly tightened to `reference-objected`); CSRF test tightened to `{200}` reachability with fresh live rows; channel CHECK bite-tested (`web` ok / `telegram` rejected).
- **Deferred notes hold:** N4 (completion_seconds → rc3-7), N7 (focus clamp — no consumer), N8/N11 (purge_after/evidence atomicity — verified no sweep touches `reference_call`), N9 (discarded dispatch Result — mitigated by W4 pin), N10 (enum drift, inert), N12-N14 (lower-risk coverage).

### 🚫 Blockers (1)

**B2-r2 — W1's fix is INERT: the review form's `_focus_seconds` is never populated by client JS, so `focus_seconds_reported` is still always 0 in production (still present since r1); the new flow test masks it.**
`server/src/reference_checks/form_pages.gleam:236-243` + `server/priv/static/reference_form.js:70-71,152-158,202-204` — caught by **6 independent lenses** (blind, edge, acceptance, security, architecture, codebase).

The HTML field was added to `view_review` (good), but `reference_form.js` never fills it:
- `initBrowser` does `var page = doc.querySelector("[data-testid='reference-form-page']"); if (!page) return;` — the review page is `data-testid="reference-review"`, so **`initBrowser` bails immediately** and no JS runs on the review page at all.
- `onSubmit` (the only writer of `[data-focus-seconds]`) is attached **only** to forms inside `.ref-question` sections (`questions.forEach(... form.addEventListener("submit", onSubmit)`) — the review form is not one, and even if it were, `onSubmit` bails on `form.closest(".ref-question")` returning null.

So a real browser submits the hardcoded `value="0"` → `focus_seconds_reported` is structurally still always 0 (the exact r1 W1 defect). The new `focus_seconds_reported_flows_into_the_result_test` POSTs `#("_focus_seconds", "240")` directly via `simulate.form_body`, **bypassing the browser entirely** — it proves the server-side plumbing (`parse_focus_seconds` → result), not that a real referee ever sends a non-zero value. The test provides false confidence that the bug is fixed.

This is a must-resolve in a fix-audit: a claimed fix that is verifiably inert, concealed by a test that bypasses the broken path, would ship a known-broken fraud signal plus a misleading test.

**Fix (small, well-scoped):** in `reference_form.js`, attach a submit listener to `[data-testid='reference-review-form']` that sets its `[data-focus-seconds]` field from the running focus accumulator (hoist `currentFocusSeconds` above the `.ref-question` bail; persist the accumulator across review navigation, e.g. via `sessionStorage`), **without** `preventDefault` (the native POST must proceed). Extend the existing `node --test` wiring seam to cover it. (Also resolves the N7 deferral's "crafted-POST-only" caveat once a real value flows.)

### Notes (6)

- **N15 (dev-only):** B1's `build_entity_url` hardcodes `https://`; a dev vacancy's `origin_domain` is `localhost:4000`, so terminal-notification CTAs become `https://localhost:4000/…` (dead against the local http server) while the invite email stays `http://` (via `origin_from_domain`). **Production unaffected** (origin is always `righttenantry.ie` → correct https). Suggest special-casing localhost in `build_entity_url`, or document the divergence.
- **N16 (defense-in-depth):** `build_entity_url` interpolates the raw `origin_domain` with zero checks. No open-redirect/SSRF today (write-time `validate_origin_domain` allow-list + fixed UUID path + `escape_html` + never fetched server-side), but a future writer storing a crafted domain would ship phishing CTAs. Suggest an allow-list check at interpolation time.
- **N17 (consistency):** the N3 objected-routing branch matches the raw `row.status == "objected"` string instead of the typed `status_from_string` parser `classify_row` uses in the same file. Functionally safe (the Declined arm admits only refused/objected), but adds a second untyped status mapping. Suggest `match status_from_string(row.status) { Objected -> … }`.
- **N18 (coverage):** B1 has no test pin — the `https://https://` CTA bug would regress silently (notification tests assert type/body, not the CTA URL). Low risk (verified by reading; email payload not testable without an SMTP mock). Cheap to pin with a `build_entity_url` unit test on a raw domain.
- **N19 (coverage):** W2 truncation has no test pin — no test POSTs a >200-char `decline_reason`. Cheap to pin: POST a 250-char reason, assert stored `result->>'decline_reason'` is 200 chars.
- **N20 (coverage):** N1's character `free_text_signals` is emitted but the character result test wasn't extended to assert the empty array. Additive, low risk.
- **W4 (partial, carried):** completed notification row + late-after-handoff "after all" copy are pinned; declined/objected notification rows are not (they share the `notify_reference_event` wrapper exercised by the completed pin — low risk).

**Verdict: NEEDS CHANGES**

B1 (the real production blocker) is genuinely fixed on all paths, and W2/W3/W5/W6 + N1/N2/N3/N5/N6 are properly resolved — that's the bulk of r1. But W1's claimed fix is verifiably inert: the `_focus_seconds` field ships in the HTML with no client wiring, so the r1 defect persists unchanged, and the flow test masks it by bypassing the browser. Completing the `reference_form.js` wiring (small, well-scoped, with a node test) resolves it and this is ready.

---

Address the findings and push a new commit; a fresh round will follow.
