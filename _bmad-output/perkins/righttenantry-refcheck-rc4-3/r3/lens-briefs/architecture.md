# LENS: architecture (source tag: `architecture`) — Perkins r3 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r3/lens-briefs/_shared.md` FIRST (shared context, inputs, lens-guards, output contract), then `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r3/lens-briefs/prior-findings.md` (the FIX AUDIT list — you own the architecture-class items: the r2 BLOCKER, r2 W1 (stale-bounce), r2 W2 (session-state clear), r2 N2 (spec drift), r2 N3 (ON CONFLICT predicate duplication), r2 N5 (single-slot edit), r2 N7 (fraud re-stamp)).

Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions (conditional-UPDATE mutation ownership AD-14, capability-token public routes AD-3, audit-on-state-change AD-16, Squirrel SQL, expand-only migrations)?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

**This is round 3 of a re-review: FIRST classify each prior architecture-class finding against the current worktree (fixed = silent; still present/wrong fix = finding with original severity, title prefixed `STILL PRESENT (r2): `). Then hunt NEW issues.**

**Round-specific architecture checks (per the architecture doc + amendments):**

1. **A7 take-over modeling.** `taken_over_at` as a distinct column (NOT a status) — sweep skips taken-over rows (ALL sweep legs — due/claim/advance), status stickiness untouched, late completion still guarded-transitions to `form_completed`. **THE r2 BLOCKER FIX: the failure paths (delivery webhooks + wrong-person) must now respect `taken_over_at` too — a bounce on a landlord-handled row stands down (no correction-loop re-entry, no exhaustion). Is the stand-down modeled at the find/guard layer (one place) or duplicated at every callsite?** The claim: the r2 rework made the failure paths taken_over_at-aware. Verify where, and that the late-completion transition still works.
2. **AD-7 one-cycle + A1 immutability.** Correct stores `corrected_email`/`corrected_phone` — original `contact_*` snapshot never overwritten; `correction_cycles` = 1; re-queues and re-arms the cadence (attempt_count reset + form_token rotation). **The r2 W2 fix: correction must clear `form_opened_at` + `draft_answers` (the previous referee's session state must not survive into the corrected referee's invite).** The `corrected_at` column — is the stale-bounce gate now modeled in SQL as a typed timestamptz comparison (r2 W1)? Is that the right place (one canonical gate vs duplicated call-site logic)?
3. **AD-16 audit.** New audit events for: take-over, correction, substitution (old + new ids), exhaustion → `unreachable`. Written with the canonical tiered audit pattern? Event types in `audit/event_type.gleam`. The audit for the idempotent substitute no-op — must NOT double-write on double-submit. The audit carries old + new row ids.
4. **AD-14 mutation ownership.** Do the actions follow the guarded-update + sticky-terminals discipline? The exhaust path (webhooks + wrong-person) must respect that objection beats everything. The app↔vacancy precheck (`verify_application_in_vacancy.sql`) — still the single canonical gate used by all action endpoints?
5. **§8.2 state rules the API computes (AR-RC13).** Server computes `can_substitute_referee` + `can_take_over`; client renders them. No client-side re-derivation. Verify the hooks flow through the detail payload and every client action affordance is hook-gated.
6. **The substitute idempotency (r2 claimed N-fix).** The r2 N3: the live-slot ON CONFLICT predicate was maintained in THREE SQL files (+ the migration index). Claimed fix: substitute now REUSES the shared idempotent insert (predicate in ONE place; concurrent double-submits resolve). Verify: does `substitute_reference_call.sql` now call the shared insert? Is the predicate actually single-sourced? **The r2 W5/W7 guard rails: identical-trio 400 + empty prefill; history-row re-submit with different details 409.** The r2 N7: fraud stamping only on REAL inserts (not the idempotent no-op).
7. **Module boundaries.** `actions_handler.gleam` — does it reuse `reference_checks/sql.gleam` and the established service pattern? New SQL files (`get_reference_call_by_id.sql`, `mark_awaiting_correction.sql`) where they belong? Is `notification_dispatch.gleam` change in keeping with the module's shape? The exhaustion notification must interpolate the CORRECTED name (post-correction), not the raw snapshot `contact_name` (r1 W2 — verify still holds).
8. **Scope drift.** Anything in the diff not asked for by Story RC4.3?

Verify against the worktree — read the actual files. Quote exact lines in `evidence`.
