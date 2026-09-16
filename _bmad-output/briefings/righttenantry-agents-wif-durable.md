# Briefing: righttenantry-agents-wif-durable

Read the standing orders first: `/Users/moses/code/docs/orchestration-playbook.md`
section 'Minion standing orders'. This briefing is your task spec.

## Task

**Make the WIF impersonation grants durable in terraform** — tonight's
empirical findings, codified. CONTEXT (verified live, 2026-09-06): the prod
deploy's `Terraform Apply` job 403'd at token-mint for WEEKS of debugging;
hand-adding a WILDCARD TokenCreator grant
(`principalSet://.../right-tenantry-agents-pool/*`) made it pass INSTANTLY.
Root cause: GCP fails to match the COMPOUND
`attribute.repository/…/attribute.ref/refs/heads/main` principalSets on
this SA (the Policy Troubleshooter itself returns
MEMBERSHIP_UNKNOWN_UNSUPPORTED for them). Every working setup in the estate
(RT prod, RTA staging) uses SINGLE-attribute (repo-scoped) or no principal
matching.

## The changes (deployment/terraform)

1. **cb SA (iam.tf / wif.tf)**: replace the compound principalSet bindings
   with a **pool-scoped** TokenCreator + WorkloadIdentityUser pair
   (`principalSet://iam.googleapis.com/projects/${project_number}/locations/global/workloadIdentityPools/right-tenantry-agents-pool/*`)
   — matching the empirically-proven-working grant. SECURITY NOTE for the
   PR body: the effective filter is the pool PROVIDER's attribute condition
   (`repository == solarity-services/RightTenantryAgents && (ref ==
   refs/heads/main || ref.startsWith('refs/pull/'))`) — the front gate
   stays; only the (broken) redundant per-binding ref filter dies.
2. **Planner SA (planner.tf)**: same treatment if its WIF binding uses the
   compound form — pool-scoped or repo-scoped (single-attribute), whichever
   matches staging's proven shape; verify against staging's live planner.
3. **Staging symmetry**: read staging's live bindings first; if staging
   carries compound principalSets that merely HAVEN'T failed yet, migrate
   them to the same pool-scoped form in the same PR (one shape everywhere).
4. **Import/drift care**: tonight's hand-added grants (repo-scoped WIUser +
   wildcard TokenCreator on prod cb SA) are UNMANAGED — bring the terraform
   in line so `plan` converges to the durable state WITHOUT double-bindings
   (the plan output must show the hand-grants being adopted/replaced
   cleanly, not duplicated).

## Acceptance

1. `make tf-plan-prod` (READ-ONLY) pasted in the PR: the binding changes
   ONLY — the hand-grants converge, nothing else moves.
2. `make tf-plan-staging` same.
3. Apply is NOT run by you (user/Silas sequence post-merge: apply staging →
   apply prod → rerun a prod deploy to prove E2E).
4. PR Decisions: the debugging saga summarized (compound principalSet
   mismatch; troubleshooter UNSUPPORTED; wildcard proven), the security
   reasoning (provider condition = the guard), links to the failing run
   34000141634 for archaeology.

## Model policy / Skills / Perkins

Minion: `zai-coding-cn/glm-5.3-flash`. Workflow: `bmad-quick-dev`.
`pr_review=1` — prod IAM, the revenue engine's identity plumbing.

## Dispatch parameters

```
job_id:    righttenantry-agents-wif-durable
repo:      RightTenantryAgents
repo_root: /Users/moses/code/RightTenantryAgents
slug:      wif-durable
base:      develop
model:     zai-coding-cn/glm-5.3-flash
pr_review: 1
notes:     Worktree from origin/develop. tf-plan-* READ-ONLY, never apply.
```
