# Lens findings — CLIENT SPA (bundle leakage, token storage, XSS, API trust)

**Job:** righttenantry-security-audit — lens: client SPA
**Repo/worktree:** `/Users/moses/.herdr/worktrees/RightTenantry/security-audit` @ develop (17d5f32) — READ-ONLY
**Posture:** adversarial (bmad-review-adversarial-general); every claim verified against disk.

## Summary

The SPA is unusually clean for a security review. There is **no raw-HTML sink**, **no secret material in client source or shipped static JS**, **no access token or PII in browser storage**, an **opaque error type that discards raw server strings at parse time**, a **strict pattern-match router with a NotFound catch-all**, **HttpOnly-cookie-held session and reset tokens**, and a **well-engineered consent layer** (opt-out-by-default, `__Host-`-prefixed, Consent Mode v2 denied-defaults, sendBeacon audit). The load-bearing gaps are all in the **analytics/attribution** layer and in **CSRF coverage consistency**:

1. PostHog **autocapture runs without text masking** on the landlord dashboard — the single highest-risk PII surface in the SPA (consent-gated, but ties scraped applicant PII to an *identified* landlord profile).
2. The **logout + password-reset chain POSTs omit the `x-csrf-token` double-submit header** that every other state-changing endpoint carries.
3. `checkout_url` from the API is handed to `window.location.assign` **without scheme/host allowlisting**.
4. **14 JavaScript FFI call sites** exist despite the repo's PROHIBITED-unless-approved rule; approvals are asserted in-file comments only.

---

## Findings table

| # | Severity | Title | File:line | Confidence |
|---|----------|-------|-----------|------------|
| F1 | Medium | PostHog autocapture scrapes dashboard PII with no text masking | `Makefile:193` / `Dockerfile:62` (snippet), `server/priv/static/consent.js` | High |
| F2 | Medium | Logout + password-reset chain POSTs omit the CSRF double-submit header | `client/src/api/auth_api.gleam:68,88,123,143,163,178` | High (gap) / Medium (exploit) |
| F3 | Low | `checkout_url` passed to `location.assign` without scheme/host allowlist | `client/src/api/payment_api.gleam:84-87`, `client/src/client.gleam:4254,4450` | Medium |
| F4 | Low | Stripe `session_id` in URL briefly exposed to `history_change` pageview capture before scrub | `client/src/client.gleam:842-940`, `Makefile:193` snippet | Medium |
| F5 | Low | 14 JS FFI sites; "explicit Moses approval" is self-asserted in-file only | `client/src/**` (see list) | High (FFI exists) / Low (approval status) |

---

## F1 — PostHog autocapture scrapes landlord-dashboard PII with no text masking

**Severity:** Medium. **Confidence:** High (config absence verified by grep).

### Evidence

The SPA's PostHog bootstrap (injected by `Makefile:193` and mirrored in `Dockerfile:62`) initialises:

```js
posthog.init("phc_...", {
  api_host: "/_ph",
  person_profiles: "identified_only",
  capture_pageview: "history_change",
  capture_pageleave: true,
  opt_out_capturing_by_default: true,
});
```

It then calls `window.posthog.identify(rt_landlord_id)` once analytics consent is granted (`rt_landlord_id` is a transient non-HttpOnly cookie carrying the landlord UUID). A grep across `client/src/`, `server/priv/static/consent.js`, and `server/priv/static/apply_analytics.js` for `mask_all_text`, `mask_text_selector`, `mask_personal`, `sanitize_properties`, and `disable_autocapture` returns **nothing** — the default PostHog autocapture configuration ships unmodified.

### Exploit sketch

1. A landlord opts into analytics (banner "Accept all" / "Analytics & support").
2. The landlord navigates the dashboard, which renders applicant PII — names, emails, phone numbers, addresses, HAP/social-welfare status (a protected characteristic under the Equal Status Acts).
3. PostHog autocapture (`array.js`, loaded via `/_ph_assets/static/array.js`) records click/submit events with a full `$elements` chain including **element text content** — the applicant's name/email/phone as rendered.
4. Because `posthog.identify(rt_landlord_id)` has run, those events are joined to an **identified** landlord profile, and the raw text is stored in PostHog.

