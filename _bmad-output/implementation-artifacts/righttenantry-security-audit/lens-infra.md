# Lens: INFRA + DEPS — RightTenantry security audit

- **Scope:** CI/CD, Docker, Terraform, Cloudflare Worker, committed secrets, dependency audit, scripts/Makefile, admin/debug endpoints, deploy triggers
- **Worktree:** `/Users/moses/.herdr/worktrees/RightTenantry/security-audit` @ `develop` (17d5f32) — READ-ONLY
- **Method:** exhaustive path enumeration; every claim verified against disk. Severity calibrated to "does it hit a real landlord today, or break a contract a future deploy depends on?"

## Summary

The infra posture is strong. Secrets are out of the repo (Secret Manager + Worker binding), GCP auth is OIDC/WIF with repo+branch lock, the X-RT-Secret origin lock closes the `.run.app` bypass, and the Docker/entrypoint path is the *good* kind of paranoid — runtime-validated placeholder substitution rather than baked secrets. Two MEDIUM findings stand out: (1) the rate limits AGENTS.md claims for login/signup/application-submit are **not implemented anywhere at the edge** (the Worker explicitly omits them), and (2) the CI deploy service account holds `projectIamAdmin`, making the deploy path a full-project-takeover primitive. The rest are hardening gaps (SHA pinning, non-root, constant-time compare on the origin gate, digest pinning) plus a warn-only destructive-migration guard.

## Findings table

| ID | Severity | Title | Location | Confidence |
|----|----------|-------|----------|------------|
| INFRA-01 | **Medium** | Documented edge rate limits (login 10/min, signup 5/h, apply submit 5/h) do not exist | `deployment/cloudflare-worker/worker.js` (AUTH_WRITE_PATTERN + "Deliberately omitted" comment); `deployment/terraform/cloudflare-rate-limits.tf` | High |
| INFRA-02 | **Medium** | Deploy SA holds `projectIamAdmin` → CI compromise = full GCP project takeover | `deployment/terraform/iam.tf:120-130` (`deploy_project_iam_admin`, `deploy_iam_admin`) | High |
| INFRA-03 | Low | X-RT-Secret origin lock uses plain `==`, not `crypto.secure_compare` | `server/src/middleware.gleam:427` | High |
| INFRA-04 | Low | GitHub Actions pinned to floating major tags, not commit SHAs | `.github/workflows/deploy-production.yml`, `deploy-staging.yml`, `test.yml`, `pr-checks.yml` | High |
| INFRA-05 | Low | Destructive-migration guard is warn-only; deploy runs `db push --include-all` with no blocking gate | `.github/workflows/pr-checks.yml:41-50`; `deploy-*.yml` "Apply Supabase migrations" step | High |
| INFRA-06 | Low | Runtime image runs as root (no `USER`; no Cloud Run runAsUser) | `Dockerfile` (Stage 2); `deployment/terraform/cloud-run.tf` | High |
| INFRA-07 | Low | Base images pinned by version tag, not digest | `Dockerfile:6,142`; `docker-compose.test.yml`; `test.yml` postgres service | High |
| INFRA-08 | Low | X-RT-Secret (Worker secret) lives in Terraform state; state-bucket IAM not verifiable from repo | `deployment/terraform/cloudflare-worker.tf:30-33`; `main.tf:15-18` | Medium |
| INFRA-09 | Info | Runtime SA has project-wide `secretmanager.secretAccessor`, not per-secret | `deployment/terraform/iam.tf:78-83` | High |
| INFRA-10 | Info | `test.yml`/`pr-checks.yml` declare no explicit `permissions:` block | `.github/workflows/test.yml`, `pr-checks.yml` | Medium |

---

## INFRA-01 — Documented edge rate limits do not exist (Medium)

**Trigger:** AGENTS.md §Deployment & Infrastructure states: "Rate limiting at Cloudflare edge: login 10/min, signup 5/hour, application submit 5/hour per IP." An operator relying on that statement believes credential-stuffing, signup-spam, and apply-form flooding are capped at the edge. They are not.

