# RightTenantry — Full-Codebase Security Audit Report

- **Repo:** RightTenantry, worktree `security-audit` @ develop `17d5f32` (2026-08-18)
- **Scope:** every scan surface from the audit briefing (OWASP-flavored, adapted to Gleam/Wisp + Supabase + Cloudflare + GCP)
- **Method:** parent-minion recon + 7 adversarial/path-tracing lenses (authz, authn, webhooks+payments, SSR/render, client SPA, data layer, infra+deps), followed by a parent verification pass re-reading the cited source at every load-bearing `file:line`. Findings adjusted where verification nuanced them (noted inline).
- **Posture:** READ-ONLY — no product code changed, no PR, no upgrades.
- **Verification status legend:** ✅ parent-verified at cited lines · 🔍 lens-reported, evidence quoted in lens file · 📝 self-documented in code comments

## Executive summary

The codebase is in **strong security shape for its size and age**. The architectural defenses are real and consistently applied: Squirrel parameterization makes SQL injection architecturally impossible (verified: all 227 `.sql` → parameterized; the single raw `pog.query` is a static `SET LOCAL`); all three webhook providers are HMAC-verified with `crypto.secure_compare`; sessions are GoTrue-validated server-side with `__Host-` signed cookies and an HMAC CSRF token; uploads are magic-byte-validated with UUID storage paths; Sentry CrashEvent headers pass an allowlist; access logs redact token routes centrally. No Critical findings. No cross-tenant data egress (verified against the SQL for every user-scoped route).

The material risks concentrate in four places:

1. **The Stripe unlock webhook trusts event shape more than payment truth** — `checkout.session.completed` is processed without checking `payment_status` (async payment methods settle later than the event) and the unlocked vacancy is keyed from event metadata rather than cross-checked against the payment row (M-1, L-4, L-9).
2. **Documented edge rate limits do not exist** — AGENTS.md promises login 10/min, signup 5/h, apply-submit 5/h at the Cloudflare edge; the Worker "deliberately omits" exactly those, and the Free-tier single `http_ratelimit` slot is spent on `/erase/`+`/dsar/` (M-2).
3. **The CI deploy identity is a full-project takeover primitive** — the deploy SA holds `projectIamAdmin` + `serviceAccountAdmin` + WIF admin, so a compromised merge to `main`/`staging` can grant itself anything (M-3).
4. **PII reaches logs on error paths** — ADK parse failures log raw applicant-bearing bodies; Supabase error bodies (echoing emails) are logged raw; Twilio failures log the raw phone number (M-6, M-7, M-8).

Plus one privacy-by-design gap worth a conscious decision: PostHog autocapture runs without text masking on the landlord dashboard (M-4), and the DSAR export includes third-party PII (referees, co-applicants, guarantors) (L-15).

**Final tally: 0 Critical, 8 Medium, 25 Low, 14 Info.** The authn layer (OAuth/PKCE, cookies, password flows) and the SSR/render layer verified clean at every sink walked — the strongest layers in the codebase.

## Triage verdicts (recorded verbatim from the lavish session, 2026-08-18)

User's answers, exactly as queued:

- M-1 (Stripe payment_status): **fix-now**
- M-2 (missing edge rate limits): **schedule**
- M-3 (deploy SA projectIamAdmin): **schedule**
- M-4 (PostHog autocapture PII): **schedule**
- M-5 (XFF trust): **schedule**
- M-6/M-7/M-8 (PII in logs): **schedule**
- Low findings (L-1..L-25) batch verdict: **schedule-batch**

