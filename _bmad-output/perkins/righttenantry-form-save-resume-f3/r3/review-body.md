## 🤖 Perkins automated review — round 3 of 3 (FINAL)

**Job:** righttenantry-form-save-resume-f3 · **Reviewed sha:** `8789054` · **Reviewers:** 7/7 completed (3 chunks × 7 lenses)
**Verification:** 23/23 findings confirmed against the code — 0 discarded as false-positive

### Round-2 fix audit (re-review)

**All 3 claimed fixes verified — including the blocker, empirically.** r2-**B1** (detached `window.setTimeout`): both timer call sites now wrap the host functions, and I re-verified the production seam in Chromium (deferred script, `env=window`, real `rt:form-step-changed` dispatch): the debounce schedules, coalesces, and one save POST fires with zero errors. The brand-checked-timers wiring pin is real. r1-**N14** (sent-flag oracle): `json_ok_with` deleted, uniform `ok:true`, and the integration test now pins that the body must NOT contain `sent` — the honest overturn is correctly implemented. r1-**N1** (POST-vs-PUT drift): spec text corrected to match the code.

**Still present since round 2** (unchanged in this delta, carried into triage below — not double-counted): all 10 round-2 warnings (W1 wholesale-wipe, W2–W6 abuse-bound gaps, W7–W10 coverage pins) and all 26 round-2 notes, plus 9 carried round-1 notes (the deferred refactors, r1-N8/N11/N12/N15/N18/N22/N27).

### Blockers (1)

**B1 · PostHog autocapture leaks the raw `data-resume-token` past the `sanitize_properties` scrub** (edge) — `form_view.gleam:269` + `form_pages.gleam:401`
The resume render puts the raw 288-bit continue token on `<body data-resume-token>` — a read-capability for applicant PII. `posthog.init` leaves **autocapture at the SDK default `true`** (no key in the config; I confirmed the default empirically). Verified against posthog-js 1.409.5 source (the version the loader ships): the autocapture element chain walks ancestors **up to and including `<body>`** and captures every attribute of non-sensitive elements as `attr__<name>`. So any consenting applicant's click on the resume page emits an `$autocapture` event whose `$elements_chain` contains `attr__data-resume-token="<token>"`. The scrub regex only redacts tokens preceded by a literal `/resume/` or `/draft-erasure/` segment — the attribute value is the bare token, so it ships to the analytics store **unredacted**, flatly violating the feature's own stated invariant ("the token must never land in the analytics store").
**Fix:** disable autocapture on the apply-form pages (the funnel is all custom events) or `element_attribute_ignorelist:['data-resume-token']`; extend the scrub + strengthen its test (see N12) as belt-and-braces.

### Warnings (1 new + 10 carried)

1. **W1 · 413 envelope lacks `ok:false` — continue-link UI reports "Link sent" on a rejected request** (codebase+edge) — `middleware.gleam:582` + `form_draft.js:309`. The body-size 413 (`{"error":{...}}`) parses fine and has no `ok` key, so `body.ok === false` is false: the UI shows "Link sent — check your inbox", sets `lastSentPayload` (suppressing the beacon retry), and fires a phantom `application_draft_saved` — though nothing was saved or emailed. Reachable: no `maxlength` on any input; ~40 free-text fields can exceed the 64 KB cap. **Fix:** add `ok:false` to the 413 envelope or check `res.ok` before parsing.
2. *Carried from round 2:* W1 blank-form wholesale-wipe of a rich prior draft · W2 fan-out counts stamped rows not sends (~4–6× overshoot) · W3 500-cap counts stripped+tombstoned rows · W4 cap-blocked save silently `ok:true` · W5 fan-out check-then-act race · W6 plus/dot alias bypass · W7–W10 coverage pins (resume start-step wiring, claim guards, loader inclusion, r1-B1 origin fix).

### Notes (12 new + 35 carried)

New: brand-check pin never exercises the wrapped `clearTimeout` seam (acceptance+blind+tests — half the B1 fix regresses green) · no-oracle doc overclaims `ok:false` "only when the Resend call failed" (upsert-abort also returns it) · upsert-abort 200-vs-500 inconsistency with the save path · `strip_draft_on_submit` manually SETs `updated_at` despite the migration's stated trigger convention (architecture+blind+codebase) · `keepalive` fetch throws synchronously >64 KiB, escaping the promise chain · spec task schema omits `erased_at` · spec "skip hidden" claim has no code arm · fixture comment describes the never-rented branch the fixture doesn't drive · two spec code anchors point at the wrong lines · byte-identical `fakeTimers()` duplicated across the two new JS test files · stage-2 reminder prefetch→continue-url mapping unpinned · token-scrub test asserts substring presence only (the replacement that actually redacts is unasserted).
Carried: 26 round-2 notes + 9 round-1 notes (deferred refactors, acknowledged trade-offs, unpinned wiring).

### Reviewer agreement

413-envelope `ok:false` (codebase+edge) · brand-check clear-seam gap (acceptance+blind+tests) · no-oracle doc overclaim (acceptance+blind) · strip `updated_at` convention drift (architecture+blind+codebase). Advisory test gate: **PASS** in all 3 chunks.

**Verdict:** NEEDS CHANGES

The round-2 blocker is genuinely, verifiably fixed — but this round found a new one: the F3 scrub defends the token in URLs while autocapture carries it out through the DOM attribute channel. One-line config fix; the human takes over from here.

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
