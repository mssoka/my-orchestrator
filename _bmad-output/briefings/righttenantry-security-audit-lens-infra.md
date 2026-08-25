# Lens briefing — security-audit / INFRA + DEPS (CI/CD, Docker, Terraform, Worker, secrets, dependency audit)

- **Job:** righttenantry-security-audit (mega-minion lens; parent minion audits the repo)
- **Model policy:** `deepseek/deepseek-v4-pro` (glm-5.3 provider-capped 429 code 1308 until 17:54:28Z — sanctioned fallback per the playbook's fallback chain; briefing override).
- **Repo/worktree (READ-ONLY):** `/Users/moses/.herdr/worktrees/RightTenantry/security-audit` @ develop (17d5f32)
- **Skill:** `bmad-review-edge-case-hunter` — exhaustive boundary enumeration, mechanism-only, every claim verified against disk.
- **Output:** write findings to `/Users/moses/code/_bmad-output/implementation-artifacts/righttenantry-security-audit/lens-infra.md`, then end with a one-paragraph summary in your pane.

## Ground rules

- READ-ONLY: no edits, no commits, no installs, no pushes. **Do not modify anything. Do not run `npm audit fix` or any upgrade.** Report-only audit. Do not spawn sub-agents.
- Evidence discipline: every finding = severity + `file:line` + trigger + consequence + remediation + confidence. Verified only.

## Scope

1. **Committed secrets scan** (report-only): grep the worktree for secret patterns — `sk_live_`, `sk_test_`, `whsec_`, `AKIA`, `AIza`, `ghp_`, `gho_`, `xox`, `SG.`, `re_` (Resend keys), `eyJ` (JWTs), `supabase service_role`, high-entropy base64 blobs in non-binary files; check `.env*` files that ARE tracked (`git ls-files | grep -i env` — `.env.example`/`.env.test` should hold no real values), `deployment/terraform/vars/*.tfvars` (must be var REFERENCES not values), `*.tfstate` committed? `git log --all --oneline -- '*.env' '*.tfstate*'` for accidental past commits (report path only, do not dig contents beyond confirming secret-ness).
2. **CI/CD** (`.github/workflows/*`): `permissions:` blocks (least privilege?), `pull_request_target` usage (fork code execution with secrets?), secret exposure to PRs from forks, artifact upload contents, pinned action SHAs vs floating tags, OIDC to GCP (Workload Identity) vs long-lived keys, `test-db` service credentials, what env secrets CI receives.
3. **Docker** (`Dockerfile`, `docker-entrypoint.sh`, `.dockerignore`): image base pins, running as root?, secrets baked into layers (ENV with keys in Dockerfile?), entrypoint secret validation logic (fail-closed on missing prod secrets?), the perl index.html passes (what gets injected — POSTHOG key only?), health-check exposure, anything listening beyond the app.
4. **Terraform** (`deployment/terraform/**`): secrets defined as Secret Manager references (not inline values), state backend, overly-broad IAM (allUsers on services? service account roles), WIF config (attribute condition locking repo/branch?), public exposure of Cloud Run services (ingress settings), Supabase/DB network posture (public pooler with password auth — what the repo controls), logging of secrets in provider config.
5. **Cloudflare Worker** (`deployment/cloudflare-worker/**`): the X-RT-Secret injection — secret comparison method, which routes get rate-limited (login 10/min, signup 5/h, apply submit 5/h — verify present + keyed how), legacy-domain 301 redirect logic (open redirect via crafted Host?), any worker-side fetch/URL handling.
6. **Dependencies** (report-only): `package.json` + `package-lock.json` — run `npm audit --omit=dev --json` (and full `npm audit --json`) in the worktree if node_modules symlink works, else read lockfile versions of runtime deps (`marked`, `tailwindcss`, anything in dependencies — note dev-tool vs shipped-code: nothing from package.json ships to browsers except build output, verify that claim from the Makefile/Dockerfile); ALSO the Gleam deps (`manifest.toml` files in shared/client/server — list versions of security-relevant deps: wisp, mist, pog, rsvp, plinth; note any pinned-to-git-main or stale majors). Report-only — NO upgrades.
7. **Scripts + Makefile**: `scripts/*`, `run_squirrel.sh`, `Makefile` — command injection via env vars into shell/perl, the sync-secrets script (`deployment/sync-secrets.sh` — reads .env, writes Secret Manager; check it can't leak into logs), test-db compose credentials (test/test acceptable for local).
8. **Admin/debug endpoints**: grep the server tree for debug/admin/status routes beyond `/health` (e.g. anything echoing config/env); `/health` DB probe exposure (public path — acceptable? info finding either way).
9. **`.github` branch protections/pipelines that deploy**: what can trigger a production deploy (which branches, who), migrations run automatically before deploy (`supabase db push` — destructive guard).

## Deliverable format

Markdown: summary, findings table (id, severity, title, file:line, confidence), one section per finding with trigger + evidence + remediation. Include the dependency-audit output summary (counts by severity, notable advisories) and verified-clean list.