The mitigating factors are real but don't eliminate the risk: `opt_out_capturing_by_default:true` (consent-gated), first-party `/_ph` proxy (no third-party beacon), and `person_profiles:"identified_only"` (events only merge onto an identified profile). None of those prevent the *capture* of raw applicant PII text once consent is given.

### Remediation

Set `mask_all_text: true` (or a targeted `mask_text_selector` for the leaderboard/application-detail rows) in the `posthog.init` config; alternatively `disable_autocapture` and rely on the explicit custom events the codebase already emits. Re-verify with a grep in the Makefile **and** Dockerfile perl passes (both mirror each other — see AGENTS.md snippet-regression rule).

---

## F2 — Logout + password-reset chain POSTs omit the CSRF double-submit header

**Severity:** Medium (gap) / exploitability depends on server SameSite enforcement (server lens). **Confidence:** High for the client-side inconsistency.

### Evidence

`client/src/api/auth_api.gleam` uses raw `rsvp.post` (no `x-csrf-token` header) for six endpoints, while every other state-changing call in the SPA goes through `api_helpers.post_json/patch_json/delete`, which attaches the header via `effective_csrf`:

| Line | Endpoint | Session-bearing? |
|------|----------|------------------|
| 68  | `signup` | no (pre-auth) |
| 88  | `login` | no (pre-auth) |
| 123 | `recover_password` | no (email-trigger) |
| 143 | `resend_confirmation` | no (email-trigger) |
| 163 | `reset_password` | **yes — HttpOnly `rt_reset` cookie** |
| 178 | `logout` | **yes — session cookie** |

Contrast: `api_helpers.post_json` (`client/src/api/api_helpers.gleam:23-41`) sets `x-csrf-token` on every POST, and `accept_policy` (line 202) uses it.

### Exploit sketch

