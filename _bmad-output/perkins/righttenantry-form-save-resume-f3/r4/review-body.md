## 🤖 Perkins automated review — round 4 of 3 (user-overridden cap — advisory; the human merges)
**Job:** righttenantry-form-save-resume-f3 · **Reviewed sha:** d3f7700 · **Reviewers:** 21/21 lens-runs completed (7 lenses × 3 chunks, diff 5,479 lines)
**Verification:** 59/61 raw findings confirmed against the code — 2 discarded as false-positive; 3 advisory gate findings kept as notes

### Round-3 fix audit (first)

**r3-B1 (blocker, PostHog autocapture leak) — FIXED, verified across every capture path.** `data-resume-token` is gone from the DOM (zero attribute sites); the token now rides `window.__rtResumeToken` via a CSP-nonced inline script (nonce replaced globally by `middleware.inject_csp_nonce`). Token charset confirmed URL-safe base64 (`wisp` internal: `strong_random_bytes |> base64_url_encode(False) |> slice`) — no script/string breakout possible. `sanitize_properties` grew the recursive key-scrub (`/resume-token/i` at any depth covers `attr__data-resume-token`; URL strings still scrubbed). Custom events carry only `{vacancy_short_code}`; the token leaves the page only in first-party JSON POST bodies. Regression pins now assert the JS global **and** the attribute's absence (`form_pages_test.gleam:331-336`, `draft_integration_test.gleam:310-315`).

**r3-W1 (413 false "Link sent") — FIXED** via the recommended client-side arm: the click chain checks `!res.ok → {ok:false}` before parsing; phantom sent-state and phantom `application_draft_saved` are closed.

**r3-N1 (clearTimeout seam) — FIXED**: the brand-check pin now re-triggers under brand-checked refs and drives pagehide-cancel with a pending timer.

r3's 11 notes and all 45 carried r2/r1 items verified still present (r3→r4 delta touched none of the cited sites; spot-verified).

### Blockers (0)

None. 🎉

### Warnings (3 new)

1. **Round-3 W1's fix branch has no pinning test** — `form_draft.js:313-317`. Every wired failure test uses an HTTP-ok response; the `!res.ok → {ok:false}` branch that fixed the 413 misrender is never driven. Reverting it ships green. *[tests]*
2. **Post-submit save/beacon can INSERT a fresh live draft** — `upsert_application_draft.sql:11-18`. The submitted/erased guards only fire on the ON CONFLICT branch; an applicant who edits their email after the last save and submits inside the debounce window gets a fresh PII-bearing draft row + live token INSERTed by the post-submit beacon — defeating the strip contract ("the application row becomes the system of record"). Retention sweep backstops at vacancy close. *[edge]*
3. **Negative-input arms on the public draft endpoints untested** — malformed-JSON→400 (both endpoints), invalid-email→400 on `/continue-link`, unknown-code→404. Only the `/draft` invalid-email twin is pinned. *[tests]*

### Notes (20 new + 56 carried)

New: stale `data-resume-token` references (spec :129/:261 + `draft_handler.gleam:435`) · `Promise.finally` outside the capability gate (3 lenses) · 413/over-cap saves retry forever · copy-pin test covers only the JS half · beacon ack-dedupe unpinned · strip doesn't clear `last_link_sent_at` · send-failure clear drops the fan-out count · strip ordered before file-resolution · resume skips `max_applications` gate · session recording not explicitly disabled on the token page · handler→handler import · no handler-level body-cap pin · `file_slot_names` pub-unused · third token-404 view · unknown-email enumeration path untested · 120-cap truncation order · exact cap boundaries · 10-minute cooldown boundary · F3 pages pin no cache/referrer/robots headers · third submission-fixture copy.

Carried (still present since rounds 1–3, not double-counted): r2-W1..W10, r2-N1..N26, r3's 11 notes, 9 round-1 notes — all re-verified this round.

### Reviewer agreement

- `Promise.finally` missing from the capability gate (blind+edge+codebase — 3 reports)
- Carried r2-N2 migration header misstates erasure/token-mint (4 lenses)
- Carried r2-W4 cap-blocked upsert answers `ok:true` (blind+edge)
- Carried r1-N22 `draft_field` unwrap false-pass (blind+edge)
- Carried r3-N11 stage-2 reminder mapping untested (tests-c2 graded **blocker**, tests-c3 note — adjudicated as carried note: code unchanged since r3, failure mode degrades to the plain pre-F3 CTA, both ends pinned; dissent recorded)

**Rejected as false-positive:** "upsert doesn't bump updated_at" (the `update_application_draft_updated_at` BEFORE UPDATE trigger fires on every save — migration :60-64) · "test_db helpers missing" (`seed_closed_vacancy`/`seed_archived_vacancy` exist at `test_db.gleam:508,533`).

**Verdict:** READY TO MERGE — round 3's blocker and warning are verifiably fixed; nothing new rises above warning. The 3 warnings and the carried inventory remain for the human's merge decision.

_This was a user-requested extra round — the round cap stays 3 elsewhere. My verdict is advisory; the human merges._
