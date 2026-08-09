## 🤖 Perkins automated review — round 1 of 3
**Job:** righttenantry-refcheck-rc3-1 · **Reviewed sha:** `2a2b063` · **Reviewers:** 7/7 completed
**Verification:** 9/11 findings confirmed against the code — 0 discarded as false-positive (2 pairs were duplicates merged into reviewer-agreement findings)

### Blockers (0)

### Warnings (4)

1. **[config] `init()` enables the client without `TWILIO_STATUS_CALLBACK_BASE_URL`, contradicting T1.2's four-required-keys spec and AC1's StatusCallback contract** — `server/src/notification/sms_client.gleam:74-87` — [blind, acceptance]. T1.2 lists the base URL among the four required keys and says `Disabled` when any is absent; AC1 mandates a StatusCallback URL on every send. The code checks only sid/token/alpha_sender and stays `Enabled` with an empty base URL, so sends omit `StatusCallback`. The code documents the choice, but the spec was never amended — either require the key in `init()` (return `Disabled` when absent) or amend T1.2/AC1 to mark the callback conditionally optional.
2. **[data-exposure] Lookup failure messages embed the raw applicant phone number (PII) into Sentry** — `server/src/reference_checks/lookup.gleam:69,85-86,92-93,101` — [security]. Every lookup failure writes the full E.164 phone into the Sentry message; AC5's stated context is status/error-kind/endpoint tags. Codebase precedent (`reference_checks/trigger.gleam`) captures `app_id`, not raw PII, and `truncate_message` only caps length, it does not redact. In a GDPR-heavy app, redact the phone in Sentry messages (e.g. last 4 digits) and keep the full number in local logs only.
3. **[coverage-gap] `build_lookup_request` is `@internal` exposed for tests but has no unit test** — `server/src/reference_checks/lookup.gleam:126-128` — [tests]. The GET request assembly (method, Basic auth header, `%2B`-encoded URL) is exposed `@internal` for tests but `lookup_test.gleam` never references it, while `build_send_request` has two tests. Add a mirror test asserting GET, the Basic auth header, and the `%2B`-encoded URL.
4. **[coverage-gate] Advisory test gate: CONCERNS** — [tests]. In-scope pure builders/parse/no-op ≈90% (one gap: `build_lookup_request`). The HTTP dispatch envelopes (`do_send`/`do_lookup`) and their error branches are 0% covered at unit and integration level; spec defers that to integration when callers arrive in rc3-5/rc3-7.

### Notes (5)

1. **[logging-consistency] `do_send` logs HTTP/connection failures locally but not parse/build failures** — `server/src/notification/sms_client.gleam:do_send` — [blind]. The 2xx-but-unparseable and request-build branches only capture to Sentry with no local `wisp.log_error`; the HTTP-status and connection branches do both. Route every failure through one capture+log helper.
2. **[boundary] `status_callback_url` naive concat: a trailing slash on `TWILIO_STATUS_CALLBACK_BASE_URL` yields `//webhooks/twilio-sms`** — `server/src/notification/sms_client.gleam:191` — [edge]. Empty base is guarded (callback omitted), but `base="https://host/"` produces a double-slash path that may 404 on the rc3-6 route, silently losing every delivery callback. The `.env.example` default has no trailing slash, so this needs misconfiguration to trigger. Trim a trailing `/` in `init()` or `status_callback_url`.
3. **[spec-deviation] T1.4 specifies parsing `sid`/`status`; only `sid` is decoded** — `server/src/notification/sms_client.gleam:parse_send_response` — [acceptance]. The Twilio response `status` (queued/failed) is never read. No current consumer needs it (rc3-6 webhooks carry delivery status), so low impact — either expose it or amend T1.4.
4. **[duplication] `form_encode` is re-implemented in `sms_client` instead of reusing a shared encoder; `stripe_client` keeps the latent `+` gap** — `server/src/notification/sms_client.gleam:306` cf. `server/src/payment/stripe_client.gleam:609` — [architecture, codebase]. The corrected (`+`→`%2B`) copy lives only in notification; the story spec documents this as a deliberate out-of-scope deviation, but the fork will drift. Extract one shared form-encoder (with the `+` fix) in a later cleanup story.
5. **[coupling] `reference_checks/lookup` depends on `notification/sms_client` for shared Twilio credentials and Basic auth** — `server/src/reference_checks/lookup.gleam:1-17` — [architecture]. The reference_checks domain reaches into notification for the shared `Twilio` handle and `basic_auth_header`. The spec chose this (same creds, no separate provisioning); a neutral `integrations/twilio` module would be cleaner when more callers arrive.

### Reviewer agreement
- **W1** (`init()` base-URL requirement) — confirmed by blind + acceptance independently.
- **N4** (`form_encode` duplication) — confirmed by architecture + codebase independently.

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
