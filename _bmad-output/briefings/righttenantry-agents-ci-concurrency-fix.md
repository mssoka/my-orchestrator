# Briefing — righttenantry-agents-ci-concurrency-fix

## Task

Fix a CI concurrency-group collision in the RightTenantryAgents repo: the
`PR Checks` workflow (lint / unit / integration) is being CANCELLED on every
PR because it shares a workflow-level concurrency group with `Terraform Plan`.

## Diagnosis (pre-done — verify, do not re-derive)

Both workflows declare the SAME workflow-level concurrency group on
pull_request events:

- `.github/workflows/pr-checks.yml`:
  `group: pr-${{ github.event.pull_request.number }}` +
  `cancel-in-progress: true`
- `.github/workflows/tf-plan.yml`:
  `group: pr-${{ github.event.pull_request.number || github.run_id }}` +
  `cancel-in-progress: ${{ github.event_name == 'pull_request' }}`

When a PR event fires, both workflows enter the same group at the same
instant; GitHub allows one run per group and the newer cancels the older.
Observed three-for-three on 2026-09-06 (11:38Z, 14:37Z, 17:13Z — PR Checks
cancelled ~1s, Terraform Plan success each time). Net effect: lint/unit/
integration have produced NO CI signal on recent PRs; only the terraform
plans gate.

## The change

In `.github/workflows/pr-checks.yml` ONLY, make the group name distinct AND
dispatch-safe:

```yaml
concurrency:
  group: checks-pr-${{ github.event.pull_request.number || github.run_id }}
  cancel-in-progress: true
```

Notes:
- The `|| github.run_id` fallback fixes a SECOND latent bug in the same
  line: pr-checks also has a `workflow_dispatch` trigger, and with an empty
  `pull_request.number` on dispatch the current bare `pr-` group makes
  manual dispatches cancel each other (tf-plan.yml's comment documents this
  exact trap — copy its pattern).
- Do NOT touch tf-plan.yml, its job-level `tf-<env>` groups (plan-vs-apply
  serialization — load-bearing), or anything else. Expected diff: ONE line
  (the group name), maybe two with the comment.

## Acceptance

1. Diff is the one group-name line in pr-checks.yml (plus optional comment).
2. YAML parses clean (python yaml or actionlint if available).
3. The PR is its own live proof: tf-plan.yml runs on ALL pull_requests and
   pr-checks triggers on `.github/workflows/**` — so BOTH workflows fire on
   this PR. Acceptance = both workflows complete on the fix PR
   (PR Checks not cancelled). If PR Checks shows cancelled again despite the
   distinct group, STOP and report — that would mean a second collision
   surface exists.
4. PR to `develop`, small body carrying the diagnosis summary above.

## Skills policy

- Workflow skill: bmad-quick-dev (tiny CI/ops fix).

## Model policy

- Unset (Silas pins at dispatch; ops default).

## pr_review

- `pr_review=0` — CI/ops-tooling fix class (sanctioned), single config line,
  self-proving acceptance on the PR itself.

## Dispatch parameters

- repo: RightTenantryAgents
- repo_root: /Users/moses/code/RightTenantryAgents
- slug: righttenantry-agents-ci-concurrency-fix
- base: develop
- worktree: standard (Silas' usual mechanics)
