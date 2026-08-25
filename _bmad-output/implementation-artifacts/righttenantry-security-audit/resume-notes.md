# Resume notes — righttenantry-security-audit (PAUSED on model wall)

**Paused:** 2026-08-18 ~08:40Z. **Reason:** user requires `zai-coding-cn/glm-5.3`
for this security audit; glm-5.3 is provider-capped (429 code 1308) until
**~17:54:28Z**. The v4-pro lens swarm was halted by pause order. Nothing is
lost; this directory is the head-start for the resume.

**Resume at:** glm-5.3 cap reset (~17:54:28Z). Launch model MUST be
`zai-coding-cn/glm-5.3` (full provider-qualified path).

## State of the audit

Repo: RightTenantry worktree `/Users/moses/.herdr/worktrees/RightTenantry/security-audit`
@ develop `17d5f32` (analytics-568-617 merge head). Read-only; no product
code touched, no PR, no commits.

### Lenses completed (5 of 7) — findings preserved in this dir

| Lens | File | Status | Highlights |
|------|------|--------|-----------|
| authz | `lens-authz.md` | ✅ done | 3 Low (F1 auto_close_vacancy unowned write; F2 URL vacancy_id never bound to application on PATCH/status + reference start/skip/re-enable; F3 archived vacancy keeps serving landlord name+address on /apply). No Critical/High, no cross-tenant egress. |
| webhooks | `lens-webhooks.md` | ✅ done | 2 Medium (W-1 checkout.session.completed ignores payment_status; W-2 unlock keyed off metadata.vacancy_id not cross-checked), 4 Low (W-3 Host-header → success/cancel_url open redirect; W-4 inbound-email auto-reply is unauthenticated un-rate-limited mail relay; W-5 no refund/dispute handling; W-6 signature parser only first v1=; W-7 amount/currency not verified), 2 Info. |
| data | `lens-data.md` | ✅ done | SQL injection architecturally impossible (Squirrel). 4 Medium PII-in-logs (F1 XFF spoof; F2 ADK parse-fail logs raw body; F3 Supabase error bodies; F4 Twilio logs phone), 6 Low (digest logs email; dev-branch erasure URL log; DSAR third-party PII; IP non-PII in audit_log; typst meta unescaped; account-delete TOCTOU). FFIs clean. |
| client | `lens-client.md` | ✅ done | 2 Medium (F1 PostHog autocapture no text masking on dashboard; F2 logout/password-reset POSTs omit CSRF header), 3 Low (F3 checkout_url location.assign no scheme/host allowlist; F4 Stripe session_id briefly in pageview; F5 14 JS-FFI sites — approval self-asserted). |
| infra | `lens-infra.md` | ✅ done | 2 Medium (INFRA-01 documented edge rate limits login/signup/apply DO NOT EXIST; INFRA-02 deploy SA has projectIamAdmin = CI compromise → full GCP takeover), 6 Low, 2 Info. npm audit: 2 high, 0 crit (nanoid/postcss, build-time only). |

### Lenses NOT completed (2 of 7)

- **lens-authn** (pane was `w1T:p22W`) — was mid-investigation, no file written.
  Leads captured from transcript: Cloudflare worker auth-write rate-limit config
  (`deployment/cloudflare-worker/worker.js:584-588` — comment "Deliberately
  omitted" the auth write paths), `SECRET_KEY`/`INTERNAL_SECRET` env handling
  (`server.gleam`). Full scope in briefing `righttenantry-security-audit-lens-authn.md`.
  **MUST re-run on resume.**
- **lens-ssr** (pane was `w1T:p22Y`) — was mid-investigation, no file written.
  Leads captured: `robots.txt`/`llms.txt` info surface, index.html nonce wiring
  (Dockerfile:108/144/145 grep guards), static inventory (fonts only, no user
  content), PostHog `is_key_char` validation. Full scope in briefing
  `righttenantry-security-audit-lens-ssr.md`. **MUST re-run on resume.**

### Parent minion's own verified findings

`parent-findings.md` — recon map + my verified CLEAN verdicts (static path
traversal safe; internal-secret gate constant-time/fail-closed) + my findings
(Host→Stripe redirects, RT_CLOUDFLARE_SECRET default, XFF trust, CSP
report-only, same-site consent guard, RESEND empty-in-prod). Dedupe against
the lens files on merge.

## What remains on resume

1. Re-run lens-authn + lens-ssr on glm-5.3 (briefings already carry the
   correct Model-policy override line — update back to glm-5.3).
2. **Parent re-verification pass** — per AGENTS.md "Reviewing review output":
   re-read the actual source at every cited `file:line` from all 7 lenses
   before trusting (reviewer agents misread; agreement ≠ verification).
3. Dedupe + merge parent findings with lens findings; assign final severity.
4. Write `security-audit-report.md` (severity-ranked table + triage columns
   fix-now / schedule / accept-risk + exploit sketches + remediation).
5. **lavish** presentation (MANDATORY) — build HTML, serve, foreground-poll
   for the user's triage verdicts; record verdicts verbatim.
6. Preserve report + all artifacts to this dir (already here).
7. `herdr notification show "righttenantry-security-audit" --body "<counts by
   severity + report path>"` (durable completion signal).
8. Ledger self-report `done`.

## Do-NOT on resume

- No fixes, no dependency upgrades, no config changes, no PR (pr_review=0,
  audit deliverable). READ-ONLY on product code.
- If anything ACTIVELY dangerous (leaked live secrets) is found, flag in the
  notification body for immediate escalation.
