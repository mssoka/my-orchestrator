You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Python 3.12, ADK agents with Pydantic V2 schemas (schemas live in tenant_scorer/schemas/, never inline). snake_case fields everywhere, PascalCase classes, str | None unions. No HttpUrl in Pydantic models (use str). litellm<=1.82.6 pin is security-critical. "No tech debt" policy. Model selection is centralized: tenant_scorer/config.py (env var > DEFAULT_MODEL > hardcoded fallback) + deployment/terraform/variables.tf (prod env-overrides). Tests: uv run pytest (tests/unit + tests/integration).

--- DIFF ---
diff --git a/deployment/README.md b/deployment/README.md
index ee5ab63..e548090 100644
--- a/deployment/README.md
+++ b/deployment/README.md
@@ -89,11 +89,11 @@ Model names and other Cloud Run env vars have defaults in `variables.tf` — ove
 | Variable | Default | What it controls |
 |---|---|---|
 | `default_model` | `gemini-3.6-flash` | Default Gemini model |
-| `consistency_checker_model` | `gemini-3.1-pro-preview` | Consistency checker agent model |
-| `personal_statement_analyzer_model` | `gemini-3.1-pro-preview` | Personal statement analyzer model |
-| `risk_scorer_model` | `gemini-3.1-pro-preview` | Risk scorer agent model |
-| `verification_compliance_judge_model` | `gemini-3.1-pro-preview` | Boundary compliance judge agent model |
-| `final_compliance_reviewer_model` | `gemini-3.1-pro-preview` | Final compliance reviewer agent model |
+| `consistency_checker_model` | `gemini-3.6-flash` | Consistency checker agent model |
+| `personal_statement_analyzer_model` | `gemini-3.6-flash` | Personal statement analyzer model |
+| `risk_scorer_model` | `gemini-3.6-flash` | Risk scorer agent model |
+| `verification_compliance_judge_model` | `gemini-3.6-flash` | Boundary compliance judge agent model |
+| `final_compliance_reviewer_model` | `gemini-3.6-flash` | Final compliance reviewer agent model |
 | `compliance_repair_model` | `gemini-3.6-flash` | Constrained compliance repair agent model |
 
 ### 3. Apply Terraform
diff --git a/deployment/terraform/variables.tf b/deployment/terraform/variables.tf
index 219d46f..86c4fc6 100644
--- a/deployment/terraform/variables.tf
+++ b/deployment/terraform/variables.tf
@@ -85,31 +85,31 @@ variable "default_model" {
 variable "consistency_checker_model" {
   type        = string
   description = "Gemini model for the consistency checker agent."
-  default     = "gemini-3.1-pro-preview"
+  default     = "gemini-3.6-flash"
 }
 
 variable "personal_statement_analyzer_model" {
   type        = string
   description = "Gemini model for the personal statement analyzer agent."
-  default     = "gemini-3.1-pro-preview"
+  default     = "gemini-3.6-flash"
 }
 
 variable "risk_scorer_model" {
   type        = string
   description = "Gemini model for the risk scorer agent."
-  default     = "gemini-3.1-pro-preview"
+  default     = "gemini-3.6-flash"
 }
 
 variable "verification_compliance_judge_model" {
   type        = string
   description = "Gemini model for the verification compliance judge agent."
-  default     = "gemini-3.1-pro-preview"
+  default     = "gemini-3.6-flash"
 }
 
 variable "final_compliance_reviewer_model" {
   type        = string
   description = "Gemini model for the final compliance reviewer agent."
-  default     = "gemini-3.1-pro-preview"
+  default     = "gemini-3.6-flash"
 }
 
 variable "compliance_repair_model" {
diff --git a/tenant_scorer/.env.example b/tenant_scorer/.env.example
index 3107550..8051478 100644
--- a/tenant_scorer/.env.example
+++ b/tenant_scorer/.env.example
@@ -10,12 +10,13 @@ DEFAULT_MODEL=gemini-3.6-flash
 # (defaults to DEFAULT_MODEL when unset; pinned to gemini-3.6-flash in terraform)
 COMPLIANCE_REPAIR_MODEL=gemini-3.6-flash
 
-# Pro model for agents requiring strong reasoning
-CONSISTENCY_CHECKER_MODEL=gemini-3.1-pro-preview
-PERSONAL_STATEMENT_ANALYZER_MODEL=gemini-3.1-pro-preview
-RISK_SCORER_MODEL=gemini-3.1-pro-preview
-VERIFICATION_COMPLIANCE_JUDGE_MODEL=gemini-3.1-pro-preview
-FINAL_COMPLIANCE_REVIEWER_MODEL=gemini-3.1-pro-preview
+# All reasoning agents on gemini-3.6-flash (cost optimization: 3.6 Flash
+# benchmarks higher than 3.1 Pro on intelligence, price, and speed).
+CONSISTENCY_CHECKER_MODEL=gemini-3.6-flash
+PERSONAL_STATEMENT_ANALYZER_MODEL=gemini-3.6-flash
+RISK_SCORER_MODEL=gemini-3.6-flash
+VERIFICATION_COMPLIANCE_JUDGE_MODEL=gemini-3.6-flash
+FINAL_COMPLIANCE_REVIEWER_MODEL=gemini-3.6-flash
 
 # ---------------------------------------------------------------------------
 # Observability — Google Cloud Trace + BigQuery Agent Analytics
diff --git a/tenant_scorer/config.py b/tenant_scorer/config.py
index 2bdf664..af9510f 100644
--- a/tenant_scorer/config.py
+++ b/tenant_scorer/config.py
@@ -69,7 +69,7 @@ def get_agent_llm(agent_name: str) -> Gemini:
 # + entry framing (20 x 64 = 1.28k) approx 55.3k chars, approx 27.6k tokens at a
 # conservative-for-English-prose 2 chars/token. The 56k cap is ~2x that
 # worst case (tokenization variance and thinking-token headroom), is
-# bounded (no unbounded machinery), and sits under gemini-3.5-flash-class
+# bounded (no unbounded machinery), and sits under gemini-3.6-flash-class
 # output limits. Without it, the ≥20-slot flood edge truncates the response
 # mid-JSON → output_schema ValidationError → fail-closed NON-retryable halt
 # on a recoverable violation flood. Residual (accepted, loop-2): a

--- SPEC / CONTEXT ---
Read these spec files BEFORE filing findings (use the read tool — they are part of your input):
- /Users/moses/code/_bmad-output/briefings/perkins-righttenantryagents-model-flash-r1.md  (round briefing — contains a CRITICAL lens-guard: a list of what NOT to flag, with the user-approved rationale. Read it fully.)
- /Users/moses/code/_bmad-output/briefings/righttenantryagents-model-flash.md  (the original job briefing = the spec: mission, acceptance criteria, hard constraints)

Verified code (read-only) lives in the worktree at: /Users/moses/.herdr/worktrees/RightTenantryAgents/perkins-model-flash-r1
Open files there with the read tool to verify claims. Never trust the diff alone.

--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in detail (quote the exact phrase from the spec when possible).

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "acceptance",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

--- FILE OUTPUT CONTRACT ---
Write ONLY your JSON array to /Users/moses/code/_bmad-output/perkins/righttenantryagents-model-flash/r1/acceptance.json
- Use the write tool; create that exact file. The path is given — do not derive it.
- The file must contain ONLY the JSON array — no prose, no markdown fencing, no preamble, no code block markers.
- [] is valid and expected when you find nothing.
- After the file is written, stop. Do not paste the JSON in chat.
