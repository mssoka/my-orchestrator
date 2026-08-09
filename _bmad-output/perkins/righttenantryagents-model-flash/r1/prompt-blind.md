You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec, no repo access. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

Reading anything beyond the diff below (repo files, briefings, the worktree, the web) INVALIDATES your lens. Do not use the read tool. Work from the diff bytes alone.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)

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

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "blind",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact diff lines that prove the claim, pasted verbatim from the diff above. Use 'N/A' only when the claim is about something genuinely absent from the diff (e.g. a missing test file). Paraphrased or reconstructed evidence is hallucination — drop the finding instead.>",
  "detail": "<≤40 words>",
  "recommended_fix": "<≤40 words>"
}

Output contract: ONLY the JSON array. No prose, no fencing, no preamble. [] is valid.

ACCURACY MANDATE: no claim you make will be taken at face value. Every finding will be cross-checked against the actual diff before reporting. Findings whose evidence cannot be located in the diff above, or whose claims contradict what the diff actually shows, are DISCARDED silently. Quote the exact diff lines in evidence. Speculation without quoted evidence is dropped. Accuracy > volume — an empty array is an honest answer when nothing is wrong.

--- FILE OUTPUT CONTRACT ---
Write ONLY your JSON array to /Users/moses/code/_bmad-output/perkins/righttenantryagents-model-flash/r1/blind.json
- Use the write tool; create that exact file. The path is given — do not derive it.
- The file must contain ONLY the JSON array — no prose, no markdown fencing, no preamble.
- [] is valid and expected when you find nothing.
- After the file is written, stop. Do not paste the JSON in chat.
