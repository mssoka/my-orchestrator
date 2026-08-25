# Lens: ARCHITECTURE (source: `architecture`)

**First:** Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r2/prompts/_preamble.md` in full and internalize the lens-guards + the fix-audit scope.

Architectural fit review. Given the diff and the surrounding codebase (read the worktree at `5576ccb`):
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

## Fix-audit priority — W1 (the DRY extraction)

- **W1 (DRY — duplicated helpers).** r1: `cross_application_reuse` + `opt_nonempty` + `parse_count` (+ `opt_to_str`) were duplicated across `form_handler.gleam` and `trigger.gleam`. **Verify FIXED and clean:** the new `reference_checks/fraud_inputs.gleam` owns these (+ `parse_int_opt`, `effective_contact`, `other_refs_from_rows`, `from_effective`). Read it. Verify:
  - The extraction is **behavior-preserving** — the moved fn bodies are identical to the r1 inline forms (the r1 consolidated.json quoted them; the diff shows the moves).
  - Both call sites (`trigger.gleam`, `form_handler.gleam`) import `fraud_inputs` and call the shared fns; the duplicate `opt_to_str` is removed from `trigger.gleam`.
  - The module boundary is coherent: `fraud.gleam` stays PURE (no DB/HTTP imports — verify); `fraud_inputs.gleam` owns the small DB+parsing glue (it imports `pog`/`sql` — appropriate for a glue module). No awkward circular dependency, no leak of DB concerns into `fraud.gleam`.
  - The extraction is the RIGHT shape (not over-abstracted): is `fraud_inputs` a sensible module, or does it mix unrelated concerns?

If the extraction is clean and behavior-preserving → FIXED (do NOT re-file). If it introduced a subtle behavior change, a coupling problem, or left a duplicate → file it.

## Delta pass — architecture of the B1 fix + the stamp scoping

- **The B1 fix's design.** `create_eligible_slots` now returns `Created(count:)` from `list.length(created_ids)` and stamps fraud AFTER the tx. The stamp scopes the WRITE to `created_ids` but the reuse COMPUTATION reads the full application set. Is this the right separation? (Computing reuse over all refs but writing only new ones is correct — reuse is about siblings, the write is about the target.) Is there a cleaner shape, or is this the minimal correct fix?
- **Module separation (carry from r1).** `fraud.gleam` PURE (no DB/HTTP); `result.gleam` STRUCTURES answers (embeds pre-built fraud_signals opaquely — the stub `form_session_fraud_signals` removed); callers gather inputs. Verify `fraud.gleam` still has no DB/HTTP imports after the fix; verify `result.gleam::structure_form_result` just embeds `ctx.fraud_signals`.
- **The synchronous line-type lookup in the trigger path** — accepted tradeoff (~1s). After the B1 fix it runs after the tx commit (good). Note a concrete risk only if you verify one.

Verify each claim by reading the actual modules.

**Output:** Write ONLY a JSON array to `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r2/architecture.json`, using `source: "architecture"`. Follow the schema, accuracy mandate, and lens-guards from the preamble. Empty array is valid. Stop when written.
