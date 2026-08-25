# Lens report — AUTHN (parent-completed)

**Note:** this lens was dispatched twice and lost twice to external factors
(model cap 429, then pane reclamation mid-hunt). The parent minion completed
the scope in-pane using the same briefing. The dead lens's transcript showed
it had reached "verify wisp cookie primitives" — that starting point is
included below.

## Verified CLEAN

- **Cookie primitives** (`wisp.set_cookie` → `gleam/http/cookie.defaults`):
  `path=/`, `secure` on HTTPS, `http_only=True`, `same_site=Lax`, no Domain.
  Session (30d) + refresh (7d) cookies: `wisp.Signed` (HMAC-SHA512) —
  tamper-proof; `rt_csrf` deliberately JS-readable (double-submit, value is
  non-secret HMAC); PKCE cookie signed, 300s.
- **OAuth flow** (`auth_handler.handle_oauth_initiate/callback`): provider
  allowlisted (`["google"]`); `redirect_to` is the env-config
  `oauth_redirect_url` (never request input); PKCE S256 with the verifier in
  a signed cookie = the CSRF/state binding (a cross-site callback carries no
  matching verifier cookie → exchange fails; login-CSRF blocked); callback
  redirects are fixed (`/dashboard`, `/login`); `pkce` + `first_touch`
  cookies cleared on every terminal arm; error path logs only codes.
- **first_touch attribution cookie** (`first_touch_cookie.gleam`): signed,
  5-min TTL, key allowlist (8 fixed UTM/click-id keys), values trimmed +
  length-clamped (`attribution.clamp_value`), cleared on terminal responses.
  CAPI/analytics injection bounded to `$set_once` properties.
- **Meta CAPI consent gate** (`dispatch_signup_meta` →
  `consent_check.marketing_granted`): no fire without consent cookie; fire-once
  on true insert only (is_new via atomic `xmax` upsert flag). #568 posture
  verified in place on BOTH signup and OAuth paths.
- **Password reset** (`password_reset_handler` + `reset_nonce_store`): 288-bit
  class one-shot nonce, atomic `ets:take` consume, 15-min TTL, length band
  32-128 enforced, HttpOnly signed `rt_reset` cookie, no token_hash in SPA
  URLs; nonce re-inserted only on benign retry arms; password change verifies
  `current_password` via real login before update (verify-then-update);
  `invalidate_all_sessions` on reset, `invalidate_other_sessions` on change
  password + account delete (wired at password_reset_handler:408,
  settings_handler:196, account_handler:137).
- **Enumeration**: `recover` always-200 (Supabase enumeration-safe mapping,
  verified in supabase.gleam); `email_not_confirmed` on login fires only with
  CORRECT credentials (not an account-existence oracle); resend-confirmation
  generic-response across unknown/confirmed/OAuth/cooldown states + 60s
  per-account cooldown + Worker per-IP limit.
- **Login CSRF/logout**: logout is CSRF-skipped by documented rationale (no
  victim-credential advantage); POSTs can't ride `rt_session` cross-site
  (SameSite=Lax).

## Findings

| ID | Severity | Title | Location | Confidence |
|----|----------|-------|----------|------------|
| A-1 | Info | Signup reveals account existence (`SignupEmailExists` distinct response) — common tradeoff, GoTrue-throttled | `auth/supabase.gleam:is_email_exists_body` → signup response | High (mechanism) |
| A-2 | Info | OAuth error arm logs `error_description` from query (log-text injection surface only — never rendered) | `auth_handler.handle_oauth_callback` error arm | High (mechanism), Info impact |

Both lens-scope questions from the briefing resolved; no Medium+ authn
findings. The auth surface is the strongest layer in the codebase.
