You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

The repository worktree you may read is at:
/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-611-panel-persist-r2
It is detached at exactly the reviewed sha 0b021b000c43fba67228df1fb19d1cb8f7f02392. Read files there; never run mutating commands (no builds that write, no git checkout, no edits).

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
diff --git a/client/src/components/reference_panel.gleam b/client/src/components/reference_panel.gleam
index 252389a9..cec2adfe 100644
--- a/client/src/components/reference_panel.gleam
+++ b/client/src/components/reference_panel.gleam
@@ -1108,21 +1108,21 @@ fn view_edit_trio(
   html.div([class("space-y-2")], [
     html.div([class("grid grid-cols-1 sm:grid-cols-3 gap-2")], [
       text_input(
-        slot,
+        call.reference_call_id,
         "name",
         copy.refcheck_field_name,
         name,
         "refcheck-edit-name-" <> slot,
       ),
       text_input(
-        slot,
+        call.reference_call_id,
         "email",
         copy.refcheck_field_email,
         email,
         "refcheck-edit-email-" <> slot,
       ),
       text_input(
-        slot,
+        call.reference_call_id,
         "phone",
         copy.refcheck_field_phone,
         phone,
diff --git a/client/test/client_test.gleam b/client/test/client_test.gleam
index 1998c2ec..1a1ac3e9 100644
--- a/client/test/client_test.gleam
+++ b/client/test/client_test.gleam
@@ -29,6 +29,9 @@ import gleeunit
 import gleeunit/should
 import helpers/format
 import helpers/leaderboard as leaderboard_helpers
+import lustre/dev/query
+import lustre/dev/simulate
+import lustre/effect
 import lustre/element
 import model
 import msg
@@ -6722,3 +6725,239 @@ pub fn refcheck_export_success_toasts_dash_free_oq5_test() {
     [] -> panic as "export success must toast"
   }
 }
+
+/// #611 keystroke-swallow pin: typing into the refcheck edit-trio must land
+/// in the `refcheck_edit` dict under the ROW's `reference_call_id` and render
+/// back into the field. The bug was a key mismatch — the trio inputs sent
+/// `UserEditedRefcheckTrio` keyed by the ref SLOT ("landlord_ref") while the
+/// view/update/save all key by `reference_call_id` ("rc-1"), so keystrokes
+/// wrote to a dict entry the view never read: the field snapped back to the
+/// prefill on every render and Save persisted the ORIGINAL contact with a
+/// success toast (the #611 repro). This drives the REAL runtime path —
+/// `simulate.input` → `cache.handle` (decode2) → `client.update` → view —
+/// and asserts all three field branches (W2), the dict writes, the
+/// re-rendered values, AND the SAVE half (Perkins r1 B1): the save click
+/// must read the same dict entry the keystrokes wrote and fire with the
+/// typed values retained.
+pub fn refcheck_trio_keystroke_lands_in_field_test() {
+  let detail =
+    application_detail.ApplicationDetail(..test_detail(), reference_calls: [
+      reference_call.ReferenceCallDetail(
+        ..refcheck_call("rc-1", reference_call.AwaitingCorrection),
+        contact_name: option.Some("Maeve O'Brien"),
+        contact_email: option.Some("maeve@example.ie"),
+        contact_phone: option.Some("+353 87 123 4567"),
+      ),
+    ])
+  let m =
+    model.Model(
+      ..model.initial(),
+      route: routes.ApplicationDetail(
+        vacancy_id: "uuid-vac-1",
+        id: "uuid-app-1",
+      ),
+      application_detail: remote_data.Success(detail),
+      refcheck_expanded: set.from_list(["rc-1"]),
+      refcheck_edit: dict.from_list([
+        #(
+          "rc-1",
+          model.RefcheckEdit(
+            call_id: "rc-1",
+            kind: model.RefcheckEditCorrect,
+            name: "Maeve O'Brien",
+            email: "maeve@example.ie",
+            phone: "+353 87 123 4567",
+            saving: False,
+            error: None,
+          ),
+        ),
+      ]),
+    )
+  let sim =
+    simulate.start(
+      simulate.application(
+        init: fn(_) { #(m, effect.none()) },
+        update: client.update,
+        view: application_detail_page.view,
+      ),
+      Nil,
+    )
+  // W2: every field branch of UserEditedRefcheckTrio lands in the dict under
+  // the ROW's id — name, email, AND phone (a mistyped literal would hit the
+  // silent `_ -> edit` fallback and drop keystrokes; each branch is typed).
+  let sim =
+    simulate.input(
+      sim,
+      on: query.element(matching: query.attribute(
+        "data-testid",
+        "refcheck-edit-name-landlord_ref",
+      )),
+      value: "Maeve Fixed",
+    )
+  let sim =
+    simulate.input(
+      sim,
+      on: query.element(matching: query.attribute(
+        "data-testid",
+        "refcheck-edit-email-landlord_ref",
+      )),
+      value: "maeve.fixed@example.ie",
+    )
+  let sim =
+    simulate.input(
+      sim,
+      on: query.element(matching: query.attribute(
+        "data-testid",
+        "refcheck-edit-phone-landlord_ref",
+      )),
+      value: "+353 87 999 0000",
+    )
+  let edited = simulate.model(sim).refcheck_edit |> dict.get("rc-1")
+  case edited {
+    Ok(edit) -> {
+      edit.name |> should.equal("Maeve Fixed")
+      edit.email |> should.equal("maeve.fixed@example.ie")
+      edit.phone |> should.equal("+353 87 999 0000")
+    }
+    Error(_) -> panic as "edit state must exist for rc-1"
+  }
+  // And the re-rendered inputs carry the typed values (no snap-back).
+  let html = simulate.view(sim) |> element.to_string
+  html |> string.contains("value=\"Maeve Fixed\"") |> should.be_true
+  html
+  |> string.contains("value=\"maeve.fixed@example.ie\"")
+  |> should.be_true
+  html |> string.contains("value=\"+353 87 999 0000\"") |> should.be_true
+
+  // B1 (Perkins r1): the SAVE half — the save click must read the SAME dict
+  // entry the keystrokes wrote and fire with the typed values. The #611
+  // harm class was save persisting the ORIGINAL contact with a success
+  // toast; a future re-key of the save path must fail here.
+  let sim =
+    simulate.click(
+      sim,
+      on: query.element(matching: query.attribute(
+        "data-testid",
+        "refcheck-edit-save-landlord_ref",
+      )),
+    )
+  let saved = simulate.model(sim).refcheck_edit |> dict.get("rc-1")
+  case saved {
+    Ok(edit) -> {
+      edit.saving |> should.be_true
+      edit.name |> should.equal("Maeve Fixed")
+      edit.email |> should.equal("maeve.fixed@example.ie")
+      edit.phone |> should.equal("+353 87 999 0000")
+    }
+    Error(_) -> panic as "edit state must survive the save click"
+  }
+}
+
+/// #611 W1 (Perkins r1): the SUBSTITUTE trio is the same `view_edit_trio`
+/// component — keystrokes must land under `reference_call_id` there too —
+/// and a detail REFETCH (background poll) with a reordered call list must
+/// not drop the in-progress edit. Acceptance 2's reorder clause: the typed
+/// substitute survives a server re-sort of the rows.
+pub fn refcheck_substitute_trio_keystroke_survives_refetch_test() {
+  let detail =
+    application_detail.ApplicationDetail(..test_detail(), reference_calls: [
+      reference_call.ReferenceCallDetail(
+        ..refcheck_call("rc-1", reference_call.Objected),
+        hooks: reference_call.ReferenceCallHooks(
+          ..reference_call.ReferenceCallHooks(
+            can_record_manual: False,
+            can_substitute_referee: False,
+            can_retry: False,
+            can_take_over: False,
+          ),
+          can_substitute_referee: True,
+        ),
+        contact_name: option.Some("Denis O'Shea"),
+        contact_email: option.Some("denis@example.ie"),
+        contact_phone: option.Some("+353 87 555 6666"),
+      ),
+      refcheck_call("rc-2", reference_call.Queued),
+    ])
+  let m =
+    model.Model(
+      ..model.initial(),
+      route: routes.ApplicationDetail(
+        vacancy_id: "uuid-vac-1",
+        id: "uuid-app-1",
+      ),
+      application_detail_request_id: option.Some("uuid-app-1"),
+      application_detail: remote_data.Success(detail),
+      refcheck_expanded: set.from_list(["rc-1"]),
+      // Substitute starts EMPTY (r2 W5) — the trio is open, nothing typed yet.
+      refcheck_edit: dict.from_list([
+        #(
+          "rc-1",
+          model.RefcheckEdit(
+            call_id: "rc-1",
+            kind: model.RefcheckEditSubstitute,
+            name: "",
+            email: "",
+            phone: "",
+            saving: False,
+            error: None,
+          ),
+        ),
+      ]),
+    )
+  let sim =
+    simulate.start(
+      simulate.application(
+        init: fn(_) { #(m, effect.none()) },
+        update: client.update,
+        view: application_detail_page.view,
+      ),
+      Nil,
+    )
+  let sim =
+    simulate.input(
+      sim,
+      on: query.element(matching: query.attribute(
+        "data-testid",
+        "refcheck-edit-email-landlord_ref",
+      )),
+      value: "new.referee@example.ie",
+    )
+  let typed = simulate.model(sim).refcheck_edit |> dict.get("rc-1")
+  case typed {
+    Ok(edit) -> edit.email |> should.equal("new.referee@example.ie")
+    Error(_) -> panic as "substitute edit state must exist for rc-1"
+  }
+  // Refetch with the rows REORDERED (rc-2 first) — the poll's refetch must
+  // preserve the in-progress edit keyed by reference_call_id.
+  let reordered =
+    application_detail.ApplicationDetail(..test_detail(), reference_calls: [
+      refcheck_call("rc-2", reference_call.Queued),
+      reference_call.ReferenceCallDetail(
+        ..refcheck_call("rc-1", reference_call.Objected),
+        hooks: reference_call.ReferenceCallHooks(
+          ..reference_call.ReferenceCallHooks(
+            can_record_manual: False,
+            can_substitute_referee: False,
+            can_retry: False,
+            can_take_over: False,
+          ),
+          can_substitute_referee: True,
+        ),
+        contact_name: option.Some("Denis O'Shea"),
+        contact_email: option.Some("denis@example.ie"),
+        contact_phone: option.Some("+353 87 555 6666"),
+      ),
+    ])
+  let sim =
+    simulate.message(sim, msg.ApiReturnedApplicationDetail(Ok(reordered)))
+  let survived = simulate.model(sim).refcheck_edit |> dict.get("rc-1")
+  case survived {
+    Ok(edit) -> edit.email |> should.equal("new.referee@example.ie")
+    Error(_) -> panic as "typed substitute must survive the reordered refetch"
+  }
+  // And the field still renders the typed value after the refetch.
+  simulate.view(sim)
+  |> element.to_string
+  |> string.contains("value=\"new.referee@example.ie\"")
+  |> should.be_true
+}


--- SPEC / CONTEXT ---
# GitHub issue #611 (the spec) — bug-hunt: reference_checks panel-correct/panel-substitute — refcheck edit-trio inputs swallow keystrokes; Save persists OLD contact

## Failure

Scenario `reference_checks/panel-correct` (and `reference_checks/panel-substitute`) — the refcheck edit-trio inputs **swallow keystrokes**: typed text never reaches the model and the field snaps back to the prefilled value ~150ms after every input event. Confirmed live by the user, by two independent bug-hunt agents, and by a controlled repro session.

**Root cause:** the input event reaches the Lustre runtime but the message never dispatches — the runtime's `decode2` returns `DispatchedEvent` (handler-path lookup / decode failure), which silently swallows the event (no exception, no console error). The event path is still recorded as "dispatched", so `is_controlled()` flips the input to **controlled**; from then on the attribute diff treats `value` as always-changed (`controlled || prev.value !== next.value`, `client.js`), so every render — including the 1s notifications poll — re-asserts `node.value` from the model via `SYNCED_ATTRIBUTES.value.added`. Since the model never received the keystroke, the OLD value is restored — with zero DOM mutations (MutationObserver sees nothing). The Gleam wiring (view → `UserEditedRefcheckTrio` → `refcheck_edit` dict) is correct at every level and matches the compiled bundle; the failure is in the runtime event path/cache layer for these specific inputs (they live in a conditionally-rendered, list-mapped row — unlike the login page inputs, which work: control-verified).

**Worst part:** Save still works — with the ORIGINAL details. A landlord "correcting" a wrong referee email believes it saved (success toast + row leaves awaiting_correction) but the old contact persists and the single correction cycle is burned. DB proof: `queued | brian.ref@righttenantry.test | correction_cycles=1` after saving with a typed new value.

## Screenshot

![panel-correct failure](https://github.com/solarity-services/RightTenantry/releases/download/bug-hunt-screenshots/bug-hunt-758f1d8-panel-correct-1786706388.png)

(Edit form open; Email field showing the ORIGINAL `brian.ref@righttenantry.test` after a fill attempt.)

## Repro (local sandbox; same code as develop @ 758f1d8)

1. Login (bug-hunt test landlord) → open any application whose reference call is in `awaiting_correction` (amber "We couldn't reach … at these details. Check with … , update them here…" row).
2. Click **Correct details** → the inline edit form opens with Name/Email/Phone prefilled.
3. Click into the Email field and type (or append a character). The keystroke lands for a blink, then the field **snaps back to the prefilled value** within ~150ms. Same on Name/Phone.
4. Click **Save & resend** anyway → success UI, but the saved row keeps the ORIGINAL contact (`correction_cycles` increments).

The **substitute** form (overflow menu → Substitute on an objected/unreachable row) uses the same `view_edit_trio` component and exhibits the identical defect — no input technique (fill, trusted CDP typing, native setters) lands text, so substitute can never submit a new referee.

## Context

- Environment: local sandbox (:4100, local dev DB; bundle = `make build-client` output, md5-verified current)
- Branch: `rt-refcheck-local-test` @ `758f1d8` (develop HEAD — the #607 follow-up merge)
- Run at: 2026-08-14
- Client: `client/src/components/reference_panel.gleam` (`text_input` helper, `view_edit_trio`) — served bundle confirmed to contain the same code

## Evidence

- Repro'd 3×: correct-minion (3 sessions incl. pristine), substitute-minion, and a controlled direct session (native setter + synthetic event AND agent-browser trusted typing).
- Control: login inputs accept the exact same input techniques in the same build (submit button enables, values persist) — defect is specific to the panel inputs.
- DB after Save-with-typed-value: `status=queued`, `corrected_email=brian.ref@righttenantry.test` (old), `correction_cycles=1`.
- Screenshots (local): `.bug-hunt-results/reference_checks/panel-correct/failure.png`, `.bug-hunt-results/reference_checks/panel-substitute/failure.png`
- Console logs: `.bug-hunt-results/reference_checks/panel-correct/console.log` (no page errors — silent swallow)

## Notes

- Copy check: the amber awaiting-correction line interpolates the applicant's first name ("Check with {first_name}"). The fixture applicant is literally named "Refcheck", so it rendered "Check with Refcheck" — a fixture artifact, not a bug. With real applicant names it reads correctly. No action needed beyond a visual sanity check with real data.
- Root-cause hypothesis for the silent `decode2` failure: the edit-trio inputs render inside a conditionally-expanded row within a `list.map` (reference_calls) — position-based event-path registration in the runtime's events cache is the prime suspect. A Lustre version bump or a different input pattern (e.g. uncontrolled + `virtual:defaultValue`, or keyed inputs) are candidate fixes; the app-team decides.

## Constraints

- Fix application code, not the scenario (testids/selectors verified correct).
- Re-run with `/bug-hunt reference_checks panel-correct` (and `panel-substitute`) — expected PASS.
- No regressions in sibling scenarios.

## Acceptance

- [ ] Root cause identified (runtime event-path/decode layer or app-side input pattern)
- [ ] Fix landed — typing in the correct-details and substitute forms updates the model; Save persists the NEW contact
- [ ] `/bug-hunt reference_checks panel-correct` and `panel-substitute` pass



--- ROUND-2 LENS GUARDS (from the Perkins briefing — framing, not findings) ---
- LOAD-BEARING — the keying is STABLE + no stale save survives. The edit-trio state (typed values + dirty flags) must be keyed by `reference_call_id` (stable across list reorders/refetches), NOT by slot index — a residual slot-keyed path (or a key that changes identity across a refetch) = a blocker (it IS the bug class). The stale-save reproduction from the issue must be pinned by a test that bites (typed value survives a reorder/refetch -> save persists the NEW value, not the stale one).
- Per-row isolation: two rows' edit state never cross-contaminates (typing in row A cannot bleed into row B — the previous slot-keying collision).
- Scope guard: #611's fix ONLY — no unrelated changes. Sibling #612 merged (em-dash) — carry-forward; its copy is settled.
- BASE = `develop` (RC4.1-4.4 + #607 + #610 + #612 merged — carry-forward only; do NOT re-open settled findings).
- RT em-dash ban + AR-RC13 guards stay intact (verify nothing in this diff weakens them).
- a11y/testids on the edit-trio inputs unchanged (verify no regression).
- This is ROUND 2 (fix-audit of a prior review round at an earlier sha). The cumulative PR diff below contains both the original keying fix and the round-1 rework test additions. Review what is present NOW.

--- ORIGINAL JOB BRIEFING (full text) ---
# Briefing — righttenantry-refcheck-611-panel-persist (issue #611 — edit-trio inputs swallow keystrokes)

- **Job id:** `righttenantry-refcheck-611-panel-persist`
- **Repo:** RightTenantry · **Base:** `develop` · **Slug:** `refcheck-611-panel-persist`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow); your own adversarial pass
  uses `bmad-review-adversarial-general` + `bmad-review-edge-case-hunter`.
- **Perkins:** `pr_review: 1` (persistence-correctness — this bug silently saved STALE
  data with a success toast).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `develop` @ 758f1d8. A sibling job (`refcheck-612-emdash-prose`) may merge
  while you work — disjoint areas; rebase onto origin/develop if it lands first.
- **CI NOTE:** GitHub Actions billing is blocked at the account level — your PR's CI will
  be red/not-started until the user fixes it. NOT a code failure. Run the FULL local
  suite green (`make test-all`) before opening the PR; Perkins verifies locally.

## Mission — fix issue #611 (the issue IS the spec — read it in full first)

**The bug (user-confirmed live, repro'd by two bug-hunt agents):** in the refcheck
panel-correct AND panel-substitute forms, the edit-trio inputs (Name/Email/Phone)
swallow keystrokes: typed text snaps back to the prefilled value ~150ms after every
input event, and **Save persists the ORIGINAL contact with a success toast** — the
landlord believes the correction saved, but the old contact survives and the single
correction cycle is burned (DB proof: `correction_cycles=1` with the old value).

**Root cause (from the issue):** the input event reaches the Lustre runtime but the
message never dispatches — `decode2` returns `DispatchedEvent` (handler-path lookup /
decode failure) and silently swallows the event. The event path is recorded as
"dispatched", so `is_controlled()` flips the input to **controlled**; the attribute
diff then treats `value` as always-changed (`controlled || prev.value !== next.value`
in `client.js`), and every render (including the 1s notifications poll) re-asserts
`node.value` from the model. Since the model never got the keystroke, the OLD value
comes back — with zero DOM mutations. The Gleam wiring (view →
`UserEditedRefcheckTrio` → `refcheck_edit` dict) is CORRECT at every level and matches
the compiled bundle; the failure is in the runtime event path/cache layer for these
specific inputs — they live in a **conditionally-rendered, list-mapped row**, unlike
the login-page inputs (which work, control-verified).

**The fix:** the runtime event-path/cache layer must dispatch (or fail LOUDLY) for
these inputs — never silently swallow. Whatever the precise repair (handler-path
lookup for conditionally-rendered list-mapped inputs, decode/cache invalidation, or a
controlled-input diff fix), it must:
1. Land text in the fields (Name/Email/Phone) on both panel-correct and
   panel-substitute forms — user-confirmed repro from the issue.
2. Save the TYPED value — DB shows the new contact and the correction cycle consumed
   only then.
3. Not regress the login-page inputs (control-verified working) or the other
   controlled inputs.
4. Fail loud, not silent: if an event path can't dispatch, it must surface an error —
   no `DispatchedEvent` swallow without a log/exception (the silent class is what made
   this bug invisible for days).

**Acceptance:**

1. Repro from the issue passes: type into all three fields — text stays; Save →
   success toast AND the row's contact updates in the DB (verify `correction_cycles`
   + the new value).
2. Same for the substitute form (new referee actually submitted).
3. Regression suite green: full `make test-all`; a pin test reproducing the
   keystroke-swallow (the issue's controlled repro) so this class cannot silently
   return.
4. PR body: root-cause writeup (why the swallow happened), the fix, and the loud-
   failure guarantee; PR closes issue #611 (`Fixes #611`).
5. Local suite green; Perkins verifies locally (CI billing blocked).

**Scope guard:** the input event-path fix only. No copy changes (that's #612's job),
no feature work, no other UI movement.

## Dispatch parameters

```
repo: RightTenantry
repo_root: /Users/moses/code/RightTenantry
slug: refcheck-611-panel-persist
base: develop
model: deepseek/deepseek-v4-flash
github_issue: 611
pr_review: 1
```


--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "edge",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
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
--- FILE-OUTPUT CONTRACT (headless mode — this overrides everything else about how you respond) ---
Write your JSON array — and NOTHING else — to the file:
/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-611-panel-persist/r2/edge.json
Use the absolute path exactly as written above; do not derive or change it. Use your file-writing tool to write the file content, then STOP — no summary message, no prose, no follow-up questions. Your only deliverable is that file. If you have zero findings, write the two characters `[]` to the file.