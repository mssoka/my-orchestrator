You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
# RightTenant — Development Standards

Always use the herdr skill for sub agents spawns

**RightTenant** is an AI-powered tenant vetting tool for self-managing landlords. Gleam/Lustre monorepo (client SPA + Wisp API + shared types). AI agents live in `~/code/RightTenantryAgents` (Python ADK on Cloud Run).

## Project Status: live (launched June 2026)

RightTenant is in production — real landlords are using it and paid ads are driving live traffic. Pre-launch latitude ("delete cleanly, rename freely") is gone. URLs, API shapes, email content, and session cookies are contracts that real users depend on.

### Backward compatibility is load-bearing

Any change that breaks an existing contract MUST be flagged in the PR title or description (use a `BREAKING:` prefix or a dedicated **Breaking change** section explaining the impact and migration path), and MUST follow expand-then-contract:

1. Ship the new shape alongside the old. Dual-read/dual-write.
2. Migrate callers and stored data forward.
3. Remove the old shape in a later deploy, once the previous Cloud Run revision can no longer roll back to it.

Contracts that are load-bearing — real users and external systems depend on each one:

- **Database schemas** — already expand-only (see Migrations below). The previous Cloud Run revision must keep working against the new schema.
- **API request/response shapes** — `shared/` JSON codecs and route handlers. A client tab opened yesterday must still work today; SPA bundles are cached.
- **URL routes** — especially `/apply/:code` (bookmarked, emailed, printed on flyers). 301-redirect on rename; never 404 a route that was live.
- **Email content** — Resend inbound reply-to format, outbound template links, footer copy referenced from sent mail that's already in landlord inboxes.
- **Stripe** — webhook event handling, metadata keys, `STRIPE_VACANCY_PRICE_ID`. In-flight Checkout sessions must still resolve.
- **Session cookies and CSRF tokens** — invalidating live sessions logs everyone out; rotate via dual-accept windows.
- **`audit_log` row shape** — compliance and DSAR exports read historical rows; columns are append-only.

A single-deploy compat break is rare and must be explicitly justified in the PR description (e.g. "this endpoint has zero callers; grepped `shared/` and `client/`").

### Defended invariants are gating

Audit-on-state-change, CSRF, free-tier counter, session forgery resistance, Stripe webhook validity, and `/apply` consent capture block the deploy regardless of frequency.

When triaging, the question is **"will this gap hit a real landlord today, or break a contract a future deploy depends on?"** Both block. Phantom edge cases still stay deferred.

## Core Principles

### No JavaScript FFI

JavaScript FFI is **PROHIBITED** unless explicitly approved by Moses. Use approved packages:

| Need | Package |
|------|---------|
| Time | `gleam_time` |
| Storage | `plinth/browser/storage` |
| DOM | `plinth/browser/document` |
| HTTP | `rsvp` (client), `wisp` (server) |
| Routing | `modem` (client SPA) |

Server-side **Erlang** FFI is fine and in active use (`db_ffi.erl`, `session_cache_ffi.erl`, `audit_report_ffi.erl`, etc.). The ban is JavaScript-only.

### No `let assert` in Production

`let assert` crashes the BEAM process — use `case` with explicit error handling. Acceptable only in test files.

### Explicit HTTP timeouts

