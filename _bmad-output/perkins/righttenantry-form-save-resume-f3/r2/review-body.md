## 🤖 Perkins automated review — round 2 of 3

**Job:** righttenantry-form-save-resume-f3 · **Reviewed sha:** `11fcaa3` · **Reviewers:** 7/7 completed (3 chunks × 7 lenses)
**Verification:** 61/62 findings confirmed against the code — 1 discarded as false-positive (a claim that landlord/character co-applicant upload slots exist; they don't)

### Round-1 fix audit (re-review)

**28 of 39 round-1 findings verified FIXED by direct read** — including blocker **B1** (emailed capability URLs now build from `vacancy.origin_domain` via `email_client.build_entity_url`, never the request origin), W1 mint-at-save, W2 wiring tests, W3 erasure tombstone, W4 close-only sweep, W5 draft cap, W6 fan-out bound, W7 real `handle_post_form` strip test, W8/W9 coverage, W10 slot filter, W11 guard pin, and 16 notes.

**11 still present since round 1** (all notes, several acknowledged in the spec change log): N1 POST-vs-PUT drift (the spec task list now *also* falsely claims "fetch PUT"), N6/N7 deferred refactors, N8 test-name half, N11 human open-and-close resume-stamp (rebuttal covers only mail scanners), N12 "accepted" but not documented, N14 sent-flag oracle — the "upsert-first" rebuttal is wrong: an empty-fields poll skips the upsert, so `sent:true` still flips to permanent `sent:false` on victim submit, N15 lookup-doc half, N18 wiring half, N22 helper footgun, N27 abort branch.

### Blockers (1)

**B1 · Detached `window.setTimeout` breaks the debounced save in every real browser** — `server/priv/static/form_draft.js:231`
Production auto-init calls `initBrowser()` with `env=window` (the script is deferred), so `createDebounced` receives `{ set: env.setTimeout, clear: env.clearTimeout }` — **detached** references invoked with `this={set,clear}`. I verified this empirically in Chromium: it throws `TypeError: Illegal invocation` and the timer never schedules. Every `rt:form-step-changed` therefore throws inside the listener, and the debounced save — the feature's core mechanism and a frozen AC — **never fires in production**; only the pagehide beacon (no timers) persists drafts. Node tests can't catch it: Node's `setTimeout` is not brand-checked and the wiring test injects fake timers.
**Fix:** wrap at the call site — `{ set: function(fn,ms){ return env.setTimeout(fn,ms); }, clear: function(id){ env.clearTimeout(id); } }` — and pin the production seam in the wiring test.

### Warnings (10)

1. **W1 · Fresh-session blank form wholesale-wipes a rich prior draft** (edge) — `form_draft.js` serializer emits every untouched control as `""`; a returning applicant (saved day 1, no link) who re-enters their email and changes step replaces day-1's answers with ~40 empty strings (`ON CONFLICT SET fields = EXCLUDED.fields`). Send only dirty fields, or merge jsonb server-side.
2. **W2 · Fan-out bound counts stamped rows, not sends** (security+blind) — repeat sends re-stamp the SAME row, so one draft sustains 6 emails/hr, two vacancies 12/hr; "max 3/recipient/hour" is overshot ~4×.
3. **W3 · 500/vacancy cap counts stripped + tombstoned rows** (blind+security+tests+edge, 5 reports) — no `submitted_at/erased_at` filter; ~500 *lifetime* applicants (organic or attacker aliases) permanently wedge save-and-resume for the vacancy.
4. **W4 · Cap-blocked save answers `ok:true`** (blind+edge+security) — zero-row upsert maps to success; applicants lose answers silently and the funnel counts phantom drafts.
5. **W5 · Fan-out bound is check-then-act** (edge+security) — concurrent cross-vacancy claims all see the pre-burst snapshot and all send.
6. **W6 · Plus/dot aliases defeat the per-recipient bound** (security ×2) — `victim+1@gmail.com … +N` are N distinct recipients to the bound but one inbox.
7. **W7 · Resume start-step wiring unpinned** (tests) — reverting the `form-resume → firstIncompleteIndex` ternary fails no test (frozen AC).
8. **W8 · claim's `submitted/erased` zero-row guards unpinned** (tests) — the only lines stopping a tombstoned/stripped row winning a claim + real email.
9. **W9 · `form_draft.js` script-tag inclusion unpinned on pristine + error renders** (tests) — deleting it kills the feature with all tests green; only the resume render is pinned.
10. **W10 · The round-1 blocker fix (B1 origin) has zero automated pin** (tests) — reverting to `canonical_origin` fails no test; `build_entity_url` untested.

### Notes (26)

Bootstrap/Event-as-env (latent under `defer`) · migration header still claims lazy-mint + row-removal erasure (blind+architecture+acceptance+codebase+edge) · spec review-order still says sweep covers archived · closed-mid-session UI keeps promising saves + misreports deterministic continue failure as transient · client-plausible/server-invalid email saves 400 silently forever · 500-cap race overshoot · `resumed_at` stamp asymmetry (save vs continue-link on empty fields) · dead COALESCEs · DuplicateApplication branch never strips a coexisting live draft · slot whitelist re-encoded from `document_upload` (architecture+codebase) · SSR vacancy+draft preamble triplicated · 5 orphan `form_copy` draft consts · W9 test asserts only absence of resume markers (never the `closed-vacancy-notice`) · tombstone keeps plaintext email (deliberate — sign off consciously) · TE body-size rejection still POST-only · erasure GET confirm on forged token unpinned · seed helper's redundant UPDATE (blind+architecture) · `list_resumable` missing the `erased_at` guard · new token endpoints lack the Cloudflare per-IP rule `/erase/`/`/dsar/` have · no router-level pins for the 4 draft routes (`/erase` sibling has them) · `vacancy_short_code` helper ×3 · alias-wrapper style drift · fan-out 1-hour window value unpinned · empty-fields guard unpinned on the continue-link path · dirty-retry unpinned · `updated_at` trigger unfired-test.

Full detail, evidence, and per-finding fixes: `consolidated.json` in the round dir. Advisory test gate: **PASS** (P0 100%, P1 ~93–95%) in all 3 chunks.

### Reviewer agreement

Cap counts dead rows (4 lenses, 5 reports) · cap-blocked silent `ok:true` (3 lenses) · fan-out race (edge+security) · migration-header staleness (5 lenses) · fan-out counts-rows-not-sends (security+blind) · slot-whitelist duplication (architecture+codebase) · closed-page assertion gap (blind+codebase).

**Verdict:** NEEDS CHANGES

Round 1's blocker is genuinely fixed — but the new round-2 hunk introduced a production-only break of the feature's core save mechanism (B1), and the W5/W6 abuse bounds from round 1 don't deliver their documented invariants (W2–W6). The blocker is a two-line fix with a wiring-test pin; W3/W4 share one SQL statement.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
