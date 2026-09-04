# Briefing: righttenantry-agents-prod-scale-to-zero

Read the standing orders first: `/Users/moses/code/docs/orchestration-playbook.md`
section 'Minion standing orders'. This briefing is your task spec.

## Task

Cut RTA prod idle cost: **scale the prod agents Cloud Run service to zero**
(user ruling, 2026-09-04). Two-line change in
`deployment/terraform/vars/production.tfvars`:

- `min_instances = 1` → `0`
- `cpu_idle = false` → `true`

Update the sizing comment to mirror staging's rationale: pre-revenue cost
cut; Gleam retries (3 attempts, 2/8/32s backoff, ~42s runway) absorb the
documented cold-start blips (see `variables.tf` 2026-05-04 history and
staging's identical move); **tripwire: flip back to `min_instances = 1` /
`cpu_idle = false` at the first paying customer or sustained load testing.**

## Scope guard

- NOTHING else changes: `cpu = 2`, `memory = 4Gi`, `max_instances = 20`
  stay. `variables.tf` defaults stay (per-env override pattern is the
  design). No staging changes. No Gleam-side changes.
- Do NOT touch `gleam_backend_service_account` / `beacon_service_account`
  (empty by design, pre-launch).

## Acceptance

1. Diff = production.tfvars values + comment only.
2. `terraform -chdir=deployment/terraform fmt -check` clean and
   `terraform -chdir=deployment/terraform init -backend=false` +
   `validate` pass locally (terraform v1.5.7 is installed).
3. Read `.github/workflows/deploy-to-prod.yml` and state in the PR body
   whether merging triggers apply (plan output snippet if the workflow
   runs one) — the reviewer must know merge = prod change.
4. PR body "Decisions & rationale": the cost rationale, the 2026-05-04
   scar + why current retry budget absorbs it, the flip-back tripwire.

## Model policy

Minion: **`zai-coding-cn/glm-5.3-flash`**.

## Skills policy

Workflow: **`bmad-quick-dev`**. No lavish (infra code, regular PR pattern).

## Perkins

`pr_review=1` — prod terraform on the revenue engine. Loop-until-APPROVED.

## Dispatch parameters

```
job_id:    righttenantry-agents-prod-scale-to-zero
repo:      RightTenantryAgents
repo_root: /Users/moses/code/RightTenantryAgents
slug:      prod-scale-to-zero
base:      develop
model:     zai-coding-cn/glm-5.3-flash
pr_review: 1
notes:     Standard worktree from origin/develop. RT repo env bootstrap per
           playbook annex if the repo carries env symlinks.
```
