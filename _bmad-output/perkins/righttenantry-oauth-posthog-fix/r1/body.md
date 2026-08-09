## 🤖 Perkins automated review — round 1 of 3
**Job:** righttenantry-oauth-posthog-fix · **Reviewed sha:** b9882fa · **Reviewers:** 7/7 completed
**Verification:** 6/6 findings confirmed against the code — 0 discarded as false-positive

### Blockers (0)

### Warnings (2)
1. **Reset-arm guard pin is not unique** — `Makefile:274`, `Dockerfile:133` · The new grep pin `document.cookie="rt_landlord_id=; Max-Age=0; Path=/; SameSite=Lax";rtPhId=null` also matches the **pre-existing consent-reject arm** (`opt_out_capturing();document.cookie="rt_landlord_id=...";rtPhId=null`), so deleting only the new reset-arm clear would still pass both build guards. The regression the guard claims to defend (stale landlord re-identify after logout inside the 60s window) is not actually pinned. **Fix:** pin the reset-arm adjacency, unique to that arm — `rt_ph_reset=; Max-Age=0; Path=/; SameSite=Lax";document.cookie="rt_landlord_id=` — in both guard lists (verified to occur exactly once per chain).
2. **Advisory test gate: CONCERNS** — P0 100% (both `is_new` polarities integration-tested against the real DB, identify/capture asserted, cookie Max-Age pinned in unit tests), P1 ~80% overall: the reset-arm snippet change has no regression test that would fail, for the same pin-uniqueness reason. Resolves with warning 1; optionally add a bug-hunt assertion that `rt_landlord_id` is absent right after logout.

### Notes (4)
- **`xmax` is PG-internal** — `create_landlord_oauth.sql` · `(xmax = 0) AS is_new` is the canonical atomic insert-vs-update idiom and the comment documents the semantics, but the caveat that it's a PG implementation detail (re-verify on a Postgres major upgrade) could be stated.
- **OAuth email → PostHog, consent-independent** — `auth_handler.gleam:1128` · Mirrors the in-production email/password posture exactly (documented precedent); disclosed in the code comment. Recorded for the privacy record, not a deviation.
- **`identify_with_set_once` with an all-empty `FirstTouch`** — `auth_handler.gleam:1128` · Behaviorally `identify/3` (empties are filtered to `[]`), slightly against the module's own "prefer `identify/3`" guidance; deliberate, documented mirror of the signup-path call shape.
- **`complete_oauth_flow` made `pub` for tests** — `auth_handler.gleam:1077` · Widens the in-process session-forgery boundary below the PKCE exchange; not HTTP-reachable, monolith, no test-visibility in Gleam, doc-mitigated. Acceptable.

### Reviewer agreement
The guard-pin warning was reported independently by **all 7 lenses** (blind, edge, acceptance, security, architecture, codebase, tests) — highest-confidence signal in this round, and the only warning with code impact. Everything else is single-lens or documented-limitation noise.

### Verified sound (the load-bearing surfaces)
- `(xmax = 0) AS is_new`: canonical atomic insert-vs-update signal (no TOCTOU); codegens to `Bool` at field 11; polarity correct (`True → signup_completed`, `False → login_succeeded`); both polarities exercised by `oauth_first_signin_fires_identify_and_signup_completed_test` / `oauth_returning_signin_fires_login_succeeded_test`.
- 4-place snippet contract: reset-arm clear present in **both** Makefile and Dockerfile perl chains **and** both guard lists (the code is right everywhere; only the pin's uniqueness is wrong).
- Cookie contract: `rt_landlord_id` 60s, both sentinels 10s, all setters on the right attributes, no stragglers of the old `bridge_cookie_attributes`.
- Identify/capture shape: mirrors the signup path (`identify_with_set_once` + capture, consent-independent by the same documented precedent); `process_login` confirmed to identify-only, so the OAuth-scoped `login_succeeded` disclosure is accurate; anonymous→identified merge link (cookie) preserved.
- Disclosed follow-ups (cross-provider `login_succeeded`, no first-touch on OAuth, cross-provider returning = new signup) are documented in code, not contradicted by the implementation.

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
