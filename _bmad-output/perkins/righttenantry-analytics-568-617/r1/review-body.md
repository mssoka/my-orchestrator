## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantry-analytics-568-617 · **Reviewed sha:** `bdfc620` · **Reviewers:** 7/7 completed
**Verification:** 16/17 findings confirmed against the code — 1 discarded as false-positive

**Round's hard gate — Meta CAPI fire-once + consent gating: HOLDS.** `dispatch_signup_meta` fires only on `row.is_new=True` (the upsert's atomic `xmax = 0` insert signal) and gates internally on `consent_check.marketing_granted(req)` (`auth_handler.gleam:1513-1542`) — the OAuth path inherits the Plan §5 consent gate by calling the same function as the password path. Returning sign-ins (`is_new=False`) fire nothing even with consent. No browser Pixel fires on the OAuth path (Pixel `CompleteRegistration` exists only in the password signup response handlers via the echoed `meta_event_id`), so CAPI alone carries the event — no CAPI+Pixel double-fire. The #617 cookie lifecycle (set-if-params at initiate → read at callback → cleared on all 8 terminal responses) and the recorded auto-create backfill decisions were verified in code. Baseline #583 behavior is structurally untouched.

### Blockers (0)

None.

### Warnings (3)

1. **Organic re-initiate leaves a stale first-touch cookie readable by the next callback** — `auth_handler.gleam:1002-1015` [edge, codebase]. Attempt 1 (paid landing) sets the cookie; the user abandons at Google (no callback → no terminal clear); a second *organic* initiate within the 300s window hits the `[] -> response` branch, which neither overwrites nor clears — the callback then `$set_once`-locks the abandoned attempt's params, contradicting the module's documented "no cookie → `provider=google`" guarantee. *Fix:* apply `first_touch_cookie.clear_cookie(response, req)` on the `[]` branch too, so every initiate is set-or-clear.
2. **The "~4KB header budget" clamp is grapheme-based, not byte-based** — `attribution.gleam` `clamp_value` [blind]. Verified against stdlib: `string.slice` slices grapheme clusters and `uri.query_to_string` percent-encodes each UTF-8 byte to `%XX`. Eight keys × 200 four-byte graphemes ⇒ ~19KB encoded — browsers silently drop the oversized Set-Cookie and attribution is lost (graceful `provider=google` fallback; analytics-only impact). *Fix:* clamp by encoded byte length before `cookie_value()`, or scope the doc claim to ASCII.
3. **The client wiring `UserClickedGoogleSignIn` → initiate-URL query has no test** — `client.gleam:2038-2053` [tests]. Server boundary and `to_query_string` are pinned, but the only link that moves `model.first_touch_params` onto the URL is untested; a regression silently re-ships the exact bug this PR fixes. The `client.update` harness exists. *Fix:* two small update tests (params present → query string; empty → `None`).

### Notes (10)

1. **`find_set_cookie` helper now duplicated across six test files** — [blind, codebase]. Three copies pre-date this diff (`cookie_attributes_test`, `csrf_cookie_test`, `external_id_cookie_test`), so the three new ones follow the established per-file convention. Leave as-is; extract a shared helper if a seventh appears.
2. **Initiate test never asserts the cookie is actually signed** — `auth_test.gleam` [blind]. Name-prefix + `Max-Age` assertions pass identically for a `wisp.Plain` cookie, while `read_cookie(Signed)` would silently return empty in production. *Fix:* assert the value contains no `utm_` substring (or round-trip decode it).
3. **`set_once_with_fallback` doc overstates the no-op** — `first_touch_cookie.gleam:96-97` [blind]. Pre-deploy OAuth accounts locked an *empty* `$set_once`, so their next sign-in writes `provider=google` (deliberate backfill per the PR body) — only the doc comment misstates it.
4. **Attribution-poisoning surface on the public initiate endpoint** — [security]. A crafted cross-site link to `/auth/oauth/google?utm_…` persists attacker params (top-level navigation = first-party Set-Cookie context), locked into a first-time Google signup's `$set_once`. Impact is attribution corruption only (allow-listed, clamped, signed); the class pre-exists via crafted landing URLs (#466). *Fix:* accept-and-document, or require `Sec-Fetch-Site: same-origin` before persisting.
5. **`provider=google` is hardcoded in a provider-agnostic flow** — `first_touch_cookie.gleam:102` [architecture]. Correct only while `allowed_oauth_providers = ["google"]`; thread the provider through if a second one is ever added.
6. **`first_touch_cookie.max_age` (300) mirrors `pkce_max_age` (300) by comment only** — [architecture, codebase]. Reference one shared constant so the two windows can't drift.
7. **Attribution key list triplicated** (client extractor, `signup_decoder`, `first_touch_cookie.keys`) with no enforced sync — [architecture]. A decoder-only key addition would silently drop OAuth attribution for it; a shared server const + sync test would pin it.
8. **Error-branch `clear_cookie` calls untested in situ** — 8 call sites, only success path + unit pinned [tests]. P3; acceptable as-is.
9. **Auto-create log-line changes untested** — log-only, settled decision [tests]. Ship as-is.
10. **Advisory test gate: PASS** — P0 100% (fire-once + consent gate integration-pinned), P1 100%, overall ≈83% [tests].

### Reviewer agreement

Three findings were independently reported by two lenses each: the stale-cookie gap [edge + codebase], the `find_set_cookie` duplication [blind + codebase], and the `max_age` mirror [architecture + codebase].

**Rejected as false-positive (1):** "dispatch_signup_meta called with `row.id` violating the fresh-event_id contract" — the third parameter *is* the landlord UUID by signature (`auth_handler.gleam:1513-1518`); the per-event `event_id` is generated inside the function. The test comment is accurate.

### ⚠️ CI caveat (not a code signal)

The PR's only CI run failed at infrastructure level: no runner was ever assigned to any of the 4 jobs (0ms durations, zero steps executed). This needs a **rerun** before merge — it says nothing about the diff.

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
