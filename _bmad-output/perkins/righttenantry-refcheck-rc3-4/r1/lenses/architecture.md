LENS: architecture (source tag: "architecture") — Architecture fit. EXACT OUTPUT PATH: `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r1/lenses/architecture.json`

**FIRST: read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r1/lenses/_shared_header.md` for the output contract, schema, and accuracy mandate.** Then apply your lens below.

## YOUR LENS — Architectural fit

Given the diff and the surrounding codebase (read the existing `handle_resend`/`resend_with_send` shape, the `classify`/`TokenState` matrix, the `dispatch()`/`maybe_send_email()` notification pattern, and `notify_application_scored`):
- Does the new code follow existing patterns? (the exit-route handlers should mirror `handle_resend`'s injectable-seam + guarded-UPDATE + audit + state-page shape)
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns? (`result.gleam` is pure/deterministic; the handler orchestrates; SQL is guarded)
- Will it create technical debt or make future changes harder?
- Does complexity match the problem?

**Single-writer check:** `reference_objection_log` should have exactly ONE writer (`apply_objection`/`insert_objection_evidence`) — grep the codebase for all writers. Is it truly single?

**Deterministic-result separation:** is `result.gleam` pure (no side effects, no LLM, testable in isolation)? Does the handler own the IO (DB/audit/notify) and delegate structuring to the pure module?

**Notification dispatch:** do `notify_reference_completed/declined/objected` follow the `dispatch()` + `maybe_send_email()` + `notification_preference` pattern of `notify_application_scored`?

For each finding, cite the file + the surrounding pattern it violates/follows. `[]` is a fine answer.
