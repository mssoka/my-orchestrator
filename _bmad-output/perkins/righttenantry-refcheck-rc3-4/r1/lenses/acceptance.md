LENS: acceptance (source tag: "acceptance") — Acceptance Auditor. EXACT OUTPUT PATH: `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r1/lenses/acceptance.json`

**FIRST: read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r1/lenses/_shared_header.md` for the output contract, schema, and accuracy mandate.** Then apply your lens below.

## YOUR LENS — Audit diff vs spec

Read the story spec at `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-4-r1/_bmad-output/implementation-artifacts/spec-rc3-4-form-completion-exit-routes-submit-decline-objection-wrong-person.md` (AC1–AC9 + the "Dev Notes" pinned copy + result-structuring + objection-stickiness sections). Audit the diff against it.

Identify:
- Violations of specific acceptance criteria (AC1–AC9). Reference the AC number + quote the violated phrase.
- Deviations from spec intent (e.g. the thank-you must be IDENTICAL across completion paths §8.6; the GET stop must mutate nothing; objection stickiness AC5).
- Missing implementation of specified behaviour.
- Contradictions between spec constraints and actual code.
- Scope drift — changes not asked for by the spec.

**Pinned-copy checks (AC9 + Dev Notes):** verify zero em-dashes in user-facing copy across `form_copy.gleam`/`form_handler.gleam`/`form_pages.gleam`/`result.gleam`, and the §7.9/§6.5/§10.2 copy strings match the pinned copy (modulo the em-dash ban). Late-completion copy branch on `taken_over_at`.

**Result structuring (AD-9):** `schema_version:"refcall-v1"`, `channel:"form"`, per-slot verification variants, `free_text_signals` verbatim, deterministic `ai_summary` with completeness-derived `confidence`, `compliance` block, `attempts[]`, `outcome`. Confirm NO LLM in the result path.

For each finding, reference the violated AC/constraint in `detail` (quote the exact spec phrase). `[]` is a fine answer.
