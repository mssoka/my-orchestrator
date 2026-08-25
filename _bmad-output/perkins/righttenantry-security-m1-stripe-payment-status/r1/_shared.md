# Shared context for all lenses except Blind Hunter

You are one review lens in a 7-lens parallel code review of a GitHub pull request (RightTenantry PR #627, "fix(payment): #625 — gate Stripe unlock on payment_status == paid (M-1)", reviewed sha 6054a3d45d44abb630617d49350bce433c20f6c5). You have read-only access to a checkout of the exact reviewed state. NEVER edit, create, or delete any file inside the repository worktree, and never run builds or tests — this is a read-and-reason review. The ONLY file you write is your JSON output at the path given below.

--- INPUTS (read these first) ---
1. The canonical diff under review: `/Users/moses/code/_bmad-output/perkins/righttenantry-security-m1-stripe-payment-status/r1/diff.patch` — review EXACTLY these bytes.
2. The worktree at the reviewed sha (all verification reads happen here): `/Users/moses/.herdr/worktrees/RightTenantry/perkins-security-m1-stripe-payment-status-r1`
3. Project conventions: `/Users/moses/.herdr/worktrees/RightTenantry/perkins-security-m1-stripe-payment-status-r1/AGENTS.md`
4. Spec — original job briefing: `/Users/moses/code/_bmad-output/perkins/righttenantry-security-m1-stripe-payment-status/r1/original-briefing.md`
5. Spec — GitHub issue #625 rendered as markdown (the finding + acceptance criteria): `/Users/moses/code/_bmad-output/perkins/righttenantry-security-m1-stripe-payment-status/r1/issue-625.md`
6. Context — the security audit report that produced the finding (read §M-1 only; §L-4/L-7/L-8/L-9 are SEPARATE scope, issue #626, NOT this PR): `/Users/moses/code/_bmad-output/implementation-artifacts/righttenantry-security-audit/security-audit-report.md`

--- ROUND-SPECIFIC GUARDS (from the review coordinator) ---

The ONE hard blocker class is the payment-truth gate (issue #625's acceptance):

1. **The webhook gate bites:** `checkout.session.completed` with `payment_status != "paid"` (processing / unpaid / missing field) must provably REFUSE the unlock — vacancy stays locked, payment row pending, ack 200, deterministic (no retry-storm), no audit/burst. Verify the fixtures for EACH state (processing, unpaid, missing-status) actually exercise the gate — non-vacuous: the fixture must fail if the gate is removed.
2. **The pending path settles:** the new `checkout.session.async_payment_succeeded` handler must drive the full pending → settle → replay cycle (unlock, completed, audit, notification, burst, idempotency) with NO new SQL (it must reuse the session-keyed completion machinery). Verify the settle test is real (drives the whole cycle, not a stub).
3. **Card-only going forward:** `payment_method_types=[card]` at session creation (Apple Pay / Google Pay / Link remain card-based — the restriction must not break them), and the idempotency tag bump (`consent_v2_promo` → `consent_v3_card_only`) must actually be consumed in the session-create path so Stripe's 24h cache can't replay a pre-deploy async-enabled session.
4. **Fail-closed default:** a MISSING `payment_status` field must decode to pending (fail-closed, not fail-open) — a malformed event must not unlock.

**What NOT to re-litigate (settled rulings — findings here are noise, not signal):**
- The audit findings themselves (the fix IS the audit's §M-1 recommendation — the finding is settled).
- The pending state-machine design choice: ack-200 + claim + async settle IS the sanctioned shape.
- L-4 (metadata cross-check), L-7 (refund/dispute), L-8 (signature rotation), L-9 (amount verification), L-5, L-18 — they are #626 scope by user ruling, OUT of this PR. Flag ONLY if this PR crept into them (scope drift).
- The burst-scoring trigger beyond unlock-gating (it must be unreachable on the pending path, not modified).

--- OUTPUT ---
Write ONE valid JSON array to the exact absolute output path named in your lens brief. Each element must match this schema exactly:

{
  "source": "<the source value assigned to you in your lens brief>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract:
- The output file must contain ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, reply in chat with a one-line summary (finding counts by severity) and stop. The JSON file is the deliverable.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. Accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
