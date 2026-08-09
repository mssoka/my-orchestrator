You are a reviewer on an automated code-review team reviewing a GitHub PR diff. You have read-only access to a checkout of the repository and may verify the diff's claims against the actual codebase with your tools (read, bash).

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/RightTenantry/perkins-csp-posthog-allowlist-r2/AGENTS.md (Gleam/Lustre monorepo). Apply its conventions only insofar as they bear on this diff.

--- DIFF ---
diff --git a/server/src/csp.gleam b/server/src/csp.gleam
index 6b7d1632..3026609c 100644
--- a/server/src/csp.gleam
+++ b/server/src/csp.gleam
@@ -107,6 +107,24 @@ pub fn header_name() -> String {
 ///     since #487; both blocked URLs are relative same-origin) — same junk
 ///     class. No www/apex issue exists: Cloudflare 301-redirects www→apex at
 ///     the edge, so `'self'` always matches same-origin scripts.
+///   - `https://eu.posthog.com` (PostHog cloud UI host): deliberately NOT
+///     allowlisted, even though `ui_host:'https://eu.posthog.com'` is set in
+///     every PostHog init (SPA shell, `/apply` form, content pages). Per
+///     PostHog's PostHogConfig reference, `ui_host` exists only so PostHog-app
+///     *links* point at the cloud UI when `api_host` is a reverse proxy — it is
+///     not a `script-src`/`connect-src` fetch target. All PostHog browser
+///     traffic is same-origin by construction:
+///       - event ingestion → `api_host:'/_ph'`, a Cloudflare Worker proxy,
+///         deliberately same-origin so ad blockers can't kill capture (see
+///         `application/form_view`); covered by `'self'` in connect-src.
+///       - the SDK script and all lazy assets (array.js, recorder.js,
+///         surveys.js, toolbar.js) load from `/_ph_assets` / the asset host
+///         derived from `api_host` — both same-origin; covered by `'self'`
+///         in script-src.
+///     The PostHog Toolbar (the one feature whose auth call would reach
+///     ui_host) is not used in production. The CSP_ENFORCE flip therefore
+///     needs NO eu.posthog.com allowlist — do not re-add one without a real
+///     Report-Only violation to back it.
 pub fn policy(nonce: String) -> String {
   let script_src = case nonce {
     "" -> "script-src 'self' https://connect.facebook.net"
diff --git a/server/test/csp_test.gleam b/server/test/csp_test.gleam
index 95f0ab7a..39d6f491 100644
--- a/server/test/csp_test.gleam
+++ b/server/test/csp_test.gleam
@@ -135,3 +135,20 @@ pub fn policy_allows_enforcement_additions_test() {
     p |> string.contains("*") |> should.be_false
   })
 }
+
+pub fn policy_never_allowlists_posthog_cloud_host_test() {
+  // INVARIANT — see csp.gleam "deliberately NOT allowlisted": https://eu.posthog.com
+  // must stay OUT of every CSP directive. PostHog browser traffic is same-origin
+  // by construction (event ingestion → api_host:'/_ph', a Cloudflare Worker proxy;
+  // the SDK + lazy assets → /_ph_assets / the api_host-derived asset host), and
+  // `ui_host` is links/navigation only — so the CSP_ENFORCE flip needs NO
+  // eu.posthog.com allowlist. Both header variants (report-only AND enforcing)
+  // render this SAME policy/1 output (header_name/0 only selects the header
+  // NAME), so asserting both branches locks both headers. If this fails, a
+  // directive was widened without a real Report-Only violation — re-read the
+  // csp.gleam rationale before "fixing" by allowlisting.
+  let policy = csp.policy("ABC123")
+  let bare_policy = csp.policy("")
+  policy |> string.contains("eu.posthog.com") |> should.be_false
+  bare_policy |> string.contains("eu.posthog.com") |> should.be_false
+}

--- SPEC / CONTEXT ---
Read the review briefing at /Users/moses/code/_bmad-output/briefings/perkins-righttenantry-csp-posthog-allowlist-r2.md — it carries the user ruling (Q3 = no-op: eu.posthog.com is INTENTIONALLY absent from every CSP directive; do not flag its absence) and the round-2 focus (fix-audit of r1 notes + review of the new absence-invariant test). Prior-round findings for context: /Users/moses/code/_bmad-output/perkins/righttenantry-csp-posthog-allowlist/r1/consolidated.json. This is round 2; r1 APPROVED with 0 blockers, notes N1 (absence-test gap — now addressed by this push) and N2 (advisory gate PASS).

--- YOUR LENS ---
Audit the diff against the spec and context docs above (the review briefing + r1 findings). Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

NOTE — the user ruling in the briefing is binding: "eu.posthog.com is intentionally absent from every CSP directive" and "the absence-invariant test asserting it stays absent is CORRECT". Re-litigating that ruling is a false positive, not an acceptance finding.
--- OUTPUT CONTRACT ---
Write ONE valid JSON array to EXACTLY this path using your write tool, then stop and reply "done":
  /Users/moses/code/_bmad-output/perkins/righttenantry-csp-posthog-allowlist/r2/acceptance.json
Do NOT print the JSON to chat. The file must contain ONLY the JSON array (no prose, no markdown fencing).

Schema per element:
{ "source": "acceptance", "severity": "blocker" | "warning" | "note", "category": "<short tag>", "title": "<one-line summary>", "location": "<file:line | file:hunk | N/A>", "evidence": "<the exact lines you READ, pasted verbatim>", "detail": "<why this is a problem, <=40 words>", "recommended_fix": "<the change to apply, <=40 words>" }

Empty array [] is valid and expected when you find nothing. Do not invent findings to fill a quota.

ACCURACY MANDATE — the most important instruction in this prompt:
NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY. Therefore: open the file, read the relevant lines, do not guess from filenames or assume from similar-looking code. The evidence field must contain the EXACT lines you read; a finding without locatable evidence is a hallucination — drop it before it leaves your output. Hedging language ("might", "could", "possibly", "potentially") is a signal you have not verified the issue — either verify and report crisply, or do not report. Prefer fewer, well-grounded findings over many speculative ones. An empty array is a fine and honest answer when nothing is wrong.