**Routing:** M-1 becomes an immediate follow-up fix job (gating — the Stripe-unlock
invariant). M-2..M-8 + the Low batch fold into follow-up fix jobs batched per the
one-issue-per-repo doctrine (#607 RT), unless severity justifies its own issue.

## Findings register

Severity-ranked. **Triage** column is for the user's fix-now / schedule / accept-risk verdict (lavish session).

### Medium

| ID | Title | Location | Status | Triage |
|----|-------|----------|--------|--------|
| M-1 | `checkout.session.completed` never checks `payment_status` — vacancy unlocks before async funds settle | `payment/webhook_handler.gleam:313-380` (verified absent across file) | ✅ | **fix-now** |
| M-2 | Documented edge rate limits (login 10/min, signup 5/h, apply 5/h per IP) are not implemented anywhere | `deployment/cloudflare-worker/worker.js:588` ("Deliberately omitted"); `deployment/terraform/cloudflare-rate-limits.tf` (1-rule Free slot → `/erase/`+`/dsar/`) | ✅ | **schedule** |
| M-3 | Deploy SA holds `projectIamAdmin` + `serviceAccountAdmin` + `workloadIdentityPoolAdmin` — CI compromise = full GCP project takeover | `deployment/terraform/iam.tf:86-103` | ✅ | **schedule** |
| M-4 | PostHog autocapture runs without text masking on the landlord dashboard — applicant PII scraped into an identified profile (consent-gated) | `Makefile:193` / `Dockerfile:62` snippet (no `mask_all_text`, autocapture defaults on) | ✅ | **schedule** |
| M-5 | `client_ip` trusts first `x-forwarded-for` value — spoofable when origin reached directly; feeds consent records + Meta CAPI egress | `request_helpers.gleam:40-53` | ✅ | **schedule** |
| M-6 | ADK response parse-failure paths log raw body (applicant data) to Cloud Logging | `ai/ai_client.gleam:1044,1170,1189,1340` | ✅ | **schedule** |
| M-7 | Supabase signup/OAuth error bodies logged raw (may echo email) | `auth/supabase.gleam:308,632,651` | ✅ | **schedule** |
| M-8 | Twilio Lookup failures log raw phone number (Cloud Logging + Sentry) | `reference_checks/lookup.gleam:85-93` | ✅ | **schedule** |

### Low

| ID | Title | Location | Status | Triage |
|----|-------|----------|--------|--------|
| L-1 | `auto_close_vacancy` mutates without owner filter, runs before the ownership-scoped read (forced early close of an expired vacancy; UUID unguessable cross-tenant) | `vacancy/sql/auto_close_vacancy.sql:5-11`; call `vacancy_handler.gleam:314` | ✅ | schedule (batch) |
| L-2 | PATCH `/status` + reference-check start/skip/re-enable never bind URL `vacancy_id` to the application's vacancy (same-owner confusion only — `vacancy.user_id = $3` IS checked) | `application/sql/update_application_status.sql:1-7`; `application_detail_handler.gleam:607,616,677`; `trigger.gleam:1060` | ✅ | schedule (batch) |
| L-3 | Archived vacancies keep serving landlord name + full property address on `/apply/:code` (closed page header renders them) | `application/form_pages.gleam:20-60` + `form_view.gleam:540-565` | ✅ | schedule (batch) |
| L-4 | Unlock keyed from event `metadata.vacancy_id`, never cross-checked against payment row's vacancy (defense-in-depth: metadata is server-authored at session creation; `sku_type` IS cross-checked fail-closed) — *parent-adjusted from lens Medium* | `payment/webhook_handler.gleam:505-555`; `payment/sql/complete_payment.sql` | ✅ | schedule (batch) |
| L-5 | Payment checkout routes read `Host` header raw → Stripe `success_url`/`cancel_url` attacker-controllable (self-only; `localhost` substring scheme-sniff bypassable; only un-allowlisted host read in codebase) | `router.gleam` (host read), `payment/payment_handler.gleam:456-463` | ✅ | schedule (batch) |
| L-6 | Inbound-email auto-reply recipient selectable from email BODY (not just envelope sender) → templated mail to arbitrary address via a public vacancy inbound address — *parent-adjusted: Svix signature IS verified; vector is email-borne, not HTTP-borne* | `inbound_email/inbound_handler.gleam:213-247`; `email_parser.gleam:55-71` | ✅ | schedule (batch) |
| L-7 | No refund/dispute webhook handling — chargeback leaves vacancy unlocked, payment `completed` | `payment/webhook_handler.gleam` (event dispatch default arm) | 🔍 | schedule (batch) |
| L-8 | Stripe signature parser checks only the first `v1=` — secret-rotation window breaks verification (availability) | `payment/stripe_webhook.gleam:45-58` | ✅ | schedule (batch) |
| L-9 | Amount/currency not verified against expected price — reconcile-and-warn only; SKU-blind env fallback on missing amount | `payment/webhook_handler.gleam:328-345,598-625` | ✅ | schedule (batch) |
| L-10 | Auth POSTs (logout/reset chain) omit CSRF header — consistent with the server's documented skip-list; exploitability rests on SameSite=Lax which holds — *parent-adjusted from lens Medium: by-design, pin it with a test* | `client/src/api/auth_api.gleam:68-178` | ✅ | schedule (batch) |
| L-11 | `checkout_url` handed to `window.location.assign` without scheme/host allowlist | `client/src/api/payment_api.gleam:84-87`; `client/src/client.gleam:4254,4450` | 🔍 | schedule (batch) |
| L-12 | Stripe `session_id` briefly exposed to `history_change` pageview capture before scrub | `client/src/client.gleam:842-940` | 🔍 | schedule (batch) |
| L-13 | Digest handler logs full landlord email unmasked | `notification/digest_handler.gleam:216,226` | ✅ | schedule (batch) |
| L-14 | Single-use erasure URL logged in a dev-conditional branch, bypassing central redaction | `application/application_handler.gleam:2177` | 🔍 | schedule (batch) |
| L-15 | DSAR export includes referee/co-applicant/guarantor third-party PII (defensible Art.15 scope call, but should be conscious + documented) | `dsar/dsar_handler.gleam:240-330,365-373` | ✅ | schedule (batch) |
| L-16 | IP classified as non-PII in audit_log — survives 6-year pseudonymisation window | `retention/audit_log_schema.gleam:123-124` | 🔍 | schedule (batch) |
| L-17 | Typst markup metacharacters unescaped in PDF generation (formatting injection, sandbox-bounded) | `ai/typst_sanitize.gleam:28-38` | 📝 | schedule (batch) |
| L-18 | Account-deletion pending-payment gate has a TOCTOU window (orphan charge, manual refund path documented) | `account/account_handler.gleam:200-238` | 📝 | schedule (batch) |
| L-19 | X-RT-Secret origin lock uses plain `==` (timing); inconsistent with codebase's own `secure_compare` standard | `middleware.gleam:425-432` | ✅ | schedule (batch) |
| L-20 | `RT_CLOUDFLARE_SECRET` defaults to committed `"local-dev-secret"` with NO production fail-closed guard (unlike `SECRET_KEY`) | `server.gleam:62-64` | ✅ | schedule (batch) |
| L-21 | GitHub Actions pinned to floating major tags, not commit SHAs | `.github/workflows/*.yml` | 🔍 | schedule (batch) |
| L-22 | Destructive-migration guard is warn-only; deploys run `db push --include-all` | `pr-checks.yml:41-50` | 🔍 | schedule (batch) |
| L-23 | Runtime image runs as root (no `USER`, no `runAsUser`) | `Dockerfile` stage 2; `cloud-run.tf` | 🔍 | schedule (batch) |
| L-24 | Base images tag-pinned, not digest-pinned | `Dockerfile:6,142` | 🔍 | schedule (batch) |
| L-25 | 14 JS FFI sites in the client; Moses-approval is self-asserted in-file only (governance) | `client/src/**` | 🔍 | schedule (batch) |

### Info

| ID | Title | Location | Status |
|----|-------|----------|--------|
| I-1 | CSP is Report-Only in production (`CSP_ENFORCE` unset) — enforce flip is the pending follow-up; directives themselves strong | `csp.gleam:58-66` | ✅ |
| I-2 | PostHog `identify` ships landlord email as `$set` person property, consent-independent | `auth/auth_handler.gleam:259-266,486-490` | 🔍 |
| I-3 | Twilio webhook signature carries no timestamp (no replay window); idempotent transitions mitigate | `notification/twilio_webhook.gleam` | 🔍 |
| I-4 | X-RT-Secret (Worker secret) lives in Terraform state; bucket IAM not verifiable from repo | `cloudflare-worker.tf:30-33` | 🔍 |
| I-5 | Runtime SA has project-wide `secretmanager.secretAccessor`, not per-secret | `iam.tf:78-83` | 🔍 |
| I-6 | `test.yml`/`pr-checks.yml` declare no explicit `permissions:` block | `.github/workflows/` | 🔍 |
| I-7 | `is_same_origin_request` accepts `sec-fetch-site: same-site` (consent endpoint only; acceptable) | `request_helpers.gleam:105-125` | ✅ |
| I-8 | `RESEND_API_KEY`/`RESEND_WEBHOOK_SECRET` empty-in-prod are non-fatal (silent degrade vs hard-fail asymmetry) | `server.gleam:78-102` | ✅ |
| I-9 | npm audit: 2 high (nanoid ≤3.3.17, postcss ≤8.5.22) — build-time only, not shipped; report-only per scope | `package-lock.json` | 🔍 |
| I-10 | `/apply/:code` invalid-code and closed responses are uniform (no vacancy enumeration via response shape) | `application_handler.gleam:53-105` | ✅ |
| I-11 | Signup reveals account existence (`SignupEmailExists` distinct response) — common tradeoff, GoTrue-throttled | `auth/supabase.gleam` (`is_email_exists_body`) | ✅ |
| I-12 | OAuth error arm logs `error_description` from query (log-text injection surface only — never rendered) | `auth_handler.handle_oauth_callback` | ✅ |
| I-13 | CSP `style-src 'unsafe-inline'` + `script-src connect.facebook.net` broaden the (report-only) policy | `csp.gleam:policy` | ✅ |
| I-14 | `*.run.app` origin-suffix trust bounded to the project's own suffix; abuse requires project access (M-3 class) | `domain_helpers.validate_origin_domain` | ✅ |

## Medium-finding details

### M-1 — Stripe unlock webhook ignores `payment_status`

**Where:** `payment/webhook_handler.gleam:313-380` (`handle_checkout_completed`); verified by absence — `payment_status` appears nowhere in the file; the event router dispatches `checkout.session.completed` directly.

**Exploit sketch:** Not attacker-crafted — a timing/integrity gap. If the Stripe Dashboard ever allows async payment methods (SEPA direct debit, Boleto, Klarna — `payment_method_types` is NOT restricted in `stripe_client.gleam`), Stripe fires `checkout.session.completed` with `payment_status: "processing"` or `"unpaid"`. The handler unlocks the vacancy + fires burst AI scoring immediately; funds may later fail (SEPA chargebacks arrive days later), leaving an unlocked vacancy with no settled payment. No refund/dispute handling (L-7) compounds it.

**Remediation:** Gate the unlock path on `payment_status == "paid"` (treat anything else as pending — ack 200 and wait for `payment_intent.succeeded` or a second completed event), or restrict `payment_method_types` to `["card"]` at session creation so completed ⇒ paid.

### M-2 — Documented edge rate limits do not exist

**Where:** `deployment/cloudflare-worker/worker.js:588` (comment: "Deliberately omitted: the rest of /api/v1/auth/* (login, signup, recover…)"); `deployment/terraform/cloudflare-rate-limits.tf` (Free tier = 1 `http_ratelimit` rule, spent on `/erase/`+`/dsar/`).

**Exploit sketch:** AGENTS.md documents "login 10/min, signup 5/hour, application submit 5/hour per IP" at the Cloudflare edge. None of these exist. Nuance from verification: GoTrue applies its own throttling to login/signup (the code maps `429`/`over_request_rate_limit`), and `resend-confirmation` has a Worker per-IP limit + DB cooldown. The practical unprotected surfaces: **`POST /apply/:code` submissions** (22MB multipart bodies, storage writes, email sends, AI-queue inserts per hit — unbounded per IP), and `/auth/recover` spam (Supabase per-email throttle only).

**Remediation:** Extend the Worker's per-IP `AUTH_WRITE_PATTERN` bucket to `/apply/*` POSTs now (Worker-based counters bypass the 1-rule cap by design); correct AGENTS.md; add the account-aware auth limits when a paid plan frees the ruleset slot.

### M-3 — Deploy SA is a full-project takeover primitive

**Where:** `deployment/terraform/iam.tf:86-103` — `deploy_iam_admin` (`roles/iam.serviceAccountAdmin`), `deploy_project_iam_admin` (`roles/resourcemanager.projectIamAdmin`), `deploy_wif_admin` (`roles/iam.workloadIdentityPoolAdmin`). (Citation corrected from lens's 120-130.)

**Exploit sketch:** Anyone who can push to `main`/`staging` (or compromise a runner) authenticates as the deploy SA via WIF and runs `terraform apply` — which can grant that SA any role in the project, mint service accounts, or re-point WIF. Single compromised merge ⇒ full GCP project control including Secret Manager access to every secret.

**Remediation:** Split the Terraform-apply identity from IAM administration: narrow the CI SA to (`artifactregistry.writer`, `run.developer`, per-secret `secretVersionAdder`), and move IAM/SA/WIF changes to a separately-triggered, human-gated workflow/identity. At minimum: required reviewers on the `production` environment + document that this SA is effectively project-owner.

### M-4 — PostHog autocapture scrapes dashboard PII, no masking

**Where:** `Makefile:193` / `Dockerfile:62` PostHog init — no `autocapture` disable, no `mask_all_text`, `capture_pageview: "history_change"`, `person_profiles: "identified_only"`, `opt_out_capturing_by_default: true`.

**Exploit sketch:** For a landlord who accepts analytics cookies (consent-gated), PostHog autocapture records clicks + input text across the dashboard — applicant names, emails, addresses, scores render in the DOM and are captured as identified events to the EU cloud. Consent to *analytics* does not clearly cover *applicant PII exfiltration to a third party* — a GDPR transparency risk more than an exploit.

**Remediation:** Configure `autocapture: {element_attributes: [...], mask_all_text: true}` (or disable autocapture entirely — pageviews + named events already cover product analytics), and document the capture scope in the privacy policy.

### M-5 — `x-forwarded-for` first-value trust

**Where:** `request_helpers.gleam:40-53`; consumed by consent capture (`cookie_consent_log.ip_text`), application submission (`submitted_ip_text`), payment consent audit, and Meta CAPI `client_ip` egress.

**Exploit sketch:** Behind Cloudflare the header is trustworthy (CF overwrites it). Direct-to-origin requests (`.run.app`, bypassing the Worker) can spoof it: an attacker forges evidentiary IPs in consent/audit records and injects an arbitrary IP into Meta CAPI payloads. Bounded by the X-RT-Secret origin lock — which itself has the L-19/L-20 weaknesses.

**Remediation:** Prefer `cf-connecting-ip` (unforgeable at the edge, present on all proxied requests) over `x-forwarded-for`; fall back to empty when absent rather than trusting client-supplied XFF.

### M-6 / M-7 / M-8 — PII in logs on error paths

**Where:** `ai/ai_client.gleam:1044,1170,1189,1340` (raw ADK bodies — applicant data in analysis streams); `auth/supabase.gleam:308,632,651` (raw Supabase error bodies — echo email/user metadata); `reference_checks/lookup.gleam:85-93` (raw phone to Cloud Logging + Sentry).

**Exploit sketch:** These are failure-path logs, so exposure is intermittent — but when they fire, applicant PII lands in Cloud Logging (retained per GCP defaults) and Sentry. The codebase otherwise has disciplined redaction (`redact_token_route`, CrashEvent header allowlist, masked email bodies) — these paths bypass it.

**Remediation:** Route the bodies through a scrubbing helper (truncate + strip emails/phones/tokens) before logging; log status + event id only, keep the raw body out entirely. Same one-line pattern the codebase already uses elsewhere.

## Surface coverage (acceptance #1)

| Surface | Status |
|--------|--------|
| AuthN: OAuth/PKCE, sessions, cookies, password flows, enumeration | lens-authn ✅ (parent-completed after 2 pane losses) — **strongest layer**: no Medium+ findings; A-1/A-2 Info |
| AuthZ: IDOR/ownership on every user-scoped route, internal endpoints, enumeration | lens-authz ✅ — all routes walked; no cross-tenant egress |
| Data layer: injection, FFIs, PII logs, analytics egress, DSAR scope, audit_log, retention | lens-data ✅ |
| Webhooks + payments + outbound (Stripe/Resend/Twilio/CAPI/PostHog/AI), SSRF inventory, uploads | lens-webhooks ✅ (SSRF sink inventory in lens file — no sink found) |
| SSR/render: XSS escaping integrity, attribute/context injection, public forms, CSP, static traversal | lens-ssr ✅ (dispatched lens verified scopes 1-3/6-8; parent completed referee forms + DSAR) — no Medium+ findings |
| Client SPA: bundle leakage, storage, XSS, API trust, routing, consent | lens-client ✅ |
| Secrets + config: committed secrets, env→bundle, key scoping, CORS | lens-infra ✅ + parent ✅ (no committed secrets found) |
| Dependencies + infra: npm audit, CI/CD permissions, Docker, Terraform, Worker, admin endpoints | lens-infra ✅ |

## Verification appendix (parent pass)

- Re-read source at every cited `file:line` for all Medium findings and most Low. Adjustments made: L-4 (W-2) Medium→Low (metadata server-authored; sku cross-check exists), L-6 (W-4) Medium→Low-Medium (Svix verified; email-borne vector), L-10 (client F2) Medium→Low (server skip-list by-design; SameSite=Lax holds), M-3 citation corrected to iam.tf:86-103.
- Parent-verified CLEAN: `/static/*` path traversal (stdlib `uri.path_segments` splits raw, no percent-decode, RFC dot-segment removal); `require_internal_secret` (`secure_compare`, empty→500 fail-closed); no committed secrets; Sentry CrashEvent header allowlist; Squirrel parameterization; upload magic-byte validation; document-download ownership + 15-min signed URLs.
- Lens artifacts (full evidence per finding): `lens-authz.md`, `lens-authn.md` (parent-completed after two pane losses — model cap, then reclamation), `lens-webhooks.md`, `lens-data.md`, `lens-client.md`, `lens-infra.md`, `lens-ssr.md` (dispatched lens + parent), and `parent-findings.md` in this directory.
