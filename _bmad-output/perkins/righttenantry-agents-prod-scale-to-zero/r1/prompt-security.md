You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

You are running headless. The repository at exactly the reviewed state is your current working directory:

/Users/moses/.herdr/worktrees/RightTenantryAgents/perkins-rta-zero-r1

Do not modify any repository file. Your ONLY write is the JSON output file named below. You are lens source: "security".

--- PROJECT CONVENTIONS ---
# CLAUDE.md

## Project: RightTenantryAgents

AI-powered tenant screening pipeline built on Google ADK (Agent Development Kit) with Pydantic V2 schemas.

## Development Commands

```bash
# Run all tests (unit + integration)
uv run pytest

# Run unit tests only
uv run pytest tests/unit/

# Run integration tests only
uv run pytest tests/integration/

# Run load tests (requires locust, not included in default test run)
uv run --extra load locust -f tests/load_test/load_test.py

# Linting
uv run --group lint ruff check .
uv run --group lint ruff format --check .

# Type checking
uv run --group lint ty check
```

## Key Conventions

- **No tech debt.** Fix issues as you find them — do not defer cleanup, leave TODOs, or accumulate broken windows.
- Python 3.12 — use `str | None` union syntax (not `Optional[str]`)
- snake_case for file names, PascalCase for classes
- All Pydantic schemas live in `tenant_scorer/schemas/` — never define inline models elsewhere
- snake_case field names everywhere (Python = JSON = DB columns, no aliasing)
- Do NOT use `HttpUrl` in Pydantic models — use `str` (Pydantic V2 serialization issue)
- `litellm<=1.82.6` constraint is security-critical — do not change dependency pins without approval
- Commit and push after marking a story or epic as done in `sprint-status.yaml`

## Project Structure

```
tenant_scorer/        # Tenant analysis agent package (sole agent — cross_summary removed)
  schemas/            # Pydantic V2 request/response/internal models (v4 contract lives in response.py)
  agent.py            # Root SequentialAgent: doc_extractor → anonymization_loop → 5 verifiers
                      #                       → verification_compliance_judge → risk_scorer
                      #                       → final_compliance_reviewer
  agents/             # 11 LlmAgents (5 verifiers + 2 compliance critics + scorer + extractor + anon loop)
  callbacks/          # state_init, envelope, anonymization_loop, safety, v4_assembly, compliance_enforcement
  tools/              # Deterministic tools — scoring, validation, response_assembly.build_v4
main.py               # FastAPI entry point for Cloud Run (ADK get_fast_api_app)
Dockerfile            # Cloud Run container (Python 3.12 + Playwright)
docs/
  contract-v4-design.md      # v4 wire contract (binding spec)
  adk-author-guide-v4.md     # Authoring rules for v4 prose + compliance
  anonymization-boundary.md  # Why personal_statement_analyzer sits outside the anon boundary
tests/
  unit/               # Unit tests (pure, no external deps) — 986 currently
  integration/        # Integration tests (may need API keys/models)
  load_test/          # Locust load tests (excluded from default pytest run)
```

## Wire Contract

**Current contract is v4** (`schema_version: "v4"`), additive over v3 — every v3 field is unchanged. v4 adds `detailed_insight`, `category_notes`, `verification_summary`, `recommendations`, and optional `category_weights`. Spec: [`docs/contract-v4-design.md`](docs/contract-v4-design.md). Authoring rules including the EU AI Act / Equal Status Acts compliance posture: [`docs/adk-author-guide-v4.md`](docs/adk-author-guide-v4.md).

The pipeline enforces compliance via two LLM critics implementing the canonical ADK Generator-Critic pattern: `verification_compliance_judge` (mid-pipeline, reads all 5 verifier outputs) and `final_compliance_reviewer` (post-assembly, reads `STATE_FINAL_OUTPUT`). On any protected-ground violation, either critic sets `STATE_PIPELINE_ERROR{code: COMPLIANCE_VIOLATION, retryable: True}`.

--- DIFF (canonical bytes — review exactly this) ---
diff --git a/deployment/terraform/vars/production.tfvars b/deployment/terraform/vars/production.tfvars
index 3a925b3..7a145f3 100644
--- a/deployment/terraform/vars/production.tfvars
+++ b/deployment/terraform/vars/production.tfvars
@@ -9,9 +9,14 @@ github_repo = "solarity-services/RightTenantryAgents"
 gleam_backend_service_account = ""
 beacon_service_account        = ""
 
-# Resource sizing — keeps one always-warm instance for Gleam session_create.
+# Resource sizing — pre-revenue cost cut: scale-to-zero (min_instances = 0)
+# with idle-CPU throttling (cpu_idle = true → request-based billing). Gleam
+# retries (3 attempts, 2/8/32s backoff, ~42s runway) absorb the cold-start
+# blips this can reintroduce (see variables.tf 2026-05-04 history and
+# staging's identical move). Tripwire: flip back to min_instances = 1 /
+# cpu_idle = false at the first paying customer or sustained load testing.
 cpu           = "2"
 memory        = "4Gi"
-cpu_idle      = false
-min_instances = 1
+cpu_idle      = true
+min_instances = 0
 max_instances = 20

--- SPEC / CONTEXT ---
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

--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

--- OUTPUT ---
Write ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "security",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Write ONLY the JSON array to this exact absolute file path (do not derive or invent a different path):
/Users/moses/code/_bmad-output/perkins/righttenantry-agents-prod-scale-to-zero/r1/security.json

Output contract:
- Write ONLY the JSON array to that file. No prose, no markdown fencing, no preamble in the file.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, stop. Your task is complete.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