Every outbound HTTP call in `server/src` must set an explicit timeout via `httpc.configure() |> httpc.timeout(<ms>)` with `httpc.dispatch`/`dispatch_bits` — never bare `httpc.send`/`send_bits` (they inherit gleam_httpc's 30s default). Size it to the call: 10s where a fast fail is safe (auth, fire-and-forget analytics, best-effort cleanup), 30s where a timeout is terminal or payload-bearing (uploads, doc signing that feeds AI scoring, inbound-email fetch). A `pr-checks`/`test.yml` grep lint enforces this alongside the `let assert` ban — so a rationale comment must never contain the literal `httpc.send`.

### No Technical Debt

Implement completely or defer entirely. No placeholders, mock functions, TODOs, or "cleanup later" comments. Every feature must handle error cases, edge cases, and integrate properly.

### No Hardcoded Data

All data displayed in the UI must come from the database via API endpoints. Exceptions: UI labels, route paths, CSS, icons, defaults during loading, and score badge thresholds.

New feature workflow: SQL file → `bash run_squirrel.sh` → API endpoint → client fetch.

### In-App Copy Voice (Landlord-Centric)

All user-facing text must follow the brand voice in `_bmad-output/story-2026-04-03.md`. Calm confidence. Specific, not vague. Outcomes, not technology.

- **Never** expose raw server/API error strings — wrap in friendly copy
- **Never** use "Error", "Failed", or technical language — use "Couldn't" or "Something didn't work"
- Use contractions naturally ("couldn't", "didn't", "it's")
- Toasts: one sentence. Error pages: two sentences max.
- Empty states must guide the landlord to the next action

| Do | Don't |
|----|-------|
| "Couldn't load this vacancy. Give it another go." | "Failed to load vacancy" |
| "Something didn't work — try again in a moment" | Raw `err` variable displayed |
| "No notes yet. Jot down your impressions after a viewing." | "No notes yet" |
| "Try again" | "Retry" |

## Architecture

Lustre full-stack SPA monorepo:

- **`shared/`** — Types and JSON codecs (target: erlang)
- **`client/`** — Lustre SPA with MVU, landlord dashboard (target: javascript)
- **`server/`** — Wisp/Mist JSON API + SSR public application form (target: erlang)
- **`_bmad-output/`** — Planning artifacts, research, brainstorming

The public application form (`/apply/:code`) is SSR, not part of the SPA. The SPA handles only authenticated landlord routes.

### Server module map (`server/src/`)

Top-level wiring: `server.gleam` (entry), `router.gleam` (route table), `middleware.gleam` (auth/CSRF/rate-limit), `config.gleam`, `compliance.gleam`, `domain_helpers.gleam`, `http_origin.gleam`, `response_helpers.gleam`, `ssr_response.gleam`.

Domain folders (each owns its handlers, services, SQL, and `*_ffi.erl` if any):

| Folder | Purpose |
|--------|---------|
| `account/` | Landlord profile, signup, free-analyses counter |
| `ai/` | ADK job orchestration, polling endpoint, score storage |
| `application/` | `/apply/:code` SSR form, submission, consent capture |
| `audit/` | Tiered audit_log writes (fail-closed Tier 1, fail-open Tier 2) |
| `auth/` | Sessions, password reset, Supabase GoTrue integration |
| `billing/` | Pricing display, free-tier gate |
| `dsar/`, `erasure/`, `retention/` | GDPR data subject access, deletion, retention jobs |
| `inbound_email/` | Resend inbound webhooks (per-vacancy reply-to) |
| `legal/` | Static legal page handlers |
| `notification/` | Outbound email (Resend) |
| `payment/` | Stripe Checkout + webhook, vacancy unlock, burst-scoring trigger |
| `sentry/` | Sentry event sink |
| `storage/` | Supabase Storage uploads (application docs) |

### Client (`client/src/`)

Standard Lustre MVU shape — every new page follows it:

- `client.gleam` — entry
- `model.gleam` / `msg.gleam` — central state and `SubjectVerbObject` messages
- `router.gleam` — modem routes
- `pages/` — one module per route
- `components/` — shared widgets
- `api/` — `rsvp` calls, JSON decoders
- `helpers/` — formatters, predicates
- `copy.gleam` — **all** landlord-facing strings live here (toast/error/empty-state copy). Brand-voice rule lives or dies on this file; never inline strings in a view.

### AI Integration

The main app communicates with AI agents via Agent Engine managed API — two-step flow (create session → stream query via SSE). AI analysis auto-triggers on application submission. Client polls `GET /api/v1/ai/jobs/:id` every 5-10s. The main app never imports or depends on ADK. Auth via GCP identity token.

## Database

### Squirrel (MANDATORY)

Always use Squirrel for type-safe SQL. Never hand-write query code.

1. Write SQL in `server/src/<module>/sql/*.sql` (one query per file)
2. Run `bash run_squirrel.sh`
3. Import: `import <module>/sql`

**Timestamp handling:** Squirrel doesn't support `timestamptz` directly.
- Output: cast to `::text` (lowercase only, never `::TEXT`)
- Input (nullable): `CASE WHEN $1 = '' THEN NULL ELSE $1::timestamptz END`
- Input (required): `$1::timestamptz` (pass as TEXT string)
- Use `""` for NULL optional timestamps

**Troubleshooting:** If Squirrel fails, investigate the SQL — it's almost always a syntax issue. Known limitation: `inet` unsupported, use `$1::text::inet` double cast.

### Migrations

1. **Author** a new migration in `supabase/migrations/<YYYYMMDDHHMMSS>_<snake_name>.sql`. The 14-digit prefix is enforced by `pr-checks.yml`.
2. **Apply locally** via `make test-db-reset` (replays the full chain against the test DB).
3. **Run Squirrel** (`bash run_squirrel.sh`) so generated query code stays in sync.
4. **Deploy.** Merging to `staging` runs migrations against staging via GitHub Actions (`supabase db push --include-all`) before Cloud Run flips. Merging to `main` does the same for production.

Conventions:
- Use `IF NOT EXISTS` / `IF EXISTS` for idempotency.
- **Expand-only.** Additive changes (`ADD COLUMN`, new tables, enum extensions) deploy in a single PR. Destructive changes (`DROP COLUMN`, `RENAME COLUMN`, type changes) must split across two deploys: first stop reading/writing the old shape, then drop. `pr-checks.yml` warns on destructive ops as a reminder.
- **No rollback.** Migrations are forward-only. On a failed deploy, the Cloud Run image rolls back; the schema stays at the new state. The previous code revision must remain compatible with the new schema — that's why expand-only is mandatory.
- **Never** edit a migration file once merged. Author a new migration that supersedes it.

## Code Style

### Patterns

- Prefer pipelines: `input |> string.trim |> validate |> result.map(create)`
- Prefer `use` expressions over nested callbacks
- All fallible operations return `Result`. All public functions have explicit type signatures.
- Use `gleam/dynamic/decode` for JSON parsing

### Naming

- Files/functions: `snake_case`
- Types: `PascalCase`
- Messages: `SubjectVerbObject` — `UserClickedLogout`, `ApiReturnedVacancies(Result)`, `BrowserChangedUrl(Uri)`, `AppRequestedVacancies`
- Views: `view_` prefix

### Module Organization

1. Main public view first
2. Major sections
3. Sub-components
4. Helper functions last

Target: <200 lines for logic modules, <400 lines for view modules.

### Code Quality

- DRY: extract helpers when logic repeats 2+ places
- Keyed elements for all dynamic lists with stable IDs
- `data-testid` on all interactive UI elements
- Labelled arguments on public functions
- Do NOT use `--minify` flag on Lustre builds (Bun tree-shaking breaks message handlers)

## Build & Test

```bash
make dev              # Build client + start server (port 4000), watchexec rebuild on .gleam/.css/.html
make build            # Compile client and server
make build-client     # Compile Lustre SPA to server/priv/static/ (also builds Tailwind)
make build-server     # Compile server only
make docker-build     # Build production image, pinned to linux/amd64 (M-series builds break without it)
make format           # Run gleam format across shared/client/server
make tailwind         # Build Tailwind CSS once → server/priv/static/tailwind.css
make tailwind-watch   # Rebuild Tailwind on change
make deps             # gleam deps download for shared/client/server
make test             # Unit tests only — shared, client, server (no Docker)
make test-all         # Unit + integration tests (requires test-db-up)
make test-shared      # Shared package tests
make test-client      # Client tests (use this, not `cd client && gleam test`)
make test-server      # Server unit tests (integration skipped)
make test-integration # Server integration tests only (requires test-db-up)
make test-db-up       # Start Docker Postgres (docker-compose.test.yml) + run migrations
make test-db-down     # Stop Docker Postgres
make test-db-reset    # Drop + re-migrate test database
make kill             # Kill any process on port 4000
make retention-run    # Run the retention_job Cloud Run Job locally (needs .env)
```

**`make build-client` post-processes `server/priv/static/index.html`** with `perl -i` passes: title, favicons, Tailwind link, and a PostHog snippet (reads `POSTHOG_API_KEY` from `.env`; warns and disables PostHog if absent). HTML scaffolding changes belong in the Makefile, not in client source — the client build overwrites `index.html` on every run. **The Dockerfile mirrors this perl chain for deployed images** (deploys run `docker build`, never the Makefile) — any new `index.html` pass must be added in BOTH places, plus an entry in both snippet-regression guards.

### Pre-PR Discipline (MANDATORY)

Before opening or pushing to a PR, always run:

```bash
make format && make test && make build
```

CI's format-check fails on any unformatted file in the repo — including pre-existing drift on the base branch. `make format` is idempotent; running it locally catches that drift before the remote does. Never skip this step "because I only touched X" — the check is repo-wide.

Tests defend named regressions. If a change doesn't introduce a regression worth catching — or the types, compiler, or an existing test already catch it — ship it without a new test. Coverage percentages, tier ladders, and "every function needs a test" rules are not useful here. Always use `gleam add` for dependencies — never edit gleam.toml manually.

### Reviewing review output (MANDATORY)

When running `/code-review`, `/review-plan`, or any other multi-agent review flow, **read the actual source at every cited `file:line` before acting on a finding**. The reviewer agents have short read windows and routinely report problems that don't exist, miss guards that are already in place, or misread control flow. Multiple reviewers agreeing on the same hallucination is normal — agreement is not verification.

- Blocker / warning / note: open the file. Verify the claim.
- "X is missing" claims: grep the module *and* its imports — the guard the reviewer thought was missing is often one hop away.
- When a finding turns out to be a false positive, say so explicitly when reporting; don't proceed to "what fix do you want" for a problem that doesn't exist.
- Accuracy and context beat speed. Auto-fixing a non-existent bug is worse than skipping a real one.

### Test Framework

- **Runner:** unitest (server), gleeunit (client, shared)
- **Assertions:** `gleeunit/should` across all packages
- **Integration tests:** Tagged with `use <- unitest.tag("integration")` and split per feature in `server/test/integration/<feature>_integration_test.gleam` (e.g. `ai_integration_test.gleam`, `vacancy_integration_test.gleam`). Skipped by default, run only via `make test-integration` or `make test-all`.
- **E2E:** `/bug-hunt` skill (YAML scenarios in `.pi/skills/bug-hunt/scenarios/` via agent-browser; requires `make dev` for local runs, or pass `staging` for the Cloud Run staging env)

### Test Conventions

- Unit tests go in `server/test/<module>/<module>_test.gleam`
- Integration tests (DB-dependent) live in `server/test/integration/`, split per feature as `<feature>_integration_test.gleam`. Shared helpers are in `helpers.gleam` and `test_db.gleam` in the same directory.
- Every integration test must start with `use <- unitest.tag("integration")`
- `data-testid` on all interactive UI elements (used by bug-hunt E2E scenarios)

### Invariants That Must Stay Defended

These don't prescribe how — whichever test (unit, integration, or bug-hunt) catches them is fine, and many are already pinned. But if a change would weaken one of these and no existing test would fail, add the smallest test that would.

- Protected characteristics never influence AI score.
- Stripe webhook only unlocks a vacancy when the payment is valid and matches the vacancy.
- Free-tier counter (3 analyses) cannot be bypassed.
- `/apply/:code` submissions persist with `consent_record`.
- Sessions cannot be forged.
- Audit-log writes fire on AI decisions, status changes, and payments.

### CI Pipeline

PR checks and deploys run `test.yml` which has two parallel jobs:
1. **unit-test** — format, `let assert` lint, `make test`, `make build`
2. **integration-test** — Postgres 16 service container, migrations, `gleam test -- --tag integration`

Both must pass before merge or deploy.

### Auto-Commit Policy

Commit and push when a story or epic is marked `done` in sprint status.

## Environment

Call `dot_env.load_default()` first in `main()`. Required env vars:

```
DATABASE_URL                  # Supabase transaction pooler (port 6543)
SQUIRREL_DIRECT_DATABASE_URL  # Squirrel code generation
STRIPE_SECRET_KEY             # Payments
STRIPE_WEBHOOK_SECRET         # Webhook verification
STRIPE_VACANCY_PRICE_ID       # Per-vacancy product price ID
RESEND_API_KEY                # Email sending
RESEND_WEBHOOK_SECRET         # Svix signing secret for inbound email
SUPABASE_ANON_KEY             # Supabase GoTrue auth (public anon key)
AI_SERVICE_URL                # Cloud Run ADK service URL (both agents)
GCP_SERVICE_ACCOUNT_JSON      # Production only: GCP auth
SECRET_KEY                    # Session signing
INTERNAL_SECRET               # Digest endpoint auth (separate from session signing)
```

## Deployment & Infrastructure

All services on Google Cloud Run (`europe-west1`). Single domain: `righttenantry.ie`. Legacy domains (`righttenantry.com`, `righttenantry.co.uk`, `righttenantry.eu`) 301-redirect to `.ie` via Cloudflare.

Each vacancy stores `origin_domain` (always `righttenantry.ie` in production). Localhost and Cloud Run `.run.app` URLs pass through for dev/staging.

### Terraform (MANDATORY for GCP infrastructure)

All GCP infrastructure must be managed via Terraform in `deployment/terraform/`. Never create GCP resources manually — define them in Terraform and apply. This includes:
- Service accounts and IAM bindings (`iam.tf`)
- Workload Identity Federation (`wif.tf`)
- Artifact Registry (`artifact-registry.tf`)
- Secret Manager secrets (`secrets.tf`)

Secret **values** are set via `deployment/sync-secrets.sh` (reads from `.env`), not Terraform.

Cloud Run **service deployment** is handled by GitHub Actions (`deploy-cloudrun@v2`), not Terraform. Terraform manages the surrounding infrastructure.

```bash
cd deployment/terraform
terraform plan -var-file=vars/staging.tfvars    # Preview changes
terraform apply -var-file=vars/staging.tfvars   # Apply to staging
terraform apply -var-file=vars/production.tfvars # Apply to production
```

Rate limiting at Cloudflare edge: login 10/min, signup 5/hour, application submit 5/hour per IP. Anti-fraud on public form: honeypot fields, timing validation (<2s = suspicious).

## Business Rules

### Pricing & Gating

- Signup free. First 3 AI analyses free per account (lifetime).
- EUR 299 per vacancy unlocks unlimited AI analysis for that vacancy.
- No subscription. Stripe Checkout (no card data stored).
- Vacancy creation unrestricted, hard cap of 20 unpaid vacancies.
- AI analysis auto-triggers on submission. After free analyses exhausted, applications queue unscored until vacancy is paid.
- Payment triggers burst analysis of queued applications.

### Score Display

Green badge: 70+ | Amber badge: 40-69 | Red badge: 0-39

### Protected Characteristics (Equal Status Acts)

AI scoring MUST NEVER use the ten Equal Status Acts grounds: gender, civil status, family status, sexual orientation, religion, age, disability, race or ethnic origin (including colour, nationality, or national origins), membership of the Traveller community, or housing assistance (HAP, RAS, or other social welfare payments). Occupants and pets ARE legitimate criteria.

### Vacancy Archiving

Soft delete via `archived_at` timestamp. Hidden from dashboard, restorable anytime. No per-vacancy hard delete — vacancy rows are hard-deleted only by landlord account deletion; applicant PII inside a vacancy is already covered by the retention job and self-service erasure.

## Compliance

- **GDPR**: Explicit consent on application form, recorded in `consent_record` (retained 6 years; survives erasure via FK `SET NULL`). Applicants get self-service data export (`/dsar/:token`) and Art. 17 erasure (`/erase/:token`) via single-use links in their confirmation email. A daily retention job (Cloud Run Job, production-only) purges rejected-applicant PII 30 days after rejection and pseudonymises `audit_log`. Landlords delete their account via `POST /api/v1/account/delete`, gated on pending Stripe payments.
- **Audit**: All AI decisions, status changes, and payments logged to `audit_log`.
- **EU AI Act** (Aug 2026): Tenant scoring likely high-risk (Annex III). All AI output includes disclaimer. Scoring criteria transparent and explainable.

## Issue Tracking

Uses **beads** skill. All issues must include the `righttenant` label.

## Reference

- Planning artifacts: `_bmad-output/planning-artifacts/`
- Use Ref MCP (`ref_search_documentation`, `ref_read_url`) before implementing unfamiliar APIs.

---

Always use the herdr skill for sub agents spawns

## Skill locations

pi is the only agent harness for this repo. bmad skills are pi-global: canonical home `/Users/moses/code/.agents/skills/` (symlinked into `~/.pi/agent/skills/`; machine-local convention). Do not reinstall bmad skills per-repo. The `.claude/skills/bmad-*` copies were removed in this branch; the `.agents/skills/bmad-*` copies are removed separately (PR #541) — until that merges, pi may still discover those per-repo copies, but they are deprecated duplicates. `_bmad/` config remains per-repo.


--- DIFF ---
diff --git a/_bmad-output/implementation-artifacts/spec-gh-643-guide-demo-cta.md b/_bmad-output/implementation-artifacts/spec-gh-643-guide-demo-cta.md
new file mode 100644
index 00000000..dfd9fb5f
--- /dev/null
+++ b/_bmad-output/implementation-artifacts/spec-gh-643-guide-demo-cta.md
@@ -0,0 +1,98 @@
+---
+title: 'Add "Try the demo" CTA to the SSR guide template (#643)'
+type: 'feature'
+created: '2026-09-03'
+status: 'done'
+baseline_commit: 61586bbd324bcd6c817bcdb5d461b42f36d61d39
+review_loop_iteration: 0
+context:
+  - '{project-root}/AGENTS.md'
+---
+
+<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">
+
+## Intent
+
+**Problem:** /demo has zero tracked entries in 13 days because the only surface linking to it is the low-traffic SPA landing page. The SSR guides are the traffic engine (~70+ views since 08-19) and link to /demo zero times.
+
+**Approach:** Add a shared secondary "Try the demo" CTA block to the SSR content layout and render it on every `/guides/*` page, directly under each guide's closing signup CTA. Plain anchor to `/demo`, `data-testid="guide-demo-cta"`, secondary visual weight.
+
+## Boundaries & Constraints
+
+**Always:**
+- Copy block verbatim: heading "See it work before you sign up", button "Try the demo", subline "A live sandbox with a mock vacancy and ranked applications. No signup." (no exclamation marks, no em dashes, outcome-led)
+- Anchor carries `attribute("data-testid", "guide-demo-cta")` and `href="/demo"` (plain, no utm params, no new instrumentation)
+- Visual weight secondary to the signup CTA: border-only card under the shadow card, outline button mirroring `demo_cta_button` in `client/src/pages/landing.gleam`, heading `text-base` vs the primary's `text-lg`
+- Mobile-safe: the card stacks (`flex flex-col gap-5 sm:flex-row`), no horizontal scroll
+- Gleam only, SSR strings; no JS FFI, no `let assert`, no new dependencies
+
+**Ask First:**
+- Any change that would render the CTA on `/tools/*`, `/resources`, or rent-post pages (scope is `/guides/*` only)
+- Any new analytics instrumentation (demo_entry already fires on /demo entry)
+
+**Never:**
+- Restyle or alter the existing signup CTA (`inline_cta`, `cta_button`) — one primary CTA per view
+- Touch the client package (client untouched per briefing)
+- Add utm parameters or tracking wrappers to the /demo link
+
+</frozen-after-approval>
+
+## Code Map
+
+- `server/src/content/layout.gleam` -- Shared page chrome + CTA primitives. `inline_cta` (line ~349) is the card anatomy to mirror; `cta_base` (line ~35) is the primary button class; imports `lustre/attribute.{attribute}` so `attribute("data-testid", ...)` works. New `pub fn guide_demo_cta()` goes here, next to `inline_cta`.
+- `server/src/content/tenant_vetting_checklist_view.gleam` -- insert after `view_cta(),` (line ~45 of composition list)
+- Guide compositions, insert `layout.guide_demo_cta(),` right after `view_cta(),`:
+  `rtb_registration_view.gleam` (~57), `notice_periods_view.gleam` (~53), `letting_agent_costs_view.gleam` (~44), `tenant_vetting_checklist_view.gleam` (~45), `rent_increase_notice_view.gleam` (~67), `rtb_disputes_view.gleam` (~61), `property_management_fees_view.gleam` (~69), `tenancy_agreement_template_view.gleam` (~71), `landlord_reference_letter_view.gleam` (~55), `rental_income_tax_view.gleam` (~101)
+- `server/src/content/part_4_tenancy_view.gleam` -- NO `view_cta()`; its primary inline_cta sits mid-page inside `view_in_practice()`. Insert `layout.guide_demo_cta(),` after `view_sources(),` (~62), keeping `layout.advice_disclaimer(),` last as fine print.
+- `client/src/pages/landing.gleam` -- read-only pattern source: `demo_cta_button` (~line 83) supplies the outline button classes.
+- `tailwind.config.js` -- content globs include `./server/src/**/*.gleam`, so any literal class used in the new block is generated.
+- `server/src/content/content_pages.gleam` -- read-only: the 11 `/guides/*` registry entries (route coverage cross-check).
+- `server/src/content/content_handler.gleam`, `server/src/router.gleam` -- read-only: handlers/routes for the 11 guide pages; bare `/guides` 301s to `/resources#guides` (no render path, no CTA needed).
+
+## Tasks & Acceptance
+
+**Execution:**
+- [x] `server/src/content/layout.gleam` -- add `pub fn guide_demo_cta() -> Element(a)`: border-only card (`mt-4 bg-white rounded-xl border-2 border-navy/10 p-6 flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between`), heading + subline left, outline anchor right (`bg-white border-2 border-navy/15 text-navy ... hover:border-amber hover:text-amber px-6 py-3`), `href="/demo"`, `data-testid="guide-demo-cta"` -- the single shared SSR block for all guide pages.
+- [x] 10 guide views with `view_cta()` -- add `layout.guide_demo_cta(),` immediately after `view_cta(),` in the composition list -- secondary companion directly under the primary card.
+- [x] `server/src/content/part_4_tenancy_view.gleam` -- add `layout.guide_demo_cta(),` after `view_sources(),` -- closing position for the one guide without a closing signup CTA.
+
+**Acceptance Criteria:**
+- Given any of the 11 `/guides/*` routes, when the page renders, then the HTML contains an `<a href="/demo" data-testid="guide-demo-cta">Try the demo</a>` inside the demo CTA card
+- Given the same page, when inspected, then the signup CTA remains the visually primary action (amber button, shadow card, larger heading) and the demo CTA is border-only/outline
+- Given a mobile viewport, when the page renders, then the CTA card stacks and no horizontal scroll appears
+- Given `/tools/*`, `/resources`, and `/resources/:slug` pages, when rendered, then no demo CTA is present
+- Given `make build` (or `cd server && gleam build`) and the server test suite, when run, then both pass with the client untouched
+
+## Verification
+
+**Commands:**
+- `cd server && gleam build` -- expected: compiles clean
+- `make test` (or `cd server && gleam test`) -- expected: existing suite green (content_test pins guide page shapes)
+- `make run` + `curl -s localhost:4000/guides/notice-periods | grep -A2 guide-demo-cta` -- expected: anchor present in rendered HTML (env bootstrapped: server/.env symlink exists)
+- `curl -s localhost:4000/tools/rpz-calculator | grep -c guide-demo-cta` -- expected: `0` (scope guard)
+
+**Manual checks (if no CLI):**
+- Rendered HTML: demo card sits directly under the signup card; card stacks on narrow widths (flex-col below sm).
+
+## Suggested Review Order
+
+**The shared CTA block**
+
+- Design intent: border-only card, outline button lifted from the landing's secondary demo control, exact issue copy
+  [`layout.gleam:389`](../../server/src/content/layout.gleam#L389)
+
+- Button classes verbatim from landing's `demo_cta_button` so the control reads the same on both surfaces
+  [`layout.gleam:37`](../../server/src/content/layout.gleam#L37)
+
+**Wiring into the 11 guide pages**
+
+- The standard case: one line under `view_cta()` (representative; ten views identical)
+  [`notice_periods_view.gleam:54`](../../server/src/content/notice_periods_view.gleam#L54)
+
+- The exception: no closing signup CTA, so the card lands after `view_sources()`, disclaimer stays last
+  [`part_4_tenancy_view.gleam:63`](../../server/src/content/part_4_tenancy_view.gleam#L63)
+
+**Regression pin**
+
+- Renders all 11 views, asserts testid + `/demo` href each; verified by mutation (dropping one call fails CI)
+  [`content_test.gleam:1829`](../../server/test/content/content_test.gleam#L1829)
diff --git a/server/src/content/landlord_reference_letter_view.gleam b/server/src/content/landlord_reference_letter_view.gleam
index b677279f..f702d667 100644
--- a/server/src/content/landlord_reference_letter_view.gleam
+++ b/server/src/content/landlord_reference_letter_view.gleam
@@ -53,6 +53,7 @@ pub fn render(
         view_verification(),
         view_faq(),
         view_cta(),
+        layout.guide_demo_cta(),
         layout.advice_disclaimer(),
       ]),
     ],
diff --git a/server/src/content/layout.gleam b/server/src/content/layout.gleam
index 463a407a..7408da13 100644
--- a/server/src/content/layout.gleam
+++ b/server/src/content/layout.gleam
@@ -30,6 +30,12 @@ import shared/config
 // pixel-identical to the product. Callers append a size class.
 const cta_base: String = "inline-block bg-amber text-white font-semibold rounded-lg hover:bg-amber/90 transition-colors focus:outline-none focus:ring-2 focus:ring-amber focus:ring-offset-2"
 
+// Outline secondary CTA, lifted verbatim from landing.gleam's `demo_cta_button`
+// so the /demo action reads as the same control on the SPA landing and the SSR
+// guides. Deliberately lower visual weight than `cta_base`: one primary action
+// per view. Callers append a size class.
+const demo_cta_base: String = "inline-block bg-white border-2 border-navy/15 text-navy font-semibold rounded-lg hover:border-amber hover:text-amber transition-colors focus:outline-none focus:ring-2 focus:ring-amber focus:ring-offset-2"
+
 const nav_link_class: String = "text-sm text-slate hover:text-charcoal transition-colors font-body"
 
 // -- Full-document wrapper ----------------------------------------------------
@@ -373,6 +379,46 @@ pub fn inline_cta(
   )
 }
 
+/// Secondary "Try the demo" CTA for the `/guides/*` pages: a border-only card
+/// placed directly under the guide's closing signup CTA (`inline_cta`) where
+/// one exists, otherwise at the end of the page content (part-4-tenancy, whose
+/// primary CTA sits mid-page). The outline button and plain border keep it
+/// visually secondary to the amber primary; the `text-base` heading sits under
+/// `inline_cta`'s `text-lg`. Plain anchor to `/demo` — the `demo_entry` event
+/// already fires on /demo entry, so no utm params or tracking wrappers here.
+pub fn guide_demo_cta() -> Element(a) {
+  html.div(
+    [
+      attribute.class(
+        "mt-4 bg-white rounded-xl border-2 border-navy/10 p-6 flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between",
+      ),
+    ],
+    [
+      html.div([attribute.class("max-w-xl")], [
+        html.p(
+          [attribute.class("font-headline text-base font-semibold text-navy")],
+          [html.text("See it work before you sign up")],
+        ),
+        html.p([attribute.class("mt-1 text-slate font-body")], [
+          html.text(
+            "A live sandbox with a mock vacancy and ranked applications. No signup.",
+          ),
+        ]),
+      ]),
+      html.div([attribute.class("shrink-0")], [
+        html.a(
+          [
+            attribute.href("/demo"),
+            attribute("data-testid", "guide-demo-cta"),
+            attribute.class(demo_cta_base <> " px-6 py-3"),
+          ],
+          [html.text("Try the demo")],
+        ),
+      ]),
+    ],
+  )
+}
+
 /// Section H2 in the brand headline style.
 pub fn section_heading(text: String) -> Element(a) {
   html.h2(
diff --git a/server/src/content/letting_agent_costs_view.gleam b/server/src/content/letting_agent_costs_view.gleam
index d162032b..df72cc69 100644
--- a/server/src/content/letting_agent_costs_view.gleam
+++ b/server/src/content/letting_agent_costs_view.gleam
@@ -42,6 +42,7 @@ pub fn render(
         view_comparison(our_price),
         view_what_you_get(our_price),
         view_cta(),
+        layout.guide_demo_cta(),
         view_source(),
         layout.advice_disclaimer(),
       ]),
diff --git a/server/src/content/notice_periods_view.gleam b/server/src/content/notice_periods_view.gleam
index e40bbce2..2273f665 100644
--- a/server/src/content/notice_periods_view.gleam
+++ b/server/src/content/notice_periods_view.gleam
@@ -51,6 +51,7 @@ pub fn render(
         view_templates(),
         view_faq(),
         view_cta(),
+        layout.guide_demo_cta(),
         view_sources(),
         layout.advice_disclaimer(),
       ]),
diff --git a/server/src/content/part_4_tenancy_view.gleam b/server/src/content/part_4_tenancy_view.gleam
index 6bde444f..9bed2a3c 100644
--- a/server/src/content/part_4_tenancy_view.gleam
+++ b/server/src/content/part_4_tenancy_view.gleam
@@ -60,6 +60,7 @@ pub fn render(
         view_in_practice(),
         view_faq(),
         view_sources(),
+        layout.guide_demo_cta(),
         layout.advice_disclaimer(),
       ]),
     ],
diff --git a/server/src/content/property_management_fees_view.gleam b/server/src/content/property_management_fees_view.gleam
index a65b024f..79d31575 100644
--- a/server/src/content/property_management_fees_view.gleam
+++ b/server/src/content/property_management_fees_view.gleam
@@ -67,6 +67,7 @@ pub fn render(
         view_tax_deductible(),
         view_need_agent(our_price),
         view_cta(),
+        layout.guide_demo_cta(),
         view_faq(our_price),
         view_sources(),
         layout.advice_disclaimer(),
diff --git a/server/src/content/rent_increase_notice_view.gleam b/server/src/content/rent_increase_notice_view.gleam
index 4d55c032..e39b6427 100644
--- a/server/src/content/rent_increase_notice_view.gleam
+++ b/server/src/content/rent_increase_notice_view.gleam
@@ -65,6 +65,7 @@ pub fn render(
         view_sources(),
         view_faq(),
         view_cta(),
+        layout.guide_demo_cta(),
         layout.advice_disclaimer(),
       ]),
     ],
diff --git a/server/src/content/rental_income_tax_view.gleam b/server/src/content/rental_income_tax_view.gleam
index 28e43dcc..ba0b9197 100644
--- a/server/src/content/rental_income_tax_view.gleam
+++ b/server/src/content/rental_income_tax_view.gleam
@@ -99,6 +99,7 @@ pub fn render(
         view_faq(),
         view_related(),
         view_cta(),
+        layout.guide_demo_cta(),
         view_source(),
         tax_disclaimer(),
       ]),
