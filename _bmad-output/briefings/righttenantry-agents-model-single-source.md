# Briefing: righttenantry-agents-model-single-source

Read the standing orders first: `/Users/moses/code/docs/orchestration-playbook.md`
section 'Minion standing orders'. This briefing is your task spec.

## Task

**Kill the two-places model config** (user ruling, 2026-09-05: "we need
this now"). Single source of truth for agent models = **code defaults**
(`tenant_scorer/config.py`) — versioned with the agents they configure,
guarded by canary tests, riding the normal PR+CI flow. Terraform becomes an
**optional, explicit, per-env override channel only** — by default it emits
NO model env vars at all.

## Why this shape (context, the incident)

Live prod ran ancient model env values while both code places said newer
ones — because terraform changes need a manual apply the team forgets, and
env overrides are invisible to the test suite. Code defaults fail loudly in
CI; env overrides fail silently in prod. Defaults belong where the tests
live.

## Implementation

1. **Terraform** (`deployment/terraform/variables.tf` + `service.tf`):
   the 7 model variables (DEFAULT_MODEL, CONSISTENCY_CHECKER,
   FINAL_COMPLIANCE_REVIEWER, PERSONAL_STATEMENT_ANALYZER, RISK_SCORER,
   VERIFICATION_COMPLIANCE_JUDGE, COMPLIANCE_REPAIR) → `default = null`;
   the service's `env` blocks for these become a **dynamic block** that
   emits an env var ONLY when the variable is set (per-env tfvars = the
   override lever; unset = absent = code defaults rule).
2. **tfvars**: neither `production.tfvars` nor `staging.tfvars` sets any
   model var (verify + keep it that way).
3. **Code**: `tenant_scorer/config.py` defaults remain the single source
   (post-38-sweep: `gemini-3.8-flash` everywhere); no code changes beyond
   what tests/docs need.
4. **Docs**: README runbook section — "changing an agent model = a code PR
   (defaults, tested); emergency pin = set the tfvars override + manual
   apply; remove the override when the code catches up."
5. **Tests**: grep for tests pinning the terraform env structure
   (the `test_concurrency` style literal extractors) — update to pin the
   NEW invariant: unset by default (null), dynamic emission present.
6. **FOLD (user ruling 2026-09-05, via Gru — CI path fix): add
   `deployment/**` to the `paths:` filters of ALL THREE workflows**
   (`.github/workflows/pr-checks.yml`, `staging.yml`, `deploy-to-prod.yml` —
   currently terraform-only PRs run NO checks; the exact gap that let prod
   drift to 3.5/3.1-pro unnoticed, Perkins W1 on #180, 7/7 lenses). Keep the
   existing tenant_scorer/tests paths; this ADDS the deployment path so the
   model tripwire + terraform pins fire on terraform-only PRs.

## Acceptance

1. Suite green; canary tests still pin the code defaults.
2. `terraform fmt`/`validate` clean.
3. **Read-only proof**: `make tf-plan-prod` (SAFE — plan only, NEVER apply)
   pasted in the PR body: the 7 model env vars show as REMOVED from the
   service template; the pending scaling changes (min 1→0, cpu_idle)
   unchanged; nothing else moves.
4. `make tf-plan-staging` also clean (same env removal expected there).
5. PR Decisions section: the design rationale (this briefing's "why") +
   the override runbook.
6. All three workflows' path filters include `deployment/**` (show the
   three diff hunks in the PR body; a terraform-only PR then triggers
   pr-checks — verify by the plan/logic, don't push a test PR).

## Sequencing (load-bearing)

**This job builds on the model-38-sweep merge** (in flight as
`righttenantry-agents-model-38-sweep`). Its base is post-sweep develop;
if the sweep has not merged when you start, HALT and report — do not
rebase around it (same files).

## Model policy

Minion: **`zai-coding-cn/glm-5.3-flash`**.

## Skills policy

Workflow: **`bmad-quick-dev`**. No lavish.

## Perkins

`pr_review=1` — terraform restructure on the revenue engine's service
template.

## Dispatch parameters

```
job_id:    righttenantry-agents-model-single-source
repo:      RightTenantryAgents
repo_root: /Users/moses/code/RightTenantryAgents
slug:      model-single-source
base:      develop
model:     zai-coding-cn/glm-5.3-flash
pr_review: 1
notes:     RELEASE GATE: dispatch only after model-38-sweep merges (same
           files — held row if needed). Worktree from origin/develop.
           tf-plan-* READ-ONLY, never apply.
```
