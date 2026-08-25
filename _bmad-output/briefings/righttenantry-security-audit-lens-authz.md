# Lens briefing — security-audit / AUTHZ (IDOR + ownership + internal endpoints)

- **Job:** righttenantry-security-audit (mega-minion lens; parent minion audits the repo)
- **Model policy:** `deepseek/deepseek-v4-pro` (glm-5.3 provider-capped 429 code 1308 until 17:54:28Z — sanctioned fallback per the playbook's fallback chain; briefing override).
- **Repo/worktree (READ-ONLY):** `/Users/moses/.herdr/worktrees/RightTenantry/security-audit` @ develop (17d5f32)
- **Skill:** `bmad-review-adversarial-general` — cynical posture; every claim verified against disk before reporting.
- **Output:** write findings to `/Users/moses/code/_bmad-output/implementation-artifacts/righttenantry-security-audit/lens-authz.md`, then end with a one-paragraph summary in your pane.

## Ground rules

- READ-ONLY: no edits, no commits, no installs, no pushes. Do not spawn sub-agents.
- Architecture context: Gleam/Wisp server; Supabase Postgres via Squirrel-generated queries (`server/src/<module>/sql/*.sql`); app connects with a privileged role (service-role — RLS is bypassed), so **application-level ownership filters in SQL are the ONLY tenant boundary**. Client SPA is untrusted.
- Sessions: `session_middleware.require_session` yields `Landlord` (id). Route params arrive as strings.
- Evidence discipline: every finding = severity (Critical/High/Medium/Low/Info) + `file:line` (worktree-absolute or repo-relative) + a concrete exploit sketch (who can do what) + remediation + confidence. Verify each finding against the actual code path end-to-end (route → handler → SQL). A false positive is a failure. If a surface is clean, say so explicitly with what you checked.

## Scope — IDOR / ownership enforcement

Walk EVERY authenticated route in `server/src/router.gleam` and verify the object-ownership chain:

1. Vacancy-scoped nested resources: application detail GET/PATCH status/open/bulk-reject, documents download, reference-checks start/skip/re-enable/take-over/correct/substitute (call_id!), AI job GET, scoring-status, compare, bulk-invite, remind-applicant(s). For each: does the handler verify the vacancy belongs to `landlord.id` BEFORE acting, and does it verify the nested object (application, document, ai job, reference call) belongs to that vacancy? Read the actual SQL (`server/src/*/sql/*.sql`) — confirm the `user_id`/owner filter is in the QUERY, not just a prior check (both matter: TOCTOU and depth). Flag any handler that loads by bare id without an owner join/where.
2. Direct-id resources: notifications (`/notifications/:id/read`), AI analyses pdf (`/ai/analyses/:id/pdf` — can landlord A fetch landlord B's report?), payment status/verify/consent, settings, billing history/invoices. Same standard.
3. Cross-tenant writes: PATCH vacancy, close/archive/restore/publish, reference-check actions — verify ownership in the UPDATE itself where possible.
4. UUID parsing: are ids parsed as UUIDs before hitting SQL (type-safe) or passed raw? Check what Squirrel emits for `$1::uuid` params.
5. **Internal endpoints** (`/api/v1/internal/digest`, `/internal/lifecycle/verification-reminders`, `/internal/reference-checks`): read `server/src/notification/digest_handler.gleam`, `lifecycle/verification_reminder_handler.gleam`, `reference_checks/sweep_handler.gleam` — how is `INTERNAL_SECRET` compared (constant-time? plain ==?); behavior when the secret is empty string (config allows "" in dev — what about prod?); what do these endpoints DO if hit (email blast? data egress?).
6. Enumeration/unbounded ops: list endpoints without pagination caps (vacancies, applications, notifications, billing) — max rows; `/apply/:code` invalid-code responses (uniform?); any endpoint that can be driven to expensive work without auth (compare, scoring-status).
7. Stripe webhook + checkout interplay is OUT of scope (another lens), but `payment_handler` ownership checks (verify, consent-check, status) are IN scope.

## Deliverable format

Markdown: summary paragraph, findings table (id, severity, title, file:line, confidence), then one section per finding with exploit sketch + evidence (code quotes) + remediation. Explicitly list the routes you verified CLEAN (one line each: route → ownership mechanism).
