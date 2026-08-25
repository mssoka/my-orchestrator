You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. The repository checkout is at: /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-followup-607-r1

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
diff --git a/.github/workflows/test.yml b/.github/workflows/test.yml
index 4e06d762..c99312af 100644
--- a/.github/workflows/test.yml
+++ b/.github/workflows/test.yml
@@ -127,6 +127,14 @@ jobs:
           fi
           echo "All outbound HTTP calls use explicit timeouts."
 
+      - name: Lint — RT-wide em-dash ban in user-facing source (#607 item 4)
+        run: |
+          python3 scripts/lint_em_dash.py
+
+      - name: "Lint — AR-RC13: server hooks are the single source of truth (#607 item 5)"
+        run: |
+          python3 scripts/lint_refcheck_hooks.py
+
       - name: Run unit tests
         run: make test
 
diff --git a/_bmad-output/implementation-artifacts/spec-refcheck-followup-607.md b/_bmad-output/implementation-artifacts/spec-refcheck-followup-607.md
new file mode 100644
index 00000000..2c82d45f
--- /dev/null
+++ b/_bmad-output/implementation-artifacts/spec-refcheck-followup-607.md
@@ -0,0 +1,86 @@
+---
+status: ready-for-dev
+title: "RefCheck follow-up #607 — five carried Perkins advisories"
+---
+
+# Spec — refcheck-followup-607
+
+Canonical spec: GitHub issue #607 (Perkins carried warnings, RC4.1 + RC4.2 +
+RC4.3). Base `develop` @ 6284611. Scope guard: the five items ONLY; where an
+item has a plausible alternative reading, take the more restrictive one and
+flag it in the PR body.
+
+## Item 1 — Escaped-form markers cover `form_token`/`payload_ref`
+
+- `server/src/application/application_detail_handler.gleam`:
+  `verify_payload_has_no_internal_fields` — the escaped marker list covers
+  `\"referee_ip\"`/`\"referee_user_agent\"` only. Add
+  `\\\"form_token\\\"` and `\\\"payload_ref\\\"` escaped markers.
+- Pin: extend `verify_payload_guard_detects_internal_markers_test` with the
+  escaped result-string wire forms for both fields (must return False).
+- Acceptance: markers cover EVERY payload field; strip still proven by the
+  existing integration test.
+
+## Item 2 — Unknown-outcome fallback (named rule in the hooks contract)
+
+- The encoder maps unknown outcome strings via `outcome_from_string`'s
+  fallback (`_ -> OutcomeUnreachable`), so an expand-window row renders
+  `outcome: "unreachable"` on a recordable row — the exact divergence
+  self-review #3 forbids.
+- Fix: `shared/reference_call.gleam` gains `outcome_from_string_optional`
+  (known → Some, ""/unknown → None); the encoder uses it. Name the rule in
+  the `ReferenceCallHooks` doc: **unknown-outcome rule** — hooks come from
+  status only; an unrecognised outcome encodes as absent, never as the
+  fallback.
+- Pins: shared test (unknown → None, known → Some, "" → None); server test —
+  encode a row with an unknown outcome string → wire `"outcome":null`, hooks
+  still recordable on a recordable status.
+
+## Item 3 — Timeline sort format-mix inversion
+
+- RC4.4 already rebuilt the timeline server-side with `normalize_at` before
+  the lexical sort and pinned the canonical same-day mix
+  (`attempt_log_appends_lifecycle_events_test`); the client renders payload
+  order without sorting (`timeline_orders_form_opened_after_reminder_test`).
+- Remaining pin: a fixture mixing formats WITHIN the attempts source
+  (space-form attempt `at` alongside T-form attempts + a space-form column
+  stamp) proving the sort normalises every side. Verify existing pins green.
+
+## Item 4 — Em-dash lint + composition sites
+
+- Two render-time em-dash joins ship to landlords today:
+  `reference_panel.gleam` `send_batch_line` (`label <> " — " <> channels`)
+  and `nudge_label` (`... <> " — " <> detail`) — #605 r2 W1.
+- Fix: move both joins into `copy.gleam` as fn-built labels with a dash-free
+  separator (parens); the copy-ban test scans them; update the client test
+  pins.
+- Lint: `scripts/lint_em_dash.py` — fails on em-dash inside string literals
+  in user-facing source (client/src except copy.gleam — the spec-verbatim
+  home — plus the server form/refcheck view surface). Wired as a CI step in
+  `test.yml` (unit-test job, alongside the existing grep lints).
+
+## Item 5 — AR-RC13 systemic guard (hooks = single source of truth)
+
+- Shared-type guard: `shared/reference_call.gleam` gains
+  `is_terminal_status(status) -> Bool`; server `compute_hooks_decoded` and
+  the client panel test fixture both consume it (the client has no
+  terminality list left to drift). Lockstep test pins the server's
+  `terminal_statuses` string list to the shared fn.
+- Test-rule pins (the distinguishing tests the r2 review said were missing):
+  v2-reserved `Completed` row renders terminal via hooks (RC4.2-r1 proof —
+  the historical list omitted `Completed`); an `Unreachable` row with
+  `can_take_over: False` renders no take-over affordance (RC4.3-r1 proof —
+  the historical menu derived take-over from status).
+- Lint: `scripts/lint_refcheck_hooks.py` — `RefcheckTakeOver` /
+  `RefcheckSubstitute` may only be constructed inside `case call.hooks.can_*`
+  blocks (indentation-scoped scan of `reference_panel.gleam`); wired into
+  `test.yml`.
+- Docs: Amendment-register entry in
+  `architecture-reference-checking-v1-2026-07-29.md` (AR-RC13 lesson entry:
+  bug class, both occurrences, the guard, the rule) + AD-11 cross-reference.
+
+## Verify
+
+`make format && make test && make build` green; new pins green (1–3, 5);
+lints green + CI wired (4); integration suite green against a local test DB;
+PR body maps item → fix → pin and carries Decisions & rationale.
diff --git a/_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md b/_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md
index 89407fef..bc25e557 100644
--- a/_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md
+++ b/_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md
@@ -109,6 +109,50 @@ maps unambiguously to AD-6's `objected` and echoes the "reply STOP" semantics it
 (lifecycle), §5.5 (webhook list), §7.2 (route table), §9.1 (Art 14 vehicle), §11 Q3
 (resolved), §13 (build shape).
 
