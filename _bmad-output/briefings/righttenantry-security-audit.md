# Briefing — righttenantry-security-audit (full-codebase vulnerability scan)

- **Job id:** `righttenantry-security-audit`
- **Repo:** RightTenantry · **Base:** `develop` @ latest (Silas resolves the exact
  sha at dispatch) · **Slug:** `security-audit`
- **Model policy:** `zai-coding-cn/glm-5.3` (USER RULING 2026-08-17 night — the
  full provider-qualified path is MANDATORY; bare glm labels misroute). Any
  mega-minion you spawn launches with the same model — name it explicitly at
  every spawn.
- **Skills policy:** `bmad-review-adversarial-general` (cynical review posture)
  + `bmad-review-edge-case-hunter` (boundary conditions) — this is a REVIEW
  job, not a build job. Fan-out lenses (if any) use the same skills per lens.
  **`lavish` is MANDATORY for the findings report** — severity-ranked, triage
  columns, the user annotates fix-now/shelf decisions in the browser.
- **Perkins:** `pr_review: 0` — **NO PR. This is an audit deliverable** (a
  report), not a code change. Do not modify product code; do not open a PR.
- **Completion signal (NO-PR JOB — mandatory):** on finish, run
  `herdr notification show "righttenantry-security-audit" --body "<one-line:
  findings count by severity + report path>"` — this is the durable completion
  signal. ALSO preserve the report + all artifacts to
  `/Users/moses/code/_bmad-output/implementation-artifacts/` BEFORE any
  sweep (worktree dies, artifacts live).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start;
  badge-out your field-notes shard per standing orders.
- **Prior art to carry (known sightings — verify, don't assume):** a Supabase
  security-definer view bypassing RLS was flagged once (Perkins r1 on PR #556,
  2026-08-01, "single sighting, still watching") — check that class
  specifically. OAuth/PKCE + short-lived cookie across the redirect (recent
  #617 work), Meta CAPI consent-gated inserts (#568/#583) — these surfaces are
  recently touched; scan them with fresh eyes.

## Mission — full-codebase security vulnerability scan

**The goal:** an adversarial, evidence-backed vulnerability audit of the
RightTenantry codebase at the dispatch sha — every severity-ranked finding
carries file:line evidence, an exploit sketch, and a proposed remediation.

**Scan surfaces (OWASP-flavored, adapted to this stack — investigate the
actual stack first, don't assume):**

1. **AuthN/AuthZ:** the OAuth + PKCE flow (state validation, redirect-uri
   handling, the short-lived cookie across the redirect), session management,
   token storage, IDOR on every user-scoped endpoint (object ownership checks,
   not just authentication).
2. **Data layer:** RLS enforcement (the security-definer class — every view/
   function that elevates), injection (SQL/raw query construction), PII
   exposure in logs/API responses, analytics payload leakage.
3. **Input/output:** XSS (render paths, any HTML construction), CSRF (state-
   changing endpoints), SSRF (any URL fetched from user input — webhooks,
   CAPI, redirects), file/upload handling if present.
4. **Secrets + config:** committed secrets/keys, env vars leaking to client
   bundles, API-key scoping (PostHog/CAPI/OAuth app secrets), CORS config.
5. **Dependencies + infra:** run the dependency auditor for the actual
  toolchain (`npm audit` / equivalent — report-only, do NOT upgrade anything);
  CI/CD pipeline permissions; any admin/debug endpoints exposed.
6. **Rate limiting / abuse:** auth endpoints, public APIs, expensive
   operations (unbounded queries, enumeration vectors).

**Method:** static analysis + adversarial manual review; fan out per-surface
lenses if useful (same model, named explicitly). Evidence discipline: every
finding = severity (Critical/High/Medium/Low/Info) + file:line + exploit sketch
+ remediation proposal + confidence. False-positive discipline: verify each
finding against the code before reporting (the Perkins 5/5 standard) — a
padded report is a failed report.

**Deliverable:** `security-audit-report.md` (+ raw lens artifacts) preserved to
`_bmad-output/implementation-artifacts/`, presented via **lavish** — severity
table, exploit sketches, triage columns (fix-now / schedule / accept-risk) for
the user's annotations.

**Routing after the verdict:** per the user's lavish triage — Critical/High
findings become follow-up fix jobs (batched per the one-issue-per-repo
doctrine, #607 RT unless the severity justifies its own); nothing gets fixed
in this job.

**Acceptance:**

1. Every scan surface covered or explicitly n/a'd with reason.
2. Every finding evidence-backed, severity-ranked, verified non-false-positive.
3. Lavish session passed with the user's triage verdicts recorded verbatim in
   the report.
4. Report + artifacts preserved to implementation-artifacts/; the notification
   fired; ledger self-report with the counts.

**Scope guard:** READ-ONLY on product code. No fixes, no dependency upgrades,
no config changes, no PRs. If you find something ACTIVELY dangerous (leaked
live secrets), flag it in the notification body for immediate escalation
instead of sitting on it.

## Dispatch parameters

```
repo: RightTenantry
repo_root: /Users/moses/code/RightTenantry
slug: security-audit
base: develop
model: zai-coding-cn/glm-5.3
pr_review: 0
```
