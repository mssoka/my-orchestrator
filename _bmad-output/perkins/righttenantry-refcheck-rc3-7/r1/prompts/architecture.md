# Lens: ARCHITECTURE (source: `architecture`)

**First:** Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r1/prompts/_preamble.md` in full and internalize the lens-guards.

Architectural fit review. Given the diff and the surrounding codebase (read the worktree):
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

Specifics worth checking in THIS diff (verify against the worktree):
- **Module separation.** The spec mandates: `fraud.gleam` is PURE (owns signal logic, no DB/HTTP); `result.gleam` STRUCTURES answers (embeds pre-built fraud_signals opaquely); callers gather inputs. Verify `fraud.gleam` has no DB/HTTP imports; verify `result.gleam`'s `structure_form_result` no longer owns fraud logic (the stub `form_session_fraud_signals` should be removed).
- **DRY.** `cross_application_reuse`, `opt_nonempty`, `parse_count` appear to be defined in BOTH `form_handler.gleam` AND `trigger.gleam`. Verify the duplication. Is it justified (module boundaries) or should it be extracted to a shared helper (e.g. in `fraud.gleam` or a `contacts` helper)? The RT convention is "extract helpers when logic repeats 2+ places."
- **The synchronous line-type lookup in the trigger path.** Accepted tradeoff (~1s). Evaluate architecturally: is it the right phase (after tx commit — good), and is there a concrete risk worth noting (not the tradeoff itself, which is accepted)?
- **`stamp_creation_fraud` re-stamps ALL the app's live rows** with a wholesale `SET fraud_signals = $2::jsonb`. Architectural concern: a wholesale overwrite that would clobber any key another path stamps later (e.g. RC4.3's `referee_contact_invalid`). Is the trigger truly once-per-app, and is the overwrite vs. merge the right shape? (Note-level is appropriate given RC4.3 is out of scope, but flag the latent risk.)
- **`line_type_to_string` / `line_type_from_string`** in `lookup.gleam` — round-trip pair; is the placement (lookup module) consistent with how the rest of `lookup.gleam` is organized?
- **The result.gleam `StructureContext` field change** (`focus_seconds: Int` → `fraud_signals: json.Json`) — verify all callers updated (sweep.gleam partial-result path, form_handler, result_test). Any missed caller = a finding.

Verify each claim by reading the actual modules.

**Output:** Write ONLY a JSON array to `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r1/architecture.json`, using `source: "architecture"`. Follow the schema, accuracy mandate, and lens-guards from the preamble. Empty array is valid. Stop when written.