**Evidence (verified):**
- `deployment/cloudflare-worker/worker.js` — `AUTH_WRITE_PATTERN` matches only `/api/v1/(vacancies|account|settings|notifications|payment)` + `/api/v1/auth/resend-confirmation` (60/min). The tail comment states explicitly: *"Deliberately omitted: the rest of /api/v1/auth/\* (login, signup, recover, reset-password, accept-policy, logout). These are pre-session routes … They will get their own rule when a paid plan frees the http_ratelimit slot."*
- `deployment/terraform/cloudflare-rate-limits.tf` — the single Free-tier `http_ratelimit` rule covers only `/erase/:token` + `/dsar/:token` (5 req/10s).
- The public application form (`/apply/:code`) is in `is_public_path` (`middleware.gleam:282`) and is **not** under `AUTH_WRITE_PATTERN`; submission has no edge rate limit. App-layer anti-fraud is honeypot + timing only (`application_handler.gleam`, `form_view.gleam`), not a rate limit.
- Partial mitigation: login *is* throttled by Supabase GoTrue (`auth_handler.gleam:582` maps GoTrue `over_request_rate_limit` → `LoginRateLimited` → 429). Signup and application submit have no equivalent.

**Consequence:** Login credential-stuffing (mitigated only by GoTrue's own throttle, not the claimed edge rule), signup spam (5/h claim unmet), and unauthenticated application-form flooding (drives AI-analysis cost + DB load) are not capped where the docs say they are. This is a documented-control-vs-actual gap, not just a missing hardening.

**Remediation:** Either implement the limits in the Worker (`caches.default` buckets already provide the mechanism — add `login`, `signup`, `apply-submit` buckets with the documented 10/min, 5/h, 5/h budgets) or correct AGENTS.md to reflect reality. Signup and apply-submit are the priority: they are unauthenticated and currently uncapped.

---

## INFRA-02 — Deploy SA holds projectIamAdmin (Medium)

**Trigger:** Any actor who can trigger the production/staging deploy workflow (push to `main`/`staging`, or staging `workflow_dispatch`) runs Terraform as the deploy SA. That SA can grant itself arbitrary project roles, so a single compromised merge = full GCP project control.

**Evidence (verified):** `deployment/terraform/iam.tf` grants the deploy SA (`rt-gleam-deploy-prod`/`-staging`):
- `roles/resourcemanager.projectIamAdmin` (`deploy_project_iam_admin`, ~line 120)
- `roles/iam.serviceAccountAdmin` (`deploy_iam_admin`)
- `roles/run.admin`, `roles/secretmanager.admin`, `roles/iam.workloadIdentityPoolAdmin`, `roles/cloudscheduler.admin`, `roles/artifactregistry.admin`

`projectIamAdmin` alone is the escalation primitive: it permits binding any role to any principal in the project, including `owner`/`editor` and `secretmanager.secretAccessor` on the runtime SA. Combined with `secretmanager.admin`, a compromised deploy path can exfiltrate every app secret (Stripe, Resend, Supabase service-role, session keys, X-RT-Secret).

**Consequence:** Blast radius is the entire GCP project (app + secrets + IAM + AI service invocation), not just the application. The mitigations (WIF repo+branch lock, `environment:` gate) shrink *who* can trigger, but do not shrink *what* the trigger grants.

**Remediation:** Split the Terraform-applying identity from the IAM-managing identity. E.g., keep the CI SA narrow (Artifact Registry writer, `run.developer`, secret *version* adder for the specific secrets) and move IAM/SA/WIF management to a separate, rarely-triggered workflow or a human-run `terraform apply` under a distinct, more-guarded principal. At minimum, document that the deploy SA is effectively project-owner and review `environment` protection rules (required reviewers on `production`).

---

## INFRA-03 — X-RT-Secret compared with `==` (Low)

**Trigger:** `require_cloudflare_secret` compares the injected header to the secret with plain string equality, while every other secret/signature comparison in the codebase uses constant-time comparison.

**Evidence (verified):** `server/src/middleware.gleam:427` — `Ok(value) if value == secret -> handler()`. Compare `response_helpers.gleam:138` (`require_internal_secret` → `crypto.secure_compare`), `auth/csrf.gleam:134`, `payment/stripe_webhook.gleam:38`, `inbound_email/svix.gleam:75`, `notification/twilio_webhook.gleam:40` — all `crypto.secure_compare`.

**Consequence:** Erlang binary `==` short-circuits on first differing byte, so a remote attacker could in principle leak the secret prefix byte-by-byte via response timing. Practical exploitability is very low (high-entropy secret, single comparison per request, network jitter), but it is a real inconsistency with the codebase's own constant-time standard for the *origin gate* specifically.

**Remediation:** Replace `value == secret` with `crypto.secure_compare(bit_array.from_string(value), bit_array.from_string(secret))`, mirroring `require_internal_secret`.

---

## INFRA-04 — Actions pinned to floating tags (Low)

**Trigger:** Supply-chain compromise or force-push of a popular action tag propagates silently into CI and deploys.

**Evidence (verified):** All third-party actions use major/minor tags, not commit SHAs: `actions/checkout@v6`, `google-github-actions/auth@v3`, `google-github-actions/setup-gcloud@v3`, `docker/setup-buildx-action@v3`, `supabase/setup-cli@v2`, `hashicorp/setup-terraform@v4`, `erlef/setup-beam@v1`, `actions/setup-node@v6`, `oven-sh/setup-bun@v2`, `actions/cache@v5`. (The hand-installed toolchains — Gleam, rebar3, Typst, Bun in the Dockerfile — *are* version+sha256 pinned; only the GitHub Actions themselves are floating.)

**Consequence:** A compromised action runs with the workflow's token (in deploy, OIDC `id-token: write`). Low likelihood, high consequence.

**Remediation:** Pin every action to a full-length commit SHA (e.g. `actions/checkout@<40-char sha>`), with a comment naming the tag it corresponds to.

---

## INFRA-05 — Destructive-migration guard is warn-only (Low)

**Trigger:** A migration containing `DROP`/`RENAME`/`ALTER TYPE` that slips human review executes against production at deploy time with no blocking gate.

**Evidence (verified):** `.github/workflows/pr-checks.yml:41-50` greps changed migrations and emits `::warning::` only (never `::error::`, never `exit 1`). Both deploy workflows then run `supabase --yes db push --include-all` against the live project before the Cloud Run flip. Migrations are forward-only with image-only rollback (documented in the rollback step), so a destructive migration is not undoable by rollback.

**Consequence:** Schema contract break (a load-bearing contract per AGENTS.md) with no automated last line of defense. Severity LOW because it matches the AGENTS.md design ("pr-checks.yml warns … as a reminder") and relies on review discipline.

**Remediation:** Promote destructive-op detection to a hard failure on `main`/`staging` targets (or require an explicit `# ALLOW-DESTRUCTIVE` marker that a human approves), keeping the warning for feature-branch PRs.

---

## INFRA-06 — Runtime image runs as root (Low)

**Trigger:** No `USER` directive in the runtime stage; Cloud Run `cloud-run.tf` sets no container security context (`runAsUser`/`runAsNonRoot`). The Erlang shipment runs as UID 0.

**Evidence (verified):** `Dockerfile` Stage 2 (lines ~142-end) has no `USER`; `google_cloud_run_v2_service.app` in `cloud-run.tf` has no `security_context`/`containers[].env` user override.

**Consequence:** A code-execution bug (e.g. a future file-write via Typst PDF render or a deserialization bug) would land as root. Cloud Run's gVisor sandbox limits host escape, so this is defense-in-depth, not a direct breach.

**Remediation:** Add a non-root `USER` (e.g. `useradd` a `righttenantry` user, `chown` `/app`, drop privileges) in Stage 2, and/or set `containers { startup_cpu_boost … }` with an explicit `run_as_non_root` security context.

---

## INFRA-07 — Base images pinned by tag, not digest (Low)

**Trigger:** A republished tag (e.g. `ghcr.io/gleam-lang/gleam:v1.15.1-erlang-alpine` or `postgres:16-alpine`) would be picked up silently on next build/CI run.

**Evidence (verified):** `Dockerfile:6` and `:142` (`ghcr.io/gleam-lang/gleam:v1.15.1-erlang-alpine`); `docker-compose.test.yml` and `test.yml` (`postgres:16-alpine`). Note the Gleam image tag does encode the exact OTP+Gleam version, reducing (not eliminating) the mutation risk.

**Consequence:** Supply-chain drift; low practical risk given the tags encode toolchain versions.

**Remediation:** Pin base images to `name@sha256:…` digests.

---

## INFRA-08 — X-RT-Secret in Terraform state (Low)

**Trigger:** The origin-lock shared secret is written into the GCS Terraform state via the Worker's `secret_text_binding.text`, so the state bucket becomes a second location that must never leak.

**Evidence (verified):** `deployment/terraform/cloudflare-worker.tf:30-33` sets `secret_text_binding { name = "RT_CLOUDFLARE_SECRET"; text = var.cloudflare_worker_secret }` — a resource attribute Terraform serializes into state. The variable is `sensitive = true` (so it won't render in plan output), but the value still lands in `terraform.tfstate` in the GCS bucket (`main.tf:15-18`, bucket name supplied via `TF_STATE_BUCKET` secret). The bucket's IAM/encryption are outside the repo and not verifiable here.

**Consequence:** Anyone/anything with read access to the state bucket learns the X-RT-Secret and can forge the origin-lock header, bypassing the direct-`.run.app` protection. Medium confidence because bucket access is not verifiable from the worktree; the exposure surface exists regardless.

**Remediation:** Confirm the state bucket is private (no public access, tight IAM, object versioning + retention), and treat it as secret-bearing. Optionally remove the Worker secret from Terraform entirely (manage it via `wrangler secret put` / Cloudflare API) so it never touches state.

---

## INFRA-09 — Project-wide secret accessor on runtime SA (Info)

**Trigger:** `roles/secretmanager.secretAccessor` is granted at project level, so the Cloud Run runtime SA can read *every* secret in the project, not only the ten `rt-*` secrets the app mounts.

**Evidence (verified):** `deployment/terraform/iam.tf:78-83` (`runtime_secret_accessor`, member = Cloud Run SA, no `condition` on resource). The container *mounts* only the narrowed per-service secret sets (`config.tf` `secret_env_vars` / `*_secret_env_vars`), so this is defense-in-depth scope creep, not an active leak.

**Remediation:** Scope with an IAM `condition` (`resource.name` on the `rt-*` secrets) or bind accessor on each secret resource individually.

---

## INFRA-10 — No explicit `permissions:` on test/pr-check workflows (Info)

**Trigger:** `test.yml` (reusable) and `pr-checks.yml` declare no top-level `permissions`, so their jobs inherit the repository default GITHUB_TOKEN scope.

**Evidence (verified):** `test.yml` and `pr-checks.yml` contain no `permissions:` key. The deploy jobs *do* declare `contents: read, id-token: write`. Fork-PR tokens are read-only regardless (GitHub enforces this), and no `pull_request_target` is used, so fork code execution with secrets is not possible.

**Consequence:** If the repo default is read/write (older orgs), same-repo PR CI runs hold a write-capable token unnecessarily. Hardening note only.

**Remediation:** Add `permissions: contents: read` to both workflows.

---

## Dependency audit

**npm** (`package.json` has **no `dependencies`** — only `devDependencies`: `tailwindcss ^3.4.0` → 3.4.19, `@tailwindcss/forms ^0.5.7`):
- `npm audit --omit=dev`: **0 vulnerabilities** across 75 resolved packages (nothing ships to the browser except the compiled `tailwind.css` output — claim verified via `npm run build:css` → static CSS, and the SPA is a Gleam/Lustre bundle).
- Full `npm audit`: **2 high, 0 critical** — `nanoid <=3.3.17` and `postcss <=8.5.22`, both **build-time only** (Tailwind CLI toolchain). Not exploitable at runtime; remediation would be a tailwindcss v4 major bump. Report-only per briefing — no upgrade performed.

**Gleam** (`shared/client/server/manifest.toml`) — all packages `source = "hex"` with `outer_checksum` present; **no `source = "git"` pins, no stale majors**:
- Server: `wisp 2.2.2`, `mist 6.0.2`, `pog 4.1.0`, `gleam_httpc 5.0.0`, `squirrel 4.6.0`, `gleam_crypto 1.5.1`.
- Client: `rsvp 1.2.0`, `plinth 0.10.2`, `lustre 5.6.0`, `modem 2.1.2`. (`mist 5.0.4` appears transitively via `lustre_dev_tools` — dev tooling, not shipped code.)
- Shared: `gleam_json 3.1.0`, `gleam_time 1.8.0`, `gleam_regexp 1.1.1`.
- No known-advisory Gleam packages identified.

## Verified-clean list

- **Committed secrets:** none. All pattern hits (`whsec_…`, `sk_test_…`, `phc_…`) are placeholder/test values (`*_test.gleam`, docs) or public-by-design identifiers. `.env` on disk is an **untracked symlink**; `.env.example` (all empty/placeholder) and `.env.test` (local `test/test`) are clean. No `.tfstate` or real `.env` in any commit (checked `git log --all`).
- **tfvars:** `supabase_anon_key` is the public anon JWT (`"role":"anon"`) — public by design. Stripe `price_*` IDs, Sentry DSNs, PostHog `phc_` keys, Meta Pixel / Google Ads IDs are all public-by-design. The secret halves (Stripe keys, Resend, Supabase **service-role**, X-RT-Secret, Meta CAPI token) are Secret-Manager-backed, set only via `sync-secrets.sh`.
- **`sync-secrets.sh`:** values piped via `--data-file=-` (stdin, not argv) → not visible in `ps`/logs; output is `tail -1` of gcloud (version line, not the value).
- **WIF:** `attribute_condition` locks `assertion.repository == solarity-services/RightTenantry` **and** `assertion.ref == refs/heads/{main|staging}`; fork PRs cannot obtain the OIDC token. No `pull_request_target` anywhere.
- **Docker build:** `.dockerignore` excludes `.env*` (re-includes `.env.example`); placeholders + **runtime format-validated** substitution (entrypoint validates `phc_[A-Za-z0-9_-]+`, `^[0-9]+$`, `^AW-[0-9]+$` before `sed`) — no secrets in layers, no config-driven XSS breakout.
- **Internal endpoints** (`/api/v1/internal/digest|lifecycle/verification-reminders|reference-checks`): gated by `INTERNAL_SECRET` via `crypto.secure_compare`; `INTERNAL_SECRET` fails closed in production (`server.gleam:250`).
- **`/health`:** public, returns only `{"status":"ok"}` / `{"status":"error","message":"Database unreachable"}` — no config/env/schema echo. No debug/admin/status routes echoing config found.
- **Redirects** (`cloudflare-redirects.tf`): fixed-scheme/host + `$1` path capture → no open redirect via crafted Host.
- **Worker proxy** (`worker.js`): fixed upstream hosts, path-traversal rejection (incl. `%2e`), header allowlist (Cookie/Authorization/X-RT-Secret never forwarded), body cap, timeout, per-IP caps.
- **test-db creds** (`test/test` in compose + CI service container): acceptable for local/ephemeral.
- **Deploy triggers:** prod = push `main`; staging = push `staging` + `workflow_dispatch`; migrations (`db push`) run before the Cloud Run flip. Branch-protection rules (required reviewers, etc.) are GitHub repo settings and **not verifiable from this worktree** — flag for the operator checklist.
