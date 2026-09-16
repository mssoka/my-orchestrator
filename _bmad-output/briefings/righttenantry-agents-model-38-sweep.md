# Briefing: righttenantry-agents-model-38-sweep

Read the standing orders first: `/Users/moses/code/docs/orchestration-playbook.md`
section 'Minion standing orders'. This briefing is your task spec.

## Task

**Sweep every RT agent model reference to `gemini-3.8-flash`** (user ruling,
2026-09-05: "we need 3.8 flash for all"). The fleet currently disagrees with
itself in TWO code places, and live prod runs a THIRD (older) set that was
never applied:

1. **Terraform** — `deployment/terraform/variables.tf`: 7 model-variable
   defaults on `gemini-3.6-flash` (DEFAULT_MODEL, CONSISTENCY_CHECKER,
   FINAL_COMPLIANCE_REVIEWER, PERSONAL_STATEMENT_ANALYZER, RISK_SCORER,
   VERIFICATION_COMPLIANCE_JUDGE, COMPLIANCE_REPAIR).
2. **Code defaults** — `tenant_scorer/config.py` (the `get_agent_model`
   default map) + test assertions pinning `gemini-3.6-flash`
   (test_agents_reference_validator, test_document_extractor,
   test_callbacks_state_init, test_config, test_schema_v4 — grep, don't
   trust this list).
3. Docs/README mentions of the model versions, if any.

All three → **`gemini-3.8-flash`**.

## Verification (load-bearing)

- **Model ID validity**: confirm `gemini-3.8-flash` is a valid model ID for
  this project's Vertex/Gemini integration before the sweep ships (docs,
  API listing, or a minimal probe the codebase already supports). A typo'd
  ID would brick every agent on deploy — this check is the job's spine.
- Full test suite green after the sweep (the pinning tests get updated to
  3.8, not deleted — they're the canaries).
- **Read-only proof of the end state**: run `make tf-plan-prod` (SAFE —
  plan only, NEVER apply) and paste the env-diff summary into the PR body:
  every model env → gemini-3.8-flash, plus the pending scaling changes
  (min 1→0, cpu_idle→true — already-merged #176, expected to ride).

## Scope guard

- Values + their pinning tests + docs ONLY. No logic changes, no terraform
  structure changes, no scaling changes (those are already merged).
- Note (do not implement) in the PR's Decisions section: the two-places
  split-brain (terraform env overrides vs code defaults) — recommend the
  single-source-of-truth follow-up (terraform sets env only for ops
  overrides; code defaults rule otherwise) as a future ruling.

## Model policy

Minion: **`zai-coding-cn/glm-5.3-flash`**.

## Skills policy

Workflow: **`bmad-quick-dev`**. No lavish.

## Perkins

`pr_review=1` — changes every agent's brain at deploy time; cheap insurance
on a high-blast-radius diff.

## Dispatch parameters

```
job_id:    righttenantry-agents-model-38-sweep
repo:      RightTenantryAgents
repo_root: /Users/moses/code/RightTenantryAgents
slug:      model-38-sweep
base:      develop
model:     zai-coding-cn/glm-5.3-flash
pr_review: 1
notes:     Worktree from origin/develop. tf-plan-prod is READ-ONLY (never
           apply). After merge, the user's tf-apply-prod lands 3.8 +
           scale-to-zero together.
```
