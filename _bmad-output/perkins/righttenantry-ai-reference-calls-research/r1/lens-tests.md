# Lens brief: test coverage / evidence traceability (source value: `tests`)

First read the shared review brief at
`/Users/moses/code/_bmad-output/perkins/righttenantry-ai-reference-calls-research/r1/shared-block.md`
and follow it exactly (inputs, spec, output contract, accuracy mandate).

Your assigned source value is `tests`. Write your findings JSON array to:
`/Users/moses/code/_bmad-output/perkins/righttenantry-ai-reference-calls-research/r1/tests.json`

## Your lens (from the code-review skill, calibrated for a research deliverable)

This PR is documentation-only; there are no behavioural code changes and no test suite
to trace against. Apply the skill's traceability method to the research deliverable
instead: the "behaviours" are the claims and recommendations in the main report; the
"tests" are the citations and evidence supporting them.

For each load-bearing claim in the main report
(`_bmad-output/planning-artifacts/research/domain-ai-voice-reference-checking-tenant-screening-research-2026-07-21.md`),
trace to its support and classify as FULL / PARTIAL / NONE:
- FULL — claim carries a specific, checkable citation (URL, statute section, official
  guidance) or quotes verifiable data, in the diff itself.
- PARTIAL — supported only by a supporting thread doc's unsourced assertion, or a
  vague attribution ("providers typically…", "reports indicate…").
- NONE — no source at all.

Prioritise P0 claims: the resume/shelve recommendation, the provider pick (incl. the
"Trilu" identification), the GDPR/ePrivacy legal-basis conclusions, and cost-per-call
figures. Emit one finding per gap with severity:
- blocker: a P0 claim with NONE support, or a citation that does not support the claim
- warning: a P0 claim with PARTIAL support, or a cluster of PARTIAL secondary claims
- note: minor unsupported asides

Blind-spot heuristics: citation URLs that look fabricated or non-resolvable; numbers
without a named source; legal conclusions with no statute/guidance anchor; claims
contradicted by their own cited source.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory evidence gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with support percentages across the claims you traced
- recommended_fix: what would raise the gate

Gate thresholds:
- PASS: P0 100% FULL, overall ≥80% FULL-or-better
- CONCERNS: P0 100% supported but some only PARTIAL, overall ≥80%
- FAIL: any P0 claim NONE/unsupported, or overall <80%

Verify citations by quoting the exact lines; where a URL is cited you may check its
plausibility but mark verification status in evidence (quote the diff line containing
the citation). Do not emit findings you cannot anchor to quoted lines.
