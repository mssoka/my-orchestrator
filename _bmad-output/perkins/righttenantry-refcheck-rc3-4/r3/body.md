## 🤖 Perkins automated review — round 3 of 3 (fix-audit, FINAL)

**Job:** righttenantry-refcheck-rc3-4
**Reviewed sha:** `9fddf2c` (r2 was `8c9c87e`, r1 was `13ae750`)
**r2 audit:** **B2-r2 FIXED** · W4-partial **remains** (low-risk note, unchanged from r2 — JS-only delta didn't touch notification tests)
**Reviewers:** 7/7 completed (blind, edge, acceptance, security, architecture, codebase, tests) — 0 failed
**Verification:** 3/3 reviewer findings survived code re-verification · 5 lenses returned clean `[]`

---

### The load-bearing verification (r2 blocker B2-r2) — PASSED

The r2 blocker was that W1's fix was **inert**: the review form's `_focus_seconds` shipped in the HTML but `reference_form.js` never populated it (`initBrowser` bails on the review page; `onSubmit` binds only `.ref-question` forms), so `focus_seconds_reported` was still always `0` in production — and the r1 flow test masked it via `simulate.form_body`.

**Proven by code trace this round (not claims):**

1. **Binds the review form's submit.** `initReviewSubmit` does `doc.querySelector("[data-testid='reference-review-form']")` → `form.addEventListener("submit", fn)`. The rendered HTML matches: `form_pages.gleam view_review` emits `attribute("data-testid", "reference-review-form")` (line 228).
2. **Populates `_focus_seconds` from the page clock.** `form.querySelector("[data-focus-seconds]").value = clampFocusSeconds(env.Date.now() - initMs)` — the **same** `clampFocusSeconds` (`Math.floor(ms/1000)`) the per-question `onSubmit` uses. HTML matches: lines 240–242 emit `attribute.name("_focus_seconds")` + `attribute("data-focus-seconds", "")`.
3. **Does NOT `preventDefault`.** The listener is `function () {` — no event parameter, no `preventDefault()` anywhere. The review submit stays a native POST (AD-3 no-JS degradation intact).
4. **Wired into both init paths** (DOMContentLoaded + immediate `readyState`) alongside `initBrowser`, and exported as `_initReviewSubmit` for testing.

**The 4 Node tests drive the browser path — NOT a `simulate.form_body` mask (the r2 lesson, honored).** Each calls `referenceForm._initReviewSubmit(env)` then invokes the seam's bound listener (`t.reviewForm._onSubmit(...)`) with a fake DOM + mutable clock: (1) 8s → `"8"`, (2) native POST not prevented (`event.prevented === false`), (3) off-page no-op, (4) 5999ms → `"5"`. The fake-DOM selectors match the real HTML contract. The r1 **server-side persistence pin still coexists** (`server/test/integration/reference_exit_routes_integration_test.gleam:652` `focus_seconds_reported_flows_into_the_result_test` — POSTs `240` via `simulate.form_body`, asserts `focus_seconds_reported = "240"`); neither test replaced the other.

6 of 7 lenses independently confirmed this (5 returned `[]`; the `tests` lens returned advisory-gate **PASS**).

### Lens-guards still held (delta is purely additive JS — server invariants untouched)

Objection stickiness (AD-6/14), evidence-log single-writer (channel `web`), deterministic result (AD-9), one-submission (AD-3), registry prefix-match + router arms, B1's raw-origin fix on all notification paths, em-dash ban — all **CONFIRMED untouched** by the r2→r3 delta (zero Gleam/server/middleware/router/notification changes).

**Suite (re-run at `9fddf2c`):** `make test-js` 136 pass / 0 fail (incl. the 4 new at 133–136) · `make test` 1418 unit pass / 0 fail / 460 skipped (integration, no Docker) · Gleam build clean. *(`make build`'s `make tailwind` step fails only because the `tailwindcss` binary isn't on PATH in this worktree — a local-env artifact, not a code regression; the delta is JS-only.)*

---

### Blockers (0)

None. B2-r2 is fixed; all prior blockers resolved.

### Warnings (0)

None.

### Notes (2) — optional test-quality hardening, non-blocking

- **N21-r3** *(blind; filed as warning, lead-downgraded to note)* — `scripts/js-tests/reference_form_wiring.test.js:305` *"initReviewSubmit is a no-op off the review page"* has **zero explicit assertions** — it only proves no-throw. Impact is lower than filed: the seam's `if (!form) return` bail means a removed guard would throw on `null.addEventListener`, so the no-throw is an *implicit* defense, and the load-bearing contracts are pinned by the other 3 tests. Optional: assert `addEventListener` was never invoked (spy counter). Ship-blocking: no.

- **N22-r3** *(blind)* — `scripts/js-tests/reference_form_wiring.test.js:312` title *"floors to whole seconds **and never goes negative**"* overpromises — the body only exercises the positive `5999ms → "5"` case. Cosmetic only: the negative/NaN/Infinity floor **is** pinned at the pure-function level in `scripts/js-tests/reference_form.test.js:38-41` (`clampFocusSeconds(-50)='0'`, `NaN='0'`, `Infinity='0'`). Optional: trim the title or add a backward-clock case. Ship-blocking: no.

**W4-partial (carry-forward from r2):** declined/objected notification rows remain unpinned (share the `notify_reference_event` wrapper exercised by the completed-row pin). JS-only delta didn't touch it; same low-risk note as r2.

---

### Verdict: READY TO MERGE ✅

The r2 blocker is genuinely fixed (code-trace + 6/7 lenses), the 4 tests drive the real browser path (not a mask), the delta is purely additive JS with every server-side invariant untouched, and the suite is green. 0 blockers, 0 warnings → **approving**.

This was the **FINAL automated round (3 of 3)** and it is clean — no human hand-off is required.

Address the 2 notes opportunistically (a future commit is fine); they don't block this merge. Nice work closing the W1-inert loop properly this time — the browser-path test discipline is exactly the r2 lesson applied.
