# Lens: Acceptance Auditor (source: `acceptance`)

Read your shared context first: `/Users/moses/code/_bmad-output/perkins/righttenantry-security-m1-stripe-payment-status/r1/_shared.md` — it defines your inputs, the round-specific guards, the output schema, and the accuracy mandate. Your assigned `source` value is `acceptance`. Your output path is: `/Users/moses/code/_bmad-output/perkins/righttenantry-security-m1-stripe-payment-status/r1/acceptance.json`

--- YOUR LENS ---

Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

The spec here is issue #625 (rendered at `issue-625.md`) + the original briefing (`original-briefing.md`). The issue's acceptance, verbatim:
- "Unlock path provably refuses `processing`/`unpaid` completed events (test fixtures for each state)."
- "Pending-payment path leaves the vacancy locked and the payment row in a waiting state, deterministically."
- "No regression on the card-only happy path (existing tests green + new fixture coverage)."
- "Local test suite is the merge ground truth (CI billing-blocked; see ruling 2026-08-16)."

Remediation asked (either or both, prefer both): (1) gate the unlock path on `payment_status == "paid"` — anything else = pending: ack 200, vacancy locked, payment row waiting, deterministic; (2) restrict `payment_method_types` to `["card"]` at session creation.

Also verify each of the four round-guard gate classes (payment-truth gate) in `_shared.md` is actually satisfied by the code + tests — the guard section is coordinator-issued spec for this round. Missing/vacuous coverage of a guard is a finding.

Scope check: the diff should NOT touch L-4 (metadata cross-check), L-7 (refund/dispute handling), L-8 (signature rotation), L-9 (amount verification) — those are issue #626. Flag any creep.
