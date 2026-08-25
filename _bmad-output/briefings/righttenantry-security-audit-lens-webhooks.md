# Lens briefing — security-audit / WEBHOOKS + PAYMENTS + OUTBOUND (Stripe, Resend, Twilio, CAPI, SSRF, injection)

- **Job:** righttenantry-security-audit (mega-minion lens; parent minion audits the repo)
- **Model policy:** `deepseek/deepseek-v4-pro` (glm-5.3 provider-capped 429 code 1308 until 17:54:28Z — sanctioned fallback per the playbook's fallback chain; briefing override).
- **Repo/worktree (READ-ONLY):** `/Users/moses/.herdr/worktrees/RightTenantry/security-audit` @ develop (17d5f32)
- **Skill:** `bmad-review-edge-case-hunter` — exhaustive path/boundary enumeration; report only unhandled conditions, each verified against the code. Attitude: none — mechanism only.
- **Output:** write findings to `/Users/moses/code/_bmad-output/implementation-artifacts/righttenantry-security-audit/lens-webhooks.md`, then end with a one-paragraph summary in your pane.

## Ground rules

- READ-ONLY: no edits, no commits, no installs, no pushes. Do not spawn sub-agents.
- Stack: Gleam/Wisp on Cloud Run; Stripe Checkout + webhook; Resend outbound email + Resend inbound webhooks (Svix); Twilio SMS (RC3.x); Meta CAPI + PostHog analytics; ADK AI service on Cloud Run (GCP identity token auth).
- Evidence discipline: every finding = severity (Critical/High/Medium/Low/Info) + `file:line` + trigger condition + exploit sketch + remediation + confidence. Verify against actual code. A false positive is a failure.

## Scope

1. **Stripe webhook** (`server/src/payment/webhook_handler.gleam`, `stripe_webhook.gleam`, `payment/sql.gleam`): signature verification (constant-time compare? tolerance window vs replay?); event dedup (same event id twice); which events unlock a vacancy — is the amount/currency/price_id verified against the expected price, or does any `checkout.session.completed` unlock? Metadata trust (vacancy_id from metadata — can a crafted session for vacancy A unlock vacancy B?); refund/dispute events; `payment_handler.handle_create_checkout` + `handle_create_extension_checkout`: the router passes `origin_host` from the **Host header** (`request.get_header(req,"host")`, default righttenantry.ie) — trace exactly where origin_host flows (success_url? cancel_url? Stripe metadata?) and whether Host-header injection can poison redirect URLs or leak the Stripe key; amount computed server-side or client-supplied? `handle_verify_payment` (Pixel verify) — what it exposes.
2. **Resend inbound email webhook** (`server/src/inbound_email/inbound_handler.gleam` + module): Svix signature verification method, replay, timestamp tolerance; parsing of inbound addresses (per-vacancy reply-to mapping — can a crafted From/reply-to attach an email to the WRONG vacancy/application?); email header injection in any outbound reply (names, subjects); `handle_bulk_invite` + `handle_remind_applicants`/`handle_remind_applicant` — recipient validation, header injection via vacancy/user-entered strings, enumeration via timing/responses.
3. **RC3.6 delivery webhooks** (`server/src/reference_checks/webhooks.gleam` — `/webhooks/resend-events`, `/webhooks/twilio-sms`): signature verification for BOTH providers; what state transitions the webhook can drive (can an unauthenticated POST mark a reference call answered/objection?); payload trust (phone numbers, statuses); `notification/twilio_webhook.gleam` if separate.
4. **Outbound clients**: `notification/email_client.gleam` (Resend), `notification/sms_client.gleam` (Twilio — status_callback_url fixed?), `meta/meta_client.gleam` (CAPI — what PII fields ship; consent gating call sites), `posthog/posthog_client.gleam` (event fields — IPs? emails?), `ai/` job orchestration (GCP identity token — token audience, where the AI service URL comes from). Explicit HTTP timeout presence per AGENTS.md lint is NOT your concern — security impact only.
5. **SSRF inventory**: every outbound fetch whose URL/host/path incorporates request-derived data (Host header, webhook payloads, redirect params, vacancy origin_domain — where is origin_domain used? validated?). Enumerate each with source→sink and verdict.
6. **Uploads** (`server/src/storage/`): Supabase Storage upload path — content-type/extension validation, size caps (middleware caps body at 22MB — per-file limits?), path construction from user input, signed-URL minting in `application_detail_handler.handle_document_download` (expiry, bucket scope).

## Deliverable format

Markdown: summary paragraph, findings table (id, severity, title, file:line, confidence), then one section per finding with trigger condition + evidence (code quotes) + remediation. Include a short SSRF sink inventory table even where clean, and list verified-clean surfaces.