diff --git a/server/src/content/rtb_disputes_view.gleam b/server/src/content/rtb_disputes_view.gleam
index 7f9e757f..0128bb35 100644
--- a/server/src/content/rtb_disputes_view.gleam
+++ b/server/src/content/rtb_disputes_view.gleam
@@ -59,6 +59,7 @@ pub fn render(
         view_what_rtb_can(),
         view_applying_online(),
         view_cta(),
+        layout.guide_demo_cta(),
         view_faq(),
         view_sources(),
         layout.advice_disclaimer(),
diff --git a/server/src/content/rtb_registration_view.gleam b/server/src/content/rtb_registration_view.gleam
index 3a21a780..6ba62b8c 100644
--- a/server/src/content/rtb_registration_view.gleam
+++ b/server/src/content/rtb_registration_view.gleam
@@ -55,6 +55,7 @@ pub fn render(
         view_key_numbers(),
         view_faq(),
         view_cta(),
+        layout.guide_demo_cta(),
         rtb_sources(),
         layout.advice_disclaimer(),
       ]),
diff --git a/server/src/content/tenancy_agreement_template_view.gleam b/server/src/content/tenancy_agreement_template_view.gleam
index 60780168..4cd5fcce 100644
--- a/server/src/content/tenancy_agreement_template_view.gleam
+++ b/server/src/content/tenancy_agreement_template_view.gleam
@@ -69,6 +69,7 @@ pub fn render(
         rtb_reference(),
         view_faq(),
         view_cta(),
+        layout.guide_demo_cta(),
         layout.advice_disclaimer(),
       ]),
     ],
