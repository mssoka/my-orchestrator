# Briefing: righttenantry-agents-tf-makefile

Read the standing orders first: `/Users/moses/code/docs/orchestration-playbook.md`
section 'Minion standing orders'. This briefing is your task spec.

## Task

**Add a `deployment/Makefile`** wrapping the terraform workflow (user
request, 2026-09-05: "i make makefile for that") so env operations are one
command instead of a documented incantation.

## Targets (per env: staging + production)

- `make tf-init ENV=staging|production` — `terraform init` with the correct
  per-env `-backend-config` (read `providers.tf` + the README setup section
  for how the GCS backend bucket is selected per env; encode it so the
  target is self-contained)
- `make tf-plan ENV=…` — plan with `vars/<env>.tfvars`
- `make tf-apply ENV=…` — apply with `vars/<env>.tfvars`
- Sensible `help` target (self-documenting, first in file). Keep it stdlib
  `make` (no bash-4 arrays — macOS bash 3.2 rule).

## Acceptance

1. **Verified, not claimed**: run `make tf-plan ENV=production` locally —
   it must produce a real plan. EXPECTED: the plan shows exactly the
   pending #176 change (revision min-instance 1→0, billing → request-based)
   and nothing else — paste the summary lines (Plan: … to change) into the
   PR body. **DO NOT APPLY.** Plan is read-only; apply stays a human/Silas
   action.
2. `make tf-plan ENV=staging` also runs clean (no unexpected diffs —
   staging already runs min=0; if drift appears, report it, don't fix).
3. README: replace/augment the manual init/plan/apply runbook section with
   the Makefile usage (keep the raw commands in a details/aside for
   onboarding).
4. No other files touched.

## Model policy

Minion: **`zai-coding-cn/glm-5.3-flash`**.

## Skills policy

Workflow: **`bmad-quick-dev`**. No lavish.

## Perkins

`pr_review=0` — CI/ops tooling (Makefile + docs), the scope-guard
exemption class.

## Dispatch parameters

```
job_id:    righttenantry-agents-tf-makefile
repo:      RightTenantryAgents
repo_root: /Users/moses/code/RightTenantryAgents
slug:      tf-makefile
base:      develop
model:     zai-coding-cn/glm-5.3-flash
pr_review: 0
notes:     Worktree from origin/develop. gcloud authed on this machine
           (mssokabi@gmail.com) — plan runs are safe/read-only. PLAN ONLY,
           never apply.
```
