# Lens brief: edge (source value: `edge`)

First read the shared review brief at
`/Users/moses/code/_bmad-output/perkins/righttenantry-ai-reference-calls-research/r1/shared-block.md`
and follow it exactly (inputs, spec, output contract, accuracy mandate).

Your assigned source value is `edge`. Write your findings JSON array to:
`/Users/moses/code/_bmad-output/perkins/righttenantry-ai-reference-calls-research/r1/edge.json`

## Your lens (from the code-review skill)

You are a pure path tracer. Do not comment on whether the code is good or bad — list
only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable
from the diff hunks. Derive edge classes from the changed code itself — no fixed
checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes),
concurrent operations and race conditions, unhandled error paths in new code, external
service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion,
state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that
lack an explicit guard in the diff; discard handled ones silently. No editorializing.

**Calibration for this docs-only PR:** the "changed lines" are prose describing flows
(call orchestration, consent, fallback, handoff schema). Treat each described flow as
the branching logic to trace — e.g. unanswered calls, mid-call hang-ups, declined
consent, wrong numbers, retry exhaustion, schema fields empty/null, concurrent
applications. Report only paths the documents leave genuinely unhandled.
