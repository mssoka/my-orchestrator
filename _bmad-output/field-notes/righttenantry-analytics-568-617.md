# Field notes — righttenantry-analytics-568-617 (PR #624)

- OAuth first-touch: `wisp.get_query` percent-decodes (round-trip clean), and a Signed wisp cookie value is base64url-wrapped by `sign_message` — ANY payload string is header-safe, so `uri.query_to_string` output is a valid cookie value; tests can craft valid signed cookies with `simulate.cookie(req, name, raw, wisp.Signed)` on a `simulate.request` (same canned secret key base).
- The `rt_consent` cookie for tests must be set as a RAW header (`simulate.header("cookie", "rt_consent=" <> percent_encode(json))`) — `simulate.cookie(..., wisp.PlainText)` base64s it and `read_raw_consent_cookie` reads verbatim (mirror payment_verify_integration_test's helper).
- "Plan §5" (Meta consent gating: Lead + CompleteRegistration consent-gated, Purchase carve-out) has NO plan doc on disk — cite the code call sites (meta/dispatch.gleam:18-22) instead; and the em-dash lint exempts `wisp.log_*` string args, so decision logs can carry em-dashes.
