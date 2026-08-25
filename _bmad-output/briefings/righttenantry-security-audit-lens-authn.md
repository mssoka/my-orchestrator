# Lens briefing — security-audit / AUTHN (OAuth, sessions, password flows, enumeration)

- **Job:** righttenantry-security-audit (mega-minion lens; parent minion audits the repo)
- **Model policy:** `zai-coding-cn/glm-5.3` (probe-confirmed back up post cap reset; the user-required model for this audit).
- **Repo/worktree (READ-ONLY):** `/Users/moses/.herdr/worktrees/RightTenantry/security-audit` @ develop (17d5f32)
- **Skill:** `bmad-review-adversarial-general` — cynical posture; every claim verified against disk before reporting.
- **Output:** write findings to `/Users/moses/code/_bmad-output/implementation-artifacts/righttenantry-security-audit/lens-authn.md`, then end with a one-paragraph summary in your pane.

## Ground rules

- READ-ONLY: no edits, no commits, no installs, no pushes. Do not spawn sub-agents.
- Stack: Gleam/Wisp server, Supabase GoTrue (server-mediated via `server/src/auth/supabase.gleam`), wisp signed cookies (`wisp.Signed`, HMAC with SECRET_KEY), `__Host-` prefixed cookie names in production (ENV=production), PKCE S256 OAuth via Google.
- Evidence discipline: every finding = severity + `file:line` + exploit sketch + remediation + confidence. Verify end-to-end against the code. A false positive is a failure. If clean, say what you checked.

## Scope — `server/src/auth/**` + auth-adjacent handlers

Recent prior art (scan with FRESH eyes, don't assume): OAuth/PKCE + short-lived cookie across the redirect (#617 work), Meta CAPI consent-gated inserts (#568/#583).

1. **OAuth flow** (`auth_handler.handle_oauth_initiate` / `handle_oauth_callback`): Is there a `state` parameter at all, or does PKCE alone carry the defense? Is the code_verifier cookie bound to the initiating browser (signed? SameSite? max-age?); can a callback be replayed or cross-site? Is `provider` validated (arbitrary value → Supabase error, or SSRF/redirect)? Is `oauth_redirect_url` fixed server-side (env) — confirm no user input reaches `redirect_to`. Check `handle_email_confirm`: token_hash handling, type param validation (can `type=recovery` be forced where signup expected?), what lands in cookies after verify, any open redirect via query params on /auth/confirm or /auth/callback.
2. **Cookie discipline** (`auth_handler.set_session_cookies`, `clear_session_cookies`, `cookie_names`): attributes — HttpOnly, Secure, SameSite, Path, Max-Age; signed cookie tamper resistance (wisp.Signed); whether the refresh cookie is scoped as tightly as the session; logout clearing.
3. **Password reset** (`password_reset_handler`, `reset_nonce_store` + its ffi): one-shot nonce semantics, cookie signing, timing, enumeration (uniform responses), cooldown/rate-limit logic (in-app, since edge is Cloudflare), resend-confirmation abuse (email bombing), generate_link path.
4. **Login/signup**: enumeration via response differences (email_not_confirmed leaks account existence?), timing, rate-limit hooks, Meta CAPI / PostHog insert on signup — what fields go where (PII leakage to third parties?), consent gating (issue #568: CAPI on OAuth signup insert).
5. **Session middleware interplay** (you may read `session_middleware.gleam`, `session_cache.gleam`, `auth@session_cache_ffi.erl`): cache poisoning paths, refresh race conditions (concurrent refresh → token rotation races), auto-create landlord fallback (email "unknown"), policy-gate bypass routes.
6. **First-touch attribution** (`first_touch_cookie.gleam`, `attribution.gleam`): the signed cookie carries UTM/click-ids across the OAuth redirect — can a crafted cookie inject arbitrary values into Meta CAPI payloads (analytics injection / PII)? Is it signed and length-capped?
7. **Change password / settings** (`settings_handler`): current-password verification, session invalidation of OTHER sessions (`invalidate_other_sessions` — actually wired?), account deletion auth path.
8. In-app rate limiting overall: which auth endpoints have app-level throttles vs relying solely on Cloudflare edge (list what you find).

## Deliverable format

Markdown: summary paragraph, findings table (id, severity, title, file:line, confidence), then one section per finding with exploit sketch + evidence (code quotes) + remediation. Explicitly list what you verified CLEAN.