diff --git a/server/src/content/tenant_vetting_checklist_view.gleam b/server/src/content/tenant_vetting_checklist_view.gleam
index b150d882..22379cc6 100644
--- a/server/src/content/tenant_vetting_checklist_view.gleam
+++ b/server/src/content/tenant_vetting_checklist_view.gleam
@@ -43,6 +43,7 @@ pub fn render(
         view_checklist(),
         view_fair(),
         view_cta(),
+        layout.guide_demo_cta(),
         layout.advice_disclaimer(),
       ]),
     ],
diff --git a/server/test/content/content_test.gleam b/server/test/content/content_test.gleam
index 5ef1bbf9..048ab5ec 100644
--- a/server/test/content/content_test.gleam
+++ b/server/test/content/content_test.gleam
@@ -1757,3 +1757,91 @@ pub fn tracking_from_config_maps_each_field_to_its_slot_test() {
   tracking.google_ads_id |> should.equal("AW-7")
   tracking.meta_pixel_id |> should.equal("999")
 }
+
+// -- Guide demo CTA (issue #643) ----------------------------------------------
+
+// Default render shapes for the guide views without a page-section helper
+// above. 29_900 cents is the €299 vacancy unlock the handlers pass through.
+fn render_rtb_registration() -> String {
+  rtb_registration_view.render(
+    canonical_origin: "https://righttenantry.ie",
+    tracking: disabled_tracking(),
+  )
+}
+
+fn render_notice_periods() -> String {
+  notice_periods_view.render(
+    canonical_origin: "https://righttenantry.ie",
+    tracking: disabled_tracking(),
+  )
+}
+
+fn render_letting_agent_costs() -> String {
+  letting_agent_costs_view.render(
+    canonical_origin: "https://righttenantry.ie",
+    vacancy_unlock_cents: 29_900,
+    tracking: disabled_tracking(),
+  )
+}
+
+fn render_tenant_vetting_checklist() -> String {
+  tenant_vetting_checklist_view.render(
+    canonical_origin: "https://righttenantry.ie",
+    tracking: disabled_tracking(),
+  )
+}
+
+fn render_rtb_disputes() -> String {
+  rtb_disputes_view.render(
+    canonical_origin: "https://righttenantry.ie",
+    tracking: disabled_tracking(),
+  )
+}
+
+fn render_property_management_fees() -> String {
+  property_management_fees_view.render(
+    canonical_origin: "https://righttenantry.ie",
+    vacancy_unlock_cents: 29_900,
+    tracking: disabled_tracking(),
+  )
+}
+
+fn render_tenancy_agreement_template() -> String {
+  tenancy_agreement_template_view.render(
+    canonical_origin: "https://righttenantry.ie",
+    tracking: disabled_tracking(),
+  )
+}
+
+fn render_part_4_tenancy() -> String {
+  part_4_tenancy_view.render(
+    canonical_origin: "https://righttenantry.ie",
+    tracking: disabled_tracking(),
+  )
+}
+
+// Every /guides/* page must render the shared secondary "Try the demo" CTA
+// (layout.guide_demo_cta): a plain anchor to /demo carrying the guide-demo-cta
+// testid. Rendering all 11 views here means a future guide whose composition
+// list drops the call fails CI instead of silently losing the /demo entry
+// surface. /tools/*, /resources and rent-post pages are deliberately out of
+// scope (one primary CTA per view).
+pub fn guide_demo_cta_present_on_every_guide_test() {
+  [
+    render_rtb_registration(),
+    render_notice_periods(),
+    render_letting_agent_costs(),
+    render_tenant_vetting_checklist(),
+    render_rent_increase_notice(),
+    render_rtb_disputes(),
+    render_property_management_fees(),
+    render_tenancy_agreement_template(),
+    render_landlord_reference_letter(),
+    render_rental_income_tax(rental_income_tax_view.Empty),
+    render_part_4_tenancy(),
+  ]
+  |> list.each(fn(html) {
+    html |> string.contains("data-testid=\"guide-demo-cta\"") |> should.be_true
+    html |> string.contains("href=\"/demo\"") |> should.be_true
+  })
+}


