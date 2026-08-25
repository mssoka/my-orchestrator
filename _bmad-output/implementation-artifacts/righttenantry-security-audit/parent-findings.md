# Parent minion verified findings — righttenantry-security-audit (PAUSED)

My own recon verification, done in parallel with the lens swarm. Every item
was verified against disk. Merge into the final report on resume.

## Verified CLEAN (I personally confirmed these are not vulnerable)

- **`/static/*` path traversal** — NOT exploitable. `wisp.path_segments` =
  `gleam/http/request.path_segments` → `gleam/uri.path_segments`, which splits
  raw (NO percent-decoding) and RFC-3986 removes `..`/`.` segments before wisp
  sees them. `%2e%2e` stays a literal filename segment; `%2F` never becomes a
  separator. The router's own `s != ".." && s != "."` filter is redundant.
  Vendored source: `gleam_stdlib/src/gleam/uri.gleam:601-628`.
- **Internal endpoints secret gate** (`require_internal_secret`,
  `server/src/response_helpers.gleam:128-149`) — uses `crypto.secure_compare`;
  empty secret returns 500 (fail-closed); `INTERNAL_SECRET` is required in
  production (`server.gleam:250`).

## Verified findings (mine; several also surfaced by lenses — merge, dedupe)

- **Host header → Stripe `success_url`/`cancel_url`** (Low). `router.gleam`
  passes `request.get_header(req,"host")` (default "righttenantry.ie") as
  `origin_host` to `payment_handler.handle_create_checkout` /
  `handle_create_extension_checkout`; `run_consent_and_checkout_tx`
  (`payment/payment_handler.gleam:456-463`) builds `scheme <> "://" <>
  origin_host` into both redirect URLs. Self-only (victim is the payer), but
  it's the one un-allowlisted host read and the `string.contains(origin_host,
  "localhost")` scheme sniff is bypassable (`Host: evil.localhost.example` →
  http). Duplicate of lens-webhooks **W-3**. Fix: route through
  `domain_helpers.validate_origin_domain`.
- **`RT_CLOUDFLARE_SECRET` default "local-dev-secret"** (Low/Medium config).
  `server.gleam:63` unwraps to a guessable committed default with NO
  production guard, unlike `SECRET_KEY` (line 67+) which fails closed. If
  Terraform ever fails to set the secret, the production origin lock compares
  against a public string. Overlaps lens-infra INFRA-03/INFRA-08.
- **`x-forwarded-for` first-value trust** (`request_helpers.gleam:40-53`) —
  spoofable if the `.run.app` origin is reached directly (bypassing CF which
  overwrites the header); affects consent `ip_text`, `submitted_ip_text`, and
  Meta CAPI IP egress. Duplicate of lens-data **F1** (rated Medium there).
- **CSP is Report-Only in production** (`server/src/csp.gleam:header_name` —
  `CSP_ENFORCE != "true"` → report-only). Directives are strong
  (`object-src 'none'`, `frame-ancestors 'none'`, `base-uri 'self'`,
  `form-action 'self'`, nonce'd script-src), but XSS defense-in-depth is not
  yet enforcing. Documented rollout state — a "schedule" triage line, not a
  bug. Note `script-src` allowlists `https://connect.facebook.net` and
  `style-src` keeps `'unsafe-inline'`.
- **`is_same_origin_request` allows `same-site`** (Info) — the consent-endpoint
  CSRF substitute accepts `sec-fetch-site: same-site`; acceptable given no
  session on `/api/v1/consent`, worth a note only.
- **`RESEND_API_KEY` / `RESEND_WEBHOOK_SECRET` empty-in-prod are non-fatal**
  (Info) — `server.gleam:78-102` logs + continues with `""`; consequences are
  availability (no email) + webhook verification fail-closed (HMAC of "" never
  matches). Not a security hole, but a "secret silently absent = degraded"
  asymmetry vs the hard-fail keys.

## Recon map (context for resume)

- Router: full route table read (`server/src/router.gleam`). Attack surface:
  public token routes `/apply/:code`, `/erase/:token`, `/dsar/:token`,
  `/reference/:token`, `/apply/:code/resume|draft-erasure/:token`; internal
  `/api/v1/internal/*` (INTERNAL_SECRET); webhooks `/api/v1/webhooks/*` +
  top-level `/webhooks/*` (provider HMAC); authenticated landlord routes
  behind `require_session` + CSRF.
- Middleware (`middleware.gleam`): CORS allowlist, per-response CSP nonce,
  X-RT-Secret origin lock (prod-only, plain `==`), body-size gate with
  CL/TE-smuggling rejection, token-redacted access logs.
- Auth: PKCE S256 (`pkce.gleam`), signed cookies (`wisp.Signed`), `__Host-`
  prefixed names in prod, session cache defers to GoTrue `/auth/v1/user`
  (server-side JWT validation), CSRF = HMAC(secret, access_token) with
  `secure_compare`.
- DB: RLS auto-enabled on all public tables (default-deny, no policies); app
  uses privileged role → app-level ownership filters in SQL are the tenant
  boundary (lens-authz confirmed no cross-tenant egress).
