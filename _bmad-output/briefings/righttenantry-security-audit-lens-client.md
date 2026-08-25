# Lens briefing — security-audit / CLIENT SPA (bundle leakage, token storage, XSS, API trust)

- **Job:** righttenantry-security-audit (mega-minion lens; parent minion audits the repo)
- **Model policy:** `deepseek/deepseek-v4-pro` (glm-5.3 provider-capped 429 code 1308 until 17:54:28Z — sanctioned fallback per the playbook's fallback chain; briefing override).
- **Repo/worktree (READ-ONLY):** `/Users/moses/.herdr/worktrees/RightTenantry/security-audit` @ develop (17d5f32)
- **Skill:** `bmad-review-adversarial-general` — cynical posture; every claim verified against disk.
- **Output:** write findings to `/Users/moses/code/_bmad-output/implementation-artifacts/righttenantry-security-audit/lens-client.md`, then end with a one-paragraph summary in your pane.

## Ground rules

- READ-ONLY: no edits, no commits, no installs. Do not spawn sub-agents.
- Stack: Lustre SPA (`client/src/**`, compiles to `server/priv/static/client.js`), modem routing, rsvp HTTP, plinth browser storage/document. Repo rule: **JavaScript FFI is PROHIBITED** — any violation is itself a finding (grep for `@external(javascript`).
- Evidence discipline: every finding = severity + `file:line` + exploit sketch + remediation + confidence. Verified only; a false positive is a failure.

## Scope

1. **Secret/env leakage into the bundle**: how do PostHog key, Meta Pixel, Google Ads id, CSP nonce placeholder get into HTML/JS (Makefile + Dockerfile perl passes bake into index.html — read `Makefile` + `Dockerfile` sections that touch index.html and check the client source for embedded strings). Grep the client source for anything resembling keys/tokens/URLs with credentials; check `client/gleam.toml` + `client/src` for compile-time defines. The PostHog API key is public-by-design — verify nothing ELSE (Supabase service role, Stripe secret, internal secret, Sentry DSN with PII-beaming settings) bakes in. Note: worktree `server/priv/static/` may hold a stale built bundle — inspect it if present (`ls server/priv/static/`) and grep the BUILT bundle for `SECRET`, `service_role`, `sk_`, `INTERNAL`.
2. **Token/credential storage**: where does the SPA keep session state? (Cookies are HttpOnly server-set — verify the SPA never copies access tokens into `plinth/browser/storage` or localStorage; `components/csrf_cookie` reads rt_csrf — document exactly what is JS-readable by design and what must never be.) Any tokens/PII persisted to storage keys — enumerate every storage read/write (`plinth/browser/storage` call sites).
3. **XSS in the SPA**: Lustre escapes by default — grep for raw HTML injection (`html.raw`, `dangerously`, `element.text` bypasses, `string_tree` into DOM). Also: URLs built from API data into `href` (javascript: scheme via stored vacancy fields or application data rendered in the dashboard), `attribute("href", user_controlled)` sinks.
4. **API trust**: decoders in `client/src/api/` — fail-open decoding of security-relevant fields (payment status, pricing — client displays price: does the client trust a server-provided price or hardcode? attack = spoofed API response via MITM? note TLS assumption), error handling that leaks raw server errors (brand rule violation = also info-leak surface).
5. **Routing/URL handling**: query params parsed into state (payment=success flows), tokens in URL fragments vs query (analytics exposure — PostHog autocapture captures URL: verify scrubbing for token-bearing routes), modem route matching with unvalidated segments.
6. **CSRF wiring**: how the SPA attaches `x-csrf-token` (reads the cookie `components/csrf_cookie`) — document the double-submit flow; can a subdomain or XSS-free injection desync it; is logout POST protected?
7. **Posthog/meta consent**: client-side event capture — what properties are attached (emails? IPs?), autocapture enabled (scrapes DOM — could scrape PII from pages), consent gating client-side (#568/#583 prior art — verify current state).

## Deliverable format

Markdown: summary, findings table (id, severity, title, file:line, confidence), one section per finding with exploit sketch + evidence + remediation. Include a "what the bundle contains" inventory (public keys/env baked in, storage keys used) and verified-clean list.
