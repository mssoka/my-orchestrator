# Briefing: righttenantryagents-compliance-analytics-model-pin

- **Repo:** /Users/moses/code/RightTenantryAgents
- **Worktree (your cwd):** /Users/moses/.herdr/worktrees/RightTenantryAgents/compliance-analytics-model-pin
- **Branch:** `compliance-analytics-model-pin` → PR targets **`develop`**
- **Base:** `develop`

## Standing orders

Read `/Users/moses/code/docs/orchestration-playbook.md` section **"Minion standing orders"** and follow it exactly. Step-01 clarify = HALT and wait for relayed answers; internal approval checkpoints are pre-approved. Self-report every status transition: `/Users/moses/code/bin/ledger set righttenantryagents-compliance-analytics-model-pin <status> "<note>"`. When blocked or finished: `herdr notification show "righttenantryagents-compliance-analytics-model-pin" --body "<one-line status>"`. Never merge the PR.

## Skills policy

- **Your workflow:** `bmad-quick-dev`.
- **Mega-minions:** review swarm uses `bmad-review-adversarial-general` + `bmad-review-edge-case-hunter` (name it explicitly when you spawn them).

## Context

Two deferred items from the PR #161 review loops (details: `/Users/moses/code/RightTenantryAgents/_bmad-output/implementation-artifacts/deferred-work.md`, sections "`compliance.review_completed` telemetry double-counts" and "Terraform `COMPLIANCE_REPAIR_MODEL` pin", deferred 2026-07-19 — gitignored file, read it at that absolute main-checkout path). Sibling job `righttenantryagents-compliance-guard-hardening` owns items 7–9 — do not touch guard/scrub/repair-request logic.

**User decisions (2026-07-21):** the repair agent's model pin is `gemini-3.6-flash` (released today), and **all** flash references in the repo move from 3.5 → 3.6.

## Task

**A. Item 6 — Terraform `COMPLIANCE_REPAIR_MODEL` pin:**
- Add `variable "compliance_repair_model"` (default `"gemini-3.6-flash"`) to `deployment/terraform/variables.tf`, and the matching `env { name = "COMPLIANCE_REPAIR_MODEL" value = var.compliance_repair_model }` block in `deployment/terraform/service.tf` alongside the other pins (lines ~62–88).
- `config.py` already resolves `{AGENT_NAME}_MODEL` env vars — verify `compliance_repair` resolves with no code change; add a unit test if the naming needs one.
- **No `terraform apply`** — deploy stays with the human post-merge; say so in the PR.

**B. Flash sweep 3.5 → 3.6 (user decision):**
- `tenant_scorer/config.py`: `_DEFAULT_HARDCODED = "gemini-3.5-flash"` → `"gemini-3.6-flash"` (check the docstring/comment on line 3 too).
- `deployment/terraform/variables.tf`: `default_model` default → `"gemini-3.6-flash"`.
- Update every test expectation referencing `gemini-3.5-flash` (at least: `tests/unit/test_config.py`, `test_agents_reference_validator.py`, `test_agents_consistency_checker.py`, `test_document_extractor.py`, `test_schema_v4.py`, `test_callbacks_state_init.py`, `test_response_formatter_v4.py`) — sweep the whole repo for stragglers (docs, notebooks, scripts).
- **Do not touch** the `gemini-3.1-pro-preview` pins — flash only.

**C. Item 5 — `compliance.review_completed` double-counts:**
- Problem: the telemetry callback fires per judge run; a remediated gate runs the judge twice (dirty→fail, clean→pass), so BQ pass-rate denominators count attempts, not runs (100 runs + 20 remediations → 120 events → phantom 83% pass rate).
- Fix: add **run/attempt-scoped dimensions** to the telemetry event payload (e.g. `run_id` + `attempt` / `remediated` flag) at the emission site (anchor: `tenant_scorer/callbacks/compliance_enforcement.py`), then update the BQ analytics queries to aggregate per run.
- **If the BQ analytics queries live outside this repo** (or can't be found after a real search), implement the emission-side dimensions and HALT with a numbered clarify question about the queries' location — do not guess.
- Unit-test the new payload fields.

## Local step (main checkout, gitignored — no commit)

Update `/Users/moses/code/RightTenantryAgents/_bmad-output/implementation-artifacts/deferred-work.md`: mark items 5 and 6 **In progress — this job** (the guard-hardening sibling marked 3/4 dismissed and 7–9 in-progress; preserve its edits).

## Env / bootstrap

- No `.env` files in the main checkout — nothing symlinked.
- `_bmad` project config was copied into the worktree.

## Verify

`make test` and `make lint` from the worktree. Final message: per-task summary (pin value, files swept with counts, telemetry payload schema before/after), any halt on the BQ queries, PR URL. PR description must carry **"Decisions & rationale"** — including that `gemini-3.6-flash` is a day-0 model chosen by the user, and that `terraform apply` + production env refresh is a post-merge human step.

## Model policy

Unset — pi default model resolution. Applies to any mega-minions you spawn (close them when done).