--- SPEC / CONTEXT ---
--- Spec doc (implementation brief) ---
# Briefing: rt-643-guide-demo-cta

**Repo:** /Users/moses/code/RightTenantry (managed). **Issue:** https://github.com/solarity-services/RightTenantry/issues/643
**Type:** enhancement, code. **Skill:** bmad-build. **Model:** deepseek/deepseek-v4-flash.
**Dispatch:** worktree on the repo's default branch; one PR titled "Add Try the demo CTA to SSR guide template (#643)"; `ledger pr` the PR url; pr_review=1.

## Task

Add a secondary "Try the demo" CTA to the SSR guide template so EVERY `/guides/*` page links to `/demo`.

## Where

- SSR template: `server/src/content/content_pages.gleam` (guide rendering), possibly `content_handler.gleam` for the shared layout wrapper.
- Pattern to mirror: `demo_cta_button` in `client/src/pages/landing.gleam` (~line 83) — match its secondary visual weight. The landing's hero CTA usage is at ~line 345 for reference.

## Requirements (from the issue — follow them exactly)

- Plain anchor to `/demo` in the SSR template, rendered on every guide page.
- `data-testid="guide-demo-cta"` on the anchor (PostHog autocapture).
- SECONDARY weight only — the guide's primary signup CTA must stay primary. One primary CTA per view.
- Brand copy rules: no exclamation marks, no em dashes, outcome-led. Use this block:
  - Heading: "See it work before you sign up"
  - Button: "Try the demo"
  - Subline: "A live sandbox with a mock vacancy and ranked applications. No signup."