+### Amendment 2026-08-13 — AR-RC13: the server hooks are the single source of truth for affordance legality (systemic guard + lesson)
+
+**Provenance:** the same bug class blocked TWO consecutive RC4 review rounds — Perkins
+RC4.2-r1 (B1: client-side terminality) and RC4.3-r1 (B3: client-side take-over/substitute
+menu legality). Both were fixed per-PR; this amendment is the durable architecture-level
+guard so the class cannot recur, filed as #607 item 5.
+
+**The bug class (AR-RC13):** the panel re-derived affordance LEGALITY from the status
+instead of consuming the server-computed `hooks` object. RC4.2-r1 shipped
+`is_terminal(call) { case call.status { ... } }` with a client-side list that omitted the
+v2-reserved `completed` variant — a v2 voice-terminal row would render recordable.
+RC4.3-r1 shipped `overflow_actions(status) { case status { ContactInitiated ->
+[RefcheckTakeOver]; Unreachable -> [RefcheckTakeOver, RefcheckSubstitute] } }` — the
+overflow menu ignored the hooks entirely. Both passed review because the test fixtures
+mirrored the client's own list, so panel and fixture drifted in lockstep.
+
+**The guard (three layers, all in the repo):**
+
+1. **Shared-type guard — terminality has ONE home.** `is_terminal_status(status)` lives in
+   `shared/reference_call.gleam`; the server's `compute_hooks_decoded` (can_record_manual)
+   AND the client test fixture both consume it. The client has no terminality list left to
+   drift; a re-derivation would introduce a new list the shared-fn fixture does not mirror,
+   so panel-vs-hooks divergence becomes test-visible for any status they disagree on. A
+   lockstep unit test pins the timeline's DB-string `terminal_statuses` list to the shared
+   fn.
+2. **Test rule — the distinguishing pins.** `completed_v2_status_renders_terminal_via_hooks_test`
+   renders the v2-reserved `Completed` row terminal (the exact r1 omission);
+   `unreachable_row_hides_take_over_when_hook_off_test` asserts the menu follows
+   `can_take_over: False` on an `unreachable` row (the exact r1 menu shape renders the
+   button and fails).
+3. **Lint rule — structural, CI-gated.** `scripts/lint_refcheck_hooks.py` fails when
+   `RefcheckTakeOver` / `RefcheckSubstitute` are constructed outside
+   `case call.hooks.can_*` blocks in the panel; wired into `test.yml` alongside the
+   em-dash and `let assert` lints.
+
+**The rule (binds every future panel change):** statuses pick the MENU and the LABELS;
+the hooks decide what the menu may CONTAIN and whether a row is terminal. The wire is the
+contract — an affordance shown (or hidden) must always be explainable from
+`hooks.can_record_manual` / `can_take_over` / `can_substitute_referee` / `can_retry`
+without reading the status.
+
+**Amended in place:** AD-11 (Prevents + hook semantics — see below), §8.2 (hooks contract
+doc: unknown-outcome rule, #607 item 2).
+
 ## 0. Scope (decided upstream — not re-litigated here)
 
 **v1 lands entirely in this repo. No voice, no Twilio telephony, no RightTenantryAgents
@@ -455,7 +499,10 @@ job; this document fixes only the shape they consume.
 
 **Binds:** the API shape and the capability flags.
 **Prevents:** the UX workstream inventing client-side state machines that disagree with AD-1;
-leaking internal fields (tokens, raw IPs) to the landlord payload.
+leaking internal fields (tokens, raw IPs) to the landlord payload. (AR-RC13 amendment
+2026-08-13: affordance legality comes ONLY from the hooks object — statuses pick menus and
+labels, never legality; terminality has a single shared home in
+`shared/reference_call.is_terminal_status`, enforced by lint + distinguishing tests.)
 
 **Hook semantics:** `can_substitute_referee` is a landlord-side *trigger for an applicant-side
 action* — clicking it emails the applicant the tokenized substitution link (§5.7); the
diff --git a/client/src/components/reference_panel.gleam b/client/src/components/reference_panel.gleam
index 638c25e9..252389a9 100644
--- a/client/src/components/reference_panel.gleam
+++ b/client/src/components/reference_panel.gleam
@@ -1475,7 +1475,10 @@ fn send_batch_line(entries: List(AttemptLogEntry)) -> TimelineLine {
     "reminder_sent" -> reminder_label(first_or_empty(entries))
     other -> other
   }
-  TimelineLine(label <> " — " <> channels, first_at(entries))
+  TimelineLine(
+    copy.refcheck_timeline_send_batch(label, channels),
+    first_at(entries),
+  )
 }
 
 fn first_or_empty(entries: List(AttemptLogEntry)) -> AttemptLogEntry {
@@ -1524,11 +1527,14 @@ fn nudge_label(entries: List(AttemptLogEntry)) -> String {
       case list.find(entries, fn(e) { e.outcome == "skipped" }) {
         Ok(skipped) ->
           // W6: join the skip reason ONLY when the server shipped one — a
-          // bare "Applicant nudge skipped" is honest, a dangling " — " is
+          // bare "Applicant nudge skipped" is honest, a dangling join is
           // not.
           case skipped.detail {
             "" -> copy.refcheck_timeline_nudge_skipped
-            detail -> copy.refcheck_timeline_nudge_skipped <> " — " <> detail
+            // #607 item 4: the reason joins through the copy fn (dash-free
+            // parens) — the old render-time `" — "` join shipped an
+            // implementer-authored em-dash (#605 r2 W1).
+            detail -> copy.refcheck_timeline_nudge_skipped_with(detail)
           }
         Error(_) -> copy.refcheck_timeline_nudge_failed
       }
diff --git a/client/src/copy.gleam b/client/src/copy.gleam
index 72561654..14879ae4 100644
--- a/client/src/copy.gleam
+++ b/client/src/copy.gleam
@@ -965,6 +965,23 @@ pub fn refcheck_timeline_reminder(n: Int) -> String {
   "Reminder " <> int.to_string(n) <> " sent"
 }
 
+/// The joined send-batch timeline line: the label plus the channel list
+/// ("Invitation sent (email + SMS)"). #607 item 4: the composition lives
+/// here so the em-dash ban test can reach it — the old render-time
+/// `label <> " — " <> channels` join shipped an implementer-authored
+/// em-dash (#605 r2 W1). Dash-free paren separator.
+pub fn refcheck_timeline_send_batch(label: String, channels: String) -> String {
+  label <> " (" <> channels <> ")"
+}
+
+/// The nudge-skipped timeline line with the server-shipped skip reason
+/// ("Applicant nudge skipped (co-nudge skipped: form already opened)").
+/// #607 item 4: composition moved here (dash-free) so the ban test scans
+/// it; the reason is appended verbatim only when the server shipped one.
+pub fn refcheck_timeline_nudge_skipped_with(detail: String) -> String {
+  refcheck_timeline_nudge_skipped <> " (" <> detail <> ")"
+}
+
 /// The terminal event's timeline label per status (§7.6's example line is
 /// "Closed — no reply" for the exhausted cadence; the others are the honest
 /// one-phrase renderings of the same terminal the state copy describes).
diff --git a/client/test/components/reference_panel_test.gleam b/client/test/components/reference_panel_test.gleam
index 5e850f0c..6411cdf8 100644
--- a/client/test/components/reference_panel_test.gleam
+++ b/client/test/components/reference_panel_test.gleam
@@ -20,9 +20,9 @@ import model.{type RefcheckConfirm, type RefcheckEdit}
 import shared/application.{type Application}
 import shared/reference_call.{
   type ReferenceCallAttempt, type ReferenceCallDetail, type ReferenceCallStatus,
-  AwaitingCorrection, CharacterRef, ContactInitiated, EmployerRef, Failed,
-  FormCompleted, LandlordRef, ManualRecorded, Objected, Partial, Queued, Refused,
-  Skipped, Unreachable,
+  AwaitingCorrection, CharacterRef, Completed, ContactInitiated, EmployerRef,
+  Failed, FormCompleted, LandlordRef, ManualRecorded, Objected, Partial, Queued,
+  Refused, Skipped, Unreachable,
 }
 
 // -- Fixtures -----------------------------------------------------------------
@@ -60,11 +60,13 @@ fn row(
     attempt_log: attempt_log_from(attempts),
     result: result,
     display_disclaimer: None,
-    // Hooks mirror the server's terminal rule (can_record_manual =
-    // !terminal) so the panel's hook-driven terminality reads realistic
-    // fixtures.
+    // Hooks mirror the SERVER's terminal rule (can_record_manual =
+    // !terminal) via the SHARED truth (AR-RC13 guard, #607 item 5) — the
+    // fixture derives hooks from the same `is_terminal_status` the server's
+    // compute_hooks uses, never from a client-side list a re-derivation
+    // could drift in lockstep with.
     hooks: reference_call.ReferenceCallHooks(
-      can_record_manual: !is_terminal_status(status),
+      can_record_manual: !reference_call.is_terminal_status(status),
       can_substitute_referee: False,
       can_retry: False,
       can_take_over: False,
@@ -135,20 +137,6 @@ fn base_hooks() -> reference_call.ReferenceCallHooks {
   )
 }
 
-fn is_terminal_status(status: ReferenceCallStatus) -> Bool {
-  case status {
-    FormCompleted
-    | ManualRecorded
-    | Partial
-    | Unreachable
-    | Refused
-    | Objected
-    | Failed
-    | reference_call.Completed -> True
-    _ -> False
-  }
-}
-
 fn invite_attempt() -> ReferenceCallAttempt {
   reference_call.ReferenceCallAttempt(
     at: "2026-08-01T10:04:00Z",
@@ -401,6 +389,34 @@ pub fn all_terminal_subline_test() {
   |> should.be_true
 }
 
+/// #607 item 5 (AR-RC13 guard): the v2-reserved `Completed` status renders
+/// TERMINAL — hooks say so (the shared truth includes `completed`; the
+/// server's can_record_manual is False), and the panel follows the hook.
+/// The RC4.2-r1 bug was a client-side terminality list that OMITTED
+/// `completed`, so a v2 voice-terminal row rendered as recordable; with the
+/// fixture now deriving hooks from the shared `is_terminal_status`, that
+/// exact re-derivation renders this row in-flight and fails this test.
+pub fn completed_v2_status_renders_terminal_via_hooks_test() {
+  // Shared truth: completed IS terminal, so the fixture's hooks say
+  // can_record_manual: False — exactly what the server would ship.
+  reference_call.is_terminal_status(Completed)
+  |> should.be_true
+  let html =
+    render(
+      calls: [row("rc-1", Completed, None, [])],
+      off: False,
+      attestation_on_file: False,
+      expanded: ["rc-1"],
+    )
+  html
+  |> string.contains("All references closed. Summaries and logs stay here.")
+  |> should.be_true
+  // No overflow control on a terminal row (hooks say no live lifecycle).
+  html
+  |> string.contains("refcheck-overflow-landlord_ref")
+  |> should.be_false
+}
+
 // -- The 12-state matrix ------------------------------------------------------
 
 /// Queued: slate pill, A5 row line on expand, no timestamp (nothing sent).
@@ -439,7 +455,7 @@ pub fn invitation_sent_state_test() {
   html |> string.contains("bg-navy/10 text-navy") |> should.be_true
   html |> string.contains("01 Aug, 10:04") |> should.be_true
   // Timeline: the invite batch joined as "email + SMS", then what-happens-next.
-  html |> string.contains("Invitation sent — email + SMS") |> should.be_true
+  html |> string.contains("Invitation sent (email + SMS)") |> should.be_true
   html
   |> string.contains("Next reminder in ~2 days if there&#39;s no reply")
   |> should.be_true
@@ -467,7 +483,7 @@ pub fn reminder_sent_state_test() {
       expanded: ["rc-1"],
     )
   html |> string.contains("Reminder sent") |> should.be_true
-  html |> string.contains("Reminder 1 sent — email + SMS") |> should.be_true
+  html |> string.contains("Reminder 1 sent (email + SMS)") |> should.be_true
   html |> string.contains("Applicant asked to nudge") |> should.be_true
 }
 
@@ -1001,7 +1017,7 @@ pub fn timeline_orders_form_opened_after_reminder_test() {
   // Pin the TIMELINE lines (</p>), not the status pill (</span>) — the pill
   // for this row is also "Form opened" and sits above the timeline in the DOM.
   let invite = first_index(html, "Invitation sent</p>")
-  let reminder = first_index(html, "Reminder 1 sent — ")
+  let reminder = first_index(html, "Reminder 1 sent (email + SMS)")
   let opened = first_index(html, "Form opened</p>")
   // Bind the comparisons first — a line starting with `(` would continue
   // the previous let-expression (Gleam line-continuation), and `|>` binds
@@ -1300,6 +1316,42 @@ pub fn overflow_menu_queued_lists_take_over_when_hook_test() {
   |> should.be_true
 }
 
+/// #607 item 5 (AR-RC13 guard): the overflow menu follows the HOOKS, not
+/// the status. An `unreachable` row whose hooks say `can_take_over: False`
+/// (the server's per-row refine — a taken-over row can never be taken over
+/// again) must render NO take-over entry, while the substitute entry stays
+/// (its hook is on). The RC4.3-r1 bug was `overflow_actions(Unreachable) ->
+/// [TakeOver, Substitute]` derived from status alone — it renders the
+/// take-over button on a row the server says is not take-overable and
+/// fails this test.
+pub fn unreachable_row_hides_take_over_when_hook_off_test() {
+  let unreachable =
+    reference_call.ReferenceCallDetail(
+      ..contact_row("rc-1", Unreachable),
+      hooks: reference_call.ReferenceCallHooks(
+        ..base_hooks(),
+        can_substitute_referee: True,
+      ),
+    )
+  let html =
+    render_with_actions(
+      calls: [unreachable],
+      off: False,
+      attestation_on_file: False,
+      expanded: [],
+      menu_open: Some("rc-1"),
+      confirm: None,
+      edit: dict.new(),
+      inflight: [],
+    )
+  html
+  |> string.contains("refcheck-action-take-over-landlord_ref")
+  |> should.be_false
+  html
+  |> string.contains("refcheck-action-substitute-landlord_ref")
+  |> should.be_true
+}
+
 /// The overflow menu opens with the right entries for a queued row (§7.4).
 pub fn overflow_menu_queued_lists_start_and_skip_test() {
   let html =
@@ -2048,15 +2100,16 @@ pub fn skipped_co_nudge_renders_skip_reason_test() {
     ])
   html
   |> string.contains(
-    "Applicant nudge skipped — co-nudge skipped: form already opened",
+    "Applicant nudge skipped (co-nudge skipped: form already opened)",
   )
   |> should.be_true
-  // No dangling join: the label ends with the reason, not \" — \" + blank.
-  html |> string.contains("nudge skipped — —") |> should.be_false
+  // No dangling join: the reason always lands inside closed parens — a
+  // dangling " (" + blank would render "nudge skipped ()".
+  html |> string.contains("nudge skipped ()") |> should.be_false
 }
 
 /// W6: a skipped co-nudge WITHOUT a shipped reason renders the plain label
-/// — never a trailing \" — \".
+/// — never a trailing join (a dangling " (" before the closing tag).
 pub fn skipped_co_nudge_without_reason_no_dangling_join_test() {
   let call =
     reference_call.ReferenceCallDetail(
@@ -2083,7 +2136,7 @@ pub fn skipped_co_nudge_without_reason_no_dangling_join_test() {
       "rc-1",
     ])
   html |> string.contains("Applicant nudge skipped") |> should.be_true
-  html |> string.contains("nudge skipped — </p>") |> should.be_false
+  html |> string.contains("nudge skipped (</p>") |> should.be_false
 }
 
 /// W3: the timeline terminal + export outcome label tables are consistent
diff --git a/client/test/copy_test.gleam b/client/test/copy_test.gleam
index 232fd229..f12f3e42 100644
--- a/client/test/copy_test.gleam
+++ b/client/test/copy_test.gleam
@@ -394,8 +394,28 @@ fn refcheck_fn_built_labels() -> List(String) {
     "completed",
   ]
   list.append(
-    list.map(terminal_statuses, copy.refcheck_timeline_terminal),
-    list.map(export_statuses, copy.refcheck_export_outcome),
+    list.append(
+      list.map(terminal_statuses, copy.refcheck_timeline_terminal),
+      list.map(export_statuses, copy.refcheck_export_outcome),
+    ),
+    // #607 item 4: the composed timeline lines (the render-time
+    // `label <> " — " <> ...` joins moved into copy so the ban test can
+    // reach them — #605 r2 W1 flagged the composition sites). Fixture args
+    // mirror production shapes: a send batch with both channels and a
+    // skipped co-nudge carrying its server-shipped reason.
+    [
+      copy.refcheck_timeline_send_batch(
+        copy.refcheck_timeline_invitation,
+        "email + SMS",
+      ),
+      copy.refcheck_timeline_send_batch(
+        copy.refcheck_timeline_reminder(2),
+        "SMS",
+      ),
+      copy.refcheck_timeline_nudge_skipped_with(
+        "co-nudge skipped: form already opened",
+      ),
+    ],
   )
   // The spec-verbatim §7.6 terminal line is the ONLY exempt arm.
   |> list.filter(fn(s) { s != "Closed — no reply" })
diff --git a/scripts/lint_em_dash.py b/scripts/lint_em_dash.py
new file mode 100644
index 00000000..22c83afd
--- /dev/null
+++ b/scripts/lint_em_dash.py
@@ -0,0 +1,142 @@
+#!/usr/bin/env python3
+"""RT-wide em-dash ban lint (#607 item 4).
+
+The 2026-08-05 user ruling: no em-dash (U+2014) in landlord-facing copy.
+The gleam copy tests pin the copy CONSTS (client/test/copy_test.gleam,
+server/test/reference_checks/form_copy_test.gleam, messages_test.gleam, ...);
+this lint closes the gap those tests cannot reach: em-dashes in STRING
+LITERALS at render/composition sites (view modules), which the 2026-08-13
+finding (#605 r2 W1) showed shipping to landlords via `label <> " — " <> ...`
+joins in reference_panel.gleam.
+
+Scope: user-facing render/composition modules only.
+- client/src/** except client/src/copy.gleam (the spec-verbatim home — its
+  verbatim em-dashes are exempt by construction and its implementer-authored
+  consts are scanned by the copy test).
+- server form/refcheck view + copy modules (dash-free today; the referee form
+  copy test already asserts absence on every string).
+
+Comments are stripped (string-literal scan only), so doc comments quoting
+spec lines never false-positive. Server log/warning strings are developer-
+facing and deliberately out of scope (the ban is landlord-facing copy).
+
+Exit 1 on any violation; prints file:line. Wired into .github/workflows/test.yml.
+"""
+
+import pathlib
+import re
+import sys
+
+ROOT = pathlib.Path(__file__).resolve().parent.parent
+
+# user-facing render/composition modules, relative to ROOT
+CLIENT_EXCLUDE = {"client/src/copy.gleam"}
+CLIENT_GLOB = "client/src/**/*.gleam"
+SERVER_INCLUDE = [
+    "server/src/copy.gleam",
+    "server/src/application/error_summary.gleam",
+    "server/src/application/draft_view.gleam",
+    "server/src/application/form_*.gleam",
+    "server/src/application/form_sections/*.gleam",
+    "server/src/reference_checks/actions_handler.gleam",
+    "server/src/reference_checks/form_*.gleam",
+    "server/src/reference_checks/fraud.gleam",
+    "server/src/reference_checks/fraud_inputs.gleam",
+    "server/src/reference_checks/messages.gleam",
+    "server/src/reference_checks/questions.gleam",
+    "server/src/reference_checks/result.gleam",
+]
+
+EM_DASH = "\u2014"
+
+# Developer-facing telemetry calls — their string arguments are log lines,
+# not landlord-facing copy (the ban is user-facing only). Single-line calls
+# cover the repo's usage (wisp.log_error / log_warning / log_info / log_debug
+# and the JS-side console.* in static assets are out of scope).
+LOG_CALL_RE = re.compile(
+    r"(log_error|log_warning|log_info|log_debug|log_critical|log_fatal|console\.\w+)\("
+)
+
+
+def strip_comments(line: str) -> str:
+    """Remove a trailing // comment, respecting in-string state."""
+    out = []
+    in_str = False
+    i = 0
+    while i < len(line):
+        c = line[i]
+        if in_str:
+            out.append(c)
+            if c == "\\" and i + 1 < len(line):
+                out.append(line[i + 1])
+                i += 2
+                continue
+            if c == '"':
+                in_str = False
+            i += 1
+            continue
+        if c == '"':
+            in_str = True
+            out.append(c)
+            i += 1
+            continue
+        if c == "/" and i + 1 < len(line) and line[i + 1] == "/":
+            break
+        out.append(c)
+        i += 1
+    return "".join(out)
+
+
+def string_literal_em_dashes(line: str) -> bool:
+    """True when an em-dash appears inside a double-quoted string literal
+    that is NOT a developer-facing log/console call argument."""
+    # after comment stripping, em-dash inside quotes only
+    cleaned = strip_comments(line)
+    if LOG_CALL_RE.search(cleaned):
+        return False
+    in_str = False
+    for i, c in enumerate(cleaned):
+        if c == '"':
+            in_str = not in_str
+        elif c == EM_DASH and in_str:
+            return True
+    return False
+
+
+def iter_files() -> list:
+    files = []
+    for p in sorted(ROOT.glob(CLIENT_GLOB)):
+        rel = p.relative_to(ROOT).as_posix()
+        if rel in CLIENT_EXCLUDE:
+            continue
+        files.append(p)
+    for pattern in SERVER_INCLUDE:
+        files.extend(sorted(ROOT.glob(pattern)))
+    # dedupe, keep order
+    seen = set()
+    return [f for f in files if not (f in seen or seen.add(f))]
+
+
+def main() -> int:
+    violations = []
+    for path in iter_files():
+        try:
+            text = path.read_text(encoding="utf-8")
+        except UnicodeDecodeError:
+            continue
+        for lineno, line in enumerate(text.splitlines(), 1):
+            if string_literal_em_dashes(line):
+                violations.append(f"{path.relative_to(ROOT)}:{lineno}: {line.strip()[:120]}")
+    if violations:
+        print("Em-dash (U+2014) found in user-facing string literal(s):")
+        for v in violations:
+            print(f"  {v}")
+        print("\nThe RT-wide em-dash ban applies to landlord/applicant-facing copy.")
+        print("Move the string into copy.gleam (dash-free) or fix the literal.")
+        return 1
+    print(f"em-dash lint clean ({len(iter_files())} files scanned)")
+    return 0
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a/scripts/lint_refcheck_hooks.py b/scripts/lint_refcheck_hooks.py
new file mode 100644
index 00000000..d3d76aff
--- /dev/null
+++ b/scripts/lint_refcheck_hooks.py
@@ -0,0 +1,97 @@
+#!/usr/bin/env python3
+"""AR-RC13 affordance-derivation lint (#607 item 5).
+
+The RC4.2-r1 and RC4.3-r1 blockers were the same bug class: the client
+panel re-derived affordance LEGALITY from the status (a client-side
+terminality list omitting v2 `completed`; an overflow menu that derived
+take-over/substitute from status arms) instead of consuming the
+server-computed `hooks` object. The fixed panel gates every hook-governed
+action on `case call.hooks.can_*`.
+
+This lint makes that structural rule durable: in the panel, the
+hook-governed action constructors (`RefcheckTakeOver`, `RefcheckSubstitute`)
+may only be CONSTRUCTED inside a `case call.hooks.can_take_over` /
+`case call.hooks.can_substitute_referee` block. Construction is the list
+shape `[RefcheckTakeOver]` / `[RefcheckSubstitute]`; pattern-match arms
+(`RefcheckTakeOver -> ...` — the confirm/edit render switches) and message
+construction (`UserChoseRefcheckAction(..., RefcheckSubstitute)`) are not
+legality decisions and are exempt by shape.
+
+`can_record_manual` terminality is guarded separately: the shared
+`is_terminal_status` is the single terminality truth, consumed by the
+server's hooks and the client fixture — the client has no list to drift.
+
+Exit 1 on any violation. Wired into .github/workflows/test.yml.
+"""
+
+import pathlib
+import re
+import sys
+
+ROOT = pathlib.Path(__file__).resolve().parent.parent
+PANEL = ROOT / "client/src/components/reference_panel.gleam"
+
+# action constructor -> the hook case that may gate it
+HOOK_FOR = {
+    "RefcheckTakeOver": "case call.hooks.can_take_over",
+    "RefcheckSubstitute": "case call.hooks.can_substitute_referee",
+}
+
+
+def indent_of(line: str) -> int:
+    return len(line) - len(line.lstrip(" "))
+
+
+def find_enclosing_hook_case(lines: list, flagged_idx: int, hook_case: str) -> bool:
+    """True when the nearest `hook_case` opener at SMALLER indentation than
+    the flagged line encloses it (Gleam blocks nest by indentation; the
+    repo is `gleam format`-clean, so this is deterministic)."""
+    flag_indent = indent_of(lines[flagged_idx])
+    for i in range(flagged_idx - 1, -1, -1):
+        line = lines[i]
+        if hook_case in line and indent_of(line) < flag_indent:
+            return True
+        # a shallower non-hook `case`/block between flag and hook-case means
+        # the flag is not inside the hook case
+        if indent_of(line) < flag_indent and re.search(r"\bcase\b|\}", line):
+            # keep scanning: the hook case may still be further up; only a
+            # `case` opener at the SAME nesting level as the flag's block
+            # disconnects it. Simplify: a `}` at shallower indent closes the
+            # hook case if we already saw it; before seeing it, any shallower
+            # `case` opener that is not the hook case disconnects.
+            if re.search(r"^\s*case\b", line) and hook_case not in line:
+                return False
+            if re.search(r"^\s*\}", line):
+                return False
+    return False
+
+
+def main() -> int:
+    text = PANEL.read_text(encoding="utf-8")
+    lines = text.splitlines()
+    violations = []
+    for i, line in enumerate(lines):
+        for action, hook_case in HOOK_FOR.items():
+            # construction shape only: identifier immediately followed by `]`
+            marker = action + "]"
+            if marker not in line:
+                continue
+            # pattern-match arms (`RefcheckTakeOver ->`) are exempt by shape
+            if re.search(rf"\b{action}\s*->", line):
+                continue
+            if not find_enclosing_hook_case(lines, i, hook_case):
+                violations.append(f"{PANEL.relative_to(ROOT)}:{i + 1}: {line.strip()[:120]}")
+    if violations:
+        print("AR-RC13 violation: hook-governed affordance constructed outside its hooks gate:")
+        for v in violations:
+            print(f"  {v}")
+        print("\nThe panel may only construct take-over/substitute actions inside")
+        print("`case call.hooks.can_take_over` / `case call.hooks.can_substitute_referee`")
+        print("blocks — the server hooks are the single source of truth (AR-RC13).")
+        return 1
+    print(f"refcheck hooks-derivation lint clean ({PANEL.name})")
+    return 0
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a/server/src/application/application_detail_handler.gleam b/server/src/application/application_detail_handler.gleam
index 52568f1b..e17cd3d8 100644
--- a/server/src/application/application_detail_handler.gleam
+++ b/server/src/application/application_detail_handler.gleam
@@ -1058,8 +1058,9 @@ fn encode_application(row: sql.GetApplicationDetailRow) -> json.Json {
 const written_response_disclaimer = "Written response, provenance-checked — not verbally confirmed. A quick call to the referee is the strongest final check."
 
 /// Terminal reference_call statuses (the migration's live-row exclusion set +
-/// `partial`). The canonical source is `compute_hooks_decoded`'s case — the
-/// migration's live-row index is the other half; keep both in lockstep.
+/// `partial`). The canonical source is `is_terminal_status` in the shared
+/// package (AR-RC13 guard, #607 item 5) — this is the same decision, encoded
+/// for DB-string rows; the lockstep unit test pins the two together.
 /// §8.2 hooks — the state rules the API computes so the panel never
 /// re-derives them client-side (AR-RC13).
 ///
@@ -1091,17 +1092,7 @@ pub fn compute_hooks(status: String) -> shared_reference_call.ReferenceCallHooks
 pub fn compute_hooks_decoded(
   status: shared_reference_call.ReferenceCallStatus,
 ) -> shared_reference_call.ReferenceCallHooks {
-  let terminal = case status {
-    shared_reference_call.FormCompleted -> True
-    shared_reference_call.Partial -> True
-    shared_reference_call.Unreachable -> True
-    shared_reference_call.Refused -> True
-    shared_reference_call.Objected -> True
-    shared_reference_call.ManualRecorded -> True
-    shared_reference_call.Failed -> True
-    shared_reference_call.Completed -> True
-    _ -> False
-  }
+  let terminal = shared_reference_call.is_terminal_status(status)
   shared_reference_call.ReferenceCallHooks(
     can_record_manual: !terminal,
     can_substitute_referee: status == shared_reference_call.Objected
@@ -1165,8 +1156,11 @@ pub fn compute_display_disclaimer(result_text: String) -> Option(String) {
 ///
 /// The result document rides as a JSON *string* field, so internal keys that
 /// would live inside it appear backslash-escaped on the wire (`\"referee_ip\"`
-/// not `"referee_ip"`) — both forms are checked so the guard can't be beaten
-/// by the escaping (Perkins-style lens finding, rc4-1 self-review #1).
+/// not `"referee_ip"`) — both forms are checked for EVERY §4.2 marker so the
+/// guard can't be beaten by the escaping (Perkins-style lens finding, rc4-1
+/// self-review #1; #607 item 1 — the escaped marker set previously covered
+/// only the two IP/UA keys, leaving escaped `form_token`/`payload_ref`
+/// unchecked).
 /// Returns True when the serialized text is clean.
 pub fn verify_payload_has_no_internal_fields(payload: String) -> Bool {
   let markers = [
@@ -1174,6 +1168,8 @@ pub fn verify_payload_has_no_internal_fields(payload: String) -> Bool {
     "\"payload_ref\"",
     "\"referee_ip\"",
     "\"referee_user_agent\"",
+    "\\\"form_token\\\"",
+    "\\\"payload_ref\\\"",
     "\\\"referee_ip\\\"",
     "\\\"referee_user_agent\\\"",
   ]
@@ -1213,10 +1209,7 @@ pub fn encode_reference_call(
     ref_slot: shared_reference_call.ref_slot_from_string(row.ref_slot),
     owner_label: shared_reference_call.owner_label_from_string(row.owner_label),
     status: shared_reference_call.status_from_string(row.status),
-    outcome: case row.outcome {
-      "" -> None
-      s -> Some(shared_reference_call.outcome_from_string(s))
-    },
+    outcome: shared_reference_call.outcome_from_string_optional(row.outcome),
     attempt_count: row.attempt_count,
     next_attempt_at: case row.next_attempt_at {
       "" -> None
diff --git a/server/test/application/application_detail_handler_test.gleam b/server/test/application/application_detail_handler_test.gleam
index 9f5fda6a..c949ff78 100644
--- a/server/test/application/application_detail_handler_test.gleam
+++ b/server/test/application/application_detail_handler_test.gleam
@@ -1,6 +1,7 @@
 import application/application_detail_handler
 import application/sql
 import gleam/json
+import gleam/list
 import gleam/option.{None, Some}
 import gleam/string
 import gleeunit/should
@@ -429,6 +430,19 @@ pub fn verify_payload_guard_detects_internal_markers_test() {
     "{\"data\":{\"reference_calls\":[{\"objection_detail\":{\"payload_ref\":\"p\"}}]}}",
   )
   |> should.be_false
+  // #607 item 1: the ESCAPED result-string forms for the two non-IP
+  // markers — a corrupt/spoofed stored result carrying form_token or
+  // payload_ref at any path ships backslash-escaped on the wire and must
+  // be caught too (the escaped set previously covered only referee_ip /
+  // referee_user_agent).
+  application_detail_handler.verify_payload_has_no_internal_fields(
+    "{\"data\":{\"reference_calls\":[{\"result\":\"{\\\"form_token\\\": \\\"tok\\\"}\"}]}}",
+  )
+  |> should.be_false
+  application_detail_handler.verify_payload_has_no_internal_fields(
+    "{\"data\":{\"reference_calls\":[{\"result\":\"{\\\"payload_ref\\\": \\\"p\\\"}\"}]}}",
+  )
+  |> should.be_false
 }
 
 /// The derived booleans (ip_matches_applicant) survive the strip — only the
@@ -468,6 +482,30 @@ pub fn encode_reference_call_pre_terminal_nullables_test() {
   |> should.be_true
 }
 
+/// #607 item 2 (unknown-outcome rule): an UNRECOGNISED outcome string in an
+/// expand-then-contract window encodes as null — absent, never the
+/// OutcomeUnreachable fallback — so a recordable row never carries a
+/// terminal-looking outcome on the wire. Hooks come from status alone and
+/// stay recordable; outcome and hooks can never diverge (self-review #3).
+pub fn encode_reference_call_unknown_outcome_encodes_null_test() {
+  let row =
+    sample_reference_call_row(
+      status: "queued",
+      outcome: "some_future_value",
+      result: "",
+    )
+  let wire =
+    application_detail_handler.encode_reference_call(row)
+    |> json.to_string
+  wire |> string.contains("\"outcome\":null") |> should.be_true
+  // The hooks still say recordable (status-derived), and the wire carries
+  // no fabricated "unreachable" outcome on the recordable row.
+  wire
+  |> string.contains("\"can_record_manual\":true")
+  |> should.be_true
+  wire |> string.contains("\"unreachable\"") |> should.be_false
+}
+
 /// Unparseable attempts degrade to [] (never a fabricated log entry).
 pub fn encode_reference_call_malformed_attempts_test() {
   let row =
@@ -547,6 +585,44 @@ pub fn attempt_log_empty_for_queued_row_test() {
   |> should.equal([])
 }
 
+/// #607 item 5 (AR-RC13 guard): the timeline's `terminal_statuses` string
+/// list must stay in LOCKSTEP with the shared `is_terminal_status` truth the
+/// hooks are computed from — every entry encodes to a status the shared fn
+/// calls terminal, and every known non-terminal status encodes to False. A
+/// future enum addition that lands in one place and not the other fails here.
+pub fn terminal_statuses_lockstep_with_shared_truth_test() {
+  let terminal = [
+    "form_completed",
+    "manual_recorded",
+    "unreachable",
+    "refused",
+    "objected",
+    "partial",
+    "failed",
+    "completed",
+  ]
+  let non_terminal = [
+    "queued",
+    "skipped",
+    "contact_initiated",
+    "awaiting_correction",
+    "scheduled",
+    "calling",
+  ]
+  list.each(terminal, fn(s) {
+    shared_reference_call.is_terminal_status(
+      shared_reference_call.status_from_string(s),
+    )
+    |> should.be_true
+  })
+  list.each(non_terminal, fn(s) {
+    shared_reference_call.is_terminal_status(
+      shared_reference_call.status_from_string(s),
+    )
+    |> should.be_false
+  })
+}
+
 /// A started row's send batches label by cadence position: batch 0
 /// invitation, batch 1 co-nudge, batches 2+ reminders (ordinal in detail).
 /// One entry per channel (the client joins same-`at` for "email + SMS").
@@ -613,6 +689,40 @@ pub fn attempt_log_appends_lifecycle_events_test() {
   ])
 }
 
+/// #607 item 3: the format mix can appear INVERTED — a legacy/corrupt
+/// attempt row whose stored `at` uses the PG `::text` space form
+/// ("2026-08-01 10:04:00+00") alongside RFC3339 T-form attempts and column
+/// stamps. The sort normalises EVERY side (space->T) before the lexical
+/// compare, so same-day events still order by instant: the space-form
+/// 08:04 invite sorts BEFORE the T-form 08:05 co-nudge and the space-form
+/// 21:12 form-opened sorts LAST.
+pub fn attempt_log_sorts_inverted_format_mix_test() {
+  application_detail_handler.build_attempt_log(
+    attempts: [
+      attempt("2026-08-01 10:04:00+00", "email"),
+      attempt("2026-08-01T10:05:00Z", "sms"),
+      attempt("2026-08-02T10:00:00Z", "email"),
+    ],
+    form_opened_at: "2026-08-01 21:12:00+00",
+    corrected_at: "",
+    taken_over_at: "",
+    substituted_at: "",
+    terminalized_at: "",
+    submitted_at: "",
+    objected_at: "",
+    updated_at: "",
+    status: "contact_initiated",
+  )
+  |> should.equal([
+    // Space-form attempt at normalises to the T separator before the sort.
+    entry("invitation_sent", "2026-08-01T10:04:00+00", "email", "delivered", ""),
+    // T-form attempt on the same day — later instant, batch 1 (co_nudge).
+    entry("co_nudge", "2026-08-01T10:05:00Z", "sms", "delivered", ""),
+    entry("form_opened", "2026-08-01T21:12:00+00", "", "", ""),
+    entry("reminder_sent", "2026-08-02T10:00:00Z", "email", "delivered", "1"),
+  ])
+}
+
 /// The post-correction re-invitation restarts the cadence at batch 0 — the
 /// corrected row's fresh invite is "Invitation sent", never a mislabelled
 /// "Reminder N" (correct_reference_call resets attempt_count to 0).
diff --git a/shared/src/shared/reference_call.gleam b/shared/src/shared/reference_call.gleam
index 2760ff9c..a333ed79 100644
--- a/shared/src/shared/reference_call.gleam
+++ b/shared/src/shared/reference_call.gleam
@@ -9,7 +9,7 @@
 
 import gleam/dynamic/decode
 import gleam/json
-import gleam/option.{type Option, None}
+import gleam/option.{type Option, None, Some}
 
 /// Mirrors the `reference_call_status` PG enum (14 values).
 /// `partial` is v1-active (A2: abandoned-with-draft-answers terminal);
@@ -140,6 +140,27 @@ pub fn status_from_string(value: String) -> ReferenceCallStatus {
   }
 }
 
+/// The TERMINALITY truth (AR-RC13 guard, #607 item 5): the single source of
+/// truth for "is this status terminal?". The server's `can_record_manual`
+/// hook is computed from this, and the client panel consumes the hook — the
+/// client holds NO terminality list of its own, so the RC4.2-r1 bug class
+/// (a client-side status list that omits a terminal variant) cannot recur.
+/// `completed` is the v2-reserved voice terminal: including it here is what
+/// the client-side re-implementations kept dropping.
+pub fn is_terminal_status(status: ReferenceCallStatus) -> Bool {
+  case status {
+    FormCompleted
+    | ManualRecorded
+    | Partial
+    | Unreachable
+    | Refused
+    | Objected
+    | Failed
+    | Completed -> True
+    _ -> False
+  }
+}
+
 /// Dynamic decoder — unknown strings FAIL (unlike `status_from_string`), so
 /// malformed API payloads surface as decode errors rather than silent
 /// coercions (ai_analysis.gleam precedent).
@@ -216,6 +237,40 @@ pub fn outcome_from_string(value: String) -> ReferenceCallOutcome {
   }
 }
 
+/// The §8.1 WIRE inverse of `encode_outcome` (the unknown-outcome rule,
+/// #607 item 2): a known outcome string encodes as Some, and '' OR an
+/// unrecognised value encodes as None — absent, never the
+/// `OutcomeUnreachable` fallback. In an enum expand-then-contract window an
+/// old server reading a new value must render NO outcome, not a
+/// terminal-looking "unreachable" on a recordable row (hooks are computed
+/// from status alone, so the wire could otherwise show a recordable row
+/// carrying a terminal outcome — the divergence self-review #3 forbids).
+/// `outcome_from_string` keeps its internal fallback for non-wire callers;
+/// the WIRE never round-trips it.
+pub fn outcome_from_string_optional(
+  value: String,
+) -> Option(ReferenceCallOutcome) {
+  case value {
+    "" -> None
+    "completed" -> Some(OutcomeCompleted)
+    "partial" -> Some(OutcomePartial)
+    "voicemail" -> Some(OutcomeVoicemail)
+    "no_answer" -> Some(OutcomeNoAnswer)
+    "busy" -> Some(OutcomeBusy)
+    "refused" -> Some(OutcomeRefused)
+    "wrong_number" -> Some(OutcomeWrongNumber)
+    "invalid_number" -> Some(OutcomeInvalidNumber)
+    "declined_ai" -> Some(OutcomeDeclinedAi)
+    "language_barrier" -> Some(OutcomeLanguageBarrier)
+    "gatekeeper_blocked" -> Some(OutcomeGatekeeperBlocked)
+    "objected" -> Some(OutcomeObjected)
+    "unreachable" -> Some(OutcomeUnreachable)
+    "form_completed" -> Some(OutcomeFormCompleted)
+    "manual_recorded" -> Some(OutcomeManualRecorded)
+    _ -> None
+  }
+}
+
 pub fn outcome_decoder() -> decode.Decoder(ReferenceCallOutcome) {
   use value <- decode.then(decode.string)
   case value {
@@ -465,6 +520,14 @@ pub fn attempt_log_entry_decoder() -> decode.Decoder(AttemptLogEntry) {
 /// The hooks object (§8.2): the state rules the API computes so the panel
 /// never re-derives them client-side (AR-RC13). Server-computed at
 /// serialisation from the row's status.
+///
+/// **Unknown-outcome rule (#607 item 2):** hooks are computed from the row's
+/// STATUS only — an unrecognised outcome value NEVER influences a hook, and
+/// the wire encoder maps an unrecognised outcome to absent (null), never to
+/// the `OutcomeUnreachable` fallback (a recordable row must never carry a
+/// terminal-looking outcome on the wire). Status's own fallback is inert by
+/// design: an unrecognised status decodes to `Failed`, so hooks and the
+/// rendered status can never diverge on the wire.
 pub type ReferenceCallHooks {
   ReferenceCallHooks(
     can_record_manual: Bool,
diff --git a/shared/test/reference_call_test.gleam b/shared/test/reference_call_test.gleam
index 82a208db..b1e6f5d4 100644
--- a/shared/test/reference_call_test.gleam
+++ b/shared/test/reference_call_test.gleam
@@ -87,6 +87,33 @@ pub fn every_status_round_trips_test() {
   })
 }
 
+/// #607 item 5 (AR-RC13 guard): the terminality truth-table — EVERY status
+/// variant names its terminality explicitly. Adding a new terminal status
+/// without updating this table (or the fn) fails here, and the same fn is
+/// what the server's can_record_manual hook and the client fixture consume.
+pub fn is_terminal_status_truth_table_test() {
+  list.each(all_statuses(), fn(status) {
+    let expected = case status {
+      FormCompleted
+      | ManualRecorded
+      | Partial
+      | Unreachable
+      | Refused
+      | Objected
+      | Failed
+      | Completed -> True
+      Queued
+      | Skipped
+      | ContactInitiated
+      | AwaitingCorrection
+      | Scheduled
+      | Calling -> False
+    }
+    reference_call.is_terminal_status(status)
+    |> should.equal(expected)
+  })
+}
+
 pub fn every_outcome_round_trips_test() {
   list.each(all_outcomes(), fn(outcome) {
     outcome
@@ -244,6 +271,21 @@ pub fn unknown_outcome_never_falls_back_to_success_test() {
   |> should.equal(OutcomeUnreachable)
 }
 
+/// The §8.1 WIRE form (#607 item 2, unknown-outcome rule): an unrecognised
+/// outcome encodes as None — absent, never the OutcomeUnreachable fallback
+/// (a recordable row must never carry a terminal-looking outcome on the
+/// wire). '' also encodes as None (the pre-terminal absent marker).
+pub fn outcome_from_string_optional_unknown_is_none_test() {
+  reference_call.outcome_from_string_optional("some_future_value")
+  |> should.equal(None)
+  reference_call.outcome_from_string_optional("")
+  |> should.equal(None)
+  reference_call.outcome_from_string_optional("completed")
+  |> should.equal(Some(OutcomeCompleted))
+  reference_call.outcome_from_string_optional("unreachable")
+  |> should.equal(Some(OutcomeUnreachable))
+}
+
 // -- RC4.1 §8.1 payload-entry codecs (AR21 round-trips) -----------------------
 
 fn sample_attempt() -> ReferenceCallAttempt {


--- SPEC / CONTEXT ---
JOB BRIEFING (the spec for this PR):
# Briefing — righttenantry-refcheck-followup-607 (#607 follow-up intake)

- **Job id:** `righttenantry-refcheck-followup-607`
- **Repo:** RightTenantry · **Base:** `develop` · **Slug:** `refcheck-followup-607`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — minions. NOT kimi, NOT glm).
  Any mega-minion you spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow).
- **Perkins:** `pr_review: 1` (app-surface hardening + an architecture-level guard — the U3
  scope guard reserves `pr_review=0` for CI/ops-tooling only).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `develop` (RC4.1–4.4 merged — the RC4 series is complete). Rebase onto
  origin/develop if it moves mid-work; clean-rebase hygiene (`git diff --check` before
  force-with-lease).

## Mission (GitHub issue #607 — the five carried advisories)

The RC4 line shipped; Perkins' carried warnings are filed in **#607** (read the issue body —
it is the canonical spec). Implement ALL FIVE items. Each was non-blocking at verdict time;
each is a real hardening candidate.

| # | Item | Source | Acceptance |
|---|---|---|---|
| 1 | **Escaped-form markers** — extend the marker set to cover `form_token` + `payload_ref` | #604 r1 (§4.2 payload strip) | Markers cover EVERY payload field; a test proves the strip holds AND the markers now catch what they missed. Defense-in-depth, not a strip replacement. |
| 2 | **Unknown-outcome fallback** — explicit behavior contract for the hooks object when an outcome is unknown (currently implicit) | #604 r1 | A NAMED fallback rule in the hooks contract + a test pinning it. |
| 3 | **Timeline sort format-mix inversion** — the attempt timeline sorts inconsistently across mixed datetime formats | #605 r1 | A mixed-format fixture sorts correctly; pin it so it cannot regress. |
| 4 | **Em-dash pin gap** — the global em-dash ban has no lint enforcement | #605 r1 | A lint/check that FAILS on em-dash; wired into the CI gate. |
| 5 | **AR-RC13 systemic guard** — client-side re-derivation of terminality/substitution instead of using server hooks is the bug class that blocked BOTH RC4.2-r1 and RC4.3-r1 | systemic (RC4.2 r1 + RC4.3 r1) | A durable architecture-level guard (lint rule / test rule / shared-type guard) making the server hooks the single source of truth; PROVE the guard would have caught the historical re-derivations (walk it against the fixed code or the PR diffs); document the guard in the architecture doc as the AR-RC13 lesson entry. |

**Repo map:** `server/` (payload strip §4.2, hooks, webhooks) · `client/` (reference panel,
timeline component) · `shared/` (codecs/types) · `scripts/`/`Makefile` (lint + test entry
points) · architecture canon: `_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md` + `epics-reference-checking-v1-2026-07-30.md` (AR-RC13 lives there).

**Verify:** full test suite green, new pins green (items 1–3, 5), lint green + CI gate wired
(item 4), PR body maps each issue item → fix → pin. Launchable increment where practical.

**Scope guard:** the five #607 items ONLY — no unrelated refactors, no design changes. Each
fix stays minimal; where an item has a plausible alternative reading, prefer the more
restrictive one and flag it in the PR body.

## Dispatch parameters

```
repo: RightTenantry
repo_root: /Users/moses/code/RightTenantry
slug: refcheck-followup-607
base: develop
model: deepseek/deepseek-v4-flash
github_issue: 607
pr_review: 1
```


ROUND BRIEFING (what the PR claims to do + lens guards):
# Perkins briefing — round 1: righttenantry-refcheck-followup-607

- **PR:** https://github.com/solarity-services/RightTenantry/pull/610 (targets `develop`)
- **Reviewed sha:** `955284755d1c64e8884d557a2999fadc2a287db2` (short `9552847`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-followup-607-r1` — detached at exactly the reviewed sha. Trust it, not `origin/develop`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-followup-607.md` + GitHub issue #607 (the canonical spec — dump it with `gh issue view 607 --json title,body,comments` into the round dir) + the architecture canon (`AR-RC13`). GitHub issue: **607**.
- **Model:** `deepseek/deepseek-v4-pro` (Perkins reasoning tier). Launch EVERY lens pane with `pi --model deepseek/deepseek-v4-pro`. NEVER glm-5.2 (retired).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**The five #607 carried advisories** (each non-blocking at its source verdict; hardening):
1. **Escaped-form markers** — the §4.2 payload-strip marker set extended to cover `form_token` + `payload_ref` (every payload field covered; the strip holds AND the markers now catch what they missed).
2. **Unknown-outcome fallback** — a NAMED contract rule: unrecognised outcome → `null` on the wire, NEVER `OutcomeUnreachable`; shared `outcome_from_string_optional` + shared & server encode pins.
3. **Format-mix sort** — the RC4.4 timeline normalize covers both datetime sides; the one missing fixture (space-form alongside T-form) added + pinned.
4. **Em-dash pin** — `scripts/lint_em_dash.py` + CI step FAILS on em-dash; two real shipping em-dashes removed (batch line + nudge-skipped join) into dash-free fn-built labels in copy.gleam, scanned by the ban test.
5. **AR-RC13 systemic guard** — `shared is_terminal_status` = single terminality truth (server hooks + client fixture consume it; the drifting test-side list deleted); truth-table + lockstep pins; `scripts/lint_refcheck_hooks.py` + CI step; proof walk: restoring the RC4.2-r1 status list fails the Completed-terminal test, restoring the RC4.3-r1 menu shape fails the lint; AR-RC13 lesson entry + AD-11 cross-ref in the architecture doc.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 ITEM 5 LOAD-BEARING — the AR-RC13 guard is the point of this PR.** The systemic guard must make server hooks the single source of terminality truth. Verify: (a) `is_terminal_status` is genuinely SHARED (server hooks + client both consume it — no client-side re-derivation list remains anywhere); (b) the truth-table + lockstep pins exist and bite; (c) the lints run in CI and FAIL on the historical shapes (the proof walk — spot-check the lint actually detects the RC4.2-r1-style list and the RC4.3-r1-style menu re-derivation; a lint that can't fail is decorative); (d) the test-side drifting list is really deleted, not duplicated. A client-side terminality re-derivation surviving anywhere = a blocker (the RC4.2-r1/RC4.3-r1 blocker class).
- **🚨 ITEM 1 — the strip still holds.** The marker extension is defense-in-depth ON TOP of the §4.2 strip: verify the strip itself is unchanged in behavior AND the markers now cover form_token + payload_ref (a test proves both). A weakened strip or a still-uncovered payload field = a real defect.
- **🚨 ITEM 2 — the fallback contract is NAMED and pinned.** Unrecognised outcome → null on the wire, never OutcomeUnreachable; the encode pins cover shared + server. An implicit/undocumented fallback or an OutcomeUnreachable on unknown = a real defect.
- **ITEM 3 — the pin bites.** The mixed-format fixture (space-form alongside T-form) sorts correctly and is pinned; the RC4.4 normalize is the mechanism (verify both sides normalise before compare).
- **ITEM 4 — the lint FAILS on em-dash.** `scripts/lint_em_dash.py` fails on an em-dash in the scanned surface; wired into CI (the workflow diff); negative controls exist. RT em-dash ban applies to implementer-authored user-facing strings — the two removed em-dashes are gone from the shipped copy.
- **Scope guard:** the five #607 items ONLY — flag anything beyond (no design changes, no unrelated refactors).
- **base = `develop`** (RC4.1–4.4 merged — carry-forward only; do NOT re-open RC4-series findings; item 3's RC4.4 origin is expected, not a defect).
- **a11y + AC testids** untouched by this PR (verify no regression).
- **bmad-quirk heads-up (context, not a finding):** review the PR content as-is at the sha.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-followup-607/r1/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = the original job briefing + the GitHub issue (dump it with `gh issue view 607 --json title,body,comments` into the round dir first), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-followup-607/r1`, and `prior_findings` = the previous round's `consolidated.json` when N > 1 (re-review: fix audit first, carry-forward markers). The headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r<N>` labels), the `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and writing `consolidated.json`. Its verdict thresholds are yours below. You MUST close every lens pane before finishing.
- **Verdict → review event:**
  - 0 blockers → `--approve`
  - 1–3 blockers → `--request-changes`
  - 4+ blockers → `--request-changes`, body leads with "MAJOR REWORK"
  - **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru ("incomplete review").
- Post as the app (owner parsed from the PR URL). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — capture STDOUT ONLY. NEVER append `2>&1`.
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` -> the mint failed; fall back to `gh pr comment <pr> --body-file <body.md>`, note `fallback-comment` in your ledger note, and call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`
- Body format:
  ```
  ## 🤖 Perkins automated review — round <N> of 3
  **Job:** <job-id> · **Reviewed sha:** <short> · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed against the code — <rejected> discarded as false-positive[, <u> kept as [unverified]]

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Address findings and push — I re-review automatically on the new sha.
  After round 3, the human takes over._
  ```
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-followup-607-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.


GITHUB ISSUE #607 (canonical spec, JSON dump):
{"body":"Perkins carried-warning pile from the RC4 line, filed so nothing evaporates. Each item was non-blocking at its verdict; all are real hardening candidates. Sources: Perkins r1 on #604 (RC4.1) and r1 on #605 (RC4.2).\n\n## From #604 (RC4.1 payload) r1 — 2 items\n- **§4.2 escaped-form markers miss `form_token`/`payload_ref`** — defense-in-depth gap: the strip itself holds, but the escaped-form marker set does not cover these two fields; tighten markers.\n- **Unknown-outcome fallback vs hooks** — behavior contract when an outcome is unknown: the hooks object needs an explicit fallback rule (currently implicit).\n\n## From #605 (RC4.2 panel) r1 — 2 items\n- **Timeline sort format-mix inversion** — the attempt timeline sorts inconsistently across mixed datetime formats (non-blocking, real).\n- **Em-dash pin gap** — em-dash copy hygiene gap under the global em-dash ban; pin a lint/check so it cannot regress.\n\n## Systemic (RC4.2 r1 + RC4.3 r1) — 1 item\n- **AR-RC13 class: client-side state re-derivation** — the same bug class (client re-deriving terminality/substitution instead of using server hooks) blocked BOTH rounds. Fix per-PR is done; the durable fix is an architecture-level guard (hooks = single source of truth; add a lint/test rule or shared-type guard so re-derivation cannot recur).","comments":[{"id":"IC_kwDORzoYgc8AAAABOj95Pg","author":{"login":"mssoka"},"authorAssociation":"MEMBER","body":"**Infra flake sighting (3rd today — #606 x2, #608 x1):** Terraform validate job times out downloading the Cloudflare provider from github.com releases; all code jobs green; rerun recovers. Pattern: if it keeps flaking, the terraform validate step needs a provider-cache/mirror (or a wait-for-GitHub-incident). Silas flagged 2026-08-12 — tracking here per the intake rule (3rd sighting = real infra debt, not noise).","createdAt":"2026-08-12T20:05:33Z","includesCreatedEdit":false,"isMinimized":false,"minimizedReason":"","reactionGroups":[],"url":"https://github.com/solarity-services/RightTenantry/issues/607#issuecomment-5272205630","viewerDidAuthor":true},{"id":"IC_kwDORzoYgc8AAAABOkLkfw","author":{"login":"mssoka"},"authorAssociation":"MEMBER","body":"**Systemic class, 2nd sighting (2026-08-12, #606 r2 W3):** format-mixed datetime comparisons (RFC3339 vs `::text`) — same family as the RC4.2 timeline-sort warning. Sibling of the existing item; the durable fix is one shared datetime-comparison helper/lint rule, not per-PR patches. Tracked here so the class gets one fix, not three.","createdAt":"2026-08-12T20:28:04Z","includesCreatedEdit":false,"isMinimized":false,"minimizedReason":"","reactionGroups":[],"url":"https://github.com/solarity-services/RightTenantry/issues/607#issuecomment-5272429695","viewerDidAuthor":true}],"title":"Follow-up intake: Perkins carried warnings (RC4.1 + RC4.2) + AR-RC13 systemic lesson"}


--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "acceptance",
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

FILE-OUTPUT CONTRACT (mechanically checked, not negotiated):
- Your ENTIRE final answer must be your JSON array, written to this exact file path: /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-followup-607/r1/acceptance.json
- Write the file with your file-writing tool, then STOP. Nothing else.
- Do not print the JSON in chat as your answer; the file is the deliverable.
- If you found nothing, write an empty array `[]` to that file.
