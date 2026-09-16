# Briefing: righttenantry-agents-tf-in-ci

Read the standing orders first: `/Users/moses/code/docs/orchestration-playbook.md`
section 'Minion standing orders'. This briefing is your task spec.

## Task

**Port RT's terraform-in-CI pattern to RTA** (user ruling, 2026-09-05:
"lets do it") — WIF keyless auth + **plan-in-PR** + **apply-on-deploy** — so
RTA stops needing manual `make tf-apply-*` entirely. The reference
implementation is RT's, verbatim-read it first:
`/Users/moses/code/RightTenantry/.github/workflows/deploy-production.yml`
and `deploy-staging.yml` (WIF provider string, setup-terraform,
init-from-secret bucket, `apply -auto-approve`).

## What RTA already has (verify, don't assume)

- **WIF plumbing likely EXISTS**: RTA's own terraform provisions the WIF
  pool/provider conditioned on `github_repo = "solarity-services/
  RightTenantryAgents"` (`deployment/terraform/wif.tf` + `iam.tf` cicd SA).
  Verify pool/provider names, project numbers, and the cicd SA's roles
  cover Cloud Run service management (add via terraform if not — that's a
  terraform change riding this same PR).
- Secrets: RT uses `TF_STATE_BUCKET`; RTA has TWO buckets
  (`righttenantry-tf-state`, `righttenantry-staging-tf-state` — see the
  Makefile). Check `gh secret list` for what exists; name per-env secrets
  consistently and document any the user must add (gh secret set — user
  action if a secret is missing; flag it loudly in the PR).

## Implementation

1. **Plan-in-PR**: a terraform plan job on PRs touching `deployment/**`
   (pr-checks.yml or a new `tf-plan.yml`): WIF auth → init (state bucket,
   read scope is fine) → `plan -var-file=vars/<env>.tfvars` for both envs —
   the infra diff shows up as a PR check. (The single-source job's path
   filter fix makes the unit tests fire on terraform PRs too — this adds
   the plan surface on top.)
2. **Apply-on-deploy**: add the terraform job to `deploy-to-prod.yml` and
   `staging.yml` (RT's shape): WIF auth → setup-terraform → init (secret
   bucket) → `apply -auto-approve -var-file=vars/<env>.tfvars`. Runs on
   every deploy push (idempotent; matches RT). REMOVE the now-obsolete
   `deployment/terraform/**` path EXCLUSION from deploy-to-prod.yml (the
   reason it existed — "terraform never runs in CI" — dies with this PR).
3. Keep `gcloud run deploy` steps as-is (app deploys unchanged) — terraform
   job runs alongside/before; order: terraform first (infra), then app
   deploy.
4. README runbook: the manual Makefile targets become the fallback; CI is
   the primary path.
5. **FOLD (Gru, 2026-09-05 — Perkins W-headline on #181): README runbook
   must state that an ACTIVE emergency-pin (a set model var in tfvars)
   intentionally shows as TRIPWIRE-RED in CI/plan output until removed —
   override-by-design, not drift.** One paragraph while the runbook section
   is already in scope; pairs with the single-source PR's W1 (the escape
   hatch: re-baseline via a why-PR, or pin uncommitted + manual apply).

## Acceptance

1. Workflows syntactically valid (actionlint if available; else careful
   YAML + `gh workflow view` post-merge sanity).
2. Local `terraform fmt`/`validate` clean; `make tf-plan-prod` +
   `make tf-plan-staging` still work (Makefile untouched in behavior).
3. WIF/SA/roles verified as present (or added via this PR's terraform) —
   the E2E proof **rides the next staging promote** (staging.yml green with
   the new terraform job); state that expectation in the PR body.
4. PR Decisions: the pattern's RT lineage, what changed vs RT (two envs,
   two buckets), any secrets the user owes.

## Sequencing (load-bearing)

**Held behind the model-single-source merge** (same workflow files — its
path-filter fold lands first). Do not start before that merges; HALT and
report if the base moves under you.

## Model policy

Minion: **`zai-coding-cn/glm-5.3-flash`**.

## Skills policy

Workflow: **`bmad-quick-dev`**. No lavish.

## Perkins

`pr_review=1` — prod CI restructure on the revenue engine.

## Dispatch parameters

```
job_id:    righttenantry-agents-tf-in-ci
repo:      RightTenantryAgents
repo_root: /Users/moses/code/RightTenantryAgents
slug:      tf-in-ci
base:      develop
model:     zai-coding-cn/glm-5.3-flash
pr_review: 1
notes:     HELD ROW — release at model-single-source merge. Worktree from
           origin/develop at release. tf-plan-* READ-ONLY locally.
```