- No new analytics instrumentation (demo_entry already fires on /demo entry).

## Acceptance

- [ ] Every /guides/* page renders the demo CTA linking to /demo
- [ ] Anchor carries `data-testid="guide-demo-cta"`
- [ ] Secondary visual weight vs the signup CTA
- [ ] Mobile renders cleanly (no horizontal scroll)
- [ ] Build + existing tests pass (`cd server && gleam test` if a suite exists; `gleam build` otherwise; client untouched)

## Notes

- Small, targeted change. Lavish not needed — open the PR directly.
- Verify by rendering one guide locally if a dev server is cheap (`make run` needs `server/.env` symlink to the repo root `.env`); otherwise show the rendered HTML in the PR description.


--- GitHub issue #643 ---
Issue title: Add "Try the demo" CTA to the SSR guide template (demo distribution)

**Owner:** gru + minions. **Source:** Herald adoption analysis, 2026-09-01. **Context:** /demo interactive sandbox shipped 2026-08-19 (#628).

## Problem

The /demo sandbox has recorded ZERO tracked entries in its first 13 days: 0 `demo_entry` events, 0 /demo pageviews, 0 clicks on any "Try the demo" CTA. Root cause is distribution, not the product:

- The ONLY surface linking to /demo is the landing page (`nav-try-demo`, `nav-try-demo-mobile`, `cta-try-demo-hero` in `client/src/pages/landing.gleam`).
- The landing is the lowest-traffic surface on the site: 5 consented views / 2 people since 08-19 (homepage is a pure SPA, unindexed).
- The guides are the traffic engine and link to /demo ZERO times.

Traffic since 08-19 (PostHog, consent-gated floor): `/guides/letting-agent-costs` 28 views / 24 people, `/guides/tenancy-agreement-template` 13 / 11, ~70+ guide views / ~60 people total, vs 5 views on the landing.

## Ask

Add a secondary "Try the demo" CTA to the SSR guide template so EVERY /guides/* page carries it.

Implementation notes:

- Guides are server-rendered: `server/src/content/content_pages.gleam` (+ `content_handler.gleam`). The CTA is a plain anchor in the SSR template.
- Visual pattern: mirror the landing's secondary demo CTA (`demo_cta_button` in `client/src/pages/landing.gleam`). Secondary weight; must NOT compete with the guide's primary signup CTA (one primary CTA per view).
- Brand copy rules: no exclamation marks, no em dashes, outcome-led. Suggested block:
  - Heading: "See it work before you sign up"
  - Button: "Try the demo"
  - Subline: "A live sandbox with a mock vacancy and ranked applications. No signup."
- `data-testid="guide-demo-cta"` on the anchor so PostHog autocapture records clicks (consent-gated as usual).
- No new instrumentation required: `demo_entry` already fires on /demo entry (consent-gated FFI in `client/src/demo/demo_analytics.gleam`).
- Un-gated measurement lives in Cloud Run request logs: hits on /demo + GETs under /static/demo/ (project `righttenantry`, service `righttenantry`, region `europe-west1`).

## Acceptance criteria

- [ ] Every /guides/* page renders the demo CTA linking to /demo
- [ ] CTA carries `data-testid="guide-demo-cta"`
- [ ] Secondary visual weight (signup CTA stays primary)
- [ ] Mobile renders cleanly (no horizontal scroll)
- [ ] Within 2 weeks of deploy: nonzero /demo entries visible in Cloud Run logs (un-gated)


(comments: none)

--- YOUR LENS ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

--- FILE OUTPUT (headless mode) ---
When your review is complete, write ONLY the JSON array (no prose, no markdown fencing, no preamble) to this exact path:
/Users/moses/code/_bmad-output/perkins/rt-643-guide-demo-cta/r1/architecture.json
Use the write-file capability to create that file. The file is the deliverable — an empty array `[]` is a valid deliverable. Then stop.