- **`logout`:** if the session cookie is ever sent cross-site (e.g. a `SameSite` configuration gap, or a future downgrade), a third-party page can POST `/api/v1/auth/logout` and force logout of a logged-in landlord (logout CSRF — denial-of-service nuisance).
- **`reset_password`:** it consumes the one-shot HttpOnly `rt_reset` cookie. If an attacker can cause a cross-site POST to `/api/v1/auth/reset-password` with their own `new_password` while a victim has a live reset cookie (narrow window, but the reset link is opened in the victim's browser), the victim's password is set to the attacker's. The double-submit CSRF defense would close this; the SPA doesn't send it.
- **`recover_password` / `resend_confirmation`:** unauthenticated email-trigger endpoints — cross-site POST = email bombing of the victim's inbox (both return 200 unconditionally for enumeration defense, so the attacker gets no confirmation but the mail is sent).

### Remediation

Route `logout` and `reset_password` (and, for defense-in-depth, `recover_password`/`resend_confirmation`) through `api_helpers.post_json` so the `x-csrf-token` header is attached. Confirm server-side that these routes *require* the header when a session/reset cookie is present. Whether the gap is exploitable today depends on the server's `SameSite` attributes — server lens should confirm.

---

## F3 — `checkout_url` passed to `location.assign` without scheme/host allowlist

**Severity:** Low. **Confidence:** Medium (mitigated by TLS + auth, but no client-side guard exists).

### Evidence

`client/src/api/payment_api.gleam:84-87`:

```gleam
fn checkout_url_decoder() -> decode.Decoder(String) {
  use url <- decode.field("checkout_url", decode.string)
  decode.success(url)
}
```

The decoded string flows to `msg.ApiReturnedCheckoutUrl(vid, Ok(url))` and then `navigate_external.assign(url)` at `client/src/client.gleam:4254` and `4450`, which is `window.location.assign(url)` (`client/src/helpers/navigate_external_ffi.mjs`).

### Exploit sketch

If the API response is ever spoofed — compromised server, a malicious/buggy browser extension rewriting the fetch response, or a MITM on a misconfigured deployment — `window.location.assign` navigates the landlord to an arbitrary URL (phishing/credential-harvest page that mimics the Stripe checkout). `javascript:` schemes are blocked by modern browsers in `location.assign`, so this is a navigation/open-redirect vector, not script execution. The SPA's own guard (`Some(current) if current == vid`) only ensures the *vacancy* matches the in-flight request; it does not validate the URL itself.

### Remediation

Validate the decoded URL before navigation: require `https:` scheme and allowlist the expected host (`checkout.stripe.com`, or the server's own canonical origin). Fail closed (toast + no navigation) on mismatch.

---

## F4 — Stripe `session_id` briefly enters `history_change` pageview capture before URL scrub

**Severity:** Low. **Confidence:** Medium.

### Evidence

`client/src/client.gleam:842-940` handles `?payment=success&session_id={CHECKOUT_SESSION_ID}` and `?extended=success&session_id=...` by (a) firing `payment_api.fire_pixel_purchase_for_session(session_id, …)`, and (b) calling `modem.replace(route_to_path(route), None, None)` to strip the query. The PostHog init sets `capture_pageview:"history_change"`, so the route-change to the URL *containing* `session_id` is eligible for pageview capture before the replace runs. The session id is a Stripe Checkout Session id (`cs_live_…`/`cs_test_…`), which is not a bearer secret (retrieval needs the secret key), but it is a capability-ish correlation token and its presence in analytics/URL history is unnecessary exposure.

### Remediation

Replace the URL *before* any analytics-visible navigation, or add a PostHog `before_send` / URL-scrub rule that strips `session_id` (and any other `token`/`code` params) from `$current_url` and `$pathname` client-side. Belt-and-braces with a server-side or edge `Referrer-Policy`/scrub is optional.

---

## F5 — 14 JavaScript FFI call sites; "explicit Moses approval" is self-asserted in-file only

**Severity:** Low (governance). **Confidence:** High that FFI exists; Low that approval is formally recorded.

### Evidence

AGENTS.md states *"JavaScript FFI is PROHIBITED unless explicitly approved by Moses."* The client contains 14 `@external(javascript, …)` sites:

- `components/policy_reaccept_modal_focus.gleam:11,14` → `policy_reaccept_modal_ffi.mjs`
- `components/cookie_settings.gleam:5` → `cookie_settings_ffi.mjs`
- `components/csrf_cookie.gleam:14` → `csrf_cookie_ffi.mjs`
- `components/meta_pixel.gleam:17,20,23` → `meta_pixel_ffi.mjs`
- `components/google_ads.gleam:25,28,31` → `google_ads_ffi.mjs`
- `helpers/download_blob.gleam:6` → `download_blob_ffi.mjs`
- `helpers/navigate_external.gleam:4,11` → `navigate_external_ffi.mjs`
- `helpers/scroll.gleam:8` → `scroll_ffi.mjs`

Each `.mjs` file carries a header comment asserting approval ("Approved FFI exception (Moses, this change)", "Moses approved this exception in-session", "Plan §2b explicitly approved"). The surfaces are genuinely narrow (one pure cookie read, three `fbq` calls, three `gtag` calls, a focus trap, a blob download, two location helpers, a scroll helper), and no raw-HTML or secret material passes through them.

### Why this is a finding

The "explicit approval" trail is **self-asserted in code comments** — there is no central registry or sign-off artifact in the repo that a reviewer can verify against. If any of these approvals were not actually granted, the rule is violated. This is a governance/auditability gap rather than a runtime vulnerability.

### Remediation

Record the approved FFI exceptions in a single committed artifact (e.g. an `FFI-APPROVALS.md` or a section in AGENTS.md) listing each module + function + approving session/PR, so the "explicitly approved" condition is checkable rather than asserted.

---

## What the bundle contains (inventory)

### Public-by-design values baked into `index.html` (Makefile + Dockerfile perl passes)

- PostHog public key (`phc_…`) — env `POSTHOG_KEY`, substituted at build; public by design.
- Meta Pixel id — env `META_PIXEL_KEY`; public by design.
- Google Ads conversion id + 3 conversion labels — env `GADS_ID`, `GADS_SIGNUP`, `GADS_LEAD`, `GADS_PURCHASE`; public by design.
- `rt-pricing-cents` `<meta>` — env `PRICE_CENTS`; public.
- `rt-cookie-policy-version` `<meta>` — env `COOKIE_VER`; public.
- `__RT_CSP_NONCE__` placeholder — replaced at runtime by the server (not a secret).

### JS-readable cookies (by design)

| Cookie | Purpose | Sensitivity |
|--------|---------|-------------|
| `rt_csrf` / `__Host-rt_csrf` | double-submit CSRF token (HMAC(secret, access_token)) | design-readable; short-lived |
| `rt_consent` / `__Host-rt_consent` | consent decision JSON | not sensitive |
| `rt_landlord_id` | landlord UUID, transient bridge to `posthog.identify`, cleared after read | identifier (not a secret) |
| `rt_landlord_external_id` | sha256 hex, transient bridge to `fbq` external_id, cleared after read | hash (not reversible PII) |
| `rt_ph_reset` | reset signal for the bridge | not sensitive |
| `rt_region_preference` | stale multi-region key, purged at boot | not sensitive |

### Browser storage keys (all UI-state only, no tokens/PII)

- localStorage: `rt_consent` (consent mirror), `rt_dismissed_sweep_nudges_v2` (application ids), `rt_refcheck_explainer_dismissed` ("1"), `rt_dismissed_sweep_nudges` (purged v1), `rt_region_preference` (purged).
- sessionStorage: `rt_comparison_ids` (JSON array of application ids).

### Session/auth state

- Access token: **server-set HttpOnly cookie** — the SPA never reads it.
- `csrf_token`: in-memory `Model` field only (`model.gleam:482,709`); never persisted.
- Reset token: HttpOnly `rt_reset` cookie; never enters SPA state or URL.

## Verified-clean list

- **No raw HTML injection:** zero `html.raw` / `dangerously` / `element.text`-bypass sinks in `client/src/`. Lustre escapes by default.
- **No `javascript:`/scheme-injectable `href` sinks:** all `attribute("href", …)` targets are internal relative paths (`/vacancies/<id>`, `/vacancies/<id>/applications/<id>`, static policy/terms paths). `href` in `application_row.gleam:43` is a fixed `/vacancies/…/applications/…` prefix + ids.
- **No secrets in client source or shipped static JS:** grep across `client/src/` and every `server/priv/static/*.js` for `sk_live`, `sk_test`, `service_role`, `SECRET`, `INTERNAL`, `supabase`, `anon`, `sentry`, `dsn`, `Bearer`, `AIza` → all hits are comments, none are values.
- **No tokens/PII in storage:** every `plinth/browser/storage` call site touches only the UI-dismissal/comparison keys above.
- **Opaque error type:** `api/api_error.gleam` exports an opaque `ApiError`; raw server message is discarded at parse (`from_body`), only `code` + `fields` survive. Copy lives in `copy.gleam` — brand-voice enforced, no info-leak.
- **Router:** strict pattern match with `_ -> NotFound` catch-all (`router.gleam`); no unvalidated-segment sinks; ids only flow into fixed API path prefixes.
- **Consent gating:** `opt_out_capturing_by_default:true`, `__Host-`-prefixed consent cookie, Consent Mode v2 denied-defaults (`gtag("consent","default",{…denied…})`), sendBeacon audit with fail-open, defensive `opt_out`+`reset` on stale/no consent.
- **Public form analytics (`apply_analytics.js`):** custom events only; `first_error_field` is a field *key*, never a value; `vacancy_short_code` is already in the URL; no input values captured.
- **Pricing trust:** price is display-only (`format_currency` in `leaderboard_view.gleam:657`, `landing.gleam:22`, `auth_layout.gleam:75`); the Stripe charge amount is server-authoritative — the client never sends the price.
- **First-touch attribution:** reads UTM/click-ids off the landing URL only, carries them in-memory (no device storage), server applies `utm_source=content` masking.
